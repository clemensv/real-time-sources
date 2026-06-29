"""HSL GTFS-static fetch and parse for reference data.

The HFP telemetry references routes and stops by id only (``route``/``route_id``
and ``stop``/``next_stop``). To make the stream self-contained, this module
downloads the HSL GTFS-static feed and yields the ``routes.txt`` and
``stops.txt`` rows as plain dictionaries; the transport apps turn those into
``fi.hsl.gtfs.Route`` and ``fi.hsl.gtfs.Stop`` reference events.

Two HSL-specific quirks are handled here so the transport apps do not have to:

* **Encoding.** The HSL GTFS text files are encoded in ``windows-1252`` (Latin
  text such as ``Sörnäinen`` decodes incorrectly as UTF-8). We try UTF-8 first
  (in case HSL switches to spec-compliant UTF-8) and fall back to windows-1252.
* **Whitespace padding.** Empty optional columns are emitted as a single space
  (e.g. ``parent_station=' '``). Those are normalised to ``None`` so empty
  values do not leak onto the wire as whitespace.
"""

from __future__ import annotations

import csv
import io
import logging
import os
import zipfile
from typing import Any, Dict, Iterator, List, Optional

import requests

logger = logging.getLogger(__name__)

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-hsl-hfp/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

# Integer columns per GTFS / HSL extension; everything else stays a string so
# the reference payloads mirror the GTFS text verbatim.
_ROUTE_INT_FIELDS = {"route_type"}
_STOP_INT_FIELDS = {"location_type", "wheelchair_boarding", "vehicle_type"}
_STOP_FLOAT_FIELDS = {"stop_lat", "stop_lon"}


def _decode(raw: bytes) -> str:
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("windows-1252")


def _clean(value: Optional[str]) -> Optional[str]:
    """Strip whitespace; map empty/whitespace-only to ``None``."""
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


class GtfsStatic:
    """Downloads and parses the HSL GTFS-static feed."""

    def __init__(self, gtfs_url: str, session: Optional[requests.Session] = None,
                 request_timeout: float = 180.0) -> None:
        self._url = gtfs_url
        self._session = session or requests.Session()
        self._session.headers["User-Agent"] = USER_AGENT
        self._timeout = request_timeout

    def _download(self) -> zipfile.ZipFile:
        logger.info("Downloading HSL GTFS-static feed from %s", self._url)
        response = self._session.get(self._url, timeout=self._timeout)
        response.raise_for_status()
        logger.info("Downloaded %d bytes of GTFS-static data", len(response.content))
        return zipfile.ZipFile(io.BytesIO(response.content))

    def _read_table(self, archive: zipfile.ZipFile, name: str,
                    int_fields: set, float_fields: set) -> Iterator[Dict[str, Any]]:
        if name not in archive.namelist():
            logger.warning("GTFS member %s not present; skipping", name)
            return
        text = _decode(archive.read(name))
        reader = csv.DictReader(io.StringIO(text))
        for row in reader:
            out: Dict[str, Any] = {}
            for key, value in row.items():
                if key is None:
                    continue
                cleaned = _clean(value)
                if cleaned is None:
                    out[key] = None
                elif key in int_fields:
                    try:
                        out[key] = int(cleaned)
                    except ValueError:
                        out[key] = None
                elif key in float_fields:
                    try:
                        out[key] = float(cleaned)
                    except ValueError:
                        out[key] = None
                else:
                    out[key] = cleaned
            yield out

    def fetch(self) -> "GtfsSnapshot":
        """Download the feed once and return parsed routes and stops."""
        archive = self._download()
        routes = list(self._read_table(archive, "routes.txt", _ROUTE_INT_FIELDS, set()))
        stops = list(self._read_table(archive, "stops.txt", _STOP_INT_FIELDS, _STOP_FLOAT_FIELDS))
        logger.info("Parsed %d routes and %d stops from GTFS-static", len(routes), len(stops))
        return GtfsSnapshot(routes=routes, stops=stops)


class GtfsSnapshot:
    """A parsed snapshot of the GTFS-static reference tables."""

    def __init__(self, routes: List[Dict[str, Any]], stops: List[Dict[str, Any]]) -> None:
        self.routes = routes
        self.stops = stops
