#!/usr/bin/env python3
"""Bind a schematized notebook while preserving every other Fabric definition part."""

from __future__ import annotations

import argparse
import ast
import base64
import binascii
import copy
import json
import re
from pathlib import Path
from typing import Any

from bind_notebook_schemas import bind_notebook


def validate_metadata(metadata: dict[str, Any], environment_id: str, kernel: str) -> None:
    if kernel != "synapse_pyspark":
        raise ValueError("Schematized notebook requires the qualified Spark kernel")
    dependencies = metadata.get("dependencies", {})
    environment = dependencies.get("environment", {})
    if not environment_id or environment.get("environmentId") != environment_id:
        raise ValueError("Notebook must retain the explicitly selected Environment binding")
    if not dependencies.get("lakehouse") or not dependencies.get("kqlDatabases"):
        raise ValueError("Notebook must retain Lakehouse and KQL database bindings")


def bind_native_source(
    source: str, overrides: dict[str, str], payload_encoding: str, environment_id: str,
) -> str:
    metadata_block = re.search(r"(?m)(?:^# META .*(?:\n|$))+", source)
    if metadata_block is None:
        raise ValueError("Expected the native notebook metadata block")
    metadata = json.loads("".join(
        line.removeprefix("# META ") + "\n" for line in metadata_block.group().splitlines()
    ))
    validate_metadata(metadata, environment_id, metadata.get("kernel_info", {}).get("name"))
    assignments: dict[str, list[ast.Assign]] = {
        "SCHEMA_BINDINGS": [], "dataschema_overrides": [], "deployment_payload_encoding": [],
    }
    for node in ast.parse(source).body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id in assignments):
            assignments[node.targets[0].id].append(node)
    if any(len(nodes) != 1 for nodes in assignments.values()):
        raise ValueError("Native notebook needs one literal selection and one deployment mapping")
    selection = ast.get_source_segment(source, assignments["SCHEMA_BINDINGS"][0])
    if selection is None:
        raise ValueError("Native notebook selection has no source text")
    bound = bind_notebook({"cells": [
        {"cell_type": "code", "source": [selection],
         "metadata": {"tags": ["parameters"]}},
        {"cell_type": "code", "source": [],
         "metadata": {"tags": ["deployment-dataschema-overrides"]}},
    ]}, overrides, payload_encoding)
    replacements = {name: nodes[0] for name, nodes in assignments.items() if name != "SCHEMA_BINDINGS"}
    injected = ast.parse("".join(bound["cells"][1]["source"])).body
    lines = source.splitlines(keepends=True)
    for name, node in sorted(replacements.items(), key=lambda item: item[1].lineno, reverse=True):
        if node.end_lineno is None or node.end_col_offset is None:
            raise ValueError("Native notebook mapping has no complete source range")
        tail = lines[node.end_lineno - 1].encode("utf-8")[node.end_col_offset:].decode("utf-8").strip()
        if node.col_offset or (tail and not tail.startswith("#")):
            raise ValueError("Native notebook mappings must occupy separate statements")
        value = next(item for item in injected
                     if isinstance(item, ast.Assign) and isinstance(item.targets[0], ast.Name)
                     and item.targets[0].id == name)
        suffix = "  " + tail if tail else ""
        lines[node.lineno - 1:node.end_lineno] = [ast.unparse(value) + suffix + "\n"]
    result = "".join(lines)
    ast.parse(result)
    return result


def bind_definition(
    definition: dict[str, Any], overrides: dict[str, str], payload_encoding: str,
    *, environment_id: str,
) -> dict[str, Any]:
    parts = definition["parts"]
    notebooks = [part for part in parts if part.get("path") in (
        "notebook-content.ipynb", "notebook-content.py",
    )]
    if len(notebooks) != 1 or notebooks[0].get("payloadType") != "InlineBase64":
        raise ValueError("Expected exactly one inline notebook content definition part")
    content = base64.b64decode(notebooks[0]["payload"], validate=True).decode("utf-8-sig")
    if notebooks[0]["path"] == "notebook-content.py":
        output = bind_native_source(content, overrides, payload_encoding, environment_id)
    else:
        notebook = json.loads(content)
        metadata = notebook["metadata"]
        validate_metadata(metadata, environment_id, metadata.get("kernelspec", {}).get("name"))
        bound = bind_notebook(notebook, overrides, payload_encoding)
        output = json.dumps(bound, indent=2, ensure_ascii=True) + "\n"
    result = copy.deepcopy(definition)
    for part in result["parts"]:
        if part.get("path") == notebooks[0]["path"]:
            part["payload"] = base64.b64encode(output.encode("utf-8")).decode("ascii")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--definition", required=True, type=Path)
    parser.add_argument("--resolved-map", required=True, type=Path)
    parser.add_argument("--payload-encoding", required=True, choices=("json", "avro"))
    parser.add_argument("--environment-id", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    root = Path(__file__).resolve().parents[2]
    if (output.is_relative_to(root)
            or output in (args.definition.resolve(), args.resolved_map.resolve())):
        parser.error("Write the bound definition outside the checkout, distinct from both inputs")
    try:
        result = bind_definition(
            json.loads(args.definition.read_text(encoding="utf-8-sig")),
            json.loads(args.resolved_map.read_text(encoding="utf-8-sig")),
            args.payload_encoding, environment_id=args.environment_id,
        )
        output.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    except (ValueError, KeyError, TypeError, OSError, SyntaxError, binascii.Error) as error:
        parser.exit(1, f"Notebook definition binding failed: {error}\n")


if __name__ == "__main__":
    main()
