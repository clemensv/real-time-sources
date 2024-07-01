import argparse
import json
import requests
import time
from cloudevents.http import to_structured
from cloudevents.http.event import CloudEvent
from azure.eventhub import EventHubProducerClient, EventData

def list_stations():
    stations = requests.get('https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json').json()
    for station in stations:
        print(f"{station['uuid']}: {station['shortname']}")

def get_water_level(station):
    measurements = requests.get(f'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{station}/W/currentmeasurement.json').json()
    for measurement in measurements:
        print(json.dumps(measurement, indent=4))

def send_cloud_event(producer, event):
    event_data_batch = producer.create_batch()
    event_data_batch.add(EventData(event))
    producer.send_batch(event_data_batch)

def feed_stations(event_hub_connection_str, event_hub_name, polling_interval):
    previous_readings = {}
    producer = EventHubProducerClient.from_connection_string(conn_str=event_hub_connection_str, eventhub_name=event_hub_name)
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

def main():
    parser = argparse.ArgumentParser(description='Interact with Pegel Online API to fetch water level data.')
    subparsers = parser.add_subparsers(dest='command')

    list_stations_parser = subparsers.add_parser('list-stations', help='List all available stations')

    station_parser = subparsers.add_parser('station', help='Get water level for the specified station')
    station_parser.add_argument('shortname', type=str, help='Short name of the station')

    feed_parser = subparsers.add_parser('feed', help='Feed stations and send updates as CloudEvents')
    feed_parser.add_argument('--event_hub_connection_str', type=str, required=True, help='Event Hub connection string')
    feed_parser.add_argument('--event_hub_name', type=str, required=True, help='Event Hub name')
    feed_parser.add_argument('--polling_interval', type=int, default=60, help='Polling interval in seconds')

    args = parser.parse_args()

    if args.command == 'list-stations':
        list_stations()
    elif args.command == 'station':
        get_water_level(args.shortname)
    elif args.command == 'feed':
        feed_stations(args.event_hub_connection_str, args.event_hub_name, args.polling_interval)
    else:
        print("Please provide a valid command. Use --help for more information.")

if __name__ == "__main__":
    main()
