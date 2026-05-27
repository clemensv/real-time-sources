"""AMQP 1.0 feeder application for EPA UV Index."""

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

from epa_uv.epa_uv import DEFAULT_POLL_INTERVAL_SECONDS, EPAUVBridge, parse_locations
from epa_uv_amqp_producer_data import DailyForecast, HourlyForecast
from epa_uv_amqp_producer_amqp_producer.producer import USEPAUVIndexAmqpProducer

logger = logging.getLogger(__name__)


def _sample_events() -> tuple[list[HourlyForecast], list[DailyForecast]]:
    hourly = HourlyForecast(location_id="seattle-wa", city="Seattle", state="wa", city_slug="seattle", forecast_datetime="2026-01-01T12:00:00", forecast_hour="20260101T12", uv_index=2)
    daily = DailyForecast(location_id="seattle-wa", city="Seattle", state="wa", city_slug="seattle", forecast_date="2026-01-01", uv_index=2, uv_alert="Low")
    return [hourly], [daily]


def _publish(producer: USEPAUVIndexAmqpProducer, hourly_events, daily_events) -> tuple[int, int]:
    hourly_count = 0
    for hourly in hourly_events:
        producer.send_hourly_forecast(data=hourly, _location_id=hourly.location_id, _state=hourly.state, _city_slug=hourly.city_slug, _forecast_hour=hourly.forecast_hour)
        hourly_count += 1
    daily_count = 0
    for daily in daily_events:
        producer.send_daily_forecast(data=daily, _location_id=daily.location_id, _state=daily.state, _city_slug=daily.city_slug, _forecast_date=daily.forecast_date)
        daily_count += 1
    return hourly_count, daily_count


def feed(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args, USEPAUVIndexAmqpProducer)
    bridge = EPAUVBridge(parse_locations(args.locations), state_file=args.state_file)
    try:
        while True:
            if args.mock_mode:
                hourly_events, daily_events = _sample_events()
            else:
                hourly_events = []
                daily_events = []
                for city, state in bridge.locations:
                    for hourly in bridge.fetch_hourly(city, state):
                        event_id = f"{hourly.location_id}|{hourly.forecast_datetime}"
                        if event_id in bridge.seen_hourly_ids:
                            continue
                        hourly_events.append(hourly)
                        bridge._remember(bridge.hourly_order, bridge.seen_hourly_ids, event_id)
                    for daily in bridge.fetch_daily(city, state):
                        event_id = f"{daily.location_id}|{daily.forecast_date}"
                        if event_id in bridge.seen_daily_ids:
                            continue
                        daily_events.append(daily)
                        bridge._remember(bridge.daily_order, bridge.seen_daily_ids, event_id)
                bridge.save_state()
            hourly_count, daily_count = _publish(producer, hourly_events, daily_events)
            logger.info("Published %d hourly and %d daily EPA UV forecasts to AMQP", hourly_count, daily_count)
            if args.once:
                break
            time.sleep(args.polling_interval)
    finally:
        producer.close()


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="EPA UV Index AMQP 1.0 bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    add_amqp_arguments(parser, "epa-uv")
    parser.add_argument("--locations", default=os.getenv("EPA_UV_LOCATIONS", "Seattle,WA"))
    parser.add_argument("--state-file", default=os.getenv("EPA_UV_STATE_FILE", "/var/lib/epa-uv/state.json"))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", str(DEFAULT_POLL_INTERVAL_SECONDS))))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--mock-mode", action="store_true", default=os.getenv("EPA_UV_MOCK", "").lower() in ("1", "true", "yes"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    feed(args)


if __name__ == "__main__":
    main()
