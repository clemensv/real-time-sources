"""Test that --once causes the feed loop to exit after a single cycle."""

import sys
from unittest.mock import patch, MagicMock

import pytest

from syke_hydro import syke_hydro as bridge


def test_once_flag_exits_after_one_cycle(monkeypatch):
    """With --once set, main() must return after a single polling cycle."""
    monkeypatch.setattr(sys, 'argv', [
        'syke-hydro',
        '--connection-string', 'BootstrapServer=localhost:9092;EntityPath=test',
        '--once',
        'feed',
    ])
    monkeypatch.setenv('KAFKA_ENABLE_TLS', 'false')

    feed_calls = {'n': 0}

    def _fake_feed(api, producer, stations_by_id, previous_readings):
        feed_calls['n'] += 1
        return 0

    def _boom(*_a, **_kw):
        raise AssertionError("time.sleep must not be called in --once mode")

    with patch.object(bridge, 'send_stations', return_value={}) as send_stations_mock, \
         patch.object(bridge, 'feed_observations', side_effect=_fake_feed), \
         patch.object(bridge, 'Producer', return_value=MagicMock()), \
         patch.object(bridge, 'FISYKEHydrologyEventProducer', return_value=MagicMock()), \
         patch.object(bridge.time, 'sleep', side_effect=_boom):
        bridge.main()

    assert feed_calls['n'] == 1
    send_stations_mock.assert_called_once()


def test_once_env_var_enables_once_mode(monkeypatch):
    """ONCE_MODE=true env var must set args.once even without the CLI flag."""
    monkeypatch.setattr(sys, 'argv', [
        'syke-hydro',
        '--connection-string', 'BootstrapServer=localhost:9092;EntityPath=test',
        'feed',
    ])
    monkeypatch.setenv('ONCE_MODE', 'true')
    monkeypatch.setenv('KAFKA_ENABLE_TLS', 'false')

    feed_calls = {'n': 0}

    def _fake_feed(*_a, **_kw):
        feed_calls['n'] += 1
        return 0

    with patch.object(bridge, 'send_stations', return_value={}), \
         patch.object(bridge, 'feed_observations', side_effect=_fake_feed), \
         patch.object(bridge, 'Producer', return_value=MagicMock()), \
         patch.object(bridge, 'FISYKEHydrologyEventProducer', return_value=MagicMock()), \
         patch.object(bridge.time, 'sleep', side_effect=AssertionError("sleep must not be called")):
        bridge.main()

    assert feed_calls['n'] == 1
