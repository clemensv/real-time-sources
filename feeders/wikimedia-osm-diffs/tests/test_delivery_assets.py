"""Delivery asset checks for wikimedia-osm-diffs."""

from __future__ import annotations

import json
from pathlib import Path


SOURCE_DIR = Path(__file__).resolve().parents[1]


def test_missing_arm_templates_exist_and_parse() -> None:
    for name in (
        "azure-template-mqtt.json",
        "azure-template-with-eventgrid-mqtt.json",
        "azure-template-with-servicebus.json",
    ):
        path = SOURCE_DIR / name
        assert path.is_file(), f"Missing {name}"
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        assert data["$schema"].startswith("https://schema.management.azure.com/")
        assert data["resources"]


def test_docs_reference_all_five_azure_templates() -> None:
    readme = (SOURCE_DIR / "README.md").read_text(encoding="utf-8")
    container = (SOURCE_DIR / "CONTAINER.md").read_text(encoding="utf-8")

    for doc in (readme, container):
        assert "Azure-5_templates" in doc
        assert "azure-template-mqtt.json" in doc
        assert "azure-template-with-eventgrid-mqtt.json" in doc
        assert "azure-template-with-servicebus.json" in doc
