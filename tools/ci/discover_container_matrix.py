#!/usr/bin/env python3
"""Filter the Build Containers matrix to sources whose paths changed.

Inputs (env):
  CHANGED_FILES : newline-separated list of changed file paths.
  EVENT_NAME    : github.event_name (workflow_dispatch / schedule / tag push
                  force full).
  REF_TYPE      : github.ref_type ('tag' forces full).
  ALL_BASE_JSON : JSON array of {path, file, image} for plain Dockerfiles.
  ALL_TRANSPORT_JSON : JSON array of {path, file, image, variant} for
                       Dockerfile.<variant>.

Outputs (GITHUB_OUTPUT):
  containers_base      : JSON array, filtered.
  containers_transport : JSON array, filtered.
  full_run             : "true" | "false".
  reason               : short human-readable reason.

Scoping rule:
  - Force full if: workflow_dispatch, schedule, tag push, no changed files,
    OR any change touches a path NOT clearly inside a single source dir
    (.github/, tools/, tests/, or any repo-root file).
  - Otherwise: keep only matrix entries whose `path` top-level dir is in the
    set of touched source dirs.
"""
from __future__ import annotations

import json
import os
import re
import sys

INFRA_PATTERNS = [
    re.compile(r"^\.github/workflows/build_containers\.yml$"),
    re.compile(r"^\.github/workflows/docker[-_].*\.ya?ml$"),
    re.compile(r"^\.github/actions/"),
    re.compile(r"^tools/ci/"),
    re.compile(r"^tests/docker_e2e/"),
    re.compile(r"^Dockerfile($|\.)"),
    re.compile(r"^requirements.*\.txt$"),
    re.compile(r"^pyproject\.toml$"),
    re.compile(r"^poetry\.lock$"),
]


def is_infra(path: str) -> bool:
    return any(p.search(path) for p in INFRA_PATTERNS)


def top_dir(path: str) -> str:
    return path.split("/", 1)[0]


def emit(name: str, value: str) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            if "\n" in value:
                delim = "EOF_DISCOVER"
                fh.write(f"{name}<<{delim}\n{value}\n{delim}\n")
            else:
                fh.write(f"{name}={value}\n")
    print(f"::notice::{name}={value[:200]}{'…' if len(value) > 200 else ''}")


def main() -> int:
    event = os.environ.get("EVENT_NAME", "")
    ref_type = os.environ.get("REF_TYPE", "")
    changed = [
        line.strip()
        for line in os.environ.get("CHANGED_FILES", "").splitlines()
        if line.strip()
    ]
    base = json.loads(os.environ.get("ALL_BASE_JSON", "[]"))
    transport = json.loads(os.environ.get("ALL_TRANSPORT_JSON", "[]"))

    force_full = False
    reason = ""

    if event in ("workflow_dispatch", "schedule"):
        force_full = True
        reason = f"event={event}"
    elif ref_type == "tag":
        force_full = True
        reason = "tag push"
    elif not changed:
        force_full = True
        reason = "no changed files"
    else:
        infra_hits = [p for p in changed if is_infra(p)]
        if infra_hits:
            force_full = True
            reason = f"infra paths changed: {', '.join(infra_hits[:5])}"

    if force_full:
        emit("full_run", "true")
        emit("reason", reason)
        emit("containers_base", json.dumps(base))
        emit("containers_transport", json.dumps(transport))
        print(
            f"[discover] full_run=true reason={reason} "
            f"base={len(base)} transport={len(transport)}",
            file=sys.stderr,
        )
        return 0

    touched_dirs = {top_dir(p) for p in changed}
    base_f = [c for c in base if top_dir(c["path"]) in touched_dirs]
    transport_f = [c for c in transport if top_dir(c["path"]) in touched_dirs]
    reason = (
        f"scoped to {len(base_f)} base / {len(transport_f)} transport image(s): "
        f"{', '.join(sorted(touched_dirs))[:200]}"
    )
    emit("full_run", "false")
    emit("reason", reason)
    emit("containers_base", json.dumps(base_f))
    emit("containers_transport", json.dumps(transport_f))
    print(
        f"[discover] full_run=false reason={reason} "
        f"base={len(base_f)} transport={len(transport_f)}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
