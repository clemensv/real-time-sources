"""DWD Open Data bridge — aggregates weather observations and alerts from the DWD Climate Data Center."""

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Set

from confluent_kafka import Producer
from dwd_producer_data import StationMetadata
from dwd_producer_data import AirTemperature10Min
from dwd_producer_data import Precipitation10Min
from dwd_producer_data import Wind10Min
from dwd_producer_data import Solar10Min
from dwd_producer_data import HourlyObservation
from dwd_producer_data import ExtremeWind10Min
from dwd_producer_data import ExtremeTemperature10Min
from dwd_producer_data import Alert
from dwd_producer_data import RadarProductCatalog
from dwd_producer_data import RadarFileProduct
from dwd_producer_data import ForecastModelCatalog
from dwd_producer_data import IconD2ForecastFile
from dwd_producer_kafka_producer.producer import (
    DEDWDCDCEventProducer,
    DEDWDWeatherEventProducer,
    DEDWDRadarEventProducer,
    DEDWDForecastEventProducer,
)

from dwd.modules.base import BaseModule
from dwd.modules.station_metadata import StationMetadataModule
from dwd.modules.station_obs_10min import StationObs10MinModule
from dwd.modules.station_obs_10min_extremes import StationObs10MinExtremesModule
from dwd.modules.station_obs_hourly import StationObsHourlyModule
from dwd.modules.weather_alerts import WeatherAlertsModule
from dwd.modules.radar_products import RadarProductsModule
from dwd.modules.icon_d2_forecast import IconD2ForecastModule
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
    "station_obs_10min_extremes": StationObs10MinExtremesModule,
    "station_obs_hourly": StationObsHourlyModule,
    "weather_alerts": WeatherAlertsModule,
    "radar_products": RadarProductsModule,
    "icon_d2_forecast": IconD2ForecastModule,
}


def _optional_int_env(var_name: str) -> Optional[int]:
    """Parse an optional int env var; treat unset/empty as None."""
    raw = os.getenv(var_name)
    if raw is None or raw.strip() == "":
        return None
    value = int(raw)
    return value or None


def _truthy_env(var_name: str) -> bool:
    """Parse bool-ish env vars using common truthy values."""
    return os.getenv(var_name, "").strip().lower() in ("1", "true", "yes")


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
    elif key == "station_obs_10min_extremes":
        return StationObs10MinExtremesModule(http_client, station_filter=station_filter)
    elif key == "station_obs_hourly":
        return StationObsHourlyModule(http_client, station_filter=station_filter)
    elif key == "station_metadata":
        return StationMetadataModule(http_client)
    elif key == "weather_alerts":
        return WeatherAlertsModule(http_client)
    elif key == "radar_products":
        return RadarProductsModule(http_client)
    elif key == "icon_d2_forecast":
        return IconD2ForecastModule(http_client)
    else:
        raise ValueError(f"Unknown module: {key}")


def _emit_event(cdc_event_producer: DEDWDCDCEventProducer,
                 weather_event_producer: DEDWDWeatherEventProducer,
                 radar_event_producer: DEDWDRadarEventProducer,
                 forecast_event_producer: DEDWDForecastEventProducer,
                 event: Dict[str, Any]) -> None:
    """Send a single event through the typed Kafka producer."""
    etype = event["type"]
    data = dict(event["data"])

    if etype in {
        "air_temperature_10min",
        "precipitation_10min",
        "wind_10min",
        "solar_10min",
        "hourly_observation",
        "extreme_wind_10min",
        "extreme_temperature_10min",
        "weather_alert",
    }:
        data.setdefault("state", None)
    elif etype in {"radar_product_catalog", "forecast_model_catalog"}:
        data.setdefault("state", None)
        data.setdefault("kind", None)
    elif etype == "radar_file_product":
        data.setdefault("file_id", None)
        data.setdefault("state", None)
        data.setdefault("product_type", None)
    elif etype == "icon_d2_forecast_file":
        data.setdefault("state", None)
        data.setdefault("variable", None)
        data.setdefault("file_id", None)

    if etype == "station_metadata":
        cdc_event_producer.send_de_dwd_cdc_station_metadata(
            _station_id=data["station_id"], data=StationMetadata(**data), flush_producer=False)
    elif etype == "air_temperature_10min":
        cdc_event_producer.send_de_dwd_cdc_air_temperature10_min(
            _station_id=data["station_id"], data=AirTemperature10Min(**data), flush_producer=False)
    elif etype == "precipitation_10min":
        cdc_event_producer.send_de_dwd_cdc_precipitation10_min(
            _station_id=data["station_id"], data=Precipitation10Min(**data), flush_producer=False)
    elif etype == "wind_10min":
        cdc_event_producer.send_de_dwd_cdc_wind10_min(
            _station_id=data["station_id"], data=Wind10Min(**data), flush_producer=False)
    elif etype == "solar_10min":
        cdc_event_producer.send_de_dwd_cdc_solar10_min(
            _station_id=data["station_id"], data=Solar10Min(**data), flush_producer=False)
    elif etype == "hourly_observation":
        cdc_event_producer.send_de_dwd_cdc_hourly_observation(
            _station_id=data["station_id"], data=HourlyObservation(**data), flush_producer=False)
    elif etype == "extreme_wind_10min":
        cdc_event_producer.send_de_dwd_cdc_extreme_wind10_min(
            _station_id=data["station_id"], data=ExtremeWind10Min(**data), flush_producer=False)
    elif etype == "extreme_temperature_10min":
        cdc_event_producer.send_de_dwd_cdc_extreme_temperature10_min(
            _station_id=data["station_id"], data=ExtremeTemperature10Min(**data), flush_producer=False)
    elif etype == "weather_alert":
        weather_event_producer.send_de_dwd_weather_alert(
            _identifier=data["identifier"], data=Alert(**data), flush_producer=False)
    elif etype == "radar_product_catalog":
        radar_event_producer.send_de_dwd_radar_radar_product_catalog(
            _file_url=data["file_url"], data=RadarProductCatalog(**data), flush_producer=False)
    elif etype == "radar_file_product":
        radar_event_producer.send_de_dwd_radar_radar_file_product(
            _file_url=data["file_url"], data=RadarFileProduct(**data), flush_producer=False)
    elif etype == "forecast_model_catalog":
        forecast_event_producer.send_de_dwd_forecast_forecast_model_catalog(
            _file_url=data["file_url"], data=ForecastModelCatalog(**data), flush_producer=False)
    elif etype == "icon_d2_forecast_file":
        forecast_event_producer.send_de_dwd_forecast_icon_d2_forecast_file(
            _file_url=data["file_url"], data=IconD2ForecastFile(**data), flush_producer=False)
    else:
        logger.warning("Unknown event type: %s", etype)


def run_feed(kafka_config: Dict[str, str], kafka_topic: str,
             polling_interval: Optional[int], state_file: str,
             modules: List[BaseModule],
             once: bool = False) -> None:
    """Main feed loop: schedule modules and emit events."""
    full_state = load_state(state_file)
    kafka_producer = Producer(kafka_config)
    cdc_event_producer = DEDWDCDCEventProducer(kafka_producer, kafka_topic)
    weather_event_producer = DEDWDWeatherEventProducer(kafka_producer, kafka_topic)
    radar_event_producer = DEDWDRadarEventProducer(kafka_producer, kafka_topic)
    forecast_event_producer = DEDWDForecastEventProducer(kafka_producer, kafka_topic)

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
                    while True:
                        try:
                            _emit_event(
                                cdc_event_producer,
                                weather_event_producer,
                                radar_event_producer,
                                forecast_event_producer,
                                ev,
                            )
                            break
                        except BufferError:
                            kafka_producer.flush(5)
                    total_events += 1
                    if total_events % 500 == 0:
                        kafka_producer.poll(0)

                if events:
                    kafka_producer.flush()

                interval = polling_interval or module.default_poll_interval
                next_poll[module.name] = time.time() + interval

            save_state(state_file, full_state)

            if total_events:
                logger.info("Emitted %d events total", total_events)

            if once:
                logger.info("ONCE_MODE enabled — exiting after one polling cycle.")
                break

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
                        default=_optional_int_env("POLLING_INTERVAL"),
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
    feed_p.add_argument("--once", action="store_true",
                        default=_truthy_env("ONCE_MODE"),
                        help="Run one poll cycle and exit (for scheduled notebook execution)")

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

        run_feed(kafka_config, topic, args.polling_interval, args.state_file, modules, once=args.once)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
