"""
End-to-end tests for the NASA FIRMS active-fire poller.
These tests call the real NASA FIRMS Area API and require a MAP_KEY in the
FIRMS_MAP_KEY environment variable.
Run with: pytest tests/test_nasa_firms_e2e.py -m e2e
"""

import os

import aiohttp
import pytest

from nasa_firms.nasa_firms import FirmsPoller


MAP_KEY = os.getenv('FIRMS_MAP_KEY')


@pytest.mark.e2e
@pytest.mark.skipif(not MAP_KEY, reason="FIRMS_MAP_KEY not set")
class TestLiveAPI:
    """Tests that call the real NASA FIRMS API."""

    @pytest.mark.asyncio
    async def test_fetch_detections(self):
        poller = FirmsPoller(map_key=MAP_KEY, sources=['VIIRS_SNPP_NRT'], day_range=1)
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=120)) as session:
            detections = await poller.fetch_detections(session, 'VIIRS_SNPP_NRT')
        assert isinstance(detections, list)
        for det in detections[:50]:
            assert -90 <= det.latitude <= 90
            assert -180 <= det.longitude <= 180
            assert len(det.record_id) == 16

    @pytest.mark.asyncio
    async def test_fetch_availability(self):
        poller = FirmsPoller(map_key=MAP_KEY, sources=['VIIRS_SNPP_NRT', 'MODIS_NRT'])
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=120)) as session:
            records = await poller.fetch_availability(session)
        assert isinstance(records, list)
        ids = {r.source for r in records}
        assert ids.issubset({'VIIRS_SNPP_NRT', 'MODIS_NRT'})
