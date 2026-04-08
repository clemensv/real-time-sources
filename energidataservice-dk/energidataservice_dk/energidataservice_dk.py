"""
Energi Data Service (Energinet) Bridge
Polls the Energi Data Service API for Danish power system snapshots and spot prices
and sends them to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
from typing import Dict, List, Optional
import argparse
import requests
from energidataservice_dk_producer_data import PowerSystemSnapshot, SpotPrice
from energidataservice_dk_producer_kafka_producer.producer import DkEnerginetEnergidataserviceEventProducer

POWER_SYSTEM_URL = "https://api.energidataservice.dk/dataset/PowerSystemRightNow"
SPOT_PRICES_URL = "https://api.energidataservice.dk/dataset/ElspotPrices"

POWER_SYSTEM_POLL_INTERVAL = 90  # >60s to respect 1 req/min/dataset rate limit
SPOT_PRICES_POLL_INTERVAL = 3600  # hourly for day-ahead prices

# Mapping from API field names to schema field names for PowerSystemRightNow
POWER_SYSTEM_FIELD_MAP = {
    "Minutes1UTC": "minutes1_utc",
    "Minutes1DK": "minutes1_dk",
    "CO2Emission": "co2_emission",
    "ProductionGe100MW": "production_ge_100mw",
    "ProductionLt100MW": "production_lt_100mw",
    "SolarPower": "solar_power",
    "OffshoreWindPower": "offshore_wind_power",
    "OnshoreWindPower": "onshore_wind_power",
    "Exchange_Sum": "exchange_sum",
    "Exchange_DK1_DE": "exchange_dk1_de",
    "Exchange_DK1_NL": "exchange_dk1_nl",
    "Exchange_DK1_GB": "exchange_dk1_gb",
    "Exchange_DK1_NO": "exchange_dk1_no",
    "Exchange_DK1_SE": "exchange_dk1_se",
    "Exchange_DK1_DK2": "exchange_dk1_dk2",
    "Exchange_DK2_DE": "exchange_dk2_de",
    "Exchange_DK2_SE": "exchange_dk2_se",
    "Exchange_Bornholm_SE": "exchange_bornholm_se",
    "aFRR_ActivatedDK1": "afrr_activated_dk1",
    "aFRR_ActivatedDK2": "afrr_activated_dk2",
    "mFRR_ActivatedDK1": "mfrr_activated_dk1",
    "mFRR_ActivatedDK2": "mfrr_activated_dk2",
    "ImbalanceDK1": "imbalance_dk1",
    "ImbalanceDK2": "imbalance_dk2",
}

# Mapping from API field names to schema field names for ElspotPrices
SPOT_PRICE_FIELD_MAP = {
    "HourUTC": "hour_utc",
    "HourDK": "hour_dk",
    "PriceArea": "price_area",
    "SpotPriceDKK": "spot_price_dkk",
    "SpotPriceEUR": "spot_price_eur",
}


def safe_float(value) -> Optional[float]:
    """Convert a value to float, returning None if the value is None or not convertible."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def map_power_system_record(record: dict) -> PowerSystemSnapshot:
    """Map an API PowerSystemRightNow record to a PowerSystemSnapshot dataclass."""
    mapped = {}
    for api_key, schema_key in POWER_SYSTEM_FIELD_MAP.items():
        mapped[schema_key] = record.get(api_key)

    # Timestamp fields are required strings
    mapped["minutes1_utc"] = str(mapped.get("minutes1_utc") or "")
    mapped["minutes1_dk"] = str(mapped.get("minutes1_dk") or "")
    # Synthesize price_area for system-wide snapshot
    mapped["price_area"] = "DK"

    # Convert numeric fields
    for key in list(POWER_SYSTEM_FIELD_MAP.values()):
        if key not in ("minutes1_utc", "minutes1_dk"):
            mapped[key] = safe_float(mapped.get(key))

    return PowerSystemSnapshot(**mapped)


def map_spot_price_record(record: dict) -> SpotPrice:
    """Map an API ElspotPrices record to a SpotPrice dataclass."""
    mapped = {}
    for api_key, schema_key in SPOT_PRICE_FIELD_MAP.items():
        mapped[schema_key] = record.get(api_key)

    mapped["hour_utc"] = str(mapped.get("hour_utc") or "")
    mapped["hour_dk"] = str(mapped.get("hour_dk") or "")
    mapped["price_area"] = str(mapped.get("price_area") or "")
    mapped["spot_price_dkk"] = safe_float(mapped.get("spot_price_dkk"))
    mapped["spot_price_eur"] = safe_float(mapped.get("spot_price_eur"))

    return SpotPrice(**mapped)


def build_power_system_url(limit: int = 5) -> str:
    """Build the URL for the PowerSystemRightNow endpoint."""
    return f"{POWER_SYSTEM_URL}?limit={limit}"


def build_spot_prices_url(limit: int = 100) -> str:
    """Build the URL for the ElspotPrices endpoint with DK filter."""
    return f'{SPOT_PRICES_URL}?limit={limit}&filter={{"PriceArea":["DK1","DK2"]}}'


class EnergiDataServicePoller:
    """
    Polls the Energi Data Service API and sends power system snapshots
    and spot prices to Kafka as CloudEvents.
    """

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str):
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        from confluent_kafka import Producer as KafkaProducer
        kafka_producer = KafkaProducer(kafka_config)
        self.producer = DkEnerginetEnergidataserviceEventProducer(kafka_producer, kafka_topic)

    @staticmethod
    def _empty_state() -> Dict:
        return {
            "last_power_system_timestamp": None,
            "last_spot_price_timestamps": {},
        }

    @classmethod
    def _normalize_state(cls, state: Optional[Dict]) -> Dict:
        normalized = cls._empty_state()
        if not isinstance(state, dict):
            return normalized
        normalized["last_power_system_timestamp"] = state.get("last_power_system_timestamp")
        spot = state.get("last_spot_price_timestamps", {})
        if isinstance(spot, dict):
            normalized["last_spot_price_timestamps"].update(spot)
        return normalized

    def load_state(self) -> Dict:
        if not self.last_polled_file or not os.path.exists(self.last_polled_file):
            return self._empty_state()
        try:
            with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                return self._normalize_state(json.load(f))
        except (json.JSONDecodeError, IOError):
            return self._empty_state()

    def save_state(self, state: Dict):
        if not self.last_polled_file:
            return
        normalized = self._normalize_state(state)
        try:
            os.makedirs(os.path.dirname(self.last_polled_file) or '.', exist_ok=True)
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(normalized, f)
        except IOError as e:
            print(f"Warning: Could not save state: {e}")

    def fetch_power_system_records(self, limit: int = 5) -> List[dict]:
        """Fetch raw records from the PowerSystemRightNow endpoint."""
        url = build_power_system_url(limit)
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("records", [])
        except Exception as err:
            print(f"Error fetching PowerSystemRightNow: {err}")
            return []

    def fetch_spot_price_records(self, limit: int = 100) -> List[dict]:
        """Fetch raw records from the ElspotPrices endpoint."""
        url = build_spot_prices_url(limit)
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("records", [])
        except Exception as err:
            print(f"Error fetching ElspotPrices: {err}")
            return []

    def poll_and_send(self, once: bool = False):
        """Main polling loop."""
        print(f"Starting Energi Data Service poller")
        print(f"  PowerSystem URL: {POWER_SYSTEM_URL}")
        print(f"  SpotPrices URL: {SPOT_PRICES_URL}")
        print(f"  Kafka topic: {self.kafka_topic}")

        last_spot_poll = 0.0

        while True:
            try:
                state = self.load_state()
                new_count = 0

                # Poll power system snapshots (records are newest-first)
                records = self.fetch_power_system_records(limit=5)
                if records:
                    latest = records[0]
                    ts = latest.get("Minutes1UTC")
                    if ts != state.get("last_power_system_timestamp"):
                        snapshot = map_power_system_record(latest)
                        self.producer.send_dk_energinet_energidataservice_power_system_snapshot(
                            snapshot.price_area, snapshot, flush_producer=False)
                        state["last_power_system_timestamp"] = ts
                        new_count += 1

                # Poll spot prices at a slower cadence
                now = time.time()
                if now - last_spot_poll >= SPOT_PRICES_POLL_INTERVAL or last_spot_poll == 0.0:
                    spot_records = self.fetch_spot_price_records(limit=100)
                    spot_timestamps = state.get("last_spot_price_timestamps", {})
                    for record in spot_records:
                        area = record.get("PriceArea", "")
                        hour = record.get("HourUTC", "")
                        dedup_key = f"{area}_{hour}"
                        if dedup_key in spot_timestamps:
                            continue
                        price = map_spot_price_record(record)
                        self.producer.send_dk_energinet_energidataservice_spot_price(
                            price.price_area, price, flush_producer=False)
                        spot_timestamps[dedup_key] = hour
                        new_count += 1
                    state["last_spot_price_timestamps"] = spot_timestamps
                    last_spot_poll = now

                if new_count > 0:
                    self.producer.producer.flush()
                    print(f"Sent {new_count} new event(s) to Kafka")

                self.save_state(state)

            except Exception as e:
                print(f"Error in polling loop: {e}")

            if once:
                break

            time.sleep(POWER_SYSTEM_POLL_INTERVAL)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse an Azure Event Hubs-style connection string and extract Kafka parameters.
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
    """Main function to parse arguments and start the poller."""
    parser = argparse.ArgumentParser(description="Energi Data Service (Energinet) Bridge")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store last seen timestamps")
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
        args.last_polled_file = os.getenv('EDS_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.eds_last_polled.json')

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

    poller = EnergiDataServicePoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file
    )
    poller.poll_and_send()
