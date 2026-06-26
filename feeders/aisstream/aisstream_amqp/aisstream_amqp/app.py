"""AISstream.io firehose -> AMQP 1.0 bridge."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from typing import Optional
from urllib.parse import urlparse

from aisstream_core import AisStreamBridge
from aisstream_amqp_producer_data import AidToNavigation, PositionReport, ShipStatic
from aisstream_amqp_producer_amqp_producer.producer import IOAISstreamAmqpProducer

logger = logging.getLogger("aisstream_amqp")
DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


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


class AisStreamAmqpClientAdapter:
    def __init__(self, producer: IOAISstreamAmqpProducer):
        self._producer = producer

    async def publish_position_report(self, *, mmsi, flag, ship_type, geohash5, payload):
        data = PositionReport(mmsi=mmsi, flag=flag, ship_type=ship_type, geohash5=geohash5, msg_type="position-report", **payload)
        self._producer.send_position_report(data=data, _mmsi=mmsi, _flag=flag, _ship_type=ship_type, _geohash5=geohash5)

    async def publish_ship_static(self, *, mmsi, flag, ship_type, geohash5, payload):
        data = ShipStatic(mmsi=mmsi, flag=flag, ship_type=ship_type, geohash5=geohash5, msg_type="static", **payload)
        self._producer.send_ship_static(data=data, _mmsi=mmsi, _flag=flag, _ship_type=ship_type, _geohash5=geohash5)

    async def publish_aid_to_navigation(self, *, mmsi, flag, ship_type, geohash5, payload):
        data = AidToNavigation(mmsi=mmsi, flag=flag, ship_type=ship_type, geohash5=geohash5, msg_type="aid-to-navigation", **payload)
        self._producer.send_aid_to_navigation(data=data, _mmsi=mmsi, _flag=flag, _ship_type=ship_type, _geohash5=geohash5)


async def _run(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args, IOAISstreamAmqpProducer)
    if args.mock:
        logger.info("Running AISstream AMQP bridge in mock mode")
        adapter = AisStreamAmqpClientAdapter(producer)
        # Emit canned mock data matching the Kafka bridge's mock corpus
        await adapter.publish_ship_static(
            mmsi="219000001", flag="DK", ship_type="cargo", geohash5="u4pru",
            payload={"user_id": 219000001, "name": "AISSTREAM MOCK STATIC",
                     "call_sign": "OXAI1", "imo_number": 1234567,
                     "ship_type_code": 70, "dim_to_bow": 10, "dim_to_stern": 90,
                     "dim_to_port": 8, "dim_to_starboard": 8, "eta": "03-15 12:00",
                     "draught": 8.5, "destination": "AARHUS", "message_id": 5})
        await adapter.publish_position_report(
            mmsi="219000001", flag="DK", ship_type="cargo", geohash5="u4pru",
            payload={"user_id": 219000001, "navigational_status": 0, "rate_of_turn": 0,
                     "sog": 12.3, "position_accuracy": True,
                     "longitude": 10.21, "latitude": 56.15, "cog": 90.5,
                     "true_heading": 91, "timestamp": 10, "raim": True, "message_id": 1})
        await adapter.publish_aid_to_navigation(
            mmsi="992190001", flag="DK", ship_type="unknown", geohash5="u4pru",
            payload={"user_id": 992190001, "name": "MOCK BUOY", "type": 5,
                     "latitude": 56.17, "longitude": 10.25,
                     "off_position": False, "virtual_atoN": False, "message_id": 21})
        producer.close()
        return
    bridge = AisStreamBridge(AisStreamAmqpClientAdapter(producer), api_key=args.api_key, ws_url=args.ws_url)
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
