"""Verify the --once flag causes main() to exit after a single polling cycle."""

import sys
from unittest.mock import MagicMock, patch

import pytest

from hongkong_epd import hongkong_epd as bridge


@pytest.fixture
def fake_kafka_producer(monkeypatch):
    """Replace confluent_kafka.Producer and the generated event producer."""
    fake_producer = MagicMock()
    monkeypatch.setattr(bridge, "Producer", MagicMock(return_value=fake_producer))

    fake_event_producer = MagicMock()
    fake_event_producer.producer = fake_producer
    monkeypatch.setattr(
        bridge,
        "HKGovEPDAQHIEventProducer",
        MagicMock(return_value=fake_event_producer),
    )
    return fake_event_producer


def test_once_flag_exits_after_one_cycle(tmp_path, fake_kafka_producer, monkeypatch):
    """With --once the polling loop must not sleep and must exit after one cycle."""
    state_file = tmp_path / "state.json"
    sleep_mock = MagicMock()
    send_stations_mock = MagicMock(return_value=18)
    feed_readings_mock = MagicMock(return_value=3)

    monkeypatch.setattr(bridge.time, "sleep", sleep_mock)
    monkeypatch.setattr(bridge, "send_stations", send_stations_mock)
    monkeypatch.setattr(bridge, "feed_readings", feed_readings_mock)

    argv = [
        "hongkong-epd",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=test",
        "--topic", "test-topic",
        "--state-file", str(state_file),
        "--polling-interval", "1",
        "--once",
        "feed",
    ]
    with patch.object(sys, "argv", argv):
        bridge.main()

    assert send_stations_mock.call_count == 1
    assert feed_readings_mock.call_count == 1
    sleep_mock.assert_not_called()


def test_once_via_env_var(tmp_path, fake_kafka_producer, monkeypatch):
    """ONCE_MODE=true should be honored the same as --once."""
    state_file = tmp_path / "state.json"
    sleep_mock = MagicMock()
    monkeypatch.setattr(bridge.time, "sleep", sleep_mock)
    monkeypatch.setattr(bridge, "send_stations", MagicMock(return_value=0))
    monkeypatch.setattr(bridge, "feed_readings", MagicMock(return_value=0))
    monkeypatch.setenv("ONCE_MODE", "true")

    argv = [
        "hongkong-epd",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=test",
        "--topic", "test-topic",
        "--state-file", str(state_file),
        "--polling-interval", "1",
        "feed",
    ]
    with patch.object(sys, "argv", argv):
        bridge.main()

    sleep_mock.assert_not_called()
