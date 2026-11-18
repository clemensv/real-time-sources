"""Audit and complete JSON Structure/Avro message coverage without changing JSON runtimes."""
from __future__ import annotations

import argparse
import copy
import json
import math
import re
from pathlib import Path
from typing import Any

import avro.schema

AVRO_FORMAT = "Avro/1.11.3"
JSON_TYPE = "application/json"
AVRO_TYPE = "application/vnd.apache.org.avro+avro"
BASE_KEYS = ("basemessage", "basemessageuri", "basemessageurl")


def resolve(document: dict, reference: str) -> Any:
    if not reference.startswith(("/", "#/")):
        raise ValueError(f"Expected a local reference: {reference}")
    node = document
    for part in reference.removeprefix("#").strip("/").split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def merge(base: dict, overlay: dict) -> dict:
    result = copy.deepcopy(base)
    for key, value in overlay.items():
        result[key] = (
            merge(result[key], value)
            if isinstance(result.get(key), dict) and isinstance(value, dict)
            else copy.deepcopy(value)
        )
    return result


def materialize(document: dict, message: dict, seen: tuple[str, ...] = ()) -> dict:
    references = [message[key] for key in BASE_KEYS if key in message]
    if len(set(references)) > 1:
        raise ValueError("Conflicting base-message attributes")
    if not references:
        return copy.deepcopy(message)
    reference = references[0]
    if reference in seen:
        raise ValueError(f"Cyclic message inheritance: {reference}")
    return merge(materialize(document, resolve(document, reference), (*seen, reference)), message)


def versioned_schema(resource: dict) -> dict:
    if "schema" in resource:
        return resource
    versions = resource["versions"]
    version_id = resource.get("defaultversionid")
    if version_id is None and len(versions) == 1:
        version_id = next(iter(versions))
    if version_id not in versions:
        raise ValueError("Schema has no unambiguous default version")
    return versions[version_id]


def logical_type_errors(schema: Any, schema_format: str, path: str = "") -> list[str]:
    """Check actual schema nodes, not user data in defaults or documentation."""
    errors: list[str] = []
    match = re.fullmatch(r"Avro/(\d+)\.(\d+)(?:\.(\d+))?", schema_format, re.I)
    if not match:
        return [f"{path}: Avro format must have a version"]
    version = tuple(int(value or 0) for value in match.groups())
    backing = {
        "decimal": ("bytes", "fixed"), "uuid": ("string",),
        "date": ("int",), "time-millis": ("int",), "time-micros": ("long",),
        "timestamp-millis": ("long",), "timestamp-micros": ("long",),
        "duration": ("fixed",),
    }
    if version >= (1, 10, 0):
        backing.update({"local-timestamp-millis": ("long",), "local-timestamp-micros": ("long",)})
    if version >= (1, 12, 0):
        backing.update({
            "uuid": ("string", "fixed"), "big-decimal": ("bytes",),
            "timestamp-nanos": ("long",), "local-timestamp-nanos": ("long",),
        })
    if version < (1, 8, 0):
        backing = {}

    def visit(node: Any, location: str) -> None:
        if isinstance(node, list):
            for index, value in enumerate(node):
                visit(value, f"{location}/{index}")
            return
        if not isinstance(node, dict):
            return
        logical = node.get("logicalType")
        kind = node.get("type")
        if logical is not None:
            if logical not in backing:
                errors.append(f"{location}: nonstandard/version-incompatible logicalType {logical}")
            elif kind not in backing[logical]:
                errors.append(f"{location}: {logical} requires {backing[logical]}, got {kind}")
            elif logical == "decimal":
                precision, scale = node.get("precision"), node.get("scale", 0)
                if type(precision) is not int or precision <= 0 or type(scale) is not int or not 0 <= scale <= precision:
                    errors.append(f"{location}: invalid decimal precision/scale")
                elif kind == "fixed":
                    size = node.get("size")
                    if type(size) is not int or size <= 0 or precision > math.floor((8 * size - 1) * math.log10(2)):
                        errors.append(f"{location}: decimal exceeds fixed size")
            elif logical in ("duration", "uuid") and kind == "fixed":
                if node.get("size") != (12 if logical == "duration" else 16):
                    errors.append(f"{location}: invalid {logical} fixed size")
        if isinstance(kind, (dict, list)):
            visit(kind, f"{location}/type")
        if kind == "record":
            for field in node.get("fields", []):
                if "logicalType" in field:
                    errors.append(f"{location}/{field['name']}: logicalType belongs on the type, not the field")
                visit(field["type"], f"{location}/{field['name']}")
        elif kind == "array":
            visit(node["items"], f"{location}/items")
        elif kind == "map":
            visit(node["values"], f"{location}/values")

    visit(schema, path)
    return errors


def _name(value: str) -> str:
    name = re.sub(r"[^A-Za-z0-9_]", "_", value)
    return name if name and not name[0].isdigit() else "_" + name


# WORKAROUND(clemensv/avrotize#569): replace with its standard-only converter
# when primitive aliases, reference ordering and RFC3339 mappings are corrected.
# WORKAROUND(clemensv/avrotize#570): keep generated documentation on one line
# until the Python generator escapes serialized schema strings correctly.
class StandardAvro:
    """Project the fleet's JSON Structure types to standard Avro schemas.

    Calendar/time strings stay strings: no offset or precision is discarded.
    Avro has no missing record field; optional properties use a null default.
    Source annotations remain in field documentation, not custom logical types.
    """

    def __init__(self, schema: dict, schema_id: str):
        self.schema = schema
        self.schema_id = schema_id
        self.named: dict[str, str] = {}
        self.active_aliases: set[str] = set()

    def convert(self) -> Any:
        root = self.schema.get("$root")
        return self.node({"$ref": root}, self.schema_id) if root else self.node(self.schema, self.schema_id)

    def node(self, schema: Any, hint: str) -> Any:
        if isinstance(schema, str):
            schema = {"type": schema}
        if "$ref" in schema:
            ref = schema["$ref"]
            if ref in self.named:
                return self.named[ref]
            if ref in self.active_aliases:
                raise ValueError(f"Recursive non-record alias: {ref}")
            target = resolve(self.schema, ref)
            fullname = ".".join(_name(part) for part in ref.removeprefix("#/definitions/").split("/"))
            is_named_enum = target.get("type") == "string" and "enum" in target and all(
                isinstance(value, str) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value) for value in target["enum"]
            )
            if target.get("type") == "object" or is_named_enum:
                self.named[ref] = fullname
            self.active_aliases.add(ref)
            result = self.node(target, fullname)
            self.active_aliases.remove(ref)
            return result
        kind = schema.get("type")
        if isinstance(kind, dict):
            return self.node(kind, hint)
        if isinstance(kind, list):
            choices = [self.node({**schema, "type": value}, hint) for value in kind]
            return self.union(choices)
        if kind == "object":
            record: dict[str, Any] = {"type": "record", "name": hint, "fields": []}
            if schema.get("description"):
                record["doc"] = " ".join(schema["description"].splitlines())
            required = schema.get("required", [])
            if any(not isinstance(item, str) for item in required):
                raise ValueError(f"{hint}: alternative required sets need an explicit mapping")
            for name, prop in schema.get("properties", {}).items():
                field_type = self.node(prop, hint + "_types." + _name(name))
                optional = name not in required
                field: dict[str, Any] = {"name": _name(name)}
                if field["name"] != name:
                    field["altnames"] = {"json": name}
                if optional:
                    branches = field_type if isinstance(field_type, list) else [field_type]
                    field_type = ["null", *[branch for branch in branches if branch != "null"]]
                    field["default"] = None
                if "default" in prop:
                    field["default"] = prop["default"]
                    if isinstance(field_type, list) and "null" in field_type:
                        nonnull = [branch for branch in field_type if branch != "null"]
                        field_type = ["null", *nonnull] if field["default"] is None else [*nonnull, "null"]
                field["type"] = field_type
                annotations = {key: value for key, value in prop.items() if key not in ("type", "description", "properties", "items", "values")}
                doc = prop.get("description", "")
                if annotations:
                    doc += " JSON Structure annotations: " + json.dumps(annotations, ensure_ascii=False, sort_keys=True)
                if optional:
                    doc += " An absent JSON property uses the declared default in Avro."
                if doc:
                    field["doc"] = " ".join(doc.strip().splitlines())
                record["fields"].append(field)
            return record
        if kind in ("array", "set"):
            return {"type": "array", "items": self.node(schema["items"], hint + "_item")}
        if kind == "map":
            return {"type": "map", "values": self.node(schema["values"], hint + "_value")}
        if kind == "choice":
            # Tagged JSON choices retain their selector as a one-field record.
            if schema.get("selector") or schema.get("$extends"):
                raise ValueError(f"{hint}: inline choices need an explicit mapping")
            return self.union([
                {"type": "record", "name": hint + "_" + _name(tag),
                 "fields": [{"name": _name(tag), "type": self.node(value, hint + "_" + _name(tag) + "_value")}]}
                for tag, value in schema["choices"].items()
            ])
        if kind == "string" and "enum" in schema:
            symbols = schema["enum"]
            if all(isinstance(value, str) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value) for value in symbols):
                return {"type": "enum", "name": hint, "symbols": symbols}
            return {"type": "string", "doc": "Allowed JSON values: " + json.dumps(symbols)}
        primitive = {
            "null": "null", "boolean": "boolean", "string": "string",
            "integer": "int", "int8": "int", "uint8": "int", "int16": "int",
            "uint16": "int", "int32": "int", "uint32": "long", "int64": "long",
            "float": "float", "double": "double", "number": "double",
            "binary": "bytes", "uri": "string", "jsonpointer": "string",
            "date": "string", "datetime": "string", "time": "string", "duration": "string",
            "uint64": "string", "int128": "string", "uint128": "string",
        }
        if kind == "uuid":
            return {"type": "string", "logicalType": "uuid"}
        if kind == "decimal":
            return {"type": "bytes", "logicalType": "decimal", "precision": schema.get("precision", 34), "scale": schema.get("scale", 7)}
        if kind not in primitive:
            raise ValueError(f"{hint}: unsupported JSON Structure type {kind!r}")
        return primitive[kind]

    @staticmethod
    def union(branches: list) -> Any:
        result: list = []
        for branch in branches:
            for item in branch if isinstance(branch, list) else [branch]:
                if item not in result:
                    result.append(item)
        return result[0] if len(result) == 1 else result


def _schema_ref(document: dict, message: dict) -> tuple[str, str, dict]:
    ref = message["dataschemauri"]
    parts = ref.removeprefix("#").strip("/").split("/")
    if len(parts) != 4 or parts[0] != "schemagroups" or parts[2] != "schemas":
        raise ValueError(f"Unsupported schema resource reference: {ref}")
    return parts[1], parts[3], resolve(document, ref)


def _shape(schema: Any, seen: tuple = ()) -> Any:
    if schema in seen:
        return "recursive"
    if schema.type == "record":
        return {field.name: (_shape(field.type, (*seen, schema)), field.has_default, field.default if field.has_default else None) for field in schema.fields}
    if schema.type == "union":
        return sorted([_shape(branch, (*seen, schema)) for branch in schema.schemas], key=str)
    if schema.type == "array":
        return ("array", _shape(schema.items, (*seen, schema)))
    if schema.type == "map":
        return ("map", _shape(schema.values, (*seen, schema)))
    if schema.type == "enum":
        return ("enum", list(schema.symbols))
    return schema.type


def _preserve_encodings(projected: Any, existing: Any, renames: dict | None = None) -> Any:
    """Keep widened integers and valid native timestamp encodings already in use."""
    if renames is None:
        renames = {}
        result = _preserve_encodings(projected, existing, renames)
        return _rewrite_references(result, renames)
    if isinstance(projected, list):
        branches = existing.schemas if existing.type == "union" else [existing]
        old_nonnull = [branch for branch in branches if branch.type != "null"]
        return [_preserve_encodings(branch, old_nonnull[0], renames) if branch != "null" and len(old_nonnull) == 1 else branch for branch in projected]
    if existing.type == "union":
        branches = [branch for branch in existing.schemas if branch.type != "null"]
        if len(branches) == 1:
            return _preserve_encodings(projected, branches[0], renames)
    if isinstance(projected, str) and projected == existing.type and existing.props.get("logicalType"):
        return existing.to_json()
    if projected == "int" and existing.type == "long":
        return "long"
    if projected == "string" and existing.type == "long" and existing.props.get("logicalType") in (
        "timestamp-millis", "timestamp-micros", "timestamp-nanos",
        "local-timestamp-millis", "local-timestamp-micros", "local-timestamp-nanos",
    ):
        return existing.to_json()
    if isinstance(projected, dict):
        if projected["type"] == "string" and existing.type == "enum" and projected.get("doc", "").startswith("Allowed JSON values: "):
            labels = json.loads(projected["doc"].removeprefix("Allowed JSON values: "))
            if [_name(label) for label in labels] == existing.symbols:
                if existing.fullname in renames.values():
                    return existing.fullname
                renames[existing.fullname] = existing.fullname
                return existing.to_json()
        if projected["type"] == existing.type and existing.type in ("record", "enum", "fixed"):
            renames[projected["name"]] = existing.fullname
            projected["name"] = existing.fullname
        if projected["type"] == existing.type == "record":
            fields = {field.name: field for field in existing.fields}
            for field in projected["fields"]:
                if field["name"] in fields:
                    field["type"] = _preserve_encodings(field["type"], fields[field["name"]].type, renames)
        elif projected["type"] == existing.type == "array":
            projected["items"] = _preserve_encodings(projected["items"], existing.items, renames)
        elif projected["type"] == existing.type == "map":
            projected["values"] = _preserve_encodings(projected["values"], existing.values, renames)
    return projected


def _rewrite_references(schema: Any, renames: dict) -> Any:
    if isinstance(schema, str):
        return renames.get(schema, schema)
    if isinstance(schema, list):
        return [_rewrite_references(branch, renames) for branch in schema]
    if isinstance(schema, dict):
        if schema.get("type") == "record":
            for field in schema["fields"]:
                field["type"] = _rewrite_references(field["type"], renames)
        for key in ("items", "values"):
            if key in schema:
                schema[key] = _rewrite_references(schema[key], renames)
        if isinstance(schema.get("type"), (dict, list)):
            schema["type"] = _rewrite_references(schema["type"], renames)
    return schema


def _valid_default(schema: Any, value: Any) -> bool:
    kind = schema.type
    if kind == "union":
        return _valid_default(schema.schemas[0], value)
    if kind == "null":
        return value is None
    if kind == "boolean":
        return type(value) is bool
    if kind in ("int", "long"):
        bits = 32 if kind == "int" else 64
        return type(value) is int and -(2 ** (bits - 1)) <= value < 2 ** (bits - 1)
    if kind in ("float", "double"):
        return type(value) in (float, int)
    if kind == "string":
        return isinstance(value, str)
    if kind == "enum":
        return value in schema.symbols
    if kind in ("bytes", "fixed"):
        return isinstance(value, str) and all(ord(char) <= 255 for char in value) and (kind != "fixed" or len(value) == schema.size)
    if kind == "array":
        return isinstance(value, list) and all(_valid_default(schema.items, item) for item in value)
    if kind == "map":
        return isinstance(value, dict) and all(isinstance(key, str) and _valid_default(schema.values, item) for key, item in value.items())
    if kind == "record":
        return isinstance(value, dict) and all(
            _valid_default(field.type, value[field.name]) if field.name in value else field.has_default
            for field in schema.fields
        )
    return False


def _default_errors(schema: Any, path: str, seen: tuple = ()) -> list[str]:
    if schema in seen:
        return []
    seen = (*seen, schema)
    errors = []
    if schema.type == "record":
        for field in schema.fields:
            if field.has_default and not _valid_default(field.type, field.default):
                errors.append(f"{path}/{field.name}: default does not match its type/first union branch")
            errors.extend(_default_errors(field.type, f"{path}/{field.name}", seen))
    elif schema.type == "union":
        for branch in schema.schemas:
            errors.extend(_default_errors(branch, path, seen))
    elif schema.type == "array":
        errors.extend(_default_errors(schema.items, path + "/items", seen))
    elif schema.type == "map":
        errors.extend(_default_errors(schema.values, path + "/values", seen))
    return errors


def _timestamps(schema: Any, path: str = "", seen: tuple = ()) -> dict:
    if schema in seen:
        return {}
    seen = (*seen, schema)
    logical = schema.props.get("logicalType", "")
    result = {path: logical} if "timestamp-" in logical else {}
    if schema.type == "record":
        children = [(field.type, path + "/" + field.name) for field in schema.fields]
    elif schema.type == "union":
        children = [(branch, path) for branch in schema.schemas]
    elif schema.type == "array":
        children = [(schema.items, path + "/items")]
    elif schema.type == "map":
        children = [(schema.values, path + "/values")]
    else:
        children = []
    for child, child_path in children:
        result.update(_timestamps(child, child_path, seen))
    return result


def original_groups(document: dict) -> dict:
    return {name: group for name, group in document["messagegroups"].items()
            if not name.endswith((".avro", ".avro.binary"))}


def complete(document: dict) -> dict:
    result = copy.deepcopy(document)
    for group in result["schemagroups"].values():
        for resource in group["schemas"].values():
            for version in resource.get("versions", {}).values():
                fmt = version.get("format", resource.get("format", ""))
                if fmt == "Avro":
                    version["format"] = AVRO_FORMAT
                if fmt.startswith("Avro"):
                    _repair_string_timestamps(version["schema"])
            if resource.get("format") == "Avro":
                resource["format"] = AVRO_FORMAT
    groups = original_groups(result)
    checked: set[tuple[str, str]] = set()
    for group in groups.values():
        for message in group["messages"].values():
            if not any(key in message for key in BASE_KEYS):
                message.setdefault("envelopemetadata", {})["datacontenttype"] = {"type": "string", "value": JSON_TYPE}

    for name, group in groups.items():
        variants = {suffix: {"messagegroupid": name + suffix, "messages": {}} for suffix in (".avro", ".avro.binary")}
        for message_id, message in group["messages"].items():
            effective = materialize(result, message)
            if not effective.get("dataschemaformat", "").startswith("JsonStructure/"):
                raise ValueError(f"{name}/{message_id}: canonical message must use JSON Structure")
            schema_group, schema_id, resource = _schema_ref(result, effective)
            avro_group = schema_group.removesuffix(".jstruct") + ".avro"
            target = result["schemagroups"].setdefault(avro_group, {"schemas": {}})["schemas"]
            source = versioned_schema(resource)
            if schema_id not in target:
                schema = StandardAvro(source["schema"], schema_id).convert()
                target[schema_id] = {
                    "name": resource.get("name", schema_id.rsplit(".", 1)[-1]),
                    "format": AVRO_FORMAT, "defaultversionid": "1",
                    "versions": {"1": {"format": AVRO_FORMAT, "schema": schema}},
                }
            elif (avro_group, schema_id) not in checked:
                previous = versioned_schema(target[schema_id])
                parsed = avro.schema.parse(json.dumps(previous["schema"]))
                projected = _preserve_encodings(StandardAvro(source["schema"], schema_id).convert(), parsed)
                if _shape(parsed) != _shape(avro.schema.parse(json.dumps(projected))):
                    versions = target[schema_id]["versions"]
                    next_version = str(max((int(value) for value in versions if value.isdecimal()), default=0) + 1)
                    versions[next_version] = {"format": AVRO_FORMAT, "schema": projected}
                    target[schema_id]["defaultversionid"] = next_version
                    target[schema_id]["format"] = AVRO_FORMAT
            checked.add((avro_group, schema_id))
            target_format = target[schema_id].get("format") or versioned_schema(target[schema_id]).get("format") or AVRO_FORMAT
            if target_format == "Avro":
                target_format = AVRO_FORMAT
            for suffix, variant in variants.items():
                overlay = {
                    "messageid": message_id,
                    "basemessage": f"/messagegroups/{name}/messages/{message_id}",
                    "dataschemaformat": target_format,
                    "dataschemauri": f"#/schemagroups/{avro_group}/schemas/{schema_id}",
                }
                if suffix == ".avro.binary":
                    overlay["envelopemetadata"] = {"datacontenttype": {"type": "string", "value": AVRO_TYPE}}
                variant["messages"][message_id] = overlay
        for suffix, variant in variants.items():
            result["messagegroups"][name + suffix] = variant

    for endpoint in result["endpoints"].values():
        refs = [ref for ref in endpoint["messagegroups"] if ref.removeprefix("#/messagegroups/") in groups]
        endpoint["messagegroups"] = list(dict.fromkeys(
            [*refs, *(ref + suffix for ref in refs for suffix in (".avro", ".avro.binary"))]
        ))
    return result


def _repair_string_timestamps(node: Any) -> None:
    """Remove invalid annotations without changing already-published string encoding."""
    if isinstance(node, dict):
        if node.get("type") == "string" and node.get("logicalType") == "timestamp-millis":
            del node["logicalType"]
        if node.get("type") == "record":
            for field in node.get("fields", []):
                if field.get("type") == "string" and field.get("logicalType") == "timestamp-millis":
                    del field["logicalType"]
                _repair_string_timestamps(field["type"])
        elif node.get("type") == "array":
            _repair_string_timestamps(node["items"])
        elif node.get("type") == "map":
            _repair_string_timestamps(node["values"])
        elif isinstance(node.get("type"), (dict, list)):
            _repair_string_timestamps(node["type"])
    elif isinstance(node, list):
        for value in node:
            _repair_string_timestamps(value)


def audit(document: dict) -> list[str]:
    errors: list[str] = []
    groups = original_groups(document)
    if not groups:
        errors.append("No canonical message groups")
    for name in document["messagegroups"]:
        base_name = name.removesuffix(".avro.binary").removesuffix(".avro")
        if base_name != name and base_name not in groups:
            errors.append(f"{name}: variant has no canonical message group")
    checked: set[tuple[str, str]] = set()
    for group_name, group in groups.items():
        for message_id, message in group["messages"].items():
            location = f"{group_name}/{message_id}"
            try:
                base = materialize(document, message)
                schema_group, schema_id, resource = _schema_ref(document, base)
                if not base["dataschemaformat"].startswith("JsonStructure/"):
                    errors.append(f"{location}: missing JSON Structure format")
                versioned_schema(resource)
                for suffix, content_type in (("", JSON_TYPE), (".avro", JSON_TYPE), (".avro.binary", AVRO_TYPE)):
                    variant_group = document["messagegroups"][group_name + suffix]
                    if variant_group["messages"].keys() != group["messages"].keys():
                        errors.append(f"{location}: variant message set differs")
                    overlay = variant_group["messages"][message_id]
                    if suffix:
                        expected_base = f"/messagegroups/{group_name}/messages/{message_id}"
                        allowed = {"messageid", "basemessage", "dataschemaformat", "dataschemauri"}
                        if suffix == ".avro.binary":
                            allowed.add("envelopemetadata")
                            if overlay.get("envelopemetadata") != {"datacontenttype": {"type": "string", "value": AVRO_TYPE}}:
                                errors.append(f"{location}{suffix}: unexpected envelope overrides")
                        if overlay.get("basemessage") != expected_base or set(overlay) != allowed or overlay.get("messageid") != message_id:
                            errors.append(f"{location}{suffix}: expected a minimal inherited overlay")
                    variant = materialize(document, overlay)
                    if variant.get("envelopemetadata", {}).get("datacontenttype", {}).get("value") != content_type:
                        errors.append(f"{location}{suffix}: incorrect CloudEvents payload type")
                    if variant.get("protocoloptions") != base.get("protocoloptions"):
                        errors.append(f"{location}{suffix}: protocol options changed")
                    for attr in ("protocol", "envelope", "envelopeoptions"):
                        if variant.get(attr) != base.get(attr):
                            errors.append(f"{location}{suffix}: {attr} changed")
                    for attr in ("type", "source", "subject"):
                        if variant.get("envelopemetadata", {}).get(attr) != base.get("envelopemetadata", {}).get(attr):
                            errors.append(f"{location}{suffix}: {attr} changed")
                    if suffix:
                        _, _, avro_resource = _schema_ref(document, variant)
                        active = versioned_schema(avro_resource)
                        if not re.fullmatch(r"Avro/\d+\.\d+(?:\.\d+)?", variant["dataschemaformat"], re.I):
                            errors.append(f"{location}{suffix}: Avro schema format must be versioned")
                        if variant["dataschemaformat"] != active.get("format", avro_resource.get("format")):
                            errors.append(f"{location}{suffix}: message/schema format differs")
                        expected_uri = f"#/schemagroups/{schema_group.removesuffix('.jstruct')}.avro/schemas/{schema_id}"
                        if variant["dataschemauri"] != expected_uri:
                            errors.append(f"{location}{suffix}: Avro reference does not match canonical schema")
                        pair = (base["dataschemauri"], variant["dataschemauri"])
                        if pair not in checked:
                            parsed = avro.schema.parse(json.dumps(active["schema"]))
                            projected = _preserve_encodings(
                                StandardAvro(versioned_schema(resource)["schema"], schema_id).convert(), parsed
                            )
                            if _shape(parsed) != _shape(avro.schema.parse(json.dumps(projected))):
                                errors.append(f"{location}{suffix}: Avro fields/nullability differ from JSON Structure")
                            checked.add(pair)
            except (KeyError, ValueError, TypeError, avro.errors.AvroException) as exc:
                errors.append(f"{location}: {exc}")
    for name, endpoint in document["endpoints"].items():
        refs = endpoint.get("messagegroups", [])
        if not refs:
            errors.append(f"{name}: endpoint has no message group associations")
        for ref in refs:
            group_name = ref.removeprefix("#/messagegroups/")
            if group_name not in document["messagegroups"]:
                errors.append(f"{name}: dangling group {ref}")
            base_name = group_name.removesuffix(".avro.binary").removesuffix(".avro")
            if base_name in groups:
                for suffix in ("", ".avro", ".avro.binary"):
                    expected = f"#/messagegroups/{base_name}{suffix}"
                    if refs.count(expected) != 1:
                        errors.append(f"{name}: missing/duplicate association {expected}")
    for gid, group in document["schemagroups"].items():
        for sid, resource in group["schemas"].items():
            native_timestamps = None
            for vid, version in resource.get("versions", {}).items():
                fmt = version.get("format", resource.get("format", ""))
                if fmt.startswith("Avro"):
                    errors.extend(logical_type_errors(version["schema"], fmt, f"{gid}/{sid}/{vid}"))
                    try:
                        parsed = avro.schema.parse(json.dumps(version["schema"]))
                        errors.extend(_default_errors(parsed, f"{gid}/{sid}/{vid}"))
                        historical = _timestamps(parsed)
                        if historical:
                            if native_timestamps is None:
                                native_timestamps = _timestamps(avro.schema.parse(json.dumps(versioned_schema(resource)["schema"])))
                            for path, logical in historical.items():
                                if native_timestamps.get(path) != logical:
                                    errors.append(f"{gid}/{sid}: default version loses native {logical} at {path}")
                    except (avro.errors.AvroException, ValueError) as exc:
                        errors.append(f"{gid}/{sid}/{vid}: invalid Avro schema: {exc}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--write", action="store_true", help="Complete inherited variants and missing Avro schemas.")
    parser.add_argument("--report", type=Path, help="Write the full per-manifest inventory and errors.")
    args = parser.parse_args(argv)
    paths = sorted(args.root.glob("**/xreg/*.xreg.json"))
    report = []
    for path in paths:
        document = json.loads(path.read_text(encoding="utf-8-sig"))
        try:
            result = complete(document) if args.write else document
            errors = audit(result)
            if args.write and not errors and result != document:
                path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        except (KeyError, ValueError, TypeError) as exc:
            result, errors = document, [str(exc)]
        report.append({
            "manifest": str(path.relative_to(args.root)),
            "groups": len(original_groups(result)),
            "messages": sum(len(g["messages"]) for g in original_groups(result).values()),
            "messagegroups": {
                name: {
                    mid: {
                        "schema": materialize(result, message).get("dataschemauri"),
                        "format": materialize(result, message).get("dataschemaformat"),
                    } for mid, message in group["messages"].items()
                } for name, group in original_groups(result).items()
            } if not errors else {},
            "endpoints": {name: endpoint.get("messagegroups", []) for name, endpoint in result.get("endpoints", {}).items()},
            "schemas": {
                f"{gid}/{sid}": {
                    "defaultversionid": resource.get("defaultversionid"),
                    "formats": {vid: version.get("format", resource.get("format")) for vid, version in resource.get("versions", {}).items()},
                } for gid, group in result.get("schemagroups", {}).items() for sid, resource in group.get("schemas", {}).items()
            },
            "errors": errors,
        })
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    failures = sum(bool(item["errors"]) for item in report)
    print(f"{len(paths)} manifests, {sum(item['messages'] for item in report)} original messages; {failures} failing manifests")
    for item in report:
        if item["errors"]:
            print(item["manifest"] + ": " + "; ".join(item["errors"][:4]))
    return int(bool(failures) or not paths)


if __name__ == "__main__":
    raise SystemExit(main())
