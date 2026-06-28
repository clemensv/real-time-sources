
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
from aisstream_mqtt_producer_data import *
from aisstream_mqtt_producer_mqtt_client.client import IOAISstreamMqttProducer, IOAISstreamMqttDispatcher

async def handle_io_aisstream_mqtt_position_report(mqtt_msg,cloud_event, io_aisstream_mqtt_position_report_data):
    """ Handles the IO.AISstream.mqtt.PositionReport message """
    print(f"Received IO.AISstream.mqtt.PositionReport on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_position_report_data}")

async def handle_io_aisstream_mqtt_ship_static_data(mqtt_msg,cloud_event, io_aisstream_mqtt_ship_static_data_data):
    """ Handles the IO.AISstream.mqtt.ShipStaticData message """
    print(f"Received IO.AISstream.mqtt.ShipStaticData on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_ship_static_data_data}")

async def handle_io_aisstream_mqtt_standard_class_bposition_report(mqtt_msg,cloud_event, io_aisstream_mqtt_standard_class_bposition_report_data):
    """ Handles the IO.AISstream.mqtt.StandardClassBPositionReport message """
    print(f"Received IO.AISstream.mqtt.StandardClassBPositionReport on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_standard_class_bposition_report_data}")

async def handle_io_aisstream_mqtt_extended_class_bposition_report(mqtt_msg,cloud_event, io_aisstream_mqtt_extended_class_bposition_report_data):
    """ Handles the IO.AISstream.mqtt.ExtendedClassBPositionReport message """
    print(f"Received IO.AISstream.mqtt.ExtendedClassBPositionReport on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_extended_class_bposition_report_data}")

async def handle_io_aisstream_mqtt_aids_to_navigation_report(mqtt_msg,cloud_event, io_aisstream_mqtt_aids_to_navigation_report_data):
    """ Handles the IO.AISstream.mqtt.AidsToNavigationReport message """
    print(f"Received IO.AISstream.mqtt.AidsToNavigationReport on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_aids_to_navigation_report_data}")

async def handle_io_aisstream_mqtt_static_data_report(mqtt_msg,cloud_event, io_aisstream_mqtt_static_data_report_data):
    """ Handles the IO.AISstream.mqtt.StaticDataReport message """
    print(f"Received IO.AISstream.mqtt.StaticDataReport on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_static_data_report_data}")

async def handle_io_aisstream_mqtt_base_station_report(mqtt_msg,cloud_event, io_aisstream_mqtt_base_station_report_data):
    """ Handles the IO.AISstream.mqtt.BaseStationReport message """
    print(f"Received IO.AISstream.mqtt.BaseStationReport on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_base_station_report_data}")

async def handle_io_aisstream_mqtt_safety_broadcast_message(mqtt_msg,cloud_event, io_aisstream_mqtt_safety_broadcast_message_data):
    """ Handles the IO.AISstream.mqtt.SafetyBroadcastMessage message """
    print(f"Received IO.AISstream.mqtt.SafetyBroadcastMessage on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_safety_broadcast_message_data}")

async def handle_io_aisstream_mqtt_standard_search_and_rescue_aircraft_report(mqtt_msg,cloud_event, io_aisstream_mqtt_standard_search_and_rescue_aircraft_report_data):
    """ Handles the IO.AISstream.mqtt.StandardSearchAndRescueAircraftReport message """
    print(f"Received IO.AISstream.mqtt.StandardSearchAndRescueAircraftReport on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_standard_search_and_rescue_aircraft_report_data}")

async def handle_io_aisstream_mqtt_long_range_ais_broadcast_message(mqtt_msg,cloud_event, io_aisstream_mqtt_long_range_ais_broadcast_message_data):
    """ Handles the IO.AISstream.mqtt.LongRangeAisBroadcastMessage message """
    print(f"Received IO.AISstream.mqtt.LongRangeAisBroadcastMessage on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_long_range_ais_broadcast_message_data}")

async def handle_io_aisstream_mqtt_addressed_safety_message(mqtt_msg,cloud_event, io_aisstream_mqtt_addressed_safety_message_data):
    """ Handles the IO.AISstream.mqtt.AddressedSafetyMessage message """
    print(f"Received IO.AISstream.mqtt.AddressedSafetyMessage on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_addressed_safety_message_data}")

async def handle_io_aisstream_mqtt_addressed_binary_message(mqtt_msg,cloud_event, io_aisstream_mqtt_addressed_binary_message_data):
    """ Handles the IO.AISstream.mqtt.AddressedBinaryMessage message """
    print(f"Received IO.AISstream.mqtt.AddressedBinaryMessage on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_addressed_binary_message_data}")

async def handle_io_aisstream_mqtt_assigned_mode_command(mqtt_msg,cloud_event, io_aisstream_mqtt_assigned_mode_command_data):
    """ Handles the IO.AISstream.mqtt.AssignedModeCommand message """
    print(f"Received IO.AISstream.mqtt.AssignedModeCommand on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_assigned_mode_command_data}")

async def handle_io_aisstream_mqtt_binary_acknowledge(mqtt_msg,cloud_event, io_aisstream_mqtt_binary_acknowledge_data):
    """ Handles the IO.AISstream.mqtt.BinaryAcknowledge message """
    print(f"Received IO.AISstream.mqtt.BinaryAcknowledge on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_binary_acknowledge_data}")

async def handle_io_aisstream_mqtt_binary_broadcast_message(mqtt_msg,cloud_event, io_aisstream_mqtt_binary_broadcast_message_data):
    """ Handles the IO.AISstream.mqtt.BinaryBroadcastMessage message """
    print(f"Received IO.AISstream.mqtt.BinaryBroadcastMessage on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_binary_broadcast_message_data}")

async def handle_io_aisstream_mqtt_channel_management(mqtt_msg,cloud_event, io_aisstream_mqtt_channel_management_data):
    """ Handles the IO.AISstream.mqtt.ChannelManagement message """
    print(f"Received IO.AISstream.mqtt.ChannelManagement on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_channel_management_data}")

async def handle_io_aisstream_mqtt_coordinated_utcinquiry(mqtt_msg,cloud_event, io_aisstream_mqtt_coordinated_utcinquiry_data):
    """ Handles the IO.AISstream.mqtt.CoordinatedUTCInquiry message """
    print(f"Received IO.AISstream.mqtt.CoordinatedUTCInquiry on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_coordinated_utcinquiry_data}")

async def handle_io_aisstream_mqtt_data_link_management_message(mqtt_msg,cloud_event, io_aisstream_mqtt_data_link_management_message_data):
    """ Handles the IO.AISstream.mqtt.DataLinkManagementMessage message """
    print(f"Received IO.AISstream.mqtt.DataLinkManagementMessage on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_data_link_management_message_data}")

async def handle_io_aisstream_mqtt_gnss_broadcast_binary_message(mqtt_msg,cloud_event, io_aisstream_mqtt_gnss_broadcast_binary_message_data):
    """ Handles the IO.AISstream.mqtt.GnssBroadcastBinaryMessage message """
    print(f"Received IO.AISstream.mqtt.GnssBroadcastBinaryMessage on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_gnss_broadcast_binary_message_data}")

async def handle_io_aisstream_mqtt_group_assignment_command(mqtt_msg,cloud_event, io_aisstream_mqtt_group_assignment_command_data):
    """ Handles the IO.AISstream.mqtt.GroupAssignmentCommand message """
    print(f"Received IO.AISstream.mqtt.GroupAssignmentCommand on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_group_assignment_command_data}")

async def handle_io_aisstream_mqtt_interrogation(mqtt_msg,cloud_event, io_aisstream_mqtt_interrogation_data):
    """ Handles the IO.AISstream.mqtt.Interrogation message """
    print(f"Received IO.AISstream.mqtt.Interrogation on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_interrogation_data}")

async def handle_io_aisstream_mqtt_multi_slot_binary_message(mqtt_msg,cloud_event, io_aisstream_mqtt_multi_slot_binary_message_data):
    """ Handles the IO.AISstream.mqtt.MultiSlotBinaryMessage message """
    print(f"Received IO.AISstream.mqtt.MultiSlotBinaryMessage on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_multi_slot_binary_message_data}")

async def handle_io_aisstream_mqtt_single_slot_binary_message(mqtt_msg,cloud_event, io_aisstream_mqtt_single_slot_binary_message_data):
    """ Handles the IO.AISstream.mqtt.SingleSlotBinaryMessage message """
    print(f"Received IO.AISstream.mqtt.SingleSlotBinaryMessage on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_aisstream_mqtt_single_slot_binary_message_data}")

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