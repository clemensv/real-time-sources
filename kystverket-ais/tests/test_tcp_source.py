"""Tests for TCP source tag block parser."""

from datetime import datetime, timezone

from kystverket_ais.tcp_source import parse_tag_block


class TestParseTagBlock:
    def test_valid_sentence(self):
        line = r'\s:2573315,c:1775041133*08\!BSVDM,1,1,,B,13mnNa0P0dPUcCPT5L7mH?w`08OA,0*42'
        result = parse_tag_block(line)
        assert result is not None
        assert result.station_id == "2573315"
        assert result.nmea.startswith("!BSVDM")

    def test_timestamp_parsed(self):
        line = r'\s:2573315,c:1775041133*08\!BSVDM,1,1,,B,13mnNa0P0dPUcCPT5L7mH?w`08OA,0*42'
        result = parse_tag_block(line)
        assert result is not None
        assert result.receive_time.tzinfo == timezone.utc
        assert result.receive_time.year >= 2025

    def test_different_station(self):
        line = r'\s:2573565,c:1775041133*09\!BSVDM,1,1,,A,B3mAr1000HJF2i:63n0eWwrUoP06,0*34'
        result = parse_tag_block(line)
        assert result is not None
        assert result.station_id == "2573565"

    def test_invalid_no_tag_block(self):
        result = parse_tag_block("!BSVDM,1,1,,B,13mnNa0P,0*42")
        assert result is None

    def test_invalid_no_nmea(self):
        result = parse_tag_block(r'\s:2573315,c:1775041133*08\some_garbage')
        assert result is None

    def test_empty_string(self):
        result = parse_tag_block("")
        assert result is None
