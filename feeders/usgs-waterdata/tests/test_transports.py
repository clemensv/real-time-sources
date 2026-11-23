import copy
import asyncio
from datetime import timedelta
import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from usgs_waterdata.poller import resource, series_resource
from usgs_waterdata.transports import AmqpSink, ExactDateTime, KafkaSink, MqttSink, generated, model_instance


def test_datetime_keeps_submicroseconds_and_sentinels_after_deepcopy():
    values = [
        "0001-01-01T00:00:00.0000000+00:00",
        "9999-12-31T23:59:59.9999999+00:00",
        "2025-01-02T03:04:05.1234567-05:00",
    ]
    for value in values:
        parsed = ExactDateTime.from_text(value)
        assert copy.deepcopy(parsed).isoformat() == value
        assert json.loads(json.dumps(parsed, default=lambda item: item.isoformat())) == value


@pytest.mark.parametrize("transport", ["kafka", "mqtt", "amqp"])
def test_generated_json_transport_preserves_threshold_precision_and_offsets(transport):
    evidence = json.loads((Path(__file__).parent / "fixtures/synthetic-features.json").read_text(encoding="utf-8"))
    feature = evidence["collections"]["time-series-metadata"]["features"][0]
    payload = series_resource(feature)
    timestamps = ["0001-01-01T00:00:00.0000000+00:00", "9999-12-31T23:59:59.9999999+00:00",
                  "2025-01-02T03:04:05.1234567-05:00"]
    payload["thresholds"] = [{"name": "precision-test", "periods": [
        {"start_time": timestamps[0], "end_time": timestamps[1], "applied_time": timestamps[2]}
    ]}]
    cls, models = generated(transport)
    model = model_instance(models["TimeSeries"], payload)
    if payload.get("data_gap_interval"):
        assert isinstance(model.data_gap_interval, timedelta)
    if transport == "kafka":
        raw = Mock()
        producer = cls(raw, "usgs-waterdata", content_mode="structured")
        producer.send_usgs_water_data_kafka_time_series(
            _time_series_id=payload["time_series_id"], data=model, flush_producer=False)
        wire = raw.produce.call_args.kwargs
        decoded = json.loads(wire["value"])["data"]
    elif transport == "mqtt":
        raw = Mock()
        producer = cls(raw, content_mode="binary")
        asyncio.run(producer.publish_usgs_water_data_mqtt_time_series(
            time_series_id=payload["time_series_id"], data=model))
        decoded = json.loads(raw.publish.call_args.args[1])
    else:
        producer = cls.__new__(cls)
        producer.content_mode = "binary"
        producer._send_via_blocking_sender = Mock()
        producer.send_time_series(_time_series_id=payload["time_series_id"], data=model)
        message = producer._send_via_blocking_sender.call_args.args[0]
        decoded = json.loads(message.body)
    period = decoded["thresholds"][0]["periods"][0]
    assert [period[key] for key in ("start_time", "end_time", "applied_time")] == timestamps


@pytest.mark.parametrize("transport", ["kafka", "mqtt", "amqp"])
def test_generated_synthetic_payloads_validate_against_contract(transport):
    from json_structure import InstanceValidator

    root = Path(__file__).parents[1]
    evidence = json.loads((root / "tests/fixtures/synthetic-features.json").read_text(encoding="utf-8"))
    contract = json.loads((root / "xreg/usgs-waterdata.xreg.json").read_text(encoding="utf-8"))
    _, models = generated(transport)
    collections = evidence["collections"]
    cases = [("TimeSeries", series_resource(feature)) for feature in collections["time-series-metadata"]["features"]]
    for collection, family, member in [("monitoring-locations", "MonitoringLocation", "location"),
                                        ("parameter-codes", "Parameter", "parameter")]:
        cases.extend((family, {"time_series_id": "native-series", member: resource(feature)})
                     for feature in collections[collection]["features"])
    cases.extend(("ContinuousObservation", {**resource(feature), "feature_id": str(feature.get("id"))})
                 for feature in collections["continuous"]["features"])
    for family, payload in cases:
        model = model_instance(models[family], payload)
        decoded = json.loads(model.to_byte_array("application/json"))
        if family == "TimeSeries":
            assert decoded["data_gap_interval"] == payload.get("data_gap_interval")
            assert decoded.get("sublocation_identifier") == payload["sublocation_identifier"]
            assert decoded.get("web_description") == payload["web_description"]
            assert len(decoded["thresholds"]) == len(payload["thresholds"])
            for expected, actual in zip(payload["thresholds"], decoded["thresholds"]):
                for key, value in expected.items():
                    if key != "periods":
                        assert actual[key] == value
                assert len(actual["periods"]) == len(expected["periods"])
                for expected_period, actual_period in zip(expected["periods"], actual["periods"]):
                    for key, value in expected_period.items():
                        assert actual_period[key] == value
        schema = contract["schemagroups"]["USGS.WaterData.jstruct"]["schemas"][f"USGS.WaterData.{family}"]["versions"]["1"]["schema"]
        validator = InstanceValidator(schema, extended=True)
        result = validator.validate(decoded)
        assert not result, (family, result)


@pytest.mark.parametrize("transport", ["kafka", "mqtt", "amqp"])
def test_duration_boundary_keeps_calendar_duration_and_original_model_type(transport):
    from isodate import Duration

    _, models = generated(transport)
    model = model_instance(models["TimeSeries"], {
        "time_series_id": "native", "thresholds": [], "data_gap_interval": "P1M",
    })
    assert isinstance(model.data_gap_interval, Duration)
    assert model.data_gap_interval.months == 1
    assert json.loads(model.to_byte_array("application/json"))["data_gap_interval"] == "P1M"
    assert isinstance(model.data_gap_interval, Duration)


@pytest.mark.parametrize("acknowledged,errors", [(False, []), (True, ["Not authorized"])])
def test_mqtt_flush_rejects_missing_or_negative_acknowledgements(acknowledged, errors):
    receipt = Mock()
    receipt.is_published.return_value = acknowledged
    sink = MqttSink()
    sink.pending, sink.errors = [receipt], errors
    with pytest.raises(RuntimeError):
        asyncio.run(sink.flush())


def test_kafka_connection_string_uses_plain_bootstrap_and_entity_topic(monkeypatch):
    raw = Mock()
    constructor = Mock(return_value=raw)
    monkeypatch.setattr("confluent_kafka.Producer", constructor)
    monkeypatch.setenv("CONNECTION_STRING", "BootstrapServer=broker:19092;EntityPath=native-topic")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    sink = KafkaSink()
    assert constructor.call_args.args[0] == {"bootstrap.servers": "broker:19092", "security.protocol": "PLAINTEXT"}
    assert sink.producer.topic == "native-topic"


def test_mqtt_empty_optional_ca_uses_system_trust(monkeypatch):
    from unittest.mock import AsyncMock

    client, producer = Mock(), Mock()
    producer.connect = AsyncMock()
    monkeypatch.setattr("paho.mqtt.client.Client", Mock(return_value=client))
    monkeypatch.setattr("usgs_waterdata.transports.generated", lambda transport: (Mock(return_value=producer), {}))
    monkeypatch.setenv("MQTT_BROKER_URL", "mqtts://broker:8883")
    monkeypatch.setenv("MQTT_AUTH_MODE", "anonymous")
    monkeypatch.setenv("MQTT_ENABLE_TLS", "true")
    monkeypatch.setenv("MQTT_CA_FILE", "")
    asyncio.run(MqttSink().start())
    assert client.tls_set.call_args.kwargs["ca_certs"] is None
    producer.connect.assert_awaited_once()


@pytest.mark.parametrize("mode,credentials", [
    ("userpass", {"MQTT_USERNAME": "publisher", "MQTT_PASSWORD": ""}),
    ("tls-cert", {"MQTT_CLIENT_CERT": "/certs/client.crt", "MQTT_CLIENT_KEY": ""}),
])
def test_mqtt_rejects_incomplete_selected_auth_mode_before_connect(monkeypatch, mode, credentials):
    from unittest.mock import AsyncMock

    producer = Mock()
    producer.connect = AsyncMock()
    monkeypatch.setattr("usgs_waterdata.transports.generated", lambda transport: (Mock(return_value=producer), {}))
    monkeypatch.setenv("MQTT_BROKER_URL", "mqtts://broker:8883")
    monkeypatch.setenv("MQTT_AUTH_MODE", mode)
    monkeypatch.setenv("MQTT_ENABLE_TLS", "true")
    for name, value in credentials.items():
        monkeypatch.setenv(name, value)
    with pytest.raises(ValueError, match="requires MQTT_"):
        asyncio.run(MqttSink().start())
    producer.connect.assert_not_awaited()


@pytest.mark.parametrize("tls,scheme,port", [(True, "amqps", 5671), (False, "amqp", 5672)])
def test_amqp_password_sender_requires_settlement_and_honors_tls(monkeypatch, tls, scheme, port):
    connection = Mock()
    constructor = Mock(return_value=connection)
    monkeypatch.setattr("proton.utils.BlockingConnection", constructor)
    monkeypatch.setenv("AMQP_BROKER_URL", f"{scheme}://user%2Bname:p%40ss%2Bword@broker:{port}/native")
    monkeypatch.setenv("AMQP_AUTH_MODE", "password")
    monkeypatch.delenv("AMQP_TLS", raising=False)
    monkeypatch.delenv("AMQP_USE_TLS", raising=False)
    sink = AmqpSink()
    assert constructor.call_args.args[0].startswith(f"{scheme}://")
    assert constructor.call_args.kwargs == {
        "timeout": 120, "user": "user+name", "password": "p@ss+word",
        "sasl_enabled": True, "allowed_mechs": "PLAIN", "allow_insecure_mechs": not tls,
    }
    assert sink.producer._blocking_sender_is_presettled is False
    from proton.reactor import AtLeastOnce
    assert isinstance(connection.create_sender.call_args.kwargs["options"], AtLeastOnce)


@pytest.mark.parametrize("use_tls,scheme,port", [("false", "amqp", 5672), ("true", "amqps", 5671)])
def test_amqp_explicit_tls_setting_reaches_generated_sas_cbs_connection(monkeypatch, use_tls, scheme, port):
    import importlib
    from types import SimpleNamespace

    cls, _ = generated("amqp")
    module = importlib.import_module(cls.__module__)
    connect = Mock()

    class Reactor:
        def __init__(self, handler):
            self.handler = handler

        def run(self):
            self.handler.on_start(SimpleNamespace(container=SimpleNamespace(connect=connect, schedule=Mock())))
            self.handler._init_future.set_result(None)

    monkeypatch.setattr(module, "Container", Reactor)
    monkeypatch.delenv("AMQP_BROKER_URL", raising=False)
    monkeypatch.setenv("AMQP_HOST", "sb-emulator")
    monkeypatch.setenv("AMQP_PORT", str(port))
    monkeypatch.setenv("AMQP_AUTH_MODE", "sas")
    monkeypatch.setenv("AMQP_USE_TLS", use_tls)
    monkeypatch.setenv("AMQP_TLS", "true" if use_tls == "false" else "false")
    monkeypatch.setenv("AMQP_SAS_KEY_NAME", "test-policy")
    monkeypatch.setenv("AMQP_SAS_KEY", "ZmFrZQ==")
    sink = AmqpSink()
    assert connect.call_args.args[0] == f"{scheme}://sb-emulator:{port}"
    assert connect.call_args.kwargs == {"sasl_enabled": True, "allowed_mechs": "ANONYMOUS", "reconnect": False}
    assert sink.producer._cbs_enabled
    assert not sink.producer.username and not sink.producer.password
    assert type(sink.producer._handler._token_provider).__name__ == "_SasTokenProvider"


def test_amqp_explicit_tls_disable_is_rejected_for_entra(monkeypatch):
    monkeypatch.setenv("AMQP_AUTH_MODE", "entra")
    monkeypatch.setenv("AMQP_USE_TLS", "false")
    monkeypatch.setenv("AMQP_TLS", "true")
    with pytest.raises(ValueError, match="Entra authentication requires TLS"):
        AmqpSink()
