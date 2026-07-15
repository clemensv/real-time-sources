"""HTTP client for the Open Charge Map v3 public API.

The :class:`OpenChargeMapAPI` class is transport-agnostic: it speaks only HTTP
and JSON. Every transport variant builds its CloudEvent producers on top of the
raw dictionaries this class yields, normalizing them onto the generated data
classes via :mod:`open_charge_map_core.normalize` without repeating HTTP error
handling.

Upstream: ``https://api.openchargemap.io/v3/`` -- Open Charge Map is the largest
global open registry of electric-vehicle charging equipment (300,000+ locations
worldwide), contributed and verified by operators, national databases and the
public under open licences. Two endpoints are consumed:

* ``/v3/poi/`` -- the point-of-interest (charging location) catalog. Supports a
  ``modifiedsince`` delta parameter, so after an initial back-fill the feeder
  pulls only locations that changed since the last high-water mark. The default
  (non-compact, non-verbose) representation is requested because the feeder
  depends on the inline expanded ``OperatorInfo`` / ``StatusType`` / ``UsageType``
  / ``SubmissionStatus`` / ``AddressInfo.Country`` objects and the expanded
  ``Connections[]`` sub-objects for denormalized labels.
* ``/v3/referencedata/`` -- the lookup tables (operators, connection types,
  current types, charger levels, countries, data providers, status types, usage
  types, submission-status types) emitted as reference events.

Access requires a free API key (register at
``https://openchargemap.org/site/loginprovider/beginlogin``). The key is read
from the ``OPENCHARGEMAP_API_KEY`` environment variable and sent in the
``X-API-Key`` request header.
"""

from __future__ import annotations

import datetime
import logging
import os
from typing import Any, Dict, List, Optional

import requests

# The upstream API root. Used verbatim as the CloudEvent ``source`` base; per-POI
# sources are formed as ``{POI_URL}#{poi_id}`` and per-reference sources as
# ``{REFERENCE_URL}#{reference_type}/{reference_id}``.
BASE_URL = "https://api.openchargemap.io/v3/"
POI_URL = BASE_URL + "poi/"
REFERENCE_URL = BASE_URL + "referencedata/"

# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-open-charge-map/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com")
    + ")"
)

logger = logging.getLogger(__name__)


class OpenChargeMapAPI:
    """Thin wrapper around the Open Charge Map v3 POI and reference-data endpoints."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        session: Optional[requests.Session] = None,
        request_timeout: float = 60.0,
        base_url: Optional[str] = None,
    ) -> None:
        self._api_key = api_key or os.environ.get("OPENCHARGEMAP_API_KEY")
        if not self._api_key:
            raise ValueError(
                "An Open Charge Map API key is required. Set the "
                "OPENCHARGEMAP_API_KEY environment variable (register a free key "
                "at https://openchargemap.org/site/loginprovider/beginlogin)."
            )
        self._session = session or requests.Session()
        self._session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "X-API-Key": self._api_key,
                "Accept": "application/json",
            }
        )
        self._request_timeout = request_timeout
        self._base_url = (base_url or os.environ.get("OCM_BASE_URL") or BASE_URL).rstrip(
            "/"
        ) + "/"

    def list_reference_data(self) -> Dict[str, Any]:
        """Return the Open Charge Map reference-data document.

        A single object keyed by lookup-table name (``Operators``,
        ``ConnectionTypes``, ``CurrentTypes``, ``ChargerTypes``, ``Countries``,
        ``DataProviders``, ``StatusTypes``, ``UsageTypes``,
        ``SubmissionStatusTypes`` and several the feeder does not emit). Each
        value is a list of lookup records.
        """
        response = self._session.get(
            self._base_url + "referencedata/",
            params={"output": "json"},
            timeout=self._request_timeout,
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            logger.warning(
                "Unexpected OCM referencedata payload type: %s", type(data).__name__
            )
            return {}
        return data

    def list_pois(
        self,
        modified_since: Optional[datetime.datetime] = None,
        country_code: Optional[str] = None,
        max_results: int = 5000,
        opendata: bool = True,
    ) -> List[Dict[str, Any]]:
        """Return charging-location (POI) records.

        Args:
            modified_since: When set, only POIs whose ``DateLastStatusUpdate`` /
                ``DateCreated`` changed at or after this instant are returned
                (the ``modifiedsince`` delta). ``None`` requests the full scope.
            country_code: Optional ISO country code (e.g. ``"GB"``) to bound the
                query to a single country. ``None`` requests the global scope.
            max_results: Upper bound on the number of records returned per call
                (the OCM ``maxresults`` parameter).
            opendata: When ``True`` (the default) only openly-licensed records
                are returned, which is the licensing-safe subset for
                republication.
        """
        params: Dict[str, Any] = {
            "output": "json",
            "compact": "false",
            "verbose": "false",
            "maxresults": max_results,
        }
        if opendata:
            params["opendata"] = "true"
        if country_code:
            params["countrycode"] = country_code
        if modified_since is not None:
            if modified_since.tzinfo is None:
                modified_since = modified_since.replace(tzinfo=datetime.timezone.utc)
            params["modifiedsince"] = (
                modified_since.astimezone(datetime.timezone.utc).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                )
            )
        response = self._session.get(
            self._base_url + "poi/", params=params, timeout=self._request_timeout
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            logger.warning("Unexpected OCM poi payload type: %s", type(data).__name__)
            return []
        return data
