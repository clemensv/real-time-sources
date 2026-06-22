"""DWD Open Data bridge — aggregates weather observations and alerts from the DWD Climate Data Center."""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from typing import Any, Dict, List, Optional, Set

from confluent_kafka import Producer
from dwd_producer_kafka_producer.producer import (
    DEDWDCDCEventProducer,
    DEDWDWeatherEventProducer,
    DEDWDRadarEventProducer,
    DEDWDForecastEventProducer,
)
from dwd_core import (
    Alert, AirTemperature10Min, DWDHttpClient, ExtremeTemperature10Min,
    ExtremeWind10Min, ForecastModelCatalog, HourlyObservation,
    IconD2ForecastFile, MODULE_CLASSES, Precipitation10Min,
    RadarFileProduct, RadarProductCatalog, Solar10Min, StationMetadata,
    Wind10Min, _create_module, _optional_int_env, _resolve_modules,
    _truthy_env, load_state, parse_connection_string, save_state,
)
from dwd.modules.base import BaseModule

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def _emit_event(cdc_event_producer: DEDWDCDCEventProducer,
                weather_event_producer: DEDWDWeatherEventProducer,
                radar_event_producer: DEDWDRadarEventProducer,
                forecast_event_producer: DEDWDForecastEventProducer,
                event: Dict[str, Any]) -> None:
    etype = event["type"]
    data = dict(event["data"])
    if etype in {"air_temperature_10min", "precipitation_10min", "wind_10min", "solar_10min", "hourly_observation", "extreme_wind_10min", "extreme_temperature_10min", "weather_alert"}:
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
        cdc_event_producer.send_de_dwd_cdc_station_metadata(_station_id=data["station_id"], data=StationMetadata(**data), flush_producer=False)
    elif etype == "air_temperature_10min":
        cdc_event_producer.send_de_dwd_cdc_air_temperature10_min(_station_id=data["station_id"], data=AirTemperature10Min(**data), flush_producer=False)
    elif etype == "precipitation_10min":
        cdc_event_producer.send_de_dwd_cdc_precipitation10_min(_station_id=data["station_id"], data=Precipitation10Min(**data), flush_producer=False)
    elif etype == "wind_10min":
        cdc_event_producer.send_de_dwd_cdc_wind10_min(_station_id=data["station_id"], data=Wind10Min(**data), flush_producer=False)
    elif etype == "solar_10min":
        cdc_event_producer.send_de_dwd_cdc_solar10_min(_station_id=data["station_id"], data=Solar10Min(**data), flush_producer=False)
    elif etype == "hourly_observation":
        cdc_event_producer.send_de_dwd_cdc_hourly_observation(_station_id=data["station_id"], data=HourlyObservation(**data), flush_producer=False)
    elif etype == "extreme_wind_10min":
        cdc_event_producer.send_de_dwd_cdc_extreme_wind10_min(_station_id=data["station_id"], data=ExtremeWind10Min(**data), flush_producer=False)
    elif etype == "extreme_temperature_10min":
        cdc_event_producer.send_de_dwd_cdc_extreme_temperature10_min(_station_id=data["station_id"], data=ExtremeTemperature10Min(**data), flush_producer=False)
    elif etype == "weather_alert":
        weather_event_producer.send_de_dwd_weather_alert(_identifier=data["identifier"], data=Alert(**data), flush_producer=False)
    elif etype == "radar_product_catalog":
        radar_event_producer.send_de_dwd_radar_radar_product_catalog(_file_url=data["file_url"], data=RadarProductCatalog(**data), flush_producer=False)
    elif etype == "radar_file_product":
        radar_event_producer.send_de_dwd_radar_radar_file_product(_file_url=data["file_url"], data=RadarFileProduct(**data), flush_producer=False)
    elif etype == "forecast_model_catalog":
        forecast_event_producer.send_de_dwd_forecast_forecast_model_catalog(_file_url=data["file_url"], data=ForecastModelCatalog(**data), flush_producer=False)
    elif etype == "icon_d2_forecast_file":
        forecast_event_producer.send_de_dwd_forecast_icon_d2_forecast_file(_file_url=data["file_url"], data=IconD2ForecastFile(**data), flush_producer=False)
    else:
        logger.warning("Unknown event type: %s", etype)


def run_feed(kafka_config: Dict[str, str], kafka_topic: str,
             polling_interval: Optional[int], state_file: str,
             modules: List[BaseModule],
             once: bool = False) -> None:
    full_state = load_state(state_file)
    kafka_producer = Producer(kafka_config)
    cdc_event_producer = DEDWDCDCEventProducer(kafka_producer, kafka_topic)
    weather_event_producer = DEDWDWeatherEventProducer(kafka_producer, kafka_topic)
    radar_event_producer = DEDWDRadarEventProducer(kafka_producer, kafka_topic)
    forecast_event_producer = DEDWDForecastEventProducer(kafka_producer, kafka_topic)
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
                            _emit_event(cdc_event_producer, weather_event_producer, radar_event_producer, forecast_event_producer, ev)
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
            if once:
                logger.info("ONCE_MODE enabled — exiting after one polling cycle.")
                break
            next_due = min(next_poll.values()) if next_poll else time.time() + 60
            time.sleep(max(1, next_due - time.time()))
        except KeyboardInterrupt:
            logger.info("Interrupted — exiting.")
            break
        except Exception as e:
            logger.error("Error: %s", e, exc_info=True)
            time.sleep(60)
    kafka_producer.flush()


def main() -> None:
    parser = argparse.ArgumentParser(description="DWD Open Data bridge — weather observations, alerts, and station metadata to Kafka")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list-modules", help="Show available module names and defaults")
    feed_p = subparsers.add_parser("feed", help="Feed data to Kafka")
    feed_p.add_argument("--kafka-bootstrap-servers", type=str, default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_p.add_argument("--kafka-topic", type=str, default=os.getenv("KAFKA_TOPIC"))
    feed_p.add_argument("--sasl-username", type=str, default=os.getenv("SASL_USERNAME"))
    feed_p.add_argument("--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"))
    feed_p.add_argument("-c", "--connection-string", type=str, default=os.getenv("CONNECTION_STRING"))
    feed_p.add_argument("-i", "--polling-interval", type=int, default=_optional_int_env("POLLING_INTERVAL"))
    feed_p.add_argument("--state-file", type=str, default=os.getenv("STATE_FILE", os.path.expanduser("~/.dwd_state.json")))
    feed_p.add_argument("--modules", type=str, default=os.getenv("DWD_MODULES"))
    feed_p.add_argument("--modules-disabled", type=str, default=os.getenv("DWD_MODULES_DISABLED"))
    feed_p.add_argument("--10min-params", type=str, default=os.getenv("DWD_10MIN_PARAMS"))
    feed_p.add_argument("--stations", type=str, default=os.getenv("DWD_STATIONS"))
    feed_p.add_argument("--base-url", type=str, default=os.getenv("DWD_BASE_URL", "https://opendata.dwd.de"))
    feed_p.add_argument("--once", action="store_true", default=_truthy_env("ONCE_MODE"))
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
            kafka_config.update({"sasl.mechanisms": "PLAIN", "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT", "sasl.username": sasl_user, "sasl.password": sasl_pw})
        elif tls_enabled:
            kafka_config["security.protocol"] = "SSL"
        station_filter = set(s.strip() for s in args.stations.split(",") if s.strip()) if args.stations else None
        http_client = DWDHttpClient(base_url=args.base_url)
        modules = _resolve_modules(http_client, args.modules, args.modules_disabled, getattr(args, "10min_params", None), station_filter)
        if not modules:
            print("Error: No modules enabled.")
            sys.exit(1)
        run_feed(kafka_config, topic, args.polling_interval, args.state_file, modules, once=args.once)
        return
    parser.print_help()


if __name__ == "__main__":
    main()
