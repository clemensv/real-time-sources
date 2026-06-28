"""AISstream.io firehose -> AMQP 1.0 bridge."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from typing import Optional
from urllib.parse import urlparse

from aisstream_core import AIS_MESSAGE_TYPES, AisStreamBridge, mock_envelopes
import aisstream_amqp_producer_data as _amqp_data
from aisstream_amqp_producer_amqp_producer.producer import IOAISstreamAmqpProducer

logger = logging.getLogger("aisstream_amqp")
DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"

# Upstream MessageType -> (raw data class, AMQP send method). The AMQP transport
# carries the same 23 raw AIS types as Kafka, keyed identically by UserID.
_AMQP_DISPATCH = {
    mt: (getattr(_amqp_data, mt), f"send_{suffix}")
    for mt, suffix in AIS_MESSAGE_TYPES
}


def _parse_amqp_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    return parsed.hostname or "localhost", port, tls, parsed.username or None, parsed.password or None, (parsed.path or "").lstrip("/") or None


def _build_amqp_producer(producer_cls, *, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username: Optional[str], password: Optional[str], entra_audience: str, entra_client_id: Optional[str], sas_key_name: Optional[str], sas_key: Optional[str]):
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

        credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return producer_cls(host=host, address=address, port=port, content_mode=content_mode, credential=credential, entra_audience=entra_audience, use_tls=use_tls)
    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return producer_cls(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)
    return producer_cls(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=use_tls)


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
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    if not address:
        raise RuntimeError("AMQP address is required")
    logging.info("Connecting AMQP producer to %s:%s/%s auth=%s tls=%s", host, port, address, args.auth_mode, tls)
    return _build_amqp_producer(producer_cls, host=host, port=port, address=address, use_tls=tls, content_mode=args.content_mode, auth_mode=args.auth_mode, username=username, password=password, entra_audience=args.entra_audience, entra_client_id=args.entra_client_id, sas_key_name=args.sas_key_name, sas_key=args.sas_key)


class AisStreamAmqpClient:
    """Emit each raw AIS type over AMQP 1.0, keyed by UserID (mirrors Kafka)."""

    def __init__(self, producer: IOAISstreamAmqpProducer):
        self._producer = producer

    async def emit(self, message_type, payload, *, user_id, mmsi, flag, ship_type, geohash5):
        mapping = _AMQP_DISPATCH.get(message_type)
        if mapping is None:
            logger.debug("Skipping unknown message type: %s", message_type)
            return
        data_class, method_name = mapping
        try:
            data = data_class.from_serializer_dict(payload)
        except Exception as exc:  # noqa: BLE001 - bad upstream payload, skip
            logger.warning("Failed to decode %s: %s", message_type, exc)
            return
        getattr(self._producer, method_name)(data=data, _user_id=str(user_id))


async def _run(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args, IOAISstreamAmqpProducer)
    bridge = AisStreamBridge(AisStreamAmqpClient(producer), api_key=args.api_key, ws_url=args.ws_url)
    if args.mock:
        logger.info("Mock mode: emitting synthetic AIS corpus and exiting")
        try:
            for envelope in mock_envelopes():
                await bridge.handle_envelope(envelope)
        finally:
            producer.close()
        return
    try:
        await bridge.run(max_events=args.max_events)
    finally:
        producer.close()


def main() -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="AISstream -> AMQP 1.0 bridge")
    sub = parser.add_subparsers(dest="command")
    feed = sub.add_parser("feed")
    add_amqp_arguments(feed, "aisstream")
    feed.add_argument("--api-key", default=os.getenv("AISSTREAM_API_KEY"))
    feed.add_argument("--mock", action="store_true", default=os.getenv("AISSTREAM_MOCK", "").lower() in ("1", "true", "yes"))
    feed.add_argument("--ws-url", default=os.getenv("AISSTREAM_WS_URL", "wss://stream.aisstream.io/v0/stream"))
    feed.add_argument("--max-events", type=int, default=int(os.getenv("AISSTREAM_MAX_EVENTS", "0")) or None)
    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        sys.exit(1)
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
