"""Bridge for JMA Bosai volcanic warnings and eruptions."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

from confluent_kafka import Producer

_CORE_DIR = Path(__file__).resolve().parents[1] / "jma_bosai_volcano_core"
if _CORE_DIR.exists() and str(_CORE_DIR) not in sys.path:
    sys.path.insert(0, str(_CORE_DIR))

from jma_bosai_volcano_core.jma_bosai_volcano import *  # noqa: F401,F403
from jma_bosai_volcano_core.jma_bosai_volcano import (
    JMABosaiVolcanoSource as _CoreSource,
    MockSource as _CoreMockSource,
    PendingTelemetry,
    map_condition_name,
    map_eruption_type_name,
    parse_eruption_record as _parse_eruption_record_raw,
    parse_volcano_catalog as _parse_volcano_catalog_raw,
    parse_warning_record as _parse_warning_record_raw,
)
from jma_bosai_volcano_producer_data import Volcano, VolcanicEruption, VolcanicWarning
from jma_bosai_volcano_producer_data.conditionenum import ConditionEnum
from jma_bosai_volcano_producer_data.eruptiontypeenum import EruptionTypeenum
from jma_bosai_volcano_producer_kafka_producer.producer import JPJMAVolcanoEventProducer

DEFAULT_TOPIC = "jma-bosai-volcano"

logging.basicConfig(level=logging.INFO)


def map_condition(value: str | None) -> ConditionEnum:
    return ConditionEnum[map_condition_name(value)]


def map_eruption_type(value: str | None) -> EruptionTypeenum | None:
    token = map_eruption_type_name(value)
    return EruptionTypeenum[token] if token else None


def parse_connection_string(connection_string: str) -> dict[str, str]:
    config: dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if part.startswith("Endpoint="):
                config["bootstrap.servers"] = part.split("=", 1)[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
                config["sasl.username"] = "$ConnectionString"
                config["sasl.password"] = connection_string.strip()
            elif part.startswith("EntityPath="):
                config["kafka_topic"] = part.split("=", 1)[1].strip('"')
            elif part.startswith("BootstrapServer="):
                config["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc
    if "sasl.username" in config:
        config["security.protocol"] = "SASL_SSL"
        config["sasl.mechanisms"] = "PLAIN"
    return config


def build_kafka_config(args: argparse.Namespace) -> tuple[dict[str, str], str]:
    if args.connection_string:
        parsed = parse_connection_string(args.connection_string)
        bootstrap = parsed.get("bootstrap.servers")
        topic = parsed.get("kafka_topic") or args.kafka_topic or DEFAULT_TOPIC
        sasl_username = parsed.get("sasl.username")
        sasl_password = parsed.get("sasl.password")
    else:
        bootstrap = args.kafka_bootstrap_servers
        topic = args.kafka_topic or DEFAULT_TOPIC
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password
    if not bootstrap:
        raise ValueError("Kafka bootstrap servers must be provided by KAFKA_BOOTSTRAP_SERVERS or CONNECTION_STRING")
    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    config = {"bootstrap.servers": bootstrap}
    if sasl_username and sasl_password:
        config.update(
            {
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_username,
                "sasl.password": sasl_password,
            }
        )
    elif tls_enabled:
        config["security.protocol"] = "SSL"
    return config, topic


def _volcano(raw: dict[str, Any]) -> Volcano:
    return Volcano(**raw)


def _warning(raw: dict[str, Any]) -> VolcanicWarning:
    payload = dict(raw)
    payload["condition"] = ConditionEnum[payload["condition"]]
    return VolcanicWarning(**payload)


def _eruption(raw: dict[str, Any]) -> VolcanicEruption:
    payload = dict(raw)
    if payload.get("eruption_type") is not None:
        payload["eruption_type"] = EruptionTypeenum[payload["eruption_type"]]
    return VolcanicEruption(**payload)


def parse_volcano_catalog(payload: Any) -> dict[str, Volcano]:
    return {code: _volcano(record) for code, record in _parse_volcano_catalog_raw(payload).items()}


def parse_warning_record(record: dict[str, Any]) -> list[VolcanicWarning]:
    return [_warning(item) for item in _parse_warning_record_raw(record)]


def parse_eruption_record(record: dict[str, Any]) -> list[VolcanicEruption]:
    return [_eruption(item) for item in _parse_eruption_record_raw(record)]


class JMABosaiVolcanoAPI(_CoreSource):
    def fetch_volcano_catalog(self) -> dict[str, Volcano]:
        return {code: _volcano(record) for code, record in self.fetch_volcano_catalog_data().items()}

    def emit_reference_data(self, producer: JPJMAVolcanoEventProducer, state: dict[str, Any], state_file: str) -> None:
        raw_records = self.build_reference_records()
        for record in raw_records:
            volcano = _volcano(record)
            producer.send_jp_jma_volcano_volcano(
                _feedurl=VOLCANO_LIST_URL,
                _volcano_code=volcano.volcano_code,
                data=volcano,
                flush_producer=False,
            )
        remainder = producer.producer.flush(timeout=30)
        if remainder:
            raise RuntimeError(f"Kafka flush left {remainder} reference events queued")
        self.commit_reference_refresh(state, state_file)

    def maybe_refresh_reference_data(self, producer: JPJMAVolcanoEventProducer, state: dict[str, Any], state_file: str, refresh_hours: int) -> None:
        if self.should_refresh_reference(state, refresh_hours):
            try:
                self.emit_reference_data(producer, state, state_file)
            except Exception as exc:  # pylint: disable=broad-except
                if self.volcano_catalog:
                    logging.warning("Keeping cached volcano catalog after refresh failure: %s", exc)
                else:
                    raise

    def poll_once(self, producer: JPJMAVolcanoEventProducer, state: dict[str, Any], state_file: str) -> tuple[int, int]:
        warning_payloads: list[dict[str, Any]] = []
        eruption_payloads: list[dict[str, Any]] = []
        try:
            warning_payloads = self.fetch_warnings()
        except Exception as exc:  # pylint: disable=broad-except
            logging.warning("Skipping warning endpoint for this cycle: %s", exc)
        try:
            eruption_payloads = self.fetch_eruptions()
        except Exception as exc:  # pylint: disable=broad-except
            logging.warning("Skipping eruption endpoint for this cycle: %s", exc)
        pending: PendingTelemetry = self.collect_pending_telemetry(state, warning_payloads, eruption_payloads)
        for warning in pending.warnings:
            event = _warning(warning)
            producer.send_jp_jma_volcano_volcanic_warning(
                _feedurl=WARNING_URL,
                _volcano_code=event.volcano_code,
                data=event,
                flush_producer=False,
            )
        for eruption in pending.eruptions:
            event = _eruption(eruption)
            producer.send_jp_jma_volcano_volcanic_eruption(
                _feedurl=ERUPTION_URL,
                _volcano_code=event.volcano_code,
                data=event,  # type: ignore[arg-type]
                flush_producer=False,
            )
        remainder = producer.producer.flush(timeout=30)
        if remainder:
            raise RuntimeError(f"Kafka flush left {remainder} telemetry events queued")
        if pending.warning_keys or pending.eruption_keys:
            self.commit_telemetry_state(state, state_file, pending.warning_keys, pending.eruption_keys)
        return len(pending.warnings), len(pending.eruptions)

    def feed(self, kafka_config: dict[str, str], kafka_topic: str, polling_interval: int, state_file: str, metadata_refresh_hours: int, once: bool = False) -> None:
        producer = JPJMAVolcanoEventProducer(Producer(kafka_config), kafka_topic)
        state = load_state(state_file)
        self.emit_reference_data(producer, state, state_file)
        while True:
            started = time.monotonic()
            self.maybe_refresh_reference_data(producer, state, state_file, metadata_refresh_hours)
            warnings, eruptions = self.poll_once(producer, state, state_file)
            logging.info("Emitted %d warning and %d eruption events", warnings, eruptions)
            if once:
                break
            time.sleep(max(0.0, polling_interval - (time.monotonic() - started)))


class MockAPI(JMABosaiVolcanoAPI, _CoreMockSource):
    pass


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Feed JMA Bosai volcanic warnings and eruptions to Kafka.")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("catalog", help="Fetch and print volcano catalog metadata")
    feed_parser = subparsers.add_parser("feed", help="Feed JMA volcano events to Kafka")
    feed_parser.add_argument("--kafka-bootstrap-servers", default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic", default=os.getenv("KAFKA_TOPIC", DEFAULT_TOPIC))
    feed_parser.add_argument("--sasl-username", default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument("-c", "--connection-string", default=os.getenv("CONNECTION_STRING"))
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "60")))
    feed_parser.add_argument("--metadata-refresh-hours", type=int, default=int(os.getenv("VOLCANO_METADATA_REFRESH_HOURS", "720")))
    feed_parser.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    args = parser.parse_args()

    api = MockAPI() if _mock_enabled() else JMABosaiVolcanoAPI()
    if args.command == "catalog":
        print(json.dumps([v.to_serializer_dict() for v in api.fetch_volcano_catalog().values()], ensure_ascii=False, indent=2))
    elif args.command == "feed":
        kafka_config, topic = build_kafka_config(args)
        api.feed(kafka_config, topic, args.polling_interval, args.state_file, args.metadata_refresh_hours, args.once or _mock_enabled())
    else:
        parser.print_help()
