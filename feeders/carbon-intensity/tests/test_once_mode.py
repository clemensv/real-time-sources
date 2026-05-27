"""Tests for --once / ONCE_MODE single-cycle execution.

Asserts that the carbon-intensity bridge exits after one polling cycle when
``--once`` is supplied. Used by the Fabric notebook hosting pattern, where the
scheduler invokes the bridge once per interval rather than relying on the
in-process ``time.sleep`` loop.
"""

import sys
from unittest.mock import patch, MagicMock

import pytest

from carbon_intensity import carbon_intensity as bridge


@pytest.fixture
def fake_kafka_env(monkeypatch, tmp_path):
    state_file = tmp_path / "state.json"
    monkeypatch.setenv("CONNECTION_STRING",
                       "Endpoint=sb://example.servicebus.windows.net/;"
                       "SharedAccessKeyName=k;SharedAccessKey=v;EntityPath=t")
    monkeypatch.setenv("STATE_FILE", str(state_file))
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")


def test_once_flag_returns_after_single_cycle(fake_kafka_env):
    """--once must cause main() to invoke poll_once exactly once and return."""
    with patch.object(bridge, "CarbonIntensityPoller") as poller_cls, \
         patch.object(bridge.time, "sleep") as sleep_mock:
        poller = MagicMock()
        poller.poll_and_send.side_effect = (
            lambda once=False: bridge.CarbonIntensityPoller.poll_and_send(poller, once=once)
        )
        poller_cls.return_value = poller

        old_argv = sys.argv
        try:
            sys.argv = ["carbon-intensity", "--once"]
            bridge.main()
        finally:
            sys.argv = old_argv

        poller.poll_and_send.assert_called_once()
        _, kwargs = poller.poll_and_send.call_args
        assert kwargs.get("once") is True
        sleep_mock.assert_not_called()


def test_once_mode_env_var_enables_single_cycle(monkeypatch, fake_kafka_env):
    """ONCE_MODE=true must behave identically to --once for the scheduler."""
    monkeypatch.setenv("ONCE_MODE", "true")
    with patch.object(bridge, "CarbonIntensityPoller") as poller_cls:
        poller = MagicMock()
        poller_cls.return_value = poller

        old_argv = sys.argv
        try:
            sys.argv = ["carbon-intensity"]
            bridge.main()
        finally:
            sys.argv = old_argv

        poller.poll_and_send.assert_called_once_with(once=True)


def test_poll_and_send_once_breaks_loop():
    """The loop body itself must exit when ``once=True`` after one cycle."""
    poller = MagicMock(spec=bridge.CarbonIntensityPoller)
    poller.load_state.return_value = {}
    poller.poll_once.return_value = "2026-04-06T09:30:00+00:00"

    with patch.object(bridge.time, "sleep") as sleep_mock:
        bridge.CarbonIntensityPoller.poll_and_send(poller, once=True)

    poller.poll_once.assert_called_once()
    sleep_mock.assert_not_called()
