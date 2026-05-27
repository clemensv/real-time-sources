"""
Unit tests for NOAA NWS Weather Alerts & Observations poller.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from noaa_nws.noaa_nws import NWSAlertPoller, parse_connection_string


@pytest.fixture
def mock_kafka_config():
    return {
        'bootstrap.servers': 'localhost:9092',
    }


@pytest.fixture
def temp_state_file():
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


def _make_poller(mock_kafka_config, temp_state_file):
    """Create a NWSAlertPoller with a mocked Kafka producer."""
    with patch('confluent_kafka.Producer') as mock_producer_class:
        mock_producer_class.return_value = MagicMock()
        poller = NWSAlertPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
        )
    return poller


@pytest.mark.unit
class TestNWSAlertPoller:
    def test_init(self, mock_kafka_config, temp_state_file):
        poller = _make_poller(mock_kafka_config, temp_state_file)
        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == temp_state_file
        assert poller.station_ids == []

    def test_load_seen_alerts_empty(self, mock_kafka_config):
        poller = _make_poller(mock_kafka_config, '/tmp/nonexistent_nws_state.json')
        state = poller.load_seen_alerts()
        assert state == {"seen_ids": []}

    def test_load_seen_alerts_existing(self, mock_kafka_config, temp_state_file):
        state_data = {"seen_ids": ["alert1", "alert2", "alert3"]}
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f)
        poller = _make_poller(mock_kafka_config, temp_state_file)
        state = poller.load_seen_alerts()
        assert state["seen_ids"] == ["alert1", "alert2", "alert3"]

    def test_save_seen_alerts(self, mock_kafka_config, temp_state_file):
        poller = _make_poller(mock_kafka_config, temp_state_file)
        poller.save_seen_alerts({"seen_ids": ["alert1", "alert2"]})
        with open(temp_state_file, 'r', encoding='utf-8') as f:
            saved = json.load(f)
        assert saved["seen_ids"] == ["alert1", "alert2"]

    @patch('noaa_nws.noaa_nws.requests.get')
    def test_poll_alerts_success(self, mock_get, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "type": "FeatureCollection",
            "features": [
                {
                    "properties": {
                        "id": "urn:oid:2.49.0.1.840.0.test1",
                        "areaDesc": "Test County",
                        "sent": "2024-01-01T00:00:00Z",
                        "effective": "2024-01-01T00:00:00Z",
                        "expires": "2024-01-01T12:00:00Z",
                        "status": "Actual",
                        "messageType": "Alert",
                        "category": "Met",
                        "severity": "Severe",
                        "certainty": "Likely",
                        "urgency": "Immediate",
                        "event": "Tornado Warning",
                        "senderName": "NWS Test",
                        "headline": "Tornado Warning for Test County",
                        "description": "A tornado warning has been issued."
                    }
                }
            ]
        }
        mock_get.return_value = mock_response
        poller = _make_poller(mock_kafka_config, temp_state_file)
        features = poller.poll_alerts()
        assert len(features) == 1
        assert features[0]["properties"]["id"] == "urn:oid:2.49.0.1.840.0.test1"

    @patch('noaa_nws.noaa_nws.requests.get')
    def test_poll_alerts_api_error(self, mock_get, mock_kafka_config, temp_state_file):
        mock_get.side_effect = Exception("Connection error")
        poller = _make_poller(mock_kafka_config, temp_state_file)
        features = poller.poll_alerts()
        assert features == []


@pytest.mark.unit
class TestParseConnectionString:
    def test_parse_valid_event_hubs(self):
        conn_str = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=myhub"
        result = parse_connection_string(conn_str)
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'myhub'
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == conn_str

    def test_parse_connection_string_without_entity_path(self):
        conn_str = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123"
        result = parse_connection_string(conn_str)
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert 'kafka_topic' not in result
        assert result['sasl.username'] == '$ConnectionString'

    def test_parse_bootstrap_server(self):
        conn_str = "BootstrapServer=localhost:9092;EntityPath=my-topic"
        result = parse_connection_string(conn_str)
        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'my-topic'

    def test_parse_password_is_full_string(self):
        conn_str = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=test;SharedAccessKey=key;EntityPath=hub"
        result = parse_connection_string(conn_str)
        assert result['sasl.password'] == conn_str


@pytest.mark.unit
class TestFetchZones:
    @patch('noaa_nws.noaa_nws.requests.get')
    def test_fetch_zones_success(self, mock_get, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "type": "FeatureCollection",
            "features": [
                {
                    "properties": {
                        "id": "AKZ101",
                        "name": "Western Prior Sound",
                        "type": "public",
                        "state": "AK",
                        "forecastOffice": "https://api.weather.gov/offices/AFC",
                        "timeZone": "America/Anchorage",
                        "radarStation": "PAHG"
                    }
                },
                {
                    "properties": {
                        "id": "TXZ211",
                        "name": "Dallas County",
                        "type": "public",
                        "state": "TX",
                        "forecastOffice": "https://api.weather.gov/offices/FWD",
                        "timeZone": "America/Chicago",
                        "radarStation": "KFWS"
                    }
                }
            ]
        }
        mock_get.return_value = mock_response
        poller = _make_poller(mock_kafka_config, temp_state_file)
        zones = poller.fetch_zones()
        assert len(zones) == 2
        assert zones[0].zone_id == "AKZ101"
        assert zones[0].state == "AK"
        assert zones[1].zone_id == "TXZ211"

    @patch('noaa_nws.noaa_nws.requests.get')
    def test_fetch_zones_api_error(self, mock_get, mock_kafka_config, temp_state_file):
        mock_get.side_effect = Exception("Connection error")
        poller = _make_poller(mock_kafka_config, temp_state_file)
        zones = poller.fetch_zones()
        assert zones == []


@pytest.mark.unit
class TestFetchObservationStations:
    @patch('noaa_nws.noaa_nws.requests.get')
    def test_fetch_stations_success(self, mock_get, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "type": "FeatureCollection",
            "features": [
                {
                    "properties": {
                        "stationIdentifier": "KJFK",
                        "name": "New York, Kennedy International Airport",
                        "elevation": {"unitCode": "wmoUnit:m", "value": 7},
                        "timeZone": "America/New_York",
                        "forecast": "https://api.weather.gov/zones/forecast/NYZ178",
                        "county": "https://api.weather.gov/zones/county/NYC081",
                        "fireWeatherZone": "https://api.weather.gov/zones/fire/NYZ178",
                    }
                },
                {
                    "properties": {
                        "stationIdentifier": "KLAX",
                        "name": "Los Angeles International Airport",
                        "elevation": {"unitCode": "wmoUnit:m", "value": 30},
                        "timeZone": "America/Los_Angeles",
                        "forecast": "https://api.weather.gov/zones/forecast/CAZ041",
                        "county": "https://api.weather.gov/zones/county/CAC037",
                        "fireWeatherZone": "https://api.weather.gov/zones/fire/CAZ041",
                    }
                }
            ],
            "pagination": {}
        }
        mock_get.return_value = mock_response
        poller = _make_poller(mock_kafka_config, temp_state_file)
        stations = poller.fetch_observation_stations()
        assert len(stations) == 2
        assert stations[0].station_id == "KJFK"
        assert stations[0].name == "New York, Kennedy International Airport"
        assert stations[0].elevation_m == 7.0
        assert stations[0].time_zone == "America/New_York"
        assert stations[0].forecast_zone == "NYZ178"
        assert stations[0].county == "NYC081"
        assert stations[0].fire_weather_zone == "NYZ178"
        assert stations[1].station_id == "KLAX"

    @patch('noaa_nws.noaa_nws.requests.get')
    def test_fetch_stations_null_elevation(self, mock_get, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "features": [
                {
                    "properties": {
                        "stationIdentifier": "TEST1",
                        "name": "Test Station",
                        "elevation": {"unitCode": "wmoUnit:m", "value": None},
                        "timeZone": "America/Chicago",
                        "forecast": "",
                        "county": "",
                        "fireWeatherZone": "",
                    }
                }
            ],
            "pagination": {}
        }
        mock_get.return_value = mock_response
        poller = _make_poller(mock_kafka_config, temp_state_file)
        stations = poller.fetch_observation_stations()
        assert len(stations) == 1
        assert stations[0].elevation_m is None

    @patch('noaa_nws.noaa_nws.requests.get')
    def test_fetch_stations_api_error(self, mock_get, mock_kafka_config, temp_state_file):
        mock_get.side_effect = Exception("Connection error")
        poller = _make_poller(mock_kafka_config, temp_state_file)
        stations = poller.fetch_observation_stations()
        assert stations == []


@pytest.mark.unit
class TestFetchLatestObservation:
    @patch('noaa_nws.noaa_nws.requests.get')
    def test_fetch_observation_success(self, mock_get, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "properties": {
                "timestamp": "2026-04-07T20:25:00+00:00",
                "textDescription": "Clear",
                "temperature": {"unitCode": "wmoUnit:degC", "value": 11, "qualityControl": "V"},
                "dewpoint": {"unitCode": "wmoUnit:degC", "value": -3, "qualityControl": "V"},
                "windDirection": {"unitCode": "wmoUnit:degree_(angle)", "value": 320, "qualityControl": "V"},
                "windSpeed": {"unitCode": "wmoUnit:km_h-1", "value": 28, "qualityControl": "V"},
                "windGust": {"unitCode": "wmoUnit:km_h-1", "value": 50, "qualityControl": "S"},
                "barometricPressure": {"unitCode": "wmoUnit:Pa", "value": 102370, "qualityControl": "V"},
                "seaLevelPressure": {"unitCode": "wmoUnit:Pa", "value": 102400, "qualityControl": "V"},
                "visibility": {"unitCode": "wmoUnit:m", "value": 16093, "qualityControl": "C"},
                "relativeHumidity": {"unitCode": "wmoUnit:percent", "value": 35, "qualityControl": "V"},
                "windChill": {"unitCode": "wmoUnit:degC", "value": None, "qualityControl": "V"},
                "heatIndex": {"unitCode": "wmoUnit:degC", "value": None, "qualityControl": "V"},
            }
        }
        mock_get.return_value = mock_response
        poller = _make_poller(mock_kafka_config, temp_state_file)
        obs = poller.fetch_latest_observation("KJFK")
        assert obs is not None
        assert obs.station_id == "KJFK"
        assert obs.timestamp == "2026-04-07T20:25:00+00:00"
        assert obs.text_description == "Clear"
        assert obs.temperature == 11.0
        assert obs.dewpoint == -3.0
        assert obs.wind_direction == 320.0
        assert obs.wind_speed == 28.0
        assert obs.wind_gust == 50.0
        assert obs.barometric_pressure == 102370.0
        assert obs.sea_level_pressure == 102400.0
        assert obs.visibility == 16093.0
        assert obs.relative_humidity == 35.0
        assert obs.wind_chill is None
        assert obs.heat_index is None

    @patch('noaa_nws.noaa_nws.requests.get')
    def test_fetch_observation_404(self, mock_get, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        poller = _make_poller(mock_kafka_config, temp_state_file)
        obs = poller.fetch_latest_observation("XXXXX")
        assert obs is None

    @patch('noaa_nws.noaa_nws.requests.get')
    def test_fetch_observation_no_timestamp(self, mock_get, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {"properties": {"textDescription": "Clear"}}
        mock_get.return_value = mock_response
        poller = _make_poller(mock_kafka_config, temp_state_file)
        obs = poller.fetch_latest_observation("KJFK")
        assert obs is None

    @patch('noaa_nws.noaa_nws.requests.get')
    def test_fetch_observation_network_error(self, mock_get, mock_kafka_config, temp_state_file):
        mock_get.side_effect = Exception("timeout")
        poller = _make_poller(mock_kafka_config, temp_state_file)
        obs = poller.fetch_latest_observation("KJFK")
        assert obs is None


@pytest.mark.unit
class TestExtractValue:
    def test_extract_from_quantity_object(self, mock_kafka_config, temp_state_file):
        poller = _make_poller(mock_kafka_config, temp_state_file)
        assert poller._extract_value({"value": 11, "unitCode": "wmoUnit:degC"}) == 11.0
        assert poller._extract_value({"value": 0}) == 0.0
        assert poller._extract_value({"value": None}) is None
        assert poller._extract_value(None) is None


@pytest.mark.unit
class TestDataclasses:
    def test_create_weather_alert(self):
        from noaa_nws_producer_data import WeatherAlert
        alert = WeatherAlert(
            alert_id="test-id",
            area_desc="Test Area",
            sent="2024-01-01T00:00:00Z",
            effective="2024-01-01T00:00:00Z",
            expires="2024-01-01T12:00:00Z",
            status="Actual",
            message_type="Alert",
            category="Met",
            severity="Severe",
            certainty="Likely",
            urgency="Immediate",
            event="Tornado Warning",
            sender_name="NWS Test",
            headline="Test Headline",
            description="Test Description"
        )
        assert alert.alert_id == "test-id"
        assert alert.severity == "Severe"

    def test_create_zone(self):
        from noaa_nws_producer_data import Zone
        zone = Zone(
            zone_id="AKZ317",
            name="Anchorage Bowl",
            type="public",
            state="AK",
            forecast_office="AFC",
            timezone="America/Anchorage",
            radar_station="PAHG"
        )
        assert zone.zone_id == "AKZ317"
        assert zone.state == "AK"

    def test_create_observation_station(self):
        from noaa_nws_producer_data.observationstation import ObservationStation
        station = ObservationStation(
            station_id="KJFK",
            name="JFK Airport",
            elevation_m=7.0,
            time_zone="America/New_York",
            forecast_zone="NYZ178",
            county="NYC081",
            fire_weather_zone="NYZ178",
        )
        assert station.station_id == "KJFK"
        assert station.elevation_m == 7.0

    def test_create_weather_observation(self):
        from noaa_nws_producer_data.weatherobservation import WeatherObservation
        obs = WeatherObservation(
            station_id="KJFK",
            timestamp="2026-04-07T20:00:00Z",
            text_description="Clear",
            temperature=11.0,
            dewpoint=-3.0,
            wind_direction=320.0,
            wind_speed=28.0,
            wind_gust=None,
            barometric_pressure=102370.0,
            sea_level_pressure=None,
            visibility=16093.0,
            relative_humidity=35.0,
            wind_chill=None,
            heat_index=None,
        )
        assert obs.station_id == "KJFK"
        assert obs.temperature == 11.0
        assert obs.wind_gust is None
