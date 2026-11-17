"""Contract checks for the schematized Fabric pilot."""

import importlib.util
import json
from pathlib import Path

import pytest
from fastavro import parse_schema
from fastavro.validation import validate

SOURCE = Path(__file__).resolve().parents[2]
FABRIC = SOURCE / "fabric"


@pytest.mark.unit
def test_projection_rebuild_preserves_contracts_and_inlines_dependencies():
    spec = importlib.util.spec_from_file_location("project_schemas", FABRIC / "project_schemas.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original = json.loads((SOURCE / "xreg" / "pegelonline.xreg.json").read_text(encoding="utf-8"))
    derived, definition, provenance = module.build(original)
    assert derived["endpoints"] == original["endpoints"]
    for group, value in original["schemagroups"].items():
        assert derived["schemagroups"][group] == value
    for filename, actual in (
        ("pegelonline.fabric.xreg.json", derived),
        ("EventSchemaSetDefinition.json", definition),
        ("projection-provenance.json", provenance),
    ):
        assert json.loads((FABRIC / "schematized" / filename).read_text(encoding="utf-8")) == actual
    for event_type in definition["eventTypes"]:
        schema = next(s for s in definition["schemas"] if s["id"] == event_type["id"])
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
