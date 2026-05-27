"""
Unit tests for USGS Earthquake data poller.
Tests that don't require external dependencies or API calls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
from usgs_earthquakes.usgs_earthquakes import USGSEarthquakePoller, FEED_URLS, DEFAULT_FEED, parse_connection_string


@pytest.fixture
def mock_kafka_config():
    """Mock Kafka configuration for testing."""
    return {
        'bootstrap.servers': 'localhost:9092',
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': 'test_user',
        'sasl.password': 'test_password'
    }


class TestUSGSEarthquakePoller:
    """Test suite for USGSEarthquakePoller initialization and configuration."""

    @patch('usgs_earthquakes.usgs_earthquakes.USGSEarthquakesEventProducer')
    @patch('usgs_earthquakes.usgs_earthquakes.Producer')
    def test_init_with_kafka_config(self, mock_producer_class, mock_event_producer, mock_kafka_config):
        """Test USGSEarthquakePoller initialization with Kafka configuration."""
        mock_producer_instance = Mock()
        mock_producer_class.return_value = mock_producer_instance

        poller = USGSEarthquakePoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file='/tmp/test_last_polled.json',
            feed='all_hour'
        )

        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == '/tmp/test_last_polled.json'
        assert poller.feed == 'all_hour'
        assert poller.min_magnitude is None

        mock_producer_class.assert_called_once_with(mock_kafka_config)
        mock_event_producer.assert_called_once_with(mock_producer_instance, 'test-topic')

    def test_init_without_kafka_config(self):
        """Test USGSEarthquakePoller initialization without Kafka configuration."""
        poller = USGSEarthquakePoller(
            kafka_config=None,
            kafka_topic='test-topic',
            last_polled_file='/tmp/test_last_polled.json',
            feed='m4.5_hour'
        )

        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == '/tmp/test_last_polled.json'
        assert poller.feed == 'm4.5_hour'

    def test_init_with_min_magnitude(self, mock_kafka_config):
        """Test USGSEarthquakePoller initialization with magnitude filter."""
        with patch('usgs_earthquakes.usgs_earthquakes.Producer'):
            poller = USGSEarthquakePoller(
                kafka_config=mock_kafka_config,
                kafka_topic='test-topic',
                min_magnitude=2.5
            )
            assert poller.min_magnitude == 2.5


class TestFeedURLs:
    """Test available feed URL configuration."""

    def test_feed_urls_dict_structure(self):
        """Test that FEED_URLS dict is properly structured."""
        assert isinstance(FEED_URLS, dict)
        assert len(FEED_URLS) > 0

    def test_default_feed_exists(self):
        """Test that the default feed key exists in FEED_URLS."""
        assert DEFAULT_FEED in FEED_URLS

    def test_all_feeds_have_valid_urls(self):
        """Test that all feed URLs point to USGS earthquake service."""
        for name, url in FEED_URLS.items():
            assert url.startswith("https://earthquake.usgs.gov/"), f"Feed {name} has invalid URL"
            assert url.endswith(".geojson"), f"Feed {name} URL doesn't end with .geojson"

    def test_feed_categories_present(self):
        """Test that hour, day, week, and month feeds are present."""
        periods = ['hour', 'day', 'week', 'month']
        for period in periods:
            assert f"all_{period}" in FEED_URLS


class TestParseEvent:
    """Test GeoJSON feature parsing into Event objects."""

    def _make_feature(self, **overrides):
        """Helper to create a minimal valid GeoJSON feature."""
        feature = {
            "type": "Feature",
            "id": "us7000test",
            "properties": {
                "mag": 4.5,
                "place": "10km NE of Test City, CA",
                "time": 1700000000000,
                "updated": 1700000100000,
                "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us7000test",
                "detail": "https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=us7000test&format=geojson",
                "felt": 10,
                "cdi": 3.5,
                "mmi": 4.0,
                "alert": "green",
                "status": "reviewed",
                "tsunami": 0,
                "sig": 312,
                "net": "us",
                "code": "7000test",
                "sources": ",us,ci,",
                "nst": 25,
                "dmin": 0.5,
                "rms": 0.8,
                "gap": 45.0,
                "magType": "mww",
                "type": "earthquake",
            },
            "geometry": {
                "type": "Point",
                "coordinates": [-118.5, 34.1, 10.5]
            }
        }
        for key, value in overrides.items():
            if key in feature:
                feature[key] = value
            elif key in feature["properties"]:
                feature["properties"][key] = value
        return feature

    def test_parse_valid_event(self):
        """Test parsing a valid GeoJSON feature."""
        poller = USGSEarthquakePoller()
        feature = self._make_feature()
        event = poller.parse_event(feature)

        assert event is not None
        assert event.id == "us7000test"
        assert event.magnitude == 4.5
        assert event.mag_type == "mww"
        assert event.place == "10km NE of Test City, CA"
        assert event.net == "us"
        assert event.code == "7000test"
        assert event.latitude == 34.1
        assert event.longitude == -118.5
        assert event.depth == 10.5
        assert event.tsunami == 0
        assert event.status == "reviewed"
        assert event.alert == "green"

    def test_parse_event_with_null_magnitude(self):
        """Test parsing an event with null magnitude."""
        poller = USGSEarthquakePoller()
        feature = self._make_feature()
        feature["properties"]["mag"] = None
        event = poller.parse_event(feature)

        assert event is not None
        assert event.magnitude is None

    def test_parse_event_min_magnitude_filter(self):
        """Test that events below min_magnitude are filtered out."""
        poller = USGSEarthquakePoller(min_magnitude=5.0)
        feature = self._make_feature()  # mag=4.5
        event = poller.parse_event(feature)

        assert event is None

    def test_parse_event_above_min_magnitude(self):
        """Test that events at or above min_magnitude pass through."""
        poller = USGSEarthquakePoller(min_magnitude=4.0)
        feature = self._make_feature()  # mag=4.5
        event = poller.parse_event(feature)

        assert event is not None
        assert event.magnitude == 4.5

    def test_parse_event_missing_id(self):
        """Test that features without an ID return None."""
        poller = USGSEarthquakePoller()
        feature = self._make_feature()
        feature["id"] = ""
        event = poller.parse_event(feature)

        assert event is None

    def test_parse_event_time_conversion(self):
        """Test that epoch millisecond timestamps are converted to ISO-8601."""
        poller = USGSEarthquakePoller()
        feature = self._make_feature()
        feature["properties"]["time"] = 1700000000000  # 2023-11-14T22:13:20Z
        event = poller.parse_event(feature)

        assert event is not None
        assert "2023-11-14" in event.event_time
        assert "22:13:20" in event.event_time

    def test_parse_event_null_optional_fields(self):
        """Test parsing an event where optional fields are None."""
        poller = USGSEarthquakePoller()
        feature = self._make_feature()
        feature["properties"]["felt"] = None
        feature["properties"]["cdi"] = None
        feature["properties"]["mmi"] = None
        feature["properties"]["alert"] = None
        feature["properties"]["nst"] = None
        event = poller.parse_event(feature)

        assert event is not None
        assert event.felt is None
        assert event.cdi is None
        assert event.mmi is None
        assert event.alert is None
        assert event.nst is None


class TestConnectionStringParsing:
    """Test connection string parsing."""

    def test_parse_valid_connection_string(self):
        """Test parsing a valid Event Hubs connection string."""
        conn_str = "Endpoint=sb://my-namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=testkey123;EntityPath=my-topic"

        result = parse_connection_string(conn_str)

        assert 'bootstrap.servers' in result
        assert 'my-namespace.servicebus.windows.net:9093' in result['bootstrap.servers']
        assert result['kafka_topic'] == 'my-topic'
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == conn_str

    def test_parse_connection_string_without_entity_path(self):
        """Test parsing a connection string without EntityPath."""
        conn_str = "Endpoint=sb://my-namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=testkey123"

        result = parse_connection_string(conn_str)

        assert 'bootstrap.servers' in result
        assert 'kafka_topic' not in result


class TestEventDataClass:
    """Test Event dataclass methods."""

    def test_event_to_json(self):
        """Test Event serialization to JSON."""
        from usgs_earthquakes_producer_data.usgs.earthquakes.event import Event

        event = Event(
            id="us7000test",
            magnitude=4.5,
            mag_type="mww",
            place="Test City",
            event_time="2023-11-14T22:13:20+00:00",
            updated="2023-11-14T22:14:00+00:00",
            url="https://earthquake.usgs.gov/test",
            detail_url="https://earthquake.usgs.gov/test/detail",
            felt=10,
            cdi=3.5,
            mmi=4.0,
            alert="green",
            status="reviewed",
            tsunami=0,
            sig=312,
            net="us",
            code="7000test",
            sources=",us,",
            nst=25,
            dmin=0.5,
            rms=0.8,
            gap=45.0,
            event_type="earthquake",
            latitude=34.1,
            longitude=-118.5,
            depth=10.5
        )

        json_result = event.to_byte_array("application/json")
        assert json_result is not None
        json_str = json_result if isinstance(json_result, str) else json_result.decode('utf-8')
        assert "us7000test" in json_str
        assert "Test City" in json_str

    def test_event_to_avro(self):
        """Test Event serialization to Avro binary."""
        from usgs_earthquakes_producer_data.usgs.earthquakes.event import Event

        event = Event(
            id="us7000test",
            magnitude=4.5,
            mag_type="mww",
            place="Test City",
            event_time="2023-11-14T22:13:20+00:00",
            updated="2023-11-14T22:14:00+00:00",
            url=None,
            detail_url=None,
            felt=None,
            cdi=None,
            mmi=None,
            alert=None,
            status="automatic",
            tsunami=0,
            sig=None,
            net="us",
            code="7000test",
            sources=None,
            nst=None,
            dmin=None,
            rms=None,
            gap=None,
            event_type="earthquake",
            latitude=34.1,
            longitude=-118.5,
            depth=10.5
        )

        avro_bytes = event.to_byte_array("avro/binary")
        assert avro_bytes is not None
        assert len(avro_bytes) > 0
