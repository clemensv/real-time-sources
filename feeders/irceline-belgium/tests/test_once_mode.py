"""Test that --once exits after one polling cycle."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from irceline_belgium import irceline_belgium as bridge


@pytest.mark.unit
def test_once_mode_exits_after_single_cycle(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"

    call_count = {"emit_reference": 0, "poll": 0}

    def fake_emit_reference(self, station_producer, timeseries_producer):
        call_count["emit_reference"] += 1
        return {}

    def fake_poll(self, *, timeseries_by_id, producer, state):
        call_count["poll"] += 1
        return 0

    class FakeProducer:
        def __init__(self, *args, **kwargs):
            pass

        def produce(self, *args, **kwargs):
            pass

        def flush(self, *args, **kwargs):
            pass

        def poll(self, *args, **kwargs):
            return 0

    class FakeEventProducer:
        def __init__(self, producer, topic):
            self.producer = producer

    monkeypatch.setattr(bridge.IrcelineBelgiumAPI, "emit_reference_data", fake_emit_reference)
    monkeypatch.setattr(bridge.IrcelineBelgiumAPI, "poll_observations", fake_poll)
    monkeypatch.setattr(bridge, "Producer", FakeProducer)
    monkeypatch.setattr(bridge, "BeIrcelineStationsEventProducer", FakeEventProducer)
    monkeypatch.setattr(bridge, "BeIrcelineTimeseriesEventProducer", FakeEventProducer)

    # Ensure time.sleep is never called (would hang) and raises if it is.
    def _no_sleep(_):
        raise AssertionError("time.sleep should not be invoked in --once mode")

    monkeypatch.setattr(bridge.time, "sleep", _no_sleep)

    api = bridge.IrcelineBelgiumAPI()
    api.run_feed(
        kafka_config={"bootstrap.servers": "localhost:9092"},
        kafka_topic="irceline-belgium",
        polling_interval=900,
        state_file=str(state_file),
        once=True,
    )

    assert call_count["emit_reference"] == 1
    assert call_count["poll"] == 1


@pytest.mark.unit
def test_once_flag_parses_from_argv(monkeypatch):
    captured = {}

    def fake_run_feed(self, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(bridge.IrcelineBelgiumAPI, "run_feed", fake_run_feed)
    monkeypatch.setattr(
        bridge.IrcelineBelgiumAPI,
        "build_kafka_config",
        classmethod(lambda cls, args: ({"bootstrap.servers": "localhost:9092"}, "irceline-belgium")),
    )
    monkeypatch.setattr(
        "sys.argv",
        ["irceline-belgium", "feed", "--kafka-bootstrap-servers", "localhost:9092", "--once"],
    )

    bridge.main()
    assert captured.get("once") is True
