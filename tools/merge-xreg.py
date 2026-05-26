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

def _normalize_refs(obj: object) -> object:
    """Recursively replace '#/'-prefixed XID references with absolute '/' XIDs.

    The xreg document format uses JSON-Pointer-style '#/collection/id' as
    local references within a single file.  When importing into xrserver the
    registry becomes the root context, so '#/messagegroups/foo' must become
    the absolute XID '/messagegroups/foo'.  xrserver rejects the '#/' form.
    """
    if isinstance(obj, str):
        return obj[1:] if obj.startswith("#/") else obj
    if isinstance(obj, list):
        return [_normalize_refs(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _normalize_refs(v) for k, v in obj.items()}
    return obj


# Maps old/deprecated attribute names → current spec attribute names at the
# message-definition level.  These renames happened in the spec after
# xrcg 0.10.x was released; xrserver now only accepts the new names.
_MESSAGE_ATTR_RENAMES: dict[str, str] = {
    "basemessageurl": "basemessageuri",
    "basemessage": "basemessageuri",
    "protocolmetadata": "protocoloptions",
}

# AMQP protocoloptions keys use hyphens in the spec model but were emitted
# with underscores by older xrcg versions.
_AMQP_PO_RENAMES: dict[str, str] = {
    "application_properties": "application-properties",
    "message_annotations": "message-annotations",
    "delivery_annotations": "delivery-annotations",
}

# MQTT protocoloptions may carry a legacy 'options' sub-object whose keys
# map to the top-level protocoloptions attributes required by the spec model.
_MQTT_OPTIONS_MAP: dict[str, str] = {
    "topic": "topic_name",
    "qos": "qos",
    "retain": "retain",
}

# The spec model's envelopemetadata tightly constrains the 'type' value for
# certain CloudEvents attributes.  xrcg sometimes emits incorrect types; these
# overrides force the correct values regardless of what xrcg generated.
_EM_TYPE_OVERRIDES: dict[str, str] = {
    "time": "timestamp",        # RFC3339 timestamp — the ONLY allowed type
    "dataschema": "uritemplate",  # URI template — the ONLY allowed type
}

# Sub-attributes inside envelopemetadata entries that are not defined in the
# spec model and must be stripped before import.
_EM_INVALID_SUBATTRS: frozenset[str] = frozenset({"name"})


import re as _re

_CAMEL_RE = _re.compile(r"(?<=[a-z0-9])([A-Z])")


def _camel_to_kebab(name: str) -> str:
    """Convert camelCase or PascalCase to kebab-case (all lowercase)."""
    return _CAMEL_RE.sub(r"-\1", name).lower()


def _normalize_protocol_options(msg: dict) -> None:
    """Fix protocol-specific keys inside ``protocoloptions`` in-place."""
    po = msg.get("protocoloptions")
    if not isinstance(po, dict):
        return
    protocol = msg.get("protocol", "")

    if protocol == "AMQP/1.0":
        for old, new in _AMQP_PO_RENAMES.items():
            if old in po:
                po[new] = po.pop(old)
        # AMQP application-properties map keys must match namecharset=extended
        # (^[a-z0-9][a-z0-9_.:\-]{0,62}$).  Convert camelCase → kebab-case.
        ap = po.get("application-properties")
        if isinstance(ap, dict):
            fixed: dict = {}
            for k, v in ap.items():
                normalized_k = _camel_to_kebab(k)
                fixed[normalized_k] = v
            po["application-properties"] = fixed

    elif protocol == "KAFKA":
        # Older xrcg wrapped scalar protocoloptions values as objects with
        # {type, value, description}.  The spec model expects direct scalar values.
        for scalar_key in ("key", "key_base64", "topic", "partition"):
            val = po.get(scalar_key)
            if isinstance(val, dict) and "value" in val:
                po[scalar_key] = val["value"]

    elif protocol.startswith("MQTT/"):
        # Flatten legacy 'options' wrapper into the parent dict
        inner = po.pop("options", None)
        if isinstance(inner, dict):
            for inner_key, outer_key in _MQTT_OPTIONS_MAP.items():
                if inner_key in inner and outer_key not in po:
                    po[outer_key] = inner[inner_key]
            # Preserve unmapped keys that are already valid spec names
            for k, v in inner.items():
                if k not in _MQTT_OPTIONS_MAP and k not in po:
                    po[k] = v


def _normalize_message_attrs(messagegroups: dict) -> dict:
    """Rename deprecated attributes inside every message definition.

    Applies :data:`_MESSAGE_ATTR_RENAMES` at the message-definition level,
    normalises the bare ``id`` field to ``messageid``, and fixes
    protocol-specific ``protocoloptions`` key names.
    """
    for mg in messagegroups.values():
        for msg_id, msg in mg.get("messages", {}).items():
            # Rename deprecated top-level message attributes
            for old, new in _MESSAGE_ATTR_RENAMES.items():
                if old in msg:
                    msg[new] = msg.pop(old)
            # Normalise bare 'id' → 'messageid'; also ensure messageid always
            # matches the message's own map key (xrserver requires this).
            if "id" in msg and "messageid" not in msg:
                msg["messageid"] = msg.pop("id")
            msg["messageid"] = msg_id
            # Fix protocol-specific protocoloptions keys
            _normalize_protocol_options(msg)
            # Fix invalid envelopemetadata attribute type values.
            # The spec model constrains which types are valid per CloudEvents
            # attribute; xrcg sometimes emits wrong types (e.g. 'uritemplate'
            # for 'time' which must always be 'timestamp').
            em = msg.get("envelopemetadata")
            if isinstance(em, dict):
                for attr, forced_type in _EM_TYPE_OVERRIDES.items():
                    if attr in em and isinstance(em[attr], dict):
                        em[attr]["type"] = forced_type
                # Strip sub-attributes that are not in the spec model
                # (valid sub-attrs: description, required, type, value)
                for ce_attr, ce_val in em.items():
                    if isinstance(ce_val, dict):
                        for invalid_key in _EM_INVALID_SUBATTRS:
                            ce_val.pop(invalid_key, None)
            # 'envelopemetadata'/'envelopeoptions' are only valid sibling
            # attributes of envelope="CloudEvents/1.0"; transport-variant
            # messages that reference a base via basemessageuri may omit
            # envelope, causing xrserver to reject the attribute.
            if ("envelopemetadata" in msg or "envelopeoptions" in msg) and "envelope" not in msg:
                msg["envelope"] = "CloudEvents/1.0"
    return messagegroups


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
            normalized = _normalize_refs(doc[key])
            overlap = set(normalized) & set(combined[key])
            if overlap:
                sys.exit(
                    f"ID collision in '{key}' when merging {path}: "
                    f"duplicate IDs {sorted(overlap)}"
                )
            combined[key].update(normalized)

        print(f"  merged: {path.relative_to(repo_root)}", file=sys.stderr)

    # Fix deprecated / renamed attributes before returning
    if "messagegroups" in combined:
        _normalize_message_attrs(combined["messagegroups"])

    # WORKAROUND(xregistry/xrserver): xrserver truncates message IDs (and
    # other XID path components) at 64 characters when storing them in the
    # registry database, but accepts longer IDs at import time without
    # error. The download step then fails to resolve cross-references
    # (basemessageuri) because the stored ID is truncated but the reference
    # is not. Until the upstream fix lands, truncate long message IDs and
    # rewrite basemessageuri references to match.
    if "messagegroups" in combined:
        _truncate_long_message_ids(combined["messagegroups"])

    # Drop empty collections so the import body is clean
    return {k: v for k, v in combined.items() if v}


_MAX_ID_LEN = 64


def _truncate_long_message_ids(messagegroups: dict) -> None:
    """Truncate message IDs > _MAX_ID_LEN and rewrite cross-references."""
    rename_map: dict[str, str] = {}
    for mgid, mg in messagegroups.items():
        msgs = mg.get("messages", {})
        new_msgs: dict = {}
        for mid, m in msgs.items():
            if len(mid) > _MAX_ID_LEN:
                new_mid = mid[:_MAX_ID_LEN]
                if new_mid in new_msgs or new_mid in msgs:
                    raise SystemExit(
                        f"Truncation collision in {mgid}: {mid} -> {new_mid}"
                    )
                rename_map[f"/messagegroups/{mgid}/messages/{mid}"] = (
                    f"/messagegroups/{mgid}/messages/{new_mid}"
                )
                m["messageid"] = new_mid
                new_msgs[new_mid] = m
            else:
                new_msgs[mid] = m
        mg["messages"] = new_msgs

    if not rename_map:
        return

    # Rewrite all basemessageuri references inside messagegroups
    for mg in messagegroups.values():
        for m in mg.get("messages", {}).values():
            ref = m.get("basemessageuri")
            if isinstance(ref, str) and ref in rename_map:
                m["basemessageuri"] = rename_map[ref]


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
