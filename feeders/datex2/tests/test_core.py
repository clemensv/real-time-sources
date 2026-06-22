import json

import pytest

from datex2_core import load_endpoints, mock_batch, select_entries


def test_mock_batch_covers_reference_telemetry_and_situation():
    batch = mock_batch()
    assert batch.measurement_sites and batch.traffic_measurements and batch.situation_records
    assert batch.measurement_sites[0]["supplier_id"] == "sample"


def test_default_catalog_loads_enabled_ndw_endpoints():
    endpoints = load_endpoints()
    assert len(endpoints) == 4
    assert all(endpoint.country == "nl" for endpoint in endpoints)
    assert all(endpoint.id == "ndw" for endpoint in endpoints)


def test_selector_returns_named_entries_in_order():
    endpoints = load_endpoints(selector="ndw-roadworks,ndw-trafficspeed")
    assert [endpoint.publication for endpoint in endpoints] == ["SituationPublication", "MeasuredDataPublication"]


def test_selector_star_includes_disabled_templates():
    endpoints = load_endpoints(selector="*")
    assert len(endpoints) == 8
    assert any(endpoint.id == "trafikverket" for endpoint in endpoints)
    assert any(endpoint.operator == "cita" for endpoint in endpoints)


def test_unknown_selector_raises():
    with pytest.raises(ValueError):
        load_endpoints(selector="does-not-exist")


def test_inline_catalog_object_with_secret_interpolation(monkeypatch):
    monkeypatch.setenv("TRAFIKVERKET_KEY", "secret-123")
    raw = json.dumps({"sources": [{"name": "se", "id": "trafikverket", "url": "https://example.invalid/feed.xml", "auth_header": "Bearer ${TRAFIKVERKET_KEY}"}]})
    endpoints = load_endpoints(raw)
    assert endpoints[0].auth_header == "Bearer secret-123"


def test_sources_file_override(tmp_path):
    catalog = tmp_path / "custom.sources.json"
    catalog.write_text(json.dumps({"sources": [{"name": "only", "id": "x", "url": "https://example.invalid/only.xml"}]}), encoding="utf-8")
    endpoints = load_endpoints(sources_file=str(catalog))
    assert len(endpoints) == 1 and endpoints[0].id == "x"


def test_endpoint_loader_accepts_registry_json():
    endpoints = load_endpoints('[{"id":"ndw","url":"https://example.invalid/feed.xml.gz","publication":"MeasuredDataPublication","country":"nl","operator":"ndw"}]')
    assert endpoints[0].id == "ndw"
    assert endpoints[0].country == "nl"


def test_select_entries_default_skips_disabled():
    entries = [{"name": "a", "enabled": True}, {"name": "b", "enabled": False}]
    assert [entry["name"] for entry in select_entries(entries)] == ["a"]


