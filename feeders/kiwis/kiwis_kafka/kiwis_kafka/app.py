from __future__ import annotations

import argparse
import logging
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from confluent_kafka import Producer
from kiwis_core import KiWISClient, build_kafka_config, load_endpoints, load_state, save_state
from kiwis_core.core import normalize_station, normalize_timeseries, normalize_value
from kiwis_producer_data import Station, Timeseries, TimeseriesValue
from kiwis_producer_kafka_producer.producer import OrgKiwisStationKafkaEventProducer, OrgKiwisTimeseriesKafkaEventProducer

logger = logging.getLogger(__name__)

def _emit_cycle(station_producer: OrgKiwisStationKafkaEventProducer, ts_producer: OrgKiwisTimeseriesKafkaEventProducer, endpoint, client: KiWISClient, state: Dict[str, str]) -> Dict[str, str]:
    for raw in client.stations():
        data = normalize_station(endpoint, raw)
        if not data["station_id"]: continue
        station_producer.send_org_kiwis_station_kafka_station(data=Station(**data), _base_url=endpoint.base_url, _kiwis_id=endpoint.kiwis_id, _station_id=data["station_id"], flush_producer=False)
    metadata = client.timeseries()
    meta_by_id: Dict[str, Dict[str, Any]] = {}
    for raw in metadata:
        data = normalize_timeseries(endpoint, raw)
        if not data["ts_id"]: continue
        meta_by_id[data["ts_id"]] = raw
        ts_producer.send_org_kiwis_timeseries_kafka_timeseries(data=Timeseries(**data), _base_url=endpoint.base_url, _kiwis_id=endpoint.kiwis_id, _ts_id=data["ts_id"], flush_producer=False)
    for ts_id, rows in client.values(list(meta_by_id)).items():
        meta = meta_by_id.get(ts_id)
        if not meta: continue
        for row in rows:
            data = normalize_value(endpoint, meta, row)
            key = f"{endpoint.kiwis_id}/{ts_id}/{data['timestamp'].isoformat()}"
            digest = f"{data.get('value')}|{data.get('quality_code')}"
            if state.get(key) == digest: continue
            ts_producer.send_org_kiwis_timeseries_kafka_timeseries_value(data=TimeseriesValue(**data), _base_url=endpoint.base_url, _kiwis_id=endpoint.kiwis_id, _ts_id=ts_id, flush_producer=False)
            state[key] = digest
    return state

async def feed(args: argparse.Namespace) -> None:
    kafka_config = build_kafka_config(args)
    entity_topic = kafka_config.pop("kafka_topic", None)
    topic = entity_topic or args.kafka_topic or "kiwis"
    producer = Producer(kafka_config)
    station_producer = OrgKiwisStationKafkaEventProducer(producer, topic)
    ts_producer = OrgKiwisTimeseriesKafkaEventProducer(producer, topic)
    state = load_state(args.state_file)
    logger.info("Starting KiWIS Kafka feeder: topic=%s mock=%s", topic, args.mock)
    while True:
        pending = dict(state)
        for endpoint in load_endpoints(args.kiwis_endpoints, mock=args.mock, sources_file=args.kiwis_sources_file, selector=args.kiwis_sources):
            _emit_cycle(station_producer, ts_producer, endpoint, KiWISClient(endpoint, mock=args.mock), pending)
        remaining = producer.flush(120)
        if remaining:
            raise RuntimeError(f"Kafka flush failed with {remaining} message(s) remaining")
        state = pending; save_state(args.state_file, state)
        if args.once: break
        time.sleep(args.polling_interval)

def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generalized KiWIS → Kafka feeder")
    sub = parser.add_subparsers(dest="command")
    p = sub.add_parser("feed")
    p.add_argument("--kiwis-endpoints", default=os.getenv("KIWIS_ENDPOINTS", ""))
    p.add_argument("--kiwis-sources-file", default=os.getenv("KIWIS_SOURCES_FILE", ""))
    p.add_argument("--kiwis-sources", default=os.getenv("KIWIS_SOURCES", ""))
    p.add_argument("--mock", action="store_true", default=os.getenv("KIWIS_MOCK", "").lower() == "true")
    p.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() == "true")
    p.add_argument("--state-file", default=os.getenv("KIWIS_STATE_FILE", os.getenv("STATE_FILE", "")))
    p.add_argument("-i", "--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "300")))
    p.add_argument("--kafka-bootstrap-servers", default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    p.add_argument("--kafka-topic", default=os.getenv("KAFKA_TOPIC"))
    p.add_argument("--connection-string", default=os.getenv("CONNECTION_STRING"))
    p.add_argument("--sasl-username", default=os.getenv("SASL_USERNAME"))
    p.add_argument("--sasl-password", default=os.getenv("SASL_PASSWORD"))
    p.add_argument("--kafka-enable-tls", action=argparse.BooleanOptionalAction, default=os.getenv("KAFKA_ENABLE_TLS", "true").lower() != "false")
    return parser

def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    args = _parser().parse_args()
    if args.command != "feed": args = _parser().parse_args(["feed"])
    import asyncio; asyncio.run(feed(args))
