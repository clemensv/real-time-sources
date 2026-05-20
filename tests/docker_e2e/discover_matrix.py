#!/usr/bin/env python3
"""Filter the Docker E2E matrix to feeders whose paths changed in a PR/push.

Inputs (env):
  CHANGED_FILES : newline-separated list of changed file paths.
  EVENT_NAME    : github.event_name (workflow_dispatch / schedule force full).

Outputs (GITHUB_OUTPUT):
  build_matrix  : JSON object {include: [...]}
  flow_matrix   : JSON object {include: [...]}
  full_run      : "true" or "false"
  reason        : short human-readable reason.

Logic:
  - If event is workflow_dispatch/schedule, or any changed file matches an
    INFRA path, emit the full matrix.
  - Else compute the set of top-level dirs touched; intersect with the
    matrix `dir` fields; emit only those entries.
  - Always emit a `{include:[]}` shape so an empty selection still produces
    a valid (no-op) matrix.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX_PATH = ROOT / "tests" / "docker_e2e" / "matrix.json"

# Anything under these paths invalidates per-feeder scoping and forces full run.
INFRA_PATTERNS = [
    re.compile(r"^tests/docker_e2e/"),
    re.compile(r"^\.github/workflows/test-docker-e2e\.yml$"),
    re.compile(r"^tools/"),
    re.compile(r"^catalog\.json$"),
]


def is_infra(path: str) -> bool:
    return any(p.search(path) for p in INFRA_PATTERNS)


def top_dir(path: str) -> str:
    return path.split("/", 1)[0] if "/" in path else path


def emit(name: str, value: str) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            if "\n" in value:
                # multi-line via heredoc-style delimiter
                delim = "EOF_MATRIX_OUT"
                fh.write(f"{name}<<{delim}\n{value}\n{delim}\n")
            else:
                fh.write(f"{name}={value}\n")
    print(f"::notice::{name}={value[:200]}{'…' if len(value) > 200 else ''}")


def main() -> int:
    matrix = json.loads(MATRIX_PATH.read_text())
    event = os.environ.get("EVENT_NAME", "")
    changed = [
        line.strip()
        for line in os.environ.get("CHANGED_FILES", "").splitlines()
        if line.strip()
    ]

    force_full = event in ("workflow_dispatch", "schedule") or not changed
    reason = (
        f"event={event}, force full"
        if event in ("workflow_dispatch", "schedule")
        else "no changed files detected, force full"
        if not changed
        else ""
    )

    if not force_full:
        infra_hits = [p for p in changed if is_infra(p)]
        if infra_hits:
            force_full = True
            reason = f"infra paths changed: {', '.join(infra_hits[:5])}"

    if force_full:
        build = matrix["build"]
        flow = matrix["flow"]
    else:
        touched_dirs = {top_dir(p) for p in changed}
        build = [m for m in matrix["build"] if m["dir"] in touched_dirs]
        flow = [m for m in matrix["flow"] if m["dir"] in touched_dirs]
        reason = (
            f"scoped to {len(build)} build / {len(flow)} flow job(s): "
            f"{', '.join(sorted(touched_dirs))[:200]}"
        )

    emit("full_run", "true" if force_full else "false")
    emit("reason", reason)
    emit("build_matrix", json.dumps({"include": build}))
    emit("flow_matrix", json.dumps({"include": flow}))

    print(f"[discover] full_run={force_full} reason={reason}", file=sys.stderr)
    print(
        f"[discover] selected build={[m['dir'] for m in build]}",
        file=sys.stderr,
    )
    print(
        f"[discover] selected flow={[m['dir'] for m in flow]}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
