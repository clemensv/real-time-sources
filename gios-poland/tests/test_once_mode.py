"""Tests for --once mode added for Fabric notebook hosting."""
from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest


def _make_poller_stub():
    poller = MagicMock()
    poller.poll_and_send = MagicMock()
    return poller


def test_once_flag_passes_once_true_to_poll_and_send(monkeypatch):
    """`--once` on the CLI must propagate to poller.poll_and_send(once=True)."""
    from gios_poland import gios_poland as bridge

    stub = _make_poller_stub()

    monkeypatch.setattr(sys, "argv", [
        "gios-poland",
        "--kafka-bootstrap-servers", "localhost:9092",
        "--kafka-topic", "gios-poland",
        "--once",
    ])
    monkeypatch.delenv("CONNECTION_STRING", raising=False)
    monkeypatch.delenv("ONCE_MODE", raising=False)
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")

    with patch.object(bridge, "GIOSPolandPoller", return_value=stub) as factory:
        bridge.main()

    factory.assert_called_once()
    stub.poll_and_send.assert_called_once_with(once=True)


def test_once_env_var_propagates(monkeypatch):
    """ONCE_MODE=true env var is equivalent to --once."""
    from gios_poland import gios_poland as bridge

    stub = _make_poller_stub()

    monkeypatch.setattr(sys, "argv", [
        "gios-poland",
        "--kafka-bootstrap-servers", "localhost:9092",
        "--kafka-topic", "gios-poland",
    ])
    monkeypatch.delenv("CONNECTION_STRING", raising=False)
    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")

    with patch.object(bridge, "GIOSPolandPoller", return_value=stub):
        bridge.main()

    stub.poll_and_send.assert_called_once_with(once=True)


def test_default_runs_continuous(monkeypatch):
    """Without --once or ONCE_MODE, poll_and_send is invoked with once=False."""
    from gios_poland import gios_poland as bridge

    stub = _make_poller_stub()

    monkeypatch.setattr(sys, "argv", [
        "gios-poland",
        "--kafka-bootstrap-servers", "localhost:9092",
        "--kafka-topic", "gios-poland",
    ])
    monkeypatch.delenv("CONNECTION_STRING", raising=False)
    monkeypatch.delenv("ONCE_MODE", raising=False)
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")

    with patch.object(bridge, "GIOSPolandPoller", return_value=stub):
        bridge.main()

    stub.poll_and_send.assert_called_once_with(once=False)


def test_poll_and_send_exits_after_one_cycle_when_once_true():
    """poll_and_send(once=True) must exit after a single iteration of the while loop."""
    from gios_poland import gios_poland as bridge

    poller = bridge.GIOSPolandPoller.__new__(bridge.GIOSPolandPoller)
    poller.BASE_URL = "http://example/invalid"
    poller.POLL_INTERVAL_SECONDS = 9999
    poller.REQUEST_DELAY = 0
    poller.kafka_topic = "x"
    poller.last_polled_file = None
    poller.producer = MagicMock()
    poller.fetch_stations = MagicMock(return_value=[])
    poller.fetch_sensors = MagicMock(return_value=[])
    poller.fetch_measurements = MagicMock(return_value=[])
    poller.fetch_air_quality_index = MagicMock(return_value=None)
    poller.load_state = MagicMock(return_value={})
    poller.save_state = MagicMock()

    with patch.object(bridge.time, "sleep") as sleep_mock:
        poller.poll_and_send(once=True)

    # Must NOT have slept on POLL_INTERVAL_SECONDS (which would indicate it
    # entered a second iteration).
    for call in sleep_mock.call_args_list:
        assert call.args[0] != poller.POLL_INTERVAL_SECONDS, \
            "poll_and_send slept on POLL_INTERVAL_SECONDS — did not exit after one cycle"
