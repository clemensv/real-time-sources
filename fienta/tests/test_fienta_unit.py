"""
Unit tests for the Fienta Public Events bridge.
"""

import json
import os
import tempfile
import argparse
from unittest.mock import MagicMock, Mock, patch

import pytest

from fienta_producer_data import Event, EventSaleStatus
from fienta.fienta import (
    FIENTA_API_URL,
    POLL_INTERVAL_SECONDS,
    FientaPoller,
    _resolve_api_filters,
    fetch_all_events,
    parse_connection_string,
    parse_event_reference,
    parse_event_sale_status,
)


SAMPLE_EVENT_RAW = {
    "id": "evt-001",
    "title": "Jazz Night at Kultuurikatel",
    "starts_at": "2024-07-15 19:00:00",
    "ends_at": "2024-07-15 22:00:00",
    "duration_string": "Mon 15. July 2024 at 19:00 - Mon 15. July 2024 at 22:00",
    "notes_about_time": "Doors open at 18:30",
    "event_status": "scheduled",
    "sale_status": "onSale",
    "attendance_mode": "offline",
    "venue": "Kultuurikatel",
    "venue_id": "venue-001",
    "address": "Põhja pst 27, Tallinn",
    "address_postal_code": "10415",
    "description": "An evening of live jazz music at the historic Kultuurikatel in Tallinn.",
    "url": "https://fienta.com/jazz-night-at-kultuurikatel",
    "buy_tickets_url": "https://fienta.com/jazz-night-at-kultuurikatel",
    "image_url": "https://fienta.com/images/evt-001.jpg",
    "image_small_url": "https://fienta.com/images/evt-001-small.jpg",
    "series_id": "jazz-night-at-kultuurikatel",
    "organizer_name": "Kultuurikatel",
    "organizer_phone": "+3726700070",
    "organizer_email": "hello@kultuurikatel.ee",
    "organizer_id": 77,
    "categories": ["music", "jazz", "concert"],
}

SAMPLE_EVENT_SOLD_OUT = {
    "id": "evt-002",
    "title": "Rock Festival Riga",
    "starts_at": "2024-08-10 15:00:00",
    "ends_at": "",
    "duration_string": "",
    "notes_about_time": "",
    "event_status": "scheduled",
    "sale_status": "soldOut",
    "attendance_mode": "offline",
    "venue": "",
    "venue_id": "",
    "address": "",
    "address_postal_code": "",
    "description": None,
    "url": "https://fienta.com/rock-festival-riga",
    "buy_tickets_url": "https://fienta.com/rock-festival-riga",
    "image_url": None,
    "image_small_url": None,
    "series_id": "",
    "organizer_name": "Rock Promotions",
    "organizer_phone": None,
    "organizer_email": None,
    "organizer_id": "",
    "categories": [],
}

SAMPLE_EVENT_ONLINE = {
    "id": 303,
    "title": "Online Webinar: Python Tips",
    "starts_at": "2024-07-20 10:00:00",
    "ends_at": "2024-07-20 12:00:00",
    "duration_string": "Sat 20. July 2024 at 10:00 - Sat 20. July 2024 at 12:00",
    "notes_about_time": None,
    "event_status": "scheduled",
    "sale_status": "notOnSale",
    "attendance_mode": "online",
    "venue": "Virtual event",
    "venue_id": None,
    "address": "",
    "address_postal_code": "",
    "description": "Learn Python tips and tricks.",
    "url": "https://fienta.com/online-webinar-python-tips",
    "buy_tickets_url": "https://fienta.com/online-webinar-python-tips",
    "image_url": None,
    "image_small_url": None,
    "series_id": None,
    "organizer_name": "Tech Talks",
    "organizer_phone": None,
    "organizer_email": "events@techtalks.example",
    "organizer_id": 15,
    "categories": ["technology", "education"],
}


@pytest.mark.unit
class TestParseEventReference:

    def test_full_event_parsed_correctly(self):
        ref = parse_event_reference(SAMPLE_EVENT_RAW)
        assert ref is not None
        assert ref.event_id == "evt-001"
        assert ref.name == "Jazz Night at Kultuurikatel"
        assert ref.start == "2024-07-15 19:00:00"
        assert ref.end == "2024-07-15 22:00:00"
        assert ref.duration_text == "Mon 15. July 2024 at 19:00 - Mon 15. July 2024 at 22:00"
        assert ref.time_notes == "Doors open at 18:30"
        assert ref.event_status == "scheduled"
        assert ref.sale_status == "onSale"
        assert ref.attendance_mode == "offline"
        assert ref.venue_name == "Kultuurikatel"
        assert ref.venue_id == "venue-001"
        assert ref.address == "Põhja pst 27, Tallinn"
        assert ref.postal_code == "10415"
        assert ref.url == "https://fienta.com/jazz-night-at-kultuurikatel"
        assert ref.buy_tickets_url == "https://fienta.com/jazz-night-at-kultuurikatel"
        assert ref.image_url == "https://fienta.com/images/evt-001.jpg"
        assert ref.image_small_url == "https://fienta.com/images/evt-001-small.jpg"
        assert ref.series_id == "jazz-night-at-kultuurikatel"
        assert ref.organizer_name == "Kultuurikatel"
        assert ref.organizer_phone == "+3726700070"
        assert ref.organizer_email == "hello@kultuurikatel.ee"
        assert ref.organizer_id == 77
        assert ref.categories == ["music", "jazz", "concert"]

    def test_optional_fields_normalized(self):
        ref = parse_event_reference(SAMPLE_EVENT_SOLD_OUT)
        assert ref is not None
        assert ref.end is None
        assert ref.duration_text is None
        assert ref.time_notes is None
        assert ref.venue_name is None
        assert ref.venue_id is None
        assert ref.address is None
        assert ref.postal_code is None
        assert ref.image_url is None
        assert ref.image_small_url is None
        assert ref.series_id is None
        assert ref.organizer_id is None
        assert ref.categories == []

    def test_id_coerced_to_string(self):
        ref = parse_event_reference(SAMPLE_EVENT_ONLINE)
        assert ref is not None
        assert ref.event_id == "303"

    def test_missing_id_returns_none(self):
        raw = dict(SAMPLE_EVENT_RAW)
        del raw["id"]
        assert parse_event_reference(raw) is None

    def test_none_categories_stay_none(self):
        raw = dict(SAMPLE_EVENT_RAW)
        raw["categories"] = None
        ref = parse_event_reference(raw)
        assert ref is not None
        assert ref.categories == []

    def test_name_falls_back_to_legacy_field(self):
        raw = {"id": "evt-004", "name": "Legacy Name", "start": "2024-01-01 10:00:00", "sale_status": "onSale", "status": "scheduled", "url": "https://example.test"}
        ref = parse_event_reference(raw)
        assert ref is not None
        assert ref.name == "Legacy Name"
        assert ref.start == "2024-01-01 10:00:00"
        assert ref.event_status == "scheduled"


@pytest.mark.unit
class TestParseEventSaleStatus:

    def test_full_event_sale_status(self):
        ess = parse_event_sale_status(SAMPLE_EVENT_RAW, observed_at="2026-04-14T06:00:00Z")
        assert ess is not None
        assert ess.event_id == "evt-001"
        assert ess.name == "Jazz Night at Kultuurikatel"
        assert ess.sale_status == "onSale"
        assert ess.event_status == "scheduled"
        assert ess.start == "2024-07-15 19:00:00"
        assert ess.end == "2024-07-15 22:00:00"
        assert ess.url == "https://fienta.com/jazz-night-at-kultuurikatel"
        assert ess.buy_tickets_url == "https://fienta.com/jazz-night-at-kultuurikatel"
        assert ess.observed_at == "2026-04-14T06:00:00Z"

    def test_observed_at_generated_when_missing(self):
        with patch("fienta.fienta._observed_at_utc", return_value="2026-04-14T06:05:00Z"):
            ess = parse_event_sale_status(SAMPLE_EVENT_RAW)
        assert ess is not None
        assert ess.observed_at == "2026-04-14T06:05:00Z"

    def test_missing_id_returns_none(self):
        raw = dict(SAMPLE_EVENT_RAW)
        del raw["id"]
        assert parse_event_sale_status(raw) is None

    def test_missing_sale_status_returns_none(self):
        raw = dict(SAMPLE_EVENT_RAW)
        del raw["sale_status"]
        assert parse_event_sale_status(raw) is None

    def test_empty_sale_status_returns_none(self):
        raw = dict(SAMPLE_EVENT_RAW)
        raw["sale_status"] = ""
        assert parse_event_sale_status(raw) is None


@pytest.mark.unit
class TestParseConnectionString:

    def test_event_hubs_connection_string(self):
        cs = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123=;EntityPath=mytopic"
        result = parse_connection_string(cs)
        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "mytopic"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["sasl.password"] == cs

    def test_plain_bootstrap_connection_string(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = parse_connection_string(cs)
        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["kafka_topic"] == "test-topic"
        assert "sasl.username" not in result

    def test_no_sasl_no_security_protocol(self):
        cs = "BootstrapServer=broker:9092;EntityPath=topic1"
        result = parse_connection_string(cs)
        assert "security.protocol" not in result


@pytest.mark.unit
class TestFilterConfiguration:

    def test_resolve_api_filters_prefers_cli_then_env(self, monkeypatch):
        monkeypatch.setenv("FIENTA_COUNTRY", "DE")
        monkeypatch.setenv("FIENTA_LOCALE", "en")
        args = argparse.Namespace(country="EE", locale=None)

        filters = _resolve_api_filters(args)

        assert filters == {
            "country": "EE",
            "locale": "en",
        }

    def test_resolve_api_filters_omits_empty_values(self, monkeypatch):
        monkeypatch.delenv("FIENTA_COUNTRY", raising=False)
        monkeypatch.delenv("FIENTA_LOCALE", raising=False)
        args = argparse.Namespace(country=None, locale=" ")

        filters = _resolve_api_filters(args)

        assert filters == {}


@pytest.mark.unit
class TestFetchAllEvents:

    def test_fetches_list_response(self):
        events = [SAMPLE_EVENT_RAW, SAMPLE_EVENT_SOLD_OUT]
        with patch("fienta.fienta.requests.get") as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = events
            mock_resp.raise_for_status = Mock()
            mock_get.return_value = mock_resp
            result = fetch_all_events()
        assert result is not None
        assert len(result) == 2
        assert result[0]["id"] == "evt-001"

    def test_fetches_paginated_events_response(self):
        page_one = {
            "events": [SAMPLE_EVENT_RAW],
            "pagination": {
                "page": 1,
                "last_page": 2,
                "next_page_url": "https://fienta.com/api/v1/public/events?page=2&",
            },
        }
        page_two = {
            "events": [SAMPLE_EVENT_SOLD_OUT],
            "pagination": {
                "page": 2,
                "last_page": 2,
                "next_page_url": None,
            },
        }
        with patch("fienta.fienta.requests.get") as mock_get:
            mock_resp_one = Mock()
            mock_resp_one.json.return_value = page_one
            mock_resp_one.raise_for_status = Mock()
            mock_resp_two = Mock()
            mock_resp_two.json.return_value = page_two
            mock_resp_two.raise_for_status = Mock()
            mock_get.side_effect = [mock_resp_one, mock_resp_two]

            result = fetch_all_events()

        assert result is not None
        assert len(result) == 2
        assert mock_get.call_count == 2

    def test_fetches_dict_response_with_data_key(self):
        payload = {"data": [SAMPLE_EVENT_RAW], "total": 1}
        with patch("fienta.fienta.requests.get") as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = payload
            mock_resp.raise_for_status = Mock()
            mock_get.return_value = mock_resp
            result = fetch_all_events()
        assert result is not None
        assert len(result) == 1

    def test_returns_partial_results_if_later_page_fails(self):
        page_one = {
            "events": [SAMPLE_EVENT_RAW],
            "pagination": {
                "page": 1,
                "last_page": 2,
                "next_page_url": "https://fienta.com/api/v1/public/events?page=2&",
            },
        }
        with patch("fienta.fienta.requests.get") as mock_get:
            mock_resp_one = Mock()
            mock_resp_one.json.return_value = page_one
            mock_resp_one.raise_for_status = Mock()
            mock_get.side_effect = [mock_resp_one, Exception("Network error")]
            result = fetch_all_events()
        assert result == [SAMPLE_EVENT_RAW]

    def test_returns_none_on_first_page_error(self):
        with patch("fienta.fienta.requests.get") as mock_get:
            mock_get.side_effect = Exception("Network error")
            result = fetch_all_events()
        assert result is None

    def test_empty_response_returns_empty_list(self):
        with patch("fienta.fienta.requests.get") as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = {"events": [], "pagination": {"page": 1, "last_page": 1, "next_page_url": None}}
            mock_resp.raise_for_status = Mock()
            mock_get.return_value = mock_resp
            result = fetch_all_events()
        assert result == []

    def test_passes_api_filters_to_requests(self):
        with patch("fienta.fienta.requests.get") as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = {"events": [], "pagination": {"page": 1, "last_page": 1, "next_page_url": None}}
            mock_resp.raise_for_status = Mock()
            mock_get.return_value = mock_resp
            fetch_all_events(api_filters={"country": "EE", "locale": "en"})

        mock_get.assert_called_once_with(
            FIENTA_API_URL,
            params={"page": 1, "country": "EE", "locale": "en"},
            timeout=60,
        )


@pytest.mark.unit
class TestFientaPollerState:

    def test_save_and_load_state(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "state.json")
            poller = object.__new__(FientaPoller)
            poller.state_file = state_file
            state = {"evt-001": "onSale", "evt-002": "soldOut"}
            poller.save_state(state)
            loaded = poller.load_state()
            assert loaded == state

    def test_load_state_missing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "nonexistent.json")
            poller = object.__new__(FientaPoller)
            poller.state_file = state_file
            assert poller.load_state() == {}

    def test_load_state_corrupted_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "bad.json")
            with open(state_file, "w", encoding="utf-8") as handle:
                handle.write("not valid json {{")
            poller = object.__new__(FientaPoller)
            poller.state_file = state_file
            assert poller.load_state() == {}


@pytest.mark.unit
class TestFientaPollerEmit:

    def _make_poller(self):
        poller = object.__new__(FientaPoller)
        poller.state_file = "state.json"
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        mock_producer.producer.flush.return_value = 0
        poller.producer = mock_producer
        return poller

    def test_emit_reference_data(self):
        poller = self._make_poller()
        count = poller.emit_reference_data([SAMPLE_EVENT_RAW, SAMPLE_EVENT_SOLD_OUT])
        assert count == 2
        assert poller.producer.send_com_fienta_event.call_count == 2
        first_call = poller.producer.send_com_fienta_event.call_args_list[0]
        assert first_call.args[0] == "evt-001"
        assert first_call.args[1].name == "Jazz Night at Kultuurikatel"
        poller.producer.producer.flush.assert_called_once()

    def test_emit_sale_status_changes_new_events(self):
        poller = self._make_poller()
        with patch("fienta.fienta._observed_at_utc", return_value="2026-04-14T06:10:00Z"):
            count, new_state = poller.emit_sale_status_changes([SAMPLE_EVENT_RAW, SAMPLE_EVENT_SOLD_OUT], {})
        assert count == 2
        assert poller.producer.send_com_fienta_event_sale_status.call_count == 2
        first_call = poller.producer.send_com_fienta_event_sale_status.call_args_list[0]
        assert first_call.args[1].observed_at == "2026-04-14T06:10:00Z"
        assert new_state["evt-001"] == "onSale"
        assert new_state["evt-002"] == "soldOut"

    def test_emit_sale_status_no_changes(self):
        poller = self._make_poller()
        state = {"evt-001": "onSale", "evt-002": "soldOut"}
        count, _ = poller.emit_sale_status_changes([SAMPLE_EVENT_RAW, SAMPLE_EVENT_SOLD_OUT], state)
        assert count == 0
        poller.producer.send_com_fienta_event_sale_status.assert_not_called()

    def test_emit_sale_status_one_changed(self):
        poller = self._make_poller()
        state = {"evt-001": "notOnSale", "evt-002": "soldOut"}
        with patch("fienta.fienta._observed_at_utc", return_value="2026-04-14T06:15:00Z"):
            count, new_state = poller.emit_sale_status_changes([SAMPLE_EVENT_RAW, SAMPLE_EVENT_SOLD_OUT], state)
        assert count == 1
        assert poller.producer.send_com_fienta_event_sale_status.call_count == 1
        assert new_state["evt-001"] == "onSale"
        assert new_state["evt-002"] == "soldOut"

    def test_flush_failure_does_not_update_state(self):
        poller = self._make_poller()
        poller.producer.producer.flush.return_value = 1
        count, new_state = poller.emit_sale_status_changes([SAMPLE_EVENT_RAW], {})
        assert count == 1
        assert new_state == {}

    def test_reference_flush_failure_logs_warning(self):
        poller = self._make_poller()
        poller.producer.producer.flush.return_value = 2
        count = poller.emit_reference_data([SAMPLE_EVENT_RAW])
        assert count == 1


@pytest.mark.unit
class TestApiConstants:

    def test_api_url(self):
        assert FIENTA_API_URL == "https://fienta.com/api/v1/public/events"

    def test_poll_interval(self):
        assert POLL_INTERVAL_SECONDS == 300


@pytest.mark.unit
class TestDataClassSerialization:

    def test_event_roundtrip(self):
        ref = parse_event_reference(SAMPLE_EVENT_RAW)
        assert ref is not None
        ref2 = Event.from_json(ref.to_json())
        assert ref2.event_id == ref.event_id
        assert ref2.name == ref.name
        assert ref2.sale_status == ref.sale_status
        assert ref2.organizer_name == ref.organizer_name
        assert ref2.buy_tickets_url == ref.buy_tickets_url

    def test_event_sale_status_roundtrip(self):
        ess = parse_event_sale_status(SAMPLE_EVENT_RAW, observed_at="2026-04-14T06:00:00Z")
        assert ess is not None
        ess2 = EventSaleStatus.from_json(ess.to_json())
        assert ess2.event_id == ess.event_id
        assert ess2.sale_status == ess.sale_status
        assert ess2.observed_at == ess.observed_at

    def test_event_to_byte_array(self):
        ref = parse_event_reference(SAMPLE_EVENT_RAW)
        assert ref is not None
        parsed = json.loads(ref.to_byte_array("application/json"))
        assert parsed["event_id"] == "evt-001"
        assert parsed["sale_status"] == "onSale"
        assert parsed["organizer_id"] == 77

    def test_event_sale_status_to_byte_array(self):
        ess = parse_event_sale_status(SAMPLE_EVENT_RAW, observed_at="2026-04-14T06:00:00Z")
        assert ess is not None
        parsed = json.loads(ess.to_byte_array("application/json"))
        assert parsed["event_id"] == "evt-001"
        assert parsed["sale_status"] == "onSale"
        assert parsed["observed_at"] == "2026-04-14T06:00:00Z"

    def test_event_nullable_fields(self):
        ref = parse_event_reference(SAMPLE_EVENT_SOLD_OUT)
        assert ref is not None
        ref2 = Event.from_json(ref.to_json())
        assert ref2.end is None
        assert ref2.venue_name is None
        assert ref2.image_url is None
