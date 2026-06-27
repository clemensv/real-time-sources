#!/usr/bin/env python3
"""P2 codegen self-test: ``py_compile`` every generated producer package so a
malformed xrcg / avrotize emission fails fast at generation time instead of at
container start.

This catches the codegen-bug class the postmortem surfaced -- a ``{time}``
subject placeholder colliding with the injected ``_time`` envelope param
(``SyntaxError: duplicate argument '_time'``), a numeric-leading enum symbol,
and empty/truncated template output. It is invoked by ``tools/require-xrcg.ps1``
immediately after each ``xrcg generate`` (single fleet-wide injection point,
since every ``generate_producer.ps1`` routes through ``Convert-GeneratedPyprojects``),
and is also runnable standalone over one or more producer directories.

Usage::

    python tools/ci/verify_generated_producer.py <producer_dir> [<producer_dir> ...]

Exit 1 if any file fails to compile.
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
        if not d.exists():
            print(f"WARN: {d} does not exist, skipping", file=sys.stderr)
            continue
        total += sum(1 for p in d.glob("**/*.py") if not SKIP.search(str(p)))
        if not compileall.compile_dir(str(d), quiet=1, maxlevels=30, rx=SKIP):
            failures.append(str(d))

    if failures:
        print(f"FAIL: py_compile errors in {len(failures)} producer dir(s): "
              f"{', '.join(failures)}", file=sys.stderr)
        return 1
    print(f"PASS: {total} generated producer file(s) compiled cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
