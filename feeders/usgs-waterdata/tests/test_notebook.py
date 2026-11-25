import ast
import json
import logging
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest


def _bootstrap_scope(monkeypatch, wheel_names):
    notebook = json.loads((Path(__file__).parents[1] / "notebook/usgs-waterdata-feed.ipynb").read_text(encoding="utf-8"))
    scope = {"logging": logging}
    lookup = ast.parse("".join(notebook["cells"][2]["source"]))
    bootstrap_nodes = [
        node for node in lookup.body
        if isinstance(node, ast.FunctionDef) and node.name == "_bootstrap"
    ]
    scope.update(
        pathlib=SimpleNamespace(Path=lambda path: SimpleNamespace(
            glob=lambda pattern: [Path(name) for name in wheel_names])),
        sys=SimpleNamespace(executable="synthetic-python"),
        importlib=SimpleNamespace(
            invalidate_caches=lambda: None,
            metadata=SimpleNamespace(version=lambda name: "test-version")),
        subprocess=subprocess,
    )
    calls = []
    monkeypatch.setattr(subprocess, "check_call", lambda command, **kwargs: calls.append((command, kwargs)))
    exec(compile(ast.Module(body=bootstrap_nodes, type_ignores=[]), "notebook-bootstrap", "exec"), scope)
    return scope, calls


WHEELS = [
    "usgs_waterdata-1.0-py3-none-any.whl",
    "usgs_waterdata_core-1.0-py3-none-any.whl",
    "usgs_waterdata_producer_data-1.0-py3-none-any.whl",
    "usgs_waterdata_producer_kafka_producer-1.0-py3-none-any.whl",
]


@pytest.mark.parametrize("wheels", [[], WHEELS[:-1], WHEELS + ["usgs_waterdata_core-2.0-py3-none-any.whl"]])
def test_python_bootstrap_rejects_missing_or_ambiguous_bundles(monkeypatch, wheels):
    scope, calls = _bootstrap_scope(monkeypatch, wheels)
    with pytest.raises(RuntimeError, match="Expected one deployed"):
        scope["_bootstrap"]()
    assert calls == []


def test_python_bootstrap_installs_deployed_packages_and_public_dependencies(monkeypatch):
    scope, calls = _bootstrap_scope(monkeypatch, WHEELS)
    scope["_bootstrap"]()
    assert len(calls) == 2
    local, dependencies = calls
    assert local[0][:7] == ["synthetic-python", "-m", "pip", "install", "--force-reinstall", "--no-deps", WHEELS[0]]
    assert set(local[0][6:]) == set(WHEELS)
    assert "confluent-kafka>=2.5.3" in dependencies[0]
    assert "cloudevents>=1.12.1,<2.0.0" in dependencies[0]
    assert "urllib3>=2.2.3" in dependencies[0]
    assert "dataclasses-json>=0.6.7,<0.7.0" in dependencies[0]
    assert local[1]["timeout"] > 0
    assert dependencies[1]["timeout"] > 0


def test_python_bootstrap_does_not_hide_installation_failure(monkeypatch):
    scope, _ = _bootstrap_scope(monkeypatch, WHEELS)

    def fail(command, **kwargs):
        raise subprocess.CalledProcessError(1, command)

    monkeypatch.setattr(subprocess, "check_call", fail)
    with pytest.raises(subprocess.CalledProcessError):
        scope["_bootstrap"]()


def test_bootstrap_failure_is_logged_and_exits_before_connection_lookup(monkeypatch, tmp_path):
    notebook = json.loads((Path(__file__).parents[1] / "notebook/usgs-waterdata-feed.ipynb").read_text(encoding="utf-8"))
    log_path = tmp_path / "last-run.log"
    file_handler = logging.FileHandler
    monkeypatch.setattr(logging, "FileHandler", lambda path, **kwargs: file_handler(log_path, **kwargs))
    exits = []
    monkeypatch.setitem(sys.modules, "notebookutils", SimpleNamespace(
        notebook=SimpleNamespace(exit=exits.append)))
    scope = {"ONCE_MODE": True, "RUN_DURATION": 900}

    def bootstrap():
        raise RuntimeError("Missing deployed wheels")

    def connection():
        pytest.fail("Connection lookup must not run after bootstrap failure")

    scope.update(_bootstrap=bootstrap, _connection=connection)
    run = "".join(notebook["cells"][3]["source"])
    run = run.replace(
        'LOG_PATH = "/lakehouse/default/Files/feeder-state/usgs-waterdata/last-run.log"',
        f"LOG_PATH = {str(log_path)!r}",
    )
    logger = logging.getLogger()
    previous_level = logger.level
    try:
        exec(compile(run, "notebook-run", "exec"), scope)
    finally:
        logger.setLevel(previous_level)
    assert exits == ["FAIL: RuntimeError: Missing deployed wheels"]
    assert "Missing deployed wheels" in log_path.read_text(encoding="utf-8")


def test_notebook_selection_parameters_override_deployer_environment():
    notebook = json.loads((Path(__file__).parents[1] / "notebook/usgs-waterdata-feed.ipynb").read_text(encoding="utf-8"))
    scope = {}
    exec("".join(notebook["cells"][1]["source"]), scope)
    scope.update(USGS_WATERDATA_SITES="USGS-12345678", USGS_WATERDATA_PARAMETERS="00065")
    environment = {"USGS_WATERDATA_SITES": "USGS-00000000", "USGS_WATERDATA_PARAMETERS": "00010"}
    scope.update(os=SimpleNamespace(environ=environment), _connection=lambda: "test-connection")
    run = ast.parse("".join(notebook["cells"][3]["source"]))
    assignments = [
        node for node in ast.walk(run)
        if isinstance(node, ast.Assign) and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Subscript)
        and ast.unparse(node.targets[0].value) == "os.environ"
    ]
    exec(compile(ast.Module(body=assignments, type_ignores=[]), "notebook-environment", "exec"), scope)
    assert environment["USGS_WATERDATA_SITES"] == "USGS-12345678"
    assert environment["USGS_WATERDATA_PARAMETERS"] == "00065"


def _connection_scope(response, source="usgs-waterdata"):
    notebook = json.loads((Path(__file__).parents[2] / source / "notebook" / f"{source}-feed.ipynb").read_text(encoding="utf-8"))
    lookup = ast.parse("".join(notebook["cells"][2]["source"]))
    function = next(node for node in lookup.body if isinstance(node, ast.FunctionDef) and node.name == "_connection")
    endpoint = "https://api.fabric.microsoft.com/v1/workspaces/synthetic/eventstreams/stream"
    calls = []

    def read(url, headers):
        calls.append(url)
        if url == endpoint + "/topology":
            return {"sources": [{"name": "input", "type": "CustomEndpoint", "id": "source"}]}
        assert url == endpoint + "/sources/source/connection"
        return response

    scope = {"WORKSPACE_ID": "synthetic", "FABRIC_API": "https://api.fabric.microsoft.com/v1",
             "EVENTSTREAM_NAME": "stream", "EVENTSTREAM_SOURCE_NAME": "input",
             "notebookutils": SimpleNamespace(credentials=SimpleNamespace(getToken=lambda audience: "synthetic-token")),
             "_pages": lambda url, headers: [{"displayName": "stream", "id": "stream"}], "_read": read}
    exec(compile(ast.Module(body=[function], type_ignores=[]), "notebook-binding", "exec"), scope)
    return scope["_connection"], calls


@pytest.mark.parametrize("source", ["usgs-waterdata", "usgs-iv", "usgs-nwis-wq"])
def test_notebook_binding_discards_keys_and_uses_issued_namespace_and_entity(source):
    response = {"type": "CustomEndpoint", "fullyQualifiedNamespace": "synthetic.servicebus.windows.net",
                "eventHubName": "synthetic-entity",
                "accessKeys": {"primaryConnectionString": "must-not-be-used"}}
    connection, calls = _connection_scope(response, source)
    assert connection() == "BootstrapServer=synthetic.servicebus.windows.net:9093;EntityPath=synthetic-entity"
    assert "accessKeys" not in response
    assert len(calls) == 2


@pytest.mark.parametrize("namespace,entity", [
    ("https://synthetic.servicebus.windows.net", "entity"),
    ("", "entity"),
    ("synthetic.servicebus.windows.net", ""),
    ("synthetic.servicebus.windows.net", "entity;SharedAccessKey=synthetic"),
])
def test_notebook_binding_rejects_missing_or_invalid_endpoint_metadata(namespace, entity):
    connection, _ = _connection_scope({"type": "CustomEndpoint", "fullyQualifiedNamespace": namespace,
                                      "eventHubName": entity})
    with pytest.raises(RuntimeError, match="namespace/entity"):
        connection()
