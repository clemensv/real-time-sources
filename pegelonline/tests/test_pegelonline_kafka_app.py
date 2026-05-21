"""Tests for the ``pegelonline_kafka`` feeder.

The Kafka producer is mocked so we can run the full ``feed`` coroutine in
``--once`` mode and assert flush semantics + per-message arguments without
needing a live broker.
"""

from __future__ import annotations

import asyncio
from unittest import mock

import pytest


@pytest.mark.unit
def test_kafka_feed_once_emits_stations_and_measurements(tmp_path):
    from pegelonline_kafka import app as kafka_app

    api = mock.Mock()
    api.list_stations.return_value = [{
        "uuid": "STATION-1",
        "number": "1",
        "shortname": "MAXAU",
        "longname": "MAXAU",
        "km": 362.3,
        "agency": "WSV",
        "longitude": 8.31,
        "latitude": 49.01,
        "water": {"shortname": "RHEIN", "longname": "RHEIN"},
    }]
    api.get_water_levels.return_value = {
        "STATION-1": {
            "timestamp": "2024-01-15T12:00:00+01:00",
            "value": 450,
            "stateMnwMhw": "normal",
            "stateNswHsw": "unknown",
        }
    }

    fake_raw_producer = mock.MagicMock()
    fake_event_producer = mock.MagicMock()

    with mock.patch.object(kafka_app, "Producer", return_value=fake_raw_producer), \
         mock.patch.object(kafka_app, "DeWsvPegelonlineKafkaEventProducer",
                           return_value=fake_event_producer):
        asyncio.run(kafka_app.feed(
            api=api,
            kafka_config={"bootstrap.servers": "localhost:9092"},
            kafka_topic="test-topic",
            polling_interval=1,
            state_file=str(tmp_path / "state.json"),
            once=True,
        ))

    assert fake_event_producer.send_de_wsv_pegelonline_kafka_station.call_count == 1
    station_call = fake_event_producer.send_de_wsv_pegelonline_kafka_station.call_args
    assert station_call.kwargs["_station_id"] == "STATION-1"
    assert station_call.kwargs["flush_producer"] is False

    assert fake_event_producer.send_de_wsv_pegelonline_kafka_current_measurement.call_count == 1
    measurement_call = fake_event_producer.send_de_wsv_pegelonline_kafka_current_measurement.call_args
    assert measurement_call.kwargs["_station_id"] == "STATION-1"
    assert measurement_call.kwargs["flush_producer"] is False

    # Stations flush + measurements flush + final flush
    assert fake_raw_producer.flush.call_count >= 2


@pytest.mark.unit
def test_kafka_feed_send_failure_still_advances_state(tmp_path):
    """A broker hiccup must not cause the same measurement to retry forever."""
    from pegelonline_kafka import app as kafka_app

    api = mock.Mock()
    api.list_stations.return_value = []
    api.get_water_levels.return_value = {
        "S1": {"timestamp": "t1", "value": 1, "stateMnwMhw": "n", "stateNswHsw": "u"},
    }

    fake_raw_producer = mock.MagicMock()
    fake_event_producer = mock.MagicMock()
    fake_event_producer.send_de_wsv_pegelonline_kafka_current_measurement.side_effect = (
        RuntimeError("broker down")
    )

    state_path = tmp_path / "state.json"
    with mock.patch.object(kafka_app, "Producer", return_value=fake_raw_producer), \
         mock.patch.object(kafka_app, "DeWsvPegelonlineKafkaEventProducer",
                           return_value=fake_event_producer):
        asyncio.run(kafka_app.feed(
            api=api,
            kafka_config={"bootstrap.servers": "localhost:9092"},
            kafka_topic="t",
            polling_interval=1,
            state_file=str(state_path),
            once=True,
        ))

    import json
    assert json.loads(state_path.read_text())["S1"]["timestamp"] == "t1"
