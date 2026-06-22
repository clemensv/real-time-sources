"""AMQP 1.0 companion feeder for autobahn."""

from __future__ import annotations

import argparse
import asyncio
import importlib
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    from proton import symbol
except Exception:  # pragma: no cover
    symbol = lambda value: value  # type: ignore

try:
    from autobahn_core import (
        DEFAULT_POLL_INTERVAL_SECONDS,
        DEFAULT_REQUEST_CONCURRENCY,
        DEFAULT_STATE_FILE,
        EVENT_FAMILIES,
        AutobahnPoller,
        parse_resources_argument,
        parse_roads_argument,
    )
except ImportError:
    from autobahn_core.autobahn_core import (
        DEFAULT_POLL_INTERVAL_SECONDS,
        DEFAULT_REQUEST_CONCURRENCY,
        DEFAULT_STATE_FILE,
        EVENT_FAMILIES,
        AutobahnPoller,
        parse_resources_argument,
        parse_roads_argument,
    )

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
SOURCE_ID = "autobahn"

logger = logging.getLogger(__name__)


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _parse_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or "").lstrip("/") or None


def _producer_class():
    mod = importlib.import_module("autobahn_amqp_producer_amqp_producer.producer")
    classes = [obj for _, obj in vars(mod).items() if isinstance(obj, type) and any(name.startswith("send_") for name in dir(obj))]
    if not classes:
        raise RuntimeError(f"No AMQP producer class found in {mod.__name__}")
    classes.sort(key=lambda cls: (len([name for name in dir(cls) if name.startswith("send_")]), cls.__name__), reverse=True)
    return classes[0]


def _load_generated_data_classes() -> dict[str, type[Any]]:
    expected = {config["schema"] for config in EVENT_FAMILIES.values()}
    module = importlib.import_module("autobahn_amqp_producer_data")
    found = {name: getattr(module, name) for name in expected if isinstance(getattr(module, name, None), type)}
    missing = sorted(expected - set(found))
    if missing:
        raise ImportError(f"Generated Autobahn AMQP data classes not found: {', '.join(missing)}")
    return found


def _apply_partition_key_workaround(producer):
    # WORKAROUND(xregistry/codegen#294): xrcg declares AMQP message_annotations
    # but does not emit them yet. Stamp x-opt-partition-key from CE subject.
    def stamp(msg):
        props = dict(getattr(msg, "properties", None) or {})
        ce_subject = props.get("cloudEvents:subject") or getattr(msg, "subject", None)
        if ce_subject:
            annotations = dict(getattr(msg, "annotations", None) or {})
            annotations[symbol("x-opt-partition-key")] = str(ce_subject)
            msg.annotations = annotations
        return msg

    if getattr(producer, "_sender", None) is not None:
        original_send = producer._sender.send
        producer._sender.send = lambda msg, *a, **kw: original_send(stamp(msg), *a, **kw)
    if hasattr(producer, "_send_via_reactor"):
        original_reactor_send = producer._send_via_reactor
        producer._send_via_reactor = lambda msg: original_reactor_send(stamp(msg))
    return producer


def _build_amqp_producer(args):
    address = args.address
    if args.broker_url:
        host, port, tls, url_user, url_pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or url_user
        password = args.password or url_pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        address = path or address
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    kwargs = dict(host=host, address=address, port=port, content_mode=args.content_mode, use_tls=tls)
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

        kwargs.update(credential=ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential(), entra_audience=args.entra_audience)
    elif args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        kwargs.update(sas_key_name=args.sas_key_name, sas_key=args.sas_key)
    else:
        kwargs.update(username=username, password=password)
    return _apply_partition_key_workaround(_producer_class()(**kwargs))


class AutobahnAmqpAdapter:
    """Thin adapter that maps Autobahn changes onto generated AMQP send methods."""

    def __init__(self, producer: Any) -> None:
        self.producer = producer
        self.data_classes = _load_generated_data_classes()
        self.sent = 0

    def send_change(self, family: str, action: str, snapshot: dict[str, Any], event_time: str) -> None:
        config = EVENT_FAMILIES[family]
        data_kwargs = dict(snapshot)
        data_kwargs["event_time"] = event_time
        data = self.data_classes[config["schema"]](**data_kwargs)
        method = getattr(self.producer, f"send_{config['method_stem']}_{action}")
        method(
            data=data,
            _identifier=snapshot["identifier"],
            _road=snapshot["road"],
            _time=event_time,
            content_type="application/json",
        )
        self.sent += 1

    def close(self) -> None:
        close = getattr(self.producer, "close", None)
        if close:
            close()


async def _run_live(args: argparse.Namespace, adapter: AutobahnAmqpAdapter) -> None:
    resources = parse_resources_argument(args.resources)
    roads = parse_roads_argument(args.roads)
    poller = AutobahnPoller(
        state_file=args.state_file,
        poll_interval_seconds=args.polling_interval,
        resources=resources,
        roads=roads,
        request_concurrency=args.request_concurrency,
    )
    while True:
        cycle_started = datetime.now(timezone.utc)
        changes, detected_changes = await asyncio.to_thread(poller.poll_once, cycle_started)
        for change in detected_changes:
            adapter.send_change(change.family, change.action, change.snapshot, change.event_time)
        poller.save_state()
        summary = poller.summarize_changes(changes)
        logger.info("Autobahn AMQP cycle complete: %s", summary or "no changes")
        if args.once:
            return
        elapsed = datetime.now(timezone.utc) - cycle_started
        remaining = timedelta(seconds=poller.poll_interval_seconds) - elapsed
        if remaining.total_seconds() > 0:
            await asyncio.sleep(remaining.total_seconds())


def _add_common_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", SOURCE_ID))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("AMQP_TLS", False))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", str(DEFAULT_POLL_INTERVAL_SECONDS))))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE.replace(".json", "_amqp_state.json")))
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    parser.add_argument("--resources", default=os.getenv("AUTOBAHN_RESOURCES", "*"))
    parser.add_argument("--roads", default=os.getenv("AUTOBAHN_ROADS", ""))
    parser.add_argument("--request-concurrency", type=int, default=int(os.getenv("AUTOBAHN_REQUEST_CONCURRENCY", str(DEFAULT_REQUEST_CONCURRENCY))))
    return parser


def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""

    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as exc:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2**attempt)
            logger.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...", attempt + 1, max_attempts, exc, delay)
            time.sleep(delay)


async def _async_main(args: argparse.Namespace) -> None:
    producer = _retry_producer_init(lambda: _build_amqp_producer(args))
    adapter = AutobahnAmqpAdapter(producer)
    try:
        await _run_live(args, adapter)
    finally:
        adapter.close()


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = _add_common_args(argparse.ArgumentParser(description=f"{SOURCE_ID} AMQP 1.0 bridge"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    asyncio.run(_async_main(args))


if __name__ == "__main__":
    main()
