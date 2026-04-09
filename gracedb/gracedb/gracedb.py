"""
GraceDB Gravitational Wave Candidate Alert Poller
Polls the GraceDB public API for superevents and sends them to a Kafka topic using SASL PLAIN authentication.
"""

import os
import json
import sys
import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional, Set
import argparse
from confluent_kafka import Producer

# pylint: disable=import-error, line-too-long
from gracedb_producer_data.org.ligo.gracedb.superevent import Superevent
from gracedb_producer_kafka_producer.producer import OrgLigoGracedbEventProducer
# pylint: enable=import-error, line-too-long


if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

BASE_API_URL = "https://gracedb.ligo.org/api/superevents/"
DEFAULT_POLL_COUNT = 25
DEFAULT_CATEGORIES = "Production,MDC"


class GraceDBPoller:
    """
    Polls the GraceDB superevent API and sends new events to a Kafka topic.
    """

    def __init__(self, kafka_config: Optional[Dict[str, str]] = None,
                 kafka_topic: Optional[str] = None,
                 last_polled_file: Optional[str] = None,
                 poll_count: int = DEFAULT_POLL_COUNT,
                 categories: Optional[str] = None):
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        self.poll_count = poll_count
        self.categories = set(c.strip() for c in (categories or DEFAULT_CATEGORIES).split(','))
        self.event_producer: Optional[OrgLigoGracedbEventProducer] = None
        if kafka_config is not None:
            producer = Producer(kafka_config)
            self.event_producer = OrgLigoGracedbEventProducer(producer, kafka_topic)

    async def fetch_superevents(self, count: Optional[int] = None) -> List[Dict[str, Any]]:
        """Fetch superevents from the GraceDB public API."""
        url = f"{BASE_API_URL}?format=json&count={count or self.poll_count}"
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            try:
                async with asyncio.timeout(30):
                    async with session.get(url) as response:
                        response.raise_for_status()
                        data = await response.json()
            except asyncio.TimeoutError:
                logger.error("Request timed out fetching superevents")
                return []
            except aiohttp.ClientError as e:
                logger.error("HTTP error fetching superevents: %s", e)
                return []
        return data.get("superevents", [])

    def parse_superevent(self, raw: Dict[str, Any]) -> Optional[Superevent]:
        """Parse a raw superevent dict from the API into a Superevent dataclass."""
        superevent_id = raw.get("superevent_id")
        if not superevent_id:
            return None

        category = raw.get("category", "")
        if category not in self.categories:
            return None

        preferred = raw.get("preferred_event_data") or {}

        labels = raw.get("labels", [])
        labels_json = json.dumps(labels) if isinstance(labels, list) else "[]"

        return Superevent(
            superevent_id=superevent_id,
            category=category,
            created=raw.get("created", ""),
            t_start=float(raw.get("t_start", 0.0)),
            t_0=float(raw.get("t_0", 0.0)),
            t_end=float(raw.get("t_end", 0.0)),
            far=float(raw.get("far", 0.0)),
            time_coinc_far=raw.get("time_coinc_far"),
            space_coinc_far=raw.get("space_coinc_far"),
            labels_json=labels_json,
            preferred_event_id=preferred.get("graceid"),
            pipeline=preferred.get("pipeline"),
            group=preferred.get("group"),
            instruments=preferred.get("instruments"),
            gw_id=raw.get("gw_id"),
            submitter=raw.get("submitter", ""),
            em_type=raw.get("em_type"),
            search=preferred.get("search"),
            far_is_upper_limit=preferred.get("far_is_upper_limit"),
            nevents=preferred.get("nevents"),
            self_uri=raw.get("links", {}).get("self", ""),
        )

    def load_seen_ids(self) -> Set[str]:
        """Load previously seen superevent IDs from file."""
        if self.last_polled_file and os.path.exists(self.last_polled_file):
            with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    return set(data.get("seen_ids", []))
                except json.JSONDecodeError:
                    logger.error("Error decoding last polled file")
                    return set()
        return set()

    def save_seen_ids(self, seen_ids: Set[str]):
        """Save seen superevent IDs to file."""
        if self.last_polled_file:
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump({"seen_ids": sorted(seen_ids)}, f)

    async def poll_and_send(self):
        """Continuously poll the GraceDB API and send new superevents to Kafka."""
        seen_ids = self.load_seen_ids()
        poll_interval = timedelta(minutes=2)

        while True:
            start_poll_time = datetime.now(timezone.utc)
            raw_events = await self.fetch_superevents()
            count_new = 0

            for raw in raw_events:
                superevent = self.parse_superevent(raw)
                if superevent is None:
                    continue

                if superevent.superevent_id in seen_ids:
                    continue

                await self.event_producer.send_org_ligo_gracedb_superevent(
                    _source_uri=BASE_API_URL,
                    _superevent_id=superevent.superevent_id,
                    _created=superevent.created,
                    data=superevent,
                    flush_producer=False,
                )
                seen_ids.add(superevent.superevent_id)
                count_new += 1

            self.event_producer.producer.flush()
            self.save_seen_ids(seen_ids)

            if count_new > 0:
                logger.info("Processed %d new superevents", count_new)
            else:
                logger.debug("No new superevents")

            # Prune seen set to bounded size (keep latest 5000)
            if len(seen_ids) > 5000:
                seen_ids = set(sorted(seen_ids)[-5000:])

            elapsed = datetime.now(timezone.utc) - start_poll_time
            remaining = poll_interval - elapsed
            if remaining.total_seconds() > 0:
                logger.debug("Sleeping for %s", remaining)
                await asyncio.sleep(remaining.total_seconds())


async def run_recent_events(count: int = 10, categories: Optional[str] = None):
    """Fetch and print recent superevents."""
    poller = GraceDBPoller(categories=categories, poll_count=count)
    raw_events = await poller.fetch_superevents(count=count)
    for raw in raw_events:
        superevent = poller.parse_superevent(raw)
        if superevent:
            print(f"{superevent.superevent_id} [{superevent.category}] FAR={superevent.far:.2e} "
                  f"pipeline={superevent.pipeline} created={superevent.created}")


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse connection string and extract bootstrap server, topic, username, and password."""
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip(
                    '"').replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=', 1)[1].strip('"')
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


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="GraceDB Gravitational Wave Candidate Alert Poller")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    feed_parser = subparsers.add_parser('feed', help="Poll GraceDB and feed superevents to Kafka")
    feed_parser.add_argument('--last-polled-file', type=str,
                             help="File to store the last polled superevent IDs")
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str,
                             help="Comma separated list of Kafka bootstrap servers")
    feed_parser.add_argument('--kafka-topic', type=str,
                             help="Kafka topic to send messages to")
    feed_parser.add_argument('--sasl-username', type=str,
                             help="Username for SASL PLAIN authentication")
    feed_parser.add_argument('--sasl-password', type=str,
                             help="Password for SASL PLAIN authentication")
    feed_parser.add_argument('--connection-string', type=str,
                             help='Event Hubs or Fabric Event Stream connection string')
    feed_parser.add_argument('--poll-count', type=int, default=DEFAULT_POLL_COUNT,
                             help=f'Number of superevents to fetch per poll (default: {DEFAULT_POLL_COUNT})')
    feed_parser.add_argument('--categories', type=str, default=DEFAULT_CATEGORIES,
                             help=f'Comma-separated categories to include (default: {DEFAULT_CATEGORIES})')
    feed_parser.add_argument('--log-level', type=str, help='Logging level', default='INFO')

    events_parser = subparsers.add_parser('events', help="List recent superevents")
    events_parser.add_argument('--count', type=int, default=10, help='Number of events to display')
    events_parser.add_argument('--categories', type=str, default=DEFAULT_CATEGORIES,
                               help='Comma-separated categories to include')

    args = parser.parse_args()

    if args.subcommand == 'events':
        asyncio.run(run_recent_events(count=args.count, categories=args.categories))
    elif args.subcommand == 'feed':
        if not args.connection_string:
            args.connection_string = os.getenv('CONNECTION_STRING')
        if not args.last_polled_file:
            args.last_polled_file = os.getenv('GRACEDB_LAST_POLLED_FILE')
            if not args.last_polled_file:
                args.last_polled_file = os.path.expanduser('~/.gracedb_last_polled.json')
        if os.getenv('LOG_LEVEL'):
            args.log_level = os.getenv('LOG_LEVEL')
        if args.log_level:
            logger.setLevel(args.log_level)

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
            print("Error: Kafka bootstrap servers must be provided.")
            sys.exit(1)
        if not kafka_topic:
            print("Error: Kafka topic must be provided.")
            sys.exit(1)

        tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
        kafka_config = {
            'bootstrap.servers': kafka_bootstrap_servers,
        }
        if sasl_username and sasl_password:
            kafka_config.update({
                'sasl.mechanisms': 'PLAIN',
                'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT',
                'sasl.username': sasl_username,
                'sasl.password': sasl_password
            })
        elif tls_enabled:
            kafka_config['security.protocol'] = 'SSL'

        poller = GraceDBPoller(
            kafka_config=kafka_config,
            kafka_topic=kafka_topic,
            last_polled_file=args.last_polled_file,
            poll_count=args.poll_count,
            categories=args.categories,
        )
        asyncio.run(poller.poll_and_send())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
