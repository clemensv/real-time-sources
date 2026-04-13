"""Xceed public nightlife and live-entertainment events bridge to Kafka."""

import os
import sys
import time
import logging
import argparse
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple

import requests
from confluent_kafka import Producer
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from xceed_producer_data.event import Event
from xceed_producer_data.eventadmission import EventAdmission
from xceed_producer_kafka_producer.producer import XceedEventProducer, XceedAdmissionsEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

API_BASE = "https://events.xceed.me/v1"
FEED_URL = "https://events.xceed.me/v1"
DEFAULT_HTTP_RETRY_TOTAL = 3
DEFAULT_POLL_INTERVAL = 300
DEFAULT_EVENT_REFRESH_INTERVAL = 3600


def create_retrying_session(user_agent: str) -> requests.Session:
    """Create an HTTP session with bounded retries for transient upstream failures."""
    session = requests.Session()
    session.headers.update({
        "Accept": "application/json",
        "User-Agent": user_agent,
    })
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


class XceedAPI:
    """Client for the Xceed Open Event API."""

    def __init__(self, user_agent: str = "real-time-sources/1.0 (github.com/clemensv/real-time-sources)"):
        self.session = create_retrying_session(user_agent)

    def fetch_events(self) -> List[Dict[str, Any]]:
        """Fetch all events from the Xceed Open Event API."""
        resp = self.session.get(f"{API_BASE}/events", timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", []) if isinstance(data, dict) else data

    def fetch_admissions(self, event_id: str) -> List[Dict[str, Any]]:
        """Fetch admission tiers for a specific event."""
        resp = self.session.get(f"{API_BASE}/events/{event_id}/admissions", timeout=30)
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", []) if isinstance(data, dict) else data


def _extract_venue(event_raw: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """Extract venue fields from the raw event object."""
    venue = event_raw.get("venue") or {}
    venue_id = venue.get("id") or None
    venue_name = venue.get("name") or None
    # City may be nested in a location sub-object or at top level
    venue_city = venue.get("city") or (venue.get("location") or {}).get("city") or None
    venue_country_code = (
        venue.get("countryCode")
        or venue.get("country_code")
        or (venue.get("location") or {}).get("countryCode")
        or (venue.get("location") or {}).get("country_code")
        or None
    )
    return venue_id, venue_name, venue_city, venue_country_code


def parse_event(raw: Dict[str, Any]) -> Event:
    """Parse a raw API event record into an Event data class."""
    event_id = raw.get("id") or ""
    legacy_id = raw.get("legacyId") or None
    name = raw.get("name") or ""

    starting_ts = raw.get("startingTime")
    starting_time = (
        datetime.fromtimestamp(starting_ts, tz=timezone.utc)
        if starting_ts is not None
        else datetime.now(tz=timezone.utc)
    )

    ending_ts = raw.get("endingTime")
    ending_time = (
        datetime.fromtimestamp(ending_ts, tz=timezone.utc)
        if ending_ts is not None
        else None
    )

    venue_id, venue_name, venue_city, venue_country_code = _extract_venue(raw)

    return Event(
        event_id=event_id,
        legacy_id=legacy_id,
        name=name,
        slug=raw.get("slug") or None,
        starting_time=starting_time,
        ending_time=ending_time,
        cover_url=raw.get("coverUrl") or None,
        external_sales_url=raw.get("externalSalesUrl") or None,
        venue_id=venue_id,
        venue_name=venue_name,
        venue_city=venue_city,
        venue_country_code=venue_country_code,
    )


def parse_admission(raw: Dict[str, Any], event_id: str) -> EventAdmission:
    """Parse a raw API admission record into an EventAdmission data class."""
    admission_id = raw.get("id") or ""
    price_raw = raw.get("price")
    price = float(price_raw) if price_raw is not None else None

    remaining_raw = raw.get("remaining")
    remaining = int(remaining_raw) if remaining_raw is not None else None

    is_sold_out = raw.get("isSoldOut")
    if is_sold_out is not None:
        is_sold_out = bool(is_sold_out)

    is_sales_closed = raw.get("isSalesClosed")
    if is_sales_closed is not None:
        is_sales_closed = bool(is_sales_closed)

    return EventAdmission(
        event_id=event_id,
        admission_id=admission_id,
        name=raw.get("name") or None,
        is_sold_out=is_sold_out,
        is_sales_closed=is_sales_closed,
        price=price,
        currency=raw.get("currency") or None,
        remaining=remaining,
    )


def parse_connection_string(connection_string: str) -> Tuple[Dict[str, str], str]:
    """Parse an Event Hubs, Fabric, or plain BootstrapServer connection string."""
    config_dict: Dict[str, str] = {
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN",
        "sasl.username": "$ConnectionString",
        "sasl.password": connection_string.strip(),
    }
    kafka_topic = ""
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=")[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                kafka_topic = part.split("=")[1].strip('"')
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = "$ConnectionString"
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = connection_string.strip()
            elif "BootstrapServer" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc
    if "sasl.username" in config_dict and config_dict.get("bootstrap.servers", "").endswith(":9093"):
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict, kafka_topic


def feed(args: argparse.Namespace) -> None:
    """Main feed loop: emit events then poll admissions on each cycle."""
    connection_string = getattr(args, "connection_string", None) or os.environ.get("CONNECTION_STRING", "")
    if not connection_string:
        logger.error("CONNECTION_STRING is required")
        sys.exit(1)

    kafka_config, kafka_topic = parse_connection_string(connection_string)

    tls_enabled = os.environ.get("KAFKA_ENABLE_TLS", "true").lower()
    if tls_enabled == "false" and "security.protocol" not in kafka_config:
        kafka_config["security.protocol"] = "PLAINTEXT"
    elif tls_enabled == "false":
        kafka_config["security.protocol"] = "PLAINTEXT"
        kafka_config.pop("sasl.username", None)
        kafka_config.pop("sasl.password", None)
        kafka_config.pop("sasl.mechanisms", None)
        kafka_config.pop("sasl.mechanism", None)

    topic = getattr(args, "topic", None) or os.environ.get("KAFKA_TOPIC", "") or kafka_topic
    if not topic:
        logger.error("Kafka topic is required (set via EntityPath in CONNECTION_STRING or --topic)")
        sys.exit(1)

    polling_interval = int(
        getattr(args, "polling_interval", None)
        or os.environ.get("POLLING_INTERVAL", str(DEFAULT_POLL_INTERVAL))
    )
    event_refresh_interval = int(
        getattr(args, "event_refresh_interval", None)
        or os.environ.get("EVENT_REFRESH_INTERVAL", str(DEFAULT_EVENT_REFRESH_INTERVAL))
    )

    producer = Producer(kafka_config)
    event_producer = XceedEventProducer(producer, topic)
    admissions_producer = XceedAdmissionsEventProducer(producer, topic)
    api = XceedAPI()

    logger.info(
        "Starting Xceed feed to Kafka topic %s at %s (poll interval=%ds, event refresh=%ds)",
        topic,
        kafka_config.get("bootstrap.servers", "?"),
        polling_interval,
        event_refresh_interval,
    )

    cached_events: List[Dict[str, Any]] = []
    last_event_refresh: Optional[datetime] = None

    def _refresh_events() -> Optional[List[Dict[str, Any]]]:
        """Fetch events and return them, or None on failure."""
        try:
            events = api.fetch_events()
            logger.info("Fetched %d events from Xceed API", len(events))
            return events
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Failed to fetch events: %s", exc)
            return None

    def _emit_events(raw_events: List[Dict[str, Any]]) -> int:
        """Emit event reference records; return count sent."""
        count = 0
        for raw in raw_events:
            try:
                event_obj = parse_event(raw)
                if not event_obj.event_id:
                    continue
                event_producer.send_xceed_event(
                    _feedurl=FEED_URL,
                    _event_id=event_obj.event_id,
                    data=event_obj,
                    flush_producer=False,
                )
                count += 1
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error emitting event %s: %s", raw.get("id", "?"), exc)
        return count

    # Initial event fetch and reference data emission
    fresh = _refresh_events()
    if fresh is not None:
        cached_events = fresh
        last_event_refresh = datetime.now(tz=timezone.utc)
        count = _emit_events(cached_events)
        producer.flush()
        logger.info("Emitted %d xceed.Event reference records", count)
    else:
        logger.warning("Initial event fetch failed; proceeding with empty event cache")
        last_event_refresh = datetime.now(tz=timezone.utc)

    # Main polling loop
    while True:
        try:
            cycle_start = datetime.now(tz=timezone.utc)

            # Refresh event list if interval has elapsed
            if (
                last_event_refresh is None
                or (cycle_start - last_event_refresh).total_seconds() >= event_refresh_interval
            ):
                fresh = _refresh_events()
                if fresh is not None:
                    cached_events = fresh
                    last_event_refresh = cycle_start
                    count = _emit_events(cached_events)
                    producer.flush()
                    logger.info("Refreshed and emitted %d xceed.Event reference records", count)
                else:
                    logger.warning("Event refresh failed; using cached %d events", len(cached_events))

            # Poll admissions for each cached event
            admission_count = 0
            for raw_event in cached_events:
                event_id = raw_event.get("id", "")
                if not event_id:
                    continue
                try:
                    admissions_raw = api.fetch_admissions(event_id)
                    for adm_raw in admissions_raw:
                        try:
                            adm = parse_admission(adm_raw, event_id)
                            if not adm.admission_id:
                                continue
                            admissions_producer.send_xceed_event_admission(
                                _feedurl=FEED_URL,
                                _event_id=event_id,
                                _admission_id=adm.admission_id,
                                data=adm,
                                flush_producer=False,
                            )
                            admission_count += 1
                        except Exception as exc:  # pylint: disable=broad-except
                            logger.error(
                                "Error emitting admission %s for event %s: %s",
                                adm_raw.get("id", "?"),
                                event_id,
                                exc,
                            )
                except Exception as exc:  # pylint: disable=broad-except
                    logger.error("Error fetching admissions for event %s: %s", event_id, exc)

            remainder = producer.flush(timeout=30)
            if remainder > 0:
                logger.error(
                    "Flush incomplete: %d messages still queued; skipping state update",
                    remainder,
                )
            else:
                logger.info(
                    "Cycle complete: polled admissions for %d events (%d admission records emitted)",
                    len(cached_events),
                    admission_count,
                )

            elapsed = (datetime.now(tz=timezone.utc) - cycle_start).total_seconds()
            wait = max(0.0, polling_interval - elapsed)
            if wait > 0:
                time.sleep(wait)

        except KeyboardInterrupt:
            logger.info("Interrupted; shutting down")
            break
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Unexpected error in polling loop: %s", exc)
            time.sleep(polling_interval)


def main() -> None:
    """Entry point for the Xceed bridge."""
    parser = argparse.ArgumentParser(description="Xceed nightlife events bridge to Kafka")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Start the event and admission polling loop")
    feed_parser.add_argument(
        "--connection-string",
        help="Kafka / Event Hubs connection string (overrides CONNECTION_STRING env var)",
    )
    feed_parser.add_argument(
        "--topic",
        help="Kafka topic name (overrides EntityPath in connection string and KAFKA_TOPIC env var)",
    )
    feed_parser.add_argument(
        "--polling-interval",
        type=int,
        default=None,
        help=f"Admission polling interval in seconds (default: {DEFAULT_POLL_INTERVAL})",
    )
    feed_parser.add_argument(
        "--event-refresh-interval",
        type=int,
        default=None,
        help=f"Event list refresh interval in seconds (default: {DEFAULT_EVENT_REFRESH_INTERVAL})",
    )

    args = parser.parse_args()
    if args.command == "feed":
        feed(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
