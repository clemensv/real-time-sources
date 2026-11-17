#!/usr/bin/env python3
"""Generate portable Fabric Event Schema Set definitions from local xRegistry."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any
from urllib.parse import unquote
import warnings

AVRO = "Avro/1.12.0"
Json = dict[str, Any]


def reference_parts(uri: str) -> list[str]:
    if uri.startswith("xreg://./"):
        uri = uri[len("xreg://."):]
    elif uri.startswith("#/"):
        uri = uri[1:]
    if not uri.startswith("/") or "?" in uri or "#" in uri:
        raise ValueError(f"Only local registry references are supported: {uri}")
    return [unquote(part).replace("~1", "/").replace("~0", "~") for part in uri[1:].split("/")]


def local_reference(parts: list[str]) -> str:
    return "#/" + "/".join(part.replace("~", "~0").replace("/", "~1") for part in parts)


def lookup(document: Json, parts: list[str]) -> Json:
    node = document
    for part in parts:
        if not isinstance(node, dict) or part not in node:
            raise ValueError(f"Missing registry reference: {local_reference(parts)}")
        node = node[part]
    if not isinstance(node, dict):
        raise ValueError(f"Registry reference is not an object: {local_reference(parts)}")
    return node


def merge(base: Json, overrides: Json) -> Json:
    result = copy.deepcopy(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def resolve_message(document: Json, parts: list[str], seen: tuple[str, ...] = ()) -> Json:
    reference = local_reference(parts)
    if reference in seen:
        raise ValueError(f"Cyclic message inheritance: {reference}")
    if len(parts) != 4 or parts[0] != "messagegroups" or parts[2] != "messages":
        raise ValueError(f"Expected a message reference: {reference}")
    message = lookup(document, parts)
    parent = message.get("basemessageuri")
    if parent:
        return merge(resolve_message(document, reference_parts(parent), seen + (reference,)), message)
    return copy.deepcopy(message)


def schema_selection(document: Json, message: Json, versions: dict[str, str]) -> tuple[list[str], str, Json, str]:
    parts = reference_parts(message["dataschemauri"])
    if (len(parts) not in (4, 6) or parts[0] != "schemagroups" or parts[2] != "schemas"
            or (len(parts) == 6 and parts[4] != "versions")):
        raise ValueError("Expected a schema resource or schema-version reference")
    resource = lookup(document, parts[:4])
    key = local_reference(parts[:4])
    version_id = versions.get(key) or (parts[5] if len(parts) == 6 else resource.get("defaultversionid"))
    if not version_id:
        raise ValueError(f"Pin a version or declare defaultversionid: {key}")
    version = lookup(resource, ["versions", version_id])
    schema_format = version.get("format") or resource.get("format") or message.get("dataschemaformat")
    if not isinstance(schema_format, str):
        raise ValueError(f"Missing schema format: {key}")
    return parts[:4], version_id, version, schema_format


def avro_record(schema: Any, root_name: str | None = None) -> Json:
    from fastavro import parse_schema

    if isinstance(schema, str):
        schema = json.loads(schema)
    schema = copy.deepcopy(schema)
    if isinstance(schema, list):
        from avrotize.common import inline_avro_references

        named = {}
        for node in schema:
            if not isinstance(node, dict) or "name" not in node:
                raise ValueError("An Avro schema bundle must contain named definitions")
            full_name = node["name"]
            if "." not in full_name and node.get("namespace"):
                full_name = node["namespace"] + "." + full_name
            if full_name in named:
                raise ValueError(f"Duplicate Avro name: {full_name}")
            named[full_name] = node
        roots = [node for name, node in named.items()
                 if node.get("type") == "record"
                 and (root_name == name or root_name == node["name"])]
        if len(roots) != 1:
            raise ValueError("Avro bundle requires one unambiguous --root-record selection")
        root = roots[0]
        schema = inline_avro_references(root, named, root.get("namespace", ""))
    if not isinstance(schema, dict) or schema.get("type") != "record":
        raise ValueError("Fabric event schemas must have a record root")
    full_name = schema["name"]
    if "." not in full_name and schema.get("namespace"):
        full_name = schema["namespace"] + "." + full_name
    if root_name and root_name not in (schema["name"], full_name):
        raise ValueError(f"Selected root record {root_name!r} does not match {full_name!r}")
    parse_schema(schema)
    return schema


def convert_structure(schema: Json, root_name: str | None) -> Json:
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "schema.json"
        target = Path(directory) / "schema.avsc"
        source.write_text(json.dumps(schema), encoding="utf-8")
        subprocess.run(
            [sys.executable, "-m", "avrotize", "s2a", str(source), "--out", str(target),
             "--no-custom-logical-types"],
            check=True,
        )
        return avro_record(json.loads(target.read_text(encoding="utf-8")), root_name or schema.get("name"))


def envelope_metadata(message: Json) -> Json:
    if message.get("envelope") != "CloudEvents/1.0":
        raise ValueError("Only CloudEvents/1.0 messages are supported")
    metadata = copy.deepcopy(message.get("envelopemetadata", {}))
    event_type = metadata.get("type", {}).get("value")
    if not isinstance(event_type, str) or not event_type or "{" in event_type:
        raise ValueError("CloudEvents type must have a literal nonempty value")
    for name, type_name in (
        ("type", "string"), ("source", "uri"), ("subject", "string"),
        ("id", "string"), ("specversion", "string"),
        ("datacontenttype", "string"), ("dataschema", "uri"),
    ):
        entry = metadata.setdefault(name, {})
        entry["type"] = type_name
        if name != "datacontenttype":
            entry["required"] = True
    metadata["specversion"]["value"] = "1.0"
    content_type = metadata["datacontenttype"].setdefault("value", "application/json")
    if not isinstance(content_type, str):
        raise ValueError("datacontenttype must have a literal JSON media type")
    media_type = content_type.split(";", 1)[0].strip().lower()
    if media_type != "application/json" and not media_type.endswith("+json"):
        raise ValueError("This tool targets JSON-wire messages, not Avro-binary payloads")
    for name, entry in metadata.items():
        value = entry.get("value")
        if isinstance(value, str) and ("{" in value or "}" in value):
            entry.pop("value")
        if entry.get("type") == "uritemplate":
            entry["type"] = "uri" if name in ("source", "dataschema") else "string"
    return metadata


def warn_logical_types(node: Any) -> None:
    standard = {
        "decimal", "big-decimal", "uuid", "date", "time-millis", "time-micros",
        "timestamp-millis", "timestamp-micros", "timestamp-nanos",
        "local-timestamp-millis", "local-timestamp-micros", "local-timestamp-nanos", "duration",
    }
    if isinstance(node, dict):
        logical_type = node.get("logicalType")
        if logical_type and logical_type not in standard:
            warnings.warn(
                f"Nonstandard logicalType {logical_type!r} preserved unchanged. "
                "Avro readers must ignore unknown logical types, but Fabric may reject this "
                "schema. Reconvert JSON Structure with Avrotize's --no-custom-logical-types "
                "option; existing Avro schemas are not rewritten. Generation is not live acceptance.",
                stacklevel=2,
            )
        for value in node.values():
            warn_logical_types(value)
    elif isinstance(node, list):
        for value in node:
            warn_logical_types(value)


def generate(
    registry: Json,
    groups: list[str],
    *,
    versions: dict[str, str] | None = None,
    roots: dict[str, str] | None = None,
    projected_versions: dict[str, str] | None = None,
    create_avro_variants: bool = False,
    include_history: bool = False,
) -> tuple[Json, Json]:
    versions = versions or {}
    roots = roots or {}
    projected_versions = projected_versions or {}
    document = copy.deepcopy(registry)
    definition: Json = {"eventTypes": [], "schemas": []}
    schema_outputs: dict[str, Json] = {}
    event_types: set[str] = set()
    used: set[str] = set()
    converted: set[str] = set()
    for group_id in groups:
        messages = lookup(registry, ["messagegroups", group_id]).get("messages")
        if not isinstance(messages, dict) or not messages:
            raise ValueError(f"Message group is empty: {group_id}")
        variants: Json = {}
        new_schemas: Json = {}
        for message_id in messages:
            message_parts = ["messagegroups", group_id, "messages", message_id]
            message = resolve_message(registry, message_parts)
            metadata = envelope_metadata(message)
            event_type = metadata["type"]["value"]
            if event_type in event_types:
                raise ValueError(f"Duplicate CloudEvents wire type: {event_type}")
            event_types.add(event_type)
            parts, selected, version, schema_format = schema_selection(registry, message, versions)
            key = local_reference(parts)
            used.add(key)
            schema_id = parts[3]
            resource = lookup(registry, parts)
            if schema_format.startswith("Avro/"):
                root = roots.get(key)
                versions_out = []
                for version_id, item in resource["versions"].items():
                    if version_id != selected and not include_history:
                        continue
                    if (item.get("format") or resource.get("format")
                            or message.get("dataschemaformat")) != schema_format:
                        if version_id == selected:
                            raise ValueError(f"Inconsistent selected Avro format: {key}")
                        continue
                    record = avro_record(item["schema"], root)
                    versions_out.append({"id": version_id, "format": AVRO,
                                         "schema": json.dumps(record, ensure_ascii=True, separators=(",", ":"))})
            elif schema_format.startswith("JsonStructure/") and create_avro_variants:
                if key not in projected_versions:
                    raise ValueError(f"Pin --projected-version {key}=VERSION for the new Avro schema")
                record = convert_structure(version["schema"], roots.get(key))
                converted.add(key)
                selected = projected_versions[key]
                versions_out = [{"id": selected, "format": AVRO,
                                 "schema": json.dumps(record, ensure_ascii=True, separators=(",", ":"))}]
                new_schemas[schema_id] = {
                    "format": AVRO, "defaultversionid": selected,
                    "versions": {selected: {"format": AVRO, "schema": record}},
                }
                target_group = group_id + ".avro.json"
                variants[message_id] = {
                    "basemessageuri": local_reference(message_parts),
                    "dataschemaformat": AVRO,
                    "dataschemauri": local_reference(
                        ["schemagroups", target_group, "schemas", schema_id, "versions", selected]),
                    "envelopemetadata": {"datacontenttype": {"value": "application/json"}},
                }
            else:
                raise ValueError(
                    f"{key} uses {schema_format}; select an Avro variant or use --create-avro-variants "
                    "for JSON Structure. Schema payload rewrites are not supported.")
            selected_schema = next(item for item in versions_out if item["id"] == selected)
            warn_logical_types(json.loads(selected_schema["schema"]))
            schema_output = {"id": schema_id, "format": AVRO, "versions": versions_out}
            if schema_id in schema_outputs and schema_outputs[schema_id] != schema_output:
                raise ValueError(f"Conflicting Fabric schema ID across groups: {schema_id}")
            schema_outputs[schema_id] = schema_output
            definition["eventTypes"].append({
                "id": event_type, "format": "CloudEvents/1.0",
                "description": message.get("description", ""),
                "envelopeMetadata": metadata,
                "schemaUrl": "#/schemas/" + schema_id, "schemaFormat": AVRO,
            })
        if variants:
            variant_group = group_id + ".avro"
            schema_group = group_id + ".avro.json"
            if variant_group in document["messagegroups"] or schema_group in document["schemagroups"]:
                raise ValueError(f"Refusing to overwrite existing variant group: {variant_group}")
            document["messagegroups"][variant_group] = {"messages": variants}
            document["schemagroups"][schema_group] = {"schemas": new_schemas}
    unused = ((set(versions) | set(roots)) - used) | (set(projected_versions) - converted)
    if unused:
        raise ValueError(f"Selections do not match selected messages: {sorted(unused)}")
    definition["schemas"] = list(schema_outputs.values())
    return document, definition


def selection_map(values: list[str]) -> dict[str, str]:
    result = {}
    for item in values:
        reference, separator, value = item.rpartition("=")
        if not separator or not value:
            raise ValueError(f"Expected local schema resource URI=VALUE: {item}")
        parts = reference_parts(reference)
        if len(parts) != 4 or parts[0] != "schemagroups" or parts[2] != "schemas":
            raise ValueError(f"Expected schema resource reference: {reference}")
        key = local_reference(parts)
        if key in result:
            raise ValueError(f"Duplicate selection: {reference}")
        result[key] = value
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--messagegroup", action="append", required=True)
    parser.add_argument("--definition", type=Path, required=True)
    parser.add_argument("--output-registry", type=Path)
    parser.add_argument("--schema-version", action="append", default=[], metavar="SCHEMA_URI=VERSION")
    parser.add_argument("--root-record", action="append", default=[], metavar="SCHEMA_URI=AVRO_NAME")
    parser.add_argument("--projected-version", action="append", default=[], metavar="SCHEMA_URI=VERSION")
    parser.add_argument("--create-avro-variants", action="store_true")
    parser.add_argument("--include-history", action="store_true",
                        help="Include other Avro versions of selected schema resources")
    args = parser.parse_args(argv)
    if args.create_avro_variants and not args.output_registry:
        parser.error("--create-avro-variants requires --output-registry")
    outputs = [args.definition] + ([args.output_registry] if args.output_registry else [])
    if len({path.resolve() for path in [args.registry, *outputs]}) != len(outputs) + 1:
        parser.error("Input registry and output paths must be distinct")
    try:
        registry = json.loads(args.registry.read_text(encoding="utf-8-sig"))
        derived, definition = generate(
            registry, args.messagegroup, versions=selection_map(args.schema_version),
            roots=selection_map(args.root_record), create_avro_variants=args.create_avro_variants,
            projected_versions=selection_map(args.projected_version),
            include_history=args.include_history,
        )
        encoded = [(args.definition, json.dumps(definition, indent=2, ensure_ascii=True) + "\n")]
        if args.output_registry:
            encoded.append((args.output_registry, json.dumps(derived, indent=2, ensure_ascii=True) + "\n"))
        for path, text in encoded:
            path.write_text(text, encoding="utf-8")
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Schema-set generation failed: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
