"""HTTP clients for DMI's three Open Data observation APIs.

All three APIs share the same OGC Features-style pagination contract under
``https://dmigw.govcloud.dk`` and require their own ``X-Gravitee-Api-Key``
header. Each client is transport-agnostic: it speaks only HTTP+JSON and
returns upstream feature dictionaries as-is so that the Kafka and MQTT
feeders can map them onto their generated data classes without repeating
HTTP error handling or pagination logic.

Reference:
  * metObs:    https://opendatadocs.dmi.govcloud.dk/APIs/Meteorological_Observation_Data
  * oceanObs:  https://opendatadocs.dmi.govcloud.dk/APIs/Oceanographic_Observation_Data
  * lightning: https://opendatadocs.dmi.govcloud.dk/APIs/Lightning_Data
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Iterable, Iterator, List, Optional

import requests


METOBS_FEED_ROOT = "https://dmigw.govcloud.dk/v2/metObs"
OCEANOBS_FEED_ROOT = "https://dmigw.govcloud.dk/v2/oceanObs"
LIGHTNING_FEED_ROOT = "https://dmigw.govcloud.dk/v2/lightningdata"

# Rate-limit is 500 requests / 5 seconds per key; per-page limit is 300_000 but
# we cap at 10_000 to keep individual responses small enough to stream in memory.
_DEFAULT_PAGE_LIMIT = 1000

logger = logging.getLogger(__name__)

# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-dmi/1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)


class _DmiBaseAPI:
    """Common request helpers for every DMI Open Data v2 collection API."""

    feed_root: str = ""

    def __init__(
        self,
        api_key: str,
        session: Optional[requests.Session] = None,
        request_timeout: float = 30.0,
    ) -> None:
        if not api_key:
            raise ValueError(
                f"{self.__class__.__name__} requires an API key (X-Gravitee-Api-Key)."
            )
        self._api_key = api_key
        self._session = session or requests.Session()
        self._session.headers["User-Agent"] = USER_AGENT
        self._request_timeout = request_timeout

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        url = f"{self.feed_root}{path}"
        headers = {"X-Gravitee-Api-Key": self._api_key, "Accept": "application/json"}
        try:
            response = self._session.get(
                url, headers=headers, params=params, timeout=self._request_timeout
            )
        except requests.RequestException as exc:
            logger.warning("DMI request to %s failed: %s", url, exc)
            return None
        if response.status_code != 200:
            logger.warning(
                "DMI request to %s returned status %s", url, response.status_code
            )
            return None
        return response.json()

    def _iter_collection(
        self,
        collection: str,
        params: Optional[Dict[str, Any]] = None,
        page_limit: int = _DEFAULT_PAGE_LIMIT,
    ) -> Iterator[Dict[str, Any]]:
        """Yield every feature from an OGC-Features-style ``/collections/<x>/items``
        endpoint, transparently paging via ``offset``/``limit``."""
        offset = 0
        request_params: Dict[str, Any] = dict(params or {})
        request_params.setdefault("limit", page_limit)
        while True:
            request_params["offset"] = offset
            page = self._get(f"/collections/{collection}/items", params=request_params)
            if not page:
                return
            features = page.get("features") or []
            if not features:
                return
            for feature in features:
                yield feature
            if len(features) < page_limit:
                return
            offset += len(features)


def _feature_properties(feature: Dict[str, Any]) -> Dict[str, Any]:
    """Return ``feature.properties`` merged with ``feature.id`` for convenience."""
    props = dict(feature.get("properties") or {})
    if "id" in feature and "id" not in props:
        props["id"] = feature["id"]
    geometry = feature.get("geometry") or {}
    coords = geometry.get("coordinates")
    if isinstance(coords, list) and len(coords) >= 2:
        props.setdefault("longitude", coords[0])
        props.setdefault("latitude", coords[1])
    return props


class DmiMetObsAPI(_DmiBaseAPI):
    """Client for DMI's *meteorological* observation collections."""

    feed_root = METOBS_FEED_ROOT

    def list_stations(self) -> List[Dict[str, Any]]:
        return [_feature_properties(f) for f in self._iter_collection("station")]

    def iter_observations(
        self,
        *,
        period: Optional[str] = None,
        datetime_filter: Optional[str] = None,
        station_id: Optional[str] = None,
        parameter_id: Optional[str] = None,
    ) -> Iterator[Dict[str, Any]]:
        params: Dict[str, Any] = {}
        if period:
            params["period"] = period
        if datetime_filter:
            params["datetime"] = datetime_filter
        if station_id:
            params["stationId"] = station_id
        if parameter_id:
            params["parameterId"] = parameter_id
        for feature in self._iter_collection("observation", params=params):
            yield _feature_properties(feature)


class DmiOceanObsAPI(_DmiBaseAPI):
    """Client for DMI's *oceanographic* observation collections."""

    feed_root = OCEANOBS_FEED_ROOT

    def list_stations(self) -> List[Dict[str, Any]]:
        return [_feature_properties(f) for f in self._iter_collection("station")]

    def list_tidewater_stations(self) -> List[Dict[str, Any]]:
        return [_feature_properties(f) for f in self._iter_collection("tidewaterstation")]

    def iter_observations(
        self,
        *,
        period: Optional[str] = None,
        datetime_filter: Optional[str] = None,
        station_id: Optional[str] = None,
        parameter_id: Optional[str] = None,
    ) -> Iterator[Dict[str, Any]]:
        params: Dict[str, Any] = {}
        if period:
            params["period"] = period
        if datetime_filter:
            params["datetime"] = datetime_filter
        if station_id:
            params["stationId"] = station_id
        if parameter_id:
            params["parameterId"] = parameter_id
        for feature in self._iter_collection("observation", params=params):
            yield _feature_properties(feature)

    def iter_tidewater(
        self,
        *,
        period: Optional[str] = None,
        datetime_filter: Optional[str] = None,
        station_id: Optional[str] = None,
    ) -> Iterator[Dict[str, Any]]:
        params: Dict[str, Any] = {}
        if period:
            params["period"] = period
        if datetime_filter:
            params["datetime"] = datetime_filter
        if station_id:
            params["stationId"] = station_id
        for feature in self._iter_collection("tidewater", params=params):
            yield _feature_properties(feature)


class DmiLightningAPI(_DmiBaseAPI):
    """Client for DMI's *lightning* collections.

    The lightning catalog reports the per-sensor detector network and the
    individual strike observations. Strikes are emitted as a high-rate stream
    (typically several per second during active weather); the Kafka feeder
    publishes every strike, while the MQTT/UNS feeder skips strikes entirely
    because per-strike events do not fit LKV semantics.
    """

    feed_root = LIGHTNING_FEED_ROOT

    def list_sensors(self) -> List[Dict[str, Any]]:
        return [_feature_properties(f) for f in self._iter_collection("sensor")]

    def iter_strikes(
        self,
        *,
        period: Optional[str] = None,
        datetime_filter: Optional[str] = None,
    ) -> Iterator[Dict[str, Any]]:
        params: Dict[str, Any] = {}
        if period:
            params["period"] = period
        if datetime_filter:
            params["datetime"] = datetime_filter
        for feature in self._iter_collection("observation", params=params):
            yield _feature_properties(feature)
