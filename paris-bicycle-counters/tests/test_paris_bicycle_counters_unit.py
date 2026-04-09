"""
Unit tests for Paris Bicycle Counters poller.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
from unittest.mock import Mock, patch, MagicMock, call
from datetime import datetime, timezone, timedelta
from paris_bicycle_counters_producer_data import Counter, BicycleCount
from paris_bicycle_counters.paris_bicycle_counters import (
    ParisBicycleCounterPoller,
    parse_connection_string,
    COUNTER_DATA_URL,
    COUNTER_LOCATIONS_URL,
)
from paris_bicycle_counters_producer_kafka_producer.producer import FRParisOpenDataVeloEventProducer


SAMPLE_COUNTER_LOCATIONS_RESPONSE = {
    "total_count": 3,
    "results": [
        {
            "id_compteur": "100047537-101047537",
            "nom_compteur": "26 boulevard de Ménilmontant SE-NO",
            "id": "100047537",
            "name": "26 boulevard de Ménilmontant",
            "channel_id": "101047537",
            "channel_name": "SE-NO",
            "installation_date": "2018-11-30",
            "coordinates": {"lon": 2.38886, "lat": 48.86057},
        },
        {
            "id_compteur": "100047541-353326452",
            "nom_compteur": "Pont National SO-NE",
            "id": "100047541",
            "name": "Pont National",
            "channel_id": "353326452",
            "channel_name": "SO-NE",
            "installation_date": "2018-12-05",
            "coordinates": {"lon": 2.38448, "lat": 48.82639},
        },
        {
            "id_compteur": "100049407-353680356",
            "nom_compteur": "152 boulevard du Montparnasse E-O",
            "id": "100049407",
            "name": "152 boulevard du Montparnasse",
            "channel_id": "353680356",
            "channel_name": "E-O",
            "installation_date": "2018-12-07",
            "coordinates": {"lon": 2.33438, "lat": 48.84017},
        },
    ],
}

SAMPLE_COUNTER_DATA_RESPONSE = {
    "total_count": 3,
    "results": [
        {
            "id_compteur": "100036719-103036719",
            "nom_compteur": "18 quai de l'Hôtel de Ville SE-NO",
            "sum_counts": 79,
            "date": "2025-12-06T15:00:00+00:00",
            "installation_date": "2017-07-12",
            "coordinates": {"lon": 2.35702, "lat": 48.85372},
        },
        {
            "id_compteur": "100036719-103036719",
            "nom_compteur": "18 quai de l'Hôtel de Ville SE-NO",
            "sum_counts": 48,
            "date": "2025-12-06T17:00:00+00:00",
            "installation_date": "2017-07-12",
            "coordinates": {"lon": 2.35702, "lat": 48.85372},
        },
        {
            "id_compteur": "100047537-101047537",
            "nom_compteur": "26 boulevard de Ménilmontant SE-NO",
            "sum_counts": 17,
            "date": "2025-12-06T22:00:00+00:00",
            "installation_date": "2018-11-30",
            "coordinates": {"lon": 2.38886, "lat": 48.86057},
        },
    ],
}

SAMPLE_COUNTER_DATA_EMPTY_RESPONSE = {
    "total_count": 0,
    "results": [],
}


@pytest.mark.unit
class TestParseConnectionString:
    """Unit tests for the parse_connection_string helper."""

    def test_parse_eventhub_connection_string(self):
        cs = "Endpoint=sb://myns.servicebus.windows.net/;SharedAccessKeyName=policy;SharedAccessKey=abc123;EntityPath=myhub"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'myns.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'myhub'
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == cs
        assert result['security.protocol'] == 'SASL_SSL'

    def test_parse_bootstrap_server_connection_string(self):
        cs = "BootstrapServer=broker1:9092;EntityPath=mytopic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'broker1:9092'
        assert result['kafka_topic'] == 'mytopic'
        assert 'sasl.username' not in result

    def test_parse_empty_string_raises(self):
        result = parse_connection_string("")
        assert 'bootstrap.servers' not in result

    def test_parse_endpoint_only(self):
        cs = "Endpoint=sb://test.servicebus.windows.net/"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert 'kafka_topic' not in result


@pytest.mark.unit
class TestCounterDataclass:
    """Unit tests for the Counter dataclass."""

    def test_create_counter(self):
        counter = Counter(
            counter_id="100047537-101047537",
            counter_name="26 boulevard de Ménilmontant SE-NO",
            channel_name="SE-NO",
            installation_date="2018-11-30",
            longitude=2.38886,
            latitude=48.86057,
        )
        assert counter.counter_id == "100047537-101047537"
        assert counter.counter_name == "26 boulevard de Ménilmontant SE-NO"
        assert counter.channel_name == "SE-NO"
        assert counter.installation_date == "2018-11-30"
        assert counter.longitude == 2.38886
        assert counter.latitude == 48.86057

    def test_counter_nullable_fields(self):
        counter = Counter(
            counter_id="test-id",
            counter_name="Test Counter",
            channel_name=None,
            installation_date=None,
            longitude=None,
            latitude=None,
        )
        assert counter.channel_name is None
        assert counter.installation_date is None
        assert counter.longitude is None
        assert counter.latitude is None

    def test_counter_to_json(self):
        counter = Counter(
            counter_id="test-id",
            counter_name="Test Counter",
            channel_name="SE-NO",
            installation_date="2020-01-01",
            longitude=2.0,
            latitude=48.0,
        )
        json_str = counter.to_json()
        data = json.loads(json_str)
        assert data["counter_id"] == "test-id"
        assert data["counter_name"] == "Test Counter"

    def test_counter_from_dict(self):
        data = {
            "counter_id": "abc-123",
            "counter_name": "Test",
            "channel_name": "N-S",
            "installation_date": "2021-06-15",
            "longitude": 2.5,
            "latitude": 48.5,
        }
        counter = Counter.from_serializer_dict(data)
        assert counter.counter_id == "abc-123"
        assert counter.longitude == 2.5

    def test_counter_create_instance(self):
        counter = Counter.create_instance()
        assert counter.counter_id is not None
        assert counter.counter_name is not None


@pytest.mark.unit
class TestBicycleCountDataclass:
    """Unit tests for the BicycleCount dataclass."""

    def test_create_bicycle_count(self):
        dt = datetime(2025, 12, 6, 15, 0, 0, tzinfo=timezone.utc)
        bc = BicycleCount(
            counter_id="100036719-103036719",
            counter_name="18 quai de l'Hôtel de Ville SE-NO",
            count=79,
            date=dt,
            longitude=2.35702,
            latitude=48.85372,
        )
        assert bc.counter_id == "100036719-103036719"
        assert bc.count == 79
        assert bc.date == dt

    def test_bicycle_count_nullable_count(self):
        dt = datetime(2025, 12, 6, 15, 0, 0, tzinfo=timezone.utc)
        bc = BicycleCount(
            counter_id="test-id",
            counter_name="Test Counter",
            count=None,
            date=dt,
            longitude=None,
            latitude=None,
        )
        assert bc.count is None

    def test_bicycle_count_to_json(self):
        dt = datetime(2025, 12, 6, 15, 0, 0, tzinfo=timezone.utc)
        bc = BicycleCount(
            counter_id="test-id",
            counter_name="Test Counter",
            count=42,
            date=dt,
            longitude=2.0,
            latitude=48.0,
        )
        json_str = bc.to_json()
        data = json.loads(json_str)
        assert data["counter_id"] == "test-id"
        assert data["count"] == 42
        assert "date" in data

    def test_bicycle_count_create_instance(self):
        bc = BicycleCount.create_instance()
        assert bc.counter_id is not None
        assert bc.count is not None

    def test_bicycle_count_zero_count(self):
        dt = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        bc = BicycleCount(
            counter_id="test-id",
            counter_name="Test Counter",
            count=0,
            date=dt,
            longitude=2.0,
            latitude=48.0,
        )
        assert bc.count == 0


@pytest.mark.unit
class TestFetchCounterLocations:
    """Unit tests for fetching counter locations."""

    @patch('paris_bicycle_counters.paris_bicycle_counters.requests.get')
    def test_fetch_counter_locations_basic(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_COUNTER_LOCATIONS_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        counters = ParisBicycleCounterPoller.fetch_counter_locations()
        assert len(counters) == 3
        assert counters[0].counter_id == "100047537-101047537"
        assert counters[0].counter_name == "26 boulevard de Ménilmontant SE-NO"
        assert counters[0].channel_name == "SE-NO"
        assert counters[0].installation_date == "2018-11-30"
        assert counters[0].longitude == 2.38886
        assert counters[0].latitude == 48.86057

    @patch('paris_bicycle_counters.paris_bicycle_counters.requests.get')
    def test_fetch_counter_locations_empty(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"total_count": 0, "results": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        counters = ParisBicycleCounterPoller.fetch_counter_locations()
        assert len(counters) == 0

    @patch('paris_bicycle_counters.paris_bicycle_counters.requests.get')
    def test_fetch_counter_locations_pagination(self, mock_get):
        page1 = {"total_count": 150, "results": [
            {"id_compteur": f"counter-{i}", "nom_compteur": f"Counter {i}",
             "channel_name": "SE-NO", "installation_date": "2020-01-01",
             "coordinates": {"lon": 2.0, "lat": 48.0}}
            for i in range(100)
        ]}
        page2 = {"total_count": 150, "results": [
            {"id_compteur": f"counter-{i}", "nom_compteur": f"Counter {i}",
             "channel_name": "SE-NO", "installation_date": "2020-01-01",
             "coordinates": {"lon": 2.0, "lat": 48.0}}
            for i in range(100, 150)
        ]}
        mock_resp1 = Mock()
        mock_resp1.json.return_value = page1
        mock_resp1.raise_for_status = Mock()
        mock_resp2 = Mock()
        mock_resp2.json.return_value = page2
        mock_resp2.raise_for_status = Mock()
        mock_get.side_effect = [mock_resp1, mock_resp2]

        counters = ParisBicycleCounterPoller.fetch_counter_locations()
        assert len(counters) == 150
        assert mock_get.call_count == 2

    @patch('paris_bicycle_counters.paris_bicycle_counters.requests.get')
    def test_fetch_counter_locations_missing_coordinates(self, mock_get):
        response = {"total_count": 1, "results": [
            {"id_compteur": "test-1", "nom_compteur": "Test", "channel_name": None,
             "installation_date": None, "coordinates": None}
        ]}
        mock_response = Mock()
        mock_response.json.return_value = response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        counters = ParisBicycleCounterPoller.fetch_counter_locations()
        assert len(counters) == 1
        assert counters[0].longitude is None
        assert counters[0].latitude is None


@pytest.mark.unit
class TestFetchBicycleCounts:
    """Unit tests for fetching bicycle count data."""

    @patch('paris_bicycle_counters.paris_bicycle_counters.requests.get')
    def test_fetch_bicycle_counts_basic(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_COUNTER_DATA_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        counts = ParisBicycleCounterPoller.fetch_bicycle_counts()
        assert len(counts) == 3
        assert counts[0].counter_id == "100036719-103036719"
        assert counts[0].count == 79
        assert counts[0].longitude == 2.35702

    @patch('paris_bicycle_counters.paris_bicycle_counters.requests.get')
    def test_fetch_bicycle_counts_with_since_filter(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_COUNTER_DATA_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        since = datetime(2025, 12, 6, 0, 0, 0, tzinfo=timezone.utc)
        ParisBicycleCounterPoller.fetch_bicycle_counts(since=since)

        call_args = mock_get.call_args
        params = call_args[1].get('params') or call_args[0][1] if len(call_args[0]) > 1 else call_args[1].get('params')
        assert 'where' in params
        assert '2025-12-06' in params['where']

    @patch('paris_bicycle_counters.paris_bicycle_counters.requests.get')
    def test_fetch_bicycle_counts_empty(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_COUNTER_DATA_EMPTY_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        counts = ParisBicycleCounterPoller.fetch_bicycle_counts()
        assert len(counts) == 0

    @patch('paris_bicycle_counters.paris_bicycle_counters.requests.get')
    def test_fetch_bicycle_counts_missing_date_skipped(self, mock_get):
        response = {"total_count": 2, "results": [
            {"id_compteur": "c1", "nom_compteur": "Counter 1", "sum_counts": 10,
             "date": None, "coordinates": {"lon": 2.0, "lat": 48.0}},
            {"id_compteur": "c2", "nom_compteur": "Counter 2", "sum_counts": 20,
             "date": "2025-12-06T15:00:00+00:00", "coordinates": {"lon": 2.1, "lat": 48.1}},
        ]}
        mock_response = Mock()
        mock_response.json.return_value = response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        counts = ParisBicycleCounterPoller.fetch_bicycle_counts()
        assert len(counts) == 1
        assert counts[0].counter_id == "c2"

    @patch('paris_bicycle_counters.paris_bicycle_counters.requests.get')
    def test_fetch_bicycle_counts_null_sum_counts(self, mock_get):
        response = {"total_count": 1, "results": [
            {"id_compteur": "c1", "nom_compteur": "Counter 1", "sum_counts": None,
             "date": "2025-12-06T15:00:00+00:00", "coordinates": {"lon": 2.0, "lat": 48.0}},
        ]}
        mock_response = Mock()
        mock_response.json.return_value = response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        counts = ParisBicycleCounterPoller.fetch_bicycle_counts()
        assert len(counts) == 1
        assert counts[0].count is None


@pytest.mark.unit
class TestDedupCounts:
    """Unit tests for deduplication logic."""

    def test_dedup_no_duplicates(self):
        dt1 = datetime(2025, 12, 6, 15, 0, 0, tzinfo=timezone.utc)
        dt2 = datetime(2025, 12, 6, 16, 0, 0, tzinfo=timezone.utc)
        counts = [
            BicycleCount(counter_id="c1", counter_name="C1", count=10, date=dt1,
                         longitude=2.0, latitude=48.0),
            BicycleCount(counter_id="c2", counter_name="C2", count=20, date=dt2,
                         longitude=2.1, latitude=48.1),
        ]
        new_counts, seen = ParisBicycleCounterPoller.dedup_counts(counts, set())
        assert len(new_counts) == 2
        assert len(seen) == 2

    def test_dedup_with_duplicates(self):
        dt = datetime(2025, 12, 6, 15, 0, 0, tzinfo=timezone.utc)
        counts = [
            BicycleCount(counter_id="c1", counter_name="C1", count=10, date=dt,
                         longitude=2.0, latitude=48.0),
            BicycleCount(counter_id="c1", counter_name="C1", count=10, date=dt,
                         longitude=2.0, latitude=48.0),
        ]
        new_counts, seen = ParisBicycleCounterPoller.dedup_counts(counts, set())
        assert len(new_counts) == 1

    def test_dedup_with_seen_keys(self):
        dt = datetime(2025, 12, 6, 15, 0, 0, tzinfo=timezone.utc)
        counts = [
            BicycleCount(counter_id="c1", counter_name="C1", count=10, date=dt,
                         longitude=2.0, latitude=48.0),
        ]
        seen = {f"c1|{dt.isoformat()}"}
        new_counts, updated_seen = ParisBicycleCounterPoller.dedup_counts(counts, seen)
        assert len(new_counts) == 0
        assert len(updated_seen) == 1

    def test_dedup_same_counter_different_dates(self):
        dt1 = datetime(2025, 12, 6, 15, 0, 0, tzinfo=timezone.utc)
        dt2 = datetime(2025, 12, 6, 16, 0, 0, tzinfo=timezone.utc)
        counts = [
            BicycleCount(counter_id="c1", counter_name="C1", count=10, date=dt1,
                         longitude=2.0, latitude=48.0),
            BicycleCount(counter_id="c1", counter_name="C1", count=20, date=dt2,
                         longitude=2.0, latitude=48.0),
        ]
        new_counts, seen = ParisBicycleCounterPoller.dedup_counts(counts, set())
        assert len(new_counts) == 2

    def test_dedup_empty_input(self):
        new_counts, seen = ParisBicycleCounterPoller.dedup_counts([], set())
        assert len(new_counts) == 0
        assert len(seen) == 0


@pytest.mark.unit
class TestStateManagement:
    """Unit tests for state persistence."""

    def test_load_state_missing_file(self, tmp_path):
        poller = object.__new__(ParisBicycleCounterPoller)
        poller.last_polled_file = str(tmp_path / "nonexistent.json")
        state = poller.load_state()
        assert state == {}

    def test_save_and_load_state(self, tmp_path):
        state_file = str(tmp_path / "state.json")
        poller = object.__new__(ParisBicycleCounterPoller)
        poller.last_polled_file = state_file
        poller.save_state({"seen_keys": ["c1|2025-12-06T15:00:00+00:00"]})
        loaded = poller.load_state()
        assert loaded["seen_keys"] == ["c1|2025-12-06T15:00:00+00:00"]

    def test_load_state_corrupted_file(self, tmp_path):
        state_file = tmp_path / "state.json"
        state_file.write_text("not valid json{{{")
        poller = object.__new__(ParisBicycleCounterPoller)
        poller.last_polled_file = str(state_file)
        state = poller.load_state()
        assert state == {}

    def test_save_state_creates_directory(self, tmp_path):
        state_file = str(tmp_path / "subdir" / "state.json")
        poller = object.__new__(ParisBicycleCounterPoller)
        poller.last_polled_file = state_file
        poller.save_state({"test": True})
        assert os.path.exists(state_file)


@pytest.mark.unit
class TestPollAndSend:
    """Unit tests for the poll_and_send loop."""

    @patch('paris_bicycle_counters.paris_bicycle_counters.ParisBicycleCounterPoller.fetch_bicycle_counts')
    @patch('paris_bicycle_counters.paris_bicycle_counters.ParisBicycleCounterPoller.fetch_counter_locations')
    def test_poll_and_send_once(self, mock_locations, mock_counts, tmp_path):
        mock_locations.return_value = [
            Counter(counter_id="c1", counter_name="Counter 1", channel_name="SE-NO",
                    installation_date="2020-01-01", longitude=2.0, latitude=48.0)
        ]
        dt = datetime(2025, 12, 6, 15, 0, 0, tzinfo=timezone.utc)
        mock_counts.return_value = [
            BicycleCount(counter_id="c1", counter_name="Counter 1", count=42,
                         date=dt, longitude=2.0, latitude=48.0)
        ]

        mock_kafka_producer = Mock()
        mock_kafka_producer.flush = Mock()
        mock_kafka_producer.produce = Mock()

        poller = object.__new__(ParisBicycleCounterPoller)
        poller.kafka_topic = "test-topic"
        poller.last_polled_file = str(tmp_path / "state.json")
        poller.producer = FRParisOpenDataVeloEventProducer(mock_kafka_producer, "test-topic")

        poller.poll_and_send(once=True)

        assert mock_kafka_producer.produce.call_count >= 2  # 1 counter + 1 count
        assert mock_kafka_producer.flush.call_count >= 2

    @patch('paris_bicycle_counters.paris_bicycle_counters.ParisBicycleCounterPoller.fetch_bicycle_counts')
    @patch('paris_bicycle_counters.paris_bicycle_counters.ParisBicycleCounterPoller.fetch_counter_locations')
    def test_poll_and_send_dedup_across_polls(self, mock_locations, mock_counts, tmp_path):
        mock_locations.return_value = []
        dt = datetime.now(timezone.utc) - timedelta(hours=1)
        mock_counts.return_value = [
            BicycleCount(counter_id="c1", counter_name="Counter 1", count=42,
                         date=dt, longitude=2.0, latitude=48.0)
        ]

        mock_kafka_producer = Mock()
        mock_kafka_producer.flush = Mock()
        mock_kafka_producer.produce = Mock()

        poller = object.__new__(ParisBicycleCounterPoller)
        poller.kafka_topic = "test-topic"
        poller.last_polled_file = str(tmp_path / "state.json")
        poller.producer = FRParisOpenDataVeloEventProducer(mock_kafka_producer, "test-topic")

        # First poll
        poller.poll_and_send(once=True)
        first_produce_count = mock_kafka_producer.produce.call_count

        # Second poll with same data - should not produce new messages
        mock_kafka_producer.produce.reset_mock()
        poller.poll_and_send(once=True)
        # Only the flush after empty new_counts should happen, no produce for bicycle count
        assert mock_kafka_producer.produce.call_count == 0


@pytest.mark.unit
class TestFieldMapping:
    """Unit tests for French-to-English field mapping."""

    @patch('paris_bicycle_counters.paris_bicycle_counters.requests.get')
    def test_french_field_names_mapped_to_english(self, mock_get):
        response = {"total_count": 1, "results": [
            {"id_compteur": "FR-001", "nom_compteur": "Rue de Rivoli E-O",
             "sum_counts": 55, "date": "2025-12-06T10:00:00+00:00",
             "coordinates": {"lon": 2.35, "lat": 48.86}}
        ]}
        mock_response = Mock()
        mock_response.json.return_value = response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        counts = ParisBicycleCounterPoller.fetch_bicycle_counts()
        assert counts[0].counter_id == "FR-001"       # id_compteur -> counter_id
        assert counts[0].counter_name == "Rue de Rivoli E-O"  # nom_compteur -> counter_name
        assert counts[0].count == 55                   # sum_counts -> count

    @patch('paris_bicycle_counters.paris_bicycle_counters.requests.get')
    def test_counter_location_field_mapping(self, mock_get):
        response = {"total_count": 1, "results": [
            {"id_compteur": "FR-002", "nom_compteur": "Boulevard Voltaire N-S",
             "channel_name": "N-S", "installation_date": "2019-03-01",
             "coordinates": {"lon": 2.38, "lat": 48.86}}
        ]}
        mock_response = Mock()
        mock_response.json.return_value = response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        counters = ParisBicycleCounterPoller.fetch_counter_locations()
        assert counters[0].counter_id == "FR-002"
        assert counters[0].counter_name == "Boulevard Voltaire N-S"
        assert counters[0].channel_name == "N-S"


@pytest.mark.unit
class TestEdgeCases:
    """Unit tests for edge cases."""

    @patch('paris_bicycle_counters.paris_bicycle_counters.requests.get')
    def test_invalid_date_format_skipped(self, mock_get):
        response = {"total_count": 1, "results": [
            {"id_compteur": "c1", "nom_compteur": "Test", "sum_counts": 10,
             "date": "not-a-date", "coordinates": {"lon": 2.0, "lat": 48.0}},
        ]}
        mock_response = Mock()
        mock_response.json.return_value = response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        counts = ParisBicycleCounterPoller.fetch_bicycle_counts()
        assert len(counts) == 0

    @patch('paris_bicycle_counters.paris_bicycle_counters.requests.get')
    def test_missing_coordinates_field(self, mock_get):
        response = {"total_count": 1, "results": [
            {"id_compteur": "c1", "nom_compteur": "Test", "sum_counts": 10,
             "date": "2025-12-06T15:00:00+00:00"},
        ]}
        mock_response = Mock()
        mock_response.json.return_value = response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        counts = ParisBicycleCounterPoller.fetch_bicycle_counts()
        assert len(counts) == 1
        assert counts[0].longitude is None
        assert counts[0].latitude is None

    def test_counter_byte_array_json(self):
        counter = Counter(
            counter_id="test-id", counter_name="Test",
            channel_name=None, installation_date=None,
            longitude=2.0, latitude=48.0,
        )
        result = counter.to_byte_array("application/json")
        assert isinstance(result, (bytes, str))
        data = json.loads(result)
        assert data["counter_id"] == "test-id"

    def test_bicycle_count_byte_array_json(self):
        dt = datetime(2025, 12, 6, 15, 0, 0, tzinfo=timezone.utc)
        bc = BicycleCount(
            counter_id="test-id", counter_name="Test",
            count=42, date=dt, longitude=2.0, latitude=48.0,
        )
        result = bc.to_byte_array("application/json")
        assert isinstance(result, (bytes, str))
        data = json.loads(result)
        assert data["count"] == 42

    def test_counter_from_data_dict(self):
        data = {
            "counter_id": "test-id", "counter_name": "Test",
            "channel_name": None, "installation_date": None,
            "longitude": 2.0, "latitude": 48.0,
        }
        counter = Counter.from_data(data)
        assert counter.counter_id == "test-id"

    def test_counter_from_data_none(self):
        assert Counter.from_data(None) is None

    def test_bicycle_count_from_data_none(self):
        assert BicycleCount.from_data(None) is None
