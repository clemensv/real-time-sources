"""Transport-neutral acquisition and normalization for AISstream feeders."""

from __future__ import annotations

import csv
import json
import logging
import os
import pathlib
from functools import lru_cache
from typing import Any, Callable, Dict, Iterable, List, Optional

import websockets.sync.client as ws_client

logger = logging.getLogger(__name__)

AISSTREAM_WS_URL = "wss://stream.aisstream.io/v0/stream"
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-aisstream/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com")
    + ")"
)
MID_ISO_VERSION = "2024-01"
_THIS_DIR = pathlib.Path(__file__).resolve().parent
_MID_CSV = _THIS_DIR / "mid_iso.csv"
_GEOHASH_ALPHABET = "0123456789bcdefghjkmnpqrstuvwxyz"

POSITION_REPORT_TYPES = {
    "PositionReport",
    "StandardClassBPositionReport",
    "ExtendedClassBPositionReport",
    "LongRangeAisBroadcastMessage",
    "StandardSearchAndRescueAircraftReport",
}
STATIC_TYPES = {"ShipStaticData", "StaticDataReport"}
AID_TO_NAVIGATION_TYPES = {"AidsToNavigationReport"}


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


def mid_to_iso(mmsi: Any) -> str:
    if mmsi is None:
        return "xx"
    value = str(mmsi).strip()
    if not value.isdigit() or len(value) < 9:
        return "xx"
    return _load_mid_table().get(value[:3], "xx")


def geohash5(latitude: Optional[float], longitude: Optional[float]) -> str:
    if latitude is None or longitude is None:
        return "00000"
    try:
        lat = float(latitude)
        lon = float(longitude)
    except (TypeError, ValueError):
        return "00000"
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        return "00000"
    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    bits: list[int] = []
    even = True
    while len(bits) < 25:
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
    for index in range(0, len(bits), 5):
        value = (bits[index] << 4) | (bits[index + 1] << 3) | (bits[index + 2] << 2) | (bits[index + 3] << 1) | bits[index + 4]
        out.append(_GEOHASH_ALPHABET[value])
    return "".join(out)


def ship_type_bucket(code: Any) -> str:
    try:
        value = int(code)
    except (TypeError, ValueError):
        return "unknown"
    if value == 0:
        return "unknown"
    if value in (30,):
        return "fishing"
    if value in (31, 32):
        return "tug"
    if value == 33:
        return "dredger"
    if value == 34:
        return "diving"
    if value == 35:
        return "military"
    if value == 36:
        return "sailing"
    if value == 37:
        return "pleasure-craft"
    if value == 51:
        return "search-and-rescue"
    if value in (50, 52, 53, 54, 55, 58, 59):
        return "service"
    if 40 <= value <= 49:
        return "high-speed-craft"
    if 60 <= value <= 69:
        return "passenger"
    if 70 <= value <= 79:
        return "cargo"
    if 80 <= value <= 89:
        return "tanker"
    if 90 <= value <= 99:
        return "other"
    return "unknown"


def _mmsi9(value: Any) -> Optional[str]:
    if value is None:
        return None
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    if number <= 0:
        return None
    return f"{number:09d}"


class ShipTypeCache:
    def __init__(self, max_size: int = 200_000) -> None:
        self._max = max_size
        self._data: Dict[str, str] = {}

    def get(self, mmsi: str) -> str:
        return self._data.get(mmsi, "unknown")

    def set(self, mmsi: str, bucket: str) -> None:
        if bucket == "unknown":
            return
        self._data[mmsi] = bucket
        if len(self._data) > self._max:
            cut = self._max // 10
            for key in list(self._data.keys())[:cut]:
                self._data.pop(key, None)


class PositionCache:
    def __init__(self, max_size: int = 200_000) -> None:
        self._max = max_size
        self._data: Dict[str, tuple[float, float]] = {}

    def get(self, mmsi: str) -> Optional[tuple[float, float]]:
        return self._data.get(mmsi)

    def set(self, mmsi: str, lat: float, lon: float) -> None:
        self._data[mmsi] = (lat, lon)
        if len(self._data) > self._max:
            cut = self._max // 10
            for key in list(self._data.keys())[:cut]:
                self._data.pop(key, None)


class WebSocketSource:
    def __init__(
        self,
        api_key: str,
        bounding_boxes: Optional[List[List[List[float]]]] = None,
        mmsi_filter: Optional[List[str]] = None,
        message_type_filter: Optional[List[str]] = None,
        url: str = AISSTREAM_WS_URL,
        max_retry_delay: int = 60,
    ) -> None:
        self.api_key = api_key
        self.bounding_boxes = bounding_boxes or [[[-90, -180], [90, 180]]]
        self.mmsi_filter = mmsi_filter
        self.message_type_filter = message_type_filter
        self.url = url
        self.max_retry_delay = max_retry_delay

    def _build_subscription(self) -> str:
        subscription: Dict[str, Any] = {
            "APIKey": self.api_key,
            "BoundingBoxes": self.bounding_boxes,
        }
        if self.mmsi_filter:
            subscription["FiltersShipMMSI"] = self.mmsi_filter
        if self.message_type_filter:
            subscription["FilterMessageTypes"] = self.message_type_filter
        return json.dumps(subscription)

    def stream(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        retry_delay = 1
        subscription = self._build_subscription()
        while True:
            try:
                logger.info("Connecting to %s ...", self.url)
                conn = ws_client.connect(
                    self.url,
                    additional_headers={"User-Agent": USER_AGENT},
                    open_timeout=30,
                    close_timeout=10,
                )
                with conn:
                    logger.info("Connected — sending subscription")
                    conn.send(subscription)
                    retry_delay = 1
                    for raw in conn:
                        try:
                            message = json.loads(raw)
                        except json.JSONDecodeError as exc:
                            logger.debug("Invalid JSON from stream: %s", exc)
                            continue
                        if "error" in message:
                            raise ConnectionError(f"AISstream error: {message['error']}")
                        callback(message)
            except KeyboardInterrupt:
                logger.info("Interrupted — closing connection.")
                break
            except Exception as exc:
                logger.warning("Connection error: %s. Reconnecting in %ds...", exc, retry_delay)
                import time

                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, self.max_retry_delay)


def parse_bounding_boxes(bbox_str: str) -> list[list[list[float]]]:
    boxes = []
    for box_str in bbox_str.split(";"):
        parts = [float(value.strip()) for value in box_str.split(",")]
        if len(parts) != 4:
            raise ValueError(f"Bounding box must have 4 values (lat1,lon1,lat2,lon2), got {len(parts)}")
        boxes.append([[parts[0], parts[1]], [parts[2], parts[3]]])
    return boxes


class AisStreamBridge:
    DEFAULT_WS_URL = AISSTREAM_WS_URL

    def __init__(
        self,
        client,
        *,
        api_key: Optional[str] = None,
        ws_url: str = DEFAULT_WS_URL,
        bounding_boxes: Optional[Iterable] = None,
    ) -> None:
        self.client = client
        self.api_key = api_key
        self.ws_url = ws_url
        self.bounding_boxes = list(bounding_boxes) if bounding_boxes else [[[-90, -180], [90, 180]]]
        self.ship_type_cache = ShipTypeCache()
        self.position_cache = PositionCache()
        self._count = 0

    async def run(self, max_events: Optional[int] = None) -> None:
        if not self.api_key:
            raise RuntimeError("AISSTREAM_API_KEY is required for live streaming.")
        import asyncio
        import websockets

        subscription = json.dumps({
            "APIKey": self.api_key,
            "BoundingBoxes": self.bounding_boxes,
        })
        retry_delay = 1
        while True:
            try:
                async with websockets.connect(
                    self.ws_url,
                    additional_headers={"User-Agent": USER_AGENT},
                    max_size=2 ** 22,
                ) as ws:
                    await ws.send(subscription)
                    logger.info("Connected to AISstream WS at %s", self.ws_url)
                    retry_delay = 1
                    async for raw in ws:
                        try:
                            envelope = json.loads(raw)
                        except (TypeError, ValueError):
                            continue
                        await self.handle_envelope(envelope)
                        self._count += 1
                        if max_events and self._count >= max_events:
                            logger.info("max_events=%d reached, exiting", max_events)
                            return
            except (asyncio.CancelledError, KeyboardInterrupt):
                raise
            except Exception as exc:
                logger.error("AISstream connection error: %s. Retrying in %ds", exc, retry_delay)
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60)

    async def handle_envelope(self, envelope: Dict[str, Any]) -> None:
        message_type = envelope.get("MessageType")
        meta = envelope.get("MetaData") or {}
        message = envelope.get("Message") or {}
        payload = next(iter(message.values()), {}) if isinstance(message, dict) else {}
        if not isinstance(payload, dict):
            return

        user_id = payload.get("UserID") or meta.get("MMSI")
        mmsi = _mmsi9(user_id)
        if mmsi is None:
            return
        flag = mid_to_iso(int(mmsi))

        if message_type in STATIC_TYPES:
            ship_type_code = payload.get("Type") or payload.get("ShipType") or 0
            bucket = ship_type_bucket(ship_type_code)
            self.ship_type_cache.set(mmsi, bucket)
            cached_pos = self.position_cache.get(mmsi)
            geohash = geohash5(*cached_pos) if cached_pos else "00000"
            eta_parts = payload.get("Eta") or {}
            eta = ""
            if isinstance(eta_parts, dict) and eta_parts:
                try:
                    eta = (
                        f"{int(eta_parts.get('Month') or 0):02d}-"
                        f"{int(eta_parts.get('Day') or 0):02d}T"
                        f"{int(eta_parts.get('Hour') or 0):02d}:"
                        f"{int(eta_parts.get('Minute') or 0):02d}:00Z"
                    )
                except (TypeError, ValueError):
                    eta = ""
            dims = payload.get("Dimension") or {}
            await self.client.publish_ship_static(
                mmsi=mmsi,
                flag=flag,
                ship_type=bucket,
                geohash5=geohash,
                payload={
                    "user_id": int(user_id) if user_id is not None else 0,
                    "name": (payload.get("Name") or payload.get("ShipName") or "").strip().strip("@"),
                    "call_sign": (payload.get("CallSign") or "").strip().strip("@"),
                    "imo_number": int(payload.get("ImoNumber") or 0),
                    "ship_type_code": int(payload.get("Type") or payload.get("ShipType") or 0),
                    "destination": (payload.get("Destination") or "").strip().strip("@"),
                    "eta": eta,
                    "draught": float(payload.get("MaximumStaticDraught") or 0.0),
                    "dim_to_bow": int(dims.get("A") or 0),
                    "dim_to_stern": int(dims.get("B") or 0),
                    "dim_to_port": int(dims.get("C") or 0),
                    "dim_to_starboard": int(dims.get("D") or 0),
                    "message_id": int(payload.get("MessageID") or 0),
                },
            )
            return

        if message_type in POSITION_REPORT_TYPES:
            lat = payload.get("Latitude")
            lon = payload.get("Longitude")
            if lat is None or lon is None:
                return
            bucket = self.ship_type_cache.get(mmsi)
            latitude = float(lat)
            longitude = float(lon)
            self.position_cache.set(mmsi, latitude, longitude)
            await self.client.publish_position_report(
                mmsi=mmsi,
                flag=flag,
                ship_type=bucket,
                geohash5=geohash5(latitude, longitude),
                payload={
                    "user_id": int(user_id) if user_id is not None else 0,
                    "latitude": latitude,
                    "longitude": longitude,
                    "sog": float(payload.get("Sog") or 0.0),
                    "cog": float(payload.get("Cog") or 0.0),
                    "true_heading": int(payload.get("TrueHeading") or 0),
                    "navigational_status": int(payload.get("NavigationalStatus") or 0),
                    "rate_of_turn": int(payload.get("RateOfTurn") or 0),
                    "position_accuracy": bool(payload.get("PositionAccuracy") or False),
                    "timestamp": int(payload.get("Timestamp") or 0),
                    "raim": bool(payload.get("Raim") or False),
                    "message_id": int(payload.get("MessageID") or 0),
                },
            )
            return

        if message_type in AID_TO_NAVIGATION_TYPES:
            lat = payload.get("Latitude")
            lon = payload.get("Longitude")
            if lat is None or lon is None:
                return
            await self.client.publish_aid_to_navigation(
                mmsi=mmsi,
                flag=flag,
                ship_type="aton",
                geohash5=geohash5(lat, lon),
                payload={
                    "user_id": int(user_id) if user_id is not None else 0,
                    "name": (payload.get("Name") or "").strip().strip("@"),
                    "type": int(payload.get("Type") or 0),
                    "latitude": float(lat),
                    "longitude": float(lon),
                    "off_position": bool(payload.get("OffPosition") or False),
                    "virtual_atoN": bool(payload.get("VirtualAtoN") or False),
                    "message_id": int(payload.get("MessageID") or 21),
                },
            )
