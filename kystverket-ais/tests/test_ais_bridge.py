"""Tests for the AIS bridge event emission logic."""

from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

from kystverket_ais.ais_bridge import _emit_event, _mmsi_key_mapper, AISBridge
from kystverket_ais.nmea_decoder import DecodedAIS


RECV_TIME = datetime(2026, 4, 2, 7, 0, 0, tzinfo=timezone.utc)


def _make_decoded(event_type: str, msg_type: int, mmsi: int, fields: dict) -> DecodedAIS:
    return DecodedAIS(
        msg_type=msg_type,
        event_type=event_type,
        mmsi=mmsi,
        station_id="2573315",
        receive_time=RECV_TIME,
        fields=fields,
    )


class TestMmsiKeyMapper:
    def test_returns_mmsi_string(self):
        data = MagicMock()
        data.mmsi = 257000000
        result = _mmsi_key_mapper(None, data)
        assert result == "257000000"


class TestEmitEvent:
    def test_position_class_a(self):
        producer = MagicMock()
        fields = {
            "mmsi": 258028380, "navigation_status": 0, "rate_of_turn": 0.0,
            "speed_over_ground": 4.8, "position_accuracy": 1,
            "longitude": 10.94, "latitude": 59.21,
            "course_over_ground": 170.0, "true_heading": 170,
            "timestamp": "2026-04-02T07:00:00+00:00",
            "station_id": "2573315", "msg_type": 1,
        }
        decoded = _make_decoded("position_report_class_a", 1, 258028380, fields)
        _emit_event(producer, decoded)
        producer.send_no_kystverket_ais_position_report_class_a.assert_called_once()

    def test_static_voyage_data(self):
        producer = MagicMock()
        fields = {
            "mmsi": 258028380, "imo_number": 1234567, "callsign": "ABCD",
            "ship_name": "TEST", "ship_type": 70,
            "dimension_to_bow": 50, "dimension_to_stern": 20,
            "dimension_to_port": 10, "dimension_to_starboard": 10,
            "draught": 5.5, "destination": "BERGEN",
            "eta_month": 4, "eta_day": 2, "eta_hour": 12, "eta_minute": 0,
            "timestamp": "2026-04-02T07:00:00+00:00", "station_id": "2573315",
        }
        decoded = _make_decoded("static_voyage_data", 5, 258028380, fields)
        _emit_event(producer, decoded)
        producer.send_no_kystverket_ais_static_voyage_data.assert_called_once()

    def test_position_class_b(self):
        producer = MagicMock()
        fields = {
            "mmsi": 257079120, "speed_over_ground": 1.7, "position_accuracy": 0,
            "longitude": 17.52, "latitude": 68.85,
            "course_over_ground": 360.0, "true_heading": 241,
            "timestamp": "2026-04-02T07:00:00+00:00",
            "station_id": "2573515", "msg_type": 18,
        }
        decoded = _make_decoded("position_report_class_b", 18, 257079120, fields)
        _emit_event(producer, decoded)
        producer.send_no_kystverket_ais_position_report_class_b.assert_called_once()

    def test_static_data_class_b(self):
        producer = MagicMock()
        fields = {
            "mmsi": 257079120, "part_number": 0, "ship_name": "TEST",
            "ship_type": 37, "callsign": "", "dimension_to_bow": 0,
            "dimension_to_stern": 0, "dimension_to_port": 0,
            "dimension_to_starboard": 0,
            "timestamp": "2026-04-02T07:00:00+00:00", "station_id": "2573515",
        }
        decoded = _make_decoded("static_data_class_b", 24, 257079120, fields)
        _emit_event(producer, decoded)
        producer.send_no_kystverket_ais_static_data_class_b.assert_called_once()

    def test_aid_to_navigation(self):
        producer = MagicMock()
        fields = {
            "mmsi": 992651067, "aid_type": 3, "name": "PLATFORM",
            "position_accuracy": 1, "longitude": 11.9, "latitude": 57.69,
            "timestamp": "2026-04-02T07:00:00+00:00", "station_id": "2573115",
        }
        decoded = _make_decoded("aid_to_navigation", 21, 992651067, fields)
        _emit_event(producer, decoded)
        producer.send_no_kystverket_ais_aid_to_navigation.assert_called_once()


class TestAISBridgeFiltering:
    def test_mmsi_filter_blocks(self):
        """Bridge should skip messages not in the MMSI filter."""
        from kystverket_ais.tcp_source import RawNMEASentence
        tcp = MagicMock()
        kafka = MagicMock()
        event_prod = MagicMock()
        decoder = MagicMock()

        # Decoder returns a decoded message with MMSI not in filter
        decoded = _make_decoded("position_report_class_a", 1, 999999999, {"mmsi": 999999999})
        decoder.decode_sentence.return_value = decoded

        bridge = AISBridge(
            tcp_source=tcp,
            kafka_producer=kafka,
            event_producer=event_prod,
            decoder=decoder,
            mmsi_filter={258028380},  # Only allow this MMSI
        )

        sentence = RawNMEASentence(station_id="2573315", receive_time=RECV_TIME,
                                    nmea="!BSVDM,1,1,,B,test,0*00")
        bridge._on_sentence(sentence)

        # Event producer should NOT have been called
        assert event_prod.send_no_kystverket_ais_position_report_class_a.call_count == 0
