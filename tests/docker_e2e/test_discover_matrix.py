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


def _run(monkeypatch, tmp_path, *, event, changed="", scope=None, base=None):
    out = tmp_path / "gh_output"
    out.write_text("", encoding="utf-8")
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    monkeypatch.setenv("EVENT_NAME", event)
    monkeypatch.setenv("CHANGED_FILES", changed)
    monkeypatch.delenv("CHANGED_FILES_PATH", raising=False)
    if scope is None:
        monkeypatch.delenv("SCOPE", raising=False)
    else:
        monkeypatch.setenv("SCOPE", scope)
    if base is None:
        monkeypatch.delenv("BASE_SHA", raising=False)
    else:
        monkeypatch.setenv("BASE_SHA", base)
    assert dm.main() == 0
    vals = _parse_github_output(out)
    return (
        vals,
        json.loads(vals["build_matrix"])["include"],
        json.loads(vals["flow_matrix"])["include"],
    )


def test_tools_change_selects_zero_jobs(tmp_path, monkeypatch):
    # tools/** does not affect Docker E2E (images build from committed feeder
    # code, not from tools/), so a tools-only change must run no E2E jobs and
    # must NOT escalate to the full matrix.
    vals, build, flow = _run(
        monkeypatch, tmp_path, event="push", changed="tools/deploy/build_wheel.py"
    )
    assert vals["full_run"] == "false"
    assert build == []
    assert flow == []


def test_docs_change_selects_zero_jobs(tmp_path, monkeypatch):
    vals, build, flow = _run(
        monkeypatch, tmp_path, event="push", changed="docs/readme.md"
    )
    assert vals["full_run"] == "false"
    assert build == [] and flow == []


def test_harness_change_runs_smoke_set(tmp_path, monkeypatch):
    matrix = json.loads(MATRIX_PATH.read_text())
    smoke_build = [m for m in matrix["build"] if m.get("smoke")]
    smoke_flow = [m for m in matrix["flow"] if m.get("smoke")]
    assert smoke_build and smoke_flow, "matrix.json must define a smoke set"
    vals, build, flow = _run(
        monkeypatch, tmp_path, event="push", changed="tests/docker_e2e/conftest.py"
    )
    assert vals["full_run"] == "false"
    assert build == smoke_build
    assert flow == smoke_flow


def test_shard_workflow_change_runs_smoke_set(tmp_path, monkeypatch):
    vals, build, flow = _run(
        monkeypatch,
        tmp_path,
        event="push",
        changed=".github/workflows/_docker-flow-shard.yml",
    )
    assert vals["full_run"] == "false"
    assert all(m.get("smoke") for m in build)
    assert build, "shard-workflow change must run the smoke set"


def test_schedule_forces_full(tmp_path, monkeypatch):
    matrix = json.loads(MATRIX_PATH.read_text())
    vals, build, flow = _run(monkeypatch, tmp_path, event="schedule")
    assert vals["full_run"] == "true"
    assert len(build) == len(matrix["build"])
    assert len(flow) == len(matrix["flow"])


def test_dispatch_default_full(tmp_path, monkeypatch):
    matrix = json.loads(MATRIX_PATH.read_text())
    # No scope input -> default full.
    vals, build, _ = _run(monkeypatch, tmp_path, event="workflow_dispatch", scope="")
    assert vals["full_run"] == "true"
    assert len(build) == len(matrix["build"])


def test_dispatch_smoke_scope(tmp_path, monkeypatch):
    vals, build, flow = _run(
        monkeypatch, tmp_path, event="workflow_dispatch", scope="smoke"
    )
    assert vals["full_run"] == "false"
    assert build and all(m.get("smoke") for m in build)
    assert flow and all(m.get("smoke") for m in flow)


def test_dispatch_changed_scope(tmp_path, monkeypatch):
    matrix = json.loads(MATRIX_PATH.read_text())
    target = matrix["build"][0]["dir"]
    feeder = target.split("/", 1)[1]
    vals, build, flow = _run(
        monkeypatch,
        tmp_path,
        event="workflow_dispatch",
        scope="changed",
        changed=f"{target}/{feeder}/{feeder}.py",
    )
    assert vals["full_run"] == "false"
    assert build and all(m["dir"] == target for m in build)


# --- additive_test_file: feeder-scoped edits to existing test classes -------

_FLOW_MATRIX = {
    "flow": [
        {"dir": "feeders/blitzortung", "test_class": "TestBlitzortungDockerFlow"},
        {"dir": "feeders/gbfs-bikeshare", "test_class": "TestGbfsMqttDockerFlow"},
    ]
}


def _test_file(blitz_cmd: str = "feed", gbfs_env: str = "live", helper: str = "x") -> str:
    return (
        "import os\n"
        "import pytest\n"
        "\n"
        f"def _shared_helper():\n    return '{helper}'\n"
        "\n"
        "class TestBlitzortungDockerFlow:\n"
        f"    command = ['python', '-m', 'blitzortung', '{blitz_cmd}']\n"
        "    def test_it(self):\n        assert True\n"
        "\n"
        "class TestGbfsMqttDockerFlow:\n"
        f"    env = {{'GBFS_MOCK': '{gbfs_env}'}}\n"
        "    def test_it(self):\n        assert True\n"
    )


def test_additive_test_file_scopes_modified_class_to_its_feeder():
    base = _test_file(blitz_cmd="feed")
    head = _test_file(blitz_cmd="feed --mock")
    dirs = dm.additive_test_file(base, head, _FLOW_MATRIX)
    assert dirs == ["feeders/blitzortung"]


def test_additive_test_file_scopes_only_changed_classes():
    base = _test_file(blitz_cmd="feed", gbfs_env="live")
    head = _test_file(blitz_cmd="feed", gbfs_env="true")
    dirs = dm.additive_test_file(base, head, _FLOW_MATRIX)
    assert dirs == ["feeders/gbfs-bikeshare"]


def test_additive_test_file_shared_helper_change_bails_to_smoke():
    base = _test_file(helper="x")
    head = _test_file(helper="y")  # module-level helper changed
    assert dm.additive_test_file(base, head, _FLOW_MATRIX) is None


def test_additive_test_file_added_class_is_additive():
    base = _test_file()
    head = _test_file() + (
        "\nclass TestNewFeederDockerFlow:\n    def test_it(self):\n        assert True\n"
    )
    # New unmapped class selects no job but is still additive (not None).
    assert dm.additive_test_file(base, head, _FLOW_MATRIX) == []


def test_additive_test_file_removed_class_bails_to_smoke():
    base = _test_file()
    head = (
        "import os\nimport pytest\n\n"
        "def _shared_helper():\n    return 'x'\n\n"
        "class TestBlitzortungDockerFlow:\n"
        "    command = ['python', '-m', 'blitzortung', 'feed']\n"
        "    def test_it(self):\n        assert True\n"
    )  # TestGbfsMqttDockerFlow removed
    assert dm.additive_test_file(base, head, _FLOW_MATRIX) is None


def test_additive_test_file_modified_unmapped_class_bails_to_smoke():
    base = (
        "import pytest\n\n"
        "class AmqpDockerFlowBase:\n    timeout = 60\n"
        "    def run(self):\n        return 1\n"
    )
    head = base.replace("timeout = 60", "timeout = 90")
    # A shared base class (no matrix entry) changed -> cannot scope.
    assert dm.additive_test_file(base, head, _FLOW_MATRIX) is None


def test_additive_test_file_decorator_change_on_mapped_class_scopes():
    # A class-level decorator change must register as a class change (the
    # decorator precedes `class`, so without span widening it would be
    # invisible to both hashes and silently under-scope).
    base = (
        "import pytest\n\n"
        "class TestBlitzortungDockerFlow:\n    def test_it(self):\n        assert True\n"
    )
    head = (
        "import pytest\n\n"
        "@pytest.mark.skip(reason='flaky')\n"
        "class TestBlitzortungDockerFlow:\n    def test_it(self):\n        assert True\n"
    )
    assert dm.additive_test_file(base, head, _FLOW_MATRIX) == ["feeders/blitzortung"]


def test_additive_test_file_decorator_change_on_unmapped_class_bails():
    base = (
        "import pytest\n\n"
        "class AmqpDockerFlowBase:\n    def run(self):\n        return 1\n"
    )
    head = (
        "import pytest\n\n"
        "@pytest.mark.usefixtures('broker')\n"
        "class AmqpDockerFlowBase:\n    def run(self):\n        return 1\n"
    )
    assert dm.additive_test_file(base, head, _FLOW_MATRIX) is None


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
