from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from poller_core import (  # noqa: E402
    ArcGisFeatureServerPoller,
    DeltaDetector,
    GeoJsonFeatureCollectionPoller,
    JsonFileStateStore,
    OffsetLimitPagination,
    create_retrying_session,
)


class FakeSession(requests.Session):
    def __init__(self, responses: List[requests.Response]) -> None:
        super().__init__()
        self.responses = responses
        self.calls: List[Dict[str, Any]] = []

    def get(self, url: str, **kwargs: Any) -> requests.Response:  # type: ignore[override]
        self.calls.append({"url": url, **kwargs})
        if not self.responses:
            raise AssertionError(f"Unexpected GET {url} {kwargs}")
        response = self.responses.pop(0)
        response.url = url
        return response


def make_response(
    payload: Optional[Dict[str, Any]],
    *,
    status: int = 200,
    headers: Optional[Dict[str, str]] = None,
    gzip_body: bool = False,
) -> requests.Response:
    response = requests.Response()
    response.status_code = status
    response.headers.update(headers or {})
    response.encoding = "utf-8"
    if payload is None:
        response._content = b""
    else:
        raw = json.dumps(payload).encode("utf-8")
        if gzip_body:
            raw = gzip.compress(raw)
            response.headers["Content-Encoding"] = "gzip"
        response._content = raw
    return response


def arcgis_feature(object_id: int, name: str, *, edited: int = 100) -> Dict[str, Any]:
    return {
        "type": "Feature",
        "properties": {"OBJECTID": object_id, "name": name, "last_edited_date": edited},
        "geometry": {"type": "Point", "coordinates": [10.0 + object_id, 50.0]},
    }


def test_arcgis_pages_all_features_and_keys_by_metadata_object_id() -> None:
    session = FakeSession([
        make_response({"objectIdField": "OBJECTID", "maxRecordCount": 2}),
        make_response({"type": "FeatureCollection", "properties": {"exceededTransferLimit": True}, "features": [arcgis_feature(1, "a"), arcgis_feature(2, "b")]}),
        make_response({"type": "FeatureCollection", "properties": {"exceededTransferLimit": False}, "features": [arcgis_feature(3, "c")]}),
    ])
    poller = ArcGisFeatureServerPoller(
        "https://example.test/arcgis/rest/services/Fires/FeatureServer",
        layer_id=0,
        order_by_fields="OBJECTID ASC",
        page_size=10,
        session=session,
    )

    result = poller.fetch()

    assert [feature["id"] for feature in result.features] == ["1", "2", "3"]
    assert result.features[0]["attributes"]["name"] == "a"
    assert result.features[0]["geometry"] == {"type": "Point", "coordinates": [11.0, 50.0]}
    assert result.metadata.page_count == 2
    assert session.calls[1]["params"]["f"] == "geojson"
    assert session.calls[1]["params"]["resultOffset"] == "0"
    assert session.calls[1]["params"]["resultRecordCount"] == "2"
    assert session.calls[2]["params"]["resultOffset"] == "2"
    assert session.calls[2]["params"]["orderByFields"] == "OBJECTID ASC"


def test_arcgis_preserves_zero_object_id() -> None:
    session = FakeSession([
        make_response({"objectIdField": "OBJECTID", "maxRecordCount": 500}),
        make_response({"type": "FeatureCollection", "features": [arcgis_feature(0, "zero")]}, status=200),
    ])
    poller = ArcGisFeatureServerPoller("https://example.test/FeatureServer/0", session=session)

    result = poller.fetch()

    assert result.features[0]["id"] == "0"


def test_arcgis_falls_back_to_json_and_uses_caller_unique_field() -> None:
    session = FakeSession([
        make_response({"objectIdField": "OBJECTID", "maxRecordCount": 500}),
        make_response({"error": {"message": "geojson not supported"}}),
        make_response({
            "features": [{"attributes": {"station_no": "SN-1", "value": 42}, "geometry": {"x": 13.0, "y": 51.0}}],
            "exceededTransferLimit": False,
        }),
    ])
    poller = ArcGisFeatureServerPoller(
        "https://example.test/arcgis/rest/services/wasser/pegelnetz/MapServer/1/query",
        unique_field="station_no",
        session=session,
    )

    result = poller.fetch()

    assert result.features == [{"id": "SN-1", "attributes": {"station_no": "SN-1", "value": 42}, "geometry": {"x": 13.0, "y": 51.0}}]
    assert session.calls[1]["params"]["f"] == "geojson"
    assert session.calls[2]["params"]["f"] == "json"


def test_arcgis_fallback_json_error_raises() -> None:
    session = FakeSession([
        make_response({"objectIdField": "OBJECTID", "maxRecordCount": 500}),
        make_response({"error": {"message": "geojson not supported"}}),
        make_response({"error": {"message": "bad where"}}),
    ])
    poller = ArcGisFeatureServerPoller("https://example.test/FeatureServer/0", session=session)

    with pytest.raises(ValueError, match="bad where"):
        poller.fetch()


def test_geojson_gzip_offset_pagination_and_id_path() -> None:
    session = FakeSession([
        make_response({"type": "FeatureCollection", "features": [geo_feature("n1"), geo_feature("n2")]}, gzip_body=True),
        make_response({"type": "FeatureCollection", "features": [geo_feature("n3")]}, gzip_body=True),
    ])
    poller = GeoJsonFeatureCollectionPoller(
        "https://example.test/feed.geojson",
        params={"status": "active"},
        id_path="properties.guid",
        pagination=OffsetLimitPagination(offset_param="startIndex", limit_param="count", limit=2),
        session=session,
    )

    result = poller.fetch()

    assert [feature["id"] for feature in result.features] == ["n1", "n2", "n3"]
    assert session.calls[0]["params"] == {"status": "active", "startIndex": "0", "count": "2"}
    assert session.calls[1]["params"]["startIndex"] == "2"
    assert result.metadata.page_count == 2


def test_geojson_link_pagination() -> None:
    session = FakeSession([
        make_response(
            {"type": "FeatureCollection", "features": [geo_feature("a")]},
            headers={"Link": '<https://example.test/feed.geojson?page=2>; rel="next"'},
        ),
        make_response({"type": "FeatureCollection", "features": [geo_feature("b")]}),
    ])
    poller = GeoJsonFeatureCollectionPoller("https://example.test/feed.geojson", id_path="properties.guid", session=session)

    result = poller.fetch()

    assert [feature["id"] for feature in result.features] == ["a", "b"]
    assert session.calls[1]["url"] == "https://example.test/feed.geojson?page=2"


def test_geojson_body_pagination_next_url() -> None:
    session = FakeSession([
        make_response({"type": "FeatureCollection", "features": [geo_feature("a")], "pagination": {"next": "https://example.test/feed.geojson?page=2"}}),
        make_response({"type": "FeatureCollection", "features": [geo_feature("b")]}),
    ])
    poller = GeoJsonFeatureCollectionPoller("https://example.test/feed.geojson", id_path="properties.guid", session=session)

    result = poller.fetch()

    assert [feature["id"] for feature in result.features] == ["a", "b"]
    assert session.calls[1]["url"] == "https://example.test/feed.geojson?page=2"


def test_geojson_terminal_status_after_accumulated_pages() -> None:
    response = make_response(None, status=400)
    response.url = "https://example.test/wfs?startIndex=2"
    session = FakeSession([
        make_response({"type": "FeatureCollection", "features": [geo_feature("a"), geo_feature("b")]}),
        response,
    ])
    poller = GeoJsonFeatureCollectionPoller(
        "https://example.test/wfs",
        id_path="properties.guid",
        pagination=OffsetLimitPagination(offset_param="startIndex", limit_param="count", limit=2),
        terminal_status_codes=(400,),
        session=session,
    )

    result = poller.fetch()

    assert [feature["id"] for feature in result.features] == ["a", "b"]
    assert result.metadata.page_count == 1


def test_geojson_conditional_get_304_uses_state_store(tmp_path: Path) -> None:
    store = JsonFileStateStore(tmp_path / "state.json")
    store.save_http_metadata(etag='"abc"', last_modified="Wed, 01 Jan 2025 00:00:00 GMT")
    session = FakeSession([make_response(None, status=304)])
    poller = GeoJsonFeatureCollectionPoller("https://example.test/feed.geojson", state_store=store, session=session)

    result = poller.fetch()

    assert result.features == []
    assert result.metadata.not_modified is True
    assert session.calls[0]["headers"] == {
        "If-None-Match": '"abc"',
        "If-Modified-Since": "Wed, 01 Jan 2025 00:00:00 GMT",
    }


def test_delta_detects_new_unchanged_and_changed_features() -> None:
    detector = DeltaDetector(timestamp_field="last_edited_date")
    state: Dict[str, Any] = {}
    first = {"id": "1", "attributes": {"last_edited_date": 100, "name": "a"}, "geometry": None}
    same = {"id": "1", "attributes": {"last_edited_date": 100, "name": "changed but timestamp wins"}, "geometry": None}
    changed = {"id": "1", "attributes": {"last_edited_date": 101, "name": "a"}, "geometry": None}
    hashed = {"id": "2", "attributes": {"name": "hash-me"}, "geometry": {"type": "Point", "coordinates": [1, 2]}}
    hashed_changed = {"id": "2", "attributes": {"name": "hash-me-too"}, "geometry": {"type": "Point", "coordinates": [1, 2]}}

    assert detector.changed_features([first], state) == [first]
    assert detector.changed_features([same], state) == []
    assert detector.changed_features([changed], state) == [changed]
    assert detector.changed_features([hashed], state) == [hashed]
    assert detector.changed_features([hashed_changed], state) == [hashed_changed]


def test_retrying_session_configures_timeout_and_backoff() -> None:
    session = create_retrying_session(user_agent="poller-core-test/1", timeout=12.5, total_retries=4, backoff_factor=0.25)
    adapter = session.get_adapter("https://")
    retries = adapter.max_retries
    assert session.headers["User-Agent"] == "poller-core-test/1"
    assert getattr(session, "default_timeout") == 12.5
    assert retries.total == 4
    assert retries.backoff_factor == 0.25
    assert 429 in retries.status_forcelist


def geo_feature(identifier: str) -> Dict[str, Any]:
    return {
        "type": "Feature",
        "id": f"feature-{identifier}",
        "properties": {"guid": identifier, "value": identifier.upper()},
        "geometry": {"type": "Point", "coordinates": [1.0, 2.0]},
    }


@pytest.mark.live
def test_live_arcgis_nifc_smoke() -> None:
    poller = ArcGisFeatureServerPoller(
        "https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/USA_Wildfires_v1/FeatureServer",
        layer_id=0,
        unique_field="IrwinID",
        order_by_fields="OBJECTID ASC",
        page_size=200,
        headers={"User-Agent": "real-time-sources-poller-core-smoke/0.1"},
    )
    try:
        result = poller.fetch()
    except requests.RequestException as exc:
        pytest.skip(f"ArcGIS live endpoint unavailable: {exc}")
    keyed = [feature for feature in result.features if feature["id"]]
    print(f"LIVE_ARCGIS_NIFC_FEATURE_COUNT={len(keyed)}")
    assert keyed


@pytest.mark.live
def test_live_geojson_usgs_earthquakes_smoke() -> None:
    poller = GeoJsonFeatureCollectionPoller(
        "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson",
        id_path="id",
        headers={"User-Agent": "real-time-sources-poller-core-smoke/0.1"},
    )
    try:
        result = poller.fetch()
    except requests.RequestException as exc:
        pytest.skip(f"GeoJSON live endpoint unavailable: {exc}")
    print(f"LIVE_GEOJSON_USGS_EARTHQUAKES_FEATURE_COUNT={len(result.features)}")
    assert result.features
    assert all(feature["id"] for feature in result.features)
