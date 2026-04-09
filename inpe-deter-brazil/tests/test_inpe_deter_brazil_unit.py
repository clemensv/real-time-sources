"""
Unit tests for INPE DETER Brazil deforestation alert poller.
Tests that don't require external dependencies or API calls.
"""

import pytest
import json
import os
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from datetime import datetime, timezone, timedelta
from inpe_deter_brazil.inpe_deter_brazil import (
    INPEDeterPoller,
    WFS_ENDPOINTS,
    DEFAULT_POLL_INTERVAL_MINUTES,
    DEFAULT_PAGE_SIZE,
    SOURCE_URI,
    compute_centroid,
    build_wfs_url,
    parse_connection_string,
)


SAMPLE_AMAZON_FEATURE = {
    "type": "Feature",
    "id": "deter_amz.fid-abc123",
    "geometry": {
        "type": "MultiPolygon",
        "coordinates": [[[
            [-48.055, -2.9296],
            [-48.0548, -2.9296],
            [-48.0544, -2.9299],
            [-48.0548, -2.9335],
            [-48.055, -2.9335],
            [-48.055, -2.9296],
        ]]]
    },
    "properties": {
        "gid": "91537_hist",
        "classname": "DESMATAMENTO_CR",
        "quadrant": None,
        "path_row": "036016",
        "view_date": "2026-02-21",
        "sensor": "WFI",
        "satellite": "AMAZONIA-1",
        "areauckm": 0,
        "uc": None,
        "areamunkm": 0.07874579199403711,
        "municipality": "Ipixuna do Para",
        "mun_geocod": "1503457",
        "uf": "PA",
        "publish_month": "2026-02-01"
    }
}

SAMPLE_CERRADO_FEATURE = {
    "type": "Feature",
    "id": "deter_cerrado.10001_curr",
    "geometry": {
        "type": "MultiPolygon",
        "coordinates": [[[
            [-46.3549, -14.0516],
            [-46.3425, -14.0518],
            [-46.342, -14.0543],
            [-46.3446, -14.0579],
            [-46.3549, -14.0516],
        ]]]
    },
    "properties": {
        "gid": "10001_curr",
        "classname": "DESMATAMENTO_CR",
        "quadrant": None,
        "path_row": "156_117",
        "view_date": "2021-09-17",
        "created_date": "2021-09-20",
        "sensor": "AWFI",
        "satellite": "CBERS-4",
        "areatotalkm": 0.5422608100141734,
        "areauckm": 0,
        "uc": None,
        "areamunkm": 0.5422608100141734,
        "municipality": "Posse",
        "uf": "GO",
        "publish_month": "2021-09-01"
    }
}


@pytest.mark.unit
class TestWFSEndpoints:
    """Test WFS endpoint configuration."""

    def test_endpoints_dict_structure(self):
        """Test that WFS_ENDPOINTS dict is properly structured."""
        assert isinstance(WFS_ENDPOINTS, dict)
        assert len(WFS_ENDPOINTS) == 2

    def test_amazon_endpoint_exists(self):
        """Test that the Amazon endpoint is configured."""
        assert "amazon" in WFS_ENDPOINTS
        assert "base_url" in WFS_ENDPOINTS["amazon"]
        assert "type_name" in WFS_ENDPOINTS["amazon"]

    def test_cerrado_endpoint_exists(self):
        """Test that the Cerrado endpoint is configured."""
        assert "cerrado" in WFS_ENDPOINTS
        assert "base_url" in WFS_ENDPOINTS["cerrado"]
        assert "type_name" in WFS_ENDPOINTS["cerrado"]

    def test_amazon_url_points_to_inpe(self):
        """Test that the Amazon URL points to INPE."""
        assert "terrabrasilis.dpi.inpe.br" in WFS_ENDPOINTS["amazon"]["base_url"]

    def test_cerrado_url_points_to_inpe(self):
        """Test that the Cerrado URL points to INPE."""
        assert "terrabrasilis.dpi.inpe.br" in WFS_ENDPOINTS["cerrado"]["base_url"]

    def test_endpoints_use_http(self):
        """Test that endpoints use HTTP (not HTTPS) as per the API."""
        for biome, config in WFS_ENDPOINTS.items():
            assert config["base_url"].startswith("http://"), f"{biome} should use HTTP"

    def test_default_poll_interval(self):
        """Test the default poll interval."""
        assert DEFAULT_POLL_INTERVAL_MINUTES == 10

    def test_default_page_size(self):
        """Test the default page size."""
        assert DEFAULT_PAGE_SIZE == 1000

    def test_source_uri(self):
        """Test the source URI constant."""
        assert "terrabrasilis" in SOURCE_URI


@pytest.mark.unit
class TestBuildWfsUrl:
    """Test WFS URL construction."""

    def test_build_amazon_url(self):
        """Test building an Amazon WFS URL."""
        url = build_wfs_url("amazon")
        assert "deter-amz" in url
        assert "service=WFS" in url
        assert "version=2.0.0" in url
        assert "request=GetFeature" in url
        assert "outputFormat=application" in url

    def test_build_cerrado_url(self):
        """Test building a Cerrado WFS URL."""
        url = build_wfs_url("cerrado")
        assert "deter-cerrado" in url
        assert "service=WFS" in url

    def test_build_url_with_cql_filter(self):
        """Test building a URL with CQL filter."""
        url = build_wfs_url("amazon", cql_filter="view_date>='2026-01-01'")
        assert "CQL_FILTER" in url
        assert "2026-01-01" in url

    def test_build_url_with_count(self):
        """Test building a URL with custom count."""
        url = build_wfs_url("amazon", count=50)
        assert "count=50" in url

    def test_build_url_with_start_index(self):
        """Test building a URL with pagination start index."""
        url = build_wfs_url("amazon", start_index=100)
        assert "startIndex=100" in url

    def test_build_url_without_cql_filter(self):
        """Test building a URL without CQL filter."""
        url = build_wfs_url("amazon")
        assert "CQL_FILTER" not in url


@pytest.mark.unit
class TestComputeCentroid:
    """Test polygon centroid computation."""

    def test_multipolygon_centroid(self):
        """Test centroid computation for a MultiPolygon."""
        geometry = {
            "type": "MultiPolygon",
            "coordinates": [[[
                [-48.0, -3.0],
                [-48.0, -2.0],
                [-47.0, -2.0],
                [-47.0, -3.0],
                [-48.0, -3.0],
            ]]]
        }
        lat, lon = compute_centroid(geometry)
        assert -3.0 < lat < -2.0
        assert -48.0 < lon < -47.0

    def test_polygon_centroid(self):
        """Test centroid computation for a Polygon."""
        geometry = {
            "type": "Polygon",
            "coordinates": [[
                [-48.0, -3.0],
                [-48.0, -2.0],
                [-47.0, -2.0],
                [-47.0, -3.0],
                [-48.0, -3.0],
            ]]
        }
        lat, lon = compute_centroid(geometry)
        assert -3.0 < lat < -2.0
        assert -48.0 < lon < -47.0

    def test_empty_geometry(self):
        """Test centroid for empty geometry returns (0, 0)."""
        geometry = {"type": "MultiPolygon", "coordinates": []}
        lat, lon = compute_centroid(geometry)
        assert lat == 0.0
        assert lon == 0.0

    def test_unknown_geometry_type(self):
        """Test centroid for unknown geometry type returns (0, 0)."""
        geometry = {"type": "Point", "coordinates": [-48.0, -3.0]}
        lat, lon = compute_centroid(geometry)
        assert lat == 0.0
        assert lon == 0.0

    def test_single_point_polygon(self):
        """Test centroid for a single-point polygon."""
        geometry = {
            "type": "MultiPolygon",
            "coordinates": [[[[-48.5, -3.5]]]]
        }
        lat, lon = compute_centroid(geometry)
        assert lat == pytest.approx(-3.5)
        assert lon == pytest.approx(-48.5)

    def test_symmetric_rectangle_centroid(self):
        """Test centroid of a symmetric rectangle."""
        geometry = {
            "type": "MultiPolygon",
            "coordinates": [[[
                [0.0, 0.0],
                [10.0, 0.0],
                [10.0, 10.0],
                [0.0, 10.0],
            ]]]
        }
        lat, lon = compute_centroid(geometry)
        assert lat == pytest.approx(5.0)
        assert lon == pytest.approx(5.0)


@pytest.mark.unit
class TestINPEDeterPollerInit:
    """Test INPEDeterPoller initialization."""

    @patch('inpe_deter_brazil.inpe_deter_brazil.BRINPEDETEREventProducer')
    @patch('inpe_deter_brazil.inpe_deter_brazil.Producer')
    def test_init_with_kafka_config(self, mock_producer_class, mock_event_producer):
        """Test initialization with Kafka configuration."""
        mock_producer_instance = Mock()
        mock_producer_class.return_value = mock_producer_instance

        poller = INPEDeterPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test-topic',
            last_polled_file='test_state.json',
        )

        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == 'test_state.json'
        assert poller.poll_interval_minutes == DEFAULT_POLL_INTERVAL_MINUTES
        mock_producer_class.assert_called_once()

    def test_init_without_kafka_config(self):
        """Test initialization without Kafka configuration."""
        poller = INPEDeterPoller(
            kafka_config=None,
            kafka_topic='test-topic',
        )

        assert poller.kafka_topic == 'test-topic'
        assert poller.event_producer is None

    def test_init_with_custom_poll_interval(self):
        """Test initialization with custom poll interval."""
        poller = INPEDeterPoller(poll_interval_minutes=5)
        assert poller.poll_interval_minutes == 5

    def test_init_with_custom_page_size(self):
        """Test initialization with custom page size."""
        poller = INPEDeterPoller(page_size=500)
        assert poller.page_size == 500

    def test_init_default_values(self):
        """Test initialization with all defaults."""
        poller = INPEDeterPoller()
        assert poller.kafka_topic is None
        assert poller.last_polled_file is None
        assert poller.event_producer is None
        assert poller.poll_interval_minutes == DEFAULT_POLL_INTERVAL_MINUTES
        assert poller.page_size == DEFAULT_PAGE_SIZE


@pytest.mark.unit
class TestParseAlert:
    """Test GeoJSON feature parsing into DeforestationAlert objects."""

    def test_parse_amazon_alert(self):
        """Test parsing an Amazon feature."""
        poller = INPEDeterPoller()
        alert = poller.parse_alert(SAMPLE_AMAZON_FEATURE, "amazon")

        assert alert is not None
        assert alert.alert_id == "91537_hist"
        assert alert.biome == "amazon"
        assert alert.classname == "DESMATAMENTO_CR"
        assert alert.view_date == "2026-02-21"
        assert alert.satellite == "AMAZONIA-1"
        assert alert.sensor == "WFI"
        assert alert.area_km2 == pytest.approx(0.07874579199403711)
        assert alert.municipality == "Ipixuna do Para"
        assert alert.state_code == "PA"
        assert alert.path_row == "036016"
        assert alert.publish_month == "2026-02-01"

    def test_parse_cerrado_alert(self):
        """Test parsing a Cerrado feature."""
        poller = INPEDeterPoller()
        alert = poller.parse_alert(SAMPLE_CERRADO_FEATURE, "cerrado")

        assert alert is not None
        assert alert.alert_id == "10001_curr"
        assert alert.biome == "cerrado"
        assert alert.classname == "DESMATAMENTO_CR"
        assert alert.view_date == "2021-09-17"
        assert alert.satellite == "CBERS-4"
        assert alert.sensor == "AWFI"
        assert alert.municipality == "Posse"
        assert alert.state_code == "GO"

    def test_parse_alert_centroid_computation(self):
        """Test that centroid is computed from the polygon geometry."""
        poller = INPEDeterPoller()
        alert = poller.parse_alert(SAMPLE_AMAZON_FEATURE, "amazon")

        assert alert is not None
        assert alert.centroid_latitude != 0.0
        assert alert.centroid_longitude != 0.0
        # Amazon alerts should be in the southern hemisphere
        assert alert.centroid_latitude < 0
        # Amazon alerts should be in the western hemisphere
        assert alert.centroid_longitude < 0

    def test_parse_alert_missing_gid(self):
        """Test that features without gid return None."""
        poller = INPEDeterPoller()
        feature = {
            "type": "Feature",
            "geometry": {"type": "MultiPolygon", "coordinates": []},
            "properties": {"view_date": "2026-01-01"}
        }
        alert = poller.parse_alert(feature, "amazon")
        assert alert is None

    def test_parse_alert_missing_view_date(self):
        """Test that features without view_date return None."""
        poller = INPEDeterPoller()
        feature = {
            "type": "Feature",
            "geometry": {"type": "MultiPolygon", "coordinates": []},
            "properties": {"gid": "12345"}
        }
        alert = poller.parse_alert(feature, "amazon")
        assert alert is None

    def test_parse_alert_no_geometry(self):
        """Test parsing a feature with no geometry."""
        poller = INPEDeterPoller()
        feature = {
            "type": "Feature",
            "geometry": None,
            "properties": {
                "gid": "12345",
                "classname": "DESMATAMENTO_CR",
                "view_date": "2026-01-01",
                "satellite": "CBERS-4",
                "sensor": "AWFI",
                "areamunkm": 0.5,
                "municipality": "Test",
                "uf": "PA",
                "path_row": "001_001",
                "publish_month": "2026-01-01",
            }
        }
        alert = poller.parse_alert(feature, "amazon")
        assert alert is not None
        assert alert.centroid_latitude == 0.0
        assert alert.centroid_longitude == 0.0

    def test_parse_alert_null_optional_fields(self):
        """Test parsing feature with null optional fields."""
        poller = INPEDeterPoller()
        feature = {
            "type": "Feature",
            "geometry": {"type": "MultiPolygon", "coordinates": [[[[0, 0]]]]},
            "properties": {
                "gid": "99999",
                "classname": "DEGRADACAO",
                "view_date": "2026-03-01",
                "satellite": "CBERS-4",
                "sensor": "WFI",
                "areamunkm": 1.0,
                "municipality": None,
                "uf": None,
                "path_row": None,
                "publish_month": None,
            }
        }
        alert = poller.parse_alert(feature, "cerrado")
        assert alert is not None
        assert alert.municipality is None
        assert alert.state_code is None
        assert alert.path_row is None
        assert alert.publish_month is None

    def test_parse_alert_biome_passed_through(self):
        """Test that the biome parameter is correctly set."""
        poller = INPEDeterPoller()
        alert_amz = poller.parse_alert(SAMPLE_AMAZON_FEATURE, "amazon")
        alert_cer = poller.parse_alert(SAMPLE_CERRADO_FEATURE, "cerrado")
        assert alert_amz.biome == "amazon"
        assert alert_cer.biome == "cerrado"

    def test_parse_alert_area_from_areamunkm(self):
        """Test that area_km2 is correctly read from areamunkm."""
        poller = INPEDeterPoller()
        alert = poller.parse_alert(SAMPLE_AMAZON_FEATURE, "amazon")
        assert alert.area_km2 == pytest.approx(0.07874579199403711)

    def test_parse_alert_zero_area(self):
        """Test parsing feature with zero area."""
        poller = INPEDeterPoller()
        feature = {
            "type": "Feature",
            "geometry": {"type": "MultiPolygon", "coordinates": [[[[0, 0]]]]},
            "properties": {
                "gid": "zero_area",
                "classname": "DESMATAMENTO_CR",
                "view_date": "2026-01-01",
                "satellite": "CBERS-4",
                "sensor": "WFI",
                "areamunkm": 0.0,
            }
        }
        alert = poller.parse_alert(feature, "amazon")
        assert alert is not None
        assert alert.area_km2 == 0.0

    def test_parse_alert_none_area(self):
        """Test parsing feature with None area."""
        poller = INPEDeterPoller()
        feature = {
            "type": "Feature",
            "geometry": {"type": "MultiPolygon", "coordinates": [[[[0, 0]]]]},
            "properties": {
                "gid": "none_area",
                "classname": "DESMATAMENTO_CR",
                "view_date": "2026-01-01",
                "satellite": "CBERS-4",
                "sensor": "WFI",
                "areamunkm": None,
            }
        }
        alert = poller.parse_alert(feature, "amazon")
        assert alert is not None
        assert alert.area_km2 == 0.0


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

    def test_parse_connection_string_with_bootstrap_server(self):
        """Test parsing a connection string with BootstrapServer."""
        conn_str = "BootstrapServer=kafka:9092;EntityPath=test-topic"

        result = parse_connection_string(conn_str)

        assert result['bootstrap.servers'] == 'kafka:9092'
        assert result['kafka_topic'] == 'test-topic'


@pytest.mark.unit
class TestStateManagement:
    """Test state file load/save operations."""

    def test_load_state_no_file(self):
        """Test loading state when file doesn't exist."""
        poller = INPEDeterPoller(last_polled_file='nonexistent_file.json')
        state = poller.load_state()
        assert state == {}

    def test_load_state_none_file(self):
        """Test loading state when last_polled_file is None."""
        poller = INPEDeterPoller(last_polled_file=None)
        state = poller.load_state()
        assert state == {}

    def test_save_and_load_state(self):
        """Test saving and loading state roundtrip."""
        state_file = 'test_inpe_state_roundtrip.json'
        try:
            poller = INPEDeterPoller(last_polled_file=state_file)
            state = {
                "amazon": {
                    "seen_ids": ["id1", "id2"],
                    "last_view_date": "2026-01-01"
                }
            }
            poller.save_state(state)

            loaded_state = poller.load_state()
            assert loaded_state == state
        finally:
            if os.path.exists(state_file):
                os.remove(state_file)

    def test_load_state_corrupt_json(self):
        """Test loading state from a corrupt JSON file."""
        state_file = 'test_inpe_state_corrupt.json'
        try:
            with open(state_file, 'w', encoding='utf-8') as f:
                f.write("not valid json{{{")
            poller = INPEDeterPoller(last_polled_file=state_file)
            state = poller.load_state()
            assert state == {}
        finally:
            if os.path.exists(state_file):
                os.remove(state_file)

    def test_save_state_none_file(self):
        """Test saving state when file path is None (should not error)."""
        poller = INPEDeterPoller(last_polled_file=None)
        poller.save_state({"test": "data"})


@pytest.mark.unit
class TestDeforestationAlertDataClass:
    """Test DeforestationAlert dataclass methods."""

    def test_alert_to_json(self):
        """Test DeforestationAlert serialization to JSON."""
        from inpe_deter_brazil_producer_data.br.inpe.deter.deforestationalert import DeforestationAlert

        alert = DeforestationAlert(
            alert_id="91537_hist",
            biome="amazon",
            classname="DESMATAMENTO_CR",
            view_date="2026-02-21",
            satellite="AMAZONIA-1",
            sensor="WFI",
            area_km2=0.078,
            municipality="Ipixuna do Para",
            state_code="PA",
            path_row="036016",
            publish_month="2026-02-01",
            centroid_latitude=-2.93,
            centroid_longitude=-48.05,
        )

        json_result = alert.to_byte_array("application/json")
        assert json_result is not None
        json_str = json_result if isinstance(json_result, str) else json_result.decode('utf-8')
        assert "91537_hist" in json_str
        assert "amazon" in json_str
        assert "DESMATAMENTO_CR" in json_str

    def test_alert_to_avro(self):
        """Test DeforestationAlert serialization to Avro binary."""
        from inpe_deter_brazil_producer_data.br.inpe.deter.deforestationalert import DeforestationAlert

        alert = DeforestationAlert(
            alert_id="10001_curr",
            biome="cerrado",
            classname="DESMATAMENTO_CR",
            view_date="2021-09-17",
            satellite="CBERS-4",
            sensor="AWFI",
            area_km2=0.542,
            municipality="Posse",
            state_code="GO",
            path_row="156_117",
            publish_month="2021-09-01",
            centroid_latitude=-14.05,
            centroid_longitude=-46.35,
        )

        avro_bytes = alert.to_byte_array("avro/binary")
        assert avro_bytes is not None
        assert len(avro_bytes) > 0

    def test_alert_to_json_with_nulls(self):
        """Test serialization with null optional fields."""
        from inpe_deter_brazil_producer_data.br.inpe.deter.deforestationalert import DeforestationAlert

        alert = DeforestationAlert(
            alert_id="test_null",
            biome="amazon",
            classname="DEGRADACAO",
            view_date="2026-03-01",
            satellite="CBERS-4",
            sensor="WFI",
            area_km2=1.0,
            municipality=None,
            state_code=None,
            path_row=None,
            publish_month=None,
            centroid_latitude=-5.0,
            centroid_longitude=-50.0,
        )

        json_result = alert.to_byte_array("application/json")
        assert json_result is not None

    def test_alert_from_serializer_dict(self):
        """Test creating alert from dictionary."""
        from inpe_deter_brazil_producer_data.br.inpe.deter.deforestationalert import DeforestationAlert

        data = {
            "alert_id": "12345",
            "biome": "amazon",
            "classname": "MINERACAO",
            "view_date": "2026-01-15",
            "satellite": "AMAZONIA-1",
            "sensor": "MSI",
            "area_km2": 2.5,
            "municipality": "Manaus",
            "state_code": "AM",
            "path_row": "001_001",
            "publish_month": "2026-01-01",
            "centroid_latitude": -3.1,
            "centroid_longitude": -60.0,
        }

        alert = DeforestationAlert.from_serializer_dict(data)
        assert alert.alert_id == "12345"
        assert alert.biome == "amazon"
        assert alert.classname == "MINERACAO"
        assert alert.area_km2 == 2.5

    def test_alert_avro_roundtrip(self):
        """Test Avro encode/decode roundtrip."""
        from inpe_deter_brazil_producer_data.br.inpe.deter.deforestationalert import DeforestationAlert

        alert = DeforestationAlert(
            alert_id="roundtrip_test",
            biome="cerrado",
            classname="CS_DESORDENADO",
            view_date="2026-06-15",
            satellite="CBERS-4",
            sensor="AWFI",
            area_km2=3.14,
            municipality="Brasilia",
            state_code="DF",
            path_row="200_100",
            publish_month="2026-06-01",
            centroid_latitude=-15.8,
            centroid_longitude=-47.9,
        )

        avro_bytes = alert.to_byte_array("avro/binary")
        restored = DeforestationAlert.from_data(avro_bytes, "avro/binary")
        assert restored.alert_id == "roundtrip_test"
        assert restored.biome == "cerrado"
        assert restored.area_km2 == pytest.approx(3.14)

    def test_alert_json_roundtrip(self):
        """Test JSON encode/decode roundtrip."""
        from inpe_deter_brazil_producer_data.br.inpe.deter.deforestationalert import DeforestationAlert

        alert = DeforestationAlert(
            alert_id="json_rt",
            biome="amazon",
            classname="DESMATAMENTO_CR",
            view_date="2026-01-01",
            satellite="AMAZONIA-1",
            sensor="WFI",
            area_km2=0.5,
            municipality="Test City",
            state_code="PA",
            path_row="010_010",
            publish_month="2026-01-01",
            centroid_latitude=-2.5,
            centroid_longitude=-48.0,
        )

        json_bytes = alert.to_byte_array("application/json")
        restored = DeforestationAlert.from_data(json_bytes, "application/json")
        assert restored.alert_id == "json_rt"
        assert restored.municipality == "Test City"


@pytest.mark.unit
class TestParseAlertEdgeCases:
    """Additional edge case tests for alert parsing."""

    def test_parse_alert_empty_classname(self):
        """Test parsing a feature with empty classname."""
        poller = INPEDeterPoller()
        feature = {
            "type": "Feature",
            "geometry": {"type": "MultiPolygon", "coordinates": [[[[0, 0]]]]},
            "properties": {
                "gid": "empty_class",
                "classname": "",
                "view_date": "2026-01-01",
                "satellite": "CBERS-4",
                "sensor": "WFI",
                "areamunkm": 0.1,
            }
        }
        alert = poller.parse_alert(feature, "amazon")
        assert alert is not None
        assert alert.classname == ""

    def test_parse_alert_different_classnames(self):
        """Test parsing features with different deforestation classes."""
        poller = INPEDeterPoller()
        classes = ["DESMATAMENTO_CR", "DEGRADACAO", "MINERACAO", "CS_DESORDENADO"]
        for cls in classes:
            feature = {
                "type": "Feature",
                "geometry": {"type": "MultiPolygon", "coordinates": [[[[0, 0]]]]},
                "properties": {
                    "gid": f"class_{cls}",
                    "classname": cls,
                    "view_date": "2026-01-01",
                    "satellite": "CBERS-4",
                    "sensor": "WFI",
                    "areamunkm": 0.1,
                }
            }
            alert = poller.parse_alert(feature, "amazon")
            assert alert is not None
            assert alert.classname == cls

    def test_parse_alert_string_gid(self):
        """Test that gid is always converted to string."""
        poller = INPEDeterPoller()
        feature = {
            "type": "Feature",
            "geometry": {"type": "MultiPolygon", "coordinates": [[[[0, 0]]]]},
            "properties": {
                "gid": 12345,
                "classname": "DESMATAMENTO_CR",
                "view_date": "2026-01-01",
                "satellite": "CBERS-4",
                "sensor": "WFI",
                "areamunkm": 0.1,
            }
        }
        alert = poller.parse_alert(feature, "amazon")
        assert alert is not None
        assert isinstance(alert.alert_id, str)
        assert alert.alert_id == "12345"

    def test_parse_alert_missing_properties(self):
        """Test parsing a feature with empty properties."""
        poller = INPEDeterPoller()
        feature = {
            "type": "Feature",
            "geometry": {"type": "MultiPolygon", "coordinates": []},
            "properties": {}
        }
        alert = poller.parse_alert(feature, "amazon")
        assert alert is None
