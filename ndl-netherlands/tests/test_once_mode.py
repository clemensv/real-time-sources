"""Verify that ``--once`` causes ``main()`` to exit after a single polling cycle."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest

from ndl_netherlands import ndl_netherlands as bridge


def test_run_forever_once_returns_after_single_cycle():
    """``run_forever(once=True)`` must return after exactly one poll cycle."""
    poller = bridge.NdwPoller.__new__(bridge.NdwPoller)
    poller.poll_interval = 60
    poller._last_situation_poll = 0
    poller.poll_and_send = MagicMock(return_value=(1, 2, 3))

    with patch.object(bridge.time, "sleep") as sleep_mock:
        bridge.NdwPoller.run_forever(poller, once=True)

    assert poller.poll_and_send.call_count == 1
    sleep_mock.assert_not_called()


def test_main_once_flag_invokes_run_forever_with_once_true(monkeypatch):
    """``main`` should propagate ``--once`` to ``poller.run_forever``."""
    monkeypatch.setenv("CONNECTION_STRING", "BootstrapServer=localhost:9092;EntityPath=t")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    monkeypatch.setattr(sys, "argv", ["ndl-netherlands", "--once"])

    fake_poller = MagicMock()
    with patch.object(bridge, "Producer"), \
         patch.object(bridge, "NLNDWTrafficMeasurementsEventProducer"), \
         patch.object(bridge, "NLNDWTrafficSituationsEventProducer"), \
         patch.object(bridge, "StateManager"), \
         patch.object(bridge, "NdwPoller", return_value=fake_poller):
        bridge.main()

    fake_poller.run_forever.assert_called_once_with(once=True)
