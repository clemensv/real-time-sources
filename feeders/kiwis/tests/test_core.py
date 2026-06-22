import json

import pytest

from kiwis_core import KiWISClient, MOCK_ENDPOINTS, load_endpoints, select_entries
from kiwis_core.core import normalize_station, normalize_timeseries, normalize_value


def test_default_mock_cycle_shapes():
    endpoint = load_endpoints(mock=True)[0]
    client = KiWISClient(endpoint, mock=True)
    station = normalize_station(endpoint, client.stations()[0])
    assert station["kiwis_id"] == "sepa"
    assert station["station_id"] == "36870"
    ts = normalize_timeseries(endpoint, client.timeseries()[0])
    assert ts["ts_id"] == "65452010"
    value = normalize_value(endpoint, client.timeseries()[0], client.values(["65452010"])["65452010"][0])
    assert value["value"] == 0.2
    assert value["quality_code"] == 254


def test_csv_endpoint_config():
    endpoints = load_endpoints("x,https://example.invalid/KiWIS,0,station_id=1,station_id=1,2,PT1H,")
    assert endpoints[0].kiwis_id == "x"
    assert endpoints[0].ts_ids == "2"


def test_default_catalog_loads_enabled_sepa_endpoint(monkeypatch):
    monkeypatch.delenv("KIWIS_ENDPOINTS", raising=False)
    monkeypatch.delenv("KIWIS_SOURCES_FILE", raising=False)
    monkeypatch.delenv("KIWIS_SOURCES", raising=False)
    endpoints = load_endpoints()
    assert len(endpoints) == 1
    assert endpoints[0].kiwis_id == "sepa"
    assert endpoints[0].base_url == "https://timeseries.sepa.org.uk/KiWIS/KiWIS"


def test_selector_returns_named_entries_in_order():
    raw = json.dumps({"sources": [
        {"name": "a", "kiwis_id": "a", "base_url": "https://example.invalid/a"},
        {"name": "b", "kiwis_id": "b", "base_url": "https://example.invalid/b"},
    ]})
    endpoints = load_endpoints(raw, selector="b,a")
    assert [endpoint.kiwis_id for endpoint in endpoints] == ["b", "a"]


def test_selector_star_includes_disabled_template(monkeypatch):
    monkeypatch.delenv("KIWIS_ENDPOINTS", raising=False)
    endpoints = load_endpoints(selector="*")
    assert len(endpoints) == 4
    assert any(endpoint.kiwis_id == "replace-me" for endpoint in endpoints)
    assert any(endpoint.base_url == "https://www.bom.gov.au/waterdata/services" for endpoint in endpoints)


def test_unknown_selector_raises():
    with pytest.raises(ValueError):
        load_endpoints(selector="does-not-exist")


def test_legacy_inline_kiwis_endpoints_takes_precedence(monkeypatch, tmp_path):
    catalog = tmp_path / "kiwis-sources.json"
    catalog.write_text(json.dumps({"sources": [{"name": "catalog", "kiwis_id": "catalog", "base_url": "https://example.invalid/catalog"}]}), encoding="utf-8")
    monkeypatch.setenv("KIWIS_ENDPOINTS", '[{"kiwis_id":"inline","base_url":"https://example.invalid/inline"}]')
    monkeypatch.setenv("KIWIS_SOURCES_FILE", str(catalog))
    endpoints = load_endpoints()
    assert len(endpoints) == 1
    assert endpoints[0].kiwis_id == "inline"


def test_env_interpolation_on_api_key(monkeypatch):
    monkeypatch.setenv("SOME_KIWIS_KEY", "secret-123")
    raw = json.dumps({"sources": [{"name": "keyed", "kiwis_id": "keyed", "base_url": "https://example.invalid/KiWIS", "api_key": "${SOME_KIWIS_KEY}"}]})
    endpoints = load_endpoints(raw)
    assert endpoints[0].api_key == "secret-123"


def test_sources_file_override_via_env(monkeypatch, tmp_path):
    catalog = tmp_path / "custom.sources.json"
    catalog.write_text(json.dumps({"sources": [{"name": "only", "kiwis_id": "only", "base_url": "https://example.invalid/only"}]}), encoding="utf-8")
    monkeypatch.delenv("KIWIS_ENDPOINTS", raising=False)
    monkeypatch.setenv("KIWIS_SOURCES_FILE", str(catalog))
    endpoints = load_endpoints()
    assert len(endpoints) == 1
    assert endpoints[0].kiwis_id == "only"


def test_catalog_metadata_is_stripped_before_endpoint_construction():
    endpoints = load_endpoints(json.dumps({"sources": [{
        "name": "meta",
        "enabled": True,
        "description": "Metadata keys must not be passed to KiWISEndpoint.",
        "kiwis_id": "meta",
        "base_url": "https://example.invalid/meta"
    }]}))
    assert endpoints[0].kiwis_id == "meta"


def test_select_entries_default_skips_disabled():
    entries = [{"name": "a", "enabled": True}, {"name": "b", "enabled": False}]
    assert [entry["name"] for entry in select_entries(entries)] == ["a"]
