"""Unit tests for the King County marine bridge."""

from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest
import requests

from king_county_marine.king_county_marine import (
    KingCountyMarineBridge,
    create_retrying_session,
    infer_sensor_level,
    infer_station_id,
    is_current_buoy_dataset,
    parse_float,
    parse_station_location,
)


VIEW = {
    "id": "6trh-ufm8",
    "name": "Coupeville Wharf Mooring Raw Data Output",
    "description": "Geography: The mooring is located at Latitude 48.2228253 and Longitude -122.6884251",
}

ROW = {
    "unixtimestamp": "1674027900000",
    "water_temp_c": "7.9413",
    "cond_sm": "2.35223",
    "pres_db": "3.858",
    "do_mgl": "9.099",
    "sonde_ph": "7.73",
    "chl_fluor_ugl": "1.291",
    "turb_ntu": "0.469",
    "std_dev_chl_fluor": "0.09",
    "std_dev_turb": "0.03",
    "sal_psu": "21.7788",
    "do_pct_sat": "88.38",
    "sonde_batt_v": "13.8",
    "suna_nitraten_um": "24",
    "suna_nitraten_mgl": "0.337",
}


@pytest.mark.unit
class TestHelpers:
    def test_create_retrying_session(self):
        session = create_retrying_session()
        https_adapter = session.get_adapter("https://data.kingcounty.gov")

        assert session.headers["User-Agent"] == "GitHub-Copilot-CLI/1.0"
        assert https_adapter.max_retries.total == 5
        assert https_adapter.max_retries.backoff_factor == 2.0

    def test_parse_float(self):
        assert parse_float("1.23") == pytest.approx(1.23)
        assert parse_float("-99.99") is None
        assert parse_float("NA") is None

    def test_parse_station_location(self):
        lat, lon = parse_station_location(VIEW["description"])
        assert lat == pytest.approx(48.2228253)
        assert lon == pytest.approx(-122.6884251)

    def test_station_identity(self):
        assert infer_station_id("Penn Cove Entrance Buoy Raw Data Output - Surface") == "penn-cove-entrance-buoy-surface"
        assert infer_sensor_level("Penn Cove Entrance Buoy Raw Data Output - Bottom") == "bottom"

    def test_current_dataset_filter(self):
        assert is_current_buoy_dataset({"resource": {"name": "Port Susan Buoy Raw Data Output (Dec 20, 2023 - present)", "type": "dataset"}})
        assert not is_current_buoy_dataset({"resource": {"name": "Port Susan Buoy Raw Data Output (Feb 3, 2022 - Dec 20, 2023)", "type": "dataset"}})


@pytest.mark.unit
class TestNormalization:
    def test_build_station(self):
        bridge = KingCountyMarineBridge()
        station = bridge.build_station(VIEW)
        assert station.station_id == "coupeville-wharf-mooring"
        assert station.latitude == pytest.approx(48.2228253)

    def test_build_reading(self):
        bridge = KingCountyMarineBridge()
        bridge.station_metadata["6trh-ufm8"] = {
            "station_id": "coupeville-wharf-mooring",
            "station_name": "Coupeville Wharf Mooring Raw Data Output",
            "sensor_level": "water-column",
        }
        reading = bridge.build_reading("6trh-ufm8", ROW)
        assert reading.station_id == "coupeville-wharf-mooring"
        assert reading.water_temperature_c == pytest.approx(7.9413)
        assert reading.nitrate_mg_l == pytest.approx(0.337)


@pytest.mark.unit
class TestPolling:
    def test_emit_reference_data_keeps_successful_datasets(self):
        bridge = KingCountyMarineBridge()
        bridge.discover_datasets = Mock(return_value=[{"id": "6trh-ufm8"}, {"id": "broken"}])
        bridge.fetch_view = Mock(side_effect=[VIEW, requests.RequestException("reset by peer")])
        producer = Mock()
        producer.producer = Mock()

        sent = bridge.emit_reference_data(producer)

        assert sent == 1
        assert list(bridge.station_metadata) == ["6trh-ufm8"]
        assert producer.send_us_wa_king_county_marine_station.call_count == 1
        producer.producer.flush.assert_called_once()

    @patch("king_county_marine.king_county_marine._save_state")
    def test_poll_and_send_continues_after_dataset_fetch_failure(self, _mock_save_state):
        bridge = KingCountyMarineBridge(state_file="state.json")
        bridge.last_reference_refresh = datetime.now(timezone.utc).isoformat()
        bridge.station_metadata = {
            "good": {
                "station_id": "coupeville-wharf-mooring",
                "station_name": "Coupeville Wharf Mooring Raw Data Output",
                "sensor_level": "water-column",
            },
            "bad": {
                "station_id": "bad-station",
                "station_name": "Bad Station",
                "sensor_level": "surface",
            },
        }
        bridge.fetch_rows = Mock(side_effect=[requests.RequestException("timeout"), [ROW]])
        producer = Mock()
        producer.producer = Mock()

        bridge.poll_and_send(producer, once=True)

        assert producer.send_us_wa_king_county_marine_water_quality_reading.call_count == 1

    @patch("king_county_marine.king_county_marine._save_state")
    def test_poll_and_send_emits_reference_and_telemetry(self, _mock_save_state):
        bridge = KingCountyMarineBridge(state_file="state.json")
        bridge.emit_reference_data = Mock(return_value=1)
        bridge.station_metadata = {
            "6trh-ufm8": {
                "station_id": "coupeville-wharf-mooring",
                "station_name": "Coupeville Wharf Mooring Raw Data Output",
                "sensor_level": "water-column",
            }
        }
        bridge.fetch_rows = Mock(return_value=[ROW])
        producer = Mock()
        producer.producer = Mock()

        bridge.poll_and_send(producer, once=True)

        assert producer.send_us_wa_king_county_marine_water_quality_reading.call_count == 1
