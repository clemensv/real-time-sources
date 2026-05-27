"""Integration tests for Ireland OPW waterlevel.ie bridge with mocked HTTP."""

import json
import pytest
import requests_mock
from unittest.mock import MagicMock, patch
from ireland_opw_waterlevel.ireland_opw_waterlevel import (
    fetch_geojson,
    extract_stations,
    extract_readings,
    emit_stations,
    emit_readings,
    dedup_key,
    FEED_URL,
)

import requests

# ---------------------------------------------------------------------------
# Sample GeoJSON response
# ---------------------------------------------------------------------------

SAMPLE_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": 1458,
            "properties": {
                "station_ref": "0000001041",
                "station_name": "Sandy Mills",
                "sensor_ref": "0001",
                "region_id": 3,
                "datetime": "2024-01-15T12:00:00Z",
                "value": "0.368",
                "err_code": 99,
            },
            "geometry": {"type": "Point", "coordinates": [-7.575758, 54.838318]}
        },
        {
            "type": "Feature",
            "id": 896,
            "properties": {
                "station_ref": "0000001041",
                "station_name": "Sandy Mills",
                "sensor_ref": "0002",
                "region_id": 3,
                "datetime": "2024-01-15T12:00:00Z",
                "value": "10.300",
                "err_code": 99,
            },
            "geometry": {"type": "Point", "coordinates": [-7.575758, 54.838318]}
        },
        {
            "type": "Feature",
            "id": 1460,
            "properties": {
                "station_ref": "0000001043",
                "station_name": "Ballybofey",
                "sensor_ref": "0001",
                "region_id": 3,
                "datetime": "2024-01-15T12:00:00Z",
                "value": "0.736",
                "err_code": 99,
            },
            "geometry": {"type": "Point", "coordinates": [-7.790749, 54.799769]}
        },
    ]
}


# ===========================================================================
# fetch_geojson tests
# ===========================================================================

@pytest.mark.integration
class TestFetchGeoJSON:
    """Test GeoJSON fetching with mocked HTTP."""

    def test_fetch_returns_features(self):
        session = requests.Session()
        with requests_mock.Mocker() as m:
            m.get(FEED_URL, json=SAMPLE_GEOJSON)
            features = fetch_geojson(session)
            assert len(features) == 3

    def test_fetch_timeout_raises(self):
        session = requests.Session()
        with requests_mock.Mocker() as m:
            m.get(FEED_URL, exc=requests.exceptions.ConnectTimeout)
            with pytest.raises(requests.exceptions.ConnectTimeout):
                fetch_geojson(session)

    def test_fetch_500_raises(self):
        session = requests.Session()
        with requests_mock.Mocker() as m:
            m.get(FEED_URL, status_code=500)
            with pytest.raises(requests.exceptions.HTTPError):
                fetch_geojson(session)

    def test_fetch_empty_collection(self):
        session = requests.Session()
        with requests_mock.Mocker() as m:
            m.get(FEED_URL, json={"type": "FeatureCollection", "features": []})
            features = fetch_geojson(session)
            assert features == []


# ===========================================================================
# emit_stations integration tests
# ===========================================================================

@pytest.mark.integration
class TestEmitStations:
    """Test station emission with mocked producer."""

    def test_emit_stations_calls_producer(self):
        mock_kafka_producer = MagicMock()
        mock_producer_client = MagicMock()
        stations = {
            "0000001041": {
                "station_ref": "0000001041",
                "station_name": "Sandy Mills",
                "region_id": 3,
                "longitude": -7.575758,
                "latitude": 54.838318,
            }
        }
        count = emit_stations(mock_producer_client, stations, mock_kafka_producer)
        assert count == 1
        mock_producer_client.send_ie_gov_opw_waterlevel_station.assert_called_once()
        mock_kafka_producer.flush.assert_called_once()

    def test_emit_multiple_stations(self):
        mock_kafka_producer = MagicMock()
        mock_producer_client = MagicMock()
        stations = {
            "0000001041": {
                "station_ref": "0000001041",
                "station_name": "Sandy Mills",
                "region_id": 3,
                "longitude": -7.575758,
                "latitude": 54.838318,
            },
            "0000001043": {
                "station_ref": "0000001043",
                "station_name": "Ballybofey",
                "region_id": 3,
                "longitude": -7.790749,
                "latitude": 54.799769,
            },
        }
        count = emit_stations(mock_producer_client, stations, mock_kafka_producer)
        assert count == 2
        assert mock_producer_client.send_ie_gov_opw_waterlevel_station.call_count == 2

    def test_emit_empty_stations(self):
        mock_kafka_producer = MagicMock()
        mock_producer_client = MagicMock()
        count = emit_stations(mock_producer_client, {}, mock_kafka_producer)
        assert count == 0
        mock_kafka_producer.flush.assert_called_once()


# ===========================================================================
# emit_readings integration tests
# ===========================================================================

@pytest.mark.integration
class TestEmitReadings:
    """Test reading emission with dedup."""

    def test_emit_readings_sends_new_readings(self):
        mock_kafka_producer = MagicMock()
        mock_producer_client = MagicMock()
        readings = [
            {
                "station_ref": "0000001041",
                "station_name": "Sandy Mills",
                "sensor_ref": "0001",
                "value": 0.368,
                "datetime": "2024-01-15T12:00:00Z",
                "err_code": 99,
            }
        ]
        seen = set()
        count = emit_readings(mock_producer_client, readings, seen, mock_kafka_producer)
        assert count == 1
        mock_producer_client.send_ie_gov_opw_waterlevel_water_level_reading.assert_called_once()

    def test_emit_readings_deduplicates(self):
        mock_kafka_producer = MagicMock()
        mock_producer_client = MagicMock()
        readings = [
            {
                "station_ref": "0000001041",
                "station_name": "Sandy Mills",
                "sensor_ref": "0001",
                "value": 0.368,
                "datetime": "2024-01-15T12:00:00Z",
                "err_code": 99,
            }
        ]
        seen = {"0000001041|0001|2024-01-15T12:00:00Z"}
        count = emit_readings(mock_producer_client, readings, seen, mock_kafka_producer)
        assert count == 0
        mock_producer_client.send_ie_gov_opw_waterlevel_water_level_reading.assert_not_called()

    def test_emit_readings_partial_dedup(self):
        mock_kafka_producer = MagicMock()
        mock_producer_client = MagicMock()
        readings = [
            {
                "station_ref": "0000001041",
                "station_name": "Sandy Mills",
                "sensor_ref": "0001",
                "value": 0.368,
                "datetime": "2024-01-15T12:00:00Z",
                "err_code": 99,
            },
            {
                "station_ref": "0000001041",
                "station_name": "Sandy Mills",
                "sensor_ref": "0002",
                "value": 10.3,
                "datetime": "2024-01-15T12:00:00Z",
                "err_code": 99,
            },
        ]
        # Only first reading already seen
        seen = {"0000001041|0001|2024-01-15T12:00:00Z"}
        count = emit_readings(mock_producer_client, readings, seen, mock_kafka_producer)
        assert count == 1

    def test_emit_readings_updates_seen_keys(self):
        mock_kafka_producer = MagicMock()
        mock_producer_client = MagicMock()
        readings = [
            {
                "station_ref": "0000001041",
                "station_name": "Sandy Mills",
                "sensor_ref": "0001",
                "value": 0.368,
                "datetime": "2024-01-15T12:00:00Z",
                "err_code": 99,
            }
        ]
        seen = set()
        emit_readings(mock_producer_client, readings, seen, mock_kafka_producer)
        assert "0000001041|0001|2024-01-15T12:00:00Z" in seen

    def test_emit_readings_null_value(self):
        mock_kafka_producer = MagicMock()
        mock_producer_client = MagicMock()
        readings = [
            {
                "station_ref": "0000001041",
                "station_name": "Sandy Mills",
                "sensor_ref": "0001",
                "value": None,
                "datetime": "2024-01-15T12:00:00Z",
                "err_code": 0,
            }
        ]
        seen = set()
        count = emit_readings(mock_producer_client, readings, seen, mock_kafka_producer)
        assert count == 1


# ===========================================================================
# Full pipeline integration test
# ===========================================================================

@pytest.mark.integration
class TestFullPipeline:
    """Test the full fetch → extract → emit pipeline with mocked HTTP and producer."""

    def test_fetch_extract_emit_pipeline(self):
        session = requests.Session()
        mock_kafka_producer = MagicMock()
        mock_producer_client = MagicMock()

        with requests_mock.Mocker() as m:
            m.get(FEED_URL, json=SAMPLE_GEOJSON)
            features = fetch_geojson(session)

        stations = extract_stations(features)
        assert len(stations) == 2

        readings = extract_readings(features)
        assert len(readings) == 3

        n_stations = emit_stations(mock_producer_client, stations, mock_kafka_producer)
        assert n_stations == 2

        seen = set()
        n_readings = emit_readings(mock_producer_client, readings, seen, mock_kafka_producer)
        assert n_readings == 3

    def test_second_poll_deduplicates(self):
        mock_kafka_producer = MagicMock()
        mock_producer_client = MagicMock()
        session = requests.Session()

        with requests_mock.Mocker() as m:
            m.get(FEED_URL, json=SAMPLE_GEOJSON)
            features = fetch_geojson(session)

        readings = extract_readings(features)
        seen = set()
        n1 = emit_readings(mock_producer_client, readings, seen, mock_kafka_producer)
        assert n1 == 3

        # Second poll with same data should emit nothing new
        n2 = emit_readings(mock_producer_client, readings, seen, mock_kafka_producer)
        assert n2 == 0
