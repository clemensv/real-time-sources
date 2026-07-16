"""HTTP client for the CelesTrak orbital-data REST API.

The :class:`CelesTrakAPI` class is transport-agnostic: it speaks only HTTP and
JSON. Every transport variant (Kafka, MQTT, AMQP) builds its CloudEvents
producers on top of the raw dictionaries this class yields, so the
transport-specific code only has to map upstream JSON onto its own generated
data classes without repeating HTTP error handling or the usage-policy guard.

Three families are exposed, all keyed on ``NORAD_CAT_ID``:

* :meth:`get_satcat` -- the US Space Force satellite catalog (SATCAT) records,
  emitted as reference data (``satcat/records.php``).
* :meth:`get_gp` -- General Perturbations mean orbital element sets, the core
  telemetry (``NORAD/elements/gp.php``).
* :meth:`get_supgp` -- optional Supplemental GP element sets contributed by
  operators and analysis centres (``NORAD/elements/supplemental/sup-gp.php``).

Usage policy (hard requirement)
-------------------------------
CelesTrak explicitly asks clients to send a descriptive ``User-Agent`` with a
contact, to query GROUP/SOURCE *views* rather than hammering per-object, and to
**stop immediately** on an error response -- repeated violations get the source
IP firewalled. This client therefore:

* sends a descriptive ``User-Agent`` (override with ``USER_AGENT`` or just the
  contact with ``USER_AGENT_CONTACT``);
* fetches whole GROUP / SOURCE views in a single request each; and
* treats HTTP 403 / 429 / 503 as a **hard stop**: it sets :attr:`halted`,
  abandons the rest of the cycle, and leaves it to the calling loop to back off
  for a long interval before even considering another request.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

import requests

BASE_URL = "https://celestrak.org"
GP_URL = f"{BASE_URL}/NORAD/elements/gp.php"
SATCAT_URL = f"{BASE_URL}/satcat/records.php"
SUPGP_URL = f"{BASE_URL}/NORAD/elements/supplemental/sup-gp.php"

# Statuses that mean "you are being rate-limited or blocked -- back off now".
HARD_STOP_STATUSES = frozenset({403, 429, 503})

# Outbound HTTP identity. Operators can override the whole string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-celestrak/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)


class CelesTrakAPI:
    """Thin wrapper around the upstream CelesTrak REST endpoints."""

    def __init__(self, session: Optional[requests.Session] = None, request_timeout: float = 30.0) -> None:
        self._session = session or requests.Session()
        self._session.headers["User-Agent"] = USER_AGENT
        self._request_timeout = request_timeout
        # Set once a hard-stop status is seen; the caller must back off and only
        # clear it (via reset_halt) after a long, deliberate pause.
        self.halted = False

    def reset_halt(self) -> None:
        """Clear the halt flag before a fresh cycle after the caller backed off."""
        self.halted = False

    # ------------------------------------------------------------------ internal
    def _get_json(self, url: str, params: Dict[str, str]) -> Optional[List[Dict[str, Any]]]:
        """GET one CelesTrak view and return its JSON array, or ``None``.

        Returns ``None`` (without raising) on any non-200 response so the polling
        loop keeps running; a 403/429/503 additionally trips :attr:`halted` so
        the caller stops querying entirely and backs off.
        """
        if self.halted:
            return None
        try:
            response = self._session.get(url, params=params, timeout=self._request_timeout)
        except requests.RequestException as exc:
            logging.warning("CelesTrak request to %s failed: %s", url, exc)
            return None
        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                # CelesTrak answers an invalid GROUP/SOURCE with a 200 text page
                # rather than JSON; treat that as an empty view.
                logging.warning("CelesTrak returned non-JSON body for %s (params=%s).", url, params)
                return []
            if isinstance(data, list):
                return data
            logging.warning("CelesTrak returned a non-array JSON body for %s (params=%s).", url, params)
            return []
        if response.status_code in HARD_STOP_STATUSES:
            logging.error(
                "CelesTrak returned HTTP %s for %s -- usage-policy hard stop; halting all "
                "queries and backing off to avoid an IP block.",
                response.status_code,
                response.url,
            )
            self.halted = True
            return None
        logging.warning(
            "CelesTrak returned HTTP %s for %s -- skipping this fetch.",
            response.status_code,
            response.url,
        )
        return None

    # ------------------------------------------------------------------ SATCAT (reference)
    def get_satcat(self, groups: List[str]) -> List[Dict[str, Any]]:
        """Return SATCAT records for the configured GROUP views, deduped by NORAD id.

        A satellite that appears in more than one group is emitted once. Stops
        early and returns whatever was collected if a hard-stop status is hit.
        """
        merged: Dict[int, Dict[str, Any]] = {}
        for group in groups:
            rows = self._get_json(SATCAT_URL, {"GROUP": group, "FORMAT": "json"})
            if self.halted:
                break
            for row in rows or []:
                norad = row.get("NORAD_CAT_ID")
                if norad is not None:
                    merged[int(norad)] = row
        return list(merged.values())

    # ------------------------------------------------------------------ GP (telemetry)
    def get_gp(self, groups: List[str]) -> List[Dict[str, Any]]:
        """Return GP element sets for the configured GROUP views, deduped by NORAD id."""
        merged: Dict[int, Dict[str, Any]] = {}
        for group in groups:
            rows = self._get_json(GP_URL, {"GROUP": group, "FORMAT": "json"})
            if self.halted:
                break
            for row in rows or []:
                norad = row.get("NORAD_CAT_ID")
                if norad is not None:
                    merged[int(norad)] = row
        return list(merged.values())

    # ------------------------------------------------------------------ SupGP (optional telemetry)
    def get_supgp(self, sources: List[str]) -> List[Dict[str, Any]]:
        """Return Supplemental GP element sets for the configured SOURCE views.

        Unlike GP, a single object may legitimately carry several SupGP element
        sets (distinguished by ``DATA_SOURCE`` and ``EPOCH``), so results are
        **not** deduped by NORAD id here; the polling loop dedupes on the full
        identity instead.
        """
        collected: List[Dict[str, Any]] = []
        for source in sources:
            rows = self._get_json(SUPGP_URL, {"SOURCE": source, "FORMAT": "json"})
            if self.halted:
                break
            collected.extend(rows or [])
        return collected
