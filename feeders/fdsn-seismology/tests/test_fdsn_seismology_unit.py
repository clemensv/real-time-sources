from __future__ import annotations

import json

import fdsn_seismology_core
from fdsn_seismology_core.fdsn_client import EarthquakeRecord, deduplicate_events, load_mock_events, parse_fdsn_text
from fdsn_seismology_core.nodes import DEFAULT_SOURCES_FILE, NODE_CATALOG, get_active_nodes, load_node_catalog, parse_node_filter
import pytest


SAMPLE_TEXT = """#EventID|Time|Latitude|Longitude|Depth/km|Author|Catalog|Contributor|ContributorID|MagType|Magnitude|MagAuthor|EventLocationName|EventType
20260604_0000095|2026-06-04T06:07:17.0Z|-21.4600|-71.8300|10.0|CSN|EMSC-RTS|CSN|2005203|m|3.3|CSN|OFF COAST OF ANTOFAGASTA, CHILE|
gfz2026kvsq|2026-06-04T04:37:28.82|-0.866|133.414|10.0|||GFZ|gfz2026kvsq|mb|4.79||West Papua Region, Indonesia|earthquake
46128882|2026-06-04T05:50:09.890000|43.1233|12.7825|10.3|SURVEY-INGV||||ML|1.5|--|1 km NW Nocera Umbra (PG)|earthquake
"""


class TestParseFdsnText:
    def test_parses_pipe_delimited_rows(self):
        records = parse_fdsn_text(SAMPLE_TEXT, node_id="emsc", node_url="https://example.test/fdsnws/event/1/")

        assert len(records) == 3
        assert records[0].event_id == "20260604_0000095"
        assert records[0].latitude == -21.46
        assert records[0].longitude == -71.83
        assert records[0].magnitude == 3.3

    def test_maps_optional_empty_fields_to_none(self):
        records = parse_fdsn_text(SAMPLE_TEXT, node_id="gfz", node_url="https://example.test/fdsnws/event/1/")
        gfz_record = next(record for record in records if record.event_id == "gfz2026kvsq")
        ingv_record = next(record for record in records if record.event_id == "46128882")

        assert gfz_record.author is None
        assert gfz_record.catalog is None
        assert gfz_record.magnitude_author is None
        assert ingv_record.contributor == "GFZ" or ingv_record.contributor == "INGV"
        assert ingv_record.contributor_id is None
        assert ingv_record.magnitude_author is None

    def test_supports_missing_event_type_column(self):
        payload = """#EventID|Time|Latitude|Longitude|Depth/km|Author|Catalog|Contributor|ContributorID|MagType|Magnitude|MagAuthor|EventLocationName
20260604_0000095|2026-06-04T06:07:18.0Z|-21.4000|-71.6800|10.0|CSN|EMSC-RTS|CSN|2005203|ml|3.4|CSN|OFF COAST OF ANTOFAGASTA, CHILE
"""
        records = parse_fdsn_text(payload, node_id="emsc", node_url="https://seismicportal.eu/fdsnws/event/1/")

        assert len(records) == 1
        assert records[0].event_type is None


class TestMockEvents:
    def test_load_mock_events_is_deterministic_and_nonempty(self):
        active = get_active_nodes(None, None)
        first = load_mock_events(active)
        second = load_mock_events(active)

        assert len(first) >= 1
        assert [r.event_id for r in first] == [r.event_id for r in second]
        assert all(r.contributor == "MOCK" for r in first)
        # Earthquakes are attributed to the first active node so keys/subjects stay stable.
        first_node_url = str(next(iter(active.values()))["base_url"])
        assert all(r.node_url == first_node_url for r in first)
        assert all(r.magnitude is not None for r in first)

    def test_load_mock_events_empty_node_selection(self):
        assert load_mock_events({}) == []


class TestNodeCatalog:
    def test_catalog_contains_expected_nodes(self):
        assert {"emsc", "gfz", "ingv", "ethz", "resif", "ipgp", "niep", "usgs"}.issubset(NODE_CATALOG)
        assert "custom" in NODE_CATALOG
        assert NODE_CATALOG["gfz"]["country"] == "DE"
        assert NODE_CATALOG["usgs"]["base_url"] == "https://earthquake.usgs.gov/fdsnws/event/1/"
        assert NODE_CATALOG["emsc"]["coverage"] == "Global aggregator"

    def test_default_active_nodes_skip_disabled_template(self):
        active = get_active_nodes(None, None)

        assert set(active) == {"emsc", "gfz", "ingv", "ethz", "resif", "ipgp", "niep", "usgs"}
        assert "custom" not in active

    def test_include_filter_can_force_include_disabled_node(self):
        active = get_active_nodes(["custom"], None)

        assert list(active) == ["custom"]
        assert active["custom"]["base_url"] == "REPLACE_WITH_FDSN_BASE_URL"

    def test_include_exclude_filters(self):
        active = get_active_nodes(["emsc", "gfz", "niep"], ["gfz"])
        assert list(active) == ["emsc", "niep"]

    def test_usgs_node_filter(self):
        active = get_active_nodes(parse_node_filter("usgs"), None)

        assert list(active) == ["usgs"]
        assert active["usgs"]["country"] == "US"

    def test_exclude_filter_subtracts_from_default_enabled_nodes(self):
        active = get_active_nodes(None, parse_node_filter("emsc,gfz"))

        assert "emsc" not in active
        assert "gfz" not in active
        assert "usgs" in active

    def test_unknown_node_filter_raises_value_error(self):
        with pytest.raises(ValueError):
            get_active_nodes(["does-not-exist"], None)

    def test_sources_file_override_honors_enabled_and_include(self, tmp_path):
        catalog = tmp_path / "custom.sources.json"
        catalog.write_text(
            json.dumps(
                {
                    "sources": [
                        {"name": "enabled", "enabled": True, "node_id": "enabled", "base_url": "https://example.invalid/fdsnws/event/1/", "coverage": "Enabled node", "country": "ZZ"},
                        {"name": "disabled", "enabled": False, "node_id": "disabled", "base_url": "https://example.invalid/private/fdsnws/event/1/", "coverage": "Disabled node", "country": "ZZ"},
                    ]
                }
            ),
            encoding="utf-8",
        )

        assert list(get_active_nodes(None, None, sources_file=str(catalog))) == ["enabled"]
        assert list(get_active_nodes(["disabled"], None, sources_file=str(catalog))) == ["disabled"]

    def test_env_interpolation_in_sources_file(self, tmp_path, monkeypatch):
        monkeypatch.setenv("PRIVATE_FDSN_BASE_URL", "https://example.invalid/env/fdsnws/event/1/")
        catalog = tmp_path / "env.sources.json"
        catalog.write_text(
            json.dumps({"sources": [{"name": "env", "node_id": "env", "base_url": "${PRIVATE_FDSN_BASE_URL}", "coverage": "Interpolated", "country": "ZZ"}]}),
            encoding="utf-8",
        )

        active = get_active_nodes(["env"], None, sources_file=str(catalog))

        assert active["env"]["base_url"] == "https://example.invalid/env/fdsnws/event/1/"

    def test_packaged_catalog_path_resolves(self):
        assert fdsn_seismology_core.__file__ is not None
        assert DEFAULT_SOURCES_FILE.endswith("fdsn-seismology.sources.json")
        assert load_node_catalog(DEFAULT_SOURCES_FILE)["usgs"]["country"] == "US"


class TestDeduplication:
    def test_prefers_richer_duplicate_record(self):
        sparse = EarthquakeRecord(
            event_id="gfz2026kvsq",
            time="2026-06-04T04:37:28.820000Z",
            latitude=-0.866,
            longitude=133.414,
            depth_km=10.0,
            author=None,
            catalog=None,
            contributor="GFZ",
            contributor_id="gfz2026kvsq",
            magnitude_type="mb",
            magnitude=4.79,
            magnitude_author=None,
            event_location_name="West Papua Region, Indonesia",
            event_type=None,
            node_url="https://seismicportal.eu/fdsnws/event/1/",
        )
        rich = EarthquakeRecord(
            event_id="gfz2026kvsq",
            time="2026-06-04T04:37:28.820000Z",
            latitude=-0.866,
            longitude=133.414,
            depth_km=10.0,
            author=None,
            catalog=None,
            contributor="GFZ",
            contributor_id="gfz2026kvsq",
            magnitude_type="mb",
            magnitude=4.79,
            magnitude_author=None,
            event_location_name="West Papua Region, Indonesia",
            event_type="earthquake",
            node_url="https://geofon.gfz-potsdam.de/fdsnws/event/1/",
        )

        deduped = deduplicate_events([sparse, rich])

        assert len(deduped) == 1
        assert deduped[0].event_type == "earthquake"
        assert deduped[0].node_url == "https://geofon.gfz-potsdam.de/fdsnws/event/1/"


class TestFormatDatetime:
    def test_emits_no_timezone_designator(self):
        """FDSN-WS time params are implicit-UTC; strict nodes (INGV/ISC) 400 on a trailing 'Z'."""
        from datetime import datetime, timezone

        from fdsn_seismology_core.fdsn_client import format_datetime

        out = format_datetime(datetime(2026, 6, 22, 12, 0, 0, 500000, tzinfo=timezone.utc))
        assert out == "2026-06-22T12:00:00"
        assert "Z" not in out and "+" not in out

    def test_converts_offset_input_to_utc(self):
        from datetime import datetime, timedelta, timezone

        from fdsn_seismology_core.fdsn_client import format_datetime

        plus2 = timezone(timedelta(hours=2))
        assert format_datetime(datetime(2026, 6, 22, 14, 0, 0, tzinfo=plus2)) == "2026-06-22T12:00:00"
