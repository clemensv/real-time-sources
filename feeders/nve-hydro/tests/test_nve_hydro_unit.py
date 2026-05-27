"""Unit tests for the NVE Hydro bridge."""

import json
import os
import pytest
from unittest.mock import MagicMock, patch

from nve_hydro.nve_hydro import (
    NVEHydroAPI,
    parse_connection_string,
    _load_state,
    _save_state,
    _station_has_parameter,
    _fetch_station_observations,
    send_stations,
    feed_observations,
    NVE_BASE_URL,
    PARAM_STAGE,
    PARAM_DISCHARGE,
)
from nve_hydro_producer_data.no.nve.hydrology.station import Station
from nve_hydro_producer_data.no.nve.hydrology.waterlevelobservation import WaterLevelObservation
from nve_hydro_producer_kafka_producer.producer import NONVEHydrologyEventProducer


# ---------------------------------------------------------------------------
# Sample API payloads
# ---------------------------------------------------------------------------

SAMPLE_STATION_1 = {
    "stationId": "2.11.0",
    "stationName": "Bulken",
    "riverName": "Vosso",
    "latitude": 60.680,
    "longitude": 6.040,
    "masl": 50.0,
    "councilName": "Voss",
    "countyName": "Vestland",
    "drainageBasinArea": 1157.0,
    "seriesList": [
        {"parameter": PARAM_STAGE},
        {"parameter": PARAM_DISCHARGE},
    ],
}

SAMPLE_STATION_2 = {
    "stationId": "12.193.0",
    "stationName": "Høgfoss",
    "riverName": "Nidelva",
    "latitude": 63.420,
    "longitude": 10.399,
    "masl": None,
    "councilName": None,
    "countyName": "Trøndelag",
    "drainageBasinArea": None,
    "seriesList": [
        {"parameter": PARAM_STAGE},
    ],
}

SAMPLE_OBSERVATIONS_STAGE = {
    "data": [
        {
            "observations": [
                {"time": "2023-11-14T12:00:00Z", "value": 1.23},
                {"time": "2023-11-14T13:00:00Z", "value": 1.45},
            ]
        }
    ]
}

SAMPLE_OBSERVATIONS_DISCHARGE = {
    "data": [
        {
            "observations": [
                {"time": "2023-11-14T12:00:00Z", "value": 45.6},
            ]
        }
    ]
}


# ---------------------------------------------------------------------------
# Connection string parsing
# ---------------------------------------------------------------------------

class TestConnectionStringParsing:
    def test_bootstrap_server(self):
        cfg = parse_connection_string("BootstrapServer=localhost:9092")
        assert cfg["bootstrap.servers"] == "localhost:9092"
        assert "sasl.username" not in cfg

    def test_event_hubs_format(self):
        cs = (
            "Endpoint=sb://my-ns.servicebus.windows.net/;"
            "SharedAccessKeyName=myPolicy;"
            "SharedAccessKey=abc123"
        )
        cfg = parse_connection_string(cs)
        assert cfg["bootstrap.servers"] == "my-ns.servicebus.windows.net:9093"
        assert cfg["sasl.username"] == "$ConnectionString"
        assert cfg["sasl.password"] == cs
        assert cfg["security.protocol"] == "SASL_SSL"
        assert cfg["sasl.mechanism"] == "PLAIN"

    def test_entity_path_extracted(self):
        cs = "BootstrapServer=broker:9092;EntityPath=nve-topic"
        cfg = parse_connection_string(cs)
        assert cfg["_entity_path"] == "nve-topic"

    def test_empty_string(self):
        assert parse_connection_string("") == {}

    def test_no_sasl_when_only_bootstrap(self):
        cfg = parse_connection_string("BootstrapServer=b:9092")
        assert "security.protocol" not in cfg


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------

class TestStateHelpers:
    def test_load_missing_file(self, tmp_path):
        assert _load_state(str(tmp_path / "no.json")) == {}

    def test_load_none_path(self):
        assert _load_state(None) == {}

    def test_save_and_reload(self, tmp_path):
        path = str(tmp_path / "state.json")
        data = {"2.11.0:2023-11-14T12:00:00Z:": "2023-11-14T12:00:00Z"}
        _save_state(path, data)
        assert _load_state(path) == data

    def test_save_trims_large_state(self, tmp_path):
        path = str(tmp_path / "big.json")
        data = {str(i): "ts" for i in range(200000)}
        _save_state(path, data)
        assert len(_load_state(path)) == 50000

    def test_save_none_path_is_noop(self):
        _save_state(None, {"k": "v"})  # must not raise

    def test_save_creates_file(self, tmp_path):
        path = str(tmp_path / "out.json")
        _save_state(path, {"x": "y"})
        assert os.path.exists(path)


# ---------------------------------------------------------------------------
# _station_has_parameter helper
# ---------------------------------------------------------------------------

class TestStationHasParameter:
    def test_station_with_stage(self):
        assert _station_has_parameter(SAMPLE_STATION_1, PARAM_STAGE) is True

    def test_station_with_discharge(self):
        assert _station_has_parameter(SAMPLE_STATION_1, PARAM_DISCHARGE) is True

    def test_station_without_discharge(self):
        assert _station_has_parameter(SAMPLE_STATION_2, PARAM_DISCHARGE) is False

    def test_empty_series_list(self):
        st = {"seriesList": []}
        assert _station_has_parameter(st, PARAM_STAGE) is False

    def test_none_series_list(self):
        st = {"seriesList": None}
        assert _station_has_parameter(st, PARAM_STAGE) is False

    def test_missing_series_list_key(self):
        st = {}
        assert _station_has_parameter(st, PARAM_STAGE) is False


# ---------------------------------------------------------------------------
# _fetch_station_observations helper
# ---------------------------------------------------------------------------

class TestFetchStationObservations:
    @patch.object(NVEHydroAPI, "get_observations")
    def test_returns_latest_value(self, mock_get_obs):
        def side_effect(sid, param):
            if param == PARAM_STAGE:
                return SAMPLE_OBSERVATIONS_STAGE["data"]
            return []
        mock_get_obs.side_effect = side_effect
        api = NVEHydroAPI("dummy-key")
        result = _fetch_station_observations(api, "2.11.0", [PARAM_STAGE, PARAM_DISCHARGE])
        assert PARAM_STAGE in result
        assert result[PARAM_STAGE]["value"] == 1.45
        assert PARAM_DISCHARGE not in result

    @patch.object(NVEHydroAPI, "get_observations")
    def test_empty_observations(self, mock_get_obs):
        mock_get_obs.return_value = []
        api = NVEHydroAPI("dummy-key")
        result = _fetch_station_observations(api, "2.11.0", [PARAM_STAGE])
        assert result == {}


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------

class TestNVEHydroAPI:
    def test_default_base_url(self):
        api = NVEHydroAPI("key")
        assert api.base_url == NVE_BASE_URL

    def test_api_key_in_header(self):
        api = NVEHydroAPI("my-secret-key")
        assert api.session.headers["X-API-Key"] == "my-secret-key"

    def test_get_stations_parsed(self, requests_mock):
        api = NVEHydroAPI("key")
        requests_mock.get(
            f"{NVE_BASE_URL}/Stations",
            json={"data": [SAMPLE_STATION_1, SAMPLE_STATION_2]},
        )
        stations = api.get_stations()
        assert len(stations) == 2
        assert stations[0]["stationId"] == "2.11.0"

    def test_get_observations_parsed(self, requests_mock):
        api = NVEHydroAPI("key")
        requests_mock.get(
            f"{NVE_BASE_URL}/Observations",
            json=SAMPLE_OBSERVATIONS_STAGE,
        )
        data = api.get_observations("2.11.0", PARAM_STAGE)
        assert len(data) == 1
        assert data[0]["observations"][0]["value"] == 1.23

    def test_get_observations_network_error(self, requests_mock):
        import requests as req
        api = NVEHydroAPI("key")
        requests_mock.get(f"{NVE_BASE_URL}/Observations",
                          exc=req.exceptions.ConnectionError("timeout"))
        # get_observations catches RequestException and returns []
        result = api.get_observations("2.11.0", PARAM_STAGE)
        assert result == []

    def test_get_stations_http_error(self, requests_mock):
        api = NVEHydroAPI("key")
        requests_mock.get(f"{NVE_BASE_URL}/Stations", status_code=401)
        import requests as req
        with pytest.raises(req.HTTPError):
            api.get_stations()


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

class TestDataClasses:
    def test_station_roundtrip(self):
        st = Station(
            station_id="2.11.0",
            station_name="Bulken",
            river_name="Vosso",
            latitude=60.68,
            longitude=6.04,
            masl=50.0,
            council_name="Voss",
            county_name="Vestland",
            drainage_basin_area=1157.0,
        )
        assert st.station_id == "2.11.0"
        data = json.loads(st.to_json())
        assert data["station_name"] == "Bulken"

    def test_station_optional_nulls(self):
        st = Station(
            station_id="12.193.0",
            station_name="Høgfoss",
            river_name=None,
            latitude=63.42,
            longitude=10.40,
            masl=None,
            council_name=None,
            county_name=None,
            drainage_basin_area=None,
        )
        assert st.masl is None
        assert st.river_name is None

    def test_observation_roundtrip(self):
        obs = WaterLevelObservation(
            station_id="2.11.0",
            water_level=1.45,
            water_level_unit="m",
            water_level_timestamp="2023-11-14T13:00:00Z",
            discharge=45.6,
            discharge_unit="m3/s",
            discharge_timestamp="2023-11-14T12:00:00Z",
        )
        assert obs.station_id == "2.11.0"
        data = json.loads(obs.to_json())
        assert data["water_level"] == 1.45
        assert data["discharge"] == 45.6


# ---------------------------------------------------------------------------
# send_stations
# ---------------------------------------------------------------------------

class TestSendStations:
    def _mock_producer(self):
        p = MagicMock(spec=NONVEHydrologyEventProducer)
        p.producer = MagicMock()
        return p

    @patch.object(NVEHydroAPI, "get_stations")
    def test_sends_all_stations_and_builds_params(self, mock_gs):
        mock_gs.return_value = [SAMPLE_STATION_1, SAMPLE_STATION_2]
        api = NVEHydroAPI("key")
        prod = self._mock_producer()
        station_params = send_stations(api, prod)
        assert prod.send_no_nve_hydrology_station.call_count == 2
        prod.producer.flush.assert_called_once()
        assert PARAM_STAGE in station_params["2.11.0"]
        assert PARAM_DISCHARGE in station_params["2.11.0"]
        assert PARAM_STAGE in station_params["12.193.0"]
        assert PARAM_DISCHARGE not in station_params["12.193.0"]

    @patch.object(NVEHydroAPI, "get_stations")
    def test_skips_station_without_id(self, mock_gs):
        mock_gs.return_value = [{"stationName": "No ID station", "seriesList": []}]
        api = NVEHydroAPI("key")
        prod = self._mock_producer()
        result = send_stations(api, prod)
        assert result == {}
        prod.send_no_nve_hydrology_station.assert_not_called()

    @patch.object(NVEHydroAPI, "get_stations")
    def test_empty_station_list(self, mock_gs):
        mock_gs.return_value = []
        api = NVEHydroAPI("key")
        prod = self._mock_producer()
        result = send_stations(api, prod)
        assert result == {}


# ---------------------------------------------------------------------------
# feed_observations
# ---------------------------------------------------------------------------

class TestFeedObservations:
    def _mock_producer(self):
        p = MagicMock(spec=NONVEHydrologyEventProducer)
        p.producer = MagicMock()
        return p

    @patch.object(NVEHydroAPI, "get_observations")
    def test_sends_new_observations(self, mock_obs):
        def side_effect(sid, param):
            if param == PARAM_STAGE:
                return SAMPLE_OBSERVATIONS_STAGE["data"]
            if param == PARAM_DISCHARGE:
                return SAMPLE_OBSERVATIONS_DISCHARGE["data"]
            return []
        mock_obs.side_effect = side_effect

        api = NVEHydroAPI("key")
        prod = self._mock_producer()
        station_params = {"2.11.0": [PARAM_STAGE, PARAM_DISCHARGE]}
        previous = {}
        count = feed_observations(api, prod, station_params, previous)
        assert count == 1
        prod.send_no_nve_hydrology_water_level_observation.assert_called_once()
        prod.producer.flush.assert_called()

    @patch.object(NVEHydroAPI, "get_observations")
    def test_deduplicates(self, mock_obs):
        mock_obs.side_effect = lambda sid, param: (
            SAMPLE_OBSERVATIONS_STAGE["data"] if param == PARAM_STAGE else []
        )
        api = NVEHydroAPI("key")
        prod = self._mock_producer()
        station_params = {"2.11.0": [PARAM_STAGE]}
        previous = {}
        feed_observations(api, prod, station_params, previous)
        prod.reset_mock()
        prod.producer = MagicMock()
        count = feed_observations(api, prod, station_params, previous)
        assert count == 0

    @patch.object(NVEHydroAPI, "get_observations")
    def test_empty_observations(self, mock_obs):
        mock_obs.return_value = []
        api = NVEHydroAPI("key")
        prod = self._mock_producer()
        count = feed_observations(api, prod, {"2.11.0": [PARAM_STAGE]}, {})
        assert count == 0


# ---------------------------------------------------------------------------
# Producer client
# ---------------------------------------------------------------------------

class TestProducerClient:
    def test_send_station_calls_produce(self):
        mock_kafka = MagicMock()
        prod = NONVEHydrologyEventProducer(mock_kafka, "nve-topic")
        st = Station(
            station_id="2.11.0", station_name="Bulken", river_name="Vosso",
            latitude=60.68, longitude=6.04, masl=50.0,
            council_name="Voss", county_name="Vestland", drainage_basin_area=1157.0,
        )
        prod.send_no_nve_hydrology_station("2.11.0", st)
        mock_kafka.produce.assert_called_once()
        mock_kafka.flush.assert_called_once()

    def test_send_observation_calls_produce(self):
        mock_kafka = MagicMock()
        prod = NONVEHydrologyEventProducer(mock_kafka, "nve-topic")
        obs = WaterLevelObservation(
            station_id="2.11.0",
            water_level=1.45, water_level_unit="m",
            water_level_timestamp="2023-11-14T13:00:00Z",
            discharge=None, discharge_unit="m3/s", discharge_timestamp="",
        )
        prod.send_no_nve_hydrology_water_level_observation("2.11.0", obs)
        mock_kafka.produce.assert_called_once()

    def test_no_flush_when_disabled(self):
        mock_kafka = MagicMock()
        prod = NONVEHydrologyEventProducer(mock_kafka, "nve-topic")
        st = Station(
            station_id="2.11.0", station_name="Bulken", river_name=None,
            latitude=60.68, longitude=6.04, masl=None,
            council_name=None, county_name=None, drainage_basin_area=None,
        )
        prod.send_no_nve_hydrology_station("2.11.0", st, flush_producer=False)
        mock_kafka.flush.assert_not_called()

    def test_kafka_key_matches_station_id(self):
        mock_kafka = MagicMock()
        prod = NONVEHydrologyEventProducer(mock_kafka, "nve-topic")
        st = Station(
            station_id="2.11.0", station_name="Bulken", river_name=None,
            latitude=60.68, longitude=6.04, masl=None,
            council_name=None, county_name=None, drainage_basin_area=None,
        )
        prod.send_no_nve_hydrology_station("2.11.0", st)
        call_kwargs = mock_kafka.produce.call_args
        key = call_kwargs[1]["key"]
        assert key in (b"2.11.0", "2.11.0")
