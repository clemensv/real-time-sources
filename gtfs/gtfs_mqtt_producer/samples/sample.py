
"""
This is sample code to use the MQTT clients contained in this project.

The sample demonstrates both publishing and subscribing to MQTT messages with
the
producer and dispatcher functionality.

There is a handler for each defined message type. The handler is an async
function that takes the following parameters:
- mqtt_message: The paho.mqtt.client.MQTTMessage object (message context).
- cloud_event: The CloudEvent data (if using CloudEvents).
- message_data: The deserialized message data.The main function creates clients
for each message group that can both produce and consume messages.
It starts dispatchers to handle incoming messages and then publishes sample
messages.

The script either reads the configuration from the command line or uses the
environment variables. The following environment variables are recognized:

- MQTT_BROKER_HOST: The MQTT broker hostname.
- MQTT_BROKER_PORT: The MQTT broker port (default: 1883).
- MQTT_TOPIC: The MQTT topic to publish/subscribe to.
- MQTT_USERNAME: The MQTT username (optional).
- MQTT_PASSWORD: The MQTT password (optional).

Alternatively, you can pass the configuration as command-line arguments.

python sample.py --broker-host <broker_host> --broker-port <broker_port> --topic
<topic>

The main function waits for a signal (Press Ctrl+C) to stop.
"""

import argparse
import asyncio
import os
import signal
from gtfs_mqtt_producer_data import *
from gtfs_mqtt_producer_mqtt_client.client import GeneralTransitFeedRealTimeMqttProducer, GeneralTransitFeedRealTimeMqttDispatcher

async def handle_general_transit_feed_real_time_vehicle_vehicle_position_mqtt(mqtt_msg,cloud_event, general_transit_feed_real_time_vehicle_vehicle_position_mqtt_data):
    """ Handles the GeneralTransitFeedRealTime.Vehicle.VehiclePosition.mqtt message """
    print(f"Received GeneralTransitFeedRealTime.Vehicle.VehiclePosition.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_real_time_vehicle_vehicle_position_mqtt_data}")

async def handle_general_transit_feed_real_time_trip_trip_update_mqtt(mqtt_msg,cloud_event, general_transit_feed_real_time_trip_trip_update_mqtt_data):
    """ Handles the GeneralTransitFeedRealTime.Trip.TripUpdate.mqtt message """
    print(f"Received GeneralTransitFeedRealTime.Trip.TripUpdate.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_real_time_trip_trip_update_mqtt_data}")

async def handle_general_transit_feed_real_time_alert_alert_mqtt(mqtt_msg,cloud_event, general_transit_feed_real_time_alert_alert_mqtt_data):
    """ Handles the GeneralTransitFeedRealTime.Alert.Alert.mqtt message """
    print(f"Received GeneralTransitFeedRealTime.Alert.Alert.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_real_time_alert_alert_mqtt_data}")
from gtfs_mqtt_producer_mqtt_client.client import GeneralTransitFeedStaticMqttProducer, GeneralTransitFeedStaticMqttDispatcher

async def handle_general_transit_feed_static_agency_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_agency_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.Agency.mqtt message """
    print(f"Received GeneralTransitFeedStatic.Agency.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_agency_mqtt_data}")

async def handle_general_transit_feed_static_areas_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_areas_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.Areas.mqtt message """
    print(f"Received GeneralTransitFeedStatic.Areas.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_areas_mqtt_data}")

async def handle_general_transit_feed_static_attributions_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_attributions_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.Attributions.mqtt message """
    print(f"Received GeneralTransitFeedStatic.Attributions.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_attributions_mqtt_data}")

async def handle_general_transit_feed_booking_rules_mqtt(mqtt_msg,cloud_event, general_transit_feed_booking_rules_mqtt_data):
    """ Handles the GeneralTransitFeed.BookingRules.mqtt message """
    print(f"Received GeneralTransitFeed.BookingRules.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_booking_rules_mqtt_data}")

async def handle_general_transit_feed_static_fare_attributes_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_fare_attributes_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.FareAttributes.mqtt message """
    print(f"Received GeneralTransitFeedStatic.FareAttributes.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_fare_attributes_mqtt_data}")

async def handle_general_transit_feed_static_fare_leg_rules_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_fare_leg_rules_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.FareLegRules.mqtt message """
    print(f"Received GeneralTransitFeedStatic.FareLegRules.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_fare_leg_rules_mqtt_data}")

async def handle_general_transit_feed_static_fare_media_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_fare_media_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.FareMedia.mqtt message """
    print(f"Received GeneralTransitFeedStatic.FareMedia.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_fare_media_mqtt_data}")

async def handle_general_transit_feed_static_fare_products_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_fare_products_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.FareProducts.mqtt message """
    print(f"Received GeneralTransitFeedStatic.FareProducts.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_fare_products_mqtt_data}")

async def handle_general_transit_feed_static_fare_rules_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_fare_rules_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.FareRules.mqtt message """
    print(f"Received GeneralTransitFeedStatic.FareRules.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_fare_rules_mqtt_data}")

async def handle_general_transit_feed_static_fare_transfer_rules_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_fare_transfer_rules_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.FareTransferRules.mqtt message """
    print(f"Received GeneralTransitFeedStatic.FareTransferRules.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_fare_transfer_rules_mqtt_data}")

async def handle_general_transit_feed_static_feed_info_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_feed_info_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.FeedInfo.mqtt message """
    print(f"Received GeneralTransitFeedStatic.FeedInfo.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_feed_info_mqtt_data}")

async def handle_general_transit_feed_static_frequencies_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_frequencies_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.Frequencies.mqtt message """
    print(f"Received GeneralTransitFeedStatic.Frequencies.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_frequencies_mqtt_data}")

async def handle_general_transit_feed_static_levels_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_levels_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.Levels.mqtt message """
    print(f"Received GeneralTransitFeedStatic.Levels.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_levels_mqtt_data}")

async def handle_general_transit_feed_static_location_geo_json_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_location_geo_json_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.LocationGeoJson.mqtt message """
    print(f"Received GeneralTransitFeedStatic.LocationGeoJson.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_location_geo_json_mqtt_data}")

async def handle_general_transit_feed_static_location_groups_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_location_groups_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.LocationGroups.mqtt message """
    print(f"Received GeneralTransitFeedStatic.LocationGroups.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_location_groups_mqtt_data}")

async def handle_general_transit_feed_static_location_group_stores_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_location_group_stores_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.LocationGroupStores.mqtt message """
    print(f"Received GeneralTransitFeedStatic.LocationGroupStores.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_location_group_stores_mqtt_data}")

async def handle_general_transit_feed_static_networks_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_networks_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.Networks.mqtt message """
    print(f"Received GeneralTransitFeedStatic.Networks.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_networks_mqtt_data}")

async def handle_general_transit_feed_static_pathways_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_pathways_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.Pathways.mqtt message """
    print(f"Received GeneralTransitFeedStatic.Pathways.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_pathways_mqtt_data}")

async def handle_general_transit_feed_static_route_networks_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_route_networks_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.RouteNetworks.mqtt message """
    print(f"Received GeneralTransitFeedStatic.RouteNetworks.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_route_networks_mqtt_data}")

async def handle_general_transit_feed_static_routes_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_routes_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.Routes.mqtt message """
    print(f"Received GeneralTransitFeedStatic.Routes.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_routes_mqtt_data}")

async def handle_general_transit_feed_static_shapes_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_shapes_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.Shapes.mqtt message """
    print(f"Received GeneralTransitFeedStatic.Shapes.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_shapes_mqtt_data}")

async def handle_general_transit_feed_static_stop_areas_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_stop_areas_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.StopAreas.mqtt message """
    print(f"Received GeneralTransitFeedStatic.StopAreas.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_stop_areas_mqtt_data}")

async def handle_general_transit_feed_static_stops_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_stops_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.Stops.mqtt message """
    print(f"Received GeneralTransitFeedStatic.Stops.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_stops_mqtt_data}")

async def handle_general_transit_feed_static_stop_times_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_stop_times_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.StopTimes.mqtt message """
    print(f"Received GeneralTransitFeedStatic.StopTimes.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_stop_times_mqtt_data}")

async def handle_general_transit_feed_static_timeframes_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_timeframes_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.Timeframes.mqtt message """
    print(f"Received GeneralTransitFeedStatic.Timeframes.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_timeframes_mqtt_data}")

async def handle_general_transit_feed_static_transfers_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_transfers_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.Transfers.mqtt message """
    print(f"Received GeneralTransitFeedStatic.Transfers.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_transfers_mqtt_data}")

async def handle_general_transit_feed_static_translations_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_translations_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.Translations.mqtt message """
    print(f"Received GeneralTransitFeedStatic.Translations.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_translations_mqtt_data}")

async def handle_general_transit_feed_static_trips_mqtt(mqtt_msg,cloud_event, general_transit_feed_static_trips_mqtt_data):
    """ Handles the GeneralTransitFeedStatic.Trips.mqtt message """
    print(f"Received GeneralTransitFeedStatic.Trips.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {general_transit_feed_static_trips_mqtt_data}")

async def main(broker_host, broker_port, topic, username=None, password=None):
    """ Main function for MQTT client """
    print(f"Connecting to {broker_host}:{broker_port}...")
    print(f"Topic: {topic}")
    print("Press Ctrl+C to stop\n")
    
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGTERM, lambda: stop_event.set())
    loop.add_signal_handler(signal.SIGINT, lambda: stop_event.set())
    
    await stop_event.wait()
    print("\nStopping...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MQTT Client")
    parser.add_argument('--broker-host', default=os.getenv('MQTT_BROKER_HOST', 'localhost'), help='MQTT broker hostname')
    parser.add_argument('--broker-port', type=int, default=int(os.getenv('MQTT_BROKER_PORT', '1883')), help='MQTT broker port')
    parser.add_argument('--topic', default=os.getenv('MQTT_TOPIC', 'testtopic'), help='MQTT topic')
    parser.add_argument('--username', default=os.getenv('MQTT_USERNAME'), help='MQTT username (optional)')
    parser.add_argument('--password', default=os.getenv('MQTT_PASSWORD'), help='MQTT password (optional)')

    args = parser.parse_args()

    asyncio.run(main(
        args.broker_host,
        args.broker_port,
        args.topic,
        args.username,
        args.password
    ))