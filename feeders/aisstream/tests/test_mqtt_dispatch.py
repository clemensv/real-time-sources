"""Tests for the MQTT/UNS transport adapter.

The MQTT bridge carries the same 23 raw AIS message types as Kafka, but
publishes each to a rich Unified-Namespace topic whose levels
(``flag``/``ship_type``/``geohash5``/``mmsi``) the bridge computes per message.
These tests assert the full 23-type dispatch table resolves to real generated
data classes / publish methods, and that ``emit`` forwards the raw decoded
payload together with the enrichment topic args.
"""

import asyncio
from unittest.mock import AsyncMock

from aisstream_core import AIS_MESSAGE_TYPES
from aisstream_mqtt.app import _MQTT_DISPATCH, AisStreamMqttClient
import aisstream_mqtt_producer_data as _mqtt_data


def _run(coro):
    return asyncio.run(coro)


_POSITION_REPORT = {
    "MessageID": 1, "RepeatIndicator": 0, "UserID": 311000255,
    "Valid": True, "NavigationalStatus": 0, "RateOfTurn": 0,
    "Sog": 14.9, "PositionAccuracy": True,
    "Longitude": -45.678, "Latitude": 12.345,
    "Cog": 260.5, "TrueHeading": 261, "Timestamp": 30,
    "SpecialManoeuvreIndicator": 0, "Spare": 0,
    "Raim": False, "CommunicationState": 0,
}


class TestMqttDispatchTable:
    def test_covers_all_23_types(self):
        assert set(_MQTT_DISPATCH) == {mt for mt, _ in AIS_MESSAGE_TYPES}
        assert len(_MQTT_DISPATCH) == 23

    def test_data_classes_and_publish_methods_resolve(self):
        suffix_by_type = dict(AIS_MESSAGE_TYPES)
        for mt, (data_class, method_name) in _MQTT_DISPATCH.items():
            assert data_class is getattr(_mqtt_data, mt)
            assert method_name == f"publish_io_aisstream_mqtt_{suffix_by_type[mt]}"


class TestMqttEmit:
    def test_forwards_enrichment_topic_args_and_typed_payload(self):
        client_mock = AsyncMock()
        client = AisStreamMqttClient(client_mock)

        _run(client.emit(
            "PositionReport", _POSITION_REPORT,
            user_id=311000255, mmsi="311000255",
            flag="gb", ship_type="cargo", geohash5="abcde",
        ))

        method = client_mock.publish_io_aisstream_mqtt_position_report
        method.assert_awaited_once()
        call = method.await_args
        assert call.kwargs["mmsi"] == "311000255"
        assert call.kwargs["flag"] == "gb"
        assert call.kwargs["ship_type"] == "cargo"
        assert call.kwargs["geohash5"] == "abcde"
        assert call.kwargs["data"].__class__.__name__ == "PositionReport"
        assert call.kwargs["qos"] == 0
        assert call.kwargs["retain"] is False

    def test_unknown_type_publishes_nothing(self):
        client_mock = AsyncMock()
        client = AisStreamMqttClient(client_mock)

        _run(client.emit(
            "NonExistentType", {},
            user_id=1, mmsi="000000001",
            flag="xx", ship_type="unknown", geohash5="00000",
        ))

        assert client_mock.mock_calls == []

    def test_undecodable_payload_is_skipped(self):
        client_mock = AsyncMock()
        client = AisStreamMqttClient(client_mock)

        _run(client.emit(
            "PositionReport", {"Longitude": object()},
            user_id=311000255, mmsi="311000255",
            flag="gb", ship_type="cargo", geohash5="abcde",
        ))

        client_mock.publish_io_aisstream_mqtt_position_report.assert_not_awaited()
