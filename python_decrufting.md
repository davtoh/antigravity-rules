# Rule: Python 2 Decrufting

## Purpose
Ensure all code conforms strictly to modern Python 3 (3.10–3.12+) standards. Prevent re-introduction of obsolete Python 2/3 compatibility shims, dead imports, and deprecated libraries.

## Guidelines

1. **No Obsolete Python 2 Compatibility Imports:**
   - **DO NOT** use `from __future__ import division, print_function, absolute_import`. In Python 3, these behaviors have been native built-in defaults since Python 3.0.
   - **DO NOT** use `from builtins import object` or inherit explicitly from `object` (e.g. `class Foo(object):` -> use `class Foo:`).
   - **DO NOT** use `past.builtins` or `basestring`. Use native `str`.
   - **DO NOT** use `six` (e.g. `six.with_metaclass`, `six.reraise`, `six.moves`). Use native Python 3 syntax (`class Foo(metaclass=Meta):`, `raise ... from ...`, `urllib.parse`, etc.).
   - The only valid `__future__` import in this repository is `from __future__ import annotations` (PEP 563) when deferred evaluation of type hints is specifically needed.

2. **Clean Dependency Footprint:**
   - Keep `requirements.txt` lean. Do not depend on `six`, `future`, or other historical bridging libraries.
   - Use the modern standard library wherever possible (`pathlib`, `typing`, `dataclasses`, `collections.abc`, `asyncio`, `urllib.parse`).

3. **Modern NumPy 2.x & Python 3 Types:**
   - Use built-in scalar types (`int`, `float`, `bool`) instead of deprecated NumPy aliases (`np.int`, `np.float`, `np.bool`, `np.alltrue`).
   - Import collections ABCs from `collections.abc` (e.g. `collections.abc.MutableMapping`, `collections.abc.Iterable`).

4. **Preserve Domain Comments & Math:**
   - When modernizing syntax or removing dead shims, strictly preserve all mathematical docstrings, computer vision algorithms, and domain comments (e.g. OpenCV coordinate formulas, homography, filter calculations).
