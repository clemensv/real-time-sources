from __future__ import annotations

import json
from pathlib import Path


def _iter_amqp_messages(manifest: dict):
    messagegroups = manifest.get("messagegroups") or {}
    for group in messagegroups.values():
        messages = group.get("messages") or {}
        for message_id, message in messages.items():
            if message.get("protocol") == "AMQP/1.0":
                yield message_id, message


def test_amqp_protocoloptions_use_hyphenated_keys():
    repo_root = Path(__file__).resolve().parents[1]
    invalid_locations: list[str] = []

    for manifest_path in sorted(repo_root.glob("*/xreg/*.xreg.json")):
        document = json.loads(manifest_path.read_text(encoding="utf-8"))
        rel_path = manifest_path.relative_to(repo_root).as_posix()
        for message_id, message in _iter_amqp_messages(document):
            protocoloptions = message.get("protocoloptions")
            if not isinstance(protocoloptions, dict):
                continue
            for key in ("application_properties", "message_annotations", "delivery_annotations"):
                if key in protocoloptions:
                    invalid_locations.append(f"{rel_path}::{message_id}::{key}")

    assert not invalid_locations, (
        "AMQP protocoloptions keys must use hyphen-separated names:\n"
        + "\n".join(sorted(invalid_locations))
    )


def test_entsoe_application_properties_keys_are_lowercase_kebab_case():
    repo_root = Path(__file__).resolve().parents[1]
    manifest_path = repo_root / "entsoe/xreg/entsoe.xreg.json"
    document = json.loads(manifest_path.read_text(encoding="utf-8"))

    invalid_locations: list[str] = []
    for message_id, message in _iter_amqp_messages(document):
        protocoloptions = message.get("protocoloptions")
        if not isinstance(protocoloptions, dict):
            continue
        app_props = protocoloptions.get("application-properties")
        if not isinstance(app_props, dict):
            continue
        for key in ("inDomain", "outDomain", "eventType", "psrType"):
            if key in app_props:
                invalid_locations.append(f"{message_id}::{key}")

    assert not invalid_locations, (
        "ENTSO-E AMQP application-properties keys must be lowercase kebab-case:\n"
        + "\n".join(sorted(invalid_locations))
    )
