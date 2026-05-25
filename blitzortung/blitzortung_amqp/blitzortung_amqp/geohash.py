"""Geohash helpers for the Blitzortung AMQP bridge."""

from __future__ import annotations

from typing import Optional

_GEOHASH_ALPHABET = "0123456789bcdefghjkmnpqrstuvwxyz"


def geohash(latitude: Optional[float], longitude: Optional[float], precision: int = 5) -> str:
    if latitude is None or longitude is None:
        return "0" * precision
    try:
        lat = float(latitude)
        lon = float(longitude)
    except (TypeError, ValueError):
        return "0" * precision
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        return "0" * precision
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
    return "".join(_GEOHASH_ALPHABET[(bits[i] << 4) | (bits[i + 1] << 3) | (bits[i + 2] << 2) | (bits[i + 3] << 1) | bits[i + 4]] for i in range(0, len(bits), 5))


def geohash5(latitude: Optional[float], longitude: Optional[float]) -> str:
    return geohash(latitude, longitude, 5)


def geohash7(latitude: Optional[float], longitude: Optional[float]) -> str:
    return geohash(latitude, longitude, 7)
