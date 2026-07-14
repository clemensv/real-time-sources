"""HTTP client for the Taiwan YouBike 2.0 public station feed.

The :class:`YouBikeAPI` class is transport-agnostic: it speaks only HTTP and
JSON. Every transport variant builds its CloudEvent producers on top of the raw
station dictionaries this class yields. Stations are returned exactly as the
upstream feed presents them (a single flat JSON array carrying both slow-moving
reference fields and fast-moving availability fields on the same object) so that
the transport-specific code can normalize them onto its generated data classes
via :mod:`taipei_youbike_core.normalize` without repeating HTTP error handling.

Upstream: ``https://apis.youbike.com.tw/json/station-yb2.json`` -- the
island-wide YouBike 2.0 station feed operated by Giant Manufacturing / YouBike
Co., Ltd. Anonymous access; the feed refreshes roughly once per minute and
returns every YouBike 2.0 station across Taiwan (~9,300 stations) in one
document.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

import requests

# The single upstream endpoint. Used verbatim as the CloudEvent ``source`` base;
# per-station sources are formed as ``{FEED_URL}#{station_id}``.
FEED_URL = "https://apis.youbike.com.tw/json/station-yb2.json"

# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-taipei-youbike/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

logger = logging.getLogger(__name__)


class YouBikeAPI:
    """Thin wrapper around the upstream YouBike 2.0 station feed."""

    def __init__(
        self,
        session: Optional[requests.Session] = None,
        request_timeout: float = 30.0,
        feed_url: Optional[str] = None,
    ) -> None:
        self._session = session or requests.Session()
        self._session.headers["User-Agent"] = USER_AGENT
        self._request_timeout = request_timeout
        # Allow overriding the feed URL (mirror hosts / testing) via FEED_URL env.
        self._feed_url = feed_url or os.environ.get("FEED_URL") or FEED_URL

    def list_stations(self) -> List[Dict[str, Any]]:
        """Return the full catalog of YouBike 2.0 stations as the feed exposes it.

        Each element is a station object carrying identity + location + nominal
        capacity (``station_no`` / ``name_tw`` / ``name_en`` / ``lat`` / ``lng``
        / ``parking_spaces`` / ``type`` / ``area_code`` ...) alongside the live
        availability fields (``available_spaces`` / ``available_spaces_detail``
        / ``empty_spaces`` / ``forbidden_spaces`` / ``available_spaces_level`` /
        ``status`` / ``updated_at`` / ``time``).
        """
        response = self._session.get(self._feed_url, timeout=self._request_timeout)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            logger.warning("Unexpected YouBike payload type: %s", type(data).__name__)
            return []
        return data
