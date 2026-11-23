"""Bounded HTTP requests and complete OGC collection reads."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from datetime import datetime, timezone
import os
from typing import Any
from urllib.parse import quote, urljoin, urlsplit

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://api.waterdata.usgs.gov/ogcapi/v1"


def utc_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"USGS observation time needs an offset: {value!r}")
    return parsed.astimezone(timezone.utc)


def time_interval(start: datetime, end: datetime) -> str:
    if start.tzinfo is None or end.tzinfo is None or start >= end:
        raise ValueError("A query requires increasing offset-aware start and end times")
    return "/".join(t.astimezone(timezone.utc).isoformat() for t in (start, end))


class WaterDataClient:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        session: requests.Session | None = None,
        page_size: int = 10000,
        timeout: float = 60,
    ) -> None:
        if not 1 <= page_size <= 50000 or timeout <= 0:
            raise ValueError("Invalid USGS page size or timeout")
        self.session = session if session is not None else requests.Session()
        self._owns_session = session is None
        retries = Retry(
            total=4,
            connect=4,
            read=4,
            status=4,
            backoff_factor=1,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET"}),
            respect_retry_after_header=True,
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": os.getenv("USER_AGENT", "real-time-sources-usgs-waterdata/0.1.0"),
            }
        )
        key = api_key if api_key is not None else os.getenv("USGS_API_KEY")
        if key:
            self.session.headers["X-Api-Key"] = key
        self.page_size = page_size
        self.timeout = timeout

    def __enter__(self) -> WaterDataClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_session:
            self.session.close()

    @staticmethod
    def _checked_url(url: str) -> str:
        parsed = urlsplit(url)
        if (
            parsed.scheme != "https"
            or parsed.netloc != "api.waterdata.usgs.gov"
            or not parsed.path.startswith("/ogcapi/v1/")
            or parsed.username is not None
            or parsed.fragment
        ):
            raise ValueError("USGS continuation points outside the Water Data OGC API")
        return url

    def _get(self, url: str, params: Mapping[str, str | int] | None = None) -> dict[str, Any]:
        self._checked_url(url)
        response = self.session.get(url, params=params, timeout=self.timeout, allow_redirects=False)
        if 300 <= response.status_code < 400:
            raise RuntimeError("USGS API redirected a request; refusing to forward credentials")
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("USGS API returned a non-object response")
        return data

    def features(self, collection: str, **filters: str) -> Iterator[dict[str, Any]]:
        if not collection or "/" in collection or any(c in collection for c in "?#"):
            raise ValueError("Expected one OGC collection identifier")
        url = f"{BASE_URL}/collections/{quote(collection, safe='')}/items"
        params: dict[str, str | int] | None = {"f": "json", "limit": self.page_size, **filters}
        seen: set[str] = set()
        while True:
            data = self._get(url, params)
            rows = data.get("features")
            links = data.get("links", [])
            if not isinstance(rows, list) or not isinstance(links, list):
                raise ValueError(f"USGS {collection} response lacks features/links arrays")
            for feature in rows:
                if (
                    not isinstance(feature, dict)
                    or feature.get("type") != "Feature"
                    or not isinstance(feature.get("properties"), dict)
                ):
                    raise ValueError(f"USGS {collection} returned a malformed feature")
                yield feature
            next_links = [link for link in links if isinstance(link, dict) and link.get("rel") == "next"]
            if not next_links:
                return
            if len(next_links) != 1 or not isinstance(next_links[0].get("href"), str):
                raise ValueError(f"USGS {collection} returned ambiguous continuation links")
            next_url = self._checked_url(urljoin(url, next_links[0]["href"]))
            if next_url in seen:
                raise ValueError(f"USGS {collection} repeated a continuation link")
            seen.add(next_url)
            url, params = next_url, None

    def item(self, collection: str, identifier: str) -> dict[str, Any]:
        if not collection or "/" in collection or not identifier:
            raise ValueError("Expected a collection and item identifier")
        data = self._get(
            f"{BASE_URL}/collections/{quote(collection, safe='')}/items/{quote(identifier, safe='')}",
            {"f": "json"},
        )
        if data.get("type") != "Feature" or not isinstance(data.get("properties"), dict):
            raise ValueError(f"USGS {collection} item is not a feature")
        return data

    def observations(
        self,
        start: datetime,
        end: datetime,
        *,
        location_ids: str = "",
        state_code: str = "",
        parameter_codes: str = "",
        modified_since: datetime | None = None,
    ) -> Iterator[dict[str, Any]]:
        filters = self._selection(location_ids, state_code, parameter_codes)
        filters["time"] = time_interval(start, end)
        if modified_since is not None:
            filters["last_modified"] = time_interval(modified_since, end)
        yield from self.features("continuous", **filters)

    @staticmethod
    def _selection(location_ids: str, state_code: str, parameter_codes: str) -> dict[str, str]:
        filters: dict[str, str] = {}
        if location_ids:
            filters["monitoring_location_id"] = location_ids
        elif state_code:
            filters["state_code"] = state_code
        else:
            raise ValueError("USGS acquisition requires explicit locations or a state code")
        if parameter_codes:
            filters["parameter_code"] = parameter_codes
        return filters

    def changes(
        self,
        start: datetime,
        end: datetime,
        *,
        location_ids: str = "",
        state_code: str = "",
        parameter_codes: str = "",
    ) -> Iterator[dict[str, Any]]:
        """Read an update-time window, including corrections to older observations."""
        filters = self._selection(location_ids, state_code, parameter_codes)
        filters["last_modified"] = time_interval(start, end)
        yield from self.features("continuous", **filters)
