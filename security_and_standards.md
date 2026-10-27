# Rule: Universal Security & Engineering Standards

## Purpose
Enforce industry-standard security (OWASP Top 10, 12-Factor App methodology), data privacy, resource safety, cross-platform robustness, and clean engineering conventions across all projects, modernizations, web services, mobile applications, and edge/IoT systems.

---

## 1. Secrets, Credentials & Zero-Hardcoded Infrastructure (12-Factor App)
- **Zero Secrets in Source Control:**
  - Never commit API keys, tokens, passwords, private keys, database credentials, camera RTSP credentials (`rtsp://user:pass@...`), webhook secrets, bot tokens, or framework `SECRET_KEY` values into version control.
  - Always utilize `.env` files and environment variables. Always provide and maintain `.env.example` templates with sanitized, non-functional placeholders.
- **Zero Hardcoded Infrastructure Details:**
  - Never embed infrastructure connection strings (`redis://...`, `postgres://...`, `mongodb://...`), hostnames/IPs (`127.0.0.1`, `localhost`), credentials, or port numbers (`6379`, `5432`, `3306`, etc.) as hardcoded fallback literals in application code or configuration dictionaries.
  - All infrastructure endpoints, ports, passwords, and external services must resolve strictly from environment variables (`os.getenv(...)`) with safe empty-string fallbacks (`""`) or explicit configuration errors when mandatory.

---

## 2. Input Validation & Injection Prevention
- **Safe Database Queries (SQL Injection Prevention):**
  - Never use raw string formatting (`%`, `.format()`, f-strings) or string concatenation to construct SQL or database queries.
  - Always use parameterized queries, ORM query builders, or prepared statements.
- **Cross-Site Scripting (XSS) & Template Escaping:**
  - Rely on framework auto-escaping in templates and UI components.
  - Never bypass HTML sanitization (e.g., avoid `|safe`, `dangerouslySetInnerHTML`, `v-html`) unless strictly required and thoroughly sanitized with an established sanitizer.
- **Command Injection & SSRF Prevention:**
  - Never pass unvalidated user input into shell execution functions (`os.system`, `subprocess(..., shell=True)`, `exec`, `eval`). Always pass arguments as sanitized arrays (`shell=False`).
  - Validate and restrict outbound network requests (webhooks, URL fetchers, RTSP streams, MQTT brokers) to prevent Server-Side Request Forgery (SSRF) against internal networks or cloud metadata endpoints.
- **CSRF & State-Changing Protections:**
  - Enforce CSRF protection or cryptographically secure token validation on all state-changing operations (`POST`, `PUT`, `DELETE`, `PATCH`).
- **Safe Authentication & Authorization:**
  - Verify permissions and authentication state on all protected endpoints, routes, and views. Use framework built-in secure hashing (Argon2, bcrypt, PBKDF2) and token generators.

---

## 3. Data Privacy, Telemetry & Safe Error Handling
- **Data Privacy & Compliance (GDPR / Sensitive Media):**
  - Do not persist or stream personally identifiable information (PII), sensitive customer data, or unmasked media unnecessarily.
  - In vision, CCTV, or telemetry pipelines, provide configuration toggles for privacy masking, face/license-plate blurring, and metadata-only forwarding (e.g. bounding boxes or counts instead of raw imagery).
- **Safe Error Handling & Stack Trace Leaks:**
  - Never leak uncaught exceptions, internal filesystem paths, or full database stack traces to clients/users in production.
  - Replace hard-crashing lookups (e.g. unhandled `.get()`) with safe lookups (e.g. `get_object_or_404()` or graceful dictionary lookups with fallback defaults).
  - Return standardized, clean HTTP error responses (`400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`).

---

## 4. Resource Safety, Concurrency & Resilience
- **Resource Management & Leak Prevention:**
  - Always use context managers (`with` statements) or explicit cleanup (`try...finally`) for file handles, network sockets, database connections, and hardware capture streams (e.g. `cap.release()`, `cv2.destroyAllWindows()`).
  - Prevent memory accumulation in streaming buffers, queues, or unconstrained caches.
- **Thread & Pipeline Safety:**
  - Cleanly decouple and synchronize CPU/IO-intensive workloads (video acquisition, AI inference, file I/O, heavy queries) from UI rendering and main event loops to avoid interface freezing.
- **Graceful Hardware & Service Fallbacks:**
  - Tests, scripts, and applications must never hard-crash if a physical peripheral (webcam, GPU, serial port, GPIO) or external service (Redis, third-party API) is unavailable.
  - Always provide fallback mocks, synthetic generators, or informative warnings.

---

## 5. Cross-Platform Compatibility
- **Zero OS Hardcoding:**
  - Code must run seamlessly across Windows (PowerShell/CMD), Linux (Ubuntu, Debian, Raspberry Pi OS), and macOS (Apple Silicon & Intel).
  - Never hardcode POSIX (`/`) or Windows (`\`) slashes in filesystem operations. Always use standard path libraries (`pathlib.Path`, `os.path`, or target language standard library).
- **Portable System Dependencies:**
  - Avoid OS-exclusive modules (e.g. Unix-only `import resource`) in shared logic; use cross-platform libraries like `psutil`.

---

## 6. Code Quality & Engineering Discipline
- **Structured Logging:**
  - Use standard language logging frameworks (`logging` in Python, standard loggers in Dart/TS) with appropriate levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`) instead of scattered raw `print()` statements in production code.
- **Modern Language Standards & Type Safety:**
  - Target modern runtimes (Python 3.10-3.12+, modern Dart 3+, modern TypeScript).
  - Phase out obsolete compatibility shims (e.g. Python 2/3 shims like `six`, `future`, `from __future__ import division`) in favor of native constructs and type annotations.
- **Modularity & Single Responsibility:**
  - Keep controllers, models, services, views, and helpers modular, cleanly decoupled, and focused on single responsibilities.