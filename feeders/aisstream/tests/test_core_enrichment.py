"""Tests for the shared AISstream core: enrichment, Type-24 ship-type
extraction, cross-message caching, and the synthetic mock corpus.

These exercise ``AisStreamBridge.handle_envelope`` / ``_enrich`` — the
transport-neutral logic that the Kafka, AMQP, and MQTT apps all drive — through
a capturing fake client, so no real producer or broker is required.
"""

import asyncio

from aisstream_core import (
    AIS_MESSAGE_TYPES,
    AisStreamBridge,
    extract_ship_type_code,
    mock_envelopes,
)


def _run(coro):
    return asyncio.run(coro)


class _CapturingClient:
    """Records every ``emit`` call so tests can assert on the routing tuple."""

    def __init__(self):
        self.calls = []

    async def emit(self, message_type, payload, *, user_id, mmsi, flag, ship_type, geohash5):
        self.calls.append({
            "message_type": message_type,
            "payload": payload,
            "user_id": user_id,
            "mmsi": mmsi,
            "flag": flag,
            "ship_type": ship_type,
            "geohash5": geohash5,
        })


class TestExtractShipTypeCode:
    def test_top_level_type(self):
        assert extract_ship_type_code({"Type": 70}) == 70

    def test_top_level_ship_type(self):
        assert extract_ship_type_code({"ShipType": 80}) == 80

    def test_reportb_ship_type_type24(self):
        # Type-24 StaticDataReport Part B nests the code under ReportB.ShipType;
        # reading only the top level would mislabel every Class-B vessel.
        assert extract_ship_type_code({"ReportB": {"ShipType": 70}}) == 70

    def test_reportb_type_fallback(self):
        assert extract_ship_type_code({"ReportB": {"Type": 60}}) == 60

    def test_top_level_wins_over_reportb(self):
        assert extract_ship_type_code({"Type": 80, "ReportB": {"ShipType": 70}}) == 80

    def test_empty_returns_zero(self):
        assert extract_ship_type_code({}) == 0


class TestEnrichmentThroughHandleEnvelope:
    def test_ship_static_sets_flag_and_ship_type(self):
        client = _CapturingClient()
        bridge = AisStreamBridge(client)
        _run(bridge.handle_envelope(mock_envelopes()[0]))  # ShipStaticData, Type 70

        (call,) = client.calls
        assert call["message_type"] == "ShipStaticData"
        assert call["user_id"] == 211_555_001
        assert call["mmsi"] == "211555001"
        assert call["flag"] == "de"          # MID 211 -> Germany
        assert call["ship_type"] == "cargo"  # Type 70 bucket
        # A Type-5 static message carries no position and no prior fix is
        # cached yet, so the geohash level falls back to the placeholder.
        assert call["geohash5"] == "00000"

    def test_position_inherits_ship_type_from_cached_static(self):
        # A PositionReport carries no ship type; after a static message for the
        # same MMSI the bridge must inherit the cached bucket (cross-message).
        client = _CapturingClient()
        bridge = AisStreamBridge(client)
        static_env, position_env, _ = mock_envelopes()
        _run(bridge.handle_envelope(static_env))
        _run(bridge.handle_envelope(position_env))

        position_call = client.calls[1]
        assert position_call["message_type"] == "PositionReport"
        assert position_call["ship_type"] == "cargo"   # inherited from cache
        assert position_call["geohash5"] != "00000"

    def test_aids_to_navigation_ship_type_is_aton(self):
        client = _CapturingClient()
        bridge = AisStreamBridge(client)
        _run(bridge.handle_envelope(mock_envelopes()[2]))  # AidsToNavigationReport

        (call,) = client.calls
        assert call["message_type"] == "AidsToNavigationReport"
        assert call["ship_type"] == "aton"

    def test_static_data_report_uses_reportb_ship_type(self):
        # Type-24 routing: ship_type must come from ReportB.ShipType, not the
        # (absent) top-level Type, otherwise Class-B vessels route as unknown.
        client = _CapturingClient()
        bridge = AisStreamBridge(client)
        env = {
            "MessageType": "StaticDataReport",
            "MetaData": {"MMSI": 244_000_001},
            "Message": {
                "StaticDataReport": {
                    "MessageID": 24, "RepeatIndicator": 0, "UserID": 244_000_001,
                    "Valid": True, "PartNumber": 1,
                    "ReportB": {"ShipType": 70, "CallSign": "AB1@@@@"},
                }
            },
        }
        _run(bridge.handle_envelope(env))

        (call,) = client.calls
        assert call["ship_type"] == "cargo"  # from ReportB.ShipType=70
        assert call["flag"] == "nl"          # MID 244 -> Netherlands

    def test_envelope_without_mmsi_is_dropped(self):
        client = _CapturingClient()
        bridge = AisStreamBridge(client)
        env = {
            "MessageType": "PositionReport",
            "MetaData": {},
            "Message": {"PositionReport": {"MessageID": 1, "Valid": True}},
        }
        _run(bridge.handle_envelope(env))
        assert client.calls == []

    def test_unknown_envelope_shape_is_dropped(self):
        client = _CapturingClient()
        bridge = AisStreamBridge(client)
        _run(bridge.handle_envelope({"MessageType": None, "Message": {}}))
        assert client.calls == []


class TestMockCorpus:
    def test_mock_envelopes_shape(self):
        envs = mock_envelopes()
        assert [e["MessageType"] for e in envs] == [
            "ShipStaticData", "PositionReport", "AidsToNavigationReport",
        ]
        for env in envs:
            assert "MetaData" in env and "Message" in env
            assert isinstance(next(iter(env["Message"].values())), dict)

    def test_message_types_table_has_23_unique_entries(self):
        names = [mt for mt, _ in AIS_MESSAGE_TYPES]
        suffixes = [suffix for _, suffix in AIS_MESSAGE_TYPES]
        assert len(names) == 23
        assert len(set(names)) == 23
        assert len(set(suffixes)) == 23
