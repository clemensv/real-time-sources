"""MQTT feeder application for BAFU Hydrology → Unified Namespace.

Reuses the upstream HTTP client and station catalog logic from the existing
``bafu_hydro`` Kafka bridge (imported as the transport-agnostic "core"
package) and pushes CloudEvents into MQTT 5.0 using the xrcg-generated
:class:`CHBAFUHydrologyMqttMqttClient`.

Topic tree: ``hydro/ch/bafu/bafu-hydro/{water_body_name}/{station_id}/{info|water-level}``.
``{water_body_name}`` is sourced from the BAFU/FOEN station catalog
(field ``water-body-name``) and normalized to lowercase kebab-case by
:func:`_uns_slug` so umlauts, spaces and slashes never reach the broker.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from bafu_hydro.bafu_hydro import BAFUHydroAPI, _load_state, _save_state
from bafu_hydro_mqtt_producer_data import Station, WaterLevelObservation
from bafu_hydro_mqtt_producer_mqtt_client.client import CHBAFUHydrologyMqttMqttClient

logger = logging.getLogger(__name__)

PAR_HEIGHT = "height"
PAR_FLOW = "flow"
PAR_TEMPERATURE = "temperature"

_UNS_REPLACEMENTS = str.maketrans({
    "ä": "a", "ö": "o", "ü": "u", "Ä": "a", "Ö": "o", "Ü": "u", "ß": "ss",
    "à": "a", "á": "a", "â": "a", "è": "e", "é": "e", "ê": "e",
    "ì": "i", "í": "i", "î": "i", "ò": "o", "ó": "o", "ô": "o",
    "ù": "u", "ú": "u", "û": "u", "ç": "c", "ñ": "n",
})


def _uns_slug(value: str) -> str:
    """Normalize an arbitrary upstream label to a UNS-safe lowercase kebab segment."""
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


def _build_station(station_id: str, details: Dict[str, Any]) -> Station:
    return Station(
        station_id=station_id,
        name=details.get("name", "") or "",
        water_body_name=details.get("water-body-name", "") or "",
        water_body_type=details.get("water-body-type", "") or "",
        latitude=float(details.get("lat", 0.0) or 0.0),
        longitude=float(details.get("lon", 0.0) or 0.0),
    )


def _build_observation(
    station_id: str,
    water_body_name: str,
    wl_val: float,
    wl_ts_str: str,
    q_val: float,
    q_ts_str: str,
    temp_val: float,
    temp_ts_str: str,
) -> WaterLevelObservation:
    return WaterLevelObservation(
        station_id=station_id,
        water_body_name=water_body_name,
        water_level=wl_val,
        water_level_unit="m",
        water_level_timestamp=wl_ts_str,
        discharge=q_val,
        discharge_unit="m3/s",
        discharge_timestamp=q_ts_str,
        water_temperature=temp_val,
        water_temperature_unit="C",
        water_temperature_timestamp=temp_ts_str,
    )


async def _publish_stations(
    mqtt_client: CHBAFUHydrologyMqttMqttClient,
    locations: Dict[str, Dict[str, Any]],
) -> None:
    for station_id, details in locations.items():
        water_slug = _uns_slug(details.get("water-body-name", ""))
        await mqtt_client.publish_ch_bafu_hydrology_mqtt_station(
            station_id=station_id,
            water_body_name=water_slug,
            data=_build_station(station_id, details),
        )


async def _publish_observations(
    api: BAFUHydroAPI,
    mqtt_client: CHBAFUHydrologyMqttMqttClient,
    locations: Dict[str, Dict[str, Any]],
    previous_readings: Dict[str, Any],
) -> int:
    latest = api.get_latest()
    measurements_by_station: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for m in latest:
        loc = str(m.get("loc", ""))
        par = m.get("par", "")
        val = m.get("val")
        ts = m.get("timestamp")
        if not loc or val is None:
            continue
        measurements_by_station.setdefault(loc, {})[par] = {"value": val, "timestamp": ts}

    sent = 0
    for station_id, params in measurements_by_station.items():
        details = locations.get(station_id)
        if details is None:
            continue

        wl_val = 0.0
        wl_ts_str = ""
        q_val = 0.0
        q_ts_str = ""
        temp_val = 0.0
        temp_ts_str = ""

        if PAR_HEIGHT in params:
            h = params[PAR_HEIGHT]
            ts = h.get("timestamp")
            wl_ts_str = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() if ts else ""
            wl_val = float(h["value"])
        if PAR_FLOW in params:
            f = params[PAR_FLOW]
            ts = f.get("timestamp")
            q_ts_str = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() if ts else ""
            q_val = float(f["value"])
        if PAR_TEMPERATURE in params:
            t = params[PAR_TEMPERATURE]
            ts = t.get("timestamp")
            temp_ts_str = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() if ts else ""
            temp_val = float(t["value"])

        if not wl_ts_str and not q_ts_str and not temp_ts_str:
            continue

        reading_key = f"{station_id}:{wl_ts_str}:{q_ts_str}:{temp_ts_str}"
        if reading_key in previous_readings:
            continue

        water_body_name_raw = details.get("water-body-name", "") or ""
        water_slug = _uns_slug(water_body_name_raw)
        try:
            await mqtt_client.publish_ch_bafu_hydrology_mqtt_water_level_observation(
                station_id=station_id,
                water_body_name=water_slug,
                data=_build_observation(
                    station_id, water_body_name_raw,
                    wl_val, wl_ts_str, q_val, q_ts_str, temp_val, temp_ts_str,
                ),
            )
            sent += 1
            previous_readings[reading_key] = wl_ts_str or q_ts_str or temp_ts_str
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Error publishing observation for %s: %s", station_id, exc)
    return sent


async def feed(
    api: BAFUHydroAPI,
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
    mqtt_client = CHBAFUHydrologyMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=loop,
    )

    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await mqtt_client.connect(broker_host, broker_port)

    locations = api.get_locations()
    logger.info("Publishing %d station info events under hydro/ch/bafu/bafu-hydro/...", len(locations))
    await _publish_stations(mqtt_client, locations)
    logger.info("Finished publishing station catalog")

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                count = await _publish_observations(api, mqtt_client, locations, previous_readings)
                end_time = datetime.now(timezone.utc)
                effective = max(0, polling_interval - (end_time - start_time).total_seconds())
                logger.info(
                    "Published %s observations in %.1fs. Sleeping until %s.",
                    count,
                    (end_time - start_time).total_seconds(),
                    (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
                )
                _save_state(state_file, previous_readings)
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if effective > 0:
                    await asyncio.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error during polling cycle: %s", exc)
                await asyncio.sleep(polling_interval)
    finally:
        await mqtt_client.disconnect()


def _parse_broker_url(url: str) -> tuple:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    port = parsed.port or (8883 if tls else 1883)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    return host, port, tls, user, pwd


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BAFU Hydrology → MQTT/UNS bridge.")
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
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.bafu_hydro_mqtt_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    return parser


def main(argv: Optional[list] = None) -> None:
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

    api = BAFUHydroAPI()
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
