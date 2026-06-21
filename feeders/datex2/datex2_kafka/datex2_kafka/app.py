from __future__ import annotations

import argparse
import logging
import os
import time
from typing import Dict

from confluent_kafka import Producer
from datex2_core import collect_batches, load_endpoints, load_state, save_state
from datex2_producer_data import MeasurementSite, SituationRecord, TrafficMeasurement
from datex2_producer_kafka_producer.producer import OrgDatex2MeasuredEventProducer, OrgDatex2SituationEventProducer


def _build_kafka_config(args: argparse.Namespace) -> Dict[str, str]:
    if args.connection_string:
        if "BootstrapServer=" in args.connection_string:
            parts = dict(part.split("=", 1) for part in args.connection_string.split(";") if "=" in part)
            config = {"bootstrap.servers": parts.get("BootstrapServer", "")}
            if parts.get("EntityPath"):
                config["kafka_topic"] = parts["EntityPath"]
            if not args.kafka_enable_tls:
                config["security.protocol"] = "PLAINTEXT"
            return config
        config, topic = OrgDatex2MeasuredEventProducer.parse_connection_string(args.connection_string)
        if topic:
            config["kafka_topic"] = topic
        return config
    config = {"bootstrap.servers": args.kafka_bootstrap_servers or "localhost:9092"}
    if args.sasl_username and args.sasl_password:
        config.update({
            "security.protocol": "SASL_SSL" if args.kafka_enable_tls else "SASL_PLAINTEXT",
            "sasl.mechanisms": "PLAIN",
            "sasl.username": args.sasl_username,
            "sasl.password": args.sasl_password,
        })
    elif not args.kafka_enable_tls:
        config["security.protocol"] = "PLAINTEXT"
    return config


def _digest(row: Dict[str, object]) -> str:
    return "|".join(f"{key}={row.get(key)}" for key in sorted(row))


def _emit_cycle(measured: OrgDatex2MeasuredEventProducer, situation: OrgDatex2SituationEventProducer, args: argparse.Namespace, state: Dict[str, str]) -> Dict[str, str]:
    batch = collect_batches(load_endpoints(args.datex2_endpoints, mock=args.mock), mock=args.mock, max_records=args.max_records)
    pending = dict(state)
    for row in batch.measurement_sites:
        key = f"site/{row['supplier_id']}/{row['measurement_site_id']}"
        if pending.get(key) == _digest(row):
            continue
        measured.send_org_datex2_measured_measurement_site(_feed_url=row["feed_url"], _supplier_id=row["supplier_id"], _measurement_site_id=row["measurement_site_id"], data=MeasurementSite(**row), flush_producer=False)
        pending[key] = _digest(row)
    for row in batch.traffic_measurements:
        key = f"measurement/{row['supplier_id']}/{row['measurement_site_id']}/{row['measurement_time_key']}"
        if pending.get(key) == _digest(row):
            continue
        measured.send_org_datex2_measured_traffic_measurement(_feed_url=row["feed_url"], _supplier_id=row["supplier_id"], _measurement_site_id=row["measurement_site_id"], data=TrafficMeasurement(**row), flush_producer=False)
        pending[key] = _digest(row)
    for row in batch.situation_records:
        key = f"situation/{row['supplier_id']}/{row['situation_record_id']}"
        if pending.get(key) == _digest(row):
            continue
        situation.send_org_datex2_situation_situation_record(_feed_url=row["feed_url"], _supplier_id=row["supplier_id"], _situation_record_id=row["situation_record_id"], data=SituationRecord(**row), flush_producer=False)
        pending[key] = _digest(row)
    return pending


def feed(args: argparse.Namespace) -> None:
    config = _build_kafka_config(args)
    topic = config.pop("kafka_topic", None) or args.kafka_topic or "datex2"
    producer = Producer(config)
    measured = OrgDatex2MeasuredEventProducer(producer, topic)
    situation = OrgDatex2SituationEventProducer(producer, topic)
    state = load_state(args.state_file)
    logging.info("Starting DATEX II Kafka feeder topic=%s mock=%s", topic, args.mock)
    while True:
        pending = _emit_cycle(measured, situation, args, state)
        remaining = producer.flush(120)
        if remaining:
            raise RuntimeError(f"Kafka flush failed with {remaining} messages remaining")
        state = pending
        save_state(args.state_file, state)
        if args.once:
            break
        time.sleep(args.polling_interval)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generalized DATEX II feeder")
    sub = parser.add_subparsers(dest="command")
    feed_parser = sub.add_parser("feed")
    feed_parser.add_argument("--datex2-endpoints", default=os.getenv("DATEX2_ENDPOINTS", ""))
    feed_parser.add_argument("--mock", action="store_true", default=os.getenv("DATEX2_MOCK", "").lower() == "true")
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() == "true")
    feed_parser.add_argument("--state-file", default=os.getenv("DATEX2_STATE_FILE", os.getenv("STATE_FILE", "")))
    feed_parser.add_argument("--max-records", type=int, default=int(os.getenv("MAX_RECORDS_PER_FAMILY", "25")))
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "300")))
    feed_parser.add_argument("--kafka-bootstrap-servers", default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic", default=os.getenv("KAFKA_TOPIC"))
    feed_parser.add_argument("--connection-string", default=os.getenv("CONNECTION_STRING"))
    feed_parser.add_argument("--sasl-username", default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument("--kafka-enable-tls", action=argparse.BooleanOptionalAction, default=os.getenv("KAFKA_ENABLE_TLS", "true").lower() != "false")
    return parser


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    parser = _parser()
    args = parser.parse_args()
    if args.command != "feed":
        args = parser.parse_args(["feed"])
    feed(args)

