"""Unit tests for the SYKE Hydro bridge."""

import json
import os
import pytest
from unittest.mock import MagicMock, patch

from syke_hydro.syke_hydro import (
    SYKEHydroAPI,
    parse_connection_string,
    _load_state,
    _save_state,
    _parse_dms,
    _get_latest_per_station,
    send_stations,
    feed_observations,
    SYKE_BASE_URL,
)
from syke_hydro_producer_data.fi.syke.hydrology.station import Station
from syke_hydro_producer_data.fi.syke.hydrology.waterlevelobservation import WaterLevelObservation
from syke_hydro_producer_kafka_producer.producer import FISYKEHydrologyEventProducer


# ---------------------------------------------------------------------------
# Sample API payloads
# ---------------------------------------------------------------------------

SAMPLE_STATION_1 = {
    "Paikka_Id": 1001,
    "Nimi": "Äänekoski",
    "PaaVesalNimi": "Äänekosken kanava",
    "VesalNimi": "Keitele",
    "KuntaNimi": "Äänekoski",
    "KoordLat": "623212",   # 62°32'12" -> ~62.537
    "KoordLong": "255943",  # 25°59'43" -> ~25.995
}

SAMPLE_STATION_2 = {
    "Paikka_Id": 2002,
    "Nimi": "Tampere",
    "PaaVesalNimi": "Kokemäenjoki",
    "VesalNimi": "Näsijärvi",
    "KuntaNimi": "Tampere",
    "KoordLat": "613006",
    "KoordLong": "234556",
}

SAMPLE_WATER_LEVELS = [
    {"Paikka_Id": 1001, "Arvo": 92.34, "Aika": "2023-11-14T10:00:00"},
    {"Paikka_Id": 1001, "Arvo": 92.45, "Aika": "2023-11-14T12:00:00"},
    {"Paikka_Id": 2002, "Arvo": 57.80, "Aika": "2023-11-14T11:00:00"},
]

SAMPLE_DISCHARGE = [
    {"Paikka_Id": 1001, "Arvo": 15.3, "Aika": "2023-11-14T12:00:00"},
]


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
        cs = "BootstrapServer=broker:9092;EntityPath=syke-topic"
        cfg = parse_connection_string(cs)
        assert cfg["_entity_path"] == "syke-topic"

    def test_empty_string(self):
        assert parse_connection_string("") == {}

    def test_no_sasl_for_plain_bootstrap(self):
        cfg = parse_connection_string("BootstrapServer=b:9092")
        assert "security.protocol" not in cfg


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------

class TestStateHelpers:
    def test_load_missing_file(self, tmp_path):
        assert _load_state(str(tmp_path / "nope.json")) == {}

    def test_load_none(self):
        assert _load_state(None) == {}

    def test_save_and_reload(self, tmp_path):
        path = str(tmp_path / "state.json")
        data = {"1001:2023-11-14T12:00:00:": "2023-11-14T12:00:00"}
        _save_state(path, data)
        assert _load_state(path) == data

    def test_save_trims_large_state(self, tmp_path):
        path = str(tmp_path / "big.json")
        data = {str(i): "ts" for i in range(200000)}
        _save_state(path, data)
        assert len(_load_state(path)) == 50000

    def test_save_none_path_noop(self):
        _save_state(None, {"a": "b"})  # must not raise

    def test_save_creates_file(self, tmp_path):
        path = str(tmp_path / "out.json")
        _save_state(path, {"x": "y"})
        assert os.path.exists(path)


# ---------------------------------------------------------------------------
# _parse_dms coordinate conversion
# ---------------------------------------------------------------------------

class TestParseDMS:
    def test_six_char_latitude(self):
        result = _parse_dms("623212")
        assert abs(result - (62 + 32/60 + 12/3600)) < 1e-9

    def test_seven_char_longitude(self):
        result = _parse_dms("0255943")
        assert abs(result - (25 + 59/60 + 43/3600)) < 1e-9

    def test_empty_string(self):
        assert _parse_dms("") == 0.0

    def test_whitespace_only(self):
        assert _parse_dms("   ") == 0.0

    def test_decimal_fallback(self):
        assert _parse_dms("62.5") == pytest.approx(62.5)

    def test_invalid_non_numeric(self):
        # Non-numeric 6-char string triggers int() ValueError — expect 0.0 via fallback
        # (real SYKE coordinates are always numeric; this exercises the else/float path)
        assert _parse_dms("1.2.3") == 0.0

    def test_zero_degrees(self):
        assert _parse_dms("000000") == 0.0


# ---------------------------------------------------------------------------
# _get_latest_per_station
# ---------------------------------------------------------------------------

class TestGetLatestPerStation:
    def test_keeps_latest_by_aika(self):
        latest = _get_latest_per_station(SAMPLE_WATER_LEVELS)
        assert latest[1001]["Aika"] == "2023-11-14T12:00:00"
        assert latest[1001]["Arvo"] == 92.45

    def test_single_entry(self):
        readings = [{"Paikka_Id": 5, "Arvo": 10.0, "Aika": "2023-01-01T00:00:00"}]
        latest = _get_latest_per_station(readings)
        assert 5 in latest
        assert latest[5]["Arvo"] == 10.0

    def test_missing_paikka_id_skipped(self):
        readings = [{"Arvo": 5.0, "Aika": "2023-01-01T00:00:00"}]
        assert _get_latest_per_station(readings) == {}

    def test_empty_list(self):
        assert _get_latest_per_station([]) == {}

    def test_multiple_stations(self):
        latest = _get_latest_per_station(SAMPLE_WATER_LEVELS)
        assert 1001 in latest
        assert 2002 in latest


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------

class TestSYKEHydroAPI:
    def test_default_base_url(self):
        api = SYKEHydroAPI()
        assert api.base_url == SYKE_BASE_URL

    def test_get_stations_calls_paikka(self, requests_mock):
        api = SYKEHydroAPI()
        requests_mock.get(
            f"{SYKE_BASE_URL}/Paikka",
            json={"value": [SAMPLE_STATION_1, SAMPLE_STATION_2]},
        )
        stations = api.get_stations()
        assert len(stations) == 2
        assert stations[0]["Paikka_Id"] == 1001

    def test_get_water_levels(self, requests_mock):
        api = SYKEHydroAPI()
        requests_mock.get(
            f"{SYKE_BASE_URL}/Vedenkorkeus",
            json={"value": SAMPLE_WATER_LEVELS},
        )
        result = api.get_water_levels("2023-11-14")
        assert len(result) == 3

    def test_get_discharge(self, requests_mock):
        api = SYKEHydroAPI()
        requests_mock.get(
            f"{SYKE_BASE_URL}/Virtaama",
            json={"value": SAMPLE_DISCHARGE},
        )
        result = api.get_discharge("2023-11-14")
        assert len(result) == 1

    def test_odata_pagination(self, requests_mock):
        api = SYKEHydroAPI()
        page2_url = f"{SYKE_BASE_URL}/Paikka?$skip=2"
        requests_mock.get(
            f"{SYKE_BASE_URL}/Paikka",
            json={"value": [SAMPLE_STATION_1], "odata.nextLink": page2_url},
        )
        requests_mock.get(
            page2_url,
            json={"value": [SAMPLE_STATION_2]},
        )
        stations = api.get_stations()
        assert len(stations) == 2

    def test_http_error_propagates(self, requests_mock):
        api = SYKEHydroAPI()
        requests_mock.get(f"{SYKE_BASE_URL}/Paikka", status_code=503)
        import requests as req
        with pytest.raises(req.HTTPError):
            api.get_stations()


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

class TestDataClasses:
    def test_station_roundtrip(self):
        st = Station(
            station_id="1001",
            name="Äänekoski",
            river_name="Äänekosken kanava",
            water_area_name="Keitele",
            municipality="Äänekoski",
            latitude=62.537,
            longitude=25.995,
        )
        assert st.station_id == "1001"
        data = json.loads(st.to_json())
        assert data["name"] == "Äänekoski"

    def test_station_optional_nulls(self):
        st = Station(
            station_id="999",
            name="Test",
            river_name=None,
            water_area_name=None,
            municipality=None,
            latitude=0.0,
            longitude=0.0,
        )
        assert st.river_name is None

    def test_observation_roundtrip(self):
        obs = WaterLevelObservation(
            station_id="1001",
            water_level=92.45,
            water_level_unit="cm",
            water_level_timestamp="2023-11-14T12:00:00",
            discharge=15.3,
            discharge_unit="m3/s",
            discharge_timestamp="2023-11-14T12:00:00",
        )
        assert obs.station_id == "1001"
        data = json.loads(obs.to_json())
        assert data["water_level"] == 92.45


# ---------------------------------------------------------------------------
# send_stations
# ---------------------------------------------------------------------------

class TestSendStations:
    def _mock_producer(self):
        p = MagicMock(spec=FISYKEHydrologyEventProducer)
        p.producer = MagicMock()
        return p

    @patch.object(SYKEHydroAPI, "get_stations")
    def test_sends_all_stations(self, mock_gs):
        mock_gs.return_value = [SAMPLE_STATION_1, SAMPLE_STATION_2]
        api = SYKEHydroAPI()
        prod = self._mock_producer()
        by_id = send_stations(api, prod)
        assert prod.send_fi_syke_hydrology_station.call_count == 2
        prod.producer.flush.assert_called_once()
        assert 1001 in by_id
        assert 2002 in by_id

    @patch.object(SYKEHydroAPI, "get_stations")
    def test_dms_coordinates_converted(self, mock_gs):
        mock_gs.return_value = [SAMPLE_STATION_1]
        api = SYKEHydroAPI()
        prod = self._mock_producer()
        send_stations(api, prod)
        call_args = prod.send_fi_syke_hydrology_station.call_args
        station_data = call_args[1]["data"]
        assert station_data.latitude == pytest.approx(62 + 32/60 + 12/3600, abs=1e-4)

    @patch.object(SYKEHydroAPI, "get_stations")
    def test_skips_station_without_paikka_id(self, mock_gs):
        mock_gs.return_value = [{"Nimi": "No ID", "KoordLat": "623212", "KoordLong": "255943"}]
        api = SYKEHydroAPI()
        prod = self._mock_producer()
        result = send_stations(api, prod)
        assert result == {}
        prod.send_fi_syke_hydrology_station.assert_not_called()

    @patch.object(SYKEHydroAPI, "get_stations")
    def test_empty_station_list(self, mock_gs):
        mock_gs.return_value = []
        api = SYKEHydroAPI()
        prod = self._mock_producer()
        assert send_stations(api, prod) == {}


# ---------------------------------------------------------------------------
# feed_observations
# ---------------------------------------------------------------------------

class TestFeedObservations:
    def _mock_producer(self):
        p = MagicMock(spec=FISYKEHydrologyEventProducer)
        p.producer = MagicMock()
        return p

    @patch.object(SYKEHydroAPI, "get_discharge")
    @patch.object(SYKEHydroAPI, "get_water_levels")
    def test_sends_new_observations(self, mock_wl, mock_q):
        mock_wl.return_value = SAMPLE_WATER_LEVELS
        mock_q.return_value = SAMPLE_DISCHARGE
        stations_by_id = {1001: SAMPLE_STATION_1, 2002: SAMPLE_STATION_2}
        prod = self._mock_producer()
        api = SYKEHydroAPI()
        previous = {}
        count = feed_observations(api, prod, stations_by_id, previous)
        assert count == 2
        assert prod.send_fi_syke_hydrology_water_level_observation.call_count == 2

    @patch.object(SYKEHydroAPI, "get_discharge")
    @patch.object(SYKEHydroAPI, "get_water_levels")
    def test_deduplicates_readings(self, mock_wl, mock_q):
        mock_wl.return_value = SAMPLE_WATER_LEVELS
        mock_q.return_value = SAMPLE_DISCHARGE
        stations_by_id = {1001: SAMPLE_STATION_1}
        prod = self._mock_producer()
        api = SYKEHydroAPI()
        previous = {}
        feed_observations(api, prod, stations_by_id, previous)
        prod.reset_mock()
        prod.producer = MagicMock()
        count = feed_observations(api, prod, stations_by_id, previous)
        assert count == 0

    @patch.object(SYKEHydroAPI, "get_discharge")
    @patch.object(SYKEHydroAPI, "get_water_levels")
    def test_skips_unknown_stations(self, mock_wl, mock_q):
        mock_wl.return_value = SAMPLE_WATER_LEVELS
        mock_q.return_value = []
        # Only 2002 in stations_by_id
        stations_by_id = {2002: SAMPLE_STATION_2}
        prod = self._mock_producer()
        api = SYKEHydroAPI()
        count = feed_observations(api, prod, stations_by_id, {})
        assert count == 1

    @patch.object(SYKEHydroAPI, "get_discharge")
    @patch.object(SYKEHydroAPI, "get_water_levels")
    def test_empty_data_returns_zero(self, mock_wl, mock_q):
        mock_wl.return_value = []
        mock_q.return_value = []
        prod = self._mock_producer()
        api = SYKEHydroAPI()
        count = feed_observations(api, prod, {1001: SAMPLE_STATION_1}, {})
        assert count == 0


# ---------------------------------------------------------------------------
# Producer client
# ---------------------------------------------------------------------------

class TestProducerClient:
    def test_send_station_calls_produce(self):
        mock_kafka = MagicMock()
        prod = FISYKEHydrologyEventProducer(mock_kafka, "syke-topic")
        st = Station(
            station_id="1001", name="Äänekoski",
            river_name=None, water_area_name=None, municipality=None,
            latitude=62.537, longitude=25.995,
        )
        prod.send_fi_syke_hydrology_station("1001", st)
        mock_kafka.produce.assert_called_once()
        mock_kafka.flush.assert_called_once()

    def test_send_observation_calls_produce(self):
        mock_kafka = MagicMock()
        prod = FISYKEHydrologyEventProducer(mock_kafka, "syke-topic")
        obs = WaterLevelObservation(
            station_id="1001",
            water_level=92.45, water_level_unit="cm",
            water_level_timestamp="2023-11-14T12:00:00",
            discharge=None, discharge_unit="m3/s", discharge_timestamp="",
        )
        prod.send_fi_syke_hydrology_water_level_observation("1001", obs)
        mock_kafka.produce.assert_called_once()

    def test_no_flush_when_disabled(self):
        mock_kafka = MagicMock()
        prod = FISYKEHydrologyEventProducer(mock_kafka, "syke-topic")
        st = Station(
            station_id="1001", name="Test",
            river_name=None, water_area_name=None, municipality=None,
            latitude=0.0, longitude=0.0,
        )
        prod.send_fi_syke_hydrology_station("1001", st, flush_producer=False)
        mock_kafka.flush.assert_not_called()

    def test_kafka_key_matches_station_id(self):
        mock_kafka = MagicMock()
        prod = FISYKEHydrologyEventProducer(mock_kafka, "syke-topic")
        st = Station(
            station_id="1001", name="Test",
            river_name=None, water_area_name=None, municipality=None,
            latitude=0.0, longitude=0.0,
        )
        prod.send_fi_syke_hydrology_station("1001", st)
        call_kwargs = mock_kafka.produce.call_args
        key = call_kwargs[1]["key"]
        assert key in (b"1001", "1001")
