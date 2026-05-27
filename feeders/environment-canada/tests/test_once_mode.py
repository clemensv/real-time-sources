"""Test that the bridge supports --once single-cycle execution.

Regression guard for the Fabric notebook hosting path, which schedules
the bridge as a single-cycle command and depends on the polling loop
exiting cleanly after one iteration.
"""

import sys
from unittest.mock import patch, MagicMock

import environment_canada.environment_canada as bridge


def test_once_flag_exits_after_one_cycle(monkeypatch):
    """With --once, main() must return after exactly one feed cycle, no sleep."""
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "environment-canada",
            "--connection-string",
            "Endpoint=sb://fake/;EntityPath=topic",
            "--topic",
            "test-topic",
            "--state-file",
            "",
            "--once",
            "feed",
        ],
    )

    sleep_mock = MagicMock()
    send_stations_mock = MagicMock()
    feed_observations_mock = MagicMock(return_value=3)
    producer_mock = MagicMock()
    event_producer_mock = MagicMock()

    with patch.object(bridge, "time", MagicMock(sleep=sleep_mock)), \
         patch.object(bridge, "Producer", return_value=producer_mock), \
         patch.object(bridge, "CAGovECCCWeatherEventProducer", return_value=event_producer_mock), \
         patch.object(bridge, "send_stations", send_stations_mock), \
         patch.object(bridge, "feed_observations", feed_observations_mock), \
         patch.object(bridge, "_load_state", return_value={}), \
         patch.object(bridge, "_save_state"):
        bridge.main()

    assert feed_observations_mock.call_count == 1, "feed_observations should run exactly once"
    sleep_mock.assert_not_called()


def test_once_via_env_var(monkeypatch):
    """Setting ONCE_MODE=true via environment must also cause single-cycle exit."""
    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "environment-canada",
            "--connection-string",
            "Endpoint=sb://fake/;EntityPath=topic",
            "--topic",
            "test-topic",
            "--state-file",
            "",
            "feed",
        ],
    )

    sleep_mock = MagicMock()
    feed_observations_mock = MagicMock(return_value=0)

    with patch.object(bridge, "time", MagicMock(sleep=sleep_mock)), \
         patch.object(bridge, "Producer", return_value=MagicMock()), \
         patch.object(bridge, "CAGovECCCWeatherEventProducer", return_value=MagicMock()), \
         patch.object(bridge, "send_stations"), \
         patch.object(bridge, "feed_observations", feed_observations_mock), \
         patch.object(bridge, "_load_state", return_value={}), \
         patch.object(bridge, "_save_state"):
        bridge.main()

    assert feed_observations_mock.call_count == 1
    sleep_mock.assert_not_called()
