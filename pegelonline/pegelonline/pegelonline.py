""" Interact with the German WSV PegelOnline API to fetch water level data for rivers in Germany. """

import asyncio
from typing import Any, List, Dict, Union
import time
import argparse
import json
import requests
import logging
import sys

from confluent_kafka import Producer
from pegelonline_producer_data.de.wsv.pegelonline.currentmeasurement import CurrentMeasurement
from pegelonline_producer_data.de.wsv.pegelonline.station import Station
from pegelonline_producer_data.de.wsv.pegelonline.water import Water
from pegelonline_producer_kafka_producer.producer import DeWsvPegelonlineEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

def list_stations() -> List[Dict[str, Any]]:
    """List all available stations."""
    stations = requests.get('https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json', timeout=10).json()
    return stations


def get_water_level(station: str) -> Dict[str, Any]:
    """Get water level for the specified station."""
    response = requests.get(f'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{station}/W/currentmeasurement.json', timeout=10)
    if response.status_code == 404:
        return None
    measurements = response.json()
    return measurements


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

async def feed_stations(connection_string: str, event_hub_name: str, polling_interval: int) -> None:
    """Feed stations and send updates as CloudEvents."""
    previous_readings: Dict[str, List[Dict[str, Any]]] = {}

    if connection_string:
        config_params = parse_connection_string(connection_string)
        kafka_bootstrap_servers = config_params.get('bootstrap.servers')
        kafka_topic = config_params.get('kafka_topic')
        sasl_username = config_params.get('sasl.username')
        sasl_password = config_params.get('sasl.password')
    else:
        raise ValueError("Event Hub connection string is required")

    if event_hub_name:
        kafka_topic = event_hub_name

    kafka_config = {
        "bootstrap.servers": kafka_bootstrap_servers,
        "sasl.mechanisms": "PLAIN",
        "security.protocol": "SASL_SSL",
        "sasl.username": sasl_username,
        "sasl.password": sasl_password,
        "acks": "all",
        "linger.ms": 100,
        "retries": 5,
        "retry.backoff.ms": 1000,
        "batch.size": 512*1024
    }
    producer: Producer = Producer(kafka_config)
    pegelonline_producer = DeWsvPegelonlineEventProducer(producer, kafka_topic)

    stations = list_stations()
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

    while True:
        for station in stations:
            shortname = station['shortname']
            measurement = get_water_level(station['uuid'])
            if measurement and ((shortname not in previous_readings) or (measurement != previous_readings[shortname])):
                logging.debug("Sending current measurement for station %s", shortname)
                await pegelonline_producer.send_de_wsv_pegelonline_current_measurement(
                    _feedurl=f"https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{shortname}/W/currentmeasurement.json",
                    _station_id=shortname,
                    data=CurrentMeasurement(
                        station_uuid=station['uuid'],
                        timestamp=measurement['timestamp'],
                        value=measurement['value'],
                        stateMnwMhw=measurement['stateMnwMhw'],
                        stateNswHsw=measurement['stateNswHsw']
                    ),
                    flush_producer=False
                )
                previous_readings[shortname] = measurement
        producer.flush()
        time.sleep(polling_interval)
    producer.close()


def main() -> None:
    """
    Interact with Pegel Online API to fetch water level data.
    Usage:
        python pegelonline.py list
        python pegelonline.py station <shortname>
        python pegelonline.py feed --event_hub_connection_str <connection_str> --event_hub_name <hub_name> [--polling_interval <interval>]
    Options:
        list                List all available stations
        station <shortname>         Get water level for the specified station
        feed                         Feed stations and send updates as CloudEvents
    Arguments:
        <shortname>                 Short name of the station
    Options for 'feed' command:
        --connection-strring   Event Hub connection string
        --event-hub-name             Event Hub name
        --polling-interval           Polling interval in seconds (default: 60)
    """
    parser = argparse.ArgumentParser(description='Interact with Pegel Online API to fetch water level data.')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list', help='List all available stations')

    station_parser = subparsers.add_parser('level', help='Get water level for the specified station')
    station_parser.add_argument('shortname', type=str, help='Short name of the station')

    feed_parser = subparsers.add_parser('feed', help='Feed stations and send updates as CloudEvents')
    feed_parser.add_argument("-c", "--connection-string", type=str, required=True, help='Event Hub connection string')
    feed_parser.add_argument("-e", "--eventhub-name", type=str, required=False, help='Event Hub name')
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=60, help='Polling interval in seconds')

    args = parser.parse_args()

    if args.command == 'list':
        station_list = list_stations()
        for station in station_list:
            print(f"{station['uuid']}: {station['shortname']}")
    elif args.command == 'level':
        measurements = get_water_level(args.shortname)
        print(json.dumps(measurements, indent=4))
    elif args.command == 'feed':
        if not args.eventhub_name:
            # test whether there is an EntityName in the connection string
            if not "EntityPath=" in args.connection_string:
                print("Error: Event Hub name is required")
                return
        asyncio.run(feed_stations(args.connection_string, args.eventhub_name, args.polling_interval))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
