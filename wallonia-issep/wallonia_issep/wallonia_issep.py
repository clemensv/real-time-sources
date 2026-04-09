"""Wallonia ISSeP air-quality bridge to Kafka."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

import requests
from confluent_kafka import Producer
from wallonia_issep_producer_data import Observation, SensorConfiguration
from wallonia_issep_producer_kafka_producer.producer import (
    BeIssepAirqualitySensorsEventProducer,
)


if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


LOGGER = logging.getLogger(__name__)


def _load_state(state_file: str) -> Dict[str, str]:
    """Load persisted per-configuration dedup state from disk."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as handle:
                return json.load(handle)
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def _save_state(state_file: str, state: Dict[str, str]) -> None:
    """Persist per-configuration dedup state to disk."""
    if not state_file:
        return
    try:
        with open(state_file, "w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, sort_keys=True)
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Could not save state to %s: %s", state_file, exc)


def _parse_bool(value: Any) -> bool:
    """Parse a truthy or falsy string value."""
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() not in {"0", "false", "no", "off", ""}


def _safe_int(value: Any) -> Optional[int]:
    """Convert a value to int, returning None if not possible."""
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _safe_float(value: Any) -> Optional[float]:
    """Convert a value to float, returning None if not possible."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


class WalloniaISsePAPI:
    """Poll the Wallonia ISSeP Opendatasoft API and emit CloudEvents."""

    BASE_URL = "https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records"
    DEFAULT_TOPIC = "wallonia-issep"
    DEFAULT_TIMEOUT = 30
    DEFAULT_LIMIT = 100
    DEFAULT_REFERENCE_REFRESH_INTERVAL = 24 * 60 * 60

    def __init__(
        self,
        session: Optional[requests.Session] = None,
        *,
        base_url: str = BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        page_limit: int = DEFAULT_LIMIT,
        reference_refresh_interval: int = DEFAULT_REFERENCE_REFRESH_INTERVAL,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.page_limit = page_limit
        self.reference_refresh_interval = reference_refresh_interval
        self.session = session or requests.Session()
        self.session.headers.setdefault("Accept", "application/json")

    @staticmethod
    def parse_connection_string(connection_string: str) -> Tuple[Dict[str, str], Optional[str]]:
        """Parse Event Hubs or plain Kafka connection strings."""
        if not connection_string:
            return {}, None

        parts: Dict[str, str] = {}
        for fragment in connection_string.split(";"):
            fragment = fragment.strip()
            if not fragment:
                continue
            key, separator, value = fragment.partition("=")
            if not separator:
                raise ValueError("Invalid connection string format")
            parts[key.strip()] = value.strip().strip('"')

        if "Endpoint" in parts:
            endpoint = parts["Endpoint"].replace("sb://", "").rstrip("/")
            return (
                {
                    "bootstrap.servers": f"{endpoint}:9093",
                    "security.protocol": "SASL_SSL",
                    "sasl.mechanisms": "PLAIN",
                    "sasl.username": "$ConnectionString",
                    "sasl.password": connection_string.strip(),
                },
                parts.get("EntityPath"),
            )

        if "BootstrapServer" in parts:
            return (
                {
                    "bootstrap.servers": parts["BootstrapServer"],
                },
                parts.get("EntityPath"),
            )

        raise ValueError("Unsupported connection string format")

    def _get_json(self, params: Optional[Dict[str, Any]] = None) -> Any:
        """Fetch JSON from the Opendatasoft API."""
        response = self.session.get(self.base_url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def fetch_all_records(self) -> List[Dict[str, Any]]:
        """Fetch all records from the API with pagination."""
        items: List[Dict[str, Any]] = []
        offset = 0
        while True:
            params = {"limit": self.page_limit, "offset": offset}
            payload = self._get_json(params=params)
            results = payload.get("results", [])
            if not results:
                break
            items.extend(results)
            total_count = payload.get("total_count", 0)
            if offset + len(results) >= total_count:
                break
            offset += self.page_limit
        return items

    def normalize_observation(self, record: Dict[str, Any]) -> Observation:
        """Normalize one upstream Opendatasoft record into an Observation."""
        config_id = str(record.get("id_configuration", ""))
        moment = str(record.get("moment", ""))

        return Observation(
            configuration_id=config_id,
            moment=moment,
            co=_safe_int(record.get("co")),
            no=_safe_int(record.get("no")),
            no2=_safe_int(record.get("no2")),
            o3no2=_safe_int(record.get("o3no2")),
            ppbno=_safe_float(record.get("ppbno")),
            ppbno_statut=_safe_int(record.get("ppbno_statut")),
            ppbno2=_safe_float(record.get("ppbno2")),
            ppbno2_statut=_safe_int(record.get("ppbno2_statut")),
            ppbo3=_safe_float(record.get("ppbo3")),
            ppbo3_statut=_safe_int(record.get("ppbo3_statut")),
            ugpcmno=_safe_float(record.get("ugpcmno")),
            ugpcmno_statut=_safe_int(record.get("ugpcmno_statut")),
            ugpcmno2=_safe_float(record.get("ugpcmno2")),
            ugpcmno2_statut=_safe_int(record.get("ugpcmno2_statut")),
            ugpcmo3=_safe_float(record.get("ugpcmo3")),
            ugpcmo3_statut=_safe_int(record.get("ugpcmo3_statut")),
            bme_t=_safe_float(record.get("bme_t")),
            bme_t_statut=_safe_int(record.get("bme_t_statut")),
            bme_pres=_safe_int(record.get("bme_pres")),
            bme_pres_statut=_safe_int(record.get("bme_pres_statut")),
            bme_rh=_safe_float(record.get("bme_rh")),
            bme_rh_statut=_safe_int(record.get("bme_rh_statut")),
            pm1=_safe_float(record.get("pm1")),
            pm1_statut=_safe_int(record.get("pm1_statut")),
            pm25=_safe_float(record.get("pm25")),
            pm25_statut=_safe_int(record.get("pm25_statut")),
            pm4=_safe_float(record.get("pm4")),
            pm4_statut=_safe_int(record.get("pm4_statut")),
            pm10=_safe_float(record.get("pm10")),
            pm10_statut=_safe_int(record.get("pm10_statut")),
            vbat=_safe_float(record.get("vbat")),
            vbat_statut=_safe_int(record.get("vbat_statut")),
            mwh_bat=_safe_float(record.get("mwh_bat")),
            mwh_pv=_safe_float(record.get("mwh_pv")),
            co_rf=_safe_float(record.get("co_rf")),
            no_rf=_safe_float(record.get("no_rf")),
            no2_rf=_safe_float(record.get("no2_rf")),
            o3no2_rf=_safe_float(record.get("o3no2_rf")),
            o3_rf=_safe_float(record.get("o3_rf")),
            pm10_rf=_safe_float(record.get("pm10_rf")),
        )

    @staticmethod
    def extract_configurations(records: List[Dict[str, Any]]) -> List[SensorConfiguration]:
        """Extract distinct sensor configurations from data records."""
        seen: Set[str] = set()
        configs: List[SensorConfiguration] = []
        for record in records:
            config_id = str(record.get("id_configuration", ""))
            if config_id and config_id not in seen:
                seen.add(config_id)
                configs.append(SensorConfiguration(configuration_id=config_id))
        return configs

    @staticmethod
    def filter_new_records(
        records: List[Dict[str, Any]],
        state: Dict[str, str],
    ) -> List[Dict[str, Any]]:
        """Return only records newer than the persisted state and advance the state."""
        new_records: List[Dict[str, Any]] = []
        for record in records:
            config_id = str(record.get("id_configuration", ""))
            moment = str(record.get("moment", ""))
            if not config_id or not moment:
                continue
            last_moment = state.get(config_id, "")
            try:
                current_dt = datetime.fromisoformat(moment)
                if last_moment:
                    last_dt = datetime.fromisoformat(last_moment)
                    if current_dt <= last_dt:
                        continue
            except ValueError:
                if moment <= last_moment:
                    continue

            new_records.append(record)
            if not last_moment or moment > last_moment:
                state[config_id] = moment

        return new_records

    @classmethod
    def build_kafka_config(cls, args: argparse.Namespace) -> Tuple[Dict[str, str], str]:
        """Build Kafka configuration from CLI arguments and environment variables."""
        parsed_config, parsed_topic = cls.parse_connection_string(args.connection_string) if args.connection_string else ({}, None)

        kafka_topic = args.kafka_topic or parsed_topic or cls.DEFAULT_TOPIC
        kafka_enable_tls = _parse_bool(args.kafka_enable_tls)
        kafka_config = dict(parsed_config)

        if args.kafka_bootstrap_servers:
            kafka_config["bootstrap.servers"] = args.kafka_bootstrap_servers

        if "bootstrap.servers" not in kafka_config:
            raise ValueError("Kafka bootstrap servers are required")

        if "sasl.username" not in kafka_config and args.sasl_username:
            kafka_config["sasl.username"] = args.sasl_username
            kafka_config["sasl.password"] = args.sasl_password or ""
            kafka_config["sasl.mechanisms"] = "PLAIN"
            kafka_config["security.protocol"] = "SASL_SSL" if kafka_enable_tls else "SASL_PLAINTEXT"
        elif "security.protocol" not in kafka_config:
            kafka_config["security.protocol"] = "SSL" if kafka_enable_tls else "PLAINTEXT"

        return kafka_config, kafka_topic

    def emit_reference_data(
        self,
        producer: BeIssepAirqualitySensorsEventProducer,
        records: List[Dict[str, Any]],
    ) -> List[SensorConfiguration]:
        """Extract and emit sensor configuration reference events."""
        configs = self.extract_configurations(records)
        for config in configs:
            producer.send_be_issep_airquality_sensor_configuration(
                _configuration_id=config.configuration_id,
                data=config,
                flush_producer=False,
            )
        producer.producer.flush()
        LOGGER.info("Sent %d sensor configuration reference events", len(configs))
        return configs

    def poll_observations(
        self,
        *,
        producer: BeIssepAirqualitySensorsEventProducer,
        state: Dict[str, str],
    ) -> Tuple[int, List[Dict[str, Any]]]:
        """Poll records and emit only new observations. Returns count and all records."""
        all_records = self.fetch_all_records()
        new_records = self.filter_new_records(all_records, state)
        observation_count = 0

        for record in new_records:
            try:
                obs = self.normalize_observation(record)
                producer.send_be_issep_airquality_observation(
                    _configuration_id=obs.configuration_id,
                    data=obs,
                    flush_producer=False,
                )
                observation_count += 1
            except Exception as exc:  # pylint: disable=broad-except
                LOGGER.warning(
                    "Could not normalize or emit observation for config %s: %s",
                    record.get("id_configuration"),
                    exc,
                )

        producer.producer.flush()
        return observation_count, all_records

    def run_feed(
        self,
        *,
        kafka_config: Dict[str, str],
        kafka_topic: str,
        polling_interval: int,
        state_file: str,
    ) -> None:
        """Run the long-lived reference-data and observation polling loop."""
        kafka_producer = Producer(kafka_config)
        producer = BeIssepAirqualitySensorsEventProducer(kafka_producer, kafka_topic)
        state = _load_state(state_file)
        last_reference_refresh = 0.0

        LOGGER.info(
            "Starting Wallonia ISSeP bridge for topic %s at bootstrap servers %s",
            kafka_topic,
            kafka_config["bootstrap.servers"],
        )

        try:
            while True:
                cycle_started = time.monotonic()
                now = time.time()

                observation_count, all_records = self.poll_observations(
                    producer=producer,
                    state=state,
                )

                if not last_reference_refresh or now - last_reference_refresh >= self.reference_refresh_interval:
                    self.emit_reference_data(producer, all_records)
                    last_reference_refresh = now

                _save_state(state_file, state)

                elapsed = time.monotonic() - cycle_started
                sleep_seconds = max(0.0, polling_interval - elapsed)
                LOGGER.info(
                    "Sent %d observation events in %.1f seconds. Waiting %.1f seconds.",
                    observation_count,
                    elapsed,
                    sleep_seconds,
                )
                if sleep_seconds:
                    time.sleep(sleep_seconds)
        except KeyboardInterrupt:
            LOGGER.info("Stopping Wallonia ISSeP bridge")
        finally:
            kafka_producer.flush()


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Wallonia ISSeP air quality bridge to Kafka")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Poll ISSeP and emit CloudEvents to Kafka")
    feed_parser.add_argument("--connection-string", type=str, default=os.getenv("CONNECTION_STRING"))
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str, default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic", type=str, default=os.getenv("KAFKA_TOPIC", WalloniaISsePAPI.DEFAULT_TOPIC))
    feed_parser.add_argument("--sasl-username", type=str, default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "600")))
    feed_parser.add_argument(
        "--state-file",
        type=str,
        default=os.getenv("STATE_FILE", os.path.expanduser("~/.wallonia_issep_state.json")),
    )
    feed_parser.add_argument("--kafka-enable-tls", type=str, default=os.getenv("KAFKA_ENABLE_TLS", "true"))

    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        return

    kafka_config, kafka_topic = WalloniaISsePAPI.build_kafka_config(args)
    api = WalloniaISsePAPI()
    api.run_feed(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        polling_interval=args.polling_interval,
        state_file=args.state_file,
    )


if __name__ == "__main__":
    main()
