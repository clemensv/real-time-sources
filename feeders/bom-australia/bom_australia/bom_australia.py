"""BOM Australia Weather Observation Bridge - Kafka transport."""

import argparse
import json
import sys
import os
import time
import typing
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from confluent_kafka import Producer

from bom_australia_producer_kafka_producer.producer import AUGovBOMWarningEventProducer
from bom_australia_producer_kafka_producer.producer import AUGovBOMWeatherEventProducer
from bom_australia_producer_data import Station, WarningBulletin, WeatherObservation

from bom_australia_core import (
    BOMAustraliaAPI,
    BOM_BASE_URL,
    BOM_STATIONS_URL,
    STATE_OBSERVATION_PAGES,
    STATION_LINK_PATTERN,
    STATE_TO_PRODUCT,
    FALLBACK_STATIONS,
    WARNING_FEEDS,
    WARNING_TITLE_PATTERN,
    WARNING_FEED_STATE_PATTERN,
    USER_AGENT,
    _warning_id_from_url,
    _parse_warning_feed_list,
    _normalize_state,
    _trim_state_bucket,
    _load_state,
    _save_state,
    _parse_station_list,
    _is_http_404,
)

logger = logging.getLogger(__name__)


def parse_connection_string(connection_string: str) -> dict:
    """Parse a Kafka connection string into a config dict."""
    config: dict[str, str] = {}
    for part in connection_string.split(";"):
        part = part.strip()
        if "=" in part:
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key == "Endpoint":
                config["bootstrap.servers"] = value.replace("sb://", "").rstrip("/") + ":9093"
            elif key == "SharedAccessKeyName":
                config["sasl.username"] = "$ConnectionString"
            elif key == "SharedAccessKey":
                config["sasl.password"] = connection_string
            elif key == "BootstrapServer":
                config["bootstrap.servers"] = value
            elif key == "EntityPath":
                config["_entity_path"] = value
    if "sasl.username" in config:
        config["security.protocol"] = "SASL_SSL"
        config["sasl.mechanism"] = "PLAIN"
    return config


def send_stations(api: BOMAustraliaAPI, producer: AUGovBOMWeatherEventProducer, station_list: list[tuple[str, int]]) -> int:
    """Fetch and emit station reference data for all configured stations."""
    sent_counter = {"n": 0}
    sent_lock = threading.Lock()

    def _process(item: tuple[str, int]) -> None:
        product_id, wmo_id = item
        try:
            obs_data = api.get_station_observations(product_id, wmo_id)
        except Exception as e:
            if _is_http_404(e):
                logger.debug("Station product not published for %s/%d (404)", product_id, wmo_id)
            else:
                logger.warning("Failed to fetch station %s/%d: %s", product_id, wmo_id, e)
            return
        try:
            station = api.parse_station(product_id, obs_data)
            if station:
                kafka_station = Station(
                    station_wmo=station.station_wmo,
                    name=station.name,
                    product_id=station.product_id,
                    state=station.state,
                    time_zone=station.time_zone,
                    latitude=station.latitude,
                    longitude=station.longitude,
                )
                producer.send_au_gov_bom_weather_station(
                    str(station.station_wmo),
                    kafka_station,
                    flush_producer=False,
                )
                with sent_lock:
                    sent_counter["n"] += 1
        except Exception as e:
            logger.warning("Failed to emit station %s/%d: %s", product_id, wmo_id, e)

    with ThreadPoolExecutor(max_workers=api.fetch_workers) as pool:
        list(pool.map(_process, station_list))

    producer.producer.flush()
    logger.info("Sent %d station reference events", sent_counter["n"])
    return sent_counter["n"]


def feed_observations(api: BOMAustraliaAPI, producer: AUGovBOMWeatherEventProducer,
                      station_list: list[tuple[str, int]], previous_readings: dict) -> int:
    """Fetch latest observations for all stations and emit new ones."""
    sent_counter = {"n": 0}
    state_lock = threading.Lock()

    def _process(item: tuple[str, int]) -> None:
        product_id, wmo_id = item
        try:
            obs_data = api.get_station_observations(product_id, wmo_id)
        except Exception as e:
            if _is_http_404(e):
                logger.debug("Observation product missing for %s/%d (404)", product_id, wmo_id)
            else:
                logger.warning("Failed to fetch observations for %s/%d: %s", product_id, wmo_id, e)
            return
        records = obs_data.get("observations", {}).get("data", [])
        if not records:
            return
        header = (obs_data.get("observations", {}).get("header") or [{}])[0]
        latest = records[0]
        obs = api.parse_observation(latest, default_state=header.get("state"))
        if not obs:
            return
        reading_key = f"{obs.station_wmo}:{obs.observation_time_utc}"
        with state_lock:
            if reading_key in previous_readings:
                return
            previous_readings[reading_key] = obs.observation_time_utc
        try:
            kafka_obs = WeatherObservation(
                station_wmo=obs.station_wmo,
                station_name=obs.station_name,
                observation_time_utc=obs.observation_time_utc,
                local_time=obs.local_time,
                air_temp=obs.air_temp,
                apparent_temp=obs.apparent_temp,
                dewpt=obs.dewpt,
                rel_hum=obs.rel_hum,
                delta_t=obs.delta_t,
                wind_dir=obs.wind_dir,
                wind_spd_kmh=obs.wind_spd_kmh,
                wind_spd_kt=obs.wind_spd_kt,
                gust_kmh=obs.gust_kmh,
                gust_kt=obs.gust_kt,
                press=obs.press,
                press_qnh=obs.press_qnh,
                press_msl=obs.press_msl,
                press_tend=obs.press_tend,
                rain_trace=obs.rain_trace,
                cloud=obs.cloud,
                cloud_oktas=obs.cloud_oktas,
                cloud_base_m=obs.cloud_base_m,
                cloud_type=obs.cloud_type,
                vis_km=obs.vis_km,
                weather=obs.weather,
                sea_state=obs.sea_state,
                swell_dir_worded=obs.swell_dir_worded,
                swell_height=obs.swell_height,
                swell_period=obs.swell_period,
                latitude=obs.latitude,
                longitude=obs.longitude,
                state=obs.state,
            )
            producer.send_au_gov_bom_weather_weather_observation(
                str(obs.station_wmo),
                kafka_obs,
                flush_producer=False,
            )
            with state_lock:
                sent_counter["n"] += 1
        except Exception as e:
            logger.warning("Failed to emit observation for %s/%d: %s", product_id, wmo_id, e)

    with ThreadPoolExecutor(max_workers=api.fetch_workers) as pool:
        list(pool.map(_process, station_list))

    producer.producer.flush()
    return sent_counter["n"]


def feed_warnings(api: BOMAustraliaAPI, producer: AUGovBOMWarningEventProducer,
                  warning_feeds: list[str], previous_warnings: dict) -> int:
    """Fetch current warning feeds and emit new or updated bulletin items."""
    sent = 0
    for feed_url in warning_feeds:
        try:
            feed_xml = api.get_warning_feed(feed_url)
            bulletins = api.parse_warning_feed(feed_url, feed_xml)
            for bulletin in bulletins:
                if previous_warnings.get(bulletin.warning_id) == bulletin.published_at:
                    continue
                kafka_bulletin = WarningBulletin(
                    warning_id=bulletin.warning_id,
                    warning_url=bulletin.warning_url,
                    feed_url=bulletin.feed_url,
                    feed_title=bulletin.feed_title,
                    title=bulletin.title,
                    published_at=bulletin.published_at,
                    issued_local_time_text=bulletin.issued_local_time_text,
                    warning_type=bulletin.warning_type,
                    affected_area_text=bulletin.affected_area_text,
                    severity=bulletin.severity,
                    state=bulletin.state,
                )
                producer.send_au_gov_bom_warning_warning_bulletin(
                    bulletin.warning_id,
                    kafka_bulletin,
                    flush_producer=False,
                )
                previous_warnings[bulletin.warning_id] = bulletin.published_at
                sent += 1
        except Exception as e:
            logger.warning("Failed to fetch warnings from %s: %s", feed_url, e)
    producer.producer.flush()
    return sent


def main():
    """Main entry point for the BOM Australia bridge."""
    parser = argparse.ArgumentParser(description="BOM Australia Weather Observation Bridge")
    parser.add_argument("--connection-string", required=False, help="Kafka/Event Hubs connection string",
                        default=os.environ.get("KAFKA_CONNECTION_STRING") or os.environ.get("CONNECTION_STRING"))
    parser.add_argument("--topic", required=False, help="Kafka topic", default=os.environ.get("KAFKA_TOPIC") or None)
    parser.add_argument("--polling-interval", type=int, default=int(os.environ.get("POLLING_INTERVAL", "600")),
                        help="Polling interval in seconds (default: 600)")
    parser.add_argument("--fetch-workers", type=int, default=int(os.environ.get("BOM_FETCH_WORKERS", "12")),
                        help="Concurrent HTTP fetch workers for per-station product downloads (default: 12)")
    parser.add_argument("--state-file", type=str,
                        default=os.environ.get("STATE_FILE", os.path.expanduser("~/.bom_australia_state.json")))
    parser.add_argument("--stations", type=str, default=os.environ.get("BOM_STATIONS", ""),
                        help="Comma-separated product_id:wmo_id pairs (overrides station discovery)")
    parser.add_argument("--state-filter", type=str, default=os.environ.get("BOM_STATE_FILTER", ""),
                        help="Comma-separated state abbreviations to filter (e.g. NSW,VIC)")
    parser.add_argument("--warning-feeds", type=str, default=os.environ.get("BOM_WARNING_FEEDS", ""),
                        help="Comma-separated BOM warning RSS feed URLs or /fwo/... feed paths")
    parser.add_argument("--once", action="store_true",
                        default=os.environ.get("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                        help="Exit after one polling cycle (also via ONCE_MODE env var).")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List configured stations")
    feed_parser = subparsers.add_parser("feed", help="Feed data to Kafka")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    api = BOMAustraliaAPI(polling_interval=args.polling_interval, fetch_workers=args.fetch_workers)
    if args.stations:
        station_list = _parse_station_list(args.stations)
    else:
        station_list = api.discover_stations(args.state_filter or None)
    warning_feeds = _parse_warning_feed_list(args.warning_feeds) if args.warning_feeds else list(WARNING_FEEDS)

    if args.command == "list":
        for product_id, wmo_id in station_list:
            try:
                obs_data = api.get_station_observations(product_id, wmo_id)
                station = api.parse_station(product_id, obs_data)
                if station:
                    print(f"{station.station_wmo}: {station.name} ({station.state}) [{station.latitude}, {station.longitude}]")
            except Exception as e:
                print(f"{product_id}/{wmo_id}: Error - {e}")
    elif args.command == "feed":
        if not args.connection_string:
            if not os.environ.get("KAFKA_BROKER"):
                print("Error: --connection-string or KAFKA_BROKER environment variable required for feed mode")
                sys.exit(1)
            kafka_config: dict[str, str] = {"bootstrap.servers": os.environ["KAFKA_BROKER"]}
        else:
            kafka_config = parse_connection_string(args.connection_string)
        if "_entity_path" in kafka_config and not args.topic:
            args.topic = kafka_config.pop("_entity_path")
        elif "_entity_path" in kafka_config:
            kafka_config.pop("_entity_path")
        if not args.topic:
            args.topic = "bom-australia"
        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        if "sasl.username" in kafka_config:
            kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
        elif tls_enabled and "security.protocol" not in kafka_config:
            pass
        kafka_config["client.id"] = "bom-australia-bridge"
        kafka_producer = Producer(kafka_config)
        event_producer = AUGovBOMWeatherEventProducer(kafka_producer, args.topic)
        warning_producer = AUGovBOMWarningEventProducer(kafka_producer, args.topic)
        logger.info("Starting BOM Australia bridge, polling every %d seconds, %d stations",
                     args.polling_interval, len(station_list))
        state = _load_state(args.state_file)
        send_stations(api, event_producer, station_list)
        while True:
            try:
                observation_count = feed_observations(api, event_producer, station_list, state["observations"])
                warning_count = feed_warnings(api, warning_producer, warning_feeds, state["warnings"])
                _save_state(args.state_file, state)
                logger.info("Sent %d observation events and %d warning events", observation_count, warning_count)
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            if args.once:
                logger.info("--once mode: exiting after first polling cycle")
                break
            time.sleep(args.polling_interval)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
