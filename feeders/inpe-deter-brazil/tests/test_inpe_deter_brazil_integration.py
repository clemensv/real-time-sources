"""
Integration tests for INPE DETER Brazil deforestation alert poller.
Tests that mock external API calls but verify end-to-end data flow.
"""

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from datetime import datetime, timezone
from inpe_deter_brazil.inpe_deter_brazil import INPEDeterPoller


SAMPLE_GEOJSON_RESPONSE = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "deter_amz.fid-abc123",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [[[
                    [-48.055, -2.9296],
                    [-48.0548, -2.9296],
                    [-48.0544, -2.9299],
                    [-48.0548, -2.9335],
                    [-48.055, -2.9335],
                    [-48.055, -2.9296],
                ]]]
            },
            "properties": {
                "gid": "91537_hist",
                "classname": "DESMATAMENTO_CR",
                "path_row": "036016",
                "view_date": "2026-02-21",
                "sensor": "WFI",
                "satellite": "AMAZONIA-1",
                "areamunkm": 0.078,
                "municipality": "Ipixuna do Para",
                "uf": "PA",
                "publish_month": "2026-02-01"
            }
        },
        {
            "type": "Feature",
            "id": "deter_amz.fid-def456",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [[[
                    [-47.7159, -2.5547],
                    [-47.7057, -2.5467],
                    [-47.7159, -2.5547],
                ]]]
            },
            "properties": {
                "gid": "13558_curr",
                "classname": "DEGRADACAO",
                "path_row": "035016",
                "view_date": "2026-03-11",
                "sensor": "WFI",
                "satellite": "AMAZONIA-1",
                "areamunkm": 0.201,
                "municipality": "Ipixuna do Para",
                "uf": "PA",
                "publish_month": "2026-03-01"
            }
        }
    ]
}


@pytest.mark.integration
class TestFetchBiome:
    """Test biome fetching with mocked HTTP responses."""

    @pytest.mark.asyncio
    async def test_fetch_amazon_returns_features(self):
        """Test that fetch_biome returns parsed features from mocked response."""
        poller = INPEDeterPoller()

        mock_response = AsyncMock()
        mock_response.raise_for_status = Mock()
        mock_response.json = AsyncMock(return_value=SAMPLE_GEOJSON_RESPONSE)

        mock_session = AsyncMock()
        mock_session.get = Mock(return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_response),
            __aexit__=AsyncMock(return_value=False)
        ))

        with patch('aiohttp.ClientSession', return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session),
            __aexit__=AsyncMock(return_value=False)
        )):
            features = await poller.fetch_biome("amazon", since_date="2026-01-01")

        assert len(features) == 2
        assert features[0]["properties"]["gid"] == "91537_hist"
        assert features[1]["properties"]["gid"] == "13558_curr"

    def test_parse_multiple_alerts(self):
        """Test parsing multiple features from a feed response."""
        poller = INPEDeterPoller()

        alerts = []
        for feature in SAMPLE_GEOJSON_RESPONSE["features"]:
            alert = poller.parse_alert(feature, "amazon")
            if alert:
                alerts.append(alert)

        assert len(alerts) == 2
        assert alerts[0].classname == "DESMATAMENTO_CR"
        assert alerts[0].alert_id == "91537_hist"
        assert alerts[1].classname == "DEGRADACAO"
        assert alerts[1].alert_id == "13558_curr"
