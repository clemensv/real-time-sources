"""Unit tests for Environment Canada Weather Observation Bridge."""

import json
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

from environment_canada.environment_canada import (
    ECWeatherAPI,
    parse_connection_string,
    send_stations,
    feed_observations,
    _load_state,
    _save_state,
)


SAMPLE_STATION_FEATURE = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [-75.67, 45.32, 79.0]},
    "properties": {
        "msc_id": "6106000",
        "name": "OTTAWA INTL A",
        "iata_id": "YOW",
        "wmo_id": 71628,
        "province_territory": "ON",
        "data_provider": "MSC",
        "dataset_network": "MSC-Sfc-Auto",
        "auto_man": "Auto",
    },
}

SAMPLE_STATION_FEATURE_2 = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [-79.63, 43.68, 173.0]},
    "properties": {
        "msc_id": "6158733",
        "name": "TORONTO LESTER B. PEARSON INTL A",
        "iata_id": "YYZ",
        "wmo_id": 71624,
        "province_territory": "ON",
        "data_provider": "MSC",
        "dataset_network": "MSC-Sfc-Auto",
        "auto_man": "Auto",
    },
}

SAMPLE_OBS_FEATURE = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [-75.67, 45.32]},
    "properties": {
        "msc_id-value": "6106000",
        "stn_nam-value": "OTTAWA INTL A",
        "obs_date_tm": "2026-04-07T12:00:00Z",
        "air_temp": -2.5,
        "dwpt_temp": -5.1,
        "rel_hum": 78,
        "stn_pres": 99.21,
        "avg_wnd_spd_10m_pst1mt": 15.0,
        "avg_wnd_dir_10m_pst1mt": 270,
        "max_wnd_spd_10m_pst1mt": 22.0,
        "pcpn_amt_pst1hr": 0.0,
    },
}

SAMPLE_OBS_FEATURE_NO_MSC = {
    "type": "Feature",
    "geometry": None,
    "properties": {
        "obs_date_tm": "2026-04-07T12:00:00Z",
        "air_temp": 1.0,
    },
}

SAMPLE_OBS_FEATURE_NO_TIME = {
    "type": "Feature",
    "geometry": None,
    "properties": {
        "msc_id-value": "6106000",
    },
}


class TestParseStation:
    def test_parse_basic_station(self):
        station = ECWeatherAPI.parse_station(SAMPLE_STATION_FEATURE)
        assert station.msc_id == "6106000"
        assert station.name == "OTTAWA INTL A"
        assert station.iata_id == "YOW"
        assert station.wmo_id == 71628
        assert station.province_territory == "ON"
        assert station.data_provider == "MSC"
        assert station.latitude == 45.32
        assert station.longitude == -75.67
        assert station.elevation == 79.0

    def test_parse_station_no_geometry(self):
        feature = {"properties": {"msc_id": "123", "name": "Test"}, "geometry": None}
        station = ECWeatherAPI.parse_station(feature)
        assert station.msc_id == "123"
        assert station.latitude is None
        assert station.longitude is None
        assert station.elevation is None

    def test_parse_station_missing_fields(self):
        feature = {"properties": {"msc_id": "456"}, "geometry": {"type": "Point", "coordinates": [-80.0, 44.0]}}
        station = ECWeatherAPI.parse_station(feature)
        assert station.msc_id == "456"
        assert station.name == ""
        assert station.latitude == 44.0


class TestParseObservation:
    def test_parse_basic_observation(self):
        obs = ECWeatherAPI.parse_observation(SAMPLE_OBS_FEATURE)
        assert obs is not None
        assert obs.msc_id == "6106000"
        assert obs.station_name == "OTTAWA INTL A"
        assert obs.air_temperature == -2.5
        assert obs.dew_point == -5.1
        assert obs.relative_humidity == 78
        assert obs.station_pressure == 99.21
        assert obs.wind_speed == 15.0
        assert obs.wind_direction == 270
        assert obs.wind_gust == 22.0
        assert obs.precipitation_1hr == 0.0
        assert obs.observation_time.tzinfo is not None

    def test_parse_observation_no_msc(self):
        obs = ECWeatherAPI.parse_observation(SAMPLE_OBS_FEATURE_NO_MSC)
        assert obs is None

    def test_parse_observation_no_time(self):
        obs = ECWeatherAPI.parse_observation(SAMPLE_OBS_FEATURE_NO_TIME)
        assert obs is None

    def test_parse_observation_partial_fields(self):
        feature = {
            "type": "Feature",
            "geometry": None,
            "properties": {
                "msc_id-value": "999",
                "stn_nam-value": "TEST",
                "obs_date_tm": "2026-04-07T06:00:00Z",
                "air_temp": 10.5,
            },
        }
        obs = ECWeatherAPI.parse_observation(feature)
        assert obs is not None
        assert obs.air_temperature == 10.5
        assert obs.dew_point is None
        assert obs.wind_speed is None

    def test_parse_observation_clim_id_fallback(self):
        feature = {
            "type": "Feature",
            "geometry": None,
            "properties": {
                "clim_id-value": "ABC123",
                "stn_nam-value": "FALLBACK",
                "obs_date_tm": "2026-04-07T09:00:00Z",
            },
        }
        obs = ECWeatherAPI.parse_observation(feature)
        assert obs is not None
        assert obs.msc_id == "ABC123"


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
        assert config["security.protocol"] == "SASL_SSL"

    def test_parse_empty(self):
        config = parse_connection_string("")
        assert config == {}


class TestSendStations:
    def test_send_stations_emits_reference(self):
        api = ECWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()

        with patch.object(api, "get_stations", return_value=[SAMPLE_STATION_FEATURE, SAMPLE_STATION_FEATURE_2]):
            count = send_stations(api, mock_producer)

        assert count == 2
        assert mock_producer.send_ca_gov_eccc_weather_station.call_count == 2
        mock_producer.producer.flush.assert_called_once()

    def test_send_stations_skips_empty_msc(self):
        api = ECWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        empty_feature = {"properties": {"msc_id": ""}, "geometry": None}

        with patch.object(api, "get_stations", return_value=[empty_feature]):
            count = send_stations(api, mock_producer)

        assert count == 0

    def test_send_stations_handles_error(self):
        api = ECWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()

        with patch.object(api, "get_stations", side_effect=Exception("timeout")):
            with pytest.raises(Exception):
                send_stations(api, mock_producer)


class TestFeedObservations:
    def test_feed_emits_new(self):
        api = ECWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        previous = {}

        with patch.object(api, "get_recent_observations", return_value=[SAMPLE_OBS_FEATURE]):
            count = feed_observations(api, mock_producer, previous)

        assert count == 1
        assert len(previous) == 1

    def test_feed_deduplicates(self):
        api = ECWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        ts = datetime(2026, 4, 7, 12, 0, 0, tzinfo=timezone.utc)
        previous = {f"6106000:{ts.isoformat()}": ts.isoformat()}

        with patch.object(api, "get_recent_observations", return_value=[SAMPLE_OBS_FEATURE]):
            count = feed_observations(api, mock_producer, previous)

        assert count == 0

    def test_feed_skips_unparseable(self):
        api = ECWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        previous = {}

        with patch.object(api, "get_recent_observations", return_value=[SAMPLE_OBS_FEATURE_NO_MSC]):
            count = feed_observations(api, mock_producer, previous)

        assert count == 0

    def test_feed_handles_fetch_error(self):
        api = ECWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        previous = {}

        with patch.object(api, "get_recent_observations", side_effect=Exception("timeout")):
            with pytest.raises(Exception):
                feed_observations(api, mock_producer, previous)


class TestState:
    def test_load_missing_file(self, tmp_path):
        assert _load_state(str(tmp_path / "nonexistent.json")) == {}

    def test_save_and_load(self, tmp_path):
        path = str(tmp_path / "state.json")
        data = {"key1": "val1", "key2": "val2"}
        _save_state(path, data)
        loaded = _load_state(path)
        assert loaded == data

    def test_save_truncates_large_state(self, tmp_path):
        path = str(tmp_path / "state.json")
        data = {str(i): str(i) for i in range(110000)}
        _save_state(path, data)
        loaded = _load_state(path)
        assert len(loaded) <= 50000

    def test_load_empty_path(self):
        assert _load_state("") == {}
