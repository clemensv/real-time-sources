from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from typing import Optional
from urllib.parse import urlparse

from mode_s_core import ModeSBridge
from mode_s_amqp_producer_data import Record as AmqpRecord
from mode_s_amqp_producer_amqp_producer.producer import ModeSAmqpProducer

logger = logging.getLogger("mode_s_amqp")
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
    return _build_amqp_producer(producer_cls, host=host, port=port, address=address, use_tls=tls, content_mode=args.content_mode, auth_mode=args.auth_mode, username=username, password=password, entra_audience=args.entra_audience, entra_client_id=args.entra_client_id, sas_key_name=args.sas_key_name, sas_key=args.sas_key)


class ModeSAmqpClient:
    def __init__(self, producer: ModeSAmqpProducer):
        self._producer = producer

    @staticmethod
    def _data(rec) -> AmqpRecord:
        return AmqpRecord(**rec.__dict__)

    async def publish_adsb(self, *, feedurl, icao24, receiver_id, data):
        payload = self._data(data)
        self._producer.send_adsb(data=payload, _feedurl=feedurl, _icao24=icao24, _receiver_id=receiver_id, _msg_type=payload.msg_type)

    async def publish_altitude_reply(self, *, feedurl, icao24, receiver_id, data):
        payload = self._data(data)
        self._producer.send_altitude_reply(data=payload, _feedurl=feedurl, _icao24=icao24, _receiver_id=receiver_id, _msg_type=payload.msg_type)

    async def publish_identity_reply(self, *, feedurl, icao24, receiver_id, data):
        payload = self._data(data)
        self._producer.send_identity_reply(data=payload, _feedurl=feedurl, _icao24=icao24, _receiver_id=receiver_id, _msg_type=payload.msg_type)

    async def publish_acquisition_reply(self, *, feedurl, icao24, receiver_id, data):
        payload = self._data(data)
        self._producer.send_acquisition_reply(data=payload, _feedurl=feedurl, _icao24=icao24, _receiver_id=receiver_id, _msg_type=payload.msg_type)

    async def publish_comm_baltitude(self, *, feedurl, icao24, receiver_id, data):
        payload = self._data(data)
        self._producer.send_comm_baltitude(data=payload, _feedurl=feedurl, _icao24=icao24, _receiver_id=receiver_id, _msg_type=payload.msg_type)

    async def publish_comm_bidentity(self, *, feedurl, icao24, receiver_id, data):
        payload = self._data(data)
        self._producer.send_comm_bidentity(data=payload, _feedurl=feedurl, _icao24=icao24, _receiver_id=receiver_id, _msg_type=payload.msg_type)


async def _run(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args, ModeSAmqpProducer)
    feedurl = args.feedurl or f"dump1090://{args.dump1090_host}:{args.dump1090_port}"
    bridge = ModeSBridge(ModeSAmqpClient(producer), feedurl=feedurl, receiver_id=args.receiver_id, ref_lat=args.ref_lat or 0.0, ref_lon=args.ref_lon or 0.0)
    try:
        if not args.dump1090_host or not args.dump1090_port:
            raise SystemExit("--dump1090-host and --dump1090-port are required")
        await bridge.run_from_dump1090(args.dump1090_host, int(args.dump1090_port), max_events=args.max_events)
    finally:
        producer.close()


def main() -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="Mode-S -> AMQP 1.0 bridge")
    sub = parser.add_subparsers(dest="command")
    feed = sub.add_parser("feed")
    add_amqp_arguments(feed, "mode-s")
    feed.add_argument("--dump1090-host", default=os.getenv("DUMP1090_HOST"))
    feed.add_argument("--dump1090-port", default=os.getenv("DUMP1090_PORT"))
    feed.add_argument("--receiver-id", default=os.getenv("MODE_S_RECEIVER_ID", os.getenv("STATIONID", "station1")))
    feed.add_argument("--ref-lat", type=float, default=float(os.getenv("REF_LAT", "0")) if os.getenv("REF_LAT") else None)
    feed.add_argument("--ref-lon", type=float, default=float(os.getenv("REF_LON", "0")) if os.getenv("REF_LON") else None)
    feed.add_argument("--feedurl", default=os.getenv("MODE_S_FEEDURL"))
    feed.add_argument("--max-events", type=int, default=int(os.getenv("MODE_S_MAX_EVENTS", "0")) or None)
    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        sys.exit(1)
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
