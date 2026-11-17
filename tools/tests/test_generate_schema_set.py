"""Shared xRegistry-to-Fabric authoring checks."""

import copy
import importlib.util
import json
from pathlib import Path
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
    ("binary", "JSON-wire"),
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
        message["envelopemetadata"]["datacontenttype"] = {"value": "avro/binary"}
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
    with pytest.warns(UserWarning, match="clemensv/avrotize#571"):
        _, definition = generator.generate(document, ["base"])
    assert len(definition["schemas"]) == 1
    assert len(definition["eventTypes"]) == 2
    schema = json.loads(definition["schemas"][0]["versions"][0]["schema"])
    assert schema["fields"][0]["type"]["logicalType"] == "rfc3339-timestamp-millis"
    for timestamp in ("2026-01-01T10:20:30+01:00", "2026-01-01T09:20:30.123456Z"):
        assert validate({"value": timestamp}, schema)


def test_avrotize_conversion_creates_parallel_inherited_variants():
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
    )
    assert document == original
    assert derived["endpoints"] == original["endpoints"]
    for collection in ("messagegroups", "schemagroups"):
        for key, value in original[collection].items():
            assert derived[collection][key] == value
    variant = derived["messagegroups"]["base.avro"]["messages"]["reading"]
    assert variant["basemessageuri"] == "#/messagegroups/base/messages/reading"
    assert variant["dataschemauri"].endswith("/Reading/versions/7")
    _, regenerated = generator.generate(derived, ["base.avro"])
    assert definition == regenerated
    record = json.loads(definition["schemas"][0]["versions"][0]["schema"])
    assert validate({"id": "sensor1", "state": "OK", "value": None, "location": None}, record)


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
