from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import json


def _iter_json_structure_schemas(repo_root: Path):
    for manifest_path in sorted(repo_root.glob("*/xreg/*.xreg.json")):
        document = json.loads(manifest_path.read_text(encoding="utf-8"))
        schemagroups = document.get("schemagroups") or {}
        for schemagroup in schemagroups.values():
            schemas = schemagroup.get("schemas") or {}
            for schema_id, schema in schemas.items():
                versions = schema.get("versions") or {}
                for version_id, version in versions.items():
                    schema_format = version.get("format") or schema.get("format") or ""
                    if not str(schema_format).startswith("JsonStructure"):
                        continue
                    yield (
                        manifest_path.relative_to(repo_root).as_posix(),
                        schema_id,
                        version_id,
                        version.get("schema") or {},
                    )


def test_json_structure_schema_ids_are_present_and_unique():
    repo_root = Path(__file__).resolve().parents[1]
    missing_ids: list[str] = []
    schema_id_index: dict[str, list[str]] = defaultdict(list)

    for manifest_path, schema_id, version_id, schema_document in _iter_json_structure_schemas(repo_root):
        schema_uri = schema_document.get("$id")
        location = f"{manifest_path}::{schema_id}@{version_id}"
        if not schema_uri:
            missing_ids.append(location)
            continue
        schema_id_index[str(schema_uri)].append(location)

    errors: list[str] = []
    if missing_ids:
        errors.append("Missing JsonStructure schema $id values:")
        errors.extend(sorted(missing_ids))

    duplicate_ids = {
        schema_uri: locations
        for schema_uri, locations in schema_id_index.items()
        if len(locations) > 1
    }
    if duplicate_ids:
        errors.append("Duplicate JsonStructure schema $id values:")
        for schema_uri in sorted(duplicate_ids):
            errors.append(f"{schema_uri} -> {', '.join(sorted(duplicate_ids[schema_uri]))}")

    assert not errors, "\n".join(errors)