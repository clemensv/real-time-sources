"""HTTP client for the Transport for London (TfL) Unified API BikePoint feed.

The :class:`TfLCyclesAPI` class is transport-agnostic: it speaks only HTTP and
JSON. Every transport variant builds its CloudEvent producers on top of the raw
``Place`` dictionaries this class yields. BikePoints are returned exactly as the
upstream API presents them (identity + ``additionalProperties`` array) so that
the transport-specific code can normalize them onto its generated data classes
via :mod:`tfl_cycles_core.normalize` without repeating HTTP error handling.

Upstream: https://api.tfl.gov.uk/BikePoint (TfL Unified API, "BikePoint"
resource). Anonymous access works but is rate limited; supplying an
application key via ``TFL_APP_KEY`` raises the quota.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

import requests

FEED_URL_ROOT = "https://api.tfl.gov.uk"
# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-tfl-cycles/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

logger = logging.getLogger(__name__)


class TfLCyclesAPI:
    """Thin wrapper around the upstream TfL Unified API BikePoint resource."""

    def __init__(
        self,
        session: Optional[requests.Session] = None,
        request_timeout: float = 30.0,
        app_key: Optional[str] = None,
    ) -> None:
        self._session = session or requests.Session()
        self._session.headers["User-Agent"] = USER_AGENT
        self._request_timeout = request_timeout
        # TfL application key for higher rate limits (optional; anonymous works).
        self._app_key = app_key or os.environ.get("TFL_APP_KEY") or None

    def _params(self) -> Dict[str, str]:
        return {"app_key": self._app_key} if self._app_key else {}

    def list_bikepoints(self) -> List[Dict[str, Any]]:
        """Return the full catalog of BikePoints as the upstream API exposes it.

        Each element is a TfL ``Place`` object carrying ``id`` / ``commonName``
        / ``lat`` / ``lon`` plus a stringly-typed ``additionalProperties`` array
        (NbBikes, NbEmptyDocks, NbDocks, Installed, Locked, Temporary, ...).
        """
        url = f"{FEED_URL_ROOT}/BikePoint"
        response = self._session.get(url, params=self._params(), timeout=self._request_timeout)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            logger.warning("Unexpected BikePoint payload type: %s", type(data).__name__)
            return []
        return data
