"""Verify --once causes main() to return after exactly one polling cycle."""

import sys
import time
from unittest.mock import patch, MagicMock

from smhi_weather import smhi_weather as bridge


def test_once_flag_exits_after_single_cycle(monkeypatch, tmp_path):
    state_file = tmp_path / "state.json"
    monkeypatch.setattr(sys, "argv", [
        "smhi-weather",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=t",
        "--state-file", str(state_file),
        "--polling-interval", "1",
        "feed",
        "--once",
    ])

    call_count = {"n": 0}

    def fake_feed(api, producer, previous_readings):
        call_count["n"] += 1
        return 0

    monkeypatch.setattr(bridge, "feed_observations", fake_feed)
    monkeypatch.setattr(bridge, "send_stations", lambda *a, **kw: None)
    monkeypatch.setattr(bridge, "_load_state", lambda *_: {})
    monkeypatch.setattr(bridge, "_save_state", lambda *_: None)
    monkeypatch.setattr(bridge, "Producer", lambda cfg: MagicMock())
    monkeypatch.setattr(bridge, "SEGovSMHIWeatherEventProducer",
                        lambda producer, topic: MagicMock())

    def fail_if_called(*_a, **_kw):
        raise AssertionError("time.sleep must not be called when --once is set")

    monkeypatch.setattr(time, "sleep", fail_if_called)

    bridge.main()

    assert call_count["n"] == 1, "feed_observations should be called exactly once with --once"


def test_once_env_var_enables_single_cycle(monkeypatch, tmp_path):
    state_file = tmp_path / "state.json"
    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setattr(sys, "argv", [
        "smhi-weather",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=t",
        "--state-file", str(state_file),
        "--polling-interval", "1",
        "feed",
    ])

    call_count = {"n": 0}

    def fake_feed(api, producer, previous_readings):
        call_count["n"] += 1
        return 0

    monkeypatch.setattr(bridge, "feed_observations", fake_feed)
    monkeypatch.setattr(bridge, "send_stations", lambda *a, **kw: None)
    monkeypatch.setattr(bridge, "_load_state", lambda *_: {})
    monkeypatch.setattr(bridge, "_save_state", lambda *_: None)
    monkeypatch.setattr(bridge, "Producer", lambda cfg: MagicMock())
    monkeypatch.setattr(bridge, "SEGovSMHIWeatherEventProducer",
                        lambda producer, topic: MagicMock())
    monkeypatch.setattr(time, "sleep",
                        lambda *_a, **_kw: (_ for _ in ()).throw(
                            AssertionError("sleep should not be called")))

    bridge.main()
    assert call_count["n"] == 1
