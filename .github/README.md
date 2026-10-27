# 🛡️ Antigravity Global Rules

Global engineering standards, security baselines, and architectural constraints enforced across all workspaces in [Google Antigravity](https://antigravity.google).

---

## 📋 Catalog of Global Rules

| Rule File | Scope | Purpose |
| :--- | :--- | :--- |
| [**`security_and_standards.md`**](../security_and_standards.md) | Universal | OWASP Top 10, 12-factor secrets management, zero hardcoded infrastructure details, data privacy/GDPR, safe error handling, and cross-platform portability. |
| [**`modernization_rules.md`**](../modernization_rules.md) | Modernization | Milestone-by-milestone workflows, `MIGRATION_LOG.md` persistence for token-interruption resilience, and preservation of reference comments. |
| [**`executable_documentation.md`**](../executable_documentation.md) | Documentation | Ensures runbooks and documentation include copy-pasteable, verified CLI commands rather than abstract placeholders. |
| [**`python_decrufting.md`**](../python_decrufting.md) | Python 3.10–3.12+ | Prohibits reintroduction of Python 2/3 shims (`six`, `future`, `from __future__ import division`) in favor of modern standard library idioms. |

---

## 🔄 Installation & Machine Sync

To use these rules globally on a new machine:

```powershell
# Clone directly into Antigravity's global rules directory
git clone https://github.com/davtoh/antigravity-rules.git "$HOME\.gemini\config\rules"
```

---

## 📄 License
MIT License. Created by [davtoh](https://github.com/davtoh).