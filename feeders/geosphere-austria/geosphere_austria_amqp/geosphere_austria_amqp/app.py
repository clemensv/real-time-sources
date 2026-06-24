"""AMQP feeder application for geosphere-austria."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import time
from urllib.parse import urlparse

try:
    from proton import symbol
except Exception:  # pragma: no cover
    symbol = lambda value: value  # type: ignore

from geosphere_austria_core import (
    create_retrying_session, fetch_station_metadata, parse_station,
    fetch_observations, parse_observation, observation_fingerprint,
    load_state, save_state, station_bundesland_segment,
    DEFAULT_POLLING_INTERVAL, DEFAULT_STATION_REFRESH_INTERVAL,
)
from geosphere_austria_amqp_producer_amqp_producer.producer import AtGeosphereTawesAmqpProducer

logger = logging.getLogger(__name__)
DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _segment(value) -> str:
    text = (str(value) if value is not None else "unknown").strip() or "unknown"
    for forbidden in ("/", "+", "#", " "):
        text = text.replace(forbidden, "-")
    return "-".join(text.split()) or "unknown"


def _parse_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or "").lstrip("/") or None


def _apply_partition_key_workaround(producer):
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
        original = producer._send_via_reactor
        producer._send_via_reactor = lambda msg: original(stamp(msg))
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
    return _apply_partition_key_workaround(AtGeosphereTawesAmqpProducer(**kwargs))


async def _run_live(args: argparse.Namespace, producer: AtGeosphereTawesAmqpProducer) -> None:
    session = create_retrying_session()
    state = load_state(args.state_file)
    cached_stations = []
    station_map = {}
    last_station_refresh = 0.0
    while True:
        now = time.time()
        station_refresh_due = (now - last_station_refresh) >= args.station_refresh_interval
        try:
            stations_raw = fetch_station_metadata(session)
            stations = [parse_station(s) for s in stations_raw]
            station_map = {s.station_id: s for s in stations}
            cached_stations = stations
        except Exception as exc:
            if not cached_stations:
                raise
            logger.warning("Station metadata refresh failed; using cached: %s", exc)
            stations = cached_stations
        if station_refresh_due:
            for station in stations:
                producer.send_weather_station(
                    data=station,  # type: ignore[arg-type]
                    _station_id=station.station_id,
                    _bundesland=station_bundesland_segment(station),
                )
            logger.info("Published %d station reference events via AMQP", len(stations))
            last_station_refresh = now
        station_ids = [s.station_id for s in stations]
        features, timestamp = fetch_observations(session, station_ids)
        fingerprints = state.get("fingerprints", {})
        sent = 0
        for feat in features:
            obs = parse_observation(feat, timestamp)
            if obs is None:
                continue
            fp = observation_fingerprint(obs)
            if fingerprints.get(obs.station_id) == fp:
                continue
            st = station_map.get(obs.station_id)
            bl = station_bundesland_segment(st) if st is not None else "unknown"
            producer.send_weather_observation(
                data=obs,  # type: ignore[arg-type]
                _station_id=obs.station_id,
                _bundesland=bl,
            )
            fingerprints[obs.station_id] = fp
            sent += 1
        state["fingerprints"] = fingerprints
        save_state(args.state_file, state)
        logger.info("Published %d observation events via AMQP", sent)
        if args.once:
            break
        await asyncio.sleep(args.polling_interval)


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="geosphere-austria AMQP bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", "geosphere-austria"))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("AMQP_TLS", False))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser("~/.geosphere_austria_amqp_state.json")))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", str(DEFAULT_POLLING_INTERVAL))))
    parser.add_argument("--station-refresh-interval", type=int, default=int(os.getenv("STATION_REFRESH_INTERVAL", str(DEFAULT_STATION_REFRESH_INTERVAL))))
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    producer = _build_amqp_producer(args)
    try:
        asyncio.run(_run_live(args, producer))
    finally:
        close = getattr(producer, "close", None)
        if close:
            close()


if __name__ == "__main__":
    main()
