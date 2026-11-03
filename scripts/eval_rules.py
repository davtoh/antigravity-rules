#!/usr/bin/env python3
"""Adversarial Regression & Token Economy Evaluation Harness for Antigravity Rules.

Compares Baseline (e.g. fcd0009 or HEAD~1) rules against Candidate
(staged index or working tree) rules on Always-On vs. Active token budgets
and adversarial behavioral prompts.

Usage:
    # 1. Quick token economy & static assertion validation on working tree:
    python scripts/eval_rules.py --metrics-only

    # 2. Inspect staged files specifically (ideal for pre-commit):
    python scripts/eval_rules.py --metrics-only --staged

    # 3. Live behavioral evaluation using Gemini API:
    python scripts/eval_rules.py --run-live --model gemini-2.5-flash

    # 4. Save report to JSON:
    python scripts/eval_rules.py --metrics-only --report-out evals/report.json
"""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
EVALS_FILE = REPO_ROOT / "evals" / "test_cases.json"
RULE_FILES = [
    "executable_documentation.md",
    "modernization_rules.md",
    "python_decrufting.md",
    "security_and_standards.md",
]
MAX_ALWAYS_ON_TOKENS = 1600
MAX_ALL_ACTIVE_TOKENS = 3500
FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def resolve_default_baseline() -> str:
    """Resolve pre-compression baseline commit (fcd0009) if present, else HEAD~1."""
    cmd = ["git", "-C", str(REPO_ROOT), "rev-parse", "--verify", "--quiet", "fcd0009^{commit}"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return "fcd0009" if res.returncode == 0 else "HEAD~1"


def get_git_content(ref: str, filename: str) -> str:
    """Fetch content of a file from a Git revision."""
    cmd = ["git", "-C", str(REPO_ROOT), "show", f"{ref}:{filename}"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return res.stdout if res.returncode == 0 else ""


def get_candidate_content(filename: str, staged: bool = False) -> str:
    """Fetch content of a file from Git staging index or working tree."""
    if staged:
        return get_git_content("", filename)
    filepath = REPO_ROOT / filename
    return filepath.read_text(encoding="utf-8") if filepath.is_file() else ""


def estimate_tokens(text: str) -> int:
    """Estimate token count (~3.7 characters per token heuristic)."""
    return int(len(text) / 3.7) if text else 0


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parse YAML frontmatter key-value pairs from a rule markdown string."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            fields[key.strip()] = val.strip().strip('"').strip("'")
    return fields


def compute_rule_token_profile(text: str) -> tuple[str, int, int]:
    """Return (trigger, always_on_turn_tokens, active_full_tokens) for a rule."""
    full_tokens = estimate_tokens(text)
    fields = parse_frontmatter(text)
    trigger = fields.get("trigger", "always_on")
    if trigger == "always_on":
        return trigger, full_tokens, full_tokens
    desc_tokens = estimate_tokens(fields.get("description", "")) + 8
    return trigger, desc_tokens, full_tokens


def compute_metrics(baseline_ref: str, staged: bool = False) -> dict[str, dict]:
    """Compute token, trigger, and line metrics between baseline and candidate."""
    metrics: dict[str, dict] = {}
    for filename in RULE_FILES:
        base_text = get_git_content(baseline_ref, filename)
        cand_text = get_candidate_content(filename, staged=staged)
        _, base_always_tok, base_active_tok = compute_rule_token_profile(base_text)
        cand_trigger, cand_always_tok, cand_active_tok = compute_rule_token_profile(cand_text)

        metrics[filename] = {
            "trigger": cand_trigger,
            "baseline_lines": len(base_text.splitlines()),
            "candidate_lines": len(cand_text.splitlines()),
            "line_delta": len(cand_text.splitlines()) - len(base_text.splitlines()),
            "baseline_tokens": base_active_tok,
            "candidate_always_on_tokens": cand_always_tok,
            "candidate_active_tokens": cand_active_tok,
            "always_on_delta": cand_always_tok - base_always_tok,
            "active_token_delta": cand_active_tok - base_active_tok,
            "always_on_savings_pct": round(((base_always_tok - cand_always_tok) / base_always_tok * 100), 1)
            if base_always_tok else 0.0,
            "active_savings_pct": round(((base_active_tok - cand_active_tok) / base_active_tok * 100), 1)
            if base_active_tok else 0.0,
        }
    return metrics


def summarize_and_print_metrics(metrics: dict[str, dict], baseline_ref: str, candidate_source: str) -> dict:
    """Print dual-budget table and return summary dictionary."""
    base_tok = sum(m["baseline_tokens"] for m in metrics.values())
    always_tok = sum(m["candidate_always_on_tokens"] for m in metrics.values())
    active_tok = sum(m["candidate_active_tokens"] for m in metrics.values())
    always_sav = round(((base_tok - always_tok) / base_tok * 100), 1) if base_tok else 0.0
    active_sav = round(((base_tok - active_tok) / base_tok * 100), 1) if base_tok else 0.0

    print("\n📊 TOKEN ECONOMY METRICS (Progressive Disclosure Dual-Budget):")
    print(f"{'Rule File':<28} {'Trigger':<15} {'Base':<7} {'Idle/Turn':<10} {'Active':<8} {'Idle Sav':<8}")
    print("-" * 82)
    for name, m in metrics.items():
        print(
            f"{name:<28} {m['trigger']:<15} {m['baseline_tokens']:<7} "
            f"{m['candidate_always_on_tokens']:<10} {m['candidate_active_tokens']:<8} {m['always_on_savings_pct']}%"
        )
    print("-" * 82)
    print(f"{'ALWAYS-ON BASELINE / TURN':<44} {base_tok:<7} {always_tok:<10} {'-':<8} {always_sav}% (Budget <= {MAX_ALWAYS_ON_TOKENS})")
    print(f"{'WORST-CASE ALL-TRIGGERED':<44} {base_tok:<7} {'-':<10} {active_tok:<8} {active_sav}% (Budget <= {MAX_ALL_ACTIVE_TOKENS})\n")
    return {
        "baseline_ref": baseline_ref,
        "candidate_source": candidate_source,
        "metrics": metrics,
        "total_baseline_tokens": base_tok,
        "total_always_on_tokens": always_tok,
        "total_candidate_tokens": active_tok,
        "always_on_savings_pct": always_sav,
        "total_savings_pct": active_sav,
    }


def verify_budget_gates(summary: dict) -> None:
    """Assert dual-tier token ceilings and exit non-zero on violation."""
    always_tok = summary["total_always_on_tokens"]
    active_tok = summary["total_candidate_tokens"]
    if always_tok > MAX_ALWAYS_ON_TOKENS or active_tok > MAX_ALL_ACTIVE_TOKENS:
        print(
            f"[-] BUDGET GATE FAILED: Always-On={always_tok}/{MAX_ALWAYS_ON_TOKENS}, "
            f"All-Active={active_tok}/{MAX_ALL_ACTIVE_TOKENS}"
        )
        sys.exit(1)
    print("✅ [METRICS PASSED]: Always-On and All-Active budgets verified within hard ceilings.")


def evaluate_assertion(assertion: dict, response_text: str) -> tuple[bool, str]:
    """Evaluate an individual test assertion against generated response text."""
    atype = assertion.get("type")
    target = assertion.get("value", "")
    reason = assertion.get("reason", "")
    checks = {
        "must_contain": (target in response_text, f"Expected '{target}' ({reason})"),
        "must_not_contain": (target not in response_text, f"Forbidden '{target}' ({reason})"),
        "must_regex": (bool(re.search(target, response_text)), f"Expected pattern '{target}' ({reason})"),
        "must_not_regex": (not bool(re.search(target, response_text)), f"Forbidden pattern '{target}' ({reason})"),
    }
    return checks.get(atype, (False, f"Unknown assertion type '{atype}'"))


def run_live_scenarios(test_cases: list[dict], staged: bool, api_key: str | None, model: str) -> None:
    """Execute live LLM calls to grade adversarial test cases."""
    print(f"[*] Running Live LLM Assertion Checks with model '{model}'...")
    effective_key = api_key or os.environ.get("GEMINI_API_KEY")
    try:
        from google import genai
        client = genai.Client(api_key=effective_key) if effective_key else genai.Client()
    except ImportError:
        print("[-] google-genai SDK not found. Install with: pip install google-genai")
        sys.exit(1)

    all_passed = True
    for tc in test_cases:
        print(f"\n[*] Evaluating scenario: {tc['id']}")
        rule_content = get_candidate_content(tc["rule"], staged=staged)
        prompt = f"System Rules:\n{rule_content}\n\nUser Request: {tc['prompt']}"
        resp_text = client.models.generate_content(model=model, contents=prompt).text or ""
        for assertion in tc["assertions"]:
            ok, msg = evaluate_assertion(assertion, resp_text)
            all_passed = all_passed and ok
            print(f"  [{'PASS' if ok else 'FAIL'}] {msg}")

    if not all_passed:
        print("\n⚠️ REGRESSION DETECTED: One or more assertions failed.")
        sys.exit(1)
    print("\n🎉 ALL ADVERSARIAL CASES PASSED: Zero behavioral regressions detected!")


def run_evals(
    metrics_only: bool,
    baseline_ref: str,
    run_live: bool,
    staged: bool,
    api_key: str | None,
    model: str,
    report_out: Path | None,
) -> None:
    """Orchestrate static token metrics and optional live LLM scenario evaluation."""
    if not EVALS_FILE.is_file():
        print(f"[-] Error: Test cases file not found at {EVALS_FILE}")
        sys.exit(1)

    test_cases = json.loads(EVALS_FILE.read_text(encoding="utf-8"))
    candidate_source = "Git Staging Index" if staged else "Working Tree"
    print("=" * 82)
    print(" 🛡️  ANTIGRAVITY RULES REGRESSION & TOKEN ECONOMY HARNESS")
    print("=" * 82)
    print(f"[*] Baseline Ref: {baseline_ref} | Candidate: {candidate_source} | Scenarios: {len(test_cases)}")

    metrics = compute_metrics(baseline_ref, staged=staged)
    summary = summarize_and_print_metrics(metrics, baseline_ref, candidate_source)
    summary["test_cases_count"] = len(test_cases)
    verify_budget_gates(summary)

    if report_out:
        report_out.parent.mkdir(parents=True, exist_ok=True)
        report_out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"[*] Report saved to {report_out}")

    if not metrics_only and run_live:
        run_live_scenarios(test_cases, staged=staged, api_key=api_key, model=model)


def main() -> None:
    """Parse CLI arguments and invoke evaluation orchestrator."""
    parser = argparse.ArgumentParser(description="Evaluate Antigravity global rules regression and token efficiency.")
    parser.add_argument("--baseline", default=None, help="Git revision for baseline (auto-detects fcd0009 or HEAD~1)")
    parser.add_argument("--staged", action="store_true", help="Compare against Git staged index rather than working tree")
    parser.add_argument("--metrics-only", action="store_true", help="Run token metrics and static budget gates only")
    parser.add_argument("--run-live", action="store_true", help="Execute live LLM calls to grade adversarial test cases")
    parser.add_argument("--api-key", default=None, help="Gemini API key for live evaluation (defaults to GEMINI_API_KEY)")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Gemini model name (default: gemini-2.5-flash)")
    parser.add_argument("--report-out", type=Path, default=None, help="Output path for JSON evaluation report")
    args = parser.parse_args()

    baseline_ref = args.baseline or resolve_default_baseline()
    metrics_only = args.metrics_only or not args.run_live
    run_evals(metrics_only, baseline_ref, args.run_live, args.staged, args.api_key, args.model, args.report_out)


if __name__ == "__main__":
    main()
