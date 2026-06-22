"""Kafka feeder for Seattle Fire 911."""

from __future__ import annotations

import argparse
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from confluent_kafka import Producer

from seattle_911_core import (
    DATASET_PAGE_URL,
    DATASET_URL,
    DEFAULT_CONNECT_TIMEOUT_SECONDS,
    DEFAULT_KAFKA_FLUSH_TIMEOUT_SECONDS,
    DEFAULT_LOOKBACK_HOURS,
    DEFAULT_OVERLAP_MINUTES,
    DEFAULT_POLL_INTERVAL_SECONDS,
    DEFAULT_READ_TIMEOUT_SECONDS,
    LOGGER,
    SeattleFire911Bridge as CoreSeattleFire911Bridge,
    _save_state,
    parse_incident,
)
from seattle_911_producer_kafka_producer.producer import USWASeattleFire911EventProducer


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


class SeattleFire911Bridge(CoreSeattleFire911Bridge):
    """Kafka-specific wrapper around the transport-neutral Seattle Fire 911 core."""

    def save_state(self) -> None:
        _save_state(
            self.state_file,
            {
                "last_seen_datetime": self.last_seen_datetime,
                "sent_incident_numbers": self.sent_incident_order,
            },
        )

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
                sent_incident_numbers: List[str] = []
                for incident in incidents:
                    if incident.incident_number in self.sent_incident_numbers:
                        newest = max(newest or "", incident.incident_datetime)
                        continue
                    producer.send_us_wa_seattle_fire911_incident(
                        incident.incident_number,
                        data=incident,
                        _time=incident.incident_datetime_utc.isoformat(),
                        flush_producer=False,
                    )
                    sent_incident_numbers.append(incident.incident_number)
                    newest = max(newest or "", incident.incident_datetime)
                    sent += 1
                _flush_or_raise(producer.producer)
                self._remember_incidents(sent_incident_numbers)
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
    parser.add_argument(
        "--once",
        action="store_true",
        default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
        help="Poll once and exit (also via ONCE_MODE env var).",
    )
    args = parser.parse_args()

    kafka_config = parse_connection_string(args.connection_string)
    kafka_topic = kafka_config.pop("kafka_topic", None)
    if not kafka_config.get("bootstrap.servers") or not kafka_topic:
        raise ValueError("CONNECTION_STRING must provide bootstrap server and EntityPath")

    producer = Producer(kafka_config)
    event_producer = USWASeattleFire911EventProducer(producer, kafka_topic)
    SeattleFire911Bridge(state_file=args.last_polled_file).poll_and_send(event_producer, once=args.once)
