"""Tests for the AISstream bridge event emission and message handling."""

from unittest.mock import MagicMock, patch

from aisstream.ais_bridge import (
    _emit_event, _mmsi_key_mapper, _parse_bounding_boxes, AISBridge,
)


class TestMmsiKeyMapper:
    def test_returns_user_id_string(self):
        data = MagicMock()
        data.UserID = 311000255
        result = _mmsi_key_mapper(None, data)
        assert result == "311000255"


class TestParseBoundingBoxes:
    def test_single_global(self):
        result = _parse_bounding_boxes("-90,-180,90,180")
        assert result == [[[-90.0, -180.0], [90.0, 180.0]]]

    def test_multiple_boxes(self):
        result = _parse_bounding_boxes("50,-10,60,5;30,120,40,140")
        assert len(result) == 2
        assert result[0] == [[50.0, -10.0], [60.0, 5.0]]
        assert result[1] == [[30.0, 120.0], [40.0, 140.0]]

    def test_invalid_raises(self):
        import pytest
        with pytest.raises(ValueError):
            _parse_bounding_boxes("1,2,3")


class TestEmitEvent:
    def test_position_report(self):
        producer = MagicMock()
        payload = {
            "MessageID": 1, "RepeatIndicator": 0, "UserID": 311000255,
            "Valid": True, "NavigationalStatus": 0, "RateOfTurn": 0,
            "Sog": 14.9, "PositionAccuracy": True,
            "Longitude": -45.678, "Latitude": 12.345,
            "Cog": 260.5, "TrueHeading": 261, "Timestamp": 30,
            "SpecialManoeuvreIndicator": 0, "Spare": 0,
            "Raim": False, "CommunicationState": 0,
        }
        result = _emit_event(producer, "PositionReport", payload)
        assert result is True
        producer.send_io_aisstream_position_report.assert_called_once()

    def test_position_report_passes_mmsi_placeholder(self):
        producer = MagicMock()
        payload = {
            "MessageID": 1, "RepeatIndicator": 0, "UserID": 311000255,
            "Valid": True, "NavigationalStatus": 0, "RateOfTurn": 0,
            "Sog": 14.9, "PositionAccuracy": True,
            "Longitude": -45.678, "Latitude": 12.345,
            "Cog": 260.5, "TrueHeading": 261, "Timestamp": 30,
            "SpecialManoeuvreIndicator": 0, "Spare": 0,
            "Raim": False, "CommunicationState": 0,
        }

        _emit_event(producer, "PositionReport", payload)

        call = producer.send_io_aisstream_position_report.call_args
        assert call.kwargs["_mmsi"] == "311000255"
        assert call.kwargs["flush_producer"] is False
        assert call.kwargs["key_mapper"] is _mmsi_key_mapper

    def test_ship_static_data(self):
        producer = MagicMock()
        payload = {
            "MessageID": 5, "RepeatIndicator": 0, "UserID": 311000255,
            "Valid": True, "AisVersion": 2, "ImoNumber": 1234567,
            "CallSign": "ABCDEFG", "Name": "TEST VESSEL",
            "Type": 70,
            "Dimension": {"A": 50, "B": 20, "C": 10, "D": 10},
            "FixType": 1,
            "Eta": {"Month": 4, "Day": 2, "Hour": 12, "Minute": 0},
            "MaximumStaticDraught": 5.5, "Destination": "BERGEN",
            "Dte": False, "Spare": False,
        }
        result = _emit_event(producer, "ShipStaticData", payload)
        assert result is True
        producer.send_io_aisstream_ship_static_data.assert_called_once()

    def test_standard_class_b(self):
        producer = MagicMock()
        payload = {
            "MessageID": 18, "RepeatIndicator": 0, "UserID": 257079120,
            "Valid": True, "Spare1": 0, "Sog": 1.7,
            "PositionAccuracy": False,
            "Longitude": 17.52, "Latitude": 68.85,
            "Cog": 360.0, "TrueHeading": 241, "Timestamp": 15,
            "Spare2": 0, "ClassBUnit": True, "ClassBDisplay": False,
            "ClassBDsc": True, "ClassBBand": True, "ClassBMsg22": False,
            "AssignedMode": False, "Raim": False,
            "CommunicationStateIsItdma": True, "CommunicationState": 0,
        }
        result = _emit_event(producer, "StandardClassBPositionReport", payload)
        assert result is True
        producer.send_io_aisstream_standard_class_bposition_report.assert_called_once()

    def test_safety_broadcast(self):
        producer = MagicMock()
        payload = {
            "MessageID": 14, "RepeatIndicator": 0, "UserID": 2190001,
            "Valid": True, "Spare": 0, "Text": "STORM WARNING",
        }
        result = _emit_event(producer, "SafetyBroadcastMessage", payload)
        assert result is True
        producer.send_io_aisstream_safety_broadcast_message.assert_called_once()

    def test_unknown_type_returns_false(self):
        producer = MagicMock()
        result = _emit_event(producer, "NonExistentType", {})
        assert result is False

    def test_all_23_types_have_mappings(self):
        from aisstream.ais_bridge import _MESSAGE_MAP
        expected_types = {
            "PositionReport", "ShipStaticData", "StandardClassBPositionReport",
            "ExtendedClassBPositionReport", "AidsToNavigationReport",
            "StaticDataReport", "BaseStationReport", "SafetyBroadcastMessage",
            "StandardSearchAndRescueAircraftReport", "LongRangeAisBroadcastMessage",
            "AddressedSafetyMessage", "AddressedBinaryMessage",
            "AssignedModeCommand", "BinaryAcknowledge", "BinaryBroadcastMessage",
            "ChannelManagement", "CoordinatedUTCInquiry",
            "DataLinkManagementMessage", "GnssBroadcastBinaryMessage",
            "GroupAssignmentCommand", "Interrogation",
            "MultiSlotBinaryMessage", "SingleSlotBinaryMessage",
        }
        assert set(_MESSAGE_MAP.keys()) == expected_types


class TestAISBridgeFiltering:
    def test_mmsi_filter_blocks(self):
        ws = MagicMock()
        kafka = MagicMock()
        event_prod = MagicMock()

        bridge = AISBridge(
            ws_source=ws,
            kafka_producer=kafka,
            event_producer=event_prod,
            mmsi_filter={"311000255"},
        )

        # Message with MMSI not in filter
        msg = {
            "MessageType": "PositionReport",
            "MetaData": {"MMSI": 999999999},
            "Message": {
                "PositionReport": {
                    "MessageID": 1, "RepeatIndicator": 0, "UserID": 999999999,
                    "Valid": True, "NavigationalStatus": 0, "RateOfTurn": 0,
                    "Sog": 0, "PositionAccuracy": False,
                    "Longitude": 0, "Latitude": 0,
                    "Cog": 0, "TrueHeading": 0, "Timestamp": 0,
                    "SpecialManoeuvreIndicator": 0, "Spare": 0,
                    "Raim": False, "CommunicationState": 0,
                }
            },
        }
        bridge._on_message(msg)
        assert event_prod.send_io_aisstream_position_report.call_count == 0

    def test_mmsi_filter_allows(self):
        ws = MagicMock()
        kafka = MagicMock()
        event_prod = MagicMock()

        bridge = AISBridge(
            ws_source=ws,
            kafka_producer=kafka,
            event_producer=event_prod,
            mmsi_filter={"311000255"},
        )

        msg = {
            "MessageType": "PositionReport",
            "MetaData": {"MMSI": 311000255},
            "Message": {
                "PositionReport": {
                    "MessageID": 1, "RepeatIndicator": 0, "UserID": 311000255,
                    "Valid": True, "NavigationalStatus": 0, "RateOfTurn": 0,
                    "Sog": 14.9, "PositionAccuracy": True,
                    "Longitude": -45.678, "Latitude": 12.345,
                    "Cog": 260.5, "TrueHeading": 261, "Timestamp": 30,
                    "SpecialManoeuvreIndicator": 0, "Spare": 0,
                    "Raim": False, "CommunicationState": 0,
                }
            },
        }
        bridge._on_message(msg)
        event_prod.send_io_aisstream_position_report.assert_called_once()
