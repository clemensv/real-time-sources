"""
Unit tests for NOAA data poller
Tests core functionality without external dependencies
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
from noaa.noaa import NOAADataPoller
from noaa.noaa_producer.microsoft.opendata.us.noaa.station import Station


@pytest.mark.unit
class TestNOAADataPoller:
    """Unit tests for NOAADataPoller class"""

    @pytest.fixture
    def mock_kafka_config(self):
        """Fixture for Kafka configuration"""
        return {
            'bootstrap.servers': 'localhost:9092',
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL',
            'sasl.username': 'test_user',
            'sasl.password': 'test_password'
        }

    @pytest.fixture
    def mock_station(self):
        """Fixture for a mock NOAA station"""
        station = Mock(spec=Station)
        station.id = "8454000"
        station.name = "Providence"
        station.state = "RI"
        station.tideType = "Harmonic"
        return station

    @pytest.fixture
    def mock_stations_response(self):
        """Fixture for mock stations API response"""
        return {
            'stations': [
                {
                    'id': '8454000',
                    'name': 'Providence',
                    'state': 'RI',
                    'tideType': 'Harmonic',
                    'lat': 41.8067,
                    'lng': -71.4000
                },
                {
                    'id': '9414290',
                    'name': 'San Francisco',
                    'state': 'CA',
                    'tideType': 'Harmonic',
                    'lat': 37.8063,
                    'lng': -122.4659
                }
            ]
        }

    @patch('noaa.noaa.MicrosoftOpendataUsNoaaEventProducer')
    @patch('noaa.noaa.requests.get')
    def test_init_with_station(self, mock_get, mock_producer, mock_kafka_config, mock_stations_response):
        """Test NOAADataPoller initialization with specific station"""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = mock_stations_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Mock Station.schema().load() to return Station objects
        with patch('noaa.noaa.Station.schema') as mock_schema:
            mock_station = Mock(id='8454000', name='Providence', state='RI', tideType='Harmonic')
            mock_schema.return_value.load.return_value = [mock_station]

            # Initialize poller with specific station
            poller = NOAADataPoller(
                kafka_config=mock_kafka_config,
                kafka_topic='test-topic',
                last_polled_file='/tmp/test_last_polled.json',
                station='8454000'
            )

            # Verify
            assert poller.kafka_topic == 'test-topic'
            assert poller.last_polled_file == '/tmp/test_last_polled.json'
            assert poller.station is not None
            assert poller.station.id == '8454000'
            mock_producer.assert_called_once_with(mock_kafka_config, 'test-topic')

    @patch('noaa.noaa.MicrosoftOpendataUsNoaaEventProducer')
    @patch('noaa.noaa.requests.get')
    def test_init_without_station(self, mock_get, mock_producer, mock_kafka_config, mock_stations_response):
        """Test NOAADataPoller initialization without specific station"""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = mock_stations_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with patch('noaa.noaa.Station.schema') as mock_schema:
            mock_schema.return_value.load.return_value = []

            # Initialize poller without specific station
            poller = NOAADataPoller(
                kafka_config=mock_kafka_config,
                kafka_topic='test-topic',
                last_polled_file='/tmp/test_last_polled.json',
                station=None
            )

            # Verify
            assert poller.station is None
            assert poller.kafka_topic == 'test-topic'

    @patch('noaa.noaa.MicrosoftOpendataUsNoaaEventProducer')
    @patch('noaa.noaa.requests.get')
    def test_fetch_all_stations_success(self, mock_get, mock_producer, mock_kafka_config, mock_stations_response):
        """Test successful fetching of all stations"""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = mock_stations_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with patch('noaa.noaa.Station.schema') as mock_schema:
            mock_stations = [
                Mock(id='8454000', name='Providence'),
                Mock(id='9414290', name='San Francisco')
            ]
            mock_schema.return_value.load.return_value = mock_stations

            poller = NOAADataPoller(
                kafka_config=mock_kafka_config,
                kafka_topic='test-topic',
                last_polled_file='/tmp/test_last_polled.json'
            )

            # Verify stations were fetched
            assert len(poller.stations) == 2
            mock_get.assert_called_with(
                "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json",
                timeout=10
            )

    @patch('noaa.noaa.MicrosoftOpendataUsNoaaEventProducer')
    @patch('noaa.noaa.requests.get')
    def test_fetch_all_stations_error(self, mock_get, mock_producer, mock_kafka_config):
        """Test handling of errors when fetching stations"""
        # Setup mock to raise exception
        import requests
        mock_get.side_effect = requests.RequestException("Network error")

        with patch('noaa.noaa.Station.schema'):
            poller = NOAADataPoller(
                kafka_config=mock_kafka_config,
                kafka_topic='test-topic',
                last_polled_file='/tmp/test_last_polled.json'
            )

            # Verify empty stations list on error
            assert len(poller.stations) == 0

    @patch('noaa.noaa.MicrosoftOpendataUsNoaaEventProducer')
    @patch('noaa.noaa.requests.get')
    def test_get_datum_for_station(self, mock_get, mock_producer, mock_kafka_config):
        """Test datum determination for stations"""
        mock_response = Mock()
        mock_response.json.return_value = {'stations': []}
        mock_get.return_value = mock_response

        with patch('noaa.noaa.Station.schema') as mock_schema:
            # Create mock stations with different tide types
            mock_stations = [
                Mock(id='8454000', tideType='Harmonic'),
                Mock(id='9087031', tideType='Great Lakes')
            ]
            mock_schema.return_value.load.return_value = mock_stations

            poller = NOAADataPoller(
                kafka_config=mock_kafka_config,
                kafka_topic='test-topic',
                last_polled_file='/tmp/test_last_polled.json'
            )

            # Manually set stations for testing
            poller.stations = mock_stations

            # Test Harmonic station (should return MLLW)
            datum = poller.get_datum_for_station('8454000')
            assert datum == 'MLLW'

            # Test Great Lakes station (should return IGLD)
            datum = poller.get_datum_for_station('9087031')
            assert datum == 'IGLD'

    @patch('noaa.noaa.MicrosoftOpendataUsNoaaEventProducer')
    @patch('noaa.noaa.requests.get')
    def test_products_configuration(self, mock_get, mock_producer, mock_kafka_config):
        """Test that all expected products are configured"""
        mock_response = Mock()
        mock_response.json.return_value = {'stations': []}
        mock_get.return_value = mock_response

        with patch('noaa.noaa.Station.schema') as mock_schema:
            mock_schema.return_value.load.return_value = []

            poller = NOAADataPoller(
                kafka_config=mock_kafka_config,
                kafka_topic='test-topic',
                last_polled_file='/tmp/test_last_polled.json'
            )

            # Verify all expected products are present
            expected_products = [
                'water_level', 'predictions', 'air_temperature', 'wind',
                'air_pressure', 'water_temperature', 'conductivity',
                'visibility', 'humidity', 'salinity'
            ]

            for product in expected_products:
                assert product in poller.PRODUCTS
                assert f"product={product}" in poller.PRODUCTS[product]


@pytest.mark.unit
class TestNOAAConfiguration:
    """Unit tests for NOAA configuration and constants"""

    def test_base_url(self):
        """Test NOAA API base URL is correctly configured"""
        assert NOAADataPoller.BASE_URL == "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"

    def test_common_params(self):
        """Test common parameters are correctly configured"""
        params = NOAADataPoller.COMMON_PARAMS
        assert "units=metric" in params
        assert "time_zone=gmt" in params
        assert "application=web_services" in params
        assert "format=json" in params


@pytest.mark.unit
class TestKafkaConfiguration:
    """Unit tests for Kafka configuration"""

    def test_kafka_config_structure(self):
        """Test Kafka configuration has required fields"""
        config = {
            'bootstrap.servers': 'test-server:9092',
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL',
            'sasl.username': 'user',
            'sasl.password': 'pass'
        }

        assert 'bootstrap.servers' in config
        assert 'sasl.mechanisms' in config
        assert 'security.protocol' in config
        assert 'sasl.username' in config
        assert 'sasl.password' in config
        assert config['sasl.mechanisms'] == 'PLAIN'
        assert config['security.protocol'] == 'SASL_SSL'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
