"""Bridge between the Nepal BIPAD Portal river monitoring API and Kafka endpoints."""

from datetime import datetime, timedelta, timezone
import os
from typing import Any, List, Dict, Optional
import logging
import sys
import time
import argparse
import json
import requests

from confluent_kafka import Producer
from nepal_bipad_hydrology_producer_data.np.gov.bipad.hydrology.riverstation import RiverStation
from nepal_bipad_hydrology_producer_data.np.gov.bipad.hydrology.waterlevelreading import WaterLevelReading
from nepal_bipad_hydrology_producer_kafka_producer.producer import NpGovBipadHydrologyEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

BIPAD_API_BASE = "https://bipadportal.gov.np/api/v1"
DEFAULT_PAGE_SIZE = 100


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
    """Save dedup state to a JSON file."""
    if not state_file:
        return
    try:
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception as e:
        logging.warning("Could not save state to %s: %s", state_file, e)


class NepalBipadHydrologyAPI:
    """Client for the Nepal BIPAD Portal river-stations REST API."""

    def __init__(self, base_url: str = BIPAD_API_BASE, page_size: int = DEFAULT_PAGE_SIZE):
        self.base_url = base_url.rstrip('/')
        self.page_size = page_size
        self.session = requests.Session()

    def fetch_all_stations(self) -> List[Dict[str, Any]]:
        """Fetch all river stations by paginating until the results array is empty.

        The API returns count=9223372036854775807 (max long), so we cannot
        trust it.  Instead we paginate until the results list is empty.
        """
        all_stations: List[Dict[str, Any]] = []
        offset = 0
        while True:
            url = f"{self.base_url}/river-stations/?format=json&limit={self.page_size}&offset={offset}"
            logging.debug("Fetching %s", url)
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            if not results:
                break
            all_stations.extend(results)
            offset += self.page_size
        return all_stations

    @staticmethod
    def parse_station(raw: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize a raw API station record into schema-compatible fields."""
        point = raw.get("point") or {}
        coords = point.get("coordinates", [0.0, 0.0])
        longitude = float(coords[0]) if len(coords) > 0 else 0.0
        latitude = float(coords[1]) if len(coords) > 1 else 0.0

        return {
            "station_id": str(raw.get("id", "")),
            "title": raw.get("title", ""),
            "basin": raw.get("basin", ""),
            "latitude": latitude,
            "longitude": longitude,
            "elevation": raw.get("elevation"),
            "danger_level": raw.get("dangerLevel"),
            "warning_level": raw.get("warningLevel"),
            "description": raw.get("description"),
            "data_source": raw.get("dataSource", ""),
            "province": raw.get("province"),
            "district": raw.get("district"),
            "municipality": raw.get("municipality"),
            "ward": raw.get("ward"),
        }

    @staticmethod
    def parse_reading(raw: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize a raw API station record into a water-level reading."""
        return {
            "station_id": str(raw.get("id", "")),
            "title": raw.get("title", ""),
            "basin": raw.get("basin", ""),
            "water_level": raw.get("waterLevel"),
            "danger_level": raw.get("dangerLevel"),
            "warning_level": raw.get("warningLevel"),
            "status": raw.get("status", "BELOW WARNING LEVEL"),
            "trend": raw.get("steady", "STEADY"),
            "water_level_on": raw.get("waterLevelOn", ""),
        }

    def parse_connection_string(self, connection_string: str) -> Dict[str, str]:
        """Parse the connection string and extract bootstrap server, topic name, username, and password."""
        config_dict: Dict[str, str] = {}
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').strip().replace('sb://', '').replace('/', '') + ':9093'
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

    def feed_stations(self, kafka_config: dict, kafka_topic: str,
                      polling_interval: int, state_file: str = '',
                      reference_refresh_hours: int = 6) -> None:
        """Fetch stations, emit reference data and telemetry in a loop."""
        previous_readings: Dict[str, str] = _load_state(state_file)

        producer = Producer(kafka_config)
        event_producer = NpGovBipadHydrologyEventProducer(producer, kafka_topic)
        feed_url = f"{self.base_url}/river-stations/?format=json"

        logging.info("Starting Nepal BIPAD hydrology bridge to topic %s at %s",
                      kafka_topic, kafka_config.get('bootstrap.servers', ''))

        last_reference_emit = datetime.min.replace(tzinfo=timezone.utc)

        while True:
            try:
                start_time = datetime.now(timezone.utc)
                raw_stations = self.fetch_all_stations()
                logging.info("Fetched %d stations from BIPAD API", len(raw_stations))

                # Emit reference data if due
                if (start_time - last_reference_emit).total_seconds() >= reference_refresh_hours * 3600:
                    for raw in raw_stations:
                        parsed = self.parse_station(raw)
                        station_data = RiverStation(
                            station_id=parsed["station_id"],
                            title=parsed["title"],
                            basin=parsed["basin"],
                            latitude=parsed["latitude"],
                            longitude=parsed["longitude"],
                            elevation=parsed["elevation"],
                            danger_level=parsed["danger_level"],
                            warning_level=parsed["warning_level"],
                            description=parsed["description"],
                            data_source=parsed["data_source"],
                            province=parsed["province"],
                            district=parsed["district"],
                            municipality=parsed["municipality"],
                            ward=parsed["ward"],
                        )
                        event_producer.send_np_gov_bipad_hydrology_river_station(
                            _feedurl=feed_url,
                            _station_id=parsed["station_id"],
                            data=station_data,
                            flush_producer=False,
                        )
                    producer.flush()
                    last_reference_emit = start_time
                    logging.info("Emitted reference data for %d stations", len(raw_stations))

                # Emit telemetry
                count = 0
                for raw in raw_stations:
                    parsed = self.parse_reading(raw)
                    sid = parsed["station_id"]
                    wl_on = parsed["water_level_on"]

                    # Dedup by station_id + water_level_on
                    dedup_key = f"{sid}:{wl_on}"
                    if dedup_key == previous_readings.get(sid):
                        continue

                    try:
                        reading_data = WaterLevelReading(
                            station_id=parsed["station_id"],
                            title=parsed["title"],
                            basin=parsed["basin"],
                            water_level=parsed["water_level"],
                            danger_level=parsed["danger_level"],
                            warning_level=parsed["warning_level"],
                            status=parsed["status"],
                            trend=parsed["trend"],
                            water_level_on=parsed["water_level_on"],
                        )
                        event_producer.send_np_gov_bipad_hydrology_water_level_reading(
                            _feedurl=feed_url,
                            _station_id=parsed["station_id"],
                            data=reading_data,
                            flush_producer=False,
                        )
                        count += 1
                        previous_readings[sid] = dedup_key
                    except Exception as e:
                        logging.error("Error sending reading for station %s: %s", sid, e)

                producer.flush()
                end_time = datetime.now(timezone.utc)
                _save_state(state_file, previous_readings)

                effective_interval = max(0, polling_interval - (end_time - start_time).total_seconds())
                logging.info("Sent %d water level readings in %.1fs. Sleeping %.0fs.",
                              count, (end_time - start_time).total_seconds(), effective_interval)
                if effective_interval > 0:
                    time.sleep(effective_interval)
            except KeyboardInterrupt:
                logging.info("Exiting...")
                break
            except Exception as e:
                logging.error("Error occurred: %s", e)
                logging.info("Retrying in %d seconds...", polling_interval)
                time.sleep(polling_interval)

        producer.flush()


def main() -> None:
    """CLI entry point for the Nepal BIPAD hydrology bridge."""
    parser = argparse.ArgumentParser(
        description='Bridge between Nepal BIPAD Portal river monitoring API and Kafka.')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list', help='List all river stations')

    feed_parser = subparsers.add_parser('feed', help='Feed stations and send updates as CloudEvents')
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
    polling_interval_default = 900  # 15 minutes
    if os.getenv('POLLING_INTERVAL'):
        polling_interval_default = int(os.getenv('POLLING_INTERVAL'))
    feed_parser.add_argument('-i', '--polling-interval', type=int,
                             help='Polling interval in seconds (default: 900)',
                             default=polling_interval_default)
    feed_parser.add_argument('--state-file', type=str,
                             default=os.getenv('STATE_FILE',
                                               os.path.expanduser('~/.nepal_bipad_hydrology_state.json')))

    args = parser.parse_args()
    api = NepalBipadHydrologyAPI()

    if args.command == 'list':
        stations = api.fetch_all_stations()
        for s in stations:
            parsed = api.parse_station(s)
            print(f"{parsed['station_id']}: {parsed['title']} ({parsed['basin']})")
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

        api.feed_stations(kafka_config, kafka_topic, args.polling_interval, args.state_file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
