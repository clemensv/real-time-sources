
"""
This is sample code to use the MQTT client contained in this project.

The sample demonstrates both publishing and subscribing to MQTT messages with
the
producer and dispatcher functionality.

There is a handler for each defined message type. The handler is an async
function that takes the following parameters:
- mqtt_message: The paho.mqtt.client.MQTTMessage object (message context).
- cloud_event: The CloudEvent data (if using CloudEvents).
- message_data: The deserialized message data.The main function creates a client
that can both produce and consume messages.
It starts a dispatcher to handle incoming messages and then publishes sample
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
from autobahn_mqtt_producer_data import *
from autobahn_mqtt_producer_mqtt_client.client import DEAutobahnMqttProducer, DEAutobahnMqttDispatcher

async def handle_de_autobahn_roadwork_appeared_mqtt(mqtt_msg,cloud_event, de_autobahn_roadwork_appeared_mqtt_data):
    """ Handles the DE.Autobahn.RoadworkAppeared.mqtt message """
    print(f"Received DE.Autobahn.RoadworkAppeared.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_roadwork_appeared_mqtt_data}")

async def handle_de_autobahn_roadwork_updated_mqtt(mqtt_msg,cloud_event, de_autobahn_roadwork_updated_mqtt_data):
    """ Handles the DE.Autobahn.RoadworkUpdated.mqtt message """
    print(f"Received DE.Autobahn.RoadworkUpdated.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_roadwork_updated_mqtt_data}")

async def handle_de_autobahn_roadwork_resolved_mqtt(mqtt_msg,cloud_event, de_autobahn_roadwork_resolved_mqtt_data):
    """ Handles the DE.Autobahn.RoadworkResolved.mqtt message """
    print(f"Received DE.Autobahn.RoadworkResolved.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_roadwork_resolved_mqtt_data}")

async def handle_de_autobahn_short_term_roadwork_appeared_mqtt(mqtt_msg,cloud_event, de_autobahn_short_term_roadwork_appeared_mqtt_data):
    """ Handles the DE.Autobahn.ShortTermRoadworkAppeared.mqtt message """
    print(f"Received DE.Autobahn.ShortTermRoadworkAppeared.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_short_term_roadwork_appeared_mqtt_data}")

async def handle_de_autobahn_short_term_roadwork_updated_mqtt(mqtt_msg,cloud_event, de_autobahn_short_term_roadwork_updated_mqtt_data):
    """ Handles the DE.Autobahn.ShortTermRoadworkUpdated.mqtt message """
    print(f"Received DE.Autobahn.ShortTermRoadworkUpdated.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_short_term_roadwork_updated_mqtt_data}")

async def handle_de_autobahn_short_term_roadwork_resolved_mqtt(mqtt_msg,cloud_event, de_autobahn_short_term_roadwork_resolved_mqtt_data):
    """ Handles the DE.Autobahn.ShortTermRoadworkResolved.mqtt message """
    print(f"Received DE.Autobahn.ShortTermRoadworkResolved.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_short_term_roadwork_resolved_mqtt_data}")

async def handle_de_autobahn_closure_appeared_mqtt(mqtt_msg,cloud_event, de_autobahn_closure_appeared_mqtt_data):
    """ Handles the DE.Autobahn.ClosureAppeared.mqtt message """
    print(f"Received DE.Autobahn.ClosureAppeared.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_closure_appeared_mqtt_data}")

async def handle_de_autobahn_closure_updated_mqtt(mqtt_msg,cloud_event, de_autobahn_closure_updated_mqtt_data):
    """ Handles the DE.Autobahn.ClosureUpdated.mqtt message """
    print(f"Received DE.Autobahn.ClosureUpdated.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_closure_updated_mqtt_data}")

async def handle_de_autobahn_closure_resolved_mqtt(mqtt_msg,cloud_event, de_autobahn_closure_resolved_mqtt_data):
    """ Handles the DE.Autobahn.ClosureResolved.mqtt message """
    print(f"Received DE.Autobahn.ClosureResolved.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_closure_resolved_mqtt_data}")

async def handle_de_autobahn_entry_exit_closure_appeared_mqtt(mqtt_msg,cloud_event, de_autobahn_entry_exit_closure_appeared_mqtt_data):
    """ Handles the DE.Autobahn.EntryExitClosureAppeared.mqtt message """
    print(f"Received DE.Autobahn.EntryExitClosureAppeared.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_entry_exit_closure_appeared_mqtt_data}")

async def handle_de_autobahn_entry_exit_closure_updated_mqtt(mqtt_msg,cloud_event, de_autobahn_entry_exit_closure_updated_mqtt_data):
    """ Handles the DE.Autobahn.EntryExitClosureUpdated.mqtt message """
    print(f"Received DE.Autobahn.EntryExitClosureUpdated.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_entry_exit_closure_updated_mqtt_data}")

async def handle_de_autobahn_entry_exit_closure_resolved_mqtt(mqtt_msg,cloud_event, de_autobahn_entry_exit_closure_resolved_mqtt_data):
    """ Handles the DE.Autobahn.EntryExitClosureResolved.mqtt message """
    print(f"Received DE.Autobahn.EntryExitClosureResolved.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_entry_exit_closure_resolved_mqtt_data}")

async def handle_de_autobahn_warning_appeared_mqtt(mqtt_msg,cloud_event, de_autobahn_warning_appeared_mqtt_data):
    """ Handles the DE.Autobahn.WarningAppeared.mqtt message """
    print(f"Received DE.Autobahn.WarningAppeared.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_warning_appeared_mqtt_data}")

async def handle_de_autobahn_warning_updated_mqtt(mqtt_msg,cloud_event, de_autobahn_warning_updated_mqtt_data):
    """ Handles the DE.Autobahn.WarningUpdated.mqtt message """
    print(f"Received DE.Autobahn.WarningUpdated.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_warning_updated_mqtt_data}")

async def handle_de_autobahn_warning_resolved_mqtt(mqtt_msg,cloud_event, de_autobahn_warning_resolved_mqtt_data):
    """ Handles the DE.Autobahn.WarningResolved.mqtt message """
    print(f"Received DE.Autobahn.WarningResolved.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_warning_resolved_mqtt_data}")

async def handle_de_autobahn_weight_limit35_restriction_appeared_mqtt(mqtt_msg,cloud_event, de_autobahn_weight_limit35_restriction_appeared_mqtt_data):
    """ Handles the DE.Autobahn.WeightLimit35RestrictionAppeared.mqtt message """
    print(f"Received DE.Autobahn.WeightLimit35RestrictionAppeared.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_weight_limit35_restriction_appeared_mqtt_data}")

async def handle_de_autobahn_weight_limit35_restriction_updated_mqtt(mqtt_msg,cloud_event, de_autobahn_weight_limit35_restriction_updated_mqtt_data):
    """ Handles the DE.Autobahn.WeightLimit35RestrictionUpdated.mqtt message """
    print(f"Received DE.Autobahn.WeightLimit35RestrictionUpdated.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_weight_limit35_restriction_updated_mqtt_data}")

async def handle_de_autobahn_weight_limit35_restriction_resolved_mqtt(mqtt_msg,cloud_event, de_autobahn_weight_limit35_restriction_resolved_mqtt_data):
    """ Handles the DE.Autobahn.WeightLimit35RestrictionResolved.mqtt message """
    print(f"Received DE.Autobahn.WeightLimit35RestrictionResolved.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_weight_limit35_restriction_resolved_mqtt_data}")

async def handle_de_autobahn_webcam_appeared_mqtt(mqtt_msg,cloud_event, de_autobahn_webcam_appeared_mqtt_data):
    """ Handles the DE.Autobahn.WebcamAppeared.mqtt message """
    print(f"Received DE.Autobahn.WebcamAppeared.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_webcam_appeared_mqtt_data}")

async def handle_de_autobahn_webcam_updated_mqtt(mqtt_msg,cloud_event, de_autobahn_webcam_updated_mqtt_data):
    """ Handles the DE.Autobahn.WebcamUpdated.mqtt message """
    print(f"Received DE.Autobahn.WebcamUpdated.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_webcam_updated_mqtt_data}")

async def handle_de_autobahn_webcam_resolved_mqtt(mqtt_msg,cloud_event, de_autobahn_webcam_resolved_mqtt_data):
    """ Handles the DE.Autobahn.WebcamResolved.mqtt message """
    print(f"Received DE.Autobahn.WebcamResolved.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_webcam_resolved_mqtt_data}")

async def handle_de_autobahn_parking_lorry_appeared_mqtt(mqtt_msg,cloud_event, de_autobahn_parking_lorry_appeared_mqtt_data):
    """ Handles the DE.Autobahn.ParkingLorryAppeared.mqtt message """
    print(f"Received DE.Autobahn.ParkingLorryAppeared.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_parking_lorry_appeared_mqtt_data}")

async def handle_de_autobahn_parking_lorry_updated_mqtt(mqtt_msg,cloud_event, de_autobahn_parking_lorry_updated_mqtt_data):
    """ Handles the DE.Autobahn.ParkingLorryUpdated.mqtt message """
    print(f"Received DE.Autobahn.ParkingLorryUpdated.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_parking_lorry_updated_mqtt_data}")

async def handle_de_autobahn_parking_lorry_resolved_mqtt(mqtt_msg,cloud_event, de_autobahn_parking_lorry_resolved_mqtt_data):
    """ Handles the DE.Autobahn.ParkingLorryResolved.mqtt message """
    print(f"Received DE.Autobahn.ParkingLorryResolved.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_parking_lorry_resolved_mqtt_data}")

async def handle_de_autobahn_electric_charging_station_appeared_mqtt(mqtt_msg,cloud_event, de_autobahn_electric_charging_station_appeared_mqtt_data):
    """ Handles the DE.Autobahn.ElectricChargingStationAppeared.mqtt message """
    print(f"Received DE.Autobahn.ElectricChargingStationAppeared.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_electric_charging_station_appeared_mqtt_data}")

async def handle_de_autobahn_electric_charging_station_updated_mqtt(mqtt_msg,cloud_event, de_autobahn_electric_charging_station_updated_mqtt_data):
    """ Handles the DE.Autobahn.ElectricChargingStationUpdated.mqtt message """
    print(f"Received DE.Autobahn.ElectricChargingStationUpdated.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_electric_charging_station_updated_mqtt_data}")

async def handle_de_autobahn_electric_charging_station_resolved_mqtt(mqtt_msg,cloud_event, de_autobahn_electric_charging_station_resolved_mqtt_data):
    """ Handles the DE.Autobahn.ElectricChargingStationResolved.mqtt message """
    print(f"Received DE.Autobahn.ElectricChargingStationResolved.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_electric_charging_station_resolved_mqtt_data}")

async def handle_de_autobahn_strong_electric_charging_station_appeared_mqtt(mqtt_msg,cloud_event, de_autobahn_strong_electric_charging_station_appeared_mqtt_data):
    """ Handles the DE.Autobahn.StrongElectricChargingStationAppeared.mqtt message """
    print(f"Received DE.Autobahn.StrongElectricChargingStationAppeared.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_strong_electric_charging_station_appeared_mqtt_data}")

async def handle_de_autobahn_strong_electric_charging_station_updated_mqtt(mqtt_msg,cloud_event, de_autobahn_strong_electric_charging_station_updated_mqtt_data):
    """ Handles the DE.Autobahn.StrongElectricChargingStationUpdated.mqtt message """
    print(f"Received DE.Autobahn.StrongElectricChargingStationUpdated.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_strong_electric_charging_station_updated_mqtt_data}")

async def handle_de_autobahn_strong_electric_charging_station_resolved_mqtt(mqtt_msg,cloud_event, de_autobahn_strong_electric_charging_station_resolved_mqtt_data):
    """ Handles the DE.Autobahn.StrongElectricChargingStationResolved.mqtt message """
    print(f"Received DE.Autobahn.StrongElectricChargingStationResolved.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_autobahn_strong_electric_charging_station_resolved_mqtt_data}")

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