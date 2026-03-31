"""BAFU Hydrological Data Bridge - fetches water level, discharge, and temperature data from Swiss FOEN/BAFU via existenz.ch API."""

import argparse
import json
import sys
import os
import time
import logging
import requests
from datetime import datetime, timezone
from confluent_kafka import Producer

from bafu_hydro_producer_data.ch.bafu.hydrology.station import Station
from bafu_hydro_producer_data.ch.bafu.hydrology.waterlevelobservation import WaterLevelObservation
from bafu_hydro_producer_kafka_producer.producer import CHBAFUHydrologyEventProducer

logger = logging.getLogger(__name__)

EXISTENZ_BASE_URL = "https://api.existenz.ch/apiv1/hydro"
BAFU_SOURCE = "https://www.hydrodaten.admin.ch"

PAR_HEIGHT = "height"
PAR_FLOW = "flow"
PAR_TEMPERATURE = "temperature"


class BAFUHydroAPI:
    """Client for the existenz.ch Hydro API (wrapping Swiss BAFU/FOEN data)."""

    def __init__(self, base_url: str = EXISTENZ_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/json'

    def get_locations(self) -> dict:
        """Fetch all station locations. Returns dict of station_id -> details."""
        url = f"{self.base_url}/locations"
        response = self.session.get(url, timeout=60)
        response.raise_for_status()
        data = response.json()
        payload = data.get('payload', {})
        result = {}
        for station_key, station_data in payload.items():
            details = station_data.get('details', {})
            if details:
                result[str(details.get('id', station_key))] = details
        return result

    def get_latest(self) -> list:
        """Fetch latest measurements for all stations and parameters."""
        url = f"{self.base_url}/latest"
        response = self.session.get(url, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get('payload', [])


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
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logging.warning("Could not load state from %s: %s", state_file, e)
    return {}


def _save_state(state_file: str, data: dict) -> None:
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


def send_stations(api: BAFUHydroAPI, producer: CHBAFUHydrologyEventProducer) -> dict:
    """Fetch all station locations and send station reference data to Kafka. Returns locations dict."""
    locations = api.get_locations()
    sent_count = 0

    for station_id, details in locations.items():
        station_data = Station(
            station_id=station_id,
            name=details.get('name', ''),
            water_body_name=details.get('water-body-name', ''),
            water_body_type=details.get('water-body-type', ''),
            latitude=details.get('lat', 0.0),
            longitude=details.get('lon', 0.0),
        )
        producer.send_ch_bafu_hydrology_station(data=station_data, flush_producer=False)
        sent_count += 1

    producer.producer.flush()
    logger.info("Sent %d station events", sent_count)
    return locations


def feed_observations(api: BAFUHydroAPI, producer: CHBAFUHydrologyEventProducer, locations: dict, previous_readings: dict) -> int:
    """Fetch latest measurements and send observations to Kafka."""
    sent_count = 0

    latest = api.get_latest()
    measurements_by_station = {}
    for m in latest:
        loc = str(m.get('loc', ''))
        par = m.get('par', '')
        val = m.get('val')
        ts = m.get('timestamp')
        if not loc or val is None:
            continue
        if loc not in measurements_by_station:
            measurements_by_station[loc] = {}
        measurements_by_station[loc][par] = {'value': val, 'timestamp': ts}

    for station_id, params in measurements_by_station.items():
        if station_id not in locations:
            continue

        wl_val = 0.0
        wl_ts_str = ""
        q_val = 0.0
        q_ts_str = ""
        temp_val = 0.0
        temp_ts_str = ""

        if PAR_HEIGHT in params:
            h = params[PAR_HEIGHT]
            ts = h.get('timestamp')
            wl_ts_str = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() if ts else ""
            wl_val = float(h['value'])

        if PAR_FLOW in params:
            f = params[PAR_FLOW]
            ts = f.get('timestamp')
            q_ts_str = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() if ts else ""
            q_val = float(f['value'])

        if PAR_TEMPERATURE in params:
            t = params[PAR_TEMPERATURE]
            ts = t.get('timestamp')
            temp_ts_str = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() if ts else ""
            temp_val = float(t['value'])

        if not wl_ts_str and not q_ts_str and not temp_ts_str:
            continue

        reading_key = f"{station_id}:{wl_ts_str}:{q_ts_str}:{temp_ts_str}"
        if reading_key in previous_readings:
            continue

        obs_data = WaterLevelObservation(
            station_id=station_id,
            water_level=wl_val,
            water_level_unit='m',
            water_level_timestamp=wl_ts_str,
            discharge=q_val,
            discharge_unit='m3/s',
            discharge_timestamp=q_ts_str,
            water_temperature=temp_val,
            water_temperature_unit='C',
            water_temperature_timestamp=temp_ts_str,
        )
        producer.send_ch_bafu_hydrology_water_level_observation(data=obs_data, flush_producer=False)
        sent_count += 1
        previous_readings[reading_key] = wl_ts_str or q_ts_str or temp_ts_str

    producer.producer.flush()
    return sent_count


def main():
    parser = argparse.ArgumentParser(description="BAFU Hydrological Data Bridge (via existenz.ch)")
    parser.add_argument('--connection-string', required=False,
                        default=os.environ.get('KAFKA_CONNECTION_STRING') or os.environ.get('CONNECTION_STRING'))
    parser.add_argument('--topic', required=False, default=os.environ.get('KAFKA_TOPIC'))
    parser.add_argument('--polling-interval', type=int,
                        default=int(os.environ.get('POLLING_INTERVAL', '600')))
    parser.add_argument('--state-file', type=str,
                        default=os.environ.get('STATE_FILE', os.path.expanduser('~/.bafu_hydro_state.json')))
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('feed', help='Feed data to Kafka')
    subparsers.add_parser('list', help='List all stations')

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    api = BAFUHydroAPI()

    if args.command == 'list':
        locations = api.get_locations()
        for sid, details in sorted(locations.items()):
            print(f"{sid}: {details.get('name')} ({details.get('water-body-name', '')}) "
                  f"[{details.get('lat')}, {details.get('lon')}]")
    elif args.command == 'feed':
        if not args.connection_string:
            if not os.environ.get('KAFKA_BROKER'):
                print("Error: --connection-string or KAFKA_BROKER required for feed mode")
                sys.exit(1)
            kafka_config = {'bootstrap.servers': os.environ['KAFKA_BROKER']}
        else:
            kafka_config = parse_connection_string(args.connection_string)
        if '_entity_path' in kafka_config and not args.topic:
            args.topic = kafka_config.pop('_entity_path')
        elif '_entity_path' in kafka_config:
            kafka_config.pop('_entity_path')
        if not args.topic:
            args.topic = 'bafu-hydro'
        tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
        if 'sasl.username' in kafka_config:
            kafka_config['security.protocol'] = 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT'
        elif tls_enabled:
            kafka_config['security.protocol'] = 'SSL'
        kafka_config['client.id'] = 'bafu-hydro-bridge'
        kafka_producer = Producer(kafka_config)
        bafu_producer = CHBAFUHydrologyEventProducer(kafka_producer, args.topic)
        logger.info("Starting BAFU Hydro bridge, polling every %d seconds", args.polling_interval)
        previous_readings = _load_state(args.state_file)
        locations = send_stations(api, bafu_producer)
        while True:
            try:
                count = feed_observations(api, bafu_producer, locations, previous_readings)
                _save_state(args.state_file, previous_readings)
                logger.info("Sent %d observation events", count)
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            time.sleep(args.polling_interval)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
