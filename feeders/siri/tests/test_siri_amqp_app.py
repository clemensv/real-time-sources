from __future__ import annotations

from unittest import mock

import pytest

from siri_core.acquisition import FeedSnapshot, VehiclePositionRecord


@pytest.mark.unit
def test_amqp_feed_once_emits_reference_and_telemetry(tmp_path):
    from siri_amqp import app as amqp_app

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
                origin_ref=None,
                origin_name=None,
                destination_ref=None,
                destination_name=None,
                longitude=0.1,
                latitude=52.0,
                bearing=10,
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
    producer = mock.MagicMock()

    amqp_app.feed(api, producer, 1, state_file=str(tmp_path / "state.json"), once=True)

    producer.send_operator.assert_called_once()
    producer.send_vehicle_position.assert_called_once()
    producer.close.assert_called_once()
