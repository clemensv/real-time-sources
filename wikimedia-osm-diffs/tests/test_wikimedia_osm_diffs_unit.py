"""Unit tests for the OpenStreetMap Minutely Diffs bridge."""

import datetime
import gzip
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from wikimedia_osm_diffs.wikimedia_osm_diffs import (
    OsmDiffsBridge,
    StateStore,
    parse_connection_string,
    parse_osmchange_xml,
    parse_state_txt,
    sequence_to_path,
    sequence_to_url,
)


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_STATE_TXT = """\
#Thu Apr 09 01:33:23 UTC 2026
sequenceNumber=7062480
timestamp=2026-04-09T01\\:32\\:55Z
"""

SAMPLE_OSC_XML = b"""\
<?xml version='1.0' encoding='UTF-8'?>
<osmChange version="0.6" generator="osmdbt-create-diff/0.9">
  <create>
    <node id="12345" version="1" timestamp="2026-04-09T01:30:00Z" uid="100" user="testuser" changeset="999" lat="48.8566" lon="2.3522">
      <tag k="name" v="Test Node"/>
      <tag k="amenity" v="cafe"/>
    </node>
    <way id="67890" version="1" timestamp="2026-04-09T01:30:05Z" uid="200" user="wayuser" changeset="1000">
      <nd ref="11111"/>
      <nd ref="22222"/>
      <tag k="highway" v="residential"/>
    </way>
  </create>
  <modify>
    <node id="54321" version="3" timestamp="2026-04-09T01:31:00Z" uid="300" user="modifier" changeset="1001" lat="51.5074" lon="-0.1278"/>
    <relation id="99999" version="2" timestamp="2026-04-09T01:31:30Z" uid="400" user="reluser" changeset="1002">
      <member type="way" ref="11111" role="outer"/>
      <tag k="type" v="multipolygon"/>
    </relation>
  </modify>
  <delete>
    <node id="11111" version="5" timestamp="2026-04-09T01:32:00Z" uid="500" user="deleter" changeset="1003" lat="40.7128" lon="-74.0060"/>
  </delete>
</osmChange>
"""

SAMPLE_OSC_NODES_ONLY = b"""\
<?xml version='1.0' encoding='UTF-8'?>
<osmChange version="0.6" generator="test">
  <create>
    <node id="1" version="1" timestamp="2026-01-01T00:00:00Z" uid="10" user="u1" changeset="100" lat="10.0" lon="20.0">
      <tag k="key1" v="value1"/>
    </node>
  </create>
</osmChange>
"""

SAMPLE_OSC_NO_USER = b"""\
<?xml version='1.0' encoding='UTF-8'?>
<osmChange version="0.6" generator="test">
  <create>
    <node id="2" version="1" timestamp="2026-01-01T00:00:00Z" changeset="101" lat="0.0" lon="0.0"/>
  </create>
</osmChange>
"""

SAMPLE_OSC_WAY_NO_COORDS = b"""\
<?xml version='1.0' encoding='UTF-8'?>
<osmChange version="0.6" generator="test">
  <modify>
    <way id="555" version="2" timestamp="2026-02-01T12:00:00Z" uid="50" user="waymod" changeset="200">
      <nd ref="100"/>
      <nd ref="101"/>
    </way>
  </modify>
</osmChange>
"""

SAMPLE_OSC_EMPTY = b"""\
<?xml version='1.0' encoding='UTF-8'?>
<osmChange version="0.6" generator="test">
</osmChange>
"""

SAMPLE_OSC_RELATION = b"""\
<?xml version='1.0' encoding='UTF-8'?>
<osmChange version="0.6" generator="test">
  <delete>
    <relation id="777" version="3" timestamp="2026-03-15T08:00:00Z" uid="60" user="reldel" changeset="300">
      <member type="node" ref="1" role="stop"/>
      <tag k="route" v="bus"/>
      <tag k="name" v="Route 42"/>
    </relation>
  </delete>
</osmChange>
"""


# ---------------------------------------------------------------------------
# State.txt parsing
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseStateTxt:
    def test_parses_sequence_number(self) -> None:
        result = parse_state_txt(SAMPLE_STATE_TXT)
        assert result["sequence_number"] == 7062480

    def test_parses_timestamp_with_escaped_colons(self) -> None:
        result = parse_state_txt(SAMPLE_STATE_TXT)
        ts = result["timestamp"]
        assert isinstance(ts, datetime.datetime)
        assert ts.year == 2026
        assert ts.month == 4
        assert ts.day == 9
        assert ts.hour == 1
        assert ts.minute == 32
        assert ts.second == 55

    def test_ignores_comments(self) -> None:
        text = "#comment\nsequenceNumber=100\ntimestamp=2026-01-01T00\\:00\\:00Z\n"
        result = parse_state_txt(text)
        assert result["sequence_number"] == 100

    def test_ignores_blank_lines(self) -> None:
        text = "\n\nsequenceNumber=42\n\ntimestamp=2026-06-01T12\\:00\\:00Z\n"
        result = parse_state_txt(text)
        assert result["sequence_number"] == 42

    def test_empty_string(self) -> None:
        result = parse_state_txt("")
        assert result == {}

    def test_only_comments(self) -> None:
        result = parse_state_txt("#only comments\n#another\n")
        assert result == {}


# ---------------------------------------------------------------------------
# Sequence number to URL path
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestSequenceToPath:
    def test_known_sequence(self) -> None:
        assert sequence_to_path(7058774) == "007/058/774"

    def test_zero_sequence(self) -> None:
        assert sequence_to_path(0) == "000/000/000"

    def test_small_sequence(self) -> None:
        assert sequence_to_path(1) == "000/000/001"

    def test_thousand_boundary(self) -> None:
        assert sequence_to_path(1000) == "000/001/000"

    def test_million_boundary(self) -> None:
        assert sequence_to_path(1000000) == "001/000/000"

    def test_sequence_to_url_default_base(self) -> None:
        url = sequence_to_url(7062480)
        assert url == "https://planet.openstreetmap.org/replication/minute/007/062/480.osc.gz"

    def test_sequence_to_url_custom_base(self) -> None:
        url = sequence_to_url(123, base_url="https://example.com/diffs")
        assert url == "https://example.com/diffs/000/000/123.osc.gz"


# ---------------------------------------------------------------------------
# OsmChange XML parsing
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseOsmChangeXml:
    def test_total_change_count(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_XML, 100)
        assert len(changes) == 5

    def test_create_node(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_XML, 100)
        node = next(c for c in changes if c["element_id"] == 12345)
        assert node["change_type"] == "create"
        assert node["element_type"] == "node"
        assert node["version"] == 1
        assert node["changeset_id"] == 999
        assert node["user_name"] == "testuser"
        assert node["user_id"] == 100
        assert node["latitude"] == pytest.approx(48.8566)
        assert node["longitude"] == pytest.approx(2.3522)
        assert node["sequence_number"] == 100

    def test_create_way(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_XML, 100)
        way = next(c for c in changes if c["element_id"] == 67890)
        assert way["change_type"] == "create"
        assert way["element_type"] == "way"
        assert way["latitude"] is None
        assert way["longitude"] is None

    def test_modify_node(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_XML, 100)
        node = next(c for c in changes if c["element_id"] == 54321)
        assert node["change_type"] == "modify"
        assert node["element_type"] == "node"
        assert node["version"] == 3

    def test_modify_relation(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_XML, 100)
        rel = next(c for c in changes if c["element_id"] == 99999)
        assert rel["change_type"] == "modify"
        assert rel["element_type"] == "relation"
        assert rel["latitude"] is None
        assert rel["longitude"] is None

    def test_delete_node(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_XML, 100)
        node = next(c for c in changes if c["element_id"] == 11111)
        assert node["change_type"] == "delete"
        assert node["element_type"] == "node"

    def test_tag_extraction_as_json(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_XML, 100)
        node = next(c for c in changes if c["element_id"] == 12345)
        tags = json.loads(node["tags"])
        assert tags == {"name": "Test Node", "amenity": "cafe"}

    def test_empty_tags_node(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_XML, 100)
        node = next(c for c in changes if c["element_id"] == 54321)
        tags = json.loads(node["tags"])
        assert tags == {}

    def test_way_tags(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_XML, 100)
        way = next(c for c in changes if c["element_id"] == 67890)
        tags = json.loads(way["tags"])
        assert tags == {"highway": "residential"}

    def test_relation_tags(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_RELATION, 500)
        rel = changes[0]
        tags = json.loads(rel["tags"])
        assert tags == {"route": "bus", "name": "Route 42"}

    def test_timestamp_parsing(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_XML, 100)
        node = next(c for c in changes if c["element_id"] == 12345)
        ts = node["timestamp"]
        assert isinstance(ts, datetime.datetime)
        assert ts.hour == 1
        assert ts.minute == 30

    def test_empty_xml(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_EMPTY, 0)
        assert changes == []

    def test_sequence_number_propagated(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_NODES_ONLY, 42)
        assert all(c["sequence_number"] == 42 for c in changes)


# ---------------------------------------------------------------------------
# Nullable field handling
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestNullableFields:
    def test_node_without_user_info(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_NO_USER, 1)
        assert len(changes) == 1
        node = changes[0]
        assert node["user_name"] is None
        assert node["user_id"] is None

    def test_way_has_no_coordinates(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_WAY_NO_COORDS, 2)
        way = changes[0]
        assert way["latitude"] is None
        assert way["longitude"] is None

    def test_relation_has_no_coordinates(self) -> None:
        changes = parse_osmchange_xml(SAMPLE_OSC_RELATION, 3)
        rel = changes[0]
        assert rel["latitude"] is None
        assert rel["longitude"] is None


# ---------------------------------------------------------------------------
# Connection string parsing
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestConnectionString:
    def test_event_hubs_connection_string(self) -> None:
        result = parse_connection_string(
            "Endpoint=sb://namespace.servicebus.windows.net/;"
            "SharedAccessKeyName=Root;"
            "SharedAccessKey=secret;"
            "EntityPath=topic"
        )
        assert result["bootstrap.servers"] == "namespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "topic"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["security.protocol"] == "SASL_SSL"

    def test_plain_bootstrap_server_connection_string(self) -> None:
        result = parse_connection_string("BootstrapServer=localhost:9092;EntityPath=topic")
        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["kafka_topic"] == "topic"

    def test_plain_bootstrap_no_sasl(self) -> None:
        result = parse_connection_string("BootstrapServer=localhost:9092;EntityPath=t")
        assert "sasl.username" not in result
        assert "security.protocol" not in result


# ---------------------------------------------------------------------------
# State store
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestStateStore:
    def test_load_returns_none_when_no_file(self, tmp_path: Path) -> None:
        store = StateStore(str(tmp_path / "missing.json"))
        assert store.load() is None

    def test_save_and_load(self, tmp_path: Path) -> None:
        path = str(tmp_path / "state.json")
        store = StateStore(path)
        store.save(7062480)
        assert store.load() == 7062480

    def test_save_overwrites(self, tmp_path: Path) -> None:
        path = str(tmp_path / "state.json")
        store = StateStore(path)
        store.save(100)
        store.save(200)
        assert store.load() == 200

    def test_load_handles_corrupt_json(self, tmp_path: Path) -> None:
        path = tmp_path / "state.json"
        path.write_text("not json", encoding="utf-8")
        store = StateStore(str(path))
        assert store.load() is None

    def test_creates_parent_directory(self, tmp_path: Path) -> None:
        path = str(tmp_path / "sub" / "dir" / "state.json")
        store = StateStore(path)
        store.save(999)
        assert store.load() == 999


# ---------------------------------------------------------------------------
# Bridge deduplication / sequence tracking
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestBridgeDedup:
    def _make_bridge(self, tmp_path: Path, last_seq: int | None = None) -> OsmDiffsBridge:
        state_store = StateStore(str(tmp_path / "state.json"))
        if last_seq is not None:
            state_store.save(last_seq)

        diffs_producer = MagicMock()
        state_producer = MagicMock()
        kafka_producer = MagicMock()

        bridge = OsmDiffsBridge(
            diffs_producer,
            state_producer,
            kafka_producer,
            state_store=state_store,
            state_url="http://invalid.test/state.txt",
            diff_base_url="http://invalid.test/diffs",
        )
        return bridge

    def test_initial_state_is_none(self, tmp_path: Path) -> None:
        bridge = self._make_bridge(tmp_path)
        assert bridge._last_sequence is None

    def test_loads_persisted_state(self, tmp_path: Path) -> None:
        bridge = self._make_bridge(tmp_path, last_seq=500)
        assert bridge._last_sequence == 500

    @patch("wikimedia_osm_diffs.wikimedia_osm_diffs.requests.Session")
    def test_skips_already_processed_sequence(self, mock_session_cls, tmp_path: Path) -> None:
        bridge = self._make_bridge(tmp_path, last_seq=100)
        mock_session = bridge._session
        mock_resp = MagicMock()
        mock_resp.text = "sequenceNumber=100\ntimestamp=2026-01-01T00\\:00\\:00Z\n"
        mock_resp.raise_for_status = MagicMock()
        mock_session.get.return_value = mock_resp

        bridge._poll_cycle()
        # Should not call get for a diff URL since sequence hasn't advanced
        assert bridge._diffs_producer.send_org_open_street_map_diffs_map_change.call_count == 0


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestErrorHandling:
    def test_parse_state_txt_missing_sequence(self) -> None:
        result = parse_state_txt("timestamp=2026-01-01T00\\:00\\:00Z\n")
        assert "sequence_number" not in result

    def test_parse_state_txt_missing_timestamp(self) -> None:
        result = parse_state_txt("sequenceNumber=100\n")
        assert result["sequence_number"] == 100
        assert "timestamp" not in result

    def test_osmchange_xml_ignores_unknown_elements(self) -> None:
        xml = b"""\
<?xml version='1.0' encoding='UTF-8'?>
<osmChange version="0.6" generator="test">
  <create>
    <unknown id="1" version="1" timestamp="2026-01-01T00:00:00Z" changeset="1"/>
    <node id="2" version="1" timestamp="2026-01-01T00:00:00Z" uid="1" user="u" changeset="1" lat="0" lon="0"/>
  </create>
</osmChange>
"""
        changes = parse_osmchange_xml(xml, 1)
        assert len(changes) == 1
        assert changes[0]["element_id"] == 2

    def test_osmchange_xml_ignores_unknown_action(self) -> None:
        xml = b"""\
<?xml version='1.0' encoding='UTF-8'?>
<osmChange version="0.6" generator="test">
  <remark>something</remark>
  <create>
    <node id="1" version="1" timestamp="2026-01-01T00:00:00Z" uid="1" user="u" changeset="1" lat="0" lon="0"/>
  </create>
</osmChange>
"""
        changes = parse_osmchange_xml(xml, 1)
        assert len(changes) == 1

    def test_state_store_load_handles_missing_key(self, tmp_path: Path) -> None:
        path = tmp_path / "state.json"
        path.write_text('{"other_key": 42}', encoding="utf-8")
        store = StateStore(str(path))
        assert store.load() is None


# ---------------------------------------------------------------------------
# Gzip decompression (integration-like but no network)
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestGzipDecompression:
    def test_decompress_and_parse(self) -> None:
        import gzip as gzip_mod
        compressed = gzip_mod.compress(SAMPLE_OSC_NODES_ONLY)
        decompressed = gzip_mod.decompress(compressed)
        changes = parse_osmchange_xml(decompressed, 10)
        assert len(changes) == 1
        assert changes[0]["element_type"] == "node"

    def test_decompress_real_format(self) -> None:
        import gzip as gzip_mod
        compressed = gzip_mod.compress(SAMPLE_OSC_XML)
        decompressed = gzip_mod.decompress(compressed)
        changes = parse_osmchange_xml(decompressed, 7062480)
        assert len(changes) == 5
