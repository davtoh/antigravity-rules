---
description: Universal security (OWASP Top 10, 12-Factor zero hardcoded secrets/URLs), core coding principles, modularity budgets, resource safety, and frontend layout discipline.
trigger: always_on
---

# Rule: Universal Security & Engineering Standards

## 1. Secrets, Credentials & Zero-Hardcoded Infrastructure (12-Factor App)
- **Zero Secrets in Source Control:** Never commit API keys, tokens, passwords, RTSP credentials (`rtsp://user:pass@...`), webhook secrets, or framework `SECRET_KEY`s. Use `.env` with a maintained `.env.example` template.
- **Zero Hardcoded Infrastructure Details:** Never embed connection strings (`redis://...`, `postgres://...`), hostnames/IPs (`127.0.0.1`, `localhost`), or ports (`6379`, `5432`) as literal fallbacks in application code. Resolve exclusively via `os.getenv(...)` with safe empty-string fallbacks (`""`) or explicit configuration errors.

---

## 2. Input Validation, Injection & State Protection
- **SQL & Query Injection:** Always use parameterized queries, ORM query builders, or prepared statements. Never use string formatting or concatenation for queries.
- **XSS & Template Escaping:** Rely on framework auto-escaping. Avoid bypassing HTML sanitization (`|safe`, `dangerouslySetInnerHTML`, `v-html`).
- **Command Injection & SSRF:** Never pass unvalidated input to shell execution (`os.system`, `subprocess(shell=True)`, `eval`). Restrict outbound network calls (webhooks, RTSP, MQTT) against private internal IP ranges and cloud metadata endpoints.
- **Archive Extraction Parity:** When extracting `.zip` or `.tar` archives, reject path traversal (`Zip-Slip`/`Tar-Slip`) **and** symlink/hardlink entries uniformly across both formats.
- **CSRF & Authentication:** Enforce CSRF protection on state-changing requests (`POST`, `PUT`, `DELETE`). Secure protected endpoints with established hashing (Argon2, bcrypt, PBKDF2).

---

## 3. Data Privacy, Error Handling & Resource Safety
- **Data Privacy (GDPR / Sensitive Media):** Do not persist unnecessary PII. Provide toggles for privacy masking, face/plate blurring, or metadata-only forwarding in vision pipelines.
- **Safe Error Handling:** Never leak uncaught exceptions, internal filesystem paths, or stack traces to clients in production. Return clean HTTP error codes (`400`, `401`, `403`, `404`).
- **Resource Management:** Always use context managers (`with` statements) or explicit cleanup (`try...finally`) for file handles, sockets, database sessions, and camera capture handles (`cap.release()`). Prevent unconstrained buffer growth.
- **Test State & Config Isolation:** Unit and integration tests must never read from or mutate live workspace config files, databases, or user data directories through default constructor paths. Always inject `tempfile.TemporaryDirectory()` (or equivalent isolated test paths) for file-backed stores and clean up via `addCleanup()`/`tearDown()`.
- **Thread & Pipeline Safety:** Decouple IO/inference workloads from UI rendering. Never use blocking `time.sleep()` in long-running reconnect or worker loops; use interruptible event waits (`Event.wait(timeout)`). Provide graceful hardware/service fallbacks.
  - **Never hold locks across blocking operations:** Never execute `thread.join()`, socket calls, or sleep waits while holding a lock (`with self._lock:`). Always release the lock prior to joining threads.
  - **Single Clock Domain & `None` Debounce Sentinels:** Never mix wall-clock epoch (`time.time()`) and monotonic (`time.monotonic()`) timestamps across schedulers, caches, or API readers; initialize elapsed/debounce timestamps to `None` rather than `0.0`.
  - **Zero Default time.sleep Fallbacks:** When adding cancellation events, default `self.stop_event` to `threading.Event()` rather than `None` to prevent falling back to uninterruptible `time.sleep()`.
  - **Upstream Factory Parity:** When parameterizing environment variables (e.g. `MQTT_BROKER`), audit all upstream pipeline factories to ensure they do not pass literal hardcoded string defaults that override environment defaults.
  - **Asynchronous Event Isolation (Target-to-View Match):** In UI event subscribers handling asynchronous job completion, always verify `currentActiveId === event.targetId` before updating DOM containers to prevent background jobs from overwriting unrelated views.
  - **Persistent State Invariant:** When a feature specifies preserving task progress or reports across tabs and navigation, state MUST be backed by a persistent storage mechanism (database, local storage, or server-side cache), not volatile in-memory JavaScript structures (`Map`, `Object`).

---

## 4. Cross-Platform & File Discipline
- **OS-Agnostic Filesystem:** Code must run seamlessly across Windows, Linux, and macOS. Never hardcode `/` or `\` slashes; use `pathlib.Path` or `os.path`. Use cross-platform libraries (e.g. `psutil`).
- **Cross-Platform Virtualenv Execution Invariant:** In any workspace containing `.venv/`, never invoke bare `python` or `python3` for project scripts, test runners, or diagnostics. Always resolve the active `.venv` binary:
  - macOS/Linux: `.venv/bin/python`
  - Windows: `.venv\Scripts\python.exe`

  Bare `python`/`python3` silently resolves to the system interpreter, which lacks all project dependencies — causing `ModuleNotFoundError` cascades that produce false negatives and waste diagnostic tokens. Use `run_diagnose.py` (which auto-resolves `.venv`) or confirm the venv path before any test run.
- **Line Ending & Patching Discipline:** Inspect and respect target file line endings (LF vs CRLF) before applying multi-line text replacements (`edit_file`) to avoid patching failures.
- **Zero-CRCRLF Binary Write Rule:** When modifying text files in Python scripts on Windows, NEVER use `Path.write_text()` or `open(..., 'w')` on strings that already contain `\r\n` (which causes Windows text-mode `\r\r\n` double-newline token bloat). Always write via `Path.write_bytes(content.encode('utf-8'))` or `open(..., 'w', newline='', encoding='utf-8')` to preserve exact line endings.

---

## 5. Core Engineering Principles & Modularity Budgets
- **Core Principles:** Single Responsibility (SRP), DRY, KISS, Descriptive Naming (`is_`, `has_`, `verb_noun`), Comments for the "Why", Consistent PEP 8/Effective Dart style, and branch-complete testing.
- **Quantitative Modularity Budgets:** Enforce the following hard limits:

| Code Element | Target | Warning (Refactor Trigger) | Hard Ceiling (Mandatory Split) | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Source File** | 150–300 L | **350 lines** | **500 lines** | Split into domain modules (`services/`, `routers/`, `repositories/`). |
| **Class** | 50–180 L | **10 methods** (or 200 L) | **12 methods** (or 300 L) | Decompose via composition or focused collaborators. |
| **Function** | 10–25 L | **30 lines** | **40 lines** | Extract pure helper functions; flatten branches. |
| **Route / Controller** | 5–15 L | **15 lines** | **25 lines** | Thin handlers: validate, call service, return response. |

- **Split-Before-You-Grow:** Never append a new feature or endpoint directly into a file $\ge$ 350 lines or a class with $\ge$ 10–12 methods. Create dedicated submodules first.

---

## 6. Frontend, CSS Specificity & Layout Discipline
- **Strict Avoidance of `!important`:** Never use `!important` in production stylesheets. Use structured specificity, parent scoping, pseudo-classes (`:fullscreen`, `:hover`), or CSS variables.
- **Defensive Layout & Overflow Containment:** All flex/grid dynamic text containers must declare `min-width: 0; overflow: hidden; text-overflow: ellipsis;` paired with `title` attributes. Enforce zero root horizontal overflow (`max-width: 100vw; overflow-x: clip;`).
- **Spacing & Separation Discipline:** Maintain proportional gaps: minimum 8px between adjacent controls, 16px–24px between major layout regions. Prevent element collisions and ensure WCAG AA touch targets ($\ge$ 24px, recommended 32–44px).
- **Directional Control States:** Navigation arrows must calculate container padding, borders, and CSS scroll-snap alignments rather than assuming exact zero offsets (`scrollLeft <= 0`).
