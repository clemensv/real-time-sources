
"""AMQP 1.0 companion feeder for noaa-nws."""
from __future__ import annotations

import argparse
import asyncio
import importlib
import logging
import os
import time
from typing import Dict
from urllib.parse import urlparse

try:
    from proton import symbol
except Exception:  # pragma: no cover
    symbol = lambda value: value  # type: ignore

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
SOURCE_ID = "noaa-nws"
PY_MODULE = "noaa_nws"
ENV_PREFIX = "NOAA_NWS"

logger = logging.getLogger(__name__)


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _topic_segment(value: object) -> str:
    text = (str(value) if value is not None else "unknown").strip() or "unknown"
    for forbidden in ("/", "+", "#", "\x00"):
        text = text.replace(forbidden, "-")
    return "-".join(text.split()) or "unknown"


def _parse_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return (
        parsed.hostname or "localhost",
        parsed.port or (5671 if tls else 5672),
        tls,
        parsed.username,
        parsed.password,
        (parsed.path or "").lstrip("/") or None,
    )


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


def _build_producer_from_args(args, cls):
    """Construct an AMQP producer of the given class using CLI/env args."""
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
    kwargs = dict(
        host=host,
        address=address,
        port=port,
        content_mode=args.content_mode,
        use_tls=tls,
    )
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        kwargs.update(
            credential=(
                ManagedIdentityCredential(client_id=args.entra_client_id)
                if args.entra_client_id
                else DefaultAzureCredential()
            ),
            entra_audience=args.entra_audience,
        )
    elif args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        kwargs.update(sas_key_name=args.sas_key_name, sas_key=args.sas_key)
    else:
        kwargs.update(username=username, password=password)
    return _apply_partition_key_workaround(cls(**kwargs))


def _build_alerts_producer(args):
    mod = importlib.import_module(f"{PY_MODULE}_amqp_producer_amqp_producer.producer")
    return _build_producer_from_args(args, mod.MicrosoftOpenDataUSNOAANWSAlertsAmqpProducer)


def _build_observations_producer(args):
    mod = importlib.import_module(f"{PY_MODULE}_amqp_producer_amqp_producer.producer")
    return _build_producer_from_args(args, mod.MicrosoftOpenDataUSNOAANWSObservationsAmqpProducer)


async def _run_live(args: argparse.Namespace, alerts_producer, obs_producer) -> None:
    """Live NWS data acquisition and AMQP emission loop."""
    from noaa_nws_core import NWSFetcher
    from noaa_nws_core.noaa_nws import POLL_INTERVAL_SECONDS, OBSERVATION_INTERVAL_SECONDS
    from noaa_nws_amqp_producer_data import WeatherAlert, ObservationStation, WeatherObservation

    fetcher = NWSFetcher(last_polled_file=args.state_file)

    # Reference data: observation stations
    logger.info("Sending NWS observation stations as reference data...")
    station_dicts = fetcher.fetch_observation_stations()
    for s in station_dicts:
        station = ObservationStation(**s)
        obs_producer.send_observation_station(
            data=station,
            _station_id=_topic_segment(s["station_id"]),
            _state=_topic_segment(s.get("state") or "unknown"),
            _zone_id=_topic_segment(s.get("zone_id") or "unknown"),
        )
    logger.info("Sent %d observation stations via AMQP", len(station_dicts))

    obs_seen: Dict[str, str] = {}
    last_obs_time = 0.0

    while True:
        # Poll and send alerts
        state = fetcher.load_seen_alerts()
        seen_ids = set(state.get("seen_ids", []))
        features = fetcher.poll_alerts()

        new_count = 0
        for feature in features:
            props = feature.get("properties", {})
            alert_id = props.get("id", "")
            if not alert_id or alert_id in seen_ids:
                continue

            affected_zones = props.get("affectedZones") or []
            state_code = (
                affected_zones[0].rsplit("/", 1)[-1][:2]
                if affected_zones
                else "US"
            )
            event = props.get("event", "")
            event_type = event.replace(" ", "_").lower() if event else "unknown"

            alert = WeatherAlert(
                alert_id=alert_id,
                area_desc=props.get("areaDesc", ""),
                sent=props.get("sent", ""),
                effective=props.get("effective", ""),
                expires=props.get("expires", ""),
                status=props.get("status", ""),
                message_type=props.get("messageType", ""),
                category=props.get("category"),
                severity=props.get("severity", ""),
                certainty=props.get("certainty", ""),
                urgency=props.get("urgency", ""),
                event=event,
                sender_name=props.get("senderName"),
                headline=props.get("headline"),
                description=props.get("description"),
                zone_id=affected_zones[0].rsplit("/", 1)[-1] if affected_zones else None,
                state=state_code,
                event_type=event_type,
            )
            alerts_producer.send_weather_alert(
                data=alert,
                _alert_id=_topic_segment(alert_id),
                _state=_topic_segment(state_code),
                _severity=_topic_segment(props.get("severity", "unknown")),
                _event_type=_topic_segment(event_type),
            )
            seen_ids.add(alert_id)
            new_count += 1

        if new_count:
            logger.info("Sent %d new alert(s) via AMQP", new_count)

        seen_list = list(seen_ids)
        if len(seen_list) > 10000:
            seen_list = seen_list[-10000:]
        state["seen_ids"] = seen_list
        fetcher.save_seen_alerts(state)

        # Poll observations on a slower cadence
        now = time.time()
        if now - last_obs_time >= OBSERVATION_INTERVAL_SECONDS:
            obs_count = 0
            for sid in fetcher.station_ids:
                obs_dict = fetcher.fetch_latest_observation(sid)
                if obs_dict and obs_dict.get("timestamp"):
                    if obs_seen.get(sid) != obs_dict["timestamp"]:
                        obs = WeatherObservation(**obs_dict)
                        obs_producer.send_weather_observation(
                            data=obs,
                            _station_id=_topic_segment(sid),
                            _state=_topic_segment(obs_dict.get("state") or "unknown"),
                            _zone_id=_topic_segment(obs_dict.get("zone_id") or "unknown"),
                        )
                        obs_count += 1
                        obs_seen[sid] = obs_dict["timestamp"]
            if obs_count:
                logger.info("Sent %d weather observation(s) via AMQP", obs_count)
            last_obs_time = now

        if args.once:
            break
        await asyncio.sleep(POLL_INTERVAL_SECONDS)


def _add_common_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", SOURCE_ID))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("AMQP_TLS", False))
    parser.add_argument(
        "--content-mode",
        choices=("binary", "structured"),
        default=os.getenv("AMQP_CONTENT_MODE", "binary"),
    )
    parser.add_argument(
        "--auth-mode",
        choices=("password", "entra", "sas"),
        default=os.getenv("AMQP_AUTH_MODE", "password"),
    )
    parser.add_argument(
        "--entra-audience",
        default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS),
    )
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    parser.add_argument(
        "--polling-interval",
        type=int,
        default=int(os.getenv("POLLING_INTERVAL", "60")),
    )
    parser.add_argument(
        "--state-file",
        default=os.getenv(
            "STATE_FILE", os.path.expanduser(f"~/.{PY_MODULE}_amqp_state.json")
        ),
    )
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
            logger.warning(
                "Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                attempt + 1,
                max_attempts,
                e,
                delay,
            )
            time.sleep(delay)


async def _async_main(args: argparse.Namespace) -> None:
    alerts_producer = None
    obs_producer = None
    try:
        alerts_producer = _retry_producer_init(lambda: _build_alerts_producer(args))
        obs_producer = _retry_producer_init(lambda: _build_observations_producer(args))
        await _run_live(args, alerts_producer, obs_producer)
    finally:
        for p in (alerts_producer, obs_producer):
            if p is not None:
                close = getattr(p, "close", None)
                if close:
                    close()


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    parser = _add_common_args(
        argparse.ArgumentParser(description=f"{SOURCE_ID} AMQP 1.0 bridge")
    )
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    asyncio.run(_async_main(args))


if __name__ == "__main__":
    main()

