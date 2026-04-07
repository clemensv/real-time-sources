"""
Unit tests for the GDACS Disaster Alert poller.
Tests parsing, normalization, state tracking, and connection string handling.
"""

import pytest
import xml.etree.ElementTree as ET
from unittest.mock import patch, Mock, AsyncMock, MagicMock
from gdacs.gdacs import (
    GDACSPoller,
    parse_rss_item,
    parse_connection_string,
    _text,
    _attr,
    _parse_float,
    _parse_int,
    _parse_bool,
    _parse_datetime,
    _parse_bbox,
    NAMESPACES,
    GDACS_RSS_URL,
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _make_rss_item(**overrides) -> ET.Element:
    """Build a minimal valid GDACS RSS <item> element for testing."""
    defaults = {
        'title': 'Green earthquake - Magnitude 5.9 - test region',
        'description': 'Test earthquake description',
        'link': 'https://www.gdacs.org/report.aspx?eventid=1533793',
        'pubDate': 'Mon, 07 Apr 2025 12:00:00 GMT',
        'gdacs:eventtype': 'EQ',
        'gdacs:eventid': '1533793',
        'gdacs:episodeid': '2001',
        'gdacs:alertlevel': 'Green',
        'gdacs:alertscore': '0.5',
        'gdacs:episodealertlevel': 'Green',
        'gdacs:episodealertscore': '0.4',
        'gdacs:eventname': 'Test Quake',
        'gdacs:country': 'Chile',
        'gdacs:iso3': 'CHL',
        'gdacs:fromdate': '2025-04-07T10:00:00Z',
        'gdacs:todate': '2025-04-07T12:00:00Z',
        'gdacs:iscurrent': 'true',
        'gdacs:version': '3',
        'gdacs:vulnerability': '1.2',
        'gdacs:bbox': '-72.0 -70.0 -35.0 -33.0',
        'geo:lat': '-34.5',
        'geo:long': '-71.2',
        'severity_value': '5.9',
        'severity_unit': 'M',
        'severity_text': 'Magnitude 5.9M, Depth:10km',
        'population_value': '250000',
        'population_unit': 'Pop',
    }
    defaults.update(overrides)

    item = ET.Element('item')
    for tag in ('title', 'description', 'link', 'pubDate'):
        el = ET.SubElement(item, tag)
        el.text = defaults[tag]

    # gdacs namespace elements
    gdacs_ns = NAMESPACES['gdacs']
    for field in ('eventtype', 'eventid', 'episodeid', 'alertlevel', 'alertscore',
                  'episodealertlevel', 'episodealertscore', 'eventname', 'country',
                  'iso3', 'fromdate', 'todate', 'iscurrent', 'version', 'vulnerability', 'bbox'):
        key = f'gdacs:{field}'
        if key in defaults and defaults[key] is not None:
            el = ET.SubElement(item, f'{{{gdacs_ns}}}{field}')
            el.text = defaults[key]

    # severity (with attributes)
    sev = ET.SubElement(item, f'{{{gdacs_ns}}}severity')
    sev.set('value', defaults['severity_value'])
    sev.set('unit', defaults['severity_unit'])
    sev.text = defaults.get('severity_text', '')

    # population (with attributes)
    pop = ET.SubElement(item, f'{{{gdacs_ns}}}population')
    pop.set('value', defaults['population_value'])
    pop.set('unit', defaults['population_unit'])

    # geo namespace
    geo_ns = NAMESPACES['geo']
    lat_el = ET.SubElement(item, f'{{{geo_ns}}}lat')
    lat_el.text = defaults['geo:lat']
    lon_el = ET.SubElement(item, f'{{{geo_ns}}}long')
    lon_el.text = defaults['geo:long']

    return item


def _make_rss_feed(*items: ET.Element) -> str:
    """Wrap items in a minimal RSS 2.0 feed document."""
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    title = ET.SubElement(channel, 'title')
    title.text = 'GDACS - Global Disaster Alert and Coordination System'
    for it in items:
        channel.append(it)
    return ET.tostring(rss, encoding='unicode')


# ── Low-level helpers ────────────────────────────────────────────────────────

class TestParseFloat:
    def test_valid(self):
        assert _parse_float('3.14') == pytest.approx(3.14)

    def test_none(self):
        assert _parse_float(None) is None

    def test_invalid(self):
        assert _parse_float('abc') is None

    def test_integer_string(self):
        assert _parse_float('42') == pytest.approx(42.0)

    def test_negative(self):
        assert _parse_float('-1.5') == pytest.approx(-1.5)


class TestParseInt:
    def test_valid(self):
        assert _parse_int('7') == 7

    def test_none(self):
        assert _parse_int(None) is None

    def test_invalid(self):
        assert _parse_int('xyz') is None

    def test_float_string(self):
        assert _parse_int('3.14') is None


class TestParseBool:
    def test_true_variants(self):
        assert _parse_bool('true') is True
        assert _parse_bool('True') is True
        assert _parse_bool('1') is True
        assert _parse_bool('yes') is True

    def test_false_variants(self):
        assert _parse_bool('false') is False
        assert _parse_bool('0') is False
        assert _parse_bool('no') is False

    def test_none(self):
        assert _parse_bool(None) is None


class TestParseDatetime:
    def test_rfc2822(self):
        result = _parse_datetime('Mon, 07 Apr 2025 12:00:00 GMT')
        assert result is not None
        assert '2025-04-07' in result

    def test_iso8601(self):
        result = _parse_datetime('2025-04-07T10:00:00Z')
        assert result is not None
        assert '2025-04-07' in result

    def test_none(self):
        assert _parse_datetime(None) is None

    def test_unparseable_returns_stripped(self):
        result = _parse_datetime('  some-weird-date  ')
        assert result == 'some-weird-date'


class TestParseBbox:
    def test_four_values(self):
        assert _parse_bbox('-72.0 -70.0 -35.0 -33.0') == (-72.0, -70.0, -35.0, -33.0)

    def test_comma_separated(self):
        assert _parse_bbox('-72.0,-70.0,-35.0,-33.0') == (-72.0, -70.0, -35.0, -33.0)

    def test_none(self):
        assert _parse_bbox(None) == (None, None, None, None)

    def test_empty(self):
        assert _parse_bbox('') == (None, None, None, None)

    def test_too_few_values(self):
        assert _parse_bbox('1.0 2.0') == (None, None, None, None)


class TestTextAndAttrHelpers:
    def test_text_found(self):
        item = _make_rss_item()
        assert _text(item, 'eventtype', 'gdacs') == 'EQ'

    def test_text_not_found(self):
        item = ET.Element('item')
        assert _text(item, 'eventtype', 'gdacs') is None

    def test_text_no_namespace(self):
        item = _make_rss_item()
        assert _text(item, 'title') is not None

    def test_attr_found(self):
        item = _make_rss_item()
        assert _attr(item, 'severity', 'gdacs', 'value') == '5.9'
        assert _attr(item, 'severity', 'gdacs', 'unit') == 'M'

    def test_attr_not_found(self):
        item = ET.Element('item')
        assert _attr(item, 'severity', 'gdacs', 'value') is None


# ── RSS item parsing ─────────────────────────────────────────────────────────

class TestParseRssItem:
    def test_full_item(self):
        item = _make_rss_item()
        alert = parse_rss_item(item)
        assert alert is not None
        assert alert.event_type == 'EQ'
        assert alert.event_id == '1533793'
        assert alert.episode_id == '2001'
        assert alert.alert_level == 'Green'
        assert alert.alert_score == pytest.approx(0.5)
        assert alert.episode_alert_level == 'Green'
        assert alert.episode_alert_score == pytest.approx(0.4)
        assert alert.event_name == 'Test Quake'
        assert alert.country == 'Chile'
        assert alert.iso3 == 'CHL'
        assert alert.latitude == pytest.approx(-34.5)
        assert alert.longitude == pytest.approx(-71.2)
        assert alert.severity_value == pytest.approx(5.9)
        assert alert.severity_unit == 'M'
        assert alert.severity_text is not None
        assert alert.population_value == pytest.approx(250000.0)
        assert alert.population_unit == 'Pop'
        assert alert.vulnerability == pytest.approx(1.2)
        assert alert.is_current is True
        assert alert.version == 3
        assert alert.link is not None
        assert alert.description is not None
        assert alert.pub_date is not None

    def test_missing_event_type(self):
        item = _make_rss_item(**{'gdacs:eventtype': None})
        # Rebuild without eventtype
        gdacs_ns = NAMESPACES['gdacs']
        el = item.find(f'{{{gdacs_ns}}}eventtype')
        if el is not None:
            item.remove(el)
        assert parse_rss_item(item) is None

    def test_missing_event_id(self):
        item = _make_rss_item()
        gdacs_ns = NAMESPACES['gdacs']
        el = item.find(f'{{{gdacs_ns}}}eventid')
        item.remove(el)
        assert parse_rss_item(item) is None

    def test_missing_alert_level(self):
        item = _make_rss_item()
        gdacs_ns = NAMESPACES['gdacs']
        el = item.find(f'{{{gdacs_ns}}}alertlevel')
        item.remove(el)
        assert parse_rss_item(item) is None

    def test_missing_latitude(self):
        item = _make_rss_item()
        geo_ns = NAMESPACES['geo']
        el = item.find(f'{{{geo_ns}}}lat')
        item.remove(el)
        assert parse_rss_item(item) is None

    def test_missing_longitude(self):
        item = _make_rss_item()
        geo_ns = NAMESPACES['geo']
        el = item.find(f'{{{geo_ns}}}long')
        item.remove(el)
        assert parse_rss_item(item) is None

    def test_missing_severity(self):
        item = _make_rss_item()
        gdacs_ns = NAMESPACES['gdacs']
        el = item.find(f'{{{gdacs_ns}}}severity')
        item.remove(el)
        assert parse_rss_item(item) is None

    def test_missing_from_date(self):
        item = _make_rss_item()
        gdacs_ns = NAMESPACES['gdacs']
        el = item.find(f'{{{gdacs_ns}}}fromdate')
        item.remove(el)
        assert parse_rss_item(item) is None

    def test_tropical_cyclone(self):
        item = _make_rss_item(**{
            'gdacs:eventtype': 'TC',
            'gdacs:eventid': '1042901',
            'severity_value': '185',
            'severity_unit': 'km/h',
        })
        alert = parse_rss_item(item)
        assert alert is not None
        assert alert.event_type == 'TC'
        assert alert.severity_value == pytest.approx(185.0)
        assert alert.severity_unit == 'km/h'

    def test_flood(self):
        item = _make_rss_item(**{
            'gdacs:eventtype': 'FL',
            'gdacs:eventid': '9000',
            'severity_value': '3.2',
            'severity_unit': 'm',
        })
        alert = parse_rss_item(item)
        assert alert is not None
        assert alert.event_type == 'FL'

    def test_volcano(self):
        item = _make_rss_item(**{
            'gdacs:eventtype': 'VO',
            'gdacs:eventid': '8001',
            'severity_value': '4',
            'severity_unit': 'VEI',
        })
        alert = parse_rss_item(item)
        assert alert is not None
        assert alert.event_type == 'VO'

    def test_missing_optional_fields(self):
        """Optional fields being absent should still produce a valid alert."""
        item = _make_rss_item()
        gdacs_ns = NAMESPACES['gdacs']
        # Remove optional elements
        for tag in ('episodeid', 'alertscore', 'episodealertlevel', 'episodealertscore',
                    'eventname', 'country', 'iso3', 'todate', 'vulnerability', 'bbox',
                    'iscurrent', 'version'):
            el = item.find(f'{{{gdacs_ns}}}{tag}')
            if el is not None:
                item.remove(el)
        # Remove population element
        el = item.find(f'{{{gdacs_ns}}}population')
        if el is not None:
            item.remove(el)
        alert = parse_rss_item(item)
        assert alert is not None
        assert alert.episode_id is None
        assert alert.alert_score is None
        assert alert.country is None
        assert alert.bbox_min_lon is None
        assert alert.vulnerability is None
        assert alert.population_value is None

    def test_bbox_parsing(self):
        item = _make_rss_item(**{'gdacs:bbox': '10.0 20.0 30.0 40.0'})
        alert = parse_rss_item(item)
        assert alert is not None
        assert alert.bbox_min_lon == pytest.approx(10.0)
        assert alert.bbox_max_lon == pytest.approx(20.0)
        assert alert.bbox_min_lat == pytest.approx(30.0)
        assert alert.bbox_max_lat == pytest.approx(40.0)

    def test_red_alert_level(self):
        item = _make_rss_item(**{'gdacs:alertlevel': 'Red', 'gdacs:alertscore': '2.8'})
        alert = parse_rss_item(item)
        assert alert is not None
        assert alert.alert_level == 'Red'
        assert alert.alert_score == pytest.approx(2.8)


# ── Feed parsing ─────────────────────────────────────────────────────────────

class TestParseFeed:
    def test_parse_multiple_items(self):
        i1 = _make_rss_item(**{'gdacs:eventid': '100'})
        i2 = _make_rss_item(**{'gdacs:eventid': '200', 'gdacs:eventtype': 'TC'})
        xml_text = _make_rss_feed(i1, i2)
        poller = GDACSPoller()
        alerts = poller.parse_feed(xml_text)
        assert len(alerts) == 2
        assert alerts[0].event_id == '100'
        assert alerts[1].event_id == '200'

    def test_empty_feed(self):
        xml_text = _make_rss_feed()
        poller = GDACSPoller()
        alerts = poller.parse_feed(xml_text)
        assert alerts == []

    def test_no_channel(self):
        xml_text = '<rss version="2.0"></rss>'
        poller = GDACSPoller()
        alerts = poller.parse_feed(xml_text)
        assert alerts == []

    def test_invalid_items_skipped(self):
        good = _make_rss_item()
        bad = ET.Element('item')  # empty, will fail parsing
        xml_text = _make_rss_feed(good, bad)
        poller = GDACSPoller()
        alerts = poller.parse_feed(xml_text)
        assert len(alerts) == 1


# ── State tracking ───────────────────────────────────────────────────────────

class TestStateTracking:
    def test_state_key_with_episode(self):
        item = _make_rss_item()
        alert = parse_rss_item(item)
        key = GDACSPoller._state_key(alert)
        assert key == 'EQ_1533793_2001'

    def test_state_key_without_episode(self):
        item = _make_rss_item()
        alert = parse_rss_item(item)
        alert.episode_id = None
        key = GDACSPoller._state_key(alert)
        assert key == 'EQ_1533793_0'

    def test_new_event_detected(self):
        """A brand-new event should be considered new (not in state)."""
        state: dict = {}
        item = _make_rss_item()
        alert = parse_rss_item(item)
        key = GDACSPoller._state_key(alert)
        assert key not in state

    def test_same_version_skipped(self):
        """An event with the same version should be skipped."""
        item = _make_rss_item(**{'gdacs:version': '3'})
        alert = parse_rss_item(item)
        state = {GDACSPoller._state_key(alert): 3}
        current_version = alert.version if alert.version is not None else 0
        assert state.get(GDACSPoller._state_key(alert), -1) >= current_version

    def test_updated_version_detected(self):
        """An event whose version incremented should be detected as updated."""
        item = _make_rss_item(**{'gdacs:version': '5'})
        alert = parse_rss_item(item)
        state = {GDACSPoller._state_key(alert): 3}
        current_version = alert.version if alert.version is not None else 0
        assert state.get(GDACSPoller._state_key(alert), -1) < current_version

    def test_load_state_empty(self, tmp_path):
        poller = GDACSPoller(state_file=str(tmp_path / 'nonexistent.json'))
        assert poller.load_state() == {}

    def test_save_and_load_state(self, tmp_path):
        path = str(tmp_path / 'state.json')
        poller = GDACSPoller(state_file=path)
        poller.save_state({'EQ_100_200': 5, 'TC_300_400': 2})
        loaded = poller.load_state()
        assert loaded == {'EQ_100_200': 5, 'TC_300_400': 2}

    def test_load_corrupt_state(self, tmp_path):
        path = tmp_path / 'state.json'
        path.write_text('not json', encoding='utf-8')
        poller = GDACSPoller(state_file=str(path))
        assert poller.load_state() == {}


# ── Connection string parsing ────────────────────────────────────────────────

class TestParseConnectionString:
    def test_event_hubs_connection_string(self):
        cs = 'Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=my-topic'
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'my-topic'
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == cs
        assert result['security.protocol'] == 'SASL_SSL'
        assert result['sasl.mechanism'] == 'PLAIN'

    def test_bootstrap_server_override(self):
        cs = 'BootstrapServer=broker1:9092;EntityPath=some-topic'
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'broker1:9092'
        assert result['kafka_topic'] == 'some-topic'

    def test_empty_string(self):
        result = parse_connection_string('')
        assert result == {}

    def test_missing_entity_path(self):
        cs = 'Endpoint=sb://ns.servicebus.windows.net/;SharedAccessKeyName=key;SharedAccessKey=secret'
        result = parse_connection_string(cs)
        assert 'kafka_topic' not in result
        assert result['bootstrap.servers'] == 'ns.servicebus.windows.net:9093'


# ── Poller initialization ───────────────────────────────────────────────────

class TestGDACSPollerInit:
    @patch('gdacs.gdacs.GDACSAlertsEventProducer')
    @patch('gdacs.gdacs.Producer')
    def test_init_with_kafka(self, mock_producer_cls, mock_event_producer_cls):
        kafka_config = {'bootstrap.servers': 'localhost:9092'}
        poller = GDACSPoller(kafka_config=kafka_config, kafka_topic='gdacs')
        mock_producer_cls.assert_called_once_with(kafka_config)
        mock_event_producer_cls.assert_called_once()
        assert poller.kafka_topic == 'gdacs'

    def test_init_without_kafka(self):
        poller = GDACSPoller()
        assert poller.event_producer is None
        assert poller.poll_interval == 300

    def test_custom_poll_interval(self):
        poller = GDACSPoller(poll_interval=60)
        assert poller.poll_interval == 60


# ── Async poll_and_send ─────────────────────────────────────────────────────

class TestPollAndSend:
    @pytest.mark.asyncio
    async def test_poll_once_emits_new_events(self, tmp_path):
        """poll_and_send with once=True should process the feed and return."""
        item = _make_rss_item(**{'gdacs:version': '1'})
        xml_text = _make_rss_feed(item)

        poller = GDACSPoller(state_file=str(tmp_path / 'state.json'))
        poller.fetch_feed = AsyncMock(return_value=xml_text)

        mock_producer = MagicMock()
        mock_producer.flush = MagicMock()
        mock_event_producer = MagicMock()
        mock_event_producer.producer = mock_producer
        mock_event_producer.send_gdacs_disaster_alert = AsyncMock()
        poller.event_producer = mock_event_producer

        await poller.poll_and_send(once=True)

        mock_event_producer.send_gdacs_disaster_alert.assert_called_once()
        mock_producer.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_poll_once_skips_seen(self, tmp_path):
        """Already-seen events at the same version should not be re-emitted."""
        item = _make_rss_item(**{'gdacs:version': '3'})
        xml_text = _make_rss_feed(item)

        state_path = tmp_path / 'state.json'
        import json
        state_path.write_text(json.dumps({'EQ_1533793_2001': 3}), encoding='utf-8')

        poller = GDACSPoller(state_file=str(state_path))
        poller.fetch_feed = AsyncMock(return_value=xml_text)

        mock_producer = MagicMock()
        mock_producer.flush = MagicMock()
        mock_event_producer = MagicMock()
        mock_event_producer.producer = mock_producer
        mock_event_producer.send_gdacs_disaster_alert = AsyncMock()
        poller.event_producer = mock_event_producer

        await poller.poll_and_send(once=True)

        mock_event_producer.send_gdacs_disaster_alert.assert_not_called()

    @pytest.mark.asyncio
    async def test_poll_once_detects_updated_version(self, tmp_path):
        """A version bump should cause re-emission."""
        item = _make_rss_item(**{'gdacs:version': '5'})
        xml_text = _make_rss_feed(item)

        state_path = tmp_path / 'state.json'
        import json
        state_path.write_text(json.dumps({'EQ_1533793_2001': 3}), encoding='utf-8')

        poller = GDACSPoller(state_file=str(state_path))
        poller.fetch_feed = AsyncMock(return_value=xml_text)

        mock_producer = MagicMock()
        mock_producer.flush = MagicMock()
        mock_event_producer = MagicMock()
        mock_event_producer.producer = mock_producer
        mock_event_producer.send_gdacs_disaster_alert = AsyncMock()
        poller.event_producer = mock_event_producer

        await poller.poll_and_send(once=True)

        mock_event_producer.send_gdacs_disaster_alert.assert_called_once()

    @pytest.mark.asyncio
    async def test_poll_once_with_fetch_error(self, tmp_path):
        """A fetch error should be logged and not crash in once mode."""
        poller = GDACSPoller(state_file=str(tmp_path / 'state.json'))
        poller.fetch_feed = AsyncMock(side_effect=Exception("network error"))

        await poller.poll_and_send(once=True)  # should not raise

    @pytest.mark.asyncio
    async def test_poll_once_no_producer(self, tmp_path):
        """poll_and_send should work without a producer (dry run)."""
        item = _make_rss_item()
        xml_text = _make_rss_feed(item)

        poller = GDACSPoller(state_file=str(tmp_path / 'state.json'))
        poller.fetch_feed = AsyncMock(return_value=xml_text)

        await poller.poll_and_send(once=True)
        state = poller.load_state()
        assert 'EQ_1533793_2001' in state


# ── Edge cases ───────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_severity_text_empty(self):
        item = _make_rss_item()
        gdacs_ns = NAMESPACES['gdacs']
        sev = item.find(f'{{{gdacs_ns}}}severity')
        sev.text = ''
        alert = parse_rss_item(item)
        assert alert is not None
        assert alert.severity_text is None or alert.severity_text == ''

    def test_zero_severity(self):
        item = _make_rss_item(**{'severity_value': '0'})
        alert = parse_rss_item(item)
        assert alert is not None
        assert alert.severity_value == pytest.approx(0.0)

    def test_negative_latitude(self):
        item = _make_rss_item(**{'geo:lat': '-89.99'})
        alert = parse_rss_item(item)
        assert alert is not None
        assert alert.latitude == pytest.approx(-89.99)

    def test_date_with_timezone_offset(self):
        result = _parse_datetime('2025-04-07T10:00:00+05:30')
        assert result is not None
        assert '2025-04-07' in result

    def test_event_types_cover_all(self):
        for etype in ('EQ', 'TC', 'FL', 'VO', 'FF', 'DR'):
            item = _make_rss_item(**{'gdacs:eventtype': etype})
            alert = parse_rss_item(item)
            assert alert is not None
            assert alert.event_type == etype
