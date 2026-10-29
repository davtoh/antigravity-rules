---
description: Universal security (OWASP Top 10, 12-Factor zero hardcoded secrets/URLs), 10 core coding principles, modularity budgets, data privacy, resource safety, and OS-agnostic cross-platform standards.
trigger: always_on
---

# Rule: Universal Security & Engineering Standards

## Purpose
Enforce industry-standard security (OWASP Top 10, 12-Factor App methodology), the 10 Core Coding Principles, quantitative modularity budgets, data privacy, resource safety, and cross-platform robustness across all projects, languages, and architectures.

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

## 6. The 10 Core Coding Principles & Modularity Budgets

### A. The 10 Core Engineering Principles
1. **Single Responsibility Principle (SRP):** Give every module, class, and function one clear domain responsibility and a single reason to change. Decouple transport/UI routing, business logic, and data persistence into distinct layers.
2. **DRY (Don't Repeat Yourself):** Avoid duplicating validation rules, query patterns, state transitions, or formatting logic. Extract shared behavior into reusable functions, composable classes, or shared modules.
3. **KISS (Keep It Simple, Stupid):** Write straightforward, readable control flow. Prefer flat structures and guard clauses over deep nesting, premature abstraction, or over-engineered meta-programming.
4. **Descriptive Naming:** Use clear, intention-revealing names for variables, predicates (`is_`, `has_`, `can_`, `should_`), functions (`verb_noun`), classes, and files so code reads as self-documenting prose without magic numbers.
5. **Comments for the "Why":** Let expressive code explain *how*, and use comments and docstrings to explain *why*—documenting design trade-offs, business invariants, non-obvious edge cases, mathematical formulas, and legacy migration rationale.
6. **Consistent Coding Style:** Follow official language-specific style guides and type systems (PEP 8 + type hints for Python 3.10–3.12+, Effective Dart, strict TypeScript/ESLint, rustfmt/gofmt) and use structured logging frameworks (`logging`, `logger`) instead of raw `print()` statements in production code.
7. **Error Handling & Robustness:** Anticipate invalid or unexpected inputs, fail gracefully, use narrow exception handling rather than bare catch-alls, and never leak raw stack traces to end users.
8. **Testing & Verification:** Pair new logic and bug fixes with automated unit and integration tests, static analysis, and type checking to catch regressions early.
9. **Version Control Hygiene:** Keep commits atomic, focused, and paired with clear, descriptive commit messages. Never commit temporary scratch files, build artifacts, or local environment state.
10. **Security First:** Sanitize untrusted inputs, parameterize queries, manage secrets exclusively via environment variables, keep dependencies lean and updated, and never hardcode sensitive data, URLs, or magic constants.

### B. Quantitative Modularity Budgets & "Split-Before-You-Grow"
To prevent "God Files" and "God Classes" that degrade human maintainability and AI context efficiency, enforce the following size budgets across all source files:

| Code Element | Healthy Target | Soft Warning (Refactor Trigger) | Hard Ceiling (Mandatory Split) | Required Action When Approaching Limit |
| :--- | :--- | :--- | :--- | :--- |
| **Source File** | 150 – 300 lines | **350 lines** | **500 lines** | Split into cohesive domain submodules (`routers/`, `services/`, `repositories/`, `components/`). |
| **Class** | 50 – 180 lines | **10 methods** (or 200 lines) | **12 methods** (or 300 lines) | Decompose using composition, focused domain services, or collaborator classes. |
| **Function / Method** | 10 – 25 lines | **30 lines** | **40 lines** | Extract pure helper functions or strategy objects; flatten nested branches. |
| **Route / Controller** | 5 – 15 lines | **15 lines** | **25 lines** | Keep handlers thin: parse/validate input, call a service method, and return the response. |

- **The "Split-Before-You-Grow" Rule:** Never append a new feature, endpoint group, or data domain directly into an existing file that is already $\ge$ 350 lines or a class with $\ge$ 10–12 methods. Instead, create a dedicated submodule, router, service, or repository and wire it in cleanly.

---

## 7. Frontend, CSS Specificity & Layout Discipline
- **Strict Avoidance of `!important`:**
  - Never use `!important` in production stylesheets. It breaks natural CSS cascade inheritance, makes styles un-overridable by responsive or thematic child components, breaks fullscreen pseudo-classes (`:fullscreen`), and creates compounding specificity debt.
  - Rely on structured CSS specificity: leverage pseudo-classes (`:fullscreen`, `:hover`, `:focus-visible`), parent-scoped selectors, or CSS custom properties (variables) rather than brute-forcing styles.
- **Defensive Layout & Overflow Containment:**
  - Prevent text-overflow blowouts by ensuring all flex and grid children containing dynamic or user-supplied strings include `min-width: 0`, `overflow: hidden`, and `text-overflow: ellipsis`, pairing them with native `title` attributes for full hover reveal.