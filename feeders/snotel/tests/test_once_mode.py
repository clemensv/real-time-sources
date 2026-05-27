"""
Tests that the SNOTEL bridge exits after a single polling cycle when
`--once` (or `ONCE_MODE=true`) is set. This is required by the Fabric
notebook hosting model where each scheduled invocation runs exactly one
cycle before returning control to the kernel.
"""

import os
import sys
from unittest.mock import patch, MagicMock

import pytest

from snotel.snotel import SnotelPoller, main


@patch('snotel.snotel.GovUsdaNrcsSnotelEventProducer')
@patch('confluent_kafka.Producer')
@patch('snotel.snotel.time.sleep')
def test_run_once_exits_after_single_cycle(
    mock_sleep, mock_producer_class, mock_event_producer, tmp_path,
):
    """``run(..., once=True)`` polls once and returns without sleeping."""
    poller = SnotelPoller(
        kafka_config={'bootstrap.servers': 'localhost:9092'},
        kafka_topic='test',
        last_polled_file=str(tmp_path / 'state.json'),
    )

    with patch.object(poller, 'poll_all', return_value=0) as mock_poll, \
         patch.object(poller, 'emit_station_reference', return_value=1) as mock_ref:
        poller.run(['838:CO:SNTL'], once=True, polling_interval=3600)

    mock_ref.assert_called_once()
    assert mock_poll.call_count == 1, "poll_all must run exactly once in --once mode"
    mock_sleep.assert_not_called(), "no sleep between cycles when once=True"


@patch('snotel.snotel.SnotelPoller')
def test_main_once_flag_propagates(mock_poller_class, monkeypatch):
    """``snotel feed --once`` propagates once=True into SnotelPoller.run."""
    instance = MagicMock()
    mock_poller_class.return_value = instance

    monkeypatch.setenv('CONNECTION_STRING', 'BootstrapServer=localhost:9092;EntityPath=snotel')
    monkeypatch.setenv('KAFKA_ENABLE_TLS', 'false')
    monkeypatch.delenv('ONCE_MODE', raising=False)

    test_argv = ['snotel', 'feed', '--once', '--stations', '838:CO:SNTL']
    with patch.object(sys, 'argv', test_argv):
        main()

    instance.run.assert_called_once()
    _, kwargs = instance.run.call_args
    assert kwargs.get('once') is True


@patch('snotel.snotel.SnotelPoller')
def test_main_once_env_var(mock_poller_class, monkeypatch):
    """``ONCE_MODE=true`` environment variable also enables once mode."""
    instance = MagicMock()
    mock_poller_class.return_value = instance

    monkeypatch.setenv('CONNECTION_STRING', 'BootstrapServer=localhost:9092;EntityPath=snotel')
    monkeypatch.setenv('KAFKA_ENABLE_TLS', 'false')
    monkeypatch.setenv('ONCE_MODE', 'true')

    test_argv = ['snotel', 'feed', '--stations', '838:CO:SNTL']
    with patch.object(sys, 'argv', test_argv):
        main()

    instance.run.assert_called_once()
    _, kwargs = instance.run.call_args
    assert kwargs.get('once') is True
