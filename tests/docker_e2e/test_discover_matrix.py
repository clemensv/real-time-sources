"""Regression tests for tests/docker_e2e/discover_matrix.py scoping.

Guards against the prefix-mismatch bug where ``top_dir`` returned the bare
feeder name (``aisstream``) while ``matrix.json`` entries use the prefixed
form (``feeders/aisstream``), causing every scoped feeder change to select
zero build/flow jobs and silently pass the Docker E2E gate.
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "discover_matrix.py"
MATRIX_PATH = HERE / "matrix.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("discover_matrix", MODULE_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


dm = _load_module()


def _parse_github_output(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    vals: dict[str, str] = {}
    multi = re.compile(r"^(\w+)<<EOF_MATRIX_OUT\n(.*?)\nEOF_MATRIX_OUT$", re.S | re.M)
    for m in multi.finditer(text):
        vals[m.group(1)] = m.group(2)
    for line in text.splitlines():
        if "<<" in line or line.startswith("EOF_MATRIX_OUT"):
            continue
        if "=" in line and not line.startswith("{"):
            k, _, v = line.partition("=")
            vals.setdefault(k, v)
    return vals


def test_top_dir_returns_feeders_prefixed_name():
    # matrix.json dir entries are "feeders/<name>"; top_dir must match.
    assert dm.top_dir("feeders/aisstream/aisstream/aisstream.py") == "feeders/aisstream"
    assert dm.top_dir("feeders/dwd/Dockerfile") == "feeders/dwd"
    # Non-feeder paths are returned as their first segment.
    assert dm.top_dir("tools/ci/foo.py") == "tools"


def test_top_dir_matches_matrix_dir_format():
    matrix = json.loads(MATRIX_PATH.read_text())
    sample = matrix["build"][0]["dir"]  # e.g. "feeders/aisstream"
    feeder = sample.split("/", 1)[1]
    assert dm.top_dir(f"{sample}/{feeder}/{feeder}.py") == sample


def test_scoped_change_selects_that_feeders_jobs(tmp_path, monkeypatch):
    matrix = json.loads(MATRIX_PATH.read_text())
    target = matrix["build"][0]["dir"]  # "feeders/<name>"
    feeder = target.split("/", 1)[1]
    changed = f"{target}/{feeder}/{feeder}.py"

    out = tmp_path / "gh_output"
    out.write_text("", encoding="utf-8")
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    monkeypatch.setenv("EVENT_NAME", "push")
    monkeypatch.setenv("CHANGED_FILES", changed)
    monkeypatch.delenv("CHANGED_FILES_PATH", raising=False)

    assert dm.main() == 0

    vals = _parse_github_output(out)
    assert vals["full_run"] == "false"
    build = json.loads(vals["build_matrix"])["include"]
    flow = json.loads(vals["flow_matrix"])["include"]

    expected_build = [m for m in matrix["build"] if m["dir"] == target]
    expected_flow = [m for m in matrix["flow"] if m["dir"] == target]

    assert build == expected_build
    assert flow == expected_flow
    # The whole point: a real feeder change must select at least one job.
    assert build, "scoped feeder change selected zero build jobs"
    assert all(m["dir"] == target for m in build)
    assert all(m["dir"] == target for m in flow)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
