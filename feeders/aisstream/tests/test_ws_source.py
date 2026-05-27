"""Tests for the WebSocket source."""

import json
from unittest.mock import MagicMock, patch

from aisstream.ws_source import WebSocketSource, AISSTREAM_WS_URL


class TestSubscriptionBuilding:
    def test_global_default(self):
        ws = WebSocketSource(api_key="test-key")
        sub = json.loads(ws._build_subscription())
        assert sub["APIKey"] == "test-key"
        assert sub["BoundingBoxes"] == [[[-90, -180], [90, 180]]]
        assert "FiltersShipMMSI" not in sub
        assert "FilterMessageTypes" not in sub

    def test_with_mmsi_filter(self):
        ws = WebSocketSource(
            api_key="test-key",
            mmsi_filter=["311000255", "258028380"],
        )
        sub = json.loads(ws._build_subscription())
        assert sub["FiltersShipMMSI"] == ["311000255", "258028380"]

    def test_with_message_type_filter(self):
        ws = WebSocketSource(
            api_key="test-key",
            message_type_filter=["PositionReport", "ShipStaticData"],
        )
        sub = json.loads(ws._build_subscription())
        assert sub["FilterMessageTypes"] == ["PositionReport", "ShipStaticData"]

    def test_custom_bounding_boxes(self):
        ws = WebSocketSource(
            api_key="test-key",
            bounding_boxes=[[[50, -10], [60, 5]], [[30, 120], [40, 140]]],
        )
        sub = json.loads(ws._build_subscription())
        assert len(sub["BoundingBoxes"]) == 2

    def test_default_url(self):
        ws = WebSocketSource(api_key="test-key")
        assert ws.url == AISSTREAM_WS_URL
