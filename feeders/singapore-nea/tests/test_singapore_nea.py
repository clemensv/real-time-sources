"""Unit tests for Singapore NEA Weather Observation Bridge."""

import json
import pytest
from unittest.mock import MagicMock, patch, call
from datetime import datetime, timezone

from singapore_nea.singapore_nea import (
    NEAWeatherAPI,
    merge_observations,
    parse_connection_string,
    send_stations,
    feed_observations,
    _load_state,
    _save_state,
    FIELD_MAP,
)


SAMPLE_TEMP_RESPONSE = {
    "metadata": {
        "stations": [
            {"id": "S109", "device_id": "S109", "name": "Ang Mo Kio Avenue 5",
             "location": {"latitude": 1.3764, "longitude": 103.8492}},
            {"id": "S50", "device_id": "S50", "name": "Clementi Road",
             "location": {"latitude": 1.3337, "longitude": 103.7768}},
        ]
    },
    "items": [
        {
            "timestamp": "2026-04-07T15:39:00+08:00",
            "readings": [
                {"station_id": "S109", "value": 25.6},
                {"station_id": "S50", "value": 26.1},
            ]
        }
    ],
    "api_info": {"status": "healthy"},
}

SAMPLE_RAIN_RESPONSE = {
    "metadata": {
        "stations": [
            {"id": "S109", "device_id": "S109", "name": "Ang Mo Kio Avenue 5",
             "location": {"latitude": 1.3764, "longitude": 103.8492}},
            {"id": "S77", "device_id": "S77", "name": "Upper Peirce Reservoir",
             "location": {"latitude": 1.378, "longitude": 103.805}},
        ]
    },
    "items": [
        {
            "timestamp": "2026-04-07T15:35:00+08:00",
            "readings": [
                {"station_id": "S109", "value": 0.0},
                {"station_id": "S77", "value": 1.2},
            ]
        }
    ],
    "api_info": {"status": "healthy"},
}

EMPTY_RESPONSE = {
    "metadata": {"stations": []},
    "items": [],
    "api_info": {"status": "healthy"},
}


class TestParseReadings:
    def test_parse_returns_readings(self):
        ts, readings = NEAWeatherAPI.parse_readings(SAMPLE_TEMP_RESPONSE)
        assert ts == "2026-04-07T15:39:00+08:00"
        assert readings["S109"] == 25.6
        assert readings["S50"] == 26.1

    def test_parse_empty(self):
        ts, readings = NEAWeatherAPI.parse_readings(EMPTY_RESPONSE)
        assert ts == ""
        assert len(readings) == 0


class TestGetAllStations:
    def test_merges_stations_from_endpoints(self):
        api = NEAWeatherAPI()
        responses = {
            "air-temperature": SAMPLE_TEMP_RESPONSE,
            "rainfall": SAMPLE_RAIN_RESPONSE,
            "relative-humidity": EMPTY_RESPONSE,
            "wind-speed": EMPTY_RESPONSE,
            "wind-direction": EMPTY_RESPONSE,
        }

        def mock_get(endpoint):
            return responses.get(endpoint, EMPTY_RESPONSE)

        with patch.object(api, "get_endpoint", side_effect=mock_get):
            stations = api.get_all_stations()

        assert "S109" in stations
        assert "S50" in stations
        assert "S77" in stations
        # S109 reports both temp and rainfall
        assert "air_temperature" in stations["S109"].data_types
        assert "rainfall" in stations["S109"].data_types

    def test_handles_endpoint_failure(self):
        api = NEAWeatherAPI()

        def mock_get(endpoint):
            if endpoint == "air-temperature":
                return SAMPLE_TEMP_RESPONSE
            raise Exception("timeout")

        with patch.object(api, "get_endpoint", side_effect=mock_get):
            stations = api.get_all_stations()

        assert "S109" in stations
        assert len(stations) == 2  # Only temp stations


class TestMergeObservations:
    def test_merges_across_endpoints(self):
        api = NEAWeatherAPI()
        responses = {
            "air-temperature": SAMPLE_TEMP_RESPONSE,
            "rainfall": SAMPLE_RAIN_RESPONSE,
            "relative-humidity": EMPTY_RESPONSE,
            "wind-speed": EMPTY_RESPONSE,
            "wind-direction": EMPTY_RESPONSE,
        }

        def mock_get(endpoint):
            return responses.get(endpoint, EMPTY_RESPONSE)

        with patch.object(api, "get_endpoint", side_effect=mock_get):
            with patch.object(api, "get_all_stations", return_value={
                "S109": MagicMock(name="Ang Mo Kio", station_id="S109"),
                "S50": MagicMock(name="Clementi", station_id="S50"),
                "S77": MagicMock(name="Upper Peirce", station_id="S77"),
            }):
                _, obs = merge_observations(api)

        sids = {o.station_id for o in obs}
        assert "S109" in sids
        s109 = [o for o in obs if o.station_id == "S109"][0]
        assert s109.air_temperature == 25.6
        assert s109.rainfall == 0.0

    def test_empty_endpoints(self):
        api = NEAWeatherAPI()

        with patch.object(api, "get_endpoint", return_value=EMPTY_RESPONSE):
            with patch.object(api, "get_all_stations", return_value={}):
                _, obs = merge_observations(api)

        assert len(obs) == 0


class TestConnectionString:
    def test_parse_plain_bootstrap(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=my-topic"
        config = parse_connection_string(cs)
        assert config["bootstrap.servers"] == "localhost:9092"
        assert config["_entity_path"] == "my-topic"

    def test_parse_event_hubs(self):
        cs = "Endpoint=sb://ns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=topic"
        config = parse_connection_string(cs)
        assert "bootstrap.servers" in config
        assert config["sasl.mechanism"] == "PLAIN"

    def test_parse_empty(self):
        config = parse_connection_string("")
        assert config == {}


class TestSendStations:
    def test_send_stations_emits_reference(self):
        api = NEAWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()

        responses = {
            "air-temperature": SAMPLE_TEMP_RESPONSE,
            "rainfall": SAMPLE_RAIN_RESPONSE,
            "relative-humidity": EMPTY_RESPONSE,
            "wind-speed": EMPTY_RESPONSE,
            "wind-direction": EMPTY_RESPONSE,
        }

        def mock_get(endpoint):
            return responses.get(endpoint, EMPTY_RESPONSE)

        with patch.object(api, "get_endpoint", side_effect=mock_get):
            count = send_stations(api, mock_producer)

        assert count == 3  # S109, S50, S77
        assert mock_producer.send_sg_gov_nea_weather_station.call_count == 3


class TestFeedObservations:
    def test_feed_emits_new(self):
        api = NEAWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        previous = {}

        responses = {
            "air-temperature": SAMPLE_TEMP_RESPONSE,
            "rainfall": SAMPLE_RAIN_RESPONSE,
            "relative-humidity": EMPTY_RESPONSE,
            "wind-speed": EMPTY_RESPONSE,
            "wind-direction": EMPTY_RESPONSE,
        }

        def mock_get(endpoint):
            return responses.get(endpoint, EMPTY_RESPONSE)

        with patch.object(api, "get_endpoint", side_effect=mock_get):
            count = feed_observations(api, mock_producer, previous)

        assert count == 3  # S109, S50, S77
        assert len(previous) == 3

    def test_feed_deduplicates(self):
        api = NEAWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        ts = "2026-04-07T15:39:00+08:00"
        previous = {
            f"S109:{ts}": ts,
            f"S50:{ts}": ts,
            f"S77:{ts}": ts,
        }

        responses = {
            "air-temperature": SAMPLE_TEMP_RESPONSE,
            "rainfall": SAMPLE_RAIN_RESPONSE,
            "relative-humidity": EMPTY_RESPONSE,
            "wind-speed": EMPTY_RESPONSE,
            "wind-direction": EMPTY_RESPONSE,
        }

        with patch.object(api, "get_endpoint", side_effect=lambda e: responses.get(e, EMPTY_RESPONSE)):
            count = feed_observations(api, mock_producer, previous)

        assert count == 0


class TestState:
    def test_load_missing_file(self, tmp_path):
        assert _load_state(str(tmp_path / "nonexistent.json")) == {}

    def test_save_and_load(self, tmp_path):
        path = str(tmp_path / "state.json")
        data = {"key1": "val1"}
        _save_state(path, data)
        loaded = _load_state(path)
        assert loaded == data

    def test_save_truncates_large_state(self, tmp_path):
        path = str(tmp_path / "state.json")
        data = {str(i): str(i) for i in range(110000)}
        _save_state(path, data)
        loaded = _load_state(path)
        assert len(loaded) <= 50000
