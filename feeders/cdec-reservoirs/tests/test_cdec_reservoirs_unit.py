"""Unit tests for CDEC Reservoirs bridge - no external dependencies."""

import pytest
from cdec_reservoirs.cdec_reservoirs import (
    CdecReservoirsAPI,
    parse_cdec_timestamp,
    normalize_value,
    _load_state,
    _save_state,
    BASE_URL,
    DEFAULT_STATIONS,
    DEFAULT_SENSORS,
    SENTINEL_VALUE,
    PST,
)


@pytest.mark.unit
class TestParseCdecTimestamp:
    """Test CDEC timestamp parsing to ISO 8601 with PST offset."""

    def test_standard_timestamp(self):
        result = parse_cdec_timestamp("2026-4-1 0:00")
        assert result == "2026-04-01T00:00:00-08:00"

    def test_two_digit_month_day(self):
        result = parse_cdec_timestamp("2026-12-15 14:00")
        assert result == "2026-12-15T14:00:00-08:00"

    def test_single_digit_hour(self):
        result = parse_cdec_timestamp("2026-1-5 9:00")
        assert result == "2026-01-05T09:00:00-08:00"

    def test_midnight(self):
        result = parse_cdec_timestamp("2026-6-15 0:00")
        assert result == "2026-06-15T00:00:00-08:00"

    def test_end_of_day(self):
        result = parse_cdec_timestamp("2026-3-31 23:00")
        assert result == "2026-03-31T23:00:00-08:00"

    def test_whitespace_handling(self):
        result = parse_cdec_timestamp("  2026-4-1 0:00  ")
        assert result == "2026-04-01T00:00:00-08:00"

    def test_invalid_timestamp_raises_error(self):
        with pytest.raises(ValueError, match="Cannot parse CDEC timestamp"):
            parse_cdec_timestamp("not-a-timestamp")

    def test_empty_string_raises_error(self):
        with pytest.raises(ValueError, match="Cannot parse CDEC timestamp"):
            parse_cdec_timestamp("")

    def test_pst_offset_is_always_minus_8(self):
        """CDEC always reports PST, never PDT."""
        # Even a summer date should have -08:00
        result = parse_cdec_timestamp("2026-7-15 12:00")
        assert "-08:00" in result

    def test_february_leap_year(self):
        result = parse_cdec_timestamp("2024-2-29 6:00")
        assert result == "2024-02-29T06:00:00-08:00"


@pytest.mark.unit
class TestNormalizeValue:
    """Test value normalization including sentinel handling."""

    def test_normal_integer_value(self):
        assert normalize_value(4090763) == 4090763.0

    def test_normal_float_value(self):
        assert normalize_value(1052.15) == 1052.15

    def test_zero_value(self):
        assert normalize_value(0) == 0.0

    def test_negative_value(self):
        assert normalize_value(-100.5) == -100.5

    def test_sentinel_minus_9999_returns_none(self):
        assert normalize_value(-9999) is None

    def test_sentinel_float_minus_9999(self):
        assert normalize_value(-9999.0) is None

    def test_none_returns_none(self):
        assert normalize_value(None) is None

    def test_string_number(self):
        assert normalize_value("123.45") == 123.45

    def test_non_numeric_string_returns_none(self):
        assert normalize_value("abc") is None

    def test_empty_string_returns_none(self):
        assert normalize_value("") is None

    def test_large_value(self):
        assert normalize_value(10000000) == 10000000.0


@pytest.mark.unit
class TestCdecReservoirsAPIInitialization:
    """Test CdecReservoirsAPI class initialization."""

    def test_default_stations(self):
        api = CdecReservoirsAPI()
        assert api.stations == DEFAULT_STATIONS

    def test_default_sensors(self):
        api = CdecReservoirsAPI()
        assert api.sensors == DEFAULT_SENSORS

    def test_default_dur_code(self):
        api = CdecReservoirsAPI()
        assert api.dur_code == "H"

    def test_custom_stations(self):
        api = CdecReservoirsAPI(stations="SHA,ORO")
        assert api.stations == "SHA,ORO"

    def test_custom_sensors(self):
        api = CdecReservoirsAPI(sensors="15,6")
        assert api.sensors == "15,6"

    def test_custom_dur_code(self):
        api = CdecReservoirsAPI(dur_code="D")
        assert api.dur_code == "D"

    def test_session_created(self):
        api = CdecReservoirsAPI()
        assert api.session is not None
        assert hasattr(api.session, 'get')


@pytest.mark.unit
class TestBuildUrl:
    """Test URL construction for the CDEC JSON Data Servlet."""

    def test_default_url(self):
        api = CdecReservoirsAPI()
        url = api.build_url("2026-04-01", "2026-04-02")
        assert BASE_URL in url
        assert "Stations=SHA,ORO,FOL,NML,DNP,HTC,SON,MIL,PNF" in url
        assert "SensorNums=15,6,76,23" in url
        assert "dur_code=H" in url
        assert "Start=2026-04-01" in url
        assert "End=2026-04-02" in url

    def test_custom_stations_url(self):
        api = CdecReservoirsAPI(stations="SHA,ORO")
        url = api.build_url("2026-04-01", "2026-04-02")
        assert "Stations=SHA,ORO" in url

    def test_custom_sensors_url(self):
        api = CdecReservoirsAPI(sensors="15")
        url = api.build_url("2026-04-01", "2026-04-02")
        assert "SensorNums=15" in url

    def test_daily_dur_code_url(self):
        api = CdecReservoirsAPI(dur_code="D")
        url = api.build_url("2026-04-01", "2026-04-02")
        assert "dur_code=D" in url


@pytest.mark.unit
class TestConnectionStringParsing:
    """Test connection string parsing for Event Hubs/Kafka."""

    def test_parse_event_hubs_connection_string(self):
        api = CdecReservoirsAPI()
        conn_str = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123==;"
            "EntityPath=myeventhub"
        )
        result = api.parse_connection_string(conn_str)
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'myeventhub'
        assert result['sasl.username'] == '$ConnectionString'
        assert conn_str.strip() in result['sasl.password']

    def test_parse_plain_bootstrap_connection_string(self):
        api = CdecReservoirsAPI()
        conn_str = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = api.parse_connection_string(conn_str)
        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'test-topic'
        assert 'sasl.username' not in result

    def test_parse_connection_string_extracts_endpoint(self):
        api = CdecReservoirsAPI()
        conn_str = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic1"
        result = api.parse_connection_string(conn_str)
        assert 'test.servicebus.windows.net:9093' == result['bootstrap.servers']

    def test_parse_connection_string_sets_sasl_protocol(self):
        api = CdecReservoirsAPI()
        conn_str = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=MyPolicy;SharedAccessKey=abc;EntityPath=t"
        result = api.parse_connection_string(conn_str)
        assert result['security.protocol'] == 'SASL_SSL'
        assert result['sasl.mechanism'] == 'PLAIN'

    def test_parse_connection_string_without_sasl(self):
        api = CdecReservoirsAPI()
        conn_str = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic"
        result = api.parse_connection_string(conn_str)
        assert 'sasl.username' not in result
        assert 'security.protocol' not in result

    def test_parse_invalid_connection_string_raises(self):
        api = CdecReservoirsAPI()
        with pytest.raises(ValueError, match="Invalid connection string format"):
            api.parse_connection_string("EndpointWithoutEquals;EntityPathAlsoInvalid")


@pytest.mark.unit
class TestConstants:
    """Test constants and configuration."""

    def test_base_url_uses_https(self):
        assert BASE_URL.startswith("https://")

    def test_base_url_points_to_cdec(self):
        assert "cdec.water.ca.gov" in BASE_URL

    def test_sentinel_value_is_minus_9999(self):
        assert SENTINEL_VALUE == -9999

    def test_pst_offset_is_minus_8_hours(self):
        from datetime import timedelta
        assert PST.utcoffset(None) == timedelta(hours=-8)

    def test_default_stations_includes_major_reservoirs(self):
        for station in ["SHA", "ORO", "FOL"]:
            assert station in DEFAULT_STATIONS

    def test_default_sensors_includes_standard_types(self):
        for sensor in ["15", "6", "76", "23"]:
            assert sensor in DEFAULT_SENSORS


@pytest.mark.unit
class TestAPIRequiredMethods:
    """Test that the API class has required public methods."""

    def test_has_build_url(self):
        api = CdecReservoirsAPI()
        assert hasattr(api, 'build_url')

    def test_has_fetch_readings(self):
        api = CdecReservoirsAPI()
        assert hasattr(api, 'fetch_readings')

    def test_has_parse_connection_string(self):
        api = CdecReservoirsAPI()
        assert hasattr(api, 'parse_connection_string')

    def test_has_feed_readings(self):
        api = CdecReservoirsAPI()
        assert hasattr(api, 'feed_readings')


@pytest.mark.unit
class TestStateManagement:
    """Test state persistence helpers."""

    def test_load_state_missing_file_returns_empty_set(self):
        result = _load_state("/nonexistent/file.json")
        assert result == set()

    def test_load_state_empty_string_returns_empty_set(self):
        result = _load_state("")
        assert result == set()

    def test_save_state_empty_string_does_nothing(self):
        # Should not raise
        _save_state("", {"key1", "key2"})

    def test_save_and_load_roundtrip(self, tmp_path):
        state_file = str(tmp_path / "state.json")
        keys = {"SHA/15/2026-4-1 0:00", "ORO/6/2026-4-1 1:00"}
        _save_state(state_file, keys)
        loaded = _load_state(state_file)
        assert loaded == keys
