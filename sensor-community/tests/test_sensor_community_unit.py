"""Unit tests for the Sensor.Community bridge."""

import pytest

from sensor_community.sensor_community import DEFAULT_SENSOR_TYPES, SensorCommunityAPI


@pytest.mark.unit
class TestSensorCommunityAPIInitialization:
    """Test SensorCommunityAPI initialization behavior."""

    def test_init_creates_session(self):
        api = SensorCommunityAPI(state_file="")
        assert api.session is not None
        assert hasattr(api.session, "get")

    def test_init_uses_default_sensor_types(self):
        api = SensorCommunityAPI(state_file="")
        assert api.sensor_types == DEFAULT_SENSOR_TYPES.split(",")

    def test_init_normalizes_country_filter(self):
        api = SensorCommunityAPI(countries="de,nl", state_file="")
        assert api.countries == {"DE", "NL"}


@pytest.mark.unit
class TestConnectionStringParsing:
    """Test connection string parsing for Event Hubs and plain Kafka."""

    def test_parse_event_hubs_connection_string(self):
        api = SensorCommunityAPI(state_file="")
        connection_string = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123==;"
            "EntityPath=myeventhub"
        )
        result = api.parse_connection_string(connection_string)

        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "myeventhub"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["sasl.password"] == connection_string
        assert result["security.protocol"] == "SASL_SSL"
        assert result["sasl.mechanism"] == "PLAIN"

    def test_parse_plain_kafka_connection_string(self):
        api = SensorCommunityAPI(state_file="")
        result = api.parse_connection_string("BootstrapServer=broker1:9092;EntityPath=sensor-community")
        assert result["bootstrap.servers"] == "broker1:9092"
        assert result["kafka_topic"] == "sensor-community"
        assert "sasl.username" not in result

    def test_parse_invalid_connection_string_raises(self):
        api = SensorCommunityAPI(state_file="")
        with pytest.raises(ValueError, match="Invalid connection string format"):
            api.parse_connection_string("EndpointWithoutEquals;EntityPath=test")


@pytest.mark.unit
class TestSensorTypeFiltering:
    """Test configured type and country filters."""

    def test_normalize_sensor_types_deduplicates_and_uppercases(self):
        result = SensorCommunityAPI.normalize_sensor_types("SDS011, bme280, SDS011, sps30")
        assert result == ["SDS011", "BME280", "SPS30"]

    def test_should_include_record_without_country_filter(self):
        api = SensorCommunityAPI(countries="", state_file="")
        record = {"location": {"country": "DE"}}
        assert api.should_include_record(record) is True

    def test_should_include_record_with_country_filter(self):
        api = SensorCommunityAPI(countries="DE,NL", state_file="")
        assert api.should_include_record({"location": {"country": "DE"}}) is True
        assert api.should_include_record({"location": {"country": "BG"}}) is False


@pytest.mark.unit
class TestMeasurementExtraction:
    """Test measurement extraction from sensordatavalues."""

    def test_extract_measurements_maps_known_value_types(self):
        values = [
            {"value_type": "P1", "value": "5.00"},
            {"value_type": "P2", "value": "3.33"},
            {"value_type": "temperature", "value": "17.5"},
            {"value_type": "humidity", "value": "61.2"},
            {"value_type": "pressure", "value": "101325.0"},
            {"value_type": "pressure_at_sealevel", "value": "101665.0"},
            {"value_type": "P0", "value": "1.11"},
            {"value_type": "P4", "value": "4.44"},
            {"value_type": "noise_LAeq", "value": "49.9"},
            {"value_type": "noise_LA_min", "value": "42.0"},
            {"value_type": "noise_LA_max", "value": "60.1"},
        ]

        result = SensorCommunityAPI.extract_measurements(values)

        assert result["pm10_ug_m3"] == 5.0
        assert result["pm2_5_ug_m3"] == 3.33
        assert result["temperature_celsius"] == 17.5
        assert result["humidity_percent"] == 61.2
        assert result["pressure_pa"] == 101325.0
        assert result["pressure_sealevel_pa"] == 101665.0
        assert result["pm1_0_ug_m3"] == 1.11
        assert result["pm4_0_ug_m3"] == 4.44
        assert result["noise_laeq_db"] == 49.9
        assert result["noise_la_min_db"] == 42.0
        assert result["noise_la_max_db"] == 60.1

    def test_extract_measurements_converts_unknown_to_none(self):
        values = [{"value_type": "P1", "value": "unknown"}]
        result = SensorCommunityAPI.extract_measurements(values)
        assert result["pm10_ug_m3"] is None
        assert result["pm2_5_ug_m3"] is None


@pytest.mark.unit
class TestTimestampDedup:
    """Test timestamp-based deduplication."""

    def test_should_emit_reading_for_new_timestamp(self):
        api = SensorCommunityAPI(state_file="")
        assert api.should_emit_reading(36083, "2026-04-06 10:24:02") is True

    def test_should_not_emit_duplicate_timestamp(self):
        api = SensorCommunityAPI(state_file="")
        api.remember_reading(36083, "2026-04-06 10:24:02")
        assert api.should_emit_reading(36083, "2026-04-06 10:24:02") is False
        assert api.should_emit_reading(36083, "2026-04-06 10:25:02") is True
