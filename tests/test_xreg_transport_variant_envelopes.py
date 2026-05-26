from __future__ import annotations

import json
from pathlib import Path


def test_transport_variants_with_envelope_metadata_set_cloudevents_envelope():
    repo_root = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    for manifest_path in sorted(repo_root.glob("*/xreg/*.xreg.json")):
        document = json.loads(manifest_path.read_text(encoding="utf-8"))
        messagegroups = document.get("messagegroups") or {}
        for messagegroup_id, messagegroup in messagegroups.items():
            messages = messagegroup.get("messages") or {}
            for message_id, message in messages.items():
                protocol = message.get("protocol")
                if protocol not in {"MQTT/5.0", "AMQP/1.0"}:
                    continue
                if "envelopemetadata" not in message and "envelopeoptions" not in message:
                    continue
                if message.get("envelope") != "CloudEvents/1.0":
                    errors.append(
                        f"{manifest_path.relative_to(repo_root).as_posix()}::{messagegroup_id}/{message_id}"
                    )

    assert not errors, (
        "MQTT/AMQP transport-variant messages with envelopemetadata/envelopeoptions must set "
        '"envelope": "CloudEvents/1.0". Offenders:\n' + "\n".join(errors)
    )
