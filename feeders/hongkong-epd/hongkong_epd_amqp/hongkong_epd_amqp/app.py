"""AMQP 1.0 feeder application for Hong Kong EPD AQHI."""

from __future__ import annotations


import argparse
import logging
import os
from typing import Optional
from urllib.parse import urlparse

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


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


import argparse
import logging
import os
import time
from datetime import datetime, timezone

from hongkong_epd.hongkong_epd import HKEPDAQHIAPI, _load_state, _save_state
STATION_ID_TO_DISTRICT = {
    "central_western": "central-and-western", "eastern": "eastern", "kwai_chung": "kwai-tsing",
    "kwun_tong": "kwun-tong", "north": "north", "sha_tin": "sha-tin",
    "sham_shui_po": "sham-shui-po", "southern": "southern", "tai_po": "tai-po",
    "tap_mun": "islands", "tseung_kwan_o": "sai-kung", "tsuen_wan": "tsuen-wan",
    "tuen_mun": "tuen-mun", "tung_chung": "islands", "yuen_long": "yuen-long",
    "causeway_bay": "wan-chai", "central": "central-and-western", "mong_kok": "yau-tsim-mong",
}
from hongkong_epd_amqp_producer_data import AQHIReading, Station
from hongkong_epd_amqp_producer_amqp_producer.producer import HKGovEPDAQHIAmqpProducer

logger = logging.getLogger(__name__)


def _station_with_district(station_id: str, station) -> Station:
    return Station(station_id=station.station_id, station_name=station.station_name, station_type=station.station_type, district=STATION_ID_TO_DISTRICT.get(station_id, "unknown"), latitude=station.latitude, longitude=station.longitude)


def _reading_with_district(station_id: str, reading) -> AQHIReading:
    return AQHIReading(station_id=reading.station_id, station_name=reading.station_name, station_type=reading.station_type, district=STATION_ID_TO_DISTRICT.get(station_id, "unknown"), reading_time=reading.reading_time, aqhi=reading.aqhi, health_risk_category=reading.health_risk_category)


def _sample_events() -> tuple[list[Station], list[AQHIReading]]:
    station = Station(station_id="central", station_name="Central", station_type="Roadside Stations", district="central-and-western", latitude=22.2836, longitude=114.1571)
    reading = AQHIReading(station_id="central", station_name="Central", station_type="Roadside Stations", district="central-and-western", reading_time=datetime(2026, 1, 1, tzinfo=timezone.utc), aqhi=3, health_risk_category="Low")
    return [station], [reading]


def _publish(producer: HKGovEPDAQHIAmqpProducer, stations: list[Station], readings: list[AQHIReading]) -> tuple[int, int]:
    for station in stations:
        producer.send_station(data=station, _station_id=station.station_id, _district=station.district)
    for reading in readings:
        producer.send_aqhireading(data=reading, _station_id=reading.station_id, _district=reading.district)
    return len(stations), len(readings)


def feed(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args, HKGovEPDAQHIAmqpProducer)
    api = HKEPDAQHIAPI(polling_interval=args.polling_interval)
    previous_readings = _load_state(args.state_file)
    try:
        while True:
            if args.mock_mode:
                stations, readings = _sample_events()
            else:
                stations = [_station_with_district(station_id, station) for station_id, station in api.get_stations().items()]
                readings = []
                for station_id, reading in sorted(api.get_latest_readings().items()):
                    reading_key = f"{station_id}:{reading.reading_time.isoformat()}"
                    if reading_key in previous_readings:
                        continue
                    readings.append(_reading_with_district(station_id, reading))
                    previous_readings[reading_key] = reading.reading_time.isoformat()
                _save_state(args.state_file, previous_readings)
            station_count, reading_count = _publish(producer, stations, readings)
            logger.info("Published %d stations and %d AQHI readings to AMQP", station_count, reading_count)
            if args.once:
                break
            time.sleep(args.polling_interval)
    finally:
        producer.close()


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Hong Kong EPD AQHI AMQP 1.0 bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    add_amqp_arguments(parser, "hongkong-epd")
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "3600")))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", "/var/lib/hongkong-epd/state.json"))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--mock-mode", action="store_true", default=os.getenv("HONGKONG_EPD_MOCK", "").lower() in ("1", "true", "yes"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    feed(args)


if __name__ == "__main__":
    main()
