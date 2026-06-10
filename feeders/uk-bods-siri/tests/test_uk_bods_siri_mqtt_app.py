from __future__ import annotations

import asyncio
from unittest import mock

import pytest

from uk_bods_siri_core.acquisition import FeedSnapshot, VehiclePositionRecord


@pytest.mark.unit
def test_mqtt_feed_once_emits_reference_and_telemetry(tmp_path):
    from uk_bods_siri_mqtt import app as mqtt_app

    api = mock.Mock()
    api.load_snapshot.return_value = FeedSnapshot(
        operators=("A2BR",),
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
            ),
        ),
    )
    fake_client = mock.AsyncMock()
    fake_paho = mock.MagicMock()

    with mock.patch.object(mqtt_app.mqtt, "Client", return_value=fake_paho), mock.patch.object(
        mqtt_app, "UkGovDftBodsMqttMqttClient", return_value=fake_client
    ):
        asyncio.run(
            mqtt_app.feed(
                api=api,
                broker_host="localhost",
                broker_port=1883,
                polling_interval=1,
                state_file=str(tmp_path / "state.json"),
                once=True,
            )
        )

    fake_client.connect.assert_awaited_once()
    fake_client.publish_uk_gov_dft_bods_mqtt_operator.assert_awaited_once()
    fake_client.publish_uk_gov_dft_bods_mqtt_vehicle_position.assert_awaited_once()
    fake_client.disconnect.assert_awaited_once()
