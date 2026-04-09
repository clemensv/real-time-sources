"""Unit tests for Australian State Wildfires Bridge."""

import json
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from australia_wildfires_producer_data import FireIncident

from australia_wildfires.australia_wildfires import (
    AustraliaWildfiresAPI,
    parse_connection_string,
    feed_incidents,
    _load_state,
    _save_state,
    _parse_nsw_description,
    _extract_point_from_geometry,
    _incident_id_from_guid,
    _parse_size_hectares,
    _parse_nsw_updated,
    _polygon_centroid,
    NSW_RFS_URL,
    VIC_EMERGENCY_URL,
    QLD_FIRE_URL,
)


# ---- Sample data from probed endpoints ----

SAMPLE_NSW_FEATURE = {
    "type": "Feature",
    "geometry": {
        "type": "GeometryCollection",
        "geometries": [
            {"type": "Point", "coordinates": [151.59561, -29.72272]},
            {
                "type": "GeometryCollection",
                "geometries": [
                    {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [151.594, -29.721],
                                [151.595, -29.722],
                                [151.596, -29.723],
                                [151.594, -29.721],
                            ]
                        ],
                    }
                ],
            },
        ],
    },
    "properties": {
        "title": "(GWYDIR HWY), MATHESON",
        "link": "https://www.rfs.nsw.gov.au/fire-information/fires-near-me",
        "category": "Advice",
        "guid": "https://incidents.rfs.nsw.gov.au/api/v1/incidents/653509",
        "guid_isPermaLink": "true",
        "pubDate": "8/04/2026 2:08:00 PM",
        "description": "ALERT LEVEL: Advice <br />LOCATION: B76 (GWYDIR HWY), MATHESON 2370 <br />COUNCIL AREA: Glen Innes Severn <br />STATUS: Under control <br />TYPE: Grass Fire <br />FIRE: Yes <br />SIZE: 0 ha <br />RESPONSIBLE AGENCY: Rural Fire Service <br />UPDATED: 9 Apr 2026 00:08",
    },
}

SAMPLE_NSW_GEOJSON = {
    "type": "FeatureCollection",
    "features": [SAMPLE_NSW_FEATURE],
}


SAMPLE_VIC_FIRE_FEATURE = {
    "type": "Feature",
    "geometry": {
        "type": "GeometryCollection",
        "geometries": [
            {"type": "Point", "coordinates": [143.063, -37.387]},
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [143.08, -37.39],
                        [143.09, -37.38],
                        [143.07, -37.37],
                        [143.08, -37.39],
                    ]
                ],
            },
        ],
    },
    "properties": {
        "feedType": "warning",
        "cap": {
            "category": "Fire",
            "event": "Grass Fire",
            "eventCode": "grassFire",
            "urgency": "Unknown",
            "severity": "Unknown",
            "certainty": "Observed",
            "contact": "test@emv.vic.gov.au",
            "senderName": "Country Fire Authority",
            "responseType": "None",
        },
        "sourceOrg": "EMV",
        "sourceId": "41825",
        "sourceFeed": "cop-cap",
        "sourceTitle": "Community Information",
        "id": "41825",
        "category1": "Community Update",
        "category2": "Fire",
        "status": "Unknown",
        "name": "Community Information",
        "action": "Stay Informed",
        "statewide": "N",
        "location": "Ballyrogan, Buangor, Dobie",
        "created": "2026-04-08T10:30:06+10:00",
        "updated": "2026-04-08T10:30:06+10:00",
        "webHeadline": None,
        "webBody": "<div>Test</div>",
        "text": "COMMUNITY INFORMATION - GRASS FIRE",
        "sizeFmt": None,
    },
}

SAMPLE_VIC_NON_FIRE_FEATURE = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [144.0, -37.0]},
    "properties": {
        "feedType": "warning",
        "cap": {"category": "Met", "event": "Flood"},
        "sourceId": "99999",
        "id": "99999",
        "category1": "Warning",
        "category2": "Flood",
        "status": "Active",
        "name": "Flood Warning",
        "location": "Test River",
        "created": "2026-04-08T10:00:00+10:00",
        "updated": "2026-04-08T10:00:00+10:00",
    },
}

SAMPLE_VIC_GEOJSON = {
    "type": "FeatureCollection",
    "features": [SAMPLE_VIC_FIRE_FEATURE, SAMPLE_VIC_NON_FIRE_FEATURE],
}


SAMPLE_QLD_FEATURE = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [151.926, -27.414, 0],
                [151.919, -27.494, 0],
                [152.047, -27.501, 0],
                [152.053, -27.421, 0],
                [151.926, -27.414, 0],
            ]
        ],
    },
    "properties": {
        "OBJECTID": 2688,
        "UniqueID": "IF39-5661721",
        "WarningTitle": "AVOID SMOKE (HAZARD REDUCTION BURN) - Cabarlah (near Toowoomba)",
        "WarningLevel": "Advice",
        "CallToAction": "AVOID SMOKE (HAZARD REDUCTION BURN)",
        "WarningText": "Test warning text",
        "Header": "Smoke is currently affecting Cabarlah, Highfields, Ballard and surrounding areas.",
        "Impacts": "- Smoke can make it hard for some people to breathe.",
        "LeaveSafely": None,
        "FurtherInformation": "Visit QFD website for more info.",
    },
}

SAMPLE_QLD_GEOJSON = {
    "type": "FeatureCollection",
    "name": "QFDWarnings",
    "features": [SAMPLE_QLD_FEATURE],
}


# ---- Test Classes ----


@pytest.mark.unit
class TestParseNSWDescription:
    def test_parse_full_description(self):
        desc = "ALERT LEVEL: Advice <br />LOCATION: B76 (GWYDIR HWY), MATHESON 2370 <br />COUNCIL AREA: Glen Innes Severn <br />STATUS: Under control <br />TYPE: Grass Fire <br />FIRE: Yes <br />SIZE: 0 ha <br />RESPONSIBLE AGENCY: Rural Fire Service <br />UPDATED: 9 Apr 2026 00:08"
        fields = _parse_nsw_description(desc)
        assert fields["ALERT LEVEL"] == "Advice"
        assert fields["LOCATION"] == "B76 (GWYDIR HWY), MATHESON 2370"
        assert fields["STATUS"] == "Under control"
        assert fields["TYPE"] == "Grass Fire"
        assert fields["SIZE"] == "0 ha"
        assert fields["RESPONSIBLE AGENCY"] == "Rural Fire Service"
        assert fields["UPDATED"] == "9 Apr 2026 00:08"

    def test_parse_empty_description(self):
        assert _parse_nsw_description("") == {}

    def test_parse_partial_description(self):
        desc = "ALERT LEVEL: Emergency Warning <br />STATUS: Out of control <br />"
        fields = _parse_nsw_description(desc)
        assert fields["ALERT LEVEL"] == "Emergency Warning"
        assert fields["STATUS"] == "Out of control"
        assert "LOCATION" not in fields


@pytest.mark.unit
class TestExtractPointFromGeometry:
    def test_point_geometry(self):
        geo = {"type": "Point", "coordinates": [151.2, -33.8]}
        lat, lon = _extract_point_from_geometry(geo)
        assert lat == pytest.approx(-33.8)
        assert lon == pytest.approx(151.2)

    def test_polygon_geometry(self):
        geo = {
            "type": "Polygon",
            "coordinates": [
                [[150.0, -33.0], [152.0, -33.0], [152.0, -35.0], [150.0, -35.0], [150.0, -33.0]]
            ],
        }
        lat, lon = _extract_point_from_geometry(geo)
        assert lat is not None
        assert lon is not None
        assert lat == pytest.approx(-33.8, abs=0.5)
        assert lon == pytest.approx(150.8, abs=0.5)

    def test_multipolygon_geometry(self):
        geo = {
            "type": "MultiPolygon",
            "coordinates": [
                [[[150.0, -33.0], [152.0, -33.0], [152.0, -35.0], [150.0, -35.0], [150.0, -33.0]]],
            ],
        }
        lat, lon = _extract_point_from_geometry(geo)
        assert lat is not None
        assert lon is not None

    def test_geometry_collection_prefers_point(self):
        geo = {
            "type": "GeometryCollection",
            "geometries": [
                {
                    "type": "Polygon",
                    "coordinates": [[[150.0, -33.0], [152.0, -33.0], [152.0, -35.0], [150.0, -33.0]]],
                },
                {"type": "Point", "coordinates": [151.5, -33.9]},
            ],
        }
        lat, lon = _extract_point_from_geometry(geo)
        assert lat == pytest.approx(-33.9)
        assert lon == pytest.approx(151.5)

    def test_geometry_collection_falls_back_to_polygon(self):
        geo = {
            "type": "GeometryCollection",
            "geometries": [
                {
                    "type": "GeometryCollection",
                    "geometries": [
                        {
                            "type": "Polygon",
                            "coordinates": [
                                [[150.0, -33.0], [152.0, -33.0], [152.0, -35.0], [150.0, -33.0]]
                            ],
                        }
                    ],
                }
            ],
        }
        lat, lon = _extract_point_from_geometry(geo)
        assert lat is not None

    def test_empty_geometry(self):
        lat, lon = _extract_point_from_geometry(None)
        assert lat is None
        assert lon is None

    def test_unknown_geometry_type(self):
        geo = {"type": "LineString", "coordinates": [[150.0, -33.0], [151.0, -34.0]]}
        lat, lon = _extract_point_from_geometry(geo)
        assert lat is None
        assert lon is None


@pytest.mark.unit
class TestPolygonCentroid:
    def test_simple_ring(self):
        ring = [[0.0, 0.0], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0], [0.0, 0.0]]
        lat, lon = _polygon_centroid(ring)
        assert lat == pytest.approx(4.0)
        assert lon == pytest.approx(4.0)

    def test_empty_ring(self):
        assert _polygon_centroid([]) == (None, None)


@pytest.mark.unit
class TestIncidentIdFromGuid:
    def test_rfs_guid_url(self):
        guid = "https://incidents.rfs.nsw.gov.au/api/v1/incidents/653509"
        assert _incident_id_from_guid(guid) == "653509"

    def test_simple_id(self):
        assert _incident_id_from_guid("12345") == "12345"

    def test_trailing_slash(self):
        assert _incident_id_from_guid("https://example.com/incidents/999/") == "999"


@pytest.mark.unit
class TestParseSizeHectares:
    def test_numeric_with_ha(self):
        assert _parse_size_hectares("150 ha") == pytest.approx(150.0)

    def test_zero(self):
        assert _parse_size_hectares("0 ha") == pytest.approx(0.0)

    def test_with_comma(self):
        assert _parse_size_hectares("1,500 ha") == pytest.approx(1500.0)

    def test_plain_number(self):
        assert _parse_size_hectares("42") == pytest.approx(42.0)

    def test_empty_string(self):
        assert _parse_size_hectares("") is None

    def test_none(self):
        assert _parse_size_hectares(None) is None

    def test_non_numeric(self):
        assert _parse_size_hectares("unknown") is None


@pytest.mark.unit
class TestParseNSWUpdated:
    def test_standard_format(self):
        result = _parse_nsw_updated("9 Apr 2026 00:08")
        assert "2026-04-09" in result
        assert "+00:00" in result

    def test_fallback_to_now(self):
        result = _parse_nsw_updated("invalid date")
        # Should return a valid ISO datetime
        assert "T" in result


@pytest.mark.unit
class TestParseNSWFeature:
    def test_parse_nsw_feature(self):
        incident = AustraliaWildfiresAPI._parse_nsw_feature(SAMPLE_NSW_FEATURE)
        assert incident is not None
        assert incident.incident_id == "653509"
        assert incident.state == "NSW"
        assert incident.title == "(GWYDIR HWY), MATHESON"
        assert incident.alert_level == "Advice"
        assert incident.status == "Under control"
        assert incident.location == "B76 (GWYDIR HWY), MATHESON 2370"
        assert incident.latitude == pytest.approx(-29.72272)
        assert incident.longitude == pytest.approx(151.59561)
        assert incident.size_hectares == pytest.approx(0.0)
        assert incident.type == "Grass Fire"
        assert incident.responsible_agency == "Rural Fire Service"
        assert incident.source_url == "https://incidents.rfs.nsw.gov.au/api/v1/incidents/653509"

    def test_parse_nsw_feature_no_guid(self):
        feature = {"properties": {"title": "Test"}, "geometry": None}
        assert AustraliaWildfiresAPI._parse_nsw_feature(feature) is None


@pytest.mark.unit
class TestParseVICFeature:
    def test_parse_vic_fire_feature(self):
        incident = AustraliaWildfiresAPI._parse_vic_feature(SAMPLE_VIC_FIRE_FEATURE)
        assert incident is not None
        assert incident.incident_id == "41825"
        assert incident.state == "VIC"
        assert incident.title == "Community Information"
        assert incident.alert_level == "Community Update"
        assert incident.status == "Unknown"
        assert incident.location == "Ballyrogan, Buangor, Dobie"
        assert incident.latitude == pytest.approx(-37.387)
        assert incident.longitude == pytest.approx(143.063)
        assert incident.type == "Grass Fire"
        assert incident.responsible_agency == "Country Fire Authority"
        assert "41825" in incident.source_url

    def test_parse_vic_feature_no_id(self):
        feature = {"properties": {}, "geometry": None}
        assert AustraliaWildfiresAPI._parse_vic_feature(feature) is None

    def test_parse_vic_feature_size_fmt(self):
        feature = dict(SAMPLE_VIC_FIRE_FEATURE)
        feature["properties"] = dict(feature["properties"])
        feature["properties"]["sizeFmt"] = "250 ha"
        incident = AustraliaWildfiresAPI._parse_vic_feature(feature)
        assert incident is not None
        assert incident.size_hectares == pytest.approx(250.0)


@pytest.mark.unit
class TestParseQLDFeature:
    def test_parse_qld_feature(self):
        incident = AustraliaWildfiresAPI._parse_qld_feature(SAMPLE_QLD_FEATURE)
        assert incident is not None
        assert incident.incident_id == "IF39-5661721"
        assert incident.state == "QLD"
        assert "Cabarlah" in incident.title
        assert incident.alert_level == "Advice"
        assert incident.status is None
        assert incident.location is not None
        assert "Smoke" in incident.location or "Cabarlah" in incident.location
        assert incident.latitude is not None
        assert incident.longitude is not None
        assert incident.type == "Hazard Reduction"
        assert incident.responsible_agency == "Queensland Fire Department"
        assert incident.source_url == QLD_FIRE_URL

    def test_parse_qld_feature_no_unique_id(self):
        feature = {"properties": {"WarningTitle": "Test"}, "geometry": None}
        assert AustraliaWildfiresAPI._parse_qld_feature(feature) is None

    def test_parse_qld_bushfire_type(self):
        feature = dict(SAMPLE_QLD_FEATURE)
        feature["properties"] = dict(feature["properties"])
        feature["properties"]["CallToAction"] = "BUSHFIRE WARNING"
        incident = AustraliaWildfiresAPI._parse_qld_feature(feature)
        assert incident is not None
        assert incident.type == "Bush Fire"

    def test_parse_qld_grass_fire_type(self):
        feature = dict(SAMPLE_QLD_FEATURE)
        feature["properties"] = dict(feature["properties"])
        feature["properties"]["CallToAction"] = "GRASS FIRE WARNING"
        incident = AustraliaWildfiresAPI._parse_qld_feature(feature)
        assert incident is not None
        assert incident.type == "Grass Fire"


@pytest.mark.unit
class TestFetchNSWIncidents:
    def test_fetch_nsw_success(self):
        api = AustraliaWildfiresAPI()
        mock_resp = MagicMock()
        mock_resp.json.return_value = SAMPLE_NSW_GEOJSON
        mock_resp.raise_for_status = MagicMock()
        with patch.object(api.session, "get", return_value=mock_resp):
            incidents = api.fetch_nsw_incidents()
        assert len(incidents) == 1
        assert incidents[0].state == "NSW"

    def test_fetch_nsw_network_error(self):
        api = AustraliaWildfiresAPI()
        with patch.object(api.session, "get", side_effect=Exception("timeout")):
            incidents = api.fetch_nsw_incidents()
        assert incidents == []


@pytest.mark.unit
class TestFetchVICIncidents:
    def test_fetch_vic_filters_fire_only(self):
        api = AustraliaWildfiresAPI()
        mock_resp = MagicMock()
        mock_resp.json.return_value = SAMPLE_VIC_GEOJSON
        mock_resp.raise_for_status = MagicMock()
        with patch.object(api.session, "get", return_value=mock_resp):
            incidents = api.fetch_vic_incidents()
        # Should only include fire feature, not flood
        assert len(incidents) == 1
        assert incidents[0].state == "VIC"
        assert incidents[0].incident_id == "41825"

    def test_fetch_vic_network_error(self):
        api = AustraliaWildfiresAPI()
        with patch.object(api.session, "get", side_effect=Exception("timeout")):
            incidents = api.fetch_vic_incidents()
        assert incidents == []


@pytest.mark.unit
class TestFetchQLDIncidents:
    def test_fetch_qld_success(self):
        api = AustraliaWildfiresAPI()
        mock_resp = MagicMock()
        mock_resp.json.return_value = SAMPLE_QLD_GEOJSON
        mock_resp.raise_for_status = MagicMock()
        with patch.object(api.session, "get", return_value=mock_resp):
            incidents = api.fetch_qld_incidents()
        assert len(incidents) == 1
        assert incidents[0].state == "QLD"

    def test_fetch_qld_network_error(self):
        api = AustraliaWildfiresAPI()
        with patch.object(api.session, "get", side_effect=Exception("timeout")):
            incidents = api.fetch_qld_incidents()
        assert incidents == []


@pytest.mark.unit
class TestConnectionString:
    def test_parse_plain_bootstrap(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=my-topic"
        config = parse_connection_string(cs)
        assert config["bootstrap.servers"] == "localhost:9092"
        assert config["_entity_path"] == "my-topic"

    def test_parse_event_hubs(self):
        cs = "Endpoint=sb://ns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=topic"
        config = parse_connection_string(cs)
        assert "bootstrap.servers" in config
        assert config["sasl.mechanism"] == "PLAIN"
        assert config["security.protocol"] == "SASL_SSL"

    def test_parse_empty_parts(self):
        config = parse_connection_string("")
        assert config == {}


@pytest.mark.unit
class TestFeedIncidents:
    def test_feed_emits_new_incidents(self):
        api = AustraliaWildfiresAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        previous = {}

        with patch.object(api, "fetch_nsw_incidents", return_value=[
            FireIncident(incident_id="1", state="NSW", title="Test Fire", alert_level="Advice",
                         status="Under control", location="Test", latitude=-33.0, longitude=151.0,
                         size_hectares=10.0, type="Bush Fire", responsible_agency="RFS",
                         updated="2026-04-09T00:00:00+00:00",
                         source_url="https://example.com/1")
        ]), patch.object(api, "fetch_vic_incidents", return_value=[]), \
             patch.object(api, "fetch_qld_incidents", return_value=[]):
            count = feed_incidents(api, mock_producer, previous)

        assert count == 1
        mock_producer.send_au_gov_emergency_wildfires_fire_incident.assert_called_once()
        assert "NSW/1" in previous

    def test_feed_deduplicates(self):
        api = AustraliaWildfiresAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        previous = {"NSW/1": "2026-04-09T00:00:00+00:00"}

        with patch.object(api, "fetch_nsw_incidents", return_value=[
            FireIncident(incident_id="1", state="NSW", title="Test Fire", alert_level="Advice",
                         status="Under control", location="Test", latitude=-33.0, longitude=151.0,
                         size_hectares=10.0, type="Bush Fire", responsible_agency="RFS",
                         updated="2026-04-09T00:00:00+00:00",
                         source_url="https://example.com/1")
        ]), patch.object(api, "fetch_vic_incidents", return_value=[]), \
             patch.object(api, "fetch_qld_incidents", return_value=[]):
            count = feed_incidents(api, mock_producer, previous)

        assert count == 0
        mock_producer.send_au_gov_emergency_wildfires_fire_incident.assert_not_called()

    def test_feed_emits_updated_incident(self):
        api = AustraliaWildfiresAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        previous = {"NSW/1": "2026-04-09T00:00:00+00:00"}

        with patch.object(api, "fetch_nsw_incidents", return_value=[
            FireIncident(incident_id="1", state="NSW", title="Test Fire", alert_level="Emergency Warning",
                         status="Out of control", location="Test", latitude=-33.0, longitude=151.0,
                         size_hectares=50.0, type="Bush Fire", responsible_agency="RFS",
                         updated="2026-04-09T01:00:00+00:00",
                         source_url="https://example.com/1")
        ]), patch.object(api, "fetch_vic_incidents", return_value=[]), \
             patch.object(api, "fetch_qld_incidents", return_value=[]):
            count = feed_incidents(api, mock_producer, previous)

        assert count == 1
        assert previous["NSW/1"] == "2026-04-09T01:00:00+00:00"

    def test_feed_multi_state(self):
        api = AustraliaWildfiresAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        previous = {}

        nsw_incident = FireIncident(
            incident_id="1", state="NSW", title="NSW Fire", alert_level="Advice",
            status=None, location=None, latitude=None, longitude=None,
            size_hectares=None, type=None, responsible_agency=None,
            updated="2026-04-09T00:00:00+00:00", source_url="https://example.com")
        vic_incident = FireIncident(
            incident_id="2", state="VIC", title="VIC Fire", alert_level="Watch and Act",
            status=None, location=None, latitude=None, longitude=None,
            size_hectares=None, type=None, responsible_agency=None,
            updated="2026-04-09T00:00:00+00:00", source_url="https://example.com")
        qld_incident = FireIncident(
            incident_id="3", state="QLD", title="QLD Fire", alert_level="Emergency Warning",
            status=None, location=None, latitude=None, longitude=None,
            size_hectares=None, type=None, responsible_agency=None,
            updated="2026-04-09T00:00:00+00:00", source_url="https://example.com")

        with patch.object(api, "fetch_nsw_incidents", return_value=[nsw_incident]), \
             patch.object(api, "fetch_vic_incidents", return_value=[vic_incident]), \
             patch.object(api, "fetch_qld_incidents", return_value=[qld_incident]):
            count = feed_incidents(api, mock_producer, previous)

        assert count == 3
        assert len(previous) == 3


@pytest.mark.unit
class TestState:
    def test_load_state_missing_file(self, tmp_path):
        assert _load_state(str(tmp_path / "nonexistent.json")) == {}

    def test_save_and_load_state(self, tmp_path):
        path = str(tmp_path / "state.json")
        data = {"NSW/1": "2026-04-09T00:00:00+00:00", "VIC/2": "2026-04-09T01:00:00+00:00"}
        _save_state(path, data)
        loaded = _load_state(path)
        assert loaded == data

    def test_save_state_truncates(self, tmp_path):
        path = str(tmp_path / "state.json")
        data = {str(i): str(i) for i in range(110000)}
        _save_state(path, data)
        loaded = _load_state(path)
        assert len(loaded) <= 50000


@pytest.mark.unit
class TestFireIncidentDataclass:
    def test_create_instance(self):
        instance = FireIncident.create_instance()
        assert instance.incident_id == "test-incident-001"
        assert instance.state == "NSW"
        assert instance.alert_level == "Advice"

    def test_to_serializer_dict(self):
        instance = FireIncident(
            incident_id="1", state="NSW", title="Test", alert_level="Advice",
            status=None, location=None, latitude=None, longitude=None,
            size_hectares=None, type=None, responsible_agency=None,
            updated="2026-01-01T00:00:00+00:00", source_url="https://example.com")
        d = instance.to_serializer_dict()
        assert d["incident_id"] == "1"
        assert d["state"] == "NSW"
        assert d["status"] is None

    def test_from_serializer_dict(self):
        d = {
            "incident_id": "42",
            "state": "VIC",
            "title": "Test Fire",
            "alert_level": "Emergency Warning",
            "status": "Active",
            "location": "Melbourne",
            "latitude": -37.8,
            "longitude": 144.9,
            "size_hectares": 100.0,
            "type": "Bush Fire",
            "responsible_agency": "CFA",
            "updated": "2026-04-09T00:00:00+00:00",
            "source_url": "https://example.com",
        }
        incident = FireIncident.from_serializer_dict(d)
        assert incident.incident_id == "42"
        assert incident.state == "VIC"
        assert incident.size_hectares == 100.0

    def test_to_json_roundtrip(self):
        instance = FireIncident.create_instance()
        json_str = instance.to_json()
        loaded = json.loads(json_str)
        assert loaded["incident_id"] == "test-incident-001"
        restored = FireIncident.from_data(loaded)
        assert restored.incident_id == instance.incident_id

    def test_to_byte_array_json(self):
        instance = FireIncident.create_instance()
        data = instance.to_byte_array("application/json")
        assert isinstance(data, (bytes, str))

    def test_from_data_none(self):
        assert FireIncident.from_data(None) is None

    def test_from_data_dict(self):
        d = {
            "incident_id": "1", "state": "NSW", "title": "T", "alert_level": "A",
            "status": None, "location": None, "latitude": None, "longitude": None,
            "size_hectares": None, "type": None, "responsible_agency": None,
            "updated": "2026-01-01T00:00:00+00:00", "source_url": "https://x.com",
        }
        result = FireIncident.from_data(d)
        assert result.incident_id == "1"


@pytest.mark.unit
class TestEndpointURLs:
    def test_nsw_url(self):
        assert "rfs.nsw.gov.au" in NSW_RFS_URL

    def test_vic_url(self):
        assert "emergency.vic.gov.au" in VIC_EMERGENCY_URL

    def test_qld_url(self):
        assert "psba-qld-gov-au" in QLD_FIRE_URL
