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

# German-to-English pollen name mapping
POLLEN_NAME_MAP = {
    "Hasel": "hazel",
    "Erle": "alder",
    "Birke": "birch",
    "Esche": "ash",
    "Graeser": "grasses",
    "Roggen": "rye",
    "Beifuss": "mugwort",
    "Ambrosia": "ragweed",
}

FORECAST_API_URL = "https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json"
POLL_INTERVAL_SECONDS = 3600  # 1 hour


def get_region_id(item: dict) -> int:
    """Derive the unique region identifier for a forecast area.

    If the area is a sub-region (partregion_id > 0), use partregion_id.
    Otherwise use the parent region_id.
    """
    partregion_id = item.get("partregion_id", -1)
    if partregion_id is not None and partregion_id > 0:
        return int(partregion_id)
    return int(item["region_id"])


def get_region_display_name(item: dict) -> str:
    """Return the best display name for a forecast area."""
    partregion_name = item.get("partregion_name", "")
    if partregion_name:
        return partregion_name
    return item.get("region_name", "")


def parse_regions(data: dict) -> List[Region]:
    """Parse region reference data from the DWD API response."""
    regions = []
    for item in data.get("content", []):
        rid = get_region_id(item)
        partregion_id_raw = item.get("partregion_id", -1)
        partregion_name_raw = item.get("partregion_name", "")
        regions.append(Region(
            region_id=rid,
            region_name=item.get("region_name", ""),
            partregion_id=None if partregion_id_raw == -1 else int(partregion_id_raw),
            partregion_name=None if not partregion_name_raw else partregion_name_raw,
        ))
    return regions


def parse_forecasts(data: dict) -> List[PollenForecast]:
    """Parse pollen forecasts from the DWD API response, mapping German names to English."""
    forecasts = []
    last_update = data.get("last_update", "")
    next_update = data.get("next_update", "")
    sender = data.get("sender")

    for item in data.get("content", []):
        rid = get_region_id(item)
        display_name = get_region_display_name(item)
        pollen = item.get("Pollen", {})

        kwargs: Dict[str, Optional[str]] = {}
        for german_name, english_name in POLLEN_NAME_MAP.items():
            pollen_data = pollen.get(german_name, {})
            if not isinstance(pollen_data, dict):
                pollen_data = {}
            kwargs[f"{english_name}_today"] = pollen_data.get("today")
            kwargs[f"{english_name}_tomorrow"] = pollen_data.get("tomorrow")
            kwargs[f"{english_name}_dayafter_to"] = pollen_data.get("dayafter_to")

        forecasts.append(PollenForecast(
            region_id=rid,
            region_name=display_name,
            last_update=last_update,
            next_update=next_update,
            sender=sender,
            **kwargs,
        ))
    return forecasts


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
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, OSError) as err:
            print(f"Warning: could not load state file: {err}")
        return {}

    def save_state(self, state: Dict):
        """Persist state to disk."""
        try:
            state_dir = os.path.dirname(self.last_polled_file)
            if state_dir:
                os.makedirs(state_dir, exist_ok=True)
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(state, f)
        except OSError as err:
            print(f"Warning: could not save state file: {err}")

    @staticmethod
    def fetch_data() -> Optional[dict]:
        """Fetch the DWD pollen forecast JSON."""
        try:
            response = requests.get(FORECAST_API_URL, timeout=60)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            print(f"Error fetching DWD pollen forecast: {err}")
            return None

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

    args = parser.parse_args()

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
    poller.poll_and_send()


if __name__ == "__main__":
    main()
