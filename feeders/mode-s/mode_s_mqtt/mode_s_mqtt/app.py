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
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from mode_s_mqtt_producer_data import Record
from mode_s_mqtt_producer_mqtt_client.client import ModeSMqttMqttClient
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
        client: ModeSMqttMqttClient,
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

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_broker(url: str) -> Tuple[str, int, bool]:
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
    client = ModeSMqttMqttClient(
        client=paho_client,
        content_mode="binary",
        loop=loop,
    )
    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await client.connect(broker_host, broker_port)

    feedurl = args.feedurl or (
        f"dump1090://{args.host}:{args.port}" if args.host and args.port
        else "mock://mode-s"
    )

    bridge = ModeSMqttBridge(
        client,
        feedurl=feedurl,
        receiver_id=args.receiver_id,
        ref_lat=args.ref_lat or 0.0,
        ref_lon=args.ref_lon or 0.0,
    )

    if args.mock:
        logger.info("Mock mode: emitting synthetic Mode-S corpus and exiting")
        await bridge.emit_mock_corpus()
        await asyncio.sleep(1.0)
        await client.disconnect()
        return

    if not args.host or not args.port:
        raise SystemExit("--host and --port (dump1090 endpoint) are required unless --mock")

    try:
        await bridge.run_from_dump1090(args.host, int(args.port),
                                       max_events=args.max_events)
    finally:
        await client.disconnect()

def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    p = argparse.ArgumentParser(description="Mode-S -> MQTT/UNS bridge")
    sub = p.add_subparsers(dest="command")

    feed = sub.add_parser("feed", help="Stream Mode-S records to MQTT")
    feed.add_argument("--mqtt-broker-url",
                      default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed.add_argument("--mqtt-enable-tls", action="store_true",
                      default=os.getenv("MQTT_ENABLE_TLS", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed.add_argument("--host", default=os.getenv("DUMP1090_HOST"))
    feed.add_argument("--port", default=os.getenv("DUMP1090_PORT"))
    feed.add_argument("--receiver-id",
                      default=os.getenv("MODE_S_RECEIVER_ID",
                                        os.getenv("STATIONID", "station1")))
    feed.add_argument("--ref-lat", type=float,
                      default=float(os.getenv("REF_LAT")) if os.getenv("REF_LAT") else None)
    feed.add_argument("--ref-lon", type=float,
                      default=float(os.getenv("REF_LON")) if os.getenv("REF_LON") else None)
    feed.add_argument("--feedurl", default=os.getenv("MODE_S_FEEDURL"))
    feed.add_argument("--max-events", type=int,
                      default=int(os.getenv("MODE_S_MAX_EVENTS", "0")) or None)
    feed.add_argument("--mock", action="store_true",
                      default=os.getenv("MODE_S_MOCK", "false").lower() in ("true", "1", "yes"),
                      help="Skip TCP feed, emit one synthetic event per family, then exit")

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
