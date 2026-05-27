"""MQTT feeder application for King County Marine → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
import logging
import os
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from king_county_marine.king_county_marine import KingCountyMarineBridge, REFERENCE_REFRESH_SECONDS
from king_county_marine_mqtt_producer_data import Station, WaterQualityReading
from king_county_marine_mqtt_producer_mqtt_client.client import USWAKingCountyMarineMqttMqttClient

logger = logging.getLogger(__name__)


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls


def _sample_events() -> tuple[list[Station], list[WaterQualityReading]]:
    station = Station(
        station_id="sample-station",
        station_name="Sample Marine Station",
        dataset_id="sample-dataset",
        dataset_name="Sample Marine Raw Data Output",
        dataset_url="https://data.kingcounty.gov/d/sample-dataset",
        sensor_level="surface",
        latitude=47.6,
        longitude=-122.3,
    )
    reading = WaterQualityReading(
        station_id="sample-station",
        station_name="Sample Marine Station",
        observation_time="2026-01-01T00:00:00Z",
        water_temperature_c=10.5,
        conductivity_s_m=None,
        pressure_dbar=None,
        dissolved_oxygen_mg_l=8.1,
        ph=7.8,
        chlorophyll_ug_l=None,
        turbidity_ntu=1.2,
        chlorophyll_stddev_ug_l=None,
        turbidity_stddev_ntu=None,
        salinity_psu=28.0,
        specific_conductivity_s_m=None,
        dissolved_oxygen_saturation_pct=95.0,
        nitrate_umol=None,
        nitrate_mg_l=None,
        wind_direction_deg=None,
        wind_speed_m_s=None,
        photosynthetically_active_radiation_umol_s_m2=None,
        air_temperature_f=None,
        air_humidity_pct=None,
        air_pressure_in_hg=None,
        system_battery_v=12.4,
        sensor_battery_v=None,
    )
    return [station], [reading]


async def feed(
    broker_host: str,
    broker_port: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    once: bool = False,
    content_mode: str = "binary",
    state_file: str = "",
    sample_mode: bool = False,
) -> None:
    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=client_id or "",
        protocol=MQTTv5,
    )
    if username:
        paho_client.username_pw_set(username, password or "")
    if tls:
        paho_client.tls_set()

    mqtt_client = USWAKingCountyMarineMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=asyncio.get_running_loop(),
    )
    bridge = KingCountyMarineBridge(state_file=state_file)

    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await mqtt_client.connect(broker_host, broker_port)
    try:
        while True:
            if sample_mode:
                stations, readings = _sample_events()
            else:
                stations = []
                readings = []
                refresh_references = True
                if bridge.last_reference_refresh:
                    last = datetime.fromisoformat(bridge.last_reference_refresh)
                    refresh_references = (datetime.now(timezone.utc) - last).total_seconds() >= REFERENCE_REFRESH_SECONDS
                if refresh_references or not bridge.station_metadata:
                    metadata = {}
                    for dataset in bridge.discover_datasets():
                        view = bridge.fetch_view(dataset["id"])
                        station = bridge.build_station(view)
                        stations.append(Station(**dataclasses.asdict(station)))
                        metadata[dataset["id"]] = {"station_id": station.station_id, "station_name": station.station_name, "sensor_level": station.sensor_level}
                    if metadata:
                        bridge.station_metadata = metadata  # type: ignore[assignment]
                        bridge.last_reference_refresh = datetime.now(timezone.utc).isoformat()
                for dataset_id in list(bridge.station_metadata.keys()):
                    for row in reversed(bridge.fetch_rows(dataset_id)):
                        reading = bridge.build_reading(dataset_id, row)
                        reading_id = f"{reading.station_id}|{reading.observation_time}"
                        if reading_id in bridge.seen_reading_ids:
                            continue
                        readings.append(WaterQualityReading(**dataclasses.asdict(reading)))
                        bridge._remember(reading_id)
                bridge.save_state()
            for station in stations:
                await mqtt_client.publish_us_wa_king_county_marine_mqtt_station(station.station_id, station)
            for reading in readings:
                await mqtt_client.publish_us_wa_king_county_marine_mqtt_water_quality_reading(reading.station_id, reading)
            logger.info("Published %d stations and %d readings to MQTT", len(stations), len(readings))
            if once:
                break
            await asyncio.sleep(900)
    finally:
        await mqtt_client.disconnect()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="King County Marine MQTT/UNS bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--state-file", default=os.getenv("KING_COUNTY_MARINE_STATE_FILE", "/var/lib/king-county-marine/state.json"))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    parser.add_argument("--sample-mode", action="store_true", default=os.getenv("KING_COUNTY_MARINE_SAMPLE_MODE", "").lower() in ("1", "true", "yes"))
    args = parser.parse_args()
    if args.feed != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, parsed_tls = _parse_broker_url(args.broker_url)
    asyncio.run(feed(
        host,
        port,
        username=args.username or None,
        password=args.password or None,
        tls=parsed_tls,
        client_id=args.client_id or None,
        once=args.once,
        content_mode=args.content_mode,
        state_file=args.state_file,
        sample_mode=args.sample_mode,
    ))


if __name__ == "__main__":
    main()
