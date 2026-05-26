#!/usr/bin/env python3
"""
Merge all *.xreg.json manifests in this repo into one xRegistry import document.

Each source directory contains a single  <source>/xreg/*.xreg.json  file whose
top-level keys are the xRegistry collection names:

    endpoints      – Kafka / MQTT / AMQP endpoint declarations
    messagegroups  – CloudEvents message group definitions
    schemagroups   – JSON Structure (and other) schema groups

This script merges those collections by shallow-merging at the collection level.
Every source uses its own namespace-prefixed IDs (e.g. "DE.Pegelonline",
"IO.AISstream") so there are no key collisions in a well-formed repo.

Usage
-----
  # Write to stdout
  python3 tools/merge-xreg.py

  # Write to file
  python3 tools/merge-xreg.py -o /tmp/combined.json

  # Custom glob pattern (relative to repo root)
  python3 tools/merge-xreg.py --pattern "*/xreg/*.xreg.json" -o combined.json

Exit codes
----------
  0  – success
  1  – no files matched / ID collision detected / JSON parse error
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

COLLECTION_KEYS = ("endpoints", "messagegroups", "schemagroups")

DEFAULT_PATTERN = "*/xreg/*.xreg.json"


def merge(pattern: str, repo_root: Path) -> dict:
    files = sorted(repo_root.glob(pattern))
    if not files:
        sys.exit(f"No files matched pattern: {pattern!r} under {repo_root}")

    combined: dict[str, dict] = {k: {} for k in COLLECTION_KEYS}

    for path in files:
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            sys.exit(f"JSON parse error in {path}: {exc}")

        for key in COLLECTION_KEYS:
            if key not in doc:
                continue
            overlap = set(doc[key]) & set(combined[key])
            if overlap:
                sys.exit(
                    f"ID collision in '{key}' when merging {path}: "
                    f"duplicate IDs {sorted(overlap)}"
                )
            combined[key].update(doc[key])

        print(f"  merged: {path.relative_to(repo_root)}", file=sys.stderr)

    # Drop empty collections so the import body is clean
    return {k: v for k, v in combined.items() if v}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge all *.xreg.json manifests into one xRegistry import document.",
    )
    parser.add_argument(
        "--pattern",
        default=DEFAULT_PATTERN,
        help=f"Glob pattern relative to repo root (default: {DEFAULT_PATTERN!r})",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="-",
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Repository root directory (default: parent of this script's tools/ dir)",
    )
    args = parser.parse_args()

    repo_root = Path(args.root) if args.root else Path(__file__).resolve().parent.parent

    result = merge(args.pattern, repo_root)

    output_json = json.dumps(result, indent=2, ensure_ascii=False) + "\n"

    if args.output == "-":
        sys.stdout.write(output_json)
    else:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_json, encoding="utf-8")
        print(
            f"Wrote {len(result.get('endpoints', {})):,} endpoints, "
            f"{len(result.get('messagegroups', {})):,} messagegroups, "
            f"{len(result.get('schemagroups', {})):,} schemagroups "
            f"→ {out_path}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
