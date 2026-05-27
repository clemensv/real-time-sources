"""Unit tests for SMHI Weather Observation Bridge."""

import json
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

from smhi_weather.smhi_weather import (
    SMHIWeatherAPI,
    parse_connection_string,
    send_stations,
    feed_observations,
    _merge_observations,
    _load_state,
    _save_state,
    ALL_PARAMS,
    PARAM_AIR_TEMP,
    PARAM_WIND_GUST,
    PARAM_DEW_POINT,
    PARAM_PRESSURE,
    PARAM_HUMIDITY,
    PARAM_PRECIP,
    PARAM_WIND_DIR,
    PARAM_WIND_SPEED,
    PARAM_MAX_WIND_SPEED,
    PARAM_VISIBILITY,
    PARAM_CLOUD_COVER,
    PARAM_PRESENT_WX,
    PARAM_SUNSHINE,
    PARAM_IRRADIANCE,
    PARAM_PRECIP_INTENSITY,
)


SAMPLE_STATION_RESPONSE = {
    "station": [
        {
            "key": "98210",
            "name": "Kiruna Flygplats",
            "title": "98210 - Kiruna Flygplats",
            "owner": "SMHI",
            "ownerCategory": "SMHI",
            "measuringStations": "CORE",
            "height": 452.0,
            "summary": "Latitud: 67.82 Longitud: 20.33 Höjd: 452.0"
        },
        {
            "key": "97280",
            "name": "Luleå-Kallax Flygplats",
            "title": "97280 - Luleå-Kallax Flygplats",
            "owner": "SMHI",
            "ownerCategory": "SMHI",
            "measuringStations": "CORE",
            "height": 17.0,
            "summary": "Latitud: 65.55 Longitud: 22.13 Höjd: 17.0"
        }
    ]
}

SAMPLE_BULK_RESPONSE = {
    "station": [
        {
            "key": "98210",
            "name": "Kiruna Flygplats",
            "value": [
                {
                    "date": 1712505600000,
                    "value": "-5.2",
                    "quality": "G"
                }
            ]
        },
        {
            "key": "97280",
            "name": "Luleå-Kallax Flygplats",
            "value": [
                {
                    "date": 1712505600000,
                    "value": "2.1",
                    "quality": "G"
                }
            ]
        }
    ]
}

SAMPLE_BULK_WIND = {
    "station": [
        {
            "key": "98210",
            "name": "Kiruna Flygplats",
            "value": [{"date": 1712505600000, "value": "12.5", "quality": "G"}]
        }
    ]
}

SAMPLE_BULK_WIND_DIR = {
    "station": [
        {
            "key": "98210",
            "name": "Kiruna Flygplats",
            "value": [{"date": 1712505600000, "value": "225", "quality": "G"}]
        }
    ]
}

SAMPLE_BULK_WIND_SPEED = {
    "station": [
        {
            "key": "98210",
            "name": "Kiruna Flygplats",
            "value": [{"date": 1712505600000, "value": "6.3", "quality": "G"}]
        }
    ]
}

SAMPLE_BULK_VISIBILITY = {
    "station": [
        {
            "key": "98210",
            "name": "Kiruna Flygplats",
            "value": [{"date": 1712505600000, "value": "30.0", "quality": "G"}]
        }
    ]
}

SAMPLE_BULK_CLOUD = {
    "station": [
        {
            "key": "98210",
            "name": "Kiruna Flygplats",
            "value": [{"date": 1712505600000, "value": "6", "quality": "G"}]
        }
    ]
}


class TestParseStation:
    def test_parse_basic_station(self):
        station = SMHIWeatherAPI.parse_station(SAMPLE_STATION_RESPONSE["station"][0])
        assert station.station_id == "98210"
        assert station.name == "Kiruna Flygplats"
        assert station.owner == "SMHI"
        assert station.owner_category == "SMHI"
        assert station.measuring_stations == "CORE"
        assert station.height == 452.0
        assert station.latitude == 67.82
        assert station.longitude == 20.33

    def test_parse_station_with_title_dash(self):
        station = SMHIWeatherAPI.parse_station(SAMPLE_STATION_RESPONSE["station"][1])
        assert station.station_id == "97280"
        assert station.name == "Luleå-Kallax Flygplats"
        assert station.latitude == 65.55
        assert station.longitude == 22.13

    def test_parse_station_missing_summary(self):
        data = {"key": "1", "title": "1 - Test", "summary": ""}
        station = SMHIWeatherAPI.parse_station(data)
        assert station.station_id == "1"
        assert station.latitude == 0.0
        assert station.longitude == 0.0


class TestParseBulkObservations:
    def test_parse_returns_stations(self):
        result = SMHIWeatherAPI.parse_bulk_observations(SAMPLE_BULK_RESPONSE)
        assert "98210" in result
        assert "97280" in result

    def test_parse_values_correct(self):
        result = SMHIWeatherAPI.parse_bulk_observations(SAMPLE_BULK_RESPONSE)
        assert result["98210"]["value"] == -5.2
        assert result["97280"]["value"] == 2.1
        assert result["98210"]["quality"] == "G"

    def test_parse_timestamp_utc(self):
        result = SMHIWeatherAPI.parse_bulk_observations(SAMPLE_BULK_RESPONSE)
        ts = result["98210"]["observation_time"]
        assert isinstance(ts, datetime)
        assert ts.tzinfo is not None

    def test_parse_empty_values(self):
        data = {"station": [{"key": "1", "name": "X", "value": []}]}
        result = SMHIWeatherAPI.parse_bulk_observations(data)
        assert len(result) == 0

    def test_parse_null_value(self):
        data = {"station": [{"key": "1", "name": "X", "value": [{"date": 1712505600000, "value": None, "quality": ""}]}]}
        result = SMHIWeatherAPI.parse_bulk_observations(data)
        assert len(result) == 0

    def test_parse_empty_station_list(self):
        result = SMHIWeatherAPI.parse_bulk_observations({"station": []})
        assert len(result) == 0


class TestMergeObservations:
    def test_merge_single_parameter(self):
        param_data = {
            PARAM_AIR_TEMP: SMHIWeatherAPI.parse_bulk_observations(SAMPLE_BULK_RESPONSE)
        }
        obs_list = _merge_observations(param_data)
        assert len(obs_list) == 2
        station_ids = {o.station_id for o in obs_list}
        assert "98210" in station_ids

    def test_merge_multiple_parameters(self):
        temp_data = SMHIWeatherAPI.parse_bulk_observations(SAMPLE_BULK_RESPONSE)
        wind_data = SMHIWeatherAPI.parse_bulk_observations(SAMPLE_BULK_WIND)
        param_data = {PARAM_AIR_TEMP: temp_data, PARAM_WIND_GUST: wind_data}
        obs_list = _merge_observations(param_data)
        kiruna = [o for o in obs_list if o.station_id == "98210"][0]
        assert kiruna.air_temperature == -5.2
        assert kiruna.wind_gust == 12.5

    def test_merge_station_only_in_wind(self):
        wind_only = {"station": [{"key": "99999", "name": "Test", "value": [{"date": 1712505600000, "value": "8.0", "quality": "G"}]}]}
        param_data = {
            PARAM_AIR_TEMP: {},
            PARAM_WIND_GUST: SMHIWeatherAPI.parse_bulk_observations(wind_only),
        }
        obs_list = _merge_observations(param_data)
        assert len(obs_list) == 1
        assert obs_list[0].wind_gust == 8.0
        assert obs_list[0].air_temperature is None

    def test_merge_new_parameters(self):
        temp_data = SMHIWeatherAPI.parse_bulk_observations(SAMPLE_BULK_RESPONSE)
        wind_dir_data = SMHIWeatherAPI.parse_bulk_observations(SAMPLE_BULK_WIND_DIR)
        wind_speed_data = SMHIWeatherAPI.parse_bulk_observations(SAMPLE_BULK_WIND_SPEED)
        vis_data = SMHIWeatherAPI.parse_bulk_observations(SAMPLE_BULK_VISIBILITY)
        cloud_data = SMHIWeatherAPI.parse_bulk_observations(SAMPLE_BULK_CLOUD)
        param_data = {
            PARAM_AIR_TEMP: temp_data,
            PARAM_WIND_DIR: wind_dir_data,
            PARAM_WIND_SPEED: wind_speed_data,
            PARAM_VISIBILITY: vis_data,
            PARAM_CLOUD_COVER: cloud_data,
        }
        obs_list = _merge_observations(param_data)
        kiruna = [o for o in obs_list if o.station_id == "98210"][0]
        assert kiruna.air_temperature == -5.2
        assert kiruna.wind_direction == 225.0
        assert kiruna.wind_speed == 6.3
        assert kiruna.visibility == 30.0
        assert kiruna.total_cloud_cover == 6
        # Station 97280 only has temperature, so new fields should be None
        lulea = [o for o in obs_list if o.station_id == "97280"][0]
        assert lulea.air_temperature == 2.1
        assert lulea.wind_direction is None
        assert lulea.wind_speed is None

    def test_all_params_list_complete(self):
        assert len(ALL_PARAMS) == 15
        assert PARAM_AIR_TEMP in ALL_PARAMS
        assert PARAM_WIND_DIR in ALL_PARAMS
        assert PARAM_PRECIP_INTENSITY in ALL_PARAMS

    def test_merge_empty(self):
        obs_list = _merge_observations({})
        assert len(obs_list) == 0


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
        api = SMHIWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()

        with patch.object(api, "get_stations_for_parameter", return_value=SAMPLE_STATION_RESPONSE["station"]):
            count = send_stations(api, mock_producer)

        assert count == 2
        assert mock_producer.send_se_gov_smhi_weather_station.call_count == 2
        mock_producer.producer.flush.assert_called_once()

    def test_send_stations_handles_error(self):
        api = SMHIWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()

        with patch.object(api, "get_stations_for_parameter", side_effect=Exception("timeout")):
            with pytest.raises(Exception):
                send_stations(api, mock_producer)


class TestFeedObservations:
    def test_feed_emits_new(self):
        api = SMHIWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        previous = {}

        with patch.object(api, "get_bulk_latest", return_value=SAMPLE_BULK_RESPONSE):
            count = feed_observations(api, mock_producer, previous)

        assert count == 2
        assert len(previous) == 2

    def test_feed_deduplicates(self):
        api = SMHIWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        ts = datetime.fromtimestamp(1712505600000 / 1000.0, tz=timezone.utc)
        previous = {f"98210:{ts.isoformat()}": ts.isoformat(), f"97280:{ts.isoformat()}": ts.isoformat()}

        with patch.object(api, "get_bulk_latest", return_value=SAMPLE_BULK_RESPONSE):
            count = feed_observations(api, mock_producer, previous)

        assert count == 0

    def test_feed_handles_fetch_error(self):
        api = SMHIWeatherAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        previous = {}

        with patch.object(api, "get_bulk_latest", side_effect=Exception("timeout")):
            count = feed_observations(api, mock_producer, previous)

        assert count == 0


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
