"""Generate JSON-wire Avro variants and the Pegelonline Fabric schema set."""

from __future__ import annotations

import copy
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from avrotize.common import inline_avro_references

SOURCE = Path(__file__).resolve().parents[1]
BASE = "de.wsv.pegelonline"
SCHEMA_GROUP = BASE + ".avro.json"


def build(registry: dict) -> tuple[dict, dict, dict]:
    """Derive Avro using Avrotize without changing existing wire contracts."""
    derived = copy.deepcopy(registry)
    schemas = {}
    messages = {}
    event_types = []
    fabric_schemas = []
    provenance = []
    for message_id, message in registry["messagegroups"][BASE]["messages"].items():
        schema_id = message["dataschemauri"].rsplit("/", 1)[1]
        source_schema = registry["schemagroups"][BASE + ".jstruct"]["schemas"][schema_id]
        version = source_schema["defaultversionid"]
        original = source_schema["versions"][version]["schema"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema.json"
            output = Path(directory) / "schema.avsc"
            path.write_text(json.dumps(original), encoding="utf-8")
            subprocess.run(
                [sys.executable, "-m", "avrotize", "s2a", str(path), "--out", str(output)],
                check=True,
            )
            avro = json.loads(output.read_text(encoding="utf-8"))
        if isinstance(avro, list):
            named = {f"{record['namespace']}.{record['name']}": record for record in avro}
            root = next(record for record in avro if record["name"] == original["name"])
            avro = inline_avro_references(root, named, root["namespace"])
        original_avro = copy.deepcopy(avro)
        projected_version = version
        if message_id.endswith(".CurrentMeasurement"):
            timestamp = next(field for field in avro["fields"] if field["name"] == "timestamp")
            if timestamp["type"] != {"type": "string", "logicalType": "rfc3339-timestamp-millis"}:
                raise ValueError("Avrotize datetime representation changed; requalify the Fabric projection.")
            # WORKAROUND(clemensv/avrotize#571): Fabric rejects this unknown logical type.
            timestamp["type"] = {"type": "string", "x-original-logical-type": "rfc3339-timestamp-millis"}
            projected_version = "2"
        schema_text = json.dumps(avro, ensure_ascii=True, separators=(",", ":"))
        schema_versions = {version: {"format": "Avro/1.12.0", "schema": original_avro}}
        schema_versions[projected_version] = {"format": "Avro/1.12.0", "schema": avro}
        schemas[schema_id] = {
            "format": "Avro/1.12.0",
            "defaultversionid": projected_version,
            "versions": schema_versions,
        }
        messages[message_id] = {
            "basemessageuri": f"/messagegroups/{BASE}/messages/{message_id}",
            "dataschemaformat": "Avro/1.12.0",
            "dataschemauri": f"#/schemagroups/{SCHEMA_GROUP}/schemas/{schema_id}/versions/{projected_version}",
            "envelopemetadata": {"datacontenttype": {"value": "application/json"}},
        }
        wire_type = message["envelopemetadata"]["type"]["value"]
        envelope = copy.deepcopy(message["envelopemetadata"])
        envelope.update({
            "id": {"type": "string", "required": True},
            "specversion": {"type": "string", "required": True, "value": "1.0"},
            "type": {"type": "string", "required": True, "value": wire_type},
            "source": {"type": "uri", "required": True},
            "subject": {"type": "string", "required": True},
            "datacontenttype": {"type": "string", "value": "application/json"},
            "dataschema": {"type": "uri", "required": True},
        })
        event_types.append({
            "id": wire_type, "format": message["envelope"],
            "description": message["description"], "envelopeMetadata": envelope,
            "schemaUrl": f"#/schemas/{schema_id}", "schemaFormat": "Avro/1.12.0",
        })
        fabric_schemas.append({
            "id": schema_id, "format": "Avro/1.12.0",
            "versions": [{"id": key, "format": "Avro/1.12.0",
                          "schema": json.dumps(value["schema"], ensure_ascii=True, separators=(",", ":"))}
                         for key, value in schema_versions.items()],
        })
        provenance.append({
            "message": message_id, "wire_type": wire_type,
            "source_schema": message["dataschemauri"], "source_version": version,
            "projected_version": projected_version,
            "variant": f"#/messagegroups/{BASE}.avro/messages/{message_id}",
            "avro_schema": messages[message_id]["dataschemauri"],
            "schema_sha256": hashlib.sha256(schema_text.encode()).hexdigest(),
        })
    derived["schemagroups"][SCHEMA_GROUP] = {
        "description": "Avrotize-derived Avro contracts for unchanged JSON payloads; existing binary-oriented Avro resources remain intact.",
        "schemas": schemas,
    }
    derived["messagegroups"][BASE + ".avro"] = {
        "description": "Avro schema representation for the existing JSON CloudEvents; no Avro binary serializer or envelope-mode change.",
        "messages": messages,
    }
    return derived, {"eventTypes": event_types, "schemas": fabric_schemas}, {
        "avrotize_version": importlib.metadata.version("avrotize"),
        "source_sha256": hashlib.sha256(json.dumps(registry, sort_keys=True).encode()).hexdigest(),
        "messages": provenance,
        "conversion_limits": [
            "Fabric rejects Avrotize's rfc3339-timestamp-millis extension. Measurement version 2 retains string and records x-original-logical-type; version 1 remains for provenance. Fabric stores timestamp as string; downstream analytics must parse datetime explicitly. Track clemensv/avrotize#571.",
            "String enums become strings; original JSON Structure enum constraints remain authoritative.",
            "Numeric ranges and units are not enforced by generic Avro; preserve and validate the original JSON Structure contract.",
            "Optional source fields may be emitted as null by the generated JSON serializer.",
        ],
    }


def main() -> None:
    registry = json.loads((SOURCE / "xreg" / "pegelonline.xreg.json").read_text(encoding="utf-8"))
    derived, definition, provenance = build(registry)
    output = Path(__file__).with_name("schematized")
    output.mkdir(exist_ok=True)
    for name, value in (
        ("pegelonline.fabric.xreg.json", derived),
        ("EventSchemaSetDefinition.json", definition),
        ("projection-provenance.json", provenance),
    ):
        (output / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    bindings = {
        item["wire_type"]: {
            "source_uri": "xreg://./" + item["source_schema"].removeprefix("#/") + "/versions/" + item["source_version"],
            "projected_version": item["projected_version"],
            "schema_sha256": item["schema_sha256"],
        }
        for item in provenance["messages"]
    }
    notebook_path = SOURCE / "notebook" / "pegelonline-feed.ipynb"
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    parameters = "".join(notebook["cells"][1]["source"])
    start = parameters.index("SCHEMA_BINDINGS = ")
    end = parameters.index("WORKSPACE_ID = ", start)
    parameters = parameters[:start] + "SCHEMA_BINDINGS = " + json.dumps(bindings, indent=4) + "\n" + parameters[end:]
    notebook["cells"][1]["source"] = parameters.splitlines(keepends=True)
    notebook_path.write_text(json.dumps(notebook, indent=1, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
