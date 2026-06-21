"""GeoJSON FeatureCollection poller."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional
from urllib.parse import urljoin

import requests

from poller_core.http import create_retrying_session, response_json
from poller_core.models import NormalizedFeature, PollMetadata, PollResult
from poller_core.state import JsonFileStateStore


@dataclass(frozen=True)
class OffsetLimitPagination:
    """Offset/limit pagination settings for GeoJSON APIs.

    Args:
        offset_param: Query parameter carrying the current offset.
        limit_param: Query parameter carrying the page size.
        limit: Page size requested from the upstream.
        start_offset: Initial offset value. Existing feeders use both 0-based
            offset and WFS-style startIndex conventions; callers configure the
            exact parameter names here.
    """

    offset_param: str = "offset"
    limit_param: str = "limit"
    limit: int = 500
    start_offset: int = 0


class GeoJsonFeatureCollectionPoller:
    """Poll a GeoJSON FeatureCollection endpoint.

    Args:
        url: Endpoint URL returning a GeoJSON FeatureCollection.
        params: Optional query parameters sent with the first request.
        id_path: Dotted path used as the stable feature id. Defaults to
            feature.id. Examples: "properties.guid", "properties.station.id".
        fallback_property: Optional properties field used when id_path is empty.
        pagination: Optional offset/limit pagination settings.
        follow_link_next: Whether to follow RFC 5988 Link headers with
            rel="next". Enabled by default.
        body_next_path: Optional dotted response-body path carrying a next-page
            URL, defaulting to NOAA NWS-style "pagination.next".
        terminal_status_codes: Optional statuses that end pagination after at
            least one page has been fetched, for WFS endpoints that return a
            terminal 400 when startIndex exceeds the result set.
        use_conditional_get: Whether to send saved ETag/Last-Modified values as
            If-None-Match/If-Modified-Since headers.
        state_store: Optional JSON state store for conditional-GET metadata.
        headers: Optional request headers, such as Authorization or User-Agent.
        session: Optional requests session. A retrying session is created when
            omitted.
    """

    def __init__(
        self,
        url: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        id_path: str = "id",
        fallback_property: Optional[str] = None,
        pagination: Optional[OffsetLimitPagination] = None,
        follow_link_next: bool = True,
        body_next_path: Optional[str] = "pagination.next",
        terminal_status_codes: tuple[int, ...] = (),
        use_conditional_get: bool = True,
        state_store: Optional[JsonFileStateStore] = None,
        headers: Optional[Mapping[str, str]] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.url = url
        self.params = dict(params or {})
        self.id_path = id_path
        self.fallback_property = fallback_property
        self.pagination = pagination
        self.follow_link_next = follow_link_next
        self.body_next_path = body_next_path
        self.terminal_status_codes = terminal_status_codes
        self.use_conditional_get = use_conditional_get
        self.state_store = state_store
        self.session = session or create_retrying_session(headers=headers)
        if headers and session is not None:
            self.session.headers.update(dict(headers))
        self._etag: Optional[str] = None
        self._last_modified: Optional[str] = None

    def fetch(self) -> PollResult:
        """Fetch one or more pages and return normalized features.

        Returns an empty feature list with metadata.not_modified=True when the
        first request receives HTTP 304.
        """
        features: List[NormalizedFeature] = []
        page_count = 0
        status_code = 0
        next_url: Optional[str] = self.url
        offset = self.pagination.start_offset if self.pagination else 0
        first_page = True
        latest_etag: Optional[str] = None
        latest_last_modified: Optional[str] = None
        while next_url:
            request_params: Optional[Dict[str, Any]] = dict(self.params) if first_page or next_url == self.url else None
            if self.pagination and next_url == self.url:
                assert request_params is not None
                request_params[self.pagination.offset_param] = str(offset)
                request_params[self.pagination.limit_param] = str(self.pagination.limit)
            headers = self._conditional_headers() if first_page else {}
            response = self.session.get(next_url, params=request_params, headers=headers or None)
            status_code = response.status_code
            if page_count > 0 and status_code in self.terminal_status_codes:
                break
            if status_code == 304:
                metadata = PollMetadata(
                    status_code=status_code,
                    not_modified=True,
                    etag=self._etag,
                    last_modified=self._last_modified,
                    page_count=page_count + 1,
                    source_url=self.url,
                )
                return PollResult(features=[], metadata=metadata)
            response.raise_for_status()
            latest_etag = response.headers.get("ETag") or latest_etag
            latest_last_modified = response.headers.get("Last-Modified") or latest_last_modified
            data = response_json(response)
            raw_features = data.get("features", [])
            if not isinstance(raw_features, list):
                raw_features = []
            features.extend(self._normalize_feature(feature) for feature in raw_features if isinstance(feature, dict))
            page_count += 1
            link_next = _next_link(response.headers.get("Link"), response.url or next_url) if self.follow_link_next else None
            body_next = _get_path(data, self.body_next_path) if self.body_next_path else None
            if link_next:
                next_url = link_next
                first_page = False
                continue
            if isinstance(body_next, str) and body_next:
                next_url = body_next
                first_page = False
                continue
            if self.pagination and len(raw_features) >= self.pagination.limit:
                offset += len(raw_features)
                next_url = self.url
                first_page = False
                continue
            break
        self._remember_http_metadata(latest_etag, latest_last_modified)
        return PollResult(
            features=features,
            metadata=PollMetadata(
                status_code=status_code,
                etag=self._etag,
                last_modified=self._last_modified,
                page_count=page_count,
                source_url=self.url,
            ),
        )

    def _conditional_headers(self) -> Dict[str, str]:
        if not self.use_conditional_get:
            return {}
        if self.state_store:
            headers = self.state_store.conditional_headers()
            self._etag = headers.get("If-None-Match") or self._etag
            self._last_modified = headers.get("If-Modified-Since") or self._last_modified
            return headers
        headers: Dict[str, str] = {}
        if self._etag:
            headers["If-None-Match"] = self._etag
        if self._last_modified:
            headers["If-Modified-Since"] = self._last_modified
        return headers

    def _remember_http_metadata(self, etag: Optional[str], last_modified: Optional[str]) -> None:
        if etag:
            self._etag = etag
        if last_modified:
            self._last_modified = last_modified
        if self.state_store and (etag or last_modified):
            self.state_store.save_http_metadata(etag=etag, last_modified=last_modified)

    def _normalize_feature(self, feature: Dict[str, Any]) -> NormalizedFeature:
        props = feature.get("properties")
        attributes: Dict[str, Any] = dict(props) if isinstance(props, dict) else {}
        raw_id = _get_path(feature, self.id_path)
        if raw_id in (None, "") and self.fallback_property:
            raw_id = attributes.get(self.fallback_property)
        if raw_id in (None, ""):
            raise ValueError(f"Feature from {self.url} has no id at {self.id_path!r}")
        geometry = feature.get("geometry") if isinstance(feature.get("geometry"), dict) else None
        return {"id": str(raw_id), "attributes": attributes, "geometry": geometry}


def _get_path(mapping: Dict[str, Any], path: str) -> Any:
    current: Any = mapping
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def _next_link(link_header: Optional[str], base_url: str) -> Optional[str]:
    if not link_header:
        return None
    for entry in link_header.split(","):
        sections = [section.strip() for section in entry.split(";")]
        if not sections or not sections[0].startswith("<") or not sections[0].endswith(">"):
            continue
        rels = [section for section in sections[1:] if section.lower().replace(" ", "") == 'rel="next"']
        if rels:
            return urljoin(base_url, sections[0][1:-1])
    return None
