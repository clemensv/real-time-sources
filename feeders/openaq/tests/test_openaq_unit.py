import json

import pytest

from openaq_core import load_query_slices, build_mock_client, select_entries, should_publish_measurement
from openaq.app import build_location, build_measurement, build_sensor


def test_mock_cycle_builds_all_payloads():
    client = build_mock_client()
    location = next(client.iter_locations([], [], None))
    sensors = {s.sensor_id: s for s in client.sensors_for_location(location)}
    measurements = client.latest_for_location(location, sensors)
    assert build_location(location).location_id == 1001
    assert build_sensor(next(iter(sensors.values()))).sensor_id == 2001
    assert build_measurement(measurements[0]).value == 11.2


def test_measurement_dedupe_state():
    client = build_mock_client()
    location = next(client.iter_locations([], [], None))
    sensors = {s.sensor_id: s for s in client.sensors_for_location(location)}
    measurement = client.latest_for_location(location, sensors)[0]
    state = {}
    assert should_publish_measurement(measurement, state) is True
    assert should_publish_measurement(measurement, state) is False


def test_default_catalog_loads_enabled_us_slice():
    slices = load_query_slices()
    assert len(slices) == 1
    assert slices[0].countries == ["US"]
    assert slices[0].locations == []
    assert slices[0].bbox is None


def test_catalog_enabled_flag_honored():
    slices = load_query_slices(selector="")
    assert [slice_.countries for slice_ in slices] == [["US"]]


def test_selector_returns_named_slices_in_order():
    slices = load_query_slices(selector="india,us-all")
    assert [slice_.countries for slice_ in slices] == [["IN"], ["US"]]


def test_selector_star_includes_disabled_slices():
    slices = load_query_slices(selector="*")
    assert len(slices) == 8
    assert any(slice_.bbox == "-10.50,41.00,15.50,56.50" for slice_ in slices)
    assert any(slice_.countries == ["BH"] for slice_ in slices)


def test_unknown_selector_raises():
    with pytest.raises(ValueError):
        load_query_slices(selector="does-not-exist")


def test_legacy_countries_single_query_path_and_precedence(tmp_path):
    catalog = tmp_path / "custom.sources.json"
    catalog.write_text(json.dumps({"sources": [{"name": "custom", "countries": "CA"}]}), encoding="utf-8")
    slices = load_query_slices(openaq_countries="BE,NL", sources_file=str(catalog))
    assert len(slices) == 1
    assert slices[0].countries == ["BE", "NL"]


def test_legacy_bbox_single_query_path():
    slices = load_query_slices(openaq_bbox="-125,24,-66,50")
    assert len(slices) == 1
    assert slices[0].countries == ["US"]
    assert slices[0].bbox == "-125,24,-66,50"


def test_sources_file_override_via_tmp_path(tmp_path):
    catalog = tmp_path / "custom.sources.json"
    catalog.write_text(json.dumps({"sources": [{"name": "only", "enabled": True, "countries": "CA", "page_limit": 10, "max_pages": 3}]}), encoding="utf-8")
    slices = load_query_slices(sources_file=str(catalog))
    assert len(slices) == 1
    assert slices[0].countries == ["CA"]
    assert slices[0].page_limit == 10
    assert slices[0].max_pages == 3


def test_catalog_env_interpolation_and_locations(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENAQ_TEST_LOCATIONS", "1001,2002")
    catalog = tmp_path / "custom.sources.json"
    catalog.write_text(json.dumps({"sources": [{"name": "env", "locations": "${OPENAQ_TEST_LOCATIONS}"}]}), encoding="utf-8")
    slices = load_query_slices(sources_file=str(catalog))
    assert slices[0].locations == [1001, 2002]


def test_metadata_fields_are_stripped_from_slice_object(tmp_path):
    catalog = tmp_path / "custom.sources.json"
    catalog.write_text(json.dumps({"sources": [{"name": "only", "enabled": True, "description": "test", "countries": "MX"}]}), encoding="utf-8")
    slice_ = load_query_slices(sources_file=str(catalog))[0]
    assert not hasattr(slice_, "name")
    assert not hasattr(slice_, "enabled")
    assert not hasattr(slice_, "description")


def test_select_entries_default_skips_disabled():
    entries = [{"name": "a", "enabled": True}, {"name": "b", "enabled": False}]
    assert [entry["name"] for entry in select_entries(entries)] == ["a"]
