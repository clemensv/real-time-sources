
import argparse
import logging
import os
from typing import Optional
from urllib.parse import urlparse

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"


def _parse_amqp_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    return parsed.hostname or "localhost", port, tls, parsed.username or None, parsed.password or None, (parsed.path or "").lstrip("/") or None


def _build_amqp_producer(producer_cls, *, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username: Optional[str], password: Optional[str], entra_audience: str, entra_client_id: Optional[str], sas_key_name: Optional[str], sas_key: Optional[str]):
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return producer_cls(host=host, address=address, port=port, content_mode=content_mode, credential=credential, entra_audience=entra_audience, use_tls=use_tls)
    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return producer_cls(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)
    return producer_cls(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=use_tls)


def add_amqp_arguments(parser: argparse.ArgumentParser, default_address: str) -> None:
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", default_address))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))


def create_amqp_producer(args: argparse.Namespace, producer_cls):
    address = args.address
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_amqp_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        if path:
            address = path
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    if not address:
        raise RuntimeError("AMQP address is required")
    logging.info("Connecting AMQP producer to %s:%s/%s auth=%s tls=%s", host, port, address, args.auth_mode, tls)
    return _build_amqp_producer(producer_cls, host=host, port=port, address=address, use_tls=tls, content_mode=args.content_mode, auth_mode=args.auth_mode, username=username, password=password, entra_audience=args.entra_audience, entra_client_id=args.entra_client_id, sas_key_name=args.sas_key_name, sas_key=args.sas_key)

import asyncio
import dataclasses
import logging
from datetime import datetime, timezone

from king_county_marine.king_county_marine import KingCountyMarineBridge, REFERENCE_REFRESH_SECONDS
from king_county_marine_amqp_producer_data import Station, WaterQualityReading
from king_county_marine_amqp_producer_amqp_producer.producer import USWAKingCountyMarineAmqpProducer

logger = logging.getLogger(__name__)


def _sample_events() -> tuple[list[Station], list[WaterQualityReading]]:
    station = Station(station_id="sample-station", station_name="Sample Marine Station", dataset_id="sample-dataset", dataset_name="Sample Marine Raw Data Output", dataset_url="https://data.kingcounty.gov/d/sample-dataset", sensor_level="surface", latitude=47.6, longitude=-122.3)
    reading = WaterQualityReading(station_id="sample-station", station_name="Sample Marine Station", observation_time="2026-01-01T00:00:00Z", water_temperature_c=10.5, conductivity_s_m=None, pressure_dbar=None, dissolved_oxygen_mg_l=8.1, ph=7.8, chlorophyll_ug_l=None, turbidity_ntu=1.2, chlorophyll_stddev_ug_l=None, turbidity_stddev_ntu=None, salinity_psu=28.0, specific_conductivity_s_m=None, dissolved_oxygen_saturation_pct=95.0, nitrate_umol=None, nitrate_mg_l=None, wind_direction_deg=None, wind_speed_m_s=None, photosynthetically_active_radiation_umol_s_m2=None, air_temperature_f=None, air_humidity_pct=None, air_pressure_in_hg=None, system_battery_v=12.4, sensor_battery_v=None)
    return [station], [reading]


def _to_station(obj) -> Station:
    return Station(**dataclasses.asdict(obj))


def _to_reading(obj) -> WaterQualityReading:
    return WaterQualityReading(**dataclasses.asdict(obj))


async def feed(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args, USWAKingCountyMarineAmqpProducer)
    bridge = KingCountyMarineBridge(state_file=args.state_file)
    try:
        while True:
            if args.sample_mode:
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
                        stations.append(_to_station(station))
                        metadata[dataset["id"]] = {"station_id": station.station_id, "station_name": station.station_name, "sensor_level": station.sensor_level}
                    if metadata:
                        bridge.station_metadata = metadata  # type: ignore[assignment]
                        bridge.last_reference_refresh = datetime.now(timezone.utc).isoformat()
                for dataset_id in list(bridge.station_metadata.keys()):
                    for row in reversed(bridge.fetch_rows(dataset_id)):
                        reading = bridge.build_reading(dataset_id, row)
                        reading_id = f"{reading.station_id}|{reading.observation_time}"
                        if reading_id in bridge.seen_reading_ids: continue
                        readings.append(_to_reading(reading)); bridge._remember(reading_id)
                bridge.save_state()
            for station in stations:
                producer.send_station(data=station, _station_id=station.station_id)
            for reading in readings:
                producer.send_water_quality_reading(data=reading, _station_id=reading.station_id)
            logger.info("Published %d stations and %d readings to AMQP", len(stations), len(readings))
            if args.once: break
            await asyncio.sleep(900)
    finally:
        producer.close()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="King County Marine AMQP 1.0 bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    add_amqp_arguments(parser, "king-county-marine")
    parser.add_argument("--state-file", default=os.getenv("KING_COUNTY_MARINE_STATE_FILE", "/var/lib/king-county-marine/state.json"))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1","true","yes"))
    parser.add_argument("--sample-mode", action="store_true", default=os.getenv("KING_COUNTY_MARINE_SAMPLE_MODE", "").lower() in ("1","true","yes"))
    args = parser.parse_args()
    if args.feed_command != "feed": parser.error("only the 'feed' command is supported")
    asyncio.run(feed(args))

if __name__ == "__main__": main()
