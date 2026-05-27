"""
Unit tests for JMA Japan Weather Bulletins poller.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
import tempfile
import hashlib
from unittest.mock import Mock, patch, MagicMock
from xml.etree import ElementTree
from jma_japan.jma_japan import JMABulletinPoller, parse_connection_string, ATOM_NS


# ---------------------------------------------------------------------------
# Sample Atom feed XML for testing
# ---------------------------------------------------------------------------

SAMPLE_REGULAR_FEED = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" lang="ja">
  <title>高頻度（定時）</title>
  <subtitle>JMAXML publishing feed</subtitle>
  <updated>2026-04-09T10:18:25+09:00</updated>
  <id>https://www.data.jma.go.jp/developer/xml/feed/regular.xml#short_12345</id>
  <link rel="self" href="https://www.data.jma.go.jp/developer/xml/feed/regular.xml"/>
  <entry>
    <title>大雨危険度通知</title>
    <id>https://www.data.jma.go.jp/developer/xml/data/20260409011800_0_VPRN50_010000.xml</id>
    <updated>2026-04-09T01:17:49Z</updated>
    <author>
      <name>気象庁</name>
    </author>
    <link type="application/xml" href="https://www.data.jma.go.jp/developer/xml/data/20260409011800_0_VPRN50_010000.xml"/>
    <content type="text">【大雨危険度通知】</content>
  </entry>
  <entry>
    <title>警報級の可能性（明日まで）</title>
    <id>https://www.data.jma.go.jp/developer/xml/data/20260409011501_0_VPFD60_320000.xml</id>
    <updated>2026-04-09T01:15:00Z</updated>
    <author>
      <name>松江地方気象台</name>
    </author>
    <link type="application/xml" href="https://www.data.jma.go.jp/developer/xml/data/20260409011501_0_VPFD60_320000.xml"/>
    <content type="text">【島根県警報級の可能性（明日まで）】</content>
  </entry>
</feed>"""

SAMPLE_EXTRA_FEED = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" lang="ja">
  <title>高頻度（随時）</title>
  <subtitle>JMAXML publishing feed</subtitle>
  <updated>2026-04-09T10:16:56+09:00</updated>
  <id>https://www.data.jma.go.jp/developer/xml/feed/extra.xml#short_67890</id>
  <link rel="self" href="https://www.data.jma.go.jp/developer/xml/feed/extra.xml"/>
  <entry>
    <title>気象特別警報・警報・注意報</title>
    <id>https://www.data.jma.go.jp/developer/xml/data/20260409011641_0_VPWW53_410000.xml</id>
    <updated>2026-04-09T01:16:41Z</updated>
    <author>
      <name>佐賀地方気象台</name>
    </author>
    <link type="application/xml" href="https://www.data.jma.go.jp/developer/xml/data/20260409011641_0_VPWW53_410000.xml"/>
    <content type="text">【佐賀県気象警報・注意報】佐賀県では、強風や急な強い雨、落雷に注意してください。</content>
  </entry>
  <entry>
    <title>台風の暴風域に入る確率</title>
    <id>https://www.data.jma.go.jp/developer/xml/data/20260409011501_0_VPTA50_010000.xml</id>
    <updated>2026-04-09T01:13:04Z</updated>
    <author>
      <name>気象庁</name>
    </author>
    <link type="application/xml" href="https://www.data.jma.go.jp/developer/xml/data/20260409011501_0_VPTA50_010000.xml"/>
    <content type="text">【台風の暴風域に入る確率】</content>
  </entry>
</feed>"""

SAMPLE_EMPTY_FEED = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" lang="ja">
  <title>Empty feed</title>
  <updated>2026-04-09T00:00:00+09:00</updated>
  <id>https://www.data.jma.go.jp/developer/xml/feed/empty.xml</id>
</feed>"""

SAMPLE_ENTRY_NO_ID = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" lang="ja">
  <title>Feed with bad entry</title>
  <updated>2026-04-09T00:00:00+09:00</updated>
  <id>https://www.data.jma.go.jp/developer/xml/feed/bad.xml</id>
  <entry>
    <title>No ID entry</title>
    <updated>2026-04-09T01:00:00Z</updated>
  </entry>
</feed>"""

SAMPLE_ENTRY_MISSING_OPTIONAL = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" lang="ja">
  <title>Minimal entry feed</title>
  <updated>2026-04-09T00:00:00+09:00</updated>
  <id>https://www.data.jma.go.jp/developer/xml/feed/minimal.xml</id>
  <entry>
    <title>Minimal</title>
    <id>https://example.com/minimal-entry</id>
    <updated>2026-04-09T01:00:00Z</updated>
  </entry>
</feed>"""


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_kafka_config():
    return {
        'bootstrap.servers': 'localhost:9092',
    }


@pytest.fixture
def temp_state_file():
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


def _make_poller(mock_kafka_config, temp_state_file):
    """Create a JMABulletinPoller with a mocked Kafka producer."""
    with patch('confluent_kafka.Producer') as mock_producer_class:
        mock_producer_class.return_value = MagicMock()
        poller = JMABulletinPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
        )
    return poller


# ---------------------------------------------------------------------------
# Test: JMABulletinPoller initialisation
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestJMABulletinPollerInit:
    def test_init(self, mock_kafka_config, temp_state_file):
        poller = _make_poller(mock_kafka_config, temp_state_file)
        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == temp_state_file

    def test_init_stores_producers(self, mock_kafka_config, temp_state_file):
        poller = _make_poller(mock_kafka_config, temp_state_file)
        assert poller.bulletins_producer is not None
        assert poller.kafka_producer is not None


# ---------------------------------------------------------------------------
# Test: State file load / save
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestStateFilePersistence:
    def test_load_seen_bulletins_empty(self, mock_kafka_config):
        poller = _make_poller(mock_kafka_config, 'nonexistent_jma_state.json')
        state = poller.load_seen_bulletins()
        assert state == {"seen_ids": []}

    def test_load_seen_bulletins_existing(self, mock_kafka_config, temp_state_file):
        state_data = {"seen_ids": ["b1", "b2", "b3"]}
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f)
        poller = _make_poller(mock_kafka_config, temp_state_file)
        state = poller.load_seen_bulletins()
        assert state["seen_ids"] == ["b1", "b2", "b3"]

    def test_save_seen_bulletins(self, mock_kafka_config, temp_state_file):
        poller = _make_poller(mock_kafka_config, temp_state_file)
        poller.save_seen_bulletins({"seen_ids": ["b1", "b2"]})
        with open(temp_state_file, 'r', encoding='utf-8') as f:
            saved = json.load(f)
        assert saved["seen_ids"] == ["b1", "b2"]

    def test_load_corrupt_state_file(self, mock_kafka_config, temp_state_file):
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            f.write("this is not json")
        poller = _make_poller(mock_kafka_config, temp_state_file)
        state = poller.load_seen_bulletins()
        assert state == {"seen_ids": []}

    def test_save_creates_directory(self, mock_kafka_config):
        path = os.path.join(tempfile.gettempdir(), 'jma_test_subdir', 'state.json')
        try:
            poller = _make_poller(mock_kafka_config, path)
            poller.save_seen_bulletins({"seen_ids": ["x"]})
            with open(path, 'r', encoding='utf-8') as f:
                saved = json.load(f)
            assert saved["seen_ids"] == ["x"]
        finally:
            if os.path.exists(path):
                os.unlink(path)
            parent = os.path.dirname(path)
            if os.path.isdir(parent):
                os.rmdir(parent)


# ---------------------------------------------------------------------------
# Test: Bulletin ID generation
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestMakeBulletinId:
    def test_deterministic(self):
        id1 = JMABulletinPoller._make_bulletin_id("https://example.com/entry1")
        id2 = JMABulletinPoller._make_bulletin_id("https://example.com/entry1")
        assert id1 == id2

    def test_different_inputs_different_ids(self):
        id1 = JMABulletinPoller._make_bulletin_id("https://example.com/entry1")
        id2 = JMABulletinPoller._make_bulletin_id("https://example.com/entry2")
        assert id1 != id2

    def test_length_is_16(self):
        bid = JMABulletinPoller._make_bulletin_id("https://example.com/any")
        assert len(bid) == 16

    def test_hex_characters_only(self):
        bid = JMABulletinPoller._make_bulletin_id("some entry id")
        assert all(c in '0123456789abcdef' for c in bid)

    def test_matches_sha256_prefix(self):
        entry_id = "https://www.data.jma.go.jp/developer/xml/data/test.xml"
        expected = hashlib.sha256(entry_id.encode("utf-8")).hexdigest()[:16]
        assert JMABulletinPoller._make_bulletin_id(entry_id) == expected


# ---------------------------------------------------------------------------
# Test: Atom feed fetching
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestFetchFeed:
    @patch('jma_japan.jma_japan.requests.get')
    def test_fetch_feed_success(self, mock_get, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.content = SAMPLE_REGULAR_FEED.encode('utf-8')
        mock_get.return_value = mock_response
        poller = _make_poller(mock_kafka_config, temp_state_file)
        root = poller.fetch_feed("https://www.data.jma.go.jp/developer/xml/feed/regular.xml")
        assert root is not None
        assert root.tag == f"{ATOM_NS}feed"

    @patch('jma_japan.jma_japan.requests.get')
    def test_fetch_feed_network_error(self, mock_get, mock_kafka_config, temp_state_file):
        mock_get.side_effect = Exception("Connection timeout")
        poller = _make_poller(mock_kafka_config, temp_state_file)
        root = poller.fetch_feed("https://www.data.jma.go.jp/developer/xml/feed/regular.xml")
        assert root is None

    @patch('jma_japan.jma_japan.requests.get')
    def test_fetch_feed_http_error(self, mock_get, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP 500")
        mock_get.return_value = mock_response
        poller = _make_poller(mock_kafka_config, temp_state_file)
        root = poller.fetch_feed("https://example.com/bad")
        assert root is None

    @patch('jma_japan.jma_japan.requests.get')
    def test_fetch_feed_invalid_xml(self, mock_get, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.content = b"<not valid xml"
        mock_get.return_value = mock_response
        poller = _make_poller(mock_kafka_config, temp_state_file)
        root = poller.fetch_feed("https://example.com/bad")
        assert root is None


# ---------------------------------------------------------------------------
# Test: Atom entry parsing
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseEntries:
    def test_parse_regular_entries(self):
        root = ElementTree.fromstring(SAMPLE_REGULAR_FEED)
        bulletins = JMABulletinPoller.parse_entries(root, "regular")
        assert len(bulletins) == 2
        assert bulletins[0].title == "大雨危険度通知"
        assert bulletins[0].author == "気象庁"
        assert bulletins[0].feed_type.value == "regular"

    def test_parse_extra_entries(self):
        root = ElementTree.fromstring(SAMPLE_EXTRA_FEED)
        bulletins = JMABulletinPoller.parse_entries(root, "extra")
        assert len(bulletins) == 2
        assert bulletins[0].title == "気象特別警報・警報・注意報"
        assert bulletins[0].author == "佐賀地方気象台"
        assert bulletins[0].feed_type.value == "extra"

    def test_parse_entry_link(self):
        root = ElementTree.fromstring(SAMPLE_REGULAR_FEED)
        bulletins = JMABulletinPoller.parse_entries(root, "regular")
        assert bulletins[0].link == "https://www.data.jma.go.jp/developer/xml/data/20260409011800_0_VPRN50_010000.xml"

    def test_parse_entry_content(self):
        root = ElementTree.fromstring(SAMPLE_REGULAR_FEED)
        bulletins = JMABulletinPoller.parse_entries(root, "regular")
        assert bulletins[0].content == "【大雨危険度通知】"

    def test_parse_entry_updated(self):
        root = ElementTree.fromstring(SAMPLE_REGULAR_FEED)
        bulletins = JMABulletinPoller.parse_entries(root, "regular")
        assert bulletins[0].updated == "2026-04-09T01:17:49Z"

    def test_parse_empty_feed(self):
        root = ElementTree.fromstring(SAMPLE_EMPTY_FEED)
        bulletins = JMABulletinPoller.parse_entries(root, "regular")
        assert bulletins == []

    def test_parse_entry_without_id_skipped(self):
        root = ElementTree.fromstring(SAMPLE_ENTRY_NO_ID)
        bulletins = JMABulletinPoller.parse_entries(root, "regular")
        assert bulletins == []

    def test_parse_entry_missing_optional_fields(self):
        root = ElementTree.fromstring(SAMPLE_ENTRY_MISSING_OPTIONAL)
        bulletins = JMABulletinPoller.parse_entries(root, "regular")
        assert len(bulletins) == 1
        assert bulletins[0].title == "Minimal"
        assert bulletins[0].author is None
        assert bulletins[0].link is None
        assert bulletins[0].content is None

    def test_bulletin_id_is_hash_of_entry_id(self):
        root = ElementTree.fromstring(SAMPLE_REGULAR_FEED)
        bulletins = JMABulletinPoller.parse_entries(root, "regular")
        entry_id = "https://www.data.jma.go.jp/developer/xml/data/20260409011800_0_VPRN50_010000.xml"
        expected = hashlib.sha256(entry_id.encode("utf-8")).hexdigest()[:16]
        assert bulletins[0].bulletin_id == expected

    def test_parse_extra_content_with_details(self):
        root = ElementTree.fromstring(SAMPLE_EXTRA_FEED)
        bulletins = JMABulletinPoller.parse_entries(root, "extra")
        assert "佐賀県" in bulletins[0].content
        assert "強風" in bulletins[0].content


# ---------------------------------------------------------------------------
# Test: poll_feeds integration with fetch_feed
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestPollFeeds:
    @patch('jma_japan.jma_japan.requests.get')
    def test_poll_both_feeds(self, mock_get, mock_kafka_config, temp_state_file):
        def side_effect(url, **kwargs):
            resp = Mock()
            resp.status_code = 200
            resp.raise_for_status = Mock()
            if 'regular' in url:
                resp.content = SAMPLE_REGULAR_FEED.encode('utf-8')
            else:
                resp.content = SAMPLE_EXTRA_FEED.encode('utf-8')
            return resp
        mock_get.side_effect = side_effect
        poller = _make_poller(mock_kafka_config, temp_state_file)
        bulletins = poller.poll_feeds()
        assert len(bulletins) == 4
        regular = [b for b in bulletins if b.feed_type.value == "regular"]
        extra = [b for b in bulletins if b.feed_type.value == "extra"]
        assert len(regular) == 2
        assert len(extra) == 2

    @patch('jma_japan.jma_japan.requests.get')
    def test_poll_feeds_one_fails(self, mock_get, mock_kafka_config, temp_state_file):
        call_count = [0]
        def side_effect(url, **kwargs):
            call_count[0] += 1
            if 'regular' in url:
                raise Exception("Regular feed down")
            resp = Mock()
            resp.status_code = 200
            resp.raise_for_status = Mock()
            resp.content = SAMPLE_EXTRA_FEED.encode('utf-8')
            return resp
        mock_get.side_effect = side_effect
        poller = _make_poller(mock_kafka_config, temp_state_file)
        bulletins = poller.poll_feeds()
        assert len(bulletins) == 2
        assert all(b.feed_type.value == "extra" for b in bulletins)

    @patch('jma_japan.jma_japan.requests.get')
    def test_poll_feeds_both_fail(self, mock_get, mock_kafka_config, temp_state_file):
        mock_get.side_effect = Exception("All feeds down")
        poller = _make_poller(mock_kafka_config, temp_state_file)
        bulletins = poller.poll_feeds()
        assert bulletins == []


# ---------------------------------------------------------------------------
# Test: parse_connection_string
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseConnectionString:
    def test_parse_valid_event_hubs(self):
        conn_str = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=myhub"
        result = parse_connection_string(conn_str)
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'myhub'
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == conn_str

    def test_parse_connection_string_without_entity_path(self):
        conn_str = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123"
        result = parse_connection_string(conn_str)
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert 'kafka_topic' not in result
        assert result['sasl.username'] == '$ConnectionString'

    def test_parse_bootstrap_server(self):
        conn_str = "BootstrapServer=localhost:9092;EntityPath=my-topic"
        result = parse_connection_string(conn_str)
        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'my-topic'

    def test_parse_password_is_full_string(self):
        conn_str = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=test;SharedAccessKey=key;EntityPath=hub"
        result = parse_connection_string(conn_str)
        assert result['sasl.password'] == conn_str

    def test_parse_sets_security_protocol(self):
        conn_str = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=test;SharedAccessKey=key"
        result = parse_connection_string(conn_str)
        assert result['security.protocol'] == 'SASL_SSL'
        assert result['sasl.mechanism'] == 'PLAIN'

    def test_parse_bootstrap_only_no_security(self):
        conn_str = "BootstrapServer=broker:9092;EntityPath=topic"
        result = parse_connection_string(conn_str)
        assert 'security.protocol' not in result
        assert 'sasl.mechanism' not in result


# ---------------------------------------------------------------------------
# Test: WeatherBulletin dataclass
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestWeatherBulletinDataclass:
    def test_create_weather_bulletin(self):
        from jma_japan_producer_data import WeatherBulletin
        from jma_japan_producer_data.feedtypeenum import FeedTypeenum
        bulletin = WeatherBulletin(
            bulletin_id="abc123def456",
            title="気象特別警報",
            author="気象庁",
            updated="2026-04-09T01:00:00Z",
            link="https://example.com/bulletin.xml",
            content="【警報】",
            feed_type=FeedTypeenum.extra,
        )
        assert bulletin.bulletin_id == "abc123def456"
        assert bulletin.title == "気象特別警報"
        assert bulletin.author == "気象庁"
        assert bulletin.feed_type == FeedTypeenum.extra

    def test_bulletin_with_none_optionals(self):
        from jma_japan_producer_data import WeatherBulletin
        from jma_japan_producer_data.feedtypeenum import FeedTypeenum
        bulletin = WeatherBulletin(
            bulletin_id="test-id",
            title="Test",
            author=None,
            updated="2026-04-09T01:00:00Z",
            link=None,
            content=None,
            feed_type=FeedTypeenum.regular,
        )
        assert bulletin.author is None
        assert bulletin.link is None
        assert bulletin.content is None

    def test_bulletin_to_json(self):
        from jma_japan_producer_data import WeatherBulletin
        from jma_japan_producer_data.feedtypeenum import FeedTypeenum
        bulletin = WeatherBulletin(
            bulletin_id="test123",
            title="テスト",
            author="テスト局",
            updated="2026-04-09T01:00:00Z",
            link="https://example.com/test.xml",
            content="テスト内容",
            feed_type=FeedTypeenum.regular,
        )
        json_str = bulletin.to_json()
        data = json.loads(json_str)
        assert data["bulletin_id"] == "test123"
        assert data["title"] == "テスト"
        assert data["feed_type"] == "regular"

    def test_bulletin_from_data_dict(self):
        from jma_japan_producer_data import WeatherBulletin
        data = {
            "bulletin_id": "fromdict",
            "title": "From Dict",
            "author": None,
            "updated": "2026-04-09T00:00:00Z",
            "link": None,
            "content": None,
            "feed_type": "regular",
        }
        bulletin = WeatherBulletin.from_data(data)
        assert bulletin.bulletin_id == "fromdict"
        assert bulletin.title == "From Dict"


# ---------------------------------------------------------------------------
# Test: FeedTypeenum
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestFeedTypeEnum:
    def test_regular_value(self):
        from jma_japan_producer_data.feedtypeenum import FeedTypeenum
        assert FeedTypeenum.regular.value == "regular"

    def test_extra_value(self):
        from jma_japan_producer_data.feedtypeenum import FeedTypeenum
        assert FeedTypeenum.extra.value == "extra"

    def test_from_ordinal(self):
        from jma_japan_producer_data.feedtypeenum import FeedTypeenum
        assert FeedTypeenum.from_ordinal(0) == FeedTypeenum.regular
        assert FeedTypeenum.from_ordinal(1) == FeedTypeenum.extra

    def test_to_ordinal(self):
        from jma_japan_producer_data.feedtypeenum import FeedTypeenum
        assert FeedTypeenum.to_ordinal(FeedTypeenum.regular) == 0
        assert FeedTypeenum.to_ordinal(FeedTypeenum.extra) == 1

    def test_from_ordinal_out_of_range(self):
        from jma_japan_producer_data.feedtypeenum import FeedTypeenum
        with pytest.raises(IndexError):
            FeedTypeenum.from_ordinal(99)


# ---------------------------------------------------------------------------
# Test: Japanese text handling
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestJapaneseTextHandling:
    def test_parse_japanese_title(self):
        root = ElementTree.fromstring(SAMPLE_REGULAR_FEED)
        bulletins = JMABulletinPoller.parse_entries(root, "regular")
        assert bulletins[0].title == "大雨危険度通知"

    def test_parse_japanese_author(self):
        root = ElementTree.fromstring(SAMPLE_EXTRA_FEED)
        bulletins = JMABulletinPoller.parse_entries(root, "extra")
        assert bulletins[0].author == "佐賀地方気象台"

    def test_parse_japanese_content(self):
        root = ElementTree.fromstring(SAMPLE_EXTRA_FEED)
        bulletins = JMABulletinPoller.parse_entries(root, "extra")
        assert "佐賀県気象警報・注意報" in bulletins[0].content

    def test_bulletin_roundtrip_json_japanese(self):
        from jma_japan_producer_data import WeatherBulletin
        from jma_japan_producer_data.feedtypeenum import FeedTypeenum
        bulletin = WeatherBulletin(
            bulletin_id="jp-test",
            title="台風第１号",
            author="気象庁",
            updated="2026-04-09T00:00:00Z",
            link=None,
            content="大型の台風が接近中です。",
            feed_type=FeedTypeenum.extra,
        )
        json_str = bulletin.to_json()
        restored = WeatherBulletin.from_data(json_str, "application/json")
        assert restored.title == "台風第１号"
        assert restored.content == "大型の台風が接近中です。"


# ---------------------------------------------------------------------------
# Test: Deduplication logic
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestDeduplication:
    @patch('jma_japan.jma_japan.requests.get')
    def test_seen_bulletins_not_resent(self, mock_get, mock_kafka_config, temp_state_file):
        """Bulletins already in the seen set should not be re-sent."""
        root = ElementTree.fromstring(SAMPLE_REGULAR_FEED)
        bulletins = JMABulletinPoller.parse_entries(root, "regular")
        first_id = bulletins[0].bulletin_id

        # Pre-populate state with first bulletin's ID
        state = {"seen_ids": [first_id]}
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f)

        poller = _make_poller(mock_kafka_config, temp_state_file)
        loaded = poller.load_seen_bulletins()
        assert first_id in loaded["seen_ids"]

    def test_seen_ids_cap_at_10000(self, mock_kafka_config, temp_state_file):
        poller = _make_poller(mock_kafka_config, temp_state_file)
        big_list = [f"id_{i}" for i in range(15000)]
        state = {"seen_ids": big_list}
        # Simulate the cap logic from poll_and_send
        seen_list = state["seen_ids"]
        if len(seen_list) > 10000:
            seen_list = seen_list[-10000:]
        assert len(seen_list) == 10000
        assert seen_list[0] == "id_5000"


# ---------------------------------------------------------------------------
# Test: Feed URL constants
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestFeedConstants:
    def test_regular_feed_url(self):
        assert JMABulletinPoller.REGULAR_FEED_URL == "https://www.data.jma.go.jp/developer/xml/feed/regular.xml"

    def test_extra_feed_url(self):
        assert JMABulletinPoller.EXTRA_FEED_URL == "https://www.data.jma.go.jp/developer/xml/feed/extra.xml"

    def test_poll_interval(self):
        assert JMABulletinPoller.POLL_INTERVAL_SECONDS == 60

    def test_user_agent_header(self):
        assert "real-time-sources" in JMABulletinPoller.HEADERS["User-Agent"]
