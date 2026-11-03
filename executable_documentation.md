---
description: Require runnable CLI/service recipes, pre-run diagnostic one-liners, and Scenario Combinations Matrices in project documentation.
trigger: always_on
---

# Rule: Executable Documentation & Scenario Matrices

## Purpose
Prevent abstract, difficult-to-run documentation. User-facing manuals (`README.md`, `SETUP_GUIDE.md`, `docs/`) must provide copy-pasteable execution commands, diagnostic one-liners, and parameter combination tables.

## Guidelines

1. **Documentation as Single Source of Truth:**
   - Keep runnable CLI recipes and configurations in project docs (`README.md`, `docs/`). Do not duplicate static command lists into separate custom skills where they drift.

2. **Pre-Run Verification One-Liners:**
   - Always provide 1–2 quick diagnostic commands before complex execution recipes:
     - Check environment / hardware probes (GPU, camera index).
     - Verify assets / weights integrity (checksum or status script).
     - Run automated test suite (`python -m unittest discover tests`).

3. **Mandatory Scenario Combinations Matrix:**
   - For commands accepting multiple flags, include a Markdown table matching user intent to exact runnable commands:

   | Scenario / Objective | Mode / Inputs | Key Parameters | Exact Runnable Command |
   | :--- | :--- | :--- | :--- |
   | Quick Smoke Test | Synthetic feed | `--source synthetic --headless` | `python main.py --source synthetic --headless --frames 30` |
   | Retail Person Tally | Webcam 0 | `--source 0 --classes person` | `python main.py --source 0 --classes person --conf 0.40` |

4. **Interactive Controls Reference:**
   - If a GUI or visual session is launched, document interactive keys (quit, clear, toggle overlays, snapshots).
