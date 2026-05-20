"""Verify that --once causes the bridge to perform exactly one polling cycle."""

import sys
from unittest.mock import patch, MagicMock

import pytest

import energidataservice_dk.energidataservice_dk as bridge


@pytest.fixture
def fake_poller():
    poller = MagicMock()
    poller.poll_and_send = MagicMock()
    return poller


def test_once_flag_invokes_single_cycle(fake_poller, monkeypatch):
    """--once CLI flag should cause poll_and_send to be called with once=True."""
    monkeypatch.setattr(bridge, 'EnergiDataServicePoller', lambda **kw: fake_poller)
    monkeypatch.setenv('CONNECTION_STRING',
                       'BootstrapServer=localhost:9092;EntityPath=test-topic')
    monkeypatch.setenv('KAFKA_ENABLE_TLS', 'false')
    monkeypatch.delenv('ONCE_MODE', raising=False)

    argv_backup = sys.argv
    try:
        sys.argv = ['energidataservice-dk', '--once']
        bridge.main()
    finally:
        sys.argv = argv_backup

    fake_poller.poll_and_send.assert_called_once_with(once=True)


def test_no_once_runs_default_loop(fake_poller, monkeypatch):
    monkeypatch.setattr(bridge, 'EnergiDataServicePoller', lambda **kw: fake_poller)
    monkeypatch.setenv('CONNECTION_STRING',
                       'BootstrapServer=localhost:9092;EntityPath=test-topic')
    monkeypatch.setenv('KAFKA_ENABLE_TLS', 'false')
    monkeypatch.delenv('ONCE_MODE', raising=False)

    argv_backup = sys.argv
    try:
        sys.argv = ['energidataservice-dk']
        bridge.main()
    finally:
        sys.argv = argv_backup

    fake_poller.poll_and_send.assert_called_once_with(once=False)


def test_once_mode_env_var_triggers_single_cycle(fake_poller, monkeypatch):
    monkeypatch.setattr(bridge, 'EnergiDataServicePoller', lambda **kw: fake_poller)
    monkeypatch.setenv('CONNECTION_STRING',
                       'BootstrapServer=localhost:9092;EntityPath=test-topic')
    monkeypatch.setenv('KAFKA_ENABLE_TLS', 'false')
    monkeypatch.setenv('ONCE_MODE', 'true')

    argv_backup = sys.argv
    try:
        sys.argv = ['energidataservice-dk']
        bridge.main()
    finally:
        sys.argv = argv_backup

    fake_poller.poll_and_send.assert_called_once_with(once=True)


def test_poller_loop_breaks_after_one_cycle_when_once_true(monkeypatch):
    """poll_and_send(once=True) should exit after a single iteration."""
    inst = bridge.EnergiDataServicePoller.__new__(bridge.EnergiDataServicePoller)
    inst.kafka_topic = 'test'
    inst.last_polled_file = None
    inst.producer = MagicMock()
    inst.load_state = MagicMock(return_value={})
    inst.save_state = MagicMock()
    inst.fetch_power_system_records = MagicMock(return_value=[])
    inst.fetch_spot_price_records = MagicMock(return_value=[])

    with patch.object(bridge.time, 'sleep') as sleep_mock:
        inst.poll_and_send(once=True)

    sleep_mock.assert_not_called()
    inst.fetch_power_system_records.assert_called_once()
