"""
JMA Japan Weather Bulletins Poller
Polls the JMA Atom feeds for weather bulletins and sends them to Kafka as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
import hashlib
from typing import Dict, List, Optional
from xml.etree import ElementTree
import argparse
import requests
from jma_japan_producer_data import WeatherBulletin
from jma_japan_producer_data.feedtypeenum import FeedTypeenum
from jma_japan_producer_kafka_producer.producer import (
    JpGoJmaWeatherBulletinsEventProducer,
)
from jma_japan_core import (
    ATOM_NS, USER_AGENT, REGULAR_FEED_URL, EXTRA_FEED_URL, POLL_INTERVAL_SECONDS,
    HEADERS, make_bulletin_id, fetch_feed, parse_entries, poll_feeds,
    load_seen_bulletins as _core_load_seen_bulletins,
    save_seen_bulletins as _core_save_seen_bulletins,
    bulletin_office_segment,
)


class JMABulletinPoller:
    """
    Polls the JMA Atom XML feeds for weather bulletins and sends them to Kafka as CloudEvents.
    """
    REGULAR_FEED_URL = REGULAR_FEED_URL
    EXTRA_FEED_URL = EXTRA_FEED_URL
    HEADERS = HEADERS
    POLL_INTERVAL_SECONDS = POLL_INTERVAL_SECONDS

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str):
        """
        Initialize the JMABulletinPoller.

        Args:
            kafka_config: Kafka configuration settings.
            kafka_topic: Kafka topic to send messages to.
            last_polled_file: File to store seen bulletin IDs for deduplication.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        from confluent_kafka import Producer
        kafka_producer = Producer(kafka_config)
        self.bulletins_producer = JpGoJmaWeatherBulletinsEventProducer(kafka_producer, kafka_topic)
        self.kafka_producer = kafka_producer

    def load_seen_bulletins(self) -> Dict:
        """Load the set of previously seen bulletin IDs from the state file."""
        return _core_load_seen_bulletins(self.last_polled_file)

    def save_seen_bulletins(self, state: Dict):
        """Save the set of seen bulletin IDs to the state file."""
        _core_save_seen_bulletins(self.last_polled_file, state)

    @staticmethod
    def _make_bulletin_id(entry_id: str) -> str:
        """Create a stable short ID from an Atom entry ID (which is typically a long URL)."""
        return make_bulletin_id(entry_id)

    def fetch_feed(self, url: str) -> Optional[ElementTree.Element]:
        """Fetch and parse an Atom XML feed."""
        return fetch_feed(url)

    @staticmethod
    def parse_entries(root: ElementTree.Element, feed_type: str) -> List[WeatherBulletin]:
        """Parse Atom feed entries into WeatherBulletin objects."""
        return parse_entries(root, feed_type)

    def poll_feeds(self) -> List[WeatherBulletin]:
        """Fetch both regular and extra feeds and return all parsed bulletins."""
        return poll_feeds()

    def poll_and_send(self, once: bool = False):
        """
        Main polling loop. Fetches bulletins, deduplicates, and sends new ones
        to Kafka as CloudEvents. Polls every POLL_INTERVAL_SECONDS.

        Args:
            once: When True, exit after a single polling cycle (used by the
                Fabric notebook scheduler).
        """
        print(f"Starting JMA Weather Bulletin poller, polling every {self.POLL_INTERVAL_SECONDS}s")
        print(f"  Regular feed: {self.REGULAR_FEED_URL}")
        print(f"  Extra feed:   {self.EXTRA_FEED_URL}")
        print(f"  Kafka topic:  {self.kafka_topic}")

        while True:
            try:
                state = self.load_seen_bulletins()
                seen_ids = set(state.get("seen_ids", []))
                bulletins = self.poll_feeds()

                new_count = 0
                for bulletin in bulletins:
                    if bulletin.bulletin_id in seen_ids:
                        continue

                    self.bulletins_producer.send_jp_go_jma_weather_bulletin(
                        bulletin.bulletin_id, bulletin, flush_producer=False)
                    seen_ids.add(bulletin.bulletin_id)
                    new_count += 1

                if new_count > 0:
                    self.kafka_producer.flush()
                    print(f"Sent {new_count} new bulletin(s) to Kafka")

                # Keep only the last 10000 seen IDs
                seen_list = list(seen_ids)
                if len(seen_list) > 10000:
                    seen_list = seen_list[-10000:]
                state["seen_ids"] = seen_list
                self.save_seen_bulletins(state)

            except Exception as e:
                print(f"Error in polling loop: {e}")

            if once:
                print("--once mode: exiting after first polling cycle")
                break

            time.sleep(self.POLL_INTERVAL_SECONDS)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse an Azure Event Hubs-style connection string and extract Kafka parameters.

    Args:
        connection_string: The connection string.

    Returns:
        Dict with bootstrap.servers, kafka_topic, sasl.username, sasl.password.
    """
    config_dict = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                    '"').replace('sb://', '').replace('/', '') + ':9093'
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


def main():
    """
    Main function to parse arguments and start the JMA bulletin poller.
    """
    parser = argparse.ArgumentParser(description="JMA Japan Weather Bulletins Poller")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store seen bulletin IDs for deduplication")
    parser.add_argument('--kafka-bootstrap-servers', type=str,
                        help="Comma separated list of Kafka bootstrap servers")
    parser.add_argument('--kafka-topic', type=str,
                        help="Kafka topic to send messages to")
    parser.add_argument('--sasl-username', type=str,
                        help="Username for SASL PLAIN authentication")
    parser.add_argument('--sasl-password', type=str,
                        help="Password for SASL PLAIN authentication")
    parser.add_argument('--connection-string', type=str,
                        help='Microsoft Event Hubs or Microsoft Fabric Event Stream connection string')
    parser.add_argument('--once', action='store_true',
                        default=os.getenv('ONCE_MODE', '').lower() in ('1', 'true', 'yes'),
                        help='Exit after one polling cycle (also via ONCE_MODE env var). Used by the Fabric notebook scheduler.')

    _argv = sys.argv[1:]
    if _argv and _argv[0] == 'feed':
        _argv = _argv[1:]
    args = parser.parse_args(_argv)

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.last_polled_file:
        args.last_polled_file = os.getenv('JMA_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.jma_last_polled.json')

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

    poller = JMABulletinPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file
    )
    poller.poll_and_send(once=args.once)


if __name__ == "__main__":
    main()
