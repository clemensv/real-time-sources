"""
UK Environment Agency Flood Monitoring Poller
Polls the EA Flood Monitoring API and sends readings to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
import logging
from typing import Dict, List, Any
import argparse
import requests
from uk_ea_flood_monitoring_producer_data.uk.gov.environment.ea.floodmonitoring.station import Station
from uk_ea_flood_monitoring_producer_data.uk.gov.environment.ea.floodmonitoring.reading import Reading
from uk_ea_flood_monitoring_producer_kafka_producer.producer import UKGovEnvironmentEAFloodMonitoringEventProducer

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


class EAFloodMonitoringAPI:
    """
    Polls the UK Environment Agency Flood Monitoring API and sends data to Kafka as CloudEvents.
    """
    STATIONS_URL = "https://environment.data.gov.uk/flood-monitoring/id/stations"
    READINGS_URL = "https://environment.data.gov.uk/flood-monitoring/data/readings"
    POLL_INTERVAL_SECONDS = 900  # 15 minutes

    def __init__(self):
        self.session = requests.Session()
        self.measure_to_station: Dict[str, str] = {}

    def list_stations(self) -> List[Dict[str, Any]]:
        """Fetch all monitoring stations."""
        response = self.session.get(
            self.STATIONS_URL,
            params={"_limit": 10000},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])

    def get_latest_readings(self) -> List[Dict[str, Any]]:
        """Fetch latest readings for all measures."""
        response = self.session.get(
            self.READINGS_URL,
            params={"latest": ""},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])

    def build_measure_map(self, stations: List[Dict[str, Any]]) -> Dict[str, str]:
        """Build a mapping from measure URI to station reference."""
        measure_map: Dict[str, str] = {}
        for station in stations:
            station_ref = station.get("stationReference", station.get("notation", ""))
            measures = station.get("measures", [])
            if isinstance(measures, list):
                for m in measures:
                    measure_id = m.get("@id", "")
                    if measure_id:
                        measure_map[measure_id] = station_ref
            elif isinstance(measures, dict):
                measure_id = measures.get("@id", "")
                if measure_id:
                    measure_map[measure_id] = station_ref
        return measure_map

    def parse_connection_string(self, connection_string: str) -> Dict[str, str]:
        """
        Parse the connection string and extract bootstrap server, topic name, username, and password.

        Args:
            connection_string (str): The connection string.

        Returns:
            Dict[str, str]: Extracted connection parameters.
        """
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
        previous_readings: Dict[str, str] = _load_state(state_file)

        from confluent_kafka import Producer
        producer = Producer(kafka_config)
        ea_producer = UKGovEnvironmentEAFloodMonitoringEventProducer(producer, kafka_topic)

        logging.info("Starting to feed stations to Kafka topic %s at bootstrap servers %s",
                      kafka_topic, kafka_config['bootstrap.servers'])

        # Fetch and send station reference data
        stations = self.list_stations()
        self.measure_to_station = self.build_measure_map(stations)

        for station in stations:
            station_ref = station.get("stationReference", station.get("notation", ""))
            raw_lat = station.get("lat", 0.0)
            raw_long = station.get("long", 0.0)
            if isinstance(raw_lat, list):
                raw_lat = raw_lat[0] if raw_lat else 0.0
            if isinstance(raw_long, list):
                raw_long = raw_long[0] if raw_long else 0.0
            station_data = Station(
                station_reference=station_ref,
                label=station.get("label", ""),
                river_name=station.get("riverName", ""),
                catchment_name=station.get("catchmentName", ""),
                town=station.get("town", ""),
                lat=raw_lat if raw_lat is not None else 0.0,
                long=raw_long if raw_long is not None else 0.0,
                notation=station.get("notation", ""),
                status=station.get("status", ""),
                date_opened=station.get("dateOpened", "")
            )
            ea_producer.send_uk_gov_environment_ea_flood_monitoring_station(
                station_ref, station_data, flush_producer=False)
        producer.flush()
        logging.info("Sent %d stations as reference data", len(stations))

        # Main polling loop
        while True:
            try:
                count = 0
                start_time = time.time()
                readings = self.get_latest_readings()

                for item in readings:
                    measure_uri = item.get("measure", "")
                    date_time = item.get("dateTime", "")
                    value = item.get("value")

                    if value is None or not isinstance(value, (int, float)):
                        continue

                    # Build a unique key for deduplication
                    reading_key = f"{measure_uri}:{date_time}"
                    if reading_key in previous_readings:
                        continue

                    # Resolve station reference from measure URI
                    station_ref = self.measure_to_station.get(measure_uri, "")
                    if not station_ref and "/" in measure_uri:
                        # Try extracting station ref from measure URI pattern
                        parts = measure_uri.split("/")
                        for i, part in enumerate(parts):
                            if part == "measures" and i + 1 < len(parts):
                                station_ref = parts[i + 1].split("-")[0]
                                break

                    reading_data = Reading(
                        station_reference=station_ref,
                        date_time=date_time,
                        measure=measure_uri,
                        value=float(value)
                    )

                    try:
                        ea_producer.send_uk_gov_environment_ea_flood_monitoring_reading(
                            station_ref, reading_data, flush_producer=False)
                        count += 1
                    # pylint: disable=broad-except
                    except Exception as e:
                        logging.error("Error sending reading to kafka: %s", e)
                    # pylint: enable=broad-except

                    previous_readings[reading_key] = date_time

                producer.flush()
                end_time = time.time()
                effective_interval = max(0, polling_interval - (end_time - start_time))
                logging.info("Sent %d readings in %.1f seconds. Waiting %.0f seconds.",
                             count, end_time - start_time, effective_interval)
                _save_state(state_file, previous_readings)
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
    """
    Interact with UK EA Flood Monitoring API to fetch water level data.
    Usage:
        python -m uk_ea_flood_monitoring list
        python -m uk_ea_flood_monitoring level <station_reference>
        python -m uk_ea_flood_monitoring feed --connection-string <connection_str>
    """
    parser = argparse.ArgumentParser(description='UK EA Flood Monitoring API bridge to Kafka')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list', help='List all available stations')

    level_parser = subparsers.add_parser('level', help='Get latest readings for a station')
    level_parser.add_argument('station_reference', type=str, help='Station reference ID')

    feed_parser = subparsers.add_parser('feed', help='Feed readings as CloudEvents to Kafka')
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str,
                             help="Comma separated list of Kafka bootstrap servers",
                             default=os.getenv('KAFKA_BOOTSTRAP_SERVERS'))
    feed_parser.add_argument('--kafka-topic', type=str,
                             help="Kafka topic to send messages to",
                             default=os.getenv('KAFKA_TOPIC'))
    feed_parser.add_argument('--sasl-username', type=str,
                             help="Username for SASL PLAIN authentication",
                             default=os.getenv('SASL_USERNAME'))
    feed_parser.add_argument('--sasl-password', type=str,
                             help="Password for SASL PLAIN authentication",
                             default=os.getenv('SASL_PASSWORD'))
    feed_parser.add_argument('-c', '--connection-string', type=str,
                             help='Microsoft Event Hubs or Fabric Event Stream connection string',
                             default=os.getenv('CONNECTION_STRING'))
    polling_interval_default = 900
    if os.getenv('POLLING_INTERVAL'):
        polling_interval_default = int(os.getenv('POLLING_INTERVAL'))
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             help='Polling interval in seconds (default: 900)',
                             default=polling_interval_default)
    feed_parser.add_argument('--state-file', type=str,
                             default=os.getenv('STATE_FILE', os.path.expanduser('~/.uk_ea_flood_monitoring_state.json')))

    args = parser.parse_args()

    api = EAFloodMonitoringAPI()

    if args.command == 'list':
        stations = api.list_stations()
        for station in stations:
            ref = station.get('stationReference', station.get('notation', ''))
            label = station.get('label', '')
            river = station.get('riverName', '')
            print(f"{ref}: {label} ({river})")
    elif args.command == 'level':
        response = api.session.get(
            f"{api.STATIONS_URL}/{args.station_reference}/readings",
            params={"latest": ""},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data.get("items", []), indent=4))
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
