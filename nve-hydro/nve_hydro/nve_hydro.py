"""NVE Hydrological Data Bridge - fetches water level and discharge data from the Norwegian Water Resources and Energy Directorate."""

import argparse
import json
import sys
import os
import time
import logging
import requests
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from confluent_kafka import Producer

from nve_hydro_producer_data.no.nve.hydrology.station import Station
from nve_hydro_producer_data.no.nve.hydrology.waterlevelobservation import WaterLevelObservation
from nve_hydro_producer_kafka_producer.producer import NONVEHydrologyEventProducer

logger = logging.getLogger(__name__)

NVE_BASE_URL = "https://hydapi.nve.no/api/v1"

PARAM_STAGE = 1000       # Water level / Vannstand (m)
PARAM_DISCHARGE = 1001   # Discharge / Vannføring (m³/s)

MAX_WORKERS = 10


class NVEHydroAPI:
    """Client for the NVE HydAPI."""

    def __init__(self, api_key: str, base_url: str = NVE_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers['X-API-Key'] = api_key
        self.session.headers['Accept'] = 'application/json'

    def get_stations(self) -> list:
        """Fetch all active stations."""
        url = f"{self.base_url}/Stations"
        params = {"Active": "1"}
        response = self.session.get(url, params=params, timeout=60)
        response.raise_for_status()
        return response.json().get('data', [])

    def get_observations(self, station_id: str, parameter: int) -> list:
        """Fetch latest observation for a station and parameter."""
        url = f"{self.base_url}/Observations"
        params = {
            "StationId": station_id,
            "Parameter": str(parameter),
            "ResolutionTime": "0",
        }
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json().get('data', [])
        except requests.RequestException as e:
            logger.debug("Failed to fetch observations for %s param %d: %s", station_id, parameter, e)
            return []


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


def _station_has_parameter(station: dict, param_id: int) -> bool:
    """Check if a station has a specific parameter in its series list."""
    for series in station.get('seriesList') or []:
        if series.get('parameter') == param_id:
            return True
    return False


def _fetch_station_observations(api: NVEHydroAPI, station_id: str, params: list) -> dict:
    """Fetch latest observations for a station across multiple parameters."""
    result = {}
    for param_id in params:
        obs_list = api.get_observations(station_id, param_id)
        for item in obs_list:
            observations = item.get('observations', [])
            if observations:
                latest = observations[-1]
                if latest.get('value') is not None:
                    result[param_id] = latest
                    break
    return result


def feed_stations(api: NVEHydroAPI, producer: NONVEHydrologyEventProducer, previous_readings: dict) -> int:
    """Fetch all data and send station reference data + observations to Kafka."""
    stations = api.get_stations()
    sent_count = 0

    station_params = {}
    for station in stations:
        sid = station.get('stationId')
        if not sid:
            continue
        params = []
        if _station_has_parameter(station, PARAM_STAGE):
            params.append(PARAM_STAGE)
        if _station_has_parameter(station, PARAM_DISCHARGE):
            params.append(PARAM_DISCHARGE)
        if params:
            station_params[sid] = params

        station_data = Station(
            station_id=sid,
            station_name=station.get('stationName', ''),
            river_name=station.get('riverName', ''),
            latitude=station.get('latitude', 0.0),
            longitude=station.get('longitude', 0.0),
            masl=station.get('masl') or 0.0,
            council_name=station.get('councilName', ''),
            county_name=station.get('countyName', ''),
            drainage_basin_area=station.get('drainageBasinArea') or 0.0,
        )
        producer.send_no_nve_hydrology_station(data=station_data, flush_producer=False)
        sent_count += 1

    def fetch_one(sid):
        return sid, _fetch_station_observations(api, sid, station_params[sid])

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_one, sid): sid for sid in station_params}
        for future in as_completed(futures):
            sid = futures[future]
            try:
                _, obs_by_param = future.result()
            except Exception as e:
                logger.debug("Error fetching observations for %s: %s", sid, e)
                continue
            if not obs_by_param:
                continue

            wl_val = None
            wl_ts = ""
            q_val = None
            q_ts = ""

            if PARAM_STAGE in obs_by_param:
                stage = obs_by_param[PARAM_STAGE]
                wl_val = float(stage["value"])
                wl_ts = stage.get("time", "")

            if PARAM_DISCHARGE in obs_by_param:
                discharge = obs_by_param[PARAM_DISCHARGE]
                q_val = float(discharge["value"])
                q_ts = discharge.get("time", "")

            if wl_val is None and q_val is None:
                continue

            reading_key = f"{sid}:{wl_ts}:{q_ts}"
            if reading_key in previous_readings:
                continue

            obs_data = WaterLevelObservation(
                station_id=sid,
                water_level=wl_val if wl_val is not None else 0.0,
                water_level_unit='m',
                water_level_timestamp=wl_ts,
                discharge=q_val if q_val is not None else 0.0,
                discharge_unit='m3/s',
                discharge_timestamp=q_ts,
            )
            producer.send_no_nve_hydrology_water_level_observation(data=obs_data, flush_producer=False)
            sent_count += 1
            previous_readings[reading_key] = wl_ts or q_ts

    producer.producer.flush()
    return sent_count


def main():
    parser = argparse.ArgumentParser(description="NVE Hydrological Data Bridge")
    parser.add_argument('--connection-string', required=False,
                        default=os.environ.get('KAFKA_CONNECTION_STRING') or os.environ.get('CONNECTION_STRING'))
    parser.add_argument('--topic', required=False, default=os.environ.get('KAFKA_TOPIC'))
    parser.add_argument('--polling-interval', type=int,
                        default=int(os.environ.get('POLLING_INTERVAL', '600')))
    parser.add_argument('--state-file', type=str,
                        default=os.environ.get('STATE_FILE', os.path.expanduser('~/.nve_hydro_state.json')))
    parser.add_argument('--api-key', type=str,
                        default=os.environ.get('NVE_API_KEY'))
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('feed', help='Feed data to Kafka')
    subparsers.add_parser('list', help='List all stations')

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    if not args.api_key:
        print("Error: NVE_API_KEY environment variable or --api-key required")
        sys.exit(1)

    api = NVEHydroAPI(args.api_key)

    if args.command == 'list':
        stations = api.get_stations()
        for s in stations:
            params = [str(p.get('parameter', '?')) for p in (s.get('seriesList') or [])]
            print(f"{s.get('stationId')}: {s.get('stationName')} ({s.get('riverName', '')}) "
                  f"[{s.get('latitude')}, {s.get('longitude')}] params={','.join(params)}")
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
            args.topic = 'nve-hydro'
        tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
        if 'sasl.username' in kafka_config:
            kafka_config['security.protocol'] = 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT'
        elif tls_enabled:
            kafka_config['security.protocol'] = 'SSL'
        kafka_config['client.id'] = 'nve-hydro-bridge'
        kafka_producer = Producer(kafka_config)
        nve_producer = NONVEHydrologyEventProducer(kafka_producer, args.topic)
        logger.info("Starting NVE Hydro bridge, polling every %d seconds", args.polling_interval)
        previous_readings = _load_state(args.state_file)
        while True:
            try:
                count = feed_stations(api, nve_producer, previous_readings)
                _save_state(args.state_file, previous_readings)
                logger.info("Sent %d events", count)
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            time.sleep(args.polling_interval)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
