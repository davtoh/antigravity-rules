---
description: Universal guidelines for project modernization, comment preservation, milestone-by-milestone workflow, portable plans, and persistent MIGRATION_LOG.md checkpoints.
trigger: always_on
---

# Universal AI Guidelines for Project Modernization & Migration

## 1. Comment & Reference Preservation
- **Preserve Knowledge & References:** Never delete comments containing documentation links, StackOverflow URLs, tutorial citations, or domain context.
- **Annotate Legacy Changes:** When updating deprecated syntax, add explanatory annotations contrasting the old vs new approach rather than stripping out original rationale.
- **Maintain Developer Checklists:** Preserve developer notes and checklist files (e.g., `NOTES.txt`).

---

## 2. Persistent Task & Migration Logging
- **Log State Regularly:** Maintain a persistent `MIGRATION_LOG.md` tracking active tasks, milestones, and architectural decisions.
- **Token & Quota Interruption Resilience:** Write clear checkpoints into `MIGRATION_LOG.md` before and after major modifications so subsequent sessions resume without re-analyzing or regressing:
  - Date & Milestone title
  - Objectives & Scope
  - Files Modified / Created
  - Verification & Test Commands
  - Next Steps / Pending Items

---

## 3. Milestone-by-Milestone Workflow & Sanitized Plans
- **Incremental Steps:** Break work into logical, cohesive milestones. Avoid sprawling, unbounded edits.
- **Portable & Sanitized Plan Artifacts:** Implementation plans, milestone logs, and architectural roadmaps must remain fully portable:
  - **No Local Paths:** NEVER embed `file:///` URIs, Windows drive letters (`C:\`), or OS user paths (`/home/...`, `Users/...`) inside committable files, implementation plans, or documentation.
  - **POSIX Paths:** Always use repository-relative forward-slash POSIX paths (`src/module/file.py#L10-L20` or `[file.py](src/module/file.py)`).
  - **OS-Agnostic Verification:** Use cross-platform commands (`python -m unittest discover tests`, `pytest tests/ -v`). Never reference OS-locked virtualenv binaries (`.venv\Scripts\...`) or personal customization directories (`~/.gemini/...`).
  - **Infrastructure Parameterization:** Use environment placeholders (`$APP_URL` or relative paths like `/api/v1/health`) rather than hardcoding literal infrastructure details.
- **Pre-Commit Staging Audit Gate:**
  - Before presenting a suggested `git commit` command, audit staged files to verify:
    1. Zero `file:///` URLs or local machine absolute paths.
    2. Zero OS-specific virtual environment binary paths.
    3. Zero hardcoded local infrastructure URLs/ports.
    4. Compliance with modularity budgets and executable verification commands.
- **Validation & Commit Review:** Run automated checks before closing each milestone, provide copy-pasteable manual verification steps, and offer concise commit message suggestions for user review.
