"""AMQP feeder application for smhi-weather."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from urllib.parse import urlparse

try:
    from proton import symbol
except Exception:  # pragma: no cover
    symbol = lambda value: value  # type: ignore

from smhi_weather_core import (
    SMHIWeatherAPI, PARAM_AIR_TEMP, ALL_PARAMS,
    merge_observations, _load_state, _save_state, observation_lan_segment,
)
from smhi_weather_amqp_producer_amqp_producer.producer import SEGovSMHIWeatherAmqpProducer

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
    return _apply_partition_key_workaround(SEGovSMHIWeatherAmqpProducer(**kwargs))


async def _run_live(args: argparse.Namespace, producer: SEGovSMHIWeatherAmqpProducer) -> None:
    api = SMHIWeatherAPI(polling_interval=args.polling_interval)
    previous_readings = _load_state(args.state_file)
    station_list = api.get_stations_for_parameter(PARAM_AIR_TEMP)
    for sdata in station_list:
        station = api.parse_station(sdata)
        producer.send_station(
            data=station,
            _station_id=station.station_id,
            _lan=station.lan or "unknown",
        )
    logger.info("Published %d station reference events via AMQP", len(station_list))
    station_lan_by_id = {str(s.get("key", "")): api.extract_lan(s) for s in station_list}
    while True:
        param_data = {}
        for param_id in ALL_PARAMS:
            try:
                bulk = api.get_bulk_latest(param_id)
                param_data[param_id] = api.parse_bulk_observations(bulk)
            except Exception as exc:
                logger.warning("Failed to fetch parameter %d: %s", param_id, exc)
        observations = merge_observations(param_data, station_lan_by_id=station_lan_by_id)
        sent = 0
        for obs in observations:
            reading_key = f"{obs.station_id}:{obs.observation_time.isoformat()}"
            if reading_key in previous_readings:
                continue
            producer.send_weather_observation(
                data=obs,
                _station_id=obs.station_id,
                _lan=observation_lan_segment(obs),
            )
            previous_readings[reading_key] = obs.observation_time.isoformat()
            sent += 1
        _save_state(args.state_file, previous_readings)
        logger.info("Published %d observation events via AMQP", sent)
        if args.once:
            break
        await asyncio.sleep(args.polling_interval)


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="smhi-weather AMQP bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", "smhi-weather"))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("AMQP_TLS", False))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser("~/.smhi_weather_amqp_state.json")))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "900")))
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
