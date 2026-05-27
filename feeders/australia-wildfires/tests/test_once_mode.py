"""Test that --once causes main() to exit after a single polling cycle."""

import sys
from unittest.mock import MagicMock, patch

from australia_wildfires import australia_wildfires as bridge


def test_once_flag_exits_after_single_cycle(monkeypatch):
    """`--once` must cause main() to return after exactly one feed_incidents call."""
    monkeypatch.setattr(sys, "argv", [
        "australia-wildfires", "--connection-string",
        "BootstrapServer=localhost:9092;EntityPath=test-topic",
        "--once", "feed",
    ])

    fetch_count = {"n": 0}

    def fake_feed_incidents(api, producer, state):
        fetch_count["n"] += 1
        return 0

    sleep_calls = {"n": 0}

    def fake_sleep(seconds):
        sleep_calls["n"] += 1
        raise AssertionError("time.sleep must not be called when --once is set")

    fake_producer = MagicMock()
    fake_event_producer = MagicMock()

    with patch.object(bridge, "feed_incidents", side_effect=fake_feed_incidents), \
         patch.object(bridge, "Producer", return_value=fake_producer), \
         patch.object(bridge, "AUGovEmergencyWildfiresEventProducer",
                       return_value=fake_event_producer), \
         patch.object(bridge.time, "sleep", side_effect=fake_sleep):
        bridge.main()

    assert fetch_count["n"] == 1, "Expected exactly one polling cycle"
    assert sleep_calls["n"] == 0, "time.sleep must not run when --once is set"


def test_once_via_env_var(monkeypatch):
    """ONCE_MODE=true env should produce the same single-cycle behaviour."""
    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setattr(sys, "argv", [
        "australia-wildfires", "--connection-string",
        "BootstrapServer=localhost:9092;EntityPath=test-topic", "feed",
    ])

    cycles = {"n": 0}

    def fake_feed_incidents(api, producer, state):
        cycles["n"] += 1
        return 0

    with patch.object(bridge, "feed_incidents", side_effect=fake_feed_incidents), \
         patch.object(bridge, "Producer", return_value=MagicMock()), \
         patch.object(bridge, "AUGovEmergencyWildfiresEventProducer",
                       return_value=MagicMock()), \
         patch.object(bridge.time, "sleep",
                       side_effect=AssertionError("sleep must not run")):
        bridge.main()

    assert cycles["n"] == 1
