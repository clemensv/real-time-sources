from __future__ import annotations

import asyncio
from unittest import mock

import pytest

from siri_core.acquisition import FeedSnapshot, VehiclePositionRecord


@pytest.mark.unit
def test_kafka_feed_once_emits_reference_and_telemetry(tmp_path):
    from siri_kafka import app as kafka_app

    api = mock.Mock()
    api.load_snapshot.return_value = FeedSnapshot(
        operators=("A2BR",),
        operator_feed_urls={"A2BR": "https://example.test/siri"},
        vehicle_positions=(
            VehiclePositionRecord(
                operator_ref="A2BR",
                vehicle_ref="3312",
                line_ref="T12",
                direction_ref="outbound",
                published_line_name="T12",
                origin_ref="0500SLONN009",
                origin_name="Longstanton Park-and-Ride",
                destination_ref="0500ESUTT002",
                destination_name="Windmill Lane",
                longitude=0.054376,
                latitude=52.29166,
                bearing=73,
                recorded_at_time="2026-06-04T05:56:35+00:00",
                valid_until_time="2026-06-04T06:02:14.931+00:00",
                block_ref="T12",
                vehicle_journey_ref="0700",
                origin_aimed_departure_time="2026-06-04T06:00:00+00:00",
                data_frame_ref="2026-06-04",
                dated_vehicle_journey_ref="VJ_1",
                item_identifier="item-1",
                feedurl="https://example.test/siri",
            ),
        ),
    )
    fake_raw_producer = mock.MagicMock()
    fake_raw_producer.flush.return_value = 0
    fake_event_producer = mock.MagicMock()

    with mock.patch.object(kafka_app, "Producer", return_value=fake_raw_producer), mock.patch.object(
        kafka_app, "OrgSiriKafkaEventProducer", return_value=fake_event_producer
    ):
        asyncio.run(
            kafka_app.feed(
                api=api,
                kafka_config={"bootstrap.servers": "localhost:9092"},
                kafka_topic="siri",
                polling_interval=1,
                state_file=str(tmp_path / "state.json"),
                once=True,
            )
        )

    assert fake_event_producer.send_org_siri_kafka_operator.call_count == 1
    assert fake_event_producer.send_org_siri_kafka_vehicle_position.call_count == 1
    assert fake_raw_producer.flush.call_count >= 2


@pytest.mark.unit
def test_kafka_flush_failure_does_not_advance_state(tmp_path):
    from siri_kafka import app as kafka_app

    api = mock.Mock()
    api.load_snapshot.return_value = FeedSnapshot(
        operators=("A2BR",),
        operator_feed_urls={"A2BR": "https://example.test/siri"},
        vehicle_positions=(
            VehiclePositionRecord(
                operator_ref="A2BR",
                vehicle_ref="3312",
                line_ref=None,
                direction_ref=None,
                published_line_name=None,
                origin_ref=None,
                origin_name=None,
                destination_ref=None,
                destination_name=None,
                longitude=None,
                latitude=None,
                bearing=None,
                recorded_at_time="2026-06-04T05:56:35+00:00",
                valid_until_time=None,
                block_ref=None,
                vehicle_journey_ref=None,
                origin_aimed_departure_time=None,
                data_frame_ref=None,
                dated_vehicle_journey_ref=None,
                item_identifier="item-1",
                feedurl="https://example.test/siri",
            ),
        ),
    )
    fake_raw_producer = mock.MagicMock()
    fake_raw_producer.flush.return_value = 1
    fake_event_producer = mock.MagicMock()
    state_path = tmp_path / "state.json"

    with mock.patch.object(kafka_app, "Producer", return_value=fake_raw_producer), mock.patch.object(
        kafka_app, "OrgSiriKafkaEventProducer", return_value=fake_event_producer
    ):
        with pytest.raises(RuntimeError):
            asyncio.run(
                kafka_app.feed(
                    api=api,
                    kafka_config={"bootstrap.servers": "localhost:9092"},
                    kafka_topic="siri",
                    polling_interval=1,
                    state_file=str(state_path),
                    once=True,
                )
            )

    assert not state_path.exists()
