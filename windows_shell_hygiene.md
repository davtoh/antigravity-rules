---
description: Windows PowerShell 5.1 shell & virtualenv hygiene to prevent quoting, grep, and exit-code masking failures.
trigger: always_on
---

# Rule: Windows Shell & Virtualenv Hygiene

When running commands on Windows (`powershell.exe`):
1. **No `rg` or `&&`**:
   - Never assume `rg` is installed; use `git grep -n "<pattern>"` (in Git repos) or `Select-String`.
   - Never use `&&` in PowerShell 5.1; chain commands cleanly and halt on non-zero `$LASTEXITCODE` (`; if ($LASTEXITCODE -ne 0) { throw "step failed" }`). Never mask Python/CLI tracebacks behind trailing `; NextCommand`.
2. **Virtualenv First**:
   - In Python repos with `.venv\`, `venv\`, or `env\`, always invoke `.venv\Scripts\python.exe` (backslashes) directly or use skill runners (`diagnose.py tests`, `run_diagnose.py tests`), never bare system `python`.
3. **Zero Fragile Inline Quotes**:
   - Never embed nested quotes inside `python -c "..."` or inline JS inside `--eval "..."`.
   - For multi-line Python/JS checks, either write a temporary script in `<ArtifactDir>/scratch/`, pass `--eval-file <path>`, or use a PowerShell single-quoted here-string variable (`$code = @' ... '@`).
   - Never write ad-hoc Python one-liners just to count file line lengths; use `diagnose.py audit --path <files>` or `code_health_audit.py`.
