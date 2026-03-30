"""
Waterinfo VMM Poller
Polls the Belgian Waterinfo KIWIS API (VMM) and sends water level data to Kafka as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any
import argparse
import requests
from waterinfo_vmm.waterinfo_vmm_producer.be.vlaanderen.waterinfo.vmm.station import Station
from waterinfo_vmm.waterinfo_vmm_producer.be.vlaanderen.waterinfo.vmm.water_level_reading import WaterLevelReading
from .waterinfo_vmm_producer.producer_client import BEVlaanderenWaterinfoVMMEventProducer

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


class WaterinfoVMMAPI:
    """
    Polls the Waterinfo.be KIWIS API (VMM provider) and sends data to Kafka as CloudEvents.
    """
    BASE_URL = "https://download.waterinfo.be/tsmdownload/KiWIS/KiWIS"
    DEFAULT_PARAMS = {
        "service": "kisters",
        "type": "QueryServices",
        "format": "json",
        "datasource": "1",
        "timezone": "UTC",
    }
    WATER_LEVEL_15M_GROUP = "192780"
    POLL_INTERVAL_SECONDS = 900  # 15 minutes

    def __init__(self):
        self.session = requests.Session()

    def _kiwis_request(self, extra_params: Dict[str, str]) -> Any:
        """Make a request to the KIWIS API."""
        params = {**self.DEFAULT_PARAMS, **extra_params}
        response = self.session.get(self.BASE_URL, params=params, timeout=60)
        response.raise_for_status()
        return response.json()

    def list_stations(self) -> List[List[str]]:
        """Fetch all stations from VMM with key metadata."""
        data = self._kiwis_request({
            "request": "getStationList",
            "returnfields": "station_no,station_name,station_latitude,station_longitude,station_id,river_name",
        })
        # First row is headers, rest is data
        return data

    def get_latest_water_levels(self) -> List[Dict[str, Any]]:
        """Fetch the latest water level readings for all 15-min stations via getTimeseriesValueLayer."""
        data = self._kiwis_request({
            "request": "getTimeseriesValueLayer",
            "timeseriesgroup_id": self.WATER_LEVEL_15M_GROUP,
            "metadata": "true",
            "md_returnfields": "ts_id,ts_name,ts_shortname,station_no,station_id,station_name,stationparameter_name,ts_unitname",
        })
        return data

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
        """Feed station and water level data as CloudEvents to Kafka."""
        previous_readings: Dict[str, str] = _load_state(state_file)

        from confluent_kafka import Producer
        producer = Producer(kafka_config)
        waterinfo_producer = BEVlaanderenWaterinfoVMMEventProducer(producer, kafka_topic)

        logging.info("Starting to feed stations to Kafka topic %s", kafka_topic)

        # Fetch and send station reference data
        station_data = self.list_stations()
        headers = station_data[0] if station_data else []
        stations = station_data[1:] if len(station_data) > 1 else []
        station_count = 0
        for row in stations:
            station_dict = dict(zip(headers, row))
            station = Station(
                station_no=station_dict.get("station_no", ""),
                station_name=station_dict.get("station_name", ""),
                station_id=str(station_dict.get("station_id", "")),
                station_latitude=float(station_dict.get("station_latitude", 0) or 0),
                station_longitude=float(station_dict.get("station_longitude", 0) or 0),
                river_name=station_dict.get("river_name", "") or "",
                stationparameter_name="",
                ts_id="",
                ts_unitname="",
            )
            waterinfo_producer.send_be_vlaanderen_waterinfo_vmm_station(
                station, flush_producer=False)
            station_count += 1
        producer.flush()
        logging.info("Sent %d stations as reference data", station_count)

        # Main polling loop
        while True:
            try:
                count = 0
                start_time = time.time()
                readings = self.get_latest_water_levels()

                for entry in readings:
                    ts_id = str(entry.get("ts_id", ""))
                    ts_timestamp = entry.get("timestamp")
                    ts_value = entry.get("ts_value")

                    if ts_value is None or ts_timestamp is None:
                        continue

                    reading_key = f"{ts_id}:{ts_timestamp}"
                    if reading_key in previous_readings:
                        continue

                    reading = WaterLevelReading(
                        ts_id=ts_id,
                        station_no=entry.get("station_no", ""),
                        station_name=entry.get("station_name", ""),
                        timestamp=ts_timestamp,
                        value=float(ts_value),
                        unit_name=entry.get("ts_unitname", "meter"),
                        parameter_name=entry.get("stationparameter_name", "H"),
                    )

                    try:
                        waterinfo_producer.send_be_vlaanderen_waterinfo_vmm_water_level_reading(
                            reading, flush_producer=False)
                        count += 1
                    # pylint: disable=broad-except
                    except Exception as e:
                        logging.error("Error sending reading to kafka: %s", e)
                    # pylint: enable=broad-except

                    previous_readings[reading_key] = ts_timestamp

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
    """Main entry point for Waterinfo VMM bridge."""
    parser = argparse.ArgumentParser(description='Waterinfo VMM (Belgium) KIWIS API bridge to Kafka')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list', help='List all available stations')

    level_parser = subparsers.add_parser('level', help='Get latest water level for a station')
    level_parser.add_argument('station_no', type=str, help='Station number (e.g., L04_007)')

    feed_parser = subparsers.add_parser('feed', help='Feed water levels as CloudEvents to Kafka')
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str,
                             default=os.getenv('KAFKA_BOOTSTRAP_SERVERS'))
    feed_parser.add_argument('--kafka-topic', type=str, default=os.getenv('KAFKA_TOPIC'))
    feed_parser.add_argument('--sasl-username', type=str, default=os.getenv('SASL_USERNAME'))
    feed_parser.add_argument('--sasl-password', type=str, default=os.getenv('SASL_PASSWORD'))
    feed_parser.add_argument('-c', '--connection-string', type=str,
                             default=os.getenv('CONNECTION_STRING'))
    polling_interval_default = 900
    if os.getenv('POLLING_INTERVAL'):
        polling_interval_default = int(os.getenv('POLLING_INTERVAL'))
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=polling_interval_default)
    feed_parser.add_argument('--state-file', type=str,
                             default=os.getenv('STATE_FILE', os.path.expanduser('~/.waterinfo_vmm_state.json')))

    args = parser.parse_args()
    api = WaterinfoVMMAPI()

    if args.command == 'list':
        station_data = api.list_stations()
        headers = station_data[0] if station_data else []
        for row in station_data[1:]:
            d = dict(zip(headers, row))
            print(f"{d.get('station_no', '')}: {d.get('station_name', '')} ({d.get('river_name', '')})")
    elif args.command == 'level':
        data = api._kiwis_request({
            "request": "getTimeseriesValues",
            "station_no": args.station_no,
            "parametertype_name": "H",
            "period": "PT1H",
        })
        print(json.dumps(data, indent=4))
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
