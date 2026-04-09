"""Integration tests for VATSIM bridge with mocked API."""

import datetime
import json
import pytest
import requests_mock
from unittest.mock import MagicMock, patch
from vatsim.vatsim import VatsimBridge, VATSIM_DATA_URL


MOCK_VATSIM_DATA = {
    "general": {
        "version": 3,
        "reload": 1,
        "update": "20260409022354",
        "update_timestamp": "2026-04-09T02:23:54.1820452Z",
        "connected_clients": 853,
        "unique_users": 795
    },
    "pilots": [
        {
            "cid": 1020616,
            "callsign": "AAL9615",
            "pilot_rating": 15,
            "latitude": 35.7678,
            "longitude": 141.33981,
            "altitude": 26010,
            "groundspeed": 426,
            "transponder": "2000",
            "heading": 269,
            "qnh_mb": 1021,
            "flight_plan": {
                "flight_rules": "I",
                "aircraft_short": "B772",
                "departure": "KORD",
                "arrival": "RJAA",
                "altitude": "36000",
                "route": "PMPKN NEATO"
            },
            "last_updated": "2026-04-09T02:23:51.7336228Z"
        },
        {
            "cid": 999999,
            "callsign": "N12345",
            "pilot_rating": 0,
            "latitude": 40.6413,
            "longitude": -73.7781,
            "altitude": 0,
            "groundspeed": 0,
            "transponder": "1200",
            "heading": 90,
            "qnh_mb": 1013,
            "flight_plan": None,
            "last_updated": "2026-04-09T02:00:00Z"
        }
    ],
    "controllers": [
        {
            "cid": 1328632,
            "callsign": "EGLL_TWR",
            "frequency": "118.500",
            "facility": 4,
            "rating": 5,
            "text_atis": ["EGLL INFO A", "RWY 27L/27R"],
            "last_updated": "2026-04-09T02:23:48.8368139Z"
        }
    ],
    "atis": [],
    "servers": [],
    "prefiles": []
}


@pytest.mark.integration
class TestFetchData:
    """Test fetching data from mock API."""

    def test_fetch_data_success(self):
        bridge = VatsimBridge()
        with requests_mock.Mocker() as m:
            m.get(VATSIM_DATA_URL, json=MOCK_VATSIM_DATA)
            data = bridge.fetch_data()
            assert "general" in data
            assert "pilots" in data
            assert "controllers" in data
            assert len(data["pilots"]) == 2
            assert len(data["controllers"]) == 1

    def test_fetch_data_timeout(self):
        import requests
        bridge = VatsimBridge()
        with requests_mock.Mocker() as m:
            m.get(VATSIM_DATA_URL, exc=requests.exceptions.ConnectTimeout)
            with pytest.raises(requests.exceptions.ConnectTimeout):
                bridge.fetch_data()

    def test_fetch_data_http_error(self):
        import requests
        bridge = VatsimBridge()
        with requests_mock.Mocker() as m:
            m.get(VATSIM_DATA_URL, status_code=500)
            with pytest.raises(requests.exceptions.HTTPError):
                bridge.fetch_data()


@pytest.mark.integration
class TestParseMockData:
    """Test parsing of full mock data."""

    def test_parse_all_pilots(self):
        bridge = VatsimBridge()
        pilots = [bridge.parse_pilot(p) for p in MOCK_VATSIM_DATA["pilots"]]
        assert len(pilots) == 2
        assert pilots[0].callsign == "AAL9615"
        assert pilots[1].callsign == "N12345"

    def test_parse_all_controllers(self):
        bridge = VatsimBridge()
        controllers = [bridge.parse_controller(c) for c in MOCK_VATSIM_DATA["controllers"]]
        assert len(controllers) == 1
        assert controllers[0].callsign == "EGLL_TWR"

    def test_parse_general_to_status(self):
        bridge = VatsimBridge()
        status = bridge.build_network_status(
            MOCK_VATSIM_DATA["general"],
            len(MOCK_VATSIM_DATA["pilots"]),
            len(MOCK_VATSIM_DATA["controllers"])
        )
        assert status.pilot_count == 2
        assert status.controller_count == 1
        assert status.connected_clients == 853


@pytest.mark.integration
class TestDedupLogic:
    """Test dedup logic with mock data."""

    def test_dedup_skips_unchanged_pilots(self):
        bridge = VatsimBridge()
        pilot = MOCK_VATSIM_DATA["pilots"][0]
        fp1 = bridge.pilot_fingerprint(pilot)
        fp2 = bridge.pilot_fingerprint(pilot)
        assert fp1 == fp2

    def test_dedup_detects_changed_pilots(self):
        bridge = VatsimBridge()
        pilot = dict(MOCK_VATSIM_DATA["pilots"][0])
        fp1 = bridge.pilot_fingerprint(pilot)
        pilot["latitude"] = 36.0
        fp2 = bridge.pilot_fingerprint(pilot)
        assert fp1 != fp2

    def test_dedup_skips_unchanged_controllers(self):
        bridge = VatsimBridge()
        ctrl = MOCK_VATSIM_DATA["controllers"][0]
        fp1 = bridge.controller_fingerprint(ctrl)
        fp2 = bridge.controller_fingerprint(ctrl)
        assert fp1 == fp2

    def test_dedup_detects_changed_controllers(self):
        bridge = VatsimBridge()
        ctrl = dict(MOCK_VATSIM_DATA["controllers"][0])
        fp1 = bridge.controller_fingerprint(ctrl)
        ctrl["frequency"] = "119.000"
        fp2 = bridge.controller_fingerprint(ctrl)
        assert fp1 != fp2


@pytest.mark.integration
class TestFullParsePipeline:
    """Test complete parse pipeline from raw data to data classes."""

    def test_pilot_round_trip_json(self):
        bridge = VatsimBridge()
        pilot = bridge.parse_pilot(MOCK_VATSIM_DATA["pilots"][0])
        json_str = pilot.to_json()
        data = json.loads(json_str)
        assert data["callsign"] == "AAL9615"
        assert data["cid"] == 1020616
        assert data["flight_rules"] == "I"

    def test_controller_round_trip_json(self):
        bridge = VatsimBridge()
        ctrl = bridge.parse_controller(MOCK_VATSIM_DATA["controllers"][0])
        json_str = ctrl.to_json()
        data = json.loads(json_str)
        assert data["callsign"] == "EGLL_TWR"
        assert "EGLL INFO A" in data["text_atis"]

    def test_status_round_trip_json(self):
        bridge = VatsimBridge()
        status = bridge.build_network_status(
            MOCK_VATSIM_DATA["general"], 2, 1
        )
        json_str = status.to_json()
        data = json.loads(json_str)
        assert data["callsign"] == "status"
        assert data["pilot_count"] == 2
