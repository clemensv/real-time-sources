"""
Paris Bicycle Counters Poller
Polls the Paris Open Data bicycle counting stations and sends hourly counts
to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
import hashlib
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timezone, timedelta
import argparse
import requests
from paris_bicycle_counters_producer_data import Counter
from paris_bicycle_counters_producer_data import BicycleCount
from paris_bicycle_counters_producer_kafka_producer.producer import FRParisOpenDataVeloEventProducer


COUNTER_DATA_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-donnees-compteurs/records"
COUNTER_LOCATIONS_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-compteurs/records"
# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-paris-bicycle-counters/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)


def ce_datetime(value: datetime) -> str:
    """Return a stable UTC-ish timestamp string for CloudEvents ids."""
    return value.isoformat().replace("+00:00", "Z")


def is_topic_safe_segment(value: str) -> bool:
    return bool(value) and not any(ch in value for ch in ('/', '+', '#', '\x00'))


def counter_info_ce_id(counter_id: str, fields: Dict[str, object]) -> str:
    encoded = json.dumps(fields, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:12]
    return f"{counter_id}/info/{digest}"


class ParisBicycleCounterPoller:
    """
    Polls the Paris Open Data bicycle counter APIs and sends counter data
    to Kafka as CloudEvents.
    """
    POLL_INTERVAL_SECONDS = 3600  # Hourly data, poll every hour

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str):
        """
        Initialize the ParisBicycleCounterPoller.

        Args:
            kafka_config: Kafka configuration settings.
            kafka_topic: Kafka topic to send messages to.
            last_polled_file: File to store last seen timestamps per counter.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        from confluent_kafka import Producer
        kafka_producer = Producer(kafka_config)
        self.producer = FRParisOpenDataVeloEventProducer(kafka_producer, kafka_topic)

    def load_state(self) -> Dict:
        """
        Load the last polled state from the state file.

        Returns:
            Dict with last seen keys per counter.
        """
        if os.path.exists(self.last_polled_file):
            try:
                with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def save_state(self, state: Dict):
        """
        Save the last polled state to the state file.

        Args:
            state: Dict with last seen keys per counter.
        """
        os.makedirs(os.path.dirname(self.last_polled_file) if os.path.dirname(self.last_polled_file) else '.', exist_ok=True)
        with open(self.last_polled_file, 'w', encoding='utf-8') as f:
            json.dump(state, f)

    @staticmethod
    def fetch_counter_locations() -> List[Counter]:
        """
        Fetch counter location reference data from the Paris Open Data API.

        Returns:
            List of Counter objects.
        """
        counters: List[Counter] = []
        offset = 0
        limit = 100
        while True:
            params = {"limit": limit, "offset": offset}
            response = requests.get(COUNTER_LOCATIONS_URL, params=params, headers={"User-Agent": USER_AGENT}, timeout=30)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            if not results:
                break
            for record in results:
                coords = record.get("coordinates") or {}
                counter_id = record.get("id_compteur", "")
                if not is_topic_safe_segment(counter_id):
                    print(f"Skipping counter with MQTT-unsafe id_compteur={counter_id!r}", file=sys.stderr)
                    continue
                fields = {
                    "counter_name": record.get("nom_compteur", ""),
                    "channel_name": record.get("channel_name"),
                    "installation_date": record.get("installation_date"),
                    "longitude": coords.get("lon"),
                    "latitude": coords.get("lat"),
                }
                counter = Counter(
                    ce_id=counter_info_ce_id(counter_id, fields),
                    counter_id=counter_id,
                    **fields,
                )
                counters.append(counter)
            if len(results) < limit:
                break
            offset += limit
        return counters

    @staticmethod
    def fetch_bicycle_counts(since: Optional[datetime] = None) -> List[BicycleCount]:
        """
        Fetch bicycle count data from the Paris Open Data API.

        Args:
            since: Only fetch records from this datetime onwards.

        Returns:
            List of BicycleCount objects.
        """
        counts: List[BicycleCount] = []
        offset = 0
        limit = 100
        # The Paris OpenData explore API caps offset+limit at 10000.
        MAX_OFFSET = 10000 - limit
        while True:
            params: Dict[str, object] = {"limit": limit, "offset": offset}
            if since:
                where_clause = f"date >= '{since.strftime('%Y-%m-%dT%H:%M:%S')}'"
                params["where"] = where_clause
            try:
                response = requests.get(COUNTER_DATA_URL, params=params, headers={"User-Agent": USER_AGENT}, timeout=30)
                response.raise_for_status()
            except requests.HTTPError as e:
                # 400 typically means we have hit the API's 10000-row paging
                # ceiling; return what we have so far rather than losing the
                # entire batch.
                print(f"Stopping pagination at offset {offset}: {e}", file=sys.stderr)
                break
            data = response.json()
            results = data.get("results", [])
            if not results:
                break
            for record in results:
                coords = record.get("coordinates") or {}
                date_str = record.get("date")
                if not date_str:
                    continue
                try:
                    date_val = datetime.fromisoformat(date_str)
                except (ValueError, TypeError):
                    continue
                counter_id = record.get("id_compteur", "")
                if not is_topic_safe_segment(counter_id):
                    print(f"Skipping count with MQTT-unsafe id_compteur={counter_id!r}", file=sys.stderr)
                    continue
                bc = BicycleCount(
                    ce_id=f"{counter_id}/{ce_datetime(date_val)}/count",
                    counter_id=counter_id,
                    counter_name=record.get("nom_compteur", ""),
                    count=record.get("sum_counts"),
                    date=date_val,
                    longitude=coords.get("lon"),
                    latitude=coords.get("lat"),
                )
                counts.append(bc)
            if len(results) < limit:
                break
            offset += limit
            if offset > MAX_OFFSET:
                break
        return counts

    @staticmethod
    def dedup_counts(counts: List[BicycleCount], seen_keys: Set[str]) -> Tuple[List[BicycleCount], Set[str]]:
        """
        Deduplicate bicycle counts using counter_id + date as the key.

        Args:
            counts: List of BicycleCount objects.
            seen_keys: Set of previously seen dedup keys.

        Returns:
            Tuple of (new unique counts, updated seen_keys set).
        """
        new_counts: List[BicycleCount] = []
        new_keys: Set[str] = set(seen_keys)
        for bc in counts:
            date_str = bc.date.isoformat() if isinstance(bc.date, datetime) else str(bc.date)
            key = f"{bc.counter_id}|{date_str}"
            if key not in new_keys:
                new_keys.add(key)
                new_counts.append(bc)
        return new_counts, new_keys

    def poll_and_send(self, once: bool = False):
        """
        Main polling loop. Fetches bicycle counts, deduplicates,
        and sends new observations to Kafka as CloudEvents.

        Args:
            once: Run one poll iteration and return. Intended for tests.
        """
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
                        bc.counter_id, bc.ce_id, ce_datetime(bc.date), bc, flush_producer=False)
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

    args = parser.parse_args()

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
