"""Deterministic offline GBFS corpus for `--mock` / CI flow tests.

The GBFS feeders normally poll live third-party auto-discovery endpoints
(e.g. Citi Bike), which makes Docker E2E flow tests non-deterministic and
prone to outages. This module provides a small, self-contained GBFS dataset
plus an in-memory HTTP session so the bridge can exercise its real
discovery / normalize / dedupe / emit path without any network access.

The payloads mirror the GBFS v2.3 wire shapes the production parser expects,
so a `--mock` run flows through exactly the same code as a live run.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .acquisition import GbfsSourceClient
from .config import ConfiguredFeed

MOCK_SYSTEM_ID = "sample-bikeshare"

MOCK_DISCOVERY_URL = "https://mock.gbfs.invalid/gbfs/gbfs.json"
MOCK_SYSTEM_URL = "https://mock.gbfs.invalid/gbfs/system_information.json"
MOCK_STATION_INFO_URL = "https://mock.gbfs.invalid/gbfs/station_information.json"
MOCK_STATION_STATUS_URL = "https://mock.gbfs.invalid/gbfs/station_status.json"
MOCK_FREE_BIKE_URL = "https://mock.gbfs.invalid/gbfs/free_bike_status.json"

MOCK_MANIFEST: Dict[str, Any] = {
    "last_updated": 1717488120,
    "ttl": 60,
    "version": "2.3",
    "data": {
        "en": {
            "feeds": [
                {"name": "system_information", "url": MOCK_SYSTEM_URL},
                {"name": "station_information", "url": MOCK_STATION_INFO_URL},
                {"name": "station_status", "url": MOCK_STATION_STATUS_URL},
                {"name": "free_bike_status", "url": MOCK_FREE_BIKE_URL},
            ]
        }
    },
}

MOCK_SYSTEM: Dict[str, Any] = {
    "last_updated": 1717488120,
    "ttl": 3600,
    "version": "2.3",
    "data": {
        "system_id": MOCK_SYSTEM_ID,
        "name": "Sample City Bikeshare",
        "operator": "Sample Mobility Operator",
        "url": "https://mock.gbfs.invalid",
        "timezone": "Europe/Berlin",
        "language": "en",
        "phone_number": "+49-000-0000000",
    },
}

MOCK_STATION_INFO: Dict[str, Any] = {
    "last_updated": 1717488120,
    "ttl": 3600,
    "version": "2.3",
    "data": {
        "stations": [
            {
                "station_id": "station-001",
                "name": "Central Station",
                "short_name": "001",
                "lat": 52.5200,
                "lon": 13.4050,
                "capacity": 24,
                "region_id": "central",
                "address": "1 Central Plaza",
                "post_code": "10115",
            },
            {
                "station_id": "station-002",
                "name": "Riverside Dock",
                "short_name": "002",
                "lat": 52.5145,
                "lon": 13.3899,
                "capacity": 16,
                "region_id": "central",
                "address": "8 Riverside Way",
                "post_code": "10117",
            },
            {
                "station_id": "station-003",
                "name": "University Gate",
                "short_name": "003",
                "lat": 52.5290,
                "lon": 13.4100,
                "capacity": 30,
                "region_id": "north",
                "address": "200 Campus Road",
                "post_code": "10119",
            },
        ]
    },
}

MOCK_STATION_STATUS: Dict[str, Any] = {
    "last_updated": 1717488123,
    "ttl": 30,
    "version": "2.3",
    "data": {
        "stations": [
            {
                "station_id": "station-001",
                "num_bikes_available": 7,
                "num_docks_available": 17,
                "num_ebikes_available": 3,
                "is_installed": 1,
                "is_renting": 1,
                "is_returning": 1,
                "last_reported": 1717488123,
            },
            {
                "station_id": "station-002",
                "num_bikes_available": 2,
                "num_docks_available": 14,
                "num_ebikes_available": 0,
                "is_installed": 1,
                "is_renting": 1,
                "is_returning": 1,
                "last_reported": 1717488123,
            },
            {
                "station_id": "station-003",
                "num_bikes_available": 15,
                "num_docks_available": 15,
                "num_ebikes_available": 6,
                "is_installed": 1,
                "is_renting": 1,
                "is_returning": 1,
                "last_reported": 1717488123,
            },
        ]
    },
}

MOCK_FREE_BIKES: Dict[str, Any] = {
    "last_updated": 1717488123,
    "ttl": 15,
    "version": "2.3",
    "data": {
        "bikes": [
            {
                "bike_id": "bike-0001",
                "lat": 52.5180,
                "lon": 13.3990,
                "is_reserved": False,
                "is_disabled": False,
                "vehicle_type_id": "ebike",
                "current_range_meters": 18000,
                "last_reported": 1717488110,
            },
            {
                "bike_id": "bike-0002",
                "lat": 52.5260,
                "lon": 13.4075,
                "is_reserved": False,
                "is_disabled": False,
                "vehicle_type_id": "bike",
                "current_range_meters": None,
                "last_reported": 1717488112,
            },
        ]
    },
}

MOCK_RESPONSES: Dict[str, Dict[str, Any]] = {
    MOCK_DISCOVERY_URL: MOCK_MANIFEST,
    MOCK_SYSTEM_URL: MOCK_SYSTEM,
    MOCK_STATION_INFO_URL: MOCK_STATION_INFO,
    MOCK_STATION_STATUS_URL: MOCK_STATION_STATUS,
    MOCK_FREE_BIKE_URL: MOCK_FREE_BIKES,
}


class _OfflineResponse:
    def __init__(self, payload: Dict[str, Any]):
        self._payload = payload
        self.status_code = 200

    def raise_for_status(self) -> None:
        return None

    def json(self) -> Dict[str, Any]:
        return self._payload


class OfflineSession:
    """Minimal `requests.Session` stand-in serving the in-memory corpus."""

    def __init__(self, mapping: Dict[str, Dict[str, Any]] | None = None):
        self.mapping = mapping if mapping is not None else MOCK_RESPONSES
        self.headers: Dict[str, str] = {}

    def get(self, url: str, timeout: int = 30) -> _OfflineResponse:  # noqa: ARG002
        if url not in self.mapping:
            raise AssertionError(f"OfflineSession received an unexpected URL: {url}")
        return _OfflineResponse(self.mapping[url])

    def mount(self, prefix: str, adapter: Any) -> None:  # noqa: ARG002 - API parity
        return None


def build_offline_client_and_feeds() -> Tuple[GbfsSourceClient, List[ConfiguredFeed]]:
    """Return a client + feed list wired to the deterministic offline corpus.

    Used by every transport app's ``--mock`` / ``GBFS_MOCK`` path so CI flow
    tests publish a stable reference + telemetry set without touching the
    network.
    """
    client = GbfsSourceClient(session=OfflineSession())
    feeds = [ConfiguredFeed(MOCK_DISCOVERY_URL, MOCK_SYSTEM_ID)]
    return client, feeds
