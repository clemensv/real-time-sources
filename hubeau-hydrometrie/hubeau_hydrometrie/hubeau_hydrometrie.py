"""
Hub'Eau Hydrométrie Poller
Polls the French Hub'Eau Hydrométrie API and sends observations to Kafka as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any
import argparse
import requests
from hubeau_hydrometrie.hubeau_hydrometrie_producer.fr.gov.eaufrance.hubeau.hydrometrie.station import Station
from hubeau_hydrometrie.hubeau_hydrometrie_producer.fr.gov.eaufrance.hubeau.hydrometrie.observation import Observation
from .hubeau_hydrometrie_producer.producer_client import FRGovEaufranceHubEauHydrometrieEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def _load_state(state_file: str) -> dict:
    """Load persisted dedup state from a JSON file."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logging.warning("Could not load state from %s: %s", state_file, e)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    """Save dedup state to a JSON file, keeping at most 100000 entries."""
    if not state_file:
        return
    try:
        if len(data) > 100000:
            keys = list(data.keys())
            data = {k: data[k] for k in keys[-50000:]}
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception as e:
        logging.warning("Could not save state to %s: %s", state_file, e)


class HubEauHydrometrieAPI:
    """
    Polls the Hub'Eau Hydrométrie API and sends data to Kafka as CloudEvents.
    """
    BASE_URL = "https://hubeau.eaufrance.fr/api/v2/hydrometrie"
    STATIONS_URL = f"{BASE_URL}/referentiel/stations"
    OBSERVATIONS_URL = f"{BASE_URL}/observations_tr"
    POLL_INTERVAL_SECONDS = 300  # 5 minutes

    def __init__(self):
        self.session = requests.Session()

    def list_stations(self) -> List[Dict[str, Any]]:
        """Fetch all monitoring stations with pagination."""
        stations = []
        page = 1
        page_size = 500
        while True:
            response = self.session.get(
                self.STATIONS_URL,
                params={"format": "json", "size": page_size, "page": page},
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            items = data.get("data", [])
            if not items:
                break
            stations.extend(items)
            if data.get("next") is None:
                break
            page += 1
        return stations

    def get_latest_observations(self) -> List[Dict[str, Any]]:
        """Fetch latest real-time observations using cursor pagination."""
        observations = []
        url = self.OBSERVATIONS_URL
        params = {"format": "json", "size": 1000}
        max_pages = 5  # Limit to prevent excessive API calls
        page_count = 0
        while url and page_count < max_pages:
            response = self.session.get(url, params=params if page_count == 0 else None, timeout=60)
            response.raise_for_status()
            data = response.json()
            items = data.get("data", [])
            if not items:
                break
            observations.extend(items)
            url = data.get("next")
            params = None  # Next URL already has params
            page_count += 1
        return observations

    def parse_connection_string(self, connection_string: str) -> Dict[str, str]:
        """Parse an Event Hubs connection string."""
        config_dict = {}
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').strip().replace('sb://', '').replace('/', '')+':9093'
                elif 'EntityPath' in part:
                    config_dict['kafka_topic'] = part.split('=')[1].strip('"').strip()
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

    def feed_stations(self, kafka_config: dict, kafka_topic: str, polling_interval: int, state_file: str = '') -> None:
        """Feed stations and send updates as CloudEvents."""
        previous_observations: Dict[str, str] = _load_state(state_file)

        from confluent_kafka import Producer
        producer = Producer(kafka_config)
        hubeau_producer = FRGovEaufranceHubEauHydrometrieEventProducer(producer, kafka_topic)

        logging.info("Starting to feed stations to Kafka topic %s", kafka_topic)

        # Fetch and send station reference data
        stations = self.list_stations()
        for station in stations:
            station_data = Station(
                code_station=station.get("code_station", ""),
                libelle_station=station.get("libelle_station", ""),
                code_site=station.get("code_site", ""),
                longitude_station=station.get("longitude_station", 0.0) or 0.0,
                latitude_station=station.get("latitude_station", 0.0) or 0.0,
                libelle_cours_eau=station.get("libelle_cours_eau", "") or "",
                libelle_commune=station.get("libelle_commune", "") or "",
                code_departement=station.get("code_departement", "") or "",
                en_service=station.get("en_service", False) or False,
                date_ouverture_station=station.get("date_ouverture_station", "") or ""
            )
            hubeau_producer.send_fr_gov_eaufrance_hubeau_hydrometrie_station(
                station_data, flush_producer=False)
        producer.flush()
        logging.info("Sent %d stations as reference data", len(stations))

        # Main polling loop
        while True:
            try:
                count = 0
                start_time = time.time()
                observations = self.get_latest_observations()

                for obs in observations:
                    code_station = obs.get("code_station", "")
                    date_obs = obs.get("date_obs", "")
                    grandeur_hydro = obs.get("grandeur_hydro", "")

                    obs_key = f"{code_station}:{grandeur_hydro}:{date_obs}"
                    if obs_key in previous_observations:
                        continue

                    resultat = obs.get("resultat_obs")
                    if resultat is None:
                        continue

                    obs_data = Observation(
                        code_station=code_station,
                        date_obs=date_obs,
                        resultat_obs=float(resultat),
                        grandeur_hydro=grandeur_hydro,
                        libelle_methode_obs=obs.get("libelle_methode_obs", "") or "",
                        libelle_qualification_obs=obs.get("libelle_qualification_obs", "") or ""
                    )

                    try:
                        hubeau_producer.send_fr_gov_eaufrance_hubeau_hydrometrie_observation(
                            obs_data, flush_producer=False)
                        count += 1
                    # pylint: disable=broad-except
                    except Exception as e:
                        logging.error("Error sending observation to kafka: %s", e)
                    # pylint: enable=broad-except

                    previous_observations[obs_key] = date_obs

                producer.flush()
                end_time = time.time()
                effective_interval = max(0, polling_interval - (end_time - start_time))
                logging.info("Sent %d observations in %.1f seconds. Waiting %.0f seconds.",
                             count, end_time - start_time, effective_interval)
                _save_state(state_file, previous_observations)
                if effective_interval > 0:
                    time.sleep(effective_interval)

            except KeyboardInterrupt:
                logging.info("Exiting...")
                break
            # pylint: disable=broad-except
            except Exception as e:
                logging.error("Error occurred: %s", e)
                logging.info("Retrying in %d seconds...", polling_interval)
                time.sleep(polling_interval)
            # pylint: enable=broad-except
        producer.flush()


def main() -> None:
    """Main entry point for Hub'Eau Hydrométrie bridge."""
    parser = argparse.ArgumentParser(description='Hub\'Eau Hydrométrie API bridge to Kafka')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list', help='List all available stations')

    level_parser = subparsers.add_parser('level', help='Get latest observations for a station')
    level_parser.add_argument('code_station', type=str, help='Station code')

    feed_parser = subparsers.add_parser('feed', help='Feed observations as CloudEvents to Kafka')
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str,
                             default=os.getenv('KAFKA_BOOTSTRAP_SERVERS'))
    feed_parser.add_argument('--kafka-topic', type=str, default=os.getenv('KAFKA_TOPIC'))
    feed_parser.add_argument('--sasl-username', type=str, default=os.getenv('SASL_USERNAME'))
    feed_parser.add_argument('--sasl-password', type=str, default=os.getenv('SASL_PASSWORD'))
    feed_parser.add_argument('-c', '--connection-string', type=str,
                             default=os.getenv('CONNECTION_STRING'))
    polling_interval_default = 300
    if os.getenv('POLLING_INTERVAL'):
        polling_interval_default = int(os.getenv('POLLING_INTERVAL'))
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=polling_interval_default)
    feed_parser.add_argument('--state-file', type=str,
                             default=os.getenv('STATE_FILE', os.path.expanduser('~/.hubeau_hydrometrie_state.json')))

    args = parser.parse_args()
    api = HubEauHydrometrieAPI()

    if args.command == 'list':
        stations = api.list_stations()
        for s in stations:
            code = s.get('code_station', '')
            label = s.get('libelle_station', '')
            river = s.get('libelle_cours_eau', '')
            print(f"{code}: {label} ({river})")
    elif args.command == 'level':
        response = api.session.get(
            api.OBSERVATIONS_URL,
            params={"code_entite": args.code_station, "size": 10, "format": "json"},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data.get("data", []), indent=4))
    elif args.command == 'feed':
        if args.connection_string:
            config_params = api.parse_connection_string(args.connection_string)
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
        api.feed_stations(kafka_config, kafka_topic, args.polling_interval, args.state_file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
