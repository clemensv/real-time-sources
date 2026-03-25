"""
Unit tests for NOAA SWPC Space Weather poller.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from noaa_goes.noaa_goes import SWPCPoller, parse_connection_string


@pytest.mark.unit
class TestSWPCPoller:
    """Unit tests for the SWPCPoller class"""

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

    @patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_init(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test SWPCPoller initialization"""
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer

        poller = SWPCPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == temp_state_file
        mock_producer_class.assert_called_once_with(mock_kafka_config)
        mock_event_producer.assert_called_once_with(mock_kafka_producer, 'test-topic')

    @patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_state_empty(self, mock_producer_class, mock_event_producer, mock_kafka_config):
        """Test loading state when no state file exists"""
        poller = SWPCPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file='/tmp/nonexistent_swpc_state.json'
        )

        state = poller.load_state()
        assert state == {"last_alert_id": None, "last_kindex_time": None, "last_solar_wind_time": None}

    @patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_state_existing(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test loading state from existing state file"""
        state_data = {"last_alert_id": "alert123", "last_kindex_time": "2024-01-01 00:00:00", "last_solar_wind_time": "2024-01-01 00:05:00"}
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f)

        poller = SWPCPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        state = poller.load_state()
        assert state["last_alert_id"] == "alert123"
        assert state["last_kindex_time"] == "2024-01-01 00:00:00"

    @patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_save_state(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test saving state to state file"""
        poller = SWPCPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        state_data = {"last_alert_id": "alert456", "last_kindex_time": "2024-01-01 03:00:00", "last_solar_wind_time": None}
        poller.save_state(state_data)

        with open(temp_state_file, 'r', encoding='utf-8') as f:
            saved = json.load(f)
        assert saved["last_alert_id"] == "alert456"

    @patch('noaa_goes.noaa_goes.requests.get')
    @patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_alerts_success(self, mock_producer_class, mock_event_producer, mock_get, mock_kafka_config, temp_state_file):
        """Test polling alerts returns alert list"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = [
            {
                "product_id": "ALTK04-20240101",
                "issue_datetime": "2024 Jan 01 0030 UTC",
                "message": "Space Weather Message Code: ALTK04\nSerial Number: 1234\nIssue Time: 2024 Jan 01 0030 UTC\n\nALERT: Geomagnetic K-index of 4\nThreshold Reached: 2024 Jan 01 0029 UTC"
            }
        ]
        mock_get.return_value = mock_response

        poller = SWPCPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        alerts = poller.poll_alerts()
        assert len(alerts) == 1
        assert alerts[0]["product_id"] == "ALTK04-20240101"

    @patch('noaa_goes.noaa_goes.requests.get')
    @patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_alerts_api_error(self, mock_producer_class, mock_event_producer, mock_get, mock_kafka_config, temp_state_file):
        """Test polling alerts handles API errors gracefully"""
        mock_get.side_effect = Exception("Connection error")

        poller = SWPCPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        alerts = poller.poll_alerts()
        assert alerts == []

    @patch('noaa_goes.noaa_goes.requests.get')
    @patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_k_index_success(self, mock_producer_class, mock_event_producer, mock_get, mock_kafka_config, temp_state_file):
        """Test polling K-index returns data rows (skipping header)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = [
            ["time_tag", "Kp", "a_running", "station_count"],
            ["2024-01-01 00:00:00.000", "2", "5", "8"],
            ["2024-01-01 03:00:00.000", "3", "7", "8"]
        ]
        mock_get.return_value = mock_response

        poller = SWPCPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        rows = poller.poll_k_index()
        assert len(rows) == 2
        assert rows[0][0] == "2024-01-01 00:00:00.000"
        assert rows[0][1] == "2"

    @patch('noaa_goes.noaa_goes.requests.get')
    @patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_k_index_api_error(self, mock_producer_class, mock_event_producer, mock_get, mock_kafka_config, temp_state_file):
        """Test polling K-index handles API errors gracefully"""
        mock_get.side_effect = Exception("Timeout")

        poller = SWPCPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        rows = poller.poll_k_index()
        assert rows == []

    @patch('noaa_goes.noaa_goes.requests.get')
    @patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_solar_wind_success(self, mock_producer_class, mock_event_producer, mock_get, mock_kafka_config, temp_state_file):
        """Test polling solar wind combines speed and mag field data"""
        speed_response = Mock()
        speed_response.status_code = 200
        speed_response.raise_for_status = Mock()
        speed_response.json.return_value = {"TimeStamp": "2024-01-01T00:05:00Z", "WindSpeed": "425.3"}

        mag_response = Mock()
        mag_response.status_code = 200
        mag_response.raise_for_status = Mock()
        mag_response.json.return_value = {"TimeStamp": "2024-01-01T00:05:00Z", "Bt": "5.2", "Bz": "-1.3"}

        mock_get.side_effect = [speed_response, mag_response]

        poller = SWPCPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        records = poller.poll_solar_wind()
        assert len(records) == 1
        assert records[0]["timestamp"] == "2024-01-01T00:05:00Z"
        assert records[0]["wind_speed"] == 425.3
        assert records[0]["bt"] == 5.2
        assert records[0]["bz"] == -1.3

    @patch('noaa_goes.noaa_goes.requests.get')
    @patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_solar_wind_api_error(self, mock_producer_class, mock_event_producer, mock_get, mock_kafka_config, temp_state_file):
        """Test polling solar wind handles API errors gracefully"""
        mock_get.side_effect = Exception("Network error")

        poller = SWPCPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        records = poller.poll_solar_wind()
        assert records == []


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
class TestSpaceWeatherAlertDataclass:
    """Unit tests for SpaceWeatherAlert dataclass creation"""

    def test_create_space_weather_alert(self):
        """Test creating a SpaceWeatherAlert dataclass instance"""
        from noaa_goes.noaa_goes_producer.microsoft.opendata.us.noaa.swpc.spaceweatheralert import SpaceWeatherAlert

        alert = SpaceWeatherAlert(
            product_id="ALTK04-20240101",
            issue_datetime="2024 Jan 01 0030 UTC",
            message="Space Weather Message Code: ALTK04\nGeomagnetic K-index of 4"
        )

        assert alert.product_id == "ALTK04-20240101"
        assert alert.issue_datetime == "2024 Jan 01 0030 UTC"
        assert "ALTK04" in alert.message

    def test_create_space_weather_alert_empty_fields(self):
        """Test creating a SpaceWeatherAlert with empty fields"""
        from noaa_goes.noaa_goes_producer.microsoft.opendata.us.noaa.swpc.spaceweatheralert import SpaceWeatherAlert

        alert = SpaceWeatherAlert(
            product_id="",
            issue_datetime="",
            message=""
        )

        assert alert.product_id == ""
        assert alert.issue_datetime == ""
        assert alert.message == ""


@pytest.mark.unit
class TestPlanetaryKIndexDataclass:
    """Unit tests for PlanetaryKIndex dataclass creation"""

    def test_create_planetary_k_index(self):
        """Test creating a PlanetaryKIndex dataclass instance"""
        from noaa_goes.noaa_goes_producer.microsoft.opendata.us.noaa.swpc.planetarykindex import PlanetaryKIndex

        kindex = PlanetaryKIndex(
            time_tag="2024-01-01 00:00:00.000",
            kp=3.0,
            a_running=15.0,
            station_count=8.0
        )

        assert kindex.time_tag == "2024-01-01 00:00:00.000"
        assert kindex.kp == 3.0
        assert kindex.a_running == 15.0
        assert kindex.station_count == 8.0

    def test_create_planetary_k_index_zero_values(self):
        """Test creating a PlanetaryKIndex with zero values"""
        from noaa_goes.noaa_goes_producer.microsoft.opendata.us.noaa.swpc.planetarykindex import PlanetaryKIndex

        kindex = PlanetaryKIndex(
            time_tag="2024-01-01 00:00:00.000",
            kp=0.0,
            a_running=0.0,
            station_count=0.0
        )

        assert kindex.kp == 0.0
        assert kindex.station_count == 0.0


@pytest.mark.unit
class TestSolarWindSummaryDataclass:
    """Unit tests for SolarWindSummary dataclass creation"""

    def test_create_solar_wind_summary(self):
        """Test creating a SolarWindSummary dataclass instance"""
        from noaa_goes.noaa_goes_producer.microsoft.opendata.us.noaa.swpc.solarwindsummary import SolarWindSummary

        summary = SolarWindSummary(
            timestamp="2024-01-01T00:05:00Z",
            wind_speed=425.3,
            bt=5.2,
            bz=-1.3
        )

        assert summary.timestamp == "2024-01-01T00:05:00Z"
        assert summary.wind_speed == 425.3
        assert summary.bt == 5.2
        assert summary.bz == -1.3

    def test_create_solar_wind_summary_zero_values(self):
        """Test creating a SolarWindSummary with zero values"""
        from noaa_goes.noaa_goes_producer.microsoft.opendata.us.noaa.swpc.solarwindsummary import SolarWindSummary

        summary = SolarWindSummary(
            timestamp="2024-01-01T00:00:00Z",
            wind_speed=0.0,
            bt=0.0,
            bz=0.0
        )

        assert summary.wind_speed == 0.0
        assert summary.bt == 0.0
        assert summary.bz == 0.0
