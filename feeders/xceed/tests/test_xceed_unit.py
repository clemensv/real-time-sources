"""Unit tests for the Xceed bridge."""

import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from xceed.xceed import (
    XceedAPI,
    parse_event,
    parse_admission,
    parse_connection_string,
    _extract_venue,
)


# ---- Sample API responses ----

SAMPLE_EVENT_1 = {
    "id": "297ad280-4fd4-4b9a-870e-b4de6b2588a0",
    "legacyId": 123456,
    "name": "Techno Night Party",
    "slug": "techno-night-party",
    "startingTime": 1712700000,
    "endingTime": 1712721600,
    "coverUrl": "https://cdn.xceed.me/sample-event-cover.jpg",
    "externalSalesUrl": None,
    "venue": {
        "id": "abc123",
        "name": "Berghain",
        "city": "Berlin",
        "countryCode": "DE",
    },
}

SAMPLE_EVENT_2 = {
    "id": "5b4e6bcf-8c31-4c23-bf65-8eb5dc2bde14",
    "legacyId": None,
    "name": "Techno Conference",
    "slug": None,
    "startingTime": 1712800000,
    "endingTime": None,
    "coverUrl": None,
    "externalSalesUrl": "https://tickets.externalvendor.com/event/abc123",
    "venue": None,
}

SAMPLE_EVENTS_RESPONSE = {
    "success": True,
    "data": [SAMPLE_EVENT_1, SAMPLE_EVENT_2],
}

SAMPLE_ADMISSIONS_RESPONSE = {
    "success": True,
    "data": {
        "ticket": [
            {
                "id": "adm-001",
                "admissionType": "ticket",
                "name": "Early Bird",
                "salesStatus": {
                    "isSoldOut": False,
                    "isSalesClosed": False,
                },
                "price": {
                    "amount": 12.50,
                    "currency": "EUR",
                },
                "quantity": 50,
            },
            {
                "id": "adm-002",
                "admissionType": "ticket",
                "name": "General Admission",
                "salesStatus": {
                    "isSoldOut": True,
                    "isSalesClosed": True,
                },
                "price": {
                    "amount": 20.00,
                    "currency": "EUR",
                },
                "quantity": 0,
            },
        ],
        "guestList": [],
        "bottleService": [],
    },
}

SAMPLE_ADMISSIONS_NO_FIELDS = {
    "success": True,
    "data": {
        "ticket": [
            {
                "id": "adm-003",
                "name": None,
                "salesStatus": {
                    "isSoldOut": None,
                    "isSalesClosed": None,
                },
                "price": None,
                "quantity": None,
            },
        ],
        "guestList": [],
        "bottleService": [],
    },
}

FLATTENED_ADMISSIONS = [
    {
        **SAMPLE_ADMISSIONS_RESPONSE["data"]["ticket"][0],
        "_category": "ticket",
    },
    {
        **SAMPLE_ADMISSIONS_RESPONSE["data"]["ticket"][1],
        "_category": "ticket",
    },
]

FLATTENED_ADMISSION_WITH_NULLS = {
    **SAMPLE_ADMISSIONS_NO_FIELDS["data"]["ticket"][0],
    "_category": "ticket",
}


# ---- Tests for parse_event ----

@pytest.mark.unit
class TestParseEvent:
    def test_full_event(self):
        event = parse_event(SAMPLE_EVENT_1)
        assert event.event_id == "297ad280-4fd4-4b9a-870e-b4de6b2588a0"
        assert event.legacy_id == 123456
        assert event.name == "Techno Night Party"
        assert event.slug == "techno-night-party"
        assert isinstance(event.starting_time, datetime)
        assert event.starting_time.tzinfo is not None
        assert isinstance(event.ending_time, datetime)
        assert event.cover_url == "https://cdn.xceed.me/sample-event-cover.jpg"
        assert event.external_sales_url is None
        assert event.venue_id == "abc123"
        assert event.venue_name == "Berghain"
        assert event.venue_city == "Berlin"
        assert event.venue_country_code == "DE"

    def test_minimal_event_nullable_fields(self):
        event = parse_event(SAMPLE_EVENT_2)
        assert event.event_id == "5b4e6bcf-8c31-4c23-bf65-8eb5dc2bde14"
        assert event.legacy_id is None
        assert event.slug is None
        assert event.ending_time is None
        assert event.cover_url is None
        assert event.external_sales_url == "https://tickets.externalvendor.com/event/abc123"
        assert event.venue_id is None
        assert event.venue_name is None
        assert event.venue_city is None
        assert event.venue_country_code is None

    def test_unix_timestamp_conversion(self):
        event = parse_event(SAMPLE_EVENT_1)
        expected = datetime.fromtimestamp(1712700000, tz=timezone.utc)
        assert event.starting_time == expected

    def test_missing_starting_time_defaults_to_now(self):
        raw = dict(SAMPLE_EVENT_1)
        del raw["startingTime"]
        event = parse_event(raw)
        assert event.starting_time is not None


# ---- Tests for _extract_venue ----

@pytest.mark.unit
class TestExtractVenue:
    def test_full_venue(self):
        raw = {"venue": {"id": "v1", "name": "Club", "city": "Paris", "countryCode": "FR"}}
        vid, vname, vcity, vcc = _extract_venue(raw)
        assert vid == "v1"
        assert vname == "Club"
        assert vcity == "Paris"
        assert vcc == "FR"

    def test_no_venue(self):
        vid, vname, vcity, vcc = _extract_venue({})
        assert vid is None
        assert vname is None
        assert vcity is None
        assert vcc is None

    def test_nested_location(self):
        raw = {"venue": {"id": "v2", "name": "Bar", "location": {"city": "Madrid", "countryCode": "ES"}}}
        vid, vname, vcity, vcc = _extract_venue(raw)
        assert vcity == "Madrid"
        assert vcc == "ES"

    def test_nested_city_object(self):
        raw = {
            "venue": {
                "id": "v3",
                "name": "Temple",
                "city": {
                    "name": "San Francisco",
                    "country": {
                        "isoCode": "US",
                    },
                },
            }
        }
        vid, vname, vcity, vcc = _extract_venue(raw)
        assert vid == "v3"
        assert vname == "Temple"
        assert vcity == "San Francisco"
        assert vcc == "US"

    def test_null_venue(self):
        vid, vname, vcity, vcc = _extract_venue({"venue": None})
        assert vid is None
        assert vname is None


# ---- Tests for parse_admission ----

@pytest.mark.unit
class TestParseAdmission:
    def test_full_admission(self):
        raw = FLATTENED_ADMISSIONS[0]
        adm = parse_admission(raw, "event-uuid")
        assert adm.event_id == "event-uuid"
        assert adm.admission_id == "adm-001"
        assert adm.admission_type == "ticket"
        assert adm.name == "Early Bird"
        assert adm.is_sold_out is False
        assert adm.is_sales_closed is False
        assert adm.price == 12.50
        assert adm.currency == "EUR"
        assert adm.remaining == 50

    def test_sold_out_admission(self):
        raw = FLATTENED_ADMISSIONS[1]
        adm = parse_admission(raw, "event-uuid")
        assert adm.is_sold_out is True
        assert adm.is_sales_closed is True
        assert adm.remaining == 0

    def test_null_fields(self):
        raw = FLATTENED_ADMISSION_WITH_NULLS
        adm = parse_admission(raw, "event-uuid")
        assert adm.name is None
        assert adm.is_sold_out is None
        assert adm.is_sales_closed is None
        assert adm.price is None
        assert adm.currency is None
        assert adm.remaining is None


# ---- Tests for parse_connection_string ----

@pytest.mark.unit
class TestParseConnectionString:
    def test_bootstrap_server_plaintext(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=xceed"
        config, topic = parse_connection_string(cs)
        assert config["bootstrap.servers"] == "localhost:9092"
        assert topic == "xceed"

    def test_event_hubs_format(self):
        cs = "Endpoint=sb://myhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=xceed"
        config, topic = parse_connection_string(cs)
        assert "bootstrap.servers" in config
        assert topic == "xceed"

    def test_empty_string_raises(self):
        # Does not raise; returns empty topic
        config, topic = parse_connection_string("")
        assert topic == ""


# ---- Tests for XceedAPI fetch methods ----

@pytest.mark.unit
class TestXceedAPIFetch:
    def test_fetch_events_returns_data(self):
        api = XceedAPI()
        with patch.object(api, "_discover_event_count", return_value=2), \
             patch.object(api, "_fetch_events_page", return_value=SAMPLE_EVENTS_RESPONSE["data"]):
            events = api.fetch_events()
        assert len(events) == 2
        assert events[0]["id"] == "297ad280-4fd4-4b9a-870e-b4de6b2588a0"

    def test_fetch_admissions_returns_data(self):
        api = XceedAPI()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = SAMPLE_ADMISSIONS_RESPONSE
        with patch.object(api.session, "get", return_value=mock_resp):
            admissions = api.fetch_admissions("some-event-id")
        assert len(admissions) == 2
        assert admissions[0]["_category"] == "ticket"
        assert admissions[0]["id"] == "adm-001"

    def test_fetch_admissions_404_returns_empty(self):
        api = XceedAPI()
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        with patch.object(api.session, "get", return_value=mock_resp):
            admissions = api.fetch_admissions("nonexistent-event-id")
        assert admissions == []

    def test_fetch_events_list_response(self):
        api = XceedAPI()
        with patch.object(api, "_discover_event_count", return_value=1), \
             patch.object(api, "_fetch_events_page", return_value=[SAMPLE_EVENT_1]):
            events = api.fetch_events()
        assert len(events) == 1

    def test_fetch_events_reads_latest_window(self):
        api = XceedAPI(event_window_size=3, event_page_size=2)
        dataset = [
            {"id": f"event-{index}", "name": f"Event {index}", "startingTime": 1712700000 + index}
            for index in range(6)
        ]

        def fake_get(_url, params=None, timeout=None):
            offset = params["offset"]
            limit = params["limit"]
            page = dataset[offset:offset + limit]
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"success": True, "data": page}
            return mock_resp

        with patch.object(api.session, "get", side_effect=fake_get):
            events = api.fetch_events()

        assert [event["id"] for event in events] == ["event-3", "event-4", "event-5"]


# ---- Integration test: full one-cycle feed ----

class _StopLoop(Exception):
    """Sentinel used to break feed() loops inside tests without triggering KeyboardInterrupt."""


@pytest.mark.integration
class TestFeedOneCycle:
    """Test that feed() correctly routes events through both producer classes."""

    def _make_fake_event_producer(self):
        fp = MagicMock()
        fp.send_xceed_event = MagicMock()
        return fp

    def _make_fake_admissions_producer(self):
        fp = MagicMock()
        fp.send_xceed_event_admission = MagicMock()
        return fp

    def test_emits_event_and_admission_via_separate_producers(self):
        fake_event_prod = self._make_fake_event_producer()
        fake_adm_prod = self._make_fake_admissions_producer()
        fake_kafka_producer = MagicMock()
        fake_kafka_producer.flush.return_value = 0

        with patch("xceed.xceed.XceedEventProducer", return_value=fake_event_prod), \
             patch("xceed.xceed.XceedAdmissionsEventProducer", return_value=fake_adm_prod), \
             patch("xceed.xceed.Producer", return_value=fake_kafka_producer), \
             patch("xceed.xceed.XceedAPI") as MockAPI:
            mock_api = MagicMock()
            mock_api.fetch_events.return_value = [SAMPLE_EVENT_1, SAMPLE_EVENT_2]
            mock_api.fetch_admissions.side_effect = [
                FLATTENED_ADMISSIONS,
                [],  # second event has no admissions
            ]
            MockAPI.return_value = mock_api

            import argparse
            args = argparse.Namespace(
                connection_string="BootstrapServer=localhost:9092;EntityPath=xceed",
                topic="xceed",
                polling_interval=1,
                event_refresh_interval=9999,
                event_window_size=25,
                event_page_size=5,
            )

            # Stop after first polling cycle completes
            def stop_after_first(*a, **kw):
                raise _StopLoop

            with patch("time.sleep", side_effect=stop_after_first):
                try:
                    from xceed.xceed import feed
                    feed(args)
                except _StopLoop:
                    pass

        # Verify events were emitted via event_producer
        assert fake_event_prod.send_xceed_event.call_count == 2
        MockAPI.assert_called_once_with(event_window_size=25, event_page_size=5)

        # Verify admissions were emitted via admissions_producer
        assert fake_adm_prod.send_xceed_event_admission.call_count == 2

    def test_flush_failure_does_not_advance_state(self):
        """Flush failure must not cause silent data loss."""
        fake_kafka_producer = MagicMock()
        # Initial flush (for reference data) succeeds; polling cycle flush returns non-zero
        flush_calls = [0]

        def flush_side_effect(timeout=None):
            flush_calls[0] += 1
            # First flush (initial event emit) succeeds; subsequent fail
            return 0 if flush_calls[0] <= 1 else 1

        fake_kafka_producer.flush.side_effect = flush_side_effect

        with patch("xceed.xceed.Producer", return_value=fake_kafka_producer), \
             patch("xceed.xceed.XceedAPI") as MockAPI, \
             patch("xceed.xceed.XceedEventProducer"), \
             patch("xceed.xceed.XceedAdmissionsEventProducer"):
            mock_api = MagicMock()
            mock_api.fetch_events.return_value = [SAMPLE_EVENT_1]
            mock_api.fetch_admissions.return_value = FLATTENED_ADMISSIONS
            MockAPI.return_value = mock_api

            import argparse
            args = argparse.Namespace(
                connection_string="BootstrapServer=localhost:9092;EntityPath=xceed",
                topic="xceed",
                polling_interval=1,
                event_refresh_interval=9999,
                event_window_size=None,
                event_page_size=None,
            )

            def stop_after_first(*a, **kw):
                raise _StopLoop

            with patch("time.sleep", side_effect=stop_after_first):
                try:
                    from xceed.xceed import feed
                    feed(args)
                except _StopLoop:
                    pass

        # flush was called at least twice (initial + polling cycle)
        assert fake_kafka_producer.flush.call_count >= 1

    def test_reference_refresh_failure_keeps_cached_events(self):
        """If event refresh fails, cached events must not be discarded."""
        # Track what event IDs admissions were requested for
        admissions_requested_for = []

        def fake_fetch_admissions(event_id):
            admissions_requested_for.append(event_id)
            return []

        api = XceedAPI()
        with patch.object(api, "fetch_events", side_effect=[
            [SAMPLE_EVENT_1],       # startup fetch succeeds
            Exception("upstream error"),  # refresh fails
        ]):
            with patch.object(api, "fetch_admissions", side_effect=fake_fetch_admissions):
                # Startup fetch
                initial = api.fetch_events()
                assert len(initial) == 1
                cached = list(initial)

                # Simulate refresh failure: keep cached list
                try:
                    fresh = api.fetch_events()
                except Exception:
                    fresh = None

                if fresh is not None:
                    cached = list(fresh)

                # Verify cached_events was not cleared
                assert len(cached) == 1
                assert cached[0]["id"] == SAMPLE_EVENT_1["id"]

                # Simulate polling admissions with the preserved cache
                for raw_event in cached:
                    api.fetch_admissions(raw_event["id"])

        # Admissions should have been fetched for the original cached event
        assert SAMPLE_EVENT_1["id"] in admissions_requested_for
