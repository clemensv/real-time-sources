import importlib.util
import json
from pathlib import Path

import pytest


SPEC = importlib.util.spec_from_file_location(
    "discover_container_matrix", Path(__file__).parents[1] / "ci" / "discover_container_matrix.py"
)
assert SPEC is not None and SPEC.loader is not None
matrix = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(matrix)


@pytest.fixture
def dispatch(monkeypatch, tmp_path):
    output = tmp_path / "output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(output))
    monkeypatch.setenv("EVENT_NAME", "workflow_dispatch")
    monkeypatch.setenv("FEEDER_FILTER", "")
    monkeypatch.setenv("ALL_BASE_JSON", json.dumps([
        {"path": "feeders/usgs-waterdata", "file": "Dockerfile"},
        {"path": "feeders/other", "file": "Dockerfile"},
    ]))
    monkeypatch.setenv("ALL_TRANSPORT_JSON", json.dumps([
        {"path": "feeders/usgs-waterdata", "file": "Dockerfile.amqp"},
        {"path": "feeders/usgs-waterdata", "file": "Dockerfile.mqtt"},
        {"path": "feeders/other", "file": "Dockerfile.amqp"},
    ]))
    return output


def test_dispatch_scopes_all_variants_without_other_feeders(monkeypatch, dispatch):
    monkeypatch.setenv("FEEDER_FILTER", "usgs-waterdata")
    assert matrix.main() == 0
    fields = dict(line.split("=", 1) for line in dispatch.read_text().splitlines())
    assert fields["full_run"] == "false"
    assert len(json.loads(fields["containers_base"])) == 1
    variants = json.loads(fields["containers_transport"])
    assert {item["file"] for item in variants} == {"Dockerfile.amqp", "Dockerfile.mqtt"}
    assert all(item["path"] == "feeders/usgs-waterdata" for item in variants)


@pytest.mark.parametrize("selection", ["unknown", "usgs-waterdata,", "../other"])
def test_invalid_dispatch_filter_fails_instead_of_building_fleet(monkeypatch, dispatch, selection):
    monkeypatch.setenv("FEEDER_FILTER", selection)
    with pytest.raises(ValueError, match="Unknown or empty"):
        matrix.main()
    assert not dispatch.exists()


def test_filter_cannot_override_pull_request_scope(monkeypatch, dispatch):
    monkeypatch.setenv("EVENT_NAME", "pull_request")
    monkeypatch.setenv("FEEDER_FILTER", "usgs-waterdata")
    with pytest.raises(ValueError, match="only supported"):
        matrix.main()


def test_empty_dispatch_filter_preserves_full_fleet(dispatch):
    assert matrix.main() == 0
    fields = dict(line.split("=", 1) for line in dispatch.read_text().splitlines())
    assert fields["full_run"] == "true"
    assert len(json.loads(fields["containers_base"])) == 2
    assert len(json.loads(fields["containers_transport"])) == 3
