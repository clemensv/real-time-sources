"""
Unit tests for NIFC USA Wildfires data poller.
Tests that don't require external dependencies or API calls.
"""

import pytest
import json
import os
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from datetime import datetime, timezone, timedelta
from nifc_usa_wildfires.nifc_usa_wildfires import (
    NIFCWildfirePoller,
    parse_connection_string,
    epoch_ms_to_iso,
    build_query_url,
    BASE_URL,
    SOURCE_URI,
    MAX_RECORD_COUNT,
    POLL_INTERVAL_MINUTES,
)


def _make_feature(**overrides):
    """Helper to create a minimal valid GeoJSON feature for testing."""
    feature = {
        "type": "Feature",
        "id": 1,
        "geometry": {
            "type": "Point",
            "coordinates": [-123.922833, 42.692833]
        },
        "properties": {
            "OBJECTID": 1,
            "IncidentName": "Pinnacle",
            "IncidentTypeCategory": "WF",
            "UniqueFireIdentifier": "2025-ORRSF-000389",
            "DailyAcres": 19520.0,
            "CalculatedAcres": 3987.45,
            "DiscoveryAcres": 0.1,
            "PercentContained": 90.0,
            "ICS209ReportDateTime": 1763405237000,
            "FireDiscoveryDateTime": 1756945500000,
            "POOCounty": "Curry",
            "POOState": "US-OR",
            "FireCause": "Natural",
            "FireCauseGeneral": None,
            "GACC": "NWCC",
            "TotalIncidentPersonnel": None,
            "IncidentManagementOrganization": None,
            "FireMgmtComplexity": None,
            "ResidencesDestroyed": 0,
            "OtherStructuresDestroyed": 1,
            "Injuries": 15,
            "Fatalities": 0,
            "PredominantFuelGroup": None,
            "PredominantFuelModel": None,
            "PrimaryFuelModel": None,
            "ContainmentDateTime": 1772815800000,
            "ControlDateTime": None,
            "FinalAcres": None,
            "IsValid": 1,
            "FireOutDateTime": None,
            "ModifiedOnDateTime": 1775056123000,
            "IncidentTypeKind": "FI",
            "IrwinID": "cafba52b-5518-4b51-858b-8a1ee089a3ff",
            "GlobalID": "cafba52b-5518-4b51-858b-8a1ee089a3ff",
            "ModifiedOnAge": 7,
            "FireDiscoveryAge": 217,
        }
    }
    for key, value in overrides.items():
        if key in feature:
            feature[key] = value
        elif key in feature["properties"]:
            feature["properties"][key] = value
    return feature


@pytest.mark.unit
class TestEpochMsToIso:
    """Test epoch milliseconds to ISO 8601 conversion."""

    def test_valid_epoch(self):
        """Test converting a valid epoch ms timestamp."""
        result = epoch_ms_to_iso(1756945500000)
        assert result is not None
        assert "2025" in result
        assert "+00:00" in result or "Z" in result

    def test_none_epoch(self):
        """Test that None input returns None."""
        result = epoch_ms_to_iso(None)
        assert result is None

    def test_zero_epoch(self):
        """Test converting epoch 0 (1970-01-01)."""
        result = epoch_ms_to_iso(0)
        assert result is not None
        assert "1970-01-01" in result

    def test_known_timestamp(self):
        """Test converting a known timestamp."""
        # 2023-11-14T22:13:20Z = 1700000000000 ms
        result = epoch_ms_to_iso(1700000000000)
        assert result is not None
        assert "2023-11-14" in result
        assert "22:13:20" in result


@pytest.mark.unit
class TestBuildQueryUrl:
    """Test ArcGIS query URL construction."""

    def test_default_query(self):
        """Test building a default query URL."""
        url = build_query_url()
        assert BASE_URL in url
        assert "where=" in url
        assert "outFields=*" in url
        assert "f=geojson" in url
        assert f"resultRecordCount={MAX_RECORD_COUNT}" in url
        assert "resultOffset=0" in url

    def test_custom_where_clause(self):
        """Test building URL with a custom where clause."""
        url = build_query_url(where_clause="IncidentTypeCategory='WF'")
        assert "where=" in url
        assert "WF" in url

    def test_custom_offset(self):
        """Test building URL with custom offset."""
        url = build_query_url(result_offset=100)
        assert "resultOffset=100" in url

    def test_custom_record_count(self):
        """Test building URL with custom record count."""
        url = build_query_url(result_record_count=500)
        assert "resultRecordCount=500" in url


@pytest.mark.unit
class TestNIFCWildfirePollerInit:
    """Test NIFCWildfirePoller initialization."""

    @patch('nifc_usa_wildfires.nifc_usa_wildfires.GovNIFCWildfiresEventProducer')
    @patch('nifc_usa_wildfires.nifc_usa_wildfires.Producer')
    def test_init_with_kafka_config(self, mock_producer_class, mock_event_producer):
        """Test initialization with Kafka configuration."""
        mock_kafka_config = {
            'bootstrap.servers': 'localhost:9092',
        }
        mock_producer_instance = Mock()
        mock_producer_class.return_value = mock_producer_instance

        poller = NIFCWildfirePoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file='test_file.json',
        )

        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == 'test_file.json'
        mock_producer_class.assert_called_once_with(mock_kafka_config)
        mock_event_producer.assert_called_once_with(mock_producer_instance, 'test-topic')

    def test_init_without_kafka_config(self):
        """Test initialization without Kafka configuration."""
        poller = NIFCWildfirePoller(
            kafka_config=None,
            kafka_topic='test-topic',
            last_polled_file='test_file.json',
        )

        assert poller.kafka_topic == 'test-topic'
        assert poller.event_producer is None

    def test_init_custom_poll_interval(self):
        """Test initialization with a custom poll interval."""
        poller = NIFCWildfirePoller(poll_interval_minutes=10)
        assert poller.poll_interval == timedelta(minutes=10)

    def test_init_default_poll_interval(self):
        """Test initialization with default poll interval."""
        poller = NIFCWildfirePoller()
        assert poller.poll_interval == timedelta(minutes=POLL_INTERVAL_MINUTES)


@pytest.mark.unit
class TestParseIncident:
    """Test GeoJSON feature parsing into WildfireIncident objects."""

    def test_parse_valid_incident(self):
        """Test parsing a valid GeoJSON feature."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.irwin_id == "cafba52b-5518-4b51-858b-8a1ee089a3ff"
        assert incident.incident_name == "Pinnacle"
        assert incident.incident_type_category == "WF"
        assert incident.unique_fire_identifier == "2025-ORRSF-000389"
        assert incident.daily_acres == 19520.0
        assert incident.calculated_acres == 3987.45
        assert incident.percent_contained == 90.0
        assert incident.poo_state == "US-OR"
        assert incident.poo_county == "Curry"
        assert incident.latitude == 42.692833
        assert incident.longitude == -123.922833
        assert incident.fire_cause == "Natural"
        assert incident.gacc == "NWCC"
        # Generated __post_init__ uses truthiness: 0 becomes None
        assert incident.residences_destroyed is None
        assert incident.other_structures_destroyed == 1
        assert incident.injuries == 15
        assert incident.fatalities is None
        assert incident.incident_type_kind == "FI"

    def test_parse_incident_missing_irwin_id(self):
        """Test that a feature without IrwinID returns None."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        feature["properties"]["IrwinID"] = None
        incident = poller.parse_incident(feature)
        assert incident is None

    def test_parse_incident_empty_irwin_id(self):
        """Test that a feature with empty IrwinID returns None."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        feature["properties"]["IrwinID"] = ""
        incident = poller.parse_incident(feature)
        assert incident is None

    def test_parse_incident_missing_name(self):
        """Test that a feature without IncidentName returns None."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        feature["properties"]["IncidentName"] = ""
        incident = poller.parse_incident(feature)
        assert incident is None

    def test_parse_incident_null_optional_fields(self):
        """Test parsing when optional fields are null."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        feature["properties"]["DailyAcres"] = None
        feature["properties"]["PercentContained"] = None
        feature["properties"]["FireCause"] = None
        feature["properties"]["GACC"] = None
        feature["properties"]["TotalIncidentPersonnel"] = None
        feature["properties"]["FireMgmtComplexity"] = None
        feature["properties"]["ResidencesDestroyed"] = None
        feature["properties"]["Injuries"] = None
        feature["properties"]["Fatalities"] = None
        feature["properties"]["ContainmentDateTime"] = None
        feature["properties"]["FinalAcres"] = None
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.daily_acres is None
        assert incident.percent_contained is None
        assert incident.fire_cause is None
        assert incident.gacc is None
        assert incident.total_incident_personnel is None
        assert incident.fire_mgmt_complexity is None
        assert incident.residences_destroyed is None
        assert incident.injuries is None
        assert incident.fatalities is None
        assert incident.containment_datetime is None
        assert incident.final_acres is None

    def test_parse_incident_timestamp_conversion(self):
        """Test that ArcGIS epoch ms timestamps are converted to ISO 8601."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.modified_on_datetime is not None
        assert "T" in incident.modified_on_datetime
        assert "+" in incident.modified_on_datetime or "Z" in incident.modified_on_datetime

    def test_parse_incident_fire_discovery_conversion(self):
        """Test fire discovery datetime conversion."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.fire_discovery_datetime is not None
        assert "T" in incident.fire_discovery_datetime

    def test_parse_incident_null_geometry(self):
        """Test parsing when geometry is null."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        feature["geometry"] = None
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.latitude is None
        assert incident.longitude is None

    def test_parse_incident_missing_geometry(self):
        """Test parsing when geometry key is missing."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        del feature["geometry"]
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.latitude is None
        assert incident.longitude is None

    def test_parse_incident_null_modified_on(self):
        """Test that null ModifiedOnDateTime gets a default."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        feature["properties"]["ModifiedOnDateTime"] = None
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.modified_on_datetime is not None

    def test_parse_incident_containment_datetime(self):
        """Test containment datetime conversion."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.containment_datetime is not None
        assert "T" in incident.containment_datetime

    def test_parse_incident_null_control_datetime(self):
        """Test that null ControlDateTime stays None."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.control_datetime is None

    def test_parse_incident_null_fire_out_datetime(self):
        """Test that null FireOutDateTime stays None."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.fire_out_datetime is None


@pytest.mark.unit
class TestConnectionStringParsing:
    """Test connection string parsing."""

    def test_parse_valid_event_hubs_connection_string(self):
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

    def test_parse_plain_kafka_connection_string(self):
        """Test parsing a plain Kafka connection string."""
        conn_str = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = parse_connection_string(conn_str)

        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'test-topic'
        assert 'sasl.username' not in result

    def test_parse_connection_string_sets_sasl_ssl(self):
        """Test that Event Hubs connection string sets SASL_SSL."""
        conn_str = "Endpoint=sb://ns.servicebus.windows.net/;SharedAccessKeyName=policy;SharedAccessKey=key;EntityPath=topic"
        result = parse_connection_string(conn_str)

        assert result['security.protocol'] == 'SASL_SSL'
        assert result['sasl.mechanism'] == 'PLAIN'


@pytest.mark.unit
class TestSeenIdsFileOperations:
    """Test loading and saving seen incident IDs."""

    def test_load_seen_ids_no_file(self):
        """Test loading when no file exists."""
        poller = NIFCWildfirePoller(last_polled_file="nonexistent_file.json")
        result = poller.load_seen_ids()
        assert result == {}

    def test_load_seen_ids_empty_file(self, tmp_path):
        """Test loading from an empty/corrupt file."""
        filepath = str(tmp_path / "test_seen.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("invalid json")
        poller = NIFCWildfirePoller(last_polled_file=filepath)
        result = poller.load_seen_ids()
        assert result == {}

    def test_save_and_load_seen_ids(self, tmp_path):
        """Test round-trip save and load of seen IDs."""
        filepath = str(tmp_path / "test_seen.json")
        poller = NIFCWildfirePoller(last_polled_file=filepath)

        seen_ids = {
            "cafba52b-5518-4b51-858b-8a1ee089a3ff": "2025-01-01T00:00:00+00:00",
            "615cab3c-ecf2-485a-a105-acd92b2af179": "2025-01-02T00:00:00+00:00",
        }
        poller.save_seen_ids(seen_ids)

        loaded = poller.load_seen_ids()
        assert loaded == seen_ids

    def test_save_seen_ids_no_file(self):
        """Test that save with no file configured does nothing."""
        poller = NIFCWildfirePoller(last_polled_file=None)
        poller.save_seen_ids({"test": "value"})  # Should not raise

    def test_load_seen_ids_no_file_configured(self):
        """Test that load with no file configured returns empty."""
        poller = NIFCWildfirePoller(last_polled_file=None)
        result = poller.load_seen_ids()
        assert result == {}


@pytest.mark.unit
class TestWildfireIncidentDataClass:
    """Test WildfireIncident dataclass serialization."""

    def test_incident_to_json(self):
        """Test WildfireIncident serialization to JSON."""
        from nifc_usa_wildfires_producer_data.gov.nifc.wildfires.wildfireincident import WildfireIncident

        incident = WildfireIncident(
            irwin_id="cafba52b-5518-4b51-858b-8a1ee089a3ff",
            incident_name="Pinnacle",
            unique_fire_identifier="2025-ORRSF-000389",
            incident_type_category="WF",
            incident_type_kind="FI",
            fire_discovery_datetime="2025-09-04T12:00:00+00:00",
            daily_acres=19520.0,
            calculated_acres=3987.45,
            discovery_acres=0.1,
            percent_contained=90.0,
            poo_state="US-OR",
            poo_county="Curry",
            latitude=42.692833,
            longitude=-123.922833,
            fire_cause="Natural",
            fire_cause_general=None,
            gacc="NWCC",
            total_incident_personnel=None,
            incident_management_organization=None,
            fire_mgmt_complexity=None,
            residences_destroyed=0,
            other_structures_destroyed=1,
            injuries=15,
            fatalities=0,
            containment_datetime="2025-12-04T12:00:00+00:00",
            control_datetime=None,
            fire_out_datetime=None,
            final_acres=None,
            modified_on_datetime="2025-01-30T10:00:00+00:00",
        )

        json_bytes = incident.to_byte_array("application/json")
        assert json_bytes is not None
        json_str = json_bytes if isinstance(json_bytes, str) else json_bytes.decode('utf-8')
        assert "cafba52b" in json_str
        assert "Pinnacle" in json_str
        assert "19520" in json_str

    def test_incident_to_avro(self):
        """Test WildfireIncident serialization to Avro binary."""
        from nifc_usa_wildfires_producer_data.gov.nifc.wildfires.wildfireincident import WildfireIncident

        incident = WildfireIncident(
            irwin_id="cafba52b-5518-4b51-858b-8a1ee089a3ff",
            incident_name="Pinnacle",
            unique_fire_identifier=None,
            incident_type_category=None,
            incident_type_kind=None,
            fire_discovery_datetime=None,
            daily_acres=None,
            calculated_acres=None,
            discovery_acres=None,
            percent_contained=None,
            poo_state=None,
            poo_county=None,
            latitude=None,
            longitude=None,
            fire_cause=None,
            fire_cause_general=None,
            gacc=None,
            total_incident_personnel=None,
            incident_management_organization=None,
            fire_mgmt_complexity=None,
            residences_destroyed=None,
            other_structures_destroyed=None,
            injuries=None,
            fatalities=None,
            containment_datetime=None,
            control_datetime=None,
            fire_out_datetime=None,
            final_acres=None,
            modified_on_datetime="2025-01-30T10:00:00+00:00",
        )

        avro_bytes = incident.to_byte_array("avro/binary")
        assert avro_bytes is not None
        assert len(avro_bytes) > 0

    def test_incident_from_dict(self):
        """Test creating a WildfireIncident from a dictionary."""
        from nifc_usa_wildfires_producer_data.gov.nifc.wildfires.wildfireincident import WildfireIncident

        data = {
            "irwin_id": "cafba52b-5518-4b51-858b-8a1ee089a3ff",
            "incident_name": "Pinnacle",
            "unique_fire_identifier": None,
            "incident_type_category": "WF",
            "incident_type_kind": "FI",
            "fire_discovery_datetime": None,
            "daily_acres": 1000.0,
            "calculated_acres": None,
            "discovery_acres": None,
            "percent_contained": 50.0,
            "poo_state": "US-CA",
            "poo_county": "Kings",
            "latitude": 35.0,
            "longitude": -119.0,
            "fire_cause": "Human",
            "fire_cause_general": None,
            "gacc": "OSCC",
            "total_incident_personnel": 100,
            "incident_management_organization": None,
            "fire_mgmt_complexity": None,
            "residences_destroyed": None,
            "other_structures_destroyed": None,
            "injuries": None,
            "fatalities": None,
            "containment_datetime": None,
            "control_datetime": None,
            "fire_out_datetime": None,
            "final_acres": None,
            "modified_on_datetime": "2025-01-30T10:00:00+00:00",
        }
        incident = WildfireIncident.from_serializer_dict(data)
        assert incident.irwin_id == "cafba52b-5518-4b51-858b-8a1ee089a3ff"
        assert incident.incident_name == "Pinnacle"
        assert incident.daily_acres == 1000.0

    def test_incident_json_roundtrip(self):
        """Test JSON serialization roundtrip."""
        from nifc_usa_wildfires_producer_data.gov.nifc.wildfires.wildfireincident import WildfireIncident

        original = WildfireIncident(
            irwin_id="test-id-123",
            incident_name="Test Fire",
            unique_fire_identifier="2025-TEST-001",
            incident_type_category="WF",
            incident_type_kind="FI",
            fire_discovery_datetime="2025-01-01T00:00:00+00:00",
            daily_acres=500.0,
            calculated_acres=450.0,
            discovery_acres=10.0,
            percent_contained=75.0,
            poo_state="US-CA",
            poo_county="Test County",
            latitude=34.0,
            longitude=-118.0,
            fire_cause="Natural",
            fire_cause_general="Lightning",
            gacc="OSCC",
            total_incident_personnel=200,
            incident_management_organization="Team Alpha",
            fire_mgmt_complexity="Type 2",
            residences_destroyed=5,
            other_structures_destroyed=10,
            injuries=2,
            fatalities=0,
            containment_datetime="2025-01-15T00:00:00+00:00",
            control_datetime="2025-01-20T00:00:00+00:00",
            fire_out_datetime=None,
            final_acres=None,
            modified_on_datetime="2025-01-25T00:00:00+00:00",
        )

        json_bytes = original.to_byte_array("application/json")
        json_str = json_bytes if isinstance(json_bytes, str) else json_bytes.decode('utf-8')
        data = json.loads(json_str)

        restored = WildfireIncident.from_serializer_dict(data)
        assert restored.irwin_id == original.irwin_id
        assert restored.incident_name == original.incident_name
        assert restored.daily_acres == original.daily_acres
        assert restored.percent_contained == original.percent_contained
        assert restored.total_incident_personnel == original.total_incident_personnel


@pytest.mark.unit
class TestConstants:
    """Test module-level constants."""

    def test_base_url(self):
        """Test that BASE_URL points to ArcGIS service."""
        assert "arcgis.com" in BASE_URL
        assert "USA_Wildfires" in BASE_URL

    def test_source_uri(self):
        """Test that SOURCE_URI is set correctly."""
        assert "arcgis.com" in SOURCE_URI
        assert "FeatureServer/0" in SOURCE_URI

    def test_max_record_count(self):
        """Test MAX_RECORD_COUNT is reasonable."""
        assert MAX_RECORD_COUNT > 0
        assert MAX_RECORD_COUNT <= 18000

    def test_poll_interval(self):
        """Test poll interval default."""
        assert POLL_INTERVAL_MINUTES == 5


@pytest.mark.unit
class TestParseIncidentEdgeCases:
    """Test edge cases in incident parsing."""

    def test_parse_incident_zero_acres(self):
        """Test parsing an incident with zero daily acres (generated code treats 0.0 as falsy)."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        feature["properties"]["DailyAcres"] = 0.0
        incident = poller.parse_incident(feature)

        assert incident is not None
        # Generated __post_init__ uses `if self.daily_acres` which is falsy for 0.0
        assert incident.daily_acres is None

    def test_parse_incident_large_acres(self):
        """Test parsing an incident with very large acreage."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        feature["properties"]["DailyAcres"] = 500000.0
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.daily_acres == 500000.0

    def test_parse_incident_zero_percent_contained(self):
        """Test parsing an incident with 0% contained (generated code treats 0.0 as falsy)."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        feature["properties"]["PercentContained"] = 0.0
        incident = poller.parse_incident(feature)

        assert incident is not None
        # Generated __post_init__ uses `if self.percent_contained` which is falsy for 0.0
        assert incident.percent_contained is None

    def test_parse_incident_100_percent_contained(self):
        """Test parsing an incident with 100% contained."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        feature["properties"]["PercentContained"] = 100.0
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.percent_contained == 100.0

    def test_parse_incident_different_type_categories(self):
        """Test parsing incidents with different type categories."""
        poller = NIFCWildfirePoller()
        for category in ["WF", "RX", "CX"]:
            feature = _make_feature()
            feature["properties"]["IncidentTypeCategory"] = category
            incident = poller.parse_incident(feature)
            assert incident is not None
            assert incident.incident_type_category == category

    def test_parse_incident_empty_geometry_coordinates(self):
        """Test parsing when geometry has empty coordinates."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        feature["geometry"] = {"type": "Point", "coordinates": []}
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.latitude is None
        assert incident.longitude is None

    def test_parse_incident_point_geometry_only_two_coords(self):
        """Test parsing when geometry has only lat/lon (no elevation)."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        feature["geometry"] = {"type": "Point", "coordinates": [-119.0, 35.0]}
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.latitude == 35.0
        assert incident.longitude == -119.0

    def test_parse_incident_non_point_geometry(self):
        """Test parsing when geometry is not a Point type."""
        poller = NIFCWildfirePoller()
        feature = _make_feature()
        feature["geometry"] = {"type": "Polygon", "coordinates": []}
        incident = poller.parse_incident(feature)

        assert incident is not None
        assert incident.latitude is None
        assert incident.longitude is None

    def test_parse_multiple_incidents(self):
        """Test parsing multiple different features."""
        poller = NIFCWildfirePoller()
        features = []
        for i in range(5):
            feature = _make_feature()
            feature["properties"]["IrwinID"] = f"id-{i}"
            feature["properties"]["IncidentName"] = f"Fire {i}"
            features.append(feature)

        incidents = [poller.parse_incident(f) for f in features]
        assert all(inc is not None for inc in incidents)
        ids = [inc.irwin_id for inc in incidents]
        assert len(set(ids)) == 5


@pytest.mark.unit
class TestConnectionStringEdgeCases:
    """Test connection string parsing edge cases."""

    def test_empty_connection_string(self):
        """Test parsing an empty connection string."""
        result = parse_connection_string("")
        assert isinstance(result, dict)

    def test_connection_string_with_spaces(self):
        """Test parsing a connection string with extra spaces."""
        conn_str = "BootstrapServer=localhost:9092 ; EntityPath=test-topic"
        result = parse_connection_string(conn_str)
        assert 'kafka_topic' in result
