import json

import pytest

from cap_alerts_core import load_sources, mock_client_and_sources, parse_cap_xml, select_entries


def test_mock_cap_xml_preserves_multi_info_and_extensions():
    client, sources = mock_client_and_sources()
    alerts = client.fetch_alerts(sources[0])
    assert len(alerts) == 1
    alert = alerts[0]
    assert alert["cap_source_id"] == "mock-cap"
    assert alert["identifier"] == "mock-20260620-001"
    assert len(alert["info"]) == 2
    assert alert["ugc_codes"] == ["CAZ001"]
    assert alert["same_codes"] == ["006001"]
    assert alert["vtec"] == ["/O.NEW.KMTR.FL.W.0001.260620T1800Z-260621T0000Z/"]
    assert alert["awareness_level"] == "3; orange; Severe"


def test_mock_zones_reference():
    client, sources = mock_client_and_sources()
    zones = client.fetch_zones(sources[0])
    assert zones[0]["zone_id"] == "CAZ001"
    assert zones[0]["cap_source_id"] == "mock-cap"

def test_default_catalog_loads_enabled_cap_sources(monkeypatch):
    monkeypatch.delenv("CAP_SOURCES", raising=False)
    monkeypatch.delenv("CAP_SOURCES_FILE", raising=False)
    monkeypatch.delenv("CAP_SELECT", raising=False)
    sources = load_sources()
    assert [source.cap_source_id for source in sources] == ["nws-us", "meteoalarm-belgium"]
    assert sources[0].zone_url == "https://api.weather.gov/zones?limit=25"


def test_cap_select_returns_named_sources_in_order(monkeypatch):
    monkeypatch.delenv("CAP_SOURCES", raising=False)
    sources = load_sources(selector="meteoalarm-belgium,nws-us-active-alerts")
    assert [source.cap_source_id for source in sources] == ["meteoalarm-belgium", "nws-us"]


def test_cap_select_star_includes_disabled_template(monkeypatch):
    monkeypatch.delenv("CAP_SOURCES", raising=False)
    sources = load_sources(selector="*")
    assert len(sources) == 13
    assert any(source.cap_source_id == "replace-me-national-cap" for source in sources)
    assert any(source.cap_source_id == "meteoalarm-ireland" for source in sources)


def test_unknown_cap_select_raises(monkeypatch):
    monkeypatch.delenv("CAP_SOURCES", raising=False)
    with pytest.raises(ValueError):
        load_sources(selector="does-not-exist")


def test_legacy_cap_sources_inline_still_works_and_takes_precedence(tmp_path, monkeypatch):
    catalog = tmp_path / "custom.sources.json"
    catalog.write_text(json.dumps({"sources": [{"name": "file", "cap_source_id": "file-source", "url": "https://example.invalid/file.xml"}]}), encoding="utf-8")
    monkeypatch.setenv("CAP_SOURCES", json.dumps([{"cap_source_id": "legacy-source", "url": "https://example.invalid/legacy.xml", "format": "cap-xml"}]))
    sources = load_sources(sources_file=str(catalog))
    assert [source.cap_source_id for source in sources] == ["legacy-source"]


def test_cap_sources_file_override_and_env_interpolation(tmp_path, monkeypatch):
    catalog = tmp_path / "custom.sources.json"
    catalog.write_text(json.dumps({"sources": [{"name": "secure", "cap_source_id": "secure-source", "url": "https://example.invalid/secure.xml", "auth_header": "Bearer ${CAP_TEST_TOKEN}"}]}), encoding="utf-8")
    monkeypatch.delenv("CAP_SOURCES", raising=False)
    monkeypatch.setenv("CAP_SOURCES_FILE", str(catalog))
    monkeypatch.setenv("CAP_TEST_TOKEN", "secret-123")
    sources = load_sources()
    assert len(sources) == 1
    assert sources[0].cap_source_id == "secure-source"
    assert sources[0].auth_header == "Bearer secret-123"


def test_select_entries_default_skips_disabled():
    entries = [{"name": "a", "enabled": True}, {"name": "b", "enabled": False}]
    assert [entry["name"] for entry in select_entries(entries)] == ["a"]


def test_capsource_rejects_unknown_format():
    """An unknown format must fail loudly at construction, not silently parse as CAP-XML."""
    from cap_alerts_core.acquisition import CapSource

    with pytest.raises(ValueError, match="unsupported format"):
        CapSource(cap_source_id="bad", url="https://example.invalid/x", format="not-a-format")
    ok = CapSource(cap_source_id="ok", url="https://example.invalid/x", format="atom-cap")
    assert ok.format == "atom-cap"
