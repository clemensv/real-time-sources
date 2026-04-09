"""
Unit tests for the USDA NRCS SNOTEL Snow and Weather bridge.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
from unittest.mock import Mock, patch, MagicMock, call
from datetime import datetime, timezone

from snotel_producer_data import Station, SnowObservation
from snotel.snotel import (
    SnotelPoller,
    parse_connection_string,
    parse_float,
    parse_csv_response,
    parse_observation_row,
    build_station_csv_url,
    DEFAULT_STATION_TRIPLETS,
    STATION_METADATA,
)


SAMPLE_CSV_TEXT = """\
#------------------------------------------------- WARNING --------------------------------------------
#
# The data you have obtained from this automated Natural Resources Conservation Service
# database are subject to revision regardless of indicated Quality Assurance level.
#
#------------------------------------------------------------------------------------------------------
#
# Reporting Frequency: Hourly
# Date Range: 2026-04-08 00:00 to 2026-04-08 03:00
#
# Data for the following site(s) are contained in this file:
#
#SNOTEL 838: University Camp, CO
#
Date,Snow Water Equivalent (in),Precipitation Accumulation (in),Air Temperature Observed (degF),Snow Depth (in)
2026-04-08 00:00,9.0,16.40,36.3,26
2026-04-08 01:00,9.0,16.40,36.1,26
2026-04-08 02:00,9.0,16.30,35.8,26
2026-04-08 03:00,9.0,16.40,34.7,26
"""

SAMPLE_CSV_MISSING_VALUES = """\
# Comment line
Date,Snow Water Equivalent (in),Precipitation Accumulation (in),Air Temperature Observed (degF),Snow Depth (in)
2026-04-08 00:00,9.0,,36.3,
2026-04-08 01:00,,16.40,,26
"""

SAMPLE_CSV_EMPTY = """\
# Only comments
# No data
"""

SAMPLE_CSV_HEADER_ONLY = """\
# Comment
Date,Snow Water Equivalent (in),Precipitation Accumulation (in),Air Temperature Observed (degF),Snow Depth (in)
"""


@pytest.mark.unit
class TestParseFloat:
    """Unit tests for the parse_float helper."""

    def test_parse_valid_float(self):
        assert parse_float("10.5") == 10.5

    def test_parse_integer(self):
        assert parse_float("42") == 42.0

    def test_parse_negative(self):
        assert parse_float("-3.2") == -3.2

    def test_parse_zero(self):
        assert parse_float("0") == 0.0

    def test_parse_empty_returns_none(self):
        assert parse_float("") is None

    def test_parse_none_returns_none(self):
        assert parse_float(None) is None

    def test_parse_whitespace_returns_none(self):
        assert parse_float("   ") is None

    def test_parse_nan_returns_none(self):
        assert parse_float("nan") is None

    def test_parse_NaN_returns_none(self):
        assert parse_float("NaN") is None

    def test_parse_invalid_string_returns_none(self):
        assert parse_float("abc") is None

    def test_parse_with_whitespace(self):
        assert parse_float("  9.0  ") == 9.0


@pytest.mark.unit
class TestBuildStationCsvUrl:
    """Unit tests for URL construction."""

    def test_basic_url(self):
        url = build_station_csv_url("838:CO:SNTL")
        assert "838:CO:SNTL" in url
        assert "WTEQ::value" in url
        assert "PREC::value" in url
        assert "TOBS::value" in url
        assert "SNWD::value" in url
        assert url.startswith("https://wcc.sc.egov.usda.gov/reportGenerator/view_csv")

    def test_alaska_station(self):
        url = build_station_csv_url("1107:AK:SNTL")
        assert "1107:AK:SNTL" in url

    def test_url_contains_hourly(self):
        url = build_station_csv_url("838:CO:SNTL")
        assert "/hourly/" in url

    def test_url_contains_date_range(self):
        url = build_station_csv_url("838:CO:SNTL")
        assert "/-1,0/" in url


@pytest.mark.unit
class TestParseCsvResponse:
    """Unit tests for CSV parsing."""

    def test_parse_sample_csv(self):
        headers, rows = parse_csv_response(SAMPLE_CSV_TEXT)
        assert len(headers) == 5
        assert headers[0] == "Date"
        assert len(rows) == 4

    def test_parse_first_data_row(self):
        _, rows = parse_csv_response(SAMPLE_CSV_TEXT)
        assert rows[0][0] == "2026-04-08 00:00"
        assert rows[0][1] == "9.0"
        assert rows[0][4] == "26"

    def test_parse_skips_comments(self):
        headers, rows = parse_csv_response(SAMPLE_CSV_TEXT)
        for h in headers:
            assert not h.startswith('#')
        for row in rows:
            assert not row[0].startswith('#')

    def test_parse_empty_csv(self):
        headers, rows = parse_csv_response(SAMPLE_CSV_EMPTY)
        assert headers == []
        assert rows == []

    def test_parse_header_only(self):
        headers, rows = parse_csv_response(SAMPLE_CSV_HEADER_ONLY)
        assert len(headers) == 5
        assert rows == []

    def test_parse_missing_values(self):
        _, rows = parse_csv_response(SAMPLE_CSV_MISSING_VALUES)
        assert len(rows) == 2
        assert rows[0][2] == ""
        assert rows[0][4] == ""
        assert rows[1][1] == ""

    def test_parse_completely_empty(self):
        headers, rows = parse_csv_response("")
        assert headers == []
        assert rows == []


@pytest.mark.unit
class TestParseObservationRow:
    """Unit tests for observation row parsing."""

    def test_parse_valid_row(self):
        row = ["2026-04-08 00:00", "9.0", "16.40", "36.3", "26"]
        obs = parse_observation_row("838:CO:SNTL", row)
        assert obs is not None
        assert obs.station_triplet == "838:CO:SNTL"
        assert obs.snow_water_equivalent == 9.0
        assert obs.precipitation == 16.40
        assert obs.air_temperature == 36.3
        assert obs.snow_depth == 26.0
        assert obs.date_time.year == 2026
        assert obs.date_time.month == 4
        assert obs.date_time.hour == 0

    def test_parse_missing_swe(self):
        row = ["2026-04-08 01:00", "", "16.40", "36.1", "26"]
        obs = parse_observation_row("838:CO:SNTL", row)
        assert obs is not None
        assert obs.snow_water_equivalent is None
        assert obs.precipitation == 16.40

    def test_parse_missing_all_values(self):
        row = ["2026-04-08 01:00", "", "", "", ""]
        obs = parse_observation_row("838:CO:SNTL", row)
        assert obs is not None
        assert obs.snow_water_equivalent is None
        assert obs.snow_depth is None
        assert obs.precipitation is None
        assert obs.air_temperature is None

    def test_parse_invalid_date(self):
        row = ["not-a-date", "9.0", "16.40", "36.3", "26"]
        obs = parse_observation_row("838:CO:SNTL", row)
        assert obs is None

    def test_parse_short_row(self):
        row = ["2026-04-08 00:00"]
        obs = parse_observation_row("838:CO:SNTL", row)
        assert obs is None

    def test_parse_empty_row(self):
        obs = parse_observation_row("838:CO:SNTL", [])
        assert obs is None

    def test_datetime_has_timezone(self):
        row = ["2026-04-08 00:00", "9.0", "16.40", "36.3", "26"]
        obs = parse_observation_row("838:CO:SNTL", row)
        assert obs.date_time.tzinfo is not None

    def test_parse_partial_row_three_values(self):
        row = ["2026-04-08 00:00", "9.0", "16.40"]
        obs = parse_observation_row("838:CO:SNTL", row)
        assert obs is not None
        assert obs.snow_water_equivalent == 9.0
        assert obs.precipitation == 16.40
        assert obs.air_temperature is None
        assert obs.snow_depth is None

    def test_negative_temperature(self):
        row = ["2026-04-08 00:00", "9.0", "16.40", "-5.2", "26"]
        obs = parse_observation_row("838:CO:SNTL", row)
        assert obs.air_temperature == -5.2


@pytest.mark.unit
class TestParseConnectionString:
    """Unit tests for connection string parsing."""

    def test_parse_eventhubs_connection_string(self):
        conn = "Endpoint=sb://myns.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=abc123;EntityPath=snotel"
        config, topic = parse_connection_string(conn)
        assert 'bootstrap.servers' in config
        assert topic == "snotel"
        assert config['security.protocol'] == 'SASL_SSL'

    def test_parse_plain_kafka_connection_string(self):
        conn = "BootstrapServer=localhost:9092;EntityPath=snotel-topic"
        config, topic = parse_connection_string(conn)
        assert config['bootstrap.servers'] == 'localhost:9092'
        assert topic == "snotel-topic"

    @patch.dict(os.environ, {"KAFKA_ENABLE_TLS": "false"})
    def test_parse_plain_kafka_with_tls_false(self):
        conn = "BootstrapServer=localhost:9092;EntityPath=test"
        config, topic = parse_connection_string(conn)
        assert config['security.protocol'] == 'PLAINTEXT'

    def test_parse_missing_topic(self):
        conn = "BootstrapServer=localhost:9092"
        config, topic = parse_connection_string(conn)
        assert config['bootstrap.servers'] == 'localhost:9092'
        assert topic == ''


@pytest.mark.unit
class TestStationMetadata:
    """Tests for the hardcoded station reference data."""

    def test_all_default_stations_have_metadata(self):
        for triplet in DEFAULT_STATION_TRIPLETS:
            assert triplet in STATION_METADATA, f"Missing metadata for {triplet}"

    def test_station_metadata_has_required_fields(self):
        for triplet, meta in STATION_METADATA.items():
            assert "name" in meta, f"Missing name for {triplet}"
            assert "state" in meta, f"Missing state for {triplet}"
            assert "elevation" in meta, f"Missing elevation for {triplet}"
            assert "latitude" in meta, f"Missing latitude for {triplet}"
            assert "longitude" in meta, f"Missing longitude for {triplet}"

    def test_station_triplet_format(self):
        for triplet in DEFAULT_STATION_TRIPLETS:
            parts = triplet.split(':')
            assert len(parts) == 3, f"Invalid triplet format: {triplet}"
            assert parts[2] == "SNTL", f"Network should be SNTL: {triplet}"

    def test_latitude_range(self):
        for triplet, meta in STATION_METADATA.items():
            assert 20.0 < meta["latitude"] < 72.0, f"Latitude out of range for {triplet}"

    def test_longitude_range(self):
        for triplet, meta in STATION_METADATA.items():
            assert -170.0 < meta["longitude"] < -100.0, f"Longitude out of range for {triplet}"


@pytest.mark.unit
class TestSnotelPollerInit:
    """Unit tests for SnotelPoller initialization."""

    @patch('snotel.snotel.GovUsdaNrcsSnotelEventProducer')
    @patch('confluent_kafka.Producer')
    def test_init(self, mock_producer_class, mock_event_producer):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer

        poller = SnotelPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test-topic',
            last_polled_file='test_state.json'
        )
        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == 'test_state.json'


@pytest.mark.unit
class TestSnotelPollerState:
    """Unit tests for state persistence."""

    @patch('snotel.snotel.GovUsdaNrcsSnotelEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_state_no_file(self, mock_producer_class, mock_event_producer, tmp_path):
        poller = SnotelPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test',
            last_polled_file=str(tmp_path / 'nonexistent.json')
        )
        state = poller.load_state()
        assert state == {"last_timestamps": {}}

    @patch('snotel.snotel.GovUsdaNrcsSnotelEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_state_existing(self, mock_producer_class, mock_event_producer, tmp_path):
        state_file = tmp_path / 'state.json'
        state_data = {"last_timestamps": {"838:CO:SNTL": "2026-04-08T03:00:00+00:00"}}
        state_file.write_text(json.dumps(state_data))

        poller = SnotelPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test',
            last_polled_file=str(state_file)
        )
        state = poller.load_state()
        assert state["last_timestamps"]["838:CO:SNTL"] == "2026-04-08T03:00:00+00:00"

    @patch('snotel.snotel.GovUsdaNrcsSnotelEventProducer')
    @patch('confluent_kafka.Producer')
    def test_save_state(self, mock_producer_class, mock_event_producer, tmp_path):
        state_file = tmp_path / 'state.json'

        poller = SnotelPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test',
            last_polled_file=str(state_file)
        )
        state = {"last_timestamps": {"838:CO:SNTL": "2026-04-08T03:00:00+00:00"}}
        poller.save_state(state)

        with open(state_file, 'r') as f:
            saved = json.load(f)
        assert saved["last_timestamps"]["838:CO:SNTL"] == "2026-04-08T03:00:00+00:00"

    @patch('snotel.snotel.GovUsdaNrcsSnotelEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_corrupt_state(self, mock_producer_class, mock_event_producer, tmp_path):
        state_file = tmp_path / 'corrupt.json'
        state_file.write_text("not valid json {{{")

        poller = SnotelPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test',
            last_polled_file=str(state_file)
        )
        state = poller.load_state()
        assert state == {"last_timestamps": {}}


@pytest.mark.unit
class TestSnotelPollerEmitStation:
    """Unit tests for station reference data emission."""

    @patch('snotel.snotel.GovUsdaNrcsSnotelEventProducer')
    @patch('confluent_kafka.Producer')
    def test_emit_station_reference(self, mock_producer_class, mock_event_producer):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer

        poller = SnotelPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test',
            last_polled_file='test_state.json'
        )

        mock_producer_instance = Mock()
        mock_producer_instance.producer = Mock()
        poller.producer = mock_producer_instance

        count = poller.emit_station_reference(["838:CO:SNTL", "669:CO:SNTL"])
        assert count == 2
        assert mock_producer_instance.send_gov_usda_nrcs_snotel_station.call_count == 2
        mock_producer_instance.producer.flush.assert_called_once()

    @patch('snotel.snotel.GovUsdaNrcsSnotelEventProducer')
    @patch('confluent_kafka.Producer')
    def test_emit_station_unknown_triplet(self, mock_producer_class, mock_event_producer):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer

        poller = SnotelPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test',
            last_polled_file='test_state.json'
        )

        mock_producer_instance = Mock()
        mock_producer_instance.producer = Mock()
        poller.producer = mock_producer_instance

        count = poller.emit_station_reference(["999:XX:SNTL"])
        assert count == 0


@pytest.mark.unit
class TestSnotelPollerPollStation:
    """Unit tests for station polling."""

    @patch('snotel.snotel.GovUsdaNrcsSnotelEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_station_emits_observations(self, mock_producer_class, mock_event_producer):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer

        poller = SnotelPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test',
            last_polled_file='test_state.json'
        )

        mock_producer_instance = Mock()
        mock_producer_instance.producer = Mock()
        poller.producer = mock_producer_instance
        poller.fetch_station_observations = Mock(return_value=SAMPLE_CSV_TEXT)

        state = {"last_timestamps": {}}
        count = poller.poll_station("838:CO:SNTL", state)
        assert count == 4
        assert mock_producer_instance.send_gov_usda_nrcs_snotel_snow_observation.call_count == 4
        assert "838:CO:SNTL" in state["last_timestamps"]

    @patch('snotel.snotel.GovUsdaNrcsSnotelEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_station_dedup(self, mock_producer_class, mock_event_producer):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer

        poller = SnotelPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test',
            last_polled_file='test_state.json'
        )

        mock_producer_instance = Mock()
        mock_producer_instance.producer = Mock()
        poller.producer = mock_producer_instance
        poller.fetch_station_observations = Mock(return_value=SAMPLE_CSV_TEXT)

        # Set state so first two rows are already seen
        state = {"last_timestamps": {"838:CO:SNTL": "2026-04-08T01:00:00+00:00"}}
        count = poller.poll_station("838:CO:SNTL", state)
        assert count == 2  # Only rows at 02:00 and 03:00

    @patch('snotel.snotel.GovUsdaNrcsSnotelEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_station_fetch_error(self, mock_producer_class, mock_event_producer):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer

        poller = SnotelPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test',
            last_polled_file='test_state.json'
        )

        import requests as req
        poller.fetch_station_observations = Mock(side_effect=req.RequestException("timeout"))
        mock_producer_instance = Mock()
        mock_producer_instance.producer = Mock()
        poller.producer = mock_producer_instance

        state = {"last_timestamps": {}}
        count = poller.poll_station("838:CO:SNTL", state)
        assert count == 0

    @patch('snotel.snotel.GovUsdaNrcsSnotelEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_station_with_missing_values(self, mock_producer_class, mock_event_producer):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer

        poller = SnotelPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test',
            last_polled_file='test_state.json'
        )

        mock_producer_instance = Mock()
        mock_producer_instance.producer = Mock()
        poller.producer = mock_producer_instance
        poller.fetch_station_observations = Mock(return_value=SAMPLE_CSV_MISSING_VALUES)

        state = {"last_timestamps": {}}
        count = poller.poll_station("838:CO:SNTL", state)
        assert count == 2


@pytest.mark.unit
class TestSnotelPollerPollAll:
    """Unit tests for poll_all."""

    @patch('snotel.snotel.GovUsdaNrcsSnotelEventProducer')
    @patch('confluent_kafka.Producer')
    def test_poll_all(self, mock_producer_class, mock_event_producer, tmp_path):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        state_file = tmp_path / 'state.json'

        poller = SnotelPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test',
            last_polled_file=str(state_file)
        )

        mock_producer_instance = Mock()
        mock_producer_instance.producer = Mock()
        poller.producer = mock_producer_instance
        poller.fetch_station_observations = Mock(return_value=SAMPLE_CSV_TEXT)

        total = poller.poll_all(["838:CO:SNTL", "669:CO:SNTL"])
        assert total == 8  # 4 rows * 2 stations


@pytest.mark.unit
class TestDataClasses:
    """Unit tests for generated data class behavior."""

    def test_station_creation(self):
        station = Station(
            station_triplet="838:CO:SNTL",
            name="University Camp",
            state="CO",
            elevation=10330.0,
            latitude=40.03,
            longitude=-105.57,
        )
        assert station.station_triplet == "838:CO:SNTL"
        assert station.name == "University Camp"
        assert station.elevation == 10330.0

    def test_station_serialization(self):
        station = Station(
            station_triplet="838:CO:SNTL",
            name="University Camp",
            state="CO",
            elevation=10330.0,
            latitude=40.03,
            longitude=-105.57,
        )
        d = station.to_serializer_dict()
        assert d["station_triplet"] == "838:CO:SNTL"
        assert d["elevation"] == 10330.0

    def test_snow_observation_creation(self):
        dt = datetime(2026, 4, 8, 0, 0, tzinfo=timezone.utc)
        obs = SnowObservation(
            station_triplet="838:CO:SNTL",
            date_time=dt,
            snow_water_equivalent=9.0,
            snow_depth=26.0,
            precipitation=16.40,
            air_temperature=36.3,
        )
        assert obs.station_triplet == "838:CO:SNTL"
        assert obs.snow_water_equivalent == 9.0
        assert obs.date_time == dt

    def test_snow_observation_nullable_fields(self):
        dt = datetime(2026, 4, 8, 0, 0, tzinfo=timezone.utc)
        obs = SnowObservation(
            station_triplet="838:CO:SNTL",
            date_time=dt,
            snow_water_equivalent=None,
            snow_depth=None,
            precipitation=None,
            air_temperature=None,
        )
        assert obs.snow_water_equivalent is None
        assert obs.snow_depth is None
        assert obs.precipitation is None
        assert obs.air_temperature is None

    def test_snow_observation_serialization(self):
        dt = datetime(2026, 4, 8, 0, 0, tzinfo=timezone.utc)
        obs = SnowObservation(
            station_triplet="838:CO:SNTL",
            date_time=dt,
            snow_water_equivalent=9.0,
            snow_depth=26.0,
            precipitation=16.40,
            air_temperature=36.3,
        )
        d = obs.to_serializer_dict()
        assert d["station_triplet"] == "838:CO:SNTL"
        assert d["snow_water_equivalent"] == 9.0

    def test_snow_observation_json_round_trip(self):
        dt = datetime(2026, 4, 8, 0, 0, tzinfo=timezone.utc)
        obs = SnowObservation(
            station_triplet="838:CO:SNTL",
            date_time=dt,
            snow_water_equivalent=9.0,
            snow_depth=26.0,
            precipitation=16.40,
            air_temperature=36.3,
        )
        json_str = obs.to_json()
        parsed = json.loads(json_str)
        assert parsed["station_triplet"] == "838:CO:SNTL"
        assert parsed["snow_water_equivalent"] == 9.0


@pytest.mark.unit
class TestDefaultStations:
    """Tests for default station list configuration."""

    def test_default_stations_not_empty(self):
        assert len(DEFAULT_STATION_TRIPLETS) > 0

    def test_default_stations_cover_multiple_states(self):
        states = {t.split(':')[1] for t in DEFAULT_STATION_TRIPLETS}
        assert len(states) >= 5

    def test_default_stations_unique(self):
        assert len(DEFAULT_STATION_TRIPLETS) == len(set(DEFAULT_STATION_TRIPLETS))
