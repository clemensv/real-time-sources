"""Unit tests for the Autobahn bridge."""

import json
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.modules.pop("autobahn", None)

from autobahn.autobahn import (
    build_family_snapshot,
    determine_event_family,
    diff_items,
    merge_snapshots,
    normalize_road_ids,
    parse_charging_points,
    parse_connection_string,
    parse_resources_argument,
    parse_roads_argument,
)


class TestArgumentParsing:
    def test_normalize_road_ids_strips_whitespace_and_duplicates(self):
        assert normalize_road_ids(["A1", " A1 ", "A60 ", "A3"]) == ["A1", "A60", "A3"]

    def test_parse_resources_argument_returns_all_for_star(self):
        resources = parse_resources_argument("*")
        assert "roadworks" in resources
        assert "electric_charging_station" in resources
        assert "webcam" in resources

    def test_parse_resources_argument_rejects_unknown_values(self):
        with pytest.raises(ValueError, match="Unsupported resources"):
            parse_resources_argument("roadworks,unknown")

    def test_parse_roads_argument_returns_none_for_star(self):
        assert parse_roads_argument("*") is None

    def test_parse_connection_string_extracts_kafka_parameters(self):
        conn_str = "Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=testkey;EntityPath=autobahn"
        result = parse_connection_string(conn_str)
        assert result["bootstrap.servers"] == "namespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "autobahn"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["sasl.password"] == conn_str


class TestFamilyClassification:
    def test_determine_event_family_uses_display_type(self):
        assert determine_event_family("roadworks", "SHORT_TERM_ROADWORKS") == "short_term_roadwork"
        assert determine_event_family("closure", "WEIGHT_LIMIT_35") == "weight_limit_35_restriction"

    def test_determine_event_family_uses_single_family_fallbacks(self):
        assert determine_event_family("warning", None) == "warning"
        assert determine_event_family("parking_lorry", None) == "parking_lorry"


class TestSnapshotBuilding:
    def test_builds_roadwork_snapshot(self):
        raw_item = {
            "identifier": "roadwork-1",
            "display_type": "ROADWORKS",
            "title": "A1 bridge works",
            "subtitle": "AS Test - AS Demo",
            "description": ["Lane closed"],
            "future": False,
            "isBlocked": "false",
            "icon": "123",
            "startLcPosition": "1000",
            "startTimestamp": "2026-04-06T08:00:00Z",
            "extent": "51.1,7.1,51.2,7.2",
            "point": "51.1,7.1",
            "coordinate": {"lat": 51.1, "long": 7.1},
            "impact": {"symbols": ["CLOSED", "ARROW_UP"]},
            "geometry": {"type": "LineString", "coordinates": [[7.1, 51.1], [7.2, 51.2]]},
        }

        family, snapshot = build_family_snapshot("A1", "roadworks", raw_item)

        assert family == "roadwork"
        assert snapshot["identifier"] == "roadwork-1"
        assert snapshot["road_ids"] == ["A1"]
        assert snapshot["coordinate_lat"] == 51.1
        assert snapshot["coordinate_lon"] == 7.1
        assert snapshot["start_lc_position"] == 1000
        assert snapshot["impact_symbols"] == ["CLOSED", "ARROW_UP"]
        assert json.loads(snapshot["geometry_json"])["type"] == "LineString"

    def test_builds_warning_snapshot(self):
        raw_item = {
            "identifier": "warning-1",
            "display_type": "WARNING",
            "title": "A1 queue",
            "description": ["Travel time loss: 7 minutes"],
            "future": False,
            "isBlocked": "false",
            "coordinate": {"lat": 53.02, "long": 8.82},
            "delayTimeValue": "7",
            "averageSpeed": "20",
            "abnormalTrafficType": "QUEUING_TRAFFIC",
            "source": "inrix",
        }

        family, snapshot = build_family_snapshot("A1", "warning", raw_item)

        assert family == "warning"
        assert snapshot["delay_minutes"] == 7
        assert snapshot["average_speed_kmh"] == 20
        assert snapshot["abnormal_traffic_type"] == "QUEUING_TRAFFIC"
        assert snapshot["source_name"] == "inrix"

    def test_builds_parking_snapshot_from_geojson_coordinate(self):
        raw_item = {
            "identifier": "parking-1",
            "display_type": "PARKING",
            "title": "A1 | Demo",
            "description": [
                "PKW Stellplätze: 21",
                "LKW Stellplätze: 48",
            ],
            "coordinate": {"type": "Point", "coordinates": [9.533484, 53.300202]},
            "lorryParkingFeatureIcons": [
                {"description": "Tankstelle"},
                {"description": "Toilette vorhanden"},
            ],
        }

        family, snapshot = build_family_snapshot("A1", "parking_lorry", raw_item)

        assert family == "parking_lorry"
        assert snapshot["coordinate_lat"] == 53.300202
        assert snapshot["coordinate_lon"] == 9.533484
        assert snapshot["amenity_descriptions"] == ["Tankstelle", "Toilette vorhanden"]
        assert snapshot["car_space_count"] == 21
        assert snapshot["lorry_space_count"] == 48

    def test_builds_charging_snapshot(self):
        raw_item = {
            "identifier": "charging-1",
            "display_type": "STRONG_ELECTRIC_CHARGING_STATION",
            "title": "A1 charging",
            "description": [
                "Autohof Demo",
                "Demoweg 1, 12345 Musterstadt",
                "Ladepunkt 1:",
                "150 kW",
                "CCS",
                "Ladepunkt 2:",
                "50 kW",
                "Typ2, CCS",
            ],
            "coordinate": {"lat": 50.1, "long": 8.6},
        }

        family, snapshot = build_family_snapshot("A1", "electric_charging_station", raw_item)

        assert family == "strong_electric_charging_station"
        assert snapshot["address_line"] == "Demoweg 1, 12345 Musterstadt"
        assert snapshot["charging_point_count"] == 2
        points = json.loads(snapshot["charging_points_json"])
        assert points[0]["power_kw"] == 150.0
        assert points[1]["connectors"] == ["Typ2", "CCS"]

    def test_builds_webcam_snapshot(self):
        raw_item = {
            "identifier": "webcam-1",
            "display_type": "WEBCAM",
            "title": "A1 webcam",
            "coordinate": {"lat": 50.0, "long": 8.0},
            "operator": "Autobahn GmbH",
            "imageurl": "https://example.test/image.jpg",
            "linkurl": "https://example.test/live",
        }

        family, snapshot = build_family_snapshot("A1", "webcam", raw_item)

        assert family == "webcam"
        assert snapshot["operator_name"] == "Autobahn GmbH"
        assert snapshot["image_url"] == "https://example.test/image.jpg"
        assert snapshot["stream_url"] == "https://example.test/live"


class TestHelpers:
    def test_parse_charging_points_extracts_address_and_connectors(self):
        address_line, charging_point_count, charging_points_json = parse_charging_points(
            [
                "Autohof Demo",
                "Demoweg 1, 12345 Musterstadt",
                "Ladepunkt 1:",
                "150 kW",
                "CCS",
            ]
        )

        assert address_line == "Demoweg 1, 12345 Musterstadt"
        assert charging_point_count == 1
        assert json.loads(charging_points_json) == [{"index": 1, "connectors": ["CCS"], "power_kw": 150.0}]

    def test_merge_snapshots_combines_road_ids(self):
        merged = merge_snapshots(
            {
                "identifier": "item-1",
                "road_ids": ["A1"],
                "title": "Roadwork",
                "display_type": "ROADWORKS",
            },
            {
                "identifier": "item-1",
                "road_ids": ["A3"],
                "title": "Roadwork",
                "display_type": "ROADWORKS",
            },
        )

        assert merged["road_ids"] == ["A1", "A3"]


class TestDiffing:
    def test_diff_items_identifies_appeared_updated_and_resolved(self):
        previous = {
            "item-1": {"identifier": "item-1", "title": "Old"},
            "item-2": {"identifier": "item-2", "title": "Removed"},
        }
        current = {
            "item-1": {"identifier": "item-1", "title": "New"},
            "item-3": {"identifier": "item-3", "title": "Appeared"},
        }

        changes = diff_items(previous, current)

        assert [item["identifier"] for item in changes["appeared"]] == ["item-3"]
        assert [item["identifier"] for item in changes["updated"]] == ["item-1"]
        assert [item["identifier"] for item in changes["resolved"]] == ["item-2"]