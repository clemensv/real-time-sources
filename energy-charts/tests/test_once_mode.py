"""Verify the --once CLI flag exits after exactly one polling cycle.

Added for Fabric notebook hosting (scheduled single-cycle runs).
"""
import sys
from unittest.mock import patch, MagicMock

import pytest


@pytest.fixture
def fake_env(monkeypatch, tmp_path):
    monkeypatch.setenv('KAFKA_ENABLE_TLS', 'false')
    monkeypatch.delenv('ONCE_MODE', raising=False)
    state = tmp_path / 'state.json'
    return {
        'state_file': str(state),
    }


def _run_with_argv(argv):
    from energy_charts import energy_charts as ec

    with patch.object(ec, 'EnergyChartsPoller') as PollerCls:
        instance = MagicMock()
        instance.poll_and_send = MagicMock()
        PollerCls.return_value = instance

        old_argv = sys.argv
        sys.argv = argv
        try:
            ec.main()
        finally:
            sys.argv = old_argv
        return instance


def test_once_flag_passes_through(fake_env):
    instance = _run_with_argv([
        'energy-charts',
        '--kafka-bootstrap-servers', 'localhost:9092',
        '--kafka-topic', 'test-topic',
        '--last-polled-file', fake_env['state_file'],
        '--once',
    ])
    instance.poll_and_send.assert_called_once_with(once=True)


def test_default_is_continuous(fake_env):
    instance = _run_with_argv([
        'energy-charts',
        '--kafka-bootstrap-servers', 'localhost:9092',
        '--kafka-topic', 'test-topic',
        '--last-polled-file', fake_env['state_file'],
    ])
    instance.poll_and_send.assert_called_once_with(once=False)


def test_once_mode_env_var(monkeypatch, fake_env):
    monkeypatch.setenv('ONCE_MODE', 'true')
    instance = _run_with_argv([
        'energy-charts',
        '--kafka-bootstrap-servers', 'localhost:9092',
        '--kafka-topic', 'test-topic',
        '--last-polled-file', fake_env['state_file'],
    ])
    instance.poll_and_send.assert_called_once_with(once=True)


def test_poll_and_send_once_exits_after_one_cycle():
    """The poll_and_send loop itself must exit when once=True."""
    from energy_charts.energy_charts import EnergyChartsPoller

    poller = EnergyChartsPoller.__new__(EnergyChartsPoller)
    poller.POWER_POLL_INTERVAL = 0
    poller.PRICE_POLL_INTERVAL = 0
    poller.SIGNAL_POLL_INTERVAL = 0
    poller.country = 'de'
    poller.emit_public_power = MagicMock(return_value=0)
    poller.emit_price = MagicMock(return_value=0)
    poller.emit_signal = MagicMock(return_value=0)
    poller._save_state = MagicMock()

    with patch('energy_charts.energy_charts.time.sleep') as sleep_mock:
        poller.poll_and_send(once=True)
        sleep_mock.assert_not_called()

    poller.emit_public_power.assert_called_once()
    poller.emit_price.assert_called_once()
    poller.emit_signal.assert_called_once()
