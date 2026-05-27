"""AISstream.io firehose -> MQTT/UNS bridge (pilot).

Subscribes to the public AISstream.io WebSocket, normalizes a curated
subset of AIS message types into three UNS event families, and
republishes each event as a non-retained QoS-0 MQTT 5 binary-mode
CloudEvent on the topic family

    maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/{msg_type}

The pilot covers three event families derived from upstream
``MessageType`` values:

* ``position-report`` (msg_type=position-report)
    - PositionReport (Type 1/2/3)
    - StandardClassBPositionReport (Type 18)
    - ExtendedClassBPositionReport (Type 19)
    - LongRangeAisBroadcastMessage (Type 27)
    - StandardSearchAndRescueAircraftReport (Type 9)
* ``static`` (msg_type=static)
    - ShipStaticData (Type 5)
    - StaticDataReport (Type 24)
* ``aid-to-navigation`` (msg_type=aid-to-navigation)
    - AidsToNavigationReport (Type 21)

Per the xRegistry keying instructions, every UNS topic placeholder is a
real field on the published dataclass: ``mmsi`` and ``geohash5`` are
the stable identity axes, ``flag`` is derived from the MMSI's MID via
the ITU registry shipped at :mod:`aisstream_mqtt.enrichment`, and
``ship_type`` is derived from the ITU-R M.1371 ShipType code (with an
in-process cache so position reports inherit the bucket published by
the most recent ShipStatic record for the same MMSI).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, Iterable, Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from aisstream_mqtt_producer_data import (
    AidToNavigation,
    PositionReport,
    ShipStatic,
)
from aisstream_mqtt_producer_mqtt_client.client import IOAISstreamMqttMqttClient

from aisstream_mqtt.enrichment import (
    MID_ISO_VERSION,
    geohash5,
    mid_to_iso,
    ship_type_bucket,
)

logger = logging.getLogger("aisstream_mqtt")


POSITION_REPORT_TYPES = {
    "PositionReport",
    "StandardClassBPositionReport",
    "ExtendedClassBPositionReport",
    "LongRangeAisBroadcastMessage",
    "StandardSearchAndRescueAircraftReport",
}
STATIC_TYPES = {"ShipStaticData", "StaticDataReport"}
AID_TO_NAVIGATION_TYPES = {"AidsToNavigationReport"}


def _mmsi9(value: Any) -> Optional[str]:
    if value is None:
        return None
    try:
        n = int(value)
    except (TypeError, ValueError):
        return None
    if n <= 0:
        return None
    return f"{n:09d}"


def _norm_segment(value: Any) -> str:
    if not value:
        return ""
    return str(value).strip().lower().replace("/", "_")


class ShipTypeCache:
    """In-process LRU-ish cache of MMSI -> ship-type bucket."""

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
            # Drop ~10% oldest entries. Cheap, FIFO-ish.
            cut = self._max // 10
            for k in list(self._data.keys())[:cut]:
                self._data.pop(k, None)


class PositionCache:
    """In-process cache of MMSI -> (lat, lon) for static-report enrichment."""

    def __init__(self, max_size: int = 200_000) -> None:
        self._max = max_size
        self._data: Dict[str, tuple[float, float]] = {}

    def get(self, mmsi: str) -> Optional[tuple[float, float]]:
        return self._data.get(mmsi)

    def set(self, mmsi: str, lat: float, lon: float) -> None:
        self._data[mmsi] = (lat, lon)
        if len(self._data) > self._max:
            cut = self._max // 10
            for k in list(self._data.keys())[:cut]:
                self._data.pop(k, None)


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


def _build_position(envelope: Dict[str, Any], payload: Dict[str, Any], meta: Dict[str, Any],
                    flag: str, ship_type: str) -> Optional[PositionReport]:
    user_id = payload.get("UserID") or meta.get("MMSI")
    mmsi = _mmsi9(user_id)
    if mmsi is None:
        return None
    lat = payload.get("Latitude")
    lon = payload.get("Longitude")
    if lat is None or lon is None:
        return None
    gh = geohash5(lat, lon)
    return PositionReport(
        mmsi=mmsi,
        flag=flag,
        ship_type=ship_type,
        geohash5=gh,
        msg_type="position-report",
        user_id=int(user_id) if user_id is not None else 0,
        latitude=float(lat),
        longitude=float(lon),
        sog=float(payload.get("Sog") or 0.0),
        cog=float(payload.get("Cog") or 0.0),
        true_heading=int(payload.get("TrueHeading") or 0),
        navigational_status=int(payload.get("NavigationalStatus") or 0),
        rate_of_turn=int(payload.get("RateOfTurn") or 0),
        position_accuracy=bool(payload.get("PositionAccuracy") or False),
        timestamp=int(payload.get("Timestamp") or 0),
        raim=bool(payload.get("Raim") or False),
        message_id=int(payload.get("MessageID") or 0),
    )


def _build_static(envelope: Dict[str, Any], payload: Dict[str, Any], meta: Dict[str, Any],
                  flag: str, ship_type: str, gh: str) -> Optional[ShipStatic]:
    user_id = payload.get("UserID") or meta.get("MMSI")
    mmsi = _mmsi9(user_id)
    if mmsi is None:
        return None
    eta_parts = payload.get("Eta") or {}
    eta_str = ""
    if isinstance(eta_parts, dict) and eta_parts:
        try:
            eta_str = (
                f"{int(eta_parts.get('Month') or 0):02d}-"
                f"{int(eta_parts.get('Day') or 0):02d}T"
                f"{int(eta_parts.get('Hour') or 0):02d}:"
                f"{int(eta_parts.get('Minute') or 0):02d}:00Z"
            )
        except (TypeError, ValueError):
            eta_str = ""
    dims = payload.get("Dimension") or {}
    name = (payload.get("Name") or payload.get("ShipName") or "").strip().strip("@")
    return ShipStatic(
        mmsi=mmsi,
        flag=flag,
        ship_type=ship_type,
        geohash5=gh,
        msg_type="static",
        user_id=int(user_id) if user_id is not None else 0,
        name=name,
        call_sign=(payload.get("CallSign") or "").strip().strip("@"),
        imo_number=int(payload.get("ImoNumber") or 0),
        ship_type_code=int(payload.get("Type") or payload.get("ShipType") or 0),
        destination=(payload.get("Destination") or "").strip().strip("@"),
        eta=eta_str,
        draught=float(payload.get("MaximumStaticDraught") or 0.0),
        dim_to_bow=int(dims.get("A") or 0),
        dim_to_stern=int(dims.get("B") or 0),
        dim_to_port=int(dims.get("C") or 0),
        dim_to_starboard=int(dims.get("D") or 0),
        message_id=int(payload.get("MessageID") or 0),
    )


def _build_aton(envelope: Dict[str, Any], payload: Dict[str, Any], meta: Dict[str, Any],
                flag: str, ship_type: str) -> Optional[AidToNavigation]:
    user_id = payload.get("UserID") or meta.get("MMSI")
    mmsi = _mmsi9(user_id)
    if mmsi is None:
        return None
    lat = payload.get("Latitude")
    lon = payload.get("Longitude")
    if lat is None or lon is None:
        return None
    return AidToNavigation(
        mmsi=mmsi,
        flag=flag,
        ship_type=ship_type,
        geohash5=geohash5(lat, lon),
        msg_type="aid-to-navigation",
        user_id=int(user_id) if user_id is not None else 0,
        name=(payload.get("Name") or "").strip().strip("@"),
        type=int(payload.get("Type") or 0),
        latitude=float(lat),
        longitude=float(lon),
        off_position=bool(payload.get("OffPosition") or False),
        virtual_atoN=bool(payload.get("VirtualAtoN") or False),
        message_id=int(payload.get("MessageID") or 21),
    )


# ---------------------------------------------------------------------------
# Bridge
# ---------------------------------------------------------------------------


class AisStreamMqttBridge:
    DEFAULT_WS_URL = "wss://stream.aisstream.io/v0/stream"
    DEFAULT_SOURCE_URI = DEFAULT_WS_URL

    def __init__(
        self,
        client: IOAISstreamMqttMqttClient,
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
            raise RuntimeError("AISSTREAM_API_KEY is required for live streaming. "
                               "Use --mock for tests.")
        # Lazy import; websockets pulls in asyncio bits we only need at run.
        import websockets

        subscription = json.dumps({
            "APIKey": self.api_key,
            "BoundingBoxes": self.bounding_boxes,
        })

        retry_delay = 1
        max_retry_delay = 60
        while True:
            try:
                async with websockets.connect(self.ws_url, max_size=2 ** 22) as ws:
                    await ws.send(subscription)
                    logger.info("Connected to AISstream WS at %s", self.ws_url)
                    retry_delay = 1
                    async for raw in ws:
                        try:
                            envelope = json.loads(raw)
                        except (TypeError, ValueError):
                            continue
                        await self._dispatch_envelope(envelope)
                        self._count += 1
                        if max_events and self._count >= max_events:
                            logger.info("max_events=%d reached, exiting", max_events)
                            return
            except (asyncio.CancelledError, KeyboardInterrupt):
                raise
            except Exception as exc:
                logger.error("AISstream connection error: %s. Retrying in %ds", exc, retry_delay)
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, max_retry_delay)

    async def _dispatch_envelope(self, envelope: Dict[str, Any]) -> None:
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
            gh = geohash5(*cached_pos) if cached_pos else "00000"
            data = _build_static(envelope, payload, meta, flag, bucket, gh)
            if data is not None:
                await self.client.publish_io_aisstream_mqtt_ship_static(
                    mmsi=data.mmsi, flag=data.flag, ship_type=data.ship_type,
                    geohash5=data.geohash5, data=data, qos=0, retain=False,
                )
        elif message_type in POSITION_REPORT_TYPES:
            bucket = self.ship_type_cache.get(mmsi)
            data = _build_position(envelope, payload, meta, flag, bucket)
            if data is not None:
                self.position_cache.set(mmsi, data.latitude, data.longitude)
                await self.client.publish_io_aisstream_mqtt_position_report(
                    mmsi=data.mmsi, flag=data.flag, ship_type=data.ship_type,
                    geohash5=data.geohash5, data=data, qos=0, retain=False,
                )
        elif message_type in AID_TO_NAVIGATION_TYPES:
            data = _build_aton(envelope, payload, meta, flag, "aton")
            if data is not None:
                await self.client.publish_io_aisstream_mqtt_aid_to_navigation(
                    mmsi=data.mmsi, flag=data.flag, ship_type=data.ship_type,
                    geohash5=data.geohash5, data=data, qos=0, retain=False,
                )

    async def emit_mock_corpus(self) -> None:
        """Publish one synthetic message per family for Docker E2E."""
        static_envelope = {
            "MessageType": "ShipStaticData",
            "MetaData": {"MMSI": 211_555_001},
            "Message": {"ShipStaticData": {
                "UserID": 211_555_001,
                "Name": "MOCK CARGO       @@@@",
                "CallSign": "DXXX@",
                "ImoNumber": 9_111_222,
                "Type": 70,
                "Destination": "DEHAM@@@@@@@@@@@@@@@",
                "Eta": {"Month": 5, "Day": 23, "Hour": 12, "Minute": 0},
                "MaximumStaticDraught": 8.5,
                "Dimension": {"A": 100, "B": 50, "C": 10, "D": 22},
                "MessageID": 5,
            }},
        }
        await self._dispatch_envelope(static_envelope)

        pos_envelope = {
            "MessageType": "PositionReport",
            "MetaData": {"MMSI": 211_555_001},
            "Message": {"PositionReport": {
                "UserID": 211_555_001,
                "Latitude": 53.5511,
                "Longitude": 9.9937,
                "Sog": 12.3,
                "Cog": 095.1,
                "TrueHeading": 95,
                "NavigationalStatus": 0,
                "RateOfTurn": 0,
                "PositionAccuracy": True,
                "Timestamp": 30,
                "Raim": False,
                "MessageID": 1,
            }},
        }
        await self._dispatch_envelope(pos_envelope)

        aton_envelope = {
            "MessageType": "AidsToNavigationReport",
            "MetaData": {"MMSI": 992_111_001},
            "Message": {"AidsToNavigationReport": {
                "UserID": 992_111_001,
                "Name": "ELBE BUOY 7         ",
                "Type": 1,
                "Latitude": 53.8800,
                "Longitude": 8.7100,
                "OffPosition": False,
                "VirtualAtoN": False,
                "MessageID": 21,
            }},
        }
        await self._dispatch_envelope(aton_envelope)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_broker(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    host = parsed.hostname or "localhost"
    port = parsed.port or (8883 if scheme == "mqtts" else 1883)
    return host, port, scheme == "mqtts"


async def _run(args: argparse.Namespace) -> None:
    broker_host, broker_port, tls = _parse_broker(args.mqtt_broker_url)
    tls = tls or args.mqtt_enable_tls

    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=args.mqtt_client_id or "",
        protocol=MQTTv5,
    )
    if args.mqtt_username:
        paho_client.username_pw_set(args.mqtt_username, args.mqtt_password or "")
    if tls:
        paho_client.tls_set()

    loop = asyncio.get_running_loop()
    client = IOAISstreamMqttMqttClient(
        client=paho_client,
        content_mode="binary",
        loop=loop,
    )
    logger.info("Connecting to MQTT broker %s:%s (tls=%s); mid_iso_version=%s",
                broker_host, broker_port, tls, MID_ISO_VERSION)
    await client.connect(broker_host, broker_port)

    bridge = AisStreamMqttBridge(
        client,
        api_key=args.api_key,
        ws_url=args.ws_url,
    )
    if args.mock:
        logger.info("Mock mode: emitting synthetic AIS corpus and exiting")
        await bridge.emit_mock_corpus()
        await asyncio.sleep(1.0)
        await client.disconnect()
        return
    await bridge.run(max_events=args.max_events)


def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    p = argparse.ArgumentParser(description="AISstream -> MQTT/UNS bridge")
    sub = p.add_subparsers(dest="command")

    feed = sub.add_parser("feed", help="Stream AIS to MQTT")
    feed.add_argument("--mqtt-broker-url",
                      default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed.add_argument("--mqtt-enable-tls", action="store_true",
                      default=os.getenv("MQTT_ENABLE_TLS", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed.add_argument("--api-key", default=os.getenv("AISSTREAM_API_KEY"),
                      help="AISstream.io API key (required unless --mock).")
    feed.add_argument("--ws-url",
                      default=os.getenv("AISSTREAM_WS_URL",
                                        AisStreamMqttBridge.DEFAULT_WS_URL))
    feed.add_argument("--max-events", type=int,
                      default=int(os.getenv("AISSTREAM_MAX_EVENTS", "0")) or None)
    feed.add_argument("--mock", action="store_true",
                      default=os.getenv("AISSTREAM_MOCK", "false").lower() in ("true", "1", "yes"),
                      help="Skip live WS, emit one synthetic event per family, then exit")

    args = p.parse_args()
    if args.command != "feed":
        p.print_help()
        sys.exit(1)

    try:
        asyncio.run(_run(args))
    except KeyboardInterrupt:
        logger.info("Shutting down")


if __name__ == "__main__":
    main()
