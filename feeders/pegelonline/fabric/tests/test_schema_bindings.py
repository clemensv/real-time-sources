"""Registered URI discovery must use selected versions and checked projections."""

import copy
import asyncio
import hashlib
import importlib
import json
from types import SimpleNamespace
from unittest import mock

import pytest

from pegelonline_core.fabric import lookup_dataschema_overrides

WS, ES, SOURCE, CAPACITY, SCHEMA_SET = (
    "00000000-0000-0000-0000-00000000000" + str(index) for index in range(1, 6)
)
ORIGINAL = "xreg://./schemagroups/example/schemas/Reading/versions/1"
SCHEMA_URL = f"https://test.messagingcatalog.azure.net/schemagroups/{SCHEMA_SET}/schemas/canonical-reading"
SCHEMA = '{"type":"record","name":"Reading","fields":[{"name":"value","type":"double"}]}'


def fixture():
    selection = {"eventSetWorkspaceId": WS, "eventSetArtifactId": SCHEMA_SET,
                 "eventTypeId": "reading-alias", "schemaVersionId": "2"}
    return {
        "expected": {"reading-alias": {"source_uri": ORIGINAL, "projected_version": "2",
                                      "schema_sha256": hashlib.sha256(SCHEMA.encode()).hexdigest()}},
        "model": {"properties": {"dataSources": [
            {"id": SOURCE, "direction": "Source", "properties": {"eventTypes": [selection]}}
        ]}},
        "event_type": {"id": "reading-alias", "schemaUrl": SCHEMA_URL},
        "versions": [
            {"id": "9", "schemaId": "canonical-reading", "format": "Avro/1.12.0",
             "selfUrl": SCHEMA_URL + "/versions/9$details", "schema": "{}"},
            {"id": "2", "schemaId": "canonical-reading", "format": "Avro/1.12.0",
             "selfUrl": SCHEMA_URL + "/versions/2$details", "schema": SCHEMA},
        ],
    }


def install_session(monkeypatch, data):
    calls = []

    class Session:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def mount(self, *args):
            pass

        def request(self, method, url, **kwargs):
            calls.append((method, url))
            status = 200
            headers = {}
            if url.startswith("https://api.fabric.microsoft.com/v1/workspaces/"):
                result = {"id": WS, "capacityId": CAPACITY}
            elif url.startswith("https://api.powerbi.com"):
                status = 307
                headers["Location"] = url.replace("api.powerbi.com", "test.analysis.windows.net")
                result = {}
            elif "/v1.0/myorg/groups/" in url:
                result = {"id": WS, "capacityId": CAPACITY}
            elif url.endswith("/generatemwctokenv2"):
                result = {"TargetUriHost": data.get("host", "test.analysis.windows.net"),
                          "CapacityObjectId": CAPACITY, "Token": "secret-scoped-token"}
            elif url.endswith("/model"):
                result = data["model"]
            elif "/eventtypes/" in url:
                result = data["event_type"]
            elif url.endswith("/schemas/canonical-reading/versions"):
                result = data["versions"]
            else:
                raise AssertionError(f"Unexpected request: {method} {url}")
            assert kwargs["allow_redirects"] is False
            return SimpleNamespace(
                status_code=status, headers=headers,
                raise_for_status=lambda: None, json=lambda: result,
            )

    monkeypatch.setattr("pegelonline_core.fabric.requests.Session", Session)
    return calls


def resolve(data):
    return lookup_dataschema_overrides(WS, ES, SOURCE, data["expected"], lambda audience: "approved-token")


@pytest.mark.unit
def test_schema_binding_uses_canonical_schema_and_pinned_version(monkeypatch):
    data = fixture()
    calls = install_session(monkeypatch, data)
    assert resolve(data) == {ORIGINAL: SCHEMA_URL + "/versions/2"}
    assert any(url.endswith("/schemas/canonical-reading/versions") for _, url in calls)
    assert not any("/connection" in url for _, url in calls)
    assert all(method in ("GET", "POST") for method, _ in calls)


@pytest.mark.unit
@pytest.mark.parametrize("failure", ["missing", "duplicate", "version", "fingerprint", "self-url", "host"])
def test_schema_binding_rejects_unqualified_registration(monkeypatch, failure):
    data = fixture()
    selections = data["model"]["properties"]["dataSources"][0]["properties"]["eventTypes"]
    if failure == "missing":
        selections.clear()
    elif failure == "duplicate":
        selections.append(copy.deepcopy(selections[0]))
    elif failure == "version":
        selections[0]["schemaVersionId"] = "9"
    elif failure == "fingerprint":
        data["versions"][1]["schema"] = json.dumps({"type": "record", "name": "Changed", "fields": []})
    elif failure == "self-url":
        data["versions"][1]["selfUrl"] = SCHEMA_URL + "/versions/9$details"
    else:
        data["host"] = "evil.example?target=.analysis.windows.net"
    install_session(monkeypatch, data)
    with pytest.raises(RuntimeError):
        resolve(data)


@pytest.mark.unit
@pytest.mark.parametrize("transport", ["kafka", "mqtt", "amqp"])
@pytest.mark.parametrize("family", ["Station", "CurrentMeasurement"])
@pytest.mark.parametrize("mode", ["structured", "binary"])
@pytest.mark.parametrize("override_schema", [False, True])
def test_generated_clients_emit_original_or_registered_schema(transport, family, mode, override_schema):
    app = importlib.import_module(f"pegelonline_{transport}.app")
    original = (
        "xreg://./schemagroups/de.wsv.pegelonline.jstruct/schemas/"
        f"de.wsv.pegelonline.{family}/versions/1"
    )
    registered = f"https://catalog.example/schemas/{family}/versions/2"
    overrides = {original: registered} if override_schema else None
    expected = registered if override_schema else original
    if family == "Station":
        data = app._build_station({
            "uuid": "STATION-1", "number": "1", "shortname": "TEST",
            "longname": "Test station", "agency": "WSV",
            "longitude": 8.0, "latitude": 50.0, "water": {"shortname": "RHEIN"},
        })
    else:
        data = app._build_measurement("STATION-1", {
            "timestamp": "2026-01-01T12:00:00+01:00", "value": 123.0,
        })
    raw = mock.Mock()
    raw.flush.return_value = 0
    if transport == "kafka":
        producer = app.DeWsvPegelonlineKafkaEventProducer(
            raw, "test-topic", content_mode=mode, dataschema_overrides=overrides,
        )
        send = (producer.send_de_wsv_pegelonline_kafka_station if family == "Station"
                else producer.send_de_wsv_pegelonline_kafka_current_measurement)
        send(_feedurl="https://example.com/stations/1", _station_id="STATION-1", data=data)
        message = raw.produce.call_args.kwargs
        attributes = (json.loads(message["value"]) if mode == "structured"
                      else {key.removeprefix("ce_"): value.decode() if isinstance(value, bytes) else value
                            for key, value in message["headers"].items()})
        if mode == "structured":
            assert attributes["data"] == json.loads(data.to_json())
            assert "data_base64" not in attributes
        assert message["key"] in ("STATION-1", b"STATION-1")
    elif transport == "mqtt":
        producer = app.DeWsvPegelonlineMqttMqttClient(
            client=raw, content_mode=mode, dataschema_overrides=overrides,
        )
        send = (producer.publish_de_wsv_pegelonline_mqtt_station if family == "Station"
                else producer.publish_de_wsv_pegelonline_mqtt_current_measurement)
        asyncio.run(send(feedurl="https://example.com/stations/1", station_id="STATION-1",
                         water_shortname="rhein", data=data))
        message = raw.publish.call_args
        attributes = (json.loads(message.args[1]) if mode == "structured"
                      else dict(message.kwargs["properties"].UserProperty))
    else:
        cls = app.DeWsvPegelonlineAmqpProducer
        with mock.patch.object(cls, "_init_blocking_sender"), \
             mock.patch.object(cls, "_send_via_blocking_sender") as sent:
            producer = cls(host="localhost", address="test", use_tls=False,
                           content_mode=mode, dataschema_overrides=overrides)
            send = producer.send_station if family == "Station" else producer.send_current_measurement
            send(data=data, _feedurl="https://example.com/stations/1",
                 _station_id="STATION-1", _water_shortname="rhein")
        message = sent.call_args.args[0]
        attributes = (json.loads(message.body) if mode == "structured"
                      else {key.removeprefix("cloudEvents:"): value
                            for key, value in message.properties.items()})
    assert attributes["dataschema"] == expected
    assert attributes["type"] == f"de.wsv.pegelonline.{family}"
    assert attributes["subject"] == "STATION-1"
    assert attributes["source"] == "https://example.com/stations/1"
    assert attributes["id"]


@pytest.mark.unit
@pytest.mark.parametrize("auth", ["password", "sas", "entra"])
def test_amqp_factory_passes_mapping_with_each_authentication_mode(auth):
    from pegelonline_amqp import app

    overrides = {ORIGINAL: SCHEMA_URL + "/versions/2"}
    with mock.patch.object(app, "DeWsvPegelonlineAmqpProducer") as constructor:
        app._build_producer(
            host="localhost", port=5672, address="test", use_tls=False,
            content_mode="binary", auth_mode=auth,
            username=None, password=None,
            entra_audience=app.DEFAULT_ENTRA_AUDIENCE_SERVICEBUS, entra_client_id=None,
            sas_key_name="test" if auth == "sas" else None,
            sas_key="dGVzdA==" if auth == "sas" else None,
            dataschema_overrides=overrides,
        )
    assert constructor.call_args.kwargs["dataschema_overrides"] == overrides
