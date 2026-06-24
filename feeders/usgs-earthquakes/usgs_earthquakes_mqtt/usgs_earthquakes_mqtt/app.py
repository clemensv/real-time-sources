"""MQTT feeder application for USGS Earthquakes → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from typing import Any, Awaitable, Callable, Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from usgs_earthquakes.usgs_earthquakes import DEFAULT_FEED, USGSEarthquakePoller
from usgs_earthquakes_mqtt_producer_mqtt_client.client import USGSEarthquakesMqttMqttClient
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
    resolved_client_id, resolved_username, resolved_password, _entra_props = _resolve_mqtt_connection_settings(
        username=username,
        password=password or "",
        client_id=client_id or "",
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho_client = mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if _entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls or _entra_props is not None:
        paho_client.tls_set()
    mqtt_client = USGSEarthquakesMqttMqttClient(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    if _entra_props is not None:
        import threading as _threading
        _connected = _threading.Event()
        def _on_connack(client, userdata, flags, reason_code, props=None):
            if (reason_code if isinstance(reason_code, int) else reason_code.value) == 0:
                _connected.set()
        paho_client.on_connect = _on_connack
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=_entra_props)
        paho_client.loop_start()
        if not await asyncio.get_running_loop().run_in_executor(None, lambda: _connected.wait(30)):
            raise RuntimeError('MQTT CONNACK timeout after 30s')
    else:
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
    parser.add_argument(
        "--last-polled-file",
        default=os.getenv("USGS_EARTHQUAKES_LAST_POLLED_FILE", os.path.expanduser("~/.usgs_earthquakes_seen_mqtt.json")),
        help="Path to the persisted checkpoint and dedupe state file for the USGS Earthquakes MQTT bridge.",
    )
    parser.add_argument(
        "--feed",
        default=os.getenv("USGS_EARTHQUAKES_FEED", DEFAULT_FEED),
        help="USGS GeoJSON summary feed to poll, for example all_hour, all_day, or significant_month.",
    )
    parser.add_argument(
        "--min-magnitude",
        type=float,
        default=float(os.getenv("USGS_EARTHQUAKES_MIN_MAGNITUDE", "0")) if os.getenv("USGS_EARTHQUAKES_MIN_MAGNITUDE") else None,
        help="Optional minimum magnitude filter applied before publishing events.",
    )
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
