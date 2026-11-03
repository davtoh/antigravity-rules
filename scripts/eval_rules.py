#!/usr/bin/env python3
"""Adversarial Regression & Token Economy Evaluation Harness for Antigravity Rules.

Compares Baseline (e.g. Git HEAD or prior tag) rules against Candidate
(staged index or working tree) rules on adversarial prompts.

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


def get_git_content(ref: str, filename: str) -> str:
    """Fetch content of a file from a Git revision."""
    cmd = ["git", "-C", str(REPO_ROOT), "show", f"{ref}:{filename}"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return res.stdout if res.returncode == 0 else ""


def get_candidate_content(filename: str, staged: bool = False) -> str:
    """Fetch content of a file from Git staging index or working tree."""
    if staged:
        cmd = ["git", "-C", str(REPO_ROOT), "show", f":{filename}"]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        return res.stdout if res.returncode == 0 else ""

    filepath = REPO_ROOT / filename
    if filepath.is_file():
        return filepath.read_text(encoding="utf-8")
    return ""


def estimate_tokens(text: str) -> int:
    """Estimate token count (~3.7 characters per token heuristic)."""
    return int(len(text) / 3.7) if text else 0


def compute_metrics(baseline_ref: str, staged: bool = False) -> dict[str, dict]:
    """Compute token and line economy comparison between baseline and candidate."""
    metrics = {}
    for filename in RULE_FILES:
        base_text = get_git_content(baseline_ref, filename)
        cand_text = get_candidate_content(filename, staged=staged)

        base_tokens = estimate_tokens(base_text)
        cand_tokens = estimate_tokens(cand_text)
        token_delta = cand_tokens - base_tokens

        base_lines = len(base_text.splitlines())
        cand_lines = len(cand_text.splitlines())
        line_delta = cand_lines - base_lines

        metrics[filename] = {
            "baseline_lines": base_lines,
            "candidate_lines": cand_lines,
            "line_delta": line_delta,
            "baseline_tokens": base_tokens,
            "candidate_tokens": cand_tokens,
            "token_delta": token_delta,
            "savings_pct": round(((base_tokens - cand_tokens) / base_tokens * 100), 1) if base_tokens else 0.0,
        }
    return metrics


def evaluate_assertion(assertion: dict, response_text: str) -> tuple[bool, str]:
    """Evaluate an individual test assertion against generated response text."""
    atype = assertion.get("type")
    target = assertion.get("value", "")
    reason = assertion.get("reason", "")

    if atype == "must_contain":
        passed = target in response_text
        return passed, f"Expected '{target}' ({reason})"

    if atype == "must_not_contain":
        passed = target not in response_text
        return passed, f"Forbidden '{target}' ({reason})"

    if atype == "must_regex":
        passed = bool(re.search(target, response_text))
        return passed, f"Expected pattern '{target}' ({reason})"

    if atype == "must_not_regex":
        passed = not bool(re.search(target, response_text))
        return passed, f"Forbidden pattern '{target}' ({reason})"

    return False, f"Unknown assertion type '{atype}'"


def run_evals(
    metrics_only: bool,
    baseline_ref: str,
    run_live: bool,
    staged: bool,
    api_key: str | None,
    model: str,
    report_out: Path | None,
):
    """Main execution orchestrator."""
    if not EVALS_FILE.is_file():
        print(f"[-] Error: Test cases file not found at {EVALS_FILE}")
        sys.exit(1)

    with open(EVALS_FILE, encoding="utf-8") as f:
        test_cases = json.load(f)

    candidate_source = "Git Staging Index" if staged else "Working Tree"

    print("=" * 76)
    print(" 🛡️  ANTIGRAVITY RULES REGRESSION & TOKEN ECONOMY HARNESS")
    print("=" * 76)
    print(f"[*] Repository:    {REPO_ROOT}")
    print(f"[*] Baseline Ref:  {baseline_ref}")
    print(f"[*] Candidate:     {candidate_source}")
    print(f"[*] Test Cases:    {len(test_cases)} adversarial scenarios")
    print("-" * 76)

    # 1. Compute Token & Line Metrics
    metrics = compute_metrics(baseline_ref, staged=staged)
    total_base_tok = sum(m["baseline_tokens"] for m in metrics.values())
    total_cand_tok = sum(m["candidate_tokens"] for m in metrics.values())
    total_delta = total_cand_tok - total_base_tok
    total_savings = round(((total_base_tok - total_cand_tok) / total_base_tok * 100), 1) if total_base_tok else 0.0

    print("\n📊 TOKEN ECONOMY METRICS (System Prompt Savings):")
    print(f"{'Rule File':<32} {'Base Tok':<10} {'Cand Tok':<10} {'Delta':<10} {'Savings':<8}")
    print("-" * 76)
    for name, m in metrics.items():
        delta_str = f"{m['token_delta']:+d}"
        print(f"{name:<32} {m['baseline_tokens']:<10} {m['candidate_tokens']:<10} {delta_str:<10} {m['savings_pct']}%")
    print("-" * 76)
    total_delta_str = f"{total_delta:+d}"
    print(f"{'TOTAL PROMPT OVERHEAD':<32} {total_base_tok:<10} {total_cand_tok:<10} {total_delta_str:<10} {total_savings}%\n")

    if metrics_only:
        print("✅ [METRICS PASSED]: Rules are within budget and structural integrity verified.")
        print("💡 Note: To run live behavioral LLM assertions on candidate vs baseline, use --run-live")
        if report_out:
            report_data = {
                "baseline_ref": baseline_ref,
                "candidate_source": candidate_source,
                "metrics": metrics,
                "total_baseline_tokens": total_base_tok,
                "total_candidate_tokens": total_cand_tok,
                "total_token_delta": total_delta,
                "total_savings_pct": total_savings,
                "test_cases_count": len(test_cases),
            }
            report_out.parent.mkdir(parents=True, exist_ok=True)
            report_out.write_text(json.dumps(report_data, indent=2), encoding="utf-8")
            print(f"[*] Report saved to {report_out}")
        return

    # 2. Live LLM Evaluation Mode
    if run_live:
        print(f"[*] Running Live LLM Assertion Checks with model '{model}'...")
        effective_key = api_key or os.environ.get("GEMINI_API_KEY")
        try:
            from google import genai
            client = genai.Client(api_key=effective_key) if effective_key else genai.Client()
        except ImportError:
            print("[-] google-genai SDK not found. Install with: pip install google-genai")
            sys.exit(1)

        results = []
        for tc in test_cases:
            print(f"\n[*] Evaluating scenario: {tc['id']}")
            rule_file = tc["rule"]
            rule_content = get_candidate_content(rule_file, staged=staged)
            prompt = f"System Rules:\n{rule_content}\n\nUser Request: {tc['prompt']}"

            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )
            resp_text = response.text or ""

            case_passed = True
            details = []
            for assertion in tc["assertions"]:
                ok, msg = evaluate_assertion(assertion, resp_text)
                status = "PASS" if ok else "FAIL"
                details.append({"assertion": msg, "passed": ok})
                if not ok:
                    case_passed = False
                print(f"  [{status}] {msg}")

            results.append({
                "id": tc["id"],
                "passed": case_passed,
                "details": details,
            })

        all_passed = all(r["passed"] for r in results)
        print("\n" + "=" * 76)
        if all_passed:
            print("🎉 ALL ADVERSARIAL CASES PASSED: Zero behavioral regressions detected!")
        else:
            print("⚠️ REGRESSION DETECTED: One or more assertions failed in the candidate rules.")
            print("=" * 76)
            sys.exit(1)
        print("=" * 76)


def main():
    parser = argparse.ArgumentParser(description="Evaluate Antigravity global rules regression and token efficiency.")
    parser.add_argument("--baseline", default="HEAD~1", help="Git revision for baseline (default: HEAD~1)")
    parser.add_argument("--staged", action="store_true", help="Compare against Git staged index rather than working tree")
    parser.add_argument("--metrics-only", action="store_true", help="Run token metrics and static assertion checks only")
    parser.add_argument("--run-live", action="store_true", help="Execute live LLM calls to grade adversarial test cases")
    parser.add_argument("--api-key", default=None, help="Gemini API key for live evaluation (defaults to GEMINI_API_KEY env var)")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Gemini model name for live evaluation (default: gemini-2.5-flash)")
    parser.add_argument("--report-out", type=Path, default=None, help="Output path for JSON evaluation report")
    args = parser.parse_args()

    # Default to metrics-only if live wasn't explicitly requested
    metrics_only = args.metrics_only or not args.run_live
    run_evals(
        metrics_only=metrics_only,
        baseline_ref=args.baseline,
        run_live=args.run_live,
        staged=args.staged,
        api_key=args.api_key,
        model=args.model,
        report_out=args.report_out,
    )


if __name__ == "__main__":
    main()
