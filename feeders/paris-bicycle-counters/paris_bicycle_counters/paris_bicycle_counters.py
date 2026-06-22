"""Kafka feeder for Paris bicycle counters."""

import argparse
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, Set

import paris_bicycle_counters_core.paris_bicycle_counters as _core_module
from confluent_kafka import Producer
from paris_bicycle_counters_core import (
    BicycleCount,
    COUNTER_DATA_URL,
    COUNTER_LOCATIONS_URL,
    Counter,
    ParisBicycleCounterPoller as ParisBicycleCounterCorePoller,
    ce_datetime,
    counter_info_ce_id,
    is_topic_safe_segment,
)
from paris_bicycle_counters_producer_kafka_producer.producer import FRParisOpenDataVeloEventProducer

requests = _core_module.requests


class ParisBicycleCounterPoller(ParisBicycleCounterCorePoller):
    """Kafka-specific Paris bicycle counter poller."""

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str):
        super().__init__(last_polled_file=last_polled_file)
        self.kafka_topic = kafka_topic
        kafka_producer = Producer(kafka_config)
        self.producer = FRParisOpenDataVeloEventProducer(kafka_producer, kafka_topic)

    def poll_and_send(self, once: bool = False):
        """Poll and publish reference plus telemetry events to Kafka."""
        print(f"Starting Paris Bicycle Counter poller, polling every {self.POLL_INTERVAL_SECONDS}s")
        print(f"  Counter data URL: {COUNTER_DATA_URL}")
        print(f"  Counter locations URL: {COUNTER_LOCATIONS_URL}")
        print(f"  Kafka topic: {self.kafka_topic}")

        # Send reference data (counter locations) at startup
        print("Sending counter locations as reference data...")
        counters = self.fetch_counter_locations()
        for counter in counters:
            self.producer.send_fr_paris_open_data_velo_counter(
                counter.counter_id, counter.ce_id, counter, flush_producer=False)
        self.producer.producer.flush()
        print(f"Sent {len(counters)} counter locations as reference data")

        while True:
            try:
                state = self.load_state()
                seen_keys: Set[str] = set(state.get("seen_keys", []))

                # The Paris open-data feed is updated with a multi-day lag
                # (typically 2-4 days). Use a wide enough window to always
                # capture at least one fresh observation per counter.
                since = datetime.now(timezone.utc) - timedelta(days=7)
                counts = self.fetch_bicycle_counts(since=since)
                new_counts, seen_keys = self.dedup_counts(counts, seen_keys)

                for bc in new_counts:
                    self.producer.send_fr_paris_open_data_velo_bicycle_count(
                        bc.counter_id, bc.ce_id, data=bc, _time=ce_datetime(bc.date), flush_producer=False)
                self.producer.producer.flush()

                # Trim seen_keys to last 48h worth of keys to avoid unbounded growth
                cutoff = datetime.now(timezone.utc) - timedelta(days=14)
                trimmed_keys: Set[str] = set()
                for key in seen_keys:
                    try:
                        date_part = key.split("|", 1)[1]
                        dt = datetime.fromisoformat(date_part)
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                        if dt >= cutoff:
                            trimmed_keys.add(key)
                    except (IndexError, ValueError):
                        trimmed_keys.add(key)
                seen_keys = trimmed_keys

                state["seen_keys"] = list(seen_keys)
                self.save_state(state)

                print(f"Polled {len(counts)} records, sent {len(new_counts)} new bicycle counts")

            except Exception as e:
                print(f"Error during polling: {e}", file=sys.stderr)

            if once:
                return

            time.sleep(self.POLL_INTERVAL_SECONDS)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse an Azure Event Hubs-style connection string and extract Kafka parameters.

    Args:
        connection_string: The connection string.

    Returns:
        Dict with bootstrap.servers, kafka_topic, sasl.username, sasl.password.
    """
    config_dict: Dict[str, str] = {}
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
    Main function to parse arguments and start the Paris bicycle counter poller.
    """
    parser = argparse.ArgumentParser(description="Paris Bicycle Counters Poller")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store last seen timestamps per counter")
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
                        help='Run a single polling cycle and exit. Honors the ONCE_MODE env var when set to a truthy value.')

    _argv = sys.argv[1:]
    if _argv and _argv[0] == 'feed':
        _argv = _argv[1:]
    args = parser.parse_args(_argv)

    if not args.once:
        once_env = os.getenv('ONCE_MODE', '').strip().lower()
        if once_env in ('1', 'true', 'yes', 'on'):
            args.once = True

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.last_polled_file:
        args.last_polled_file = os.getenv('PARIS_VELO_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.paris_velo_last_polled.json')

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
    kafka_config: Dict[str, str] = {
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

    poller = ParisBicycleCounterPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file
    )
    poller.poll_and_send(once=args.once)


if __name__ == "__main__":
    main()
