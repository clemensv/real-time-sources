"""MQTT feeder application for INPE DETER Brazil → Unified Namespace."""

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

from inpe_deter_brazil.inpe_deter_brazil import DEFAULT_PAGE_SIZE, INPEDeterPoller, SOURCE_URI, WFS_ENDPOINTS
from inpe_deter_brazil_mqtt_producer_mqtt_client.client import BRINPEDETERMqttMqttClient
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

def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls

def _parse_biomes(value: str) -> list[str]:
    requested = [item.strip().lower() for item in value.split(",") if item.strip()]
    if not requested:
        return list(WFS_ENDPOINTS.keys())
    invalid = sorted(set(requested) - set(WFS_ENDPOINTS.keys()))
    if invalid:
        raise ValueError(f"Unsupported biomes: {', '.join(invalid)}")
    return requested

async def feed(
    broker_host: str,
    broker_port: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    biomes: str = "",
    page_size: int = DEFAULT_PAGE_SIZE,
    since_date: Optional[str] = None,
    once: bool = False,
    content_mode: str = "binary",
    poll_interval_minutes: int = 10,
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

    mqtt_client = BRINPEDETERMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=asyncio.get_running_loop(),
    )
    poller = INPEDeterPoller(page_size=page_size, poll_interval_minutes=poll_interval_minutes)
    selected_biomes = _parse_biomes(biomes)

    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    if _entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=_entra_props)
        paho_client.loop_start()
    else:
        await mqtt_client.connect(broker_host, broker_port)
    try:
        while True:
            published = 0
            for biome in selected_biomes:
                features = await poller.fetch_biome(biome, since_date=since_date)
                logger.info("Fetched %d INPE DETER features for %s", len(features), biome)
                for feature in features:
                    alert = poller.parse_alert(feature, biome)
                    if alert is None:
                        continue
                    await mqtt_client.publish_br_inpe_deter_mqtt_deforestation_alert(
                        source_uri=SOURCE_URI,
                        biome=alert.biome,  # type: ignore[arg-type]
                        alert_id=alert.alert_id,
                        view_date=alert.view_date,
                        state_slug=alert.state_slug,  # type: ignore[arg-type]
                        class_slug=alert.class_slug,  # type: ignore[arg-type]
                        data=alert,  # type: ignore[arg-type]
                    )
                    published += 1
            logger.info("Published %d INPE DETER alerts to MQTT", published)
            if once:
                break
            await asyncio.sleep(max(1, poll_interval_minutes * 60))
    finally:
        await mqtt_client.disconnect()

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="INPE DETER Brazil MQTT/UNS bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--biomes", default=os.getenv("INPE_BIOMES", ""))
    parser.add_argument("--page-size", type=int, default=int(os.getenv("PAGE_SIZE", str(DEFAULT_PAGE_SIZE))))
    parser.add_argument("--since-date", default=os.getenv("SINCE_DATE", ""))
    parser.add_argument("--poll-interval-minutes", type=int, default=int(os.getenv("POLL_INTERVAL_MINUTES", "10")))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, parsed_tls = _parse_broker_url(args.broker_url)
    asyncio.run(feed(
        host,
        port,
        username=args.username or None,
        password=args.password or None,
        tls=parsed_tls,
        client_id=args.client_id or None,
        biomes=args.biomes,
        page_size=args.page_size,
        since_date=args.since_date or None,
        once=args.once,
        content_mode=args.content_mode,
        poll_interval_minutes=args.poll_interval_minutes,
    ))

if __name__ == "__main__":
    main()
