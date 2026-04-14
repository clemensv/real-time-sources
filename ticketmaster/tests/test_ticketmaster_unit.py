"""
Unit tests for the Ticketmaster Discovery API bridge.
"""

import json
import os
import tempfile
import pytest
from unittest.mock import MagicMock, patch, call
from datetime import datetime, timezone

from ticketmaster.ticketmaster import (
    TicketmasterBridge,
    _load_state,
    _save_state,
    _parse_event,
    _parse_venue,
    _parse_attraction,
    _parse_classification,
    _first_classification,
    parse_connection_string,
)
from ticketmaster_producer_data import Event, Venue, Attraction, Classification


# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------

def _make_raw_event(**overrides) -> dict:
    """Build a minimal valid Ticketmaster API event dict."""
    base = {
        "id": "G5v0Z9iQkPl_2",
        "name": "Test Concert",
        "type": "event",
        "url": "https://www.ticketmaster.com/event/G5v0Z9iQkPl_2",
        "locale": "en-us",
        "dates": {
            "start": {
                "localDate": "2024-07-20",
                "localTime": "19:30:00",
                "dateTime": "2024-07-20T23:30:00Z",
            },
            "status": {"code": "onsale"},
        },
        "classifications": [
            {
                "segment": {"id": "KZFzniwnSyZfZ7v7nJ", "name": "Music"},
                "primaryGenre": {"id": "KnvZfZ7vAeA", "name": "Rock"},
                "primarySubGenre": {"id": "KZazBEonSMnZfZ7v6F1", "name": "Pop"},
            }
        ],
        "_embedded": {
            "venues": [
                {
                    "id": "KovZpaFVAeA",
                    "name": "Madison Square Garden",
                    "city": {"name": "New York"},
                    "state": {"stateCode": "NY"},
                    "country": {"countryCode": "US"},
                    "location": {"latitude": "40.7505", "longitude": "-73.9934"},
                }
            ],
            "attractions": [
                {"id": "K8vZ91718H7", "name": "Taylor Swift"},
            ],
        },
        "priceRanges": [{"min": 85.0, "max": 450.0, "currency": "USD"}],
        "sales": {
            "public": {
                "startDateTime": "2024-01-15T15:00:00Z",
                "endDateTime": "2024-07-20T23:30:00Z",
            }
        },
        "info": "Event info text.",
        "pleaseNote": "No cameras.",
    }
    base.update(overrides)
    return base


def _make_raw_venue(**overrides) -> dict:
    """Build a minimal valid Ticketmaster API venue dict."""
    base = {
        "id": "KovZpaFVAeA",
        "name": "Madison Square Garden",
        "url": "https://www.ticketmaster.com/venue/KovZpaFVAeA",
        "locale": "en-us",
        "timezone": "America/New_York",
        "city": {"name": "New York"},
        "state": {"stateCode": "NY"},
        "country": {"countryCode": "US"},
        "address": {"line1": "4 Pennsylvania Plaza"},
        "postalCode": "10001",
        "location": {"latitude": "40.7505", "longitude": "-73.9934"},
    }
    base.update(overrides)
    return base


def _make_raw_attraction(**overrides) -> dict:
    """Build a minimal valid Ticketmaster API attraction dict."""
    base = {
        "id": "K8vZ91718H7",
        "name": "Taylor Swift",
        "url": "https://www.ticketmaster.com/artist/K8vZ91718H7",
        "locale": "en-us",
        "classifications": [
            {
                "segment": {"id": "KZFzniwnSyZfZ7v7nJ", "name": "Music"},
                "primaryGenre": {"id": "KnvZfZ7vAeA", "name": "Rock"},
                "primarySubGenre": {"id": "KZazBEonSMnZfZ7v6F1", "name": "Pop"},
            }
        ],
    }
    base.update(overrides)
    return base


def _make_raw_classification(**overrides) -> dict:
    """Build a minimal valid Ticketmaster API classification dict."""
    base = {
        "type": "segment",
        "segment": {"id": "KZFzniwnSyZfZ7v7nJ", "name": "Music"},
        "primaryGenre": {"id": "KnvZfZ7vAeA", "name": "Rock"},
        "primarySubGenre": {"id": "KZazBEonSMnZfZ7v6F1", "name": "Pop"},
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# parse_connection_string
# ---------------------------------------------------------------------------

class TestParseConnectionString:

    @pytest.mark.unit
    def test_event_hubs_format(self):
        conn = (
            "Endpoint=sb://my-ns.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=secret123;"
            "EntityPath=ticketmaster"
        )
        result = parse_connection_string(conn)
        assert "my-ns.servicebus.windows.net:9093" in result["bootstrap.servers"]
        assert result["kafka_topic"] == "ticketmaster"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["sasl.password"] == conn
        assert result["sasl.mechanisms"] == "PLAIN"
        assert result["security.protocol"] == "SASL_SSL"

    @pytest.mark.unit
    def test_plain_bootstrap_format(self):
        conn = "BootstrapServer=localhost:9092;EntityPath=ticketmaster"
        result = parse_connection_string(conn)
        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["kafka_topic"] == "ticketmaster"


# ---------------------------------------------------------------------------
# _parse_event
# ---------------------------------------------------------------------------

class TestParseEvent:

    @pytest.mark.unit
    def test_parses_full_event(self):
        raw = _make_raw_event()
        event = _parse_event(raw)
        assert event is not None
        assert event.event_id == "G5v0Z9iQkPl_2"
        assert event.name == "Test Concert"
        assert event.type == "event"
        assert event.start_date == "2024-07-20"
        assert event.start_time == "19:30:00"
        assert event.start_datetime_utc == "2024-07-20T23:30:00Z"
        assert event.status == "onsale"
        assert event.segment_id == "KZFzniwnSyZfZ7v7nJ"
        assert event.segment_name == "Music"
        assert event.genre_id == "KnvZfZ7vAeA"
        assert event.genre_name == "Rock"
        assert event.venue_id == "KovZpaFVAeA"
        assert event.venue_name == "Madison Square Garden"
        assert event.venue_city == "New York"
        assert event.venue_state_code == "NY"
        assert event.venue_country_code == "US"
        assert event.venue_latitude == 40.7505
        assert event.venue_longitude == -73.9934
        assert event.price_min == 85.0
        assert event.price_max == 450.0
        assert event.currency == "USD"
        assert "K8vZ91718H7" in event.attraction_ids
        assert "Taylor Swift" in event.attraction_names
        assert event.info == "Event info text."
        assert event.please_note == "No cameras."

    @pytest.mark.unit
    def test_returns_none_missing_id(self):
        raw = _make_raw_event(id="")
        assert _parse_event(raw) is None

    @pytest.mark.unit
    def test_returns_none_missing_name(self):
        raw = _make_raw_event(name="")
        assert _parse_event(raw) is None

    @pytest.mark.unit
    def test_null_optional_fields(self):
        raw = _make_raw_event()
        raw["priceRanges"] = []
        raw["_embedded"]["venues"] = []
        raw["_embedded"]["attractions"] = []
        event = _parse_event(raw)
        assert event is not None
        assert event.price_min is None
        assert event.price_max is None
        assert event.currency is None
        assert event.venue_id is None
        assert event.attraction_ids is None

    @pytest.mark.unit
    def test_event_no_classifications(self):
        raw = _make_raw_event()
        raw["classifications"] = []
        event = _parse_event(raw)
        assert event is not None
        assert event.segment_id is None
        assert event.genre_id is None

    @pytest.mark.unit
    def test_start_datetime_local_combined(self):
        raw = _make_raw_event()
        event = _parse_event(raw)
        assert event is not None
        assert event.start_datetime_local == "2024-07-20T19:30:00"

    @pytest.mark.unit
    def test_start_datetime_local_date_only(self):
        raw = _make_raw_event()
        raw["dates"]["start"] = {"localDate": "2024-07-20", "dateTime": "2024-07-20T23:00:00Z"}
        event = _parse_event(raw)
        assert event is not None
        assert event.start_datetime_local == "2024-07-20"


# ---------------------------------------------------------------------------
# _parse_venue
# ---------------------------------------------------------------------------

class TestParseVenue:

    @pytest.mark.unit
    def test_parses_full_venue(self):
        raw = _make_raw_venue()
        venue = _parse_venue(raw)
        assert venue is not None
        assert venue.entity_id == "KovZpaFVAeA"
        assert venue.name == "Madison Square Garden"
        assert venue.timezone == "America/New_York"
        assert venue.city == "New York"
        assert venue.state_code == "NY"
        assert venue.country_code == "US"
        assert venue.address == "4 Pennsylvania Plaza"
        assert venue.postal_code == "10001"
        assert venue.latitude == 40.7505
        assert venue.longitude == -73.9934

    @pytest.mark.unit
    def test_returns_none_missing_id(self):
        raw = _make_raw_venue(id="")
        assert _parse_venue(raw) is None

    @pytest.mark.unit
    def test_null_optional_location(self):
        raw = _make_raw_venue()
        raw["location"] = {}
        venue = _parse_venue(raw)
        assert venue is not None
        assert venue.latitude is None
        assert venue.longitude is None


# ---------------------------------------------------------------------------
# _parse_attraction
# ---------------------------------------------------------------------------

class TestParseAttraction:

    @pytest.mark.unit
    def test_parses_full_attraction(self):
        raw = _make_raw_attraction()
        attr = _parse_attraction(raw)
        assert attr is not None
        assert attr.entity_id == "K8vZ91718H7"
        assert attr.name == "Taylor Swift"
        assert attr.segment_id == "KZFzniwnSyZfZ7v7nJ"
        assert attr.segment_name == "Music"
        assert attr.genre_name == "Rock"

    @pytest.mark.unit
    def test_returns_none_missing_id(self):
        raw = _make_raw_attraction(id="")
        assert _parse_attraction(raw) is None


# ---------------------------------------------------------------------------
# _parse_classification
# ---------------------------------------------------------------------------

class TestParseClassification:

    @pytest.mark.unit
    def test_parses_full_classification(self):
        raw = _make_raw_classification()
        clf = _parse_classification(raw)
        assert clf is not None
        assert clf.entity_id == "KZFzniwnSyZfZ7v7nJ"
        assert clf.name == "Music"
        assert clf.type == "segment"
        assert clf.primary_genre_id == "KnvZfZ7vAeA"
        assert clf.primary_genre_name == "Rock"

    @pytest.mark.unit
    def test_returns_none_missing_segment(self):
        raw = {"type": "segment"}
        assert _parse_classification(raw) is None


# ---------------------------------------------------------------------------
# TicketmasterBridge — reference-data emit methods
# ---------------------------------------------------------------------------

class TestBridgeReferenceEmit:

    def _make_bridge(self):
        ref_prod = MagicMock()
        ref_prod.producer = MagicMock()
        ref_prod.producer.flush.return_value = 0
        events_prod = MagicMock()
        events_prod.producer = MagicMock()
        events_prod.producer.flush.return_value = 0
        bridge = TicketmasterBridge(
            api_key="test-key",
            events_producer=events_prod,
            reference_producer=ref_prod,
            country_codes="US",
        )
        return bridge, ref_prod, events_prod

    @pytest.mark.unit
    def test_emit_classifications(self):
        bridge, ref_prod, _ = self._make_bridge()
        clf = Classification(
            entity_id="KZFzniwnSyZfZ7v7nJ",
            name="Music",
            type="segment",
            primary_genre_id=None,
            primary_genre_name=None,
            primary_subgenre_id=None,
            primary_subgenre_name=None,
        )
        count = bridge.emit_classifications({"KZFzniwnSyZfZ7v7nJ": clf})
        assert count == 1
        ref_prod.send_ticketmaster_reference_classification.assert_called_once()
        call_kwargs = ref_prod.send_ticketmaster_reference_classification.call_args
        assert call_kwargs.kwargs["_entity_id"] == "KZFzniwnSyZfZ7v7nJ"
        assert call_kwargs.kwargs["flush_producer"] is False

    @pytest.mark.unit
    def test_emit_venues(self):
        bridge, ref_prod, _ = self._make_bridge()
        venue = Venue(
            entity_id="KovZpaFVAeA",
            name="MSG",
            url=None, locale=None, timezone=None, city=None,
            state_code=None, country_code=None, address=None,
            postal_code=None, latitude=None, longitude=None,
        )
        count = bridge.emit_venues({"KovZpaFVAeA": venue})
        assert count == 1
        ref_prod.send_ticketmaster_reference_venue.assert_called_once()

    @pytest.mark.unit
    def test_emit_attractions(self):
        bridge, ref_prod, _ = self._make_bridge()
        attr = Attraction(
            entity_id="K8vZ91718H7",
            name="Taylor Swift",
            url=None, locale=None, segment_id=None, segment_name=None,
            genre_id=None, genre_name=None, subgenre_id=None, subgenre_name=None,
        )
        count = bridge.emit_attractions({"K8vZ91718H7": attr})
        assert count == 1
        ref_prod.send_ticketmaster_reference_attraction.assert_called_once()


# ---------------------------------------------------------------------------
# TicketmasterBridge — flush-failure: state must NOT advance
# ---------------------------------------------------------------------------

class TestBridgeFlushFailure:

    @pytest.mark.unit
    def test_flush_failure_does_not_advance_dedupe_state(self):
        """If Kafka flush returns non-zero, seen_events must not be updated."""
        events_prod = MagicMock()
        events_prod.producer = MagicMock()
        # Simulate flush failure (non-zero messages remain)
        events_prod.producer.flush.return_value = 1

        bridge = TicketmasterBridge(
            api_key="test-key",
            events_producer=events_prod,
            reference_producer=None,
            country_codes="US",
        )

        raw_events = [_make_raw_event()]
        with patch.object(bridge, "fetch_events_for_country", return_value=raw_events):
            bridge.poll_events()

        # Dedupe state must remain empty because flush failed
        assert len(bridge._seen_events) == 0
        # But the send method should have been called
        events_prod.send_ticketmaster_events_event.assert_called_once()

    @pytest.mark.unit
    def test_flush_success_advances_dedupe_state(self):
        """If Kafka flush returns zero, seen_events should be updated."""
        events_prod = MagicMock()
        events_prod.producer = MagicMock()
        events_prod.producer.flush.return_value = 0  # success

        bridge = TicketmasterBridge(
            api_key="test-key",
            events_producer=events_prod,
            reference_producer=None,
            country_codes="US",
        )

        raw_events = [_make_raw_event()]
        with patch.object(bridge, "fetch_events_for_country", return_value=raw_events):
            bridge.poll_events()

        assert "G5v0Z9iQkPl_2" in bridge._seen_events

    @pytest.mark.unit
    def test_same_event_not_re_emitted_when_status_unchanged(self):
        """Events that were already emitted with the same status should not be re-emitted."""
        events_prod = MagicMock()
        events_prod.producer = MagicMock()
        events_prod.producer.flush.return_value = 0

        bridge = TicketmasterBridge(
            api_key="test-key",
            events_producer=events_prod,
            reference_producer=None,
            country_codes="US",
        )

        raw_events = [_make_raw_event()]
        with patch.object(bridge, "fetch_events_for_country", return_value=raw_events):
            bridge.poll_events()  # First poll
            events_prod.send_ticketmaster_events_event.reset_mock()
            bridge.poll_events()  # Second poll — same events, same status

        # Should not be re-emitted
        events_prod.send_ticketmaster_events_event.assert_not_called()


# ---------------------------------------------------------------------------
# TicketmasterBridge — multi-family wiring test
# ---------------------------------------------------------------------------

class TestBridgeMultiFamilyWiring:

    @pytest.mark.unit
    def test_one_cycle_routes_all_families(self):
        """A single run cycle must route events to events producer and reference to reference producer."""
        events_prod = MagicMock()
        events_prod.producer = MagicMock()
        events_prod.producer.flush.return_value = 0

        ref_prod = MagicMock()
        ref_prod.producer = MagicMock()
        ref_prod.producer.flush.return_value = 0

        bridge = TicketmasterBridge(
            api_key="test-key",
            events_producer=events_prod,
            reference_producer=ref_prod,
            country_codes="US",
        )

        raw_venue = _make_raw_venue()
        raw_attr = _make_raw_attraction()
        raw_clf = _make_raw_classification()
        raw_event = _make_raw_event()

        with (
            patch.object(bridge, "fetch_classifications", return_value={"KZFzniwnSyZfZ7v7nJ": _parse_classification(raw_clf)}),
            patch.object(bridge, "fetch_venues_for_country", return_value={"KovZpaFVAeA": _parse_venue(raw_venue)}),
            patch.object(bridge, "fetch_attractions_for_country", return_value={"K8vZ91718H7": _parse_attraction(raw_attr)}),
            patch.object(bridge, "fetch_events_for_country", return_value=[raw_event]),
        ):
            bridge.refresh_reference_data()
            bridge.poll_events()

        # Reference producer must have been called for all 3 reference families
        ref_prod.send_ticketmaster_reference_classification.assert_called_once()
        ref_prod.send_ticketmaster_reference_venue.assert_called_once()
        ref_prod.send_ticketmaster_reference_attraction.assert_called_once()

        # Events producer must have been called for the event
        events_prod.send_ticketmaster_events_event.assert_called_once()


# ---------------------------------------------------------------------------
# TicketmasterBridge — transient reference refresh failure (cache preservation)
# ---------------------------------------------------------------------------

class TestBridgeReferenceRefreshFailure:

    @pytest.mark.unit
    def test_failed_venue_refresh_keeps_prior_cache(self):
        """A failed venue refresh must not discard the existing cache."""
        ref_prod = MagicMock()
        ref_prod.producer = MagicMock()
        ref_prod.producer.flush.return_value = 0

        bridge = TicketmasterBridge(
            api_key="test-key",
            events_producer=None,
            reference_producer=ref_prod,
            country_codes="US",
        )

        # Seed the cache
        existing_venue = _parse_venue(_make_raw_venue())
        bridge._venue_cache = {existing_venue.entity_id: existing_venue}

        clf = _parse_classification(_make_raw_classification())
        with (
            patch.object(bridge, "fetch_classifications", return_value={"KZFzniwnSyZfZ7v7nJ": clf}),
            patch.object(bridge, "fetch_venues_for_country", side_effect=Exception("network error")),
            patch.object(bridge, "fetch_attractions_for_country", return_value={}),
        ):
            bridge.refresh_reference_data()

        # Prior venue cache should still be intact
        assert "KovZpaFVAeA" in bridge._venue_cache

    @pytest.mark.unit
    def test_failed_country_venue_does_not_abort_other_countries(self):
        """A failed venue fetch for one country should not prevent other countries from being processed."""
        ref_prod = MagicMock()
        ref_prod.producer = MagicMock()
        ref_prod.producer.flush.return_value = 0

        bridge = TicketmasterBridge(
            api_key="test-key",
            events_producer=None,
            reference_producer=ref_prod,
            country_codes="US,GB",
        )

        us_venue = _parse_venue({**_make_raw_venue(), "id": "VenueUS", "name": "US Venue"})
        gb_venue = _parse_venue({**_make_raw_venue(), "id": "VenueGB", "name": "GB Venue"})

        call_count = {"n": 0}

        def venue_side_effect(country_code):
            call_count["n"] += 1
            if country_code == "US":
                raise Exception("US venue fetch failed")
            return {"VenueGB": gb_venue}

        with (
            patch.object(bridge, "fetch_classifications", return_value={}),
            patch.object(bridge, "fetch_venues_for_country", side_effect=venue_side_effect),
            patch.object(bridge, "fetch_attractions_for_country", return_value={}),
        ):
            bridge.refresh_reference_data()

        # Both countries attempted
        assert call_count["n"] == 2
        # GB venue should be in cache
        assert "VenueGB" in bridge._venue_cache


# ---------------------------------------------------------------------------
# State persistence: _load_state / _save_state / file-backed bridge
# ---------------------------------------------------------------------------

class TestStatePersistence:

    @pytest.mark.unit
    def test_load_state_missing_file_returns_empty(self):
        """_load_state returns an empty dict when the file does not exist."""
        assert _load_state("/tmp/__nonexistent_ticketmaster_state__.json") == {}

    @pytest.mark.unit
    def test_load_state_empty_string_returns_empty(self):
        """_load_state returns an empty dict when no path is provided."""
        assert _load_state("") == {}

    @pytest.mark.unit
    def test_save_and_reload_round_trip(self):
        """State written by _save_state is readable by _load_state."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            data = {"evt1": "evt1:onsale", "evt2": "evt2:cancelled"}
            _save_state(path, data)
            loaded = _load_state(path)
            assert loaded == data
        finally:
            os.unlink(path)

    @pytest.mark.unit
    def test_save_state_creates_parent_dir(self):
        """_save_state creates missing parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "subdir", "ticketmaster_state.json")
            _save_state(path, {"k": "v"})
            assert os.path.exists(path)

    @pytest.mark.unit
    def test_bridge_loads_state_at_init(self):
        """Bridge constructor loads persisted dedupe state from the state file."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            json.dump({"existing_id": "existing_id:onsale"}, f)
            path = f.name
        try:
            bridge = TicketmasterBridge(
                api_key="test-key",
                events_producer=None,
                reference_producer=None,
                state_file=path,
            )
            assert bridge._seen_events == {"existing_id": "existing_id:onsale"}
        finally:
            os.unlink(path)

    @pytest.mark.unit
    def test_bridge_persists_state_after_successful_flush(self):
        """Bridge writes updated dedupe state to the state file after a successful flush."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name

        try:
            events_prod = MagicMock()
            events_prod.producer = MagicMock()
            events_prod.producer.flush.return_value = 0  # flush succeeds

            bridge = TicketmasterBridge(
                api_key="test-key",
                events_producer=events_prod,
                reference_producer=None,
                country_codes="US",
                state_file=path,
            )

            raw_events = [_make_raw_event()]
            with patch.object(bridge, "fetch_events_for_country", return_value=raw_events):
                bridge.poll_events()

            # State file must be written
            on_disk = _load_state(path)
            assert "G5v0Z9iQkPl_2" in on_disk
        finally:
            if os.path.exists(path):
                os.unlink(path)

    @pytest.mark.unit
    def test_bridge_does_not_persist_state_after_flush_failure(self):
        """Bridge must NOT write state to file when Kafka flush leaves messages undelivered."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            json.dump({}, f)
            path = f.name

        try:
            events_prod = MagicMock()
            events_prod.producer = MagicMock()
            events_prod.producer.flush.return_value = 1  # flush fails

            bridge = TicketmasterBridge(
                api_key="test-key",
                events_producer=events_prod,
                reference_producer=None,
                country_codes="US",
                state_file=path,
            )

            raw_events = [_make_raw_event()]
            with patch.object(bridge, "fetch_events_for_country", return_value=raw_events):
                bridge.poll_events()

            # File must still be empty — flush failed, state not advanced
            on_disk = _load_state(path)
            assert on_disk == {}
        finally:
            if os.path.exists(path):
                os.unlink(path)
