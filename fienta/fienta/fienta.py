"""
Fienta Public Events Bridge
Polls the Fienta public events API and sends events to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
import logging
from typing import Dict, List, Optional, Tuple
import argparse
import requests
from fienta_producer_data import Event, EventSaleStatus
from fienta_producer_kafka_producer.producer import ComFientaEventProducer

FIENTA_API_URL = "https://fienta.com/api/v1/public/events"
POLL_INTERVAL_SECONDS = 300  # 5 minutes
REFERENCE_REFRESH_SECONDS = 3600  # 1 hour

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
LOGGER = logging.getLogger(__name__)


def fetch_events(page: int = 1) -> Optional[List[dict]]:
    """Fetch a page of public events from the Fienta API.

    Returns a list of event dicts, or None on error.
    The API returns up to 1000 events per page.
    """
    try:
        params: Dict[str, object] = {"page": page}
        response = requests.get(FIENTA_API_URL, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        # Handle both list and dict (paginated) response shapes
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("data") or data.get("events") or []
        return []
    except Exception as err:
        LOGGER.error("Error fetching Fienta events (page=%d): %s", page, err)
        return None


def fetch_all_events() -> Optional[List[dict]]:
    """Fetch all public events across all pages."""
    all_events: List[dict] = []
    page = 1
    while True:
        events = fetch_events(page=page)
        if events is None:
            return None if not all_events else all_events
        if not events:
            break
        all_events.extend(events)
        if len(events) < 1000:
            # Last page
            break
        page += 1
    return all_events


def parse_event_reference(raw: dict) -> Optional[Event]:
    """Parse a raw API event dict into an Event reference data object."""
    event_id = str(raw.get("id", "")).strip()
    if not event_id:
        return None
    name = raw.get("name") or ""
    organizer = raw.get("organizer") or {}
    categories_raw = raw.get("categories")
    categories: Optional[List[str]] = None
    if isinstance(categories_raw, list):
        categories = [str(c) for c in categories_raw if c is not None]
    location_raw = raw.get("location")
    location: Optional[str] = None
    if isinstance(location_raw, str):
        location = location_raw or None
    elif isinstance(location_raw, dict):
        location = location_raw.get("name") or location_raw.get("address") or None
    return Event(
        event_id=event_id,
        name=name,
        slug=raw.get("slug") or None,
        description=raw.get("description") or None,
        start=raw.get("start") or "",
        end=raw.get("end") or None,
        timezone=raw.get("timezone") or None,
        url=raw.get("url") or "",
        language=raw.get("language") or None,
        currency=raw.get("currency") or None,
        status=raw.get("status") or "published",
        sale_status=raw.get("sale_status") or "notOnSale",
        is_online=raw.get("is_online"),
        is_free=raw.get("is_free"),
        location=location,
        country=raw.get("country") or None,
        region=raw.get("region") or None,
        image_url=raw.get("image_url") or None,
        organizer_name=organizer.get("name") if isinstance(organizer, dict) else None,
        organizer_url=organizer.get("url") if isinstance(organizer, dict) else None,
        categories=categories,
        created_at=raw.get("created_at") or None,
        updated_at=raw.get("updated_at") or None,
    )


def parse_event_sale_status(raw: dict) -> Optional[EventSaleStatus]:
    """Parse a raw API event dict into an EventSaleStatus telemetry object."""
    event_id = str(raw.get("id", "")).strip()
    if not event_id:
        return None
    sale_status = raw.get("sale_status")
    if not sale_status:
        return None
    updated_at = raw.get("updated_at") or raw.get("created_at") or ""
    return EventSaleStatus(
        event_id=event_id,
        name=raw.get("name") or "",
        sale_status=sale_status,
        status=raw.get("status") or None,
        start=raw.get("start") or None,
        url=raw.get("url") or None,
        updated_at=updated_at,
    )


class FientaPoller:
    """Polls the Fienta public events API and sends CloudEvents to Kafka."""

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, state_file: str):
        self.kafka_topic = kafka_topic
        self.state_file = state_file
        from confluent_kafka import Producer as KafkaProducer
        kafka_producer = KafkaProducer(kafka_config)
        self.producer = ComFientaEventProducer(kafka_producer, kafka_topic)

    def load_state(self) -> Dict:
        """Load persisted sale-status state from disk."""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, OSError) as err:
            LOGGER.warning("Could not load state file: %s", err)
        return {}

    def save_state(self, state: Dict) -> None:
        """Persist sale-status state to disk."""
        try:
            state_dir = os.path.dirname(self.state_file)
            if state_dir:
                os.makedirs(state_dir, exist_ok=True)
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f)
        except OSError as err:
            LOGGER.warning("Could not save state file: %s", err)

    def emit_reference_data(self, events: List[dict]) -> int:
        """Emit Event reference data for all events. Returns count sent."""
        sent = 0
        for raw in events:
            ref = parse_event_reference(raw)
            if ref is None:
                continue
            self.producer.send_com_fienta_event(ref.event_id, ref, flush_producer=False)
            sent += 1
        if sent:
            remaining = self.producer.producer.flush(timeout=10)
            if remaining > 0:
                LOGGER.warning("Flush incomplete: %d messages still in queue", remaining)
                return sent
        return sent

    def emit_sale_status_changes(self, events: List[dict], state: Dict) -> Tuple[int, Dict]:
        """Emit EventSaleStatus events for changed sale statuses. Returns (count, updated_state)."""
        sent = 0
        flushed = False
        for raw in events:
            event_id = str(raw.get("id", "")).strip()
            if not event_id:
                continue
            current_status = raw.get("sale_status")
            if not current_status:
                continue
            previous_status = state.get(event_id)
            if current_status != previous_status:
                ess = parse_event_sale_status(raw)
                if ess is None:
                    continue
                self.producer.send_com_fienta_event_sale_status(
                    ess.event_id, ess, flush_producer=False)
                sent += 1
                flushed = False
        if sent:
            remaining = self.producer.producer.flush(timeout=10)
            if remaining > 0:
                LOGGER.warning("Flush incomplete: %d messages still in queue", remaining)
                return sent, state
            flushed = True
        # Only update state after successful flush
        if flushed or not sent:
            for raw in events:
                event_id = str(raw.get("id", "")).strip()
                current_status = raw.get("sale_status")
                if event_id and current_status:
                    state[event_id] = current_status
        return sent, state

    def poll_and_send(self, once: bool = False) -> None:
        """Main polling loop."""
        LOGGER.info("Starting Fienta poller, polling every %ds", POLL_INTERVAL_SECONDS)
        LOGGER.info("  API URL: %s", FIENTA_API_URL)
        LOGGER.info("  Kafka topic: %s", self.kafka_topic)

        # Emit reference data at startup
        LOGGER.info("Fetching initial Fienta events for reference data...")
        events = fetch_all_events()
        if events is not None:
            ref_sent = self.emit_reference_data(events)
            LOGGER.info("Sent %d event reference records", ref_sent)
        else:
            LOGGER.warning("Could not fetch events at startup; skipping reference emission")
            events = []

        state = self.load_state()

        # Emit initial sale-status snapshot
        if events:
            ess_sent, state = self.emit_sale_status_changes(events, state)
            LOGGER.info("Sent %d initial sale-status events", ess_sent)
            self.save_state(state)

        if once:
            return

        last_reference_time = time.monotonic()

        while True:
            try:
                time.sleep(POLL_INTERVAL_SECONDS)
                now = time.monotonic()

                events = fetch_all_events()
                if events is None:
                    LOGGER.warning("Failed to fetch events; will retry next poll")
                    continue

                # Refresh reference data periodically
                if (now - last_reference_time) >= REFERENCE_REFRESH_SECONDS:
                    ref_sent = self.emit_reference_data(events)
                    LOGGER.info("Refreshed %d event reference records", ref_sent)
                    last_reference_time = now

                # Emit sale-status changes
                state = self.load_state()
                ess_sent, state = self.emit_sale_status_changes(events, state)
                if ess_sent:
                    LOGGER.info("Sent %d sale-status change events", ess_sent)
                    self.save_state(state)
                else:
                    LOGGER.info("No sale-status changes detected (%d events polled)", len(events))

            except Exception as err:  # pylint: disable=broad-except
                LOGGER.error("Error in polling loop: %s", err)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Azure Event Hubs / Fabric / plain Kafka connection string."""
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = (
                    part.split('=')[1].strip('"')
                    .replace('sb://', '').replace('/', '') + ':9093'
                )
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=')[1].strip('"')
            elif 'SharedAccessKeyName' in part:
                config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part:
                config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if 'sasl.username' in config_dict:
        config_dict['security.protocol'] = 'SASL_SSL'
        config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fienta Public Events Bridge – polls the Fienta API and sends CloudEvents to Kafka"
    )
    parser.add_argument(
        'command', nargs='?', default='feed',
        choices=['feed'],
        help="Command to run (default: feed)"
    )
    parser.add_argument('--state-file', type=str,
                        help="Path to state file for sale-status deduplication")
    parser.add_argument('--kafka-bootstrap-servers', type=str,
                        help="Comma-separated list of Kafka bootstrap servers")
    parser.add_argument('--kafka-topic', type=str,
                        help="Kafka topic to send messages to")
    parser.add_argument('--sasl-username', type=str,
                        help="Username for SASL PLAIN authentication")
    parser.add_argument('--sasl-password', type=str,
                        help="Password for SASL PLAIN authentication")
    parser.add_argument('--connection-string', type=str,
                        help='Event Hubs / Fabric / plain Kafka connection string')

    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.state_file:
        args.state_file = os.getenv('FIENTA_STATE_FILE',
                                     os.path.expanduser('~/.fienta_state.json'))

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = config_params.get('bootstrap.servers')
        kafka_topic = config_params.get('kafka_topic')
        sasl_username = config_params.get('sasl.username')
        sasl_password = config_params.get('sasl.password')
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided via --kafka-bootstrap-servers or --connection-string.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided via --kafka-topic or --connection-string.")
        sys.exit(1)

    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
    kafka_config: Dict[str, str] = {'bootstrap.servers': kafka_bootstrap_servers}
    if sasl_username and sasl_password:
        kafka_config.update({
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password,
        })
    elif tls_enabled:
        kafka_config['security.protocol'] = 'SSL'

    poller = FientaPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        state_file=args.state_file,
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
