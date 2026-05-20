"""Verify the bridge exits after one polling cycle when --once is supplied."""

from __future__ import annotations

import sys
from unittest.mock import patch

import pytest

from sensor_community import sensor_community as bridge


@pytest.mark.unit
def test_once_flag_exits_after_single_cycle(monkeypatch):
    """`sensor-community feed --once` should invoke poll_once exactly once."""

    monkeypatch.setenv("CONNECTION_STRING", "BootstrapServer=localhost:9092;EntityPath=test-topic")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    monkeypatch.delenv("ONCE_MODE", raising=False)

    call_count = {"poll_once": 0}

    class _Result:
        sensor_info_count = 0
        sensor_reading_count = 0

    def _fake_poll_once(self, event_producer):
        call_count["poll_once"] += 1
        return _Result()

    class _FakeProducer:
        def __init__(self, *_args, **_kwargs):
            pass

        def flush(self, *_args, **_kwargs):
            return 0

        def produce(self, *_args, **_kwargs):
            return None

        def poll(self, *_args, **_kwargs):
            return 0

    class _FakeEventProducer:
        def __init__(self, *_args, **_kwargs):
            pass

    saved_argv = sys.argv
    sys.argv = [
        "sensor-community",
        "feed",
        "--polling-interval",
        "1",
        "--once",
    ]
    try:
        with patch.object(bridge.SensorCommunityAPI, "poll_once", _fake_poll_once), \
             patch.object(bridge, "Producer", _FakeProducer), \
             patch.object(bridge, "IoSensorCommunityEventProducer", _FakeEventProducer), \
             patch.object(bridge.time, "sleep", lambda *_a, **_kw: None):
            bridge.main()
    finally:
        sys.argv = saved_argv

    assert call_count["poll_once"] == 1


@pytest.mark.unit
def test_once_mode_env_var_enables_single_cycle(monkeypatch):
    """`ONCE_MODE=true` should default `--once` to True."""

    monkeypatch.setenv("CONNECTION_STRING", "BootstrapServer=localhost:9092;EntityPath=test-topic")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    monkeypatch.setenv("ONCE_MODE", "true")

    call_count = {"poll_once": 0}

    class _Result:
        sensor_info_count = 0
        sensor_reading_count = 0

    def _fake_poll_once(self, event_producer):
        call_count["poll_once"] += 1
        return _Result()

    class _FakeProducer:
        def __init__(self, *_args, **_kwargs):
            pass

        def flush(self, *_args, **_kwargs):
            return 0

    class _FakeEventProducer:
        def __init__(self, *_args, **_kwargs):
            pass

    saved_argv = sys.argv
    sys.argv = ["sensor-community", "feed", "--polling-interval", "1"]
    try:
        with patch.object(bridge.SensorCommunityAPI, "poll_once", _fake_poll_once), \
             patch.object(bridge, "Producer", _FakeProducer), \
             patch.object(bridge, "IoSensorCommunityEventProducer", _FakeEventProducer), \
             patch.object(bridge.time, "sleep", lambda *_a, **_kw: None):
            bridge.main()
    finally:
        sys.argv = saved_argv

    assert call_count["poll_once"] == 1
