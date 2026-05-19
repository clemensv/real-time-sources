"""Test that --once causes the bridge to exit after a single polling cycle."""

import sys
from unittest.mock import patch, MagicMock

import pytest

import elexon_bmrs.elexon_bmrs as bridge


def _fake_poller_factory(call_counter):
    def _ctor(*_args, **_kwargs):
        instance = MagicMock()

        def _poll(once=False):
            call_counter['calls'] += 1
            call_counter['once'] = once

        instance.poll_and_send.side_effect = _poll
        return instance

    return _ctor


def test_once_flag_runs_single_cycle(monkeypatch):
    """--once must be threaded into poll_and_send(once=True) so the loop exits."""
    counter = {'calls': 0, 'once': None}

    monkeypatch.setattr(
        bridge,
        'ElexonBMRSPoller',
        _fake_poller_factory(counter),
    )
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'elexon-bmrs',
            '--once',
            '--connection-string',
            'BootstrapServer=localhost:9092;EntityPath=test',
        ],
    )
    monkeypatch.setenv('KAFKA_ENABLE_TLS', 'false')

    bridge.main()

    assert counter['calls'] == 1
    assert counter['once'] is True


def test_once_mode_env_var(monkeypatch):
    """ONCE_MODE=true env var must also trigger single-cycle exit."""
    counter = {'calls': 0, 'once': None}

    monkeypatch.setattr(
        bridge,
        'ElexonBMRSPoller',
        _fake_poller_factory(counter),
    )
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'elexon-bmrs',
            '--connection-string',
            'BootstrapServer=localhost:9092;EntityPath=test',
        ],
    )
    monkeypatch.setenv('KAFKA_ENABLE_TLS', 'false')
    monkeypatch.setenv('ONCE_MODE', 'true')

    bridge.main()

    assert counter['calls'] == 1
    assert counter['once'] is True
