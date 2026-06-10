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
the ITU registry shipped at :mod:`kystverket_ais_mqtt.enrichment`, and
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
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from kystverket_ais_mqtt_producer_data import (
    AidToNavigation,
    PositionReport,
    ShipStatic,
)
from kystverket_ais_mqtt_producer_mqtt_client.client import NOKystverketAISMqttMqttClient

from kystverket_ais.nmea_decoder import NMEADecoder, DecodedAIS
from kystverket_ais.tcp_source import TCPSource, RawNMEASentence

from kystverket_ais_mqtt.enrichment import (
    MID_ISO_VERSION,
    geohash5,
    mid_to_iso,
    ship_type_bucket,
)
import json

def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
    params = {
        "api-version": "2018-02-01",
        "resource": audience or "https://eventgrid.azure.net/",
    }
    if managed_identity_client_id:
        params["client_id"] = managed_identity_client_id

    request = Request(
        "http://169.254.169.254/metadata/identity/oauth2/token?" + urlencode(params),
        headers={"Metadata": "true"},
    )
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    token = payload.get("accessToken") or payload.get("access_token")
    if not token:
        raise RuntimeError("IMDS token response did not contain an access token")
    return str(token)

def _resolve_mqtt_connection_settings(*, username=None, password=None, client_id=None, auth_mode=None):
    resolved_client_id = str(client_id or os.getenv("MQTT_CLIENT_ID") or "").strip()
    auth_mode = str(auth_mode or os.getenv("MQTT_AUTH_MODE", "password")).strip().lower() or "password"

    if auth_mode != "entra":
        return resolved_client_id, str(username or ""), str(password or "")

    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    resolved_username = resolved_client_id or str(username or "").strip()
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")

    resolved_password = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    return resolved_client_id, resolved_username, resolved_password

logger = logging.getLogger("kystverket_ais_mqtt")

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
    if em not in (None, 0):
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

class KystverketAisMqttBridge:
    DEFAULT_TCP_HOST = "153.44.253.27"
    DEFAULT_TCP_PORT = 5631

    def __init__(
        self,
        client: NOKystverketAISMqttMqttClient,
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
                self.dispatch(decoded), self._loop)
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
                await self.client.publish_no_kystverket_ais_mqtt_ship_static(
                    mmsi=data.mmsi, flag=data.flag, ship_type=data.ship_type,
                    geohash5=data.geohash5, data=data, qos=0, retain=False,
                )
        elif decoded.event_type in ("position_report_class_a", "position_report_class_b"):
            bucket = self.ship_type_cache.get(mmsi9)
            data = _build_position(fields, decoded, flag, bucket)
            if data is not None:
                self.position_cache.set(mmsi9, data.latitude, data.longitude)
                await self.client.publish_no_kystverket_ais_mqtt_position_report(
                    mmsi=data.mmsi, flag=data.flag, ship_type=data.ship_type,
                    geohash5=data.geohash5, data=data, qos=0, retain=False,
                )
        elif decoded.event_type == "aid_to_navigation":
            data = _build_aton(fields, decoded, flag)
            if data is not None:
                await self.client.publish_no_kystverket_ais_mqtt_aid_to_navigation(
                    mmsi=data.mmsi, flag=data.flag, ship_type=data.ship_type,
                    geohash5=data.geohash5, data=data, qos=0, retain=False,
                )

    async def emit_mock_corpus(self) -> None:
        """Publish one synthetic message per family for Docker E2E."""
        now = datetime.now(timezone.utc).isoformat()

        # Static — MMSI MID 257 = Norway, ShipType 70 = cargo
        static = DecodedAIS(
            msg_type=5,
            event_type="static_voyage_data",
            mmsi=257_555_001,
            station_id="MOCK-NO",
            receive_time=datetime.now(timezone.utc),
            fields={
                "mmsi": 257_555_001,
                "imo_number": 9_111_222,
                "callsign": "LXXX",
                "ship_name": "MOCK FJORD CARGO",
                "ship_type": 70,
                "dimension_to_bow": 100,
                "dimension_to_stern": 50,
                "dimension_to_port": 10,
                "dimension_to_starboard": 22,
                "draught": 8.5,
                "destination": "NOOSL",
                "eta_month": 5, "eta_day": 23, "eta_hour": 12, "eta_minute": 0,
                "timestamp": now, "station_id": "MOCK-NO",
            },
        )
        await self.dispatch(static)

        # Position class A
        pos = DecodedAIS(
            msg_type=1,
            event_type="position_report_class_a",
            mmsi=257_555_001,
            station_id="MOCK-NO",
            receive_time=datetime.now(timezone.utc),
            fields={
                "mmsi": 257_555_001,
                "navigation_status": 0,
                "rate_of_turn": 0.0,
                "speed_over_ground": 12.3,
                "position_accuracy": 1,
                "longitude": 10.7522,
                "latitude": 59.9139,
                "course_over_ground": 95.1,
                "true_heading": 95,
                "timestamp": now,
                "station_id": "MOCK-NO",
                "msg_type": 1,
            },
        )
        await self.dispatch(pos)

        # AtoN (MMSI 992 257 xxx = Norwegian AtoN)
        aton = DecodedAIS(
            msg_type=21,
            event_type="aid_to_navigation",
            mmsi=992_257_001,
            station_id="MOCK-NO",
            receive_time=datetime.now(timezone.utc),
            fields={
                "mmsi": 992_257_001,
                "aid_type": 1,
                "name": "OSLOFJORD BUOY 7",
                "position_accuracy": 1,
                "longitude": 10.74,
                "latitude": 59.40,
                "timestamp": now,
                "station_id": "MOCK-NO",
            },
        )
        await self.dispatch(aton)

def _parse_broker(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    host = parsed.hostname or "localhost"
    port = parsed.port or (8883 if scheme == "mqtts" else 1883)
    return host, port, scheme == "mqtts"

async def _run(args: argparse.Namespace) -> None:
    broker_host, broker_port, tls = _parse_broker(args.mqtt_broker_url)
    tls = tls or args.mqtt_enable_tls

    resolved_client_id, resolved_username, resolved_password = _resolve_mqtt_connection_settings(
        username=args.mqtt_username,
        password=args.mqtt_password or "",
        client_id=args.mqtt_client_id or "",
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho_client = mqtt.Client(client_id=resolved_client_id or "", 
        callback_api_version=CallbackAPIVersion.VERSION2,
        protocol=MQTTv5,
    )
    if resolved_username or resolved_password:
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls:
        paho_client.tls_set()

    loop = asyncio.get_running_loop()
    client = NOKystverketAISMqttMqttClient(
        client=paho_client,
        content_mode="binary",
        loop=loop,
    )
    logger.info("Connecting to MQTT broker %s:%s (tls=%s); mid_iso_version=%s",
                broker_host, broker_port, tls, MID_ISO_VERSION)
    await client.connect(broker_host, broker_port)

    bridge = KystverketAisMqttBridge(
        client,
        tcp_host=args.tcp_host,
        tcp_port=args.tcp_port,
    )
    if args.mock:
        logger.info("Mock mode: emitting synthetic Kystverket AIS corpus and exiting")
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

    p = argparse.ArgumentParser(description="Kystverket AIS -> MQTT/UNS bridge")
    sub = p.add_subparsers(dest="command")

    feed = sub.add_parser("feed", help="Stream Kystverket AIS to MQTT")
    feed.add_argument("--mqtt-broker-url",
                      default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed.add_argument("--mqtt-enable-tls", action="store_true",
                      default=os.getenv("MQTT_ENABLE_TLS", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed.add_argument("--tcp-host",
                      default=os.getenv("AIS_TCP_HOST", KystverketAisMqttBridge.DEFAULT_TCP_HOST))
    feed.add_argument("--tcp-port", type=int,
                      default=int(os.getenv("AIS_TCP_PORT", str(KystverketAisMqttBridge.DEFAULT_TCP_PORT))))
    feed.add_argument("--max-events", type=int,
                      default=int(os.getenv("KYSTVERKET_AIS_MAX_EVENTS", "0")) or None)
    feed.add_argument("--mock", action="store_true",
                      default=os.getenv("KYSTVERKET_AIS_MOCK", "false").lower() in ("true", "1", "yes"),
                      help="Skip live TCP, emit one synthetic event per family, then exit")

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
