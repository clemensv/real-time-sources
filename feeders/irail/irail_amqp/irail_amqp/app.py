"""AMQP 1.0 companion feeder for irail."""
from __future__ import annotations

import argparse
import asyncio
import importlib
import inspect
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any, Optional
from urllib.parse import urlparse

try:
    from proton import symbol
except Exception:  # pragma: no cover
    symbol = lambda value: value  # type: ignore

from irail_core import IRailAPI, REQUEST_DELAY

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
SOURCE_ID = "irail"
PY_MODULE = "irail"
ENV_PREFIX = "IRAIL"

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
    mod = importlib.import_module(f"{PY_MODULE}_amqp_producer_amqp_producer.producer")
    classes = [obj for _, obj in vars(mod).items() if inspect.isclass(obj) and any(name.startswith("send_") for name in dir(obj))]
    if not classes:
        raise RuntimeError(f"No AMQP producer class found in {mod.__name__}")
    classes.sort(key=lambda cls: (len([name for name in dir(cls) if name.startswith("send_")]), cls.__name__), reverse=True)
    return classes[0]


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
    if getattr(producer, "_send_queue", None) is not None:
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


async def _run_live(args: argparse.Namespace, producer: Any) -> None:
    """Fetch live iRail data and emit it via the AMQP producer."""
    api = IRailAPI()
    station_filter = getattr(args, "station_filter", "") or os.getenv("STATION_FILTER", "")
    filter_set = {s.strip() for s in station_filter.split(",") if s.strip()} if station_filter else set()
    polling_interval = getattr(args, "polling_interval", 300)

    all_stations_raw = api.fetch_stations()
    station_ids: list[str] = []
    for raw in all_stations_raw:
        try:
            station = api.parse_station(raw)
            if filter_set and station.station_id not in filter_set:
                continue
            station_ids.append(station.station_id)
            producer.send_station(data=station, _station_id=station.station_id)
        except Exception as exc:
            logger.error("Error sending station %s: %s", raw.get("id", "?"), exc)
    logger.info("Sent %d station reference records via AMQP", len(station_ids))

    while True:
        start_time = datetime.now(timezone.utc)
        board_specs = (
            ("departure", api.parse_liveboard, producer.send_station_board),
            ("arrival", api.parse_arrivalboard, producer.send_arrival_board),
        )
        departure_count = 0
        arrival_count = 0
        for station_id in station_ids:
            for board_kind, parser, sender in board_specs:
                try:
                    liveboard_raw = api.fetch_liveboard(station_id, arrdep=board_kind)
                    if liveboard_raw is None:
                        continue
                    board = parser(liveboard_raw, station_id)
                    sender(data=board, _station_id=station_id)
                    if board_kind == "departure":
                        departure_count += 1
                    else:
                        arrival_count += 1
                except Exception as exc:
                    logger.error("Error fetching %s board for %s: %s", board_kind, station_id, exc)
                time.sleep(REQUEST_DELAY)
        elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
        logger.info(
            "Sent %d departure boards and %d arrival boards in %.1f s via AMQP",
            departure_count,
            arrival_count,
            elapsed,
        )
        if args.once:
            break
        await asyncio.sleep(max(0, polling_interval - elapsed))


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
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "300")))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser(f"~/.{PY_MODULE}_amqp_state.json")))
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    parser.add_argument("--station-filter", default=os.getenv("STATION_FILTER", ""))
    return parser


def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logger.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            time.sleep(delay)


async def _async_main(args: argparse.Namespace) -> None:
    producer = _retry_producer_init(lambda: _build_amqp_producer(args))
    try:
        await _run_live(args, producer)
    finally:
        close = getattr(producer, "close", None)
        if close:
            close()


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = _add_common_args(argparse.ArgumentParser(description=f"{SOURCE_ID} AMQP 1.0 bridge"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    asyncio.run(_async_main(args))


if __name__ == "__main__":
    main()
