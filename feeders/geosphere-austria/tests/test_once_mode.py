"""Test that --once flag (and ONCE_MODE env var) causes main() to exit after one cycle."""

from __future__ import annotations

import sys
from unittest.mock import patch, MagicMock

import pytest

from geosphere_austria import geosphere_austria as bridge

pytestmark = pytest.mark.unit


def _run_main_with_argv(argv, monkeypatch):
    monkeypatch.setenv("CONNECTION_STRING", "BootstrapServer=localhost:9092;EntityPath=t")
    monkeypatch.setenv("POLLING_INTERVAL", "9999")
    monkeypatch.setenv("STATION_REFRESH_INTERVAL", "9999")
    monkeypatch.setenv("STATE_FILE", "")
    monkeypatch.setattr(sys, "argv", argv)

    cycle = MagicMock(return_value=(0, 0, []))
    sleep = MagicMock(side_effect=AssertionError("time.sleep called in --once mode"))

    with patch.object(bridge, "Producer", MagicMock()), \
         patch.object(bridge, "AtGeosphereTawesEventProducer", MagicMock()), \
         patch.object(bridge, "create_retrying_session", MagicMock()), \
         patch.object(bridge, "load_state", MagicMock(return_value={})), \
         patch.object(bridge, "save_state", MagicMock()), \
         patch.object(bridge, "run_feed_cycle", cycle), \
         patch.object(bridge.time, "sleep", sleep):
        bridge.main()

    return cycle, sleep


def test_once_flag_exits_after_one_cycle(monkeypatch):
    cycle, sleep = _run_main_with_argv(["geosphere-austria", "feed", "--once"], monkeypatch)
    assert cycle.call_count == 1
    sleep.assert_not_called()


def test_once_mode_env_var_exits_after_one_cycle(monkeypatch):
    monkeypatch.setenv("ONCE_MODE", "true")
    cycle, sleep = _run_main_with_argv(["geosphere-austria", "feed"], monkeypatch)
    assert cycle.call_count == 1
    sleep.assert_not_called()
