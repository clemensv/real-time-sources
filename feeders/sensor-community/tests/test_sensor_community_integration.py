"""Integration tests for the Sensor.Community bridge with mocked HTTP."""

from __future__ import annotations

import pytest
import requests_mock

from sensor_community.sensor_community import SensorCommunityAPI


class DummyEventProducer:
    """Capture emitted events for assertions."""

    def __init__(self) -> None:
        self.sensor_infos: list[tuple[str, int, object]] = []
        self.sensor_readings: list[tuple[str, int, object]] = []

    def send_io_sensor_community_sensor_info(self, _feedurl, _sensor_id, data, flush_producer=False):
        self.sensor_infos.append((_feedurl, _sensor_id, data))

    def send_io_sensor_community_sensor_reading(self, _feedurl, _sensor_id, data, flush_producer=False):
        self.sensor_readings.append((_feedurl, _sensor_id, data))


@pytest.mark.integration
class TestSensorCommunityPolling:
    """Test polling and event emission with mocked HTTP responses."""

    def test_poll_once_emits_sensor_info_and_sensor_reading(self):
        api = SensorCommunityAPI(sensor_types="SDS011", state_file="")
        event_producer = DummyEventProducer()
        payload = [
            {
                "timestamp": "2026-04-06 10:24:02",
                "sensor": {
                    "sensor_type": {"name": "SDS011", "manufacturer": "Nova Fitness", "id": 14},
                    "id": 36083,
                    "pin": "1",
                },
                "location": {
                    "id": 9042,
                    "longitude": "25.62",
                    "country": "BG",
                    "altitude": "220.0",
                    "latitude": "42.42",
                    "indoor": 0,
                },
                "sensordatavalues": [
                    {"value": "5.00", "value_type": "P1", "id": 12345},
                    {"value": "3.33", "value_type": "P2", "id": 12346},
                ],
            }
        ]

        with requests_mock.Mocker() as mocker:
            mocker.get("https://data.sensor.community/airrohr/v1/filter/type=SDS011", json=payload)
            result = api.poll_once(event_producer)

        assert result.sensor_info_count == 1
        assert result.sensor_reading_count == 1
        assert len(event_producer.sensor_infos) == 1
        assert len(event_producer.sensor_readings) == 1
        feed_url, sensor_id, info = event_producer.sensor_infos[0]
        assert feed_url == "https://data.sensor.community/airrohr/v1/sensor/36083/"
        assert sensor_id == 36083
        assert info.sensor_type_name == "SDS011"
        assert info.country == "BG"
        _, _, reading = event_producer.sensor_readings[0]
        assert reading.pm10_ug_m3 == 5.0
        assert reading.pm2_5_ug_m3 == 3.33

    def test_poll_once_skips_duplicate_reading_but_still_keeps_state(self):
        api = SensorCommunityAPI(sensor_types="SDS011", state_file="")
        event_producer = DummyEventProducer()
        payload = [
            {
                "timestamp": "2026-04-06 10:24:02",
                "sensor": {
                    "sensor_type": {"name": "SDS011", "manufacturer": "Nova Fitness", "id": 14},
                    "id": 36083,
                    "pin": "1",
                },
                "location": {
                    "id": 9042,
                    "longitude": "25.62",
                    "country": "BG",
                    "altitude": "220.0",
                    "latitude": "42.42",
                    "indoor": 0,
                },
                "sensordatavalues": [
                    {"value": "5.00", "value_type": "P1", "id": 12345},
                    {"value": "3.33", "value_type": "P2", "id": 12346},
                ],
            }
        ]

        with requests_mock.Mocker() as mocker:
            mocker.get("https://data.sensor.community/airrohr/v1/filter/type=SDS011", json=payload)
            first = api.poll_once(event_producer)
            second = api.poll_once(event_producer)

        assert first.sensor_info_count == 1
        assert first.sensor_reading_count == 1
        assert second.sensor_info_count == 0
        assert second.sensor_reading_count == 0
        assert len(event_producer.sensor_infos) == 1
        assert len(event_producer.sensor_readings) == 1
