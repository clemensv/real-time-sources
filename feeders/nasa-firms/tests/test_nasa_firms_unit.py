"""
Unit tests for the NASA FIRMS active-fire poller.
Tests that don't require external dependencies or API calls.
"""

import pytest
from unittest.mock import Mock, patch

from nasa_firms.nasa_firms import (
    FirmsPoller,
    DEFAULT_SOURCES,
    SOURCE_META,
    confidence_level,
    geo_tile,
    parse_connection_string,
)
from nasa_firms_producer_data import (
    FireDetection,
    DataAvailability,
    InstrumentEnum,
    ConfidenceLevelenum,
    DaynightEnum,
)


@pytest.fixture
def mock_kafka_config():
    """Mock Kafka configuration for testing."""
    return {
        'bootstrap.servers': 'localhost:9092',
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': 'test_user',
        'sasl.password': 'test_password',
    }


def _viirs_row(**overrides):
    """A representative VIIRS_SNPP_NRT CSV row (DictReader output)."""
    row = {
        "latitude": "-12.345",
        "longitude": "34.567",
        "bright_ti4": "330.1",
        "scan": "0.45",
        "track": "0.39",
        "acq_date": "2024-01-15",
        "acq_time": "112",          # FIRMS emits HHMM without leading zero
        "satellite": "N",
        "instrument": "VIIRS",
        "confidence": "n",
        "version": "2.0NRT",
        "bright_ti5": "295.0",
        "frp": "12.7",
        "daynight": "D",
    }
    row.update(overrides)
    return row


def _modis_row(**overrides):
    """A representative MODIS_NRT CSV row (DictReader output)."""
    row = {
        "latitude": "55.10",
        "longitude": "-120.20",
        "brightness": "320.5",
        "scan": "1.1",
        "track": "1.0",
        "acq_date": "2024-01-15",
        "acq_time": "0935",
        "satellite": "Terra",
        "instrument": "MODIS",
        "confidence": "85",
        "version": "6.1NRT",
        "bright_t31": "290.1",
        "frp": "40.2",
        "daynight": "N",
    }
    row.update(overrides)
    return row


class TestFirmsPollerInit:
    """FirmsPoller construction and configuration."""

    @patch('nasa_firms.nasa_firms.NASAFIRMSEventProducer')
    @patch('nasa_firms.nasa_firms.Producer')
    def test_init_with_kafka_config(self, mock_producer_class, mock_event_producer, mock_kafka_config):
        mock_producer_instance = Mock()
        mock_producer_class.return_value = mock_producer_instance

        poller = FirmsPoller(
            map_key='abc',
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file='/tmp/test_seen.json',
        )

        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == '/tmp/test_seen.json'
        assert poller.sources == list(DEFAULT_SOURCES)
        mock_producer_class.assert_called_once_with(mock_kafka_config)
        mock_event_producer.assert_called_once_with(mock_producer_instance, 'test-topic')

    def test_init_without_kafka_config(self):
        poller = FirmsPoller(map_key='abc', kafka_topic='test-topic')
        assert poller.event_producer is None
        assert poller.kafka_topic == 'test-topic'

    def test_init_with_injected_event_producer(self):
        injected = Mock()
        poller = FirmsPoller(map_key='abc', event_producer=injected)
        assert poller.event_producer is injected

    def test_init_with_custom_sources(self):
        poller = FirmsPoller(sources=['MODIS_NRT'])
        assert poller.sources == ['MODIS_NRT']


class TestDefaultSources:
    """The configured global NRT source set."""

    def test_defaults_are_global_nrt(self):
        assert 'VIIRS_SNPP_NRT' in DEFAULT_SOURCES
        assert 'MODIS_NRT' in DEFAULT_SOURCES
        assert all(s.endswith('_NRT') for s in DEFAULT_SOURCES)

    def test_every_default_has_metadata(self):
        for src in DEFAULT_SOURCES:
            assert src in SOURCE_META
            instrument, satellite, resolution = SOURCE_META[src]
            assert instrument in ('VIIRS', 'MODIS')
            assert satellite
            assert resolution > 0


class TestConfidenceLevel:
    """Sensor-specific confidence normalization."""

    @pytest.mark.parametrize("raw,expected", [
        ("l", ConfidenceLevelenum.low),
        ("n", ConfidenceLevelenum.nominal),
        ("h", ConfidenceLevelenum.high),
        ("low", ConfidenceLevelenum.low),
        ("high", ConfidenceLevelenum.high),
    ])
    def test_viirs_letters(self, raw, expected):
        assert confidence_level("VIIRS", raw) == expected

    @pytest.mark.parametrize("raw,expected", [
        ("10", ConfidenceLevelenum.low),
        ("29", ConfidenceLevelenum.low),
        ("30", ConfidenceLevelenum.nominal),
        ("80", ConfidenceLevelenum.nominal),
        ("81", ConfidenceLevelenum.high),
        ("100", ConfidenceLevelenum.high),
    ])
    def test_modis_percent(self, raw, expected):
        assert confidence_level("MODIS", raw) == expected

    def test_none_defaults_nominal(self):
        assert confidence_level("VIIRS", None) == ConfidenceLevelenum.nominal

    def test_garbage_defaults_nominal(self):
        assert confidence_level("VIIRS", "???") == ConfidenceLevelenum.nominal


class TestGeoTile:
    """Coarse 10-degree tiling for geofencing."""

    def test_positive(self):
        assert geo_tile(12.3, 34.6) == "lat10_lon30"

    def test_negative(self):
        assert geo_tile(-12.3, -34.6) == "lat-20_lon-40"

    def test_zero(self):
        assert geo_tile(0.0, 0.0) == "lat0_lon0"


class TestParseDetection:
    """CSV row -> FireDetection parsing."""

    def test_parse_viirs(self):
        poller = FirmsPoller()
        det = poller.parse_detection("VIIRS_SNPP_NRT", _viirs_row())
        assert det is not None
        assert det.source == "VIIRS_SNPP_NRT"
        assert det.latitude == -12.345
        assert det.longitude == 34.567
        assert det.instrument == InstrumentEnum.VIIRS
        assert det.bright_ti4 == 330.1
        assert det.frp == 12.7
        assert det.confidence == "n"
        assert det.confidence_level == ConfidenceLevelenum.nominal
        assert det.daynight == DaynightEnum.D
        assert det.acq_time == "0112"  # zero-padded to HHMM
        assert det.acq_datetime == "2024-01-15T01:12:00Z"
        assert det.tile == geo_tile(-12.345, 34.567)
        assert len(det.record_id) == 16

    def test_parse_modis(self):
        poller = FirmsPoller()
        det = poller.parse_detection("MODIS_NRT", _modis_row())
        assert det is not None
        assert det.instrument == InstrumentEnum.MODIS
        assert det.brightness == 320.5
        assert det.bright_t31 == 290.1
        assert det.confidence == "85"
        assert det.confidence_level == ConfidenceLevelenum.high
        assert det.daynight == DaynightEnum.N

    def test_record_id_is_stable(self):
        poller = FirmsPoller()
        a = poller.parse_detection("VIIRS_SNPP_NRT", _viirs_row())
        b = poller.parse_detection("VIIRS_SNPP_NRT", _viirs_row())
        assert a.record_id == b.record_id

    def test_record_id_differs_by_location(self):
        poller = FirmsPoller()
        a = poller.parse_detection("VIIRS_SNPP_NRT", _viirs_row())
        b = poller.parse_detection("VIIRS_SNPP_NRT", _viirs_row(latitude="-12.346"))
        assert a.record_id != b.record_id

    def test_missing_coordinates_returns_none(self):
        poller = FirmsPoller()
        assert poller.parse_detection("VIIRS_SNPP_NRT", _viirs_row(latitude="")) is None
        assert poller.parse_detection("VIIRS_SNPP_NRT", _viirs_row(longitude="")) is None

    def test_unknown_daynight_is_none(self):
        poller = FirmsPoller()
        det = poller.parse_detection("VIIRS_SNPP_NRT", _viirs_row(daynight=""))
        assert det.daynight is None


class TestParseCsv:
    """Tolerant CSV parsing of FIRMS responses."""

    def test_parses_header_and_rows(self):
        text = "latitude,longitude,frp\n1.0,2.0,3.0\n4.0,5.0,6.0\n"
        rows = FirmsPoller._parse_csv(text)
        assert len(rows) == 2
        assert rows[0]["latitude"] == "1.0"

    def test_plaintext_error_returns_empty(self):
        # FIRMS returns plain-text errors (bad key/quota) with HTTP 200.
        assert FirmsPoller._parse_csv("Invalid MAP_KEY.") == []

    def test_empty_returns_empty(self):
        assert FirmsPoller._parse_csv("") == []


class TestConnectionStringParsing:
    """Connection string parsing."""

    def test_event_hubs_format(self):
        conn = ("Endpoint=sb://ns.servicebus.windows.net/;"
                "SharedAccessKeyName=Root;SharedAccessKey=key123;EntityPath=nasa-firms")
        result = parse_connection_string(conn)
        assert result['bootstrap.servers'] == 'ns.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'nasa-firms'
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == conn
        assert result['security.protocol'] == 'SASL_SSL'

    def test_bootstrap_server_format(self):
        conn = "BootstrapServer=localhost:9092;EntityPath=nasa-firms"
        result = parse_connection_string(conn)
        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'nasa-firms'


class TestDataClasses:
    """Generated dataclass serialization round-trips."""

    def _detection(self):
        return FirmsPoller().parse_detection("VIIRS_SNPP_NRT", _viirs_row())

    def test_fire_detection_to_json(self):
        det = self._detection()
        out = det.to_byte_array("application/json")
        text = out if isinstance(out, str) else out.decode("utf-8")
        assert "VIIRS_SNPP_NRT" in text
        assert det.record_id in text

    def test_data_availability_to_json(self):
        rec = DataAvailability(
            source="MODIS_NRT",
            record_id="coverage",
            data_id="MODIS_NRT",
            min_date="2024-01-01",
            max_date="2024-01-15",
            instrument=InstrumentEnum.MODIS,
            satellite="Terra/Aqua",
            resolution_m=1000.0,
            retrieved_at="2024-01-15T00:00:00+00:00",
        )
        out = rec.to_byte_array("application/json")
        text = out if isinstance(out, str) else out.decode("utf-8")
        assert "MODIS_NRT" in text
        assert "coverage" in text
