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
