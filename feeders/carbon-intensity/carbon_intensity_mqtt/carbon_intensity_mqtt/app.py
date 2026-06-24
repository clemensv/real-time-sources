"""MQTT feeder application for Carbon Intensity UK → Unified Namespace."""

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

from carbon_intensity.carbon_intensity import CarbonIntensityPoller, POLL_INTERVAL_SECONDS
from carbon_intensity_mqtt_producer_mqtt_client.client import UkOrgCarbonintensityMqttMqttClient
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

def _ce_timestamp(value) -> str:
    return value.isoformat().replace("+00:00", "Z")

class CarbonIntensityMqttPoller(CarbonIntensityPoller):
    """Carbon Intensity poller that emits MQTT/UNS CloudEvents."""

    def __init__(self, mqtt_client: UkOrgCarbonintensityMqttMqttClient, last_polled_file: str):
        self.kafka_topic = ""
        self.last_polled_file = last_polled_file
        self.producer = mqtt_client
        self.regional_producer = mqtt_client

    def emit_intensity(self, intensity):
        raise NotImplementedError("use emit_intensity_async")

    def emit_generation_mix(self, gen_mix):
        raise NotImplementedError("use emit_generation_mix_async")

    def emit_regional(self, regional):
        raise NotImplementedError("use emit_regional_async")

    async def emit_intensity_async(self, intensity) -> None:
        await self.producer.publish_uk_org_carbonintensity_mqtt_intensity(  # type: ignore[attr-defined]
            period_from=_ce_timestamp(intensity.period_from),
            ce_id=intensity.ce_id,
            region=intensity.region,
            data=intensity,
        )

    async def emit_generation_mix_async(self, gen_mix) -> None:
        await self.producer.publish_uk_org_carbonintensity_mqtt_generation_mix(  # type: ignore[attr-defined]
            period_from=_ce_timestamp(gen_mix.period_from),
            ce_id=gen_mix.ce_id,
            region=gen_mix.region,
            data=gen_mix,
        )

    async def emit_regional_async(self, regional) -> None:
        await self.producer.publish_uk_org_carbonintensity_mqtt_regional_intensity(  # type: ignore[attr-defined]
            region_id=str(regional.region_id),
            ce_id=regional.ce_id,
            region=regional.region,
            data=regional,
        )

    async def poll_once_async(self) -> Optional[str]:
        intensity_data = self.fetch_intensity()
        generation_data = self.fetch_generation()
        regional_data = self.fetch_regional()

        emitted_key = None

        if intensity_data:
            intensity = self.parse_intensity(intensity_data)
            if intensity:
                await self.emit_intensity_async(intensity)
                emitted_key = intensity.period_from.isoformat()
                logger.info("Emitted intensity for %s", emitted_key)

        if generation_data:
            gen_mix = self.parse_generation(generation_data)
            if gen_mix:
                await self.emit_generation_mix_async(gen_mix)
                logger.info("Emitted generation mix for %s", gen_mix.period_from.isoformat())

        if regional_data:
            regionals = self.parse_regional(regional_data)
            for region in regionals:
                await self.emit_regional_async(region)
            if regionals:
                logger.info("Emitted %d regional intensity records", len(regionals))

        return emitted_key

    async def poll_and_send_async(self, once: bool = False) -> None:
        state = self.load_state()
        last_period = state.get("last_period_from")
        logger.info("Starting Carbon Intensity MQTT poller (last_period=%s, once=%s)", last_period, once)

        while True:
            try:
                emitted_key = await self.poll_once_async()
                if emitted_key and emitted_key != last_period:
                    last_period = emitted_key
                    state["last_period_from"] = last_period
                    self.save_state(state)
            except Exception:
                logger.exception("Error during poll cycle")

            if once:
                logger.info("--once mode: exiting after first polling cycle")
                return

            logger.info("Sleeping %ss until next poll", POLL_INTERVAL_SECONDS)
            await asyncio.sleep(POLL_INTERVAL_SECONDS)

async def feed(
    broker_host: str,
    broker_port: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    state_file: str = "",
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

    mqtt_client = UkOrgCarbonintensityMqttMqttClient(
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
        poller = CarbonIntensityMqttPoller(mqtt_client, state_file or os.path.expanduser("~/.carbon_intensity_mqtt_last_polled.json"))
        await poller.poll_and_send_async(once=once)
    finally:
        await mqtt_client.disconnect()

def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Carbon Intensity MQTT/UNS bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--state-file", default=os.getenv("CARBON_INTENSITY_MQTT_STATE_FILE", os.getenv("STATE_FILE", "")))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    asyncio.run(feed(
        host,
        port,
        username=args.username or None,
        password=args.password or None,
        tls=tls,
        client_id=args.client_id or None,
        state_file=args.state_file,
        once=args.once,
        content_mode=args.content_mode,
    ))
