"""
Integration tests for USGS Earthquake data poller.
Tests that mock external API calls but verify end-to-end data flow.
"""

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from datetime import datetime, timezone
from usgs_earthquakes.usgs_earthquakes import USGSEarthquakePoller


SAMPLE_GEOJSON_RESPONSE = {
    "type": "FeatureCollection",
    "metadata": {
        "generated": 1700000200000,
        "url": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson",
        "title": "USGS All Earthquakes, Past Hour",
        "status": 200,
        "api": "1.10.3",
        "count": 2
    },
    "features": [
        {
            "type": "Feature",
            "id": "us7000abc1",
            "properties": {
                "mag": 5.2,
                "place": "50km NW of Somewhere, Country",
                "time": 1700000000000,
                "updated": 1700000100000,
                "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us7000abc1",
                "detail": "https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=us7000abc1&format=geojson",
                "felt": 50,
                "cdi": 4.2,
                "mmi": 5.1,
                "alert": "green",
                "status": "reviewed",
                "tsunami": 0,
                "sig": 416,
                "net": "us",
                "code": "7000abc1",
                "sources": ",us,",
                "nst": 30,
                "dmin": 1.2,
                "rms": 0.65,
                "gap": 60.0,
                "magType": "mww",
                "type": "earthquake"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [-120.5, 35.2, 15.0]
            }
        },
        {
            "type": "Feature",
            "id": "ci12345678",
            "properties": {
                "mag": 2.1,
                "place": "5km E of Small Town, CA",
                "time": 1700000050000,
                "updated": 1700000150000,
                "url": "https://earthquake.usgs.gov/earthquakes/eventpage/ci12345678",
                "detail": "https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=ci12345678&format=geojson",
                "felt": None,
                "cdi": None,
                "mmi": None,
                "alert": None,
                "status": "automatic",
                "tsunami": 0,
                "sig": 68,
                "net": "ci",
                "code": "12345678",
                "sources": ",ci,",
                "nst": 12,
                "dmin": 0.03,
                "rms": 0.12,
                "gap": 90.0,
                "magType": "ml",
                "type": "earthquake"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [-117.2, 33.8, 8.5]
            }
        }
    ]
}


@pytest.mark.integration
class TestFetchFeed:
    """Test feed fetching with mocked HTTP responses."""

    @pytest.mark.asyncio
    async def test_fetch_feed_returns_features(self):
        """Test that fetch_feed returns parsed features from mocked response."""
        poller = USGSEarthquakePoller(feed='all_hour')

        mock_response = AsyncMock()
        mock_response.raise_for_status = Mock()
        mock_response.json = AsyncMock(return_value=SAMPLE_GEOJSON_RESPONSE)

        mock_session = AsyncMock()
        mock_session.get = Mock(return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response), __aexit__=AsyncMock(return_value=False)))

        with patch('aiohttp.ClientSession', return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session), __aexit__=AsyncMock(return_value=False))):
            features = await poller.fetch_feed()

        assert len(features) == 2
        assert features[0]["id"] == "us7000abc1"
        assert features[1]["id"] == "ci12345678"

    def test_parse_multiple_events(self):
        """Test parsing multiple features from a feed response."""
        poller = USGSEarthquakePoller()

        events = []
        for feature in SAMPLE_GEOJSON_RESPONSE["features"]:
            event = poller.parse_event(feature)
            if event:
                events.append(event)

        assert len(events) == 2
        assert events[0].magnitude == 5.2
        assert events[0].net == "us"
        assert events[1].magnitude == 2.1
        assert events[1].net == "ci"
