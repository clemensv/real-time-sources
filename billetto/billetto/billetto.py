"""
Billetto Public Events Bridge
Polls the Billetto public events REST API and sends events to a Kafka topic.
"""

import os
import sys
import json
import time
import hashlib
import logging
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Mapping, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from confluent_kafka import Producer

# pylint: disable=import-error, line-too-long
from billetto_producer_data import Event
from billetto_producer_kafka_producer.producer import BillettoEventsEventProducer
# pylint: enable=import-error, line-too-long

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://billetto.dk"
DEFAULT_EVENTS_PATH = "/api/v3/public/events"
DEFAULT_PAGE_SIZE = 100
DEFAULT_POLLING_INTERVAL = 300  # seconds
DEFAULT_TOPIC = "billetto-events"
MIN_RATE_LIMIT_COOLDOWN_SECONDS = 60.0
FILTER_ENV_VARS = {
    "postal_code": "BILLETTO_POSTAL_CODE",
    "macroregion": "BILLETTO_MACROREGION",
    "region": "BILLETTO_REGION",
    "subregion": "BILLETTO_SUBREGION",
    "organizer_id": "BILLETTO_ORGANIZER_ID",
    "type": "BILLETTO_EVENT_TYPE",
    "category": "BILLETTO_CATEGORY",
    "subcategory": "BILLETTO_SUBCATEGORY",
}


def _make_session(api_keypair: str) -> requests.Session:
    """Create a retrying requests session with Billetto API authentication."""
    session = requests.Session()
    session.headers.update({
        "Api-Keypair": api_keypair,
        "Accept": "application/json",
    })
    retry = Retry(
        total=5,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _safe_header_int(headers: Mapping[str, str], name: str) -> Optional[int]:
    """Parse an integer rate-limit header, returning None when absent or invalid."""
    raw_value = headers.get(name)
    if raw_value in (None, ""):
        return None
    try:
        return int(raw_value)
    except (TypeError, ValueError):
        logger.warning("Ignoring invalid Billetto header %s=%r", name, raw_value)
        return None


def _collect_api_filters(
    *,
    postal_code: Optional[str] = None,
    macroregion: Optional[str] = None,
    region: Optional[str] = None,
    subregion: Optional[str] = None,
    organizer_id: Optional[str] = None,
    event_type: Optional[str] = None,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
) -> Dict[str, str]:
    """Collect supported Billetto API filters, dropping empty values."""
    filter_values = {
        "postal_code": postal_code,
        "macroregion": macroregion,
        "region": region,
        "subregion": subregion,
        "organizer_id": organizer_id,
        "type": event_type,
        "category": category,
        "subcategory": subcategory,
    }
    return {
        key: value.strip()
        for key, value in filter_values.items()
        if isinstance(value, str) and value.strip()
    }


def _resolve_api_filters(args: argparse.Namespace) -> Dict[str, str]:
    """Resolve supported Billetto API filters from CLI arguments or environment."""
    return _collect_api_filters(
        postal_code=getattr(args, "postal_code", None) or os.environ.get(FILTER_ENV_VARS["postal_code"]),
        macroregion=getattr(args, "macroregion", None) or os.environ.get(FILTER_ENV_VARS["macroregion"]),
        region=getattr(args, "region", None) or os.environ.get(FILTER_ENV_VARS["region"]),
        subregion=getattr(args, "subregion", None) or os.environ.get(FILTER_ENV_VARS["subregion"]),
        organizer_id=getattr(args, "organizer_id", None) or os.environ.get(FILTER_ENV_VARS["organizer_id"]),
        event_type=getattr(args, "event_type", None) or os.environ.get(FILTER_ENV_VARS["type"]),
        category=getattr(args, "category", None) or os.environ.get(FILTER_ENV_VARS["category"]),
        subcategory=getattr(args, "subcategory", None) or os.environ.get(FILTER_ENV_VARS["subcategory"]),
    )


def _add_filter_arguments(parser: argparse.ArgumentParser) -> None:
    """Add supported Billetto API filter arguments to a sub-command parser."""
    parser.add_argument(
        "--postal-code",
        type=str,
        default=None,
        help="Limit events to a specific postal code returned by Billetto's public feed.",
    )
    parser.add_argument(
        "--macroregion",
        type=str,
        default=None,
        help="Limit events to a Billetto macroregion such as Danmark or Södra Sverige.",
    )
    parser.add_argument(
        "--region",
        type=str,
        default=None,
        help="Limit events to a Billetto region such as Hovedstaden or Midtjylland.",
    )
    parser.add_argument(
        "--subregion",
        type=str,
        default=None,
        help="Limit events to a Billetto subregion such as Byen København or Østjylland.",
    )
    parser.add_argument(
        "--organizer-id",
        type=str,
        default=None,
        help="Limit events to one Billetto organizer ID.",
    )
    parser.add_argument(
        "--event-type",
        dest="event_type",
        type=str,
        default=None,
        help="Limit events by Billetto event type such as concert, seminar, or festival.",
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="Limit events by Billetto category such as music, sports, or performing_arts.",
    )
    parser.add_argument(
        "--subcategory",
        type=str,
        default=None,
        help="Limit events by Billetto subcategory such as pop, theatre, or cycling.",
    )


def parse_connection_string(connection_string: str) -> Tuple[Dict[str, str], str]:
    """Parse a Kafka connection string (plain broker or Event Hubs / Fabric format).

    Returns:
        (kafka_config, topic_name)
    """
    # Plain BootstrapServer format: BootstrapServer=host:port;EntityPath=topic
    if connection_string.strip().startswith("BootstrapServer="):
        config: Dict[str, str] = {}
        topic_name = ""
        enable_tls = os.environ.get("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        for part in connection_string.split(";"):
            part = part.strip()
            if part.startswith("BootstrapServer="):
                config["bootstrap.servers"] = part[len("BootstrapServer="):]
            elif part.startswith("EntityPath="):
                topic_name = part[len("EntityPath="):]
        if enable_tls:
            config["security.protocol"] = "SSL"
        return config, topic_name

    # Azure Event Hubs / Fabric Event Streams AMQP-style connection string
    config_dict: Dict[str, str] = {
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN",
        "sasl.username": "$ConnectionString",
        "sasl.password": connection_string.strip(),
    }
    topic_name = ""
    for part in connection_string.split(";"):
        part = part.strip()
        if part.startswith("Endpoint="):
            endpoint = part[len("Endpoint="):].strip('"').replace("sb://", "").rstrip("/")
            config_dict["bootstrap.servers"] = endpoint + ":9093"
        elif part.startswith("EntityPath="):
            topic_name = part[len("EntityPath="):].strip('"')
    return config_dict, topic_name


def _event_hash(raw: dict) -> str:
    """Compute a deterministic hash for deduplication."""
    canonical = json.dumps(raw, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(canonical.encode()).hexdigest()


def _parse_event(raw: dict) -> Optional[Event]:
    """Normalize a raw Billetto API event dict into an Event dataclass."""
    event_id = raw.get("id")
    if event_id is None:
        return None

    location = raw.get("location") or {}
    organiser = raw.get("organiser") or {}
    minimum_price = raw.get("minimum_price") or {}

    return Event(
        event_id=int(event_id),
        title=raw.get("title") or "",
        description=raw.get("description"),
        startdate=raw.get("startdate") or "",
        enddate=raw.get("enddate"),
        url=raw.get("url"),
        image_link=raw.get("image_link"),
        status=raw.get("status"),
        location_city=location.get("city"),
        location_name=location.get("location_name"),
        location_address=location.get("address"),
        location_zip_code=location.get("zip_code"),
        location_country_code=location.get("country_code"),
        location_latitude=_safe_float(location.get("latitude")),
        location_longitude=_safe_float(location.get("longitude")),
        organiser_id=_safe_int(organiser.get("id")),
        organiser_name=organiser.get("name"),
        minimum_price_amount_in_cents=_safe_int(minimum_price.get("amount_in_cents")),
        minimum_price_currency=minimum_price.get("currency"),
        availability=_derive_availability(raw),
    )


def _safe_float(value) -> Optional[float]:
    """Convert a value to float, returning None on failure."""
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _safe_int(value) -> Optional[int]:
    """Convert a value to int, returning None on failure."""
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _derive_availability(raw: dict) -> Optional[str]:
    """Derive a string availability status from the raw event payload."""
    # Explicit sold_out flag
    if raw.get("sold_out") is True:
        return "sold_out"
    # Check availability field if present
    avail = raw.get("availability")
    if isinstance(avail, dict):
        status = avail.get("status")
        if status:
            return str(status)
    if isinstance(avail, str):
        return avail
    # Infer from end date — if event has passed, mark unavailable
    enddate = raw.get("enddate") or raw.get("startdate")
    if enddate:
        try:
            end = datetime.fromisoformat(enddate.replace("Z", "+00:00"))
            if end.tzinfo is None:
                end = end.replace(tzinfo=timezone.utc)
            if end < datetime.now(timezone.utc):
                return "unavailable"
        except (ValueError, AttributeError):
            pass
    return "available"


class BillettoPoller:
    """Polls the Billetto public events API and emits CloudEvents to Kafka."""

    def __init__(
        self,
        api_keypair: str,
        base_url: str = DEFAULT_BASE_URL,
        page_size: int = DEFAULT_PAGE_SIZE,
        api_filters: Optional[Dict[str, str]] = None,
        kafka_config: Optional[Dict[str, str]] = None,
        kafka_topic: Optional[str] = None,
        state_file: str = "",
        sleep_func: Callable[[float], None] = time.sleep,
        monotonic_func: Callable[[], float] = time.monotonic,
    ):
        self.api_keypair = api_keypair
        self.base_url = base_url.rstrip("/")
        self.page_size = page_size
        self.api_filters = dict(api_filters or {})
        self.kafka_topic = kafka_topic
        self.state_file = state_file
        self._session: Optional[requests.Session] = None
        self._sleep = sleep_func
        self._monotonic = monotonic_func
        self._rate_limit_cooldown_until = 0.0

        if kafka_config is not None:
            producer = Producer(kafka_config)
            self.event_producer = BillettoEventsEventProducer(producer, kafka_topic)
        else:
            self.event_producer = None

    def _get_session(self) -> requests.Session:
        if self._session is None:
            self._session = _make_session(self.api_keypair)
        return self._session

    def _schedule_rate_limit_cooldown(self, headers: Mapping[str, str], reason: str) -> None:
        """Start or extend the global Billetto API cool-off window."""
        retry_after_ms = _safe_header_int(headers, "X-Ratelimit-Retry-After") or 0
        cooldown_seconds = max(MIN_RATE_LIMIT_COOLDOWN_SECONDS, retry_after_ms / 1000.0)
        cooldown_until = self._monotonic() + cooldown_seconds
        self._rate_limit_cooldown_until = max(self._rate_limit_cooldown_until, cooldown_until)
        logger.warning(
            "Billetto rate limit triggered (%s). Cooling down for %.3f seconds",
            reason,
            cooldown_seconds,
        )

    def _wait_for_rate_limit_cooldown(self) -> None:
        """Sleep until Billetto's documented cool-off window has elapsed."""
        remaining_seconds = self._rate_limit_cooldown_until - self._monotonic()
        if remaining_seconds <= 0:
            return
        logger.warning(
            "Waiting %.3f seconds before the next Billetto API call due to rate limiting",
            remaining_seconds,
        )
        self._sleep(remaining_seconds)
        self._rate_limit_cooldown_until = 0.0

    def _apply_rate_limit_headers(self, response: requests.Response) -> None:
        """Update local rate-limit state from Billetto's response headers."""
        headers = response.headers or {}
        remaining = _safe_header_int(headers, "X-Ratelimit-Remaining")
        retry_after_ms = _safe_header_int(headers, "X-Ratelimit-Retry-After")

        if response.status_code == 429:
            self._schedule_rate_limit_cooldown(headers, "429 Too Many Requests")
            return

        if remaining is not None and remaining <= 0:
            reason = f"remaining={remaining}"
            if retry_after_ms is not None:
                reason += f", retry_after_ms={retry_after_ms}"
            self._schedule_rate_limit_cooldown(headers, reason)

    def _initial_request_params(self, limit: Optional[int] = None) -> Dict[str, str | int]:
        """Build the upstream query parameters for the first page request."""
        params: Dict[str, str | int] = {"limit": limit or self.page_size}
        params.update(self.api_filters)
        return params

    def fetch_events_page(
        self,
        url: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Tuple[List[dict], Optional[str], bool]:
        """Fetch one page of events from the Billetto API.

        Returns:
            (events, next_url, has_more)
        """
        self._wait_for_rate_limit_cooldown()

        try:
            if url is None:
                response = self._get_session().get(
                    f"{self.base_url}{DEFAULT_EVENTS_PATH}",
                    params=self._initial_request_params(limit=limit),
                    timeout=30,
                )
            else:
                response = self._get_session().get(url, timeout=30)
            self._apply_rate_limit_headers(response)
            if response.status_code == 429:
                logger.warning(
                    "Billetto API returned 429 for %s",
                    url or f"{self.base_url}{DEFAULT_EVENTS_PATH}",
                )
                return [], None, False
            response.raise_for_status()
            body = response.json()
        except requests.exceptions.RequestException as exc:
            logger.error(
                "Error fetching events from %s: %s",
                url or f"{self.base_url}{DEFAULT_EVENTS_PATH}",
                exc,
            )
            return [], None, False
        except (ValueError, KeyError) as exc:
            logger.error(
                "Error parsing API response from %s: %s",
                url or f"{self.base_url}{DEFAULT_EVENTS_PATH}",
                exc,
            )
            return [], None, False

        events = body.get("data", [])
        next_url = body.get("next_url")
        has_more = bool(body.get("has_more", False))
        return events, next_url, has_more

    def fetch_all_events(self) -> List[dict]:
        """Fetch all available events across all pages."""
        all_events: List[dict] = []
        url = None
        page = 0
        while True:
            raw_events, next_url, has_more = self.fetch_events_page(url)
            all_events.extend(raw_events)
            page += 1
            logger.debug("Fetched page %d, %d events (has_more=%s)", page, len(raw_events), has_more)
            if not has_more or not next_url:
                break
            url = next_url
        return all_events

    def load_state(self) -> Dict[str, str]:
        """Load deduplication state from disk."""
        if self.state_file and os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as fh:
                    return json.load(fh)
            except (OSError, ValueError) as exc:
                logger.warning("Could not load state file %s: %s", self.state_file, exc)
        return {}

    def save_state(self, state: Dict[str, str]) -> None:
        """Persist deduplication state to disk."""
        if not self.state_file:
            return
        try:
            state_path = Path(self.state_file)
            state_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = state_path.with_suffix(state_path.suffix + ".tmp")
            with temp_path.open("w", encoding="utf-8") as fh:
                json.dump(state, fh)
            temp_path.replace(state_path)
        except OSError as exc:
            logger.warning("Could not save state file %s: %s", self.state_file, exc)

    def poll_once(self, state: Dict[str, str]) -> Tuple[int, Dict[str, str]]:
        """Run a single poll cycle.

        Fetches all events, emits those with changed content, and returns
        the number of events sent and the pending state updates.

        State is committed only after a successful flush.
        """
        raw_events = self.fetch_all_events()
        if not raw_events:
            logger.info("No events returned from Billetto API")
            return 0, state

        pending_state: Dict[str, str] = {}
        sent = 0

        for raw in raw_events:
            event_id = raw.get("id")
            if event_id is None:
                continue

            key = str(event_id)
            digest = _event_hash(raw)

            if state.get(key) == digest:
                continue

            event = _parse_event(raw)
            if event is None:
                continue

            startdate = event.startdate or datetime.now(timezone.utc).isoformat()

            self.event_producer.send_billetto_events_event(
                _event_id=key,
                _startdate=startdate,
                data=event,
                flush_producer=False,
            )
            pending_state[key] = digest
            sent += 1

        if sent > 0:
            remainder = self.event_producer.producer.flush(timeout=30)
            if remainder != 0:
                logger.error(
                    "Kafka flush returned non-zero remainder (%d); state NOT advanced", remainder
                )
                return 0, state
            # Commit state only after successful delivery
            new_state = dict(state)
            new_state.update(pending_state)
            return sent, new_state

        return 0, state

    def feed(self, polling_interval: int = DEFAULT_POLLING_INTERVAL) -> None:
        """Run the continuous polling loop."""
        state = self.load_state()
        logger.info(
            "Starting Billetto bridge, polling every %d seconds (loaded %d known events)",
            polling_interval,
            len(state),
        )

        while True:
            try:
                sent, new_state = self.poll_once(state)
                if sent > 0:
                    self.save_state(new_state)
                    state = new_state
                logger.info("Poll cycle complete: %d new/updated events sent", sent)
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Unhandled error in polling loop: %s", exc, exc_info=True)
            self._sleep(polling_interval)


def main() -> None:
    """Main entry point for the Billetto bridge."""
    parser = argparse.ArgumentParser(
        description="Poll Billetto public events and publish them as CloudEvents to Kafka.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser(
        "feed",
        help="Continuously poll Billetto and emit event telemetry to Kafka.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    feed_parser.add_argument(
        "--connection-string",
        type=str,
        help="Kafka, Event Hubs, or Fabric connection string. EntityPath becomes the topic unless --topic overrides it.",
    )
    feed_parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="Kafka topic override. Use this only when you do not want the EntityPath from the connection string.",
    )
    feed_parser.add_argument(
        "--polling-interval",
        type=int,
        default=None,
        help="Seconds between Billetto poll cycles.",
    )
    feed_parser.add_argument(
        "--state-file",
        type=str,
        default="",
        help="Path to the JSON file that stores event dedupe state across restarts.",
    )
    feed_parser.add_argument(
        "--api-keypair",
        type=str,
        default=None,
        help="Billetto API keypair in key_id:secret form. Falls back to BILLETTO_API_KEYPAIR.",
    )
    feed_parser.add_argument(
        "--base-url",
        type=str,
        default=None,
        help="Billetto API base URL. Change this when you want a different Billetto domain such as billetto.co.uk.",
    )
    feed_parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Python logging level such as DEBUG, INFO, WARNING, or ERROR.",
    )
    _add_filter_arguments(feed_parser)

    list_parser = subparsers.add_parser(
        "list",
        help="Fetch one page of Billetto events and print a readable summary.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    list_parser.add_argument(
        "--api-keypair",
        type=str,
        default=None,
        help="Billetto API keypair in key_id:secret form. Falls back to BILLETTO_API_KEYPAIR.",
    )
    list_parser.add_argument(
        "--base-url",
        type=str,
        default=None,
        help="Billetto API base URL. Change this when you want a different Billetto domain such as billetto.co.uk.",
    )
    list_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of events to request and print from the first page.",
    )
    _add_filter_arguments(list_parser)

    args = parser.parse_args()

    if args.command == "feed":
        log_level = getattr(logging, (args.log_level or os.environ.get("LOG_LEVEL", "INFO")).upper(), logging.INFO)
        logging.getLogger().setLevel(log_level)

        api_keypair = args.api_keypair or os.environ.get("BILLETTO_API_KEYPAIR", "")
        if not api_keypair:
            logger.error("BILLETTO_API_KEYPAIR environment variable or --api-keypair argument is required")
            sys.exit(1)

        connection_string = args.connection_string or os.environ.get("CONNECTION_STRING", "")
        if not connection_string:
            logger.error("CONNECTION_STRING environment variable or --connection-string argument is required")
            sys.exit(1)

        kafka_config, topic_from_cs = parse_connection_string(connection_string)
        topic = args.topic or topic_from_cs or os.environ.get("KAFKA_TOPIC") or DEFAULT_TOPIC

        polling_interval = args.polling_interval
        if polling_interval is None:
            polling_interval = int(os.environ.get("POLLING_INTERVAL", str(DEFAULT_POLLING_INTERVAL)))

        base_url = args.base_url or os.environ.get("BILLETTO_BASE_URL", DEFAULT_BASE_URL)
        state_file = args.state_file or os.environ.get("STATE_FILE", "")
        api_filters = _resolve_api_filters(args)

        logger.info("Connecting to Kafka topic '%s'", topic)
        poller = BillettoPoller(
            api_keypair=api_keypair,
            base_url=base_url,
            api_filters=api_filters,
            kafka_config=kafka_config,
            kafka_topic=topic,
            state_file=state_file,
        )
        poller.feed(polling_interval=polling_interval)

    elif args.command == "list":
        api_keypair = args.api_keypair or os.environ.get("BILLETTO_API_KEYPAIR", "")
        if not api_keypair:
            logger.error("BILLETTO_API_KEYPAIR environment variable or --api-keypair argument is required")
            sys.exit(1)
        base_url = args.base_url or os.environ.get("BILLETTO_BASE_URL", DEFAULT_BASE_URL)
        api_filters = _resolve_api_filters(args)
        poller = BillettoPoller(api_keypair=api_keypair, base_url=base_url, api_filters=api_filters)
        events, _, _ = poller.fetch_events_page(limit=args.limit)
        print(f"{'ID':<10} {'Title':<50} {'Start':<25} {'City':<20}")
        print("-" * 110)
        for ev in events[:args.limit]:
            loc = ev.get("location") or {}
            print(
                f"{ev.get('id', ''):<10} "
                f"{str(ev.get('title', ''))[:49]:<50} "
                f"{str(ev.get('startdate', '')):<25} "
                f"{str(loc.get('city', ''))[:19]:<20}"
            )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
