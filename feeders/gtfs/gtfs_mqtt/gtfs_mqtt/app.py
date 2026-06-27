from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import re
from typing import Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from gtfs_core.core import DEFAULT_POLL_INTERVAL_SECONDS, DEFAULT_SCHEDULE_POLL_INTERVAL_SECONDS, load_source_configs, poll_and_publish_gtfs
from gtfs_mqtt_producer_mqtt_client.client import (
    GeneralTransitFeedRealTimeMqttMqttClient,
    GeneralTransitFeedStaticMqttMqttClient,
)

logger = logging.getLogger("gtfs_mqtt")


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
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    from paho.mqtt.properties import Properties as _MqttConnProps

    connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
    connect_props.AuthenticationMethod = "OAUTH2-JWT"
    connect_props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, connect_props


def _parse_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in {"mqtts", "ssl", "tls"}
    port = parsed.port or (8883 if tls else 1883)
    host = parsed.hostname or "localhost"
    return host, port, tls, parsed.username, parsed.password


class GtfsMqttPublisher:
    def __init__(
        self,
        realtime_client: GeneralTransitFeedRealTimeMqttMqttClient,
        static_client: GeneralTransitFeedStaticMqttMqttClient,
    ) -> None:
        self._realtime = realtime_client
        self._static = static_client

    async def flush(self) -> None:
        return None

    async def poll(self) -> None:
        return None

    def __getattr__(self, name: str):
        if hasattr(self._realtime, name):
            return getattr(self._realtime, name)
        if hasattr(self._static, name):
            return getattr(self._static, name)
        raise AttributeError(name)


async def _connect_clients(args: argparse.Namespace) -> tuple[GtfsMqttPublisher, GeneralTransitFeedRealTimeMqttMqttClient]:
    broker_host, broker_port, tls_from_url, url_user, url_password = _parse_broker_url(args.mqtt_broker_url)
    tls_enabled = args.mqtt_enable_tls or tls_from_url or broker_port == 8883
    resolved_client_id, resolved_username, resolved_password, entra_props = _resolve_mqtt_connection_settings(
        username=args.mqtt_username or url_user,
        password=args.mqtt_password or url_password,
        client_id=args.mqtt_client_id,
        auth_mode=args.mqtt_auth_mode,
    )

    paho_client = mqtt.Client(
        client_id=resolved_client_id or "",
        callback_api_version=CallbackAPIVersion.VERSION2,
        protocol=MQTTv5,
    )
    if entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls_enabled:
        paho_client.tls_set()

    realtime_client = GeneralTransitFeedRealTimeMqttMqttClient(paho_client, content_mode=args.mqtt_content_mode)
    static_client = GeneralTransitFeedStaticMqttMqttClient(paho_client, content_mode=args.mqtt_content_mode)
    # Direct paho connect: multiple generated MqttClient instances sharing one
    # paho client overwrite each other's on_connect, causing connect() timeout.
    import threading as _threading
    _connected = _threading.Event()
    def _on_connack(client, userdata, flags, reason_code, props=None):
        rc = getattr(reason_code, 'value', reason_code) if not isinstance(reason_code, int) else reason_code
        if rc == 0:
            _connected.set()
    paho_client.on_connect = _on_connack
    if entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=30, clean_start=True, properties=entra_props)
    else:
        paho_client.connect(broker_host, broker_port, keepalive=30)
    paho_client.loop_start()
    if not await asyncio.get_running_loop().run_in_executor(None, lambda: _connected.wait(30)):
        raise RuntimeError('MQTT CONNACK timeout after 30s')
    return GtfsMqttPublisher(realtime_client, static_client), realtime_client


async def _run(args: argparse.Namespace) -> None:
    source_configs = load_source_configs(
        gtfs_rt_urls=args.gtfs_rt_urls,
        gtfs_urls=args.gtfs_urls,
        mdb_source_id=args.mdb_source_id,
        agency=args.agency,
        route=args.route,
        gtfs_rt_headers=args.gtfs_rt_headers,
        gtfs_headers=args.gtfs_headers,
        sources_file=args.gtfs_sources_file,
        selector=args.gtfs_sources,
    )
    if not source_configs:
        if args.agency:
            raise ValueError("No GTFS URL or Mobility Database source ID specified")
        raise ValueError("No agency specified")
    for source_config in source_configs:
        if not source_config.get("agency"):
            raise ValueError("No agency specified")
        if not source_config.get("gtfs_urls") and not source_config.get("gtfs_rt_urls") and not source_config.get("mdb_source_id"):
            raise ValueError("No GTFS URL or Mobility Database source ID specified")
    publisher, connection_owner = await _connect_clients(args)
    try:
        tasks = [
            poll_and_publish_gtfs(
                agency_id=source_config.get("agency"),
                publisher=publisher,
                gtfs_rt_urls=source_config.get("gtfs_rt_urls"),
                gtfs_rt_headers=source_config.get("gtfs_rt_headers"),
                gtfs_urls=source_config.get("gtfs_urls"),
                gtfs_headers=source_config.get("gtfs_headers"),
                mdb_source_id=source_config.get("mdb_source_id"),
                route=source_config.get("route", "*"),
                poll_interval=args.poll_interval,
                schedule_poll_interval=args.schedule_poll_interval,
                cache_dir=args.cache_dir,
                force_schedule_refresh=args.force_schedule_refresh,
                once=args.once,
            )
            for source_config in source_configs
        ]
        if len(tasks) == 1:
            await tasks[0]
        else:
            await asyncio.gather(*tasks)
    finally:
        await connection_owner.disconnect()


def _build_parser() -> argparse.ArgumentParser:
    split_pattern = r'''(?:(?<!\\)"[^"]*"|'[^']*'|[^\s"']+)+'''
    parser = argparse.ArgumentParser(description="GTFS MQTT bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument(
        "--mqtt-broker-url",
        default=os.getenv("MQTT_BROKER_URL") or f"mqtt://{os.getenv('MQTT_HOST', 'localhost')}:{os.getenv('MQTT_PORT', '1883')}",
    )
    parser.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    parser.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    parser.add_argument("--mqtt-auth-mode", default=os.getenv("MQTT_AUTH_MODE", "password"))
    parser.add_argument("--mqtt-enable-tls", action="store_true", default=os.getenv("MQTT_TLS", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--mqtt-content-mode", choices=("structured", "binary"), default=os.getenv("MQTT_CONTENT_MODE", "structured"))
    parser.add_argument("-r", "--route", default="*" if not os.environ.get("ROUTE") else os.environ.get("ROUTE"))
    parser.add_argument("--gtfs-rt-urls", nargs="+", default=os.environ.get("GTFS_RT_URLS").split(",") if os.environ.get("GTFS_RT_URLS") else None)
    parser.add_argument("--gtfs-urls", nargs="+", default=os.environ.get("GTFS_URLS").split(",") if os.environ.get("GTFS_URLS") else None)
    parser.add_argument("-m", "--mdb-source-id", default=os.environ.get("MDB_SOURCE_ID"))
    parser.add_argument("-a", "--agency", default=os.environ.get("AGENCY"))
    parser.add_argument("--gtfs-sources-file", default=os.environ.get("GTFS_SOURCES_FILE", ""))
    parser.add_argument("--gtfs-sources", default=os.environ.get("GTFS_SOURCES", ""))
    parser.add_argument("--gtfs-rt-headers", action="append", nargs="*", default=re.findall(split_pattern, os.environ.get("GTFS_RT_HEADERS", "")) if os.environ.get("GTFS_RT_HEADERS") else None)
    parser.add_argument("--gtfs-headers", action="append", nargs="*", default=re.findall(split_pattern, os.environ.get("GTFS_HEADERS", "")) if os.environ.get("GTFS_HEADERS") else None)
    parser.add_argument("--poll-interval", type=float, default=float(os.environ.get("POLL_INTERVAL", "0")) if os.environ.get("POLL_INTERVAL") else DEFAULT_POLL_INTERVAL_SECONDS)
    parser.add_argument("--schedule-poll-interval", type=float, default=float(os.environ.get("SCHEDULE_POLL_INTERVAL", "0")) if os.environ.get("SCHEDULE_POLL_INTERVAL") else DEFAULT_SCHEDULE_POLL_INTERVAL_SECONDS)
    parser.add_argument("--cache-dir", type=str, default=os.environ.get("CACHE_DIR"))
    parser.add_argument("--log-level", type=str, default=os.environ.get("LOG_LEVEL", "INFO"), choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    parser.add_argument("--force-schedule-refresh", action="store_true", default=False)
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes", "on"))
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    logging.basicConfig(level=args.log_level.upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
