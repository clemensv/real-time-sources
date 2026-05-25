"""AMQP feeder application for JMA Bosai earthquakes → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import time
from typing import Optional
from urllib.parse import urlparse

import requests

from jma_bosai_quake.jma_bosai_quake import (
    DEFAULT_STATE_FILE,
    LIST_URL,
    SUPPORTED_BULLETIN_TYPES,
    JmaBosaiQuakeAPI,
    bulletin_type_from_filename,
)
from jma_bosai_quake_amqp_producer_amqp_producer.producer import JPJMAQuakeAmqpProducer

logger = logging.getLogger(__name__)



DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


class _AmqpPublishFacade:
    def __init__(self, producers):
        self._producers = list(producers)

    def close(self):
        for producer in self._producers:
            close = getattr(producer, "close", None)
            if close is not None:
                close()

    def __getattr__(self, name: str):
        if not name.startswith("publish_"):
            raise AttributeError(name)
        suffix = name.split("_mqtt_", 1)[1] if "_mqtt_" in name else name[len("publish_"):]
        target = None
        for producer in self._producers:
            target = getattr(producer, f"send_{suffix}", None)
            if target is not None:
                break
        if target is None:
            raise AttributeError(f"send_{suffix}")

        async def _publish(**kwargs):
            accepted = set(target.__code__.co_varnames[:target.__code__.co_argcount])
            call = {}
            for key, value in kwargs.items():
                if key in ("data", "content_type"):
                    call[key] = value
                elif key in ("flush_producer", "qos", "retain"):
                    continue
                else:
                    candidate = "_" + key.lstrip("_")
                    if candidate in accepted:
                        call[candidate] = value
            target(**call)

        return _publish


def _build_publisher(*, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username, password, entra_audience: str, entra_client_id, sas_key_name, sas_key):
    producers = []
    for cls in (JPJMAQuakeAmqpProducer,):
        if auth_mode == "entra":
            from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
            credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
            producer = cls(host=host, address=address, port=port, content_mode=content_mode, credential=credential, entra_audience=entra_audience, use_tls=use_tls)
        elif auth_mode == "sas":
            if not sas_key_name or not sas_key:
                raise RuntimeError("AMQP_AUTH_MODE=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
            producer = cls(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)
        else:
            producer = cls(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=use_tls)
        producers.append(producer)
    return _AmqpPublishFacade(producers)


async def _publish_once(api: JmaBosaiQuakeAPI, mqtt_client: JPJMAQuakeMqttMqttClient) -> int:
    reports = api.list_reports()
    pending_keys: list[tuple[str, int]] = []
    emitted = 0
    for entry in reversed(reports):
        bulletin_type = bulletin_type_from_filename(entry.get("json"))
        if bulletin_type not in SUPPORTED_BULLETIN_TYPES:
            logger.warning("Skipping unsupported JMA earthquake bulletin type %s from %s", bulletin_type or "<missing>", entry.get("json"))
            continue
        key = api.state_key(entry)
        if key in api.seen:
            continue
        detail = None
        try:
            detail = api.fetch_detail(entry.get("json", ""))
        except requests.RequestException as exc:
            logger.warning("Detail fetch failed for %s: %s", entry.get("json"), exc)
        try:
            data = api.normalize_report(entry, detail)
            await mqtt_client.publish_jp_jma_quake_mqtt_earthquake_report(
                feedurl=LIST_URL,
                prefecture=data.prefecture,
                magnitude_bucket=data.magnitude_bucket,
                event_id=data.event_id,
                serial=str(data.serial),
                data=data,
            )
            pending_keys.append(key)
            emitted += 1
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Skipping malformed earthquake report %s: %s", entry.get("eid"), exc)
    if pending_keys:
        api.mark_seen(pending_keys)
    return emitted


async def feed(
    api: JmaBosaiQuakeAPI,
    broker_host: str,
    broker_port: int,
    *,
    polling_interval: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    content_mode: str = "binary",
    once: bool = False,
) -> None:
    mqtt_client = _build_publisher(
        host=broker_host, port=broker_port, address=os.getenv("AMQP_ADDRESS", "jma-bosai-quake"),
        use_tls=tls, content_mode=content_mode, auth_mode=os.getenv("AMQP_AUTH_MODE", "password"),
        username=username, password=password,
        entra_audience=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS),
        entra_client_id=os.getenv("AMQP_ENTRA_CLIENT_ID"),
        sas_key_name=os.getenv("AMQP_SAS_KEY_NAME"), sas_key=os.getenv("AMQP_SAS_KEY"),
    )
    try:
        while True:
            started = time.monotonic()
            count = await _publish_once(api, mqtt_client)
            logger.info("Published %d JMA earthquake report(s)", count)
            if once:
                break
            await asyncio.sleep(max(0, polling_interval - (time.monotonic() - started)))
    finally:
        mqtt_client.close()


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="JMA Bosai earthquake AMQP 1.0 bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL", "amqp://localhost:5672"))
    parser.add_argument("--state-file", default=os.getenv("JMA_BOSAI_QUAKE_AMQP_STATE_FILE", os.getenv("STATE_FILE", DEFAULT_STATE_FILE)))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "60")))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("AMQP_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    api = JmaBosaiQuakeAPI(state_file=args.state_file)
    logger.info("Polling %s and publishing to AMQP %s:%d", LIST_URL, host, port)
    asyncio.run(feed(api, host, port, polling_interval=args.polling_interval, username=args.username or None, password=args.password or None, tls=tls, client_id=args.client_id or None, content_mode=args.content_mode, once=args.once))
