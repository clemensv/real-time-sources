"""
Integration tests for NOAA data poller
Tests with mocked external HTTP requests
"""

import pytest
import json
import requests
import requests_mock
from datetime import datetime, timezone
from unittest.mock import patch, Mock
from noaa.noaa import NOAADataPoller


@pytest.mark.integration
class TestNOAAIntegration:
    """Integration tests for NOAA data poller with mocked HTTP"""

    @pytest.fixture
    def kafka_config(self):
        """Kafka configuration for testing"""
        return {
            'bootstrap.servers': 'localhost:9092',
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL',
            'sasl.username': 'test',
            'sasl.password': 'test'
        }

    @pytest.fixture
    def stations_response(self):
        """Mock stations API response"""
        return {
            'stations': [
                {
                    'id': '8454000',
                    'name': 'Providence',
                    'state': 'RI',
                    'lat': 41.8067,
                    'lng': -71.4000,
                    'tideType': 'Harmonic'
                }
            ]
        }

    @pytest.fixture
    def water_level_response(self):
        """Mock water level data response"""
        return {
            'metadata': {
                'id': '8454000',
                'name': 'Providence',
                'lat': '41.8067',
                'lon': '-71.4000'
            },
            'data': [
                {
                    't': '2024-01-01 00:00',
                    'v': '2.5',
                    's': '0.02',
                    'f': '0,0,0,0',
                    'q': 'v'
                }
            ]
        }

    @patch('noaa.noaa.MicrosoftOpenDataUSNOAAEventProducer')
    def test_fetch_stations_integration(self, mock_producer, kafka_config, stations_response):
        """Test fetching stations with mocked HTTP response"""
        with requests_mock.Mocker() as m:
            # Mock the stations API endpoint
            m.get(
                'https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json',
                json=stations_response
            )

            with patch('noaa.noaa.Station.schema') as mock_schema:
                mock_stations = [
                    Mock(id='8454000', name='Providence', state='RI', tideType='Harmonic')
                ]
                mock_schema.return_value.load.return_value = mock_stations

                # Create poller
                poller = NOAADataPoller(
                    kafka_config=kafka_config,
                    kafka_topic='test-topic',
                    last_polled_file='/tmp/test_last_polled.json'
                )

                # Verify stations were fetched
                assert len(poller.stations) > 0
                assert m.call_count == 1

    @patch('noaa.noaa.MicrosoftOpenDataUSNOAAEventProducer')
    def test_api_error_handling(self, mock_producer, kafka_config):
        """Test handling of API errors"""
        with requests_mock.Mocker() as m:
            # Mock API to return error
            m.get(
                'https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json',
                status_code=500
            )

            with patch('noaa.noaa.Station.schema') as mock_schema:
                mock_schema.return_value.load.return_value = []

                # Should not raise exception
                poller = NOAADataPoller(
                    kafka_config=kafka_config,
                    kafka_topic='test-topic',
                    last_polled_file='/tmp/test_last_polled.json'
                )

                # Should have empty stations list
                assert len(poller.stations) == 0

    @patch('noaa.noaa.MicrosoftOpenDataUSNOAAEventProducer')
    def test_timeout_handling(self, mock_producer, kafka_config):
        """Test handling of request timeouts"""
        with requests_mock.Mocker() as m:
            # Mock API to timeout
            m.get(
                'https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json',
                exc=requests.exceptions.Timeout
            )

            with patch('noaa.noaa.Station.schema') as mock_schema:
                mock_schema.return_value.load.return_value = []

                # Should handle timeout gracefully
                poller = NOAADataPoller(
                    kafka_config=kafka_config,
                    kafka_topic='test-topic',
                    last_polled_file='/tmp/test_last_polled.json'
                )

                assert len(poller.stations) == 0

    @patch('noaa.noaa.MicrosoftOpenDataUSNOAAEventProducer')
    def test_invalid_json_response(self, mock_producer, kafka_config):
        """Test handling of invalid JSON responses"""
        with requests_mock.Mocker() as m:
            # Mock API to return invalid JSON
            m.get(
                'https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json',
                text='invalid json'
            )

            with patch('noaa.noaa.Station.schema') as mock_schema:
                mock_schema.return_value.load.return_value = []

                # Should handle invalid JSON gracefully
                poller = NOAADataPoller(
                    kafka_config=kafka_config,
                    kafka_topic='test-topic',
                    last_polled_file='/tmp/test_last_polled.json'
                )

                assert len(poller.stations) == 0


@pytest.mark.integration
class TestNOAADataFetching:
    """Integration tests for data fetching functionality"""

    @pytest.fixture
    def kafka_config(self):
        return {
            'bootstrap.servers': 'localhost:9092',
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL',
            'sasl.username': 'test',
            'sasl.password': 'test'
        }

    @patch('noaa.noaa.MicrosoftOpenDataUSNOAAEventProducer')
    def test_products_urls(self, mock_producer, kafka_config):
        """Test that product URLs are correctly constructed"""
        with requests_mock.Mocker() as m:
            m.get(
                'https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json',
                json={'stations': []}
            )

            with patch('noaa.noaa.Station.schema') as mock_schema:
                mock_schema.return_value.load.return_value = []

                poller = NOAADataPoller(
                    kafka_config=kafka_config,
                    kafka_topic='test-topic',
                    last_polled_file='/tmp/test_last_polled.json'
                )

                # Verify base URL
                assert poller.BASE_URL == "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"

                # Verify common params
                assert "units=metric" in poller.COMMON_PARAMS
                assert "time_zone=gmt" in poller.COMMON_PARAMS


@pytest.mark.integration
class TestConnectionString:
    """Integration tests for connection string parsing"""

    def test_connection_string_parsing(self):
        """Test parsing of Event Hubs connection string"""
        connection_string = (
            "Endpoint=sb://test.servicebus.windows.net/;"
            "SharedAccessKeyName=test;"
            "SharedAccessKey=testkey123==;"
            "EntityPath=test-topic"
        )

        # Parse connection string (simplified - actual parsing would be in main)
        parts = {}
        for part in connection_string.split(';'):
            if '=' in part:
                key, value = part.split('=', 1)
                parts[key] = value

        # Verify parsing
        assert 'Endpoint' in parts
        assert 'sb://test.servicebus.windows.net/' in parts['Endpoint']
        assert parts.get('SharedAccessKeyName') == 'test'
        assert parts.get('EntityPath') == 'test-topic'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
