"""Verify the bridge's --once flag exits after a single polling cycle."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest

from fmi_finland import fmi_finland as bridge

pytestmark = pytest.mark.unit


def test_once_flag_runs_single_cycle_then_returns(monkeypatch, tmp_path):
    """`fmi-finland feed --once` must invoke run_feed_cycle exactly once and return."""

    state_file = tmp_path / "state.json"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "fmi-finland",
            "feed",
            "--kafka-bootstrap-servers",
            "localhost:9092",
            "--state-file",
            str(state_file),
            "--once",
        ],
    )

    fake_producer = MagicMock()
    cycle_calls = {"count": 0}

    def fake_cycle(*_args, **_kwargs):
        cycle_calls["count"] += 1
        return {"stations": 1, "observations": 2}

    sleep_mock = MagicMock()

    with patch.object(bridge, "FMIAirQualityAPI"), patch.object(
        bridge, "FiFmiOpendataAirqualityEventProducer", return_value=fake_producer
    ), patch.object(bridge, "Producer"), patch.object(
        bridge, "run_feed_cycle", side_effect=fake_cycle
    ), patch.object(bridge.time, "sleep", sleep_mock):
        bridge.main()

    assert cycle_calls["count"] == 1, "run_feed_cycle should run exactly once with --once"
    sleep_mock.assert_not_called()


def test_once_flag_via_env(monkeypatch, tmp_path):
    """Setting ONCE_MODE=true should also trigger a single-cycle exit."""

    state_file = tmp_path / "state.json"

    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "fmi-finland",
            "feed",
            "--kafka-bootstrap-servers",
            "localhost:9092",
            "--state-file",
            str(state_file),
        ],
    )

    cycle_calls = {"count": 0}

    def fake_cycle(*_args, **_kwargs):
        cycle_calls["count"] += 1
        return {"stations": 0, "observations": 0}

    with patch.object(bridge, "FMIAirQualityAPI"), patch.object(
        bridge, "FiFmiOpendataAirqualityEventProducer"
    ), patch.object(bridge, "Producer"), patch.object(
        bridge, "run_feed_cycle", side_effect=fake_cycle
    ), patch.object(bridge.time, "sleep", MagicMock()):
        bridge.main()

    assert cycle_calls["count"] == 1
