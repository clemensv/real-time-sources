"""Tests for the --once flag added for Fabric notebook hosting."""

from unittest.mock import patch, MagicMock

import pytest

from canada_aqhi import canada_aqhi as bridge


def test_once_flag_exits_after_single_cycle(monkeypatch):
    """`main()` must return after a single poll cycle when --once is set."""

    # Avoid any real Kafka or network behaviour.
    monkeypatch.setattr(bridge, "Producer", lambda config: MagicMock())
    monkeypatch.setattr(bridge, "CaGcWeatherAqhiEventProducer", lambda producer, topic: MagicMock())
    monkeypatch.setattr(bridge, "build_kafka_config", lambda args: ({}, "test-topic"))

    call_count = {"value": 0}

    def fake_poll_once(self, *args, **kwargs):
        call_count["value"] += 1
        return {"communities": 0, "observations": 0, "forecasts": 0}

    monkeypatch.setattr(bridge.CanadaAQHIBridge, "poll_once", fake_poll_once)

    # If --once is not honored, time.sleep would be called and the loop would
    # iterate again — fail loudly if that happens.
    def fail_sleep(_seconds):
        raise AssertionError("time.sleep should not be called when --once is set")

    monkeypatch.setattr(bridge.time, "sleep", fail_sleep)

    monkeypatch.setattr(
        "sys.argv",
        ["canada-aqhi", "feed", "--connection-string", "BootstrapServer=h:9092;EntityPath=t", "--once"],
    )

    bridge.main()

    assert call_count["value"] == 1
