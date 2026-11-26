#!/usr/bin/env python3
"""P2 codegen self-test: ``py_compile`` every generated producer package so a
malformed xrcg / avrotize emission fails fast at generation time instead of at
container start.

This catches the codegen-bug class the postmortem surfaced -- a ``{time}``
subject placeholder colliding with the injected ``_time`` envelope param
(``SyntaxError: duplicate argument '_time'``), a numeric-leading enum symbol,
and syntactically truncated template output. Missing directories and directories
without Python modules also fail. It is invoked by ``tools/require-xrcg.ps1``
immediately after each ``xrcg generate`` (single fleet-wide injection point,
since every ``generate_producer.ps1`` routes through ``Convert-GeneratedPyprojects``),
and is also runnable standalone over one or more producer directories.

Usage::

    python tools/ci/verify_generated_producer.py <producer_dir> [<producer_dir> ...]

Exit 1 if any directory is missing, contains no eligible Python modules, or has
a file that fails to compile. This checks syntax, not runtime imports or whether
every required template produced a file.
"""
from __future__ import annotations

import compileall
import re
import sys
from pathlib import Path

SKIP = re.compile(r"[\\/](build|\.git|__pycache__)[\\/]")


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: verify_generated_producer.py <producer_dir> ...", file=sys.stderr)
        return 2

    failures: list[str] = []
    total = 0
    for arg in argv:
        d = Path(arg)
        if not d.is_dir():
            failures.append(f"{d}: output directory is missing or is not a directory")
            continue
        modules = [p for p in d.glob("**/*.py") if not SKIP.search(str(p))]
        if not modules:
            failures.append(f"{d}: no eligible Python modules were generated")
            continue
        total += len(modules)
        compiled = [compileall.compile_file(str(p), quiet=1) for p in modules]
        if not all(compiled):
            failures.append(f"{d}: Python compilation failed")

    if failures:
        print(f"FAIL: generated producer validation failed in {len(failures)} dir(s): "
              f"{', '.join(failures)}", file=sys.stderr)
        return 1
    print(f"PASS: {total} generated producer file(s) compiled cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
