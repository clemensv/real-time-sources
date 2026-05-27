"""
End-to-end tests for INPE DETER Brazil deforestation alert poller.
These tests call the real INPE DETER WFS API.
Run with: pytest tests/test_inpe_deter_brazil_e2e.py -m e2e
"""

import pytest
from inpe_deter_brazil.inpe_deter_brazil import INPEDeterPoller, WFS_ENDPOINTS


@pytest.mark.e2e
class TestLiveAPI:
    """Tests that call the real INPE DETER WFS API."""

    @pytest.mark.asyncio
    async def test_fetch_amazon_alerts(self):
        """Test fetching Amazon alerts from the live API."""
        poller = INPEDeterPoller(page_size=5)
        features = await poller.fetch_biome("amazon", since_date="2026-01-01")

        assert isinstance(features, list)
        for feature in features:
            assert "properties" in feature
            assert "geometry" in feature

    @pytest.mark.asyncio
    async def test_fetch_cerrado_alerts(self):
        """Test fetching Cerrado alerts from the live API."""
        poller = INPEDeterPoller(page_size=5)
        features = await poller.fetch_biome("cerrado")

        assert isinstance(features, list)
        assert len(features) > 0, "Expected at least one Cerrado alert"

    @pytest.mark.asyncio
    async def test_fetch_and_parse_amazon_alerts(self):
        """Test fetching and parsing Amazon alerts from the live API."""
        poller = INPEDeterPoller(page_size=5)
        features = await poller.fetch_biome("amazon", since_date="2026-01-01")

        alerts = []
        for feature in features:
            alert = poller.parse_alert(feature, "amazon")
            if alert:
                alerts.append(alert)

        assert len(alerts) > 0, "Expected at least one parseable Amazon alert"
        alert = alerts[0]
        assert alert.alert_id
        assert alert.biome == "amazon"
        assert alert.view_date
        assert isinstance(alert.centroid_latitude, float)
        assert isinstance(alert.centroid_longitude, float)

    @pytest.mark.asyncio
    async def test_alert_serialization_roundtrip(self):
        """Test that live alerts can be serialized to JSON and Avro."""
        poller = INPEDeterPoller(page_size=3)
        features = await poller.fetch_biome("cerrado")
        assert len(features) > 0

        alert = poller.parse_alert(features[0], "cerrado")
        assert alert is not None

        json_bytes = alert.to_byte_array("application/json")
        assert json_bytes is not None
        assert len(json_bytes) > 0

        avro_bytes = alert.to_byte_array("avro/binary")
        assert avro_bytes is not None
        assert len(avro_bytes) > 0
