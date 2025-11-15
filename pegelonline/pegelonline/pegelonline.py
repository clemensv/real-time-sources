""" Interact with the German WSV PegelOnline API to fetch water level data for rivers in Germany. """

from datetime import datetime, timedelta, timezone
import os
from typing import Any, List, Dict
import asyncio
import logging
import sys
import time
import argparse
import json
import requests


from confluent_kafka import Producer
from pegelonline_producer_data.de.wsv.pegelonline.currentmeasurement import CurrentMeasurement
from pegelonline_producer_data.de.wsv.pegelonline.station import Station
from pegelonline_producer_data.de.wsv.pegelonline.water import Water
from pegelonline_producer_kafka_producer.producer import DeWsvPegelonlineEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


class PegelOnlineAPI:
    def __init__(self):
        self.skip_urls = []
        self.etags = {}
        self.session = requests.Session()

    def list_stations(self) -> List[Dict[str, Any]]:
        """List all available stations."""
        stations = self.session.get('https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json', timeout=10).json()
        return stations

    def get_water_level(self, station: str) -> Dict[str, Any] | None:
        """Get water level for the specified station."""
        url = f'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{station}/W/currentmeasurement.json'
        if url in self.skip_urls:
            return None
        etag = self.etags.get(url)
        headers = {'If-None-Match': etag} if etag else None
        response = self.session.get(url, headers=headers, timeout=10)
        if response.status_code != 200 and response.status_code != 304:
            logging.warning("Request to %s failed with status code %s. Sidelining URL.", url, response.status_code)
            self.skip_urls.append(url)
            return None
        elif response.status_code == 200:
            self.etags[url] = response.headers.get('ETag')
            measurements = response.json()
        elif response.status_code == 304:
            measurements = None
        return measurements
    
    def get_water_levels(self) -> Dict[str, Any]:
        """Get water levels for all stations."""
        station_levels = {}
        url = 'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json?includeTimeseries=true&includeCurrentMeasurement=true'
        response = self.session.get(url, timeout=10)
        if response.status_code != 200:
            logging.warning("Request to %s failed with status code %s.", url, response.status_code)
            return {}
        stations = response.json()
        for station in stations:
            if 'timeseries' in station:
                for timeseries in station['timeseries']:
                    if timeseries['shortname'] == 'W':
                        station_levels[station['uuid']] = timeseries['currentMeasurement']
                        station_levels[station['uuid']]['uuid'] = station['uuid']
        return station_levels

    def parse_connection_string(self, connection_string: str) -> Dict[str, str]:
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
                        '"').strip().replace('sb://', '').replace('/', '')+':9093'
                elif 'EntityPath' in part:
                    config_dict['kafka_topic'] = part.split('=')[1].strip('"').strip()
        except IndexError as e:
            raise ValueError("Invalid connection string format") from e
        return config_dict

    async def feed_stations(self, kafka_config: dict, kafka_topic: str, polling_interval: int) -> None:
        """Feed stations and send updates as CloudEvents."""
        previous_readings: Dict[str, List[Dict[str, Any]]] = {}

        producer: Producer = Producer(kafka_config)
        pegelonline_producer = DeWsvPegelonlineEventProducer(producer, kafka_topic)

        logging.info("Starting to feed stations to Kafka topic %s at bootstrap servers %s", kafka_topic, kafka_config['bootstrap.servers'])
        stations = self.list_stations()
        for station in stations:
            station_data = Station(
                uuid=station.get('uuid'),
                number=station.get('number'),
                shortname=station.get('shortname'),
                longname=station.get('longname'),
                km=station.get('km') if station.get('km') else -1,
                agency=station.get('agency'),
                longitude=station.get('longitude') if station.get('longitude') else -1,
                latitude=station.get('latitude') if station.get('latitude') else -1,
                water=Water(
                    shortname=station.get('water').get('shortname'),
                    longname=station.get('water').get('longname')
                )
            )
            await pegelonline_producer.send_de_wsv_pegelonline_station(
                _feedurl=f"https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{station['shortname']}",
                _station_id=station["uuid"],
                data=station_data, flush_producer=False)
        producer.flush()
        logging.info("Finished sending station data updates to Kafka topic %s", kafka_topic)

        while True:
            try:
                count = 0
                start_time = datetime.now(timezone.utc)
                measurements = self.get_water_levels()
                for station_id, measurement in measurements.items():
                    if (station_id not in previous_readings) or (measurement['timestamp'] != previous_readings[station_id]['timestamp']):
                        count += 1
                        logging.debug("Sending current measurement for station %s", measurement.get('uuid'))
                        try:
                            await pegelonline_producer.send_de_wsv_pegelonline_current_measurement(
                                _feedurl=f"https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{station_id}/W/currentmeasurement.json",
                                _station_id=station_id,
                                data=CurrentMeasurement(
                                    station_uuid=station_id,
                                    timestamp=measurement['timestamp'],
                                    value=measurement['value'],
                                    stateMnwMhw=measurement['stateMnwMhw'],
                                    stateNswHsw=measurement['stateNswHsw']
                                ),
                                flush_producer=False
                            )
                        # pylint: disable=broad-except
                        except Exception as e:
                            logging.error("Error sending to kafka: %s", e)
                        # pylint: enable=broad-except
                        previous_readings[station_id] = measurement
                producer.flush()
                end_time = datetime.now(timezone.utc)
                effective_polling_interval = max(0, polling_interval-(end_time - start_time).total_seconds())
                logging.info("Sent %s current measurements in %s seconds. Now waiting until %s.", count, (end_time - start_time).total_seconds(), (datetime.now(timezone.utc) + timedelta(seconds=effective_polling_interval)).isoformat())
                if effective_polling_interval > 0:
                    time.sleep(effective_polling_interval)
            except KeyboardInterrupt:
                logging.info("Exiting...")
                break
            # pylint: disable=broad-except
            except Exception as e:
                logging.error("Error occurred: %s", e)
                break
            # pylint: enable=broad-except
        producer.flush()


def main() -> None:
    """
    Interact with Pegel Online API to fetch water level data.
    Usage:
        python pegelonline.py list
        python pegelonline.py station <shortname>
        python pegelonline.py feed --event_hub_connection_str <connection_str> --event_hub_name <hub_name> [--polling_interval <interval>]
    Options:
        list                 List all available stations
        station <shortname>  Get water level for the specified station
        feed                 Feed stations and send updates as CloudEvents to a Kafka topic
    Arguments:
        <shortname>                 Short name of the station
    Options for 'feed' command:
        --kafka-bootstrap-servers <servers>    Comma separated list of Kafka bootstrap servers
        --kafka-topic <topic>                  Kafka topic to send messages to
        --sasl-username <username>             Username for SASL PLAIN authentication
        --sasl-password <password>             Password for SASL PLAIN authentication
        --connection-string <connection_str>   Microsoft Event Hubs or Microsoft Fabric Event Stream connection string
        --polling-interval <interval>          Polling interval in seconds
    """
    parser = argparse.ArgumentParser(description='Interact with Pegel Online API to fetch water level data.')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list', help='List all available stations')

    station_parser = subparsers.add_parser('level', help='Get water level for the specified station')
    station_parser.add_argument('shortname', type=str, help='Short name of the station')

    feed_parser = subparsers.add_parser('feed', help='Feed stations and send updates as CloudEvents')
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str,
                             help="Comma separated list of Kafka bootstrap servers", default=os.getenv('KAFKA_BOOTSTRAP_SERVERS'))
    feed_parser.add_argument('--kafka-topic', type=str, help="Kafka topic to send messages to",
                             default=os.getenv('KAFKA_TOPIC'))
    feed_parser.add_argument('--sasl-username', type=str,
                             help="Username for SASL PLAIN authentication", default=os.getenv('SASL_USERNAME'))
    feed_parser.add_argument('--sasl-password', type=str,
                             help="Password for SASL PLAIN authentication", default=os.getenv('SASL_PASSWORD'))
    feed_parser.add_argument('-c', '--connection-string', type=str,
                             help='Microsoft Event Hubs or Microsoft Fabric Event Stream connection string', default=os.getenv('CONNECTION_STRING'))
    polling_interval_default = 60
    if os.getenv('POLLING_INTERVAL'):
        polling_interval_default = int(os.getenv('POLLING_INTERVAL'))
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             help='Polling interval in seconds', default=polling_interval_default)

    args = parser.parse_args()

    api = PegelOnlineAPI()

    if args.command == 'list':
        station_list = api.list_stations()
        for station in station_list:
            print(f"{station['uuid']}: {station['shortname']}")
    elif args.command == 'level':
        measurements = api.get_water_level(args.shortname)
        print(json.dumps(measurements, indent=4))
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

        asyncio.run(api.feed_stations(kafka_config, kafka_topic, args.polling_interval))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
