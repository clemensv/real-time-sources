"""
NOAA Data Poller
Polls NOAA data and sends it to a Kafka topic using SASL PLAIN authentication.
"""

import os
import json
import time
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import uuid
import requests
from confluent_kafka import Producer
from cloudevents.http import CloudEvent, to_structured
import argparse

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
        "air_gap": "product=air_gap",
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
        self.producer = Producer(kafka_config)
        self.stations = self.fetch_all_stations()
        if station:
            self.station = next((station for station in self.stations if station['id'] == station), None)
            if not self.station:
                print(f"Station {station} not found.")
                sys.exit(1)
        else:
            self.station = None
        

    def fetch_all_stations(self) -> list:
        """
        Fetch all NOAA stations.

        Returns:
            list: List of all NOAA stations.
        """
        url = "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            stations_data = response.json()
            stations = stations_data.get('stations', [])
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
        station_info:Any = next((station for station in self.stations if station['id'] == station_id), {})
        tide_type = station_info.get("tideType", "")
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
            response = requests.get(product_url)
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

    def create_cloud_event(self, data: dict, product: str, station: str, timestamp: datetime) -> tuple:
        """
        Create a CloudEvent from the data.

        Args:
            data (dict): The data to include in the event.
            product (str): The product name.
            station (str): The station ID.
            timestamp (datetime): The timestamp of the event.

        Returns:
            tuple: Headers and body of the CloudEvent.
        """
        attributes = {
            "type": f"Microsoft.OpenData.US.NOAA.{self.pascal(product)}",
            "source": f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station}.json",
            "subject": f"{station}",
            "time": timestamp.isoformat(),
            "id": str(uuid.uuid4()),
            "datacontenttype": "application/json"
        }
        event = CloudEvent(attributes, data)
        headers, body = to_structured(event)
        return headers, body

    def send_to_kafka(self, headers: Dict[str, str], body: bytes, key: bytes):
        """
        Send the CloudEvent to Kafka.

        Args:
            headers (Dict[str, str]): Headers of the CloudEvent.
            body (bytes): Body of the CloudEvent.
            key (bytes): Key for the Kafka message.
        """
        try:
            self.producer.produce(topic=self.kafka_topic, key=key, value=body, headers=headers)
        except Exception as err:
            print(f"Error sending data to Kafka: {err}")

    def load_last_polled_times(self) -> Dict:
        """
        Load the last polled times from a file.

        Returns:
            Dict: The last polled times for each station and product.
        """
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
            headers, body = self.create_cloud_event(station, "station", station['id'], datetime.now(timezone.utc))
            self.send_to_kafka(headers, body, key=station['id'].encode('utf-8'))
        self.producer.flush()      

        while True:
            for station in self.stations if not self.station else [self.station]:
                station_id = station['id']
                for product in self.PRODUCTS:
                    print(f"Polling {product} data for station {station_id}: {station['name']}:", end='')
                    last_polled_time = last_polled_times.get(product, {}).get(
                        station_id, datetime.now(timezone.utc) - timedelta(hours=24))
                    new_data_records = self.poll_noaa_api(product, station_id, last_polled_time)
                    print(f" {len(new_data_records)} new records found since {last_polled_time}")

                    max_timestamp = last_polled_time
                    for record in new_data_records:
                        ts_parsed = datetime.strptime(record['t'], "%Y-%m-%d %H:%M")
                        timestamp = ts_parsed.replace(tzinfo=timezone.utc)
                        record['t'] = timestamp.isoformat()
                        record['station_id'] = station_id
                        # if the 'v' field is present, convert it to a float
                        if 'v' in record:
                            record['v'] = float(record['v'])
                        # if the 's' field is present, convert it to a float
                        if 's' in record:
                            record['s'] = float(record['s'])
                        if timestamp > max_timestamp:
                            max_timestamp = timestamp
                        headers, body = self.create_cloud_event(record, product, station_id, timestamp)
                        self.send_to_kafka(headers, body, key=station_id.encode('utf-8'))

                    if new_data_records:
                        if product not in last_polled_times:
                            last_polled_times[product] = {}
                        last_polled_times[product][station_id] = max_timestamp
                        self.save_last_polled_times(last_polled_times)
                # flush all the station data to Kafka
                self.producer.flush()          
           

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
                config_dict['bootstrap.servers'] = part.split('=')[1].strip('"').replace('sb://', '').replace('/', '')+':9093'
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
                        default=os.path.expanduser('~/.noaa_last_polled.json'),
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
    parser.add_argument('--station', action='station', help='Station ID to poll data for. If not provided, data for all stations will be polled.')

    args = parser.parse_args()

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
