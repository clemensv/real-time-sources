"""Unit tests for Ireland OPW waterlevel.ie bridge — no external dependencies."""

import json
import os
import pytest
from ireland_opw_waterlevel.ireland_opw_waterlevel import (
    parse_value,
    extract_stations,
    extract_readings,
    dedup_key,
    parse_connection_string,
    _load_state,
    _save_state,
    FEED_URL,
)


# ---------------------------------------------------------------------------
# Sample GeoJSON features used across tests
# ---------------------------------------------------------------------------

SAMPLE_FEATURES = [
    {
        "type": "Feature",
        "id": 1458,
        "properties": {
            "station_ref": "0000001041",
            "station_name": "Sandy Mills",
            "sensor_ref": "0001",
            "region_id": 3,
            "datetime": "2024-01-15T12:00:00Z",
            "value": "0.368",
            "err_code": 99,
            "url": "/0000001041/0001/",
            "csv_file": "/data/month/01041_0001.csv"
        },
        "geometry": {"type": "Point", "coordinates": [-7.575758, 54.838318]}
    },
    {
        "type": "Feature",
        "id": 896,
        "properties": {
            "station_ref": "0000001041",
            "station_name": "Sandy Mills",
            "sensor_ref": "0002",
            "region_id": 3,
            "datetime": "2024-01-15T12:00:00Z",
            "value": "10.300",
            "err_code": 99,
            "url": "/0000001041/0002/",
            "csv_file": "/data/month/01041_0002.csv"
        },
        "geometry": {"type": "Point", "coordinates": [-7.575758, 54.838318]}
    },
    {
        "type": "Feature",
        "id": 1082,
        "properties": {
            "station_ref": "0000001041",
            "station_name": "Sandy Mills",
            "sensor_ref": "0003",
            "region_id": 3,
            "datetime": "2024-01-15T12:00:00Z",
            "value": "12.900",
            "err_code": 99,
            "url": "/0000001041/0003/",
            "csv_file": "/data/month/01041_0003.csv"
        },
        "geometry": {"type": "Point", "coordinates": [-7.575758, 54.838318]}
    },
    {
        "type": "Feature",
        "id": 1051,
        "properties": {
            "station_ref": "0000001041",
            "station_name": "Sandy Mills",
            "sensor_ref": "OD",
            "region_id": 3,
            "datetime": "2024-01-15T12:00:00Z",
            "value": "4.023",
            "err_code": 99,
            "url": "/0000001041/OD/",
            "csv_file": "/data/month/01041_OD.csv"
        },
        "geometry": {"type": "Point", "coordinates": [-7.575758, 54.838318]}
    },
    {
        "type": "Feature",
        "id": 1460,
        "properties": {
            "station_ref": "0000001043",
            "station_name": "Ballybofey",
            "sensor_ref": "0001",
            "region_id": 3,
            "datetime": "2024-01-15T12:00:00Z",
            "value": "0.736",
            "err_code": 99,
            "url": "/0000001043/0001/",
            "csv_file": "/data/month/01043_0001.csv"
        },
        "geometry": {"type": "Point", "coordinates": [-7.790749, 54.799769]}
    },
]


# ===========================================================================
# parse_value tests
# ===========================================================================

@pytest.mark.unit
class TestParseValue:
    """Test string → float parsing."""

    def test_valid_float(self):
        assert parse_value("0.368") == pytest.approx(0.368)

    def test_valid_negative(self):
        assert parse_value("-1.5") == pytest.approx(-1.5)

    def test_valid_integer_string(self):
        assert parse_value("42") == pytest.approx(42.0)

    def test_none_returns_none(self):
        assert parse_value(None) is None

    def test_empty_string_returns_none(self):
        assert parse_value("") is None

    def test_non_numeric_returns_none(self):
        assert parse_value("abc") is None

    def test_whitespace_string(self):
        assert parse_value("  ") is None

    def test_zero(self):
        assert parse_value("0") == pytest.approx(0.0)

    def test_large_value(self):
        assert parse_value("99999.99") == pytest.approx(99999.99)


# ===========================================================================
# extract_stations tests
# ===========================================================================

@pytest.mark.unit
class TestExtractStations:
    """Test station extraction from GeoJSON features."""

    def test_extracts_unique_stations(self):
        stations = extract_stations(SAMPLE_FEATURES)
        assert len(stations) == 2
        assert "0000001041" in stations
        assert "0000001043" in stations

    def test_station_name(self):
        stations = extract_stations(SAMPLE_FEATURES)
        assert stations["0000001041"]["station_name"] == "Sandy Mills"
        assert stations["0000001043"]["station_name"] == "Ballybofey"

    def test_station_region_id(self):
        stations = extract_stations(SAMPLE_FEATURES)
        assert stations["0000001041"]["region_id"] == 3

    def test_station_coordinates(self):
        stations = extract_stations(SAMPLE_FEATURES)
        s = stations["0000001041"]
        assert s["longitude"] == pytest.approx(-7.575758)
        assert s["latitude"] == pytest.approx(54.838318)

    def test_empty_features_returns_empty(self):
        assert extract_stations([]) == {}

    def test_missing_station_ref_skipped(self):
        features = [{"properties": {"station_name": "Test"}, "geometry": {"coordinates": [0, 0]}}]
        assert extract_stations(features) == {}

    def test_dedup_keeps_first_occurrence(self):
        stations = extract_stations(SAMPLE_FEATURES)
        # station 1041 appears 4 times, only one entry expected
        assert stations["0000001041"]["station_name"] == "Sandy Mills"

    def test_missing_geometry_defaults_to_zero(self):
        features = [{
            "properties": {"station_ref": "0000099999", "station_name": "NoGeo", "region_id": 1},
            "geometry": {"coordinates": []}
        }]
        stations = extract_stations(features)
        assert stations["0000099999"]["longitude"] == 0.0
        assert stations["0000099999"]["latitude"] == 0.0


# ===========================================================================
# extract_readings tests
# ===========================================================================

@pytest.mark.unit
class TestExtractReadings:
    """Test reading extraction from GeoJSON features."""

    def test_returns_all_features_as_readings(self):
        readings = extract_readings(SAMPLE_FEATURES)
        assert len(readings) == 5

    def test_reading_has_required_fields(self):
        readings = extract_readings(SAMPLE_FEATURES)
        r = readings[0]
        assert r["station_ref"] == "0000001041"
        assert r["station_name"] == "Sandy Mills"
        assert r["sensor_ref"] == "0001"
        assert r["value"] == pytest.approx(0.368)
        assert r["datetime"] == "2024-01-15T12:00:00Z"
        assert r["err_code"] == 99

    def test_different_sensor_refs(self):
        readings = extract_readings(SAMPLE_FEATURES)
        sensor_refs = [r["sensor_ref"] for r in readings if r["station_ref"] == "0000001041"]
        assert set(sensor_refs) == {"0001", "0002", "0003", "OD"}

    def test_empty_features_returns_empty(self):
        assert extract_readings([]) == []

    def test_value_parsed_as_float(self):
        readings = extract_readings(SAMPLE_FEATURES)
        assert isinstance(readings[0]["value"], float)

    def test_err_code_parsed_as_int(self):
        readings = extract_readings(SAMPLE_FEATURES)
        assert isinstance(readings[0]["err_code"], int)


# ===========================================================================
# dedup_key tests
# ===========================================================================

@pytest.mark.unit
class TestDedupKey:
    """Test dedup key generation."""

    def test_basic_key(self):
        reading = {"station_ref": "0000001041", "sensor_ref": "0001", "datetime": "2024-01-15T12:00:00Z"}
        assert dedup_key(reading) == "0000001041|0001|2024-01-15T12:00:00Z"

    def test_different_sensor_refs_produce_different_keys(self):
        r1 = {"station_ref": "0000001041", "sensor_ref": "0001", "datetime": "2024-01-15T12:00:00Z"}
        r2 = {"station_ref": "0000001041", "sensor_ref": "0002", "datetime": "2024-01-15T12:00:00Z"}
        assert dedup_key(r1) != dedup_key(r2)

    def test_different_datetimes_produce_different_keys(self):
        r1 = {"station_ref": "0000001041", "sensor_ref": "0001", "datetime": "2024-01-15T12:00:00Z"}
        r2 = {"station_ref": "0000001041", "sensor_ref": "0001", "datetime": "2024-01-15T12:15:00Z"}
        assert dedup_key(r1) != dedup_key(r2)

    def test_same_inputs_produce_same_key(self):
        r = {"station_ref": "0000001041", "sensor_ref": "0001", "datetime": "2024-01-15T12:00:00Z"}
        assert dedup_key(r) == dedup_key(r)


# ===========================================================================
# parse_connection_string tests
# ===========================================================================

@pytest.mark.unit
class TestParseConnectionString:
    """Test connection string parsing."""

    def test_event_hubs_connection_string(self):
        cs = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123==;"
            "EntityPath=myeventhub"
        )
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'myeventhub'
        assert result['sasl.username'] == '$ConnectionString'
        assert cs.strip() in result['sasl.password']

    def test_bootstrap_server_format(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'test-topic'
        assert 'sasl.username' not in result

    def test_endpoint_extracts_server(self):
        cs = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic1"
        result = parse_connection_string(cs)
        assert 'test.servicebus.windows.net:9093' == result['bootstrap.servers']
        assert 'sb://' not in result['bootstrap.servers']

    def test_sets_sasl_credentials(self):
        cs = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=MyPolicy;SharedAccessKey=abc123;EntityPath=topic"
        result = parse_connection_string(cs)
        assert result['sasl.username'] == '$ConnectionString'
        assert result['security.protocol'] == 'SASL_SSL'
        assert result['sasl.mechanism'] == 'PLAIN'

    def test_without_sasl_no_security(self):
        cs = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic"
        result = parse_connection_string(cs)
        assert 'sasl.username' not in result
        assert 'security.protocol' not in result

    def test_invalid_format_raises_error(self):
        with pytest.raises(ValueError, match="Invalid connection string format"):
            parse_connection_string("EndpointWithoutEquals;EntityPathAlsoInvalid")


# ===========================================================================
# State persistence tests
# ===========================================================================

@pytest.mark.unit
class TestStatePersistence:
    """Test state load/save."""

    def test_load_nonexistent_returns_empty(self):
        assert _load_state("/nonexistent/path/state.json") == {}

    def test_load_empty_path_returns_empty(self):
        assert _load_state("") == {}

    def test_save_and_load_roundtrip(self, tmp_path):
        state_file = str(tmp_path / "state.json")
        data = {"seen_keys": ["a|b|c", "d|e|f"]}
        _save_state(state_file, data)
        loaded = _load_state(state_file)
        assert loaded == data

    def test_save_empty_path_does_nothing(self):
        _save_state("", {"key": "value"})  # Should not raise

    def test_load_invalid_json_returns_empty(self, tmp_path):
        state_file = str(tmp_path / "bad.json")
        with open(state_file, 'w') as f:
            f.write("not json")
        assert _load_state(state_file) == {}


# ===========================================================================
# Constants and API URL tests
# ===========================================================================

@pytest.mark.unit
class TestConstants:
    """Test module constants."""

    def test_feed_url_is_https(self):
        assert FEED_URL.startswith("https://")

    def test_feed_url_points_to_waterlevel_ie(self):
        assert "waterlevel.ie" in FEED_URL

    def test_feed_url_ends_with_latest(self):
        assert FEED_URL.endswith("/latest/")


# ===========================================================================
# Module import tests
# ===========================================================================

@pytest.mark.unit
class TestModuleStructure:
    """Verify module exports."""

    def test_main_is_importable(self):
        from ireland_opw_waterlevel import main
        assert callable(main)

    def test_bridge_has_feed_function(self):
        from ireland_opw_waterlevel.ireland_opw_waterlevel import feed
        assert callable(feed)

    def test_bridge_has_fetch_geojson(self):
        from ireland_opw_waterlevel.ireland_opw_waterlevel import fetch_geojson
        assert callable(fetch_geojson)

    def test_bridge_has_emit_stations(self):
        from ireland_opw_waterlevel.ireland_opw_waterlevel import emit_stations
        assert callable(emit_stations)

    def test_bridge_has_emit_readings(self):
        from ireland_opw_waterlevel.ireland_opw_waterlevel import emit_readings
        assert callable(emit_readings)
