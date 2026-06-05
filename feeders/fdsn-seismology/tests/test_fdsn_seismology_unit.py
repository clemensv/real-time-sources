from __future__ import annotations

from fdsn_seismology_core.fdsn_client import EarthquakeRecord, deduplicate_events, parse_fdsn_text
from fdsn_seismology_core.nodes import NODE_CATALOG, get_active_nodes


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


class TestNodeCatalog:
    def test_catalog_contains_expected_nodes(self):
        assert set(NODE_CATALOG) == {"emsc", "gfz", "ingv", "ethz", "resif", "ipgp", "niep"}
        assert NODE_CATALOG["gfz"]["country"] == "DE"
        assert NODE_CATALOG["emsc"]["coverage"] == "Global aggregator"

    def test_include_exclude_filters(self):
        active = get_active_nodes(["emsc", "gfz", "niep"], ["gfz"])
        assert list(active) == ["emsc", "niep"]


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
