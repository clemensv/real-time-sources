"""Notebook boundary checks without a Fabric kernel or broker."""

import json
import hashlib
import logging
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

NOTEBOOK = Path(__file__).resolve().parents[2] / "notebook" / "pegelonline-feed.ipynb"


def helpers(monkeypatch, get):
    monkeypatch.setitem(sys.modules, "notebookutils", SimpleNamespace(
        credentials=SimpleNamespace(getToken=lambda audience: "test-token")))
    monkeypatch.setitem(sys.modules, "requests", SimpleNamespace(get=get))
    cells = json.loads(NOTEBOOK.read_text())["cells"]
    namespace = {}
    exec(compile("".join(cells[2]["source"]), str(NOTEBOOK), "exec"), namespace)
    return namespace


@pytest.mark.unit
def test_notebook_selects_named_source_not_first_endpoint(monkeypatch):
    paths = []

    def get(url, **kwargs):
        paths.append(url)
        if url.endswith("/eventstreams"):
            result = {"value": [{"id": "es", "displayName": "pilot"}]}
        elif url.endswith("/topology"):
            result = {"sources": [
                {"id": "wrong", "type": "CustomEndpoint", "name": "other"},
                {"id": "selected", "type": "CustomEndpoint", "name": "input"},
            ]}
        else:
            assert url.endswith("/sources/selected/connection")
            result = {"accessKeys": {"primaryConnectionString": "selected-connection"}}
        return SimpleNamespace(raise_for_status=lambda: None, json=lambda: result)

    namespace = helpers(monkeypatch, get)
    assert namespace["lookup_es_connection_string"]("ws", "pilot", "input") == "selected-connection"
    assert len(paths) == 3


@pytest.mark.unit
def test_notebook_rejects_missing_named_source(monkeypatch):
    results = iter([{"value": [{"id": "es", "displayName": "pilot"}]}, {"sources": []}])

    def get(*args, **kwargs):
        result = next(results)
        return SimpleNamespace(raise_for_status=lambda: None, json=lambda: result)

    namespace = helpers(monkeypatch, get)
    with pytest.raises(RuntimeError, match="named CustomEndpoint"):
        namespace["lookup_es_connection_string"]("ws", "pilot", "input")


@pytest.mark.unit
def test_notebook_maps_sas_connection_without_losing_key_padding(monkeypatch):
    namespace = helpers(monkeypatch, None)
    environment = namespace["amqp_environment"](
        "Endpoint=sb://test.servicebus.windows.net/;EntityPath=input;"
        "SharedAccessKeyName=send;SharedAccessKey=abc=="
    )
    assert environment["AMQP_HOST"] == "test.servicebus.windows.net"
    assert environment["AMQP_ADDRESS"] == "input"
    assert environment["AMQP_SAS_KEY"] == "abc=="
    assert environment["AMQP_CONTENT_MODE"] == "binary"
    with pytest.raises(ValueError, match="Eventstream Event Hubs"):
        namespace["amqp_environment"]("Endpoint=https://example.com;EntityPath=input")


@pytest.mark.unit
@pytest.mark.parametrize("send_error", [False, True])
def test_notebook_preserves_state_and_reports_feeder_errors(monkeypatch, tmp_path, send_error):
    monkeypatch.setenv("SSL_CERT_FILE", "test-ca-bundle")
    namespace = helpers(monkeypatch, None)
    state = tmp_path / "state.json"
    state.write_text('{"existing": true}')
    exits = []

    def feed(api, producer, polling_interval, **kwargs):
        assert kwargs["state_file"] == str(state)
        assert kwargs["once"] is True
        if send_error:
            logging.error("Publish rejected")

    monkeypatch.setitem(sys.modules, "pegelonline_amqp.app", SimpleNamespace(feed=feed))
    monkeypatch.setitem(sys.modules, "pegelonline_core", SimpleNamespace(PegelOnlineAPI=lambda: None))
    overrides = {"xreg://./schemas/Station/versions/1": "https://catalog.example/schemas/Station/versions/1"}
    monkeypatch.setitem(sys.modules, "pegelonline_core.fabric", SimpleNamespace(
        lookup_dataschema_overrides=lambda *args: overrides))
    constructed = []

    def producer(**kwargs):
        constructed.append(kwargs)
        return SimpleNamespace(close=lambda: None)

    monkeypatch.setitem(sys.modules, "pegelonline_amqp_producer_amqp_producer.producer", SimpleNamespace(
        DeWsvPegelonlineAmqpProducer=producer))
    monkeypatch.setitem(sys.modules, "proton", SimpleNamespace(SSL=SimpleNamespace(present=lambda: True)))
    namespace["requests"].certs = SimpleNamespace(where=lambda: "test-ca-bundle")
    namespace.update(
        LOG_PATH=str(tmp_path / "last-run.log"), STATE_FILE=str(state),
        RUN_DURATION=5, POLLING_INTERVAL=60, ONCE_MODE=True,
        WORKSPACE_ID="ws", EVENTSTREAM_NAME="pilot", SOURCE_NAME="input",
        SCHEMA_BINDINGS={},
        lookup_es_binding=lambda *args: ("es", "source",
            "Endpoint=sb://test.servicebus.windows.net/;EntityPath=input;"
            "SharedAccessKeyName=send;SharedAccessKey=abc==",
        ),
        notebookutils=SimpleNamespace(notebook=SimpleNamespace(exit=exits.append)),
    )
    cells = json.loads(NOTEBOOK.read_text())["cells"]
    exec(compile("".join(cells[3]["source"]), str(NOTEBOOK), "exec"), namespace)
    assert state.read_text() == '{"existing": true}'
    assert exits[0].startswith("FAIL:") if send_error else exits == ["OK"]
    log = (tmp_path / "last-run.log").read_text()
    assert ("Publish rejected" in log) == send_error
    assert "abc==" not in log
    assert constructed[0]["dataschema_overrides"] == overrides


@pytest.mark.unit
def test_notebook_bindings_match_canonical_identities_and_selected_schemas():
    cells = json.loads(NOTEBOOK.read_text())["cells"]
    namespace = {}
    exec("".join(cells[1]["source"]), namespace)
    source = NOTEBOOK.parents[1]
    registry = json.loads((source / "xreg" / "pegelonline.xreg.json").read_text())
    derived = json.loads((source / "fabric" / "schematized" / "pegelonline.fabric.xreg.json").read_text())
    definition = json.loads((source / "fabric" / "schematized" / "EventSchemaSetDefinition.json").read_text())
    messages = registry["messagegroups"]["de.wsv.pegelonline"]["messages"]
    assert set(namespace["SCHEMA_BINDINGS"]) == {event["id"] for event in definition["eventTypes"]}
    for event in definition["eventTypes"]:
        message = messages[event["id"]]
        binding = namespace["SCHEMA_BINDINGS"][event["id"]]
        schema_resource = registry
        for part in message["dataschemauri"].removeprefix("#/").split("/"):
            schema_resource = schema_resource[part]
        assert binding["source_uri"] == (
            "xreg://./" + message["dataschemauri"].removeprefix("#/")
            + "/versions/" + schema_resource["defaultversionid"])
        variant = derived["messagegroups"]["de.wsv.pegelonline.avro"]["messages"][event["id"]]
        assert binding["projected_version"] == variant["dataschemauri"].rsplit("/", 1)[1]
        schema = next(s for s in definition["schemas"] if s["id"] == event["schemaUrl"].removeprefix("#/schemas/"))
        version = next(v for v in schema["versions"] if v["id"] == binding["projected_version"])
        canonical_schema = json.dumps(json.loads(version["schema"]), ensure_ascii=True, separators=(",", ":"))
        assert binding["schema_sha256"] == hashlib.sha256(canonical_schema.encode()).hexdigest()
