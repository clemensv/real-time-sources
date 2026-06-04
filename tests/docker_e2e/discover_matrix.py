#!/usr/bin/env python3
"""Filter the Docker E2E matrix to feeders whose paths changed in a PR/push.

Inputs (env):
  CHANGED_FILES : newline-separated list of changed file paths.
  EVENT_NAME    : github.event_name (workflow_dispatch / schedule force full).
  BASE_SHA      : merge base SHA (optional; enables additive-infra scoping).
  HEAD_SHA      : head SHA (optional; defaults to HEAD).

Outputs (GITHUB_OUTPUT):
  build_matrix    : JSON object {include: [...]} (full, legacy/debug)
  flow_matrix     : JSON object {include: [...]} (full, legacy/debug)
  build_matrix_<n>: JSON object {include: [...]} per shard (0..SHARD_COUNT-1)
  flow_matrix_<n> : JSON object {include: [...]} per shard (0..SHARD_COUNT-1)
  full_run        : "true" or "false"
  reason          : short human-readable reason.

Logic:
  - If event is workflow_dispatch/schedule, or any changed file matches an
    INFRA path that is NOT additive-safe, emit the full matrix.
  - Else compute the set of top-level dirs touched; intersect with the
    matrix `dir` fields; emit only those entries.
  - Additive-safe infra files (matrix.json, catalog.json,
    test_docker_*_flow.py) contribute their newly-added source dirs to the
    scoped set when the diff is purely additive (existing entries
    unchanged); otherwise they force the full run.
  - Always emit a `{include:[]}` shape so an empty selection still produces
    a valid (no-op) matrix.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX_PATH = ROOT / "tests" / "docker_e2e" / "matrix.json"

# GitHub Actions hard-limits a single matrix to 256 jobs. The full feeder
# matrix (build + flow) has outgrown that, so on a force_full run the matrix
# can no longer instantiate as one strategy. We therefore split each section
# into a fixed number of shards and emit one matrix output per shard
# (build_matrix_0..N-1 / flow_matrix_0..N-1); the workflow fans these out to
# parallel reusable-workflow calls. Entries fill shards sequentially up to
# SHARD_CAP so that scoped (few-feeder) runs stay compact in shard 0 and only
# spill into later shards when the full matrix runs.
SHARD_COUNT = 4
SHARD_CAP = 250  # < 256 GitHub limit, leaves headroom inside each shard

# Anything under these paths invalidates per-feeder scoping and forces full
# run UNLESS the change is purely additive (handled per-file below).
INFRA_PATTERNS = [
    re.compile(r"^tests/docker_e2e/"),
    re.compile(r"^\.github/workflows/test-docker-e2e\.yml$"),
    re.compile(r"^tools/"),
    re.compile(r"^catalog\.json$"),
]

# Subset of infra paths that may be additive-safe (parsed for structured diff).
ADDITIVE_INFRA_FILES = {
    "catalog.json",
    "tests/docker_e2e/matrix.json",
}
ADDITIVE_TEST_FILE_RE = re.compile(r"^tests/docker_e2e/test_docker_\w+_flow\.py$")

# Catalog flags that may flip false -> true additively without forcing full run.
ADDITIVE_BOOL_FLAGS = {"mqtt", "amqp", "kql", "notebook"}


def is_infra(path: str) -> bool:
    return any(p.search(path) for p in INFRA_PATTERNS)


def is_additive_candidate(path: str) -> bool:
    return path in ADDITIVE_INFRA_FILES or bool(ADDITIVE_TEST_FILE_RE.match(path))


def top_dir(path: str) -> str:
    parts = path.split("/")
    if len(parts) >= 2 and parts[0] == "feeders":
        # matrix.json entries use dir="feeders/<name>" (since feeders were
        # moved under feeders/), so we must return the same prefixed form for
        # the scoped filter `m["dir"] in touched_dirs` to match. Returning the
        # bare name silently scoped every feeder change to zero jobs.
        return f"feeders/{parts[1]}"
    return parts[0]


def emit(name: str, value: str) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            if "\n" in value:
                delim = "EOF_MATRIX_OUT"
                fh.write(f"{name}<<{delim}\n{value}\n{delim}\n")
            else:
                fh.write(f"{name}={value}\n")
    print(f"::notice::{name}={value[:200]}{'…' if len(value) > 200 else ''}")


def git_show(sha: str, path: str) -> str | None:
    if not sha:
        return None
    try:
        return subprocess.check_output(
            ["git", "show", f"{sha}:{path}"], text=True, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        return None


def read_head(path: str) -> str | None:
    p = ROOT / path
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8")


def additive_catalog(base_txt: str, head_txt: str) -> list[str] | None:
    """Return list of source ids whose row was added or had flags flipped
    false->true; None if the diff is not additive-safe."""
    try:
        base = json.loads(base_txt)
        head = json.loads(head_txt)
    except json.JSONDecodeError:
        return None
    base_by_id = {s.get("id"): s for s in base if isinstance(s, dict)}
    head_by_id = {s.get("id"): s for s in head if isinstance(s, dict)}
    if not base_by_id or not head_by_id:
        return None
    # No removals allowed.
    if set(base_by_id) - set(head_by_id):
        return None
    touched: list[str] = []
    for sid, head_row in head_by_id.items():
        base_row = base_by_id.get(sid)
        if base_row is None:
            touched.append(sid)
            continue
        # Walk every key; existing rows may only flip ADDITIVE_BOOL_FLAGS false->true.
        keys = set(base_row) | set(head_row)
        flipped = False
        for k in keys:
            bv = base_row.get(k)
            hv = head_row.get(k)
            if bv == hv:
                continue
            if k in ADDITIVE_BOOL_FLAGS and bv in (False, None) and hv is True:
                flipped = True
                continue
            # Any other field change disqualifies additive scoping.
            return None
        if flipped:
            touched.append(sid)
    return touched


def additive_matrix(base_txt: str, head_txt: str) -> list[str] | None:
    try:
        base = json.loads(base_txt)
        head = json.loads(head_txt)
    except json.JSONDecodeError:
        return None

    def key(entry: dict) -> tuple:
        return (
            entry.get("dir"),
            entry.get("image"),
            entry.get("file"),
            entry.get("test_class"),
            entry.get("module"),
            entry.get("test_file"),
        )

    touched: set[str] = set()
    for section in ("build", "flow"):
        base_entries = base.get(section, []) if isinstance(base, dict) else []
        head_entries = head.get(section, []) if isinstance(head, dict) else []
        base_keys = {key(e): e for e in base_entries if isinstance(e, dict)}
        head_keys = {key(e): e for e in head_entries if isinstance(e, dict)}
        # No removals or modifications of existing entries.
        for k, base_e in base_keys.items():
            if k not in head_keys:
                return None
            if json.dumps(base_e, sort_keys=True) != json.dumps(
                head_keys[k], sort_keys=True
            ):
                return None
        for k, head_e in head_keys.items():
            if k not in base_keys:
                d = head_e.get("dir")
                if d:
                    touched.add(d)
    return sorted(touched)


def _class_blocks(text: str) -> dict[str, str]:
    """Map class_name -> hash(class source) for top-level test classes.

    Uses AST so adding helper code or new classes between existing classes
    does not look like a body change to those classes.
    """
    import ast

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return {}
    lines = text.splitlines(keepends=True)
    out: dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        start = node.lineno - 1
        end = getattr(node, "end_lineno", None) or start + 1
        body = "".join(lines[start:end])
        out[node.name] = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return out


def additive_test_file(base_txt: str, head_txt: str, matrix: dict) -> list[str] | None:
    base_classes = _class_blocks(base_txt)
    head_classes = _class_blocks(head_txt)
    # No removals or body changes of existing classes.
    for cls, base_hash in base_classes.items():
        if cls not in head_classes or head_classes[cls] != base_hash:
            return None
    # Map test_class -> dir via matrix entries.
    cls_to_dir = {}
    for entry in matrix.get("flow", []):
        tc = entry.get("test_class")
        d = entry.get("dir")
        if tc and d:
            cls_to_dir[tc] = d
    touched: set[str] = set()
    for cls in set(head_classes) - set(base_classes):
        d = cls_to_dir.get(cls)
        if d:
            touched.add(d)
    return sorted(touched)


def scope_additive_infra(
    paths: list[str], base_sha: str, matrix: dict
) -> tuple[set[str], list[str]]:
    """Return (extra_touched_dirs, blocking_paths). Blocking paths force full."""
    extra: set[str] = set()
    blockers: list[str] = []
    for path in paths:
        base_txt = git_show(base_sha, path)
        head_txt = read_head(path)
        if base_txt is None or head_txt is None:
            blockers.append(path)
            continue
        if path == "catalog.json":
            ids = additive_catalog(base_txt, head_txt)
            if ids is None:
                blockers.append(path)
            else:
                extra.update(ids)
        elif path == "tests/docker_e2e/matrix.json":
            dirs = additive_matrix(base_txt, head_txt)
            if dirs is None:
                blockers.append(path)
            else:
                extra.update(dirs)
        elif ADDITIVE_TEST_FILE_RE.match(path):
            dirs = additive_test_file(base_txt, head_txt, matrix)
            if dirs is None:
                blockers.append(path)
            else:
                extra.update(dirs)
        else:
            blockers.append(path)
    return extra, blockers


def _load_changed_files() -> list[str]:
    path = os.environ.get("CHANGED_FILES_PATH", "").strip()
    if path and os.path.isfile(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            raw = fh.read()
    else:
        raw = os.environ.get("CHANGED_FILES", "")
    return [line.strip() for line in raw.splitlines() if line.strip()]


def shard_entries(entries: list) -> list[list]:
    """Split entries into SHARD_COUNT shards, filling sequentially up to
    SHARD_CAP per shard so scoped runs stay in shard 0. Raises if the total
    exceeds the total capacity (SHARD_COUNT * SHARD_CAP), which signals that
    SHARD_COUNT must be increased (and matching jobs added to the workflow)."""
    shards: list[list] = [[] for _ in range(SHARD_COUNT)]
    for i, entry in enumerate(entries):
        idx = i // SHARD_CAP
        if idx >= SHARD_COUNT:
            raise SystemExit(
                f"[discover] matrix section has {len(entries)} entries, "
                f"exceeding capacity {SHARD_COUNT * SHARD_CAP} "
                f"(SHARD_COUNT={SHARD_COUNT} x SHARD_CAP={SHARD_CAP}). "
                f"Increase SHARD_COUNT and add matching shard jobs to "
                f"test-docker-e2e.yml."
            )
        shards[idx].append(entry)
    return shards


def main() -> int:
    matrix = json.loads(MATRIX_PATH.read_text())
    event = os.environ.get("EVENT_NAME", "")
    base_sha = os.environ.get("BASE_SHA", "").strip()
    changed = _load_changed_files()

    force_full = event in ("workflow_dispatch", "schedule") or not changed
    reason = (
        f"event={event}, force full"
        if event in ("workflow_dispatch", "schedule")
        else "no changed files detected, force full"
        if not changed
        else ""
    )

    extra_dirs: set[str] = set()
    if not force_full:
        infra_hits = [p for p in changed if is_infra(p)]
        if infra_hits:
            additive_paths = [p for p in infra_hits if is_additive_candidate(p)]
            hard_infra = [p for p in infra_hits if not is_additive_candidate(p)]
            if hard_infra:
                force_full = True
                reason = f"infra paths changed: {', '.join(hard_infra[:5])}"
            elif additive_paths and base_sha:
                extra, blockers = scope_additive_infra(
                    additive_paths, base_sha, matrix
                )
                if blockers:
                    force_full = True
                    reason = (
                        "infra changes not provably additive: "
                        + ", ".join(blockers[:5])
                    )
                else:
                    extra_dirs.update(extra)
            elif additive_paths and not base_sha:
                force_full = True
                reason = (
                    "infra paths changed and no BASE_SHA to verify additive: "
                    + ", ".join(additive_paths[:5])
                )

    if force_full:
        build = matrix["build"]
        flow = matrix["flow"]
    else:
        touched_dirs = {top_dir(p) for p in changed if not is_infra(p)}
        touched_dirs.update(extra_dirs)
        build = [m for m in matrix["build"] if m["dir"] in touched_dirs]
        flow = [m for m in matrix["flow"] if m["dir"] in touched_dirs]
        reason = (
            f"scoped to {len(build)} build / {len(flow)} flow job(s): "
            f"{', '.join(sorted(touched_dirs))[:200]}"
        )

    emit("full_run", "true" if force_full else "false")
    emit("reason", reason)
    # Legacy single-matrix outputs (kept for debugging / external consumers).
    emit("build_matrix", json.dumps({"include": build}))
    emit("flow_matrix", json.dumps({"include": flow}))
    # Sharded outputs consumed by the workflow (build_matrix_<n> / flow_matrix_<n>).
    for n, chunk in enumerate(shard_entries(build)):
        emit(f"build_matrix_{n}", json.dumps({"include": chunk}))
    for n, chunk in enumerate(shard_entries(flow)):
        emit(f"flow_matrix_{n}", json.dumps({"include": chunk}))

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
