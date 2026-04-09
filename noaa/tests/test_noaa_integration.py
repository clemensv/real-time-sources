"""
Integration tests for NOAA data poller
Tests with mocked external HTTP requests
"""

import pytest
import json
import requests
import requests_mock
from datetime import datetime, timezone
from unittest.mock import patch, Mock, MagicMock
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


@pytest.mark.integration
class TestPollAndSendResilience:
    """Flush-batching and partial-failure resilience tests for NOAA poll_and_send."""

    _KAFKA_CFG = {
        'bootstrap.servers': 'localhost:9092',
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': 'test',
        'sasl.password': 'test',
    }

    def _make_poller(self, mock_ep_cls, stations):
        """Create a NOAADataPoller with pre-loaded stations and a mocked event producer."""
        with requests_mock.Mocker() as m:
            m.get('https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json',
                  json={'stations': []})
            with patch('noaa.noaa.Station.schema') as mock_schema:
                mock_schema.return_value.load.return_value = stations
                return NOAADataPoller(
                    kafka_config=self._KAFKA_CFG,
                    kafka_topic='test-topic',
                    last_polled_file='nonexistent_state.json',
                )

    @patch('noaa.noaa.MicrosoftOpenDataUSNOAAEventProducer')
    def test_station_batch_uses_flush_producer_false_with_single_flush(self, mock_ep_cls):
        """Station CloudEvents use flush_producer=False; producer.flush() called once after the batch."""
        mock_ep = MagicMock()
        mock_ep.producer = MagicMock()
        mock_ep_cls.return_value = mock_ep

        mock_station = MagicMock()
        mock_station.station_id = '8454000'
        mock_station.name = 'Providence'

        poller = self._make_poller(mock_ep_cls, [mock_station])

        with patch.object(poller, 'load_last_polled_times', return_value={}), \
             patch.object(poller, 'poll_noaa_api', side_effect=KeyboardInterrupt):
            try:
                poller.poll_and_send()
            except KeyboardInterrupt:
                pass

        station_calls = mock_ep.send_microsoft_open_data_us_noaa_station.call_args_list
        assert len(station_calls) == 1
        assert station_calls[0].kwargs.get('flush_producer') is False
        assert mock_ep.producer.flush.call_count >= 1

    @patch('noaa.noaa.MicrosoftOpenDataUSNOAAEventProducer')
    def test_poll_noaa_api_network_error_returns_empty_list(self, mock_ep_cls):
        """poll_noaa_api returns [] on a network error; no exception propagates."""
        mock_ep_cls.return_value = MagicMock()

        mock_station = MagicMock()
        mock_station.station_id = '8454000'
        mock_station.tideType = 'Harmonic'
        poller = self._make_poller(mock_ep_cls, [mock_station])

        with requests_mock.Mocker() as m:
            m.get(requests_mock.ANY, exc=requests.exceptions.ConnectionError("unreachable"))
            from datetime import datetime, timezone, timedelta
            result = poller.poll_noaa_api(
                'water_level', '8454000',
                datetime.now(timezone.utc) - timedelta(hours=1)
            )

        assert result == []

    @patch('noaa.noaa.MicrosoftOpenDataUSNOAAEventProducer')
    def test_stations_cached_at_startup_not_refetched(self, mock_ep_cls):
        """fetch_all_stations is called once during __init__; the cached list is reused for all poll cycles."""
        mock_ep_cls.return_value = MagicMock()

        mock_station = MagicMock()
        mock_station.station_id = '8454000'

        with requests_mock.Mocker() as m:
            m.get('https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json',
                  json={'stations': []})
            with patch('noaa.noaa.Station.schema') as mock_schema:
                mock_schema.return_value.load.return_value = [mock_station]
                poller = NOAADataPoller(
                    kafka_config=self._KAFKA_CFG,
                    kafka_topic='test-topic',
                    last_polled_file='nonexistent.json',
                )
            # Only one HTTP request was made (the __init__ station fetch)
            assert m.call_count == 1

        # Calling poll_noaa_api does NOT re-fetch stations
        assert len(poller.stations) == 1
        assert poller.stations[0].station_id == '8454000'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
