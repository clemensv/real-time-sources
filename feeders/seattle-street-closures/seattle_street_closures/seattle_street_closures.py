"""Seattle street closures bridge."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import time
from typing import Dict, List

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from confluent_kafka import Producer

from seattle_street_closures_producer_data import StreetClosure
from seattle_street_closures_producer_kafka_producer.producer import (
    USWASeattleStreetClosuresEventProducer,
)

LOGGER = logging.getLogger(__name__)

DATASET_URL = "https://data.seattle.gov/resource/ium9-iqtc.json"
DEFAULT_POLL_INTERVAL_SECONDS = 900
DEFAULT_CONNECT_TIMEOUT_SECONDS = 10
DEFAULT_READ_TIMEOUT_SECONDS = 120
DEFAULT_KAFKA_FLUSH_TIMEOUT_SECONDS = 30
DEFAULT_HTTP_RETRY_TOTAL = 3


def _build_retrying_session() -> requests.Session:
    """Create an HTTP session with bounded retries for transient upstream failures."""
    session = requests.Session()
    session.headers.update({"User-Agent": "GitHub-Copilot-CLI/1.0"})
    retry = Retry(
        total=DEFAULT_HTTP_RETRY_TOTAL,
        connect=DEFAULT_HTTP_RETRY_TOTAL,
        read=DEFAULT_HTTP_RETRY_TOTAL,
        status=DEFAULT_HTTP_RETRY_TOTAL,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _flush_or_raise(producer: Producer, timeout_seconds: int = DEFAULT_KAFKA_FLUSH_TIMEOUT_SECONDS) -> None:
    """Flush Kafka and fail the poll when messages remain undelivered."""
    remaining = producer.flush(timeout=timeout_seconds)
    if remaining:
        raise RuntimeError(
            f"Kafka flush timed out with {remaining} undelivered message(s) still queued"
        )


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse Event Hubs/Fabric or plain Kafka connection strings."""
    config_dict: Dict[str, str] = {}
    if not connection_string:
        return config_dict
    try:
        for part in connection_string.split(";"):
            if "=" not in part:
                continue
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"')
            if key == "Endpoint":
                config_dict["bootstrap.servers"] = value.replace("sb://", "").rstrip("/") + ":9093"
            elif key == "EntityPath":
                config_dict["kafka_topic"] = value
            elif key == "SharedAccessKeyName":
                config_dict["sasl.username"] = "$ConnectionString"
            elif key == "SharedAccessKey":
                config_dict["sasl.password"] = connection_string.strip()
            elif key == "BootstrapServer":
                config_dict["bootstrap.servers"] = value
    except ValueError as exc:
        raise ValueError("Invalid connection string format") from exc
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


def _load_state(state_file: str) -> dict:
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as handle:
                return json.load(handle)
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    if not state_file:
        return
    state_dir = os.path.dirname(state_file)
    if state_dir:
        os.makedirs(state_dir, exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def normalize_date(value: str | None) -> str | None:
    """Normalize Socrata calendar-date values to YYYY-MM-DD."""
    if not value:
        return None
    return value[:10]


def build_closure_id(record: dict) -> str:
    """Build the stable row identity for a closure occurrence window."""
    return "|".join(
        [
            str(record.get("permit_number", "")),
            str(record.get("segkey", "")),
            str(normalize_date(record.get("start_date")) or ""),
            str(normalize_date(record.get("end_date")) or ""),
        ]
    )


def parse_closure(record: dict) -> StreetClosure:
    """Map a Socrata row into the generated StreetClosure data class."""
    geometry = record.get("line_string")
    geometry_json = json.dumps(geometry, separators=(",", ":"), sort_keys=True) if geometry else None
    return StreetClosure(
        closure_id=build_closure_id(record),
        permit_number=str(record.get("permit_number", "")),
        permit_type=record.get("permit_type", ""),
        project_name=record.get("project_name"),
        project_description=record.get("project_description"),
        start_date=normalize_date(record.get("start_date")),
        end_date=normalize_date(record.get("end_date")),
        sunday=record.get("sunday"),
        monday=record.get("monday"),
        tuesday=record.get("tuesday"),
        wednesday=record.get("wednesday"),
        thursday=record.get("thursday"),
        friday=record.get("friday"),
        saturday=record.get("saturday"),
        street_on=record.get("street_on"),
        street_from=record.get("street_from"),
        street_to=record.get("street_to"),
        segkey=str(record.get("segkey", "")) if record.get("segkey") is not None else None,
        geometry_json=geometry_json,
    )


def closure_digest(closure: StreetClosure) -> str:
    """Hash the normalized closure payload for change detection."""
    return hashlib.sha256(closure.to_json().encode("utf-8")).hexdigest()


class SeattleStreetClosuresBridge:
    """Poll the Seattle street closures dataset and emit changed rows."""

    def __init__(self, state_file: str = ""):
        self.state_file = state_file
        self.session = _build_retrying_session()
        state = _load_state(state_file)
        self.previous_digests: Dict[str, str] = dict(state.get("previous_digests", {}))

    def save_state(self) -> None:
        _save_state(self.state_file, {"previous_digests": self.previous_digests})

    def fetch_closures(self) -> List[StreetClosure]:
        """Fetch the full current closure snapshot."""
        closures: List[StreetClosure] = []
        offset = 0
        limit = 1000
        while True:
            params = {
                "$select": ",".join(
                    [
                        "permit_number",
                        "permit_type",
                        "project_name",
                        "project_description",
                        "start_date",
                        "end_date",
                        "sunday",
                        "monday",
                        "tuesday",
                        "wednesday",
                        "thursday",
                        "friday",
                        "saturday",
                        "street_on",
                        "street_from",
                        "street_to",
                        "segkey",
                        "line_string",
                    ]
                ),
                "$order": "permit_number ASC",
                "$limit": limit,
                "$offset": offset,
            }
            response = self.session.get(
                DATASET_URL,
                params=params,
                timeout=(DEFAULT_CONNECT_TIMEOUT_SECONDS, DEFAULT_READ_TIMEOUT_SECONDS),
            )
            response.raise_for_status()
            rows = response.json()
            if not rows:
                break
            closures.extend(parse_closure(row) for row in rows if row.get("permit_number"))
            if len(rows) < limit:
                break
            offset += limit
        return closures

    def poll_and_send(self, producer: USWASeattleStreetClosuresEventProducer, once: bool = False) -> None:
        """Run the polling loop."""
        while True:
            try:
                closures = self.fetch_closures()
                current_digests: Dict[str, str] = {}
                sent = 0
                for closure in closures:
                    digest = closure_digest(closure)
                    current_digests[closure.closure_id] = digest
                    if self.previous_digests.get(closure.closure_id) == digest:
                        continue
                    producer.send_us_wa_seattle_street_closures_street_closure(
                        closure.closure_id,
                        closure,
                        flush_producer=False,
                    )
                    sent += 1
                _flush_or_raise(producer.producer)
                self.previous_digests = current_digests
                self.save_state()
                LOGGER.info("Fetched %d closures and sent %d new or changed rows", len(closures), sent)
            except Exception as exc:  # pylint: disable=broad-except
                LOGGER.exception("Error during Seattle street closure poll: %s", exc)

            if once:
                return
            time.sleep(DEFAULT_POLL_INTERVAL_SECONDS)


def main() -> None:
    """CLI entry point."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Seattle street closures bridge")
    parser.add_argument(
        "--connection-string",
        default=os.getenv("CONNECTION_STRING", ""),
        help="Kafka/Event Hubs/Fabric connection string",
    )
    parser.add_argument(
        "--state-file",
        default=os.getenv(
            "SEATTLE_STREET_CLOSURES_STATE_FILE",
            "/mnt/fileshare/seattle_street_closures_state.json",
        ),
        help="Path to the persisted snapshot state file",
    )
    parser.add_argument("--once", action="store_true", help="Poll once and exit")
    args = parser.parse_args()

    kafka_config = parse_connection_string(args.connection_string)
    kafka_topic = kafka_config.pop("kafka_topic", None)
    if not kafka_config.get("bootstrap.servers") or not kafka_topic:
        raise ValueError("CONNECTION_STRING must provide bootstrap server and EntityPath")

    producer = Producer(kafka_config)
    event_producer = USWASeattleStreetClosuresEventProducer(producer, kafka_topic)
    SeattleStreetClosuresBridge(state_file=args.state_file).poll_and_send(event_producer, once=args.once)
