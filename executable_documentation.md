---
description: Activate when adding/modifying CLI flags, APIs, or features, or updating README.md, SETUP_GUIDE.md, or docs/. Enforces code-doc sync, runnable CLI recipes, and Scenario Combinations Matrices.
trigger: model_decision
---

# Rule: Executable Documentation & Scenario Matrices

## Purpose
Ensure manuals (`README.md`, `SETUP_GUIDE.md`, `docs/`) provide runnable commands, diagnostic one-liners, and parameter tables kept strictly synchronized with code changes.

## Guidelines

1. **Documentation as Single Source of Truth & Code-Doc Sync:**
   - Keep runnable CLI recipes and configurations in project docs (`README.md`, `docs/`). Do not duplicate static command lists into separate custom skills where they drift.
   - **Code-Doc Sync Invariant:** Whenever code introduces, alters, or deprecates CLI flags, environment variables, APIs, or workflows, update corresponding `README.md`, `docs/`, and Scenario Combinations Matrix in the same milestone. Never leave new functionality undocumented.

2. **Pre-Run Verification One-Liners:**
   - Always provide 1–2 quick diagnostic commands before complex execution recipes:
     - Check environment / hardware probes (GPU, camera index).
     - Verify assets / weights integrity (checksum or status script).
     - Run automated test suite (`python -m unittest discover tests`).

3. **Mandatory Scenario Combinations Matrix:**
   - For multi-flag commands, include a Markdown table matching user intent to runnable commands:

   | Scenario / Objective | Mode / Inputs | Key Parameters | Exact Runnable Command |
   | :--- | :--- | :--- | :--- |
   | Quick Smoke Test | Synthetic feed | `--source synthetic --headless` | `python main.py --source synthetic --headless --frames 30` |
   | Retail Person Tally | Webcam 0 | `--source 0 --classes person` | `python main.py --source 0 --classes person --conf 0.40` |

4. **Interactive Controls Reference:**
   - If a GUI or visual session is launched, document interactive keys (quit, clear, toggle overlays, snapshots).
