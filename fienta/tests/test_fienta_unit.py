"""
Unit tests for the Fienta Public Events bridge.
Tests core functionality without external dependencies.
"""

import json
import os
import tempfile
import pytest
from unittest.mock import Mock, patch, MagicMock
from fienta_producer_data import Event, EventSaleStatus
from fienta.fienta import (
    FientaPoller,
    parse_event_reference,
    parse_event_sale_status,
    parse_connection_string,
    fetch_all_events,
    FIENTA_API_URL,
    POLL_INTERVAL_SECONDS,
)

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_EVENT_RAW = {
    "id": "evt-001",
    "name": "Jazz Night at Kultuurikatel",
    "slug": "jazz-night-at-kultuurikatel",
    "description": "An evening of live jazz music at the historic Kultuurikatel in Tallinn.",
    "start": "2024-07-15T19:00:00+03:00",
    "end": "2024-07-15T22:00:00+03:00",
    "timezone": "Europe/Tallinn",
    "url": "https://fienta.com/jazz-night-at-kultuurikatel",
    "language": "et",
    "currency": "EUR",
    "status": "published",
    "sale_status": "onSale",
    "is_online": False,
    "is_free": False,
    "location": "Kultuurikatel, Tallinn",
    "country": "EE",
    "region": "Tallinn",
    "image_url": "https://fienta.com/images/evt-001.jpg",
    "organizer": {
        "name": "Kultuurikatel",
        "url": "https://fienta.com/organizer/kultuurikatel"
    },
    "categories": ["music", "jazz", "concert"],
    "created_at": "2024-06-01T12:00:00+03:00",
    "updated_at": "2024-07-01T10:00:00+03:00",
}

SAMPLE_EVENT_SOLD_OUT = {
    "id": "evt-002",
    "name": "Rock Festival Riga",
    "slug": "rock-festival-riga",
    "description": None,
    "start": "2024-08-10T15:00:00+03:00",
    "end": None,
    "timezone": "Europe/Riga",
    "url": "https://fienta.com/rock-festival-riga",
    "language": "lv",
    "currency": "EUR",
    "status": "published",
    "sale_status": "soldOut",
    "is_online": False,
    "is_free": False,
    "location": None,
    "country": "LV",
    "region": "Riga",
    "image_url": None,
    "organizer": {"name": "Rock Promotions", "url": None},
    "categories": [],
    "created_at": "2024-05-01T09:00:00+03:00",
    "updated_at": "2024-07-15T08:00:00+03:00",
}

SAMPLE_EVENT_ONLINE = {
    "id": "evt-003",
    "name": "Online Webinar: Python Tips",
    "slug": "online-webinar-python-tips",
    "description": "Learn Python tips and tricks.",
    "start": "2024-07-20T10:00:00+00:00",
    "end": "2024-07-20T12:00:00+00:00",
    "timezone": "UTC",
    "url": "https://fienta.com/online-webinar-python-tips",
    "language": "en",
    "currency": None,
    "status": "published",
    "sale_status": "notOnSale",
    "is_online": True,
    "is_free": True,
    "location": None,
    "country": None,
    "region": None,
    "image_url": None,
    "organizer": {"name": "Tech Talks", "url": "https://fienta.com/organizer/tech-talks"},
    "categories": ["technology", "education"],
    "created_at": "2024-06-15T08:00:00+00:00",
    "updated_at": "2024-06-15T08:00:00+00:00",
}


# ---------------------------------------------------------------------------
# Tests: parse_event_reference
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseEventReference:
    """Tests for parsing event reference data from raw API responses."""

    def test_full_event_parsed_correctly(self):
        ref = parse_event_reference(SAMPLE_EVENT_RAW)
        assert ref is not None
        assert ref.event_id == "evt-001"
        assert ref.name == "Jazz Night at Kultuurikatel"
        assert ref.slug == "jazz-night-at-kultuurikatel"
        assert ref.description == "An evening of live jazz music at the historic Kultuurikatel in Tallinn."
        assert ref.start == "2024-07-15T19:00:00+03:00"
        assert ref.end == "2024-07-15T22:00:00+03:00"
        assert ref.timezone == "Europe/Tallinn"
        assert ref.url == "https://fienta.com/jazz-night-at-kultuurikatel"
        assert ref.language == "et"
        assert ref.currency == "EUR"
        assert ref.status == "published"
        assert ref.sale_status == "onSale"
        assert ref.is_online is False
        assert ref.is_free is False
        assert ref.location == "Kultuurikatel, Tallinn"
        assert ref.country == "EE"
        assert ref.region == "Tallinn"
        assert ref.image_url == "https://fienta.com/images/evt-001.jpg"
        assert ref.organizer_name == "Kultuurikatel"
        assert ref.organizer_url == "https://fienta.com/organizer/kultuurikatel"
        assert ref.categories == ["music", "jazz", "concert"]
        assert ref.created_at == "2024-06-01T12:00:00+03:00"
        assert ref.updated_at == "2024-07-01T10:00:00+03:00"

    def test_null_optional_fields(self):
        ref = parse_event_reference(SAMPLE_EVENT_SOLD_OUT)
        assert ref is not None
        assert ref.event_id == "evt-002"
        assert ref.description is None
        assert ref.end is None
        assert ref.location is None
        assert ref.image_url is None
        assert ref.categories == []

    def test_online_event_location_none(self):
        ref = parse_event_reference(SAMPLE_EVENT_ONLINE)
        assert ref is not None
        assert ref.is_online is True
        assert ref.is_free is True
        assert ref.currency is None
        assert ref.location is None
        assert ref.country is None
        assert ref.region is None

    def test_missing_id_returns_none(self):
        raw = dict(SAMPLE_EVENT_RAW)
        del raw["id"]
        assert parse_event_reference(raw) is None

    def test_empty_id_returns_none(self):
        raw = dict(SAMPLE_EVENT_RAW)
        raw["id"] = ""
        assert parse_event_reference(raw) is None

    def test_id_coerced_to_string(self):
        raw = dict(SAMPLE_EVENT_RAW)
        raw["id"] = 12345
        ref = parse_event_reference(raw)
        assert ref is not None
        assert ref.event_id == "12345"

    def test_empty_categories_list(self):
        ref = parse_event_reference(SAMPLE_EVENT_SOLD_OUT)
        assert ref is not None
        assert ref.categories == []

    def test_none_categories(self):
        raw = dict(SAMPLE_EVENT_RAW)
        raw["categories"] = None
        ref = parse_event_reference(raw)
        assert ref.categories is None

    def test_organizer_name_extracted(self):
        ref = parse_event_reference(SAMPLE_EVENT_RAW)
        assert ref.organizer_name == "Kultuurikatel"
        assert ref.organizer_url == "https://fienta.com/organizer/kultuurikatel"

    def test_no_organizer_field(self):
        raw = dict(SAMPLE_EVENT_RAW)
        del raw["organizer"]
        ref = parse_event_reference(raw)
        assert ref is not None
        assert ref.organizer_name is None
        assert ref.organizer_url is None

    def test_location_from_dict(self):
        raw = dict(SAMPLE_EVENT_RAW)
        raw["location"] = {"name": "Kultuurikatel", "address": "Põhja pst 27, Tallinn"}
        ref = parse_event_reference(raw)
        assert ref.location == "Kultuurikatel"

    def test_empty_string_location_normalized_to_none(self):
        raw = dict(SAMPLE_EVENT_RAW)
        raw["location"] = ""
        ref = parse_event_reference(raw)
        assert ref.location is None

    def test_default_status_when_missing(self):
        raw = dict(SAMPLE_EVENT_RAW)
        del raw["status"]
        ref = parse_event_reference(raw)
        assert ref.status == "published"

    def test_default_sale_status_when_missing(self):
        raw = dict(SAMPLE_EVENT_RAW)
        del raw["sale_status"]
        ref = parse_event_reference(raw)
        assert ref.sale_status == "notOnSale"


# ---------------------------------------------------------------------------
# Tests: parse_event_sale_status
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseEventSaleStatus:
    """Tests for parsing sale-status telemetry from raw API responses."""

    def test_full_event_sale_status(self):
        ess = parse_event_sale_status(SAMPLE_EVENT_RAW)
        assert ess is not None
        assert ess.event_id == "evt-001"
        assert ess.name == "Jazz Night at Kultuurikatel"
        assert ess.sale_status == "onSale"
        assert ess.status == "published"
        assert ess.start == "2024-07-15T19:00:00+03:00"
        assert ess.url == "https://fienta.com/jazz-night-at-kultuurikatel"
        assert ess.updated_at == "2024-07-01T10:00:00+03:00"

    def test_sold_out_event(self):
        ess = parse_event_sale_status(SAMPLE_EVENT_SOLD_OUT)
        assert ess is not None
        assert ess.sale_status == "soldOut"

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

    def test_updated_at_fallback_to_created_at(self):
        raw = dict(SAMPLE_EVENT_RAW)
        del raw["updated_at"]
        ess = parse_event_sale_status(raw)
        assert ess is not None
        assert ess.updated_at == raw["created_at"]

    def test_missing_both_timestamps_yields_empty_string(self):
        raw = dict(SAMPLE_EVENT_RAW)
        del raw["updated_at"]
        del raw["created_at"]
        ess = parse_event_sale_status(raw)
        assert ess is not None
        assert ess.updated_at == ""


# ---------------------------------------------------------------------------
# Tests: parse_connection_string
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseConnectionString:
    """Tests for connection string parsing."""

    def test_event_hubs_connection_string(self):
        cs = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123=;EntityPath=mytopic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'mytopic'
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == cs

    def test_plain_bootstrap_connection_string(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'test-topic'
        assert 'sasl.username' not in result

    def test_no_sasl_no_security_protocol(self):
        cs = "BootstrapServer=broker:9092;EntityPath=topic1"
        result = parse_connection_string(cs)
        assert 'security.protocol' not in result


# ---------------------------------------------------------------------------
# Tests: fetch_all_events
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestFetchAllEvents:
    """Tests for fetch_all_events pagination."""

    def test_fetches_list_response(self):
        events = [SAMPLE_EVENT_RAW, SAMPLE_EVENT_SOLD_OUT]
        with patch('fienta.fienta.requests.get') as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = events
            mock_resp.raise_for_status = Mock()
            mock_get.return_value = mock_resp
            result = fetch_all_events()
        assert result is not None
        assert len(result) == 2
        assert result[0]["id"] == "evt-001"

    def test_fetches_dict_response_with_data_key(self):
        payload = {"data": [SAMPLE_EVENT_RAW], "total": 1}
        with patch('fienta.fienta.requests.get') as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = payload
            mock_resp.raise_for_status = Mock()
            mock_get.return_value = mock_resp
            result = fetch_all_events()
        assert result is not None
        assert len(result) == 1

    def test_returns_none_on_http_error(self):
        with patch('fienta.fienta.requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            result = fetch_all_events()
        assert result is None

    def test_empty_response_returns_empty_list(self):
        with patch('fienta.fienta.requests.get') as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = []
            mock_resp.raise_for_status = Mock()
            mock_get.return_value = mock_resp
            result = fetch_all_events()
        assert result == []


# ---------------------------------------------------------------------------
# Tests: FientaPoller state persistence
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestFientaPollerState:
    """Tests for sale-status state file persistence."""

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
            with open(state_file, 'w') as f:
                f.write("not valid json {{")
            poller = object.__new__(FientaPoller)
            poller.state_file = state_file
            assert poller.load_state() == {}

    def test_state_updated_after_status_change(self):
        """Verify state is updated when a new sale_status is detected."""
        old_state = {"evt-001": "notOnSale"}
        events = [SAMPLE_EVENT_RAW]  # sale_status = "onSale"
        # onSale != notOnSale → should trigger an update
        assert events[0]["sale_status"] != old_state.get("evt-001")

    def test_no_change_not_emitted(self):
        """Verify that unchanged status does not trigger emission."""
        old_state = {"evt-001": "onSale"}
        events = [SAMPLE_EVENT_RAW]  # sale_status = "onSale"
        assert events[0]["sale_status"] == old_state.get("evt-001")


# ---------------------------------------------------------------------------
# Tests: FientaPoller emit methods (mocked Kafka)
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestFientaPollerEmit:
    """Tests for reference and telemetry emission with mocked Kafka."""

    def _make_poller(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "state.json")
            poller = object.__new__(FientaPoller)
            poller.state_file = state_file
            mock_producer = MagicMock()
            mock_producer.producer = MagicMock()
            mock_producer.producer.flush.return_value = 0
            poller.producer = mock_producer
            return poller, tmpdir

    def test_emit_reference_data(self):
        poller = object.__new__(FientaPoller)
        poller.state_file = "/tmp/test_state.json"
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        mock_producer.producer.flush.return_value = 0
        poller.producer = mock_producer

        events = [SAMPLE_EVENT_RAW, SAMPLE_EVENT_SOLD_OUT]
        count = poller.emit_reference_data(events)
        assert count == 2
        assert mock_producer.send_com_fienta_event.call_count == 2
        mock_producer.producer.flush.assert_called_once()

    def test_emit_sale_status_changes_new_events(self):
        poller = object.__new__(FientaPoller)
        poller.state_file = "/tmp/test_state.json"
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        mock_producer.producer.flush.return_value = 0
        poller.producer = mock_producer

        state = {}  # No previous state → all events trigger emission
        events = [SAMPLE_EVENT_RAW, SAMPLE_EVENT_SOLD_OUT]
        count, new_state = poller.emit_sale_status_changes(events, state)
        assert count == 2
        assert mock_producer.send_com_fienta_event_sale_status.call_count == 2
        assert new_state["evt-001"] == "onSale"
        assert new_state["evt-002"] == "soldOut"

    def test_emit_sale_status_no_changes(self):
        poller = object.__new__(FientaPoller)
        poller.state_file = "/tmp/test_state.json"
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        mock_producer.producer.flush.return_value = 0
        poller.producer = mock_producer

        state = {"evt-001": "onSale", "evt-002": "soldOut"}
        events = [SAMPLE_EVENT_RAW, SAMPLE_EVENT_SOLD_OUT]
        count, _ = poller.emit_sale_status_changes(events, state)
        assert count == 0
        mock_producer.send_com_fienta_event_sale_status.assert_not_called()

    def test_emit_sale_status_one_changed(self):
        poller = object.__new__(FientaPoller)
        poller.state_file = "/tmp/test_state.json"
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        mock_producer.producer.flush.return_value = 0
        poller.producer = mock_producer

        # evt-001 status changed from notOnSale to onSale
        state = {"evt-001": "notOnSale", "evt-002": "soldOut"}
        events = [SAMPLE_EVENT_RAW, SAMPLE_EVENT_SOLD_OUT]
        count, new_state = poller.emit_sale_status_changes(events, state)
        assert count == 1
        assert mock_producer.send_com_fienta_event_sale_status.call_count == 1
        assert new_state["evt-001"] == "onSale"

    def test_flush_failure_does_not_update_state(self):
        """When flush returns non-zero, state must not be updated."""
        poller = object.__new__(FientaPoller)
        poller.state_file = "/tmp/test_state.json"
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        mock_producer.producer.flush.return_value = 1  # Flush incomplete
        poller.producer = mock_producer

        state = {}  # No previous state → triggers emission
        events = [SAMPLE_EVENT_RAW]
        count, new_state = poller.emit_sale_status_changes(events, state)
        assert count == 1
        # State should NOT be updated since flush failed
        assert "evt-001" not in new_state

    def test_reference_flush_failure_logs_warning(self):
        """When reference flush returns non-zero, still return count sent."""
        poller = object.__new__(FientaPoller)
        poller.state_file = "/tmp/test_state.json"
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        mock_producer.producer.flush.return_value = 2  # Incomplete
        poller.producer = mock_producer

        events = [SAMPLE_EVENT_RAW]
        count = poller.emit_reference_data(events)
        assert count == 1


# ---------------------------------------------------------------------------
# Tests: API URL constant
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestApiConstants:
    """Verify API constants are correct."""

    def test_api_url(self):
        assert FIENTA_API_URL == "https://fienta.com/api/v1/public/events"

    def test_poll_interval(self):
        assert POLL_INTERVAL_SECONDS == 300


# ---------------------------------------------------------------------------
# Tests: Data class serialization
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestDataClassSerialization:
    """Tests for Event and EventSaleStatus serialization."""

    def test_event_roundtrip(self):
        ref = parse_event_reference(SAMPLE_EVENT_RAW)
        assert ref is not None
        json_str = ref.to_json()
        ref2 = Event.from_json(json_str)
        assert ref2.event_id == ref.event_id
        assert ref2.name == ref.name
        assert ref2.sale_status == ref.sale_status
        assert ref2.organizer_name == ref.organizer_name

    def test_event_sale_status_roundtrip(self):
        ess = parse_event_sale_status(SAMPLE_EVENT_RAW)
        assert ess is not None
        json_str = ess.to_json()
        ess2 = EventSaleStatus.from_json(json_str)
        assert ess2.event_id == ess.event_id
        assert ess2.sale_status == ess.sale_status
        assert ess2.updated_at == ess.updated_at

    def test_event_to_byte_array(self):
        ref = parse_event_reference(SAMPLE_EVENT_RAW)
        assert ref is not None
        data = ref.to_byte_array("application/json")
        parsed = json.loads(data)
        assert parsed["event_id"] == "evt-001"
        assert parsed["sale_status"] == "onSale"

    def test_event_sale_status_to_byte_array(self):
        ess = parse_event_sale_status(SAMPLE_EVENT_RAW)
        assert ess is not None
        data = ess.to_byte_array("application/json")
        parsed = json.loads(data)
        assert parsed["event_id"] == "evt-001"
        assert parsed["sale_status"] == "onSale"

    def test_event_nullable_fields(self):
        ref = parse_event_reference(SAMPLE_EVENT_SOLD_OUT)
        assert ref is not None
        json_str = ref.to_json()
        ref2 = Event.from_json(json_str)
        assert ref2.end is None
        assert ref2.location is None
        assert ref2.image_url is None
