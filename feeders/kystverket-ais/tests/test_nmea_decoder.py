"""Tests for the NMEA AIS decoder."""

from datetime import datetime, timezone

from kystverket_ais.nmea_decoder import NMEADecoder, SUPPORTED_TYPES


# Real NMEA sentences captured from Kystverket stream
POSITION_TYPE1 = "!BSVDM,1,1,,B,13mnNa0P0dPUcCPT5L7mH?w`08OA,0*42"
POSITION_TYPE3 = "!BSVDM,1,1,,A,33aEOj@P00PBl;`Gk5URBL040000,0*79"
POSITION_TYPE18 = "!BSVDM,1,1,,A,B3mAr1000HJF2i:63n0eWwrUoP06,0*34"

# Multi-sentence type 5 (static and voyage)
STATIC_VOYAGE_PART1 = "!BSVDM,2,1,3,B,55?MbV02>EKjl4<H220l4r:0EQ18622222222220l1@E822t40Ht50,0*10"
STATIC_VOYAGE_PART2 = "!BSVDM,2,2,3,B,00000000000,2*26"

STATION = "2573315"
RECV_TIME = datetime(2026, 4, 2, 7, 0, 0, tzinfo=timezone.utc)


class TestSingleSentenceDecode:
    def test_decode_type1_position(self):
        decoder = NMEADecoder()
        result = decoder.decode_sentence(POSITION_TYPE1, STATION, RECV_TIME)
        assert result is not None
        assert result.event_type == "position_report_class_a"
        assert result.msg_type in (1, 2, 3)
        assert result.mmsi > 0
        assert result.station_id == STATION

    def test_position_a_fields(self):
        decoder = NMEADecoder()
        result = decoder.decode_sentence(POSITION_TYPE1, STATION, RECV_TIME)
        assert result is not None
        f = result.fields
        assert "mmsi" in f
        assert "longitude" in f
        assert "latitude" in f
        assert "speed_over_ground" in f
        assert "course_over_ground" in f
        assert "true_heading" in f
        assert "navigation_status" in f
        assert "timestamp" in f
        assert "station_id" in f
        assert "msg_type" in f

    def test_decode_type18_class_b(self):
        decoder = NMEADecoder()
        result = decoder.decode_sentence(POSITION_TYPE18, STATION, RECV_TIME)
        assert result is not None
        assert result.event_type == "position_report_class_b"
        assert result.msg_type == 18

    def test_class_b_fields(self):
        decoder = NMEADecoder()
        result = decoder.decode_sentence(POSITION_TYPE18, STATION, RECV_TIME)
        assert result is not None
        f = result.fields
        assert "mmsi" in f
        assert "longitude" in f
        assert "latitude" in f
        assert "speed_over_ground" in f
        assert "msg_type" in f

    def test_unsupported_type_filtered(self):
        # Only accept type 5
        decoder = NMEADecoder(message_types={5})
        result = decoder.decode_sentence(POSITION_TYPE1, STATION, RECV_TIME)
        assert result is None

    def test_invalid_nmea(self):
        decoder = NMEADecoder()
        result = decoder.decode_sentence("not_valid_nmea", STATION, RECV_TIME)
        assert result is None

    def test_too_few_parts(self):
        decoder = NMEADecoder()
        result = decoder.decode_sentence("!BSVDM,1,1", STATION, RECV_TIME)
        assert result is None


class TestMultiSentenceDecode:
    def test_type5_reassembly(self):
        decoder = NMEADecoder()
        # First fragment should return None (buffering)
        result1 = decoder.decode_sentence(STATIC_VOYAGE_PART1, STATION, RECV_TIME)
        assert result1 is None
        # Second fragment completes the message
        result2 = decoder.decode_sentence(STATIC_VOYAGE_PART2, STATION, RECV_TIME)
        assert result2 is not None
        assert result2.event_type == "static_voyage_data"
        assert result2.msg_type == 5

    def test_type5_fields(self):
        decoder = NMEADecoder()
        decoder.decode_sentence(STATIC_VOYAGE_PART1, STATION, RECV_TIME)
        result = decoder.decode_sentence(STATIC_VOYAGE_PART2, STATION, RECV_TIME)
        assert result is not None
        f = result.fields
        assert "mmsi" in f
        assert "imo_number" in f
        assert "ship_name" in f
        assert "ship_type" in f
        assert "draught" in f
        assert "destination" in f

    def test_orphan_fragment_ignored(self):
        """Second fragment without first should return None."""
        decoder = NMEADecoder()
        result = decoder.decode_sentence(STATIC_VOYAGE_PART2, STATION, RECV_TIME)
        assert result is None


class TestTimestampAndStation:
    def test_timestamp_iso_format(self):
        decoder = NMEADecoder()
        result = decoder.decode_sentence(POSITION_TYPE1, STATION, RECV_TIME)
        assert result is not None
        assert result.fields["timestamp"] == "2026-04-02T07:00:00+00:00"

    def test_station_propagated(self):
        decoder = NMEADecoder()
        result = decoder.decode_sentence(POSITION_TYPE1, "9999999", RECV_TIME)
        assert result is not None
        assert result.fields["station_id"] == "9999999"
        assert result.station_id == "9999999"
