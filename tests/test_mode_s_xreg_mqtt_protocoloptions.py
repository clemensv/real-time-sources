from __future__ import annotations

import json
from pathlib import Path


def test_mode_s_mqtt_protocoloptions_are_flat():
    repo_root = Path(__file__).resolve().parents[1]
    manifest_path = repo_root / "mode-s" / "xreg" / "mode_s.xreg.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    mqtt_endpoint = manifest["endpoints"]["Mode_S.Mqtt"]
    endpoint_protocoloptions = mqtt_endpoint["protocoloptions"]
    assert "options" not in endpoint_protocoloptions
    assert "qos" in endpoint_protocoloptions
    assert "retain" in endpoint_protocoloptions

    mqtt_messages = manifest["messagegroups"]["Mode_S.mqtt"]["messages"]
    for mqtt_message in mqtt_messages.values():
        protocoloptions = mqtt_message["protocoloptions"]
        assert "options" not in protocoloptions
        assert "topic" in protocoloptions
        assert "qos" in protocoloptions
