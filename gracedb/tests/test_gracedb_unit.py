"""
Unit tests for GraceDB Gravitational Wave Candidate Alert poller.
Tests that don't require external dependencies or API calls.
"""

import json
import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
from gracedb.gracedb import (
    GraceDBPoller, BASE_API_URL, DEFAULT_POLL_COUNT,
    DEFAULT_CATEGORIES, parse_connection_string
)


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


def _make_raw_superevent(**overrides):
    """Helper to create a minimal valid raw superevent dict from the API."""
    raw = {
        "superevent_id": "MS260408x",
        "gw_id": None,
        "category": "MDC",
        "created": "2026-04-08 23:59:34 UTC",
        "submitter": "read-cvmfs-emfollow",
        "em_type": "M632681",
        "t_start": 1459726873.430086,
        "t_0": 1459726874.430086,
        "t_end": 1459726875.430086,
        "far": 6.786496426516116e-14,
        "time_coinc_far": 4.196368604676061e-18,
        "space_coinc_far": 5.042499300641276e-18,
        "labels": [
            "EM_READY", "ADVNO", "EM_COINC", "SKYMAP_READY",
            "EMBRIGHT_READY", "PASTRO_READY", "GCN_PRELIM_SENT",
            "RAVEN_ALERT", "DQR_REQUEST", "COMBINEDSKYMAP_READY",
            "HIGH_PROFILE", "SIGNIF_LOCKED", "LOW_SIGNIF_LOCKED"
        ],
        "links": {
            "labels": "https://gracedb.ligo.org/api/superevents/MS260408x/labels/",
            "logs": "https://gracedb.ligo.org/api/superevents/MS260408x/logs/",
            "files": "https://gracedb.ligo.org/api/superevents/MS260408x/files/",
            "self": "https://gracedb.ligo.org/api/superevents/MS260408x/",
            "voevents": "https://gracedb.ligo.org/api/superevents/MS260408x/voevents/",
            "emobservations": "https://gracedb.ligo.org/api/superevents/MS260408x/emobservations/"
        },
        "preferred_event_data": {
            "submitter": "read-cvmfs-emfollow",
            "created": "2026-04-08 23:59:33 UTC",
            "group": "CBC",
            "pipeline": "gstlal",
            "graceid": "M632680",
            "gpstime": 1459726874.430086,
            "reporting_latency": 1117.15517,
            "instruments": "H1,V1",
            "nevents": 2,
            "offline": False,
            "search": "MDC",
            "far": 6.786496426516116e-14,
            "far_is_upper_limit": False,
            "likelihood": 48.00926465985882,
            "labels": ["SKYMAP_READY", "EMBRIGHT_READY", "PASTRO_READY", "RAVEN_ALERT"],
        },
    }
    raw.update(overrides)
    return raw


@pytest.mark.unit
class TestGraceDBPollerInit:
    """Test suite for GraceDBPoller initialization and configuration."""

    @patch('gracedb.gracedb.OrgLigoGracedbEventProducer')
    @patch('gracedb.gracedb.Producer')
    def test_init_with_kafka_config(self, mock_producer_class, mock_event_producer, mock_kafka_config):
        """Test GraceDBPoller initialization with Kafka configuration."""
        mock_producer_instance = Mock()
        mock_producer_class.return_value = mock_producer_instance

        poller = GraceDBPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file='test_last_polled.json',
        )

        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == 'test_last_polled.json'
        assert poller.poll_count == DEFAULT_POLL_COUNT

        mock_producer_class.assert_called_once_with(mock_kafka_config)
        mock_event_producer.assert_called_once_with(mock_producer_instance, 'test-topic')

    def test_init_without_kafka_config(self):
        """Test GraceDBPoller initialization without Kafka configuration."""
        poller = GraceDBPoller(
            kafka_config=None,
            kafka_topic='test-topic',
            last_polled_file='test_last_polled.json',
        )

        assert poller.kafka_topic == 'test-topic'
        assert poller.event_producer is None

    def test_init_default_categories(self):
        """Test that default categories include Production and MDC."""
        poller = GraceDBPoller()
        assert "Production" in poller.categories
        assert "MDC" in poller.categories

    def test_init_custom_categories(self):
        """Test custom category configuration."""
        poller = GraceDBPoller(categories="Production")
        assert poller.categories == {"Production"}
        assert "MDC" not in poller.categories

    def test_init_custom_poll_count(self):
        """Test custom poll count."""
        poller = GraceDBPoller(poll_count=50)
        assert poller.poll_count == 50


@pytest.mark.unit
class TestConstants:
    """Test module-level constants."""

    def test_base_api_url(self):
        """Test that the base API URL points to GraceDB."""
        assert BASE_API_URL.startswith("https://gracedb.ligo.org/api/")
        assert "superevents" in BASE_API_URL

    def test_default_poll_count_reasonable(self):
        """Test that default poll count is a reasonable number."""
        assert 1 <= DEFAULT_POLL_COUNT <= 100

    def test_default_categories_string(self):
        """Test that default categories string is well-formed."""
        categories = DEFAULT_CATEGORIES.split(',')
        assert len(categories) >= 1
        assert "Production" in categories or "MDC" in categories


@pytest.mark.unit
class TestParseSuperevent:
    """Test raw API response parsing into Superevent objects."""

    def test_parse_valid_superevent(self):
        """Test parsing a complete valid superevent."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent()
        superevent = poller.parse_superevent(raw)

        assert superevent is not None
        assert superevent.superevent_id == "MS260408x"
        assert superevent.category == "MDC"
        assert superevent.created == "2026-04-08 23:59:34 UTC"
        assert superevent.t_0 == 1459726874.430086
        assert superevent.far == 6.786496426516116e-14
        assert superevent.pipeline == "gstlal"
        assert superevent.group == "CBC"
        assert superevent.instruments == "H1,V1"
        assert superevent.preferred_event_id == "M632680"
        assert superevent.submitter == "read-cvmfs-emfollow"

    def test_parse_labels_json(self):
        """Test that labels are serialized as a JSON array string."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent()
        superevent = poller.parse_superevent(raw)

        assert superevent is not None
        labels = json.loads(superevent.labels_json)
        assert isinstance(labels, list)
        assert "EM_READY" in labels
        assert "GCN_PRELIM_SENT" in labels

    def test_parse_empty_labels(self):
        """Test parsing a superevent with no labels."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent(labels=[])
        superevent = poller.parse_superevent(raw)

        assert superevent is not None
        assert superevent.labels_json == "[]"

    def test_parse_missing_superevent_id(self):
        """Test that events without an ID return None."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent(superevent_id="")
        superevent = poller.parse_superevent(raw)
        assert superevent is None

    def test_parse_missing_superevent_id_key(self):
        """Test that events without superevent_id key return None."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent()
        del raw["superevent_id"]
        superevent = poller.parse_superevent(raw)
        assert superevent is None

    def test_parse_category_filter_production(self):
        """Test that Production events pass through with default categories."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent(category="Production")
        superevent = poller.parse_superevent(raw)
        assert superevent is not None
        assert superevent.category == "Production"

    def test_parse_category_filter_test_excluded(self):
        """Test that Test events are excluded by default categories."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent(category="Test")
        superevent = poller.parse_superevent(raw)
        assert superevent is None

    def test_parse_category_filter_custom(self):
        """Test custom category filter."""
        poller = GraceDBPoller(categories="Test")
        raw = _make_raw_superevent(category="Test")
        superevent = poller.parse_superevent(raw)
        assert superevent is not None

    def test_parse_null_optional_fields(self):
        """Test parsing a superevent where optional fields are None."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent(
            gw_id=None,
            em_type=None,
            time_coinc_far=None,
            space_coinc_far=None,
        )
        raw["preferred_event_data"] = None
        superevent = poller.parse_superevent(raw)

        assert superevent is not None
        assert superevent.gw_id is None
        assert superevent.em_type is None
        assert superevent.time_coinc_far is None
        assert superevent.space_coinc_far is None
        assert superevent.preferred_event_id is None
        assert superevent.pipeline is None
        assert superevent.group is None

    def test_parse_gps_times(self):
        """Test that GPS times are correctly parsed as doubles."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent()
        superevent = poller.parse_superevent(raw)

        assert superevent is not None
        assert isinstance(superevent.t_start, float)
        assert isinstance(superevent.t_0, float)
        assert isinstance(superevent.t_end, float)
        assert superevent.t_start < superevent.t_0 < superevent.t_end

    def test_parse_far_value(self):
        """Test that FAR is parsed as a double."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent(far=1e-10)
        superevent = poller.parse_superevent(raw)

        assert superevent is not None
        assert isinstance(superevent.far, float)
        assert superevent.far == 1e-10

    def test_parse_self_uri(self):
        """Test that self_uri is extracted from links."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent()
        superevent = poller.parse_superevent(raw)

        assert superevent is not None
        assert "gracedb.ligo.org" in superevent.self_uri
        assert "MS260408x" in superevent.self_uri

    def test_parse_coinc_far_values(self):
        """Test parsing of coincidence FAR values."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent()
        superevent = poller.parse_superevent(raw)

        assert superevent is not None
        assert superevent.time_coinc_far == pytest.approx(4.196368604676061e-18)
        assert superevent.space_coinc_far == pytest.approx(5.042499300641276e-18)

    def test_parse_nevents(self):
        """Test parsing nevents from preferred_event_data."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent()
        superevent = poller.parse_superevent(raw)

        assert superevent is not None
        assert superevent.nevents == 2

    def test_parse_search_field(self):
        """Test parsing search field from preferred_event_data."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent()
        superevent = poller.parse_superevent(raw)

        assert superevent is not None
        assert superevent.search == "MDC"

    def test_parse_far_is_upper_limit(self):
        """Test parsing far_is_upper_limit field. Note: the generated dataclass
        converts False to None due to its truthiness check in __post_init__."""
        poller = GraceDBPoller()
        raw = _make_raw_superevent()
        # Set far_is_upper_limit to True so it survives the truthiness check
        raw["preferred_event_data"]["far_is_upper_limit"] = True
        superevent = poller.parse_superevent(raw)

        assert superevent is not None
        assert superevent.far_is_upper_limit is True


@pytest.mark.unit
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

    def test_parse_plain_bootstrap_connection_string(self):
        """Test parsing a plain Kafka bootstrap server connection string."""
        conn_str = "BootstrapServer=localhost:9092;EntityPath=gracedb"
        result = parse_connection_string(conn_str)

        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'gracedb'
        assert 'sasl.username' not in result


@pytest.mark.unit
class TestSeenIdsState:
    """Test seen ID state persistence."""

    def test_load_seen_ids_no_file(self):
        """Test loading when no file exists."""
        poller = GraceDBPoller(last_polled_file='nonexistent_file_xyz.json')
        seen = poller.load_seen_ids()
        assert seen == set()

    def test_load_seen_ids_no_file_configured(self):
        """Test loading when no file is configured."""
        poller = GraceDBPoller(last_polled_file=None)
        seen = poller.load_seen_ids()
        assert seen == set()

    def test_save_and_load_seen_ids(self, tmp_path):
        """Test round-trip save and load of seen IDs."""
        state_file = str(tmp_path / "seen.json")
        poller = GraceDBPoller(last_polled_file=state_file)

        test_ids = {"S240414a", "MS260408x", "S250101b"}
        poller.save_seen_ids(test_ids)

        loaded = poller.load_seen_ids()
        assert loaded == test_ids

    def test_load_seen_ids_corrupt_file(self, tmp_path):
        """Test loading from a corrupt JSON file."""
        state_file = str(tmp_path / "corrupt.json")
        with open(state_file, 'w') as f:
            f.write("not valid json{{{")

        poller = GraceDBPoller(last_polled_file=state_file)
        seen = poller.load_seen_ids()
        assert seen == set()


@pytest.mark.unit
class TestSupereventDataClass:
    """Test Superevent dataclass methods."""

    def test_superevent_to_json(self):
        """Test Superevent serialization to JSON."""
        from gracedb_producer_data.org.ligo.gracedb.superevent import Superevent

        superevent = Superevent(
            superevent_id="MS260408x",
            category="MDC",
            created="2026-04-08 23:59:34 UTC",
            t_start=1459726873.430086,
            t_0=1459726874.430086,
            t_end=1459726875.430086,
            far=6.786496426516116e-14,
            time_coinc_far=4.196368604676061e-18,
            space_coinc_far=5.042499300641276e-18,
            labels_json='["EM_READY","GCN_PRELIM_SENT"]',
            preferred_event_id="M632680",
            pipeline="gstlal",
            group="CBC",
            instruments="H1,V1",
            gw_id=None,
            submitter="read-cvmfs-emfollow",
            em_type=None,
            search="MDC",
            far_is_upper_limit=False,
            nevents=2,
            self_uri="https://gracedb.ligo.org/api/superevents/MS260408x/",
        )

        json_result = superevent.to_byte_array("application/json")
        assert json_result is not None
        json_str = json_result if isinstance(json_result, str) else json_result.decode('utf-8')
        assert "MS260408x" in json_str
        assert "gstlal" in json_str

    def test_superevent_to_avro(self):
        """Test Superevent serialization to Avro binary."""
        from gracedb_producer_data.org.ligo.gracedb.superevent import Superevent

        superevent = Superevent(
            superevent_id="MS260408x",
            category="MDC",
            created="2026-04-08 23:59:34 UTC",
            t_start=1459726873.430086,
            t_0=1459726874.430086,
            t_end=1459726875.430086,
            far=6.786496426516116e-14,
            time_coinc_far=None,
            space_coinc_far=None,
            labels_json='[]',
            preferred_event_id=None,
            pipeline=None,
            group=None,
            instruments=None,
            gw_id=None,
            submitter="read-cvmfs-emfollow",
            em_type=None,
            search=None,
            far_is_upper_limit=None,
            nevents=None,
            self_uri="https://gracedb.ligo.org/api/superevents/MS260408x/",
        )

        avro_bytes = superevent.to_byte_array("avro/binary")
        assert avro_bytes is not None
        assert len(avro_bytes) > 0

    def test_superevent_from_dict(self):
        """Test Superevent creation from dictionary."""
        from gracedb_producer_data.org.ligo.gracedb.superevent import Superevent

        data = {
            "superevent_id": "S240414a",
            "category": "Production",
            "created": "2024-04-14 10:00:00 UTC",
            "t_start": 1397000000.0,
            "t_0": 1397000001.0,
            "t_end": 1397000002.0,
            "far": 1e-20,
            "time_coinc_far": None,
            "space_coinc_far": None,
            "labels_json": "[]",
            "preferred_event_id": None,
            "pipeline": None,
            "group": None,
            "instruments": None,
            "gw_id": None,
            "submitter": "test",
            "em_type": None,
            "search": None,
            "far_is_upper_limit": None,
            "nevents": None,
            "self_uri": "https://gracedb.ligo.org/api/superevents/S240414a/",
        }

        superevent = Superevent.from_serializer_dict(data)
        assert superevent.superevent_id == "S240414a"
        assert superevent.category == "Production"
        assert superevent.far == 1e-20
