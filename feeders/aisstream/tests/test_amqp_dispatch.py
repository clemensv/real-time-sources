"""Tests for the AMQP transport adapter.

The AMQP bridge carries the same 23 raw AIS message types as Kafka and keys
each event by ``UserID`` (the vessel MMSI) — it performs **no** topic
enrichment. These tests assert the full 23-type dispatch table resolves to real
generated data classes / send methods, and that ``emit`` forwards the raw
decoded payload keyed by ``_user_id`` without leaking the MQTT topic args.
"""

import asyncio
from unittest.mock import MagicMock

from aisstream_core import AIS_MESSAGE_TYPES
from aisstream_amqp.app import _AMQP_DISPATCH, AisStreamAmqpClient
import aisstream_amqp_producer_data as _amqp_data


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

_SHIP_STATIC = {
    "MessageID": 5, "RepeatIndicator": 0, "UserID": 211555001,
    "Valid": True, "AisVersion": 2, "ImoNumber": 1234567,
    "CallSign": "ABCDEFG", "Name": "TEST VESSEL",
    "Type": 70,
    "Dimension": {"A": 50, "B": 20, "C": 10, "D": 10},
    "FixType": 1,
    "Eta": {"Month": 4, "Day": 2, "Hour": 12, "Minute": 0},
    "MaximumStaticDraught": 5.5, "Destination": "BERGEN",
    "Dte": False, "Spare": False,
}


class TestAmqpDispatchTable:
    def test_covers_all_23_types(self):
        assert set(_AMQP_DISPATCH) == {mt for mt, _ in AIS_MESSAGE_TYPES}
        assert len(_AMQP_DISPATCH) == 23

    def test_data_classes_and_send_methods_resolve(self):
        suffix_by_type = dict(AIS_MESSAGE_TYPES)
        for mt, (data_class, method_name) in _AMQP_DISPATCH.items():
            assert data_class is getattr(_amqp_data, mt)
            assert method_name == f"send_{suffix_by_type[mt]}"


class TestAmqpEmit:
    def test_keys_by_user_id_and_forwards_typed_payload(self):
        producer = MagicMock()
        client = AisStreamAmqpClient(producer)

        _run(client.emit(
            "PositionReport", _POSITION_REPORT,
            user_id=311000255, mmsi="311000255",
            flag="gb", ship_type="cargo", geohash5="abcde",
        ))

        producer.send_position_report.assert_called_once()
        call = producer.send_position_report.call_args
        assert call.kwargs["_user_id"] == "311000255"
        assert call.kwargs["data"].__class__.__name__ == "PositionReport"

    def test_does_not_leak_enrichment_topic_args(self):
        # AMQP mirrors Kafka keying: only the UserID matters. The MQTT topic
        # levels (mmsi/flag/ship_type/geohash5) must NOT reach the AMQP send.
        producer = MagicMock()
        client = AisStreamAmqpClient(producer)

        _run(client.emit(
            "ShipStaticData", _SHIP_STATIC,
            user_id=211555001, mmsi="211555001",
            flag="de", ship_type="cargo", geohash5="u1xyz",
        ))

        call = producer.send_ship_static_data.call_args
        assert set(call.kwargs) <= {"data", "_user_id"}
        for forbidden in ("mmsi", "flag", "ship_type", "geohash5"):
            assert forbidden not in call.kwargs

    def test_unknown_type_emits_nothing(self):
        producer = MagicMock()
        client = AisStreamAmqpClient(producer)

        _run(client.emit(
            "NonExistentType", {},
            user_id=1, mmsi="000000001",
            flag="xx", ship_type="unknown", geohash5="00000",
        ))

        assert producer.method_calls == []

    def test_undecodable_payload_is_skipped(self):
        producer = MagicMock()
        client = AisStreamAmqpClient(producer)

        # A payload the data class cannot decode must be dropped, not crash.
        _run(client.emit(
            "PositionReport", {"Longitude": object()},
            user_id=311000255, mmsi="311000255",
            flag="gb", ship_type="cargo", geohash5="abcde",
        ))

        producer.send_position_report.assert_not_called()
