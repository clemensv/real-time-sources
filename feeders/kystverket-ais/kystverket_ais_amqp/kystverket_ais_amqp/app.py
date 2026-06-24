"""Kystverket AIS firehose -> MQTT/UNS bridge.

Connects to the Norwegian Coastal Administration's public AIS TCP NMEA
firehose, decodes the supported ITU-R M.1371 messages, normalizes them
into three UNS event families, and republishes each event as a
non-retained QoS-0 MQTT 5 binary-mode CloudEvent on the topic family

    maritime/no/kystverket/kystverket-ais/{flag}/{ship_type}/{geohash5}/{mmsi}/{msg_type}

Event families:

* ``position-report`` (msg_type=position-report)
    - PositionReportClassA (Type 1/2/3)
    - PositionReportClassB (Type 18/19)
* ``static`` (msg_type=static)
    - StaticVoyageData (Type 5)
    - StaticDataClassB (Type 24)
* ``aid-to-navigation`` (msg_type=aid-to-navigation)
    - AidToNavigation (Type 21)

Per the xRegistry keying instructions, every UNS topic placeholder is a
real field on the published dataclass: ``mmsi`` and ``geohash5`` are
the stable identity axes, ``flag`` is derived from the MMSI's MID via
the ITU registry shipped at :mod:`kystverket_ais_amqp.enrichment`, and
``ship_type`` is derived from the ITU-R M.1371 ShipType code (with an
in-process cache so position reports inherit the bucket published by
the most recent ShipStatic / StaticDataClassB record for the same
MMSI).
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from kystverket_ais_amqp_producer_data import (
    AidToNavigation,
    PositionReport,
    ShipStatic,
)
from kystverket_ais_amqp_producer_amqp_producer.producer import NOKystverketAISAmqpProducer

from kystverket_ais_core import NMEADecoder, DecodedAIS
from kystverket_ais_core import TCPSource, RawNMEASentence

from .enrichment import (
    MID_ISO_VERSION,
    geohash5,
    mid_to_iso,
    ship_type_bucket,
)

logger = logging.getLogger("kystverket_ais_amqp")


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


def _f(v, default=0.0):
    try:
        return float(v) if v is not None else default
    except (TypeError, ValueError):
        return default


def _i(v, default=0):
    try:
        return int(v) if v is not None else default
    except (TypeError, ValueError):
        return default


def _s(v) -> str:
    return "" if v is None else str(v).strip().strip("@")


def _build_position(fields: Dict[str, Any], decoded: DecodedAIS,
                    flag: str, ship_type: str) -> Optional[PositionReport]:
    mmsi = _mmsi9(fields.get("mmsi"))
    if mmsi is None:
        return None
    lat = fields.get("latitude")
    lon = fields.get("longitude")
    if lat is None or lon is None:
        return None
    return PositionReport(
        mmsi=mmsi,
        flag=flag,
        ship_type=ship_type,
        geohash5=geohash5(lat, lon),
        msg_type="position-report",
        latitude=_f(lat),
        longitude=_f(lon),
        speed_over_ground=_f(fields.get("speed_over_ground")),
        course_over_ground=_f(fields.get("course_over_ground")),
        true_heading=_i(fields.get("true_heading")),
        navigation_status=_i(fields.get("navigation_status")),
        rate_of_turn=_f(fields.get("rate_of_turn")),
        position_accuracy=_i(fields.get("position_accuracy")),
        timestamp=_s(fields.get("timestamp")),
        station_id=_s(fields.get("station_id")),
        ais_msg_type=int(decoded.msg_type),
    )


def _build_static(fields: Dict[str, Any], decoded: DecodedAIS,
                  flag: str, ship_type: str, gh: str,
                  ship_type_code: int) -> Optional[ShipStatic]:
    mmsi = _mmsi9(fields.get("mmsi"))
    if mmsi is None:
        return None
    eta_str = ""
    em = fields.get("eta_month")
    if em is not None and em != 0:
        try:
            eta_str = (
                f"{int(em):02d}-"
                f"{int(fields.get('eta_day') or 0):02d}T"
                f"{int(fields.get('eta_hour') or 0):02d}:"
                f"{int(fields.get('eta_minute') or 0):02d}:00Z"
            )
        except (TypeError, ValueError):
            eta_str = ""
    return ShipStatic(
        mmsi=mmsi,
        flag=flag,
        ship_type=ship_type,
        geohash5=gh,
        msg_type="static",
        ship_name=_s(fields.get("ship_name")),
        callsign=_s(fields.get("callsign")),
        imo_number=_i(fields.get("imo_number")),
        ship_type_code=ship_type_code,
        destination=_s(fields.get("destination")),
        eta=eta_str,
        draught=_f(fields.get("draught")),
        dim_to_bow=_i(fields.get("dimension_to_bow")),
        dim_to_stern=_i(fields.get("dimension_to_stern")),
        dim_to_port=_i(fields.get("dimension_to_port")),
        dim_to_starboard=_i(fields.get("dimension_to_starboard")),
        timestamp=_s(fields.get("timestamp")),
        station_id=_s(fields.get("station_id")),
        ais_msg_type=int(decoded.msg_type),
    )


def _build_aton(fields: Dict[str, Any], decoded: DecodedAIS,
                flag: str) -> Optional[AidToNavigation]:
    mmsi = _mmsi9(fields.get("mmsi"))
    if mmsi is None:
        return None
    lat = fields.get("latitude")
    lon = fields.get("longitude")
    if lat is None or lon is None:
        return None
    return AidToNavigation(
        mmsi=mmsi,
        flag=flag,
        ship_type="aton",
        geohash5=geohash5(lat, lon),
        msg_type="aid-to-navigation",
        name=_s(fields.get("name")),
        aid_type=_i(fields.get("aid_type")),
        latitude=_f(lat),
        longitude=_f(lon),
        position_accuracy=_i(fields.get("position_accuracy")),
        timestamp=_s(fields.get("timestamp")),
        station_id=_s(fields.get("station_id")),
        ais_msg_type=int(decoded.msg_type),
    )


class KystverketAisAmqpBridge:
    DEFAULT_TCP_HOST = "153.44.253.27"
    DEFAULT_TCP_PORT = 5631

    def __init__(
        self,
        client: KystverketAisAmqpClient,
        *,
        tcp_host: str = DEFAULT_TCP_HOST,
        tcp_port: int = DEFAULT_TCP_PORT,
    ) -> None:
        self.client = client
        self.tcp_host = tcp_host
        self.tcp_port = tcp_port
        self.ship_type_cache = ShipTypeCache()
        self.position_cache = PositionCache()
        self._count = 0
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    async def run(self, max_events: Optional[int] = None) -> None:
        """Stream TCP NMEA -> decode -> publish until cancelled."""
        self._loop = asyncio.get_running_loop()
        decoder = NMEADecoder()
        tcp = TCPSource(host=self.tcp_host, port=self.tcp_port)

        done = asyncio.Event()

        def on_sentence(sentence: RawNMEASentence) -> None:
            try:
                decoded = decoder.decode_sentence(
                    sentence.nmea, sentence.station_id, sentence.receive_time
                )
            except Exception as exc:
                logger.debug("decode error: %s", exc)
                return
            if decoded is None:
                return
            fut = asyncio.run_coroutine_threadsafe(
                self.dispatch(decoded), self._loop)  # type: ignore[arg-type]
            try:
                fut.result(timeout=5.0)
            except Exception as exc:
                logger.warning("publish failed for MMSI %s: %s", decoded.mmsi, exc)
            self._count += 1
            if max_events and self._count >= max_events:
                done.set()
                raise KeyboardInterrupt("max_events reached")

        # Run blocking TCP loop in a thread
        import threading
        t = threading.Thread(target=tcp.stream, args=(on_sentence,), daemon=True)
        t.start()
        try:
            await done.wait() if max_events else await asyncio.Event().wait()
        finally:
            pass

    async def dispatch(self, decoded: DecodedAIS) -> None:
        fields = decoded.fields
        mmsi9 = _mmsi9(fields.get("mmsi"))
        if mmsi9 is None:
            return
        flag = mid_to_iso(int(mmsi9))

        if decoded.event_type in ("static_voyage_data", "static_data_class_b"):
            ship_type_code = _i(fields.get("ship_type"))
            bucket = ship_type_bucket(ship_type_code)
            self.ship_type_cache.set(mmsi9, bucket)
            cached_pos = self.position_cache.get(mmsi9)
            gh = geohash5(*cached_pos) if cached_pos else "00000"
            data = _build_static(fields, decoded, flag, bucket, gh, ship_type_code)
            if data is not None:
                await self.client.publish_ship_static(
                    mmsi=data.mmsi, flag=data.flag, ship_type=data.ship_type,
                    geohash5=data.geohash5, data=data, qos=0, retain=False,
                )
        elif decoded.event_type in ("position_report_class_a", "position_report_class_b"):
            bucket = self.ship_type_cache.get(mmsi9)
            data = _build_position(fields, decoded, flag, bucket)
            if data is not None:
                self.position_cache.set(mmsi9, data.latitude, data.longitude)
                await self.client.publish_position_report(
                    mmsi=data.mmsi, flag=data.flag, ship_type=data.ship_type,
                    geohash5=data.geohash5, data=data, qos=0, retain=False,
                )
        elif decoded.event_type == "aid_to_navigation":
            data = _build_aton(fields, decoded, flag)
            if data is not None:
                await self.client.publish_aid_to_navigation(
                    mmsi=data.mmsi, flag=data.flag, ship_type=data.ship_type,
                    geohash5=data.geohash5, data=data, qos=0, retain=False,
                )



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


class KystverketAisAmqpClient:
    def __init__(self, producer: NOKystverketAISAmqpProducer):
        self.producer = producer

    async def publish_position_report(self, *, mmsi, flag, ship_type, geohash5, data, **_):
        self.producer.send_position_report(data=data, _mmsi=mmsi, _flag=flag, _ship_type=ship_type, _geohash5=geohash5)

    async def publish_ship_static(self, *, mmsi, flag, ship_type, geohash5, data, **_):
        self.producer.send_ship_static(data=data, _mmsi=mmsi, _flag=flag, _ship_type=ship_type, _geohash5=geohash5)

    async def publish_aid_to_navigation(self, *, mmsi, flag, ship_type, geohash5, data, **_):
        self.producer.send_aid_to_navigation(data=data, _mmsi=mmsi, _flag=flag, _ship_type=ship_type, _geohash5=geohash5)


async def _run(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args, NOKystverketAISAmqpProducer)
    client = KystverketAisAmqpClient(producer)
    bridge = KystverketAisAmqpBridge(client, tcp_host=args.tcp_host, tcp_port=args.tcp_port)
    try:
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
    p = argparse.ArgumentParser(description="Kystverket AIS -> AMQP 1.0 bridge")
    sub = p.add_subparsers(dest="command")
    feed = sub.add_parser("feed")
    add_amqp_arguments(feed, "kystverket-ais")
    feed.add_argument("--tcp-host", default=os.getenv("AIS_TCP_HOST", KystverketAisAmqpBridge.DEFAULT_TCP_HOST))
    feed.add_argument("--tcp-port", type=int, default=int(os.getenv("AIS_TCP_PORT", str(KystverketAisAmqpBridge.DEFAULT_TCP_PORT))))
    feed.add_argument("--max-events", type=int, default=int(os.getenv("KYSTVERKET_AIS_MAX_EVENTS", "0")) or None)
    args = p.parse_args()
    if args.command != "feed":
        p.print_help(); sys.exit(1)
    asyncio.run(_run(args))

if __name__ == "__main__":
    main()
