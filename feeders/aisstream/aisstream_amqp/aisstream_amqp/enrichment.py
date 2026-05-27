"""Enrichment helpers for the AISstream -> MQTT/UNS bridge.

Three axis derivations:

* :func:`mid_to_iso`  - first three digits of the MMSI mapped to an
  ISO-3166-1 alpha-2 country code via the ITU MID (Maritime
  Identification Digit) registry. Returns ``'xx'`` for MIDs that have
  no country mapping (e.g. inland-water identifiers 0xx, auxiliary
  craft, base stations, SAR aircraft, MOB / EPIRB devices) or for
  MMSIs shorter than 9 digits.
* :func:`geohash5`   - 5-character geohash of a (lat, lon) pair.
* :func:`ship_type_bucket` - ITU-R M.1371 ship type code (0..99) to
  the kebab-case UNS bucket used as the ``{ship_type}`` segment.

The MID table is the public ITU MID registry (ITU-R M.585) trimmed to
the ~310 MIDs in active use as of 2024. It is checked in directly to
avoid a runtime download. To refresh, edit ``mid_iso.csv`` next to this
module and bump ``MID_ISO_VERSION``.
"""

from __future__ import annotations

import csv
import pathlib
from functools import lru_cache
from typing import Dict, Optional

MID_ISO_VERSION = "2024-01"

_THIS_DIR = pathlib.Path(__file__).resolve().parent
_MID_CSV = _THIS_DIR / "mid_iso.csv"


@lru_cache(maxsize=1)
def _load_mid_table() -> Dict[str, str]:
    table: Dict[str, str] = {}
    with _MID_CSV.open("r", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            mid, iso = row[0].strip(), row[1].strip().lower()
            if mid and iso:
                table[mid] = iso
    return table


def mid_to_iso(mmsi) -> str:
    """Return the ISO-3166-1 alpha-2 code for ``mmsi`` or ``'xx'``."""
    if mmsi is None:
        return "xx"
    s = str(mmsi).strip()
    if not s.isdigit() or len(s) < 9:
        return "xx"
    mid = s[:3]
    return _load_mid_table().get(mid, "xx")


_GEOHASH_ALPHABET = "0123456789bcdefghjkmnpqrstuvwxyz"


def geohash5(latitude: Optional[float], longitude: Optional[float]) -> str:
    """Return the 5-character geohash of (lat, lon).

    Returns ``'00000'`` if either coordinate is missing or out of the
    valid range. Implements the standard base-32 geohash encoder; no
    external dependency.
    """
    if latitude is None or longitude is None:
        return "00000"
    try:
        lat = float(latitude)
        lon = float(longitude)
    except (TypeError, ValueError):
        return "00000"
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        return "00000"
    precision = 5
    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    bits = []
    even = True
    while len(bits) < precision * 5:
        if even:
            mid = (lon_range[0] + lon_range[1]) / 2
            if lon >= mid:
                bits.append(1)
                lon_range[0] = mid
            else:
                bits.append(0)
                lon_range[1] = mid
        else:
            mid = (lat_range[0] + lat_range[1]) / 2
            if lat >= mid:
                bits.append(1)
                lat_range[0] = mid
            else:
                bits.append(0)
                lat_range[1] = mid
        even = not even
    out = []
    for i in range(0, len(bits), 5):
        idx = (bits[i] << 4) | (bits[i + 1] << 3) | (bits[i + 2] << 2) | (bits[i + 3] << 1) | bits[i + 4]
        out.append(_GEOHASH_ALPHABET[idx])
    return "".join(out)


# ITU-R M.1371 Table 53 ShipType code -> kebab UNS bucket. We collapse
# the 100 codes into 12 publicly useful buckets; the raw numeric code
# is preserved on the payload as ``ship_type_code``.
def ship_type_bucket(code) -> str:
    """Return the kebab-case ship-type bucket for an ITU code."""
    if code is None:
        return "unknown"
    try:
        c = int(code)
    except (TypeError, ValueError):
        return "unknown"
    if c == 0:
        return "unknown"
    if c in (30,):
        return "fishing"
    if c in (31, 32):
        return "tug"
    if c == 33:
        return "dredger"
    if c == 34:
        return "diving"
    if c == 35:
        return "military"
    if c == 36:
        return "sailing"
    if c == 37:
        return "pleasure-craft"
    if c == 51:
        return "search-and-rescue"
    if c in (50, 52, 53, 54, 55, 58, 59):
        return "service"  # pilot, port-tender, anti-pollution, law-enforcement, medical, etc.
    if 40 <= c <= 49:
        return "high-speed-craft"
    if 60 <= c <= 69:
        return "passenger"
    if 70 <= c <= 79:
        return "cargo"
    if 80 <= c <= 89:
        return "tanker"
    if 90 <= c <= 99:
        return "other"
    return "unknown"
