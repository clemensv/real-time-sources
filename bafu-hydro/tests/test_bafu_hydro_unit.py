"""Unit tests for the BAFU Hydro bridge."""

import json
import os
import pytest
from unittest.mock import MagicMock, patch

from bafu_hydro.bafu_hydro import (
    BAFUHydroAPI,
    parse_connection_string,
    _load_state,
    _save_state,
    send_stations,
    feed_observations,
    EXISTENZ_BASE_URL,
    PAR_HEIGHT,
    PAR_FLOW,
    PAR_TEMPERATURE,
)
from bafu_hydro_producer_data.ch.bafu.hydrology.station import Station
from bafu_hydro_producer_data.ch.bafu.hydrology.waterlevelobservation import WaterLevelObservation
from bafu_hydro_producer_kafka_producer.producer import CHBAFUHydrologyEventProducer


# ---------------------------------------------------------------------------
# Sample API payloads
# ---------------------------------------------------------------------------

SAMPLE_LOCATIONS_RESPONSE = {
    "payload": {
        "2018": {
            "details": {
                "id": 2018,
                "name": "Rhein - Basel",
                "water-body-name": "Rhein",
                "water-body-type": "river",
                "lat": 47.5596,
                "lon": 7.5886,
            }
        },
        "2030": {
            "details": {
                "id": 2030,
                "name": "Aare - Bern",
                "water-body-name": "Aare",
                "water-body-type": "river",
                "lat": 46.9480,
                "lon": 7.4474,
            }
        },
    }
}

SAMPLE_LATEST_RESPONSE = {
    "payload": [
        {"loc": 2018, "par": PAR_HEIGHT,      "val": 2.56, "timestamp": 1700000000},
        {"loc": 2018, "par": PAR_FLOW,        "val": 1234.5, "timestamp": 1700000000},
        {"loc": 2018, "par": PAR_TEMPERATURE, "val": 12.3, "timestamp": 1700000000},
        {"loc": 2030, "par": PAR_HEIGHT,      "val": 1.10, "timestamp": 1700000100},
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
        cs = "BootstrapServer=broker:9092;EntityPath=my-topic"
        cfg = parse_connection_string(cs)
        assert cfg["_entity_path"] == "my-topic"
        assert cfg["bootstrap.servers"] == "broker:9092"

    def test_empty_string_returns_empty(self):
        cfg = parse_connection_string("")
        assert cfg == {}

    def test_no_sasl_when_only_bootstrap(self):
        cfg = parse_connection_string("BootstrapServer=b:9092")
        assert "sasl.username" not in cfg
        assert "security.protocol" not in cfg


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------

class TestStateHelpers:
    def test_load_state_missing_file(self, tmp_path):
        result = _load_state(str(tmp_path / "nonexistent.json"))
        assert result == {}

    def test_load_state_none_path(self):
        result = _load_state(None)
        assert result == {}

    def test_save_and_reload(self, tmp_path):
        path = str(tmp_path / "state.json")
        data = {"2018:2023-01-01T00:00:00+00:00::": "2023-01-01T00:00:00+00:00"}
        _save_state(path, data)
        loaded = _load_state(path)
        assert loaded == data

    def test_save_trims_large_state(self, tmp_path):
        path = str(tmp_path / "big.json")
        data = {str(i): "ts" for i in range(200000)}
        _save_state(path, data)
        loaded = _load_state(path)
        assert len(loaded) == 50000

    def test_save_none_path_is_noop(self):
        _save_state(None, {"key": "val"})  # must not raise

    def test_save_creates_file(self, tmp_path):
        path = str(tmp_path / "new.json")
        _save_state(path, {"a": "b"})
        assert os.path.exists(path)


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------

class TestBAFUHydroAPI:
    def test_default_base_url(self):
        api = BAFUHydroAPI()
        assert api.base_url == EXISTENZ_BASE_URL

    def test_custom_base_url(self):
        api = BAFUHydroAPI(base_url="https://example.com")
        assert api.base_url == "https://example.com"

    def test_get_locations_parsed(self, requests_mock):
        api = BAFUHydroAPI()
        requests_mock.get(f"{EXISTENZ_BASE_URL}/locations", json=SAMPLE_LOCATIONS_RESPONSE)
        locs = api.get_locations()
        assert "2018" in locs
        assert locs["2018"]["name"] == "Rhein - Basel"
        assert locs["2030"]["lat"] == 46.9480

    def test_get_locations_empty_payload(self, requests_mock):
        api = BAFUHydroAPI()
        requests_mock.get(f"{EXISTENZ_BASE_URL}/locations", json={"payload": {}})
        assert api.get_locations() == {}

    def test_get_latest_parsed(self, requests_mock):
        api = BAFUHydroAPI()
        requests_mock.get(f"{EXISTENZ_BASE_URL}/latest", json=SAMPLE_LATEST_RESPONSE)
        latest = api.get_latest()
        assert len(latest) == 4
        assert latest[0]["loc"] == 2018

    def test_get_locations_http_error(self, requests_mock):
        api = BAFUHydroAPI()
        requests_mock.get(f"{EXISTENZ_BASE_URL}/locations", status_code=500)
        import requests as req
        with pytest.raises(req.HTTPError):
            api.get_locations()


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

class TestDataClasses:
    def test_station_roundtrip(self):
        st = Station(
            station_id="2018",
            name="Rhein - Basel",
            water_body_name="Rhein",
            water_body_type="river",
            latitude=47.5596,
            longitude=7.5886,
        )
        assert st.station_id == "2018"
        assert st.latitude == 47.5596
        data = json.loads(st.to_json())
        assert data["station_id"] == "2018"
        assert data["name"] == "Rhein - Basel"

    def test_water_level_observation_roundtrip(self):
        obs = WaterLevelObservation(
            station_id="2018",
            water_level=2.56,
            water_level_unit="m",
            water_level_timestamp="2023-11-14T22:13:20+00:00",
            discharge=1234.5,
            discharge_unit="m3/s",
            discharge_timestamp="2023-11-14T22:13:20+00:00",
            water_temperature=12.3,
            water_temperature_unit="C",
            water_temperature_timestamp="2023-11-14T22:13:20+00:00",
        )
        assert obs.station_id == "2018"
        assert obs.water_level == 2.56
        data = json.loads(obs.to_json())
        assert data["discharge"] == 1234.5

    def test_station_optional_fields_none(self):
        st = Station(
            station_id="999",
            name="Test",
            water_body_name=None,
            water_body_type=None,
            latitude=0.0,
            longitude=0.0,
        )
        assert st.water_body_name is None
        assert st.water_body_type is None


# ---------------------------------------------------------------------------
# send_stations
# ---------------------------------------------------------------------------

class TestSendStations:
    def _mock_producer(self):
        p = MagicMock(spec=CHBAFUHydrologyEventProducer)
        p.producer = MagicMock()
        return p

    @patch("bafu_hydro.bafu_hydro.BAFUHydroAPI.get_locations")
    def test_sends_all_stations(self, mock_locs):
        mock_locs.return_value = {
            "2018": {"name": "Rhein - Basel", "water-body-name": "Rhein",
                     "water-body-type": "river", "lat": 47.56, "lon": 7.59},
            "2030": {"name": "Aare - Bern", "water-body-name": "Aare",
                     "water-body-type": "river", "lat": 46.95, "lon": 7.45},
        }
        api = BAFUHydroAPI()
        prod = self._mock_producer()
        locs = send_stations(api, prod)
        assert prod.send_ch_bafu_hydrology_station.call_count == 2
        prod.producer.flush.assert_called_once()
        assert "2018" in locs

    @patch("bafu_hydro.bafu_hydro.BAFUHydroAPI.get_locations")
    def test_returns_empty_when_no_stations(self, mock_locs):
        mock_locs.return_value = {}
        api = BAFUHydroAPI()
        prod = self._mock_producer()
        locs = send_stations(api, prod)
        assert locs == {}
        prod.send_ch_bafu_hydrology_station.assert_not_called()


# ---------------------------------------------------------------------------
# feed_observations
# ---------------------------------------------------------------------------

class TestFeedObservations:
    def _mock_producer(self):
        p = MagicMock(spec=CHBAFUHydrologyEventProducer)
        p.producer = MagicMock()
        return p

    @patch("bafu_hydro.bafu_hydro.BAFUHydroAPI.get_latest")
    def test_sends_new_observations(self, mock_latest):
        mock_latest.return_value = SAMPLE_LATEST_RESPONSE["payload"]
        locations = {
            "2018": {"name": "Rhein - Basel"},
            "2030": {"name": "Aare - Bern"},
        }
        prod = self._mock_producer()
        api = BAFUHydroAPI()
        previous = {}
        count = feed_observations(api, prod, locations, previous)
        assert count == 2
        assert prod.send_ch_bafu_hydrology_water_level_observation.call_count == 2
        prod.producer.flush.assert_called_once()

    @patch("bafu_hydro.bafu_hydro.BAFUHydroAPI.get_latest")
    def test_deduplicates_readings(self, mock_latest):
        mock_latest.return_value = SAMPLE_LATEST_RESPONSE["payload"]
        locations = {"2018": {}, "2030": {}}
        prod = self._mock_producer()
        api = BAFUHydroAPI()
        previous = {}
        feed_observations(api, prod, locations, previous)
        # Second call with same data — all readings are already in previous_readings
        prod.reset_mock()
        prod.producer = MagicMock()
        count = feed_observations(api, prod, locations, previous)
        assert count == 0
        prod.send_ch_bafu_hydrology_water_level_observation.assert_not_called()

    @patch("bafu_hydro.bafu_hydro.BAFUHydroAPI.get_latest")
    def test_skips_unknown_stations(self, mock_latest):
        mock_latest.return_value = SAMPLE_LATEST_RESPONSE["payload"]
        # locations dict only contains 2030
        locations = {"2030": {}}
        prod = self._mock_producer()
        api = BAFUHydroAPI()
        count = feed_observations(api, prod, locations, {})
        assert count == 1

    @patch("bafu_hydro.bafu_hydro.BAFUHydroAPI.get_latest")
    def test_skips_null_values(self, mock_latest):
        mock_latest.return_value = [{"loc": 2018, "par": PAR_HEIGHT, "val": None, "timestamp": 1700000000}]
        locations = {"2018": {}}
        prod = self._mock_producer()
        api = BAFUHydroAPI()
        count = feed_observations(api, prod, locations, {})
        assert count == 0

    @patch("bafu_hydro.bafu_hydro.BAFUHydroAPI.get_latest")
    def test_empty_latest_returns_zero(self, mock_latest):
        mock_latest.return_value = []
        prod = self._mock_producer()
        api = BAFUHydroAPI()
        count = feed_observations(api, prod, {"2018": {}}, {})
        assert count == 0


# ---------------------------------------------------------------------------
# Producer client (Kafka produce path)
# ---------------------------------------------------------------------------

class TestProducerClient:
    def test_send_station_calls_produce(self):
        mock_kafka = MagicMock()
        prod = CHBAFUHydrologyEventProducer(mock_kafka, "bafu-topic")
        st = Station(station_id="2018", name="Rhein", water_body_name=None,
                     water_body_type=None, latitude=47.56, longitude=7.59)
        prod.send_ch_bafu_hydrology_station("2018", st)
        mock_kafka.produce.assert_called_once()
        mock_kafka.flush.assert_called_once()

    def test_send_observation_calls_produce(self):
        mock_kafka = MagicMock()
        prod = CHBAFUHydrologyEventProducer(mock_kafka, "bafu-topic")
        obs = WaterLevelObservation(
            station_id="2018",
            water_level=2.56, water_level_unit="m",
            water_level_timestamp="2023-11-14T22:13:20+00:00",
            discharge=None, discharge_unit="m3/s", discharge_timestamp="",
            water_temperature=None, water_temperature_unit="C",
            water_temperature_timestamp="",
        )
        prod.send_ch_bafu_hydrology_water_level_observation("2018", obs)
        mock_kafka.produce.assert_called_once()

    def test_no_flush_when_disabled(self):
        mock_kafka = MagicMock()
        prod = CHBAFUHydrologyEventProducer(mock_kafka, "bafu-topic")
        st = Station(station_id="2018", name="Rhein", water_body_name=None,
                     water_body_type=None, latitude=47.56, longitude=7.59)
        prod.send_ch_bafu_hydrology_station("2018", st, flush_producer=False)
        mock_kafka.produce.assert_called_once()
        mock_kafka.flush.assert_not_called()

    def test_binary_content_mode(self):
        mock_kafka = MagicMock()
        prod = CHBAFUHydrologyEventProducer(mock_kafka, "bafu-topic", content_mode="binary")
        st = Station(station_id="2018", name="Rhein", water_body_name=None,
                     water_body_type=None, latitude=47.56, longitude=7.59)
        prod.send_ch_bafu_hydrology_station("2018", st)
        mock_kafka.produce.assert_called_once()
        # binary mode produces a string key while structured mode produces bytes
        call_kwargs = mock_kafka.produce.call_args
        assert call_kwargs[1]["key"] in (b"2018", "2018")

    def test_kafka_key_matches_station_id(self):
        mock_kafka = MagicMock()
        prod = CHBAFUHydrologyEventProducer(mock_kafka, "bafu-topic")
        st = Station(station_id="2018", name="Rhein", water_body_name=None,
                     water_body_type=None, latitude=47.56, longitude=7.59)
        prod.send_ch_bafu_hydrology_station("2018", st)
        call_kwargs = mock_kafka.produce.call_args
        key = call_kwargs[1]["key"]
        assert key in (b"2018", "2018")
