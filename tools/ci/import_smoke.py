#!/usr/bin/env python3
"""P0a import smoke-test: prove a feeder's runtime modules actually import.

The class-A "shipped but never ran" defects -- a ``Dockerfile.amqp`` that
installed only ``_producer_data``; an ``app.py`` missing a ``_feedurl``
positional; a ``{time}`` subject placeholder colliding with the CloudEvents
envelope ``_time`` param producing ``SyntaxError: duplicate argument`` in the
generated producer -- all passed ``docker build`` and unit tests and emitted
**zero events**, because the runtime module never imported. This gate closes
the import-time half of that class deterministically.

For one ``feeders/<source>`` it:

1. ``py_compile`` every ``.py`` in the tree (generated + hand-written).
2. Editable-installs the generated sub-packages in dependency order
   (``*_data`` -> ``*_core`` -> producers -> the main feeder package last).
   The install runs in two passes -- a ``--no-deps`` pass that registers
   every local package first (so a transport app that depends on the main
   feeder package resolves even though it is not on PyPI), then a normal
   pass that pulls external dependencies.
3. Imports each transport variant's runtime module taken from the
   ``python -m <module>`` target of every ``Dockerfile*`` -- importing
   ``<module>.app`` when that submodule exists, else the bare ``<module>``.
   It never imports ``__main__``: 72 feeders call ``main()`` at module scope
   and would hang, so each import runs in a subprocess under a timeout.

Usage::

    python tools/ci/import_smoke.py feeders/<source>
    python tools/ci/import_smoke.py feeders/<source> --plan          # compile + plan only
    python tools/ci/import_smoke.py feeders/<source> --no-install    # compile + import, skip pip
    python tools/ci/import_smoke.py feeders/<source> --install-only  # compile + install, skip import
    python tools/ci/import_smoke.py feeders/<source> --timeout 60

``--plan`` is the safe local-Windows mode: it never installs, so it cannot trip
over platform-only build deps (e.g. qpid-proton for the AMQP variant). Full
install+import runs in Linux CI (``.github/workflows/import-smoke.yml``).
"""
from __future__ import annotations

import argparse
import compileall
import json
import re
import subprocess
import sys
from pathlib import Path

CMD_RE = re.compile(r"^\s*(?:CMD|ENTRYPOINT)\s+(\[.*\])\s*$")
SKIP_RE = re.compile(r"[\\/](build|\.git|__pycache__)[\\/]")

# Force the *strict* PEP 660 editable strategy for every local install. The
# default ("lenient"/"compat") strategy is setuptools-version dependent: on some
# runners it writes the feeder project root (``feeders/<src>``) onto ``sys.path``
# via a static ``.pth``. Because each ``feeders/<src>`` holds sibling sub-project
# dirs named exactly like their package (``<src>_core/``, ``<src>_producer/`` --
# none of which carry an ``__init__.py`` at the project level), that root-on-path
# turns ``<src>_core`` into an *empty namespace package* that shadows the real
# editable install -> ``ImportError: cannot import name 'X' from '<src>_core'
# (unknown location)`` at collection time. Strict mode only ever exposes the
# declared packages (under ``build/__editable__.../``), never the project root,
# so the sibling-shadow cannot form. Backends that don't understand the setting
# (e.g. non-setuptools) simply ignore it.
_EDITABLE_STRICT = ["--config-settings", "editable_mode=strict"]

# Imports <module>.app when present (the MQTT/AMQP companion crash site), else
# the bare module. Never __main__.
SMOKE = (
    "import importlib, importlib.util as _u; "
    "_m = {mod!r}; "
    "importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"
)


def _cmd_module(arr: list) -> str | None:
    if not arr or arr[0] not in ("python", "python3"):
        return None
    if "-m" in arr:
        i = arr.index("-m")
        if i + 1 < len(arr):
            return arr[i + 1]
    return None


def dockerfile_modules(feeder: Path) -> list[str]:
    """Runtime module targets from every Dockerfile* CMD/ENTRYPOINT (python -m X)."""
    mods: list[str] = []
    for df in sorted(feeder.glob("Dockerfile*")):
        if not df.is_file():
            continue
        for line in df.read_text(encoding="utf-8", errors="replace").splitlines():
            m = CMD_RE.match(line)
            if not m:
                continue
            try:
                arr = json.loads(m.group(1))
            except json.JSONDecodeError:
                continue
            mod = _cmd_module(arr)
            if mod and mod not in mods:
                mods.append(mod)
    return mods


def install_order(feeder: Path) -> list[Path]:
    """Editable-install targets (dirs with a pyproject.toml) in dependency order:
    ``*_data`` -> ``*_core`` -> producers -> other sub-packages -> the main
    feeder package (installed last)."""

    def priority(p: Path) -> int:
        name = p.name
        if name.endswith("_data"):
            return 0
        if name.endswith("_core"):
            return 1
        if "producer" in name or name.endswith("_mqtt_client") or name.endswith("_amqp"):
            return 2
        return 3

    subs: set[Path] = set()
    for pp in feeder.glob("**/pyproject.toml"):
        d = pp.parent
        if d == feeder or SKIP_RE.search(str(d) + "/") or "tests" in d.parts:
            continue
        subs.add(d)
    ordered = sorted(subs, key=lambda d: (priority(d), d.as_posix()))
    # Append the top-level feeder dir as the main package **only** when it is
    # itself an installable Python project. Transport-split sources (e.g.
    # pegelonline, gbfs-bikeshare, tfl-cycles) have no aggregating top-level
    # pyproject.toml -- every installable unit is a sub-package already in
    # ``ordered`` -- so ``pip install -e feeders/<src>`` would fail with "does
    # not appear to be a Python project". Sources with a top-level pyproject
    # (e.g. hsl-hfp) still get it installed last.
    if (feeder / "pyproject.toml").exists():
        ordered = ordered + [feeder]
    return ordered


def _run(cmd: list) -> int:
    print("    $ " + " ".join(str(c) for c in cmd))
    return subprocess.run(cmd).returncode


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Feeder import smoke-test (postmortem P0a).")
    ap.add_argument("feeder", help="path to feeders/<source>")
    ap.add_argument("--plan", action="store_true",
                    help="compile + print the install/import plan, then stop")
    ap.add_argument("--install-only", action="store_true",
                    help="compile + ordered editable install, but do not import")
    ap.add_argument("--no-install", action="store_true",
                    help="compile + import, skipping the pip install step")
    ap.add_argument("--timeout", type=int, default=120,
                    help="per-import subprocess timeout in seconds (default 120)")
    args = ap.parse_args(argv)

    feeder = Path(args.feeder).resolve()
    if not feeder.is_dir():
        print(f"ERROR: not a directory: {feeder}", file=sys.stderr)
        return 2

    modules = dockerfile_modules(feeder)
    order = install_order(feeder)

    print(f"== import smoke: {feeder.name} ==")
    print("  install order (editable):")
    for d in order:
        print(f"    - {d.name}")
    print("  import targets (.app if present, else bare module; never __main__):")
    for m in modules:
        print(f"    - {m}")

    # Gate 2 (py_compile) always runs first.
    print("  py_compile feeder tree ...")
    if not compileall.compile_dir(str(feeder), quiet=1, maxlevels=30, rx=SKIP_RE):
        print("FAIL: py_compile reported errors", file=sys.stderr)
        return 1

    if args.plan:
        print("PLAN OK (compile passed; install + import skipped)")
        return 0

    if not args.no_install:
        # Pass 1: register every local editable package WITHOUT dependency
        # resolution. A transport app sub-package (e.g. ``<src>_mqtt``) often
        # declares the main feeder package (``<src>``) as a dependency; that
        # package is not on PyPI, so a single with-deps pass in priority order
        # fails ("No matching distribution found for <src>") because the main
        # package is installed last. Registering all locals first makes the
        # intra-feeder graph resolvable regardless of order.
        for d in order:
            if _run([sys.executable, "-m", "pip", "install", "--no-input",
                     "--no-deps", *_EDITABLE_STRICT, "-e", str(d)]) != 0:
                print(f"FAIL: pip install --no-deps -e {d}", file=sys.stderr)
                return 1
        # Pass 2: resolve external dependencies now that every local package is
        # already satisfied from the editable set above.
        for d in order:
            if _run([sys.executable, "-m", "pip", "install", "--no-input",
                     *_EDITABLE_STRICT, "-e", str(d)]) != 0:
                print(f"FAIL: pip install -e {d}", file=sys.stderr)
                return 1

    if args.install_only:
        print("INSTALL OK (imports skipped)")
        return 0

    if not modules:
        print("WARN: no Dockerfile 'python -m' target found; nothing to import",
              file=sys.stderr)
        return 0

    failures: list[str] = []
    for m in modules:
        code = SMOKE.format(mod=m)
        try:
            rc = subprocess.run([sys.executable, "-c", code], timeout=args.timeout).returncode
        except subprocess.TimeoutExpired:
            print(f"FAIL: import {m} timed out after {args.timeout}s "
                  f"(does it call main() at import time?)", file=sys.stderr)
            failures.append(m)
            continue
        if rc != 0:
            print(f"FAIL: import {m} (exit {rc})", file=sys.stderr)
            failures.append(m)
        else:
            print(f"  OK import {m}")

    if failures:
        print(f"FAIL: {len(failures)} import(s) failed: {', '.join(failures)}",
              file=sys.stderr)
        return 1
    print(f"PASS: {len(modules)} module(s) imported cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
