"""
Unit tests for NOAA NWS Weather Alerts poller.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from noaa_nws.noaa_nws import NWSAlertPoller, parse_connection_string


@pytest.mark.unit
class TestNWSAlertPoller:
    """Unit tests for the NWSAlertPoller class"""

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

    @patch('noaa_nws.noaa_nws.MicrosoftOpenDataUSNOAANWSEventProducer')
    @patch('confluent_kafka.Producer')
    def test_init(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test NWSAlertPoller initialization"""
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer

        poller = NWSAlertPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == temp_state_file
        mock_producer_class.assert_called_once_with(mock_kafka_config)
        mock_event_producer.assert_called_once_with(mock_kafka_producer, 'test-topic')

    @patch('noaa_nws.noaa_nws.MicrosoftOpenDataUSNOAANWSEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_seen_alerts_empty(self, mock_producer_class, mock_event_producer, mock_kafka_config):
        """Test loading seen alerts when no state file exists"""
        poller = NWSAlertPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file='/tmp/nonexistent_nws_state.json'
        )

        state = poller.load_seen_alerts()
        assert state == {"seen_ids": []}

    @patch('noaa_nws.noaa_nws.MicrosoftOpenDataUSNOAANWSEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_seen_alerts_existing(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test loading seen alerts from existing state file"""
        state_data = {"seen_ids": ["alert1", "alert2", "alert3"]}
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f)

        poller = NWSAlertPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        state = poller.load_seen_alerts()
        assert state["seen_ids"] == ["alert1", "alert2", "alert3"]

    @patch('noaa_nws.noaa_nws.MicrosoftOpenDataUSNOAANWSEventProducer')
    @patch('confluent_kafka.Producer')
    def test_save_seen_alerts(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test saving seen alerts to state file"""
        poller = NWSAlertPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        state_data = {"seen_ids": ["alert1", "alert2"]}
        poller.save_seen_alerts(state_data)

        with open(temp_state_file, 'r', encoding='utf-8') as f:
            saved = json.load(f)
        assert saved["seen_ids"] == ["alert1", "alert2"]

    @patch('noaa_nws.noaa_nws.requests.get')
    @patch('noaa_nws.noaa_nws.MicrosoftOpenDataUSNOAANWSEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_alerts_success(self, mock_producer_class, mock_event_producer, mock_get, mock_kafka_config, temp_state_file):
        """Test polling alerts returns features"""
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

        poller = NWSAlertPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        features = poller.poll_alerts()
        assert len(features) == 1
        assert features[0]["properties"]["id"] == "urn:oid:2.49.0.1.840.0.test1"

    @patch('noaa_nws.noaa_nws.requests.get')
    @patch('noaa_nws.noaa_nws.MicrosoftOpenDataUSNOAANWSEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_alerts_api_error(self, mock_producer_class, mock_event_producer, mock_get, mock_kafka_config, temp_state_file):
        """Test polling alerts handles API errors gracefully"""
        mock_get.side_effect = Exception("Connection error")

        poller = NWSAlertPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        features = poller.poll_alerts()
        assert features == []


@pytest.mark.unit
class TestParseConnectionString:
    """Unit tests for parse_connection_string function"""

    def test_parse_valid_connection_string(self):
        """Test parsing a valid Event Hubs connection string"""
        conn_str = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=myhub"

        result = parse_connection_string(conn_str)

        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'myhub'
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == conn_str

    def test_parse_connection_string_without_entity_path(self):
        """Test parsing a connection string without EntityPath"""
        conn_str = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123"

        result = parse_connection_string(conn_str)

        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert 'kafka_topic' not in result
        assert result['sasl.username'] == '$ConnectionString'

    def test_parse_connection_string_password_is_full_string(self):
        """Test that the password is the entire connection string"""
        conn_str = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=test;SharedAccessKey=key;EntityPath=hub"

        result = parse_connection_string(conn_str)

        assert result['sasl.password'] == conn_str


@pytest.mark.unit
class TestWeatherAlertDataclass:
    """Unit tests for WeatherAlert dataclass creation"""

    def test_create_weather_alert(self):
        """Test creating a WeatherAlert dataclass instance"""
        from noaa_nws.noaa_nws_producer.microsoft.opendata.us.noaa.nws.weatheralert import WeatherAlert

        alert = WeatherAlert(
            alert_id="urn:oid:2.49.0.1.840.0.test1",
            area_desc="Test County, TX",
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
            sender_name="NWS Fort Worth TX",
            headline="Tornado Warning for Test County",
            description="The National Weather Service has issued a tornado warning."
        )

        assert alert.alert_id == "urn:oid:2.49.0.1.840.0.test1"
        assert alert.area_desc == "Test County, TX"
        assert alert.severity == "Severe"
        assert alert.event == "Tornado Warning"
        assert alert.sender_name == "NWS Fort Worth TX"

    def test_weather_alert_optional_fields(self):
        """Test creating a WeatherAlert with empty optional fields"""
        from noaa_nws.noaa_nws_producer.microsoft.opendata.us.noaa.nws.weatheralert import WeatherAlert

        alert = WeatherAlert(
            alert_id="test-id",
            area_desc="Test Area",
            sent="2024-01-01T00:00:00Z",
            effective="2024-01-01T00:00:00Z",
            expires="2024-01-01T12:00:00Z",
            status="Actual",
            message_type="Alert",
            category="Met",
            severity="Minor",
            certainty="Possible",
            urgency="Future",
            event="Heat Advisory",
            sender_name="",
            headline="",
            description=""
        )

        assert alert.alert_id == "test-id"
        assert alert.headline == ""
        assert alert.description == ""


@pytest.mark.unit
class TestFetchZones:
    """Unit tests for NWSAlertPoller.fetch_zones()"""

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

    @patch('noaa_nws.noaa_nws.requests.get')
    @patch('noaa_nws.noaa_nws.MicrosoftOpenDataUSNOAANWSEventProducer')
    @patch('confluent_kafka.Producer')
    def test_fetch_zones_success(self, mock_producer_class, mock_event_producer, mock_get, mock_kafka_config, temp_state_file):
        """Test fetching zones parses response correctly"""
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

        poller = NWSAlertPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        zones = poller.fetch_zones()
        assert len(zones) == 2
        assert zones[0].zone_id == "AKZ101"
        assert zones[0].name == "Western Prior Sound"
        assert zones[0].state == "AK"
        assert zones[0].forecast_office == "https://api.weather.gov/offices/AFC"
        assert zones[0].timezone == "America/Anchorage"
        assert zones[0].radar_station == "PAHG"
        assert zones[1].zone_id == "TXZ211"
        assert zones[1].state == "TX"

    @patch('noaa_nws.noaa_nws.requests.get')
    @patch('noaa_nws.noaa_nws.MicrosoftOpenDataUSNOAANWSEventProducer')
    @patch('confluent_kafka.Producer')
    def test_fetch_zones_api_error(self, mock_producer_class, mock_event_producer, mock_get, mock_kafka_config, temp_state_file):
        """Test fetch_zones handles API errors gracefully"""
        mock_get.side_effect = Exception("Connection error")

        poller = NWSAlertPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        zones = poller.fetch_zones()
        assert zones == []


@pytest.mark.unit
class TestZoneDataclass:
    """Unit tests for Zone dataclass creation"""

    def test_create_zone(self):
        """Test creating a Zone dataclass instance"""
        from noaa_nws.noaa_nws_producer.microsoft.opendata.us.noaa.nws.zone import Zone

        zone = Zone(
            zone_id="AKZ317",
            name="Anchorage Bowl",
            type="public",
            state="AK",
            forecast_office="https://api.weather.gov/offices/AFC",
            timezone="America/Anchorage",
            radar_station="PAHG"
        )

        assert zone.zone_id == "AKZ317"
        assert zone.name == "Anchorage Bowl"
        assert zone.type == "public"
        assert zone.state == "AK"
        assert zone.forecast_office == "https://api.weather.gov/offices/AFC"
        assert zone.timezone == "America/Anchorage"
        assert zone.radar_station == "PAHG"

    def test_zone_with_empty_optional_fields(self):
        """Test creating a Zone with empty optional fields"""
        from noaa_nws.noaa_nws_producer.microsoft.opendata.us.noaa.nws.zone import Zone

        zone = Zone(
            zone_id="TXZ001",
            name="Test Zone",
            type="",
            state="TX",
            forecast_office="",
            timezone="",
            radar_station=""
        )

        assert zone.zone_id == "TXZ001"
        assert zone.name == "Test Zone"
        assert zone.state == "TX"
        assert zone.forecast_office == ""
