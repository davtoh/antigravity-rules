# Rule: Executable Documentation & Scenario Matrices

## Purpose
Prevent abstract, difficult-to-run documentation. When creating or updating features, CLI tools, services, or milestones, always provide copy-pasteable sample execution commands and parameter combination tables directly in user-facing manuals (`README`, `SETUP_GUIDE`, or Sphinx/Markdown docs). Developers and users should never have to memorize argument permutations or guess valid configurations.

## Guidelines

1. **Documentation as the Single Source of Truth:**
   - Always place runnable examples, CLI recipes, and configuration permutations directly in the project's documentation (`README.md` / `README.rst`, `SETUP_GUIDE.md`, or `docs/`).
   - Do NOT duplicate static project-specific command lists into separate custom skills or hidden directories where they become stale and drift out of sync.

2. **Always Provide Pre-Run Verification One-Liners:**
   - Before presenting complex run commands, provide 1–2 quick diagnostic or verification commands so the user can verify readiness:
     - Model weight presence and checksum integrity checks (e.g., `python scripts/download_models.py --status`).
     - Hardware/environment probes (e.g., camera device indices, GPU/DirectML execution providers).
     - Automated test verification commands (e.g., running the test suite).

3. **Mandatory "Scenario Combinations Matrix":**
   - Whenever a command accepts multiple arguments (e.g., `--source`, `--detector`, `--conf`, `--classes`, `--headless`), provide a structured Markdown/RST table that pairs **real-world user intent** with the exact copy-pasteable command:
     - *Synthetic / Headless Smoke Test*: For CI/CD or users without hardware.
     - *Standard Local Execution*: Default webcam or interactive GUI.
     - *Specific Filtering / High Confidence*: Retail, security, or domain-specific filtering.
     - *High-Resolution / Production Mode*: RTSP network streams or recording video output.
     - *Headless Server / Remote Worker*: Server mode with offscreen backends.

   *Example Matrix Format:*
   | Scenario / Objective | Mode / Inputs | Key Parameters | Exact Runnable Command |
   | :--- | :--- | :--- | :--- |
   | Quick Smoke Test | Synthetic feed | `--source synthetic --headless` | `python main.py --source synthetic --headless --frames 30` |
   | Retail Person Tally | Webcam 0 | `--source 0 --classes person` | `python main.py --source 0 --classes person --conf 0.40` |

4. **Provide Interactive Keyboard & Control References:**
   - If an interactive GUI or visual session is launched, always document user controls (e.g., keys to quit, clear tracks, toggle overlays, or save snapshots).

5. **Cross-Project Reusability:**
   - Apply this standard consistently across all repositories:
     - **Machine Learning / CV**: Detector, model weights, input source, confidence threshold, video recording.
     - **Web Services / Celery**: Worker startup, concurrency pools (`-P solo` vs. prefork), log levels, queue names.
     - **CLI Tools**: Subcommands, flags, dry-run options, output formats (`--json`, `--table`).
