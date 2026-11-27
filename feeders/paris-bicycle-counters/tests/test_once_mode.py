"""Tests for --once / ONCE_MODE single-cycle execution."""

import argparse
import asyncio
import os
import sys
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

import pytest
import requests

from paris_bicycle_counters import paris_bicycle_counters as bridge
from paris_bicycle_counters_amqp import app as amqp_app
from paris_bicycle_counters_core import BicycleCount, Counter


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


@pytest.fixture
def amqp_poll(monkeypatch, tmp_path):
    args = argparse.Namespace(state_file=str(tmp_path / "amqp-state.json"), once=True, mock_mode=False)
    counter = Counter(
        ce_id="counter-1/info", counter_id="counter-1", counter_name="Counter 1",
        channel_name=None, installation_date=None, longitude=None, latitude=None,
    )
    count = BicycleCount(
        ce_id="counter-1/count", counter_id="counter-1", counter_name="Counter 1",
        count=17, date=datetime.now(timezone.utc), longitude=None, latitude=None,
    )
    locations = MagicMock(return_value=[counter])
    counts = MagicMock(return_value=[count])
    build = MagicMock()
    monkeypatch.setattr(amqp_app.ParisBicycleCounterPoller, "fetch_counter_locations", locations)
    monkeypatch.setattr(amqp_app.ParisBicycleCounterPoller, "fetch_bicycle_counts", counts)
    monkeypatch.setattr(amqp_app, "_build_amqp_producer", build)
    return args, locations, counts, build


@pytest.mark.unit
class TestAmqpPollLifecycle:
    def test_connection_does_not_span_acquisition_or_poll_sleep(self, amqp_poll, monkeypatch):
        args, locations, counts, build = amqp_poll
        counter = locations.return_value[0]
        count = counts.return_value[0]
        active = []
        created = []
        emitted = []

        def open_producer(_args):
            assert not active
            producer = MagicMock()
            producer.close.side_effect = lambda: active.remove(producer)
            producer.send_counter.side_effect = lambda **kwargs: emitted.append(("reference", kwargs["_counter_id"]))
            producer.send_bicycle_count.side_effect = lambda **kwargs: emitted.append(("measurement", kwargs["_counter_id"]))
            active.append(producer)
            created.append(producer)
            return producer

        def acquire(rows):
            assert not active, "AMQP connection remained open during upstream acquisition"
            return rows

        async def between_polls(_seconds):
            assert not active, "AMQP connection remained open during the polling interval"
            args.once = True

        build.side_effect = open_producer
        locations.side_effect = lambda: acquire([counter])
        counts.side_effect = lambda **kwargs: acquire([count])
        monkeypatch.setattr(amqp_app.asyncio, "sleep", between_polls)
        args.once = False

        asyncio.run(amqp_app._async_main(args))

        assert len(created) == 2
        assert emitted == [
            ("reference", counter.counter_id),
            ("measurement", count.counter_id),
            ("reference", counter.counter_id),
        ]
        for producer in created:
            producer.close.assert_called_once()
        assert not active

    def test_upstream_failure_is_visible_without_opening_a_connection(self, amqp_poll):
        args, _locations, counts, build = amqp_poll
        counts.side_effect = requests.ReadTimeout("Paris count acquisition timed out")

        with pytest.raises(requests.ReadTimeout, match="Paris count acquisition timed out"):
            asyncio.run(amqp_app._async_main(args))

        build.assert_not_called()
        assert not os.path.exists(args.state_file)

    def test_delivery_failure_closes_connection_without_advancing_state(self, amqp_poll, tmp_path):
        args, _locations, _counts, build = amqp_poll
        state_file = tmp_path / "amqp-state.json"
        original_state = '{"seen_keys": ["previous-counter|2026-11-01T00:00:00Z"]}'
        state_file.write_text(original_state, encoding="utf-8")
        producer = build.return_value
        producer.send_bicycle_count.side_effect = RuntimeError("AMQP delivery failed")

        with pytest.raises(RuntimeError, match="AMQP delivery failed"):
            asyncio.run(amqp_app._async_main(args))

        producer.close.assert_called_once()
        assert state_file.read_text(encoding="utf-8") == original_state
