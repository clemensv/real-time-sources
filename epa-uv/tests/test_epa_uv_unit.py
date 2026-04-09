"""Unit tests for the EPA UV bridge."""

from unittest.mock import Mock, patch

import pytest

from epa_uv.epa_uv import (
    DAILY_URL,
    HOURLY_URL,
    EPAUVBridge,
    parse_daily_row,
    parse_hourly_row,
    parse_locations,
)


HOURLY_ROWS = [
    {"ORDER": 1, "CITY": "Seattle", "STATE": "WA", "DATE_TIME": "Apr/09/2026 04 AM", "UV_VALUE": 0},
    {"ORDER": 2, "CITY": "Seattle", "STATE": "WA", "DATE_TIME": "Apr/09/2026 05 AM", "UV_VALUE": 1},
]
DAILY_ROWS = [
    {"CITY": "Seattle", "STATE": "WA", "UV_INDEX": "5", "UV_ALERT": "0", "DATE": "Apr/09/2026"}
]


@pytest.mark.unit
class TestParsing:
    def test_parse_locations(self):
        assert parse_locations("Seattle,WA;Portland,OR") == [("Seattle", "WA"), ("Portland", "OR")]

    def test_parse_hourly_row(self):
        forecast = parse_hourly_row("Seattle", "WA", HOURLY_ROWS[0])
        assert forecast.location_id == "seattle-wa"
        assert forecast.forecast_datetime == "2026-04-09T04:00:00"

    def test_parse_daily_row(self):
        forecast = parse_daily_row("Seattle", "WA", DAILY_ROWS[0])
        assert forecast.location_id == "seattle-wa"
        assert forecast.forecast_date == "2026-04-09"
        assert forecast.uv_alert == "0"


@pytest.mark.unit
class TestFetch:
    def test_fetches_hourly_and_daily_endpoints(self):
        bridge = EPAUVBridge([("Seattle", "WA")])
        first = Mock()
        first.json.return_value = HOURLY_ROWS
        first.raise_for_status.return_value = None
        second = Mock()
        second.json.return_value = DAILY_ROWS
        second.raise_for_status.return_value = None
        bridge.session.get = Mock(side_effect=[first, second])

        hourly = bridge.fetch_hourly("Seattle", "WA")
        daily = bridge.fetch_daily("Seattle", "WA")

        assert len(hourly) == 2
        assert len(daily) == 1
        assert bridge.session.get.call_args_list[0].args[0] == HOURLY_URL.format(city="Seattle", state="WA")
        assert bridge.session.get.call_args_list[1].args[0] == DAILY_URL.format(city="Seattle", state="WA")


@pytest.mark.unit
class TestPolling:
    @patch("epa_uv.epa_uv._save_state")
    def test_poll_and_send_deduplicates(self, _mock_save_state):
        bridge = EPAUVBridge([("Seattle", "WA")], state_file="state.json")
        bridge.fetch_hourly = Mock(return_value=[parse_hourly_row("Seattle", "WA", HOURLY_ROWS[0])])
        bridge.fetch_daily = Mock(return_value=[parse_daily_row("Seattle", "WA", DAILY_ROWS[0])])
        producer = Mock()
        producer.producer = Mock()

        bridge.poll_and_send(producer, once=True)
        bridge.poll_and_send(producer, once=True)

        assert producer.send_us_epa_uvindex_hourly_forecast.call_count == 1
        assert producer.send_us_epa_uvindex_daily_forecast.call_count == 1
