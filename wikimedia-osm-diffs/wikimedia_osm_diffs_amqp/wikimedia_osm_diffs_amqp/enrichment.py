"""Geohash-5 enrichment for OSM diff UNS topic placeholders."""

from __future__ import annotations

from typing import Optional

_GEOHASH_ALPHABET = "0123456789bcdefghjkmnpqrstuvwxyz"


def geohash5(latitude: Optional[float], longitude: Optional[float]) -> str:
    """Return the 5-character base32 geohash for ``(latitude, longitude)``.

    Returns ``"nogeo"`` when either coordinate is missing or out of range.
    The returned string is always lowercase ASCII and exactly five
    characters long, suitable for direct substitution into MQTT topic
    placeholders.
    """
    if latitude is None or longitude is None:
        return "nogeo"
    try:
        lat = float(latitude)
        lon = float(longitude)
    except (TypeError, ValueError):
        return "nogeo"
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        return "nogeo"

    precision = 5
    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    bits: list[int] = []
    even = True
    while len(bits) < precision * 5:
        if even:
            mid = (lon_range[0] + lon_range[1]) / 2.0
            if lon >= mid:
                bits.append(1)
                lon_range[0] = mid
            else:
                bits.append(0)
                lon_range[1] = mid
        else:
            mid = (lat_range[0] + lat_range[1]) / 2.0
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
