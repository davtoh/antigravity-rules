---
description: Activate when modernizing legacy code, migrating frameworks, writing implementation plans, updating MIGRATION_LOG.md or AGENTS.md, or auditing staged commits.
trigger: model_decision
---

# Universal AI Guidelines for Project Modernization & Migration

## 1. Comment & Reference Preservation
- **Preserve Knowledge & References:** Never delete comments containing documentation links, StackOverflow URLs, tutorial citations, or domain context.
- **Annotate Legacy Changes:** When updating deprecated syntax, add explanatory annotations contrasting old vs new syntax rather than stripping rationale.
- **Maintain Developer Checklists:** Preserve developer notes and checklist files (e.g., `NOTES.txt`).

---

## 2. Persistent Task & Migration Logging
- **Log State Regularly:** Maintain a persistent `MIGRATION_LOG.md` tracking active tasks, milestones, and architectural decisions.
- **Token & Quota Interruption Resilience:** Write checkpoints into `MIGRATION_LOG.md` before and after major modifications so subsequent sessions resume without regressing: milestone title, objectives, files modified/created, test commands, and pending items.

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
