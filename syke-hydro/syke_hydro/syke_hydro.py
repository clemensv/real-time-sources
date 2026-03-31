"""SYKE Hydrological Data Bridge - fetches water level and discharge data from the Finnish Environment Institute (SYKE)."""

import argparse
import json
import sys
import os
import time
import logging
import requests
from datetime import datetime, timezone, timedelta
from confluent_kafka import Producer

from syke_hydro_producer_data.fi.syke.hydrology.station import Station
from syke_hydro_producer_data.fi.syke.hydrology.waterlevelobservation import WaterLevelObservation
from syke_hydro_producer_kafka_producer.producer import FISYKEHydrologyEventProducer

logger = logging.getLogger(__name__)

SYKE_BASE_URL = "https://rajapinnat.ymparisto.fi/api/Hydrologiarajapinta/1.1/odata"

MAX_ODATA_TOP = 5000


def _parse_dms(coord: str) -> float:
    """Parse SYKE DMS coordinate string to decimal degrees."""
    if not coord or not coord.strip():
        return 0.0
    coord = coord.strip()
    if len(coord) == 6:
        degrees = int(coord[:2])
        minutes = int(coord[2:4])
        seconds = int(coord[4:6])
    elif len(coord) == 7:
        degrees = int(coord[:3])
        minutes = int(coord[3:5])
        seconds = int(coord[5:7])
    else:
        try:
            return float(coord)
        except ValueError:
            return 0.0
    return degrees + minutes / 60.0 + seconds / 3600.0


class SYKEHydroAPI:
    """Client for the SYKE Hydrology OData API."""

    def __init__(self, base_url: str = SYKE_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/json'

    def _odata_get_all(self, entity: str, params: dict = None) -> list:
        """Fetch all records from an OData endpoint, handling pagination."""
        url = f"{self.base_url}/{entity}"
        all_records = []
        query_params = dict(params or {})
        query_params.setdefault('$top', str(MAX_ODATA_TOP))

        while url:
            response = self.session.get(url, params=query_params, timeout=120)
            response.raise_for_status()
            data = response.json()
            all_records.extend(data.get('value', []))
            next_link = data.get('odata.nextLink')
            if next_link:
                url = next_link
                query_params = {}
            else:
                break
        return all_records

    def get_stations(self) -> list:
        """Fetch all active stations from Paikka entity."""
        return self._odata_get_all('Paikka', {'$filter': 'Tila_Id eq 1'})

    def get_water_levels(self, since_date: str) -> list:
        """Fetch recent water level readings (Vedenkorkeus)."""
        return self._odata_get_all('Vedenkorkeus', {
            '$filter': f"Aika ge datetime'{since_date}T00:00:00'",
            '$orderby': 'Paikka_Id,Aika desc',
        })

    def get_discharge(self, since_date: str) -> list:
        """Fetch recent discharge readings (Virtaama)."""
        return self._odata_get_all('Virtaama', {
            '$filter': f"Aika ge datetime'{since_date}T00:00:00'",
            '$orderby': 'Paikka_Id,Aika desc',
        })


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


def _get_latest_per_station(readings: list) -> dict:
    """Group readings by Paikka_Id and keep only the latest per station."""
    latest = {}
    for r in readings:
        pid = r.get('Paikka_Id')
        if pid is None:
            continue
        existing = latest.get(pid)
        if existing is None or r.get('Aika', '') > existing.get('Aika', ''):
            latest[pid] = r
    return latest


def send_stations(api: SYKEHydroAPI, producer: FISYKEHydrologyEventProducer) -> dict:
    """Fetch all stations and send station reference data to Kafka. Returns stations_by_id dict."""
    stations = api.get_stations()
    sent_count = 0

    stations_by_id = {}
    for station in stations:
        pid = station.get('Paikka_Id')
        if pid is None:
            continue
        stations_by_id[pid] = station

        lat = _parse_dms(station.get('KoordLat', ''))
        lon = _parse_dms(station.get('KoordLong', ''))

        station_data = Station(
            station_id=str(pid),
            name=station.get('Nimi', ''),
            river_name=station.get('PaaVesalNimi', ''),
            water_area_name=station.get('VesalNimi', ''),
            municipality=station.get('KuntaNimi', ''),
            latitude=lat,
            longitude=lon,
        )
        producer.send_fi_syke_hydrology_station(data=station_data, flush_producer=False)
        sent_count += 1

    producer.producer.flush()
    logger.info("Sent %d station events", sent_count)
    return stations_by_id


def feed_observations(api: SYKEHydroAPI, producer: FISYKEHydrologyEventProducer, stations_by_id: dict, previous_readings: dict) -> int:
    """Fetch water level and discharge observations and send to Kafka."""
    sent_count = 0
    since = (datetime.now(timezone.utc) - timedelta(days=2)).strftime('%Y-%m-%d')

    # Fetch water level and discharge observations
    water_levels = api.get_water_levels(since)
    latest_wl = _get_latest_per_station(water_levels)
    discharges = api.get_discharge(since)
    latest_q = _get_latest_per_station(discharges)

    # Merge both parameters per station into a single event
    all_pids = set(latest_wl.keys()) | set(latest_q.keys())
    for pid in all_pids:
        if pid not in stations_by_id:
            continue

        wl = latest_wl.get(pid)
        q = latest_q.get(pid)

        wl_val = float(wl['Arvo']) if wl and wl.get('Arvo') is not None else 0.0
        wl_ts = wl.get('Aika', '') if wl and wl.get('Arvo') is not None else ''
        q_val = float(q['Arvo']) if q and q.get('Arvo') is not None else 0.0
        q_ts = q.get('Aika', '') if q and q.get('Arvo') is not None else ''

        if not wl_ts and not q_ts:
            continue

        reading_key = f"{pid}:{wl_ts}:{q_ts}"
        if reading_key in previous_readings:
            continue

        obs_data = WaterLevelObservation(
            station_id=str(pid),
            water_level=wl_val,
            water_level_unit='cm',
            water_level_timestamp=wl_ts,
            discharge=q_val,
            discharge_unit='m3/s',
            discharge_timestamp=q_ts,
        )
        producer.send_fi_syke_hydrology_water_level_observation(data=obs_data, flush_producer=False)
        sent_count += 1
        previous_readings[reading_key] = wl_ts or q_ts

    producer.producer.flush()
    return sent_count


def main():
    parser = argparse.ArgumentParser(description="SYKE Hydrological Data Bridge")
    parser.add_argument('--connection-string', required=False,
                        default=os.environ.get('KAFKA_CONNECTION_STRING') or os.environ.get('CONNECTION_STRING'))
    parser.add_argument('--topic', required=False, default=os.environ.get('KAFKA_TOPIC'))
    parser.add_argument('--polling-interval', type=int,
                        default=int(os.environ.get('POLLING_INTERVAL', '3600')))
    parser.add_argument('--state-file', type=str,
                        default=os.environ.get('STATE_FILE', os.path.expanduser('~/.syke_hydro_state.json')))
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('feed', help='Feed data to Kafka')
    subparsers.add_parser('list', help='List all stations')

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    api = SYKEHydroAPI()

    if args.command == 'list':
        stations = api.get_stations()
        for s in stations:
            lat = _parse_dms(s.get('KoordLat', ''))
            lon = _parse_dms(s.get('KoordLong', ''))
            print(f"{s.get('Paikka_Id')}: {s.get('Nimi')} ({s.get('PaaVesalNimi', '')}) [{lat}, {lon}]")
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
            args.topic = 'syke-hydro'
        tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
        if 'sasl.username' in kafka_config:
            kafka_config['security.protocol'] = 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT'
        elif tls_enabled:
            kafka_config['security.protocol'] = 'SSL'
        kafka_config['client.id'] = 'syke-hydro-bridge'
        kafka_producer = Producer(kafka_config)
        syke_producer = FISYKEHydrologyEventProducer(kafka_producer, args.topic)
        logger.info("Starting SYKE Hydro bridge, polling every %d seconds", args.polling_interval)
        previous_readings = _load_state(args.state_file)
        stations_by_id = send_stations(api, syke_producer)
        while True:
            try:
                count = feed_observations(api, syke_producer, stations_by_id, previous_readings)
                _save_state(args.state_file, previous_readings)
                logger.info("Sent %d observation events", count)
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            time.sleep(args.polling_interval)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
