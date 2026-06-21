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
import inspect
import json
import logging
import os
import sys
from typing import Any, Dict, Iterable, Optional
from urllib.parse import urlparse

from aisstream_amqp_producer_data import (
    AidToNavigation,
    PositionReport,
    ShipStatic,
)
from aisstream_amqp_producer_amqp_producer.producer import IOAISstreamAmqpProducer

from .enrichment import (
    MID_ISO_VERSION,
    geohash5,
    mid_to_iso,
    ship_type_bucket,
)

logger = logging.getLogger("aisstream_mqtt")


# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-aisstream/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

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
        client: AisStreamAmqpClient,
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



import argparse
import logging
import os
from typing import Optional
from urllib.parse import urlparse

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"


def _parse_amqp_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    return parsed.hostname or "localhost", port, tls, parsed.username or None, parsed.password or None, (parsed.path or "").lstrip("/") or None


def _build_amqp_producer(producer_cls, *, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username: Optional[str], password: Optional[str], entra_audience: str, entra_client_id: Optional[str], sas_key_name: Optional[str], sas_key: Optional[str]):
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return producer_cls(host=host, address=address, port=port, content_mode=content_mode, credential=credential, entra_audience=entra_audience, use_tls=use_tls)
    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return producer_cls(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)
    return producer_cls(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=use_tls)


def add_amqp_arguments(parser: argparse.ArgumentParser, default_address: str) -> None:
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", default_address))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))


def create_amqp_producer(args: argparse.Namespace, producer_cls):
    address = args.address
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_amqp_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        if path:
            address = path
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    if not address:
        raise RuntimeError("AMQP address is required")
    logging.info("Connecting AMQP producer to %s:%s/%s auth=%s tls=%s", host, port, address, args.auth_mode, tls)
    return _build_amqp_producer(producer_cls, host=host, port=port, address=address, use_tls=tls, content_mode=args.content_mode, auth_mode=args.auth_mode, username=username, password=password, entra_audience=args.entra_audience, entra_client_id=args.entra_client_id, sas_key_name=args.sas_key_name, sas_key=args.sas_key)


class AisStreamAmqpClient:
    def __init__(self, producer: IOAISstreamAmqpProducer):
        self.producer = producer

    async def publish_io_aisstream_mqtt_position_report(self, *, mmsi, flag, ship_type, geohash5, data, **_):
        self.producer.send_position_report(data=data, _mmsi=mmsi, _flag=flag, _ship_type=ship_type, _geohash5=geohash5)

    async def publish_io_aisstream_mqtt_ship_static(self, *, mmsi, flag, ship_type, geohash5, data, **_):
        self.producer.send_ship_static(data=data, _mmsi=mmsi, _flag=flag, _ship_type=ship_type, _geohash5=geohash5)

    async def publish_io_aisstream_mqtt_aid_to_navigation(self, *, mmsi, flag, ship_type, geohash5, data, **_):
        self.producer.send_aid_to_navigation(data=data, _mmsi=mmsi, _flag=flag, _ship_type=ship_type, _geohash5=geohash5)


async def _run(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args, IOAISstreamAmqpProducer)
    client = AisStreamAmqpClient(producer)
    bridge = AisStreamMqttBridge(client, api_key=args.api_key, ws_url=args.ws_url)
    try:
        if args.mock:
            logger.info("Mock mode: emitting synthetic AISstream corpus to AMQP and exiting")
            await bridge.emit_mock_corpus()
            return
        await bridge.run(max_events=args.max_events)
    finally:
        producer.close()


def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            import time; time.sleep(delay)
def main() -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(description="AISstream -> AMQP 1.0 bridge")
    sub = p.add_subparsers(dest="command")
    feed = sub.add_parser("feed")
    add_amqp_arguments(feed, "aisstream")
    feed.add_argument("--api-key", default=os.getenv("AISSTREAM_API_KEY"))
    feed.add_argument("--ws-url", default=os.getenv("AISSTREAM_WS_URL", AisStreamMqttBridge.DEFAULT_WS_URL))
    feed.add_argument("--max-events", type=int, default=int(os.getenv("AISSTREAM_MAX_EVENTS", "0")) or None)
    feed.add_argument("--mock", action="store_true", default=os.getenv("AISSTREAM_MOCK", "").lower() in ("1","true","yes"))
    args = p.parse_args()
    if args.command != "feed":
        p.print_help(); sys.exit(1)
    asyncio.run(_run(args))

if __name__ == "__main__":
    main()
