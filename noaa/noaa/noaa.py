"""
NOAA Data Poller
Polls NOAA data and sends it to a Kafka topic using SASL PLAIN authentication.
"""

# pylint: disable=line-too-long


import os
import json
import sys
from datetime import datetime, timedelta, timezone
from typing import Dict, List
import argparse
import requests
from noaa.noaa_producer.microsoft.opendata.us.noaa.airpressure import AirPressure
from noaa.noaa_producer.microsoft.opendata.us.noaa.airtemperature import AirTemperature
from noaa.noaa_producer.microsoft.opendata.us.noaa.conductivity import Conductivity
from noaa.noaa_producer.microsoft.opendata.us.noaa.humidity import Humidity
from noaa.noaa_producer.microsoft.opendata.us.noaa.predictions import Predictions
from noaa.noaa_producer.microsoft.opendata.us.noaa.salinity import Salinity
from noaa.noaa_producer.microsoft.opendata.us.noaa.station import Station
from noaa.noaa_producer.microsoft.opendata.us.noaa.visibility import Visibility
from noaa.noaa_producer.microsoft.opendata.us.noaa.waterlevel import WaterLevel
from noaa.noaa_producer.microsoft.opendata.us.noaa.watertemperature import WaterTemperature
from noaa.noaa_producer.microsoft.opendata.us.noaa.wind import Wind
from noaa.noaa_producer.microsoft.opendata.us.noaa.qualitylevel import QualityLevel
from .noaa_producer.producer_client import MicrosoftOpendataUsNoaaEventProducer


class NOAADataPoller:
    """
    Class to poll NOAA data and send it to a Kafka topic.
    """
    BASE_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
    COMMON_PARAMS = "&units=metric&time_zone=gmt&application=web_services&format=json"

    PRODUCTS = {
        "water_level": "product=water_level",
        "predictions": "product=predictions",
        "air_temperature": "product=air_temperature",
        "wind": "product=wind",
        "air_pressure": "product=air_pressure",
        "water_temperature": "product=water_temperature",
        "conductivity": "product=conductivity",
        "visibility": "product=visibility",
        "humidity": "product=humidity",
        "salinity": "product=salinity"
    }

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str, station: str = None):
        """
        Initialize the NOAADataPoller class.

        Args:
            kafka_config (Dict[str, str]): Kafka configuration settings.
            kafka_topic (str): Kafka topic to send messages to.
            last_polled_file (str): File to store the last polled times for each station and product.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        self.producer = MicrosoftOpendataUsNoaaEventProducer(kafka_config, kafka_topic)
        self.stations = self.fetch_all_stations()
        if station:
            self.station = next((s for s in self.stations if s.id == station), None)
            if not self.station:
                print(f"Station {station} not found.")
                sys.exit(1)
        else:
            self.station = None

    def fetch_all_stations(self) -> List[Station]:
        """
        Fetch all NOAA stations.

        Returns:
            list: List of all NOAA stations.
        """
        url = "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            stations_data = response.json()
# pylint: disable=no-member
            stations = Station.schema().load(stations_data.get('stations', []), many=True)
# pylint: enable=no-member
            return stations
        except requests.RequestException as err:
            print(f"Error fetching stations: {err}")
            return []

    def get_datum_for_station(self, station_id: str) -> str:
        """
        Determine the datum value for a station based on its tideType.

        Args:
            station_id (str): The ID of the station.

        Returns:
            str: The datum value (either "MLLW" or "IGLD").
        """
        station_info: Station = next((station for station in self.stations if station.id == station_id), {})
        tide_type = station_info.tideType
        return "IGLD" if tide_type == "Great Lakes" else "MLLW"

    def poll_noaa_api(self, product: str, station_id: str, last_polled_time: datetime) -> list:
        """
        Poll the NOAA API for new data.

        Args:
            product (str): The product to poll.
            station_id (str): The ID of the station.
            last_polled_time (datetime): The last time data was polled.

        Returns:
            list: List of new data records.
        """
        datum = self.get_datum_for_station(station_id)
        if datum == "IGLD" and "predictions" in product:
            return []  # Great Lakes stations don't have prediction data
        product_url = f"{self.BASE_URL}?{self.PRODUCTS[product]}{self.COMMON_PARAMS}&station={station_id}"
        if product != "currents_predictions" and product != "currents":
            product_url += f"&datum={datum}"
        product_url += f"&begin_date={last_polled_time.strftime('%Y%m%d %H:%M')}&end_date={datetime.now(timezone.utc).strftime('%Y%m%d %H:%M')}"
        data_key = "data" if "predictions" not in product else "predictions"
        try:
            response = requests.get(product_url, timeout=10)
            response.raise_for_status()
            data = response.json().get(data_key, [])
            new_data = []
            for record in data:
                new_data.append(record)

            return new_data
        except requests.RequestException as err:
            print(f"Error fetching data for station {station_id}: {err}")
            return []

    def pascal(self, s: str) -> str:
        """
        Convert a snake_case string to PascalCase.

        Args:
            s (str): The snake_case string.

        Returns:
            str: The PascalCase string.
        """
        return ''.join([part.capitalize() for part in s.split('_')])

    def load_last_polled_times(self) -> Dict:
        """
        Load the last polled times from a file.

        Returns:
            Dict: The last polled times for each station and product.
        """
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, 'r', encoding='utf-8') as file:
                    saved_times: Dict[str, Dict[str, str]] = json.load(file)
                    last_polled_times: Dict[str, Dict[str, datetime]] = {}
                    for product, stations in saved_times.items():
                        for station, timestamp in stations.items():
                            if product not in last_polled_times:
                                last_polled_times[product] = {}
                            last_polled_times[product][station] = datetime.fromisoformat(timestamp)
                    return last_polled_times
        except Exception:
            print("Error loading last polled times")
        return {}

    def save_last_polled_times(self, last_polled_times: Dict):
        """
        Save the last polled times to a file.

        Args:
            last_polled_times (Dict): The last polled times for each station and product.
        """
        # convert all datetime objects to string for serialization
        saved_times: Dict[str, Dict[str, str]] = {}
        for product, stations in last_polled_times.items():
            for station, timestamp in stations.items():
                if product not in saved_times:
                    saved_times[product] = {}
                saved_times[product][station] = timestamp.isoformat()
        with open(self.last_polled_file, 'w', encoding='utf-8') as file:
            json.dump(saved_times, file)

    def poll_and_send(self):
        """
        Poll NOAA data and send it to Kafka.
        """
        last_polled_times = self.load_last_polled_times()

        for station in self.stations:
            self.producer.send_microsoft_opendata_us_noaa_station(station, flush_producer=False)
        self.producer.producer.flush()

        while True:
            for station in self.stations if not self.station else [self.station]:
                station_id = station.id
                for product in self.PRODUCTS:
                    print(f"Polling {product} data for station {station_id}: {station.name}:", end='')
                    last_polled_time = last_polled_times.get(product, {}).get(
                        station_id, datetime.now(timezone.utc) - timedelta(hours=24))
                    new_data_records = self.poll_noaa_api(product, station_id, last_polled_time)
                    print(f" {len(new_data_records)} new records found since {last_polled_time}")

                    max_timestamp = last_polled_time
                    for record in new_data_records:
                        ts_parsed = datetime.strptime(record['t'], "%Y-%m-%d %H:%M")
                        timestamp = ts_parsed.replace(tzinfo=timezone.utc)

                        if product == "water_level":
                            water_level = WaterLevel(
                                station_id=station_id,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                                stddev=float(record['s']) if 's' in record and record['s'] else 0.0,
                                outside_sigma_band=bool(record.get('f', '').split(',')[0] == '1'),
                                flat_tolerance_limit=bool(record.get('f', '').split(',')[1] == '1'),
                                rate_of_change_limit=bool(record.get('f', '').split(',')[2] == '1'),
                                max_min_expected_height=bool(record.get('f', '').split(',')[3] == '1'),
                                quality=QualityLevel.Preliminary if record.get(
                                    'q', '') == 'p' else QualityLevel.Verified
                            )
                            self.producer.send_microsoft_opendata_us_noaa_waterlevel(
                                water_level, station_id, flush_producer=False)
                        elif product == "predictions":
                            prediction = Predictions(
                                station_id=station_id,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                            )
                            self.producer.send_microsoft_opendata_us_noaa_predictions(
                                prediction, station_id, flush_producer=False)
                        elif product == "air_temperature":
                            air_temperature = AirTemperature(
                                station_id=station_id,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                                max_temp_exceeded=bool(record.get('f', '').split(',')[0] == '1'),
                                min_temp_exceeded=bool(record.get('f', '').split(',')[1] == '1'),
                                rate_of_change_exceeded=bool(record.get('f', '').split(',')[2] == '1')
                            )
                            self.producer.send_microsoft_opendata_us_noaa_airtemperature(
                                air_temperature, station_id, flush_producer=False)
                        elif product == "wind":
                            wind = Wind(
                                station_id=station_id,
                                timestamp=timestamp.isoformat(),
                                speed=float(record['s']) if 's' in record and record['s'] else 0.0,
                                direction_degrees=record['d'] if 'd' in record and record['d'] else 0.0,
                                direction_text=record['dr'] if 'dr' in record and record['dr'] else '',
                                gusts=float(record['g']) if 'g' in record and record['g'] else 0.0,
                                max_wind_speed_exceeded=bool(record.get('f', '').split(',')[0] == '1'),
                                rate_of_change_exceeded=bool(record.get('f', '').split(',')[1] == '1')
                            )
                            self.producer.send_microsoft_opendata_us_noaa_wind(wind, station_id, flush_producer=False)
                        elif product == "air_pressure":
                            air_pressure = AirPressure(
                                station_id=station_id,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                                max_pressure_exceeded=bool(record.get('f', '').split(',')[0] == '1'),
                                min_pressure_exceeded=bool(record.get('f', '').split(',')[1] == '1'),
                                rate_of_change_exceeded=bool(record.get('f', '').split(',')[2] == '1')
                            )
                            self.producer.send_microsoft_opendata_us_noaa_airpressure(
                                air_pressure, station_id, flush_producer=False)
                        elif product == "water_temperature":
                            water_temperature = WaterTemperature(
                                station_id=station_id,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                                max_temp_exceeded=bool(record.get('f', '').split(',')[0] == '1'),
                                min_temp_exceeded=bool(record.get('f', '').split(',')[1] == '1'),
                                rate_of_change_exceeded=bool(record.get('f', '').split(',')[2] == '1')
                            )
                            self.producer.send_microsoft_opendata_us_noaa_watertemperature(
                                water_temperature, station_id, flush_producer=False)
                        elif product == "conductivity":
                            conductivity = Conductivity(
                                station_id=station_id,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                                max_conductivity_exceeded=bool(record.get('f', '').split(',')[0] == '1'),
                                min_conductivity_exceeded=bool(record.get('f', '').split(',')[1] == '1'),
                                rate_of_change_exceeded=bool(record.get('f', '').split(',')[2] == '1')
                            )
                            self.producer.send_microsoft_opendata_us_noaa_conductivity(
                                conductivity, station_id, flush_producer=False)
                        elif product == "visibility":
                            visibility = Visibility(
                                station_id=station_id,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                                max_visibility_exceeded=bool(record.get('f', '').split(',')[0] == '1'),
                                min_visibility_exceeded=bool(record.get('f', '').split(',')[1] == '1'),
                                rate_of_change_exceeded=bool(record.get('f', '').split(',')[2] == '1')
                            )
                            self.producer.send_microsoft_opendata_us_noaa_visibility(
                                visibility, station_id, flush_producer=False)
                        elif product == "humidity":
                            humidity = Humidity(
                                station_id=station_id,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                                max_humidity_exceeded=bool(record.get('f', '').split(',')[0] == '1'),
                                min_humidity_exceeded=bool(record.get('f', '').split(',')[1] == '1'),
                                rate_of_change_exceeded=bool(record.get('f', '').split(',')[2] == '1')
                            )
                            self.producer.send_microsoft_opendata_us_noaa_humidity(
                                humidity, station_id, flush_producer=False)
                        elif product == "salinity":
                            salinity = Salinity(
                                station_id=station_id,
                                timestamp=timestamp.isoformat(),
                                salinity=float(record['s']) if 's' in record and record['s'] else 0.0,
                                grams_per_kg=float(record['g']) if 'g' in record and record['g'] else 0.0,
                            )
                            self.producer.send_microsoft_opendata_us_noaa_salinity(
                                salinity, station_id, flush_producer=False)

                        if timestamp > max_timestamp:
                            max_timestamp = timestamp
                    self.producer.producer.flush()
                    if new_data_records:
                        if product not in last_polled_times:
                            last_polled_times[product] = {}
                        last_polled_times[product][station_id] = max_timestamp
                        self.save_last_polled_times(last_polled_times)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse the connection string and extract bootstrap server, topic name, username, and password.

    Args:
        connection_string (str): The connection string.

    Returns:
        Dict[str, str]: Extracted connection parameters.
    """
    config_dict = {
        'sasl.username': '$ConnectionString',
        'sasl.password': connection_string.strip(),
    }
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                    '"').replace('sb://', '').replace('/', '')+':9093'
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=')[1].strip('"')
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    return config_dict


def main():
    """
    Main function to parse arguments and start the NOAA data poller.
    """
    parser = argparse.ArgumentParser(description="NOAA Data Poller")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store the last polled times for each station and product")
    parser.add_argument('--kafka-bootstrap-servers', type=str,
                        help="Comma separated list of Kafka bootstrap servers")
    parser.add_argument('--kafka-topic', type=str,
                        help="Kafka topic to send messages to")
    parser.add_argument('--sasl-username', type=str,
                        help="Username for SASL PLAIN authentication")
    parser.add_argument('--sasl-password', type=str,
                        help="Password for SASL PLAIN authentication")
    parser.add_argument('--connection-string', type=str,
                        help='Microsoft Event Hubs or Microsoft Fabric Event Stream connection string')
    parser.add_argument('--station', type=str,
                        help='Station ID to poll data for. If not provided, data for all stations will be polled.')

    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.last_polled_file:
        args.last_polled_file = os.getenv('NOAA_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.noaa_last_polled.json')

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = config_params.get('bootstrap.servers')
        kafka_topic = config_params.get('kafka_topic')
        sasl_username = config_params.get('sasl.username')
        sasl_password = config_params.get('sasl.password')
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    # Check if required parameters are provided
    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided either through the command line or connection string.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided either through the command line or connection string.")
        sys.exit(1)
    if not sasl_username or not sasl_password:
        print("Error: SASL username and password must be provided either through the command line or connection string.")
        sys.exit(1)

    kafka_config = {
        'bootstrap.servers': kafka_bootstrap_servers,
        'sasl.mechanisms': 'PLAIN',
        'security.protocol': 'SASL_SSL',
        'sasl.username': sasl_username,
        'sasl.password': sasl_password
    }

    poller = NOAADataPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file,
        station=args.station
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
