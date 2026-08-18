from __future__ import annotations

import importlib.util
import json
from pathlib import Path

EXPECTED_XREG_MANIFEST_PATTERN = "feeders/*/xreg/*.xreg.json"


def _load_merge_xreg_module():
    module_path = Path(__file__).resolve().parents[1] / "tools" / "merge-xreg.py"
    spec = importlib.util.spec_from_file_location("merge_xreg", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_merge_truncates_long_message_ids_and_rewrites_base_refs(tmp_path):
    module = _load_merge_xreg_module()
    manifest_dir = tmp_path / "feeders" / "sample-source" / "xreg"
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

    merged = module.merge(EXPECTED_XREG_MANIFEST_PATTERN, tmp_path)

    messages = merged["messagegroups"]["com.example.sample"]["messages"]
    truncated_id = long_id[: module._MAX_ID_LEN]
    assert truncated_id in messages
    assert messages[truncated_id]["messageid"] == truncated_id
    assert messages["com.example.child"]["basemessageuri"] == (
        f"/messagegroups/com.example.sample/messages/{truncated_id}"
    )


def test_default_pattern_targets_feeder_manifests():
    module = _load_merge_xreg_module()
    assert module.DEFAULT_PATTERN == EXPECTED_XREG_MANIFEST_PATTERN


def test_build_xregistry_workflow_uses_expected_manifest_pattern():
    repo_root = Path(__file__).resolve().parents[1]
    workflow = (repo_root / ".github/workflows/build-xregistry-site.yml").read_text(
        encoding="utf-8"
    )
    assert EXPECTED_XREG_MANIFEST_PATTERN in workflow
