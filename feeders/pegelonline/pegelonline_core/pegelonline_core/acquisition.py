"""HTTP client for the WSV PegelOnline REST API.

The :class:`PegelOnlineAPI` class is transport-agnostic: it speaks only HTTP
and JSON. Both the Kafka and the MQTT feeder build their CloudEvent producers
on top of the dictionaries this class yields. Stations and current
measurements are returned exactly as the upstream API presents them so that
the transport-specific code can map them onto its generated data classes
without having to repeat HTTP error handling, ETag caching, or sideline
bookkeeping.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

import requests


FEED_URL_ROOT = "https://www.pegelonline.wsv.de/webservices/rest-api/v2"
# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-pegelonline/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)


class PegelOnlineAPI:
    """Thin wrapper around the upstream PegelOnline REST API."""

    def __init__(self, session: Optional[requests.Session] = None, request_timeout: float = 10.0) -> None:
        self._session = session or requests.Session()
        self._session.headers["User-Agent"] = USER_AGENT
        self._request_timeout = request_timeout
        # URLs that returned non-200/304 are sidelined for the lifetime of the process.
        self.skip_urls: List[str] = []
        # ETag cache keyed by full URL.
        self.etags: Dict[str, str] = {}

    # ------------------------------------------------------------------ stations
    def list_stations(self) -> List[Dict[str, Any]]:
        """Return the catalog of all stations as the upstream API exposes it."""
        url = f"{FEED_URL_ROOT}/stations.json"
        response = self._session.get(url, timeout=self._request_timeout)
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------ measurements
    def get_water_level(self, station: str) -> Optional[Dict[str, Any]]:
        """Return the latest water-level measurement for one station.

        Returns ``None`` when the URL has been sidelined or the API has nothing
        new to deliver (HTTP 304 against the cached ETag).
        """
        url = f"{FEED_URL_ROOT}/stations/{station}/W/currentmeasurement.json"
        if url in self.skip_urls:
            return None
        etag = self.etags.get(url)
        headers = {"If-None-Match": etag} if etag else None
        response = self._session.get(url, headers=headers, timeout=self._request_timeout)
        if response.status_code == 200:
            self.etags[url] = response.headers.get("ETag", "")
            return response.json()
        if response.status_code == 304:
            return None
        logging.warning(
            "Request to %s failed with status code %s. Sidelining URL.",
            url,
            response.status_code,
        )
        self.skip_urls.append(url)
        return None

    def get_water_levels(self) -> Dict[str, Dict[str, Any]]:
        """Return current measurements for every station in a single call.

        The PegelOnline API exposes a bulk variant of ``stations.json`` that
        includes the current ``W`` timeseries measurement inline. We pull that
        in one request and reshape it into ``{station_uuid: measurement}`` so
        the polling loop can compare against the previously persisted state.
        """
        url = f"{FEED_URL_ROOT}/stations.json?includeTimeseries=true&includeCurrentMeasurement=true"
        response = self._session.get(url, timeout=self._request_timeout)
        if response.status_code != 200:
            logging.warning("Request to %s failed with status code %s.", url, response.status_code)
            return {}
        station_levels: Dict[str, Dict[str, Any]] = {}
        for station in response.json():
            for timeseries in station.get("timeseries", []) or []:
                if timeseries.get("shortname") == "W" and "currentMeasurement" in timeseries:
                    measurement = dict(timeseries["currentMeasurement"])
                    measurement["uuid"] = station["uuid"]
                    station_levels[station["uuid"]] = measurement
        return station_levels
