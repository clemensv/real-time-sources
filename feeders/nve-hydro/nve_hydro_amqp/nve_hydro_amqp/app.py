"""AMQP feeder application for NVE Hydrology → Unified Namespace.

Reuses the upstream HydAPI client and station catalog logic from the
existing ``nve_hydro`` Kafka bridge and pushes CloudEvents into AMQP 1.0
using the xrcg-generated :class:`NONVEHydrologyAmqpProducer`.

Topic tree: ``hydro/no/nve/nve-hydro/{river_name}/{station_id}/{info|water-level}``.
``{river_name}`` is sourced from the NVE HydAPI station catalog
(``riverName`` / Norwegian ``Vassdrag``) and normalized to lowercase
kebab-case by :func:`_uns_slug`.
"""

from __future__ import annotations

import argparse
import asyncio
import time
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from nve_hydro.nve_hydro import (
    NVEHydroAPI,
    PARAM_DISCHARGE,
    PARAM_STAGE,
    REFERENCE_REFRESH_SECONDS,
    _load_state,
    _parse_datetime,
    _save_state,
    fetch_observation_batches,
    _station_has_parameter,
)
from nve_hydro_amqp_producer_data import Station, WaterLevelObservation
from nve_hydro_amqp_producer_amqp_producer.producer import NONVEHydrologyAmqpProducer

logger = logging.getLogger(__name__)

_UNS_REPLACEMENTS = str.maketrans({
    "æ": "ae", "ø": "o", "å": "aa", "Æ": "ae", "Ø": "o", "Å": "aa",
    "ä": "a", "ö": "o", "ü": "u", "Ä": "a", "Ö": "o", "Ü": "u", "ß": "ss",
})


def _uns_slug(value: str) -> str:
    if not value:
        return "unknown"
    raw = value.translate(_UNS_REPLACEMENTS).lower().strip()
    out = []
    for ch in raw:
        if ch.isalnum():
            out.append(ch)
        elif ch in ("-", "_"):
            out.append(ch)
        else:
            out.append("-")
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "unknown"


def _build_station(s: Dict[str, Any]) -> Station:
    masl = s.get("masl")
    drainage_basin_area = s.get("drainageBasinArea")
    return Station(
        station_id=s.get("stationId", ""),
        station_name=s.get("stationName", "") or "",
        river_name=s.get("riverName"),
        latitude=float(s.get("latitude", 0.0) or 0.0),
        longitude=float(s.get("longitude", 0.0) or 0.0),
        masl=float(masl) if masl is not None else None,
        council_name=s.get("councilName"),
        county_name=s.get("countyName"),
        drainage_basin_area=(
            float(drainage_basin_area)
            if drainage_basin_area is not None
            else None
        ),
    )


def _publish_stations(
    producer: NONVEHydrologyAmqpProducer,
    stations: List[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    by_id: Dict[str, Dict[str, Any]] = {}
    for s in stations:
        sid = s.get("stationId")
        if not sid:
            continue
        river_slug = _uns_slug(s.get("riverName", ""))
        by_id[sid] = s
        producer.send_station(
            _station_id=sid,
            _river_name=river_slug,
            data=_build_station(s),
        )
    return by_id


def _publish_observations(
    api: NVEHydroAPI,
    producer: NONVEHydrologyAmqpProducer,
    stations_by_id: Dict[str, Dict[str, Any]],
    previous_readings: Dict[str, Any],
) -> int:
    station_params: Dict[str, List[int]] = {}
    for sid, station in stations_by_id.items():
        params: List[int] = []
        if _station_has_parameter(station, PARAM_STAGE):
            params.append(PARAM_STAGE)
        if _station_has_parameter(station, PARAM_DISCHARGE):
            params.append(PARAM_DISCHARGE)
        if params:
            station_params[sid] = params

    sent = 0
    observations_by_station = fetch_observation_batches(api, station_params)
    for sid, obs_by_param in observations_by_station.items():
        if not obs_by_param:
            continue

        wl_val = None
        wl_ts = ""
        q_val = None
        q_ts = ""
        stage: Dict[str, Any] = {}
        discharge: Dict[str, Any] = {}
        if PARAM_STAGE in obs_by_param:
            stage = obs_by_param[PARAM_STAGE]
            wl_val = float(stage["value"])
            wl_ts = stage.get("time", "")
        if PARAM_DISCHARGE in obs_by_param:
            discharge = obs_by_param[PARAM_DISCHARGE]
            q_val = float(discharge["value"])
            q_ts = discharge.get("time", "")
        if wl_val is None and q_val is None:
            continue

        reading_key = f"{sid}:{wl_ts}:{q_ts}"
        if reading_key in previous_readings:
            continue

        station = stations_by_id.get(sid) or {}
        river_raw = station.get("riverName", "") or ""
        river_slug = _uns_slug(river_raw)
        try:
            producer.send_water_level_observation(
                _station_id=sid,
                _river_name=river_slug,
                data=WaterLevelObservation(
                    station_id=sid,
                    river_name=river_raw,
                    water_level=wl_val,
                    water_level_unit=stage.get("unit") if wl_val is not None else None,
                    water_level_timestamp=_parse_datetime(wl_ts),
                    water_level_quality=stage.get("quality"),
                    water_level_correction=stage.get("correction"),
                    water_level_series_version=stage.get("series_version"),
                    water_level_method=stage.get("method"),
                    discharge=q_val,
                    discharge_unit=discharge.get("unit") if q_val is not None else None,
                    discharge_timestamp=_parse_datetime(q_ts),
                    discharge_quality=discharge.get("quality"),
                    discharge_correction=discharge.get("correction"),
                    discharge_series_version=discharge.get("series_version"),
                    discharge_method=discharge.get("method"),
                ),
            )
            sent += 1
            previous_readings[reading_key] = wl_ts or q_ts
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Error publishing observation for %s: %s", sid, exc)
    return sent


def _publish_mock(producer: NONVEHydrologyAmqpProducer) -> None:
    station = Station(station_id="mock-station", station_name="Mock Station", river_name="Mock River", latitude=60.0, longitude=10.0, masl=100.0, council_name="Mock", county_name="Mock", drainage_basin_area=10.0)
    observation = WaterLevelObservation(
        station_id="mock-station",
        river_name="Mock River",
        water_level=1.23,
        water_level_unit="m",
        water_level_timestamp=datetime.now(timezone.utc),
        water_level_quality=2,
        water_level_correction=0,
        water_level_series_version=1,
        water_level_method="Instantaneous",
        discharge=12.3,
        discharge_unit="m³/s",
        discharge_timestamp=datetime.now(timezone.utc),
        discharge_quality=2,
        discharge_correction=0,
        discharge_series_version=1,
        discharge_method="Instantaneous",
    )
    producer.send_station(data=station, _station_id="mock-station", _river_name="mock-river")
    producer.send_water_level_observation(data=observation, _station_id="mock-station", _river_name="mock-river")


def feed(
    api: NVEHydroAPI,
    broker_host: str,
    broker_port: int,
    polling_interval: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    state_file: str = "",
    once: bool = False,
    content_mode: str = "binary",
    address: str = "nve-hydro",
    auth_mode: str = "password",
    entra_audience: str = "https://servicebus.azure.net/.default",
    entra_client_id: Optional[str] = None,
    sas_key_name: Optional[str] = None,
    sas_key: Optional[str] = None,
) -> None:
    previous_readings = _load_state(state_file)
    producer = _retry_producer_init(lambda: _build_producer(host=broker_host, port=broker_port, address=address, use_tls=tls, content_mode=content_mode, auth_mode=auth_mode, username=username, password=password, entra_audience=entra_audience, entra_client_id=entra_client_id, sas_key_name=sas_key_name, sas_key=sas_key))
    if os.getenv("MOCK_MODE", "").lower() in ("1", "true", "yes"):
        _publish_mock(producer)
        producer.close()
        return


    stations = api.get_stations()
    logger.info("Publishing %d station info events under hydro/no/nve/nve-hydro/...", len(stations))
    stations_by_id = _publish_stations(producer, stations)
    logger.info("Finished publishing station catalog")
    last_station_refresh = time.monotonic()

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                count = _publish_observations(api, producer, stations_by_id, previous_readings)
                end_time = datetime.now(timezone.utc)
                effective = max(0, polling_interval - (end_time - start_time).total_seconds())
                logger.info("Published %d observations in %.1fs.", count, (end_time - start_time).total_seconds())
                _save_state(state_file, previous_readings)
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if time.monotonic() - last_station_refresh >= REFERENCE_REFRESH_SECONDS:
                    refreshed = api.get_stations()
                    stations_by_id = _publish_stations(producer, refreshed)
                    last_station_refresh = time.monotonic()
                    logger.info("Refreshed %d station info events", len(stations_by_id))
                if effective > 0:
                    time.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error during polling cycle: %s", exc)
                time.sleep(polling_interval)
    finally:
        producer.close()



DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"


def _build_producer(*, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username: Optional[str], password: Optional[str], entra_audience: str, entra_client_id: Optional[str], sas_key_name: Optional[str], sas_key: Optional[str]) -> NONVEHydrologyAmqpProducer:
    # WORKAROUND(xregistry/codegen#638): xrcg defaults generated producers to
    # structured mode even when the selected endpoint declares binary mode.
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return NONVEHydrologyAmqpProducer(host=host, address=address, port=port, content_mode=content_mode, credential=credential, entra_audience=entra_audience, use_tls=use_tls)  # type: ignore[arg-type]
    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError("auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return NONVEHydrologyAmqpProducer(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)  # type: ignore[arg-type]
    return NONVEHydrologyAmqpProducer(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=use_tls)  # type: ignore[arg-type]

def _parse_broker_url(url: str) -> tuple:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    path = (parsed.path or "").lstrip("/") or None
    return host, port, tls, user, pwd, path


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NVE Hydrology → AMQP 1.0 bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Feed stations and observations as CloudEvents to AMQP")
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("AMQP_BROKER_URL"))
    feed_parser.add_argument("--broker-host", type=str, default=os.getenv("AMQP_HOST"))
    feed_parser.add_argument("--broker-port", type=int,
                             default=int(os.getenv("AMQP_PORT", "0")) or None)
    feed_parser.add_argument("--username", type=str, default=os.getenv("AMQP_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("AMQP_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true",
                             default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--client-id", type=str, default=os.getenv("AMQP_CLIENT_ID"))
    feed_parser.add_argument("--content-mode", type=str, default=os.getenv("AMQP_CONTENT_MODE", "binary"),
                             choices=["binary", "structured"])
    feed_parser.add_argument("--address", type=str, default=os.getenv("AMQP_ADDRESS", "nve-hydro"))
    feed_parser.add_argument("--auth-mode", type=str, default=os.getenv("AMQP_AUTH_MODE", "password"), choices=["password", "entra", "sas"])
    feed_parser.add_argument("--entra-audience", type=str, default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    feed_parser.add_argument("--entra-client-id", type=str, default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    feed_parser.add_argument("--sas-key-name", type=str, default=os.getenv("AMQP_SAS_KEY_NAME"))
    feed_parser.add_argument("--sas-key", type=str, default=os.getenv("AMQP_SAS_KEY"))
    feed_parser.add_argument("--api-key", type=str, default=os.getenv("NVE_API_KEY"))
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "600")))
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.nve_hydro_amqp_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
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
            logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            import time; time.sleep(delay)
def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.print_help()
        return

    if not args.api_key:
        print("Error: NVE_API_KEY environment variable or --api-key required")
        sys.exit(1)

    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.broker_port:
            port = args.broker_port
        address = path or args.address
        if args.tls:
            tls = True
    else:
        host = args.broker_host or "localhost"
        tls = bool(args.tls)
        port = args.broker_port or (5671 if tls else 5672)
        username = args.username
        password = args.password
        address = args.address

    api = NVEHydroAPI(args.api_key)
    feed(
            api, host, port, args.polling_interval,
            username=username, password=password, tls=tls,
            client_id=args.client_id, state_file=args.state_file,
            once=args.once, content_mode=args.content_mode,
            address=address, auth_mode=args.auth_mode, entra_audience=args.entra_audience,
            entra_client_id=args.entra_client_id, sas_key_name=args.sas_key_name, sas_key=args.sas_key,
        )


if __name__ == "__main__":
    main()
