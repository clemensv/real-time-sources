from datetime import datetime, timezone
import os
import time
import argparse
import json
from dataclasses import dataclass
from cloudevents.http import CloudEvent

from nextbus_core import (
    NEXTBUS_BASE_URL,
    USER_AGENT,
    element_to_dict,
    get_route_config_updates,
    get_schedule_updates,
    get_message_updates,
    get_vehicle_positions,
    print_agencies,
    print_routes,
    print_route_predictions,
    print_stops,
    print_vehicle_locations,
    print_predictions,
)

backoff_time: float = 0
poll_interval: float = 10

@dataclass
class KafkaEventData:
    event: CloudEvent

    @property
    def properties(self):
        return {
            "cloudEvents:specversion": self.event["specversion"],
            "cloudEvents:type": self.event["type"],
            "cloudEvents:source": self.event["source"],
            "cloudEvents:id": self.event["id"],
            "cloudEvents:time": self.event["time"],
            "cloudEvents:subject": self.event["subject"],
        }


class KafkaEventBatch:
    def __init__(self, partition_key: str | None = None):
        self.partition_key = partition_key
        self.events: list[KafkaEventData] = []

    def add(self, event_data: KafkaEventData):
        self.events.append(event_data)

    def __len__(self):
        return len(self.events)


class NextbusKafkaProducerClient:
    def __init__(self, producer):
        self.producer = producer

    @classmethod
    def from_connection_string(cls, connection_string: str, topic: str | None = None):
        from nextbus_producer_kafka_producer.producer import NextbusKafkaEventProducer

        return cls(NextbusKafkaEventProducer.from_connection_string(connection_string, topic=topic))

    def create_batch(self, partition_key: str | None = None):
        return KafkaEventBatch(partition_key)

    def send_event(self, event_data: KafkaEventData, partition_key: str | None = None):
        self._send_event(event_data.event)

    def send_batch(self, event_data_batch: KafkaEventBatch):
        for event_data in event_data_batch.events:
            self._send_event(event_data.event)

    def close(self):
        self.producer.producer.flush()

    def _send_event(self, event: CloudEvent):
        from nextbus_producer_data import Message, RouteConfig, Schedule, VehiclePosition

        data = event.data
        event_type = event["type"]
        if event_type == "nextbus.VehiclePosition":
            payload = VehiclePosition(
                agency_id=data["agency"],
                route_tag=data.get("routeTag") or "",
                vehicle_id=data["id"],
                stop_or_vehicle_id=data["id"],
                event_type="vehicle",
                lat=data.get("lat"),
                lon=data.get("lon"),
                timestamp=data.get("timestamp"),
            )
            self.producer.send_nextbus_kafka_vehicle_position(
                payload.agency_id, payload.route_tag, payload.vehicle_id, payload, _time=event["time"]
            )
        elif event_type == "nextbus.RouteConfig":
            payload = RouteConfig(
                agency_id=data["agency"],
                route_tag=data["routeTag"],
                stop_or_vehicle_id=data["routeTag"],
                event_type="route-config",
                route_config=data["routeConfig"],
            )
            self.producer.send_nextbus_kafka_route_config(
                payload.agency_id, payload.route_tag, payload.stop_or_vehicle_id, payload, _time=event["time"]
            )
        elif event_type == "nextbus.Schedule":
            payload = Schedule(
                agency_id=data["agency"],
                route_tag=data["routeTag"],
                stop_or_vehicle_id=data["routeTag"],
                event_type="schedule",
                schedule=data["schedule"],
            )
            self.producer.send_nextbus_kafka_schedule(
                payload.agency_id, payload.route_tag, payload.stop_or_vehicle_id, payload, _time=event["time"]
            )
        elif event_type == "nextbus.Message":
            payload = Message(
                agency_id=data["agency"],
                route_tag=data["routeTag"],
                stop_or_vehicle_id=data["routeTag"],
                event_type="message",
                message=data["messages"],
            )
            self.producer.send_nextbus_kafka_message(
                payload.agency_id, payload.route_tag, payload.stop_or_vehicle_id, payload, _time=event["time"]
            )
        else:
            raise ValueError(f"Unsupported Nextbus event type: {event_type}")


def poll_and_submit_route_config(producer_client: NextbusKafkaProducerClient, agency_tag: str):
    """Fetch changed route configs and submit as CloudEvents to Kafka."""
    for rc_data in get_route_config_updates(agency_tag, backoff_time=backoff_time):
        route_tag = rc_data["routeTag"]
        event = CloudEvent({
            "specversion": "1.0",
            "type": "nextbus.RouteConfig",
            "source": "https://retro.umoiq.com/service/publicXMLFeed",
            "subject": f"{agency_tag}/{route_tag}/route-config/{route_tag}",
            "datacontenttype": "application/json",
            "time": datetime.now(timezone.utc).isoformat()
        })
        event.data = rc_data
        producer_client.send_event(create_event_data(event), partition_key=f"route/{agency_tag}/{route_tag}")
        print(f"Sent route config for {agency_tag}/{route_tag}")


def poll_and_submit_schedule(producer_client: NextbusKafkaProducerClient, agency_tag: str):
    """Fetch changed schedules and submit as CloudEvents to Kafka."""
    for sched_data in get_schedule_updates(agency_tag, backoff_time=backoff_time):
        route_tag = sched_data["routeTag"]
        event = CloudEvent({
            "specversion": "1.0",
            "type": "nextbus.Schedule",
            "source": "https://retro.umoiq.com/service/publicXMLFeed",
            "subject": f"{agency_tag}/{route_tag}/schedule/{route_tag}",
            "datacontenttype": "application/json",
            "time": datetime.now(timezone.utc).isoformat()
        })
        event.data = sched_data
        producer_client.send_event(create_event_data(event), partition_key=f"schedule/{agency_tag}/{route_tag}")
        print(f"Sent schedule for {agency_tag}/{route_tag}")


def poll_and_submit_messages(producer_client: NextbusKafkaProducerClient, agency_tag: str):
    """Fetch changed messages and submit as CloudEvents to Kafka."""
    for msg_data in get_message_updates(agency_tag, backoff_time=backoff_time):
        route_tag = msg_data["routeTag"]
        event = CloudEvent({
            "specversion": "1.0",
            "type": "nextbus.Message",
            "source": "https://retro.umoiq.com/service/publicXMLFeed",
            "subject": f"{agency_tag}/{route_tag}/message/{route_tag}",
            "datacontenttype": "application/json",
            "time": datetime.now(timezone.utc).isoformat()
        })
        event.data = msg_data
        producer_client.send_event(create_event_data(event), partition_key=f"messages/{agency_tag}/{route_tag}")
        print(f"Sent messages for {agency_tag}/{route_tag}")


def poll_and_submit_vehicle_locations(producer_client: NextbusKafkaProducerClient, agency_tag: str, route: str | None, last_time: float | None):
    """Fetch vehicle positions and submit as CloudEvents to Kafka."""
    positions, feed_last_time = get_vehicle_positions(agency_tag, route, last_time)
    if feed_last_time is None:
        return last_time

    event_data_batch = producer_client.create_batch(partition_key=agency_tag)
    for vp in positions:
        last_report_time_iso = datetime.utcfromtimestamp(vp["timestamp"]).isoformat()
        event = CloudEvent({
            "specversion": "1.0",
            "type": "nextbus.VehiclePosition",
            "source": "https://retro.umoiq.com/service/publicXMLFeed",
            "subject": f"{agency_tag}/{vp.get('routeTag')}/vehicle/{vp.get('id')}",
            "datacontenttype": "application/json",
            "time": last_report_time_iso
        })
        event.data = vp
        try:
            event_data_batch.add(create_event_data(event))
        except ValueError:
            producer_client.send_batch(event_data_batch)
            event_data_batch = producer_client.create_batch(partition_key=agency_tag)
            event_data_batch.add(create_event_data(event))

    producer_client.send_batch(event_data_batch)
    print(f"Sent {len(event_data_batch)} vehicle positions")
    return feed_last_time

def create_event_data(event : CloudEvent) -> KafkaEventData:
    return KafkaEventData(event)


def feed(feed_connection_string: str, feed_topic: str | None, reference_connection_string: str | None, reference_topic: str | None, agency_tag: str, route: str | None, once: bool = False):
    """Poll vehicle locations and submit CloudEvents through the Kafka endpoint."""
    feed_producer_client = NextbusKafkaProducerClient.from_connection_string(feed_connection_string, topic=feed_topic)
    reference_producer_client = feed_producer_client
    if reference_connection_string:
        reference_producer_client = NextbusKafkaProducerClient.from_connection_string(reference_connection_string, topic=reference_topic)

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
            if once:
                break
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("Loop interrupted by user")
    finally:
        feed_producer_client.close()
        if reference_producer_client is not None:
            if reference_producer_client is not feed_producer_client:
                reference_producer_client.close()


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
    _feed_cs = os.environ.get("CONNECTION_STRING") or os.environ.get("FEED_CONNECTION_STRING")
    _feed_topic = os.environ.get("KAFKA_TOPIC") or os.environ.get("FEED_EVENT_HUB_NAME")
    _ref_cs = os.environ.get("REFERENCE_CONNECTION_STRING")
    _ref_topic = os.environ.get("REFERENCE_KAFKA_TOPIC") or os.environ.get("REFERENCE_EVENT_HUB_NAME")
    _agency = os.environ.get("AGENCY")
    feed_parser = subparsers.add_parser("feed", help="poll vehicle locations and submit to a Kafka-compatible endpoint")
    feed_parser.add_argument("--feed-connection-string", "--connection-string", help="the Kafka/Event Streams connection string", default=_feed_cs, required=_feed_cs is None)
    feed_parser.add_argument("--feed-event-hub-name", "--topic", dest="feed_topic", help="optional Kafka topic override; defaults to EntityPath in the connection string", default=_feed_topic, required=False)
    feed_parser.add_argument("--reference-connection-string", help="optional separate connection string for reference data", default=_ref_cs, required=False)
    feed_parser.add_argument("--reference-event-hub-name", "--reference-topic", dest="reference_topic", help="optional separate topic for reference data", default=_ref_topic, required=False)
    feed_parser.add_argument("--agency", help="the tag of the agency to poll vehicle locations for", default=_agency, required=_agency is None)
    feed_parser.add_argument("--route", help="the route to poll vehicle locations for, omit or '*' to poll all routes", required=False, default=os.environ.get("ROUTE", "*"))
    feed_parser.add_argument("--poll-interval", help="the number of seconds to wait between polling vehicle locations", required=False, type=float, default=float(os.environ.get("POLLING_INTERVAL") or os.environ.get("POLL_INTERVAL", "10")))
    feed_parser.add_argument("--backoff-interval", help="the number of seconds to wait before retrying after an error", required=False, type=float, default=float(os.environ.get("BACKOFF_INTERVAL", "0")))
    feed_parser.add_argument("--once", action="store_true", default=os.environ.get("ONCE_MODE", "").lower() in ("1", "true", "yes"), help="Run a single polling cycle and exit")
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
    global backoff_time, poll_interval
    backoff_time = args.backoff_interval
    poll_interval = args.poll_interval
    feed(args.feed_connection_string, args.feed_topic, args.reference_connection_string, args.reference_topic, args.agency, args.route, once=args.once)

if __name__ == "__main__":
    main()

