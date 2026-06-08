#!/usr/bin/env python3
"""Filter the Docker E2E matrix to feeders whose paths changed in a PR/push.

Inputs (env):
  CHANGED_FILES : newline-separated list of changed file paths.
  EVENT_NAME    : github.event_name (schedule forces full; see SCOPE).
  SCOPE         : manual override for workflow_dispatch: full / smoke / changed
                  (default full). Ignored for push/pull_request/schedule.
  BASE_SHA      : merge base SHA (optional; enables additive-infra scoping).
  HEAD_SHA      : head SHA (optional; defaults to HEAD).

Outputs (GITHUB_OUTPUT):
  build_matrix    : JSON object {include: [...]} (full, legacy/debug)
  flow_matrix     : JSON object {include: [...]} (full, legacy/debug)
  build_matrix_<n>: JSON object {include: [...]} per shard (0..SHARD_COUNT-1)
  flow_matrix_<n> : JSON object {include: [...]} per shard (0..SHARD_COUNT-1)
  full_run        : "true" or "false"
  reason          : short human-readable reason.

Run-scoping policy (the full 664-job matrix is expensive and, under runner
load, starves live-upstream flow tests into transient failures, so we reserve
it for the weekly scheduled run and on-demand dispatch):

  - schedule .............. FULL matrix (weekly authoritative gate).
  - workflow_dispatch ..... honours SCOPE (full | smoke | changed; default full).
  - push / pull_request ... change-scoped:
      * feeder dir changed -> just that feeder's build+flow jobs.
      * additive-safe infra (matrix.json / catalog.json / test_docker_*_flow.py
        purely additive) -> the newly-added feeders' jobs.
      * harness change (anything under tests/docker_e2e/** that is NOT
        additive-safe, the e2e workflow yml, the reusable shard ymls, or a
        non-additive catalog.json) -> the SMOKE set: a small curated,
        transport-spanning subset (entries flagged "smoke": true in
        matrix.json) that cheaply proves the harness still works across
        Kafka/MQTT/AMQP. Full feeder coverage for harness changes comes from
        the weekly scheduled run.
      * shared runtime patches that span more than 8 feeder dirs -> the
        SMOKE set, because broad live-upstream E2E runs are noisy and
        unstable for these shared patches.
      * nothing matched (e.g. tools/** or docs only) -> zero jobs (no-op);
        tools/** does not affect Docker E2E because images are built from the
        committed feeder code, not regenerated from tools/.
  - Always emit a `{include:[]}` shape so an empty selection still produces a
    valid (no-op) matrix.
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
MAX_SCOPED_FEEDER_DIRS = 8

# Anything under these paths is a test-harness change: it invalidates
# per-feeder scoping because it can affect every feeder's E2E run. A
# non-additive change here triggers the SMOKE set (not the full matrix) on
# push/PR; the weekly scheduled run provides full coverage. Note: tools/** is
# deliberately NOT here -- Docker E2E builds images from committed feeder code
# and never regenerates producers from tools/, so tool changes need no E2E.
INFRA_PATTERNS = [
    re.compile(r"^tests/docker_e2e/"),
    re.compile(r"^\.github/workflows/test-docker-e2e\.yml$"),
    re.compile(r"^\.github/workflows/_docker-build-shard\.yml$"),
    re.compile(r"^\.github/workflows/_docker-flow-shard\.yml$"),
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
        # Include any class-level decorators (which precede ``node.lineno``)
        # in the hashed span so a decorator-only change (e.g. adding
        # @pytest.mark.skip) registers as a class-body change rather than
        # silently slipping past both this hash and the non-class hash.
        start = min([node.lineno] + [d.lineno for d in node.decorator_list]) - 1
        end = getattr(node, "end_lineno", None) or start + 1
        body = "".join(lines[start:end])
        out[node.name] = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return out


def _module_nonclass_hash(text: str) -> str | None:
    """Hash of all top-level statements that are NOT class definitions.

    Returns None if the source cannot be parsed. Used to prove that a change
    to a test file is confined to test-class bodies and does not touch shared
    module-level code (imports, fixtures, helper functions) that could affect
    every feeder's E2E run.
    """
    import ast

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None
    lines = text.splitlines(keepends=True)
    segments: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            continue
        start = node.lineno - 1
        end = getattr(node, "end_lineno", None) or start + 1
        segments.append("".join(lines[start:end]))
    return hashlib.sha256("\x00".join(segments).encode("utf-8")).hexdigest()


def additive_test_file(base_txt: str, head_txt: str, matrix: dict) -> list[str] | None:
    """Scope a Docker-E2E test-file change to the affected feeder dirs.

    Returns the list of feeder dirs whose flow jobs should run, or None to
    signal the change cannot be attributed to specific feeders (the caller
    then falls back to the smoke set).

    A change is attributable when it is confined to test-class bodies and
    every added/modified class maps to a feeder dir via the matrix. It bails
    (None) when shared module-level code changed (imports, fixtures, helper
    functions), when an existing class was removed, or when a *modified*
    existing class has no matrix mapping (e.g. a shared base class) -- any of
    which can affect feeders we cannot enumerate from the class alone. This
    lets a PR that flips one feeder's own test class to ``--mock`` run that
    feeder's flow job instead of the whole smoke set.
    """
    # Shared, non-class module-level code must be byte-identical; otherwise a
    # changed import / fixture / helper could affect every feeder's run.
    base_shared = _module_nonclass_hash(base_txt)
    head_shared = _module_nonclass_hash(head_txt)
    if base_shared is None or head_shared is None or base_shared != head_shared:
        return None

    base_classes = _class_blocks(base_txt)
    head_classes = _class_blocks(head_txt)
    # No removals of existing classes (a deletion may alter shared behavior).
    for cls in base_classes:
        if cls not in head_classes:
            return None

    # Map test_class -> dir via matrix entries.
    cls_to_dir = {}
    for entry in matrix.get("flow", []):
        tc = entry.get("test_class")
        d = entry.get("dir")
        if tc and d:
            cls_to_dir[tc] = d

    touched: set[str] = set()
    for cls, head_hash in head_classes.items():
        base_hash = base_classes.get(cls)
        if base_hash is None:
            # Newly added class: additive. Attribute to its feeder if mapped;
            # an unmapped new class selects no job (matches the prior add-only
            # behavior -- nothing references it yet, so it is safe).
            d = cls_to_dir.get(cls)
            if d:
                touched.add(d)
        elif base_hash != head_hash:
            # Modified existing class body. Attribute to its feeder dir. A
            # modified class that is NOT a flow-matrix entry is a shared base
            # class whose change can affect many feeders -> cannot scope.
            d = cls_to_dir.get(cls)
            if d is None:
                return None
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
    scope = os.environ.get("SCOPE", "").strip().lower()
    base_sha = os.environ.get("BASE_SHA", "").strip()
    changed = _load_changed_files()

    force_full = False
    smoke = False
    reason = ""

    if event == "schedule":
        force_full = True
        reason = "scheduled run: full weekly matrix"
    elif event == "workflow_dispatch":
        # Manual dispatch honours the SCOPE input (default full).
        if scope == "smoke":
            smoke = True
            reason = "manual dispatch: smoke scope"
        elif scope == "changed":
            reason = "manual dispatch: changed scope"
        else:
            force_full = True
            reason = "manual dispatch: full scope"
    elif not changed:
        # No diff to scope from (e.g. first push of a branch); be safe with
        # the smoke set rather than the full matrix on push/PR.
        smoke = True
        reason = "no changed files detected, running smoke set"

    extra_dirs: set[str] = set()
    if not force_full and not smoke and event not in ("schedule", "workflow_dispatch"):
        infra_hits = [p for p in changed if is_infra(p)]
        if infra_hits:
            additive_paths = [p for p in infra_hits if is_additive_candidate(p)]
            hard_infra = [p for p in infra_hits if not is_additive_candidate(p)]
            if hard_infra:
                # Non-additive harness change: run the smoke set on push/PR.
                # The weekly scheduled run covers the full feeder matrix.
                smoke = True
                reason = (
                    "harness paths changed, running smoke set: "
                    + ", ".join(hard_infra[:5])
                )
            elif additive_paths and base_sha:
                extra, blockers = scope_additive_infra(
                    additive_paths, base_sha, matrix
                )
                if blockers:
                    smoke = True
                    reason = (
                        "infra changes not provably additive, running smoke set: "
                        + ", ".join(blockers[:5])
                    )
                else:
                    extra_dirs.update(extra)
            elif additive_paths and not base_sha:
                smoke = True
                reason = (
                    "infra paths changed and no BASE_SHA to verify additive, "
                    "running smoke set: " + ", ".join(additive_paths[:5])
                )

    touched_dirs = {top_dir(p) for p in changed if not is_infra(p)}
    touched_dirs.update(extra_dirs)

    if force_full:
        build = matrix["build"]
        flow = matrix["flow"]
    elif smoke:
        build = [m for m in matrix["build"] if m.get("smoke")]
        flow = [m for m in matrix["flow"] if m.get("smoke")]
        reason = (
            f"{reason} -> {len(build)} build / {len(flow)} flow smoke job(s)"
        )
    else:
        if len(touched_dirs) > MAX_SCOPED_FEEDER_DIRS:
            smoke = True
            build = [m for m in matrix["build"] if m.get("smoke")]
            flow = [m for m in matrix["flow"] if m.get("smoke")]
            reason = (
                f"shared runtime change spans {len(touched_dirs)} feeder dirs; "
                "running smoke set instead of live-upstream E2E for every touched feeder "
                f"-> {len(build)} build / {len(flow)} flow smoke job(s)"
            )
        else:
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
