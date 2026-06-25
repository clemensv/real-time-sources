from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from mode_s_core import ModeSBridge
from mode_s_mqtt_producer_data import Record as MqttRecord
from mode_s_mqtt_producer_mqtt_client.client import ModeSMqttMqttClient

logger = logging.getLogger("mode_s_mqtt")


def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
    params = {"api-version": "2018-02-01", "resource": audience or "https://eventgrid.azure.net/"}
    if managed_identity_client_id:
        params["client_id"] = managed_identity_client_id
    request = Request("http://169.254.169.254/metadata/identity/oauth2/token?" + urlencode(params), headers={"Metadata": "true"})
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
        return resolved_client_id, str(username or ""), str(password or ""), None
    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    resolved_username = resolved_client_id or str(username or "").strip()
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")
    resolved_password = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    from paho.mqtt.properties import Properties as _MqttConnProps
    connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
    connect_props.AuthenticationMethod = "OAUTH2-JWT"
    connect_props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, connect_props


class ModeSMqttClientAdapter:
    def __init__(self, client: ModeSMqttMqttClient):
        self._client = client

    @staticmethod
    def _data(rec) -> MqttRecord:
        return MqttRecord(**rec.__dict__)

    async def publish_adsb(self, *, feedurl, icao24, receiver_id, data):
        await self._client.publish_mode_s_adsb_mqtt(feedurl=feedurl, icao24=icao24, receiver_id=receiver_id, data=self._data(data), qos=0, retain=False)

    async def publish_altitude_reply(self, *, feedurl, icao24, receiver_id, data):
        await self._client.publish_mode_s_altitude_reply_mqtt(feedurl=feedurl, icao24=icao24, receiver_id=receiver_id, data=self._data(data), qos=0, retain=False)

    async def publish_identity_reply(self, *, feedurl, icao24, receiver_id, data):
        await self._client.publish_mode_s_identity_reply_mqtt(feedurl=feedurl, icao24=icao24, receiver_id=receiver_id, data=self._data(data), qos=0, retain=False)

    async def publish_acquisition_reply(self, *, feedurl, icao24, receiver_id, data):
        await self._client.publish_mode_s_acquisition_reply_mqtt(feedurl=feedurl, icao24=icao24, receiver_id=receiver_id, data=self._data(data), qos=0, retain=False)

    async def publish_comm_baltitude(self, *, feedurl, icao24, receiver_id, data):
        await self._client.publish_mode_s_comm_baltitude_mqtt(feedurl=feedurl, icao24=icao24, receiver_id=receiver_id, data=self._data(data), qos=0, retain=False)

    async def publish_comm_bidentity(self, *, feedurl, icao24, receiver_id, data):
        await self._client.publish_mode_s_comm_bidentity_mqtt(feedurl=feedurl, icao24=icao24, receiver_id=receiver_id, data=self._data(data), qos=0, retain=False)


def _parse_broker(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    return parsed.hostname or "localhost", parsed.port or (8883 if scheme == "mqtts" else 1883), scheme == "mqtts"


async def _emit_mock_corpus(bridge: ModeSBridge) -> None:
    """Emit one synthetic record per DF family for Docker E2E testing."""
    import time as _time
    from mode_s_core import ModeSRecord
    ts = int(_time.time() * 1000)
    families = [
        (17, "df17-adsb", 11),
        (4, "df4-altitude", None),
        (5, "df5-identity", None),
        (11, "df11-acquisition", None),
        (20, "df20-comm-b", None),
        (21, "df21-comm-b", None),
    ]
    for df, msg_type, tc in families:
        rec = ModeSRecord(
            icao24="abc123", receiver_id="mock-station", msg_type=msg_type,
            ts=ts, df=df, tc=tc, bcode=None, alt=35000 if df in (4, 20) else None,
            cs="MOCK01" if df == 17 else None, sq="1200" if df == 5 else None,
            lat=59.9 if df == 17 else None, lon=10.7 if df == 17 else None,
            spd=450.0 if df == 17 else None, ang=90.0 if df == 17 else None,
            vr=0.0, rssi=-3.5,
        )
        await bridge.publish_record(rec)
    logger.info("Mock corpus emitted: %d records", len(families))


async def _run(args: argparse.Namespace) -> None:
    broker_host, broker_port, tls = _parse_broker(args.mqtt_broker_url)
    tls = tls or args.mqtt_enable_tls
    resolved_client_id, resolved_username, resolved_password, entra_props = _resolve_mqtt_connection_settings(username=args.mqtt_username, password=args.mqtt_password or "", client_id=args.mqtt_client_id or "", auth_mode=os.getenv("MQTT_AUTH_MODE"))
    paho_client = mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls or entra_props is not None:
        paho_client.tls_set()
    loop = asyncio.get_running_loop()
    client = ModeSMqttMqttClient(client=paho_client, content_mode="binary", loop=loop)
    if entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=entra_props)
        paho_client.loop_start()
    else:
        await client.connect(broker_host, broker_port)
    feedurl = args.feedurl or f"dump1090://{args.host}:{args.port}"
    bridge = ModeSBridge(ModeSMqttClientAdapter(client), feedurl=feedurl, receiver_id=args.receiver_id, ref_lat=args.ref_lat or 0.0, ref_lon=args.ref_lon or 0.0)
    try:
        if os.getenv("MODE_S_MOCK", "false").lower() in ("true", "1", "yes"):
            await _emit_mock_corpus(bridge)
        elif not args.host or not args.port:
            raise SystemExit("--host and --port are required")
        else:
            await bridge.run_from_dump1090(args.host, int(args.port), max_events=args.max_events)
    finally:
        await client.disconnect()


def main() -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="Mode-S -> MQTT/UNS bridge")
    sub = parser.add_subparsers(dest="command")
    feed = sub.add_parser("feed", help="Stream Mode-S records to MQTT")
    feed.add_argument("--mqtt-broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed.add_argument("--mqtt-enable-tls", action="store_true", default=os.getenv("MQTT_ENABLE_TLS", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed.add_argument("--host", default=os.getenv("DUMP1090_HOST"))
    feed.add_argument("--port", default=os.getenv("DUMP1090_PORT"))
    feed.add_argument("--receiver-id", default=os.getenv("MODE_S_RECEIVER_ID", os.getenv("STATIONID", "station1")))
    feed.add_argument("--ref-lat", type=float, default=float(os.getenv("REF_LAT", "0")) if os.getenv("REF_LAT") else None)
    feed.add_argument("--ref-lon", type=float, default=float(os.getenv("REF_LON", "0")) if os.getenv("REF_LON") else None)
    feed.add_argument("--feedurl", default=os.getenv("MODE_S_FEEDURL"))
    feed.add_argument("--max-events", type=int, default=int(os.getenv("MODE_S_MAX_EVENTS", "0")) or None)
    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        sys.exit(1)
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
