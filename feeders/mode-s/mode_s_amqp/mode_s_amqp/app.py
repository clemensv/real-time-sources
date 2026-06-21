"""Mode-S firehose -> MQTT/UNS bridge.

Connects to a Beast/dump1090 TCP feed (via :mod:`pyModeS`), decodes Mode-S
downlink frames, buckets them per Downlink Format (DF) family, and
republishes each record as a non-retained QoS-0 MQTT 5 binary-mode
CloudEvent on the topic family

    aviation/intl/mode-s/mode-s/{icao24}/{receiver_id}/{msg_type}

The DF families produced are:

* ``df17-adsb``        - DF17/DF18 ADS-B extended squitter
* ``df4-altitude``     - DF4 altitude reply
* ``df5-identity``     - DF5 identity reply
* ``df11-acquisition`` - DF11 all-call/acquisition reply
* ``df20-comm-b``      - DF20 Comm-B altitude reply
* ``df21-comm-b``      - DF21 Comm-B identity reply

Frames with other DF values are dropped: the underlying decoder does not
differentiate them into stable record families.

Run with::

    python -m mode_s_mqtt feed --mqtt-broker-url localhost:1883 \
        --host dump1090 --port 30005 --receiver-id station1
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import math
import os
import sys
import threading
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

from mode_s_amqp_producer_data import Record
from mode_s_amqp_producer_amqp_producer.producer import ModeSAmqpProducer

logger = logging.getLogger("mode_s_mqtt")


# ---------------------------------------------------------------------------
# DF -> msg_type mapping
# ---------------------------------------------------------------------------

# Each Downlink Format bucket is published with the kebab-case literal
# baked into the trailing topic segment by xrcg.
DF_TO_MSG_TYPE: Dict[int, str] = {
    4: "df4-altitude",
    5: "df5-identity",
    11: "df11-acquisition",
    17: "df17-adsb",
    18: "df17-adsb",   # DF18 (TIS-B/ADS-R) shares the ADS-B decoder path
    20: "df20-comm-b",
    21: "df21-comm-b",
}


def _norm_segment(value: Optional[str]) -> str:
    if not value:
        return ""
    return str(value).strip().lower().replace("/", "_").replace("#", "_").replace("+", "_")


def _hex_icao(icao_value: Optional[str]) -> str:
    if not icao_value:
        return ""
    return _norm_segment(icao_value)


# ---------------------------------------------------------------------------
# Decoder
# ---------------------------------------------------------------------------


def _decode_rssi(raw_msg: bytes) -> Optional[float]:
    """Decode the Beast 1-byte RSSI field (byte 7 of a raw Beast frame)."""
    if len(raw_msg) < 7:
        return None
    raw_rssi = raw_msg[6]
    if raw_rssi <= 0:
        return None
    rssi_ratio = raw_rssi / 255
    signal_level = rssi_ratio ** 2
    return round(10 * math.log10(signal_level), 2)


def decode_one(msg_hex: str, ts_ms: int, receiver_id: str,
               ref_lat: float = 0.0, ref_lon: float = 0.0) -> Optional[Record]:
    """Decode a single hex Mode-S frame into a :class:`Record`.

    Returns ``None`` when the frame does not belong to one of the
    supported DF families or when pyModeS reports a parse failure.
    """
    import pyModeS as pms  # local import keeps the CLI lightweight in --mock mode

    try:
        raw_msg = bytes.fromhex(msg_hex)
    except ValueError:
        return None
    if len(raw_msg) < 7:
        return None

    try:
        df = pms.df(msg_hex)
        icao = pms.icao(msg_hex)
    except Exception:
        return None
    if icao is None:
        return None
    if df not in DF_TO_MSG_TYPE:
        return None

    msg_type = DF_TO_MSG_TYPE[df]
    rssi = _decode_rssi(raw_msg)
    rec = Record(
        icao24=_hex_icao(icao),
        receiver_id=_norm_segment(receiver_id),
        msg_type=msg_type,
        ts=int(ts_ms),
        df=int(df),
        tc=None, bcode=None, alt=None, cs=None, sq=None,
        lat=None, lon=None, spd=None, ang=None, vr=None,
        rssi=rssi,
    )

    try:
        if df in (17, 18):
            tc = pms.typecode(msg_hex)
            rec.tc = tc
            if tc is None:
                pass
            elif 1 <= tc <= 4:
                rec.cs = pms.adsb.callsign(msg_hex)
            elif 5 <= tc <= 8:
                lat, lon = pms.adsb.surface_position_with_ref(msg_hex, ref_lat, ref_lon)
                rec.lat, rec.lon = lat, lon
            elif 9 <= tc <= 18:
                rec.alt = pms.adsb.altitude(msg_hex)
                lat, lon = pms.adsb.airborne_position_with_ref(msg_hex, ref_lat, ref_lon)
                rec.lat, rec.lon = lat, lon
            elif tc == 19:
                speed, angle, vr, _spd_type = pms.adsb.velocity(msg_hex)
                rec.spd, rec.ang, rec.vr = speed, angle, vr
            elif 20 <= tc <= 22:
                rec.alt = pms.adsb.altitude(msg_hex)
                lat, lon = pms.adsb.airborne_position_with_ref(msg_hex, ref_lat, ref_lon)
                rec.lat, rec.lon = lat, lon
        elif df == 20:
            try:
                rec.alt = pms.common.altcode(msg_hex)
            except Exception:
                pass
            try:
                rec.bcode = pms.bds.infer(msg_hex, mrar=True) or None
            except Exception:
                pass
        elif df == 21:
            try:
                rec.sq = str(pms.common.idcode(msg_hex))
            except Exception:
                pass
            try:
                rec.bcode = pms.bds.infer(msg_hex, mrar=True) or None
            except Exception:
                pass
    except Exception as exc:  # pragma: no cover - decoder edge cases
        logger.debug("decode partial-failure for %s: %s", msg_hex, exc)

    return rec


# ---------------------------------------------------------------------------
# MQTT bridge
# ---------------------------------------------------------------------------


_PUBLISH_BY_MSG_TYPE = {
    "df17-adsb":        "publish_mode_s_adsb_mqtt",
    "df4-altitude":     "publish_mode_s_altitude_reply_mqtt",
    "df5-identity":     "publish_mode_s_identity_reply_mqtt",
    "df11-acquisition": "publish_mode_s_acquisition_reply_mqtt",
    "df20-comm-b":      "publish_mode_s_comm_baltitude_mqtt",
    "df21-comm-b":      "publish_mode_s_comm_bidentity_mqtt",
}


class ModeSMqttBridge:
    """Beast/dump1090 -> MQTT/UNS pump."""

    def __init__(
        self,
        client: ModeSAmqpClient,
        *,
        feedurl: str,
        receiver_id: str,
        ref_lat: float = 0.0,
        ref_lon: float = 0.0,
    ) -> None:
        self.client = client
        self.feedurl = feedurl
        self.receiver_id = receiver_id
        self.ref_lat = ref_lat
        self.ref_lon = ref_lon
        self._count = 0

    async def publish_record(self, rec: Record) -> None:
        publish_name = _PUBLISH_BY_MSG_TYPE.get(rec.msg_type)
        if publish_name is None:
            return
        publish_fn = getattr(self.client, publish_name)
        await publish_fn(
            feedurl=self.feedurl,
            icao24=rec.icao24,
            receiver_id=rec.receiver_id,
            data=rec,
            qos=0,
            retain=False,
        )
        self._count += 1

    async def run_from_dump1090(self, host: str, port: int,
                                rawtype: str = "beast",
                                max_events: Optional[int] = None) -> None:
        """Connect to a Beast/dump1090 TCP feed and pump records to MQTT."""
        import pyModeS as pms
        from pyModeS.extra.tcpclient import TcpClient

        loop = asyncio.get_running_loop()
        bridge_self = self

        class _PumpClient(TcpClient):
            def __init__(self):
                super().__init__(host, port, rawtype)

            def handle_messages(self, messages):
                for msg_hex, ts in messages:
                    rec = decode_one(
                        msg_hex,
                        int(ts * 1000),
                        bridge_self.receiver_id,
                        bridge_self.ref_lat,
                        bridge_self.ref_lon,
                    )
                    if rec is None:
                        continue
                    fut = asyncio.run_coroutine_threadsafe(
                        bridge_self.publish_record(rec), loop
                    )
                    try:
                        fut.result(timeout=10)
                    except Exception as exc:  # pragma: no cover
                        logger.warning("publish failed: %s", exc)
                    if max_events and bridge_self._count >= max_events:
                        self.stop_flag = True
                        return

        pump = _PumpClient()
        await loop.run_in_executor(None, pump.run)

    async def emit_mock_corpus(self) -> None:
        """Publish one synthetic record per family for Docker E2E.

        Synthetic records bypass the decoder; we pre-build the Record
        dataclass with realistic axis values for each msg_type.
        """
        ts_ms = 1_700_000_000_000
        families: List[Tuple[str, str, Dict[str, Any]]] = [
            ("df17-adsb",       "a1b2c3", {"df": 17, "tc": 11, "alt": 35000,
                                            "lat": 52.5200, "lon": 13.4050,
                                            "cs": "DLH123"}),
            ("df4-altitude",    "a1b2c4", {"df": 4,  "alt": 27000}),
            ("df5-identity",    "a1b2c5", {"df": 5,  "sq": "7000"}),
            ("df11-acquisition", "a1b2c6", {"df": 11}),
            ("df20-comm-b",     "a1b2c7", {"df": 20, "alt": 31000, "bcode": "BDS50"}),
            ("df21-comm-b",     "a1b2c8", {"df": 21, "sq": "1234", "bcode": "BDS60"}),
        ]
        for msg_type, icao, extras in families:
            rec = Record(
                icao24=_norm_segment(icao),
                receiver_id=_norm_segment(self.receiver_id),
                msg_type=msg_type,
                ts=ts_ms,
                df=extras["df"],
                tc=extras.get("tc"),
                bcode=extras.get("bcode"),
                alt=extras.get("alt"),
                cs=extras.get("cs"),
                sq=extras.get("sq"),
                lat=extras.get("lat"),
                lon=extras.get("lon"),
                spd=extras.get("spd"),
                ang=extras.get("ang"),
                vr=extras.get("vr"),
                rssi=-12.5,
            )
            await self.publish_record(rec)



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


_PUBLISH_AMQP_BY_MSG_TYPE = {
    "df17-adsb": "send_adsb",
    "df4-altitude": "send_altitude_reply",
    "df5-identity": "send_identity_reply",
    "df11-acquisition": "send_acquisition_reply",
    "df20-comm-b": "send_comm_baltitude",
    "df21-comm-b": "send_comm_bidentity",
}

class ModeSAmqpClient:
    def __init__(self, producer: ModeSAmqpProducer):
        self.producer = producer

    async def publish_mode_s_adsb_mqtt(self, **kwargs): await self._publish(**kwargs)
    async def publish_mode_s_altitude_reply_mqtt(self, **kwargs): await self._publish(**kwargs)
    async def publish_mode_s_identity_reply_mqtt(self, **kwargs): await self._publish(**kwargs)
    async def publish_mode_s_acquisition_reply_mqtt(self, **kwargs): await self._publish(**kwargs)
    async def publish_mode_s_comm_baltitude_mqtt(self, **kwargs): await self._publish(**kwargs)
    async def publish_mode_s_comm_bidentity_mqtt(self, **kwargs): await self._publish(**kwargs)

    async def _publish(self, *, feedurl, icao24, receiver_id, data, **_):
        fn = getattr(self.producer, _PUBLISH_AMQP_BY_MSG_TYPE[data.msg_type])
        fn(data=data, _feedurl=feedurl, _icao24=icao24, _receiver_id=receiver_id, _msg_type=data.msg_type)


async def _run(args: argparse.Namespace) -> None:
    producer = _retry_producer_init(lambda: create_amqp_producer(args, ModeSAmqpProducer))
    client = ModeSAmqpClient(producer)
    feedurl = args.feedurl or (f"dump1090://{args.dump1090_host}:{args.dump1090_port}" if args.dump1090_host and args.dump1090_port else "mock://mode-s")
    bridge = ModeSMqttBridge(client, feedurl=feedurl, receiver_id=args.receiver_id, ref_lat=args.ref_lat or 0.0, ref_lon=args.ref_lon or 0.0)
    try:
        if args.mock:
            logger.info("Mock mode: emitting synthetic Mode-S corpus to AMQP and exiting")
            await bridge.emit_mock_corpus(); return
        if not args.dump1090_host or not args.dump1090_port:
            raise SystemExit("--dump1090-host and --dump1090-port are required unless --mock")
        await bridge.run_from_dump1090(args.dump1090_host, int(args.dump1090_port), max_events=args.max_events)
    finally:
        producer.close()


def main() -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(description="Mode-S -> AMQP 1.0 bridge")
    sub = p.add_subparsers(dest="command")
    feed = sub.add_parser("feed")
    add_amqp_arguments(feed, "mode-s")
    feed.add_argument("--dump1090-host", default=os.getenv("DUMP1090_HOST"))
    feed.add_argument("--dump1090-port", default=os.getenv("DUMP1090_PORT"))
    feed.add_argument("--receiver-id", default=os.getenv("MODE_S_RECEIVER_ID", os.getenv("STATIONID", "station1")))
    feed.add_argument("--ref-lat", type=float, default=float(os.getenv("REF_LAT")) if os.getenv("REF_LAT") else None)
    feed.add_argument("--ref-lon", type=float, default=float(os.getenv("REF_LON")) if os.getenv("REF_LON") else None)
    feed.add_argument("--feedurl", default=os.getenv("MODE_S_FEEDURL"))
    feed.add_argument("--max-events", type=int, default=int(os.getenv("MODE_S_MAX_EVENTS", "0")) or None)
    feed.add_argument("--mock", action="store_true", default=os.getenv("MODE_S_MOCK", "").lower() in ("1","true","yes"))
    args = p.parse_args()
    if args.command != "feed": p.print_help(); sys.exit(1)
    asyncio.run(_run(args))

if __name__ == "__main__": main()
