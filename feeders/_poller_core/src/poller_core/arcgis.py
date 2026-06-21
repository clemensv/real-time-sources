"""ArcGIS FeatureServer layer poller."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional
from urllib.parse import urlparse

import requests

from poller_core.http import create_retrying_session, response_json
from poller_core.models import NormalizedFeature, PollMetadata, PollResult

DEFAULT_PAGE_SIZE = 2000


class ArcGisFeatureServerPoller:
    """Poll an ArcGIS FeatureServer or MapServer layer query endpoint.

    Args:
        base_url: Service URL ending at FeatureServer, MapServer, a layer id, or
            a layer query endpoint. All forms used by existing bespoke feeders
            are normalized internally.
        layer_id: Layer id to query when base_url is the service root. Ignored
            when base_url already ends with a numeric layer id or /query.
        where: ArcGIS where clause, defaulting to all features.
        out_fields: ArcGIS outFields value, defaulting to all fields.
        out_sr: Optional output spatial reference, for example "4326".
        unique_field: Optional stable id field. When omitted, layer metadata is
            queried and objectIdField is used.
        order_by_fields: Optional stable orderByFields value for paging.
        page_size: resultRecordCount per request. Metadata maxRecordCount lowers
            this value when available.
        token: Optional ArcGIS token sent as a query parameter.
        headers: Optional request headers, such as Authorization or User-Agent.
        session: Optional requests session. A retrying session is created when
            omitted.
    """

    def __init__(
        self,
        base_url: str,
        layer_id: int = 0,
        *,
        where: str = "1=1",
        out_fields: str = "*",
        out_sr: Optional[str] = None,
        unique_field: Optional[str] = None,
        order_by_fields: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
        token: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.layer_url, self.query_url = _layer_and_query_urls(base_url, layer_id)
        self.where = where
        self.out_fields = out_fields
        self.out_sr = out_sr
        self.unique_field = unique_field
        self.order_by_fields = order_by_fields
        self.page_size = page_size
        self.token = token
        self.session = session or create_retrying_session(headers=headers)
        if headers and session is not None:
            self.session.headers.update(dict(headers))
        self._object_id_field: Optional[str] = None
        self._max_record_count: Optional[int] = None

    def fetch(self) -> PollResult:
        """Fetch all pages and return normalized features keyed by stable id."""
        metadata = self.layer_metadata()
        object_id_field = self.unique_field or _string_or_none(metadata.get("objectIdField")) or "OBJECTID"
        max_record_count = _int_or_none(metadata.get("maxRecordCount")) or self.page_size
        page_size = max(1, min(self.page_size, max_record_count))
        all_features: List[NormalizedFeature] = []
        offset = 0
        page_count = 0
        status_code = 0
        while True:
            data, status_code = self._query_page(offset, page_size, preferred_format="geojson")
            page_count += 1
            features = data.get("features", [])
            if not isinstance(features, list):
                features = []
            all_features.extend(
                self._normalize_feature(feature, object_id_field) for feature in features if isinstance(feature, dict)
            )
            exceeded = _exceeded_transfer_limit(data)
            if not features:
                break
            if not exceeded and len(features) < page_size:
                break
            offset += len(features)
        return PollResult(
            features=all_features,
            metadata=PollMetadata(
                status_code=status_code,
                page_count=page_count,
                source_url=self.query_url,
            ),
        )

    def layer_metadata(self) -> Dict[str, Any]:
        """Return and cache ArcGIS layer metadata discovered via ?f=json."""
        if self._object_id_field is not None:
            return {"objectIdField": self._object_id_field, "maxRecordCount": self._max_record_count}
        params: Dict[str, Any] = {"f": "json"}
        if self.token:
            params["token"] = self.token
        response = self.session.get(self.layer_url, params=params)
        response.raise_for_status()
        data = response_json(response)
        self._object_id_field = _string_or_none(data.get("objectIdField")) or "OBJECTID"
        self._max_record_count = _int_or_none(data.get("maxRecordCount"))
        return data

    def _query_page(self, offset: int, page_size: int, *, preferred_format: str) -> tuple[Dict[str, Any], int]:
        params = self._query_params(offset, page_size, preferred_format)
        try:
            response = self.session.get(self.query_url, params=params)
            response.raise_for_status()
            data = response_json(response)
            if isinstance(data.get("error"), dict):
                raise ValueError(str(data["error"]))
            return data, response.status_code
        except (requests.RequestException, ValueError):
            if preferred_format == "json":
                raise
        params = self._query_params(offset, page_size, "json")
        response = self.session.get(self.query_url, params=params)
        response.raise_for_status()
        data = response_json(response)
        if isinstance(data.get("error"), dict):
            raise ValueError(str(data["error"]))
        return data, response.status_code

    def _query_params(self, offset: int, page_size: int, output_format: str) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "f": output_format,
            "where": self.where,
            "outFields": self.out_fields,
            "resultRecordCount": str(page_size),
            "resultOffset": str(offset),
        }
        if self.out_sr:
            params["outSR"] = self.out_sr
        if self.order_by_fields:
            params["orderByFields"] = self.order_by_fields
        if self.token:
            params["token"] = self.token
        return params

    def _normalize_feature(self, feature: Dict[str, Any], object_id_field: str) -> NormalizedFeature:
        attributes = feature.get("attributes")
        if not isinstance(attributes, dict):
            props = feature.get("properties")
            attributes = props if isinstance(props, dict) else {}
        geometry = feature.get("geometry") if isinstance(feature.get("geometry"), dict) else None
        raw_id = _first_present(
            attributes.get(object_id_field),
            feature.get("id"),
            attributes.get("OBJECTID"),
            attributes.get("FID"),
        )
        if raw_id is None:
            raw_id = stable_repr({"attributes": attributes, "geometry": geometry})
        return {"id": str(raw_id), "attributes": dict(attributes), "geometry": geometry}


def _layer_and_query_urls(base_url: str, layer_id: int) -> tuple[str, str]:
    trimmed = base_url.rstrip("/")
    if trimmed.lower().endswith("/query"):
        layer_url = trimmed.rsplit("/", 1)[0]
        return layer_url, trimmed
    last_segment = urlparse(trimmed).path.rstrip("/").rsplit("/", 1)[-1]
    if last_segment.isdigit():
        return trimmed, f"{trimmed}/query"
    layer_url = f"{trimmed}/{layer_id}"
    return layer_url, f"{layer_url}/query"


def _exceeded_transfer_limit(data: Dict[str, Any]) -> bool:
    props = data.get("properties")
    if isinstance(props, dict) and bool(props.get("exceededTransferLimit")):
        return True
    return bool(data.get("exceededTransferLimit"))


def _string_or_none(value: Any) -> Optional[str]:
    return value if isinstance(value, str) and value else None


def _int_or_none(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def stable_repr(value: Any) -> str:
    """Return a deterministic fallback id for malformed upstream features."""
    import json
    import hashlib

    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _first_present(*values: Any) -> Any:
    for value in values:
        if value is not None and value != "":
            return value
    return None
