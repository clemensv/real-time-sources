"""Verify that `feed --once` causes main() to exit after one polling cycle."""

import sys
import time
from unittest.mock import patch, MagicMock

import pytest

from hko_hong_kong import hko_hong_kong as bridge


@pytest.fixture(autouse=True)
def _no_sleep():
    with patch.object(bridge.time, "sleep", side_effect=AssertionError(
            "time.sleep must not be called when --once is set"
    )):
        yield


def test_once_mode_exits_after_one_cycle(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    monkeypatch.setattr(sys, "argv", [
        "hko-hong-kong",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=test-hko",
        "--polling-interval", "1",
        "--state-file", str(state_file),
        "feed",
        "--once",
    ])

    feed_calls = {"n": 0}

    def fake_feed(api, producer, previous):
        feed_calls["n"] += 1
        return 0

    with patch.object(bridge, "Producer", return_value=MagicMock()), \
         patch.object(bridge, "HKGovHKOWeatherEventProducer", return_value=MagicMock()), \
         patch.object(bridge, "send_stations", return_value=0), \
         patch.object(bridge, "feed_observations", side_effect=fake_feed):
        start = time.monotonic()
        bridge.main()
        elapsed = time.monotonic() - start

    assert feed_calls["n"] == 1, "feed_observations should run exactly once in --once mode"
    assert elapsed < 5, "main() should return promptly in --once mode without sleeping"
