"""MQTT feeder application for USGS Earthquakes → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from typing import Any, Awaitable, Callable, Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from usgs_earthquakes.usgs_earthquakes import DEFAULT_FEED, USGSEarthquakePoller
from usgs_earthquakes_mqtt_producer_mqtt_client.client import USGSEarthquakesMqttMqttClient

logger = logging.getLogger(__name__)


class _MqttProducerAdapter:
    def __init__(self, client: USGSEarthquakesMqttMqttClient):
        self.producer = self
        self._client = client
        self._tasks: set[asyncio.Task[None]] = set()
        self._failures: list[BaseException] = []
        self._semaphore = asyncio.Semaphore(64)

    def send_usgs_earthquakes_event(self, **kwargs: Any) -> None:
        kwargs.pop("flush_producer", None)
        data = kwargs["data"]
        normalized = {key[1:] if key.startswith("_") else key: value for key, value in kwargs.items()}
        normalized["magnitude_bucket"] = data.magnitude_bucket
        task = asyncio.create_task(self._publish(**normalized))
        self._tasks.add(task)
        task.add_done_callback(self._finish_task)

    async def _publish(self, **kwargs: Any) -> None:
        async with self._semaphore:
            await self._client.publish_usgs_earthquakes_mqtt_event(**kwargs)

    def _finish_task(self, task: asyncio.Task[None]) -> None:
        self._tasks.discard(task)
        try:
            task.result()
        except BaseException as exc:  # pylint: disable=broad-except
            self._failures.append(exc)
            logger.exception("MQTT publish failed", exc_info=exc)

    def flush(self) -> Awaitable[None]:
        return self.drain()

    async def drain(self) -> None:
        while self._tasks:
            await asyncio.gather(*list(self._tasks), return_exceptions=True)
        if self._failures:
            raise RuntimeError("one or more MQTT publishes failed") from self._failures[0]


async def feed(poller: USGSEarthquakePoller, broker_host: str, broker_port: int, *, username: Optional[str] = None, password: Optional[str] = None, tls: bool = False, client_id: Optional[str] = None, content_mode: str = "binary", once: bool = False) -> None:
    paho_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=client_id or "", protocol=MQTTv5)
    if username:
        paho_client.username_pw_set(username, password or "")
    if tls:
        paho_client.tls_set()
    mqtt_client = USGSEarthquakesMqttMqttClient(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
    await mqtt_client.connect(broker_host, broker_port)
    adapter = _MqttProducerAdapter(mqtt_client)
    poller.event_producer = adapter
    try:
        await poller.poll_and_send(once=once)
        await adapter.drain()
    finally:
        await mqtt_client.disconnect()


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="USGS Earthquakes MQTT/UNS bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--last-polled-file", default=os.getenv("USGS_EARTHQUAKES_LAST_POLLED_FILE", os.path.expanduser("~/.usgs_earthquakes_seen_mqtt.json")))
    parser.add_argument("--feed", default=os.getenv("USGS_EARTHQUAKES_FEED", DEFAULT_FEED))
    parser.add_argument("--min-magnitude", type=float, default=float(os.getenv("USGS_EARTHQUAKES_MIN_MAGNITUDE")) if os.getenv("USGS_EARTHQUAKES_MIN_MAGNITUDE") else None)
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    poller = USGSEarthquakePoller(last_polled_file=args.last_polled_file, feed=args.feed, min_magnitude=args.min_magnitude)
    asyncio.run(feed(poller, host, port, username=args.username or None, password=args.password or None, tls=tls, client_id=args.client_id or None, content_mode=args.content_mode, once=args.once))
