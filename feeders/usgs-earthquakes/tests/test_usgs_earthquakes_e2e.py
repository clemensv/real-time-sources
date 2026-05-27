"""
End-to-end tests for USGS Earthquake data poller.
These tests call the real USGS Earthquake API.
Run with: pytest tests/test_usgs_earthquakes_e2e.py -m e2e
"""

import pytest
from usgs_earthquakes.usgs_earthquakes import USGSEarthquakePoller, FEED_URLS


@pytest.mark.e2e
class TestLiveAPI:
    """Tests that call the real USGS Earthquake GeoJSON API."""

    @pytest.mark.asyncio
    async def test_fetch_all_hour_feed(self):
        """Test fetching the all_hour feed from the live API."""
        poller = USGSEarthquakePoller(feed='all_hour')
        features = await poller.fetch_feed()

        assert isinstance(features, list)
        # There are almost always earthquakes in any given hour
        # but we can't guarantee it, so just check the type
        for feature in features:
            assert "id" in feature
            assert "properties" in feature
            assert "geometry" in feature

    @pytest.mark.asyncio
    async def test_fetch_and_parse_events(self):
        """Test fetching and parsing events from the live API."""
        poller = USGSEarthquakePoller(feed='all_day')
        features = await poller.fetch_feed()

        assert len(features) > 0, "Expected at least one earthquake in the past day"

        events = []
        for feature in features:
            event = poller.parse_event(feature)
            if event:
                events.append(event)

        assert len(events) > 0, "Expected at least one parseable event"

        # Validate the first event has expected fields populated
        event = events[0]
        assert event.id
        assert event.event_time
        assert event.net
        assert event.code
        assert isinstance(event.latitude, float)
        assert isinstance(event.longitude, float)
        assert -90 <= event.latitude <= 90
        assert -180 <= event.longitude <= 180

    @pytest.mark.asyncio
    async def test_fetch_significant_month(self):
        """Test fetching the significant_month feed which typically has events."""
        poller = USGSEarthquakePoller(feed='significant_month')
        features = await poller.fetch_feed()

        assert isinstance(features, list)
        if features:
            event = poller.parse_event(features[0])
            assert event is not None
            assert event.magnitude is not None
            # Significant events should have notable magnitude
            assert event.magnitude >= 4.0

    @pytest.mark.asyncio
    async def test_event_serialization_roundtrip(self):
        """Test that live events can be serialized to JSON and Avro."""
        poller = USGSEarthquakePoller(feed='all_day')
        features = await poller.fetch_feed()

        assert len(features) > 0
        event = poller.parse_event(features[0])
        assert event is not None

        # JSON roundtrip
        json_bytes = event.to_byte_array("application/json")
        assert json_bytes is not None
        assert len(json_bytes) > 0

        # Avro roundtrip
        avro_bytes = event.to_byte_array("avro/binary")
        assert avro_bytes is not None
        assert len(avro_bytes) > 0

    @pytest.mark.asyncio
    async def test_min_magnitude_filter_with_live_data(self):
        """Test that magnitude filtering works with live data."""
        poller = USGSEarthquakePoller(feed='all_day', min_magnitude=4.0)
        features = await poller.fetch_feed()

        for feature in features:
            event = poller.parse_event(feature)
            if event is not None:
                assert event.magnitude is None or event.magnitude >= 4.0
