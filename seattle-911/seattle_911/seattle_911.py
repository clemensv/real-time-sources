"""Seattle Fire 911 bridge."""

from __future__ import annotations

import argparse
import json
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests
from confluent_kafka import Producer

from seattle_911_producer_data import Incident
from seattle_911_producer_kafka_producer.producer import USWASeattleFire911EventProducer

LOGGER = logging.getLogger(__name__)

DATASET_URL = "https://data.seattle.gov/resource/kzjm-xkqj.json"
DATASET_PAGE_URL = "https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj"
DEFAULT_POLL_INTERVAL_SECONDS = 300
DEFAULT_LOOKBACK_HOURS = 24
DEFAULT_OVERLAP_MINUTES = 10
MAX_SEEN_IDS = 50000


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


def parse_incident(record: dict) -> Incident:
    """Map a Socrata row into the generated Incident data class."""
    return Incident(
        incident_number=str(record.get("incident_number", "")),
        incident_type=record.get("type", ""),
        incident_datetime=record.get("datetime", ""),
        address=record.get("address"),
        latitude=float(record["latitude"]) if record.get("latitude") not in (None, "") else None,
        longitude=float(record["longitude"]) if record.get("longitude") not in (None, "") else None,
    )


class SeattleFire911Bridge:
    """Poll the Seattle Fire 911 dataset and emit incident events."""

    def __init__(self, state_file: str = ""):
        self.state_file = state_file
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "GitHub-Copilot-CLI/1.0"})
        state = _load_state(state_file)
        sent_ids = [str(value) for value in state.get("sent_incident_numbers", [])]
        self.sent_incident_numbers = set(sent_ids[-MAX_SEEN_IDS:])
        self.sent_incident_order = sent_ids[-MAX_SEEN_IDS:]
        self.last_seen_datetime = state.get("last_seen_datetime")

    def save_state(self) -> None:
        _save_state(
            self.state_file,
            {
                "last_seen_datetime": self.last_seen_datetime,
                "sent_incident_numbers": self.sent_incident_order[-MAX_SEEN_IDS:],
            },
        )

    def fetch_incidents(self, since: Optional[datetime] = None) -> List[Incident]:
        """Fetch recent incident rows from the SODA endpoint."""
        incidents: List[Incident] = []
        offset = 0
        limit = 1000
        while True:
            params = {
                "$select": "address,type,datetime,latitude,longitude,incident_number",
                "$order": "datetime ASC",
                "$limit": limit,
                "$offset": offset,
            }
            if since is not None:
                params["$where"] = f"datetime >= '{since.strftime('%Y-%m-%dT%H:%M:%S')}'"
            response = self.session.get(DATASET_URL, params=params, timeout=60)
            response.raise_for_status()
            rows = response.json()
            if not rows:
                break
            incidents.extend(parse_incident(row) for row in rows if row.get("incident_number"))
            if len(rows) < limit:
                break
            offset += limit
        return incidents

    def _remember_incident(self, incident_number: str) -> None:
        if incident_number in self.sent_incident_numbers:
            return
        self.sent_incident_numbers.add(incident_number)
        self.sent_incident_order.append(incident_number)
        if len(self.sent_incident_order) > MAX_SEEN_IDS:
            removed = self.sent_incident_order.pop(0)
            self.sent_incident_numbers.discard(removed)

    def poll_and_send(self, producer: USWASeattleFire911EventProducer, once: bool = False) -> None:
        """Run the polling loop."""
        LOGGER.info("Starting Seattle Fire 911 bridge for %s", DATASET_PAGE_URL)
        while True:
            try:
                if self.last_seen_datetime:
                    last_seen = datetime.fromisoformat(self.last_seen_datetime)
                    since = last_seen - timedelta(minutes=DEFAULT_OVERLAP_MINUTES)
                else:
                    since = datetime.utcnow() - timedelta(hours=DEFAULT_LOOKBACK_HOURS)

                incidents = self.fetch_incidents(since=since)
                sent = 0
                newest: Optional[str] = self.last_seen_datetime
                for incident in incidents:
                    if incident.incident_number in self.sent_incident_numbers:
                        newest = max(newest or "", incident.incident_datetime)
                        continue
                    producer.send_us_wa_seattle_fire911_incident(
                        incident.incident_number,
                        incident,
                        flush_producer=False,
                    )
                    self._remember_incident(incident.incident_number)
                    newest = max(newest or "", incident.incident_datetime)
                    sent += 1
                producer.producer.flush()
                if newest:
                    self.last_seen_datetime = newest
                self.save_state()
                LOGGER.info("Fetched %d incidents and sent %d new incidents", len(incidents), sent)
            except Exception as exc:  # pylint: disable=broad-except
                LOGGER.exception("Error during Seattle Fire 911 poll: %s", exc)

            if once:
                return
            time.sleep(DEFAULT_POLL_INTERVAL_SECONDS)


def main() -> None:
    """CLI entry point."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Seattle Fire 911 bridge")
    parser.add_argument(
        "--connection-string",
        default=os.getenv("CONNECTION_STRING", ""),
        help="Kafka/Event Hubs/Fabric connection string",
    )
    parser.add_argument(
        "--last-polled-file",
        default=os.getenv(
            "SEATTLE_911_LAST_POLLED_FILE",
            "/mnt/fileshare/seattle_911_last_polled.json",
        ),
        help="Path to the persisted dedupe state file",
    )
    parser.add_argument("--once", action="store_true", help="Poll once and exit")
    args = parser.parse_args()

    kafka_config = parse_connection_string(args.connection_string)
    kafka_topic = kafka_config.pop("kafka_topic", None)
    if not kafka_config.get("bootstrap.servers") or not kafka_topic:
        raise ValueError("CONNECTION_STRING must provide bootstrap server and EntityPath")

    producer = Producer(kafka_config)
    event_producer = USWASeattleFire911EventProducer(producer, kafka_topic)
    SeattleFire911Bridge(state_file=args.last_polled_file).poll_and_send(event_producer, once=args.once)
