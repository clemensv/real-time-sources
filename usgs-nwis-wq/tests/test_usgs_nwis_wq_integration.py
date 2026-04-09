"""
Integration tests for USGS NWIS Water Quality bridge.
Tests with mocked API responses.
"""

import pytest
import json
import asyncio
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from datetime import datetime, timezone
import aiohttp

from usgs_nwis_wq.usgs_nwis_wq import USGSWaterQualityPoller


MOCK_JSON_RESPONSE = {
    "value": {
        "queryInfo": {"queryURL": "http://waterservices.usgs.gov/nwis/iv/"},
        "timeSeries": [
            {
                "sourceInfo": {
                    "siteName": "TEST RIVER AT TEST CITY",
                    "siteCode": [{"value": "01646500", "agencyCode": "USGS"}],
                    "timeZoneInfo": {
                        "defaultTimeZone": {"zoneOffset": "-05:00"},
                        "daylightSavingsTimeZone": {"zoneOffset": "-04:00"},
                        "siteUsesDaylightSavingsTime": True
                    },
                    "geoLocation": {
                        "geogLocation": {"latitude": 38.95, "longitude": -77.13}
                    },
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "24", "name": "stateCd"}
                    ]
                },
                "variable": {
                    "variableCode": [{"value": "00300"}],
                    "variableName": "Dissolved oxygen",
                    "variableDescription": "Dissolved oxygen, mg/L",
                    "unit": {"unitCode": "mg/l"},
                    "noDataValue": -999999.0
                },
                "values": [
                    {
                        "value": [
                            {"value": "9.5", "qualifiers": ["P"],
                             "dateTime": "2024-11-15T10:00:00.000-05:00"},
                            {"value": "9.6", "qualifiers": ["P"],
                             "dateTime": "2024-11-15T10:15:00.000-05:00"}
                        ]
                    }
                ]
            }
        ]
    }
}


@pytest.mark.integration
class TestFetchJSON:
    """Test JSON fetching from USGS API (mocked)."""

    @pytest.mark.asyncio
    async def test_fetch_json_success(self):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=MOCK_JSON_RESPONSE)
        mock_response.raise_for_status = MagicMock()
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        with patch('aiohttp.ClientSession', return_value=mock_session):
            poller = USGSWaterQualityPoller()
            result = await poller.fetch_json("https://test.example.com")
            assert result is not None
            assert 'value' in result

    @pytest.mark.asyncio
    async def test_fetch_json_timeout(self):
        mock_session = MagicMock()
        mock_session.get = MagicMock(side_effect=asyncio.TimeoutError)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        with patch('aiohttp.ClientSession', return_value=mock_session):
            poller = USGSWaterQualityPoller()
            result = await poller.fetch_json("https://test.example.com")
            assert result is None

    @pytest.mark.asyncio
    async def test_fetch_json_http_error(self):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock(side_effect=aiohttp.ClientError("404"))
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        with patch('aiohttp.ClientSession', return_value=mock_session):
            poller = USGSWaterQualityPoller()
            result = await poller.fetch_json("https://test.example.com")
            assert result is None


@pytest.mark.integration
class TestPollAndSendWithMocks:
    """Test the poll_and_send flow with mocked producers."""

    @pytest.mark.asyncio
    async def test_poll_sites_sends_readings(self):
        """Verify that poll_and_send sends site and reading events."""
        mock_producer = MagicMock()
        mock_producer.flush = MagicMock()

        mock_site_producer = MagicMock()
        mock_site_producer.producer = mock_producer
        mock_site_producer.send_usgs_water_quality_sites_monitoring_site = MagicMock()

        mock_readings_producer = MagicMock()
        mock_readings_producer.producer = mock_producer
        mock_readings_producer.send_usgs_water_quality_readings_water_quality_reading = MagicMock()

        poller = USGSWaterQualityPoller(
            sites=['01646500'],
            parameter_codes='00300',
        )
        poller.site_producer = mock_site_producer
        poller.readings_producer = mock_readings_producer

        # Mock fetch_json to return data once, then break the loop
        call_count = 0
        async def mock_fetch(url):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return MOCK_JSON_RESPONSE
            return None

        poller.fetch_json = mock_fetch

        # Run one iteration by patching sleep to raise a custom exception
        class _BreakLoop(Exception):
            pass

        async def _break_sleep(_):
            raise _BreakLoop()

        with patch('asyncio.sleep', side_effect=_break_sleep):
            try:
                await poller.poll_and_send()
            except _BreakLoop:
                pass

        mock_site_producer.send_usgs_water_quality_sites_monitoring_site.assert_called()
        mock_readings_producer.send_usgs_water_quality_readings_water_quality_reading.assert_called()
        assert mock_readings_producer.send_usgs_water_quality_readings_water_quality_reading.call_count == 2
