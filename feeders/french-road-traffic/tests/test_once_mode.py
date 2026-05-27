"""Verify --once causes the bridge to exit after a single polling cycle."""

from __future__ import annotations

from unittest import mock

import pytest

from french_road_traffic import french_road_traffic as bridge


@pytest.fixture
def stub_kafka(monkeypatch):
    """Replace the Confluent Kafka Producer and generated event producers."""

    producer_mock = mock.MagicMock()
    monkeypatch.setattr(bridge, "Producer", mock.MagicMock(return_value=producer_mock))
    monkeypatch.setattr(
        bridge,
        "FrGouvTransportBisonFuteTrafficFlowEventProducer",
        mock.MagicMock(),
    )
    monkeypatch.setattr(
        bridge,
        "FrGouvTransportBisonFuteRoadEventEventProducer",
        mock.MagicMock(),
    )
    return producer_mock


def test_run_bridge_once_exits_after_single_cycle(monkeypatch, stub_kafka):
    """When once=True, run_bridge must return after one fetch cycle."""

    monkeypatch.setattr(bridge, "fetch_xml", mock.MagicMock(return_value=b"<x/>"))
    monkeypatch.setattr(bridge, "parse_traffic_flow_xml", mock.MagicMock(return_value=[]))
    monkeypatch.setattr(bridge, "parse_road_events_xml", mock.MagicMock(return_value=[]))

    sleep_calls = []
    monkeypatch.setattr(bridge.time, "sleep", lambda s: sleep_calls.append(s))

    bridge.run_bridge(
        kafka_config={"bootstrap.servers": "x:9092"},
        topic_flow="t-flow",
        topic_events="t-events",
        polling_interval=1,
        once=True,
    )

    assert bridge.fetch_xml.call_count == 2  # flow + events, single cycle
    assert sleep_calls == []  # no polling sleep when --once


def test_main_once_flag_triggers_single_cycle(monkeypatch, stub_kafka):
    """`feed --once` should call run_bridge with once=True and exit."""

    run_calls = {}

    def fake_run_bridge(*args, **kwargs):
        run_calls["args"] = args
        run_calls["kwargs"] = kwargs

    monkeypatch.setattr(bridge, "run_bridge", fake_run_bridge)
    monkeypatch.setenv("KAFKA_BOOTSTRAP_SERVERS", "x:9092")
    monkeypatch.setattr(
        bridge.sys,
        "argv",
        ["french-road-traffic", "feed", "--once"],
    )

    bridge.main()

    assert run_calls["kwargs"].get("once") is True
