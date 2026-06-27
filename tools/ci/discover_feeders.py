#!/usr/bin/env python3
"""Emit a change-scoped feeder matrix for the fast CI gates (import-smoke,
feeder-tests).

Maps changed files to ``feeders/<source>`` directories and escalates to the
full feeder set when a fleet-wide path changes (shared tooling, workflows,
the Docker E2E harness, or a root build/lint config) -- because a change there
can break any feeder, not just the ones whose own files changed. This mirrors
the fleet-escalation rule in ``tests/docker_e2e/discover_matrix.py``.

Changed files are read (in priority order) from positional args, a
``--changed-file=<path>`` newline list, or the ``CHANGED_FILES`` env var
(newline-separated). Writes ``matrix``, ``count`` and ``empty`` to
``$GITHUB_OUTPUT`` and prints a human-readable summary.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
FEEDERS = REPO / "feeders"

# A change to any of these invalidates per-feeder scoping -> run the whole fleet.
FLEET_PATTERNS = [
    re.compile(r"^tools/"),
    re.compile(r"^\.github/workflows/"),
    re.compile(r"^tests/docker_e2e/"),
    re.compile(r"^(pyproject\.toml|poetry\.lock|mypy\.ini|requirements[^/]*\.txt)$"),
]
# More than this many distinct feeders touched -> just run them all.
MAX_SCOPED = 25


def _is_feeder(d: Path) -> bool:
    # A feeder dir has a pyproject.toml; underscore-prefixed dirs (e.g.
    # `_poller_core`) are shared libraries, not feeders, and must not enter
    # the matrix.
    return (d.is_dir() and not d.name.startswith("_")
            and (d / "pyproject.toml").exists())


def all_feeders() -> list[str]:
    if not FEEDERS.is_dir():
        return []
    return sorted(d.name for d in FEEDERS.iterdir() if _is_feeder(d))


def read_changed(argv: list[str]) -> list[str]:
    files: list[str] = []
    for a in argv:
        if a.startswith("--changed-file="):
            p = Path(a.split("=", 1)[1])
            if p.exists():
                files += p.read_text(encoding="utf-8").splitlines()
        elif not a.startswith("-"):
            files.append(a)
    if not files:
        files = os.environ.get("CHANGED_FILES", "").splitlines()
    return [f.strip().replace("\\", "/") for f in files if f.strip()]


def main(argv: list[str]) -> int:
    files = read_changed(argv)
    fleet = any(p.search(f) for f in files for p in FLEET_PATTERNS)

    scoped: set[str] = set()
    for f in files:
        m = re.match(r"^feeders/([^/]+)/", f)
        if m and _is_feeder(FEEDERS / m.group(1)):
            scoped.add(m.group(1))

    if fleet:
        feeders, reason = all_feeders(), "fleet-wide change -> full fleet"
    elif len(scoped) > MAX_SCOPED:
        feeders, reason = all_feeders(), f">{MAX_SCOPED} feeders touched -> full fleet"
    else:
        feeders, reason = sorted(scoped), "scoped"

    matrix = {"feeder": feeders}
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(f"matrix={json.dumps(matrix)}\n")
            fh.write(f"count={len(feeders)}\n")
            fh.write(f"empty={'true' if not feeders else 'false'}\n")

    print(f"discover_feeders: {reason}; {len(feeders)} feeder(s)")
    for f in feeders:
        print(f"  - {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
