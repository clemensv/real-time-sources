from datetime import datetime, timezone
import time
import requests
import xml.etree.ElementTree as ET
from azure.eventhub import EventHubProducerClient, EventData
import argparse
import json
from cloudevents.http import CloudEvent
from cloudevents.conversion import to_json

NEXTBUS_BASE_URL = "https://retro.umoiq.com/service/publicXMLFeed"   
backoff_time: float = 0
poll_interval: float = 10

def print_route_predictions(agency_tag, route_tag):
    # Make a request to the NextBus API to get the predictions for the specified route
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "predictions", "a": agency_tag, "r": route_tag})
    if response.status_code == 404:
        return
    
    response.raise_for_status()

    # Parse the XML response and print the predictions for the route
    root = ET.fromstring(response.content)
    for direction in root.findall("predictions/direction"):
        print(f"Direction: {direction.get('title')}")
        for prediction in direction.findall("prediction"):
            print(f"  {prediction.get('minutes')} minutes")

def print_stops(agency_tag, route_tag):
    # Make a request to the NextBus API to get the configuration for the specified route
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "routeConfig", "a": agency_tag, "r": route_tag})
    if response.status_code == 404:
        return

    response.raise_for_status()

    # Parse the XML response and print the stops for the route
    root = ET.fromstring(response.content)
    for stop in root.findall("route/stop"):
        print(f"{stop.get('tag')}: {stop.get('title')}, ({stop.get('lat')},{stop.get('lon')}), https://geohack.toolforge.org/geohack.php?language=en&params={stop.get('lat')};{stop.get('lon')}")
        
def print_agencies():
    # Make a request to the NextBus API to get the list of agencies
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "agencyList"})
    if response.status_code == 404:
        return

    # Parse the XML response and print the list of agencies with tags and names
    root = ET.fromstring(response.content)
    for agency in root.findall("agency"):
        print(f"{agency.get('tag')}: {agency.get('title')}")

def print_routes(agency_tag):
    # Make a request to the NextBus API to get the list of routes for the specified agency
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "routeList", "a": agency_tag})
    if response.status_code == 404:
        return
    
    response.raise_for_status()

    # Parse the XML response and print the list of routes for the agency
    root = ET.fromstring(response.content)
    for route in root.findall("route"):
        print(f"{route.get('tag')}: {route.get('title')}")


def element_to_dict(element):
    data = {}
    for child in element:
        if len(child) > 0 or child.attrib:
            if child.tag in data:
                if not isinstance(data[child.tag], list):
                    data[child.tag] = [data[child.tag]]
                data[child.tag].append(element_to_dict(child))
            else:
                data[child.tag] = element_to_dict(child)
        else:
            data[child.tag] = child.text

    # Add attributes directly to the dictionary
    data.update(element.attrib)
    return data

route_checksums = {}
def poll_and_submit_route_config(producer_client: EventHubProducerClient, agency_tag: str):
    # Make a request to the NextBus API to get the list of routes for the specified agency
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "routeList", "a": agency_tag})
    if response.status_code == 404:
        return
    
    response.raise_for_status()

    # Parse the XML response and submit the route configuration for each route to the Event Hub
    root = ET.fromstring(response.content)
    for route in root.findall("route"):
        route_tag = route.get("tag")
        # slow down the request rate
        time.sleep(backoff_time)        
        
        response = requests.get(NEXTBUS_BASE_URL, params={"command": "routeConfig", "a": agency_tag, "r": route_tag})
        if response.status_code == 404:
            # API is flaky, try again
            response = requests.get(NEXTBUS_BASE_URL, params={"command": "routeConfig", "a": agency_tag, "r": route_tag})
            if response.status_code == 404:
                print(f"404 for {agency_tag}/{route_tag}")
                continue
        
        response.raise_for_status()
        content = response.content
        checksum = hash(content)
        if route_tag in route_checksums and route_checksums[route_tag] == checksum:
            continue
        route_checksums[route_tag] = checksum
        root = ET.fromstring(response.content)
        route_config = {
            "agency": agency_tag,
            "routeTag": route_tag,
            "routeConfig": json.dumps(element_to_dict(root)),
        }
        # Create a CloudEvent of type nextbus.routeConfig
        event = CloudEvent({
            "specversion": "1.0",
            "type": "nextbus.routeConfig",
            "source": "https://retro.umoiq.com/service/publicXMLFeed",
            "subject": f"{agency_tag}/{route_tag}",
            "datacontenttype": "application/json",
            "time": datetime.now(timezone.utc).isoformat()
        })  
        event.data = route_config      
        event_data = create_event_data(event)
        producer_client.send_event(event_data, partition_key=f"route/{agency_tag}/{route_tag}")
        print(f"Sent route config for {agency_tag}/{route_tag}")
        

schedule_checksums = {}

def poll_and_submit_schedule(producer_client: EventHubProducerClient, agency_tag: str):
    # Make a request to the NextBus API to get the list of routes for the specified agency
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "routeList", "a": agency_tag})
    if response.status_code == 404:
        return
    
    response.raise_for_status()

    # Parse the XML response and submit the schedule for each route to the Event Hub
    root = ET.fromstring(response.content)
    for route in root.findall("route"):
        route_tag = route.get("tag")
        # slow down the request rate
        time.sleep(backoff_time)        
        response = requests.get(NEXTBUS_BASE_URL, params={"command": "schedule", "a": agency_tag, "r": route_tag})
        if response.status_code == 404:
            print(f"404 for {agency_tag}/{route_tag}")
            continue
        response.raise_for_status()
        content = response.content
        checksum = hash(content)
        if route_tag in schedule_checksums and schedule_checksums[route_tag] == checksum:
            continue
        schedule_checksums[route_tag] = checksum
        root = ET.fromstring(response.content)
        schedule = {
            "agency": agency_tag,
            "routeTag": route_tag,
            "schedule": json.dumps(element_to_dict(root)),
        }
        # Create a CloudEvent of type nextbus.schedule
        event = CloudEvent({
            "specversion": "1.0",
            "type": "nextbus.schedule",
            "source": "https://retro.umoiq.com/service/publicXMLFeed",
            "subject": f"{agency_tag}/{route_tag}",
            "datacontenttype": "application/json",
            "time": datetime.now(timezone.utc).isoformat()
        })  
        event.data = schedule      
        event_data = create_event_data(event)
        producer_client.send_event(event_data, partition_key=f"schedule/{agency_tag}/{route_tag}")
        print(f"Sent schedule for {agency_tag}/{route_tag}")

messages_checksums = {}
def poll_and_submit_messages(producer_client : EventHubProducerClient, agency_tag : str):
    # Make a request to the NextBus API to get the list of routes for the specified agency
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "routeList", "a": agency_tag})
    if response.status_code == 404:
        return
    
    response.raise_for_status()

    # Parse the XML response and submit the schedule for each route to the Event Hub
    root = ET.fromstring(response.content)
    for route in root.findall("route"):
        route_tag = route.get("tag")
        # slow down the request rate
        time.sleep(backoff_time)        
        response = requests.get(NEXTBUS_BASE_URL, params={"command": "messages", "a": agency_tag, "r": route_tag})
        if response.status_code == 404:
            print(f"404 for {agency_tag}/{route_tag}")
            continue
        response.raise_for_status()
        content = response.content
        checksum = hash(content)
        if route_tag in messages_checksums and messages_checksums[route_tag] == checksum:
            continue
        messages_checksums[route_tag] = checksum
        root = ET.fromstring(response.content)
        messages = {
            "agency": agency_tag,
            "routeTag": route_tag,
            "messages": json.dumps(element_to_dict(root)),
        }
        # Create a CloudEvent of type nextbus.messages
        event = CloudEvent({
            "specversion": "1.0",
            "type": "nextbus.messages",
            "source": "https://retro.umoiq.com/service/publicXMLFeed",
            "subject": f"{agency_tag}/{route_tag}",
            "datacontenttype": "application/json",
            "time": datetime.now(timezone.utc).isoformat()
        })  
        event.data = messages      
        event_data = create_event_data(event)
        producer_client.send_event(event_data, partition_key=f"messages/{agency_tag}/{route_tag}")
        print(f"Sent messages for {agency_tag}/{route_tag}")



vehicle_last_report_times = {}

def poll_and_submit_vehicle_locations(producer_client: EventHubProducerClient, agency_tag: str, route: str | None, last_time : float | None):
    # Make a request to the NextBus API to get the vehicle locations for the specified route
    params = {"command": "vehicleLocations", "a": agency_tag}
    if route != "*":
        params["r"] = route
    if last_time is not None:
        params["t"] = int(last_time)

    
    response = requests.get(NEXTBUS_BASE_URL, params=params)
    if response.status_code == 404:
        return
    
    response.raise_for_status()

    # Parse the XML response and submit each vehicle location to the Event Hub
    root = ET.fromstring(response.content)
    event_data_batch = producer_client.create_batch(partition_key=agency_tag)
    vehicles = root.findall("vehicle")
    for vehicle in vehicles:
        vehicle_id = f"{agency_tag}/{vehicle.get('id')}"
        last_report_time = float(root.find("lastTime").get("time"))/1000 - float(vehicle.get("secsSinceReport"))
        if vehicle_id in vehicle_last_report_times and last_report_time <= vehicle_last_report_times[vehicle_id]:
            continue
        event_detail = {
            "agency": agency_tag,
            "routeTag": vehicle.get("routeTag"),
            "dirTag": vehicle.get("dirTag"),
            "id": vehicle.get("id"),
            "lat": vehicle.get("lat"),
            "lon": vehicle.get("lon"),
            "predictable": vehicle.get("predictable"),
            "heading": vehicle.get("heading"),
            "speedKmHr": vehicle.get("speedKmHr"),
            "timestamp": last_report_time
        }
        last_report_time_iso = datetime.utcfromtimestamp(last_report_time).isoformat()
            
        event = CloudEvent({
            "specversion": "1.0",
            "type": "nextbus.vehiclePosition",
            "source": "https://retro.umoiq.com/service/publicXMLFeed",
            "subject": f"{agency_tag}/{vehicle.get('id')}",
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
    return float(root.find("lastTime").get("time"))

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


def feed(feed_connection_string: str, feed_event_hub_name: str, reference_connection_string: str | None, reference_event_hub_name: str | None, agency_tag: str, route: str | None):
    """Poll vehicle locations and submit to an Event Hub"""
    feed_producer_client = EventHubProducerClient.from_connection_string(feed_connection_string, eventhub_name=feed_event_hub_name)
    reference_producer_client = None
    if reference_connection_string is not None:
        reference_producer_client = EventHubProducerClient.from_connection_string(reference_connection_string, eventhub_name=reference_event_hub_name)

    last_vehicle_location_time = time.time()
    last_route_config_time = last_schedule_time = last_messages_time = None

    try:
        while True:
            if reference_producer_client is not None:
                current_time = time.time()
                if last_route_config_time is None or current_time - last_route_config_time >= 3600:
                    poll_and_submit_route_config(reference_producer_client, agency_tag)
                    last_route_config_time = current_time
                if last_schedule_time is None or current_time - last_schedule_time >= 3600:
                    poll_and_submit_schedule(reference_producer_client, agency_tag)
                    last_schedule_time = current_time
                if last_messages_time is None or current_time - last_messages_time >= 3600:
                    poll_and_submit_messages(reference_producer_client, agency_tag)
                    last_messages_time = current_time
            last_vehicle_location_time = poll_and_submit_vehicle_locations(feed_producer_client, agency_tag, route, last_vehicle_location_time)
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("Loop interrupted by user")

    # Close the Event Hub producer client
    feed_producer_client.close()


def print_vehicle_locations(agency, route):
    # Make a request to the NextBus API to get the vehicle locations for the specified route
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "vehicleLocations", "a" : agency, "r": route})
    response.raise_for_status()

    # Parse the XML response and print the vehicle locations for the route
    root = ET.fromstring(response.content)
    for vehicle in root.findall("vehicle"):
        print(f"{vehicle.get('id')}: ({vehicle.get('lat')},{vehicle.get('lon')}), heading {vehicle.get('heading')}°, {vehicle.get('speedKmHr')} km/h, https://geohack.toolforge.org/geohack.php?language=en&params={vehicle.get('lat')};{vehicle.get('lon')}")

def print_predictions(agency_tag, stop_id, route_tag):
 
    # Make a request to the NextBus API to get the predictions for the specified stop
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "predictions", "a": agency_tag, "s": stop_id, "r": route_tag})
    response.raise_for_status()

    # Parse the XML response and print the predictions for the stop
    root = ET.fromstring(response.content)
    print(f"Predictions for stop {root.find('predictions').get('stopTitle')}")
    for prediction in root.findall("predictions/direction/prediction"):
        print(f"{prediction.get('minutes')} minutes ({prediction.get('seconds')} seconds), Vehicle {prediction.get('vehicle')}")

def main():
    # Define the command-line arguments and subcommands
    parser = argparse.ArgumentParser(description="Real-time transit data for NextBus")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    # Define the "agencies" command
    agencies_parser = subparsers.add_parser("agencies", help="get the list of transit agencies")
    agencies_parser.set_defaults(func=lambda args: print_agencies())

    # Define the "routes" command
    route_parser = subparsers.add_parser("routes", help="get the list of routes for an agency")
    route_parser.add_argument("--agency", help="the tag of the agency to get routes for")
    route_parser.set_defaults(func=lambda args: print_routes(args.agency))

    # Define the "feed" command
    feed_parser = subparsers.add_parser("feed", help="poll vehicle locations and submit to an Event Hub")
    feed_parser.add_argument("--feed-connection-string", help="the connection string for the Event Hub namespace", required=True)
    feed_parser.add_argument("--feed-event-hub-name", help="the name of the Event Hub to submit to", required=True)
    feed_parser.add_argument("--reference-connection-string", help="the connection string for the Event Hub namespace for reference data", required=False)
    feed_parser.add_argument("--reference-event-hub-name", help="the name of the Event Hub to submit reference data to", required=False)
    feed_parser.add_argument("--agency", help="the tag of the agency to poll vehicle locations for", required=False)
    feed_parser.add_argument("--route", help="the route to poll vehicle locations for, omit or '*' to poll all routes", required=False, default="*")
    feed_parser.add_argument("--poll-interval", help="the number of seconds to wait between polling vehicle locations", required=False, type=float, default=10)
    feed_parser.add_argument("--backoff-interval", help="the number of seconds to wait before retrying after an error", required=False, type=float, default=0)
    feed_parser.set_defaults(func=lambda args: launch_feed(args))

    # Define the "vehicle-locations" command
    vehicle_locations_parser = subparsers.add_parser("vehicle-locations", help="get the vehicle locations for a route")
    vehicle_locations_parser.add_argument("--agency", help="the tag of the agency to get vehicle locations for", required=True)
    vehicle_locations_parser.add_argument("--route", help="the route to get vehicle locations for", required=True)
    vehicle_locations_parser.set_defaults(func=lambda args: print_vehicle_locations(args.agency, args.route))

    # Define the "predictions" command
    predictions_parser = subparsers.add_parser("predictions", help="get the predictions for a stop")
    predictions_parser.add_argument("--agency", help="the tag of the agency to get predictions for", required=True)
    predictions_parser.add_argument("--stop-id", help="the ID of the stop to get predictions for", required=True)
    predictions_parser.add_argument("--route", help="the tag of the route to get predictions for", required=True)
    predictions_parser.set_defaults(func=lambda args: print_predictions(args.agency, args.stop_id, args.route))

    #define the "route-config" command
    route_config_parser = subparsers.add_parser("route-config", help="get the configuration for a route")
    route_config_parser.add_argument("--agency", help="the tag of the agency to get the route configuration for", required=True)
    route_config_parser.add_argument("--route", help="the route to get the configuration for", required=True)
    route_config_parser.set_defaults(func=lambda args: print_stops(args.agency, args.route))

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
    feed(args.feed_connection_string, args.feed_event_hub_name, args.reference_connection_string, args.reference_event_hub_name, args.agency, args.route)

if __name__ == "__main__":
    main()


