"""
Unit tests for the Tokyo Docomo Bikeshare GBFS poller.
Tests core functionality without external dependencies.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call

from tokyo_docomo_bikeshare.tokyo_docomo_bikeshare import (
    DocomoBikesharePoller,
    parse_connection_string,
    SYSTEM_ID,
    DEFAULT_POLL_INTERVAL_SECONDS,
)
from tokyo_docomo_bikeshare_producer_data import BikeshareSystem, BikeshareStation, BikeshareStationStatus


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

SAMPLE_GBFS_MANIFEST = {
    "ttl": 10,
    "last_updated": 1700000000,
    "version": "2.3",
    "data": {
        "en": {
            "feeds": [
                {"name": "system_information", "url": "https://example.com/system_information.json"},
                {"name": "station_information", "url": "https://example.com/station_information.json"},
                {"name": "station_status", "url": "https://example.com/station_status.json"},
            ]
        }
    }
}

SAMPLE_SYSTEM_INFO = {
    "ttl": 60,
    "last_updated": 1700000000,
    "version": "2.3",
    "data": {
        "system_id": "docomo-cycle-tokyo",
        "language": "ja",
        "name": "ドコモ・バイクシェア",
        "short_name": "DocomoBike",
        "operator": "NTT Docomo, Inc.",
        "url": "https://docomo-cycle.jp/",
        "timezone": "Asia/Tokyo",
        "license_url": "https://example.com/license",
    }
}

SAMPLE_STATIONS = [
    {
        "station_id": "00010137",
        "name": "A4-01.東京駅八重洲口 / Tokyo Station Yaesu",
        "lat": 35.6804,
        "lon": 139.7704,
        "capacity": 40,
        "region_id": "1",
    },
    {
        "station_id": "00010138",
        "name": "A4-02.有楽町 / Yurakucho",
        "lat": 35.6750,
        "lon": 139.7636,
        "capacity": 20,
    },
]

SAMPLE_STATION_INFO = {
    "ttl": 60,
    "last_updated": 1700000000,
    "version": "2.3",
    "data": {"stations": SAMPLE_STATIONS},
}

SAMPLE_STATUSES = [
    {
        "station_id": "00010137",
        "num_bikes_available": 5,
        "num_docks_available": 35,
        "num_bikes_disabled": 0,
        "num_docks_disabled": 0,
        "is_installed": True,
        "is_renting": True,
        "is_returning": True,
        "last_reported": 1700000060,
    },
    {
        "station_id": "00010138",
        "num_bikes_available": 3,
        "num_docks_available": 17,
        "is_installed": True,
        "is_renting": True,
        "is_returning": True,
        "last_reported": 1700000060,
    },
]

SAMPLE_STATUS_PAYLOAD = {
    "ttl": 60,
    "last_updated": 1700000060,
    "version": "2.3",
    "data": {"stations": SAMPLE_STATUSES},
}


def _make_poller(kafka_config=None, topic="test-topic"):
    """Construct a DocomoBikesharePoller with mocked Kafka internals."""
    if kafka_config is None:
        kafka_config = {"bootstrap.servers": "localhost:9092"}
    with patch("confluent_kafka.Producer"), \
         patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareSystemEventProducer"), \
         patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareStationsEventProducer"):
        poller = DocomoBikesharePoller(kafka_config=kafka_config, kafka_topic=topic)
    return poller


# ---------------------------------------------------------------------------
# Connection string parsing
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseConnectionString:
    def test_plain_bootstrap_and_topic(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=my-topic"
        cfg = parse_connection_string(cs)
        assert cfg["bootstrap.servers"] == "localhost:9092"
        assert cfg["kafka_topic"] == "my-topic"
        assert "sasl.username" not in cfg

    def test_event_hubs_format(self):
        cs = (
            "Endpoint=sb://myhub.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=secretkey123;"
            "EntityPath=bikeshare-topic"
        )
        cfg = parse_connection_string(cs)
        assert "myhub" in cfg["bootstrap.servers"]
        assert cfg["kafka_topic"] == "bikeshare-topic"
        assert cfg["sasl.username"] == "$ConnectionString"
        assert "sasl.password" in cfg
        assert cfg["security.protocol"] == "SASL_SSL"

    def test_invalid_format_raises(self):
        # A part that contains 'BootstrapServer' but no '=' after the key will
        # cause an IndexError when split('=', 1)[1] is accessed, which the
        # function re-raises as ValueError.
        with pytest.raises(ValueError):
            parse_connection_string("BootstrapServer")


# ---------------------------------------------------------------------------
# Poller construction
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestDocomoBikesharePollerInit:
    def test_init_creates_both_producers(self):
        kafka_config = {"bootstrap.servers": "localhost:9092"}
        with patch("confluent_kafka.Producer") as mock_kp, \
             patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareSystemEventProducer") as mock_sys, \
             patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareStationsEventProducer") as mock_sta:
            poller = DocomoBikesharePoller(kafka_config=kafka_config, kafka_topic="t")
            assert mock_sys.called
            assert mock_sta.called
            assert poller.kafka_topic == "t"


# ---------------------------------------------------------------------------
# System information emission
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestEmitSystem:
    def test_emit_system_creates_correct_dataclass(self):
        poller = _make_poller()
        poller.system_producer = Mock()
        info = SAMPLE_SYSTEM_INFO["data"]
        poller._emit_system(info)
        poller.system_producer.send_jp_odpt_docomo_bikeshare_bikeshare_system.assert_called_once()
        args, kwargs = poller.system_producer.send_jp_odpt_docomo_bikeshare_bikeshare_system.call_args
        assert args[0] == "docomo-cycle-tokyo"
        system = args[1]
        assert isinstance(system, BikeshareSystem)
        assert system.system_id == "docomo-cycle-tokyo"
        assert system.name == "ドコモ・バイクシェア"
        assert system.timezone == "Asia/Tokyo"
        assert kwargs.get("flush_producer") is False

    def test_emit_system_uses_defaults_for_missing_fields(self):
        poller = _make_poller()
        poller.system_producer = Mock()
        poller._emit_system({"system_id": "docomo-cycle-tokyo", "language": "ja", "name": "Test", "timezone": "Asia/Tokyo"})
        args, _ = poller.system_producer.send_jp_odpt_docomo_bikeshare_bikeshare_system.call_args
        system = args[1]
        assert system.operator is None
        assert system.url is None


# ---------------------------------------------------------------------------
# Station information emission
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestEmitStations:
    def test_emit_stations_calls_send_for_each_station(self):
        poller = _make_poller()
        poller.stations_producer = Mock()
        poller._emit_stations(SAMPLE_STATIONS)
        assert poller.stations_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station.call_count == 2

    def test_emit_stations_passes_system_id_and_station_id(self):
        poller = _make_poller()
        poller.stations_producer = Mock()
        poller._emit_stations(SAMPLE_STATIONS)
        calls = poller.stations_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station.call_args_list
        system_ids = [c.args[0] for c in calls]
        station_ids = [c.args[1] for c in calls]
        assert all(sid == SYSTEM_ID for sid in system_ids)
        assert "00010137" in station_ids
        assert "00010138" in station_ids

    def test_emit_stations_skips_missing_station_id(self):
        poller = _make_poller()
        poller.stations_producer = Mock()
        stations = [{"station_id": "", "name": "Bad", "lat": 0.0, "lon": 0.0}]
        poller._emit_stations(stations)
        poller.stations_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station.assert_not_called()

    def test_emit_stations_station_has_system_id_field(self):
        poller = _make_poller()
        poller.stations_producer = Mock()
        poller._emit_stations(SAMPLE_STATIONS[:1])
        args, _ = poller.stations_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station.call_args
        station = args[2]
        assert isinstance(station, BikeshareStation)
        assert station.system_id == SYSTEM_ID
        assert station.station_id == "00010137"


# ---------------------------------------------------------------------------
# Station status emission and deduplication
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestEmitStationStatuses:
    def test_emit_all_on_first_call(self):
        poller = _make_poller()
        poller.stations_producer = Mock()
        count, pending = poller._emit_station_statuses(SAMPLE_STATUSES)
        assert count == 2
        assert len(pending) == 2

    def test_skips_unchanged_last_reported(self):
        poller = _make_poller()
        poller.stations_producer = Mock()
        # Prime the dedupe state
        poller._last_status = {"00010137": 1700000060, "00010138": 1700000060}
        count, pending = poller._emit_station_statuses(SAMPLE_STATUSES)
        assert count == 0
        assert len(pending) == 0
        poller.stations_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station_status.assert_not_called()

    def test_emits_only_updated_stations(self):
        poller = _make_poller()
        poller.stations_producer = Mock()
        poller._last_status = {"00010137": 1700000060}
        updated = list(SAMPLE_STATUSES)
        updated[1] = dict(updated[1], last_reported=1700000120)
        count, pending = poller._emit_station_statuses(updated)
        assert count == 1
        assert "00010138" in pending

    def test_status_payload_has_system_id_field(self):
        poller = _make_poller()
        poller.stations_producer = Mock()
        poller._emit_station_statuses(SAMPLE_STATUSES[:1])
        args, _ = poller.stations_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station_status.call_args
        status = args[2]
        assert isinstance(status, BikeshareStationStatus)
        assert status.system_id == SYSTEM_ID
        assert status.station_id == "00010137"

    def test_flush_producer_false(self):
        poller = _make_poller()
        poller.stations_producer = Mock()
        poller._emit_station_statuses(SAMPLE_STATUSES[:1])
        _, kwargs = poller.stations_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station_status.call_args
        assert kwargs.get("flush_producer") is False


# ---------------------------------------------------------------------------
# Flush-failure: dedupe state must NOT advance
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestFlushFailureDoesNotAdvanceState:
    def test_dedupe_state_unchanged_on_flush_failure(self):
        """When flush() returns non-zero, _last_status must not be updated."""
        kafka_config = {"bootstrap.servers": "localhost:9092"}
        with patch("confluent_kafka.Producer"), \
             patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareSystemEventProducer") as mock_sys_cls, \
             patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareStationsEventProducer") as mock_sta_cls:

            mock_kafka_producer = Mock()
            mock_kafka_producer.flush.return_value = 1  # non-zero: flush failure
            mock_sys_producer = Mock()
            mock_sys_producer.producer = mock_kafka_producer
            mock_sta_producer = Mock()

            mock_sys_cls.return_value = mock_sys_producer
            mock_sta_cls.return_value = mock_sta_producer

            poller = DocomoBikesharePoller(kafka_config=kafka_config, kafka_topic="t")

        # Pre-seed some state so reference refresh is not triggered
        poller._last_reference_emit = float('inf')

        with patch.object(poller, '_fetch_station_status', return_value=(SAMPLE_STATUSES, 60)), \
             patch.object(poller, '_fetch_feed_urls', return_value={
                 'system_information': 'http://x/si',
                 'station_information': 'http://x/sti',
                 'station_status': 'http://x/ss',
             }):
            poller.poll_and_send(once=True)

        # Dedupe state must remain empty because flush failed
        assert poller._last_status == {}

    def test_dedupe_state_advances_on_successful_flush(self):
        """When flush() returns 0, _last_status must be updated."""
        kafka_config = {"bootstrap.servers": "localhost:9092"}
        with patch("confluent_kafka.Producer"), \
             patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareSystemEventProducer") as mock_sys_cls, \
             patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareStationsEventProducer") as mock_sta_cls:

            mock_kafka_producer = Mock()
            mock_kafka_producer.flush.return_value = 0  # success
            mock_sys_producer = Mock()
            mock_sys_producer.producer = mock_kafka_producer
            mock_sta_producer = Mock()

            mock_sys_cls.return_value = mock_sys_producer
            mock_sta_cls.return_value = mock_sta_producer

            poller = DocomoBikesharePoller(kafka_config=kafka_config, kafka_topic="t")

        poller._last_reference_emit = float('inf')

        with patch.object(poller, '_fetch_station_status', return_value=(SAMPLE_STATUSES, 60)), \
             patch.object(poller, '_fetch_feed_urls', return_value={
                 'system_information': 'http://x/si',
                 'station_information': 'http://x/sti',
                 'station_status': 'http://x/ss',
             }):
            poller.poll_and_send(once=True)

        assert poller._last_status["00010137"] == 1700000060
        assert poller._last_status["00010138"] == 1700000060


# ---------------------------------------------------------------------------
# Reference refresh failure: cached data preserved
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestReferenceRefreshFailure:
    def test_station_cache_preserved_when_refresh_fails(self):
        """If station_information fetch fails, the old cache must survive."""
        kafka_config = {"bootstrap.servers": "localhost:9092"}
        with patch("confluent_kafka.Producer"), \
             patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareSystemEventProducer") as mock_sys_cls, \
             patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareStationsEventProducer") as mock_sta_cls:

            mock_kafka_producer = Mock()
            mock_kafka_producer.flush.return_value = 0
            mock_sys_producer = Mock()
            mock_sys_producer.producer = mock_kafka_producer
            mock_sta_producer = Mock()

            mock_sys_cls.return_value = mock_sys_producer
            mock_sta_cls.return_value = mock_sta_producer

            poller = DocomoBikesharePoller(kafka_config=kafka_config, kafka_topic="t")

        # Pre-populate cache with old data
        old_stations = list(SAMPLE_STATIONS)
        poller._cached_stations = old_stations

        # Force reference refresh by resetting timestamp
        poller._last_reference_emit = float("-inf")

        with patch.object(poller, '_fetch_feed_urls', return_value={
                 'system_information': 'http://x/si',
                 'station_information': 'http://x/sti',
                 'station_status': 'http://x/ss',
             }), \
             patch.object(poller, '_fetch_system_information', return_value=SAMPLE_SYSTEM_INFO["data"]), \
             patch.object(poller, '_fetch_station_information', return_value=None), \
             patch.object(poller, '_fetch_station_status', return_value=([], 60)):
            poller.poll_and_send(once=True)

        # Cache must still contain the old data
        assert poller._cached_stations is old_stations

    def test_station_cache_updated_when_refresh_succeeds(self):
        """If station_information fetch succeeds, the cache must be updated."""
        kafka_config = {"bootstrap.servers": "localhost:9092"}
        with patch("confluent_kafka.Producer"), \
             patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareSystemEventProducer") as mock_sys_cls, \
             patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareStationsEventProducer") as mock_sta_cls:

            mock_kafka_producer = Mock()
            mock_kafka_producer.flush.return_value = 0
            mock_sys_producer = Mock()
            mock_sys_producer.producer = mock_kafka_producer
            mock_sta_producer = Mock()

            mock_sys_cls.return_value = mock_sys_producer
            mock_sta_cls.return_value = mock_sta_producer

            poller = DocomoBikesharePoller(kafka_config=kafka_config, kafka_topic="t")

        new_stations = [{"station_id": "99999", "name": "New Station", "lat": 35.0, "lon": 139.0}]
        poller._last_reference_emit = float("-inf")

        with patch.object(poller, '_fetch_feed_urls', return_value={
                 'system_information': 'http://x/si',
                 'station_information': 'http://x/sti',
                 'station_status': 'http://x/ss',
             }), \
             patch.object(poller, '_fetch_system_information', return_value=SAMPLE_SYSTEM_INFO["data"]), \
             patch.object(poller, '_fetch_station_information', return_value=new_stations), \
             patch.object(poller, '_fetch_station_status', return_value=([], 60)):
            poller.poll_and_send(once=True)

        assert poller._cached_stations is new_stations


# ---------------------------------------------------------------------------
# Multi-producer wiring: one cycle exercises both event families
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestFullCycleWiring:
    def test_both_producer_classes_receive_calls(self):
        """One poll cycle must route events through both producer classes."""
        kafka_config = {"bootstrap.servers": "localhost:9092"}
        with patch("confluent_kafka.Producer"), \
             patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareSystemEventProducer") as mock_sys_cls, \
             patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareStationsEventProducer") as mock_sta_cls:

            mock_kafka_producer = Mock()
            mock_kafka_producer.flush.return_value = 0
            mock_sys_producer = Mock()
            mock_sys_producer.producer = mock_kafka_producer
            mock_sta_producer = Mock()

            mock_sys_cls.return_value = mock_sys_producer
            mock_sta_cls.return_value = mock_sta_producer

            poller = DocomoBikesharePoller(kafka_config=kafka_config, kafka_topic="t")

        poller._last_reference_emit = float("-inf")

        with patch.object(poller, '_fetch_feed_urls', return_value={
                 'system_information': 'http://x/si',
                 'station_information': 'http://x/sti',
                 'station_status': 'http://x/ss',
             }), \
             patch.object(poller, '_fetch_system_information', return_value=SAMPLE_SYSTEM_INFO["data"]), \
             patch.object(poller, '_fetch_station_information', return_value=SAMPLE_STATIONS), \
             patch.object(poller, '_fetch_station_status', return_value=(SAMPLE_STATUSES, 60)):
            poller.poll_and_send(once=True)

        # system_producer must have sent BikeshareSystem
        mock_sys_producer.send_jp_odpt_docomo_bikeshare_bikeshare_system.assert_called()
        # stations_producer must have sent BikeshareStation and BikeshareStationStatus
        mock_sta_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station.assert_called()
        mock_sta_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station_status.assert_called()


# ---------------------------------------------------------------------------
# Integration-style: parsing helpers
# ---------------------------------------------------------------------------

@pytest.mark.integration
class TestFetchSystemInformation:
    def test_parse_system_info_from_mock_response(self):
        import requests_mock as rm
        with rm.Mocker() as m:
            m.get("http://test/system_information.json", json=SAMPLE_SYSTEM_INFO)
            kafka_config = {"bootstrap.servers": "localhost:9092"}
            with patch("confluent_kafka.Producer"), \
                 patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareSystemEventProducer"), \
                 patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareStationsEventProducer"):
                poller = DocomoBikesharePoller(kafka_config=kafka_config, kafka_topic="t")
            result = poller._fetch_system_information("http://test/system_information.json")
            assert result is not None
            assert result["system_id"] == "docomo-cycle-tokyo"
            assert result["timezone"] == "Asia/Tokyo"

    def test_parse_station_information_from_mock_response(self):
        import requests_mock as rm
        with rm.Mocker() as m:
            m.get("http://test/station_information.json", json=SAMPLE_STATION_INFO)
            kafka_config = {"bootstrap.servers": "localhost:9092"}
            with patch("confluent_kafka.Producer"), \
                 patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareSystemEventProducer"), \
                 patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareStationsEventProducer"):
                poller = DocomoBikesharePoller(kafka_config=kafka_config, kafka_topic="t")
            result = poller._fetch_station_information("http://test/station_information.json")
            assert result is not None
            assert len(result) == 2
            assert result[0]["station_id"] == "00010137"

    def test_parse_station_status_from_mock_response(self):
        import requests_mock as rm
        with rm.Mocker() as m:
            m.get("http://test/station_status.json", json=SAMPLE_STATUS_PAYLOAD)
            kafka_config = {"bootstrap.servers": "localhost:9092"}
            with patch("confluent_kafka.Producer"), \
                 patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareSystemEventProducer"), \
                 patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareStationsEventProducer"):
                poller = DocomoBikesharePoller(kafka_config=kafka_config, kafka_topic="t")
            result, ttl = poller._fetch_station_status("http://test/station_status.json")
            assert result is not None
            assert len(result) == 2
            assert ttl == 60

    def test_fetch_feed_urls_fallback_on_failure(self):
        import requests_mock as rm
        with rm.Mocker() as m:
            m.get(
                "https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/gbfs.json",
                status_code=503
            )
            kafka_config = {"bootstrap.servers": "localhost:9092"}
            with patch("confluent_kafka.Producer"), \
                 patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareSystemEventProducer"), \
                 patch("tokyo_docomo_bikeshare.tokyo_docomo_bikeshare.JPODPTDocomoBikeshareStationsEventProducer"):
                poller = DocomoBikesharePoller(kafka_config=kafka_config, kafka_topic="t")
            urls = poller._fetch_feed_urls()
            assert "station_status" in urls
            assert "station_information" in urls
            assert "system_information" in urls
