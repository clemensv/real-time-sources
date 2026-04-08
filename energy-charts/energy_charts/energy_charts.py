"""
Energy-Charts (Fraunhofer ISE) Bridge
Polls European electricity generation, price, and grid carbon signal data
and sends it to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
import re
from typing import Dict, List, Optional, Set
from datetime import datetime, timezone
import argparse
import requests
from energy_charts_producer_data import PublicPower, SpotPrice, GridSignal
from energy_charts_producer_kafka_producer.producer import InfoEnergyChartsEventProducer

# Map API production type names to schema field names
PRODUCTION_TYPE_MAP = {
    "Hydro pumped storage consumption": "hydro_pumped_storage_consumption_mw",
    "Cross border electricity trading": "cross_border_electricity_trading_mw",
    "Hydro Run-of-River": "hydro_run_of_river_mw",
    "Biomass": "biomass_mw",
    "Fossil brown coal / lignite": "fossil_brown_coal_lignite_mw",
    "Fossil hard coal": "fossil_hard_coal_mw",
    "Fossil oil": "fossil_oil_mw",
    "Fossil coal-derived gas": "fossil_coal_derived_gas_mw",
    "Fossil gas": "fossil_gas_mw",
    "Geothermal": "geothermal_mw",
    "Hydro water reservoir": "hydro_water_reservoir_mw",
    "Hydro pumped storage": "hydro_pumped_storage_mw",
    "Others": "others_mw",
    "Waste": "waste_mw",
    "Wind offshore": "wind_offshore_mw",
    "Wind onshore": "wind_onshore_mw",
    "Solar": "solar_mw",
    "Nuclear": "nuclear_mw",
    "Load": "load_mw",
    "Residual load": "residual_load_mw",
    "Renewable share of generation": "renewable_share_of_generation_pct",
    "Renewable share of load": "renewable_share_of_load_pct",
}

API_BASE = "https://api.energy-charts.info"


class EnergyChartsPoller:
    """
    Polls the Energy-Charts API for electricity generation, prices, and grid
    carbon signals, and sends them to Kafka as CloudEvents.
    """
    POWER_POLL_INTERVAL = 900    # 15 minutes
    PRICE_POLL_INTERVAL = 3600   # 1 hour
    SIGNAL_POLL_INTERVAL = 900   # 15 minutes

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str,
                 country: str = "de", bidding_zone: str = "DE-LU",
                 last_polled_file: str = ""):
        """
        Initialize the EnergyChartsPoller.

        Args:
            kafka_config: Kafka producer configuration.
            kafka_topic: Kafka topic for events.
            country: ISO 3166-1 alpha-2 country code (default: 'de').
            bidding_zone: ENTSO-E bidding zone for price queries (default: 'DE-LU').
            last_polled_file: Path to state file for deduplication.
        """
        self.country = country.lower()
        self.bidding_zone = bidding_zone
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

        from confluent_kafka import Producer
        kafka_producer = Producer(kafka_config)
        self.producer = InfoEnergyChartsEventProducer(kafka_producer, kafka_topic)

        self._seen_power: Set[int] = set()
        self._seen_price: Set[int] = set()
        self._seen_signal: Set[int] = set()
        self._load_state()

    # ------------------------------------------------------------------
    # State persistence for deduplication
    # ------------------------------------------------------------------

    def _load_state(self):
        """Load previously seen timestamps from the state file."""
        if self.last_polled_file and os.path.isfile(self.last_polled_file):
            try:
                with open(self.last_polled_file, "r", encoding="utf-8") as f:
                    state = json.load(f)
                self._seen_power = set(state.get("power", []))
                self._seen_price = set(state.get("price", []))
                self._seen_signal = set(state.get("signal", []))
            except (json.JSONDecodeError, OSError) as exc:
                print(f"Warning: could not load state file: {exc}")

    def _save_state(self):
        """Persist seen timestamps to the state file."""
        if not self.last_polled_file:
            return
        try:
            state = {
                "power": sorted(self._seen_power)[-500:] if self._seen_power else [],
                "price": sorted(self._seen_price)[-500:] if self._seen_price else [],
                "signal": sorted(self._seen_signal)[-500:] if self._seen_signal else [],
            }
            os.makedirs(os.path.dirname(self.last_polled_file) or ".", exist_ok=True)
            with open(self.last_polled_file, "w", encoding="utf-8") as f:
                json.dump(state, f)
        except OSError as exc:
            print(f"Warning: could not save state file: {exc}")

    # ------------------------------------------------------------------
    # API fetch helpers
    # ------------------------------------------------------------------

    @staticmethod
    def fetch_public_power(session: requests.Session, country: str) -> dict:
        """Fetch the /public_power endpoint for a given country."""
        url = f"{API_BASE}/public_power?country={country}"
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def fetch_price(session: requests.Session, bidding_zone: str) -> dict:
        """Fetch the /price endpoint for a given bidding zone."""
        url = f"{API_BASE}/price?bzn={bidding_zone}"
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def fetch_signal(session: requests.Session, country: str) -> dict:
        """Fetch the /signal endpoint for a given country."""
        url = f"{API_BASE}/signal?country={country}"
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Parsing / transformation
    # ------------------------------------------------------------------

    @staticmethod
    def parse_public_power(raw: dict, country: str) -> List[PublicPower]:
        """
        Transform the parallel-array /public_power response into a list
        of PublicPower data-class instances, one per timestamp.
        """
        unix_seconds_list = raw.get("unix_seconds", [])
        production_types = raw.get("production_types", [])

        # Build a mapping: field_name -> data array
        field_arrays: Dict[str, list] = {}
        for pt in production_types:
            name = pt.get("name", "")
            field_name = PRODUCTION_TYPE_MAP.get(name)
            if field_name and "data" in pt:
                field_arrays[field_name] = pt["data"]

        results: List[PublicPower] = []
        for i, ts in enumerate(unix_seconds_list):
            kwargs: Dict[str, object] = {
                "country": country,
                "timestamp": datetime.fromtimestamp(ts, tz=timezone.utc),
                "unix_seconds": ts,
            }
            for field_name, arr in field_arrays.items():
                kwargs[field_name] = arr[i] if i < len(arr) else None

            # Fill missing nullable fields with None
            for fn in PRODUCTION_TYPE_MAP.values():
                if fn not in kwargs:
                    kwargs[fn] = None

            results.append(PublicPower(**kwargs))
        return results

    @staticmethod
    def parse_price(raw: dict, country: str, bidding_zone: str) -> List[SpotPrice]:
        """
        Transform the /price response into a list of SpotPrice instances.
        """
        unix_seconds_list = raw.get("unix_seconds", [])
        prices = raw.get("price", [])
        unit_label = raw.get("unit")
        results: List[SpotPrice] = []
        for i, ts in enumerate(unix_seconds_list):
            price_val = prices[i] if i < len(prices) else None
            results.append(SpotPrice(
                country=country,
                bidding_zone=bidding_zone,
                timestamp=datetime.fromtimestamp(ts, tz=timezone.utc),
                unix_seconds=ts,
                price_eur_per_mwh=price_val,
                unit=unit_label,
            ))
        return results

    @staticmethod
    def parse_signal(raw: dict, country: str) -> List[GridSignal]:
        """
        Transform the /signal response into a list of GridSignal instances.
        """
        unix_seconds_list = raw.get("unix_seconds", [])
        shares = raw.get("share", [])
        signals = raw.get("signal", [])
        substitute_val = raw.get("substitute", None)
        results: List[GridSignal] = []
        for i, ts in enumerate(unix_seconds_list):
            sig = signals[i] if i < len(signals) else None
            share = shares[i] if i < len(shares) else None
            sub = substitute_val if isinstance(substitute_val, bool) else None
            # dataclasses_json converts falsy Optional values (0, False) to
            # None during __init__. Use object.__setattr__ to preserve them.
            rec = GridSignal(
                country=country,
                timestamp=datetime.fromtimestamp(ts, tz=timezone.utc),
                unix_seconds=ts,
                signal=sig if sig else None,
                renewable_share_pct=share,
                substitute=sub if sub else None,
            )
            if sig is not None:
                object.__setattr__(rec, 'signal', sig)
            if sub is not None:
                object.__setattr__(rec, 'substitute', sub)
            results.append(rec)
        return results

    # ------------------------------------------------------------------
    # Emit helpers
    # ------------------------------------------------------------------

    def emit_public_power(self) -> int:
        """Fetch, parse, deduplicate, and emit PublicPower events. Returns count."""
        try:
            raw = self.fetch_public_power(self.session, self.country)
        except Exception as exc:
            print(f"Error fetching public_power: {exc}")
            return 0
        records = self.parse_public_power(raw, self.country)
        count = 0
        for rec in records:
            if rec.unix_seconds in self._seen_power:
                continue
            self.producer.send_info_energy_charts_public_power(
                _country=rec.country, data=rec, flush_producer=False
            )
            self._seen_power.add(rec.unix_seconds)
            count += 1
        if count > 0:
            self.producer.producer.flush()
            print(f"Emitted {count} PublicPower events for {self.country}")
        return count

    def emit_price(self) -> int:
        """Fetch, parse, deduplicate, and emit SpotPrice events. Returns count."""
        try:
            raw = self.fetch_price(self.session, self.bidding_zone)
        except Exception as exc:
            print(f"Error fetching price: {exc}")
            return 0
        records = self.parse_price(raw, self.country, self.bidding_zone)
        count = 0
        for rec in records:
            if rec.unix_seconds in self._seen_price:
                continue
            self.producer.send_info_energy_charts_spot_price(
                _country=rec.country, data=rec, flush_producer=False
            )
            self._seen_price.add(rec.unix_seconds)
            count += 1
        if count > 0:
            self.producer.producer.flush()
            print(f"Emitted {count} SpotPrice events for {self.bidding_zone}")
        return count

    def emit_signal(self) -> int:
        """Fetch, parse, deduplicate, and emit GridSignal events. Returns count."""
        try:
            raw = self.fetch_signal(self.session, self.country)
        except Exception as exc:
            print(f"Error fetching signal: {exc}")
            return 0
        records = self.parse_signal(raw, self.country)
        count = 0
        for rec in records:
            if rec.unix_seconds in self._seen_signal:
                continue
            self.producer.send_info_energy_charts_grid_signal(
                _country=rec.country, data=rec, flush_producer=False
            )
            self._seen_signal.add(rec.unix_seconds)
            count += 1
        if count > 0:
            self.producer.producer.flush()
            print(f"Emitted {count} GridSignal events for {self.country}")
        return count

    # ------------------------------------------------------------------
    # Main polling loop
    # ------------------------------------------------------------------

    def poll_and_send(self, once: bool = False):
        """
        Main polling loop. Polls all three endpoints at their respective
        intervals. If `once` is True, runs a single cycle and exits.
        """
        last_power = 0.0
        last_price = 0.0
        last_signal = 0.0

        while True:
            now = time.time()
            try:
                if now - last_power >= self.POWER_POLL_INTERVAL:
                    self.emit_public_power()
                    last_power = now

                if now - last_signal >= self.SIGNAL_POLL_INTERVAL:
                    self.emit_signal()
                    last_signal = now

                if now - last_price >= self.PRICE_POLL_INTERVAL:
                    self.emit_price()
                    last_price = now

                self._save_state()
            except Exception as exc:
                print(f"Error in polling loop: {exc}")

            if once:
                break

            # Sleep in short intervals so all timers are checked frequently
            time.sleep(60)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse an Azure Event Hubs-style connection string and extract Kafka
    parameters.

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
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc
    if 'sasl.username' in config_dict:
        config_dict['security.protocol'] = 'SASL_SSL'
        config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict


def main():
    """Main entry point for the Energy-Charts bridge."""
    parser = argparse.ArgumentParser(description="Energy-Charts Bridge")
    parser.add_argument('--kafka-bootstrap-servers', type=str,
                        help="Comma separated list of Kafka bootstrap servers")
    parser.add_argument('--kafka-topic', type=str,
                        help="Kafka topic to send messages to")
    parser.add_argument('--sasl-username', type=str,
                        help="Username for SASL PLAIN authentication")
    parser.add_argument('--sasl-password', type=str,
                        help="Password for SASL PLAIN authentication")
    parser.add_argument('--connection-string', type=str,
                        help="Azure Event Hubs or Fabric Event Stream connection string")
    parser.add_argument('--country', type=str,
                        help="ISO country code (default: de)")
    parser.add_argument('--bidding-zone', type=str,
                        help="ENTSO-E bidding zone (default: DE-LU)")
    parser.add_argument('--last-polled-file', type=str,
                        help="State file for deduplication")

    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.country:
        args.country = os.getenv('COUNTRY', 'de')
    if not args.bidding_zone:
        args.bidding_zone = os.getenv('BIDDING_ZONE', 'DE-LU')
    if not args.last_polled_file:
        args.last_polled_file = os.getenv('ENERGY_CHARTS_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser(
                '~/.energy_charts_last_polled.json'
            )

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = config_params.get('bootstrap.servers')
        kafka_topic = config_params.get('kafka_topic')
        sasl_username = config_params.get('sasl.username')
        sasl_password = config_params.get('sasl.password')
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers or os.getenv('KAFKA_BOOTSTRAP_SERVERS')
        kafka_topic = args.kafka_topic or os.getenv('KAFKA_TOPIC')
        sasl_username = args.sasl_username or os.getenv('SASL_USERNAME')
        sasl_password = args.sasl_password or os.getenv('SASL_PASSWORD')

    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided.")
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

    poller = EnergyChartsPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        country=args.country,
        bidding_zone=args.bidding_zone,
        last_polled_file=args.last_polled_file,
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
