"""Tests for PTWC Tsunami bridge."""

import asyncio
import json
import os
import tempfile
import xml.etree.ElementTree as ET
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from ptwc_tsunami.ptwc_tsunami import (
    PTWCTsunamiPoller,
    _get_summary_html,
    _parse_note,
    _parse_summary_field,
    _safe_str,
    _text,
    parse_connection_string,
    parse_entry,
)


# --- sample atom XML ---

SAMPLE_FEED_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#"
      xmlns:georss="http://www.georss.org/georss">
  <id>urn:uuid:2d946d30-d375-4d4f-bc16-e260cc4c2bb2</id>
  <title>Tsunami Information Statement Number 1</title>
  <updated>2026-04-03T08:28:39Z</updated>
  <author>
    <name>NWS National Tsunami Warning Center Palmer AK</name>
    <uri>https://www.tsunami.gov/</uri>
    <email>ntwc@noaa.gov</email>
  </author>
  <entry>
    <title>60 miles SW of Buldir I., Alaska</title>
    <updated>2026-04-03T08:28:39Z</updated>
    <geo:lat>51.610</geo:lat>
    <geo:long>174.990</geo:long>
    <summary type="xhtml"><div xmlns="http://www.w3.org/1999/xhtml">
      <strong>Category:</strong> Information<br/>
      <strong>Bulletin Issue Time: </strong> 2026.04.03 08:28:39 UTC <br/>
      <strong>Preliminary Magnitude: </strong>5.2(mb)<br/>
      <strong>Lat/Lon: </strong>51.610 / 174.990<br/>
      <strong>Affected Region: </strong>60 miles SW of Buldir I., Alaska<br/>
      <b>Note:</b>  * There is NO tsunami danger from this earthquake.<br/>
      <strong>Definition: </strong>An information statement indicates that an earthquake has occurred.
      <a href="https://www.tsunami.gov/events/PAAQ/2026/04/03/tcwskp/1/WEAK53/WEAK53.txt">View bulletin</a>
    </div></summary>
    <id>urn:uuid:7a6b0584-8201-4ef6-aac6-e512d77cbfb9</id>
    <link rel="related" title="CapXML document"
          href="https://www.tsunami.gov/events/PAAQ/2026/04/03/tcwskp/1/WEAK53/PAAQCAP.xml"
          type="application/cap+xml" />
    <link rel="alternate" title="Bulletin"
          href="https://www.tsunami.gov/events/PAAQ/2026/04/03/tcwskp/1/WEAK53/WEAK53.txt"
          type="application/xml" />
  </entry>
</feed>
"""

SAMPLE_EMPTY_FEED_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
  <id>urn:uuid:f1887553-cd57-4739-81e9-8aba3ae6fc96</id>
  <title>TSUNAMI MESSAGE NUMBER 7</title>
  <updated>2026-04-02T01:11:18Z</updated>
  <author>
    <name>NWS PACIFIC TSUNAMI WARNING CENTER HONOLULU HI</name>
  </author>
</feed>
"""


def _parse_sample_entry():
    """Parse the sample feed and return the first entry element."""
    root = ET.fromstring(SAMPLE_FEED_XML)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    return root.findall("atom:entry", ns)[0]


# --- _safe_str ---

class TestSafeStr:
    def test_none(self):
        assert _safe_str(None) is None

    def test_empty(self):
        assert _safe_str("") is None

    def test_whitespace(self):
        assert _safe_str("  ") is None

    def test_value(self):
        assert _safe_str("hello") == "hello"

    def test_strips(self):
        assert _safe_str("  hello  ") == "hello"


# --- _text ---

class TestText:
    def test_none_element(self):
        assert _text(None) is None

    def test_element_no_text(self):
        el = ET.Element("test")
        assert _text(el) is None

    def test_element_text(self):
        el = ET.Element("test")
        el.text = "  hello  "
        assert _text(el) == "hello"


# --- _parse_summary_field ---

class TestParseSummaryField:
    SUMMARY = (
        '<strong>Category:</strong> Information<br/>'
        '<strong>Preliminary Magnitude: </strong>5.2(mb)<br/>'
        '<strong>Affected Region: </strong>60 miles SW<br/>'
    )

    def test_category(self):
        assert _parse_summary_field(self.SUMMARY, "Category") == "Information"

    def test_magnitude(self):
        assert _parse_summary_field(self.SUMMARY, "Preliminary Magnitude") == "5.2(mb)"

    def test_affected_region(self):
        assert _parse_summary_field(self.SUMMARY, "Affected Region") == "60 miles SW"

    def test_not_found(self):
        assert _parse_summary_field(self.SUMMARY, "Nonexistent") is None

    def test_empty_html(self):
        assert _parse_summary_field("", "Category") is None


# --- _parse_note ---

class TestParseNote:
    def test_found(self):
        html = '<b>Note:</b>  * There is NO tsunami danger.<br/>'
        result = _parse_note(html)
        assert result is not None
        assert "NO tsunami danger" in result

    def test_not_found(self):
        assert _parse_note('<strong>Category:</strong> Info<br/>') is None

    def test_empty(self):
        assert _parse_note("") is None


# --- parse_entry ---

class TestParseEntry:
    def test_basic(self):
        entry = _parse_sample_entry()
        b = parse_entry(entry, "PAAQ", "NWS National Tsunami Warning Center Palmer AK")
        assert b is not None
        assert b.bulletin_id == "urn:uuid:7a6b0584-8201-4ef6-aac6-e512d77cbfb9"
        assert b.feed == "PAAQ"
        assert b.center == "NWS National Tsunami Warning Center Palmer AK"
        assert b.title == "60 miles SW of Buldir I., Alaska"
        assert b.updated == "2026-04-03T08:28:39Z"
        assert b.latitude == pytest.approx(51.610)
        assert b.longitude == pytest.approx(174.990)
        assert b.category == "Information"
        assert b.magnitude == "5.2(mb)"
        assert b.affected_region == "60 miles SW of Buldir I., Alaska"
        assert b.note is not None
        assert "NO tsunami danger" in b.note
        assert b.bulletin_url == "https://www.tsunami.gov/events/PAAQ/2026/04/03/tcwskp/1/WEAK53/WEAK53.txt"
        assert b.cap_url == "https://www.tsunami.gov/events/PAAQ/2026/04/03/tcwskp/1/WEAK53/PAAQCAP.xml"

    def test_no_id(self):
        xml_str = '<entry xmlns="http://www.w3.org/2005/Atom"><title>T</title><updated>2026-01-01T00:00:00Z</updated></entry>'
        entry = ET.fromstring(xml_str)
        assert parse_entry(entry, "PAAQ") is None

    def test_no_title(self):
        xml_str = '<entry xmlns="http://www.w3.org/2005/Atom"><id>urn:uuid:abc</id><updated>2026-01-01T00:00:00Z</updated></entry>'
        entry = ET.fromstring(xml_str)
        assert parse_entry(entry, "PAAQ") is None


# --- parse_connection_string ---

class TestParseConnectionString:
    def test_event_hubs(self):
        cs = "Endpoint=sb://ns.servicebus.windows.net/;SharedAccessKeyName=policy;SharedAccessKey=key123;EntityPath=topic1"
        result = parse_connection_string(cs)
        assert result["bootstrap.servers"] == "ns.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "topic1"

    def test_empty_returns_no_servers(self):
        result = parse_connection_string("")
        assert "bootstrap.servers" not in result


# --- PTWCTsunamiPoller state ---

class TestPollerState:
    def test_load_save(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{}")
            tmp = f.name
        try:
            poller = PTWCTsunamiPoller(state_file=tmp)
            state = poller.load_state()
            assert state == {}
            state["urn:uuid:abc"] = "2026-04-03T08:28:39Z"
            poller.save_state(state)
            assert poller.load_state() == {"urn:uuid:abc": "2026-04-03T08:28:39Z"}
        finally:
            os.unlink(tmp)

    def test_load_missing(self):
        poller = PTWCTsunamiPoller(state_file="/tmp/nonexistent_ptwc.json")
        assert poller.load_state() == {}


# --- PTWCTsunamiPoller poll_and_send ---

class TestPollerPollAndSend:
    @pytest.mark.asyncio
    async def test_poll_once_sends_new(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{}")
            tmp = f.name

        try:
            poller = PTWCTsunamiPoller(state_file=tmp, feeds=["PAAQ"])
            mock_producer = MagicMock()
            mock_event_producer = MagicMock()
            mock_event_producer.send_ptwc_tsunami_bulletin = AsyncMock()
            mock_event_producer.producer = mock_producer
            poller.event_producer = mock_event_producer

            root = ET.fromstring(SAMPLE_FEED_XML)

            async def mock_fetch(session, feed_name):
                return root

            poller.fetch_feed = mock_fetch

            await poller.poll_and_send(once=True)

            mock_event_producer.send_ptwc_tsunami_bulletin.assert_called_once()
            call_kwargs = mock_event_producer.send_ptwc_tsunami_bulletin.call_args
            assert call_kwargs[1]["_bulletin_id"] == "urn:uuid:7a6b0584-8201-4ef6-aac6-e512d77cbfb9"
            mock_producer.flush.assert_called_once()
        finally:
            os.unlink(tmp)

    @pytest.mark.asyncio
    async def test_poll_skips_seen(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"urn:uuid:7a6b0584-8201-4ef6-aac6-e512d77cbfb9": "2026-04-03T08:28:39Z"}, f)
            tmp = f.name

        try:
            poller = PTWCTsunamiPoller(state_file=tmp, feeds=["PAAQ"])
            mock_producer = MagicMock()
            mock_event_producer = MagicMock()
            mock_event_producer.send_ptwc_tsunami_bulletin = AsyncMock()
            mock_event_producer.producer = mock_producer
            poller.event_producer = mock_event_producer

            root = ET.fromstring(SAMPLE_FEED_XML)

            async def mock_fetch(session, feed_name):
                return root

            poller.fetch_feed = mock_fetch

            await poller.poll_and_send(once=True)

            mock_event_producer.send_ptwc_tsunami_bulletin.assert_not_called()
        finally:
            os.unlink(tmp)

    @pytest.mark.asyncio
    async def test_poll_empty_feed(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{}")
            tmp = f.name

        try:
            poller = PTWCTsunamiPoller(state_file=tmp, feeds=["PHEB"])

            root = ET.fromstring(SAMPLE_EMPTY_FEED_XML)

            async def mock_fetch(session, feed_name):
                return root

            poller.fetch_feed = mock_fetch

            await poller.poll_and_send(once=True)

            state = poller.load_state()
            assert len(state) == 0
        finally:
            os.unlink(tmp)

    @pytest.mark.asyncio
    async def test_poll_no_producer(self):
        """Dry-run mode without Kafka producer."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{}")
            tmp = f.name

        try:
            poller = PTWCTsunamiPoller(state_file=tmp, feeds=["PAAQ"])
            root = ET.fromstring(SAMPLE_FEED_XML)

            async def mock_fetch(session, feed_name):
                return root

            poller.fetch_feed = mock_fetch

            await poller.poll_and_send(once=True)

            state = poller.load_state()
            assert "urn:uuid:7a6b0584-8201-4ef6-aac6-e512d77cbfb9" in state
        finally:
            os.unlink(tmp)

    @pytest.mark.asyncio
    async def test_poll_feed_returns_none(self):
        """Gracefully handles a feed that returns None (404/error)."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{}")
            tmp = f.name

        try:
            poller = PTWCTsunamiPoller(state_file=tmp, feeds=["PAAQ"])

            async def mock_fetch(session, feed_name):
                return None

            poller.fetch_feed = mock_fetch

            await poller.poll_and_send(once=True)

            state = poller.load_state()
            assert len(state) == 0
        finally:
            os.unlink(tmp)
