"""Digitraffic Road bridge — Finnish road TMS and weather sensor data to Kafka as CloudEvents."""

import argparse
import logging
import os
import sys
import time
from typing import Any, Dict, Optional, Set

from confluent_kafka import Producer
from digitraffic_road_producer_data import TmsSensorData, WeatherSensorData
from digitraffic_road_producer_kafka_producer.producer import FiDigitrafficRoadSensorsEventProducer

from digitraffic_road.mqtt_source import MQTTSource

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Event Hubs / Fabric Event Stream connection string."""
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=", 1)[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=", 1)[1].strip('"')
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = "$ConnectionString"
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = connection_string.strip()
            elif "BootstrapServer" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


def _emit_event(
    event_producer: FiDigitrafficRoadSensorsEventProducer,
    data_type: str,
    station_id: int,
    sensor_id: int,
    payload: Dict[str, Any],
) -> bool:
    """Send a decoded MQTT sensor message through the typed Kafka producer.

    Returns True if emitted, False if the data type is unknown.
    """
    enriched = dict(payload)
    enriched["station_id"] = station_id
    enriched["sensor_id"] = sensor_id

    try:
        if data_type == "tms":
            # TMS payloads may have optional start/end for windowed sensors
            if "start" not in enriched:
                enriched["start"] = None
            if "end" not in enriched:
                enriched["end"] = None
            data = TmsSensorData.from_serializer_dict(enriched)
            event_producer.send_fi_digitraffic_road_sensors_tms_sensor_data(
                _station_id=str(station_id),
                _sensor_id=str(sensor_id),
                data=data,
                flush_producer=False,
            )
            return True
        elif data_type == "weather":
            data = WeatherSensorData.from_serializer_dict(enriched)
            event_producer.send_fi_digitraffic_road_sensors_weather_sensor_data(
                _station_id=str(station_id),
                _sensor_id=str(sensor_id),
                data=data,
                flush_producer=False,
            )
            return True
        else:
            logger.debug("Skipping unknown data type: %s", data_type)
            return False
    except Exception as e:
        logger.warning(
            "Failed to emit %s for station %d sensor %d: %s",
            data_type, station_id, sensor_id, e,
        )
        return False


class DigitrafficRoadBridge:
    """Connects Digitraffic Road MQTT to Kafka via CloudEvents."""

    def __init__(
        self,
        mqtt_source: MQTTSource,
        kafka_producer: Producer,
        event_producer: FiDigitrafficRoadSensorsEventProducer,
        station_filter: Optional[Set[int]] = None,
        flush_interval: int = 1000,
    ):
        self._mqtt = mqtt_source
        self._kafka = kafka_producer
        self._event_producer = event_producer
        self._station_filter = station_filter
        self._flush_interval = flush_interval
        self._count = 0
        self._total = 0
        self._skipped = 0
        self._start_time = 0.0

    def run(self) -> None:
        """Start the bridge — blocks forever."""
        self._start_time = time.time()
        logger.info("Starting Digitraffic Road bridge")
        self._mqtt.stream(self._on_message)

    def _on_message(self, data_type: str, station_id: int, sensor_id: int, payload: Dict[str, Any]) -> None:
        """Handle a single MQTT message."""
        if _emit_event(self._event_producer, data_type, station_id, sensor_id, payload):
            self._count += 1
            self._total += 1
        else:
            self._skipped += 1

        if self._count >= self._flush_interval:
            self._kafka.flush()
            elapsed = time.time() - self._start_time
            rate = self._total / elapsed if elapsed > 0 else 0
            logger.info(
                "Flushed %d events (total: %d, skipped: %d, %.1f msg/sec)",
                self._count, self._total, self._skipped, rate,
            )
            self._count = 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Digitraffic Road bridge — Finnish road sensor data to Kafka",
    )
    subparsers = parser.add_subparsers(dest="command")

    # --- stream ---
    stream_p = subparsers.add_parser("stream", help="Stream sensor data to Kafka")
    stream_p.add_argument(
        "--kafka-bootstrap-servers", type=str,
        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    )
    stream_p.add_argument(
        "--kafka-topic", type=str, default=os.getenv("KAFKA_TOPIC"),
    )
    stream_p.add_argument(
        "--sasl-username", type=str, default=os.getenv("SASL_USERNAME"),
    )
    stream_p.add_argument(
        "--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"),
    )
    stream_p.add_argument(
        "-c", "--connection-string", type=str,
        default=os.getenv("CONNECTION_STRING"),
    )
    stream_p.add_argument(
        "--subscribe", type=str,
        default=os.getenv("DIGITRAFFIC_ROAD_SUBSCRIBE", "tms,weather"),
        help="Comma-separated: tms,weather (default: both)",
    )
    stream_p.add_argument(
        "--station-filter", type=str,
        default=os.getenv("DIGITRAFFIC_ROAD_STATION_FILTER"),
        help="Comma-separated station IDs to include (default: all)",
    )
    stream_p.add_argument(
        "--flush-interval", type=int,
        default=int(os.getenv("DIGITRAFFIC_ROAD_FLUSH_INTERVAL", "1000")),
        help="Flush Kafka producer every N events",
    )

    # --- probe ---
    probe_p = subparsers.add_parser("probe", help="Connect to MQTT and print messages")
    probe_p.add_argument(
        "--subscribe", type=str,
        default=os.getenv("DIGITRAFFIC_ROAD_SUBSCRIBE", "tms,weather"),
        help="Comma-separated: tms,weather (default: both)",
    )
    probe_p.add_argument(
        "--station-filter", type=str,
        default=os.getenv("DIGITRAFFIC_ROAD_STATION_FILTER"),
        help="Comma-separated station IDs to include",
    )
    probe_p.add_argument(
        "--duration", type=int, default=15,
        help="Probe duration in seconds (default: 15)",
    )

    args = parser.parse_args()

    if args.command == "probe":
        _run_probe(args)
        return

    if args.command == "stream":
        subs = [s.strip() for s in args.subscribe.split(",")]
        sub_tms = "tms" in subs
        sub_weather = "weather" in subs

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

        station_filter_set = None
        if args.station_filter:
            station_filter_set = set(
                int(s.strip()) for s in args.station_filter.split(",") if s.strip()
            )

        mqtt_source = MQTTSource(
            subscribe_tms=sub_tms,
            subscribe_weather=sub_weather,
            station_filter=station_filter_set,
        )
        kafka_producer = Producer(kafka_config)
        event_producer = FiDigitrafficRoadSensorsEventProducer(kafka_producer, topic)

        bridge = DigitrafficRoadBridge(
            mqtt_source=mqtt_source,
            kafka_producer=kafka_producer,
            event_producer=event_producer,
            station_filter=station_filter_set,
            flush_interval=args.flush_interval,
        )

        try:
            bridge.run()
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            kafka_producer.flush()
        return

    parser.print_help()


def _run_probe(args) -> None:
    """Connect to the live Digitraffic MQTT and print messages for --duration seconds."""
    from collections import Counter
    import json as _json

    subs = [s.strip() for s in args.subscribe.split(",")]
    sub_tms = "tms" in subs
    sub_weather = "weather" in subs

    station_filter_set = None
    if args.station_filter:
        station_filter_set = set(
            int(s.strip()) for s in args.station_filter.split(",") if s.strip()
        )

    mqtt_src = MQTTSource(
        subscribe_tms=sub_tms,
        subscribe_weather=sub_weather,
        station_filter=station_filter_set,
    )

    counter: Counter = Counter()
    start = time.time()
    sample_count: Dict[str, int] = {}

    def on_message(data_type: str, station_id: int, sensor_id: int, payload: Dict[str, Any]) -> None:
        counter[data_type] += 1

        shown = sample_count.get(data_type, 0)
        if shown < 3:
            sample_count[data_type] = shown + 1
            print(
                f"[{data_type}] station={station_id} sensor={sensor_id} "
                f"{_json.dumps(payload)[:200]}"
            )

        if time.time() - start > args.duration:
            raise KeyboardInterrupt("Probe timeout")

    try:
        mqtt_src.stream(on_message)
    except KeyboardInterrupt:
        pass

    elapsed = time.time() - start
    total = sum(counter.values())
    print(f"\n--- Probe results ({elapsed:.0f}s) ---")
    for k, v in counter.most_common():
        print(f"  {k}: {v}")
    print(f"  Total: {total}")
    if elapsed > 0:
        print(f"  Rate: {total / elapsed:.1f} msg/sec")


if __name__ == "__main__":
    main()
