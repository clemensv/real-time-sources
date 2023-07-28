from azure.eventhub import EventHubProducerClient, EventData
from google.transit import gtfs_realtime_pb2
import requests
from google.protobuf.message import DecodeError
from datetime import datetime
import argparse
import time
from cloudevents.http import CloudEvent
from cloudevents.conversion import to_json
from math import radians, cos, sin, asin, sqrt

backoff_time: float = 0
poll_interval: float = 20
vehicle_last_report_times = {}
vehicle_last_positions = {}

def calculate_speed(last_position, current_position, last_report_time, current_report_time):
    """Calculate the speed between two positions"""
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [last_position.longitude, last_position.latitude, current_position.longitude, current_position.latitude])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c

    # Calculate speed in km/hr
    time_diff = current_report_time - last_report_time
    speed = km / (time_diff / 3600)
    return speed


def poll_and_submit_vehicle_locations(producer_client: EventHubProducerClient, feed_url: str, headers: dict, agency_tag: str, route: str | None):
    # Make a request to the GTFS Realtime API to get the vehicle locations for the specified route
    response = requests.get(feed_url, headers=headers)
    response.raise_for_status()

    # Parse the Protocol Buffer message and submit each vehicle location to the Event Hub
    try:
        feed_message = gtfs_realtime_pb2.FeedMessage()
        feed_message.ParseFromString(response.content)
    except DecodeError:
        raise ValueError("Failed to parse the GTFS Realtime message")

    event_data_batch = producer_client.create_batch(partition_key=agency_tag)
    for entity in feed_message.entity:
        if entity.HasField('vehicle'):
            vehicle = entity.vehicle
            vehicle_id = f"{agency_tag}/{vehicle.vehicle.id}"
            last_report_time = vehicle.timestamp
            if vehicle_id in vehicle_last_report_times and last_report_time <= vehicle_last_report_times[vehicle_id]:
                continue
            # if we have remembered a previous position for this vehicle, check if it has moved and calcuate the speed
            # if the speed value is 0
            if vehicle_id in vehicle_last_positions:
                last_position = vehicle_last_positions[vehicle_id]
                if last_position.latitude == vehicle.position.latitude and last_position.longitude == vehicle.position.longitude:
                    vehicle.position.speed = 0
                else:
                    vehicle.position.speed = calculate_speed(last_position, vehicle.position, vehicle_last_report_times[vehicle_id], last_report_time)
            vehicle_last_positions[vehicle_id] = vehicle.position                    

            event_detail = {
                "agency": agency_tag,
                "routeTag": vehicle.trip.route_id,
                "dirTag": vehicle.trip.trip_id,  # Trip ID can act as direction ID in GTFS
                "id": vehicle.vehicle.id,
                "lat": vehicle.position.latitude,
                "lon": vehicle.position.longitude,
                "predictable": None,  # GTFS does not have a direct equivalent for this field
                "heading": vehicle.position.bearing,
                "speedKmHr": vehicle.position.speed,
                "timestamp": last_report_time
            }
            last_report_time_iso = datetime.utcfromtimestamp(last_report_time).isoformat()

            event = CloudEvent({
                "specversion": "1.0",
                "type": "gtfs.vehiclePosition",
                "source": f"uri:{agency_tag}",
                "subject": f"{agency_tag}/{vehicle.vehicle.id}",
                "datacontenttype": "application/json",
                "time": last_report_time_iso
            })
            event.data = event_detail
            try:
                event_data_batch.add(create_event_data(event))
            except ValueError:
                # batch is full, send it and create a new one
                producer_client.send_batch(event_data_batch)
                event_data_batch = producer_client.create_batch(partition_key=agency_tag)
                event_data_batch.add(create_event_data(event))
            vehicle_last_report_times[vehicle_id] = last_report_time

    producer_client.send_batch(event_data_batch)
    print(f"Sent {len(event_data_batch)} vehicle positions")

def feed(feed_connection_string: str, feed_event_hub_name: str, agency_tag: str, feed_url: str, headers: dict, route: str | None):
    """Poll vehicle locations and submit to an Event Hub"""
    feed_producer_client = EventHubProducerClient.from_connection_string(feed_connection_string, eventhub_name=feed_event_hub_name)
    
    try:
        while True:
            poll_and_submit_vehicle_locations(feed_producer_client, feed_url, headers, agency_tag, route)
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("Loop interrupted by user")

    # Close the Event Hub producer client
    feed_producer_client.close()

def create_event_data(event : CloudEvent) -> EventData:
    event_json = to_json(event)                
    event_data = EventData(event_json)
    event_data.content_type = "application/cloudevents+json; charset=utf-8"
    event_data.properties = {
            "cloudEvents:specversion": event['specversion'],
            "cloudEvents:type": event['type'],
            "cloudEvents:source": event['source'],
            "cloudEvents:id": event['id'],
            "cloudEvents:time": event['time'],
            "cloudEvents:subject": event['subject'],
        }
    
    return event_data

def print_vehicle_locations(feed_url: str, headers: dict, agency, route):
    # Make a request to the GTFS Realtime API to get the vehicle locations for the specified route
    response = requests.get(feed_url, headers=headers)
    response.raise_for_status()

    # Parse the Protocol Buffer message and submit each vehicle location to the Event Hub
    try:
        feed_message = gtfs_realtime_pb2.FeedMessage()
        feed_message.ParseFromString(response.content)
    except DecodeError:
        raise ValueError("Failed to parse the GTFS Realtime message")

    for entity in feed_message.entity:
        if entity.HasField('vehicle') and (route == None or entity.vehicle.trip.route_id == route):
            vehicle = entity.vehicle
            print(f"{vehicle.vehicle.id}: ({vehicle.position.latitude},{vehicle.position.longitude}), heading {vehicle.position.bearing}°, {vehicle.position.speed} km/h, https://geohack.toolforge.org/geohack.php?language=en&params={vehicle.position.latitude};{vehicle.position.longitude}")


def main():
    # Define the command-line arguments and subcommands
    parser = argparse.ArgumentParser(description="Real-time transit data for NextBus")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    # Define the "feed" command
    feed_parser = subparsers.add_parser("feed", help="poll vehicle locations and submit to an Event Hub")
    feed_parser.add_argument("--feed-connection-string", help="the connection string for the Event Hub namespace", required=True)
    feed_parser.add_argument("--feed-event-hub-name", help="the name of the Event Hub to submit to", required=True)
    feed_parser.add_argument("--agency", help="the tag of the agency to poll vehicle locations for", required=False)
    feed_parser.add_argument("--route", help="the route to poll vehicle locations for, omit or '*' to poll all routes", required=False, default="*")
    feed_parser.add_argument("--gtfs-url", help="the URL of the GTFS Realtime feed", required=True)
    feed_parser.add_argument('--header', action='append', nargs=2, help='HTTP header to send with the request to the GTFS Realtime feed')
    feed_parser.add_argument("--poll-interval", help="the number of seconds to wait between polling vehicle locations", required=False, type=float, default=20)
    feed_parser.set_defaults(func=lambda args: launch_feed(args))

    # Define the "vehicle-locations" command
    vehicle_locations_parser = subparsers.add_parser("vehicle-locations", help="get the vehicle locations for a route")
    vehicle_locations_parser.add_argument("--agency", help="the tag of the agency to get vehicle locations for", required=True)
    vehicle_locations_parser.add_argument("--route", help="the route to get vehicle locations for", required=False)
    vehicle_locations_parser.add_argument("--gtfs-url", help="the URL of the GTFS Realtime feed", required=True)
    vehicle_locations_parser.add_argument('--header', action='append', nargs=2, help='HTTP header to send with the request to the GTFS Realtime feed')

    vehicle_locations_parser.set_defaults(func=lambda args: print_vehicle_locations(args.gtfs_url, {k: v for k, v in args.param} if 'param' in args else None, args.agency, args.route))

    # Parse the command-line arguments and execute the selected command
    args = parser.parse_args()
    # Check if the 'func' attribute is present in the 'Namespace' object
    if hasattr(args, 'func') and callable(args.func):
        args.func(args)
    else:
        parser.print_help()

def launch_feed(args):
    backoff_time = args.backoff_interval
    poll_interval = args.poll_interval
    headers = None
    if args.header:
        headers = {k: v for k, v in args.header}
    feed(args.feed_connection_string, args.feed_event_hub_name, args.agency, args.gtfs_url, headers, args.route)

if __name__ == "__main__":
    main()


