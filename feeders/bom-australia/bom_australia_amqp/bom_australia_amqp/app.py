"""AMQP 1.0 companion feeder for bom-australia — real acquisition loop."""
from __future__ import annotations

import argparse
import asyncio
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
SOURCE_ID = "bom-australia"
PY_MODULE = "bom_australia"

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
    return (
        parsed.hostname or "localhost",
        parsed.port or (5671 if tls else 5672),
        tls,
        parsed.username,
        parsed.password,
        (parsed.path or "").lstrip("/") or None,
    )


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


def _build_weather_producer(args):
    from bom_australia_amqp_producer_amqp_producer.producer import AUGovBOMWeatherAmqpProducer
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
    kwargs = dict(host=host, address=address, port=port,
                  content_mode=args.content_mode, use_tls=tls)
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        kwargs.update(
            credential=ManagedIdentityCredential(client_id=args.entra_client_id)
            if args.entra_client_id else DefaultAzureCredential(),
            entra_audience=args.entra_audience,
        )
    elif args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        kwargs.update(sas_key_name=args.sas_key_name, sas_key=args.sas_key)
    else:
        kwargs.update(username=username, password=password)
    return _apply_partition_key_workaround(AUGovBOMWeatherAmqpProducer(**kwargs))


def _build_warning_producer(args):
    from bom_australia_amqp_producer_amqp_producer.producer import AUGovBOMWarningAmqpProducer
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
    kwargs = dict(host=host, address=address, port=port,
                  content_mode=args.content_mode, use_tls=tls)
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        kwargs.update(
            credential=ManagedIdentityCredential(client_id=args.entra_client_id)
            if args.entra_client_id else DefaultAzureCredential(),
            entra_audience=args.entra_audience,
        )
    elif args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        kwargs.update(sas_key_name=args.sas_key_name, sas_key=args.sas_key)
    else:
        kwargs.update(username=username, password=password)
    return _apply_partition_key_workaround(AUGovBOMWarningAmqpProducer(**kwargs))


async def _run_live(args: argparse.Namespace, weather_producer, warning_producer) -> None:
    """Acquire live BOM data and emit via AMQP."""
    from bom_australia_core import (  # type: ignore[attr-defined]
        BOMAustraliaAPI,
        WARNING_FEEDS,
        _load_state,
        _save_state,
        _parse_station_list,
        _parse_warning_feed_list,
        fetch_stations_parallel,
        fetch_latest_observations_parallel,
        fetch_new_warnings,
    )
    from bom_australia_amqp_producer_data import (
        Station as AmqpStation,
        WeatherObservation as AmqpWeatherObservation,
        WarningBulletin as AmqpWarningBulletin,
    )

    api = BOMAustraliaAPI(
        polling_interval=args.polling_interval,
        fetch_workers=args.fetch_workers,
    )

    if args.stations:
        station_list = _parse_station_list(args.stations)
    else:
        station_list = api.discover_stations(args.state_filter or None)
    warning_feeds = (
        _parse_warning_feed_list(args.warning_feeds)
        if args.warning_feeds
        else list(WARNING_FEEDS)
    )

    state = _load_state(args.state_file)
    previous_observations: dict = state.get("observations", {})
    previous_warnings: dict = state.get("warnings", {})

    logger.info("Emitting station reference data via AMQP (%d stations)…", len(station_list))
    stations = fetch_stations_parallel(api, station_list)
    for core_station, _ in stations:
        amqp_station = AmqpStation(
            station_wmo=core_station.station_wmo,
            name=core_station.name,
            product_id=core_station.product_id,
            state=core_station.state,
            time_zone=core_station.time_zone,
            latitude=core_station.latitude,
            longitude=core_station.longitude,
        )
        weather_producer.send_station(
            data=amqp_station,
            _station_wmo=core_station.station_wmo,
            _state=core_station.state or "unknown",
        )
    logger.info("Sent %d station record(s) via AMQP", len(stations))

    while True:
        logger.info("Polling observations for %d stations…", len(station_list))
        new_obs = fetch_latest_observations_parallel(api, station_list, previous_observations)
        for core_obs, _ in new_obs:
            amqp_obs = AmqpWeatherObservation(
                station_wmo=core_obs.station_wmo,
                station_name=core_obs.station_name,
                observation_time_utc=datetime.fromisoformat(core_obs.observation_time_utc),
                local_time=core_obs.local_time,
                air_temp=core_obs.air_temp,
                apparent_temp=core_obs.apparent_temp,
                dewpt=core_obs.dewpt,
                rel_hum=core_obs.rel_hum,
                delta_t=core_obs.delta_t,
                wind_dir=core_obs.wind_dir,
                wind_spd_kmh=core_obs.wind_spd_kmh,
                wind_spd_kt=core_obs.wind_spd_kt,
                gust_kmh=core_obs.gust_kmh,
                gust_kt=core_obs.gust_kt,
                press=core_obs.press,
                press_qnh=core_obs.press_qnh,
                press_msl=core_obs.press_msl,
                press_tend=core_obs.press_tend,
                rain_trace=core_obs.rain_trace,
                cloud=core_obs.cloud,
                cloud_oktas=core_obs.cloud_oktas,
                cloud_base_m=core_obs.cloud_base_m,
                cloud_type=core_obs.cloud_type,
                vis_km=core_obs.vis_km,
                weather=core_obs.weather,
                sea_state=core_obs.sea_state,
                swell_dir_worded=core_obs.swell_dir_worded,
                swell_height=core_obs.swell_height,
                swell_period=core_obs.swell_period,
                latitude=core_obs.latitude,
                longitude=core_obs.longitude,
                state=core_obs.state,
            )
            weather_producer.send_weather_observation(
                data=amqp_obs,
                _station_wmo=core_obs.station_wmo,
                _state=core_obs.state or "unknown",
            )
        logger.info("Sent %d new observation(s) via AMQP", len(new_obs))

        new_bulletins = fetch_new_warnings(api, warning_feeds, previous_warnings)
        for bulletin in new_bulletins:
            amqp_bulletin = AmqpWarningBulletin(
                warning_id=bulletin.warning_id,
                warning_url=bulletin.warning_url,
                feed_url=bulletin.feed_url,
                feed_title=bulletin.feed_title,
                title=bulletin.title,
                published_at=datetime.fromisoformat(bulletin.published_at),
                issued_local_time_text=bulletin.issued_local_time_text,
                warning_type=bulletin.warning_type,
                affected_area_text=bulletin.affected_area_text,
                severity=bulletin.severity,
                state=bulletin.state,
            )
            warning_producer.send_warning_bulletin(
                data=amqp_bulletin,
                _state=bulletin.state or "unknown",
                _severity=bulletin.severity or "unknown",
                _warning_id=bulletin.warning_id,
            )
        logger.info("Sent %d new warning(s) via AMQP", len(new_bulletins))

        _save_state(
            args.state_file,
            {"observations": previous_observations, "warnings": previous_warnings},
        )

        if args.once:
            break
        await asyncio.sleep(args.polling_interval)


def _add_common_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", SOURCE_ID))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("AMQP_TLS", False))
    parser.add_argument("--content-mode", choices=("binary", "structured"),
                        default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"),
                        default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience",
                        default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    parser.add_argument("--polling-interval", type=int,
                        default=int(os.getenv("POLLING_INTERVAL", "600")))
    parser.add_argument("--fetch-workers", type=int,
                        default=int(os.getenv("BOM_FETCH_WORKERS", "12")))
    parser.add_argument("--state-file",
                        default=os.getenv("STATE_FILE", os.path.expanduser(f"~/.{PY_MODULE}_amqp_state.json")))
    parser.add_argument("--stations", default=os.getenv("BOM_STATIONS", ""))
    parser.add_argument("--state-filter", default=os.getenv("BOM_STATE_FILTER", ""))
    parser.add_argument("--warning-feeds", default=os.getenv("BOM_WARNING_FEEDS", ""))
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    return parser


def _retry_producer_init(factory, max_attempts: int = 5, initial_delay: int = 10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logger.warning(
                "Producer init attempt %d/%d failed: %s. Retrying in %ds…",
                attempt + 1, max_attempts, e, delay,
            )
            time.sleep(delay)


async def _async_main(args: argparse.Namespace) -> None:
    weather_producer = _retry_producer_init(lambda: _build_weather_producer(args))
    warning_producer = _retry_producer_init(lambda: _build_warning_producer(args))
    try:
        await _run_live(args, weather_producer, warning_producer)
    finally:
        for p in (weather_producer, warning_producer):
            close = getattr(p, "close", None)
            if close:
                try:
                    close()
                except Exception:
                    pass


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    parser = _add_common_args(argparse.ArgumentParser(description=f"{SOURCE_ID} AMQP 1.0 bridge"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    asyncio.run(_async_main(args))


if __name__ == "__main__":
    main()
