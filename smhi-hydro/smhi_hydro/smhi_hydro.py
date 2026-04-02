"""SMHI Hydrological Data Bridge - fetches discharge data from the Swedish Meteorological and Hydrological Institute."""

import argparse
import json
import sys
import os
import time
import typing
import logging
import requests
from datetime import datetime, timezone
from confluent_kafka import Producer

from smhi_hydro.smhi_hydro_producer.producer_client import SEGovSMHIHydroEventProducer
from smhi_hydro.smhi_hydro_producer.se.gov.smhi.hydro.station import Station
from smhi_hydro.smhi_hydro_producer.se.gov.smhi.hydro.discharge_observation import DischargeObservation

logger = logging.getLogger(__name__)

SMHI_BASE_URL = "https://opendata-download-hydroobs.smhi.se/api/version/1.0"
SMHI_BULK_DISCHARGE_URL = f"{SMHI_BASE_URL}/parameter/2/station-set/all/period/latest-hour/data.json"


class SMHIHydroAPI:
    """Client for the SMHI open data hydrological API."""

    def __init__(self, base_url: str = SMHI_BASE_URL, polling_interval: int = 900):
        self.base_url = base_url
        self.bulk_discharge_url = f"{base_url}/parameter/2/station-set/all/period/latest-hour/data.json"
        self.polling_interval = polling_interval
        self.session = requests.Session()

    def get_bulk_discharge_data(self) -> dict:
        """Fetch bulk discharge data for all stations from the latest-hour endpoint."""
        response = self.session.get(self.bulk_discharge_url, timeout=60)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def parse_station(station_data: dict) -> Station:
        """Parse a station entry from the bulk data into a Station object."""
        return Station(
            station_id=str(station_data["key"]),
            name=station_data["name"],
            owner=station_data.get("owner", ""),
            measuring_stations=station_data.get("measuringStations", ""),
            region=int(station_data.get("region", 0)),
            catchment_name=station_data.get("catchmentName", ""),
            catchment_number=int(station_data.get("catchmentNumber", 0)),
            catchment_size=float(station_data.get("catchmentSize", 0.0)),
            latitude=float(station_data["latitude"]),
            longitude=float(station_data["longitude"]),
        )

    @staticmethod
    def parse_latest_observation(station_data: dict) -> typing.Optional[DischargeObservation]:
        """Parse the latest discharge observation from a station's value array."""
        values = station_data.get("value", [])
        if not values:
            return None

        latest = values[-1]
        value = latest.get("value")
        if value is None:
            return None

        epoch_ms = latest["date"]
        ts = datetime.fromtimestamp(epoch_ms / 1000.0, tz=timezone.utc).isoformat()

        return DischargeObservation(
            station_id=str(station_data["key"]),
            station_name=station_data["name"],
            catchment_name=station_data.get("catchmentName", ""),
            timestamp=ts,
            discharge=float(value),
            quality=latest.get("quality", ""),
        )


def parse_connection_string(connection_string: str) -> dict:
    """Parse a Kafka connection string into a config dict."""
    config = {}
    for part in connection_string.split(';'):
        part = part.strip()
        if '=' in part:
            key, value = part.split('=', 1)
            key = key.strip()
            value = value.strip()
            if key == 'Endpoint':
                config['bootstrap.servers'] = value.replace('sb://', '').rstrip('/') + ':9093'
            elif key == 'SharedAccessKeyName':
                config['sasl.username'] = '$ConnectionString'
            elif key == 'SharedAccessKey':
                config['sasl.password'] = connection_string
            elif key == 'BootstrapServer':
                config['bootstrap.servers'] = value
            elif key == 'EntityPath':
                config['_entity_path'] = value
    if 'sasl.username' in config:
        config['security.protocol'] = 'SASL_SSL'
        config['sasl.mechanism'] = 'PLAIN'
    return config


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


def send_stations(api: SMHIHydroAPI, producer: SEGovSMHIHydroEventProducer) -> int:
    """Fetch bulk data and send station reference data to Kafka."""
    bulk_data = api.get_bulk_discharge_data()
    stations = bulk_data.get("station", [])
    sent_count = 0

    for station_data in stations:
        station = api.parse_station(station_data)
        producer.send_se_gov_smhi_hydro_station(
            station,
            flush_producer=False,
            key_mapper=lambda ce, s: f"SE.Gov.SMHI.Hydro.Station:{s.station_id}"
        )
        sent_count += 1

    producer.producer.flush()
    logger.info("Sent %d station events", sent_count)
    return sent_count


def feed_observations(api: SMHIHydroAPI, producer: SEGovSMHIHydroEventProducer, previous_readings: dict) -> int:
    """Fetch bulk discharge data and send observations to Kafka."""
    bulk_data = api.get_bulk_discharge_data()
    stations = bulk_data.get("station", [])
    sent_count = 0

    for station_data in stations:
        observation = api.parse_latest_observation(station_data)
        if observation:
            reading_key = f"{observation.station_id}:{observation.timestamp}"
            if reading_key in previous_readings:
                continue
            producer.send_se_gov_smhi_hydro_discharge_observation(
                observation,
                flush_producer=False,
                key_mapper=lambda ce, o: f"SE.Gov.SMHI.Hydro.DischargeObservation:{o.station_id}"
            )
            sent_count += 1
            previous_readings[reading_key] = observation.timestamp

    producer.producer.flush()
    return sent_count


def feed_stations(api: SMHIHydroAPI, producer: SEGovSMHIHydroEventProducer) -> int:
    """Fetch all stations and observations and send to Kafka. Returns total events sent."""
    station_count = send_stations(api, producer)
    obs_count = feed_observations(api, producer, {})
    return station_count + obs_count


def main():
    """Main entry point for the SMHI Hydro bridge."""
    parser = argparse.ArgumentParser(description="SMHI Hydrological Data Bridge")
    parser.add_argument('--connection-string', required=False, help='Kafka/Event Hubs connection string',
                        default=os.environ.get('KAFKA_CONNECTION_STRING') or os.environ.get('CONNECTION_STRING'))
    parser.add_argument('--topic', required=False, help='Kafka topic', default=os.environ.get('KAFKA_TOPIC') or None)
    parser.add_argument('--polling-interval', type=int, default=int(os.environ.get('POLLING_INTERVAL', '900')),
                        help='Polling interval in seconds (default: 900)')
    parser.add_argument('--state-file', type=str,
                        default=os.environ.get('STATE_FILE', os.path.expanduser('~/.smhi_hydro_state.json')))
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('list', help='List all stations')
    obs_parser = subparsers.add_parser('observation', help='Get latest discharge for a station')
    obs_parser.add_argument('station_id', help='Station ID (e.g. 1583)')
    subparsers.add_parser('feed', help='Feed data to Kafka')

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    api = SMHIHydroAPI(polling_interval=args.polling_interval)

    if args.command == 'list':
        bulk_data = api.get_bulk_discharge_data()
        for station_data in bulk_data.get("station", []):
            station = api.parse_station(station_data)
            print(f"{station.station_id}: {station.name} ({station.catchment_name}) [{station.latitude}, {station.longitude}]")
    elif args.command == 'observation':
        bulk_data = api.get_bulk_discharge_data()
        for station_data in bulk_data.get("station", []):
            if str(station_data["key"]) == args.station_id:
                obs = api.parse_latest_observation(station_data)
                if obs:
                    print(f"Discharge: {obs.discharge} m³/s at {obs.timestamp} (quality: {obs.quality})")
                else:
                    print("No observation data available for this station.")
                break
        else:
            print(f"Station {args.station_id} not found")
    elif args.command == 'feed':
        if not args.connection_string:
            if not os.environ.get('KAFKA_BROKER'):
                print("Error: --connection-string or KAFKA_BROKER environment variable required for feed mode")
                sys.exit(1)
            kafka_config = {
                'bootstrap.servers': os.environ['KAFKA_BROKER'],
            }
        else:
            kafka_config = parse_connection_string(args.connection_string)
        if '_entity_path' in kafka_config and not args.topic:
            args.topic = kafka_config.pop('_entity_path')
        elif '_entity_path' in kafka_config:
            kafka_config.pop('_entity_path')
        if not args.topic:
            args.topic = 'smhi-hydro'
        tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
        if 'sasl.username' in kafka_config:
            kafka_config['security.protocol'] = 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT'
        elif tls_enabled:
            kafka_config['security.protocol'] = 'SSL'
        kafka_config['client.id'] = 'smhi-hydro-bridge'
        producer = Producer(kafka_config)
        event_producer = SEGovSMHIHydroEventProducer(producer, args.topic)
        logger.info("Starting SMHI Hydro bridge, polling every %d seconds", args.polling_interval)
        previous_readings = _load_state(args.state_file)
        send_stations(api, event_producer)
        while True:
            try:
                count = feed_observations(api, event_producer, previous_readings)
                _save_state(args.state_file, previous_readings)
                logger.info("Sent %d observation events", count)
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            time.sleep(args.polling_interval)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
