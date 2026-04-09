"""
Elexon BMRS (GB Electricity Market) Bridge
Polls the Elexon BMRS API for generation mix and demand outturn data
and sends them to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
from typing import Dict, List, Optional
from datetime import datetime, timezone
import argparse
import requests
from elexon_bmrs_producer_data import GenerationMix, DemandOutturn
from elexon_bmrs_producer_kafka_producer.producer import UKCoElexonBMRSEventProducer


# Mapping from BMRS fuelType strings to GenerationMix field names
FUEL_TYPE_FIELD_MAP = {
    "BIOMASS": "biomass_mw",
    "CCGT": "ccgt_mw",
    "COAL": "coal_mw",
    "NUCLEAR": "nuclear_mw",
    "WIND": "wind_mw",
    "OCGT": "ocgt_mw",
    "OIL": "oil_mw",
    "NPSHYD": "npshyd_mw",
    "PS": "ps_mw",
    "INTFR": "intfr_mw",
    "INTNED": "intned_mw",
    "INTNEM": "intnem_mw",
    "INTELEC": "intelec_mw",
    "INTIFA2": "intifa2_mw",
    "INTNSL": "intnsl_mw",
    "INTVKL": "intvkl_mw",
    "OTHER": "other_mw",
}


class ElexonBMRSPoller:
    """
    Polls the Elexon BMRS API for generation mix and demand outturn data,
    then emits CloudEvents to a Kafka topic.
    """
    GENERATION_URL = "https://data.elexon.co.uk/bmrs/api/v1/generation/outturn/summary"
    DEMAND_URL = "https://data.elexon.co.uk/bmrs/api/v1/demand/outturn"
    POLL_INTERVAL_SECONDS = 1800  # 30 minutes

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str):
        """
        Initialize the ElexonBMRSPoller.

        Args:
            kafka_config: Kafka configuration settings.
            kafka_topic: Kafka topic to send messages to.
            last_polled_file: File to store last seen settlement period timestamps.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        from confluent_kafka import Producer
        kafka_producer = Producer(kafka_config)
        self.producer = UKCoElexonBMRSEventProducer(kafka_producer, kafka_topic)

    def load_state(self) -> Dict:
        """
        Load persisted state from disk.

        Returns:
            Dict with last seen timestamps per event type.
        """
        if not os.path.exists(self.last_polled_file):
            return {"generation": {}, "demand": {}}
        try:
            with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
            if not isinstance(state, dict):
                return {"generation": {}, "demand": {}}
            if "generation" not in state:
                state["generation"] = {}
            if "demand" not in state:
                state["demand"] = {}
            return state
        except (json.JSONDecodeError, IOError):
            return {"generation": {}, "demand": {}}

    def save_state(self, state: Dict) -> None:
        """
        Persist state to disk.

        Args:
            state: State dictionary to save.
        """
        try:
            state_dir = os.path.dirname(self.last_polled_file)
            if state_dir:
                os.makedirs(state_dir, exist_ok=True)
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save state: {e}")

    @staticmethod
    def parse_generation_response(data: list) -> List[GenerationMix]:
        """
        Parse the BMRS generation outturn summary response into GenerationMix data classes.

        Args:
            data: Parsed JSON list from the generation/outturn/summary endpoint.

        Returns:
            List of GenerationMix instances.
        """
        results = []
        if not isinstance(data, list):
            return results
        for record in data:
            if not isinstance(record, dict):
                continue
            settlement_period = record.get("settlementPeriod")
            start_time_str = record.get("startTime")
            if settlement_period is None or start_time_str is None:
                continue
            try:
                start_time = datetime.fromisoformat(start_time_str)
            except (ValueError, TypeError):
                continue

            fuel_values = {field: None for field in FUEL_TYPE_FIELD_MAP.values()}
            for fuel_entry in record.get("data", []):
                if not isinstance(fuel_entry, dict):
                    continue
                fuel_type = fuel_entry.get("fuelType", "").upper()
                generation = fuel_entry.get("generation")
                field_name = FUEL_TYPE_FIELD_MAP.get(fuel_type)
                if field_name:
                    fuel_values[field_name] = float(generation) if generation is not None else None

            mix = GenerationMix(
                settlement_period=int(settlement_period),
                start_time=start_time,
                **fuel_values,
            )
            results.append(mix)
        return results

    @staticmethod
    def parse_demand_response(data: dict) -> List[DemandOutturn]:
        """
        Parse the BMRS demand outturn response into DemandOutturn data classes.

        Args:
            data: Parsed JSON from the demand/outturn endpoint.

        Returns:
            List of DemandOutturn instances.
        """
        results = []
        records = data.get("data", []) if isinstance(data, dict) else data if isinstance(data, list) else []
        for record in records:
            if not isinstance(record, dict):
                continue
            settlement_period = record.get("settlementPeriod")
            settlement_date = record.get("settlementDate")
            start_time_str = record.get("startTime")
            if settlement_period is None or settlement_date is None or start_time_str is None:
                continue
            try:
                start_time = datetime.fromisoformat(start_time_str)
            except (ValueError, TypeError):
                continue

            publish_time = None
            pt_str = record.get("publishTime")
            if pt_str:
                try:
                    publish_time = datetime.fromisoformat(pt_str)
                except (ValueError, TypeError):
                    pass

            demand = DemandOutturn(
                settlement_period=int(settlement_period),
                settlement_date=str(settlement_date),
                start_time=start_time,
                publish_time=publish_time,
                initial_demand_outturn_mw=float(record["initialDemandOutturn"]) if record.get("initialDemandOutturn") is not None else None,
                initial_transmission_system_demand_outturn_mw=float(record["initialTransmissionSystemDemandOutturn"]) if record.get("initialTransmissionSystemDemandOutturn") is not None else None,
            )
            results.append(demand)
        return results

    def fetch_generation(self) -> Optional[list]:
        """
        Fetch generation outturn summary from the BMRS API.

        Returns:
            Parsed JSON list, or None on failure.
        """
        try:
            response = requests.get(self.GENERATION_URL, params={"format": "json"}, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching generation data: {e}")
            return None

    def fetch_demand(self) -> Optional[dict]:
        """
        Fetch demand outturn from the BMRS API.

        Returns:
            Parsed JSON dict, or None on failure.
        """
        try:
            response = requests.get(self.DEMAND_URL, params={"format": "json"}, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching demand data: {e}")
            return None

    def poll_and_send(self, once: bool = False) -> None:
        """
        Main polling loop. Fetches data from the BMRS API and emits CloudEvents.

        Args:
            once: If True, run only a single poll cycle.
        """
        while True:
            state = self.load_state()
            gen_sent = 0
            dem_sent = 0

            try:
                # Fetch and emit generation mix data
                gen_data = self.fetch_generation()
                if gen_data is not None:
                    mixes = self.parse_generation_response(gen_data)
                    for mix in mixes:
                        state_key = f"{mix.settlement_period}_{mix.start_time.isoformat()}"
                        if state_key not in state["generation"]:
                            self.producer.send_uk_co_elexon_bmrs_generation_mix(
                                _settlement_period=str(mix.settlement_period),
                                data=mix,
                                flush_producer=False,
                            )
                            state["generation"][state_key] = mix.start_time.isoformat()
                            gen_sent += 1
                    self.producer.producer.flush()

                # Fetch and emit demand outturn data
                dem_data = self.fetch_demand()
                if dem_data is not None:
                    demands = self.parse_demand_response(dem_data)
                    for demand in demands:
                        state_key = f"{demand.settlement_period}_{demand.start_time.isoformat()}"
                        if state_key not in state["demand"]:
                            self.producer.send_uk_co_elexon_bmrs_demand_outturn(
                                _settlement_period=str(demand.settlement_period),
                                data=demand,
                                flush_producer=False,
                            )
                            state["demand"][state_key] = demand.start_time.isoformat()
                            dem_sent += 1
                    self.producer.producer.flush()

                # Prune old state entries (keep last 200 per type)
                for key in ("generation", "demand"):
                    if len(state[key]) > 200:
                        sorted_keys = sorted(state[key].keys())
                        for old_key in sorted_keys[:-200]:
                            del state[key][old_key]

                self.save_state(state)
                print(f"Poll complete: sent {gen_sent} generation, {dem_sent} demand events")

            except Exception as e:
                print(f"Error in polling loop: {e}")

            if once:
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
    Main function to parse arguments and start the Elexon BMRS poller.
    """
    parser = argparse.ArgumentParser(description="Elexon BMRS (GB Electricity Market) Bridge")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store last seen settlement period timestamps")
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
        args.last_polled_file = os.getenv('BMRS_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.bmrs_last_polled.json')

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
            'sasl.password': sasl_password,
        })
    elif tls_enabled:
        kafka_config['security.protocol'] = 'SSL'

    poller = ElexonBMRSPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file,
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
