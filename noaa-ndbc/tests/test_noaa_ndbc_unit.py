"""
Unit tests for NOAA NDBC Buoy Observations poller.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from noaa_ndbc.noaa_ndbc import NDBCBuoyPoller, parse_connection_string, parse_float


SAMPLE_OBS_TEXT = """\
#STN     LAT      LON  YYYY MM DD hh mm WDIR WSPD  GST  WVHT   DPD   APD MWD   PRES  PTDY  ATMP  WTMP  DEWP  VIS  TIDE
#        deg      deg   yr mo da hr mn  deg  m/s  m/s    m    sec   sec deg    hPa   hPa  degC  degC  degC   nmi    ft
41001  34.700  -72.700 2024 06 15 14 50 210  8.2 10.3   1.5   7.1   5.2 200 1015.2  -1.2  22.3  24.1  18.5   MM   MM
41002  32.300  -75.200 2024 06 15 14 50 180  5.1  6.8   0.8   8.0   4.5 190 1016.0   0.3  23.1  25.5  20.2   MM   MM
BURL1  28.900  -89.400 2024 06 15 14 50  MM   MM   MM    MM    MM    MM  MM 1014.5    MM  28.7  29.3    MM   MM   MM
"""


@pytest.mark.unit
class TestParsFloat:
    """Unit tests for the parse_float helper"""

    def test_parse_valid_float(self):
        assert parse_float("10.5") == 10.5

    def test_parse_integer(self):
        assert parse_float("42") == 42.0

    def test_parse_mm_returns_none(self):
        assert parse_float("MM") is None

    def test_parse_empty_returns_none(self):
        assert parse_float("") is None

    def test_parse_none_returns_none(self):
        assert parse_float(None) is None

    def test_parse_negative(self):
        assert parse_float("-3.2") == -3.2

    def test_parse_whitespace_mm(self):
        assert parse_float("  MM  ") is None


@pytest.mark.unit
class TestNDBCBuoyPoller:
    """Unit tests for the NDBCBuoyPoller class"""

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

    @patch('noaa_ndbc.noaa_ndbc.MicrosoftOpenDataUSNOAANDBCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_init(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test NDBCBuoyPoller initialization"""
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer

        poller = NDBCBuoyPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == temp_state_file
        mock_producer_class.assert_called_once_with(mock_kafka_config)
        mock_event_producer.assert_called_once_with(mock_kafka_producer, 'test-topic')

    @patch('noaa_ndbc.noaa_ndbc.MicrosoftOpenDataUSNOAANDBCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_state_empty(self, mock_producer_class, mock_event_producer, mock_kafka_config):
        """Test loading state when no state file exists"""
        poller = NDBCBuoyPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file='/tmp/nonexistent_ndbc_state.json'
        )

        state = poller.load_state()
        assert state == {"last_timestamps": {}}

    @patch('noaa_ndbc.noaa_ndbc.MicrosoftOpenDataUSNOAANDBCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_state_existing(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test loading state from existing state file"""
        state_data = {"last_timestamps": {"41001": "2024-06-15T14:50:00+00:00", "41002": "2024-06-15T14:50:00+00:00"}}
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f)

        poller = NDBCBuoyPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        state = poller.load_state()
        assert state["last_timestamps"]["41001"] == "2024-06-15T14:50:00+00:00"

    @patch('noaa_ndbc.noaa_ndbc.MicrosoftOpenDataUSNOAANDBCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_save_state(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test saving state to state file"""
        poller = NDBCBuoyPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        state_data = {"last_timestamps": {"41001": "2024-06-15T14:50:00+00:00"}}
        poller.save_state(state_data)

        with open(temp_state_file, 'r', encoding='utf-8') as f:
            saved = json.load(f)
        assert saved["last_timestamps"]["41001"] == "2024-06-15T14:50:00+00:00"

    @patch('noaa_ndbc.noaa_ndbc.MicrosoftOpenDataUSNOAANDBCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_parse_observations(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test parsing fixed-width observation text"""
        poller = NDBCBuoyPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        observations = poller.parse_observations(SAMPLE_OBS_TEXT)

        assert len(observations) == 3

        # Check first observation (41001) with full data
        obs1 = observations[0]
        assert obs1.station_id == "41001"
        assert obs1.latitude == 34.700
        assert obs1.longitude == -72.700
        assert obs1.timestamp == "2024-06-15T14:50:00+00:00"
        assert obs1.wind_direction == 210.0
        assert obs1.wind_speed == 8.2
        assert obs1.gust == 10.3
        assert obs1.wave_height == 1.5
        assert obs1.dominant_wave_period == 7.1
        assert obs1.average_wave_period == 5.2
        assert obs1.mean_wave_direction == 200.0
        assert obs1.pressure == 1015.2
        assert obs1.air_temperature == 22.3
        assert obs1.water_temperature == 24.1
        assert obs1.dewpoint == 18.5

        # Check second observation
        obs2 = observations[1]
        assert obs2.station_id == "41002"
        assert obs2.latitude == 32.300

    @patch('noaa_ndbc.noaa_ndbc.MicrosoftOpenDataUSNOAANDBCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_parse_observations_mm_handling(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test that MM (missing measurement) values are handled correctly"""
        poller = NDBCBuoyPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        observations = poller.parse_observations(SAMPLE_OBS_TEXT)

        # Third observation (BURL1) has many MM values
        obs3 = observations[2]
        assert obs3.station_id == "BURL1"
        assert obs3.latitude == 28.900
        assert obs3.longitude == -89.400
        # MM values should be converted to 0.0
        assert obs3.wind_direction == 0.0
        assert obs3.wind_speed == 0.0
        assert obs3.gust == 0.0
        assert obs3.wave_height == 0.0
        assert obs3.pressure == 1014.5  # This one has a value
        assert obs3.air_temperature == 28.7  # This one has a value
        assert obs3.water_temperature == 29.3  # This one has a value
        assert obs3.dewpoint == 0.0  # MM

    @patch('noaa_ndbc.noaa_ndbc.MicrosoftOpenDataUSNOAANDBCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_parse_observations_empty_text(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test parsing empty text returns empty list"""
        poller = NDBCBuoyPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        observations = poller.parse_observations("")
        assert observations == []

    @patch('noaa_ndbc.noaa_ndbc.MicrosoftOpenDataUSNOAANDBCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_parse_observations_header_only(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test parsing text with only headers returns empty list"""
        header_only = """\
#STN     LAT      LON  YYYY MM DD hh mm WDIR WSPD  GST  WVHT   DPD   APD MWD   PRES  PTDY  ATMP  WTMP  DEWP  VIS  TIDE
#        deg      deg   yr mo da hr mn  deg  m/s  m/s    m    sec   sec deg    hPa   hPa  degC  degC  degC   nmi    ft
"""
        poller = NDBCBuoyPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        observations = poller.parse_observations(header_only)
        assert observations == []

    @patch('noaa_ndbc.noaa_ndbc.requests.get')
    @patch('noaa_ndbc.noaa_ndbc.MicrosoftOpenDataUSNOAANDBCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_observations_success(self, mock_producer_class, mock_event_producer, mock_get, mock_kafka_config, temp_state_file):
        """Test polling observations successfully"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.text = SAMPLE_OBS_TEXT
        mock_get.return_value = mock_response

        poller = NDBCBuoyPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        observations = poller.poll_observations()
        assert len(observations) == 3
        mock_get.assert_called_once_with(NDBCBuoyPoller.LATEST_OBS_URL, timeout=60)

    @patch('noaa_ndbc.noaa_ndbc.requests.get')
    @patch('noaa_ndbc.noaa_ndbc.MicrosoftOpenDataUSNOAANDBCEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_observations_failure(self, mock_producer_class, mock_event_producer, mock_get, mock_kafka_config, temp_state_file):
        """Test polling observations handles HTTP errors"""
        mock_get.side_effect = Exception("Network error")

        poller = NDBCBuoyPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )

        observations = poller.poll_observations()
        assert observations == []


@pytest.mark.unit
class TestParseConnectionString:
    """Unit tests for connection string parsing"""

    def test_parse_valid_connection_string(self):
        conn_str = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=mykey;SharedAccessKey=abc123;EntityPath=myhub"
        result = parse_connection_string(conn_str)

        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'myhub'
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == conn_str

    def test_parse_connection_string_password(self):
        conn_str = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=TestKey123;EntityPath=test-topic"
        result = parse_connection_string(conn_str)

        assert result['sasl.password'] == conn_str
        assert result['sasl.username'] == '$ConnectionString'
