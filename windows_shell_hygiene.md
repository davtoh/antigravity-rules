---
description: Windows PowerShell 5.1 shell & virtualenv hygiene to prevent quoting, grep, and exit-code masking failures.
trigger: always_on
---

# Rule: Windows Shell & Virtualenv Hygiene

When running commands on Windows (`powershell.exe`):
1. **No `rg` or `&&`**:
   - Never assume `rg` is installed; use `git grep -n "<pattern>"` (in Git repos) or `Select-String`.
   - **`git grep` Exit Code `1` Semantics**: `git grep` exits `1` when **zero** matches are found (the expected pass condition for negative assertions such as checking for `file:///` or secrets). Never treat `$LASTEXITCODE -eq 1` from `git grep` as a command error or leave it as the final exit code of a chained diagnostic check; check `if ($LASTEXITCODE -gt 1) { throw "git grep failed" }`.
   - Never use `&&` in PowerShell 5.1; chain external/native executables (`python`, `git`, `pytest`, `flutter`) cleanly and halt on non-zero `$LASTEXITCODE` (`; if ($LASTEXITCODE -ne 0) { throw "step failed" }`). Never attach `$LASTEXITCODE` checks to PowerShell cmdlets (`Remove-Item`, `Move-Item`, `Copy-Item`); use `-ErrorAction Stop` instead. Never mask Python/CLI tracebacks behind trailing `; NextCommand`.
2. **Virtualenv First**:
   - In Python repos with `.venv\`, `venv\`, or `env\`, always invoke `.venv\Scripts\python.exe` (backslashes) directly or use skill runners (`diagnose.py tests`, `run_diagnose.py tests`), never bare system `python`.
3. **Zero Fragile Inline Quotes**:
   - Never embed nested quotes inside `python -c "..."` or inline JS inside `--eval "..."`.
   - For multi-line Python/JS checks, either write a temporary script in `<ArtifactDir>/scratch/`, pass `--eval-file <path>`, or use a PowerShell single-quoted here-string variable (`$code = @' ... '@`).
   - Never write ad-hoc Python one-liners just to count file line lengths; use `diagnose.py audit --path <files>`.
4. **Serial Same-File Edits & Safe JSON Output**:
   - Never issue multiple parallel `edit_file` calls on the same file in one turn (later `Target` blocks go stale and fail); merge adjacent edits into one call or apply them sequentially.
   - When consuming `--json` CLI output from Python, do not pipe it through PowerShell into `python -c` (BOM/encoding and quoting traps); call `subprocess.run([...], capture_output=True, text=True, encoding='utf-8')` inside a scratch script instead.
