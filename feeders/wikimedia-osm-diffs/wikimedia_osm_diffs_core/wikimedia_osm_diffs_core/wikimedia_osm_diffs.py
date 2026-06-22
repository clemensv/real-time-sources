"""Transport-neutral Wikimedia OSM diffs helpers."""

from __future__ import annotations

import datetime
import gzip
import json
import logging
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Optional

import requests

STATE_URL = "https://planet.openstreetmap.org/replication/minute/state.txt"
DIFF_BASE_URL = "https://planet.openstreetmap.org/replication/minute"
DEFAULT_STATE_FILE = os.path.expanduser("~/.wikimedia_osm_diffs_state.json")
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-wikimedia-osm-diffs/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com")
    + ")"
)
DEFAULT_USER_AGENT = USER_AGENT
logger = logging.getLogger(__name__)
_GEOHASH_ALPHABET = "0123456789bcdefghjkmnpqrstuvwxyz"


def parse_state_txt(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if key == "sequenceNumber":
            result["sequence_number"] = int(value)
        elif key == "timestamp":
            ts_str = value.replace("\\:", ":")
            if ts_str.endswith("Z"):
                ts_str = ts_str[:-1] + "+00:00"
            result["timestamp"] = datetime.datetime.fromisoformat(ts_str)
    return result


def sequence_to_path(seq: int) -> str:
    a = seq // 1_000_000
    b = (seq % 1_000_000) // 1_000
    c = seq % 1_000
    return f"{a:03d}/{b:03d}/{c:03d}"


def sequence_to_url(seq: int, base_url: str = DIFF_BASE_URL) -> str:
    return f"{base_url}/{sequence_to_path(seq)}.osc.gz"


def geohash5(latitude: Optional[float], longitude: Optional[float]) -> str:
    if latitude is None or longitude is None:
        return "nogeo"
    try:
        lat = float(latitude)
        lon = float(longitude)
    except (TypeError, ValueError):
        return "nogeo"
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        return "nogeo"
    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    bits: list[int] = []
    even = True
    while len(bits) < 25:
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


def parse_osmchange_xml(xml_bytes: bytes, sequence_number: int) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_bytes)
    changes: list[dict[str, Any]] = []
    for action_elem in root:
        change_type = action_elem.tag
        if change_type not in ("create", "modify", "delete"):
            continue
        for elem in action_elem:
            element_type = elem.tag
            if element_type not in ("node", "way", "relation"):
                continue
            tags: dict[str, str] = {}
            for tag_elem in elem.findall("tag"):
                k = tag_elem.get("k", "")
                v = tag_elem.get("v", "")
                if k:
                    tags[k] = v
            ts_str = elem.get("timestamp", "")
            if ts_str:
                if ts_str.endswith("Z"):
                    ts_str = ts_str[:-1] + "+00:00"
                ts = datetime.datetime.fromisoformat(ts_str)
            else:
                ts = datetime.datetime.now(datetime.timezone.utc)
            uid_str = elem.get("uid")
            user_id = int(uid_str) if uid_str else None
            user_name = elem.get("user") or None
            lat_str = elem.get("lat")
            lon_str = elem.get("lon")
            latitude = float(lat_str) if lat_str else None
            longitude = float(lon_str) if lon_str else None
            changes.append({
                "change_type": change_type,
                "element_type": element_type,
                "element_id": int(elem.get("id", "0")),
                "geohash5": geohash5(latitude, longitude),
                "version": int(elem.get("version", "0")),
                "timestamp": ts,
                "changeset_id": int(elem.get("changeset", "0")),
                "user_name": user_name,
                "user_id": user_id,
                "latitude": latitude,
                "longitude": longitude,
                "tags": json.dumps(tags, separators=(",", ":"), ensure_ascii=False),
                "sequence_number": sequence_number,
            })
    return changes


class StateStore:
    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def load(self) -> Optional[int]:
        if not self._path.exists():
            return None
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Failed to load state file %s: %s", self._path, exc)
            return None
        return payload.get("last_sequence_number")

    def save(self, last_sequence_number: int) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps({"last_sequence_number": last_sequence_number}, indent=2), encoding="utf-8")


def build_session(user_agent: str = DEFAULT_USER_AGENT) -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = user_agent
    return session


def fetch_state(session: requests.Session, state_url: str = STATE_URL) -> Optional[dict[str, Any]]:
    try:
        resp = session.get(state_url, timeout=30)
        resp.raise_for_status()
        return parse_state_txt(resp.text)
    except (requests.RequestException, ValueError, KeyError) as exc:
        logger.warning("Failed to fetch state: %s", exc)
        return None


def fetch_sequence_changes(session: requests.Session, seq: int, diff_base_url: str = DIFF_BASE_URL) -> list[dict[str, Any]]:
    url = sequence_to_url(seq, diff_base_url)
    resp = session.get(url, timeout=60)
    resp.raise_for_status()
    return parse_osmchange_xml(gzip.decompress(resp.content), seq)
