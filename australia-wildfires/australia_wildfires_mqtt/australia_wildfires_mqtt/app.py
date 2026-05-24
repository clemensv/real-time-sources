"""MQTT feeder application for Australian wildfires → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
import logging
import os
import re
import unicodedata
from typing import Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from australia_wildfires.australia_wildfires import AustraliaWildfiresAPI
from australia_wildfires_mqtt_producer_data import FireIncident as MqttFireIncident
from australia_wildfires_mqtt_producer_mqtt_client.client import AUGovEmergencyWildfiresMqttMqttClient

logger = logging.getLogger(__name__)


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls


def topic_slug(value: object, default: str = "unknown") -> str:
    text = str(value or "").strip()
    if not text:
        return default
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return slug or default


def topic_safe_id(value: object, default: str = "unknown") -> str:
    text = str(value or "").strip()
    if not text:
        return default
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", normalized).strip("-._")
    return safe or default


def _to_mqtt_incident(incident) -> MqttFireIncident:
    payload = dataclasses.asdict(incident)
    payload["state"] = topic_slug(payload.get("state"))
    payload["status"] = topic_slug(payload.get("status"))
    payload["incident_id"] = topic_safe_id(payload.get("incident_id"))
    return MqttFireIncident(**payload)


async def feed(
    broker_host: str,
    broker_port: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    once: bool = False,
    content_mode: str = "binary",
    polling_interval: int = 300,
) -> None:
    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=client_id or "",
        protocol=MQTTv5,
    )
    if username:
        paho_client.username_pw_set(username, password or "")
    if tls:
        paho_client.tls_set()

    mqtt_client = AUGovEmergencyWildfiresMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=asyncio.get_running_loop(),
    )
    api = AustraliaWildfiresAPI(polling_interval=polling_interval)

    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await mqtt_client.connect(broker_host, broker_port)
    try:
        while True:
            if os.getenv("AUSTRALIA_WILDFIRES_SAMPLE_MODE", "").lower() in ("1", "true", "yes"):
                incidents = [MqttFireIncident(
                    incident_id="sample-incident-001",
                    state="nsw",
                    title="Sample Fire Incident",
                    alert_level="Advice",
                    status="under-control",
                    location="Sample Location, NSW",
                    latitude=-33.0,
                    longitude=151.0,
                    size_hectares=10.5,
                    type="Bush Fire",
                    responsible_agency="Rural Fire Service",
                    updated="2026-01-01T00:00:00+00:00",
                    source_url="https://www.rfs.nsw.gov.au/feeds/majorIncidents.json",
                )]
            else:
                incidents = []
                incidents.extend(_to_mqtt_incident(item) for item in api.fetch_nsw_incidents())
                incidents.extend(_to_mqtt_incident(item) for item in api.fetch_vic_incidents())
                incidents.extend(_to_mqtt_incident(item) for item in api.fetch_qld_incidents())
            published = 0
            for mqtt_incident in incidents:
                await mqtt_client.publish_au_gov_emergency_wildfires_mqtt_fire_incident(
                    state=mqtt_incident.state,
                    incident_id=mqtt_incident.incident_id,
                    status=mqtt_incident.status,
                    data=mqtt_incident,
                )
                published += 1
            logger.info("Published %d Australian wildfire incidents to MQTT", published)
            if once:
                break
            await asyncio.sleep(max(1, polling_interval))
    finally:
        await mqtt_client.disconnect()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Australian wildfires MQTT/UNS bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "300")))
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
        once=args.once,
        content_mode=args.content_mode,
        polling_interval=args.polling_interval,
    ))


if __name__ == "__main__":
    main()
