"""Wikimedia EventStreams firehose -> AMQP 1.0 bridge."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from typing import Optional
from urllib.parse import urlparse

from wikimedia_eventstreams_amqp_producer_amqp_producer.producer import WikimediaEventStreamsAmqpProducer
from wikimedia_eventstreams_amqp_producer_data import RecentChange
from wikimedia_eventstreams_core.wikimedia_eventstreams import (
    DEFAULT_USER_AGENT,
    STREAM_URL,
    iter_recentchange_payloads,
    normalize_recent_change,
)

logger = logging.getLogger(__name__)
DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


def _norm_segment(value: Optional[str]) -> str:
    if not value:
        return ""
    return str(value).strip().lower().replace("/", "_").replace("#", "_").replace("+", "_")


class _AmqpClient:
    def __init__(self, producer):
        self.producer = producer
        self._send_methods = [name for name in dir(producer) if name.startswith("send_") and not name.endswith("_batch")]

    def __getattr__(self, name: str):
        if not name.startswith("publish_"):
            raise AttributeError(name)
        send_name = f"send_{name[len('publish_') :]}"
        method = getattr(self.producer, send_name)

        async def _publish(**kwargs):
            data = kwargs.pop("data")
            kwargs.pop("qos", None)
            kwargs.pop("retain", None)
            params = set(method.__code__.co_varnames[: method.__code__.co_argcount])
            call_kwargs = {f"_{k}": v for k, v in kwargs.items() if v is not None and f"_{k}" in params}
            method(data=data, **call_kwargs)

        return _publish


class WikimediaAmqpBridge:
    def __init__(self, client: _AmqpClient, *, stream_url: str = STREAM_URL, user_agent: str = DEFAULT_USER_AGENT) -> None:
        self.client = client
        self.stream_url = stream_url
        self.user_agent = user_agent
        self._count = 0

    async def publish_event(self, payload: dict) -> bool:
        meta = payload.get("meta")
        if not isinstance(meta, dict) or meta.get("domain") == "canary":
            return False
        event_id = meta.get("id")
        event_time = meta.get("dt")
        wiki = payload.get("wiki")
        if not event_id or not event_time or not wiki:
            return False
        normalized = normalize_recent_change(payload)
        data = RecentChange.from_serializer_dict(normalized)
        await self.client.publish_wikimedia_event_streams_recent_change(
            wiki=_norm_segment(wiki),
            namespace=_norm_segment(normalized["namespace"]),
            event_id=_norm_segment(str(event_id)),
            event_time=str(event_time),
            data=data,
            qos=0,
            retain=False,
        )
        self._count += 1
        return True

    async def run(self, max_events: Optional[int] = None) -> None:
        async for payload in iter_recentchange_payloads(stream_url=self.stream_url, user_agent=self.user_agent):
            try:
                await self.publish_event(payload)
            except Exception as exc:
                logger.warning("publish failed: %s", exc)
                continue
            if max_events and self._count >= max_events:
                return


def _parse_amqp_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    return parsed.hostname or "localhost", port, tls, parsed.username or None, parsed.password or None, (parsed.path or "").lstrip("/") or None


def add_amqp_arguments(parser: argparse.ArgumentParser, default_address: str) -> None:
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", default_address))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))


def create_amqp_producer(args: argparse.Namespace, producer_cls):
    address = args.address
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_amqp_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        if path:
            address = path
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode in ("entra", "sas")
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential()
        return producer_cls(host=host, address=address, port=port, content_mode=args.content_mode, credential=credential, entra_audience=args.entra_audience, use_tls=tls)
    if args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return producer_cls(host=host, address=address, port=port, content_mode=args.content_mode, sas_key_name=args.sas_key_name, sas_key=args.sas_key, use_tls=tls)
    return producer_cls(host=host, address=address, port=port, username=username, password=password, content_mode=args.content_mode, use_tls=tls)


async def _emit_mock_amqp(client: _AmqpClient) -> None:
    """Emit synthetic RecentChange events for deterministic E2E testing."""
    from datetime import datetime, timezone
    for i in range(4):
        data = RecentChange.from_serializer_dict({
            "wiki": "enwiki",
            "type": "edit",
            "namespace": "0",
            "title": f"Mock_Article_{i}",
            "comment": "mock edit",
            "user": "MockUser",
            "bot": False,
            "minor": False,
            "patrolled": False,
            "length_old": 100 + i,
            "length_new": 110 + i,
            "revision_old": 1000 + i,
            "revision_new": 1001 + i,
            "server_url": "https://en.wikipedia.org",
            "server_name": "en.wikipedia.org",
            "event_id": f"mock-{i:08d}",
            "event_time": datetime(2024, 1, 1, 0, 0, i, tzinfo=timezone.utc).isoformat(),
        })
        await client.publish_wikimedia_event_streams_recent_change(
            wiki="enwiki",
            namespace="0",
            event_id=f"mock-{i:08d}",
            event_time=datetime(2024, 1, 1, 0, 0, i, tzinfo=timezone.utc).isoformat(),
            data=data,
            qos=0,
            retain=False,
        )
    import time
    time.sleep(1)
    logger.info("Mock mode: emitted 4 synthetic RecentChange events via AMQP")


async def _run(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args, WikimediaEventStreamsAmqpProducer)
    client = _AmqpClient(producer)
    try:
        if getattr(args, 'mock', False):
            await _emit_mock_amqp(client)
        else:
            await WikimediaAmqpBridge(client, stream_url=args.stream_url, user_agent=args.user_agent).run(max_events=args.max_events)
    finally:
        producer.close()


def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(description="Wikimedia EventStreams -> AMQP 1.0 bridge")
    sub = p.add_subparsers(dest="command")
    feed = sub.add_parser("feed", help="Stream Wikimedia recentchange to AMQP")
    add_amqp_arguments(feed, "wikimedia-eventstreams")
    feed.add_argument("--stream-url", default=os.getenv("WIKIMEDIA_EVENTSTREAMS_URL", STREAM_URL))
    feed.add_argument("--user-agent", default=os.getenv("WIKIMEDIA_EVENTSTREAMS_USER_AGENT", DEFAULT_USER_AGENT))
    feed.add_argument("--max-events", type=int, default=int(os.getenv("WIKIMEDIA_EVENTSTREAMS_MAX_EVENTS", "0")) or None)
    feed.add_argument("--mock", action="store_true", default=os.getenv("WIKIMEDIA_EVENTSTREAMS_MOCK", "").lower() in ("1", "true", "yes"))
    args = p.parse_args()
    if args.command != "feed":
        p.print_help()
        sys.exit(1)
    try:
        asyncio.run(_run(args))
    except KeyboardInterrupt:
        logger.info("Shutting down")


if __name__ == "__main__":
    main()
