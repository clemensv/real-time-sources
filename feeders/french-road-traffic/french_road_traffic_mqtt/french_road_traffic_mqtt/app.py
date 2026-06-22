from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import threading
from typing import Any
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from french_road_traffic_core.french_road_traffic import (
    DEFAULT_POLL_INTERVAL_SECONDS,
    FEED_SOURCE_EVENTS,
    FEED_SOURCE_FLOW,
    FrenchRoadTrafficSource,
    normalize_road_segment,
)
from french_road_traffic_mqtt_producer.french_road_traffic_mqtt_producer_data.fr.gouv.transport.bison_fute.roadevent import RoadEvent
from french_road_traffic_mqtt_producer.french_road_traffic_mqtt_producer_data.fr.gouv.transport.bison_fute.trafficflowmeasurement import TrafficFlowMeasurement
from french_road_traffic_mqtt_producer.french_road_traffic_mqtt_producer_mqtt_client.client import (
    FrGouvTransportBisonFuteRoadEventMqttMqttClient,
    FrGouvTransportBisonFuteTrafficFlowMqttMqttClient,
)

logger = logging.getLogger(__name__)


def _fetch_entra_token(audience: str, managed_identity_client_id: str | None = None) -> str:
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


def _resolve_connection_settings(username: str | None, password: str | None) -> tuple[str, str, Any | None]:
    auth_mode = str(os.getenv("MQTT_AUTH_MODE", "password")).strip().lower() or "password"
    resolved_username = str(username or os.getenv("MQTT_USERNAME") or "")
    resolved_password = str(password or os.getenv("MQTT_PASSWORD") or "")
    if auth_mode != "entra":
        return resolved_username, resolved_password, None
    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    client_id = str(os.getenv("MQTT_CLIENT_ID") or "").strip()
    resolved_username = client_id or resolved_username
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID is required for MQTT_AUTH_MODE=entra")
    resolved_password = _fetch_entra_token(audience, managed_identity_client_id)
    from paho.mqtt.packettypes import PacketTypes
    from paho.mqtt.properties import Properties

    props = Properties(PacketTypes.CONNECT)
    props.AuthenticationMethod = "OAUTH2-JWT"
    props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_username, resolved_password, props


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    tls = (parsed.scheme or "mqtt").lower() in {"mqtts", "ssl", "tls"}
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls


def _flow_data(record: dict[str, Any]) -> TrafficFlowMeasurement:
    return TrafficFlowMeasurement(**record)


def _event_data(record: dict[str, Any]) -> RoadEvent:
    return RoadEvent(**record)


async def _publish_cycle(
    source: FrenchRoadTrafficSource,
    flow_client: FrGouvTransportBisonFuteTrafficFlowMqttMqttClient,
    event_client: FrGouvTransportBisonFuteRoadEventMqttMqttClient,
) -> None:
    flow_count = 0
    event_count = 0
    for record in source.fetch_traffic_flow():
        await flow_client.publish_fr_gouv_transport_bison_fute_traffic_flow_measurement_mqtt(
            feedurl=FEED_SOURCE_FLOW,
            site_id=record["site_id"],
            road="unknown",
            data=_flow_data(record),
        )
        flow_count += 1
    for record in source.fetch_road_events():
        await event_client.publish_fr_gouv_transport_bison_fute_road_event_mqtt(
            feedurl=FEED_SOURCE_EVENTS,
            situation_id=record["situation_id"],
            road=normalize_road_segment(record.get("road_number")),
            data=_event_data(record),
        )
        event_count += 1
    logger.info("Published %d flow measurements and %d road events", flow_count, event_count)


async def _run(args: argparse.Namespace) -> None:
    source = FrenchRoadTrafficSource()
    host, port, tls = _parse_broker_url(args.broker_url)
    username, password, entra_props = _resolve_connection_settings(args.username, args.password)
    paho_client = mqtt.Client(
        client_id=os.getenv("MQTT_CLIENT_ID") or "french-road-traffic-mqtt",
        callback_api_version=CallbackAPIVersion.VERSION2,
        protocol=MQTTv5,
    )
    if entra_props is None and (username or password):
        paho_client.username_pw_set(username, password)
    if tls or os.getenv("MQTT_TLS", "").lower() in {"1", "true", "yes"}:
        paho_client.tls_set()

    loop = asyncio.get_running_loop()
    flow_client = FrGouvTransportBisonFuteTrafficFlowMqttMqttClient(client=paho_client, content_mode=args.content_mode, loop=loop)
    event_client = FrGouvTransportBisonFuteRoadEventMqttMqttClient(client=paho_client, content_mode=args.content_mode, loop=loop)
    if entra_props is not None:
        connected = threading.Event()

        def _on_connect(_client, _userdata, _flags, reason_code, _properties=None):
            if (reason_code if isinstance(reason_code, int) else getattr(reason_code, "value", reason_code)) == 0:
                connected.set()

        paho_client.on_connect = _on_connect
        paho_client.connect(host, port, keepalive=60, clean_start=True, properties=entra_props)
        paho_client.loop_start()
        if not await loop.run_in_executor(None, lambda: connected.wait(30)):
            raise RuntimeError("MQTT CONNACK timeout after 30s")
    else:
        await event_client.connect(host, port)
    try:
        while True:
            await _publish_cycle(source, flow_client, event_client)
            if args.once:
                break
            await asyncio.sleep(args.polling_interval)
    finally:
        await event_client.disconnect()


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="French Road Traffic MQTT bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME"))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD"))
    parser.add_argument("--content-mode", default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", str(DEFAULT_POLL_INTERVAL_SECONDS))))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in {"1", "true", "yes"})
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
