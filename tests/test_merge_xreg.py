from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def _load_merge_xreg_module():
    module_path = Path(__file__).resolve().parents[1] / "tools" / "merge-xreg.py"
    spec = importlib.util.spec_from_file_location("merge_xreg", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_merge_preserves_long_message_ids_and_base_refs(tmp_path):
    module = _load_merge_xreg_module()
    manifest_dir = tmp_path / "sample-source" / "xreg"
    manifest_dir.mkdir(parents=True)

    long_id = "com.example.very.long.message.identifier.with.more.than.sixtythree.characters"
    manifest = {
        "messagegroups": {
            "com.example.sample": {
                "messages": {
                    long_id: {
                        "messageid": long_id,
                        "envelope": "CloudEvents/1.0",
                        "protocol": "KAFKA",
                    },
                    "com.example.child": {
                        "messageid": "com.example.child",
                        "basemessageuri": f"#/messagegroups/com.example.sample/messages/{long_id}",
                        "protocol": "KAFKA",
                    },
                }
            }
        }
    }
    (manifest_dir / "sample.xreg.json").write_text(json.dumps(manifest), encoding="utf-8")

    merged = module.merge("*/xreg/*.xreg.json", tmp_path)

    messages = merged["messagegroups"]["com.example.sample"]["messages"]
    assert long_id in messages
    assert messages[long_id]["messageid"] == long_id
    assert messages["com.example.child"]["basemessageuri"] == (
        f"/messagegroups/com.example.sample/messages/{long_id}"
    )
