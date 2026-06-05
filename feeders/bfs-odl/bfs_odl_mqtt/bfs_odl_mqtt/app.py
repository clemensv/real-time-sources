"""MQTT feeder application for BfS ODL → Unified Namespace.

Reuses the upstream HTTP client logic from the existing ``bfs_odl`` Kafka
bridge and pushes CloudEvents into MQTT 5.0 using the xrcg-generated
:class:`DeBfsOdlMqttMqttClient`.

Topic tree: ``radiation/de/bfs/bfs-odl/{state}/{station_id}/{info|dose-rate}``.
``{state}`` is derived from the first two digits of the station Kennziffer
(AGS administrative-region code) and normalized to a lowercase kebab-case slug.
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

from bfs_odl.bfs_odl import BfsOdlAPI, _load_state, _save_state, FEED_URL
from bfs_odl_mqtt_producer_data import Station, DoseRateMeasurement
from bfs_odl_mqtt_producer_mqtt_client.client import DeBfsOdlMqttMqttClient

logger = logging.getLogger(__name__)

# AGS first-two-digit code → Bundesland name
_AGS_TO_STATE: Dict[str, str] = {
    "01": "schleswig-holstein",
    "02": "hamburg",
    "03": "niedersachsen",
    "04": "bremen",
    "05": "nordrhein-westfalen",
    "06": "hessen",
    "07": "rheinland-pfalz",
    "08": "baden-wuerttemberg",
    "09": "bayern",
    "10": "saarland",
    "11": "berlin",
    "12": "brandenburg",
    "13": "mecklenburg-vorpommern",
    "14": "sachsen",
    "15": "sachsen-anhalt",
    "16": "thueringen",
}

_UNS_REPLACEMENTS = str.maketrans({
    "ä": "ae", "ö": "oe", "ü": "ue", "Ä": "ae", "Ö": "oe", "Ü": "ue", "ß": "ss",
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


def _state_from_station_id(station_id: str) -> str:
    """Derive the Bundesland slug from a BfS station Kennziffer (AGS prefix)."""
    prefix = station_id[:2] if len(station_id) >= 2 else ""
    return _AGS_TO_STATE.get(prefix, "unknown")


def _build_station(feature: Dict[str, Any], state: str) -> Station:
    """Build MQTT Station dataclass from a WFS GeoJSON feature."""
    props = feature["properties"]
    geom = feature.get("geometry") or {}
    coords = geom.get("coordinates", [None, None])
    return Station(
        station_id=props["kenn"],
        state=state,
        station_code=props.get("id", ""),
        name=props.get("name", ""),
        postal_code=props.get("plz", ""),
        site_status=props.get("site_status", 0),
        site_status_text=props.get("site_status_text", ""),
        kid=props.get("kid", 0),
        height_above_sea=props.get("height_above_sea"),
        longitude=coords[0] if coords[0] is not None else 0.0,
        latitude=coords[1] if coords[1] is not None else 0.0,
    )


def _build_measurement(feature: Dict[str, Any], state: str) -> DoseRateMeasurement:
    """Build MQTT DoseRateMeasurement dataclass from a WFS GeoJSON feature."""
    props = feature["properties"]
    return DoseRateMeasurement(
        station_id=props["kenn"],
        state=state,
        start_measure=props.get("start_measure", ""),
        end_measure=props.get("end_measure", ""),
        value=props.get("value"),
        value_cosmic=props.get("value_cosmic"),
        value_terrestrial=props.get("value_terrestrial"),
        validated=props.get("validated", 0),
        nuclide=props.get("nuclide", ""),
    )


def _sample_features():
    station = {"type": "Feature", "properties": {"kenn": "033510091", "id": "DEZ0305", "name": "Sample Station", "plz": "30159", "site_status": 1, "site_status_text": "in Betrieb", "kid": 1, "height_above_sea": 55.0}, "geometry": {"type": "Point", "coordinates": [9.73, 52.37]}}
    measurement = {"type": "Feature", "properties": {"kenn": "033510091", "start_measure": "2026-01-01T00:00:00Z", "end_measure": "2026-01-01T01:00:00Z", "value": 0.08, "value_cosmic": 0.03, "value_terrestrial": 0.05, "validated": 1, "nuclide": "Gamma-ODL-Brutto"}, "geometry": {"type": "Point", "coordinates": [9.73, 52.37]}}
    return [station], [measurement]


async def _publish_stations(
    mqtt_client: DeBfsOdlMqttMqttClient,
    stations: list,
) -> None:
    for feature in stations:
        props = feature.get("properties", {})
        station_id = props.get("kenn", "")
        state = _state_from_station_id(station_id)
        try:
            await mqtt_client.publish_de_bfs_odl_mqtt_station(
                feedurl=FEED_URL,
                station_id=station_id,
                state=state,
                data=_build_station(feature, state),
            )
        except Exception as exc:
            logger.error("Error publishing station %s: %s", station_id, exc)


async def _publish_measurements(
    mqtt_client: DeBfsOdlMqttMqttClient,
    measurements: list,
    previous_readings: Dict[str, str],
) -> int:
    sent = 0
    for feature in measurements:
        props = feature.get("properties", {})
        station_id = props.get("kenn", "")
        end_measure = props.get("end_measure", "")
        if station_id in previous_readings and previous_readings[station_id] == end_measure:
            continue
        state = _state_from_station_id(station_id)
        try:
            await mqtt_client.publish_de_bfs_odl_mqtt_dose_rate_measurement(
                feedurl=FEED_URL,
                station_id=station_id,
                state=state,
                data=_build_measurement(feature, state),
            )
            sent += 1
            previous_readings[station_id] = end_measure
        except Exception as exc:
            logger.error("Error publishing measurement for %s: %s", station_id, exc)
    return sent


async def feed(
    api: BfsOdlAPI,
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
    mqtt_client = DeBfsOdlMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=loop,
    )

    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await mqtt_client.connect(broker_host, broker_port)

    stations, sample_measurements = _sample_features() if os.getenv("BFS_ODL_SAMPLE_MODE", "").lower() in ("1", "true", "yes") else (api.fetch_stations(), None)
    logger.info("Publishing %d station info events under radiation/de/bfs/bfs-odl/...", len(stations))
    await _publish_stations(mqtt_client, stations)
    logger.info("Finished publishing station catalog")

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                measurements = sample_measurements if sample_measurements is not None else api.fetch_latest_measurements()
                count = await _publish_measurements(mqtt_client, measurements, previous_readings)
                end_time = datetime.now(timezone.utc)
                effective = max(0, polling_interval - (end_time - start_time).total_seconds())
                logger.info(
                    "Published %d dose-rate measurements in %.1fs. Sleeping until %s.",
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
            except Exception as exc:
                logger.error("Error during polling cycle: %s", exc)
                if once:
                    break
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
    parser = argparse.ArgumentParser(description="BfS ODL → MQTT/UNS bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Feed stations and dose-rate as CloudEvents to MQTT")
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
                             default=int(os.getenv("POLLING_INTERVAL", "3600")))
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.bfs_odl_mqtt_state.json")))
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

    api = BfsOdlAPI()
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
