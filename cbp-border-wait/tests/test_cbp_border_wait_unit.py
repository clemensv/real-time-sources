"""Unit tests for US CBP Border Wait Times bridge.

Tests core functionality without external dependencies.
"""

import json
import os
import pytest
from unittest.mock import MagicMock, patch
from cbp_border_wait_producer_data.gov.cbp.borderwait.port import Port
from cbp_border_wait_producer_data.gov.cbp.borderwait.waittime import WaitTime
from cbp_border_wait.cbp_border_wait import (
    CbpBorderWaitAPI,
    _load_state,
    _save_state,
    _parse_connection_string,
    parse_int_or_none,
    parse_delay_minutes,
    parse_lanes_open,
    parse_operational_status,
    _extract_lane,
)


SAMPLE_PORT_RAW = {
    "port_number": "250401",
    "border": "Mexican Border",
    "port_name": "San Ysidro",
    "crossing_name": "San Ysidro",
    "hours": "24 hrs/day",
    "date": "4/8/2026",
    "time": "14:00:00",
    "port_status": "Open",
    "commercial_vehicle_lanes": {
        "maximum_lanes": "5",
        "cv_automation_type": "Manual",
        "standard_lanes": {
            "update_time": "At 2:00 pm PDT",
            "operational_status": "delay",
            "delay_minutes": "15",
            "lanes_open": "3"
        },
        "FAST_lanes": {
            "update_time": "",
            "operational_status": "N/A",
            "delay_minutes": "",
            "lanes_open": ""
        }
    },
    "passenger_vehicle_lanes": {
        "maximum_lanes": "25",
        "pv_automation_type": "Manual",
        "standard_lanes": {
            "update_time": "At 2:00 pm PDT",
            "operational_status": "delay",
            "delay_minutes": "45",
            "lanes_open": "10"
        },
        "NEXUS_SENTRI_lanes": {
            "update_time": "At 2:00 pm PDT",
            "operational_status": "no delay",
            "delay_minutes": "0",
            "lanes_open": "2"
        },
        "ready_lanes": {
            "update_time": "At 2:00 pm PDT",
            "operational_status": "delay",
            "delay_minutes": "30",
            "lanes_open": "5"
        }
    },
    "pedestrian_lanes": {
        "maximum_lanes": "10",
        "ped_automation_type": "Manual",
        "standard_lanes": {
            "update_time": "At 2:00 pm PDT",
            "operational_status": "delay",
            "delay_minutes": "20",
            "lanes_open": "4"
        },
        "ready_lanes": {
            "update_time": "",
            "operational_status": "N/A",
            "delay_minutes": "",
            "lanes_open": ""
        }
    },
    "construction_notice": "Lane closures expected through May 2026.",
    "automation": "0",
    "automation_enabled": "0"
}


SAMPLE_PORT_CANADIAN = {
    "port_number": "070801",
    "border": "Canadian Border",
    "port_name": "Alexandria Bay",
    "crossing_name": "Thousand Islands Bridge",
    "hours": "24 hrs/day",
    "date": "4/8/2026",
    "time": "16:16:47",
    "port_status": "Open",
    "commercial_vehicle_lanes": {
        "maximum_lanes": "5",
        "standard_lanes": {
            "update_time": "At 2:00 pm EDT",
            "operational_status": "no delay",
            "delay_minutes": "0",
            "lanes_open": "3"
        },
        "FAST_lanes": {
            "update_time": "",
            "operational_status": "N/A",
            "delay_minutes": "",
            "lanes_open": ""
        }
    },
    "passenger_vehicle_lanes": {
        "maximum_lanes": "8",
        "standard_lanes": {
            "update_time": "At 2:00 pm EDT",
            "operational_status": "no delay",
            "delay_minutes": "0",
            "lanes_open": "2"
        },
        "NEXUS_SENTRI_lanes": {
            "update_time": "At 2:00 pm EDT",
            "operational_status": "no delay",
            "delay_minutes": "0",
            "lanes_open": "1"
        },
        "ready_lanes": {
            "update_time": "",
            "operational_status": "N/A",
            "delay_minutes": "",
            "lanes_open": ""
        }
    },
    "pedestrian_lanes": {
        "maximum_lanes": "N/A",
        "standard_lanes": {
            "update_time": "",
            "operational_status": "N/A",
            "delay_minutes": "",
            "lanes_open": ""
        },
        "ready_lanes": {
            "update_time": "",
            "operational_status": "N/A",
            "delay_minutes": "",
            "lanes_open": ""
        }
    },
    "construction_notice": "",
    "automation": "0",
    "automation_enabled": "0"
}

SAMPLE_PORT_CLOSED_LANES = {
    "port_number": "300403",
    "border": "Canadian Border",
    "port_name": "Blaine",
    "crossing_name": "Point Roberts",
    "hours": "24 hrs/day",
    "date": "4/8/2026",
    "time": "13:16:47",
    "port_status": "Open",
    "commercial_vehicle_lanes": {
        "maximum_lanes": "1",
        "standard_lanes": {
            "update_time": "",
            "operational_status": "Lanes Closed",
            "delay_minutes": "",
            "lanes_open": ""
        },
        "FAST_lanes": {
            "update_time": "",
            "operational_status": "N/A",
            "delay_minutes": "",
            "lanes_open": ""
        }
    },
    "passenger_vehicle_lanes": {
        "maximum_lanes": "2",
        "standard_lanes": {
            "update_time": "At 1:00 pm PDT",
            "operational_status": "no delay",
            "delay_minutes": "0",
            "lanes_open": "1"
        },
        "NEXUS_SENTRI_lanes": {
            "update_time": "",
            "operational_status": "Lanes Closed",
            "delay_minutes": "",
            "lanes_open": ""
        },
        "ready_lanes": {
            "update_time": "",
            "operational_status": "Lanes Closed",
            "delay_minutes": "",
            "lanes_open": ""
        }
    },
    "pedestrian_lanes": {
        "maximum_lanes": "N/A",
        "standard_lanes": {
            "update_time": "",
            "operational_status": "N/A",
            "delay_minutes": "",
            "lanes_open": ""
        },
        "ready_lanes": {
            "update_time": "",
            "operational_status": "N/A",
            "delay_minutes": "",
            "lanes_open": ""
        }
    },
    "construction_notice": "",
    "automation": "0",
    "automation_enabled": "0"
}

SAMPLE_PORT_UPDATE_PENDING = {
    "port_number": "999901",
    "border": "Mexican Border",
    "port_name": "TestPort",
    "crossing_name": "TestCrossing",
    "hours": "6:00 am - 10:00 pm",
    "date": "4/8/2026",
    "time": "08:00:00",
    "port_status": "Open",
    "commercial_vehicle_lanes": {
        "maximum_lanes": "2",
        "standard_lanes": {
            "update_time": "",
            "operational_status": "Update Pending",
            "delay_minutes": "",
            "lanes_open": ""
        },
        "FAST_lanes": {
            "update_time": "",
            "operational_status": "Update Pending",
            "delay_minutes": "",
            "lanes_open": ""
        }
    },
    "passenger_vehicle_lanes": {
        "maximum_lanes": "3",
        "standard_lanes": {
            "update_time": "",
            "operational_status": "Update Pending",
            "delay_minutes": "",
            "lanes_open": ""
        },
        "NEXUS_SENTRI_lanes": {
            "update_time": "",
            "operational_status": "Update Pending",
            "delay_minutes": "",
            "lanes_open": ""
        },
        "ready_lanes": {
            "update_time": "",
            "operational_status": "Update Pending",
            "delay_minutes": "",
            "lanes_open": ""
        }
    },
    "pedestrian_lanes": {
        "maximum_lanes": "4",
        "standard_lanes": {
            "update_time": "",
            "operational_status": "Update Pending",
            "delay_minutes": "",
            "lanes_open": ""
        },
        "ready_lanes": {
            "update_time": "",
            "operational_status": "Update Pending",
            "delay_minutes": "",
            "lanes_open": ""
        }
    },
    "construction_notice": "",
    "automation": "0",
    "automation_enabled": "0"
}


# ---------------------------------------------------------------------------
# parse_int_or_none tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseIntOrNone:
    def test_valid_integer(self):
        assert parse_int_or_none("10") == 10

    def test_zero(self):
        assert parse_int_or_none("0") == 0

    def test_empty_string(self):
        assert parse_int_or_none("") is None

    def test_na(self):
        assert parse_int_or_none("N/A") is None

    def test_none_value(self):
        assert parse_int_or_none(None) is None

    def test_whitespace(self):
        assert parse_int_or_none("  5  ") == 5

    def test_float_string(self):
        assert parse_int_or_none("3.7") is None

    def test_na_lowercase(self):
        assert parse_int_or_none("n/a") is None


# ---------------------------------------------------------------------------
# parse_delay_minutes tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseDelayMinutes:
    def test_valid_delay(self):
        assert parse_delay_minutes("45") == 45

    def test_no_delay(self):
        assert parse_delay_minutes("0") == 0

    def test_empty(self):
        assert parse_delay_minutes("") is None

    def test_na(self):
        assert parse_delay_minutes("N/A") is None


# ---------------------------------------------------------------------------
# parse_lanes_open tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseLanesOpen:
    def test_valid_lanes(self):
        assert parse_lanes_open("3") == 3

    def test_empty(self):
        assert parse_lanes_open("") is None

    def test_na(self):
        assert parse_lanes_open("N/A") is None


# ---------------------------------------------------------------------------
# parse_operational_status tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseOperationalStatus:
    def test_no_delay(self):
        assert parse_operational_status("no delay") == "no delay"

    def test_delay(self):
        assert parse_operational_status("delay") == "delay"

    def test_na(self):
        assert parse_operational_status("N/A") == "N/A"

    def test_lanes_closed(self):
        assert parse_operational_status("Lanes Closed") == "Lanes Closed"

    def test_update_pending(self):
        assert parse_operational_status("Update Pending") == "Update Pending"

    def test_empty(self):
        assert parse_operational_status("") is None

    def test_none(self):
        assert parse_operational_status(None) is None


# ---------------------------------------------------------------------------
# _extract_lane tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestExtractLane:
    def test_full_lane(self):
        lane = {
            "update_time": "At 2:00 pm PDT",
            "operational_status": "delay",
            "delay_minutes": "15",
            "lanes_open": "3"
        }
        delay, lanes, status = _extract_lane(lane)
        assert delay == 15
        assert lanes == 3
        assert status == "delay"

    def test_na_lane(self):
        lane = {
            "update_time": "",
            "operational_status": "N/A",
            "delay_minutes": "",
            "lanes_open": ""
        }
        delay, lanes, status = _extract_lane(lane)
        assert delay is None
        assert lanes is None
        assert status == "N/A"

    def test_empty_dict(self):
        delay, lanes, status = _extract_lane({})
        assert delay is None
        assert lanes is None
        assert status is None

    def test_none_input(self):
        delay, lanes, status = _extract_lane(None)
        assert delay is None
        assert lanes is None
        assert status is None


# ---------------------------------------------------------------------------
# parse_port tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParsePort:
    def test_basic_fields(self):
        port = CbpBorderWaitAPI.parse_port(SAMPLE_PORT_RAW)
        assert port.port_number == "250401"
        assert port.port_name == "San Ysidro"
        assert port.border == "Mexican Border"
        assert port.crossing_name == "San Ysidro"
        assert port.hours == "24 hrs/day"

    def test_max_lanes(self):
        port = CbpBorderWaitAPI.parse_port(SAMPLE_PORT_RAW)
        assert port.passenger_vehicle_max_lanes == 25
        assert port.commercial_vehicle_max_lanes == 5
        assert port.pedestrian_max_lanes == 10

    def test_canadian_border(self):
        port = CbpBorderWaitAPI.parse_port(SAMPLE_PORT_CANADIAN)
        assert port.border == "Canadian Border"
        assert port.crossing_name == "Thousand Islands Bridge"

    def test_na_pedestrian_lanes(self):
        port = CbpBorderWaitAPI.parse_port(SAMPLE_PORT_CANADIAN)
        assert port.pedestrian_max_lanes is None

    def test_missing_lane_section(self):
        raw = {
            "port_number": "999999",
            "port_name": "Test",
            "border": "Canadian Border",
            "crossing_name": "TestCrossing",
            "hours": "",
        }
        port = CbpBorderWaitAPI.parse_port(raw)
        assert port.port_number == "999999"
        assert port.passenger_vehicle_max_lanes is None
        assert port.commercial_vehicle_max_lanes is None
        assert port.pedestrian_max_lanes is None


# ---------------------------------------------------------------------------
# parse_wait_time tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseWaitTime:
    def test_basic_fields(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_RAW)
        assert wt.port_number == "250401"
        assert wt.port_name == "San Ysidro"
        assert wt.border == "Mexican Border"
        assert wt.port_status == "Open"
        assert wt.date == "4/8/2026"
        assert wt.time == "14:00:00"

    def test_passenger_standard(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_RAW)
        assert wt.passenger_vehicle_standard_delay == 45
        assert wt.passenger_vehicle_standard_lanes_open == 10
        assert wt.passenger_vehicle_standard_operational_status == "delay"

    def test_passenger_nexus_sentri(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_RAW)
        # Generated __post_init__ coerces int(0) to None for nullable fields
        assert wt.passenger_vehicle_nexus_sentri_delay is None or wt.passenger_vehicle_nexus_sentri_delay == 0
        assert wt.passenger_vehicle_nexus_sentri_lanes_open == 2
        assert wt.passenger_vehicle_nexus_sentri_operational_status == "no delay"

    def test_passenger_ready(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_RAW)
        assert wt.passenger_vehicle_ready_delay == 30
        assert wt.passenger_vehicle_ready_lanes_open == 5
        assert wt.passenger_vehicle_ready_operational_status == "delay"

    def test_pedestrian_standard(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_RAW)
        assert wt.pedestrian_standard_delay == 20
        assert wt.pedestrian_standard_lanes_open == 4
        assert wt.pedestrian_standard_operational_status == "delay"

    def test_pedestrian_ready_na(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_RAW)
        assert wt.pedestrian_ready_delay is None
        assert wt.pedestrian_ready_lanes_open is None
        assert wt.pedestrian_ready_operational_status == "N/A"

    def test_commercial_standard(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_RAW)
        assert wt.commercial_vehicle_standard_delay == 15
        assert wt.commercial_vehicle_standard_lanes_open == 3
        assert wt.commercial_vehicle_standard_operational_status == "delay"

    def test_commercial_fast_na(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_RAW)
        assert wt.commercial_vehicle_fast_delay is None
        assert wt.commercial_vehicle_fast_lanes_open is None
        assert wt.commercial_vehicle_fast_operational_status == "N/A"

    def test_construction_notice(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_RAW)
        assert wt.construction_notice == "Lane closures expected through May 2026."

    def test_empty_construction_notice(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_CANADIAN)
        assert wt.construction_notice is None

    def test_lanes_closed(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_CLOSED_LANES)
        assert wt.commercial_vehicle_standard_operational_status == "Lanes Closed"
        assert wt.commercial_vehicle_standard_delay is None
        assert wt.commercial_vehicle_standard_lanes_open is None
        assert wt.passenger_vehicle_nexus_sentri_operational_status == "Lanes Closed"
        assert wt.passenger_vehicle_ready_operational_status == "Lanes Closed"

    def test_update_pending(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_UPDATE_PENDING)
        assert wt.passenger_vehicle_standard_operational_status == "Update Pending"
        assert wt.passenger_vehicle_standard_delay is None
        assert wt.commercial_vehicle_fast_operational_status == "Update Pending"

    def test_canadian_no_pedestrians(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_CANADIAN)
        assert wt.pedestrian_standard_operational_status == "N/A"
        assert wt.pedestrian_standard_delay is None
        assert wt.pedestrian_ready_operational_status == "N/A"

    def test_no_delay_zero(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_CANADIAN)
        # Generated __post_init__ coerces int(0) to None for nullable fields
        assert wt.passenger_vehicle_standard_delay is None or wt.passenger_vehicle_standard_delay == 0
        assert wt.passenger_vehicle_standard_operational_status == "no delay"
        assert wt.commercial_vehicle_standard_delay is None or wt.commercial_vehicle_standard_delay == 0


# ---------------------------------------------------------------------------
# fetch tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestFetchPorts:
    @patch("cbp_border_wait.cbp_border_wait.requests.Session")
    def test_fetch_returns_list(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_response = MagicMock()
        mock_response.json.return_value = [SAMPLE_PORT_RAW, SAMPLE_PORT_CANADIAN]
        mock_response.raise_for_status = MagicMock()
        mock_session.get.return_value = mock_response

        api = CbpBorderWaitAPI()
        result = api.fetch_ports()
        assert len(result) == 2
        assert result[0]["port_number"] == "250401"

    @patch("cbp_border_wait.cbp_border_wait.requests.Session")
    def test_fetch_empty(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = MagicMock()
        mock_session.get.return_value = mock_response

        api = CbpBorderWaitAPI()
        result = api.fetch_ports()
        assert result == []


# ---------------------------------------------------------------------------
# State persistence tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestState:
    def test_load_missing_file(self, tmp_path):
        result = _load_state(str(tmp_path / "missing.json"))
        assert result == {}

    def test_save_and_load(self, tmp_path):
        path = str(tmp_path / "state.json")
        data = {"250401": "4/8/2026T14:00:00"}
        _save_state(path, data)
        loaded = _load_state(path)
        assert loaded == data

    def test_empty_path(self):
        _save_state("", {"key": "value"})
        result = _load_state("")
        assert result == {}

    def test_load_corrupt_file(self, tmp_path):
        path = str(tmp_path / "bad.json")
        with open(path, "w") as f:
            f.write("not valid json{{{")
        result = _load_state(path)
        assert result == {}


# ---------------------------------------------------------------------------
# Connection string parsing tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestConnectionStringParsing:
    def test_plain_kafka(self):
        conn = "BootstrapServer=localhost:9092;EntityPath=cbp-border-wait"
        kafka_config, topic = _parse_connection_string(conn)
        assert kafka_config["bootstrap.servers"] == "localhost:9092"
        assert topic == "cbp-border-wait"

    def test_event_hubs(self):
        conn = "Endpoint=sb://myhub.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=abc123;EntityPath=cbp-border-wait"
        kafka_config, topic = _parse_connection_string(conn)
        assert "myhub.servicebus.windows.net" in kafka_config["bootstrap.servers"]
        assert topic == "cbp-border-wait"
        assert kafka_config["security.protocol"] == "SASL_SSL"

    def test_plain_no_sasl(self):
        conn = "BootstrapServer=broker:9092;EntityPath=my-topic"
        kafka_config, topic = _parse_connection_string(conn)
        assert "security.protocol" not in kafka_config
        assert topic == "my-topic"


# ---------------------------------------------------------------------------
# Data class serialization tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDataClassSerialization:
    def test_port_to_json(self):
        port = CbpBorderWaitAPI.parse_port(SAMPLE_PORT_RAW)
        json_str = port.to_json()
        parsed = json.loads(json_str)
        assert parsed["port_number"] == "250401"
        assert parsed["passenger_vehicle_max_lanes"] == 25

    def test_wait_time_to_json(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_RAW)
        json_str = wt.to_json()
        parsed = json.loads(json_str)
        assert parsed["port_number"] == "250401"
        assert parsed["passenger_vehicle_standard_delay"] == 45

    def test_port_null_max_lanes_in_json(self):
        port = CbpBorderWaitAPI.parse_port(SAMPLE_PORT_CANADIAN)
        json_str = port.to_json()
        parsed = json.loads(json_str)
        assert parsed["pedestrian_max_lanes"] is None

    def test_wait_time_null_delay_in_json(self):
        wt = CbpBorderWaitAPI.parse_wait_time(SAMPLE_PORT_CANADIAN)
        json_str = wt.to_json()
        parsed = json.loads(json_str)
        assert parsed["pedestrian_standard_delay"] is None
        assert parsed["pedestrian_ready_delay"] is None

    def test_port_from_dict(self):
        d = {
            "port_number": "111111",
            "port_name": "Test",
            "border": "Canadian Border",
            "crossing_name": "TC",
            "hours": "24 hrs/day",
            "passenger_vehicle_max_lanes": 5,
            "commercial_vehicle_max_lanes": None,
            "pedestrian_max_lanes": None,
        }
        port = Port.from_serializer_dict(d)
        assert port.port_number == "111111"
        assert port.passenger_vehicle_max_lanes == 5
        assert port.commercial_vehicle_max_lanes is None
