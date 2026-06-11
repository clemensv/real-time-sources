"""MQTT feeder application for USGS Instantaneous Values → Unified Namespace."""

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

from usgs_iv.usgs_iv import USGSDataPoller
from usgs_iv_mqtt_producer_mqtt_client.client import (
    USGSInstantaneousValuesMqttMqttClient,
    USGSSitesMqttMqttClient,
)
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
    def __init__(self, client: Any, prefix: str):
        self.producer = self
        self._client = client
        self._prefix = prefix
        self._tasks: set[asyncio.Task[None]] = set()
        self._failures: list[BaseException] = []
        self._semaphore = asyncio.Semaphore(64)

    def __getattr__(self, name: str) -> Callable[..., None]:
        if not name.startswith("send_"):
            raise AttributeError(name)
        publish_name = name.replace("send_", "publish_").replace(self._prefix, f"{self._prefix}mqtt_")
        publish: Callable[..., Awaitable[None]] = getattr(self._client, publish_name)

        async def _publish_with_limit(**kwargs: Any) -> None:
            async with self._semaphore:
                await publish(**kwargs)

        def _send(**kwargs: Any) -> None:
            kwargs.pop("flush_producer", None)
            normalized = {key[1:] if key.startswith("_") else key: value for key, value in kwargs.items()}
            task = asyncio.create_task(_publish_with_limit(**normalized))
            self._tasks.add(task)
            task.add_done_callback(self._finish_task)

        return _send

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
            pending = list(self._tasks)
            await asyncio.gather(*pending, return_exceptions=True)
        if self._failures:
            raise RuntimeError("one or more MQTT publishes failed") from self._failures[0]

async def feed(
    poller: USGSDataPoller,
    broker_host: str,
    broker_port: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    content_mode: str = "binary",
) -> None:
    site_client_id = f"{client_id or 'usgs-iv'}-sites"
    values_client_id = f"{client_id or 'usgs-iv'}-values"
    _, site_username, site_password, _entra_props = _resolve_mqtt_connection_settings(
        username=username,
        password=password or "",
        client_id=site_client_id,
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )
    _, values_username, values_password, _ = _resolve_mqtt_connection_settings(
        username=username,
        password=password or "",
        client_id=values_client_id,
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    site_paho = mqtt.Client(client_id=site_client_id, callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    values_paho = mqtt.Client(client_id=values_client_id, callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if _entra_props is None and (site_username or site_password):
        site_paho.username_pw_set(site_username, site_password)
    if _entra_props is None and (values_username or values_password):
        values_paho.username_pw_set(values_username, values_password)
    if tls or _entra_props is not None:
        site_paho.tls_set()
        values_paho.tls_set()
    site_client = USGSSitesMqttMqttClient(client=site_paho, content_mode=content_mode, loop=asyncio.get_running_loop())
    values_client = USGSInstantaneousValuesMqttMqttClient(client=values_paho, content_mode=content_mode, loop=asyncio.get_running_loop())
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    if _entra_props is not None:
        import paho.mqtt.properties as _mqtt_props_mod
        from paho.mqtt.properties import Properties as _EP
        from paho.mqtt.packettypes import PacketTypes as _PKT
        _site_props = _EP(_PKT.CONNECT); _site_props.AuthenticationMethod = "OAUTH2-JWT"; _site_props.AuthenticationData = _entra_props.AuthenticationData
        _vals_props = _EP(_PKT.CONNECT); _vals_props.AuthenticationMethod = "OAUTH2-JWT"; _vals_props.AuthenticationData = _entra_props.AuthenticationData
        site_paho.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=_site_props); site_paho.loop_start()
        values_paho.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=_vals_props); values_paho.loop_start()
    else:
        await site_client.connect(broker_host, broker_port)
        await values_client.connect(broker_host, broker_port)
    site_adapter = _MqttProducerAdapter(site_client, "usgs_sites_")
    values_adapter = _MqttProducerAdapter(values_client, "usgs_instantaneous_values_")
    poller.site_producer = site_adapter
    poller.values_producer = values_adapter
    try:
        await poller.poll_and_send()
        await site_adapter.drain()
        await values_adapter.drain()
    finally:
        await site_client.disconnect()
        await values_client.disconnect()

def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="USGS IV MQTT/UNS bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--last-polled-file", default=os.getenv("USGS_LAST_POLLED_FILE", os.path.expanduser("~/.usgs_last_polled_mqtt.json")))
    parser.add_argument("--state", default=os.getenv("USGS_STATE", ""))
    parser.add_argument("--force-site-refresh", action="store_true", default=os.getenv("USGS_FORCE_SITE_REFRESH", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--force-data-refresh", action="store_true", default=os.getenv("USGS_FORCE_DATA_REFRESH", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    poller = USGSDataPoller(
        last_polled_file=args.last_polled_file,
        state=args.state or None,
        force_site_refresh=args.force_site_refresh,
        force_data_refresh=args.force_data_refresh,
        once=args.once,
    )
    asyncio.run(feed(
        poller,
        host,
        port,
        username=args.username or None,
        password=args.password or None,
        tls=tls,
        client_id=args.client_id or None,
        content_mode=args.content_mode,
    ))
