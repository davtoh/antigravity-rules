---
description: Enforce modern Python 3 standards, prohibit all __future__ imports, eliminate obsolete Python 2/3 shims, and preserve domain math.
trigger: always_on
---

# Rule: Python Decrufting & Modern Standards

## Purpose
Ensure all Python code conforms strictly to modern Python 3 (3.10–3.15+) standards. Eliminate obsolete Python 2/3 compatibility shims, dead imports, and deprecated libraries.

## Guidelines

1. **Strictly No `__future__` Imports:**
   - **DO NOT** use `from __future__ import annotations` or any other `__future__` imports (e.g., `division`, `print_function`, `absolute_import`).
   - Modern Python natively supports modern syntax, PEP 604 type unions (`X | Y`), and built-in type evaluations. Never add `__future__` shims.

2. **No Obsolete Python 2 Compatibility Shims:**
   - **DO NOT** use `from builtins import object` or explicit `class Foo(object):` (use `class Foo:`).
   - **DO NOT** use `past.builtins`, `basestring`, or `unicode`. Use native `str`.
   - **DO NOT** use `six` (e.g. `six.with_metaclass`, `six.reraise`, `six.moves`). Use native Python 3 syntax (`class Foo(metaclass=Meta):`, `raise ... from ...`, `urllib.parse`, etc.).

3. **Lean Dependencies & Standard Library:**
   - Never depend on `six`, `future`, or historical bridging libraries in `requirements.txt`.
   - Use standard library modules (`pathlib`, `typing`, `dataclasses`, `collections.abc`, `asyncio`, `urllib.parse`).

4. **Modern Types & Builtins:**
   - Use built-in scalar types (`int`, `float`, `bool`) instead of deprecated NumPy aliases (`np.int`, `np.float`, `np.bool`).
   - Import collections ABCs from `collections.abc` (e.g. `collections.abc.Iterable`, `collections.abc.Mapping`).

5. **Preserve Domain Comments & Algorithms:**
   - Preserve all mathematical docstrings, CV algorithms, and domain comments (e.g., OpenCV coordinate formulas, homography, filter calculations).

6. **Automated Verification:**
   - Verify modernized files using `ruff check --select UP,FA,B` or `python -m py_compile <file>`.

