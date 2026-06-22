"""
DWD Pollenflug (German Pollen Forecast) Bridge
Polls the DWD pollen forecast API and sends forecasts to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
from typing import Dict, List, Optional
import argparse
import requests
from dwd_pollenflug_producer_data import Region, PollenForecast
from dwd_pollenflug_producer_kafka_producer.producer import DEDWDPollenflugEventProducer
from dwd_pollenflug_core import (
    POLLEN_NAME_MAP, USER_AGENT, FORECAST_API_URL, POLL_INTERVAL_SECONDS,
    get_region_id, get_region_display_name, parse_regions, parse_forecasts,
    fetch_data as _core_fetch_data, load_state as _core_load_state,
    save_state as _core_save_state,
)


class DWDPollenflugPoller:
    """Polls the DWD Pollenflug API and sends events to Kafka."""

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str):
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        from confluent_kafka import Producer as KafkaProducer
        kafka_producer = KafkaProducer(kafka_config)
        self.producer = DEDWDPollenflugEventProducer(kafka_producer, kafka_topic)

    def load_state(self) -> Dict:
        """Load persisted state from disk."""
        return _core_load_state(self.last_polled_file)

    def save_state(self, state: Dict):
        """Persist state to disk."""
        _core_save_state(self.last_polled_file, state)

    @staticmethod
    def fetch_data() -> Optional[dict]:
        """Fetch the DWD pollen forecast JSON."""
        return _core_fetch_data()

    def poll_and_send(self, once: bool = False):
        """Main polling loop."""
        print(f"Starting DWD Pollenflug poller, polling every {POLL_INTERVAL_SECONDS}s")
        print(f"  API URL: {FORECAST_API_URL}")
        print(f"  Kafka topic: {self.kafka_topic}")

        # Emit reference data at startup
        print("Fetching initial data for reference regions...")
        data = self.fetch_data()
        if data:
            regions = parse_regions(data)
            for region in regions:
                self.producer.send_de_dwd_pollenflug_region(
                    str(region.region_id), region, flush_producer=False)
            self.producer.producer.flush()
            print(f"Sent {len(regions)} regions as reference data")

        while True:
            try:
                state = self.load_state()
                last_update_seen = state.get("last_update")

                data = self.fetch_data()
                if data:
                    current_last_update = data.get("last_update", "")

                    if current_last_update and current_last_update != last_update_seen:
                        forecasts = parse_forecasts(data)
                        for forecast in forecasts:
                            self.producer.send_de_dwd_pollenflug_pollen_forecast(
                                str(forecast.region_id), forecast, flush_producer=False)
                        self.producer.producer.flush()
                        print(f"Sent {len(forecasts)} pollen forecasts (last_update={current_last_update})")
                        state["last_update"] = current_last_update
                        self.save_state(state)
                    else:
                        print(f"No new data (last_update={current_last_update})")

            except Exception as e:
                print(f"Error in polling loop: {e}")

            if once:
                break

            time.sleep(POLL_INTERVAL_SECONDS)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Azure Event Hubs-style connection string and extract Kafka parameters."""
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
    """Main entry point."""
    parser = argparse.ArgumentParser(description="DWD Pollenflug (German Pollen Forecast) Bridge")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store last seen update timestamp")
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
                        help="Run a single polling cycle and exit (used by scheduled hosts e.g. Fabric notebooks)")

    _argv = sys.argv[1:]
    if _argv and _argv[0] == 'feed':
        _argv = _argv[1:]
    args = parser.parse_args(_argv)

    once_env = os.getenv('ONCE_MODE', '').strip().lower() in ('1', 'true', 'yes')
    once = bool(args.once or once_env)

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.last_polled_file:
        args.last_polled_file = os.getenv('DWD_POLLENFLUG_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.dwd_pollenflug_last_polled.json')

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
            'sasl.password': sasl_password,
        })
    elif tls_enabled:
        kafka_config['security.protocol'] = 'SSL'

    poller = DWDPollenflugPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file,
    )
    poller.poll_and_send(once=once)


if __name__ == "__main__":
    main()
