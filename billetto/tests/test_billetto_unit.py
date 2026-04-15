"""Unit tests for the Billetto bridge."""

import json
import sys
import pytest
from unittest.mock import MagicMock, patch, call
from datetime import datetime, timezone
import requests

from billetto.billetto import (
    BillettoPoller,
    _parse_event,
    _event_hash,
    _derive_availability,
    _safe_float,
    _safe_int,
    main,
    parse_connection_string,
)
from billetto_producer_data import Event


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_raw_event():
    return {
        "id": 12345,
        "title": "Summer Jazz Festival",
        "description": "<p>A wonderful evening of jazz</p>",
        "startdate": "2026-07-15T19:00:00",
        "enddate": "2026-07-15T23:00:00",
        "url": "https://billetto.dk/e/summer-jazz-festival",
        "image_link": "https://billetto.dk/images/event/12345.jpg",
        "status": "published",
        "location": {
            "city": "Copenhagen",
            "location_name": "The Jazz Club",
            "address": "Nørregade 1",
            "zip_code": "1165",
            "country_code": "DK",
            "latitude": 55.6761,
            "longitude": 12.5683,
        },
        "organiser": {
            "id": 999,
            "name": "Jazz Events DK",
        },
        "minimum_price": {
            "amount_in_cents": 15000,
            "currency": "DKK",
        },
    }


@pytest.fixture
def sample_raw_event_minimal():
    return {
        "id": 7890,
        "title": "Free Community Meetup",
        "startdate": "2026-08-01T18:00:00",
    }


@pytest.fixture
def mock_kafka_config():
    return {"bootstrap.servers": "localhost:9092"}


# ---------------------------------------------------------------------------
# TestParseEvent
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseEvent:
    def test_full_event(self, sample_raw_event):
        event = _parse_event(sample_raw_event)
        assert event is not None
        assert event.event_id == 12345
        assert event.title == "Summer Jazz Festival"
        assert event.description == "<p>A wonderful evening of jazz</p>"
        assert event.startdate == "2026-07-15T19:00:00"
        assert event.enddate == "2026-07-15T23:00:00"
        assert event.url == "https://billetto.dk/e/summer-jazz-festival"
        assert event.image_link == "https://billetto.dk/images/event/12345.jpg"
        assert event.status == "published"
        assert event.location_city == "Copenhagen"
        assert event.location_name == "The Jazz Club"
        assert event.location_address == "Nørregade 1"
        assert event.location_zip_code == "1165"
        assert event.location_country_code == "DK"
        assert event.location_latitude == pytest.approx(55.6761)
        assert event.location_longitude == pytest.approx(12.5683)
        assert event.organiser_id == 999
        assert event.organiser_name == "Jazz Events DK"
        assert event.minimum_price_amount_in_cents == 15000
        assert event.minimum_price_currency == "DKK"

    def test_minimal_event(self, sample_raw_event_minimal):
        event = _parse_event(sample_raw_event_minimal)
        assert event is not None
        assert event.event_id == 7890
        assert event.title == "Free Community Meetup"
        assert event.description is None
        assert event.enddate is None
        assert event.url is None
        assert event.image_link is None
        assert event.location_city is None
        assert event.organiser_id is None
        assert event.minimum_price_amount_in_cents is None

    def test_missing_id_returns_none(self):
        raw = {"title": "No ID Event", "startdate": "2026-06-01T10:00:00"}
        assert _parse_event(raw) is None

    def test_null_location_field(self):
        raw = {
            "id": 111,
            "title": "Online Event",
            "startdate": "2026-06-01T10:00:00",
            "location": None,
        }
        event = _parse_event(raw)
        assert event is not None
        assert event.location_city is None

    def test_null_organiser_field(self):
        raw = {
            "id": 222,
            "title": "Anonymous Event",
            "startdate": "2026-06-01T10:00:00",
            "organiser": None,
        }
        event = _parse_event(raw)
        assert event is not None
        assert event.organiser_id is None
        assert event.organiser_name is None

    def test_event_id_as_string(self):
        raw = {"id": "333", "title": "String ID Event", "startdate": "2026-06-01T10:00:00"}
        event = _parse_event(raw)
        assert event is not None
        assert event.event_id == 333
        assert isinstance(event.event_id, int)


# ---------------------------------------------------------------------------
# TestDeriveAvailability
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestDeriveAvailability:
    def test_sold_out_flag(self):
        assert _derive_availability({"sold_out": True}) == "sold_out"

    def test_availability_dict_with_status(self):
        raw = {"availability": {"status": "available"}}
        assert _derive_availability(raw) == "available"

    def test_availability_string(self):
        raw = {"availability": "sold_out"}
        assert _derive_availability(raw) == "sold_out"

    def test_future_event_available(self):
        raw = {"startdate": "2099-01-01T10:00:00", "enddate": "2099-01-01T12:00:00"}
        assert _derive_availability(raw) == "available"

    def test_past_event_unavailable(self):
        raw = {"startdate": "2020-01-01T10:00:00", "enddate": "2020-01-01T12:00:00"}
        assert _derive_availability(raw) == "unavailable"


# ---------------------------------------------------------------------------
# TestEventHash
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestEventHash:
    def test_same_content_same_hash(self, sample_raw_event):
        h1 = _event_hash(sample_raw_event)
        h2 = _event_hash(sample_raw_event)
        assert h1 == h2

    def test_different_content_different_hash(self, sample_raw_event):
        modified = dict(sample_raw_event)
        modified["title"] = "Different Title"
        assert _event_hash(sample_raw_event) != _event_hash(modified)

    def test_returns_string(self, sample_raw_event):
        assert isinstance(_event_hash(sample_raw_event), str)


# ---------------------------------------------------------------------------
# TestSafeConversions
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestSafeConversions:
    def test_safe_float_none(self):
        assert _safe_float(None) is None

    def test_safe_float_int(self):
        assert _safe_float(42) == pytest.approx(42.0)

    def test_safe_float_string(self):
        assert _safe_float("3.14") == pytest.approx(3.14)

    def test_safe_float_invalid(self):
        assert _safe_float("abc") is None

    def test_safe_int_none(self):
        assert _safe_int(None) is None

    def test_safe_int_string(self):
        assert _safe_int("99") == 99

    def test_safe_int_invalid(self):
        assert _safe_int("not_a_number") is None


# ---------------------------------------------------------------------------
# TestParseConnectionString
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseConnectionString:
    def test_plain_bootstrap(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=my-topic"
        config, topic = parse_connection_string(cs)
        assert config["bootstrap.servers"] == "localhost:9092"
        assert topic == "my-topic"

    def test_plain_bootstrap_no_tls(self):
        import os
        os.environ["KAFKA_ENABLE_TLS"] = "false"
        cs = "BootstrapServer=localhost:9092;EntityPath=my-topic"
        config, topic = parse_connection_string(cs)
        assert "security.protocol" not in config
        del os.environ["KAFKA_ENABLE_TLS"]

    def test_event_hubs_format(self):
        cs = (
            "Endpoint=sb://myhub.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123=;"
            "EntityPath=my-topic"
        )
        config, topic = parse_connection_string(cs)
        assert "myhub.servicebus.windows.net" in config["bootstrap.servers"]
        assert topic == "my-topic"
        assert config["sasl.username"] == "$ConnectionString"


@pytest.mark.unit
class TestMainConfiguration:
    def test_connection_string_topic_overrides_env_default(self, monkeypatch):
        monkeypatch.setenv("BILLETTO_API_KEYPAIR", "key:secret")
        monkeypatch.setenv("CONNECTION_STRING", "BootstrapServer=localhost:9092;EntityPath=topic-from-cs")
        monkeypatch.setenv("KAFKA_TOPIC", "topic-from-env")
        monkeypatch.setattr(sys, "argv", ["billetto", "feed"])

        with patch("billetto.billetto.BillettoPoller") as poller_cls:
            poller = poller_cls.return_value
            poller.feed.return_value = None

            main()

        assert poller_cls.call_args is not None
        assert poller_cls.call_args.kwargs["kafka_topic"] == "topic-from-cs"


# ---------------------------------------------------------------------------
# TestBillettoPollerFetch
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestBillettoPollerFetch:
    def test_fetch_page_success(self, sample_raw_event):
        poller = BillettoPoller(api_keypair="key:secret")
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [sample_raw_event],
            "has_more": False,
            "next_url": None,
        }
        mock_response.raise_for_status.return_value = None

        with patch.object(poller._get_session(), "get", return_value=mock_response):
            events, next_url, has_more = poller.fetch_events_page()

        assert len(events) == 1
        assert events[0]["id"] == 12345
        assert not has_more
        assert next_url is None

    def test_fetch_page_http_error_returns_empty(self):
        import requests as req
        poller = BillettoPoller(api_keypair="key:secret")
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = req.exceptions.HTTPError("HTTP 500")

        with patch.object(poller._get_session(), "get", return_value=mock_response):
            events, next_url, has_more = poller.fetch_events_page()

        assert events == []
        assert not has_more

    def test_fetch_page_network_error_returns_empty(self):
        poller = BillettoPoller(api_keypair="key:secret")
        with patch.object(poller._get_session(), "get", side_effect=requests.exceptions.ConnectionError("refused")):
            events, next_url, has_more = poller.fetch_events_page()

        assert events == []
        assert not has_more


class _FakeClock:
    def __init__(self):
        self.now = 0.0
        self.slept = []

    def monotonic(self):
        return self.now

    def sleep(self, seconds: float):
        self.slept.append(seconds)
        self.now += seconds


@pytest.mark.unit
class TestBillettoPollerRateLimit:
    def test_429_enforces_minimum_global_cooldown(self):
        clock = _FakeClock()
        poller = BillettoPoller(
            api_keypair="key:secret",
            sleep_func=clock.sleep,
            monotonic_func=clock.monotonic,
        )
        throttled = MagicMock()
        throttled.status_code = 429
        throttled.headers = {"X-Ratelimit-Retry-After": "45000"}

        with patch.object(poller._get_session(), "get", return_value=throttled):
            events, next_url, has_more = poller.fetch_events_page()

        assert events == []
        assert next_url is None
        assert has_more is False
        assert poller._rate_limit_cooldown_until == pytest.approx(60.0)

        with patch.object(
            poller._get_session(),
            "get",
            side_effect=requests.exceptions.ConnectionError("stop after cooldown"),
        ):
            events, next_url, has_more = poller.fetch_events_page()

        assert clock.slept == [60.0]
        assert events == []
        assert next_url is None
        assert has_more is False

    def test_zero_remaining_waits_for_retry_after_before_next_page(self, sample_raw_event):
        clock = _FakeClock()
        poller = BillettoPoller(
            api_keypair="key:secret",
            sleep_func=clock.sleep,
            monotonic_func=clock.monotonic,
        )
        first_page = MagicMock()
        first_page.status_code = 200
        first_page.headers = {
            "X-Ratelimit-Remaining": "0",
            "X-Ratelimit-Retry-After": "61000",
        }
        first_page.raise_for_status.return_value = None
        first_page.json.return_value = {
            "data": [sample_raw_event],
            "has_more": True,
            "next_url": "https://billetto.dk/api/v3/public/events?page=2",
        }

        second_page = MagicMock()
        second_page.status_code = 200
        second_page.headers = {"X-Ratelimit-Remaining": "10"}
        second_page.raise_for_status.return_value = None
        second_page.json.return_value = {
            "data": [],
            "has_more": False,
            "next_url": None,
        }

        with patch.object(poller._get_session(), "get", side_effect=[first_page, second_page]):
            events = poller.fetch_all_events()

        assert len(events) == 1
        assert events[0]["id"] == 12345
        assert clock.slept == [61.0]


# ---------------------------------------------------------------------------
# TestBillettoPollerPollOnce
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestBillettoPollerPollOnce:
    def _make_poller(self, mock_producer):
        poller = BillettoPoller(api_keypair="key:secret", kafka_topic="test-topic")
        mock_event_producer = MagicMock()
        mock_event_producer.producer = mock_producer
        poller.event_producer = mock_event_producer
        return poller

    def test_new_event_sent(self, sample_raw_event):
        mock_producer = MagicMock()
        mock_producer.flush.return_value = 0
        poller = self._make_poller(mock_producer)

        with patch.object(poller, "fetch_all_events", return_value=[sample_raw_event]):
            sent, new_state = poller.poll_once({})

        assert sent == 1
        assert "12345" in new_state
        poller.event_producer.send_billetto_events_event.assert_called_once()

    def test_unchanged_event_not_resent(self, sample_raw_event):
        mock_producer = MagicMock()
        mock_producer.flush.return_value = 0
        poller = self._make_poller(mock_producer)
        existing_state = {"12345": _event_hash(sample_raw_event)}

        with patch.object(poller, "fetch_all_events", return_value=[sample_raw_event]):
            sent, new_state = poller.poll_once(existing_state)

        assert sent == 0
        poller.event_producer.send_billetto_events_event.assert_not_called()

    def test_changed_event_resent(self, sample_raw_event):
        mock_producer = MagicMock()
        mock_producer.flush.return_value = 0
        poller = self._make_poller(mock_producer)
        old_state = {"12345": "old_hash_value"}

        with patch.object(poller, "fetch_all_events", return_value=[sample_raw_event]):
            sent, new_state = poller.poll_once(old_state)

        assert sent == 1
        assert new_state["12345"] == _event_hash(sample_raw_event)

    def test_flush_failure_does_not_advance_state(self, sample_raw_event):
        """State must NOT be committed when Kafka flush returns non-zero remainder."""
        mock_producer = MagicMock()
        mock_producer.flush.return_value = 1  # non-zero = failure
        poller = self._make_poller(mock_producer)
        initial_state = {}

        with patch.object(poller, "fetch_all_events", return_value=[sample_raw_event]):
            sent, returned_state = poller.poll_once(initial_state)

        assert sent == 0
        assert returned_state is initial_state or returned_state == initial_state
        assert "12345" not in returned_state

    def test_empty_response_returns_unchanged_state(self):
        mock_producer = MagicMock()
        poller = self._make_poller(mock_producer)
        initial_state = {"12345": "some_hash"}

        with patch.object(poller, "fetch_all_events", return_value=[]):
            sent, returned_state = poller.poll_once(initial_state)

        assert sent == 0
        assert returned_state == initial_state

    def test_event_without_id_skipped(self):
        mock_producer = MagicMock()
        mock_producer.flush.return_value = 0
        poller = self._make_poller(mock_producer)
        bad_event = {"title": "No ID", "startdate": "2026-06-01T10:00:00"}

        with patch.object(poller, "fetch_all_events", return_value=[bad_event]):
            sent, _ = poller.poll_once({})

        assert sent == 0
        poller.event_producer.send_billetto_events_event.assert_not_called()

    def test_send_uses_string_event_id_as_key(self, sample_raw_event):
        """The _event_id passed to send_* must be a string matching the event ID."""
        mock_producer = MagicMock()
        mock_producer.flush.return_value = 0
        poller = self._make_poller(mock_producer)

        with patch.object(poller, "fetch_all_events", return_value=[sample_raw_event]):
            poller.poll_once({})

        call_kwargs = poller.event_producer.send_billetto_events_event.call_args
        assert call_kwargs is not None
        assert call_kwargs.kwargs.get("_event_id") == "12345" or call_kwargs.args[0] == "12345"


# ---------------------------------------------------------------------------
# TestBillettoPollerState
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestBillettoPollerState:
    def test_load_state_missing_file(self, tmp_path):
        poller = BillettoPoller(api_keypair="k:s", state_file=str(tmp_path / "state.json"))
        state = poller.load_state()
        assert state == {}

    def test_save_and_load_state(self, tmp_path):
        state_file = str(tmp_path / "state.json")
        poller = BillettoPoller(api_keypair="k:s", state_file=state_file)
        poller.save_state({"12345": "abc", "67890": "def"})
        loaded = poller.load_state()
        assert loaded == {"12345": "abc", "67890": "def"}
        assert not (tmp_path / "state.json.tmp").exists()

    def test_save_state_no_file_is_noop(self):
        poller = BillettoPoller(api_keypair="k:s", state_file="")
        poller.save_state({"12345": "abc"})  # Should not raise

    def test_save_state_creates_parent_directory(self, tmp_path):
        state_file = tmp_path / "state" / "state.json"
        poller = BillettoPoller(api_keypair="k:s", state_file=str(state_file))
        poller.save_state({"12345": "abc"})
        assert state_file.exists()
        assert poller.load_state() == {"12345": "abc"}

    def test_load_state_invalid_json(self, tmp_path):
        state_file = tmp_path / "state.json"
        state_file.write_text("not-valid-json")
        poller = BillettoPoller(api_keypair="k:s", state_file=str(state_file))
        state = poller.load_state()
        assert state == {}
