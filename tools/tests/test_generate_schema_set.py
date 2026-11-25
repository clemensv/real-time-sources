"""Shared xRegistry-to-Fabric authoring checks."""

import copy
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

import pytest
from fastavro.validation import validate

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "deploy-fabric" / "generate_schema_set.py"
SPEC = importlib.util.spec_from_file_location("generate_schema_set", SCRIPT)
assert SPEC and SPEC.loader
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


def registry():
    record = {
        "type": "record", "name": "Reading", "namespace": "example",
        "fields": [{"name": "value", "type": ["null", "double"], "default": None}],
    }
    return {
        "endpoints": {"kafka": {"protocol": "KAFKA", "protocoloptions": {"key": "{id}"}}},
        "messagegroups": {
            "base": {"messages": {"reading": {
                "envelope": "CloudEvents/1.0", "description": "Sensor reading",
                "envelopemetadata": {
                    "type": {"value": "example.Reading"},
                    "source": {"type": "uritemplate", "value": "https://example.test/{id}"},
                    "subject": {"type": "uritemplate", "value": "{id}", "description": "Sensor ID"},
                },
                "dataschemaformat": "Avro/1.12.0",
                "dataschemauri": "xreg://./schemagroups/sensors/schemas/Reading",
            }}},
            "variant": {"messages": {"reading.avro": {
                "basemessageuri": "/messagegroups/base/messages/reading",
                "envelopemetadata": {"subject": {"required": True}},
            }}},
        },
        "schemagroups": {"sensors": {"schemas": {"Reading": {
            "format": "Avro/1.12.0", "defaultversionid": "1",
            "versions": {
                "1": {"schema": record},
                "2": {"schema": {**record, "doc": "Second version"}},
            },
        }}}},
    }


def test_python_data_generation_supports_json_and_avro(tmp_path, monkeypatch):
    source = tmp_path / "registry.json"
    source.write_text(json.dumps(registry()))
    output = tmp_path / "data"
    assert generator.main([
        "--registry", str(source), "--messagegroup", "variant",
        "--definition", str(tmp_path / "definition.json"),
        "--python-data-output", str(output), "--python-package", "test_dual_data",
    ]) == 0
    assert re.search(r'(?m)^avro\s*=', (output / "pyproject.toml").read_text())
    monkeypatch.syspath_prepend(str(output / "src"))
    from test_dual_data.example.reading import Reading
    import avro.io
    import io

    record = Reading(value=12.5)
    assert json.loads(record.to_byte_array("application/json")) == {"value": 12.5}
    encoded = record.to_byte_array("application/vnd.apache.avro+avro")
    assert avro.io.DatumReader(Reading.AvroType).read(
        avro.io.BinaryDecoder(io.BytesIO(encoded))) == {"value": 12.5}


@pytest.mark.parametrize("options", [
    ["--python-data-output", "data"],
    ["--python-package", "test_dual_data"],
    ["--python-data-output", "data", "--python-package", "test_dual_data", "--include-history"],
])
def test_python_data_generation_rejects_incomplete_or_historical_selection(tmp_path, options):
    with pytest.raises(SystemExit) as error:
        generator.main([
            "--registry", str(tmp_path / "missing.json"), "--messagegroup", "variant",
            "--definition", str(tmp_path / "definition.json"), *options,
        ])
    assert error.value.code == 2
    assert not (tmp_path / "definition.json").exists()


def test_inherited_metadata_versions_and_no_input_mutation():
    original = registry()
    before = copy.deepcopy(original)
    derived, definition = generator.generate(
        original, ["variant"],
        versions={"#/schemagroups/sensors/schemas/Reading": "2"},
    )
    assert original == before == derived
    event = definition["eventTypes"][0]
    assert event["id"] == "example.Reading"
    assert event["description"] == "Sensor reading"
    metadata = event["envelopeMetadata"]
    assert metadata["subject"] == {"type": "string", "required": True, "description": "Sensor ID"}
    assert metadata["source"] == {"type": "uri", "required": True}
    assert metadata["dataschema"] == {"type": "uri", "required": True}
    assert metadata["datacontenttype"]["value"] == "application/json"
    assert [v["id"] for v in definition["schemas"][0]["versions"]] == ["2"]
    assert json.loads(definition["schemas"][0]["versions"][0]["schema"])["doc"] == "Second version"


@pytest.mark.parametrize("change,match", [
    ("cycle", "Cyclic"),
    ("remote", "Only local"),
    ("missing", "Missing registry"),
    ("unversioned", "Pin a version"),
    ("binary", "Unsupported payload"),
    ("duplicate", "Duplicate CloudEvents"),
])
def test_invalid_selections_fail_explicitly(change, match):
    document = registry()
    message = document["messagegroups"]["base"]["messages"]["reading"]
    groups = ["variant"]
    if change == "cycle":
        message["basemessageuri"] = "#/messagegroups/variant/messages/reading.avro"
    elif change == "remote":
        message["dataschemauri"] = "https://example.test/schema"
    elif change == "missing":
        message["dataschemauri"] += "/versions/absent"
    elif change == "unversioned":
        del document["schemagroups"]["sensors"]["schemas"]["Reading"]["defaultversionid"]
    elif change == "binary":
        message["envelopemetadata"]["datacontenttype"] = {"value": "application/octet-stream"}
    elif change == "duplicate":
        groups.append("base")
    with pytest.raises(ValueError, match=match):
        generator.generate(document, groups)


def test_multiple_families_nondefault_version_and_unknown_logical_type():
    document = registry()
    message = document["messagegroups"]["base"]["messages"]["reading"]
    message["dataschemauri"] += "/versions/2"
    resource = document["schemagroups"]["sensors"]["schemas"]["Reading"]
    resource["versions"]["2"]["schema"]["fields"][0]["type"] = {
        "type": "string", "logicalType": "rfc3339-timestamp-millis",
    }
    del resource["versions"]["2"]["schema"]["fields"][0]["default"]
    second = copy.deepcopy(message)
    second["envelopemetadata"]["type"]["value"] = "example.Other"
    document["messagegroups"]["base"]["messages"]["other"] = second
    with pytest.warns(UserWarning, match="--no-custom-logical-types"):
        _, definition = generator.generate(document, ["base"])
    assert len(definition["schemas"]) == 1
    assert len(definition["eventTypes"]) == 2
    schema = json.loads(definition["schemas"][0]["versions"][0]["schema"])
    assert schema["fields"][0]["type"]["logicalType"] == "rfc3339-timestamp-millis"
    for timestamp in ("2026-01-01T10:20:30+01:00", "2026-01-01T09:20:30.123456Z"):
        assert validate({"value": timestamp}, schema)


@pytest.mark.parametrize("encoding", [None, "json", "avro"])
def test_avrotize_conversion_creates_parallel_inherited_variants(encoding):
    document = registry()
    message = document["messagegroups"]["base"]["messages"]["reading"]
    message["dataschemaformat"] = "JsonStructure/draft-02"
    resource = document["schemagroups"]["sensors"]["schemas"]["Reading"]
    resource["format"] = "JsonStructure/draft-02"
    structure = {
        "$schema": "https://json-structure.org/meta/core/v0/#",
        "$id": "https://example.test/Reading",
        "name": "Reading", "namespace": "example", "type": "object",
        "required": ["id", "state"],
        "properties": {
            "id": {"type": "string", "description": "Sensor identifier"},
            "state": {"type": "string", "enum": ["OK", "BAD"]},
            "value": {"type": ["null", "double"]},
            "location": {"$ref": "#/definitions/Location"},
        },
        "definitions": {"Location": {
            "type": "object", "name": "Location",
            "properties": {"latitude": {"type": "double"}},
        }},
    }
    resource["versions"] = {"1": {"schema": structure}}
    original = copy.deepcopy(document)
    with pytest.raises(ValueError, match="projected-version"):
        generator.generate(document, ["base"], create_avro_variants=True)
    derived, definition = generator.generate(
        document, ["base"], create_avro_variants=True,
        projected_versions={"#/schemagroups/sensors/schemas/Reading": "7"},
        payload_encoding=encoding,
    )
    assert document == original
    assert derived["endpoints"] == original["endpoints"]
    for collection in ("messagegroups", "schemagroups"):
        for key, value in original[collection].items():
            assert derived[collection][key] == value
    variant = derived["messagegroups"]["base.avro"]["messages"]["reading"]
    assert variant["basemessageuri"] == "#/messagegroups/base/messages/reading"
    assert variant["dataschemauri"].endswith("/Reading/versions/7")
    assert variant["envelopemetadata"]["datacontenttype"]["value"] == (
        "application/vnd.apache.avro+avro" if encoding == "avro" else "application/json")
    _, regenerated = generator.generate(derived, ["base.avro"])
    assert definition == regenerated
    record = json.loads(definition["schemas"][0]["versions"][0]["schema"])
    assert validate({"id": "sensor1", "state": "OK", "value": None, "location": None}, record)


def test_payload_encoding_changes_metadata_without_changing_schema():
    original = registry()
    before = copy.deepcopy(original)
    _, json_definition = generator.generate(original, ["variant"], payload_encoding="json")
    _, avro_definition = generator.generate(original, ["variant"], payload_encoding="avro")
    assert original == before
    assert avro_definition["schemas"] == json_definition["schemas"]
    assert avro_definition["eventTypes"][0]["envelopeMetadata"]["datacontenttype"]["value"] == (
        "application/vnd.apache.avro+avro")
    original["messagegroups"]["base"]["messages"]["reading"]["envelopemetadata"][
        "datacontenttype"] = {"value": "application/vnd.apache.avro+avro"}
    assert generator.generate(original, ["variant"])[1] == avro_definition
    with pytest.raises(ValueError, match="Payload encoding"):
        generator.generate(original, ["variant"], payload_encoding="invalid")


def test_bundle_inlining_and_explicit_root():
    nodes = [
        {"type": "record", "name": "Reading", "namespace": "example",
         "fields": [{"name": "location", "type": "example.Location"}]},
        {"type": "record", "name": "Location", "namespace": "example",
         "fields": [{"name": "latitude", "type": "double"}]},
    ]
    with pytest.raises(ValueError, match="root-record"):
        generator.avro_record(nodes)
    record = generator.avro_record(nodes, "example.Reading")
    assert record["fields"][0]["type"]["type"] == "record"
    assert validate({"location": {"latitude": 51.0}}, record)
    with pytest.raises(ValueError, match="does not match"):
        generator.avro_record(record, "WrongRoot")


def test_portable_conversion_reproduces_pilot_records_from_canonical_structure():
    source = ROOT / "feeders" / "pegelonline"
    canonical = json.loads((source / "xreg" / "pegelonline.xreg.json").read_text(encoding="utf-8"))
    retained = json.loads(
        (source / "fabric" / "schematized" / "EventSchemaSetDefinition.json").read_text(encoding="utf-8"))
    versions = {
        "#/schemagroups/de.wsv.pegelonline.jstruct/schemas/de.wsv.pegelonline.Station": "1",
        "#/schemagroups/de.wsv.pegelonline.jstruct/schemas/de.wsv.pegelonline.CurrentMeasurement": "2",
    }
    _, definition = generator.generate(
        canonical, ["de.wsv.pegelonline"], create_avro_variants=True,
        projected_versions=versions,
    )
    for generated in definition["schemas"]:
        historical = next(item for item in retained["schemas"] if item["id"] == generated["id"])
        version = generated["versions"][0]
        previous = next(item for item in historical["versions"] if item["id"] == version["id"])
        assert version["schema"] == previous["schema"]
    measurement = next(item for item in definition["schemas"] if item["id"].endswith(".CurrentMeasurement"))
    record = json.loads(measurement["versions"][0]["schema"])
    timestamp = next(field for field in record["fields"] if field["name"] == "timestamp")
    assert timestamp["type"] == {
        "type": "string", "x-original-logical-type": "rfc3339-timestamp-millis",
    }
    payload = {
        "station_id": "sensor1", "timestamp": "2026-01-01T10:20:30.123456+01:00",
        "value": 1.0, "stateMnwMhw": None, "stateNswHsw": None, "trend": None,
    }
    assert validate(payload, record, strict=True)
    assert not validate({**payload, "timestamp": 1}, record, strict=True, raise_errors=False)


def test_portable_conversion_preserves_standard_logical_types():
    record = generator.convert_structure({
        "name": "Reading", "type": "object",
        "properties": {
            "timestamp": {"type": "datetime"},
            "date": {"type": "date"},
            "id": {"type": "uuid"},
        },
        "required": ["timestamp", "date", "id"],
    }, None)
    fields = {field["name"]: field["type"] for field in record["fields"]}
    assert fields["timestamp"] == {
        "type": "string", "x-original-logical-type": "rfc3339-timestamp-millis",
    }
    assert fields["date"] == {"type": "string", "x-original-logical-type": "rfc3339-date"}
    assert fields["id"] == {"type": "string", "logicalType": "uuid"}


def test_cli_reproduces_pilot_schema_bytes_without_touching_inputs(tmp_path):
    directory = ROOT / "feeders" / "pegelonline" / "fabric" / "schematized"
    source = directory / "pegelonline.fabric.xreg.json"
    target = tmp_path / "definition.json"
    command = [
        sys.executable, str(SCRIPT), "--registry", str(source),
        "--messagegroup", "de.wsv.pegelonline.avro", "--include-history", "--definition", str(target),
    ]
    subprocess.run(command, check=True)
    actual = json.loads(target.read_text())
    expected = json.loads((directory / "EventSchemaSetDefinition.json").read_text())
    assert actual["schemas"] == expected["schemas"]
    for event, previous in zip(actual["eventTypes"], expected["eventTypes"]):
        assert event["id"] == previous["id"]
        assert event["schemaUrl"] == previous["schemaUrl"]
    first = target.read_bytes()
    subprocess.run(command, check=True)
    assert target.read_bytes() == first


def test_cli_invalid_version_leaves_output_absent(tmp_path):
    source = tmp_path / "registry.json"
    target = tmp_path / "definition.json"
    source.write_text(json.dumps(registry()))
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--registry", str(source), "--messagegroup", "variant",
         "--schema-version", "#/schemagroups/sensors/schemas/Reading=absent",
         "--definition", str(target)], capture_output=True, text=True,
    )
    assert result.returncode == 1
    assert "Missing registry reference" in result.stderr
    assert not target.exists()
