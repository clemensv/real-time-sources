"""Unit tests for --once / ONCE_MODE single-cycle execution in the SMHI Hydro bridge."""

import sys
import time as time_module
from unittest.mock import MagicMock, patch

import pytest

from smhi_hydro import smhi_hydro as bridge


SAMPLE_BULK = {
    "station": [
        {
            "key": "1583",
            "name": "VÄSTERSEL",
            "owner": "SMHI",
            "measuringStations": "CORE",
            "region": 36,
            "catchmentName": "MOÄLVEN",
            "catchmentNumber": 36000,
            "catchmentSize": 1465.2,
            "latitude": 63.4332,
            "longitude": 18.3034,
            "value": [{"date": 1774454400000, "value": 16.0, "quality": "O"}],
        }
    ]
}


def _run_main_with_once(monkeypatch, once_argv=True, once_env=False):
    """Invoke bridge.main() in feed mode with --once and assert single-cycle exit."""
    monkeypatch.setenv("KAFKA_BROKER", "localhost:9092")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    if once_env:
        monkeypatch.setenv("ONCE_MODE", "true")
    else:
        monkeypatch.delenv("ONCE_MODE", raising=False)

    argv = ["smhi-hydro", "--state-file", "", "feed"]
    if once_argv:
        argv.append("--once")
    monkeypatch.setattr(sys, "argv", argv)

    sleep_calls = []
    monkeypatch.setattr(time_module, "sleep", lambda s: sleep_calls.append(s))

    with patch.object(bridge.SMHIHydroAPI, "get_bulk_discharge_data", return_value=SAMPLE_BULK) as mock_get, \
         patch.object(bridge, "Producer", return_value=MagicMock()):
        bridge.main()

    return mock_get, sleep_calls


def test_once_flag_exits_after_single_cycle(monkeypatch):
    mock_get, sleep_calls = _run_main_with_once(monkeypatch, once_argv=True)
    # send_stations + feed_observations = 2 calls to the bulk endpoint, then exit.
    assert mock_get.call_count == 2
    assert sleep_calls == [], "--once must not sleep for the next polling cycle"


def test_once_env_var_exits_after_single_cycle(monkeypatch):
    mock_get, sleep_calls = _run_main_with_once(monkeypatch, once_argv=False, once_env=True)
    assert mock_get.call_count == 2
    assert sleep_calls == []
