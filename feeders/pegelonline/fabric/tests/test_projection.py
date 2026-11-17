"""Contract checks for the schematized Fabric pilot."""

import json
from pathlib import Path

import pytest
from fastavro import parse_schema
from fastavro.validation import validate

SOURCE = Path(__file__).resolve().parents[2]
FABRIC = SOURCE / "fabric"


@pytest.mark.unit
def test_checked_projection_preserves_contracts_and_resolves_selected_schemas():
    original = json.loads((SOURCE / "xreg" / "pegelonline.xreg.json").read_text(encoding="utf-8"))
    derived = json.loads((FABRIC / "schematized" / "pegelonline.fabric.xreg.json").read_text())
    definition = json.loads((FABRIC / "schematized" / "EventSchemaSetDefinition.json").read_text())
    assert derived["endpoints"] == original["endpoints"]
    for collection in ("schemagroups", "messagegroups"):
        for key, value in original[collection].items():
            assert derived[collection][key] == value
    variants = derived["messagegroups"]["de.wsv.pegelonline.avro"]["messages"]
    assert {event["id"] for event in definition["eventTypes"]} == set(variants)
    assert {schema["id"] for schema in definition["schemas"]} == set(variants)
    for event_type in definition["eventTypes"]:
        message = variants[event_type["id"]]
        inherited = derived
        for part in message["basemessageuri"].strip("/").split("/"):
            inherited = inherited[part]
        assert event_type["id"] == inherited["envelopemetadata"]["type"]["value"]
        projected = derived
        for part in message["dataschemauri"].removeprefix("#/").split("/"):
            projected = projected[part]
        schema_id = event_type["schemaUrl"].removeprefix("#/schemas/")
        schema = next(s for s in definition["schemas"] if s["id"] == schema_id)
        selected_version = message["dataschemauri"].rsplit("/", 1)[1]
        selected = next(v for v in schema["versions"] if v["id"] == selected_version)
        assert selected["format"] == projected["format"] == event_type["schemaFormat"]
        assert json.loads(selected["schema"]) == projected["schema"]
        for version in schema["versions"]:
            record = json.loads(version["schema"])
            assert record["type"] == "record"
            parse_schema(record)
        assert event_type["envelopeMetadata"]["type"]["value"] == event_type["id"]


@pytest.mark.unit
def test_measurement_projection_matches_json_timestamp_nulls_and_wire_enums():
    definition = json.loads((FABRIC / "schematized" / "EventSchemaSetDefinition.json").read_text())
    schema = next(s for s in definition["schemas"] if s["id"].endswith(".CurrentMeasurement"))
    version = next(v for v in schema["versions"] if v["id"] == "2")
    record = parse_schema(json.loads(version["schema"]))
    timestamp = next(f for f in record["fields"] if f["name"] == "timestamp")
    assert "logicalType" not in timestamp["type"]
    assert timestamp["type"]["x-original-logical-type"] == "rfc3339-timestamp-millis"
    payload = {
        "station_id": "b475386c-30cc-453a-b3b7-1d17ace13595",
        "timestamp": "2026-11-16T11:30:00+01:00",
        "value": 121.0,
        "stateMnwMhw": "out-dated",
        "stateNswHsw": None,
        "trend": None,
    }
    assert validate(payload, record, strict=True)
    assert not validate({**payload, "timestamp": 1794825000000}, record, strict=True, raise_errors=False)
