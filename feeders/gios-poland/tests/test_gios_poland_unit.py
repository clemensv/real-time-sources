"""
Unit tests for GIOŚ Poland Air Quality poller.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
import tempfile
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from gios_poland_producer_data import Station
from gios_poland_producer_data import Sensor
from gios_poland_producer_data import Measurement
from gios_poland_producer_data import AirQualityIndex
from gios_poland.gios_poland import (
    GIOSPolandPoller,
    parse_connection_string,
    map_polish_fields,
    parse_gios_timestamp,
    parse_optional_float,
    parse_optional_int,
    parse_station,
    parse_sensor,
    parse_measurement,
    parse_air_quality_index,
    STATION_FIELD_MAP,
    SENSOR_FIELD_MAP,
    MEASUREMENT_FIELD_MAP,
    AQI_FIELD_MAP,
)


SAMPLE_STATION_RAW = {
    "Identyfikator stacji": 52,
    "Kod stacji": "DsLegAlRzecz",
    "Nazwa stacji": "Legnica, Al. Rzeczypospolitej",
    "WGS84 φ N": "51.204503",
    "WGS84 λ E": "16.180513",
    "Identyfikator miasta": 453,
    "Nazwa miasta": "Legnica",
    "Gmina": "Legnica",
    "Powiat": "Legnica",
    "Województwo": "DOLNOŚLĄSKIE",
    "Ulica": "Al. Rzeczypospolitej 10/12",
}

SAMPLE_SENSOR_RAW = {
    "Identyfikator stanowiska": 291,
    "Identyfikator stacji": 52,
    "Wskaźnik": "dwutlenek azotu",
    "Wskaźnik - wzór": "NO2",
    "Wskaźnik - kod": "NO2",
    "Id wskaźnika": 6,
}

SAMPLE_MEASUREMENT_RAW = {
    "Kod stanowiska": "DsLegAlRzecz-NO2-1g",
    "Data": "2026-04-08 21:00:00",
    "Wartość": 16.0,
}

SAMPLE_MEASUREMENT_NULL_VALUE = {
    "Kod stanowiska": "DsLegAlRzecz-NO2-1g",
    "Data": "2026-04-08 20:00:00",
    "Wartość": None,
}

SAMPLE_AQI_RAW = {
    "Identyfikator stacji pomiarowej": 52,
    "Data wykonania obliczeń indeksu": "2026-04-08 20:20:20",
    "Wartość indeksu": 0,
    "Nazwa kategorii indeksu": "Bardzo dobry",
    "Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika st": "2026-04-08 20:00:00",
    "Data wykonania obliczeń indeksu dla wskaźnika SO2": "2026-04-08 20:20:20",
    "Wartość indeksu dla wskaźnika SO2": 0,
    "Nazwa kategorii indeksu dla wskażnika SO2": "Bardzo dobry",
    "Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika SO2": "2026-04-08 20:00:00",
    "Data wykonania obliczeń indeksu dla wskaźnika NO2": "2026-04-08 20:20:20",
    "Wartość indeksu dla wskaźnika NO2": 0,
    "Nazwa kategorii indeksu dla wskażnika NO2": "Bardzo dobry",
    "Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika NO2": "2026-04-08 20:00:00",
    "Data wykonania obliczeń indeksu dla wskaźnika PM10": "2026-04-08 20:20:20",
    "Wartość indeksu dla wskaźnika PM10": 0,
    "Nazwa kategorii indeksu dla wskażnika PM10": "Bardzo dobry",
    "Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika PM10": "2026-04-08 20:00:00",
    "Data wykonania obliczeń indeksu dla wskaźnika PM2.5": "2026-04-08 20:20:20",
    "Wartość indeksu dla wskaźnika PM2.5": 0,
    "Nazwa kategorii indeksu dla wskażnika PM2.5": "Bardzo dobry",
    "Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika PM2.5": "2026-04-08 20:00:00",
    "Data wykonania obliczeń indeksu dla wskaźnika O3": "2026-04-08 20:20:20",
    "Wartość indeksu dla wskaźnika O3": 0,
    "Nazwa kategorii indeksu dla wskażnika O3": "Bardzo dobry",
    "Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika O3": "2026-04-08 20:00:00",
    "Status indeksu ogólnego dla stacji pomiarowej": True,
    "Kod zanieczyszczenia krytycznego": "OZON",
}


@pytest.mark.unit
class TestMapPolishFields:
    """Unit tests for the map_polish_fields helper"""

    def test_maps_station_fields(self):
        result = map_polish_fields(SAMPLE_STATION_RAW, STATION_FIELD_MAP)
        assert result["station_id"] == 52
        assert result["station_code"] == "DsLegAlRzecz"
        assert result["name"] == "Legnica, Al. Rzeczypospolitej"
        assert result["latitude"] == "51.204503"
        assert result["longitude"] == "16.180513"
        assert result["city_name"] == "Legnica"
        assert result["voivodeship"] == "DOLNOŚLĄSKIE"

    def test_maps_sensor_fields(self):
        result = map_polish_fields(SAMPLE_SENSOR_RAW, SENSOR_FIELD_MAP)
        assert result["sensor_id"] == 291
        assert result["station_id"] == 52
        assert result["parameter_name"] == "dwutlenek azotu"
        assert result["parameter_code"] == "NO2"

    def test_maps_measurement_fields(self):
        result = map_polish_fields(SAMPLE_MEASUREMENT_RAW, MEASUREMENT_FIELD_MAP)
        assert result["sensor_code"] == "DsLegAlRzecz-NO2-1g"
        assert result["timestamp"] == "2026-04-08 21:00:00"
        assert result["value"] == 16.0

    def test_ignores_unmapped_fields(self):
        data = {"Identyfikator stacji": 52, "UnknownField": "foo"}
        result = map_polish_fields(data, STATION_FIELD_MAP)
        assert result["station_id"] == 52
        assert "UnknownField" not in result


@pytest.mark.unit
class TestParseGiosTimestamp:
    """Unit tests for the parse_gios_timestamp helper"""

    def test_parse_standard_format(self):
        ts = parse_gios_timestamp("2026-04-08 21:00:00")
        assert ts is not None
        assert ts.year == 2026
        assert ts.month == 4
        assert ts.day == 8
        assert ts.hour == 21
        assert ts.minute == 0

    def test_parse_iso_format(self):
        ts = parse_gios_timestamp("2026-04-08T21:00:00")
        assert ts is not None
        assert ts.hour == 21

    def test_parse_none_returns_none(self):
        assert parse_gios_timestamp(None) is None

    def test_parse_empty_returns_none(self):
        assert parse_gios_timestamp("") is None

    def test_parse_invalid_returns_none(self):
        assert parse_gios_timestamp("not-a-date") is None

    def test_parse_datetime_passthrough(self):
        dt = datetime(2026, 4, 8, 21, 0, 0)
        assert parse_gios_timestamp(dt) is dt


@pytest.mark.unit
class TestParseOptionalFloat:
    """Unit tests for the parse_optional_float helper"""

    def test_parse_valid_float(self):
        assert parse_optional_float(16.0) == 16.0

    def test_parse_string_float(self):
        assert parse_optional_float("51.204503") == 51.204503

    def test_parse_none_returns_none(self):
        assert parse_optional_float(None) is None

    def test_parse_invalid_returns_none(self):
        assert parse_optional_float("not-a-number") is None


@pytest.mark.unit
class TestParseOptionalInt:
    """Unit tests for the parse_optional_int helper"""

    def test_parse_valid_int(self):
        assert parse_optional_int(52) == 52

    def test_parse_string_int(self):
        assert parse_optional_int("52") == 52

    def test_parse_none_returns_none(self):
        assert parse_optional_int(None) is None

    def test_parse_invalid_returns_none(self):
        assert parse_optional_int("not-an-int") is None


@pytest.mark.unit
class TestParseStation:
    """Unit tests for station parsing"""

    def test_parse_valid_station(self):
        station = parse_station(SAMPLE_STATION_RAW)
        assert station is not None
        assert station.station_id == 52
        assert station.station_code == "DsLegAlRzecz"
        assert station.name == "Legnica, Al. Rzeczypospolitej"
        assert station.latitude == pytest.approx(51.204503)
        assert station.longitude == pytest.approx(16.180513)
        assert station.city_id == 453
        assert station.city_name == "Legnica"
        assert station.commune == "Legnica"
        assert station.district == "Legnica"
        assert station.voivodeship == "DOLNOŚLĄSKIE"
        assert station.street == "Al. Rzeczypospolitej 10/12"

    def test_parse_station_with_null_street(self):
        raw = dict(SAMPLE_STATION_RAW)
        raw["Ulica"] = None
        station = parse_station(raw)
        assert station is not None
        assert station.street is None

    def test_parse_station_missing_required_field(self):
        raw = dict(SAMPLE_STATION_RAW)
        del raw["Identyfikator stacji"]
        station = parse_station(raw)
        assert station is None


@pytest.mark.unit
class TestParseSensor:
    """Unit tests for sensor parsing"""

    def test_parse_valid_sensor(self):
        sensor = parse_sensor(SAMPLE_SENSOR_RAW)
        assert sensor is not None
        assert sensor.sensor_id == 291
        assert sensor.station_id == 52
        assert sensor.parameter_name == "dwutlenek azotu"
        assert sensor.parameter_formula == "NO2"
        assert sensor.parameter_code == "NO2"
        assert sensor.parameter_id == 6

    def test_parse_sensor_missing_required_field(self):
        raw = dict(SAMPLE_SENSOR_RAW)
        del raw["Identyfikator stanowiska"]
        sensor = parse_sensor(raw)
        assert sensor is None


@pytest.mark.unit
class TestParseMeasurement:
    """Unit tests for measurement parsing"""

    def test_parse_valid_measurement(self):
        measurement = parse_measurement(SAMPLE_MEASUREMENT_RAW, station_id=52, sensor_id=291)
        assert measurement is not None
        assert measurement.station_id == 52
        assert measurement.sensor_id == 291
        assert measurement.sensor_code == "DsLegAlRzecz-NO2-1g"
        assert measurement.value == 16.0
        assert measurement.timestamp.year == 2026
        assert measurement.timestamp.hour == 21

    def test_parse_measurement_with_null_value(self):
        measurement = parse_measurement(SAMPLE_MEASUREMENT_NULL_VALUE, station_id=52, sensor_id=291)
        assert measurement is not None
        assert measurement.value is None
        assert measurement.timestamp.hour == 20

    def test_parse_measurement_missing_timestamp(self):
        raw = {"Kod stanowiska": "test", "Wartość": 5.0}
        measurement = parse_measurement(raw, station_id=52, sensor_id=291)
        assert measurement is None


@pytest.mark.unit
class TestParseAirQualityIndex:
    """Unit tests for AQI parsing"""

    def test_parse_valid_aqi(self):
        aqi = parse_air_quality_index(SAMPLE_AQI_RAW)
        assert aqi is not None
        assert aqi.station_id == 52
        assert aqi.index_value == 0
        assert aqi.index_category == "Bardzo dobry"
        assert aqi.so2_index_value == 0
        assert aqi.so2_index_category == "Bardzo dobry"
        assert aqi.no2_index_value == 0
        assert aqi.pm10_index_value == 0
        assert aqi.pm25_index_value == 0
        assert aqi.o3_index_value == 0
        assert aqi.overall_status is True
        assert aqi.critical_pollutant_code == "OZON"
        assert aqi.calculation_timestamp.year == 2026
        assert aqi.calculation_timestamp.hour == 20
        assert aqi.calculation_timestamp.minute == 20

    def test_parse_aqi_with_null_subindex(self):
        raw = dict(SAMPLE_AQI_RAW)
        raw["Wartość indeksu dla wskaźnika SO2"] = None
        raw["Nazwa kategorii indeksu dla wskażnika SO2"] = None
        aqi = parse_air_quality_index(raw)
        assert aqi is not None
        assert aqi.so2_index_value is None
        assert aqi.so2_index_category is None

    def test_parse_aqi_missing_calculation_timestamp(self):
        raw = dict(SAMPLE_AQI_RAW)
        del raw["Data wykonania obliczeń indeksu"]
        aqi = parse_air_quality_index(raw)
        assert aqi is None

    def test_aqi_categories_mapping(self):
        """Test that all 6 AQI categories are correctly preserved"""
        categories = [
            ("Bardzo dobry", 0),
            ("Dobry", 1),
            ("Umiarkowany", 2),
            ("Dostateczny", 3),
            ("Zły", 4),
            ("Bardzo zły", 5),
        ]
        for category_name, category_value in categories:
            raw = dict(SAMPLE_AQI_RAW)
            raw["Wartość indeksu"] = category_value
            raw["Nazwa kategorii indeksu"] = category_name
            aqi = parse_air_quality_index(raw)
            assert aqi is not None
            assert aqi.index_value == category_value
            assert aqi.index_category == category_name


@pytest.mark.unit
class TestParseConnectionString:
    """Unit tests for connection string parsing"""

    def test_parse_event_hubs_connection_string(self):
        conn_str = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=mykey;SharedAccessKey=secret123;EntityPath=mytopic"
        result = parse_connection_string(conn_str)
        assert 'mynamespace.servicebus.windows.net:9093' in result['bootstrap.servers']
        assert result['kafka_topic'] == 'mytopic'
        assert result['sasl.username'] == '$ConnectionString'
        assert result['security.protocol'] == 'SASL_SSL'

    def test_parse_bootstrap_server_connection_string(self):
        conn_str = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = parse_connection_string(conn_str)
        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'test-topic'

    def test_parse_empty_connection_string(self):
        result = parse_connection_string("")
        assert 'bootstrap.servers' not in result


@pytest.mark.unit
class TestGIOSPolandPoller:
    """Unit tests for the GIOSPolandPoller class"""

    @pytest.fixture
    def mock_kafka_config(self):
        return {
            'bootstrap.servers': 'localhost:9092',
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL',
            'sasl.username': 'test_user',
            'sasl.password': 'test_password'
        }

    @pytest.fixture
    def temp_state_file(self):
        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    @patch('gios_poland.gios_poland.PlGovGiosAirqualityEventProducer')
    @patch('confluent_kafka.Producer')
    def test_init(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test GIOSPolandPoller initialization"""
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer

        poller = GIOSPolandPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == temp_state_file
        mock_producer_class.assert_called_once_with(mock_kafka_config)
        mock_event_producer.assert_called_once_with(mock_kafka_producer, 'test-topic')

    @patch('gios_poland.gios_poland.PlGovGiosAirqualityEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_state_empty(self, mock_producer_class, mock_event_producer, mock_kafka_config):
        """Test loading state when no state file exists"""
        poller = GIOSPolandPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file='nonexistent_gios_state.json'
        )

        state = poller.load_state()
        assert state == {"measurement_timestamps": {}, "aqi_timestamps": {}}

    @patch('gios_poland.gios_poland.PlGovGiosAirqualityEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_and_save_state(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test saving and loading state"""
        poller = GIOSPolandPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        state = {
            "measurement_timestamps": {"291:2026-04-08T21:00:00": "2026-04-08T21:00:00"},
            "aqi_timestamps": {"52:2026-04-08T20:20:20": "2026-04-08T20:20:20"},
        }
        poller.save_state(state)

        loaded = poller.load_state()
        assert loaded["measurement_timestamps"]["291:2026-04-08T21:00:00"] == "2026-04-08T21:00:00"
        assert loaded["aqi_timestamps"]["52:2026-04-08T20:20:20"] == "2026-04-08T20:20:20"

    def test_station_serialization_roundtrip(self):
        """Test that Station dataclass can be serialized and deserialized"""
        station = parse_station(SAMPLE_STATION_RAW)
        assert station is not None
        json_str = station.to_json()
        data = json.loads(json_str)
        assert data["station_id"] == 52
        assert data["station_code"] == "DsLegAlRzecz"

    def test_sensor_serialization_roundtrip(self):
        """Test that Sensor dataclass can be serialized and deserialized"""
        sensor = parse_sensor(SAMPLE_SENSOR_RAW)
        assert sensor is not None
        json_str = sensor.to_json()
        data = json.loads(json_str)
        assert data["sensor_id"] == 291
        assert data["parameter_code"] == "NO2"

    def test_measurement_serialization_roundtrip(self):
        """Test that Measurement dataclass can be serialized and deserialized"""
        measurement = parse_measurement(SAMPLE_MEASUREMENT_RAW, station_id=52, sensor_id=291)
        assert measurement is not None
        json_str = measurement.to_json()
        data = json.loads(json_str)
        assert data["station_id"] == 52
        assert data["sensor_id"] == 291
        assert data["value"] == 16.0

    def test_deduplication_logic(self):
        """Test that deduplication works by timestamp key"""
        timestamps = {}
        raw_list = [SAMPLE_MEASUREMENT_RAW, SAMPLE_MEASUREMENT_RAW]
        new_count = 0
        for raw in raw_list:
            m = parse_measurement(raw, station_id=52, sensor_id=291)
            if m is None:
                continue
            ts_key = f"{291}:{m.timestamp.isoformat()}"
            if ts_key in timestamps:
                continue
            timestamps[ts_key] = m.timestamp.isoformat()
            new_count += 1
        assert new_count == 1
