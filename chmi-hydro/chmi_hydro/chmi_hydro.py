"""ČHMÚ Hydrological Data Bridge - fetches water level data from the Czech Hydrometeorological Institute."""

import argparse
import json
import sys
import os
import time
import typing
import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from confluent_kafka import Producer

from chmi_hydro.chmi_hydro_producer.producer_client import CZGovCHMIHydroEventProducer
from chmi_hydro.chmi_hydro_producer.cz.gov.chmi.hydro.station import Station
from chmi_hydro.chmi_hydro_producer.cz.gov.chmi.hydro.water_level_observation import WaterLevelObservation

logger = logging.getLogger(__name__)

CHMI_BASE_URL = "https://opendata.chmi.cz/hydrology/now"
CHMI_METADATA_URL = f"{CHMI_BASE_URL}/metadata/meta1.json"
CHMI_DATA_URL = f"{CHMI_BASE_URL}/data"

MAX_WORKERS = 10


class CHMIHydroAPI:
    """Client for the ČHMÚ open data hydrological API."""

    def __init__(self, base_url: str = CHMI_BASE_URL, polling_interval: int = 600):
        self.base_url = base_url
        self.metadata_url = f"{base_url}/metadata/meta1.json"
        self.data_url = f"{base_url}/data"
        self.polling_interval = polling_interval
        self.session = requests.Session()
        self._station_metadata: typing.Optional[typing.List[typing.List]] = None
        self._station_header: typing.Optional[typing.List[str]] = None

    def get_metadata(self) -> typing.List[typing.List]:
        """Fetch station metadata from meta1.json."""
        response = self.session.get(self.metadata_url, timeout=30)
        response.raise_for_status()
        payload = response.json()
        data_section = payload["data"]["data"]
        self._station_header = data_section["header"].split(",")
        self._station_metadata = data_section["values"]
        return self._station_metadata

    def get_station_data(self, station_id: str) -> typing.Optional[dict]:
        """Fetch current data for a specific station."""
        url = f"{self.data_url}/{station_id}.json"
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.debug("Failed to fetch data for station %s: %s", station_id, e)
            return None

    def get_all_station_data(self, station_ids: typing.List[str]) -> typing.Dict[str, dict]:
        """Fetch data for all stations concurrently."""
        results = {}
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(self.get_station_data, sid): sid for sid in station_ids}
            for future in as_completed(futures):
                sid = futures[future]
                try:
                    data = future.result()
                    if data:
                        results[sid] = data
                except Exception as e:
                    logger.debug("Error fetching station %s: %s", sid, e)
        return results

    @staticmethod
    def parse_station(record: typing.List) -> Station:
        """Parse a metadata record array into a Station object.

        Meta1.json header: objID,DBC,STATION_NAME,STREAM_NAME,GEOGR1,GEOGR2,
        SPA_TYP,SPAH_DS,SPAH_UNIT,DRYH,SPA1H,SPA2H,SPA3H,SPA4H,
        SPAQ_DS,SPAQ_UNIT,DRYQ,SPA1Q,SPA2Q,SPA3Q,SPA4Q,ISFORECAST
        """
        return Station(
            station_id=str(record[0]),
            dbc=str(record[1]),
            station_name=str(record[2]),
            stream_name=str(record[3]) if record[3] else "",
            latitude=float(record[4]) if record[4] is not None else 0.0,
            longitude=float(record[5]) if record[5] is not None else 0.0,
            flood_level_1=float(record[10]) if record[10] is not None else None,
            flood_level_2=float(record[11]) if record[11] is not None else None,
            flood_level_3=float(record[12]) if record[12] is not None else None,
            flood_level_4=float(record[13]) if record[13] is not None else None,
            has_forecast=bool(record[21]) if len(record) > 21 else False,
        )

    @staticmethod
    def parse_observation(station_id: str, station_name: str, stream_name: str,
                          data: dict) -> typing.Optional[WaterLevelObservation]:
        """Parse a station data file into a WaterLevelObservation.

        Extracts the latest measurement from each time series (H, Q, TH).
        """
        obj_list = data.get("objList", [])
        if not obj_list:
            return None

        obj = obj_list[0]
        ts_list = obj.get("tsList", [])
        if not ts_list:
            return None

        water_level = None
        water_level_ts = None
        discharge = None
        discharge_ts = None
        water_temp = None
        water_temp_ts = None

        for ts in ts_list:
            ts_con_id = ts.get("tsConID", "")
            ts_data = ts.get("tsData", [])
            if not ts_data:
                continue
            latest = ts_data[-1]
            dt = latest.get("dt")
            value = latest.get("value")
            if value is None:
                continue

            if ts_con_id == "H":
                water_level = float(value)
                water_level_ts = dt
            elif ts_con_id == "Q":
                discharge = float(value)
                discharge_ts = dt
            elif ts_con_id == "TH":
                water_temp = float(value)
                water_temp_ts = dt

        if water_level is None and discharge is None and water_temp is None:
            return None

        return WaterLevelObservation(
            station_id=station_id,
            station_name=station_name,
            stream_name=stream_name,
            water_level=water_level,
            water_level_timestamp=water_level_ts,
            discharge=discharge,
            discharge_timestamp=discharge_ts,
            water_temperature=water_temp,
            water_temperature_timestamp=water_temp_ts,
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
                config['bootstrap.servers'] = value.replace('sb://', '').rstrip('/')
            elif key == 'SharedAccessKeyName':
                config['sasl.username'] = '$ConnectionString'
            elif key == 'SharedAccessKey':
                config['sasl.password'] = connection_string
            elif key == 'BootstrapServer':
                config['bootstrap.servers'] = value
    if 'sasl.username' in config:
        config['security.protocol'] = 'SASL_SSL'
        config['sasl.mechanism'] = 'PLAIN'
    return config


def feed_stations(api: CHMIHydroAPI, producer: CZGovCHMIHydroEventProducer) -> int:
    """Fetch all data and send station reference data + observations to Kafka."""
    metadata = api.get_metadata()
    sent_count = 0

    station_ids = []
    stations_by_id = {}
    for record in metadata:
        station = api.parse_station(record)
        station_ids.append(station.station_id)
        stations_by_id[station.station_id] = station
        producer.send_cz_gov_chmi_hydro_station(
            station,
            flush_producer=False,
            key_mapper=lambda ce, s: f"CZ.Gov.CHMI.Hydro.Station:{s.station_id}"
        )
        sent_count += 1

    all_data = api.get_all_station_data(station_ids)

    for sid, data in all_data.items():
        station = stations_by_id.get(sid)
        if not station:
            continue
        observation = api.parse_observation(sid, station.station_name, station.stream_name, data)
        if observation:
            producer.send_cz_gov_chmi_hydro_water_level_observation(
                observation,
                flush_producer=False,
                key_mapper=lambda ce, o: f"CZ.Gov.CHMI.Hydro.WaterLevelObservation:{o.station_id}"
            )
            sent_count += 1

    producer.producer.flush()
    return sent_count


def main():
    """Main entry point for the ČHMÚ Hydro bridge."""
    parser = argparse.ArgumentParser(description="ČHMÚ Hydrological Data Bridge")
    parser.add_argument('--connection-string', required=False, help='Kafka/Event Hubs connection string',
                        default=os.environ.get('KAFKA_CONNECTION_STRING') or os.environ.get('CONNECTION_STRING'))
    parser.add_argument('--topic', required=False, help='Kafka topic', default=os.environ.get('KAFKA_TOPIC', 'chmi-hydro'))
    parser.add_argument('--polling-interval', type=int, default=int(os.environ.get('POLLING_INTERVAL', '600')),
                        help='Polling interval in seconds (default: 600)')
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('list', help='List all stations')
    level_parser = subparsers.add_parser('level', help='Get water level for a station')
    level_parser.add_argument('station_id', help='Station ID (e.g. 0-203-1-001000)')
    subparsers.add_parser('feed', help='Feed data to Kafka')

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    api = CHMIHydroAPI(polling_interval=args.polling_interval)

    if args.command == 'list':
        metadata = api.get_metadata()
        for record in metadata:
            station = api.parse_station(record)
            print(f"{station.station_id}: {station.station_name} ({station.stream_name}) [{station.latitude}, {station.longitude}]")
    elif args.command == 'level':
        data = api.get_station_data(args.station_id)
        if data:
            obs = api.parse_observation(args.station_id, "", "", data)
            if obs:
                if obs.water_level is not None:
                    print(f"Water level: {obs.water_level} cm at {obs.water_level_timestamp}")
                if obs.discharge is not None:
                    print(f"Discharge: {obs.discharge} m³/s at {obs.discharge_timestamp}")
                if obs.water_temperature is not None:
                    print(f"Water temperature: {obs.water_temperature}°C at {obs.water_temperature_timestamp}")
            else:
                print("No observation data available for this station.")
        else:
            print(f"Could not fetch data for station {args.station_id}")
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
        kafka_config['client.id'] = 'chmi-hydro-bridge'
        producer = Producer(kafka_config)
        event_producer = CZGovCHMIHydroEventProducer(producer, args.topic)
        logger.info("Starting ČHMÚ Hydro bridge, polling every %d seconds", args.polling_interval)
        while True:
            try:
                count = feed_stations(api, event_producer)
                logger.info("Sent %d events", count)
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            time.sleep(args.polling_interval)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
