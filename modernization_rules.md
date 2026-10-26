# Universal AI Guidelines for Project Modernization & Language Migration

> **Portable Rule Template:** This file can be placed into your global config directory (`~/.gemini/config/rules/modernization_rules.md`) or copied to root `AGENTS.md` in any repository being revived or migrated.

---

## 1. Comment & Reference Preservation
- **Preserve Knowledge & References:** Never delete comments that contain documentation links, StackOverflow URLs, tutorial citations, or educational context.
- **Annotate Legacy Changes:** When updating deprecated syntax (e.g. Django 2.x to 5.x, or Python 2/3, or when translating to another language like Go/Rust/TypeScript), add explanatory annotations contrasting the old vs new approach rather than stripping out the original rationale.
- **Maintain Developer Checklists:** Preserve developer notes and checklist files (e.g. `NOTES.txt`).

---

## 2. Persistent Task & Migration Logging
- **Log State Regularly:** Maintain a persistent `MIGRATION_LOG.md` tracking active tasks, milestones, and architectural decisions.
- **Token & Quota Interruption Resilience:** Write clear checkpoints into `MIGRATION_LOG.md` before and after major modifications. If an AI session runs out of quota or context window, the next session can pick up directly from the latest checkpoint without re-analyzing or regressing.
- **Structure:**
  - Date & Milestone title
  - Objectives & Scope
  - Files Modified / Created
  - Verification & Test Commands
  - Next Steps / Pending Items

---

## 3. Milestone-by-Milestone Workflow & Review
- **Incremental Steps:** Break work into logical, cohesive milestones. Avoid sprawling, unbounded edits.
- **Automated Validation:** Execute automated checks (system diagnostics, unit tests, route checks, linters) before closing each milestone.
- **Manual Verification Instructions:** Provide explicit, copy-pasteable manual testing steps so the developer can verify in the browser or terminal.
- **Developer Review & Commit Gate:** Provide a concise summary and commit message suggestion. Let the user test and commit milestone by milestone.

---

## 4. Security & Engineering Standards
- **OWASP Top 10 & Framework Hardening:**
  - Zero hardcoded credentials or secrets. Use 12-factor `.env` files with version-controlled `.env.example`.
  - Use parameterized queries; never construct SQL with string interpolation.
  - Enforce CSRF protection on state-changing requests.
  - Safe error handling: return clean 404s/400s rather than unhandled 500 exceptions with stack traces.
  - Sanitize input and validate form data.
- **Cross-Platform Compatibility:**
  - Code must run cleanly on Windows (PowerShell/CMD), Linux (bash), and macOS.
  - Never hardcode OS-specific filesystem slashes; use standard path libraries (`pathlib.Path`, `os.path`, or target language standard library).
- **Target Language Idioms:**
  - When modernizing in Python: PEP 8, type hints where helpful, standard library zones (`zoneinfo`).
  - When migrating to other languages (Node/Go/Rust/C#): follow official idioms, project scaffolding, and dependency management standards.
