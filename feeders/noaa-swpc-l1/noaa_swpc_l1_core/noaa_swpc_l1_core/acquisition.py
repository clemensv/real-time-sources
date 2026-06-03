"""HTTP client for the NOAA SWPC propagated-solar-wind product.

The :class:`SwpcL1API` is transport-agnostic: it speaks only HTTP and JSON.
All three feeders (Kafka, MQTT, AMQP) build their CloudEvent producers on top
of the dictionaries / dataclasses this module yields.

Upstream shape (verbatim, live-confirmed):

* URL: ``https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json``
* Response: array-of-arrays. Row 0 = header
  ``[time_tag, speed, density, temperature, bx, by, bz, bt, vx, vy, vz,
  propagated_time_tag]``. Rows 1..N = one observation per minute, ~10,080
  rows for a 7-day rolling window. ``vx/vy/vz`` are commonly null
  (DSCOVR does not measure them reliably); magnetometer values can also be
  null on instrument gaps; plasma values rarely null.
* Upstream timestamps are ``"YYYY-MM-DD HH:MM:SS.fff"`` strings with
  implicit UTC. This module normalizes to RFC 3339 with explicit ``Z``.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, List, Optional

import requests


FEED_URL = "https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json"

EXPECTED_COLUMNS = [
    "time_tag",
    "speed",
    "density",
    "temperature",
    "bx",
    "by",
    "bz",
    "bt",
    "vx",
    "vy",
    "vz",
    "propagated_time_tag",
]


logger = logging.getLogger(__name__)

# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-noaa-swpc-l1/1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

@dataclass(frozen=True)
class PropagatedSolarWindRow:
    """Normalized representation of one upstream row.

    All numeric fields are :class:`float` or :data:`None`; timestamps are
    timezone-aware :class:`datetime` values in UTC. ``spacecraft`` is
    synthesized by the caller (bridge), not present in the upstream payload.
    """

    spacecraft: str
    time_tag: datetime
    propagated_time_tag: datetime
    speed: Optional[float]
    density: Optional[float]
    temperature: Optional[float]
    bx: Optional[float]
    by: Optional[float]
    bz: Optional[float]
    bt: Optional[float]
    vx: Optional[float]
    vy: Optional[float]
    vz: Optional[float]


def _parse_timestamp(raw: str) -> datetime:
    """Parse SWPC's ``YYYY-MM-DD HH:MM:SS.fff`` (implicit UTC) into aware UTC."""
    # SWPC always uses a single space separator and fractional seconds.
    # Accept missing fractional seconds defensively.
    fmts = ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S")
    for fmt in fmts:
        try:
            return datetime.strptime(raw, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    # Last-ditch: ISO 8601 with explicit offset.
    return datetime.fromisoformat(raw).astimezone(timezone.utc)


def _to_float(value: Any) -> Optional[float]:
    """Convert upstream value (str/number/null) to ``float`` or ``None``."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def parse_row(row: List[Any], spacecraft: str) -> Optional[PropagatedSolarWindRow]:
    """Convert one upstream row to a :class:`PropagatedSolarWindRow`.

    Returns :data:`None` when the row lacks a parseable ``time_tag`` or
    ``propagated_time_tag`` (those two fields are mandatory in the
    contract). Partial-null plasma/magnetic/velocity values are kept —
    operators want those rows on the wire.
    """
    if not row or len(row) < len(EXPECTED_COLUMNS):
        return None
    try:
        time_tag = _parse_timestamp(str(row[0]))
        propagated_time_tag = _parse_timestamp(str(row[11]))
    except (ValueError, TypeError) as e:
        logger.debug("Skipping unparseable row %r: %s", row, e)
        return None
    return PropagatedSolarWindRow(
        spacecraft=spacecraft,
        time_tag=time_tag,
        propagated_time_tag=propagated_time_tag,
        speed=_to_float(row[1]),
        density=_to_float(row[2]),
        temperature=_to_float(row[3]),
        bx=_to_float(row[4]),
        by=_to_float(row[5]),
        bz=_to_float(row[6]),
        bt=_to_float(row[7]),
        vx=_to_float(row[8]),
        vy=_to_float(row[9]),
        vz=_to_float(row[10]),
    )


class SwpcL1API:
    """Thin wrapper around the upstream SWPC propagated-solar-wind endpoint."""

    def __init__(
        self,
        session: Optional[requests.Session] = None,
        request_timeout: float = 30.0,
        feed_url: str = FEED_URL,
    ) -> None:
        self._session = session or requests.Session()
        if not hasattr(self._session, "headers"):
            self._session.headers = {}
        self._session.headers["User-Agent"] = USER_AGENT
        self._request_timeout = request_timeout
        self._feed_url = feed_url

    @property
    def feed_url(self) -> str:
        return self._feed_url

    def fetch_raw(self) -> List[List[Any]]:
        """GET the upstream document and return the raw array-of-arrays."""
        response = self._session.get(self._feed_url, timeout=self._request_timeout)
        response.raise_for_status()
        document = response.json()
        if not isinstance(document, list) or len(document) < 1:
            raise ValueError("Unexpected SWPC payload shape: not an array-of-arrays")
        return document

    def fetch_rows(self, spacecraft: str) -> List[PropagatedSolarWindRow]:
        """GET the upstream document and yield parsed rows in chronological order.

        Validates that the header row exposes the expected 12 columns in the
        documented order; raises :class:`ValueError` on header drift so that
        downstream consumers cannot silently emit mis-aligned values.
        """
        document = self.fetch_raw()
        header = [str(c).strip().lower() for c in document[0]]
        if header != EXPECTED_COLUMNS:
            raise ValueError(
                f"SWPC propagated-solar-wind header changed: expected {EXPECTED_COLUMNS!r}, got {header!r}"
            )
        rows: List[PropagatedSolarWindRow] = []
        for raw in document[1:]:
            parsed = parse_row(raw, spacecraft=spacecraft)
            if parsed is not None:
                rows.append(parsed)
        rows.sort(key=lambda r: r.time_tag)
        return rows

    def fetch_new_rows(
        self,
        spacecraft: str,
        *,
        since: Optional[datetime] = None,
    ) -> Iterable[PropagatedSolarWindRow]:
        """Yield rows strictly newer than ``since`` (UTC datetime or ``None``)."""
        rows = self.fetch_rows(spacecraft)
        if since is None:
            yield from rows
            return
        for row in rows:
            if row.time_tag > since:
                yield row
