"""OpenStreetMap minutely diffs -> AMQP 1.0 bridge."""

from __future__ import annotations

import argparse
import asyncio
import datetime
import logging
import os
import sys
from typing import Optional
from urllib.parse import urlparse

from wikimedia_osm_diffs_amqp_producer_amqp_producer.producer import OrgOpenStreetMapDiffsAmqpProducer
from wikimedia_osm_diffs_amqp_producer_data import MapChange, ReplicationState
from wikimedia_osm_diffs_core.wikimedia_osm_diffs import (
    DEFAULT_STATE_FILE,
    DEFAULT_USER_AGENT,
    DIFF_BASE_URL,
    STATE_URL,
    StateStore,
    build_session,
    fetch_sequence_changes,
    fetch_state,
    sequence_to_url,
)

logger = logging.getLogger(__name__)
DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


class _AmqpClient:
    def __init__(self, producer):
        self.producer = producer

    def __getattr__(self, name: str):
        if not name.startswith("publish_"):
            raise AttributeError(name)
        method = getattr(self.producer, f"send_{name[len('publish_') : ]}")

        async def _publish(**kwargs):
            data = kwargs.pop("data")
            kwargs.pop("qos", None)
            kwargs.pop("retain", None)
            params = set(method.__code__.co_varnames[: method.__code__.co_argcount])
            call_kwargs = {f"_{k}": v for k, v in kwargs.items() if v is not None and f"_{k}" in params}
            method(data=data, **call_kwargs)

        return _publish


class OsmDiffsAmqpBridge:
    def __init__(self, client: _AmqpClient, *, state_store: Optional[StateStore] = None, state_url: str = STATE_URL, diff_base_url: str = DIFF_BASE_URL, user_agent: str = DEFAULT_USER_AGENT, poll_interval: int = 60, max_retry_delay: int = 120, once: bool = False) -> None:
        self.client = client
        self._state_store = state_store
        self._state_url = state_url
        self._diff_base_url = diff_base_url
        self._poll_interval = poll_interval
        self._max_retry_delay = max_retry_delay
        self._once = once
        self._last_sequence = state_store.load() if state_store else None
        self._session = build_session(user_agent)

    async def run(self) -> None:
        retry_delay = 1
        while True:
            try:
                await self._poll_cycle()
                retry_delay = 1
                if self._once:
                    return
                await asyncio.sleep(self._poll_interval)
            except (asyncio.CancelledError, KeyboardInterrupt):
                raise
            except Exception as exc:
                logger.warning("Poll cycle error: %s. Retrying in %ds.", exc, retry_delay)
                if self._once:
                    return
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, self._max_retry_delay)

    async def _poll_cycle(self) -> None:
        state = fetch_state(self._session, self._state_url)
        if state is None:
            return
        current_seq = state["sequence_number"]
        current_ts = state["timestamp"]
        if self._last_sequence is not None and current_seq <= self._last_sequence:
            return
        start_seq = (self._last_sequence + 1) if self._last_sequence is not None else current_seq
        start_seq = max(start_seq, current_seq - 4)
        for seq in range(start_seq, current_seq + 1):
            await self._process_sequence(seq)
        await self._publish_replication_state(current_seq, current_ts)
        self._last_sequence = current_seq
        if self._state_store:
            self._state_store.save(current_seq)

    async def _process_sequence(self, seq: int) -> None:
        for change in fetch_sequence_changes(self._session, seq, self._diff_base_url):
            await self._publish_change(change)

    async def _publish_change(self, change: dict) -> None:
        data = MapChange.from_serializer_dict(change)
        publish = getattr(self.client, f"publish_org_open_street_map_diffs_{change['element_type']}")
        await publish(geohash5=data.geohash5 or "nogeo", element_id=str(data.element_id), data=data, qos=0, retain=False)

    async def _publish_replication_state(self, seq: int, ts: datetime.datetime) -> None:
        state_data = ReplicationState(sequence_number=seq, timestamp=ts, source_url=sequence_to_url(seq, self._diff_base_url))
        await self.client.publish_org_open_street_map_diffs_replication_state(data=state_data, qos=0, retain=True)


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


async def _run(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args, OrgOpenStreetMapDiffsAmqpProducer)
    client = _AmqpClient(producer)
    state_store = StateStore(args.state_file) if args.state_file else None
    try:
        await OsmDiffsAmqpBridge(client, state_store=state_store, state_url=args.state_url, diff_base_url=args.diff_base_url, poll_interval=args.poll_interval, once=args.once).run()
    finally:
        producer.close()


def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(description="OSM minutely diffs -> AMQP 1.0 bridge")
    sub = p.add_subparsers(dest="command")
    feed = sub.add_parser("feed", help="Stream OSM diffs to AMQP")
    add_amqp_arguments(feed, "wikimedia-osm-diffs")
    feed.add_argument("--state-url", default=os.getenv("OSM_DIFFS_STATE_URL", STATE_URL))
    feed.add_argument("--diff-base-url", default=os.getenv("OSM_DIFFS_BASE_URL", DIFF_BASE_URL))
    feed.add_argument("--state-file", default=os.getenv("OSM_DIFFS_STATE_FILE", DEFAULT_STATE_FILE))
    feed.add_argument("--poll-interval", type=int, default=int(os.getenv("OSM_DIFFS_POLL_INTERVAL", "60")))
    feed.add_argument("--once", action="store_true", default=os.getenv("OSM_DIFFS_ONCE", "false").lower() in ("true", "1", "yes"))
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
