"""
End-to-end tests for USGS NWIS Water Quality bridge.
Tests against real USGS API endpoints.
"""

import pytest
import asyncio
from usgs_nwis_wq.usgs_nwis_wq import USGSWaterQualityPoller


@pytest.mark.e2e
class TestUSGSWaterQualityAPIEndToEnd:
    """End-to-end tests against real USGS Water Quality API."""

    @pytest.mark.asyncio
    async def test_fetch_real_data_single_site(self):
        """Fetch real WQ data for a known site (Potomac River)."""
        poller = USGSWaterQualityPoller()
        url = USGSWaterQualityPoller.build_api_url(
            sites=['01646500'], parameter_codes='00300,00010', period='PT2H'
        )
        data = await poller.fetch_json(url)
        assert data is not None
        assert 'value' in data
        ts = data['value'].get('timeSeries', [])
        # Site may or may not have data depending on sensor status
        print(f"\nFetched {len(ts)} time series for site 01646500")

    @pytest.mark.asyncio
    async def test_parse_real_response(self):
        """Fetch and parse real data for Maryland."""
        poller = USGSWaterQualityPoller()
        url = USGSWaterQualityPoller.build_api_url(
            state_cd='MD', parameter_codes='00300,00010,00400', period='PT2H'
        )
        data = await poller.fetch_json(url)
        if data:
            sites, readings = USGSWaterQualityPoller.parse_waterml_response(data)
            print(f"\nMD: {len(sites)} sites, {len(readings)} readings")
            if sites:
                s = sites[0]
                assert s.site_number
                assert s.agency_code
            if readings:
                r = readings[0]
                assert r.site_number
                assert r.parameter_code
                assert r.date_time
