"""MQTT feeder application for CHMI Hydrology → Unified Namespace.

Reuses the upstream API client and parsing helpers from the existing
``chmi_hydro`` Kafka bridge and pushes CloudEvents into MQTT 5.0 using
the xrcg-generated :class:`CZGovCHMIHydroMqttMqttClient`.

Topic tree: ``hydro/cz/chmi/chmi-hydro/{stream_name}/{station_id}/{info|water-level}``.
``{stream_name}`` comes from the CHMI station metadata (``SPA_TYP`` row,
field ``RTOK_NAZEV``) and is normalized to lowercase kebab-case by
:func:`_uns_slug`.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from chmi_hydro.chmi_hydro import (
    CHMIHydroAPI,
    _load_state,
    _save_state,
)
from chmi_hydro_mqtt_producer_data import Station, WaterLevelObservation
from chmi_hydro_mqtt_producer_mqtt_client.client import CZGovCHMIHydroMqttMqttClient

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


async def _publish_stations(
    mqtt_client: CZGovCHMIHydroMqttMqttClient,
    api: CHMIHydroAPI,
):
    metadata = api.get_metadata()
    stations_by_id = {}
    for record in metadata:
        station = api.parse_station(record)
        stations_by_id[station.station_id] = station
        await mqtt_client.publish_cz_gov_chmi_hydro_mqtt_station(
            station_id=station.station_id,
            stream_name=_uns_slug(station.stream_name or ""),
            data=Station(
                station_id=station.station_id,
                dbc=station.dbc,
                station_name=station.station_name,
                stream_name=station.stream_name or "",
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


async def _publish_observations(
    api: CHMIHydroAPI,
    mqtt_client: CZGovCHMIHydroMqttMqttClient,
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
            await mqtt_client.publish_cz_gov_chmi_hydro_mqtt_water_level_observation(
                station_id=sid,
                stream_name=_uns_slug(station.stream_name or ""),
                data=WaterLevelObservation(
                    station_id=obs.station_id,
                    station_name=obs.station_name,
                    stream_name=obs.stream_name or "",
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


async def feed(
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
) -> None:
    previous_readings = _load_state(state_file)
    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=client_id or "",
        protocol=MQTTv5,
    )
    if username:
        paho_client.username_pw_set(username, password or "")
    if tls:
        paho_client.tls_set()

    loop = asyncio.get_running_loop()
    mqtt_client = CZGovCHMIHydroMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=loop,
    )

    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await mqtt_client.connect(broker_host, broker_port)

    logger.info("Publishing CHMI station catalog as MQTT info events...")
    stations_by_id = await _publish_stations(mqtt_client, api)
    logger.info("Published %d station info events", len(stations_by_id))

    try:
        while True:
            try:
                start = datetime.now(timezone.utc)
                count = await _publish_observations(api, mqtt_client, stations_by_id, previous_readings)
                end = datetime.now(timezone.utc)
                elapsed = (end - start).total_seconds()
                logger.info("Published %d observations in %.1fs.", count, elapsed)
                _save_state(state_file, previous_readings)
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                sleep_for = max(0, polling_interval - elapsed)
                if sleep_for > 0:
                    await asyncio.sleep(sleep_for)
            except KeyboardInterrupt:
                break
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error during polling cycle: %s", exc)
                await asyncio.sleep(polling_interval)
    finally:
        await mqtt_client.disconnect()


def _parse_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    port = parsed.port or (8883 if tls else 1883)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    return host, port, tls, user, pwd


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CHMI Hydrology → MQTT/UNS bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Feed stations and observations as CloudEvents to MQTT")
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("MQTT_BROKER_URL"))
    feed_parser.add_argument("--broker-host", type=str, default=os.getenv("MQTT_HOST"))
    feed_parser.add_argument("--broker-port", type=int,
                             default=int(os.getenv("MQTT_PORT", "0")) or None)
    feed_parser.add_argument("--username", type=str, default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true",
                             default=os.getenv("MQTT_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--client-id", type=str, default=os.getenv("MQTT_CLIENT_ID"))
    feed_parser.add_argument("--content-mode", type=str, default=os.getenv("MQTT_CONTENT_MODE", "binary"),
                             choices=["binary", "structured"])
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "600")))
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.chmi_hydro_mqtt_state.json")))
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
        host, port, tls, user, pwd = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.broker_port:
            port = args.broker_port
        if args.tls:
            tls = True
    else:
        host = args.broker_host or "localhost"
        tls = bool(args.tls)
        port = args.broker_port or (8883 if tls else 1883)
        username = args.username
        password = args.password

    api = CHMIHydroAPI()
    asyncio.run(
        feed(
            api, host, port, args.polling_interval,
            username=username, password=password, tls=tls,
            client_id=args.client_id, state_file=args.state_file,
            once=args.once, content_mode=args.content_mode,
        )
    )


if __name__ == "__main__":
    main()
