"""Bridge for French national non-conceded road network real-time traffic data."""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

from confluent_kafka import Producer

_CORE_DIR = Path(__file__).resolve().parents[1] / "french_road_traffic_core"
if _CORE_DIR.exists() and str(_CORE_DIR) not in sys.path:
    sys.path.insert(0, str(_CORE_DIR))

from french_road_traffic_core.french_road_traffic import *  # noqa: F401,F403
from french_road_traffic_core.french_road_traffic import FrenchRoadTrafficSource
from french_road_traffic_producer_data.fr.gouv.transport.bison_fute.roadevent import RoadEvent
from french_road_traffic_producer_data.fr.gouv.transport.bison_fute.trafficflowmeasurement import TrafficFlowMeasurement
from french_road_traffic_producer_kafka_producer.producer import (
    FrGouvTransportBisonFuteRoadEventEventProducer,
    FrGouvTransportBisonFuteTrafficFlowEventProducer,
)

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
                config_dict["bootstrap.servers"] = part.split("=")[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=")[1].strip('"').strip()
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


def _flow_data(record: dict[str, Any]) -> TrafficFlowMeasurement:
    return TrafficFlowMeasurement(
        site_id=record["site_id"],
        measurement_time=record["measurement_time"],
        vehicle_flow_rate=record.get("vehicle_flow_rate"),
        average_speed=record.get("average_speed"),
        input_values_flow=record.get("input_values_flow"),
        input_values_speed=record.get("input_values_speed"),
    )


def _event_data(record: dict[str, Any]) -> RoadEvent:
    return RoadEvent(
        situation_id=record["situation_id"],
        record_id=record["record_id"],
        version=record.get("version"),
        severity=record.get("severity"),
        record_type=record.get("record_type"),
        probability=record.get("probability"),
        latitude=record.get("latitude"),
        longitude=record.get("longitude"),
        road_number=record.get("road_number"),
        town_name=record.get("town_name"),
        direction=record.get("direction"),
        description=record.get("description"),
        location_description=record.get("location_description"),
        source_name=record.get("source_name"),
        validity_status=record.get("validity_status"),
        overall_start_time=record.get("overall_start_time"),
        overall_end_time=record.get("overall_end_time"),
        creation_time=record["creation_time"],
        observation_time=record.get("observation_time"),
    )


def fetch_xml(session, url: str, timeout: int = DEFAULT_REQUEST_TIMEOUT_SECONDS) -> bytes:
    return FrenchRoadTrafficSource(session=session, timeout=timeout).fetch_xml(url, timeout=timeout)


def run_bridge(
    kafka_config: dict[str, str],
    topic_flow: str,
    topic_events: str,
    polling_interval: int,
    flow_url: str = TRAFFIC_FLOW_URL,
    events_url: str = ROAD_EVENTS_URL,
    once: bool = False,
) -> None:
    producer = Producer(kafka_config)
    flow_producer = FrGouvTransportBisonFuteTrafficFlowEventProducer(producer, topic_flow)
    event_producer = FrGouvTransportBisonFuteRoadEventEventProducer(producer, topic_events)
    session = build_retrying_session()
    logger.info("Starting French Road Traffic bridge — flow topic=%s, events topic=%s, interval=%ds", topic_flow, topic_events, polling_interval)
    while True:
        try:
            started = time.time()
            flow_count = 0
            event_count = 0
            try:
                for record in parse_traffic_flow_xml(fetch_xml(session, flow_url)):
                    flow_producer.send_fr_gouv_transport_bison_fute_traffic_flow_measurement(
                        _feedurl=FEED_SOURCE_FLOW,
                        _site_id=record["site_id"],
                        data=_flow_data(record),
                        flush_producer=False,
                    )
                    flow_count += 1
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error fetching/parsing traffic flow: %s", exc)
            try:
                for record in parse_road_events_xml(fetch_xml(session, events_url)):
                    event_producer.send_fr_gouv_transport_bison_fute_road_event(
                        _feedurl=FEED_SOURCE_EVENTS,
                        _situation_id=record["situation_id"],
                        data=_event_data(record),
                        flush_producer=False,
                    )
                    event_count += 1
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error fetching/parsing road events: %s", exc)
            producer.flush()
            elapsed = time.time() - started
            logger.info("Emitted %d flow measurements + %d road events in %.1fs", flow_count, event_count, elapsed)
            if once:
                logger.info("--once mode: exiting after first polling cycle")
                break
            remaining = max(0.0, polling_interval - elapsed)
            if remaining > 0:
                time.sleep(remaining)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            break
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Unexpected error: %s", exc)
            logger.info("Retrying in %ds...", polling_interval)
            time.sleep(polling_interval)
    producer.flush()


def main() -> None:
    parser = argparse.ArgumentParser(description="French Road Traffic bridge — real-time DATEX II data to Kafka")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Start the polling bridge")
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str, default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic-flow", type=str, default=os.getenv("KAFKA_TOPIC_FLOW", "french-road-traffic-flow"))
    feed_parser.add_argument("--kafka-topic-events", type=str, default=os.getenv("KAFKA_TOPIC_EVENTS", "french-road-traffic-events"))
    feed_parser.add_argument("--sasl-username", type=str, default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument("-c", "--connection-string", type=str, default=os.getenv("CONNECTION_STRING"))
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", str(DEFAULT_POLL_INTERVAL_SECONDS))))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "false").lower() in ("true", "1", "yes"))
    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        sys.exit(1)

    topic_flow = args.kafka_topic_flow
    topic_events = args.kafka_topic_events
    bootstrap_servers = args.kafka_bootstrap_servers
    sasl_username = args.sasl_username
    sasl_password = args.sasl_password
    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        bootstrap_servers = config_params.get("bootstrap.servers", bootstrap_servers)
        sasl_username = config_params.get("sasl.username", sasl_username)
        sasl_password = config_params.get("sasl.password", sasl_password)
        topic_from_cs = config_params.get("kafka_topic")
        if topic_from_cs:
            topic_flow = topic_flow or topic_from_cs
            topic_events = topic_events or topic_from_cs
    if not bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided via --kafka-bootstrap-servers or CONNECTION_STRING.", file=sys.stderr)
        sys.exit(1)

    kafka_config: dict[str, str] = {"bootstrap.servers": bootstrap_servers}
    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    if sasl_username and sasl_password:
        kafka_config.update(
            {
                "sasl.mechanisms": "PLAIN",
                "sasl.username": sasl_username,
                "sasl.password": sasl_password,
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
            }
        )
    elif tls_enabled:
        kafka_config["security.protocol"] = "SSL"

    run_bridge(
        kafka_config=kafka_config,
        topic_flow=topic_flow,
        topic_events=topic_events,
        polling_interval=args.polling_interval,
        once=args.once,
    )
