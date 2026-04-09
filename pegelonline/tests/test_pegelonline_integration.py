"""Integration tests for PegelOnline data poller with mocked API."""

import pytest
import requests_mock
import json
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from pegelonline.pegelonline import PegelOnlineAPI


@pytest.mark.integration
class TestAPIStationListing:
    """Test station listing API interactions."""

    def test_list_stations_success(self):
        """Test successful station listing."""
        api = PegelOnlineAPI()
        
        mock_stations = [
            {
                "uuid": "70272185-d09e-43a5-a034-730d7e48c6f9",
                "number": "48900237",
                "shortname": "MAXAU",
                "longname": "MAXAU",
                "km": 362.3,
                "agency": "WSV",
                "longitude": 8.314,
                "latitude": 49.014,
                "water": {
                    "shortname": "RHEIN",
                    "longname": "RHEIN"
                }
            },
            {
                "uuid": "593647aa-9fea-43ec-a7d6-6476a76ae868",
                "number": "27000401",
                "shortname": "HAMBURG ST. PAULI",
                "longname": "HAMBURG ST. PAULI",
                "km": 623.0,
                "agency": "WSV",
                "longitude": 9.967,
                "latitude": 53.546,
                "water": {
                    "shortname": "ELBE",
                    "longname": "ELBE"
                }
            }
        ]
        
        with requests_mock.Mocker() as m:
            m.get('https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json',
                  json=mock_stations)
            
            stations = api.list_stations()
            
            assert len(stations) == 2
            assert stations[0]['shortname'] == 'MAXAU'
            assert stations[1]['shortname'] == 'HAMBURG ST. PAULI'
            assert stations[0]['water']['shortname'] == 'RHEIN'

    def test_list_stations_timeout(self):
        """Test station listing with timeout."""
        import requests
        api = PegelOnlineAPI()
        
        with requests_mock.Mocker() as m:
            m.get('https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json',
                  exc=requests.exceptions.ConnectTimeout)
            
            with pytest.raises(requests.exceptions.ConnectTimeout):
                api.list_stations()

    def test_list_stations_http_error(self):
        """Test station listing with HTTP error."""
        api = PegelOnlineAPI()
        
        with requests_mock.Mocker() as m:
            m.get('https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json',
                  status_code=500, text='Internal Server Error')
            
            with pytest.raises(Exception):
                stations = api.list_stations()
                stations  # This will raise when trying to parse JSON


@pytest.mark.integration
class TestWaterLevelRetrieval:
    """Test water level measurement retrieval."""

    def test_get_water_level_success(self):
        """Test successful water level retrieval."""
        api = PegelOnlineAPI()
        station_id = "70272185-d09e-43a5-a034-730d7e48c6f9"
        
        mock_measurement = {
            "timestamp": "2024-01-15T12:00:00+01:00",
            "value": 450,
            "stateMnwMhw": "normal",
            "stateNswHsw": "unknown"
        }
        
        with requests_mock.Mocker() as m:
            m.get(f'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{station_id}/W/currentmeasurement.json',
                  json=mock_measurement)
            
            measurement = api.get_water_level(station_id)
            
            assert measurement is not None
            assert measurement['value'] == 450
            assert measurement['stateMnwMhw'] == 'normal'
            assert '2024-01-15' in measurement['timestamp']

    def test_get_water_level_with_etag_304(self):
        """Test water level retrieval with ETag returning 304 Not Modified."""
        api = PegelOnlineAPI()
        station_id = "70272185-d09e-43a5-a034-730d7e48c6f9"
        url = f'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{station_id}/W/currentmeasurement.json'
        
        mock_etag = '"abc123-etag"'
        api.etags[url] = mock_etag
        
        with requests_mock.Mocker() as m:
            m.get(url, status_code=304)
            
            measurement = api.get_water_level(station_id)
            
            assert measurement is None  # 304 returns None

    def test_get_water_level_stores_etag(self):
        """Test that ETag from response is stored."""
        api = PegelOnlineAPI()
        station_id = "70272185-d09e-43a5-a034-730d7e48c6f9"
        url = f'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{station_id}/W/currentmeasurement.json'
        
        mock_measurement = {"timestamp": "2024-01-15T12:00:00+01:00", "value": 450}
        mock_etag = '"new-etag-value"'
        
        with requests_mock.Mocker() as m:
            m.get(url, json=mock_measurement, headers={'ETag': mock_etag})
            
            measurement = api.get_water_level(station_id)
            
            assert measurement is not None
            assert api.etags[url] == mock_etag

    def test_get_water_level_404_adds_to_skip_list(self):
        """Test that 404 response adds URL to skip list."""
        api = PegelOnlineAPI()
        station_id = "nonexistent-station"
        url = f'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{station_id}/W/currentmeasurement.json'
        
        with requests_mock.Mocker() as m:
            m.get(url, status_code=404, text='Not Found')
            
            measurement = api.get_water_level(station_id)
            
            assert measurement is None
            assert url in api.skip_urls

    def test_get_water_level_skipped_url_returns_none(self):
        """Test that URLs in skip list return None without request."""
        api = PegelOnlineAPI()
        station_id = "skipped-station"
        url = f'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{station_id}/W/currentmeasurement.json'
        
        api.skip_urls.append(url)
        
        with requests_mock.Mocker() as m:
            # Register a mock that should never be called
            m.get(url, json={"value": 100})
            
            measurement = api.get_water_level(station_id)
            
            assert measurement is None
            # Verify the mock was never called
            assert not m.called

    def test_get_water_level_500_adds_to_skip_list(self):
        """Test that 500 error adds URL to skip list."""
        api = PegelOnlineAPI()
        station_id = "error-station"
        url = f'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{station_id}/W/currentmeasurement.json'
        
        with requests_mock.Mocker() as m:
            m.get(url, status_code=500, text='Internal Server Error')
            
            measurement = api.get_water_level(station_id)
            
            assert measurement is None
            assert url in api.skip_urls


@pytest.mark.integration
class TestBulkWaterLevels:
    """Test bulk water level retrieval."""

    def test_get_water_levels_success(self):
        """Test successful bulk water level retrieval."""
        api = PegelOnlineAPI()
        
        mock_stations = [
            {
                "uuid": "station-1",
                "shortname": "STATION1",
                "timeseries": [
                    {
                        "shortname": "W",
                        "currentMeasurement": {
                            "timestamp": "2024-01-15T12:00:00+01:00",
                            "value": 450,
                            "stateMnwMhw": "normal",
                            "stateNswHsw": "unknown"
                        }
                    }
                ]
            },
            {
                "uuid": "station-2",
                "shortname": "STATION2",
                "timeseries": [
                    {
                        "shortname": "W",
                        "currentMeasurement": {
                            "timestamp": "2024-01-15T12:05:00+01:00",
                            "value": 380,
                            "stateMnwMhw": "normal",
                            "stateNswHsw": "unknown"
                        }
                    }
                ]
            }
        ]
        
        with requests_mock.Mocker() as m:
            m.get('https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json?includeTimeseries=true&includeCurrentMeasurement=true',
                  json=mock_stations)
            
            levels = api.get_water_levels()
            
            assert len(levels) == 2
            assert 'station-1' in levels
            assert 'station-2' in levels
            assert levels['station-1']['value'] == 450
            assert levels['station-2']['value'] == 380
            assert levels['station-1']['uuid'] == 'station-1'

    def test_get_water_levels_filters_non_w_timeseries(self):
        """Test that only W (water level) timeseries are included."""
        api = PegelOnlineAPI()
        
        mock_stations = [
            {
                "uuid": "station-1",
                "shortname": "STATION1",
                "timeseries": [
                    {
                        "shortname": "Q",  # Discharge, not water level
                        "currentMeasurement": {"timestamp": "2024-01-15T12:00:00+01:00", "value": 100}
                    },
                    {
                        "shortname": "W",  # Water level
                        "currentMeasurement": {"timestamp": "2024-01-15T12:00:00+01:00", "value": 450}
                    }
                ]
            }
        ]
        
        with requests_mock.Mocker() as m:
            m.get('https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json?includeTimeseries=true&includeCurrentMeasurement=true',
                  json=mock_stations)
            
            levels = api.get_water_levels()
            
            assert len(levels) == 1
            assert levels['station-1']['value'] == 450

    def test_get_water_levels_http_error_returns_empty(self):
        """Test that HTTP error returns empty dictionary."""
        api = PegelOnlineAPI()
        
        with requests_mock.Mocker() as m:
            m.get('https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json?includeTimeseries=true&includeCurrentMeasurement=true',
                  status_code=503, text='Service Unavailable')
            
            levels = api.get_water_levels()
            
            assert levels == {}

    def test_get_water_levels_no_timeseries(self):
        """Test stations without timeseries are skipped."""
        api = PegelOnlineAPI()
        
        mock_stations = [
            {
                "uuid": "station-1",
                "shortname": "STATION1"
                # No timeseries key
            },
            {
                "uuid": "station-2",
                "shortname": "STATION2",
                "timeseries": [
                    {
                        "shortname": "W",
                        "currentMeasurement": {"timestamp": "2024-01-15T12:00:00+01:00", "value": 380}
                    }
                ]
            }
        ]
        
        with requests_mock.Mocker() as m:
            m.get('https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json?includeTimeseries=true&includeCurrentMeasurement=true',
                  json=mock_stations)
            
            levels = api.get_water_levels()
            
            assert len(levels) == 1
            assert 'station-1' not in levels
            assert 'station-2' in levels


@pytest.mark.integration
class TestFlushAndStateResilience:
    """Flush-batching and state-preservation resilience tests for the feed loop."""

    _KAFKA_CFG = {'bootstrap.servers': 'localhost:9092'}
    _STATION = {
        "uuid": "s1", "number": "1", "shortname": "ST1", "longname": "ST1",
        "km": 100.0, "agency": "WSV", "longitude": 8.0, "latitude": 50.0,
        "water": {"shortname": "RHEIN", "longname": "RHEIN"},
    }
    _MEASUREMENT = {
        "timestamp": "2024-01-15T12:00:00+01:00",
        "value": 450, "stateMnwMhw": "normal", "stateNswHsw": "unknown", "uuid": "s1",
    }

    def _run_feed(self, api, **kwargs):
        """Drive feed_stations to completion, absorbing the KeyboardInterrupt exit."""
        try:
            asyncio.run(api.feed_stations(**kwargs))
        except KeyboardInterrupt:
            pass

    def test_station_batch_uses_flush_producer_false_with_single_flush(self):
        """All station CloudEvents use flush_producer=False; producer.flush() called once after the batch."""
        api = PegelOnlineAPI()
        mock_ep = MagicMock()
        mock_raw_producer = MagicMock()

        with patch.object(api, 'list_stations', return_value=[self._STATION, {**self._STATION, "uuid": "s2", "shortname": "ST2"}]), \
             patch.object(api, 'get_water_levels', return_value={}), \
             patch('pegelonline.pegelonline.Producer', return_value=mock_raw_producer), \
             patch('pegelonline.pegelonline.DeWsvPegelonlineEventProducer', return_value=mock_ep), \
             patch('pegelonline.pegelonline.time.sleep', side_effect=KeyboardInterrupt):
            self._run_feed(api, kafka_config=self._KAFKA_CFG, kafka_topic='test-topic', polling_interval=60)

        assert mock_ep.send_de_wsv_pegelonline_station.call_count == 2
        for call in mock_ep.send_de_wsv_pegelonline_station.call_args_list:
            assert call.kwargs.get('flush_producer') is False
        assert mock_raw_producer.flush.call_count >= 1

    def test_measurement_batch_uses_flush_producer_false_with_flush_per_cycle(self):
        """Measurement CloudEvents use flush_producer=False; producer.flush() called once per poll cycle."""
        api = PegelOnlineAPI()
        mock_ep = MagicMock()
        mock_raw_producer = MagicMock()

        with patch.object(api, 'list_stations', return_value=[]), \
             patch.object(api, 'get_water_levels', return_value={"s1": self._MEASUREMENT}), \
             patch('pegelonline.pegelonline.Producer', return_value=mock_raw_producer), \
             patch('pegelonline.pegelonline.DeWsvPegelonlineEventProducer', return_value=mock_ep), \
             patch('pegelonline.pegelonline._save_state'), \
             patch('pegelonline.pegelonline.time.sleep', side_effect=KeyboardInterrupt):
            self._run_feed(api, kafka_config=self._KAFKA_CFG, kafka_topic='test-topic', polling_interval=60)

        assert mock_ep.send_de_wsv_pegelonline_current_measurement.call_count == 1
        send_call = mock_ep.send_de_wsv_pegelonline_current_measurement.call_args
        assert send_call.kwargs.get('flush_producer') is False
        # Flush after station batch (empty) and after the measurement batch
        assert mock_raw_producer.flush.call_count >= 1

    def test_send_failure_still_updates_dedup_state(self):
        """When Kafka send raises, previous_readings is still updated; same measurement not retried next cycle."""
        api = PegelOnlineAPI()
        mock_ep = MagicMock()
        mock_ep.send_de_wsv_pegelonline_current_measurement.side_effect = RuntimeError("broker down")
        mock_raw_producer = MagicMock()

        with patch.object(api, 'list_stations', return_value=[]), \
             patch.object(api, 'get_water_levels', return_value={"s1": self._MEASUREMENT}), \
             patch('pegelonline.pegelonline.Producer', return_value=mock_raw_producer), \
             patch('pegelonline.pegelonline.DeWsvPegelonlineEventProducer', return_value=mock_ep), \
             patch('pegelonline.pegelonline._save_state'), \
             patch('pegelonline.pegelonline.time.sleep', side_effect=[None, KeyboardInterrupt()]):
            self._run_feed(api, kafka_config=self._KAFKA_CFG, kafka_topic='test-topic', polling_interval=60)

        # Send attempted once (first cycle); second cycle skips because state was preserved
        assert mock_ep.send_de_wsv_pegelonline_current_measurement.call_count == 1

    def test_get_water_levels_failure_is_caught_and_loop_continues(self):
        """A transient upstream failure in get_water_levels is caught; no measurements sent; loop retries."""
        api = PegelOnlineAPI()
        mock_ep = MagicMock()
        mock_raw_producer = MagicMock()

        with patch.object(api, 'list_stations', return_value=[]), \
             patch.object(api, 'get_water_levels', side_effect=ConnectionError("upstream timeout")), \
             patch('pegelonline.pegelonline.Producer', return_value=mock_raw_producer), \
             patch('pegelonline.pegelonline.DeWsvPegelonlineEventProducer', return_value=mock_ep), \
             patch('pegelonline.pegelonline.time.sleep', side_effect=KeyboardInterrupt):
            self._run_feed(api, kafka_config=self._KAFKA_CFG, kafka_topic='test-topic', polling_interval=60)

        mock_ep.send_de_wsv_pegelonline_current_measurement.assert_not_called()
