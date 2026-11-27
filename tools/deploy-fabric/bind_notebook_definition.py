#!/usr/bin/env python3
"""Bind a schematized notebook while preserving every other Fabric definition part."""

from __future__ import annotations

import argparse
import base64
import binascii
import copy
import json
from pathlib import Path
from typing import Any

from bind_notebook_schemas import bind_notebook


def bind_definition(
    definition: dict[str, Any], overrides: dict[str, str], payload_encoding: str,
    *, environment_id: str,
) -> dict[str, Any]:
    parts = definition["parts"]
    notebooks = [part for part in parts if part.get("path") == "notebook-content.ipynb"]
    if len(notebooks) != 1 or notebooks[0].get("payloadType") != "InlineBase64":
        raise ValueError("Expected exactly one inline notebook-content.ipynb definition part")
    notebook = json.loads(base64.b64decode(notebooks[0]["payload"], validate=True).decode("utf-8-sig"))
    metadata = notebook["metadata"]
    if metadata.get("kernelspec", {}).get("name") != "synapse_pyspark":
        raise ValueError("Schematized notebook requires the qualified Spark kernel")
    dependencies = metadata.get("dependencies", {})
    environment = dependencies.get("environment", {})
    if not environment_id or environment.get("environmentId") != environment_id:
        raise ValueError("Notebook must retain the explicitly selected Environment binding")
    if not dependencies.get("lakehouse") or not dependencies.get("kqlDatabases"):
        raise ValueError("Notebook must retain Lakehouse and KQL database bindings")
    bound = bind_notebook(notebook, overrides, payload_encoding)
    result = copy.deepcopy(definition)
    for part in result["parts"]:
        if part.get("path") == "notebook-content.ipynb":
            part["payload"] = base64.b64encode(
                (json.dumps(bound, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
            ).decode("ascii")
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
    except (ValueError, KeyError, TypeError, OSError, binascii.Error) as error:
        parser.exit(1, f"Notebook definition binding failed: {error}\n")


if __name__ == "__main__":
    main()
