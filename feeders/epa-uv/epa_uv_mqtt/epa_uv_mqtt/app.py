"""MQTT feeder application for EPA UV Index → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from typing import Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from epa_uv.epa_uv import DEFAULT_POLL_INTERVAL_SECONDS, EPAUVBridge, parse_locations
from epa_uv_mqtt_producer_mqtt_client.client import USEPAUVIndexMqttMqttClient
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
        return resolved_client_id, str(username or ""), str(password or ""), None

    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    resolved_username = resolved_client_id or str(username or "").strip()
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")

    resolved_password = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    from paho.mqtt.properties import Properties as _MqttConnProps
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    _connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
    _connect_props.AuthenticationMethod = "OAUTH2-JWT"
    _connect_props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, _connect_props

logger = logging.getLogger(__name__)

async def feed(
    bridge: EPAUVBridge,
    broker_host: str,
    broker_port: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    once: bool = False,
    content_mode: str = "binary",
) -> None:
    resolved_client_id, resolved_username, resolved_password, _entra_props = _resolve_mqtt_connection_settings(
        username=username,
        password=password or "",
        client_id=client_id or "",
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho_client = mqtt.Client(client_id=resolved_client_id or "", 
        callback_api_version=CallbackAPIVersion.VERSION2,
        protocol=MQTTv5,
    )
    if _entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls or _entra_props is not None:
        paho_client.tls_set()

    mqtt_client = USEPAUVIndexMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=asyncio.get_running_loop(),
    )
    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    if _entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=_entra_props)
        paho_client.loop_start()
    else:
        await mqtt_client.connect(broker_host, broker_port)
    try:
        while True:
            hourly_sent = 0
            daily_sent = 0
            for city, state in bridge.locations:
                for hourly in bridge.fetch_hourly(city, state):
                    event_id = f"{hourly.location_id}|{hourly.forecast_datetime}"
                    if event_id in bridge.seen_hourly_ids:
                        continue
                    await mqtt_client.publish_us_epa_uvindex_mqtt_hourly_forecast(
                        location_id=hourly.location_id,
                        state=hourly.state,
                        city_slug=hourly.city_slug,
                        forecast_hour=hourly.forecast_hour,
                        data=hourly,
                    )
                    bridge._remember(bridge.hourly_order, bridge.seen_hourly_ids, event_id)
                    hourly_sent += 1
                for daily in bridge.fetch_daily(city, state):
                    event_id = f"{daily.location_id}|{daily.forecast_date}"
                    if event_id in bridge.seen_daily_ids:
                        continue
                    await mqtt_client.publish_us_epa_uvindex_mqtt_daily_forecast(
                        location_id=daily.location_id,
                        state=daily.state,
                        city_slug=daily.city_slug,
                        forecast_date=daily.forecast_date,
                        data=daily,
                    )
                    bridge._remember(bridge.daily_order, bridge.seen_daily_ids, event_id)
                    daily_sent += 1
            bridge.save_state()
            logger.info("Published %d hourly forecasts and %d daily forecasts", hourly_sent, daily_sent)
            if once:
                break
            await asyncio.sleep(DEFAULT_POLL_INTERVAL_SECONDS)
    finally:
        await mqtt_client.disconnect()

def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="EPA UV MQTT/UNS bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--locations", default=os.getenv("EPA_UV_LOCATIONS", "Seattle,WA"))
    parser.add_argument("--state-file", default=os.getenv("EPA_UV_STATE_FILE", ""))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    bridge = EPAUVBridge(parse_locations(args.locations), state_file=args.state_file)
    asyncio.run(feed(
        bridge,
        host,
        port,
        username=args.username or None,
        password=args.password or None,
        tls=tls,
        client_id=args.client_id or None,
        once=args.once,
        content_mode=args.content_mode,
    ))
