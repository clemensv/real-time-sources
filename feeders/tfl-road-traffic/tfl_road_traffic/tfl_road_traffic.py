"""TfL Road Traffic Kafka bridge."""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from pathlib import Path

_CORE_DIR = Path(__file__).resolve().parents[1] / "tfl_road_traffic_core"
if _CORE_DIR.exists() and str(_CORE_DIR) not in sys.path:
    sys.path.insert(0, str(_CORE_DIR))

from tfl_road_traffic_core.tfl_road_traffic import *  # noqa: F401,F403
from tfl_road_traffic_core.tfl_road_traffic import (
    TflRoadTrafficSource as _CoreSource,
    build_road_corridor_record,
    build_road_disruption_record,
    build_road_status_record,
)
from tfl_road_traffic_producer_data import RoadCorridor, RoadDisruption, RoadStatus

try:
    from tfl_road_traffic_producer_kafka_producer.producer import UkGovTflRoadCorridorsEventProducer
except ModuleNotFoundError:  # pragma: no cover
    UkGovTflRoadCorridorsEventProducer = None

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def parse_connection_string(connection_string: str) -> dict[str, str]:
    config_dict: dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
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


def build_road_corridor(raw: dict) -> RoadCorridor | None:
    record = build_road_corridor_record(raw)
    return RoadCorridor(**record) if record else None


def build_road_status(raw: dict) -> RoadStatus | None:
    record = build_road_status_record(raw)
    return RoadStatus(**record) if record else None


def build_road_disruption(raw: dict) -> RoadDisruption | None:
    record = build_road_disruption_record(raw)
    return RoadDisruption(**record) if record else None


class UkGovTflRoadDisruptionsEventProducer:
    def __init__(self, producer, topic: str):
        self.producer = producer
        self.topic = topic

    def send_uk_gov_tfl_road_road_disruption(self, _road_id: str, _severity: str, _disruption_id: str, data: RoadDisruption, flush_producer: bool = True) -> None:
        self.producer.produce(self.topic, key=f"disruptions/{_road_id}/{_severity}/{_disruption_id}", value=data.to_byte_array("application/json"))
        if flush_producer:
            self.producer.flush()


class TflRoadTrafficPoller(_CoreSource):
    def __init__(self, kafka_config: dict[str, str], kafka_topic: str, polling_interval: int = 60, reference_refresh_interval: int = 3600, session=None):
        super().__init__(polling_interval=polling_interval, reference_refresh_interval=reference_refresh_interval, session=session)
        from confluent_kafka import Producer as KafkaProducer

        self.kafka_topic = kafka_topic
        self._kafka_producer = KafkaProducer(kafka_config)
        self.corridors_producer = UkGovTflRoadCorridorsEventProducer(self._kafka_producer, kafka_topic)
        self.disruptions_producer = UkGovTflRoadDisruptionsEventProducer(self._kafka_producer, kafka_topic)

    def emit_reference_data(self, raw_corridors: list[dict]) -> int:
        events_sent = 0
        for raw in raw_corridors:
            corridor = build_road_corridor(raw)
            if corridor is None:
                continue
            self.corridors_producer.send_uk_gov_tfl_road_road_corridor(corridor.road_id, corridor, flush_producer=False)
            events_sent += 1
        if events_sent > 0 and self._kafka_producer.flush(timeout=30) != 0:
            logger.error("Flush failed for reference data")
            return 0
        return events_sent

    def emit_status_data(self, raw_statuses: list[dict]) -> int:
        events_sent = 0
        for raw in raw_statuses:
            status = build_road_status(raw)
            if status is None:
                continue
            self.corridors_producer.send_uk_gov_tfl_road_road_status(status.road_id, status, flush_producer=False)
            events_sent += 1
        if events_sent > 0 and self._kafka_producer.flush(timeout=30) != 0:
            logger.error("Flush failed for status data")
            return 0
        return events_sent

    def emit_disruption_data(self, raw_disruptions: list[dict]) -> int:
        to_emit, candidate_state = self.pending_disruptions(raw_disruptions)
        for record in to_emit:
            disruption = RoadDisruption(**record)
            self.disruptions_producer.send_uk_gov_tfl_road_road_disruption(
                disruption.road_id,
                disruption.severity,
                disruption.disruption_id,
                disruption,
                flush_producer=False,
            )
        if to_emit and self._kafka_producer.flush(timeout=30) != 0:
            logger.error("Flush failed for disruption data")
            return 0
        self.commit_disruption_state(candidate_state)
        return len(to_emit)

    def poll_and_send(self) -> None:
        logger.info("TfL Road Traffic poller starting (interval=%ds)", self.polling_interval)
        while True:
            if self.reference_due():
                raw_corridors = self.fetch_corridors()
                if raw_corridors is not None:
                    self.remember_reference_fetch(raw_corridors)
                    self.emit_reference_data(raw_corridors)
                elif self._cached_corridors is not None:
                    logger.warning("Reference refresh failed; keeping %d cached corridors", len(self._cached_corridors))
                else:
                    logger.warning("Reference fetch failed and no cache available")
            raw_statuses = self.fetch_statuses()
            if raw_statuses is not None:
                self.emit_status_data(raw_statuses)
            raw_disruptions = self.fetch_disruptions()
            if raw_disruptions is not None:
                self.emit_disruption_data(raw_disruptions)
            time.sleep(self.polling_interval)


def main() -> None:
    parser = argparse.ArgumentParser(description="Transport for London (TfL) Road Traffic bridge to Kafka")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Run the polling bridge")
    feed_parser.add_argument("--connection-string", type=str)
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str)
    feed_parser.add_argument("--kafka-topic", type=str, default="tfl-road-traffic")
    feed_parser.add_argument("--sasl-username", type=str)
    feed_parser.add_argument("--sasl-password", type=str)
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)

    connection_string = args.connection_string or os.getenv("CONNECTION_STRING")
    enable_tls = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    polling_interval = int(os.getenv("POLLING_INTERVAL", "60"))
    reference_refresh_interval = int(os.getenv("REFERENCE_REFRESH_INTERVAL", "3600"))
    kafka_topic = args.kafka_topic
    kafka_bootstrap_servers = args.kafka_bootstrap_servers
    sasl_username = args.sasl_username
    sasl_password = args.sasl_password
    if connection_string:
        config_params = parse_connection_string(connection_string)
        kafka_bootstrap_servers = config_params.get("bootstrap.servers", kafka_bootstrap_servers)
        kafka_topic = config_params.get("kafka_topic", kafka_topic)
        sasl_username = config_params.get("sasl.username", sasl_username)
        sasl_password = config_params.get("sasl.password", sasl_password)
    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided.", file=sys.stderr)
        sys.exit(1)

    kafka_config: dict[str, str] = {"bootstrap.servers": kafka_bootstrap_servers}
    if sasl_username and sasl_password:
        kafka_config.update(
            {
                "sasl.mechanisms": "PLAIN",
                "sasl.username": sasl_username,
                "sasl.password": sasl_password,
                "security.protocol": "SASL_SSL",
            }
        )
    elif enable_tls:
        kafka_config["security.protocol"] = "SSL"

    TflRoadTrafficPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        polling_interval=polling_interval,
        reference_refresh_interval=reference_refresh_interval,
    ).poll_and_send()
