"""Tests for --once / ONCE_MODE single-cycle execution."""

import os
import sys
from unittest.mock import patch, MagicMock

import pytest

from paris_bicycle_counters import paris_bicycle_counters as bridge


def _patched_poller_factory(call_recorder):
    def _factory(*args, **kwargs):
        inst = MagicMock()
        def _poll(once=False):
            call_recorder['once'] = once
            call_recorder['calls'] += 1
        inst.poll_and_send.side_effect = _poll
        return inst
    return _factory


def test_once_flag_runs_single_cycle(monkeypatch):
    recorder = {'once': None, 'calls': 0}
    monkeypatch.setenv('CONNECTION_STRING',
                       'BootstrapServer=localhost:9092;EntityPath=test-topic')
    monkeypatch.delenv('ONCE_MODE', raising=False)
    monkeypatch.setattr(sys, 'argv', ['paris-bicycle-counters', '--once'])
    with patch.object(bridge, 'ParisBicycleCounterPoller',
                      side_effect=_patched_poller_factory(recorder)):
        bridge.main()
    assert recorder['calls'] == 1
    assert recorder['once'] is True


def test_once_mode_env_var(monkeypatch):
    recorder = {'once': None, 'calls': 0}
    monkeypatch.setenv('CONNECTION_STRING',
                       'BootstrapServer=localhost:9092;EntityPath=test-topic')
    monkeypatch.setenv('ONCE_MODE', 'true')
    monkeypatch.setattr(sys, 'argv', ['paris-bicycle-counters'])
    with patch.object(bridge, 'ParisBicycleCounterPoller',
                      side_effect=_patched_poller_factory(recorder)):
        bridge.main()
    assert recorder['calls'] == 1
    assert recorder['once'] is True


def test_default_runs_continuous(monkeypatch):
    recorder = {'once': None, 'calls': 0}
    monkeypatch.setenv('CONNECTION_STRING',
                       'BootstrapServer=localhost:9092;EntityPath=test-topic')
    monkeypatch.delenv('ONCE_MODE', raising=False)
    monkeypatch.setattr(sys, 'argv', ['paris-bicycle-counters'])
    with patch.object(bridge, 'ParisBicycleCounterPoller',
                      side_effect=_patched_poller_factory(recorder)):
        bridge.main()
    assert recorder['calls'] == 1
    assert recorder['once'] is False
