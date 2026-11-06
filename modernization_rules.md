---
description: Activate when modernizing legacy code, migrating frameworks, writing implementation plans, managing changelogs, updating AGENTS.md, or auditing staged commits.
trigger: model_decision
---

# Universal AI Guidelines for Project Modernization & Migration

## 1. Comment & Reference Preservation
- **Preserve Knowledge & References:** Never delete comments containing documentation links, StackOverflow URLs, tutorial citations, or domain context.
- **Annotate Legacy Changes:** When updating deprecated syntax, add explanatory annotations contrasting old vs new syntax rather than stripping rationale.
- **Maintain Developer Checklists:** Preserve developer notes and checklist files (e.g., `NOTES.txt`).

---

## 2. Unified Changelog & Campaign State Protocol
- **Campaign State Separation:** In-flight refactoring campaign state lives in `<workspace>/.refactor/state.json` and `.refactor/plan.md`. Permanent architectural topology lives in `<workspace>/AGENTS.md` (< 40 lines, updated in-place).
- **Zero-Token Milestone Logging:** Never call `read_file` or `edit_file` on changelog files, and never hardcode legacy log paths. Record milestone completions exclusively via the unified CLI:
  ```bash
  python skills/system-diagnostics/scripts/diagnose.py changelog add --title "<Title>" --type <type> --summary "<Summary>" --verify "<Command (Result)>"
  ```
- **Single-Generation Echo Protocol:** `diagnose.py changelog add` automatically rotates older entries (keeping active log <= 150 lines), archives historical overflow into `.changelogs/`, and prints a copy-pasteable `git commit` snippet. Re-use this printed snippet directly—never spend output tokens regenerating redundant commit prose in chat.

---

## 3. Milestone-by-Milestone Workflow & Sanitized Plans
- **Incremental Steps:** Break work into logical, cohesive milestones. Avoid sprawling, unbounded edits.
- **Portable & Sanitized Plan Artifacts:** Plans, logs, and roadmaps must remain fully portable:
  - **POSIX Paths & No Local Paths:** Always use repo-relative forward-slash POSIX paths (`src/module/file.py#L10-L20`); NEVER embed `file:///` URIs, drive letters (`C:`), or user paths (`/home/`, `Users/`).
  - **OS-Agnostic Verification:** Use cross-platform commands (`pytest`, `python -m unittest discover tests`); never reference OS-locked virtualenvs (`.venv/Scripts`) or personal directories (`~/.gemini/`).
  - **Infrastructure Parameterization:** Use environment placeholders (`$APP_URL`) rather than hardcoded local hosts/ports.
- **Pre-Commit Staging Audit Gate & Zero Unprompted Staging:**
  - **Zero Unprompted Staging:** Never execute `git add` or `git rm` during refactoring or coding unless explicitly asked. Delete files via filesystem (`os.remove` / `Remove-Item`) so all diffs remain unstaged for user review.
  - Before suggesting `git add` / `git commit`, audit working tree and staged files:
    1. Zero `file:///` URLs or local machine absolute paths.
    2. Zero OS-specific virtual environment binary paths.
    3. Zero hardcoded local infrastructure URLs/ports.
    4. Code-Doc Sync: If CLI flags, options, or workflows changed, verify corresponding `README.md` or `docs/` updates are staged.
    5. Compliance with modularity budgets and executable verification commands.
- **Validation & Commit Review:** Run automated checks before closing milestones, provide copy-pasteable manual verification steps, and offer concise commit suggestions.

---

## 4. Global vs. Local Rule Separation (`AGENTS.md` Delta Contract)
- **Zero Global Duplication:** Never copy global rules (`~/.gemini/config/rules/`) into a workspace's `AGENTS.md` or `.agents/rules/`. Path deduplication does not deduplicate repeated text across global and local files.
- **Delta-Only Local `AGENTS.md` (`< 40` lines / `< 500` tokens):** Restrict workspace `AGENTS.md` files strictly to repository-specific deltas:
  1. Exact OS-agnostic test, build, and lint commands (`pytest`, `flutter test`, `$APP_URL`).
  2. Directory ownership map (`src/routers/`, `src/services/`, `src/repositories/`).
  3. Explicit project-level overrides where local domain rules intentionally supersede a global default.
