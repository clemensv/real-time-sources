"""
Ticketmaster Discovery API bridge to Apache Kafka.

Polls the Ticketmaster Discovery API v2 for upcoming events, venues,
attractions, and classifications, then emits them as CloudEvents to a
Kafka topic using the generated producer wrappers.

Reference data (venues, attractions, classifications) is emitted at
startup and refreshed periodically so downstream consumers can maintain
temporally consistent views of the entities that telemetry (events)
references.
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional, Set, List
from urllib.parse import urlencode

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from confluent_kafka import Producer

from ticketmaster_producer_data import Event, Venue, Attraction, Classification
from ticketmaster_producer_kafka_producer.producer import (
    TicketmasterEventsEventProducer,
    TicketmasterReferenceEventProducer,
)

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

DISCOVERY_API_BASE = "https://app.ticketmaster.com/discovery/v2"


def _load_state(state_file: str) -> Dict[str, str]:
    """Load persisted dedupe state from a JSON file. Returns empty dict on any error."""
    if not state_file:
        return {}
    try:
        if os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def _save_state(state_file: str, data: Dict[str, str]) -> None:
    """Persist dedupe state to a JSON file. Silently ignores errors."""
    if not state_file:
        return
    try:
        state_dir = os.path.dirname(state_file)
        if state_dir:
            os.makedirs(state_dir, exist_ok=True)
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning("Could not save state to %s: %s", state_file, exc)

# Default polling and refresh cadences
DEFAULT_POLL_INTERVAL = 300       # 5 minutes between event polls
DEFAULT_REFERENCE_REFRESH = 3600  # 1 hour between reference-data refreshes
DEFAULT_PAGE_SIZE = 200           # Maximum allowed by the API
DEFAULT_COUNTRY_CODES = "AU,AT,BE,CA,CZ,DK,FI,FR,DE,GR,HU,IE,IT,MX,NL,NZ,NO,PL,PT,ES,SE,CH,GB,US"


def _make_session() -> requests.Session:
    """Create a requests session with bounded retry policy for transient failures."""
    session = requests.Session()
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


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse a Kafka connection string (Event Hubs or plain bootstrap format).

    Args:
        connection_string: The connection string.

    Returns:
        Dict with extracted Kafka configuration parameters.
    """
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=", 1)[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=", 1)[1].strip('"')
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = "$ConnectionString"
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = connection_string.strip()
            elif "BootstrapServer" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanisms"] = "PLAIN"
    return config_dict


def _first_classification(classifications: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract the first non-undefined classification segment/genre/subgenre from a list."""
    for clf in classifications:
        segment = clf.get("segment", {})
        genre = clf.get("primaryGenre", {})
        subgenre = clf.get("primarySubGenre", {})
        if segment:
            return {
                "segment_id": segment.get("id"),
                "segment_name": segment.get("name"),
                "genre_id": genre.get("id"),
                "genre_name": genre.get("name"),
                "subgenre_id": subgenre.get("id"),
                "subgenre_name": subgenre.get("name"),
            }
    return {}


def _parse_event(raw: Dict[str, Any]) -> Optional[Event]:
    """Parse a raw Ticketmaster API event dict into an Event data class."""
    event_id = raw.get("id", "")
    name = raw.get("name", "")
    if not event_id or not name:
        return None

    dates = raw.get("dates", {})
    start = dates.get("start", {})
    status_obj = dates.get("status", {})

    classifications = raw.get("classifications", [])
    clf = _first_classification(classifications)

    embedded = raw.get("_embedded", {})
    venues = embedded.get("venues", [])
    venue = venues[0] if venues else {}
    location = venue.get("location", {})

    attractions = embedded.get("attractions", [])
    attraction_ids = json.dumps([a.get("id") for a in attractions if a.get("id")])
    attraction_names = json.dumps([a.get("name") for a in attractions if a.get("name")])

    price_ranges = raw.get("priceRanges", [])
    price_min = None
    price_max = None
    currency = None
    if price_ranges:
        price_min = price_ranges[0].get("min")
        price_max = price_ranges[0].get("max")
        currency = price_ranges[0].get("currency")

    sales = raw.get("sales", {})
    public_sales = sales.get("public", {})

    start_utc: Optional[str] = start.get("dateTime")

    return Event(
        event_id=event_id,
        name=name,
        type=raw.get("type"),
        url=raw.get("url"),
        locale=raw.get("locale"),
        start_date=start.get("localDate"),
        start_time=start.get("localTime"),
        start_datetime_local=(
            (start["localDate"] + "T" + start["localTime"])
            if start.get("localDate") and start.get("localTime")
            else start.get("localDate")
        ),
        start_datetime_utc=start_utc,
        status=status_obj.get("code"),
        segment_id=clf.get("segment_id"),
        segment_name=clf.get("segment_name"),
        genre_id=clf.get("genre_id"),
        genre_name=clf.get("genre_name"),
        subgenre_id=clf.get("subgenre_id"),
        subgenre_name=clf.get("subgenre_name"),
        venue_id=venue.get("id"),
        venue_name=venue.get("name"),
        venue_city=(venue.get("city") or {}).get("name"),
        venue_state_code=(venue.get("state") or {}).get("stateCode"),
        venue_country_code=(venue.get("country") or {}).get("countryCode"),
        venue_latitude=(
            float(location["latitude"]) if location.get("latitude") else None
        ),
        venue_longitude=(
            float(location["longitude"]) if location.get("longitude") else None
        ),
        price_min=price_min,
        price_max=price_max,
        currency=currency,
        attraction_ids=attraction_ids if attraction_ids != "[]" else None,
        attraction_names=attraction_names if attraction_names != "[]" else None,
        onsale_start_datetime=public_sales.get("startDateTime"),
        onsale_end_datetime=public_sales.get("endDateTime"),
        info=raw.get("info"),
        please_note=raw.get("pleaseNote"),
    )


def _parse_venue(raw: Dict[str, Any]) -> Optional[Venue]:
    """Parse a raw Ticketmaster API venue dict into a Venue data class."""
    venue_id = raw.get("id", "")
    name = raw.get("name", "")
    if not venue_id or not name:
        return None
    location = raw.get("location", {})
    return Venue(
        entity_id=venue_id,
        name=name,
        url=raw.get("url"),
        locale=raw.get("locale"),
        timezone=raw.get("timezone"),
        city=(raw.get("city") or {}).get("name"),
        state_code=(raw.get("state") or {}).get("stateCode"),
        country_code=(raw.get("country") or {}).get("countryCode"),
        address=(raw.get("address") or {}).get("line1"),
        postal_code=raw.get("postalCode"),
        latitude=float(location["latitude"]) if location.get("latitude") else None,
        longitude=float(location["longitude"]) if location.get("longitude") else None,
    )


def _parse_attraction(raw: Dict[str, Any]) -> Optional[Attraction]:
    """Parse a raw Ticketmaster API attraction dict into an Attraction data class."""
    attraction_id = raw.get("id", "")
    name = raw.get("name", "")
    if not attraction_id or not name:
        return None
    classifications = raw.get("classifications", [])
    clf = _first_classification(classifications)
    return Attraction(
        entity_id=attraction_id,
        name=name,
        url=raw.get("url"),
        locale=raw.get("locale"),
        segment_id=clf.get("segment_id"),
        segment_name=clf.get("segment_name"),
        genre_id=clf.get("genre_id"),
        genre_name=clf.get("genre_name"),
        subgenre_id=clf.get("subgenre_id"),
        subgenre_name=clf.get("subgenre_name"),
    )


def _parse_classification(raw: Dict[str, Any]) -> Optional[Classification]:
    """Parse a raw Ticketmaster API classification dict into a Classification data class."""
    segment = raw.get("segment", {})
    segment_id = segment.get("id", "")
    segment_name = segment.get("name", "")
    if not segment_id or not segment_name:
        return None
    primary_genre = raw.get("primaryGenre", {})
    primary_subgenre = raw.get("primarySubGenre", {})
    return Classification(
        entity_id=segment_id,
        name=segment_name,
        type=raw.get("type"),
        primary_genre_id=primary_genre.get("id"),
        primary_genre_name=primary_genre.get("name"),
        primary_subgenre_id=primary_subgenre.get("id"),
        primary_subgenre_name=primary_subgenre.get("name"),
    )


class TicketmasterBridge:
    """
    Polls the Ticketmaster Discovery API and emits CloudEvents to Kafka.

    Reference data (venues, attractions, classifications) is emitted at
    startup and refreshed every `reference_refresh_interval` seconds.
    Event telemetry is polled every `poll_interval` seconds.
    """

    def __init__(
        self,
        api_key: str,
        events_producer: Optional[TicketmasterEventsEventProducer] = None,
        reference_producer: Optional[TicketmasterReferenceEventProducer] = None,
        poll_interval: int = DEFAULT_POLL_INTERVAL,
        reference_refresh_interval: int = DEFAULT_REFERENCE_REFRESH,
        country_codes: str = DEFAULT_COUNTRY_CODES,
        page_size: int = DEFAULT_PAGE_SIZE,
        state_file: str = "",
    ) -> None:
        self.api_key = api_key
        self.events_producer = events_producer
        self.reference_producer = reference_producer
        self.poll_interval = poll_interval
        self.reference_refresh_interval = reference_refresh_interval
        self.country_codes = country_codes
        self.page_size = page_size
        self.state_file = state_file
        self._session = _make_session()

        # Dedupe state: event_id → dedup key (event_id:status); persisted to state_file
        self._seen_events: Dict[str, str] = _load_state(state_file)
        logger.info(
            "Loaded %d seen-event entries from state file: %s",
            len(self._seen_events),
            state_file or "(none — in-memory only)",
        )
        # Reference caches (entity_id → data object); kept across failed refreshes
        self._venue_cache: Dict[str, Venue] = {}
        self._attraction_cache: Dict[str, Attraction] = {}
        self._classification_cache: Dict[str, Classification] = {}
        self._last_reference_refresh: Optional[datetime] = None

    # ------------------------------------------------------------------
    # HTTP helpers
    # ------------------------------------------------------------------

    def _get(self, path: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Issue a GET request to the Discovery API and return the parsed JSON."""
        params = {**params, "apikey": self.api_key}
        url = f"{DISCOVERY_API_BASE}/{path}"
        try:
            resp = self._session.get(url, params=params, timeout=30)
            if resp.status_code == 429:
                logger.warning("Rate limited by Ticketmaster API; backing off 60s")
                time.sleep(60)
                resp = self._session.get(url, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.error("HTTP error for %s: %s", path, exc)
            return None

    def _paginate(self, path: str, params: Dict[str, Any], key: str) -> List[Dict[str, Any]]:
        """
        Collect all pages from a paginated Discovery API endpoint.

        Respects the API rate limit by sleeping between pages when needed.
        """
        results: List[Dict[str, Any]] = []
        page = 0
        while True:
            data = self._get(path, {**params, "page": page, "size": self.page_size})
            if data is None:
                break
            embedded = data.get("_embedded", {})
            items = embedded.get(key, [])
            results.extend(items)

            page_info = data.get("page", {})
            total_pages = page_info.get("totalPages", 1)
            if page >= total_pages - 1 or not items:
                break
            page += 1
            # Stay within 5 req/s rate limit
            time.sleep(0.25)
        return results

    # ------------------------------------------------------------------
    # Reference data
    # ------------------------------------------------------------------

    def fetch_classifications(self) -> Dict[str, Classification]:
        """Fetch all classification segments from the Discovery API."""
        raw_list = self._paginate("classifications.json", {}, "classifications")
        result: Dict[str, Classification] = {}
        for raw in raw_list:
            clf = _parse_classification(raw)
            if clf:
                result[clf.entity_id] = clf
        return result

    def fetch_venues_for_country(self, country_code: str) -> Dict[str, Venue]:
        """Fetch venues for a single country code."""
        raw_list = self._paginate(
            "venues.json", {"countryCode": country_code, "locale": "*"}, "venues"
        )
        result: Dict[str, Venue] = {}
        for raw in raw_list:
            venue = _parse_venue(raw)
            if venue:
                result[venue.entity_id] = venue
        return result

    def fetch_attractions_for_country(self, country_code: str) -> Dict[str, Attraction]:
        """Fetch attractions for a single country code."""
        raw_list = self._paginate(
            "attractions.json", {"countryCode": country_code, "locale": "*"}, "attractions"
        )
        result: Dict[str, Attraction] = {}
        for raw in raw_list:
            attr = _parse_attraction(raw)
            if attr:
                result[attr.entity_id] = attr
        return result

    def emit_classifications(self, classifications: Dict[str, Classification]) -> int:
        """Emit classification reference events. Returns count emitted."""
        if not self.reference_producer:
            return 0
        count = 0
        for clf in classifications.values():
            self.reference_producer.send_ticketmaster_reference_classification(
                _entity_id=clf.entity_id,
                data=clf,
                flush_producer=False,
            )
            count += 1
        return count

    def emit_venues(self, venues: Dict[str, Venue]) -> int:
        """Emit venue reference events. Returns count emitted."""
        if not self.reference_producer:
            return 0
        count = 0
        for venue in venues.values():
            self.reference_producer.send_ticketmaster_reference_venue(
                _entity_id=venue.entity_id,
                data=venue,
                flush_producer=False,
            )
            count += 1
        return count

    def emit_attractions(self, attractions: Dict[str, Attraction]) -> int:
        """Emit attraction reference events. Returns count emitted."""
        if not self.reference_producer:
            return 0
        count = 0
        for attr in attractions.values():
            self.reference_producer.send_ticketmaster_reference_attraction(
                _entity_id=attr.entity_id,
                data=attr,
                flush_producer=False,
            )
            count += 1
        return count

    def refresh_reference_data(self) -> None:
        """
        Fetch and emit all reference data (classifications, venues, attractions).

        Builds fresh caches separately and swaps them in only after a successful
        fetch, so a failed refresh never discards a still-usable prior cache.
        """
        logger.info("Refreshing reference data (classifications, venues, attractions)…")

        # --- Classifications (fast: only ~20 records) ---
        try:
            new_classifications = self.fetch_classifications()
            if new_classifications:
                count = self.emit_classifications(new_classifications)
                self._classification_cache = new_classifications
                logger.info("Emitted %d classification reference events", count)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Classification refresh failed: %s; keeping prior cache", exc)

        # --- Venues and attractions per country (isolate per-country failures) ---
        new_venues: Dict[str, Venue] = {}
        new_attractions: Dict[str, Attraction] = {}

        for country_code in [c.strip() for c in self.country_codes.split(",") if c.strip()]:
            try:
                venues = self.fetch_venues_for_country(country_code)
                new_venues.update(venues)
            except Exception as exc:  # pylint: disable=broad-except
                logger.warning("Venue fetch failed for %s: %s; skipping country", country_code, exc)

            try:
                attractions = self.fetch_attractions_for_country(country_code)
                new_attractions.update(attractions)
            except Exception as exc:  # pylint: disable=broad-except
                logger.warning(
                    "Attraction fetch failed for %s: %s; skipping country", country_code, exc
                )
            # Respect rate limits between countries
            time.sleep(0.5)

        if new_venues:
            count = self.emit_venues(new_venues)
            self._venue_cache = new_venues
            logger.info("Emitted %d venue reference events", count)
        elif self._venue_cache:
            logger.warning("Venue refresh returned no results; keeping prior cache (%d entries)", len(self._venue_cache))

        if new_attractions:
            count = self.emit_attractions(new_attractions)
            self._attraction_cache = new_attractions
            logger.info("Emitted %d attraction reference events", count)
        elif self._attraction_cache:
            logger.warning(
                "Attraction refresh returned no results; keeping prior cache (%d entries)",
                len(self._attraction_cache),
            )

        # Flush after entire reference batch
        if self.reference_producer:
            remaining = self.reference_producer.producer.flush(timeout=60)
            if remaining > 0:
                logger.error(
                    "Kafka flush after reference refresh left %d messages undelivered", remaining
                )
            else:
                self._last_reference_refresh = datetime.now(timezone.utc)

    # ------------------------------------------------------------------
    # Event telemetry
    # ------------------------------------------------------------------

    def fetch_events_for_country(
        self, country_code: str, start_datetime: str, end_datetime: str
    ) -> List[Dict[str, Any]]:
        """Fetch all upcoming events for one country in the given time window."""
        return self._paginate(
            "events.json",
            {
                "countryCode": country_code,
                "startDateTime": start_datetime,
                "endDateTime": end_datetime,
                "locale": "*",
                "sort": "date,asc",
            },
            "events",
        )

    def poll_events(self) -> None:
        """
        Poll upcoming events for all configured country codes and emit new or
        updated events as CloudEvents.

        Deduplicate by event_id + status to avoid re-emitting unchanged records.
        Advance dedupe state only after a successful Kafka flush.
        """
        if not self.events_producer:
            return

        now_utc = datetime.now(timezone.utc)
        # Look ahead 90 days
        start_dt = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_dt = (now_utc + timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")

        pending_state: Dict[str, str] = {}
        count_new = 0
        count_updated = 0

        for country_code in [c.strip() for c in self.country_codes.split(",") if c.strip()]:
            try:
                raw_events = self.fetch_events_for_country(country_code, start_dt, end_dt)
            except Exception as exc:  # pylint: disable=broad-except
                logger.warning("Event fetch failed for %s: %s; skipping", country_code, exc)
                continue

            for raw in raw_events:
                event = _parse_event(raw)
                if event is None:
                    continue

                # Deduplicate by event_id + status (status changes are meaningful)
                dedup_key = f"{event.event_id}:{event.status}"
                if self._seen_events.get(event.event_id) == dedup_key:
                    continue

                if event.event_id not in self._seen_events:
                    count_new += 1
                else:
                    count_updated += 1

                # Use UTC datetime as time attribute; fall back to current time
                time_attr = event.start_datetime_utc or now_utc.isoformat()

                self.events_producer.send_ticketmaster_events_event(
                    _event_id=event.event_id,
                    _start_datetime_utc=time_attr,
                    data=event,
                    flush_producer=False,
                )
                pending_state[event.event_id] = dedup_key

            # Rate limit between countries
            time.sleep(0.5)

        # Flush and only advance state after successful delivery
        remaining = self.events_producer.producer.flush(timeout=60)
        if remaining > 0:
            logger.error(
                "Kafka flush left %d event messages undelivered; dedupe state not advanced",
                remaining,
            )
            return

        self._seen_events.update(pending_state)
        # Trim state: keep only events whose ID we emitted in this or previous cycles
        # Prune events not seen in the last 90 days (approximate via state size cap)
        if len(self._seen_events) > 100_000:
            # Keep the most recently added entries
            excess = len(self._seen_events) - 80_000
            keys_to_remove = list(self._seen_events.keys())[:excess]
            for k in keys_to_remove:
                del self._seen_events[k]

        _save_state(self.state_file, self._seen_events)

        if count_new > 0 or count_updated > 0:
            logger.info(
                "Emitted %d new and %d updated event telemetry records",
                count_new,
                count_updated,
            )
        else:
            logger.debug("No new or updated events found")

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self) -> None:
        """
        Main bridge loop: emit reference data at startup then poll events
        continuously, refreshing reference data every `reference_refresh_interval`.
        """
        logger.info(
            "Starting Ticketmaster bridge; countries=%s poll_interval=%ds ref_refresh=%ds",
            self.country_codes,
            self.poll_interval,
            self.reference_refresh_interval,
        )

        # Emit reference data first
        self.refresh_reference_data()

        while True:
            cycle_start = time.monotonic()

            # Refresh reference data periodically
            if self._last_reference_refresh is None or (
                datetime.now(timezone.utc) - self._last_reference_refresh
                >= timedelta(seconds=self.reference_refresh_interval)
            ):
                self.refresh_reference_data()

            # Poll event telemetry
            self.poll_events()

            elapsed = time.monotonic() - cycle_start
            sleep_time = max(0, self.poll_interval - elapsed)
            logger.debug("Cycle complete in %.1fs; sleeping %.1fs", elapsed, sleep_time)
            if sleep_time > 0:
                time.sleep(sleep_time)


def main() -> None:
    """Parse arguments and start the Ticketmaster bridge."""
    parser = argparse.ArgumentParser(description="Ticketmaster Discovery API to Kafka bridge")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    feed_parser = subparsers.add_parser("feed", help="Poll Ticketmaster and stream to Kafka")
    feed_parser.add_argument("--connection-string", type=str,
                             help="Kafka/Event Hubs/Fabric connection string")
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str,
                             help="Kafka bootstrap server(s)")
    feed_parser.add_argument("--kafka-topic", type=str,
                             help="Kafka topic name")
    feed_parser.add_argument("--sasl-username", type=str, help="SASL username")
    feed_parser.add_argument("--sasl-password", type=str, help="SASL password")
    feed_parser.add_argument("--api-key", type=str,
                             help="Ticketmaster Discovery API key")
    feed_parser.add_argument("--country-codes", type=str, default=DEFAULT_COUNTRY_CODES,
                             help="Comma-separated ISO 3166-1 alpha-2 country codes to poll")
    feed_parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL,
                             help=f"Seconds between event polls (default: {DEFAULT_POLL_INTERVAL})")
    feed_parser.add_argument("--reference-refresh", type=int, default=DEFAULT_REFERENCE_REFRESH,
                             help=f"Seconds between reference-data refreshes (default: {DEFAULT_REFERENCE_REFRESH})")
    feed_parser.add_argument("--log-level", type=str, default="INFO",
                             help="Logging level (default: INFO)")
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.ticketmaster_state.json")),
                             help="Path to JSON file for persisting dedupe state across restarts "
                                  "(default: ~/.ticketmaster_state.json; set STATE_FILE env var to override)")

    args = parser.parse_args()

    if args.subcommand == "feed":
        # Resolve configuration from args and environment
        connection_string = args.connection_string or os.getenv("CONNECTION_STRING")
        api_key = args.api_key or os.getenv("TICKETMASTER_API_KEY")
        country_codes = args.country_codes or os.getenv("COUNTRY_CODES", DEFAULT_COUNTRY_CODES)
        poll_interval = int(os.getenv("POLL_INTERVAL", str(args.poll_interval)))
        reference_refresh = int(os.getenv("REFERENCE_REFRESH", str(args.reference_refresh)))
        state_file = args.state_file or os.getenv("STATE_FILE", os.path.expanduser("~/.ticketmaster_state.json"))

        log_level = os.getenv("LOG_LEVEL", args.log_level)
        logging.getLogger().setLevel(log_level)

        if not api_key:
            print("Error: TICKETMASTER_API_KEY environment variable or --api-key argument is required.")
            sys.exit(1)

        if connection_string:
            config_params = parse_connection_string(connection_string)
            kafka_bootstrap_servers = config_params.get("bootstrap.servers")
            kafka_topic = config_params.get("kafka_topic")
            sasl_username = config_params.get("sasl.username")
            sasl_password = config_params.get("sasl.password")
        else:
            kafka_bootstrap_servers = args.kafka_bootstrap_servers or os.getenv("KAFKA_BOOTSTRAP_SERVERS")
            kafka_topic = args.kafka_topic or os.getenv("KAFKA_TOPIC")
            sasl_username = args.sasl_username or os.getenv("KAFKA_SASL_USERNAME")
            sasl_password = args.sasl_password or os.getenv("KAFKA_SASL_PASSWORD")

        if not kafka_bootstrap_servers:
            print("Error: Kafka bootstrap servers must be provided.")
            sys.exit(1)
        if not kafka_topic:
            print("Error: Kafka topic must be provided.")
            sys.exit(1)

        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        kafka_config: Dict[str, str] = {"bootstrap.servers": kafka_bootstrap_servers}
        if sasl_username and sasl_password:
            kafka_config.update({
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_username,
                "sasl.password": sasl_password,
            })
        elif tls_enabled:
            kafka_config["security.protocol"] = "SSL"

        kafka_producer = Producer(kafka_config)
        events_producer = TicketmasterEventsEventProducer(kafka_producer, kafka_topic)
        reference_producer = TicketmasterReferenceEventProducer(kafka_producer, kafka_topic)

        bridge = TicketmasterBridge(
            api_key=api_key,
            events_producer=events_producer,
            reference_producer=reference_producer,
            poll_interval=poll_interval,
            reference_refresh_interval=reference_refresh,
            country_codes=country_codes,
            state_file=state_file,
        )
        bridge.run()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
