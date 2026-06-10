"""MQTT feeder application for Paris bicycle counters → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
from datetime import datetime, timezone, timedelta
from typing import Optional, Set
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from paris_bicycle_counters.paris_bicycle_counters import ParisBicycleCounterPoller
from paris_bicycle_counters_mqtt_producer_mqtt_client.client import FRParisOpenDataVeloMqttMqttClient

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

logger = logging.getLogger(__name__)

class ParisBicycleCounterMqttPoller(ParisBicycleCounterPoller):
    def __init__(self, mqtt_client: FRParisOpenDataVeloMqttMqttClient, last_polled_file: str):
        self.kafka_topic = ""
        self.last_polled_file = last_polled_file
        self.producer = mqtt_client

    async def poll_and_send_async(self, once: bool = False) -> None:
        logger.info("Starting Paris Bicycle Counter MQTT poller (once=%s)", once)
        while True:
            counters = self.fetch_counter_locations()
            for counter in counters:
                await self.producer.publish_fr_paris_open_data_velo_mqtt_counter(
                    counter_id=counter.counter_id,
                    ce_id=counter.ce_id,
                    data=counter,
                )
            logger.info("Published %d retained counter info records", len(counters))

            state = self.load_state()
            seen_keys: Set[str] = set(state.get("seen_keys", []))
            since = datetime.now(timezone.utc) - timedelta(days=7)
            counts = self.fetch_bicycle_counts(since=since)
            new_counts, seen_keys = self.dedup_counts(counts, seen_keys)
            for count in new_counts:
                await self.producer.publish_fr_paris_open_data_velo_mqtt_bicycle_count(
                    counter_id=count.counter_id,
                    ce_id=count.ce_id,
                    date=count.date.isoformat().replace("+00:00", "Z") if hasattr(count.date, "isoformat") else str(count.date),
                    data=count,
                )

            cutoff = datetime.now(timezone.utc) - timedelta(days=14)
            trimmed_keys: Set[str] = set()
            for key in seen_keys:
                try:
                    date_part = key.split("|", 1)[1]
                    dt = datetime.fromisoformat(date_part)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    if dt >= cutoff:
                        trimmed_keys.add(key)
                except (IndexError, ValueError):
                    trimmed_keys.add(key)
            state["seen_keys"] = list(trimmed_keys)
            self.save_state(state)
            logger.info("Polled %d count records, published %d new count events", len(counts), len(new_counts))

            if once:
                return
            await asyncio.sleep(self.POLL_INTERVAL_SECONDS)

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
    resolved_client_id, resolved_username, resolved_password = _resolve_mqtt_connection_settings(
        username=username,
        password=password or "",
        client_id=client_id or "",
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

    mqtt_client = FRParisOpenDataVeloMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=asyncio.get_running_loop(),
    )
    await mqtt_client.connect(broker_host, broker_port)
    try:
        poller = ParisBicycleCounterMqttPoller(
            mqtt_client,
            state_file or os.path.expanduser("~/.paris_bicycle_counters_mqtt_state.json"),
        )
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
    parser = argparse.ArgumentParser(description="Paris bicycle counters MQTT/UNS bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--state-file", default=os.getenv("PARIS_BICYCLE_COUNTERS_MQTT_STATE_FILE", os.getenv("STATE_FILE", "")))
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
