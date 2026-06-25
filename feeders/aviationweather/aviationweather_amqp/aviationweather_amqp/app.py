"""AMQP 1.0 feeder for AviationWeather.gov."""
from __future__ import annotations

import argparse
import asyncio
import importlib
import inspect
import logging
import os
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

try:
    from proton import symbol
except Exception:  # pragma: no cover
    symbol = lambda value: value  # type: ignore

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
SOURCE_ID = "aviationweather"
PY_MODULE = "aviationweather"

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
    # WORKAROUND(xregistry/codegen#294): stamp x-opt-partition-key from CE subject
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


async def _run_live(args: argparse.Namespace, producer) -> None:
    """Acquire live AviationWeather.gov data and publish via AMQP."""
    from aviationweather_core import (
        AviationWeatherPoller,
        DEFAULT_STATIONS,
        METAR_POLL_INTERVAL,
        SIGMET_POLL_INTERVAL,
        STATION_REFRESH_HOURS,
    )

    station_ids = os.getenv("AVIATIONWEATHER_STATIONS", DEFAULT_STATIONS)
    if getattr(args, "stations", None):
        station_ids = args.stations

    state_file = getattr(args, "state_file", None) or os.path.expanduser(f"~/.{PY_MODULE}_amqp_state.json")

    poller = AviationWeatherPoller(
        last_polled_file=state_file,
        station_ids=station_ids,
        metar_poll_interval=METAR_POLL_INTERVAL,
        sigmet_poll_interval=SIGMET_POLL_INTERVAL,
    )

    def utcnow_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    logger.info("Emitting station reference data via AMQP...")
    station_count = 0
    for raw in poller.fetch_station_json(poller.station_ids):
        station = poller.parse_station(raw)
        if station:
            producer.send_station(data=station, _icao_id=station.icao_id, _time=utcnow_iso())
            station_count += 1
    logger.info("Sent %d station(s) via AMQP", station_count)

    state = poller.load_state()
    metar_timestamps = state.get("metar_timestamps", {})
    seen_sigmet_keys: set = set(state.get("sigmet_keys", []))
    last_sigmet_poll = 0.0
    last_station_refresh = time.monotonic()

    while True:
        now = time.monotonic()

        metar_count = 0
        for raw in poller.fetch_metar_json(poller.station_ids):
            metar = poller.parse_metar(raw)
            if metar is None:
                continue
            if metar_timestamps.get(metar.icao_id) == metar.obs_time:
                continue
            producer.send_metar(data=metar, _icao_id=metar.icao_id, _time=metar.obs_time)
            metar_timestamps[metar.icao_id] = metar.obs_time
            metar_count += 1
        if metar_count:
            logger.info("Sent %d new METAR(s) via AMQP", metar_count)

        if now - last_sigmet_poll >= SIGMET_POLL_INTERVAL:
            sigmet_count = 0
            current_keys: set = set()
            for raw in poller.fetch_airsigmet_json():
                sigmet = poller.parse_us_sigmet(raw)
                if sigmet:
                    key = poller.sigmet_dedup_key(sigmet)
                    current_keys.add(key)
                    if key not in seen_sigmet_keys:
                        producer.send_sigmet(data=sigmet, _region=sigmet.region, _sigmet_id=sigmet.sigmet_id, _time=sigmet.valid_time_from)
                        sigmet_count += 1
            for raw in poller.fetch_isigmet_json():
                sigmet = poller.parse_intl_sigmet(raw)
                if sigmet:
                    key = poller.sigmet_dedup_key(sigmet)
                    current_keys.add(key)
                    if key not in seen_sigmet_keys:
                        producer.send_sigmet(data=sigmet, _region=sigmet.region, _sigmet_id=sigmet.sigmet_id, _time=sigmet.valid_time_from)
                        sigmet_count += 1
            seen_sigmet_keys = current_keys
            if sigmet_count:
                logger.info("Sent %d new SIGMET(s) via AMQP", sigmet_count)
            last_sigmet_poll = now

        if now - last_station_refresh >= STATION_REFRESH_HOURS * 3600:
            refresh_count = 0
            for raw in poller.fetch_station_json(poller.station_ids):
                station = poller.parse_station(raw)
                if station:
                    producer.send_station(data=station, _icao_id=station.icao_id, _time=utcnow_iso())
                    refresh_count += 1
            logger.info("Refreshed %d station(s) via AMQP", refresh_count)
            last_station_refresh = now

        poller.save_state({
            "metar_timestamps": metar_timestamps,
            "sigmet_keys": list(seen_sigmet_keys),
        })

        if args.once:
            break
        await asyncio.sleep(METAR_POLL_INTERVAL)


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
    parser.add_argument("--stations", default=os.getenv("AVIATIONWEATHER_STATIONS", ""))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser(f"~/.{PY_MODULE}_amqp_state.json")))
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
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
