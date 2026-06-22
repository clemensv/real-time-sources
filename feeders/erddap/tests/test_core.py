from __future__ import annotations

import json
from pathlib import Path

import pytest

from erddap_core import ErddapClient, parse_sources, select_entries


@pytest.fixture(autouse=True)
def _clear_erddap_source_env(monkeypatch):
    monkeypatch.delenv("ERDDAP_SOURCES", raising=False)
    monkeypatch.delenv("ERDDAP_SOURCES_FILE", raising=False)
    monkeypatch.delenv("ERDDAP_SELECT", raising=False)


def test_parse_default_catalog_loads_ioos_source():
    sources = parse_sources(None)
    assert len(sources) == 1
    assert sources[0].erddap_id == "ioos-sensors"
    assert sources[0].dataset_id == "org_cormp_sun2"
    assert "sea_water_temperature" in sources[0].variables


def test_default_selector_honors_enabled_flag():
    sources = parse_sources(None)
    assert [source.dataset_id for source in sources] == ["org_cormp_sun2"]


def test_selector_returns_named_sources_in_order():
    raw = json.dumps({"sources": [
        {"name": "a", "erddap_id": "a", "base_url": "https://a.example/erddap", "dataset_id": "a_ds", "variables": ["temp"]},
        {"name": "b", "erddap_id": "b", "base_url": "https://b.example/erddap", "dataset_id": "b_ds", "variables": ["salt"]},
    ]})
    sources = parse_sources(raw, selector="b,a")
    assert [source.erddap_id for source in sources] == ["b", "a"]


def test_selector_star_includes_disabled_templates():
    sources = parse_sources(None, selector="*")
    assert len(sources) >= 2
    assert any(source.erddap_id == "protected-erddap" for source in sources)
    assert any(source.erddap_id == "otn-tracking" for source in sources)


def test_unknown_selector_raises():
    with pytest.raises(ValueError):
        parse_sources(None, selector="does-not-exist")


def test_legacy_erddap_sources_inline_still_works_and_takes_precedence(tmp_path):
    catalog = tmp_path / "custom.sources.json"
    catalog.write_text(json.dumps({"sources": [{
        "name": "catalog",
        "erddap_id": "catalog",
        "base_url": "https://catalog.example/erddap",
        "dataset_id": "catalog_ds",
        "variables": ["temperature"],
    }]}), encoding="utf-8")
    legacy = "legacy|https://legacy.example/erddap|legacy_ds|temp|station|time>=max(time)-2hours"
    sources = parse_sources(legacy, sources_file=str(catalog))
    assert len(sources) == 1
    assert sources[0].erddap_id == "legacy"
    assert sources[0].dataset_id == "legacy_ds"


def test_env_interpolation_on_auth_header(monkeypatch):
    monkeypatch.setenv("ERDDAP_TOKEN", "secret-123")
    raw = json.dumps({"sources": [{
        "name": "private",
        "erddap_id": "private",
        "base_url": "https://private.example/erddap",
        "dataset_id": "private_ds",
        "variables": ["temp"],
        "auth_header": "Bearer ${ERDDAP_TOKEN}",
    }]})
    sources = parse_sources(raw)
    assert sources[0].auth_header == "Bearer secret-123"


def test_erddap_sources_file_env_override(tmp_path, monkeypatch):
    catalog = tmp_path / "custom.sources.json"
    catalog.write_text(json.dumps({"sources": [{
        "name": "only",
        "erddap_id": "only",
        "base_url": "https://only.example/erddap",
        "dataset_id": "only_ds",
        "variables": ["temperature"],
    }]}), encoding="utf-8")
    monkeypatch.setenv("ERDDAP_SOURCES_FILE", str(catalog))
    sources = parse_sources(None)
    assert len(sources) == 1
    assert sources[0].erddap_id == "only"


def test_catalog_only_keys_are_stripped_before_dataclass_construction():
    raw = json.dumps({"sources": [{
        "name": "decorated",
        "enabled": True,
        "description": "Catalog metadata, not an ErddapSource field.",
        "erddap_id": "decorated",
        "base_url": "https://decorated.example/erddap",
        "dataset_id": "decorated_ds",
        "variables": ["temperature"],
    }]})
    sources = parse_sources(raw)
    assert sources[0].erddap_id == "decorated"
    assert not hasattr(sources[0], "enabled")


def test_select_entries_default_skips_disabled():
    entries = [{"name": "a", "enabled": True}, {"name": "b", "enabled": False}]
    assert [entry["name"] for entry in select_entries(entries)] == ["a"]


def test_mock_snapshot_emits_reference_and_telemetry():
    source = parse_sources(None)[0]
    fixture = Path(__file__).resolve().parents[1] / "fixtures" / "mock_erddap.json"
    snap = ErddapClient(str(fixture)).fetch_dataset(source, {}, mock=True)
    assert snap.dataset["dataset_id"] == "org_cormp_sun2"
    assert snap.station["station_id"] == "org_cormp_sun2"
    assert len(snap.observations) == 2
    assert "sea_water_temperature" in snap.observations[0]["measurements"]
    assert snap.state_updates
