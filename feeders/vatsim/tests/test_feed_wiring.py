"""One-cycle wiring test covering all three VATSIM generated producer classes.

NetVatsimPilotsEventProducer, NetVatsimControllersEventProducer, and
NetVatsimStatusEventProducer are all imported and used by VatsimBridge.feed().
This test drives one complete polling cycle with fake producers and verifies
every producer class sends at least one event.
"""

import datetime
from unittest.mock import MagicMock, patch

import pytest

from vatsim.vatsim import VatsimBridge, VATSIM_DATA_URL


# ---------------------------------------------------------------------------
# Mock payload — one pilot, one controller, complete general section
# ---------------------------------------------------------------------------

_MOCK_DATA = {
    "general": {
        "version": 3,
        "reload": 1,
        "update": "20260101000000",
        "update_timestamp": "2026-01-01T00:00:00.000000Z",
        "connected_clients": 500,
        "unique_users": 480,
    },
    "pilots": [
        {
            "cid": 1000001,
            "callsign": "BAW001",
            "pilot_rating": 1,
            "latitude": 51.477,
            "longitude": -0.461,
            "altitude": 35000,
            "groundspeed": 450,
            "transponder": "2000",
            "heading": 90,
            "qnh_mb": 1013,
            "flight_plan": {
                "flight_rules": "I",
                "aircraft_short": "B77W",
                "departure": "EGLL",
                "arrival": "KJFK",
                "altitude": "35000",
                "route": "WOBUN UT420 BEDRA",
            },
            "last_updated": "2026-01-01T00:00:00.000000Z",
        }
    ],
    "controllers": [
        {
            "cid": 2000001,
            "callsign": "EGLL_APP",
            "frequency": "119.725",
            "facility": 5,
            "rating": 4,
            "text_atis": ["EGLL APPROACH", "QNH 1013"],
            "last_updated": "2026-01-01T00:00:00.000000Z",
        }
    ],
    "atis": [],
    "servers": [],
    "prefiles": [],
}


# ---------------------------------------------------------------------------
# One-cycle wiring test
# ---------------------------------------------------------------------------

@pytest.mark.integration
class TestVatsimFeedProducerWiring:
    """VatsimBridge.feed() instantiates and calls all three generated producers."""

    def test_one_cycle_exercises_all_three_producer_classes(self):
        sent = []

        class FakePilotsProducer:
            def __init__(self, *_a, **_kw):
                pass

            def send_net_vatsim_pilot_position(self, **_kw):
                sent.append("pilots:pilot_position")

        class FakeControllersProducer:
            def __init__(self, *_a, **_kw):
                pass

            def send_net_vatsim_controller_position(self, **_kw):
                sent.append("controllers:controller_position")

        class FakeStatusProducer:
            def __init__(self, *_a, **_kw):
                pass

            def send_net_vatsim_network_status(self, **_kw):
                sent.append("status:network_status")

        fake_kafka = MagicMock()
        bridge = VatsimBridge()

        with patch("vatsim.vatsim.Producer", return_value=fake_kafka), \
             patch("vatsim.vatsim.NetVatsimPilotsEventProducer", FakePilotsProducer), \
             patch("vatsim.vatsim.NetVatsimControllersEventProducer", FakeControllersProducer), \
             patch("vatsim.vatsim.NetVatsimStatusEventProducer", FakeStatusProducer), \
             patch.object(bridge, "fetch_data", return_value=_MOCK_DATA), \
             patch("vatsim.vatsim._load_state", return_value={}), \
             patch("vatsim.vatsim._save_state"), \
             patch("vatsim.vatsim.time.sleep", side_effect=KeyboardInterrupt):
            bridge.feed(
                kafka_config={"bootstrap.servers": "localhost:9092"},
                kafka_topic="test-topic",
                polling_interval=15,
                state_file="",
            )

        assert "status:network_status" in sent, "StatusEventProducer was not called"
        assert "pilots:pilot_position" in sent, "PilotsEventProducer was not called"
        assert "controllers:controller_position" in sent, "ControllersEventProducer was not called"

    def test_dedup_suppresses_duplicate_pilots(self):
        """A pilot already in state is not re-emitted."""
        sent = []

        class FakePilots:
            def __init__(self, *_a, **_kw):
                pass

            def send_net_vatsim_pilot_position(self, **_kw):
                sent.append("pilot")

        class FakeControllers:
            def __init__(self, *_a, **_kw):
                pass

            def send_net_vatsim_controller_position(self, **_kw):
                pass

        class FakeStatus:
            def __init__(self, *_a, **_kw):
                pass

            def send_net_vatsim_network_status(self, **_kw):
                pass

        pilot = _MOCK_DATA["pilots"][0]
        bridge = VatsimBridge()
        # Pre-populate state so the pilot fingerprint matches — no emit expected
        existing_fp = bridge.pilot_fingerprint(pilot)
        pre_state = {"BAW001": existing_fp}

        with patch("vatsim.vatsim.Producer", return_value=MagicMock()), \
             patch("vatsim.vatsim.NetVatsimPilotsEventProducer", FakePilots), \
             patch("vatsim.vatsim.NetVatsimControllersEventProducer", FakeControllers), \
             patch("vatsim.vatsim.NetVatsimStatusEventProducer", FakeStatus), \
             patch.object(bridge, "fetch_data", return_value=_MOCK_DATA), \
             patch("vatsim.vatsim._load_state", return_value={"pilots": pre_state, "controllers": {}}), \
             patch("vatsim.vatsim._save_state"), \
             patch("vatsim.vatsim.time.sleep", side_effect=KeyboardInterrupt):
            bridge.feed(
                kafka_config={"bootstrap.servers": "localhost:9092"},
                kafka_topic="test-topic",
                polling_interval=15,
                state_file="",
            )

        assert sent == [], "Unchanged pilot should not be re-emitted"
