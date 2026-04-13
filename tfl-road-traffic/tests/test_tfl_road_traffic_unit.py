"""
Unit tests for the TfL Road Traffic bridge.

Covers:
- Connection string parsing
- Data class building (RoadCorridor, RoadStatus, RoadDisruption, Street)
- Poller emit methods with mock producers
- Disruption deduplication logic
- Flush failure leaves state unchanged
- Reference refresh timing and cache preservation on failure
- Multi-group wiring validation
"""
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional
from unittest.mock import MagicMock, patch, call

import pytest

from tfl_road_traffic.tfl_road_traffic import (
    parse_connection_string,
    build_road_corridor,
    build_road_status,
    build_road_disruption,
    build_street,
    TflRoadTrafficPoller,
    _parse_dt,
    _serialize_geo,
)
from tfl_road_traffic_producer_data import RoadCorridor, RoadStatus, RoadDisruption


# ---------------------------------------------------------------------------
# Sample upstream data dicts mirroring TfL API responses
# ---------------------------------------------------------------------------

SAMPLE_CORRIDOR = {
    "id": "a2",
    "displayName": "A2",
    "statusSeverity": "Good",
    "statusSeverityDescription": "No Exceptional Delays",
    "bounds": "[[0.0,51.4],[0.1,51.5]]",
    "envelope": "some-envelope",
    "url": "/Road/a2",
    "statusAggregationStartDate": "2024-01-15T08:00:00Z",
    "statusAggregationEndDate": "2024-01-15T10:00:00Z",
}

SAMPLE_STATUS = {
    "id": "a12",
    "displayName": "A12",
    "statusSeverity": "Moderate",
    "statusSeverityDescription": "Some Delays",
    "bounds": None,
    "envelope": None,
    "url": "/Road/a12",
    "statusAggregationStartDate": None,
    "statusAggregationEndDate": None,
}

SAMPLE_DISRUPTION = {
    "id": "TIMS-12345",
    "category": "RealTime",
    "subCategory": "Incident",
    "severity": "Serious",
    "ordinal": 1,
    "url": "/Road/all/Disruption/TIMS-12345",
    "point": "POINT(-0.1 51.5)",
    "comments": "Road works near junction",
    "currentUpdate": "Lane closed",
    "currentUpdateDateTime": "2024-01-15T09:30:00Z",
    "corridorIds": ["a2"],
    "startDateTime": "2024-01-15T08:00:00Z",
    "endDateTime": "2024-01-15T18:00:00Z",
    "lastModifiedTime": "2024-01-15T09:30:00+00:00",
    "levelOfInterest": "High",
    "location": "A2 near Borough",
    "isProvisional": False,
    "hasClosures": True,
    "streets": [
        {
            "name": "Old Kent Road",
            "closure": "Partial",
            "directions": "Northbound",
            "sourceSystemId": "sys-001",
            "sourceSystemKey": "key-001",
        }
    ],
    "geography": {"type": "Point", "coordinates": [-0.1, 51.5]},
    "geometry": {"type": "LineString", "coordinates": [[-0.1, 51.5], [-0.2, 51.6]]},
    "status": "Active",
    "isActive": True,
}

SAMPLE_DISRUPTION_2 = {
    "id": "TIMS-99999",
    "category": "PlannedWork",
    "subCategory": "Utility works",
    "severity": "Minimal",
    "ordinal": 5,
    "url": "/Road/all/Disruption/TIMS-99999",
    "point": None,
    "comments": None,
    "currentUpdate": None,
    "currentUpdateDateTime": None,
    "corridorIds": None,
    "startDateTime": None,
    "endDateTime": None,
    "lastModifiedTime": "2024-01-15T07:00:00+00:00",
    "levelOfInterest": "Low",
    "location": None,
    "isProvisional": None,
    "hasClosures": None,
    "streets": None,
    "geography": None,
    "geometry": None,
    "status": None,
    "isActive": None,
}


# ---------------------------------------------------------------------------
# TestParseConnectionString
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseConnectionString:
    def test_bootstrap_server_format(self):
        cs = "BootstrapServer=mybroker:9092;EntityPath=tfl-road-traffic"
        result = parse_connection_string(cs)
        assert result["bootstrap.servers"] == "mybroker:9092"
        assert result["kafka_topic"] == "tfl-road-traffic"
        assert "sasl.username" not in result

    def test_event_hubs_format(self):
        cs = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=secretkey123;"
            "EntityPath=tfl-road-traffic"
        )
        result = parse_connection_string(cs)
        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "tfl-road-traffic"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["sasl.password"] == cs.strip()
        assert result["security.protocol"] == "SASL_SSL"

    def test_bootstrap_no_entity_path(self):
        cs = "BootstrapServer=mybroker:9092"
        result = parse_connection_string(cs)
        assert result["bootstrap.servers"] == "mybroker:9092"
        assert "kafka_topic" not in result

    def test_missing_fields_returns_empty(self):
        result = parse_connection_string("SomethingElse=value")
        assert result == {}


# ---------------------------------------------------------------------------
# TestParseDt
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseDt:
    def test_z_suffix(self):
        dt = _parse_dt("2024-01-15T09:30:00Z")
        assert dt is not None
        assert dt.tzinfo is not None

    def test_offset_suffix(self):
        dt = _parse_dt("2024-01-15T09:30:00+00:00")
        assert dt is not None

    def test_none_returns_none(self):
        assert _parse_dt(None) is None

    def test_empty_returns_none(self):
        assert _parse_dt("") is None

    def test_invalid_returns_none(self):
        assert _parse_dt("not-a-date") is None


# ---------------------------------------------------------------------------
# TestSerializeGeo
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestSerializeGeo:
    def test_dict_serialized_to_json_string(self):
        geo = {"type": "Point", "coordinates": [-0.1, 51.5]}
        result = _serialize_geo(geo)
        assert isinstance(result, str)
        assert json.loads(result) == geo

    def test_list_serialized_to_json_string(self):
        geo = [[-0.1, 51.5], [-0.2, 51.6]]
        result = _serialize_geo(geo)
        assert isinstance(result, str)
        assert json.loads(result) == geo

    def test_none_returns_none(self):
        assert _serialize_geo(None) is None

    def test_string_passes_through(self):
        assert _serialize_geo("POINT(-0.1 51.5)") == "POINT(-0.1 51.5)"


# ---------------------------------------------------------------------------
# TestBuildRoadCorridor
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestBuildRoadCorridor:
    def test_full_fields(self):
        corridor = build_road_corridor(SAMPLE_CORRIDOR)
        assert corridor is not None
        assert isinstance(corridor, RoadCorridor)
        assert corridor.road_id == "a2"
        assert corridor.display_name == "A2"
        assert corridor.status_severity == "Good"
        assert corridor.status_severity_description == "No Exceptional Delays"
        assert corridor.bounds == "[[0.0,51.4],[0.1,51.5]]"
        assert corridor.url == "/Road/a2"

    def test_datetime_parsing(self):
        corridor = build_road_corridor(SAMPLE_CORRIDOR)
        assert corridor.status_aggregation_start_date is not None
        assert isinstance(corridor.status_aggregation_start_date, datetime)
        assert corridor.status_aggregation_end_date is not None

    def test_missing_id_returns_none(self):
        raw = dict(SAMPLE_CORRIDOR)
        del raw["id"]
        assert build_road_corridor(raw) is None

    def test_missing_display_name_returns_none(self):
        raw = dict(SAMPLE_CORRIDOR)
        del raw["displayName"]
        assert build_road_corridor(raw) is None

    def test_null_optional_fields(self):
        raw = {
            "id": "m25",
            "displayName": "M25",
            "statusSeverity": None,
            "statusSeverityDescription": None,
            "bounds": None,
            "envelope": None,
            "url": None,
            "statusAggregationStartDate": None,
            "statusAggregationEndDate": None,
        }
        corridor = build_road_corridor(raw)
        assert corridor is not None
        assert corridor.status_severity is None
        assert corridor.status_aggregation_start_date is None


# ---------------------------------------------------------------------------
# TestBuildRoadStatus
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestBuildRoadStatus:
    def test_full_fields(self):
        status = build_road_status(SAMPLE_STATUS)
        assert status is not None
        assert isinstance(status, RoadStatus)
        assert status.road_id == "a12"
        assert status.display_name == "A12"
        assert status.status_severity == "Moderate"
        assert status.status_aggregation_start_date is None

    def test_missing_id_returns_none(self):
        raw = dict(SAMPLE_STATUS)
        del raw["id"]
        assert build_road_status(raw) is None

    def test_missing_display_name_returns_none(self):
        raw = dict(SAMPLE_STATUS)
        del raw["displayName"]
        assert build_road_status(raw) is None


# ---------------------------------------------------------------------------
# TestBuildStreet
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestBuildStreet:
    def test_full_fields(self):
        raw = {
            "name": "Old Kent Road",
            "closure": "Partial",
            "directions": "Northbound",
            "sourceSystemId": "sys-001",
            "sourceSystemKey": "key-001",
        }
        street = build_street(raw)
        assert street["name"] == "Old Kent Road"
        assert street["closure"] == "Partial"
        assert street["directions"] == "Northbound"
        assert street["source_system_id"] == "sys-001"
        assert street["source_system_key"] == "key-001"

    def test_empty_dict(self):
        street = build_street({})
        assert street["name"] is None
        assert street["source_system_id"] is None
        assert street["source_system_key"] is None

    def test_upstream_camelcase_mapped(self):
        raw = {"sourceSystemId": "X", "sourceSystemKey": "Y"}
        street = build_street(raw)
        assert "sourceSystemId" not in street
        assert "sourceSystemKey" not in street
        assert street["source_system_id"] == "X"
        assert street["source_system_key"] == "Y"


# ---------------------------------------------------------------------------
# TestBuildRoadDisruption
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestBuildRoadDisruption:
    def test_full_fields(self):
        disruption = build_road_disruption(SAMPLE_DISRUPTION)
        assert disruption is not None
        assert isinstance(disruption, RoadDisruption)
        assert disruption.disruption_id == "TIMS-12345"
        assert disruption.category == "RealTime"
        assert disruption.sub_category == "Incident"
        assert disruption.severity == "Serious"
        assert disruption.ordinal == 1
        assert disruption.current_update == "Lane closed"
        assert disruption.corridor_ids == ["a2"]
        assert disruption.level_of_interest == "High"
        assert disruption.is_provisional is False
        assert disruption.has_closures is True
        assert disruption.is_active is True
        assert disruption.status == "Active"

    def test_datetime_fields_parsed(self):
        disruption = build_road_disruption(SAMPLE_DISRUPTION)
        assert disruption.current_update_datetime is not None
        assert isinstance(disruption.current_update_datetime, datetime)
        assert disruption.start_datetime is not None
        assert disruption.end_datetime is not None
        assert disruption.last_modified_time is not None

    def test_geography_serialized_to_json_string(self):
        disruption = build_road_disruption(SAMPLE_DISRUPTION)
        assert isinstance(disruption.geography, str)
        parsed = json.loads(disruption.geography)
        assert parsed["type"] == "Point"

    def test_geometry_serialized_to_json_string(self):
        disruption = build_road_disruption(SAMPLE_DISRUPTION)
        assert isinstance(disruption.geometry, str)
        parsed = json.loads(disruption.geometry)
        assert parsed["type"] == "LineString"

    def test_streets_built(self):
        disruption = build_road_disruption(SAMPLE_DISRUPTION)
        assert disruption.streets is not None
        assert len(disruption.streets) == 1
        assert disruption.streets[0]["name"] == "Old Kent Road"
        assert disruption.streets[0]["source_system_id"] == "sys-001"

    def test_null_optional_fields(self):
        disruption = build_road_disruption(SAMPLE_DISRUPTION_2)
        assert disruption is not None
        assert disruption.disruption_id == "TIMS-99999"
        assert disruption.comments is None
        assert disruption.corridor_ids is None
        assert disruption.streets is None
        assert disruption.geography is None
        assert disruption.geometry is None
        assert disruption.is_provisional is None

    def test_missing_id_returns_none(self):
        raw = dict(SAMPLE_DISRUPTION)
        del raw["id"]
        assert build_road_disruption(raw) is None


# ---------------------------------------------------------------------------
# Helper to create a mock poller with injected mock producers
# ---------------------------------------------------------------------------

def _make_mock_poller():
    """Create a TflRoadTrafficPoller with all Kafka components mocked."""
    with patch("tfl_road_traffic.tfl_road_traffic.UkGovTflRoadCorridorsEventProducer") as MockCorr, \
         patch("tfl_road_traffic.tfl_road_traffic.UkGovTflRoadDisruptionsEventProducer") as MockDisr, \
         patch("confluent_kafka.Producer"):
        mock_corridors_producer = MagicMock()
        mock_disruptions_producer = MagicMock()
        MockCorr.return_value = mock_corridors_producer
        MockDisr.return_value = mock_disruptions_producer

        mock_kafka_producer = MagicMock()
        mock_kafka_producer.flush.return_value = 0

        poller = TflRoadTrafficPoller.__new__(TflRoadTrafficPoller)
        poller.kafka_topic = "tfl-road-traffic"
        poller.polling_interval = 60
        poller.reference_refresh_interval = 3600
        poller.session = MagicMock()
        poller._kafka_producer = mock_kafka_producer
        poller.corridors_producer = mock_corridors_producer
        poller.disruptions_producer = mock_disruptions_producer
        poller._seen_disruptions = {}
        poller._last_reference_time = 0.0
        poller._cached_corridors = None

    return poller, mock_corridors_producer, mock_disruptions_producer, mock_kafka_producer


# ---------------------------------------------------------------------------
# TestTflRoadTrafficPoller
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestTflRoadTrafficPoller:
    def test_emit_reference_data_calls_send_corridor(self):
        poller, mock_corr, mock_disr, mock_kafka = _make_mock_poller()
        mock_kafka.flush.return_value = 0

        count = poller.emit_reference_data([SAMPLE_CORRIDOR])

        assert count == 1
        mock_corr.send_uk_gov_tfl_road_road_corridor.assert_called_once()
        call_args = mock_corr.send_uk_gov_tfl_road_road_corridor.call_args
        assert call_args[0][0] == "a2"
        assert isinstance(call_args[0][1], RoadCorridor)
        assert call_args[1].get("flush_producer") is False

    def test_emit_reference_data_flush_failure_returns_zero(self):
        poller, mock_corr, mock_disr, mock_kafka = _make_mock_poller()
        mock_kafka.flush.return_value = 1  # failure

        count = poller.emit_reference_data([SAMPLE_CORRIDOR])

        assert count == 0

    def test_emit_status_data_calls_send_status(self):
        poller, mock_corr, mock_disr, mock_kafka = _make_mock_poller()
        mock_kafka.flush.return_value = 0

        count = poller.emit_status_data([SAMPLE_STATUS])

        assert count == 1
        mock_corr.send_uk_gov_tfl_road_road_status.assert_called_once()
        call_args = mock_corr.send_uk_gov_tfl_road_road_status.call_args
        assert call_args[0][0] == "a12"
        assert isinstance(call_args[0][1], RoadStatus)
        assert call_args[1].get("flush_producer") is False

    def test_emit_status_data_flush_failure_returns_zero(self):
        poller, mock_corr, mock_disr, mock_kafka = _make_mock_poller()
        mock_kafka.flush.return_value = 5

        count = poller.emit_status_data([SAMPLE_STATUS])

        assert count == 0

    def test_emit_disruption_data_new_disruption_emitted(self):
        poller, mock_corr, mock_disr, mock_kafka = _make_mock_poller()
        mock_kafka.flush.return_value = 0

        count = poller.emit_disruption_data([SAMPLE_DISRUPTION])

        assert count == 1
        mock_disr.send_uk_gov_tfl_road_road_disruption.assert_called_once()
        call_args = mock_disr.send_uk_gov_tfl_road_road_disruption.call_args
        assert call_args[0][0] == "TIMS-12345"
        assert isinstance(call_args[0][1], RoadDisruption)
        assert call_args[1].get("flush_producer") is False

    def test_emit_disruption_deduplication_same_modified_time_skipped(self):
        poller, mock_corr, mock_disr, mock_kafka = _make_mock_poller()
        mock_kafka.flush.return_value = 0

        # First emit establishes state
        poller.emit_disruption_data([SAMPLE_DISRUPTION])
        mock_disr.send_uk_gov_tfl_road_road_disruption.reset_mock()

        # Second emit with same lastModifiedTime should skip
        count = poller.emit_disruption_data([SAMPLE_DISRUPTION])
        assert count == 0
        mock_disr.send_uk_gov_tfl_road_road_disruption.assert_not_called()

    def test_emit_disruption_deduplication_changed_modified_time_re_emitted(self):
        poller, mock_corr, mock_disr, mock_kafka = _make_mock_poller()
        mock_kafka.flush.return_value = 0

        poller.emit_disruption_data([SAMPLE_DISRUPTION])
        mock_disr.send_uk_gov_tfl_road_road_disruption.reset_mock()

        updated = dict(SAMPLE_DISRUPTION)
        updated["lastModifiedTime"] = "2024-01-15T11:00:00+00:00"
        count = poller.emit_disruption_data([updated])

        assert count == 1
        mock_disr.send_uk_gov_tfl_road_road_disruption.assert_called_once()

    def test_emit_disruption_flush_failure_leaves_state_unchanged(self):
        poller, mock_corr, mock_disr, mock_kafka = _make_mock_poller()
        mock_kafka.flush.return_value = 3  # failure

        count = poller.emit_disruption_data([SAMPLE_DISRUPTION])

        assert count == 0
        # State must NOT be updated on flush failure
        assert "TIMS-12345" not in poller._seen_disruptions

    def test_emit_disruption_flush_failure_resends_on_next_cycle(self):
        poller, mock_corr, mock_disr, mock_kafka = _make_mock_poller()
        mock_kafka.flush.return_value = 3  # fail first time

        poller.emit_disruption_data([SAMPLE_DISRUPTION])
        assert mock_disr.send_uk_gov_tfl_road_road_disruption.call_count == 1
        mock_disr.send_uk_gov_tfl_road_road_disruption.reset_mock()

        # Now fix flush; same disruption should be re-sent
        mock_kafka.flush.return_value = 0
        count = poller.emit_disruption_data([SAMPLE_DISRUPTION])
        assert count == 1
        mock_disr.send_uk_gov_tfl_road_road_disruption.assert_called_once()

    def test_reference_cache_preserved_on_fetch_failure(self):
        """If reference fetch fails but a cache exists, the cache is retained."""
        import time as _time
        poller, mock_corr, mock_disr, mock_kafka = _make_mock_poller()
        mock_kafka.flush.return_value = 0

        initial_corridors = [SAMPLE_CORRIDOR]
        poller._cached_corridors = initial_corridors
        poller._last_reference_time = 0.0
        poller.reference_refresh_interval = 0  # always refresh

        # Simulate fetch failure
        poller.fetch_corridors = MagicMock(return_value=None)
        poller.fetch_statuses = MagicMock(return_value=[])
        poller.fetch_disruptions = MagicMock(return_value=[])

        with patch("time.sleep", side_effect=StopIteration):
            try:
                poller.poll_and_send()
            except StopIteration:
                pass

        # Cache must still be the original; reference not re-emitted from None
        assert poller._cached_corridors is initial_corridors
        # Reference time should NOT have advanced (fetch failed)
        assert poller._last_reference_time == 0.0

    def test_reference_refresh_interval_respected(self):
        """Reference data is only re-fetched when the interval has elapsed."""
        import time as _time
        poller, mock_corr, mock_disr, mock_kafka = _make_mock_poller()
        mock_kafka.flush.return_value = 0

        poller.fetch_corridors = MagicMock(return_value=[SAMPLE_CORRIDOR])
        poller.fetch_statuses = MagicMock(return_value=[])
        poller.fetch_disruptions = MagicMock(return_value=[])
        # Set last_reference_time to just now so refresh is NOT due
        poller._last_reference_time = _time.monotonic()
        poller.reference_refresh_interval = 3600

        with patch("time.sleep", side_effect=StopIteration):
            try:
                poller.poll_and_send()
            except StopIteration:
                pass

        # Reference was NOT due, so fetch_corridors should NOT be called
        poller.fetch_corridors.assert_not_called()

    def test_status_fetch_failure_does_not_abort_disruption_emit(self):
        """If status fetch fails, disruption emit still proceeds."""
        poller, mock_corr, mock_disr, mock_kafka = _make_mock_poller()
        mock_kafka.flush.return_value = 0

        poller.fetch_corridors = MagicMock(return_value=None)
        poller.fetch_statuses = MagicMock(return_value=None)  # status fails
        poller.fetch_disruptions = MagicMock(return_value=[SAMPLE_DISRUPTION])
        poller._last_reference_time = 0.0  # reference due but fetch returns None
        poller.reference_refresh_interval = 0  # always refresh

        with patch("time.sleep", side_effect=StopIteration):
            try:
                poller.poll_and_send()
            except StopIteration:
                pass

        # Disruption should still have been emitted despite status failure
        mock_disr.send_uk_gov_tfl_road_road_disruption.assert_called_once()


# ---------------------------------------------------------------------------
# TestMultiGroupWiring
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestMultiGroupWiring:
    def test_both_producer_groups_exercised_in_one_cycle(self):
        """
        Verify that one full poll cycle exercises both corridors (reference + status)
        and disruptions producer groups.
        """
        import time as _time
        poller, mock_corr, mock_disr, mock_kafka = _make_mock_poller()
        mock_kafka.flush.return_value = 0

        poller.fetch_corridors = MagicMock(return_value=[SAMPLE_CORRIDOR])
        poller.fetch_statuses = MagicMock(return_value=[SAMPLE_STATUS])
        poller.fetch_disruptions = MagicMock(return_value=[SAMPLE_DISRUPTION])
        poller._last_reference_time = 0.0  # force reference refresh
        poller.reference_refresh_interval = 0  # always refresh

        with patch("time.sleep", side_effect=StopIteration):
            try:
                poller.poll_and_send()
            except StopIteration:
                pass

        # Corridors producer: reference (RoadCorridor) + status (RoadStatus)
        mock_corr.send_uk_gov_tfl_road_road_corridor.assert_called_once()
        mock_corr.send_uk_gov_tfl_road_road_status.assert_called_once()
        # Disruptions producer: disruption
        mock_disr.send_uk_gov_tfl_road_road_disruption.assert_called_once()

    def test_disruptions_producer_separate_from_corridors_producer(self):
        """
        Ensure that corridor sends do NOT call disruptions producer and vice versa.
        """
        poller, mock_corr, mock_disr, mock_kafka = _make_mock_poller()
        mock_kafka.flush.return_value = 0

        poller.emit_reference_data([SAMPLE_CORRIDOR])

        # Disruptions producer must not have been touched
        mock_disr.send_uk_gov_tfl_road_road_disruption.assert_not_called()

        mock_corr.reset_mock()
        poller.emit_disruption_data([SAMPLE_DISRUPTION])

        # Corridors producer must not have been touched
        mock_corr.send_uk_gov_tfl_road_road_corridor.assert_not_called()
        mock_corr.send_uk_gov_tfl_road_road_status.assert_not_called()
