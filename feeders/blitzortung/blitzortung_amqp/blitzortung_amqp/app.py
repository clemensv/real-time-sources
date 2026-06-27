"""Blitzortung lightning firehose -> AMQP 1.0 bridge."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Any, Optional
from urllib.parse import urlparse

import websockets

from blitzortung_amqp_producer_amqp_producer.producer import BlitzortungLightningAmqpProducer
from blitzortung_amqp_producer_data import LightningStroke
from blitzortung_core.blitzortung import DEFAULT_BBOX, DEFAULT_USER_AGENT, DEFAULT_WS_URLS, normalize_stroke

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
        send_name = f"send_{name[len('publish_') :]}"
        for producer in self._producers:
            target = getattr(producer, send_name, None)
            if target is not None:
                break
        else:
            raise AttributeError(send_name)

        async def _publish(**kwargs):
            accepted = set(target.__code__.co_varnames[: target.__code__.co_argcount])
            call = {}
            for key, value in kwargs.items():
                if key in ("data", "content_type"):
                    call[key] = value
                elif key in ("flush_producer", "qos", "retain", "time", "_time"):
                    continue
                else:
                    candidate = "_" + key.lstrip("_")
                    if candidate in accepted:
                        call[candidate] = value
            target(**call)

        return _publish


def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as exc:  # pragma: no cover - defensive
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...", attempt + 1, max_attempts, exc, delay)
            import time

            time.sleep(delay)


def _build_publisher(*, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username, password, entra_audience: str, entra_client_id, sas_key_name, sas_key):
    producers = []
    for cls in (BlitzortungLightningAmqpProducer,):
        if auth_mode == "entra":
            from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

            credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
            producer = _retry_producer_init(
                lambda: cls(
                    host=host,
                    address=address,
                    port=port,
                    content_mode=content_mode,  # type: ignore[arg-type]
                    credential=credential,
                    entra_audience=entra_audience,
                    use_tls=use_tls,
                )
            )
        elif auth_mode == "sas":
            if not sas_key_name or not sas_key:
                raise RuntimeError("AMQP_AUTH_MODE=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
            producer = _retry_producer_init(
                lambda: cls(
                    host=host,
                    address=address,
                    port=port,
                    content_mode=content_mode,  # type: ignore[arg-type]
                    sas_key_name=sas_key_name,
                    sas_key=sas_key,
                    use_tls=use_tls,
                )
            )
        else:
            producer = _retry_producer_init(
                lambda: cls(
                    host=host,
                    address=address,
                    port=port,
                    username=username,
                    password=password,
                    content_mode=content_mode,  # type: ignore[arg-type]
                    use_tls=use_tls,
                )
            )
        producers.append(producer)
    return _AmqpPublishFacade(producers)


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


class BlitzortungAmqpBridge:
    def __init__(self, client: _AmqpPublishFacade, *, ws_urls=DEFAULT_WS_URLS, bbox=DEFAULT_BBOX, user_agent: str = DEFAULT_USER_AGENT) -> None:
        self.client = client
        self.ws_urls = list(ws_urls)
        self.bbox = bbox
        self.user_agent = user_agent
        self._count = 0

    async def run(self, max_events: Optional[int] = None) -> None:
        bbox_msg = json.dumps({"west": self.bbox[3], "east": self.bbox[1], "north": self.bbox[0], "south": self.bbox[2], "limit": 0})
        retry_delay = 1
        max_retry_delay = 60
        url_idx = 0
        while True:
            url = self.ws_urls[url_idx % len(self.ws_urls)]
            try:
                async with websockets.connect(url, user_agent_header=self.user_agent, max_size=2**22) as ws:
                    await ws.send(bbox_msg)
                    logger.info("Connected to Blitzortung WS at %s", url)
                    retry_delay = 1
                    async for raw in ws:
                        try:
                            envelope = json.loads(raw)
                        except (TypeError, ValueError):
                            continue
                        await self._dispatch_envelope(envelope)
                        if max_events and self._count >= max_events:
                            return
            except (asyncio.CancelledError, KeyboardInterrupt):
                raise
            except Exception as exc:
                logger.error("Blitzortung WS error: %s. Retrying in %ds", exc, retry_delay)
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, max_retry_delay)
                url_idx += 1

    async def _dispatch_envelope(self, envelope: Any) -> None:
        if isinstance(envelope, dict) and isinstance(envelope.get("strokes"), list):
            for raw in envelope["strokes"]:
                await self._publish_one(raw)
        elif isinstance(envelope, dict):
            await self._publish_one(envelope)
        elif isinstance(envelope, list):
            for raw in envelope:
                await self._publish_one(raw)

    async def _publish_one(self, raw: dict[str, Any]) -> None:
        try:
            data = LightningStroke.from_serializer_dict(normalize_stroke(raw))
        except (KeyError, TypeError, ValueError):
            return
        await self.client.publish_blitzortung_lightning_lightning_stroke(
            source_id=str(data.source_id),
            geohash5=data.geohash5,
            geohash7=data.geohash7,
            stroke_id=data.stroke_id,
            time=data.event_time,
            data=data,
            qos=0,
            retain=False,
        )
        self._count += 1


async def _emit_mock(producer) -> None:
    """Emit synthetic lightning strokes for deterministic E2E testing."""
    from datetime import datetime, timezone
    base_time_ms = int(datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)
    for index in range(3):
        stroke_raw = {
            "src": 1,
            "id": 9_000_000_000 + index,
            "time": base_time_ms + index,
            "lat": 50.0 + index * 0.1,
            "lon": 8.0 + index * 0.1,
            "srv": 1,
            "del": 0,
            "dev": 1000.0,
            "sta": {"100": 0, "101": 1},
        }
        data = LightningStroke.from_serializer_dict(normalize_stroke(stroke_raw))
        await producer.publish_blitzortung_lightning_lightning_stroke(
            source_id=str(data.source_id),
            geohash5=data.geohash5,
            geohash7=data.geohash7,
            stroke_id=data.stroke_id,
            time=data.event_time,
            data=data,
        )
    logger.info("Mock mode: emitted 3 synthetic Blitzortung strokes via AMQP")


async def _run(args: argparse.Namespace) -> None:
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
    producer = _build_publisher(
        host=host,
        port=port,
        address=address,
        use_tls=tls,
        content_mode=args.content_mode,
        auth_mode=args.auth_mode,
        username=username,
        password=password,
        entra_audience=args.entra_audience,
        entra_client_id=args.entra_client_id,
        sas_key_name=args.sas_key_name,
        sas_key=args.sas_key,
    )
    try:
        if getattr(args, 'mock', False):
            await _emit_mock(producer)
        else:
            await BlitzortungAmqpBridge(producer).run(max_events=args.max_events)
    finally:
        producer.close()


def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(description="Blitzortung -> AMQP 1.0 bridge")
    sub = p.add_subparsers(dest="command")
    feed = sub.add_parser("feed", help="Stream Blitzortung strokes to AMQP")
    add_amqp_arguments(feed, "blitzortung")
    feed.add_argument("--max-events", type=int, default=int(os.getenv("BLITZORTUNG_MAX_EVENTS", "0")) or None)
    feed.add_argument("--mock", action="store_true", default=os.getenv("BLITZORTUNG_MOCK", "").lower() in ("1", "true", "yes"))
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
