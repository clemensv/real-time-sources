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

# Single source of truth: every upstream AISstream MessageType paired with the
# snake_case method suffix the generators derive from it. The generated data
# class name equals the MessageType string for all 23 types, so a transport's
# dispatch table is `{mt: (getattr(producer_data, mt), <prefix> + suffix)}`.
# Kafka uses `send_io_aisstream_<suffix>`, AMQP uses `send_<suffix>`, and MQTT
# uses `publish_io_aisstream_mqtt_<suffix>`.
AIS_MESSAGE_TYPES: List[tuple[str, str]] = [
    ("PositionReport", "position_report"),
    ("ShipStaticData", "ship_static_data"),
    ("StandardClassBPositionReport", "standard_class_bposition_report"),
    ("ExtendedClassBPositionReport", "extended_class_bposition_report"),
    ("AidsToNavigationReport", "aids_to_navigation_report"),
    ("StaticDataReport", "static_data_report"),
    ("BaseStationReport", "base_station_report"),
    ("SafetyBroadcastMessage", "safety_broadcast_message"),
    ("StandardSearchAndRescueAircraftReport", "standard_search_and_rescue_aircraft_report"),
    ("LongRangeAisBroadcastMessage", "long_range_ais_broadcast_message"),
    ("AddressedSafetyMessage", "addressed_safety_message"),
    ("AddressedBinaryMessage", "addressed_binary_message"),
    ("AssignedModeCommand", "assigned_mode_command"),
    ("BinaryAcknowledge", "binary_acknowledge"),
    ("BinaryBroadcastMessage", "binary_broadcast_message"),
    ("ChannelManagement", "channel_management"),
    ("CoordinatedUTCInquiry", "coordinated_utcinquiry"),
    ("DataLinkManagementMessage", "data_link_management_message"),
    ("GnssBroadcastBinaryMessage", "gnss_broadcast_binary_message"),
    ("GroupAssignmentCommand", "group_assignment_command"),
    ("Interrogation", "interrogation"),
    ("MultiSlotBinaryMessage", "multi_slot_binary_message"),
    ("SingleSlotBinaryMessage", "single_slot_binary_message"),
]


def extract_ship_type_code(payload: Dict[str, Any]) -> Any:
    """Return the AIS ship-type code used for the MQTT ``ship_type`` topic level.

    Type 5 (``ShipStaticData``) carries the code at the top level under ``Type``.
    Type 24 (``StaticDataReport``) Part B nests it under ``ReportB.ShipType`` —
    reading only the top level silently mislabels every Class-B vessel as
    ``unknown``. Check the nested Part-B report as a fallback.
    """
    code = payload.get("Type") or payload.get("ShipType")
    if code:
        return code
    report_b = payload.get("ReportB")
    if isinstance(report_b, dict):
        return report_b.get("ShipType") or report_b.get("Type") or 0
    return 0


def mock_envelopes() -> List[Dict[str, Any]]:
    """A small synthetic AISstream corpus (raw upstream envelope shape).

    Mirrors the Kafka bridge's mock corpus so all three transports exercise the
    same static / position / aid-to-navigation paths in ``--mock`` runs.
    """
    return [
        {
            "MessageType": "ShipStaticData",
            "MetaData": {"MMSI": 211_555_001},
            "Message": {
                "ShipStaticData": {
                    "MessageID": 5, "RepeatIndicator": 0, "UserID": 211_555_001,
                    "Valid": True, "AisVersion": 1, "ImoNumber": 9_111_222,
                    "CallSign": "DXXX@", "Name": "MOCK CARGO       @@@@",
                    "Type": 70,
                    "Dimension": {"A": 100, "B": 50, "C": 10, "D": 22},
                    "FixType": 1,
                    "Eta": {"Month": 5, "Day": 23, "Hour": 12, "Minute": 0},
                    "MaximumStaticDraught": 8.5, "Destination": "DEHAM@@@@@@@@@@@@@@@",
                    "Dte": False, "Spare": False,
                }
            },
        },
        {
            "MessageType": "PositionReport",
            "MetaData": {"MMSI": 211_555_001},
            "Message": {
                "PositionReport": {
                    "MessageID": 1, "RepeatIndicator": 0, "UserID": 211_555_001,
                    "Valid": True, "NavigationalStatus": 0, "RateOfTurn": 0,
                    "Sog": 12.3, "PositionAccuracy": True,
                    "Longitude": 9.9937, "Latitude": 53.5511,
                    "Cog": 95.1, "TrueHeading": 95, "Timestamp": 30,
                    "SpecialManoeuvreIndicator": 0, "Spare": 0,
                    "Raim": False, "CommunicationState": 0,
                }
            },
        },
        {
            "MessageType": "AidsToNavigationReport",
            "MetaData": {"MMSI": 992_111_001},
            "Message": {
                "AidsToNavigationReport": {
                    "MessageID": 21, "RepeatIndicator": 0, "UserID": 992_111_001,
                    "Valid": True, "Type": 1, "Name": "ELBE BUOY 7",
                    "PositionAccuracy": True, "Longitude": 8.71, "Latitude": 53.88,
                    "Dimension": {"A": 2, "B": 2, "C": 1, "D": 1},
                    "Fixtype": 1, "Timestamp": 20, "OffPosition": False,
                    "AtoN": 0, "Raim": False, "VirtualAtoN": False,
                    "AssignedMode": False, "Spare": False, "NameExtension": "",
                }
            },
        },
    ]


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

    def _enrich(self, message_type: str, payload: Dict[str, Any], meta: Dict[str, Any]):
        """Derive the MQTT topic-routing tuple for any of the 23 AIS types.

        Returns ``(user_id, mmsi, flag, ship_type, geohash5)`` or ``None`` when
        the message carries no usable MMSI (cannot be keyed or routed). The
        ``ship_type`` and position caches are refreshed from static and
        positioned messages so that types lacking those fields inherit the most
        recent value for the same vessel.
        """
        user_id = payload.get("UserID") or meta.get("MMSI")
        mmsi = _mmsi9(user_id)
        if mmsi is None:
            return None
        flag = mid_to_iso(int(mmsi))

        if message_type in STATIC_TYPES:
            bucket = ship_type_bucket(extract_ship_type_code(payload))
            self.ship_type_cache.set(mmsi, bucket)
            ship_type = bucket if bucket != "unknown" else self.ship_type_cache.get(mmsi)
        elif message_type in AID_TO_NAVIGATION_TYPES:
            ship_type = "aton"
        else:
            ship_type = self.ship_type_cache.get(mmsi)

        lat = payload.get("Latitude")
        lon = payload.get("Longitude")
        geohash = "00000"
        if lat is not None and lon is not None:
            try:
                latf, lonf = float(lat), float(lon)
                self.position_cache.set(mmsi, latf, lonf)
                geohash = geohash5(latf, lonf)
            except (TypeError, ValueError):
                geohash = "00000"
        else:
            cached = self.position_cache.get(mmsi)
            if cached:
                geohash = geohash5(*cached)
        return user_id, mmsi, flag, ship_type, geohash

    async def handle_envelope(self, envelope: Dict[str, Any]) -> None:
        """Dispatch one raw AISstream envelope to the transport client.

        The full upstream payload is forwarded unchanged; the bridge only
        computes the enrichment tuple the MQTT topic template needs. AMQP and
        Kafka clients ignore everything but ``user_id``.
        """
        message_type = envelope.get("MessageType")
        meta = envelope.get("MetaData") or {}
        message = envelope.get("Message") or {}
        payload = next(iter(message.values()), {}) if isinstance(message, dict) else {}
        if not message_type or not isinstance(payload, dict):
            return
        enriched = self._enrich(message_type, payload, meta)
        if enriched is None:
            return
        user_id, mmsi, flag, ship_type, geohash = enriched
        await self.client.emit(
            message_type,
            payload,
            user_id=user_id,
            mmsi=mmsi,
            flag=flag,
            ship_type=ship_type,
            geohash5=geohash,
        )
