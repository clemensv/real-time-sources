"""Both feeder families use the selected generated payload encoder."""

import io
import importlib
import json
from pathlib import Path
from unittest.mock import Mock

import avro.io
import avro.schema
import pytest

from pegelonline_amqp.app import feed
from pegelonline_amqp import app

FABRIC = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("content_type", ["application/json", "application/vnd.apache.avro+avro"])
@pytest.mark.parametrize("nullable_value", [None, 0])
def test_feed_encodes_both_families_against_registered_schemas(content_type, nullable_value):
    station_id = "00000000-0000-4000-8000-000000000001"
    station = {
        "uuid": station_id, "shortname": "TEST", "longname": None, "number": None,
        "km": nullable_value, "agency": None, "latitude": 51.0, "longitude": 7.0,
        "water": {"shortname": "test", "longname": None},
    }
    measurement = {
        "timestamp": "2026-01-01T12:00:00+01:00", "value": 123.0,
        "stateMnwMhw": "out-dated", "stateNswHsw": None, "trend": nullable_value,
    }
    api = Mock()
    api.list_stations.return_value = [station]
    api.get_water_levels.return_value = {station_id: measurement}
    producer = Mock()
    feed(api, producer, 60, once=True, content_type=content_type)
    definition = json.loads((FABRIC / "schematized" / "EventSchemaSetDefinition.json").read_text())
    for method, family, version in (
        (producer.send_station, "Station", "1"),
        (producer.send_current_measurement, "CurrentMeasurement", "2"),
    ):
        method.assert_called_once()
        kwargs = method.call_args.kwargs
        assert kwargs["content_type"] == content_type
        assert kwargs["_station_id"] == station_id
        data = kwargs["data"]
        wire = data.to_byte_array(content_type)
        assert isinstance(wire, bytes)
        if content_type == "application/json":
            decoded = json.loads(wire)
        else:
            resource = next(s for s in definition["schemas"] if s["id"].endswith("." + family))
            schema = avro.schema.parse(next(v["schema"] for v in resource["versions"] if v["id"] == version))
            stream = io.BytesIO(wire)
            decoded = avro.io.DatumReader(schema).read(avro.io.BinaryDecoder(stream))
            assert stream.tell() == len(wire)
        assert decoded == json.loads(data.to_byte_array("application/json"))
        if family == "CurrentMeasurement":
            assert decoded == {"station_id": station_id, **measurement, "stateNswHsw": "unknown"}
        else:
            assert decoded["km"] == nullable_value
            assert decoded["water"]["longname"] is None


def test_feed_rejects_unknown_content_type_before_fetching():
    api = Mock()
    with pytest.raises(ValueError, match="Unsupported payload"):
        feed(api, Mock(), 60, once=True, content_type="application/xml")
    api.list_stations.assert_not_called()


@pytest.mark.parametrize("transport", ["kafka", "mqtt", "amqp"])
@pytest.mark.parametrize("states", [{}, {"stateMnwMhw": None, "stateNswHsw": None},
                                  {"stateMnwMhw": "low", "stateNswHsw": "out-dated"}])
def test_missing_classifications_encode_canonical_unknown(transport, states):
    module = importlib.import_module(f"pegelonline_{transport}.app")
    raw = {"timestamp": "2026-01-01T12:00:00+01:00", "value": 0.0, "trend": 0, **states}
    data = module._build_measurement("00000000-0000-4000-8000-000000000001", raw)
    decoded = json.loads(data.to_byte_array("application/json"))
    assert decoded["stateMnwMhw"] == (states.get("stateMnwMhw") or "unknown")
    assert decoded["stateNswHsw"] == (states.get("stateNswHsw") or "unknown")
    assert decoded["trend"] == 0
    assert decoded["value"] == 0.0


@pytest.mark.parametrize("transport", ["kafka", "mqtt", "amqp"])
def test_classification_type_errors_are_not_converted_to_unknown(transport):
    module = importlib.import_module(f"pegelonline_{transport}.app")
    with pytest.raises(ValueError, match="stateMnwMhw must be a string"):
        module._build_measurement("synthetic-station", {
            "timestamp": "2026-01-01T12:00:00+01:00", "value": 0.0, "stateMnwMhw": 0,
        })


@pytest.mark.parametrize("encoding", ["json", "avro"])
def test_payload_encoding_environment_and_cli_override(monkeypatch, encoding):
    monkeypatch.setenv("AMQP_PAYLOAD_ENCODING", encoding)
    parser = app._build_arg_parser()
    assert parser.parse_args(["feed"]).payload_encoding == encoding
    override = "avro" if encoding == "json" else "json"
    assert parser.parse_args(["feed", "--payload-encoding", override]).payload_encoding == override


def test_invalid_payload_encoding_environment_fails_before_initialization(monkeypatch):
    monkeypatch.setenv("AMQP_PAYLOAD_ENCODING", "xml")
    api_factory = Mock()
    monkeypatch.setattr(app, "PegelOnlineAPI", api_factory)
    with pytest.raises(SystemExit) as error:
        app.main(["feed", "--once"])
    assert error.value.code == 2
    api_factory.assert_not_called()
