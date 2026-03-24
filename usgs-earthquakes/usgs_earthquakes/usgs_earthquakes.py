"""
USGS Earthquake Data Poller
Polls the USGS Earthquake Hazards Program GeoJSON feeds and sends events to a Kafka topic using SASL PLAIN authentication.
"""

import os
import json
import sys
import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, AsyncIterator, Any, Optional
import argparse
from confluent_kafka import Producer

# pylint: disable=import-error, line-too-long
from usgs_earthquakes.usgs_earthquakes_producer.usgs.earthquakes.event import Event
from usgs_earthquakes.usgs_earthquakes_producer.producer_client import USGSEarthquakesEventProducer
# pylint: enable=import-error, line-too-long


if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# Available feed URLs by time period and minimum magnitude
FEED_URLS = {
    "all_hour": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson",
    "significant_hour": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_hour.geojson",
    "m4.5_hour": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_hour.geojson",
    "m2.5_hour": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_hour.geojson",
    "m1.0_hour": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_hour.geojson",
    "all_day": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson",
    "significant_day": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_day.geojson",
    "m4.5_day": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson",
    "m2.5_day": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson",
    "m1.0_day": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_day.geojson",
    "all_week": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson",
    "significant_week": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.geojson",
    "m4.5_week": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.geojson",
    "m2.5_week": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson",
    "m1.0_week": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.geojson",
    "all_month": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson",
    "significant_month": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson",
    "m4.5_month": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_month.geojson",
    "m2.5_month": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson",
    "m1.0_month": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_month.geojson",
}

DEFAULT_FEED = "all_hour"


class USGSEarthquakePoller:
    """
    Class to poll USGS Earthquake GeoJSON feeds and send events to a Kafka topic.
    """
    BASE_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/"

    def __init__(self, kafka_config: Dict[str, str] | None = None, kafka_topic: str | None = None,
                 last_polled_file: str | None = None, feed: str = DEFAULT_FEED,
                 min_magnitude: Optional[float] = None):
        """
        Initialize the USGSEarthquakePoller.

        Args:
            kafka_config: Kafka configuration settings.
            kafka_topic: Kafka topic to send messages to.
            last_polled_file: File to store the last polled event IDs.
            feed: Feed name key from FEED_URLS (default: all_hour).
            min_magnitude: Minimum magnitude filter (applied client-side). If None, all events pass.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        if kafka_config is not None:
            producer = Producer(kafka_config)
            self.event_producer = USGSEarthquakesEventProducer(producer, kafka_topic)
        self.feed = feed
        self.min_magnitude = min_magnitude

    async def fetch_feed(self) -> List[Dict[str, Any]]:
        """
        Fetch earthquake data from the USGS GeoJSON feed.

        Returns:
            List of feature dictionaries from the GeoJSON response.
        """
        url = FEED_URLS.get(self.feed)
        if not url:
            logger.error("Unknown feed: %s. Available feeds: %s", self.feed, ', '.join(FEED_URLS.keys()))
            return []

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            try:
                async with asyncio.timeout(30):
                    async with session.get(url) as response:
                        response.raise_for_status()
                        data = await response.json()
            except asyncio.TimeoutError:
                logger.error("Request timed out for feed %s", self.feed)
                return []
            except aiohttp.ClientError as e:
                logger.error("HTTP error occurred: %s", e)
                return []

        features = data.get("features", [])
        return features

    def parse_event(self, feature: Dict[str, Any]) -> Optional[Event]:
        """
        Parse a GeoJSON feature into an Event dataclass.

        Args:
            feature: A GeoJSON feature dictionary from the USGS API.

        Returns:
            An Event instance, or None if the feature cannot be parsed.
        """
        props = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        coordinates = geometry.get("coordinates", [None, None, None])

        event_id = feature.get("id", "")
        if not event_id:
            return None

        magnitude = props.get("mag")
        if self.min_magnitude is not None and magnitude is not None:
            if magnitude < self.min_magnitude:
                return None

        # Convert epoch milliseconds to ISO-8601
        time_ms = props.get("time")
        if time_ms is not None:
            event_time = datetime.fromtimestamp(time_ms / 1000, tz=timezone.utc).isoformat()
        else:
            event_time = datetime.now(timezone.utc).isoformat()

        updated_ms = props.get("updated")
        if updated_ms is not None:
            updated = datetime.fromtimestamp(updated_ms / 1000, tz=timezone.utc).isoformat()
        else:
            updated = event_time

        longitude = coordinates[0] if len(coordinates) > 0 and coordinates[0] is not None else 0.0
        latitude = coordinates[1] if len(coordinates) > 1 and coordinates[1] is not None else 0.0
        depth = coordinates[2] if len(coordinates) > 2 else None

        return Event(
            id=event_id,
            magnitude=magnitude,
            mag_type=props.get("magType"),
            place=props.get("place"),
            event_time=event_time,
            updated=updated,
            url=props.get("url"),
            detail_url=props.get("detail"),
            felt=props.get("felt"),
            cdi=props.get("cdi"),
            mmi=props.get("mmi"),
            alert=props.get("alert"),
            status=props.get("status", "automatic"),
            tsunami=props.get("tsunami", 0),
            sig=props.get("sig"),
            net=props.get("net", ""),
            code=props.get("code", ""),
            sources=props.get("sources"),
            nst=props.get("nst"),
            dmin=props.get("dmin"),
            rms=props.get("rms"),
            gap=props.get("gap"),
            event_type=props.get("type"),
            latitude=latitude,
            longitude=longitude,
            depth=depth
        )

    def load_seen_event_ids(self) -> Dict[str, str]:
        """
        Load previously seen event IDs and their update timestamps from file.

        Returns:
            Dict mapping event ID to last-seen 'updated' timestamp.
        """
        if self.last_polled_file and os.path.exists(self.last_polled_file):
            with open(self.last_polled_file, 'r', encoding='utf-8') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    logger.error("Error decoding last polled file")
                    return {}
        return {}

    def save_seen_event_ids(self, seen_ids: Dict[str, str]):
        """
        Save seen event IDs and update timestamps to file.

        Args:
            seen_ids: Dict mapping event ID to 'updated' timestamp.
        """
        if self.last_polled_file:
            with open(self.last_polled_file, 'w', encoding='utf-8') as file:
                json.dump(seen_ids, file)

    async def poll_and_send(self):
        """
        Continuously poll the USGS earthquake feed and send new/updated events to Kafka.
        """
        seen_ids = self.load_seen_event_ids()
        poll_interval = timedelta(minutes=1)

        while True:
            start_poll_time = datetime.now(timezone.utc)
            features = await self.fetch_feed()
            count_new = 0
            count_updated = 0

            for feature in features:
                event = self.parse_event(feature)
                if event is None:
                    continue

                # Check if we've already seen and sent this exact version
                prev_updated = seen_ids.get(event.id)
                if prev_updated == event.updated:
                    continue

                if prev_updated is None:
                    count_new += 1
                else:
                    count_updated += 1

                await self.event_producer.send_usgs_earthquakes_event(
                    _source_uri=self.BASE_URL,
                    _net=event.net,
                    _code=event.code,
                    _event_time=event.event_time,
                    data=event,
                    flush_producer=False
                )

                seen_ids[event.id] = event.updated

            self.event_producer.producer.flush()
            self.save_seen_event_ids(seen_ids)

            if count_new > 0 or count_updated > 0:
                logger.info("Processed %d new and %d updated earthquake events", count_new, count_updated)
            else:
                logger.debug("No new earthquake events")

            # Prune old events from the seen set (keep last 30 days worth)
            cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
            seen_ids = {eid: ts for eid, ts in seen_ids.items() if ts >= cutoff}

            elapsed = datetime.now(timezone.utc) - start_poll_time
            remaining = poll_interval - elapsed
            if remaining.total_seconds() > 0:
                logger.debug("Sleeping for %s", remaining)
                await asyncio.sleep(remaining.total_seconds())


async def run_recent_events(feed: str, min_magnitude: Optional[float] = None):
    """Fetch and print recent earthquake events."""
    poller = USGSEarthquakePoller(feed=feed, min_magnitude=min_magnitude)
    features = await poller.fetch_feed()
    for feature in features:
        event = poller.parse_event(feature)
        if event:
            mag_str = f"M{event.magnitude:.1f}" if event.magnitude is not None else "M?"
            print(f"{mag_str} - {event.place} ({event.event_time}) [{event.id}]")


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse the connection string and extract bootstrap server, topic name, username, and password.

    Args:
        connection_string: The connection string.

    Returns:
        Dict with extracted connection parameters.
    """
    config_dict = {
        'sasl.username': '$ConnectionString',
        'sasl.password': connection_string.strip(),
    }
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip(
                    '"').replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=', 1)[1].strip('"')
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    return config_dict


def main():
    """
    Main function to parse arguments and start the USGS earthquake poller.
    """
    parser = argparse.ArgumentParser(description="USGS Earthquake Data Poller")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    feed_parser = subparsers.add_parser('feed', help="Poll USGS earthquake data and feed it to Kafka")
    feed_parser.add_argument('--last-polled-file', type=str,
                             help="File to store the last polled event IDs")
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str,
                             help="Comma separated list of Kafka bootstrap servers")
    feed_parser.add_argument('--kafka-topic', type=str,
                             help="Kafka topic to send messages to")
    feed_parser.add_argument('--sasl-username', type=str,
                             help="Username for SASL PLAIN authentication")
    feed_parser.add_argument('--sasl-password', type=str,
                             help="Password for SASL PLAIN authentication")
    feed_parser.add_argument('--connection-string', type=str,
                             help='Microsoft Event Hubs or Microsoft Fabric Event Stream connection string')
    feed_parser.add_argument('--feed', type=str, default=DEFAULT_FEED,
                             help=f'Feed to poll (default: {DEFAULT_FEED}). Options: {", ".join(FEED_URLS.keys())}')
    feed_parser.add_argument('--min-magnitude', type=float, default=None,
                             help='Minimum magnitude filter (client-side)')
    feed_parser.add_argument('--log-level', type=str,
                             help='Logging level', default='INFO')

    events_parser = subparsers.add_parser('events', help="List recent earthquake events")
    events_parser.add_argument('--feed', type=str, default='all_hour',
                               help='Feed to query (default: all_hour)')
    events_parser.add_argument('--min-magnitude', type=float, default=None,
                               help='Minimum magnitude filter')

    feeds_parser = subparsers.add_parser('feeds', help="List available feeds")

    args = parser.parse_args()

    if args.subcommand == 'events':
        asyncio.run(run_recent_events(args.feed, args.min_magnitude))
    elif args.subcommand == 'feeds':
        for name, url in FEED_URLS.items():
            print(f"{name}: {url}")
    elif args.subcommand == 'feed':

        if not args.connection_string:
            args.connection_string = os.getenv('CONNECTION_STRING')
        if not args.last_polled_file:
            args.last_polled_file = os.getenv('USGS_EQ_LAST_POLLED_FILE')
            if not args.last_polled_file:
                args.last_polled_file = os.path.expanduser('~/.usgs_earthquakes_last_polled.json')
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
            print("Error: Kafka bootstrap servers must be provided either through the command line or connection string.")
            sys.exit(1)
        if not kafka_topic:
            print("Error: Kafka topic must be provided either through the command line or connection string.")
            sys.exit(1)
        if not sasl_username or not sasl_password:
            print("Error: SASL username and password must be provided either through the command line or connection string.")
            sys.exit(1)

        kafka_config = {
            'bootstrap.servers': kafka_bootstrap_servers,
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password
        }

        poller = USGSEarthquakePoller(
            kafka_config=kafka_config,
            kafka_topic=kafka_topic,
            last_polled_file=args.last_polled_file,
            feed=args.feed,
            min_magnitude=args.min_magnitude
        )

        asyncio.run(poller.poll_and_send())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
