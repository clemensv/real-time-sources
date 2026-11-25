#!/usr/bin/env python3
"""Inject a deployment-resolved schema URL map into a portable notebook copy."""

from __future__ import annotations

import argparse
import ast
import copy
import json
from pathlib import Path
from pprint import pformat
from typing import Any
from urllib.parse import urlparse

CELL_TAG = "deployment-dataschema-overrides"


def bind_notebook(
    notebook: dict[str, Any], overrides: dict[str, str], payload_encoding: str,
) -> dict[str, Any]:
    if payload_encoding not in ("json", "avro"):
        raise ValueError("Deployment payload encoding must be json or avro")
    cells = notebook["cells"]
    selections = []
    for cell in cells:
        if "parameters" not in cell.get("metadata", {}).get("tags", []):
            continue
        for node in ast.parse("".join(cell["source"])).body:
            if (isinstance(node, ast.Assign) and len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name)
                    and node.targets[0].id == "SCHEMA_BINDINGS"):
                selections.append(ast.literal_eval(node.value))
    if len(selections) != 1 or not selections[0]:
        raise ValueError("Expected one nonempty literal SCHEMA_BINDINGS selection")
    expected = {binding["source_uri"] for binding in selections[0].values()}
    if not isinstance(overrides, dict) or not overrides or set(overrides) != expected:
        raise ValueError("Resolved schema map must cover exactly the selected source URIs")
    for source, target in overrides.items():
        if not source.startswith("xreg://./") or not isinstance(target, str):
            raise ValueError("Expected original xreg schema URIs and registered HTTPS URLs")
        uri = urlparse(target)
        if (uri.scheme != "https" or not uri.hostname or uri.username or uri.password
                or uri.query or uri.fragment or "/versions/" not in uri.path):
            raise ValueError("Expected credential-free registered HTTPS schema-version URLs")
    tagged = [index for index, cell in enumerate(cells)
              if CELL_TAG in cell.get("metadata", {}).get("tags", [])]
    if len(tagged) != 1 or cells[tagged[0]]["cell_type"] != "code":
        raise ValueError("Expected exactly one schema mapping code cell")
    result = copy.deepcopy(notebook)
    cell = result["cells"][tagged[0]]
    cell["source"] = (
        "# Resolved and fingerprint-verified during deployment; keep this copy outside Git.\n"
        + "dataschema_overrides = " + pformat(overrides, sort_dicts=True, width=100) + "\n"
        + f"deployment_payload_encoding = {payload_encoding!r}\n"
    ).splitlines(keepends=True)
    cell["outputs"] = []
    cell["execution_count"] = None
    for item in result["cells"]:
        if item["cell_type"] == "code":
            ast.parse("".join(item["source"]))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", required=True, type=Path)
    parser.add_argument("--resolved-map", required=True, type=Path)
    parser.add_argument("--payload-encoding", required=True, choices=("json", "avro"),
                        help="Encoding qualified against registered metadata and history serialization")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    output = args.output.resolve()
    if (output == args.notebook.resolve() or output == args.resolved_map.resolve()
            or output.is_relative_to(root)):
        parser.error("Write the deployment copy outside the checkout, distinct from both inputs")
    try:
        notebook = json.loads(args.notebook.read_text(encoding="utf-8"))
        overrides = json.loads(args.resolved_map.read_text(encoding="utf-8"))
        result = bind_notebook(notebook, overrides, args.payload_encoding)
        output.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(1, f"Notebook binding failed: {error}\n")


if __name__ == "__main__":
    main()
