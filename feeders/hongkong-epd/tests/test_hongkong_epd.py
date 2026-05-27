"""Unit tests for the Hong Kong EPD AQHI bridge."""

from unittest.mock import MagicMock, patch

from hongkong_epd.hongkong_epd import (
    HKEPDAQHIAPI,
    aqhi_to_health_risk,
    feed_readings,
    parse_connection_string,
    send_stations,
)


SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<AQHI24HrReport>
  <lastBuildDate>Wed, 08 Apr 2026 18:30:00 +0800</lastBuildDate>
  <item>
    <type>General Stations</type>
    <StationName>Central/Western</StationName>
    <DateTime>Wed, 08 Apr 2026 17:00:00 +0800</DateTime>
    <aqhi>4</aqhi>
  </item>
  <item>
    <type>General Stations</type>
    <StationName>Central/Western</StationName>
    <DateTime>Wed, 08 Apr 2026 18:00:00 +0800</DateTime>
    <aqhi>5</aqhi>
  </item>
  <item>
    <type>Roadside Stations</type>
    <StationName>Mong Kok</StationName>
    <DateTime>Wed, 08 Apr 2026 18:00:00 +0800</DateTime>
    <aqhi>8</aqhi>
  </item>
</AQHI24HrReport>
"""


class TestAQHICategory:
    def test_health_risk_mapping(self):
        assert aqhi_to_health_risk(2) == "Low"
        assert aqhi_to_health_risk(6) == "Moderate"
        assert aqhi_to_health_risk(7) == "High"
        assert aqhi_to_health_risk(9) == "Very High"
        assert aqhi_to_health_risk(11) == "Serious"


class TestHKEPDAQHIAPI:
    def test_get_stations_returns_reference_data(self):
        api = HKEPDAQHIAPI()
        stations = api.get_stations()

        assert len(stations) == 18
        assert stations["central_western"].station_type == "General Stations"
        assert stations["mong_kok"].station_type == "Roadside Stations"

    def test_get_latest_readings_uses_latest_per_station(self):
        api = HKEPDAQHIAPI()
        with patch.object(api, "get_feed_xml", return_value=SAMPLE_XML):
            readings = api.get_latest_readings()

        assert set(readings.keys()) == {"central_western", "mong_kok"}
        assert readings["central_western"].aqhi == 5
        assert readings["central_western"].health_risk_category == "Moderate"
        assert readings["mong_kok"].health_risk_category == "Very High"


class TestConnectionString:
    def test_parse_plain_bootstrap(self):
        config = parse_connection_string("BootstrapServer=localhost:9092;EntityPath=aqhi")
        assert config["bootstrap.servers"] == "localhost:9092"
        assert config["_entity_path"] == "aqhi"


class TestStationEmission:
    def test_send_stations_emits_all_reference_events(self):
        api = HKEPDAQHIAPI()
        producer = MagicMock()
        producer.producer = MagicMock()

        count = send_stations(api, producer)

        assert count == 18
        assert producer.send_hk_gov_epd_aqhi_station.call_count == 18


class TestReadingEmission:
    def test_feed_readings_emits_latest_events(self):
        api = HKEPDAQHIAPI()
        producer = MagicMock()
        producer.producer = MagicMock()
        previous = {}

        with patch.object(api, "get_feed_xml", return_value=SAMPLE_XML):
            count = feed_readings(api, producer, previous)

        assert count == 2
        assert len(previous) == 2
        assert producer.send_hk_gov_epd_aqhi_aqhireading.call_count == 2

    def test_feed_readings_deduplicates(self):
        api = HKEPDAQHIAPI()
        producer = MagicMock()
        producer.producer = MagicMock()
        previous = {
            "central_western:2026-04-08T18:00:00+08:00": "2026-04-08T18:00:00+08:00",
            "mong_kok:2026-04-08T18:00:00+08:00": "2026-04-08T18:00:00+08:00",
        }

        with patch.object(api, "get_feed_xml", return_value=SAMPLE_XML):
            count = feed_readings(api, producer, previous)

        assert count == 0
