"""DWD Open Data bridge — aggregates weather observations and alerts from the DWD Climate Data Center."""

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Set

from confluent_kafka import Producer
from dwd_producer_data.de.dwd.cdc.stationmetadata import StationMetadata
from dwd_producer_data.de.dwd.cdc.airtemperature10min import AirTemperature10Min
from dwd_producer_data.de.dwd.cdc.precipitation10min import Precipitation10Min
from dwd_producer_data.de.dwd.cdc.wind10min import Wind10Min
from dwd_producer_data.de.dwd.cdc.solar10min import Solar10Min
from dwd_producer_data.de.dwd.cdc.hourlyobservation import HourlyObservation
from dwd_producer_data.de.dwd.cdc.alert import Alert
from dwd_producer_kafka_producer.producer import DEDWDCDCEventProducer

from dwd.modules.base import BaseModule
from dwd.modules.station_metadata import StationMetadataModule
from dwd.modules.station_obs_10min import StationObs10MinModule
from dwd.modules.station_obs_hourly import StationObsHourlyModule
from dwd.modules.weather_alerts import WeatherAlertsModule
from dwd.util.http_client import DWDHttpClient
from dwd.util.state import load_state, save_state

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Module registry
MODULE_CLASSES = {
    "station_metadata": StationMetadataModule,
    "station_obs_10min": StationObs10MinModule,
    "station_obs_hourly": StationObsHourlyModule,
    "weather_alerts": WeatherAlertsModule,
}


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Event Hubs / Fabric Event Stream connection string."""
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=")[1].strip('"').strip().replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=")[1].strip('"').strip()
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = "$ConnectionString"
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = connection_string.strip()
            elif "BootstrapServer" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


def _resolve_modules(http_client: DWDHttpClient,
                     enabled_csv: Optional[str],
                     disabled_csv: Optional[str],
                     ten_min_params: Optional[str],
                     station_filter: Optional[Set[str]]) -> List[BaseModule]:
    """Instantiate and return enabled modules."""
    enabled = set(m.strip() for m in enabled_csv.split(",") if m.strip()) if enabled_csv else None
    disabled = set(m.strip() for m in disabled_csv.split(",") if m.strip()) if disabled_csv else set()

    modules: List[BaseModule] = []
    for key, cls in MODULE_CLASSES.items():
        if enabled is not None and key not in enabled:
            continue
        if key in disabled:
            continue
        # Check default_enabled when no explicit list is given
        if enabled is None:
            instance = _create_module(key, http_client, ten_min_params, station_filter)
            if instance.default_enabled:
                modules.append(instance)
        else:
            modules.append(_create_module(key, http_client, ten_min_params, station_filter))

    return modules


def _create_module(key: str, http_client: DWDHttpClient,
                   ten_min_params: Optional[str],
                   station_filter: Optional[Set[str]]) -> BaseModule:
    """Create a module instance with the appropriate constructor args."""
    if key == "station_obs_10min":
        categories = [p.strip() for p in ten_min_params.split(",")] if ten_min_params else None
        return StationObs10MinModule(http_client, categories=categories, station_filter=station_filter)
    elif key == "station_obs_hourly":
        return StationObsHourlyModule(http_client, station_filter=station_filter)
    elif key == "station_metadata":
        return StationMetadataModule(http_client)
    elif key == "weather_alerts":
        return WeatherAlertsModule(http_client)
    else:
        raise ValueError(f"Unknown module: {key}")


def _emit_event(event_producer: DEDWDCDCEventProducer, event: Dict[str, Any]) -> None:
    """Send a single event through the typed Kafka producer."""
    etype = event["type"]
    data = event["data"]

    if etype == "station_metadata":
        event_producer.send_de_dwd_cdc_station_metadata(
            data=StationMetadata(**data), flush_producer=False)
    elif etype == "air_temperature_10min":
        event_producer.send_de_dwd_cdc_air_temperature10_min(
            data=AirTemperature10Min(**data), flush_producer=False)
    elif etype == "precipitation_10min":
        event_producer.send_de_dwd_cdc_precipitation10_min(
            data=Precipitation10Min(**data), flush_producer=False)
    elif etype == "wind_10min":
        event_producer.send_de_dwd_cdc_wind10_min(
            data=Wind10Min(**data), flush_producer=False)
    elif etype == "solar_10min":
        event_producer.send_de_dwd_cdc_solar10_min(
            data=Solar10Min(**data), flush_producer=False)
    elif etype == "hourly_observation":
        event_producer.send_de_dwd_cdc_hourly_observation(
            data=HourlyObservation(**data), flush_producer=False)
    elif etype == "weather_alert":
        event_producer.send_de_dwd_weather_alert(
            data=Alert(**data), flush_producer=False)
    else:
        logger.warning("Unknown event type: %s", etype)


def run_feed(kafka_config: Dict[str, str], kafka_topic: str,
             polling_interval: Optional[int], state_file: str,
             modules: List[BaseModule]) -> None:
    """Main feed loop: schedule modules and emit events."""
    full_state = load_state(state_file)
    kafka_producer = Producer(kafka_config)
    event_producer = DEDWDCDCEventProducer(kafka_producer, kafka_topic)

    module_names = ", ".join(m.name for m in modules)
    logger.info("Starting DWD feed → topic=%s, bootstrap=%s, modules=[%s]",
                kafka_topic, kafka_config.get("bootstrap.servers"), module_names)

    # Track next-poll times per module
    next_poll: Dict[str, float] = {m.name: 0 for m in modules}

    while True:
        try:
            now = time.time()
            total_events = 0

            for module in modules:
                if now < next_poll.get(module.name, 0):
                    continue

                mod_state = full_state.setdefault(module.name, {})
                try:
                    events = module.poll(mod_state)
                except Exception as e:
                    logger.error("Module %s poll error: %s", module.name, e, exc_info=True)
                    events = []

                for ev in events:
                    _emit_event(event_producer, ev)
                    total_events += 1

                if events:
                    kafka_producer.flush()

                interval = polling_interval or module.default_poll_interval
                next_poll[module.name] = time.time() + interval

            save_state(state_file, full_state)

            if total_events:
                logger.info("Emitted %d events total", total_events)

            # Sleep until next module is due
            next_due = min(next_poll.values()) if next_poll else time.time() + 60
            sleep_time = max(1, next_due - time.time())
            logger.debug("Sleeping %.0fs until next poll", sleep_time)
            time.sleep(sleep_time)

        except KeyboardInterrupt:
            logger.info("Interrupted — exiting.")
            break
        except Exception as e:
            logger.error("Error: %s", e, exc_info=True)
            time.sleep(60)

    kafka_producer.flush()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="DWD Open Data bridge — weather observations, alerts, and station metadata to Kafka")
    subparsers = parser.add_subparsers(dest="command")

    # --- list-modules ---
    subparsers.add_parser("list-modules", help="Show available module names and defaults")

    # --- feed ---
    feed_p = subparsers.add_parser("feed", help="Feed data to Kafka")
    feed_p.add_argument("--kafka-bootstrap-servers", type=str,
                        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_p.add_argument("--kafka-topic", type=str, default=os.getenv("KAFKA_TOPIC"))
    feed_p.add_argument("--sasl-username", type=str, default=os.getenv("SASL_USERNAME"))
    feed_p.add_argument("--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"))
    feed_p.add_argument("-c", "--connection-string", type=str,
                        default=os.getenv("CONNECTION_STRING"))
    feed_p.add_argument("-i", "--polling-interval", type=int,
                        default=int(os.getenv("POLLING_INTERVAL", "0")) or None,
                        help="Global polling interval override in seconds (default: per-module)")
    feed_p.add_argument("--state-file", type=str,
                        default=os.getenv("STATE_FILE",
                                          os.path.expanduser("~/.dwd_state.json")))
    feed_p.add_argument("--modules", type=str, default=os.getenv("DWD_MODULES"),
                        help="Comma-separated module names to enable")
    feed_p.add_argument("--modules-disabled", type=str, default=os.getenv("DWD_MODULES_DISABLED"),
                        help="Comma-separated module names to disable")
    feed_p.add_argument("--10min-params", type=str,
                        default=os.getenv("DWD_10MIN_PARAMS"),
                        help="Comma-separated 10-min parameter categories")
    feed_p.add_argument("--stations", type=str, default=os.getenv("DWD_STATIONS"),
                        help="Comma-separated station IDs to include (default: all)")
    feed_p.add_argument("--base-url", type=str,
                        default=os.getenv("DWD_BASE_URL", "https://opendata.dwd.de"))

    args = parser.parse_args()

    if args.command == "list-modules":
        for key, cls in MODULE_CLASSES.items():
            http = DWDHttpClient()
            mod = _create_module(key, http, None, None)
            enabled = "ON" if mod.default_enabled else "OFF"
            print(f"  {key:25s}  {enabled:3s}  poll={mod.default_poll_interval}s")
        return

    if args.command == "feed":
        if args.connection_string:
            cfg = parse_connection_string(args.connection_string)
            bootstrap = cfg.get("bootstrap.servers")
            topic = cfg.get("kafka_topic")
            sasl_user = cfg.get("sasl.username")
            sasl_pw = cfg.get("sasl.password")
        else:
            bootstrap = args.kafka_bootstrap_servers
            topic = args.kafka_topic
            sasl_user = args.sasl_username
            sasl_pw = args.sasl_password

        if not bootstrap:
            print("Error: Kafka bootstrap servers required (--kafka-bootstrap-servers or -c).")
            sys.exit(1)
        if not topic:
            print("Error: Kafka topic required (--kafka-topic or -c).")
            sys.exit(1)

        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        kafka_config: Dict[str, str] = {"bootstrap.servers": bootstrap}
        if sasl_user and sasl_pw:
            kafka_config.update({
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_user,
                "sasl.password": sasl_pw,
            })
        elif tls_enabled:
            kafka_config["security.protocol"] = "SSL"

        station_filter = None
        if args.stations:
            station_filter = set(s.strip() for s in args.stations.split(",") if s.strip())

        http_client = DWDHttpClient(base_url=args.base_url)
        modules = _resolve_modules(http_client, args.modules, args.modules_disabled,
                                   getattr(args, "10min_params", None), station_filter)

        if not modules:
            print("Error: No modules enabled.")
            sys.exit(1)

        run_feed(kafka_config, topic, args.polling_interval, args.state_file, modules)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
