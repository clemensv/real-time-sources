"""AISstream.io firehose -> MQTT/UNS bridge."""

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

from aisstream_core import AisStreamBridge
from aisstream_mqtt_producer_data import AidToNavigation, PositionReport, ShipStatic
from aisstream_mqtt_producer_mqtt_client.client import IOAISstreamMqttMqttClient

logger = logging.getLogger("aisstream_mqtt")


def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
    params = {"api-version": "2018-02-01", "resource": audience or "https://eventgrid.azure.net/"}
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


class AisStreamMqttClientAdapter:
    def __init__(self, client: IOAISstreamMqttMqttClient):
        self._client = client

    async def publish_position_report(self, *, mmsi, flag, ship_type, geohash5, payload):
        data = PositionReport(mmsi=mmsi, flag=flag, ship_type=ship_type, geohash5=geohash5, msg_type="position-report", **payload)
        await self._client.publish_io_aisstream_mqtt_position_report(mmsi=mmsi, flag=flag, ship_type=ship_type, geohash5=geohash5, data=data, qos=0, retain=False)

    async def publish_ship_static(self, *, mmsi, flag, ship_type, geohash5, payload):
        data = ShipStatic(mmsi=mmsi, flag=flag, ship_type=ship_type, geohash5=geohash5, msg_type="static", **payload)
        await self._client.publish_io_aisstream_mqtt_ship_static(mmsi=mmsi, flag=flag, ship_type=ship_type, geohash5=geohash5, data=data, qos=0, retain=False)

    async def publish_aid_to_navigation(self, *, mmsi, flag, ship_type, geohash5, payload):
        data = AidToNavigation(mmsi=mmsi, flag=flag, ship_type=ship_type, geohash5=geohash5, msg_type="aid-to-navigation", **payload)
        await self._client.publish_io_aisstream_mqtt_aid_to_navigation(mmsi=mmsi, flag=flag, ship_type=ship_type, geohash5=geohash5, data=data, qos=0, retain=False)


def _mock_envelopes():
    return [
        {"MessageType": "ShipStaticData", "MetaData": {"MMSI": 211_555_001}, "Message": {"ShipStaticData": {"UserID": 211_555_001, "Name": "MOCK CARGO       @@@@", "CallSign": "DXXX@", "ImoNumber": 9_111_222, "Type": 70, "Destination": "DEHAM@@@@@@@@@@@@@@@", "Eta": {"Month": 5, "Day": 23, "Hour": 12, "Minute": 0}, "MaximumStaticDraught": 8.5, "Dimension": {"A": 100, "B": 50, "C": 10, "D": 22}, "MessageID": 5}}},
        {"MessageType": "PositionReport", "MetaData": {"MMSI": 211_555_001}, "Message": {"PositionReport": {"UserID": 211_555_001, "Latitude": 53.5511, "Longitude": 9.9937, "Sog": 12.3, "Cog": 95.1, "TrueHeading": 95, "NavigationalStatus": 0, "RateOfTurn": 0, "PositionAccuracy": True, "Timestamp": 30, "Raim": False, "MessageID": 1}}},
        {"MessageType": "AidsToNavigationReport", "MetaData": {"MMSI": 992_111_001}, "Message": {"AidsToNavigationReport": {"UserID": 992_111_001, "Name": "ELBE BUOY 7", "Type": 1, "Latitude": 53.88, "Longitude": 8.71, "OffPosition": False, "VirtualAtoN": False, "MessageID": 21}}},
    ]


def _parse_broker(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    return parsed.hostname or "localhost", parsed.port or (8883 if scheme == "mqtts" else 1883), scheme == "mqtts"


async def _run(args: argparse.Namespace) -> None:
    broker_host, broker_port, tls = _parse_broker(args.mqtt_broker_url)
    tls = tls or args.mqtt_enable_tls
    resolved_client_id, resolved_username, resolved_password, entra_props = _resolve_mqtt_connection_settings(
        username=args.mqtt_username,
        password=args.mqtt_password or "",
        client_id=args.mqtt_client_id or "",
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )
    paho_client = mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls or entra_props is not None:
        paho_client.tls_set()
    loop = asyncio.get_running_loop()
    mqtt_client = IOAISstreamMqttMqttClient(client=paho_client, content_mode="binary", loop=loop)
    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    if entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=entra_props)
        paho_client.loop_start()
    else:
        await mqtt_client.connect(broker_host, broker_port)
    bridge = AisStreamBridge(AisStreamMqttClientAdapter(mqtt_client), api_key=args.api_key, ws_url=args.ws_url)
    try:
        if args.mock:
            logger.info("Mock mode: emitting synthetic AIS corpus and exiting")
            for envelope in _mock_envelopes():
                await bridge.handle_envelope(envelope)
            await asyncio.sleep(1.0)
            return
        await bridge.run(max_events=args.max_events)
    finally:
        await mqtt_client.disconnect()


def main() -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="AISstream -> MQTT/UNS bridge")
    sub = parser.add_subparsers(dest="command")
    feed = sub.add_parser("feed", help="Stream AIS to MQTT")
    feed.add_argument("--mqtt-broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed.add_argument("--mqtt-enable-tls", action="store_true", default=os.getenv("MQTT_ENABLE_TLS", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed.add_argument("--api-key", default=os.getenv("AISSTREAM_API_KEY"))
    feed.add_argument("--ws-url", default=os.getenv("AISSTREAM_WS_URL", "wss://stream.aisstream.io/v0/stream"))
    feed.add_argument("--max-events", type=int, default=int(os.getenv("AISSTREAM_MAX_EVENTS", "0")) or None)
    feed.add_argument("--mock", action="store_true", default=os.getenv("AISSTREAM_MOCK", "false").lower() in ("true", "1", "yes"))
    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        sys.exit(1)
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
