"""Unit tests for the EPA UV bridge."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from unittest.mock import Mock, patch

import pytest
import requests

from epa_uv import epa_uv as bridge_module

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

    @pytest.mark.parametrize(
        "family,statuses",
        [
            pytest.param("hourly", [404, 200], id="transient-hourly-404"),
            pytest.param("daily", [502, 200], id="transient-daily-502"),
            pytest.param("hourly", [404, 404, 404, 404], id="exhausted-hourly-404"),
            pytest.param("daily", [400], id="non-retryable-daily-400"),
            pytest.param("daily", [413], id="non-retryable-retry-after"),
            pytest.param("daily", [429, 200], id="bounded-retry-after"),
            pytest.param("hourly", [503, 503, 503, 503], id="exhausted-hourly-503"),
            pytest.param("hourly", [None, 200], id="connection-reset"),
            pytest.param("daily", [None, None, None, None], id="exhausted-connection-resets"),
        ],
    )
    def test_retries_transient_responses_but_surfaces_terminal_errors(self, monkeypatch, family, statuses):
        calls = []
        delays = []
        rows = HOURLY_ROWS if family == "hourly" else DAILY_ROWS
        monkeypatch.setattr("urllib3.util.retry.time.sleep", delays.append)

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                status = statuses[min(len(calls), len(statuses) - 1)]
                calls.append(self.path)
                if status is None:
                    self.close_connection = True
                    return
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                if status in (413, 429):
                    self.send_header("Retry-After", "3600")
                self.end_headers()
                self.wfile.write(json.dumps(rows if status == 200 else {"error": "fixture"}).encode("utf-8"))

            def log_message(self, *args):
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        bridge = None
        try:
            monkeypatch.setattr(bridge_module, f"{family.upper()}_URL", f"http://127.0.0.1:{server.server_port}/forecast")
            bridge = EPAUVBridge([("Seattle", "WA")])
            fetch = bridge.fetch_hourly if family == "hourly" else bridge.fetch_daily
            if statuses[-1] == 200:
                assert len(fetch("Seattle", "WA")) == len(rows)
            elif statuses[-1] is None:
                with pytest.raises(requests.ConnectionError):
                    fetch("Seattle", "WA")
            else:
                with pytest.raises(requests.HTTPError, match=str(statuses[-1])):
                    fetch("Seattle", "WA")
            assert len(calls) == len(statuses)
            assert all(0 < delay <= 5 for delay in delays)
            if 429 in statuses:
                assert delays == [5]
        finally:
            if bridge is not None:
                bridge.session.close()
            server.shutdown()
            thread.join(timeout=5)
            server.server_close()


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
