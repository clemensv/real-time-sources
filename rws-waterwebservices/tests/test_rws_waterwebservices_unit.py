"""Unit tests for RWS Waterwebservices bridge."""

import json
import pytest
from unittest.mock import patch, MagicMock
from rws_waterwebservices.rws_waterwebservices import RWSWaterwebservicesAPI
from rws_waterwebservices_producer_data import Station
from rws_waterwebservices_producer_data import WaterLevelObservation


class TestRWSInitialization:
    """Tests for RWSWaterwebservicesAPI initialization."""

    def test_init_creates_session(self):
        api = RWSWaterwebservicesAPI()
        assert api.session is not None

    def test_base_url_uses_https(self):
        api = RWSWaterwebservicesAPI()
        assert api.BASE_URL.startswith("https://")

    def test_base_url_points_to_rws(self):
        api = RWSWaterwebservicesAPI()
        assert "waterwebservices.rijkswaterstaat.nl" in api.BASE_URL

    def test_poll_interval_default(self):
        api = RWSWaterwebservicesAPI()
        assert api.POLL_INTERVAL_SECONDS == 600

    def test_compartiment_code(self):
        api = RWSWaterwebservicesAPI()
        assert api.COMPARTIMENT_CODE == "OW"

    def test_grootheid_code(self):
        api = RWSWaterwebservicesAPI()
        assert api.GROOTHEID_CODE == "WATHTE"

    def test_api_has_required_methods(self):
        api = RWSWaterwebservicesAPI()
        assert hasattr(api, 'get_catalog')
        assert hasattr(api, 'get_water_level_stations')
        assert hasattr(api, 'get_latest_observations')
        assert hasattr(api, 'feed_stations')
        assert hasattr(api, 'parse_connection_string')


class TestConnectionStringParsing:
    """Tests for Event Hubs connection string parsing."""

    def test_parse_event_hubs_connection_string(self):
        api = RWSWaterwebservicesAPI()
        cs = "Endpoint=sb://mynamespace.servicebus.windows.net;SharedAccessKeyName=mykey;SharedAccessKey=secret;EntityPath=mytopic"
        config = api.parse_connection_string(cs)
        assert 'bootstrap.servers' in config
        assert 'kafka_topic' in config

    def test_parse_connection_string_extracts_endpoint(self):
        api = RWSWaterwebservicesAPI()
        cs = "Endpoint=sb://test.servicebus.windows.net;SharedAccessKeyName=key;SharedAccessKey=secret;EntityPath=topic"
        config = api.parse_connection_string(cs)
        assert config['bootstrap.servers'] == "test.servicebus.windows.net:9093"

    def test_parse_connection_string_extracts_entity_path(self):
        api = RWSWaterwebservicesAPI()
        cs = "Endpoint=sb://test.servicebus.windows.net;SharedAccessKeyName=key;SharedAccessKey=secret;EntityPath=my-topic"
        config = api.parse_connection_string(cs)
        assert config['kafka_topic'] == "my-topic"

    def test_parse_connection_string_sets_sasl(self):
        api = RWSWaterwebservicesAPI()
        cs = "Endpoint=sb://x.servicebus.windows.net;SharedAccessKeyName=k;SharedAccessKey=s;EntityPath=t"
        config = api.parse_connection_string(cs)
        assert config['sasl.username'] == '$ConnectionString'
        assert config['sasl.password'] == cs

    def test_parse_connection_string_with_whitespace(self):
        api = RWSWaterwebservicesAPI()
        cs = "  Endpoint=sb://test.servicebus.windows.net;SharedAccessKeyName=k;SharedAccessKey=s;EntityPath=topic  "
        config = api.parse_connection_string(cs)
        assert config['sasl.password'] == cs.strip()
        assert config['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert config['kafka_topic'] == 'topic'

    def test_parse_connection_string_missing_endpoint(self):
        api = RWSWaterwebservicesAPI()
        config = api.parse_connection_string("InvalidString")
        assert 'bootstrap.servers' not in config


class TestDataClasses:
    """Tests for Station and WaterLevelObservation data classes."""

    def test_station_creation(self):
        station = Station(
            code="HOlv",
            name="Hoek van Holland",
            latitude=51.979,
            longitude=4.120,
            coordinate_system="25831",
        )
        assert station.code == "HOlv"
        assert station.name == "Hoek van Holland"
        assert station.latitude == 51.979

    def test_station_json_roundtrip(self):
        station = Station(
            code="DELF",
            name="Delfzijl",
            latitude=53.326,
            longitude=6.933,
            coordinate_system="25831",
        )
        json_str = station.to_json()
        data = json.loads(json_str)
        restored = Station.from_dict(data)
        assert restored.code == station.code
        assert restored.latitude == station.latitude

    def test_water_level_observation_creation(self):
        obs = WaterLevelObservation(
            location_code="HOlv",
            location_name="Hoek van Holland",
            timestamp="2026-03-25T10:00:00.000+01:00",
            value=123.0,
            unit="cm",
            quality_code="",
            status="",
            compartment="OW",
            parameter="WATHTE",
        )
        assert obs.location_code == "HOlv"
        assert obs.value == 123.0
        assert obs.unit == "cm"

    def test_water_level_observation_json_roundtrip(self):
        obs = WaterLevelObservation(
            location_code="DELF",
            location_name="Delfzijl",
            timestamp="2026-03-25T10:00:00.000+01:00",
            value=456.0,
            unit="cm",
            quality_code="25",
            status="Ongecontroleerd",
            compartment="OW",
            parameter="WATHTE",
        )
        json_str = obs.to_json()
        restored = WaterLevelObservation.from_data(json_str, "application/json")
        assert restored.location_code == obs.location_code
        assert restored.value == obs.value
        assert restored.timestamp == obs.timestamp

    def test_station_to_byte_array(self):
        station = Station(
            code="TEST",
            name="Test Station",
            latitude=52.0,
            longitude=5.0,
            coordinate_system="25831",
        )
        data = station.to_byte_array("application/json")
        assert isinstance(data, (bytes, str))
        parsed = json.loads(data)
        assert parsed["code"] == "TEST"

    def test_observation_from_data(self):
        json_str = '{"location_code": "HOlv", "location_name": "Hoek van Holland", "timestamp": "2026-01-01T00:00:00Z", "value": 100.0, "unit": "cm", "quality_code": "", "status": "", "compartment": "OW", "parameter": "WATHTE"}'
        obs = WaterLevelObservation.from_data(json_str, "application/json")
        assert obs.location_code == "HOlv"
        assert obs.value == 100.0


class TestAPIRequests:
    """Tests for API request construction."""

    @patch.object(RWSWaterwebservicesAPI, '_post_request')
    def test_get_catalog_calls_correct_endpoint(self, mock_post):
        mock_post.return_value = {"Succesvol": True, "AquoMetadataLijst": [], "LocatieLijst": [], "AquoMetadataLocatieLijst": []}
        api = RWSWaterwebservicesAPI()
        api.get_catalog()
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert "METADATASERVICES" in call_args[0][0]

    @patch.object(RWSWaterwebservicesAPI, '_post_request')
    def test_get_water_level_stations_filters_correctly(self, mock_post):
        mock_post.return_value = {
            "Succesvol": True,
            "AquoMetadataLijst": [
                {"Compartiment": {"Code": "OW"}, "Grootheid": {"Code": "WATHTE"}, "AquoMetadata_MessageID": 147},
                {"Compartiment": {"Code": "OW"}, "Grootheid": {"Code": "STROOMSHD"}, "AquoMetadata_MessageID": 200},
            ],
            "AquoMetadataLocatieLijst": [
                {"AquoMetaData_MessageID": 147, "Locatie_MessageID": 1},
                {"AquoMetaData_MessageID": 200, "Locatie_MessageID": 2},
            ],
            "LocatieLijst": [
                {"Code": "station1", "Naam": "Station 1", "Lat": 52.0, "Lon": 5.0, "Locatie_MessageID": 1},
                {"Code": "station2", "Naam": "Station 2", "Lat": 53.0, "Lon": 6.0, "Locatie_MessageID": 2},
            ],
        }
        api = RWSWaterwebservicesAPI()
        stations = api.get_water_level_stations()
        assert len(stations) == 1
        assert stations[0]["Code"] == "station1"

    @patch.object(RWSWaterwebservicesAPI, '_post_request')
    def test_get_latest_observations_calls_correct_endpoint(self, mock_post):
        mock_post.return_value = {"Succesvol": True, "WaarnemingenLijst": []}
        api = RWSWaterwebservicesAPI()
        api.get_latest_observations(["hoekvanholland"])
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert "ONLINEWAARNEMINGENSERVICES" in call_args[0][0]

    @patch.object(RWSWaterwebservicesAPI, '_post_request')
    def test_get_latest_observations_returns_empty_on_failure(self, mock_post):
        mock_post.return_value = {"Succesvol": False, "Foutmelding": "error"}
        api = RWSWaterwebservicesAPI()
        result = api.get_latest_observations(["hoekvanholland"])
        assert result == []

    @patch.object(RWSWaterwebservicesAPI, '_post_request')
    def test_get_latest_observations_handles_204(self, mock_post):
        mock_post.return_value = None  # 204 No Content
        api = RWSWaterwebservicesAPI()
        result = api.get_latest_observations(["unknown_station"])
        assert result == []

    @patch.object(RWSWaterwebservicesAPI, '_post_request')
    def test_get_latest_observations_returns_data(self, mock_post):
        mock_post.return_value = {
            "Succesvol": True,
            "WaarnemingenLijst": [
                {
                    "Locatie": {"Code": "hoekvanholland", "Naam": "Hoek van Holland", "Lat": 51.98, "Lon": 4.12},
                    "AquoMetadata": {"Eenheid": {"Code": "cm"}},
                    "MetingenLijst": [{"Tijdstip": "2026-01-01T00:00:00.000+01:00", "Meetwaarde": {"Waarde_Numeriek": 100.0}, "WaarnemingMetadata": {"Kwaliteitswaardecode": "00", "Statuswaarde": "Ongecontroleerd"}}]
                }
            ]
        }
        api = RWSWaterwebservicesAPI()
        result = api.get_latest_observations(["hoekvanholland"])
        assert len(result) == 1
        assert result[0]["Locatie"]["Code"] == "hoekvanholland"

    @patch.object(RWSWaterwebservicesAPI, '_post_request')
    def test_get_latest_observations_batches_requests(self, mock_post):
        mock_post.return_value = {"Succesvol": True, "WaarnemingenLijst": [{"test": True}]}
        api = RWSWaterwebservicesAPI()
        api.BATCH_SIZE = 2
        result = api.get_latest_observations(["s1", "s2", "s3"])
        assert mock_post.call_count == 2  # 2 batches: [s1,s2], [s3]
        assert len(result) == 2  # 1 item per batch
