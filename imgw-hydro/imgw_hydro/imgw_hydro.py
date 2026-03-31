"""IMGW-PIB Hydrological Data Bridge - fetches water level data from the Polish Institute of Meteorology and Water Management."""

import argparse
import json
import sys
import os
import time
import typing
import logging
import requests
from confluent_kafka import Producer

from imgw_hydro.imgw_hydro_producer.producer_client import PLGovIMGWHydroEventProducer
from imgw_hydro.imgw_hydro_producer.pl.gov.imgw.hydro.station import Station
from imgw_hydro.imgw_hydro_producer.pl.gov.imgw.hydro.water_level_observation import WaterLevelObservation

logger = logging.getLogger(__name__)

IMGW_BASE_URL = "https://danepubliczne.imgw.pl/api/data/hydro"

class IMGWHydroAPI:
    """Client for the IMGW-PIB public hydrological data API."""

    def __init__(self, base_url: str = IMGW_BASE_URL, polling_interval: int = 600):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.session = requests.Session()

    def get_all_data(self) -> typing.List[dict]:
        """Fetch all hydrological station data from the IMGW API."""
        response = self.session.get(self.base_url, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_station_data(self, station_id: str) -> dict:
        """Fetch data for a specific station by ID."""
        response = self.session.get(f"{self.base_url}/id/{station_id}", timeout=30)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def parse_station(record: dict) -> Station:
        """Parse an API record into a Station object."""
        return Station(
            id_stacji=record.get("id_stacji", ""),
            stacja=record.get("stacja", ""),
            rzeka=record.get("rzeka", "") or "",
            wojewodztwo=record.get("wojewodztwo", "") or "",
            longitude=float(record["lon"]) if record.get("lon") else 0.0,
            latitude=float(record["lat"]) if record.get("lat") else 0.0,
        )

    @staticmethod
    def parse_observation(record: dict) -> typing.Optional[WaterLevelObservation]:
        """Parse an API record into a WaterLevelObservation object, or None if no water level."""
        water_level_str = record.get("stan_wody")
        if water_level_str is None:
            return None
        try:
            water_level = float(water_level_str)
        except (ValueError, TypeError):
            return None

        water_temp = None
        if record.get("temperatura_wody") is not None:
            try:
                water_temp = float(record["temperatura_wody"])
            except (ValueError, TypeError):
                water_temp = None

        discharge = None
        if record.get("przeplyw") is not None:
            try:
                discharge = float(record["przeplyw"])
            except (ValueError, TypeError):
                discharge = None

        return WaterLevelObservation(
            station_id=record.get("id_stacji", ""),
            station_name=record.get("stacja", ""),
            river=record.get("rzeka", "") or "",
            voivodeship=record.get("wojewodztwo", "") or "",
            water_level=water_level,
            water_level_timestamp=record.get("stan_wody_data_pomiaru", "") or "",
            water_temperature=water_temp,
            water_temperature_timestamp=record.get("temperatura_wody_data_pomiaru"),
            discharge=discharge,
            discharge_timestamp=record.get("przeplyw_data"),
            ice_phenomenon_code=record.get("zjawisko_lodowe"),
            overgrowth_code=record.get("zjawisko_zarastania"),
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


def send_stations(api: IMGWHydroAPI, producer: PLGovIMGWHydroEventProducer) -> int:
    """Fetch all data and send station reference data to Kafka."""
    records = api.get_all_data()
    sent_count = 0
    for record in records:
        station = api.parse_station(record)
        producer.send_pl_gov_imgw_hydro_station(
            station,
            flush_producer=False,
            key_mapper=lambda ce, s: f"PL.Gov.IMGW.Hydro.Station:{s.id_stacji}"
        )
        sent_count += 1
    producer.producer.flush()
    logger.info("Sent %d station events", sent_count)
    return sent_count


def feed_observations(api: IMGWHydroAPI, producer: PLGovIMGWHydroEventProducer, previous_readings: dict) -> int:
    """Fetch all data and send observations to Kafka."""
    records = api.get_all_data()
    sent_count = 0
    for record in records:
        observation = api.parse_observation(record)
        if observation:
            reading_key = f"{observation.station_id}:{observation.water_level_timestamp}"
            if reading_key in previous_readings:
                continue
            producer.send_pl_gov_imgw_hydro_water_level_observation(
                observation,
                flush_producer=False,
                key_mapper=lambda ce, o: f"PL.Gov.IMGW.Hydro.WaterLevelObservation:{o.station_id}"
            )
            sent_count += 1
            previous_readings[reading_key] = observation.water_level_timestamp
    producer.producer.flush()
    return sent_count


def main():
    """Main entry point for the IMGW Hydro bridge."""
    parser = argparse.ArgumentParser(description="IMGW-PIB Hydrological Data Bridge")
    parser.add_argument('--connection-string', required=False, help='Kafka/Event Hubs connection string',
                        default=os.environ.get('KAFKA_CONNECTION_STRING') or os.environ.get('CONNECTION_STRING'))
    parser.add_argument('--topic', required=False, help='Kafka topic', default=os.environ.get('KAFKA_TOPIC') or None)
    parser.add_argument('--polling-interval', type=int, default=int(os.environ.get('POLLING_INTERVAL', '600')),
                        help='Polling interval in seconds (default: 600)')
    parser.add_argument('--state-file', type=str,
                        default=os.environ.get('STATE_FILE', os.path.expanduser('~/.imgw_hydro_state.json')))
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('list', help='List all stations')
    level_parser = subparsers.add_parser('level', help='Get water level for a station')
    level_parser.add_argument('station_id', help='Station ID')
    subparsers.add_parser('feed', help='Feed data to Kafka')

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    api = IMGWHydroAPI(polling_interval=args.polling_interval)

    if args.command == 'list':
        records = api.get_all_data()
        for record in records:
            station = api.parse_station(record)
            print(f"{station.id_stacji}: {station.stacja} ({station.rzeka}) - {station.wojewodztwo}")
    elif args.command == 'level':
        record = api.get_station_data(args.station_id)
        if isinstance(record, list):
            record = record[0]
        obs = api.parse_observation(record)
        if obs:
            print(f"Station: {obs.station_name} ({obs.river})")
            print(f"Water level: {obs.water_level} cm at {obs.water_level_timestamp}")
            if obs.water_temperature is not None:
                print(f"Water temperature: {obs.water_temperature}°C at {obs.water_temperature_timestamp}")
            if obs.discharge is not None:
                print(f"Discharge: {obs.discharge} m³/s at {obs.discharge_timestamp}")
        else:
            print("No observation data available for this station.")
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
            args.topic = 'imgw-hydro'
        tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
        if 'sasl.username' in kafka_config:
            kafka_config['security.protocol'] = 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT'
        elif tls_enabled:
            kafka_config['security.protocol'] = 'SSL'
        kafka_config['client.id'] = 'imgw-hydro-bridge'
        producer = Producer(kafka_config)
        event_producer = PLGovIMGWHydroEventProducer(producer, args.topic)
        logger.info("Starting IMGW Hydro bridge, polling every %d seconds", args.polling_interval)
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
