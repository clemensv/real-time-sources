"""Unit tests for VATSIM bridge - no external dependencies."""

import datetime
import json
import pytest
from unittest.mock import MagicMock
from vatsim.vatsim import VatsimBridge, _load_state, _save_state


SAMPLE_PILOT = {
    "cid": 1020616,
    "name": "Ryan Pitt KICT",
    "callsign": "AAL9615",
    "server": "USA-SE",
    "pilot_rating": 15,
    "latitude": 35.7678,
    "longitude": 141.33981,
    "altitude": 26010,
    "groundspeed": 426,
    "transponder": "2000",
    "heading": 269,
    "qnh_i_hg": 30.16,
    "qnh_mb": 1021,
    "flight_plan": {
        "flight_rules": "I",
        "aircraft": "B772/H-SDE2E3FGHIJ5LORVWXY/LB1D1",
        "aircraft_faa": "H/B772/L",
        "aircraft_short": "B772",
        "departure": "KORD",
        "arrival": "RJAA",
        "alternate": "RJTT",
        "cruise_tas": "481",
        "altitude": "36000",
        "deptime": "1400",
        "enroute_time": "1241",
        "fuel_time": "1522",
        "remarks": "PBN/A1B1D1S2T1",
        "route": "PMPKN NEATO DLLAN",
        "revision_id": 3,
        "assigned_transponder": "0617"
    },
    "logon_time": "2026-04-08T13:45:10Z",
    "last_updated": "2026-04-09T02:23:51.7336228Z"
}

SAMPLE_PILOT_NO_FP = {
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

SAMPLE_CONTROLLER = {
    "cid": 1328632,
    "name": "1328632",
    "callsign": "EGLL_TWR",
    "frequency": "118.500",
    "facility": 4,
    "rating": 5,
    "server": "UK",
    "visual_range": 50,
    "text_atis": ["EGLL INFO A", "RWY 27L/27R IN USE", "QNH 1013"],
    "last_updated": "2026-04-09T02:23:48.8368139Z",
    "logon_time": "2026-04-08T19:19:47Z"
}

SAMPLE_CONTROLLER_NO_ATIS = {
    "cid": 1111111,
    "callsign": "FFT1755",
    "frequency": "199.998",
    "facility": 0,
    "rating": 1,
    "text_atis": None,
    "last_updated": "2026-04-09T02:23:48Z"
}

SAMPLE_GENERAL = {
    "version": 3,
    "reload": 1,
    "update": "20260409022354",
    "update_timestamp": "2026-04-09T02:23:54.1820452Z",
    "connected_clients": 853,
    "unique_users": 795
}


@pytest.mark.unit
class TestVatsimBridgeInit:
    """Test VatsimBridge initialization."""

    def test_creates_session(self):
        bridge = VatsimBridge()
        assert bridge.session is not None

    def test_custom_session(self):
        mock_session = MagicMock()
        bridge = VatsimBridge(session=mock_session)
        assert bridge.session is mock_session


@pytest.mark.unit
class TestParsePilot:
    """Test pilot parsing."""

    def test_parse_pilot_with_flight_plan(self):
        pilot = VatsimBridge.parse_pilot(SAMPLE_PILOT)
        assert pilot.cid == 1020616
        assert pilot.callsign == "AAL9615"
        assert pilot.latitude == 35.7678
        assert pilot.longitude == 141.33981
        assert pilot.altitude == 26010
        assert pilot.groundspeed == 426
        assert pilot.heading == 269
        assert pilot.transponder == "2000"
        assert pilot.qnh_mb == 1021
        assert pilot.flight_rules == "I"
        assert pilot.aircraft_short == "B772"
        assert pilot.departure == "KORD"
        assert pilot.arrival == "RJAA"
        assert pilot.route == "PMPKN NEATO DLLAN"
        assert pilot.cruise_altitude == "36000"
        assert pilot.pilot_rating == 15
        assert isinstance(pilot.last_updated, datetime.datetime)

    def test_parse_pilot_no_flight_plan(self):
        pilot = VatsimBridge.parse_pilot(SAMPLE_PILOT_NO_FP)
        assert pilot.cid == 999999
        assert pilot.callsign == "N12345"
        assert pilot.flight_rules is None
        assert pilot.aircraft_short is None
        assert pilot.departure is None
        assert pilot.arrival is None
        assert pilot.route is None
        assert pilot.cruise_altitude is None

    def test_parse_pilot_returns_correct_type(self):
        from vatsim_producer_data.net.vatsim.pilotposition import PilotPosition
        pilot = VatsimBridge.parse_pilot(SAMPLE_PILOT)
        assert isinstance(pilot, PilotPosition)

    def test_parse_pilot_last_updated_is_datetime(self):
        pilot = VatsimBridge.parse_pilot(SAMPLE_PILOT)
        assert isinstance(pilot.last_updated, datetime.datetime)
        assert pilot.last_updated.year == 2026

    def test_parse_pilot_qnh_mb_default(self):
        raw = dict(SAMPLE_PILOT)
        del raw["qnh_mb"]
        pilot = VatsimBridge.parse_pilot(raw)
        assert pilot.qnh_mb == 0


@pytest.mark.unit
class TestParseController:
    """Test controller parsing."""

    def test_parse_controller_with_atis(self):
        ctrl = VatsimBridge.parse_controller(SAMPLE_CONTROLLER)
        assert ctrl.cid == 1328632
        assert ctrl.callsign == "EGLL_TWR"
        assert ctrl.frequency == "118.500"
        assert ctrl.facility == 4
        assert ctrl.rating == 5
        assert ctrl.text_atis == "EGLL INFO A\nRWY 27L/27R IN USE\nQNH 1013"
        assert isinstance(ctrl.last_updated, datetime.datetime)

    def test_parse_controller_no_atis(self):
        ctrl = VatsimBridge.parse_controller(SAMPLE_CONTROLLER_NO_ATIS)
        assert ctrl.text_atis is None

    def test_parse_controller_returns_correct_type(self):
        from vatsim_producer_data.net.vatsim.controllerposition import ControllerPosition
        ctrl = VatsimBridge.parse_controller(SAMPLE_CONTROLLER)
        assert isinstance(ctrl, ControllerPosition)

    def test_parse_controller_empty_atis_list(self):
        raw = dict(SAMPLE_CONTROLLER)
        raw["text_atis"] = []
        ctrl = VatsimBridge.parse_controller(raw)
        assert ctrl.text_atis is None

    def test_parse_controller_atis_string(self):
        raw = dict(SAMPLE_CONTROLLER)
        raw["text_atis"] = "Single line ATIS"
        ctrl = VatsimBridge.parse_controller(raw)
        assert ctrl.text_atis == "Single line ATIS"


@pytest.mark.unit
class TestBuildNetworkStatus:
    """Test network status construction."""

    def test_build_network_status(self):
        status = VatsimBridge.build_network_status(SAMPLE_GENERAL, 720, 73)
        assert status.callsign == "status"
        assert status.connected_clients == 853
        assert status.unique_users == 795
        assert status.pilot_count == 720
        assert status.controller_count == 73
        assert isinstance(status.update_timestamp, datetime.datetime)

    def test_build_network_status_type(self):
        from vatsim_producer_data.net.vatsim.networkstatus import NetworkStatus
        status = VatsimBridge.build_network_status(SAMPLE_GENERAL, 100, 10)
        assert isinstance(status, NetworkStatus)


@pytest.mark.unit
class TestDeduplication:
    """Test fingerprint and dedup logic."""

    def test_pilot_fingerprint_format(self):
        fp = VatsimBridge.pilot_fingerprint(SAMPLE_PILOT)
        assert "35.7678" in fp
        assert "141.33981" in fp
        assert "26010" in fp
        assert "426" in fp
        assert "269" in fp

    def test_pilot_fingerprint_changes_on_position_change(self):
        fp1 = VatsimBridge.pilot_fingerprint(SAMPLE_PILOT)
        modified = dict(SAMPLE_PILOT)
        modified["latitude"] = 36.0
        fp2 = VatsimBridge.pilot_fingerprint(modified)
        assert fp1 != fp2

    def test_pilot_fingerprint_same_for_same_data(self):
        fp1 = VatsimBridge.pilot_fingerprint(SAMPLE_PILOT)
        fp2 = VatsimBridge.pilot_fingerprint(SAMPLE_PILOT)
        assert fp1 == fp2

    def test_controller_fingerprint_format(self):
        fp = VatsimBridge.controller_fingerprint(SAMPLE_CONTROLLER)
        assert "118.500" in fp
        assert "4" in fp
        assert "5" in fp

    def test_controller_fingerprint_changes_on_frequency_change(self):
        fp1 = VatsimBridge.controller_fingerprint(SAMPLE_CONTROLLER)
        modified = dict(SAMPLE_CONTROLLER)
        modified["frequency"] = "119.000"
        fp2 = VatsimBridge.controller_fingerprint(modified)
        assert fp1 != fp2


@pytest.mark.unit
class TestConnectionStringParsing:
    """Test connection string parsing."""

    def test_parse_event_hubs_connection_string(self):
        bridge = VatsimBridge()
        cs = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123==;"
            "EntityPath=myeventhub"
        )
        result = bridge.parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'myeventhub'
        assert result['sasl.username'] == '$ConnectionString'

    def test_parse_plain_bootstrap_connection_string(self):
        bridge = VatsimBridge()
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = bridge.parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'test-topic'
        assert 'sasl.username' not in result

    def test_parse_connection_string_endpoint_extraction(self):
        bridge = VatsimBridge()
        cs = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic1"
        result = bridge.parse_connection_string(cs)
        assert 'test.servicebus.windows.net:9093' == result['bootstrap.servers']

    def test_parse_connection_string_invalid_raises(self):
        bridge = VatsimBridge()
        with pytest.raises(ValueError, match="Invalid connection string format"):
            bridge.parse_connection_string("EndpointWithoutEquals")


@pytest.mark.unit
class TestStateManagement:
    """Test state load/save."""

    def test_load_state_missing_file(self):
        state = _load_state("nonexistent_file.json")
        assert state == {}

    def test_load_state_empty_path(self):
        state = _load_state("")
        assert state == {}

    def test_save_state_empty_path(self):
        _save_state("", {"test": "data"})  # Should not raise

    def test_save_and_load_state(self, tmp_path):
        state_file = str(tmp_path / "state.json")
        test_state = {"pilots": {"AAL123": "fp1"}, "controllers": {"EGLL_TWR": "fp2"}}
        _save_state(state_file, test_state)
        loaded = _load_state(state_file)
        assert loaded == test_state


@pytest.mark.unit
class TestPilotPositionSerialization:
    """Test PilotPosition data class serialization."""

    def test_pilot_to_json(self):
        pilot = VatsimBridge.parse_pilot(SAMPLE_PILOT)
        json_str = pilot.to_json()
        data = json.loads(json_str)
        assert data["callsign"] == "AAL9615"
        assert data["cid"] == 1020616

    def test_pilot_to_serializer_dict(self):
        pilot = VatsimBridge.parse_pilot(SAMPLE_PILOT)
        d = pilot.to_serializer_dict()
        assert d["callsign"] == "AAL9615"
        assert d["latitude"] == 35.7678

    def test_pilot_nullable_fields_in_dict(self):
        pilot = VatsimBridge.parse_pilot(SAMPLE_PILOT_NO_FP)
        d = pilot.to_serializer_dict()
        assert d["flight_rules"] is None
        assert d["departure"] is None


@pytest.mark.unit
class TestControllerPositionSerialization:
    """Test ControllerPosition data class serialization."""

    def test_controller_to_json(self):
        ctrl = VatsimBridge.parse_controller(SAMPLE_CONTROLLER)
        json_str = ctrl.to_json()
        data = json.loads(json_str)
        assert data["callsign"] == "EGLL_TWR"
        assert data["frequency"] == "118.500"

    def test_controller_nullable_atis_in_dict(self):
        ctrl = VatsimBridge.parse_controller(SAMPLE_CONTROLLER_NO_ATIS)
        d = ctrl.to_serializer_dict()
        assert d["text_atis"] is None


@pytest.mark.unit
class TestNetworkStatusSerialization:
    """Test NetworkStatus data class serialization."""

    def test_status_to_json(self):
        status = VatsimBridge.build_network_status(SAMPLE_GENERAL, 720, 73)
        json_str = status.to_json()
        data = json.loads(json_str)
        assert data["callsign"] == "status"
        assert data["pilot_count"] == 720

    def test_status_to_serializer_dict(self):
        status = VatsimBridge.build_network_status(SAMPLE_GENERAL, 100, 10)
        d = status.to_serializer_dict()
        assert d["connected_clients"] == 853
        assert d["unique_users"] == 795
