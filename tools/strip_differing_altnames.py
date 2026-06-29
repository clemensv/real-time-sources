#!/usr/bin/env python3
"""Strip JSON Structure altnames that would change emitted wire keys."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def strip_differing_altnames(node: Any, property_name: str | None = None) -> int:
    """Remove altnames entries whose value differs from the containing property name."""
    removed = 0
    if isinstance(node, dict):
        altnames = node.get("altnames")
        if property_name is not None and isinstance(altnames, dict):
            for key, value in list(altnames.items()):
                if value != property_name:
                    del altnames[key]
                    removed += 1
            if not altnames:
                del node["altnames"]

        properties = node.get("properties")
        if isinstance(properties, dict):
            for child_name, child in properties.items():
                removed += strip_differing_altnames(child, child_name)

        for key, value in node.items():
            if key == "properties":
                continue
            removed += strip_differing_altnames(value, property_name)
    elif isinstance(node, list):
        for item in node:
            removed += strip_differing_altnames(item, property_name)
    return removed


def manifest_paths(root: Path) -> list[Path]:
    return sorted(root.glob("feeders/*/xreg/*.xreg.json"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove JSON Structure altnames entries whose values differ from their property names."
    )
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument("--write", action="store_true", help="Rewrite changed manifests")
    args = parser.parse_args()

    total = 0
    changed: list[tuple[Path, int]] = []
    for path in manifest_paths(args.root):
        original = path.read_text(encoding="utf-8")
        document = json.loads(original)
        removed = strip_differing_altnames(document)
        if removed:
            changed.append((path, removed))
            total += removed
            if args.write:
                path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for path, removed in changed:
        try:
            rel = path.relative_to(args.root)
        except ValueError:
            rel = path
        print(f"{rel}: {removed}")
    print(f"total: {total}")

    if total and not args.write:
        print("Run again with --write to update manifests.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
