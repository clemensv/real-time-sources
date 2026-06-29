#!/usr/bin/env python3
"""Write an xRegistry view containing producer endpoints and their groups."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any


def _ref_name(ref: str) -> str | None:
    prefix = "#/messagegroups/"
    return ref[len(prefix) :] if isinstance(ref, str) and ref.startswith(prefix) else None


def producer_view(document: dict[str, Any]) -> dict[str, Any]:
    view = copy.deepcopy(document)
    endpoints = view.get("endpoints")
    if not isinstance(endpoints, dict):
        return view

    producer_endpoints: dict[str, Any] = {}
    referenced_groups: set[str] = set()
    for name, endpoint in endpoints.items():
        usage = endpoint.get("usage", []) if isinstance(endpoint, dict) else []
        if "producer" not in usage:
            continue
        producer_endpoints[name] = endpoint
        for ref in endpoint.get("messagegroups", []):
            group_name = _ref_name(ref)
            if group_name:
                referenced_groups.add(group_name)

    view["endpoints"] = producer_endpoints

    messagegroups = view.get("messagegroups")
    if isinstance(messagegroups, dict) and referenced_groups:
        view["messagegroups"] = {
            name: group for name, group in messagegroups.items() if name in referenced_groups
        }

    return view


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: xreg-producer-view.py <input.xreg.json> <output.xreg.json>", file=sys.stderr)
        return 2
    source = Path(argv[1])
    target = Path(argv[2])
    document = json.loads(source.read_text(encoding="utf-8"))
    target.write_text(json.dumps(producer_view(document), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
