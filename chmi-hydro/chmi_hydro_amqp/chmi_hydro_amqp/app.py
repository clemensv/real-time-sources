"""AMQP feeder application for CHMI Hydrology → Unified Namespace.

Reuses the upstream API client and parsing helpers from the existing
``chmi_hydro`` Kafka bridge and pushes CloudEvents into AMQP 1.0 using
the xrcg-generated :class:`CZGovCHMIHydroAmqpProducer`.

Topic tree: ``hydro/cz/chmi/chmi-hydro/{stream_name}/{station_id}/{info|water-level}``.
``{stream_name}`` comes from the CHMI station metadata (``SPA_TYP`` row,
field ``RTOK_NAZEV``) and is normalized to lowercase kebab-case by
:func:`_uns_slug`.
"""

from __future__ import annotations

import argparse
import time
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

from chmi_hydro.chmi_hydro import (
    CHMIHydroAPI,
    _load_state,
    _save_state,
)
from chmi_hydro_amqp_producer_data import Station, WaterLevelObservation
from chmi_hydro_amqp_producer_amqp_producer.producer import CZGovCHMIHydroAmqpProducer

logger = logging.getLogger(__name__)

_UNS_REPLACEMENTS = str.maketrans({
    "á": "a", "č": "c", "ď": "d", "é": "e", "ě": "e", "í": "i", "ň": "n",
    "ó": "o", "ř": "r", "š": "s", "ť": "t", "ú": "u", "ů": "u", "ý": "y", "ž": "z",
    "Á": "a", "Č": "c", "Ď": "d", "É": "e", "Ě": "e", "Í": "i", "Ň": "n",
    "Ó": "o", "Ř": "r", "Š": "s", "Ť": "t", "Ú": "u", "Ů": "u", "Ý": "y", "Ž": "z",
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


def _publish_stations(
    producer: CZGovCHMIHydroAmqpProducer,
    api: CHMIHydroAPI,
):
    metadata = api.get_metadata()
    stations_by_id = {}
    for record in metadata:
        station = api.parse_station(record)
        stations_by_id[station.station_id] = station
        producer.send_station(
            _station_id=station.station_id,
            _stream_name=_uns_slug(station.stream_name or ""),
            data=Station(
                _station_id=station.station_id,
                dbc=station.dbc,
                station_name=station.station_name,
                _stream_name=station.stream_name or "",
                latitude=station.latitude,
                longitude=station.longitude,
                flood_level_1=station.flood_level_1,
                flood_level_2=station.flood_level_2,
                flood_level_3=station.flood_level_3,
                flood_level_4=station.flood_level_4,
                has_forecast=station.has_forecast,
            ),
        )
    return stations_by_id


def _publish_observations(
    api: CHMIHydroAPI,
    producer: CZGovCHMIHydroAmqpProducer,
    stations_by_id,
    previous_readings,
) -> int:
    sent = 0
    station_ids = list(stations_by_id.keys())
    all_data = api.get_all_station_data(station_ids)
    for sid, data in all_data.items():
        station = stations_by_id.get(sid)
        if not station:
            continue
        obs = api.parse_observation(sid, station.station_name, station.stream_name or "", data)
        if not obs:
            continue
        reading_key = f"{sid}:{obs.water_level_timestamp or ''}"
        if reading_key in previous_readings:
            continue
        try:
            producer.send_water_level_observation(
                _station_id=sid,
                _stream_name=_uns_slug(station.stream_name or ""),
                data=WaterLevelObservation(
                    _station_id=obs.station_id,
                    station_name=obs.station_name,
                    _stream_name=obs.stream_name or "",
                    water_level=obs.water_level,
                    water_level_timestamp=obs.water_level_timestamp,
                    discharge=obs.discharge,
                    discharge_timestamp=obs.discharge_timestamp,
                    water_temperature=obs.water_temperature,
                    water_temperature_timestamp=obs.water_temperature_timestamp,
                ),
            )
            previous_readings[reading_key] = obs.water_level_timestamp or ""
            sent += 1
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Failed to publish observation for %s: %s", sid, exc)
    return sent


def _publish_mock(producer: CZGovCHMIHydroAmqpProducer) -> None:
    station = Station(station_id="mock-station", dbc="MOCK", station_name="Mock Station", stream_name="Mock Stream", latitude=50.0, longitude=14.0, flood_level_1=1.0, flood_level_2=2.0, flood_level_3=3.0, flood_level_4=4.0, has_forecast=False)
    observation = WaterLevelObservation(station_id="mock-station", station_name="Mock Station", stream_name="Mock Stream", water_level=123.0, water_level_timestamp=datetime.now(timezone.utc), discharge=12.3, discharge_timestamp=datetime.now(timezone.utc), water_temperature=8.0, water_temperature_timestamp=datetime.now(timezone.utc))
    producer.send_station(data=station, _station_id="mock-station", _stream_name="mock-stream")
    producer.send_water_level_observation(data=observation, _station_id="mock-station", _stream_name="mock-stream")


def feed(
    api: CHMIHydroAPI,
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
    address: str = "chmi-hydro",
    auth_mode: str = "password",
    entra_audience: str = "https://servicebus.azure.net/.default",
    entra_client_id: Optional[str] = None,
    sas_key_name: Optional[str] = None,
    sas_key: Optional[str] = None,
) -> None:
    previous_readings = _load_state(state_file)
    producer = _build_producer(host=broker_host, port=broker_port, address=address, use_tls=tls, content_mode=content_mode, auth_mode=auth_mode, username=username, password=password, entra_audience=entra_audience, entra_client_id=entra_client_id, sas_key_name=sas_key_name, sas_key=sas_key)
    if os.getenv("MOCK_MODE", "").lower() in ("1", "true", "yes"):
        _publish_mock(producer)
        producer.close()
        return


    logger.info("Publishing CHMI station catalog as AMQP info events...")
    stations_by_id = _publish_stations(producer, api)
    logger.info("Published %d station info events", len(stations_by_id))

    try:
        while True:
            try:
                start = datetime.now(timezone.utc)
                count = _publish_observations(api, producer, stations_by_id, previous_readings)
                end = datetime.now(timezone.utc)
                elapsed = (end - start).total_seconds()
                logger.info("Published %d observations in %.1fs.", count, elapsed)
                _save_state(state_file, previous_readings)
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                sleep_for = max(0, polling_interval - elapsed)
                if sleep_for > 0:
                    time.sleep(sleep_for)
            except KeyboardInterrupt:
                break
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error during polling cycle: %s", exc)
                time.sleep(polling_interval)
    finally:
        producer.close()



DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"


def _build_producer(*, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username: Optional[str], password: Optional[str], entra_audience: str, entra_client_id: Optional[str], sas_key_name: Optional[str], sas_key: Optional[str]) -> CZGovCHMIHydroAmqpProducer:
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return CZGovCHMIHydroAmqpProducer(host=host, address=address, port=port, content_mode=content_mode, credential=credential, entra_audience=entra_audience, use_tls=use_tls)  # type: ignore[arg-type]
    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError("auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return CZGovCHMIHydroAmqpProducer(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)  # type: ignore[arg-type]
    return CZGovCHMIHydroAmqpProducer(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=use_tls)  # type: ignore[arg-type]

def _parse_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    return host, port, tls, user, pwd


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CHMI Hydrology → AMQP 1.0 bridge.")
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
    feed_parser.add_argument("--address", type=str, default=os.getenv("AMQP_ADDRESS", "chmi-hydro"))
    feed_parser.add_argument("--auth-mode", type=str, default=os.getenv("AMQP_AUTH_MODE", "password"), choices=["password", "entra", "sas"])
    feed_parser.add_argument("--entra-audience", type=str, default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    feed_parser.add_argument("--entra-client-id", type=str, default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    feed_parser.add_argument("--sas-key-name", type=str, default=os.getenv("AMQP_SAS_KEY_NAME"))
    feed_parser.add_argument("--sas-key", type=str, default=os.getenv("AMQP_SAS_KEY"))
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "600")))
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.chmi_hydro_amqp_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    return parser


def main(argv=None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.print_help()
        return

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

    api = CHMIHydroAPI()
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
