"""
TfL Road Traffic Bridge

Polls the Transport for London (TfL) Unified API for road corridor status
and disruption data, emitting CloudEvents to Kafka.

Endpoints used:
  GET https://api.tfl.gov.uk/Road              - corridor catalog (reference)
  GET https://api.tfl.gov.uk/Road/all/Status   - corridor status (telemetry)
  GET https://api.tfl.gov.uk/Road/all/Disruption - disruption telemetry
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from tfl_road_traffic_producer_data import RoadCorridor, RoadStatus, RoadDisruption
from tfl_road_traffic_producer_kafka_producer.producer import (
    UkGovTflRoadCorridorsEventProducer,
    UkGovTflRoadDisruptionsEventProducer,
)

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

TFL_ROAD_URL = "https://api.tfl.gov.uk/Road"
TFL_STATUS_URL = "https://api.tfl.gov.uk/Road/all/Status"
TFL_DISRUPTION_URL = "https://api.tfl.gov.uk/Road/all/Disruption"


def _make_session() -> requests.Session:
    """Create a requests session with bounded retry logic for transient upstream failures."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse an Azure Event Hubs-style or plain Kafka connection string.

    Supports:
        - BootstrapServer=host:port;EntityPath=topic
        - Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=...

    Args:
        connection_string: The connection string.

    Returns:
        Dict with bootstrap.servers, kafka_topic, and optional SASL params.
    """
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = (
                    part.split('=', 1)[1].strip('"')
                    .replace('sb://', '')
                    .replace('/', '') + ':9093'
                )
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=', 1)[1].strip('"')
            elif 'SharedAccessKeyName' in part:
                config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part:
                config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc
    if 'sasl.username' in config_dict:
        config_dict['security.protocol'] = 'SASL_SSL'
        config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    """Parse an ISO 8601 datetime string, handling Z suffix."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (ValueError, TypeError):
        logger.debug("Could not parse datetime: %s", value)
        return None


def _serialize_geo(value: Any) -> Optional[str]:
    """Serialize a geography/geometry value to a JSON string if it is a dict or list."""
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return str(value)


def build_road_corridor(raw: dict) -> Optional[RoadCorridor]:
    """
    Build a RoadCorridor data class from a raw TfL /Road API response dict.

    Maps upstream camelCase field names to English schema field names.

    Args:
        raw: Dict from the TfL /Road endpoint.

    Returns:
        RoadCorridor instance, or None if road_id is missing.
    """
    road_id = raw.get('id')
    display_name = raw.get('displayName')
    if not road_id or not display_name:
        return None
    return RoadCorridor(
        road_id=road_id,
        display_name=display_name,
        status_severity=raw.get('statusSeverity') or None,
        status_severity_description=raw.get('statusSeverityDescription') or None,
        bounds=raw.get('bounds') or None,
        envelope=raw.get('envelope') or None,
        url=raw.get('url') or None,
        status_aggregation_start_date=_parse_dt(raw.get('statusAggregationStartDate')),
        status_aggregation_end_date=_parse_dt(raw.get('statusAggregationEndDate')),
    )


def build_road_status(raw: dict) -> Optional[RoadStatus]:
    """
    Build a RoadStatus data class from a raw TfL /Road/all/Status API response dict.

    Maps upstream camelCase field names to English schema field names.

    Args:
        raw: Dict from the TfL /Road/all/Status endpoint.

    Returns:
        RoadStatus instance, or None if road_id is missing.
    """
    road_id = raw.get('id')
    display_name = raw.get('displayName')
    if not road_id or not display_name:
        return None
    return RoadStatus(
        road_id=road_id,
        display_name=display_name,
        status_severity=raw.get('statusSeverity') or None,
        status_severity_description=raw.get('statusSeverityDescription') or None,
        bounds=raw.get('bounds') or None,
        envelope=raw.get('envelope') or None,
        url=raw.get('url') or None,
        status_aggregation_start_date=_parse_dt(raw.get('statusAggregationStartDate')),
        status_aggregation_end_date=_parse_dt(raw.get('statusAggregationEndDate')),
    )


def build_street(raw: dict) -> dict:
    """
    Build a street dict from a raw TfL streets array entry.

    Maps upstream camelCase field names to English schema field names.
    Returns a plain dict since the generated streets field is typing.Any.

    Args:
        raw: Dict from the upstream streets array.

    Returns:
        Dict with English field names.
    """
    return {
        'name': raw.get('name') or None,
        'closure': raw.get('closure') or None,
        'directions': raw.get('directions') or None,
        'source_system_id': raw.get('sourceSystemId') or None,
        'source_system_key': raw.get('sourceSystemKey') or None,
    }


def build_road_disruption(raw: dict) -> Optional[RoadDisruption]:
    """
    Build a RoadDisruption data class from a raw TfL /Road/all/Disruption API response dict.

    Maps upstream camelCase field names to English schema field names.

    Args:
        raw: Dict from the TfL /Road/all/Disruption endpoint.

    Returns:
        RoadDisruption instance, or None if disruption_id is missing.
    """
    disruption_id = raw.get('id')
    if not disruption_id:
        return None

    raw_streets = raw.get('streets')
    streets = [build_street(s) for s in raw_streets] if isinstance(raw_streets, list) else None

    return RoadDisruption(
        disruption_id=disruption_id,
        category=raw.get('category') or None,
        sub_category=raw.get('subCategory') or None,
        severity=raw.get('severity') or None,
        ordinal=raw.get('ordinal'),
        url=raw.get('url') or None,
        point=raw.get('point') or None,
        comments=raw.get('comments') or None,
        current_update=raw.get('currentUpdate') or None,
        current_update_datetime=_parse_dt(raw.get('currentUpdateDateTime')),
        corridor_ids=raw.get('corridorIds') or None,
        start_datetime=_parse_dt(raw.get('startDateTime')),
        end_datetime=_parse_dt(raw.get('endDateTime')),
        last_modified_time=_parse_dt(raw.get('lastModifiedTime')),
        level_of_interest=raw.get('levelOfInterest') or None,
        location=raw.get('location') or None,
        is_provisional=raw.get('isProvisional'),
        has_closures=raw.get('hasClosures'),
        streets=streets,
        geography=_serialize_geo(raw.get('geography')),
        geometry=_serialize_geo(raw.get('geometry')),
        status=raw.get('status') or None,
        is_active=raw.get('isActive'),
    )


class TflRoadTrafficPoller:
    """
    Polls the TfL Unified API and emits CloudEvents for road corridors and disruptions.

    Uses two separate generated producer classes sharing one Kafka Producer instance.
    Reference data (corridors) is emitted at startup and refreshed periodically.
    Disruptions are deduped by id+lastModifiedTime.
    """

    def __init__(
        self,
        kafka_config: Dict[str, str],
        kafka_topic: str,
        polling_interval: int = 60,
        reference_refresh_interval: int = 3600,
        session: Optional[requests.Session] = None,
    ):
        """
        Initialize the poller.

        Args:
            kafka_config: Confluent Kafka producer config dict.
            kafka_topic: Kafka topic to send all events to.
            polling_interval: Seconds between telemetry poll cycles.
            reference_refresh_interval: Seconds between reference data refreshes.
            session: Optional requests.Session (injected for testing).
        """
        from confluent_kafka import Producer as KafkaProducer
        self.kafka_topic = kafka_topic
        self.polling_interval = polling_interval
        self.reference_refresh_interval = reference_refresh_interval
        self.session = session or _make_session()

        self._kafka_producer = KafkaProducer(kafka_config)
        self.corridors_producer = UkGovTflRoadCorridorsEventProducer(
            self._kafka_producer, kafka_topic
        )
        self.disruptions_producer = UkGovTflRoadDisruptionsEventProducer(
            self._kafka_producer, kafka_topic
        )

        self._seen_disruptions: Dict[str, str] = {}
        self._last_reference_time: float = 0.0
        self._cached_corridors: Optional[List[dict]] = None

    def _fetch_json(self, url: str) -> Optional[Any]:
        """Fetch JSON from a URL, returning None on any error."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            logger.warning("Failed to fetch %s: %s", url, exc)
            return None

    def fetch_corridors(self) -> Optional[List[dict]]:
        """Fetch road corridor reference data from GET /Road."""
        data = self._fetch_json(TFL_ROAD_URL)
        if data is None:
            return None
        if isinstance(data, list):
            return data
        logger.warning("Unexpected /Road response type: %s", type(data))
        return None

    def fetch_statuses(self) -> Optional[List[dict]]:
        """Fetch road status telemetry from GET /Road/all/Status."""
        data = self._fetch_json(TFL_STATUS_URL)
        if data is None:
            return None
        if isinstance(data, list):
            return data
        logger.warning("Unexpected /Road/all/Status response type: %s", type(data))
        return None

    def fetch_disruptions(self) -> Optional[List[dict]]:
        """Fetch road disruption telemetry from GET /Road/all/Disruption."""
        data = self._fetch_json(TFL_DISRUPTION_URL)
        if data is None:
            return None
        if isinstance(data, list):
            return data
        logger.warning("Unexpected /Road/all/Disruption response type: %s", type(data))
        return None

    def emit_reference_data(self, raw_corridors: List[dict]) -> int:
        """
        Emit RoadCorridor reference events for all corridors.

        Sends all events with flush_producer=False then flushes once.
        Emits nothing and returns 0 if flush fails.

        Args:
            raw_corridors: List of raw corridor dicts from the TfL /Road endpoint.

        Returns:
            Number of reference events emitted, or 0 on flush failure.
        """
        events_sent = 0
        for raw in raw_corridors:
            corridor = build_road_corridor(raw)
            if corridor is None:
                continue
            self.corridors_producer.send_uk_gov_tfl_road_road_corridor(
                corridor.road_id, corridor, flush_producer=False
            )
            events_sent += 1

        if events_sent > 0:
            remaining = self._kafka_producer.flush(timeout=30)
            if remaining != 0:
                logger.error(
                    "Flush failed for reference data: %d messages undelivered", remaining
                )
                return 0

        logger.info("Emitted %d RoadCorridor reference events", events_sent)
        return events_sent

    def emit_status_data(self, raw_statuses: List[dict]) -> int:
        """
        Emit RoadStatus telemetry events for all corridors.

        Sends all events with flush_producer=False then flushes once.
        Returns 0 if flush fails.

        Args:
            raw_statuses: List of raw status dicts from the TfL /Road/all/Status endpoint.

        Returns:
            Number of telemetry events emitted, or 0 on flush failure.
        """
        events_sent = 0
        for raw in raw_statuses:
            status = build_road_status(raw)
            if status is None:
                continue
            self.corridors_producer.send_uk_gov_tfl_road_road_status(
                status.road_id, status, flush_producer=False
            )
            events_sent += 1

        if events_sent > 0:
            remaining = self._kafka_producer.flush(timeout=30)
            if remaining != 0:
                logger.error(
                    "Flush failed for status data: %d messages undelivered", remaining
                )
                return 0

        logger.info("Emitted %d RoadStatus telemetry events", events_sent)
        return events_sent

    def emit_disruption_data(self, raw_disruptions: List[dict]) -> int:
        """
        Emit RoadDisruption telemetry events for new or changed disruptions.

        Disruptions are deduped by id + lastModifiedTime. State is only advanced
        after a successful flush (flush returns 0).

        Args:
            raw_disruptions: List of raw disruption dicts from /Road/all/Disruption.

        Returns:
            Number of disruption events emitted this cycle, or 0 on flush failure.
        """
        to_emit: List[RoadDisruption] = []
        candidate_state: Dict[str, str] = {}

        for raw in raw_disruptions:
            disruption_id = raw.get('id')
            if not disruption_id:
                continue
            last_modified = raw.get('lastModifiedTime', '')
            seen_key = self._seen_disruptions.get(disruption_id)
            if seen_key == last_modified:
                continue

            disruption = build_road_disruption(raw)
            if disruption is None:
                continue
            to_emit.append(disruption)
            candidate_state[disruption_id] = last_modified

        if not to_emit:
            return 0

        for disruption in to_emit:
            self.disruptions_producer.send_uk_gov_tfl_road_road_disruption(
                disruption.disruption_id, disruption, flush_producer=False
            )

        remaining = self._kafka_producer.flush(timeout=30)
        if remaining != 0:
            logger.error(
                "Flush failed for disruption data: %d messages undelivered", remaining
            )
            return 0

        self._seen_disruptions.update(candidate_state)
        logger.info("Emitted %d RoadDisruption telemetry events", len(to_emit))
        return len(to_emit)

    def poll_and_send(self) -> None:
        """
        Main polling loop.

        Emits reference data first at startup (and periodically), then fetches
        status and disruption telemetry on every cycle.
        """
        logger.info("TfL Road Traffic poller starting (interval=%ds)", self.polling_interval)
        while True:
            now = time.monotonic()
            reference_due = (now - self._last_reference_time) >= self.reference_refresh_interval

            if reference_due:
                raw_corridors = self.fetch_corridors()
                if raw_corridors is not None:
                    self._cached_corridors = raw_corridors
                    self.emit_reference_data(raw_corridors)
                    self._last_reference_time = time.monotonic()
                elif self._cached_corridors is not None:
                    logger.warning(
                        "Reference refresh failed; keeping %d cached corridors",
                        len(self._cached_corridors),
                    )
                else:
                    logger.warning("Reference fetch failed and no cache available")

            raw_statuses = self.fetch_statuses()
            if raw_statuses is not None:
                self.emit_status_data(raw_statuses)
            else:
                logger.warning("Status fetch failed; skipping status emit this cycle")

            raw_disruptions = self.fetch_disruptions()
            if raw_disruptions is not None:
                self.emit_disruption_data(raw_disruptions)
            else:
                logger.warning("Disruption fetch failed; skipping disruption emit this cycle")

            logger.debug("Sleeping %ds until next poll", self.polling_interval)
            time.sleep(self.polling_interval)


def main() -> None:
    """Entry point for the TfL Road Traffic bridge."""
    parser = argparse.ArgumentParser(
        description="Transport for London (TfL) Road Traffic bridge to Kafka"
    )
    subparsers = parser.add_subparsers(dest='command')
    feed_parser = subparsers.add_parser('feed', help='Run the polling bridge')
    feed_parser.add_argument(
        '--connection-string',
        type=str,
        help="Kafka connection string (BootstrapServer=... or Azure Event Hubs format)",
    )
    feed_parser.add_argument(
        '--kafka-bootstrap-servers',
        type=str,
        help="Comma-separated list of Kafka bootstrap servers",
    )
    feed_parser.add_argument(
        '--kafka-topic',
        type=str,
        default='tfl-road-traffic',
        help="Kafka topic to send events to (default: tfl-road-traffic)",
    )
    feed_parser.add_argument(
        '--sasl-username',
        type=str,
        help="SASL username for Kafka authentication",
    )
    feed_parser.add_argument(
        '--sasl-password',
        type=str,
        help="SASL password for Kafka authentication",
    )

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)

    connection_string = args.connection_string or os.getenv('CONNECTION_STRING')
    enable_tls = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
    polling_interval = int(os.getenv('POLLING_INTERVAL', '60'))
    reference_refresh_interval = int(os.getenv('REFERENCE_REFRESH_INTERVAL', '3600'))

    kafka_topic = args.kafka_topic
    kafka_bootstrap_servers = args.kafka_bootstrap_servers
    sasl_username = args.sasl_username
    sasl_password = args.sasl_password

    if connection_string:
        config_params = parse_connection_string(connection_string)
        kafka_bootstrap_servers = config_params.get('bootstrap.servers', kafka_bootstrap_servers)
        kafka_topic = config_params.get('kafka_topic', kafka_topic)
        sasl_username = config_params.get('sasl.username', sasl_username)
        sasl_password = config_params.get('sasl.password', sasl_password)

    if not kafka_bootstrap_servers:
        print(
            "Error: Kafka bootstrap servers must be provided via --kafka-bootstrap-servers "
            "or CONNECTION_STRING.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not kafka_topic:
        print(
            "Error: Kafka topic must be provided via --kafka-topic or CONNECTION_STRING.",
            file=sys.stderr,
        )
        sys.exit(1)

    kafka_config: Dict[str, str] = {
        'bootstrap.servers': kafka_bootstrap_servers,
    }
    if sasl_username and sasl_password:
        kafka_config.update({
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password,
            'security.protocol': 'SASL_SSL',
        })
    elif enable_tls:
        kafka_config['security.protocol'] = 'SSL'

    poller = TflRoadTrafficPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        polling_interval=polling_interval,
        reference_refresh_interval=reference_refresh_interval,
    )
    poller.poll_and_send()
