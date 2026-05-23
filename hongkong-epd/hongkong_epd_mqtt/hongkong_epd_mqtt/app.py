"""MQTT feeder application for Hong Kong EPD AQHI → Unified Namespace.

Reuses the upstream HTTP client and station catalog logic from the existing
``hongkong_epd`` Kafka bridge and pushes CloudEvents into MQTT 5.0 using the
xrcg-generated :class:`HKGovEPDAQHIMqttMqttClient`.

Topic tree: ``aq/hk/epd/hongkong-epd/{district}/{station_id}/{info|aqhi}``.
``{district}`` is the Hong Kong 18-district administrative area where the
station is located, normalized to lowercase snake_case.
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

from hongkong_epd.hongkong_epd import (
    HKEPDAQHIAPI,
    STATION_COORDS,
    _load_state,
    _save_state,
)
from hongkong_epd_mqtt_producer_data import AQHIReading, Station
from hongkong_epd_mqtt_producer_mqtt_client.client import HKGovEPDAQHIMqttMqttClient

logger = logging.getLogger(__name__)

# Mapping from station_id to the Hong Kong 18-district administrative area.
STATION_ID_TO_DISTRICT: Dict[str, str] = {
    "central_western": "central_and_western",
    "eastern": "eastern",
    "kwai_chung": "kwai_tsing",
    "kwun_tong": "kwun_tong",
    "north": "north",
    "sha_tin": "sha_tin",
    "sham_shui_po": "sham_shui_po",
    "southern": "southern",
    "tai_po": "tai_po",
    "tap_mun": "islands",
    "tseung_kwan_o": "sai_kung",
    "tsuen_wan": "tsuen_wan",
    "tuen_mun": "tuen_mun",
    "tung_chung": "islands",
    "yuen_long": "yuen_long",
    "causeway_bay": "wan_chai",
    "central": "central_and_western",
    "mong_kok": "yau_tsim_mong",
}


async def _publish_stations(
    mqtt_client: HKGovEPDAQHIMqttMqttClient,
    api: HKEPDAQHIAPI,
) -> None:
    """Emit station reference data as retained /info events."""
    stations = api.get_stations()
    for station_id, station in stations.items():
        district = STATION_ID_TO_DISTRICT.get(station_id, "unknown")
        mqtt_station = Station(
            station_id=station.station_id,
            station_name=station.station_name,
            station_type=station.station_type,
            district=district,
            latitude=station.latitude,
            longitude=station.longitude,
        )
        await mqtt_client.publish_hk_gov_epd_aqhi_mqtt_station(
            station_id=station_id,
            district=district,
            data=mqtt_station,
        )


async def _publish_readings(
    mqtt_client: HKGovEPDAQHIMqttMqttClient,
    api: HKEPDAQHIAPI,
    previous_readings: Dict[str, Any],
) -> int:
    """Emit latest AQHI readings as retained /aqhi events, deduplicated."""
    readings = api.get_latest_readings()
    sent = 0
    for station_id, reading in sorted(readings.items()):
        reading_key = f"{station_id}:{reading.reading_time.isoformat()}"
        if reading_key in previous_readings:
            continue
        district = STATION_ID_TO_DISTRICT.get(station_id, "unknown")
        mqtt_reading = AQHIReading(
            station_id=reading.station_id,
            station_name=reading.station_name,
            station_type=reading.station_type,
            district=district,
            reading_time=reading.reading_time,
            aqhi=reading.aqhi,
            health_risk_category=reading.health_risk_category,
        )
        try:
            await mqtt_client.publish_hk_gov_epd_aqhi_mqtt_aqhireading(
                station_id=station_id,
                district=district,
                data=mqtt_reading,
            )
            sent += 1
            previous_readings[reading_key] = reading.reading_time.isoformat()
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Error publishing AQHI reading for %s: %s", station_id, exc)
    return sent


async def feed(
    api: HKEPDAQHIAPI,
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
    mqtt_client = HKGovEPDAQHIMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=loop,
    )

    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await mqtt_client.connect(broker_host, broker_port)

    logger.info("Publishing station info events under aq/hk/epd/hongkong-epd/...")
    await _publish_stations(mqtt_client, api)
    logger.info("Finished publishing station catalog")

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                count = await _publish_readings(mqtt_client, api, previous_readings)
                end_time = datetime.now(timezone.utc)
                effective = max(0, polling_interval - (end_time - start_time).total_seconds())
                logger.info(
                    "Published %s AQHI readings in %.1fs. Sleeping until %s.",
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
    parser = argparse.ArgumentParser(description="Hong Kong EPD AQHI → MQTT/UNS bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Feed stations and AQHI readings as CloudEvents to MQTT")
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
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.hongkong_epd_mqtt_state.json")))
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

    api = HKEPDAQHIAPI(polling_interval=args.polling_interval)
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
