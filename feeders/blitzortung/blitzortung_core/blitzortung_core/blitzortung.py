"""Transport-neutral Blitzortung acquisition helpers."""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

import websockets.sync.client as ws_client

_GEOHASH_ALPHABET = "0123456789bcdefghjkmnpqrstuvwxyz"

DEFAULT_WS_URLS = (
    "wss://live.lightningmaps.org:443/",
    "wss://live2.lightningmaps.org:443/",
)
DEFAULT_BBOX = (90.0, 180.0, -90.0, -180.0)
DEFAULT_TOPIC = "blitzortung"
DEFAULT_SOURCE_MASK = 4
DEFAULT_STATE_FILE = os.path.expanduser("~/.blitzortung_state.json")
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-blitzortung/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com")
    + ")"
)
DEFAULT_USER_AGENT = USER_AGENT
logger = logging.getLogger(__name__)


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
    bits: list[int] = []
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


def geohash5(latitude: Optional[float], longitude: Optional[float]) -> str:
    return geohash(latitude, longitude, 5)


def geohash7(latitude: Optional[float], longitude: Optional[float]) -> str:
    return geohash(latitude, longitude, 7)


def parse_connection_string(connection_string: str) -> dict[str, str]:
    config_dict: dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=", 1)[1].strip('"').strip().replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=", 1)[1].strip('"').strip()
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = "$ConnectionString"
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = connection_string.strip()
            elif "BootstrapServer" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


def parse_ws_urls(value: str | None) -> list[str]:
    if not value:
        return list(DEFAULT_WS_URLS)
    urls = [item.strip() for item in value.split(",") if item.strip()]
    if not urls:
        raise ValueError("At least one websocket URL is required")
    return urls


def parse_bbox(value: str | None) -> tuple[float, float, float, float]:
    if not value:
        return DEFAULT_BBOX
    parts = [float(item.strip()) for item in value.split(",")]
    if len(parts) != 4:
        raise ValueError("Bounding box must be north,east,south,west")
    north, east, south, west = parts
    if north < south:
        raise ValueError("Bounding box north must be >= south")
    if not (-90.0 <= south <= 90.0 and -90.0 <= north <= 90.0):
        raise ValueError("Latitude bounds must be between -90 and 90")
    if not (-180.0 <= west <= 180.0 and -180.0 <= east <= 180.0):
        raise ValueError("Longitude bounds must be between -180 and 180")
    return north, east, south, west


def parse_bool(value: str | bool | None, *, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return value.strip().lower() in {"1", "true", "yes", "on"}


def epoch_millis_to_iso8601(timestamp_ms: int) -> str:
    return datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def build_request(last_ids: dict[str, int], *, include_stations: bool, bbox: tuple[float, float, float, float], source_mask: int, zoom: int = 5, reason: str = "feed", loop_count: int = 0, server_time: int = 0) -> str:
    north, east, south, west = bbox
    payload = {
        "v": 24,
        "i": last_ids,
        "s": include_stations,
        "x": 0,
        "w": 0,
        "tx": 0,
        "tw": 0,
        "a": source_mask,
        "z": zoom,
        "b": True,
        "h": "",
        "l": loop_count,
        "t": server_time,
        "from_lightningmaps_org": True,
        "p": [north, east, south, west],
        "r": reason,
    }
    return json.dumps(payload, separators=(",", ":"))


def normalize_stroke(stroke: dict[str, Any]) -> dict[str, Any]:
    timestamp_ms = int(stroke["time"])
    station_map = stroke.get("sta")
    detector_participations: list[dict[str, int]] = []
    if isinstance(station_map, dict):
        for station_id, status in sorted(station_map.items(), key=lambda item: int(item[0])):
            detector_participations.append({"station_id": int(station_id), "status": int(status)})
    latitude = float(stroke["lat"])
    longitude = float(stroke["lon"])
    return {
        "source_id": int(stroke["src"]),
        "stroke_id": str(stroke["id"]),
        "event_time": epoch_millis_to_iso8601(timestamp_ms),
        "event_timestamp_ms": timestamp_ms,
        "latitude": latitude,
        "longitude": longitude,
        "server_id": int(stroke["srv"]) if stroke.get("srv") is not None else None,
        "server_delay_ms": int(stroke["del"]) if stroke.get("del") is not None else None,
        "accuracy_diameter_m": float(stroke["dev"]) if stroke.get("dev") is not None else None,
        "detector_participations": detector_participations,
        "geohash5": geohash5(latitude, longitude),
        "geohash7": geohash7(latitude, longitude),
    }


@dataclass
class BridgeState:
    last_ids: dict[str, int]
    recent_keys: list[str]


class StateStore:
    def __init__(self, path: str, dedupe_size: int) -> None:
        self._path = Path(path)
        self._dedupe_size = dedupe_size

    def load(self) -> BridgeState:
        if not self._path.exists():
            return BridgeState(last_ids={}, recent_keys=[])
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Failed to load state file %s: %s", self._path, exc)
            return BridgeState(last_ids={}, recent_keys=[])
        last_ids = {str(key): int(value) for key, value in payload.get("last_ids", {}).items() if key is not None and value is not None}
        recent_keys = [str(item) for item in payload.get("recent_keys", []) if item]
        return BridgeState(last_ids=last_ids, recent_keys=recent_keys[-self._dedupe_size :])

    def save(self, state: BridgeState) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"last_ids": state.last_ids, "recent_keys": state.recent_keys[-self._dedupe_size :]}
        self._path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def iter_live_messages(urls: list[str], *, last_ids_provider, include_stations: bool, bbox: tuple[float, float, float, float], source_mask: int, user_agent: str, max_retry_delay: int, reason: str) -> Iterable[dict[str, Any]]:
    retry_delay = 1
    attempt = 0
    while True:
        url = urls[attempt % len(urls)]
        attempt += 1
        try:
            logger.info("Connecting to %s", url)
            with ws_client.connect(url, open_timeout=20, close_timeout=10, user_agent_header=user_agent) as connection:
                connection.send(build_request(last_ids_provider(), include_stations=include_stations, bbox=bbox, source_mask=source_mask, reason=reason))
                retry_delay = 1
                for raw in connection:
                    try:
                        yield json.loads(raw)
                    except json.JSONDecodeError as exc:
                        logger.debug("Skipping non-JSON websocket frame: %s", exc)
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            logger.warning("Websocket error from %s: %s. Reconnecting in %ds.", url, exc, retry_delay)
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, max_retry_delay)
