from __future__ import annotations

import json
from pathlib import Path


TARGET_MANIFESTS = (
    Path("dmi/xreg/dmi.xreg.json"),
    Path("noaa-swpc-l1/xreg/noaa_swpc_l1.xreg.json"),
    Path("pegelonline/xreg/pegelonline.xreg.json"),
)


def _walk_json(value, path: str = ""):
    if isinstance(value, dict):
        for key, item in value.items():
            item_path = f"{path}/{key}"
            yield item_path, key, item
            yield from _walk_json(item, item_path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk_json(item, f"{path}/{index}")


def test_protocoloptions_is_used_and_scalar_options_are_unwrapped():
    repo_root = Path(__file__).resolve().parents[1]

    protocolmetadata_locations: list[str] = []
    wrapped_scalar_locations: list[str] = []

    for rel_path in TARGET_MANIFESTS:
        manifest_path = repo_root / rel_path
        document = json.loads(manifest_path.read_text(encoding="utf-8"))

        for json_path, key, value in _walk_json(document):
            if key == "protocolmetadata":
                protocolmetadata_locations.append(f"{rel_path.as_posix()}:{json_path}")
            if key in {"key", "topic", "partition"} and isinstance(value, dict):
                if "type" in value and "value" in value:
                    wrapped_scalar_locations.append(f"{rel_path.as_posix()}:{json_path}")

    errors: list[str] = []
    if protocolmetadata_locations:
        errors.append("Found legacy protocolmetadata keys:")
        errors.extend(sorted(protocolmetadata_locations))
    if wrapped_scalar_locations:
        errors.append("Found wrapped key/topic/partition scalar options:")
        errors.extend(sorted(wrapped_scalar_locations))

    assert not errors, "\n".join(errors)
