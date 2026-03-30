"""Unit tests for Waterinfo VMM bridge."""

import json
import pytest
from unittest.mock import patch, MagicMock
from waterinfo_vmm.waterinfo_vmm import WaterinfoVMMAPI
from waterinfo_vmm.waterinfo_vmm_producer.be.vlaanderen.waterinfo.vmm.station import Station
from waterinfo_vmm.waterinfo_vmm_producer.be.vlaanderen.waterinfo.vmm.water_level_reading import WaterLevelReading


class TestWaterinfoVMMInitialization:
    """Tests for WaterinfoVMMAPI initialization."""

    def test_init_creates_session(self):
        api = WaterinfoVMMAPI()
        assert api.session is not None

    def test_base_url_uses_https(self):
        api = WaterinfoVMMAPI()
        assert api.BASE_URL.startswith("https://")

    def test_kiwis_base_url(self):
        api = WaterinfoVMMAPI()
        assert "KiWIS" in api.BASE_URL

    def test_default_params_include_service(self):
        api = WaterinfoVMMAPI()
        assert api.DEFAULT_PARAMS["service"] == "kisters"
        assert api.DEFAULT_PARAMS["format"] == "json"
        assert api.DEFAULT_PARAMS["timezone"] == "UTC"

    def test_poll_interval_default(self):
        api = WaterinfoVMMAPI()
        assert api.POLL_INTERVAL_SECONDS == 900

    def test_water_level_group_id(self):
        api = WaterinfoVMMAPI()
        assert api.WATER_LEVEL_15M_GROUP == "192780"

    def test_api_has_required_methods(self):
        api = WaterinfoVMMAPI()
        assert hasattr(api, 'list_stations')
        assert hasattr(api, 'get_latest_water_levels')
        assert hasattr(api, 'feed_stations')
        assert hasattr(api, 'parse_connection_string')


class TestConnectionStringParsing:
    """Tests for Event Hubs connection string parsing."""

    def test_parse_event_hubs_connection_string(self):
        api = WaterinfoVMMAPI()
        cs = "Endpoint=sb://mynamespace.servicebus.windows.net;SharedAccessKeyName=mykey;SharedAccessKey=secret;EntityPath=mytopic"
        config = api.parse_connection_string(cs)
        assert 'bootstrap.servers' in config
        assert 'kafka_topic' in config

    def test_parse_connection_string_extracts_endpoint(self):
        api = WaterinfoVMMAPI()
        cs = "Endpoint=sb://test.servicebus.windows.net;SharedAccessKeyName=key;SharedAccessKey=secret;EntityPath=topic"
        config = api.parse_connection_string(cs)
        assert config['bootstrap.servers'] == "test.servicebus.windows.net:9093"

    def test_parse_connection_string_extracts_entity_path(self):
        api = WaterinfoVMMAPI()
        cs = "Endpoint=sb://test.servicebus.windows.net;SharedAccessKeyName=key;SharedAccessKey=secret;EntityPath=my-topic"
        config = api.parse_connection_string(cs)
        assert config['kafka_topic'] == "my-topic"

    def test_parse_connection_string_sets_sasl(self):
        api = WaterinfoVMMAPI()
        cs = "Endpoint=sb://x.servicebus.windows.net;SharedAccessKeyName=k;SharedAccessKey=s;EntityPath=t"
        config = api.parse_connection_string(cs)
        assert config['sasl.username'] == '$ConnectionString'
        assert config['sasl.password'] == cs

    def test_parse_connection_string_with_whitespace(self):
        api = WaterinfoVMMAPI()
        cs = "  Endpoint=sb://test.servicebus.windows.net;SharedAccessKeyName=k;SharedAccessKey=s;EntityPath=topic  "
        config = api.parse_connection_string(cs)
        assert config['sasl.password'] == cs.strip()
        assert config['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert config['kafka_topic'] == 'topic'

    def test_parse_connection_string_missing_endpoint(self):
        api = WaterinfoVMMAPI()
        config = api.parse_connection_string("InvalidString")
        assert 'bootstrap.servers' not in config


class TestDataClasses:
    """Tests for Station and WaterLevelReading data classes."""

    def test_station_creation(self):
        station = Station(
            station_no="L04_007",
            station_name="Wijnegem/Groot Schijn",
            station_id="12345",
            station_latitude=51.234,
            station_longitude=4.567,
            river_name="Groot Schijn",
            stationparameter_name="H",
            ts_id="99999042",
            ts_unitname="meter",
        )
        assert station.station_no == "L04_007"
        assert station.station_name == "Wijnegem/Groot Schijn"
        assert station.station_latitude == 51.234

    def test_station_json_roundtrip(self):
        station = Station(
            station_no="S02_44H",
            station_name="Kleit/Ede",
            station_id="441678",
            station_latitude=51.179,
            station_longitude=3.463,
            river_name="Ede",
            stationparameter_name="H",
            ts_id="306367042",
            ts_unitname="meter",
        )
        json_str = station.to_json()
        data = json.loads(json_str)
        restored = Station.from_dict(data)
        assert restored.station_no == station.station_no
        assert restored.station_latitude == station.station_latitude

    def test_water_level_reading_creation(self):
        reading = WaterLevelReading(
            ts_id="306367042",
            station_no="S02_44H",
            station_name="Kleit/Ede",
            timestamp="2026-03-25T10:15:00.000Z",
            value=6.118,
            unit_name="meter",
            parameter_name="H",
        )
        assert reading.ts_id == "306367042"
        assert reading.value == 6.118
        assert reading.parameter_name == "H"

    def test_water_level_reading_json_roundtrip(self):
        reading = WaterLevelReading(
            ts_id="92956042",
            station_no="L04_00H",
            station_name="Kieldrecht/Noordzuidverbinding",
            timestamp="2026-03-25T10:15:00.000Z",
            value=0.991,
            unit_name="meter",
            parameter_name="H",
        )
        json_str = reading.to_json()
        data = json.loads(json_str)
        restored = WaterLevelReading.from_dict(data)
        assert restored.ts_id == reading.ts_id
        assert restored.value == reading.value
        assert restored.timestamp == reading.timestamp

    def test_station_to_byte_array(self):
        station = Station(
            station_no="TEST",
            station_name="Test Station",
            station_id="1",
            station_latitude=50.0,
            station_longitude=4.0,
            river_name="Test River",
            stationparameter_name="H",
            ts_id="1",
            ts_unitname="meter",
        )
        data = station.to_byte_array("application/json")
        assert isinstance(data, bytes)
        parsed = json.loads(data)
        assert parsed["station_no"] == "TEST"

    def test_reading_from_data(self):
        json_str = '{"ts_id": "1", "station_no": "A", "station_name": "B", "timestamp": "2026-01-01T00:00:00Z", "value": 1.5, "unit_name": "meter", "parameter_name": "H"}'
        reading = WaterLevelReading.from_data(json_str)
        assert reading.ts_id == "1"
        assert reading.value == 1.5
