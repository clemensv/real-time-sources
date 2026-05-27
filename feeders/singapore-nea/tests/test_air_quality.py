"""Unit tests for Singapore NEA air quality support."""

from unittest.mock import MagicMock, patch

from singapore_nea.air_quality import (
    NEAAirQualityAPI,
    fetch_and_send_pm25,
    fetch_and_send_psi,
    fetch_and_send_regions,
)


SAMPLE_PSI_RESPONSE = {
    "region_metadata": [
        {"name": "west", "label_location": {"latitude": 1.35735, "longitude": 103.7}},
        {"name": "east", "label_location": {"latitude": 1.35735, "longitude": 103.94}},
        {"name": "central", "label_location": {"latitude": 1.35735, "longitude": 103.82}},
        {"name": "south", "label_location": {"latitude": 1.29587, "longitude": 103.82}},
        {"name": "north", "label_location": {"latitude": 1.41803, "longitude": 103.82}},
    ],
    "items": [
        {
            "timestamp": "2026-04-08T19:00:00+08:00",
            "update_timestamp": "2026-04-08T19:00:48+08:00",
            "readings": {
                "o3_sub_index": {"west": 17, "east": 34, "central": 45, "south": 34, "north": 18},
                "pm10_twenty_four_hourly": {"west": 24, "east": 41, "central": 41, "south": 26, "north": 26},
                "pm10_sub_index": {"west": 24, "east": 41, "central": 41, "south": 26, "north": 26},
                "co_sub_index": {"west": 3, "east": 7, "central": 6, "south": 5, "north": 7},
                "pm25_twenty_four_hourly": {"west": 18, "east": 26, "central": 30, "south": 17, "north": 19},
                "so2_sub_index": {"west": 3, "east": 5, "central": 3, "south": 5, "north": 2},
                "co_eight_hour_max": {"west": 0, "east": 1, "central": 1, "south": 1, "north": 1},
                "no2_one_hour_max": {"west": 29, "east": 44, "central": 41, "south": 36, "north": 40},
                "so2_twenty_four_hourly": {"west": 5, "east": 7, "central": 5, "south": 8, "north": 3},
                "pm25_sub_index": {"west": 57, "east": 66, "central": 71, "south": 57, "north": 59},
                "psi_twenty_four_hourly": {"west": 57, "east": 66, "central": 71, "south": 57, "north": 59},
                "o3_eight_hour_max": {"west": 39, "east": 79, "central": 107, "south": 80, "north": 43},
            },
        }
    ],
}

SAMPLE_PM25_RESPONSE = {
    "region_metadata": SAMPLE_PSI_RESPONSE["region_metadata"],
    "items": [
        {
            "timestamp": "2026-04-08T19:00:00+08:00",
            "update_timestamp": "2026-04-08T19:00:47+08:00",
            "readings": {
                "pm25_one_hourly": {
                    "west": 4,
                    "east": 19,
                    "central": 29,
                    "south": 21,
                    "north": 16,
                }
            },
        }
    ],
}


class TestNEAAirQualityAPI:
    def test_get_regions_returns_all_regions(self):
        api = NEAAirQualityAPI()
        with patch.object(api, "get_psi", return_value=SAMPLE_PSI_RESPONSE):
            regions = api.get_regions()

        assert set(regions.keys()) == {"west", "east", "central", "south", "north"}
        assert regions["west"].longitude == 103.7


class TestRegionEmission:
    def test_fetch_and_send_regions(self):
        api = NEAAirQualityAPI()
        producer = MagicMock()
        producer.producer = MagicMock()

        with patch.object(api, "get_psi", return_value=SAMPLE_PSI_RESPONSE):
            count = fetch_and_send_regions(api, producer)

        assert count == 5
        assert producer.send_sg_gov_nea_air_quality_region.call_count == 5
        producer.producer.flush.assert_called_once()


class TestPSIEmission:
    def test_fetch_and_send_psi_emits_new_readings(self):
        api = NEAAirQualityAPI()
        producer = MagicMock()
        producer.producer = MagicMock()
        previous = {}

        with patch.object(api, "get_psi", return_value=SAMPLE_PSI_RESPONSE):
            count = fetch_and_send_psi(api, producer, previous)

        assert count == 5
        assert len(previous) == 5
        assert producer.send_sg_gov_nea_air_quality_psireading.call_count == 5

    def test_fetch_and_send_psi_deduplicates_timestamp(self):
        api = NEAAirQualityAPI()
        producer = MagicMock()
        producer.producer = MagicMock()
        previous = {
            f"{region}:2026-04-08T19:00:00+08:00": "2026-04-08T19:00:00+08:00"
            for region in ("west", "east", "central", "south", "north")
        }

        with patch.object(api, "get_psi", return_value=SAMPLE_PSI_RESPONSE):
            count = fetch_and_send_psi(api, producer, previous)

        assert count == 0


class TestPM25Emission:
    def test_fetch_and_send_pm25_emits_new_readings(self):
        api = NEAAirQualityAPI()
        producer = MagicMock()
        producer.producer = MagicMock()
        previous = {}

        with patch.object(api, "get_pm25", return_value=SAMPLE_PM25_RESPONSE):
            count = fetch_and_send_pm25(api, producer, previous)

        assert count == 5
        assert len(previous) == 5
        assert producer.send_sg_gov_nea_air_quality_pm25_reading.call_count == 5

