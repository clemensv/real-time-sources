"""Tests for the CAP XML alert parser."""

from dwd.parsers.cap_parser import parse_cap_xml


SAMPLE_CAP = """\
<?xml version="1.0" encoding="UTF-8"?>
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.2">
  <identifier>2.49.0.0.276.0.DWD.PVW.1234567890.1</identifier>
  <sender>opendata@dwd.de</sender>
  <sent>2026-03-30T09:06:00-00:00</sent>
  <status>Actual</status>
  <msgType>Alert</msgType>
  <info>
    <language>de-DE</language>
    <event>FROST</event>
    <urgency>Immediate</urgency>
    <severity>Moderate</severity>
    <certainty>Likely</certainty>
    <headline>Amtliche WARNUNG vor FROST</headline>
    <description>Es tritt mäßiger Frost auf.</description>
    <effective>2026-03-30T18:00:00+01:00</effective>
    <onset>2026-03-30T20:00:00+01:00</onset>
    <expires>2026-03-31T10:00:00+01:00</expires>
    <area>
      <areaDesc>Kreis Ahrweiler</areaDesc>
      <geocode>
        <valueName>WARNCELLID</valueName>
        <value>807131000</value>
      </geocode>
    </area>
    <area>
      <areaDesc>Stadt Bonn</areaDesc>
      <geocode>
        <valueName>WARNCELLID</valueName>
        <value>805314000</value>
      </geocode>
    </area>
  </info>
</alert>
"""


class TestCapParser:
    def test_parses_single_alert(self):
        alerts = parse_cap_xml(SAMPLE_CAP)
        assert len(alerts) == 1

    def test_identifier(self):
        alerts = parse_cap_xml(SAMPLE_CAP)
        assert alerts[0]["identifier"] == "2.49.0.0.276.0.DWD.PVW.1234567890.1"

    def test_sender(self):
        alerts = parse_cap_xml(SAMPLE_CAP)
        assert alerts[0]["sender"] == "opendata@dwd.de"

    def test_severity(self):
        alerts = parse_cap_xml(SAMPLE_CAP)
        assert alerts[0]["severity"] == "Moderate"

    def test_event(self):
        alerts = parse_cap_xml(SAMPLE_CAP)
        assert alerts[0]["event"] == "FROST"

    def test_area_desc_joined(self):
        alerts = parse_cap_xml(SAMPLE_CAP)
        assert "Kreis Ahrweiler" in alerts[0]["area_desc"]
        assert "Stadt Bonn" in alerts[0]["area_desc"]

    def test_geocodes(self):
        alerts = parse_cap_xml(SAMPLE_CAP)
        import json
        geocodes = json.loads(alerts[0]["geocodes"])
        # Only the last WARNCELLID is kept (same key)
        assert "WARNCELLID" in geocodes

    def test_headline(self):
        alerts = parse_cap_xml(SAMPLE_CAP)
        assert "FROST" in alerts[0]["headline"]

    def test_empty_input(self):
        alerts = parse_cap_xml("")
        assert alerts == []

    def test_invalid_xml(self):
        alerts = parse_cap_xml("<not-cap>broken</not-cap>")
        assert alerts == []
