from typing import Any, List, Dict, Union
import time
import argparse
import json
import requests


from cloudevents.http import to_structured
from cloudevents.http.event import CloudEvent
from azure.eventhub import EventHubProducerClient, EventData


def list_stations() -> List[Dict[str, Any]]:
    """List all available stations."""
    stations = requests.get('https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json', timeout=10).json()
    return stations


def get_water_level(station: str) -> List[Dict[str, Any]]:
    """Get water level for the specified station."""
    measurements = requests.get(
        f'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{station}/W/currentmeasurement.json', timeout=10).json()
    return measurements


def send_cloud_event(producer: EventHubProducerClient, event: Union[Dict[str, Any], CloudEvent]) -> None:
    """Send CloudEvent to Event Hub."""
    producer.send_event(EventData(event))


def feed_stations(event_hub_connection_str: str, event_hub_name: str, polling_interval: int) -> None:
    """Feed stations and send updates as CloudEvents."""
    previous_readings: Dict[str, List[Dict[str, Any]]] = {}
    producer = EventHubProducerClient.from_connection_string(conn_str=event_hub_connection_str)
    if event_hub_name:
        producer.eventhub_name = event_hub_name
    while True:
        stations = list_stations()
        for station in stations:
            shortname = station['shortname']
            measurements = get_water_level(shortname)
            if shortname not in previous_readings or measurements != previous_readings[shortname]:
                event = CloudEvent(
                    {
                        "source": f"https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{shortname}",
                        "type": "pegelonline.station.reading",
                        "datacontenttype": "application/json",
                    },
                    measurements
                )
                send_cloud_event(producer, to_structured(event))
                previous_readings[shortname] = measurements
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
        feed_stations(args.connection_string, args.eventhub_name, args.polling_interval)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
