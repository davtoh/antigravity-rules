# 🛡️ Antigravity Global Rules

Global engineering standards, security baselines, and progressive-disclosure architectural constraints enforced across workspaces in [Google Antigravity](https://antigravity.google).

---

## 📋 Catalog & Progressive Disclosure Matrix

Only `always_on` rules are injected unconditionally every turn. Rules using `glob` or `model_decision` inject only a lightweight ~50-token descriptor until a matching file or task activates them—cutting baseline per-turn overhead by **74.9%** (`6,212` → `1,560` tokens).

| Rule File | Trigger Mode | Activation Condition | Idle Cost / Turn | Active Cost | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [**`security_and_standards.md`**](../security_and_standards.md) | `always_on` | Unconditional | ~1,396 tok | ~1,396 tok | OWASP Top 10, 12-factor zero hardcoded infrastructure, 350/500-line modularity budgets, resource safety, and CSS layout discipline. |
| [**`python_decrufting.md`**](../python_decrufting.md) | `glob` (`**/*.py`) | Any `.py` file open or edited | ~54 tok | ~564 tok | Enforces Python 3.10–3.15+ idioms, prohibits all `__future__` imports and `six`/`past` shims, and preserves domain math. |
| [**`executable_documentation.md`**](../executable_documentation.md) | `model_decision` | Writing/updating `README.md`, `SETUP_GUIDE.md`, `docs/`, or adding new CLI features | ~59 tok | ~547 tok | Enforces code-doc synchronization, pre-run diagnostic one-liners, runnable CLI recipes, and Scenario Combinations Matrices. |
| [**`modernization_rules.md`**](../modernization_rules.md) | `model_decision` | Modernizing code, `MIGRATION_LOG.md`, `AGENTS.md`, plans, or commits | ~50 tok | ~977 tok | Milestone workflows, comment preservation, portable plans, pre-commit audit gates, and Delta-Only local `AGENTS.md`. |
| **Total Overhead** | **Dual-Budget Gate** | **Idle Turn vs. All-Triggered** | **~1,559 tok** ($\le 1,600$) | **~3,484 tok** ($\le 3,500$) | Verified automatically via `tests/test_rules.py` and `scripts/eval_rules.py`. |

---

## ⚡ Pre-Run Verification One-Liners

Run these two cross-platform commands from the repository root before committing rule changes:

```bash
# 1. Run static structural, frontmatter, path-hygiene, and dual-budget unit tests (9 checks in ~5ms)
python -m unittest discover -s tests -v

# 2. Run token economy evaluation harness against historical baseline
python scripts/eval_rules.py --metrics-only
```

---

## 🎯 Scenario Combinations Matrix

| Scenario / Objective | Mode / Inputs | Key Parameters | Exact Runnable Command |
| :--- | :--- | :--- | :--- |
| **Fast Unit & Contract Check** | Static test suite | `-s tests -v` | `python -m unittest discover -s tests -v` |
| **Working Tree Token Audit** | Working tree vs `fcd0009` | `--metrics-only` | `python scripts/eval_rules.py --metrics-only` |
| **Pre-Commit Staged Audit** | Git staged index vs `HEAD` | `--metrics-only --staged --baseline HEAD` | `python scripts/eval_rules.py --metrics-only --staged --baseline HEAD` |
| **Export JSON Metrics Report** | Working tree + JSON output | `--metrics-only --report-out evals/report.json` | `python scripts/eval_rules.py --metrics-only --report-out evals/report.json` |
| **Live Adversarial LLM Eval** | Gemini API behavioral check | `--run-live --model gemini-2.5-flash` | `python scripts/eval_rules.py --run-live --model gemini-2.5-flash` |

---

## 🧩 Global vs. Local Rule Separation (`AGENTS.md` Delta Contract)

Because Antigravity deduplicates rules by file path rather than text similarity, **never copy global rules from `~/.gemini/config/rules/` into a project's `<workspace>/AGENTS.md`**. Keep local `<workspace>/AGENTS.md` files strictly under **40 lines / 500 tokens** containing only project-specific deltas:

```markdown
# Project Delta Rules (AGENTS.md)

## 1. Build, Test & Verification Commands
- Unit Tests: `pytest tests/ -v`
- Lint & Typecheck: `ruff check . && mypy src/`
- Live UI Audit: `python scripts/cdp_inspect.py --url $APP_URL --audit-layout`

## 2. Directory Ownership Map
- `src/routers/` — Thin HTTP route handlers (<= 25 lines; validate -> call service -> return).
- `src/services/` — Pure domain orchestration and business logic.
- `src/repositories/` — Parameterized data access and external I/O.

## 3. Project-Specific Overrides
- Target Python runtime: `3.12+` (strictly no `__future__` imports).
```

---

## 🔄 Installation & Machine Sync

To install these rules globally on a new machine:

```powershell
# Windows PowerShell
git clone https://github.com/davtoh/antigravity-rules.git "$HOME\.gemini\config\rules"
```

```bash
# macOS / Linux (bash/zsh)
git clone https://github.com/davtoh/antigravity-rules.git "${HOME}/.gemini/config/rules"
```

---

## 📄 License
MIT License. Created by [davtoh](https://github.com/davtoh).
