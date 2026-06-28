
"""
This is sample code to produce events to Apache Kafka with the producer clients
contained in this project. You will still need to supply event data in the
marked
placews below before the program can be run.

The script gets the configuration from the command line or uses the environment
variables. The following environment variables are recognized:

- KAFKA_PRODUCER_CONFIG: The Kafka producer configuration.
- KAFKA_TOPICS: The Kafka topics to send events to.
- FABRIC_CONNECTION_STRING: A Microsoft Fabric or Azure Event Hubs connection
string.

Alternatively, you can pass the configuration as command-line arguments.

- `--producer-config`: The Kafka producer configuration.
- `--topics`: The Kafka topics to send events to.
- `-c` or `--connection-string`: The Microsoft Fabric or Azure Event Hubs
connection string.
"""

import argparse
import os
import asyncio
import json
import uuid
from typing import Optional
from datetime import datetime
from confluent_kafka import Producer as KafkaProducer

# imports the producer clients for the message group(s)

from aisstream_producer_kafka_producer.producer import IOAISstreamEventProducer
from aisstream_producer_kafka_producer.producer import IOAISstreamMqttEventProducer
from aisstream_producer_kafka_producer.producer import IOAISstreamAmqpEventProducer

# imports for the data classes for each event

from aisstream_producer_data import PositionReport
from aisstream_producer_data import ShipStaticData
from aisstream_producer_data import StandardClassBPositionReport
from aisstream_producer_data import ExtendedClassBPositionReport
from aisstream_producer_data import AidsToNavigationReport
from aisstream_producer_data import StaticDataReport
from aisstream_producer_data import BaseStationReport
from aisstream_producer_data import SafetyBroadcastMessage
from aisstream_producer_data import StandardSearchAndRescueAircraftReport
from aisstream_producer_data import LongRangeAisBroadcastMessage
from aisstream_producer_data import AddressedSafetyMessage
from aisstream_producer_data import AddressedBinaryMessage
from aisstream_producer_data import AssignedModeCommand
from aisstream_producer_data import BinaryAcknowledge
from aisstream_producer_data import BinaryBroadcastMessage
from aisstream_producer_data import ChannelManagement
from aisstream_producer_data import CoordinatedUTCInquiry
from aisstream_producer_data import DataLinkManagementMessage
from aisstream_producer_data import GnssBroadcastBinaryMessage
from aisstream_producer_data import GroupAssignmentCommand
from aisstream_producer_data import Interrogation
from aisstream_producer_data import MultiSlotBinaryMessage
from aisstream_producer_data import SingleSlotBinaryMessage

async def main(connection_string: Optional[str], producer_config: Optional[str], topic: Optional[str]):
    """
    Main function to produce events to Apache Kafka

    Args:
        connection_string (Optional[str]): The Fabric connection string
        producer_config (Optional[str]): The Kafka producer configuration
        topic (Optional[str]): The Kafka topic to send events to
    """
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        ioaisstream_event_producer = IOAISstreamEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ioaisstream_event_producer = IOAISstreamEventProducer(kafka_producer, topic, 'binary')

    # ---- IO.AISstream.PositionReport ----
    # TODO: Supply event data for the IO.AISstream.PositionReport event
    _position_report = PositionReport()

    # sends the 'IO.AISstream.PositionReport' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_position_report(_user_id = 'TODO: replace me', data = _position_report)
    print(f"Sent 'IO.AISstream.PositionReport' event: {_position_report.to_json()}")

    # ---- IO.AISstream.ShipStaticData ----
    # TODO: Supply event data for the IO.AISstream.ShipStaticData event
    _ship_static_data = ShipStaticData()

    # sends the 'IO.AISstream.ShipStaticData' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_ship_static_data(_user_id = 'TODO: replace me', data = _ship_static_data)
    print(f"Sent 'IO.AISstream.ShipStaticData' event: {_ship_static_data.to_json()}")

    # ---- IO.AISstream.StandardClassBPositionReport ----
    # TODO: Supply event data for the IO.AISstream.StandardClassBPositionReport event
    _standard_class_bposition_report = StandardClassBPositionReport()

    # sends the 'IO.AISstream.StandardClassBPositionReport' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_standard_class_bposition_report(_user_id = 'TODO: replace me', data = _standard_class_bposition_report)
    print(f"Sent 'IO.AISstream.StandardClassBPositionReport' event: {_standard_class_bposition_report.to_json()}")

    # ---- IO.AISstream.ExtendedClassBPositionReport ----
    # TODO: Supply event data for the IO.AISstream.ExtendedClassBPositionReport event
    _extended_class_bposition_report = ExtendedClassBPositionReport()

    # sends the 'IO.AISstream.ExtendedClassBPositionReport' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_extended_class_bposition_report(_user_id = 'TODO: replace me', data = _extended_class_bposition_report)
    print(f"Sent 'IO.AISstream.ExtendedClassBPositionReport' event: {_extended_class_bposition_report.to_json()}")

    # ---- IO.AISstream.AidsToNavigationReport ----
    # TODO: Supply event data for the IO.AISstream.AidsToNavigationReport event
    _aids_to_navigation_report = AidsToNavigationReport()

    # sends the 'IO.AISstream.AidsToNavigationReport' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_aids_to_navigation_report(_user_id = 'TODO: replace me', data = _aids_to_navigation_report)
    print(f"Sent 'IO.AISstream.AidsToNavigationReport' event: {_aids_to_navigation_report.to_json()}")

    # ---- IO.AISstream.StaticDataReport ----
    # TODO: Supply event data for the IO.AISstream.StaticDataReport event
    _static_data_report = StaticDataReport()

    # sends the 'IO.AISstream.StaticDataReport' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_static_data_report(_user_id = 'TODO: replace me', data = _static_data_report)
    print(f"Sent 'IO.AISstream.StaticDataReport' event: {_static_data_report.to_json()}")

    # ---- IO.AISstream.BaseStationReport ----
    # TODO: Supply event data for the IO.AISstream.BaseStationReport event
    _base_station_report = BaseStationReport()

    # sends the 'IO.AISstream.BaseStationReport' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_base_station_report(_user_id = 'TODO: replace me', data = _base_station_report)
    print(f"Sent 'IO.AISstream.BaseStationReport' event: {_base_station_report.to_json()}")

    # ---- IO.AISstream.SafetyBroadcastMessage ----
    # TODO: Supply event data for the IO.AISstream.SafetyBroadcastMessage event
    _safety_broadcast_message = SafetyBroadcastMessage()

    # sends the 'IO.AISstream.SafetyBroadcastMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_safety_broadcast_message(_user_id = 'TODO: replace me', data = _safety_broadcast_message)
    print(f"Sent 'IO.AISstream.SafetyBroadcastMessage' event: {_safety_broadcast_message.to_json()}")

    # ---- IO.AISstream.StandardSearchAndRescueAircraftReport ----
    # TODO: Supply event data for the IO.AISstream.StandardSearchAndRescueAircraftReport event
    _standard_search_and_rescue_aircraft_report = StandardSearchAndRescueAircraftReport()

    # sends the 'IO.AISstream.StandardSearchAndRescueAircraftReport' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_standard_search_and_rescue_aircraft_report(_user_id = 'TODO: replace me', data = _standard_search_and_rescue_aircraft_report)
    print(f"Sent 'IO.AISstream.StandardSearchAndRescueAircraftReport' event: {_standard_search_and_rescue_aircraft_report.to_json()}")

    # ---- IO.AISstream.LongRangeAisBroadcastMessage ----
    # TODO: Supply event data for the IO.AISstream.LongRangeAisBroadcastMessage event
    _long_range_ais_broadcast_message = LongRangeAisBroadcastMessage()

    # sends the 'IO.AISstream.LongRangeAisBroadcastMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_long_range_ais_broadcast_message(_user_id = 'TODO: replace me', data = _long_range_ais_broadcast_message)
    print(f"Sent 'IO.AISstream.LongRangeAisBroadcastMessage' event: {_long_range_ais_broadcast_message.to_json()}")

    # ---- IO.AISstream.AddressedSafetyMessage ----
    # TODO: Supply event data for the IO.AISstream.AddressedSafetyMessage event
    _addressed_safety_message = AddressedSafetyMessage()

    # sends the 'IO.AISstream.AddressedSafetyMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_addressed_safety_message(_user_id = 'TODO: replace me', data = _addressed_safety_message)
    print(f"Sent 'IO.AISstream.AddressedSafetyMessage' event: {_addressed_safety_message.to_json()}")

    # ---- IO.AISstream.AddressedBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.AddressedBinaryMessage event
    _addressed_binary_message = AddressedBinaryMessage()

    # sends the 'IO.AISstream.AddressedBinaryMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_addressed_binary_message(_user_id = 'TODO: replace me', data = _addressed_binary_message)
    print(f"Sent 'IO.AISstream.AddressedBinaryMessage' event: {_addressed_binary_message.to_json()}")

    # ---- IO.AISstream.AssignedModeCommand ----
    # TODO: Supply event data for the IO.AISstream.AssignedModeCommand event
    _assigned_mode_command = AssignedModeCommand()

    # sends the 'IO.AISstream.AssignedModeCommand' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_assigned_mode_command(_user_id = 'TODO: replace me', data = _assigned_mode_command)
    print(f"Sent 'IO.AISstream.AssignedModeCommand' event: {_assigned_mode_command.to_json()}")

    # ---- IO.AISstream.BinaryAcknowledge ----
    # TODO: Supply event data for the IO.AISstream.BinaryAcknowledge event
    _binary_acknowledge = BinaryAcknowledge()

    # sends the 'IO.AISstream.BinaryAcknowledge' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_binary_acknowledge(_user_id = 'TODO: replace me', data = _binary_acknowledge)
    print(f"Sent 'IO.AISstream.BinaryAcknowledge' event: {_binary_acknowledge.to_json()}")

    # ---- IO.AISstream.BinaryBroadcastMessage ----
    # TODO: Supply event data for the IO.AISstream.BinaryBroadcastMessage event
    _binary_broadcast_message = BinaryBroadcastMessage()

    # sends the 'IO.AISstream.BinaryBroadcastMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_binary_broadcast_message(_user_id = 'TODO: replace me', data = _binary_broadcast_message)
    print(f"Sent 'IO.AISstream.BinaryBroadcastMessage' event: {_binary_broadcast_message.to_json()}")

    # ---- IO.AISstream.ChannelManagement ----
    # TODO: Supply event data for the IO.AISstream.ChannelManagement event
    _channel_management = ChannelManagement()

    # sends the 'IO.AISstream.ChannelManagement' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_channel_management(_user_id = 'TODO: replace me', data = _channel_management)
    print(f"Sent 'IO.AISstream.ChannelManagement' event: {_channel_management.to_json()}")

    # ---- IO.AISstream.CoordinatedUTCInquiry ----
    # TODO: Supply event data for the IO.AISstream.CoordinatedUTCInquiry event
    _coordinated_utcinquiry = CoordinatedUTCInquiry()

    # sends the 'IO.AISstream.CoordinatedUTCInquiry' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_coordinated_utcinquiry(_user_id = 'TODO: replace me', data = _coordinated_utcinquiry)
    print(f"Sent 'IO.AISstream.CoordinatedUTCInquiry' event: {_coordinated_utcinquiry.to_json()}")

    # ---- IO.AISstream.DataLinkManagementMessage ----
    # TODO: Supply event data for the IO.AISstream.DataLinkManagementMessage event
    _data_link_management_message = DataLinkManagementMessage()

    # sends the 'IO.AISstream.DataLinkManagementMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_data_link_management_message(_user_id = 'TODO: replace me', data = _data_link_management_message)
    print(f"Sent 'IO.AISstream.DataLinkManagementMessage' event: {_data_link_management_message.to_json()}")

    # ---- IO.AISstream.GnssBroadcastBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.GnssBroadcastBinaryMessage event
    _gnss_broadcast_binary_message = GnssBroadcastBinaryMessage()

    # sends the 'IO.AISstream.GnssBroadcastBinaryMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_gnss_broadcast_binary_message(_user_id = 'TODO: replace me', data = _gnss_broadcast_binary_message)
    print(f"Sent 'IO.AISstream.GnssBroadcastBinaryMessage' event: {_gnss_broadcast_binary_message.to_json()}")

    # ---- IO.AISstream.GroupAssignmentCommand ----
    # TODO: Supply event data for the IO.AISstream.GroupAssignmentCommand event
    _group_assignment_command = GroupAssignmentCommand()

    # sends the 'IO.AISstream.GroupAssignmentCommand' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_group_assignment_command(_user_id = 'TODO: replace me', data = _group_assignment_command)
    print(f"Sent 'IO.AISstream.GroupAssignmentCommand' event: {_group_assignment_command.to_json()}")

    # ---- IO.AISstream.Interrogation ----
    # TODO: Supply event data for the IO.AISstream.Interrogation event
    _interrogation = Interrogation()

    # sends the 'IO.AISstream.Interrogation' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_interrogation(_user_id = 'TODO: replace me', data = _interrogation)
    print(f"Sent 'IO.AISstream.Interrogation' event: {_interrogation.to_json()}")

    # ---- IO.AISstream.MultiSlotBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.MultiSlotBinaryMessage event
    _multi_slot_binary_message = MultiSlotBinaryMessage()

    # sends the 'IO.AISstream.MultiSlotBinaryMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_multi_slot_binary_message(_user_id = 'TODO: replace me', data = _multi_slot_binary_message)
    print(f"Sent 'IO.AISstream.MultiSlotBinaryMessage' event: {_multi_slot_binary_message.to_json()}")

    # ---- IO.AISstream.SingleSlotBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.SingleSlotBinaryMessage event
    _single_slot_binary_message = SingleSlotBinaryMessage()

    # sends the 'IO.AISstream.SingleSlotBinaryMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_single_slot_binary_message(_user_id = 'TODO: replace me', data = _single_slot_binary_message)
    print(f"Sent 'IO.AISstream.SingleSlotBinaryMessage' event: {_single_slot_binary_message.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        ioaisstream_mqtt_event_producer = IOAISstreamMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ioaisstream_mqtt_event_producer = IOAISstreamMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- IO.AISstream.mqtt.PositionReport ----
    # TODO: Supply event data for the IO.AISstream.mqtt.PositionReport event
    _position_report = PositionReport()

    # sends the 'IO.AISstream.mqtt.PositionReport' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_position_report(_mmsi = 'TODO: replace me', data = _position_report)
    print(f"Sent 'IO.AISstream.mqtt.PositionReport' event: {_position_report.to_json()}")

    # ---- IO.AISstream.mqtt.ShipStaticData ----
    # TODO: Supply event data for the IO.AISstream.mqtt.ShipStaticData event
    _ship_static_data = ShipStaticData()

    # sends the 'IO.AISstream.mqtt.ShipStaticData' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_ship_static_data(_mmsi = 'TODO: replace me', data = _ship_static_data)
    print(f"Sent 'IO.AISstream.mqtt.ShipStaticData' event: {_ship_static_data.to_json()}")

    # ---- IO.AISstream.mqtt.StandardClassBPositionReport ----
    # TODO: Supply event data for the IO.AISstream.mqtt.StandardClassBPositionReport event
    _standard_class_bposition_report = StandardClassBPositionReport()

    # sends the 'IO.AISstream.mqtt.StandardClassBPositionReport' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_standard_class_bposition_report(_mmsi = 'TODO: replace me', data = _standard_class_bposition_report)
    print(f"Sent 'IO.AISstream.mqtt.StandardClassBPositionReport' event: {_standard_class_bposition_report.to_json()}")

    # ---- IO.AISstream.mqtt.ExtendedClassBPositionReport ----
    # TODO: Supply event data for the IO.AISstream.mqtt.ExtendedClassBPositionReport event
    _extended_class_bposition_report = ExtendedClassBPositionReport()

    # sends the 'IO.AISstream.mqtt.ExtendedClassBPositionReport' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_extended_class_bposition_report(_mmsi = 'TODO: replace me', data = _extended_class_bposition_report)
    print(f"Sent 'IO.AISstream.mqtt.ExtendedClassBPositionReport' event: {_extended_class_bposition_report.to_json()}")

    # ---- IO.AISstream.mqtt.AidsToNavigationReport ----
    # TODO: Supply event data for the IO.AISstream.mqtt.AidsToNavigationReport event
    _aids_to_navigation_report = AidsToNavigationReport()

    # sends the 'IO.AISstream.mqtt.AidsToNavigationReport' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_aids_to_navigation_report(_mmsi = 'TODO: replace me', data = _aids_to_navigation_report)
    print(f"Sent 'IO.AISstream.mqtt.AidsToNavigationReport' event: {_aids_to_navigation_report.to_json()}")

    # ---- IO.AISstream.mqtt.StaticDataReport ----
    # TODO: Supply event data for the IO.AISstream.mqtt.StaticDataReport event
    _static_data_report = StaticDataReport()

    # sends the 'IO.AISstream.mqtt.StaticDataReport' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_static_data_report(_mmsi = 'TODO: replace me', data = _static_data_report)
    print(f"Sent 'IO.AISstream.mqtt.StaticDataReport' event: {_static_data_report.to_json()}")

    # ---- IO.AISstream.mqtt.BaseStationReport ----
    # TODO: Supply event data for the IO.AISstream.mqtt.BaseStationReport event
    _base_station_report = BaseStationReport()

    # sends the 'IO.AISstream.mqtt.BaseStationReport' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_base_station_report(_mmsi = 'TODO: replace me', data = _base_station_report)
    print(f"Sent 'IO.AISstream.mqtt.BaseStationReport' event: {_base_station_report.to_json()}")

    # ---- IO.AISstream.mqtt.SafetyBroadcastMessage ----
    # TODO: Supply event data for the IO.AISstream.mqtt.SafetyBroadcastMessage event
    _safety_broadcast_message = SafetyBroadcastMessage()

    # sends the 'IO.AISstream.mqtt.SafetyBroadcastMessage' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_safety_broadcast_message(_mmsi = 'TODO: replace me', data = _safety_broadcast_message)
    print(f"Sent 'IO.AISstream.mqtt.SafetyBroadcastMessage' event: {_safety_broadcast_message.to_json()}")

    # ---- IO.AISstream.mqtt.StandardSearchAndRescueAircraftReport ----
    # TODO: Supply event data for the IO.AISstream.mqtt.StandardSearchAndRescueAircraftReport event
    _standard_search_and_rescue_aircraft_report = StandardSearchAndRescueAircraftReport()

    # sends the 'IO.AISstream.mqtt.StandardSearchAndRescueAircraftReport' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_standard_search_and_rescue_aircraft_report(_mmsi = 'TODO: replace me', data = _standard_search_and_rescue_aircraft_report)
    print(f"Sent 'IO.AISstream.mqtt.StandardSearchAndRescueAircraftReport' event: {_standard_search_and_rescue_aircraft_report.to_json()}")

    # ---- IO.AISstream.mqtt.LongRangeAisBroadcastMessage ----
    # TODO: Supply event data for the IO.AISstream.mqtt.LongRangeAisBroadcastMessage event
    _long_range_ais_broadcast_message = LongRangeAisBroadcastMessage()

    # sends the 'IO.AISstream.mqtt.LongRangeAisBroadcastMessage' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_long_range_ais_broadcast_message(_mmsi = 'TODO: replace me', data = _long_range_ais_broadcast_message)
    print(f"Sent 'IO.AISstream.mqtt.LongRangeAisBroadcastMessage' event: {_long_range_ais_broadcast_message.to_json()}")

    # ---- IO.AISstream.mqtt.AddressedSafetyMessage ----
    # TODO: Supply event data for the IO.AISstream.mqtt.AddressedSafetyMessage event
    _addressed_safety_message = AddressedSafetyMessage()

    # sends the 'IO.AISstream.mqtt.AddressedSafetyMessage' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_addressed_safety_message(_mmsi = 'TODO: replace me', data = _addressed_safety_message)
    print(f"Sent 'IO.AISstream.mqtt.AddressedSafetyMessage' event: {_addressed_safety_message.to_json()}")

    # ---- IO.AISstream.mqtt.AddressedBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.mqtt.AddressedBinaryMessage event
    _addressed_binary_message = AddressedBinaryMessage()

    # sends the 'IO.AISstream.mqtt.AddressedBinaryMessage' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_addressed_binary_message(_mmsi = 'TODO: replace me', data = _addressed_binary_message)
    print(f"Sent 'IO.AISstream.mqtt.AddressedBinaryMessage' event: {_addressed_binary_message.to_json()}")

    # ---- IO.AISstream.mqtt.AssignedModeCommand ----
    # TODO: Supply event data for the IO.AISstream.mqtt.AssignedModeCommand event
    _assigned_mode_command = AssignedModeCommand()

    # sends the 'IO.AISstream.mqtt.AssignedModeCommand' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_assigned_mode_command(_mmsi = 'TODO: replace me', data = _assigned_mode_command)
    print(f"Sent 'IO.AISstream.mqtt.AssignedModeCommand' event: {_assigned_mode_command.to_json()}")

    # ---- IO.AISstream.mqtt.BinaryAcknowledge ----
    # TODO: Supply event data for the IO.AISstream.mqtt.BinaryAcknowledge event
    _binary_acknowledge = BinaryAcknowledge()

    # sends the 'IO.AISstream.mqtt.BinaryAcknowledge' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_binary_acknowledge(_mmsi = 'TODO: replace me', data = _binary_acknowledge)
    print(f"Sent 'IO.AISstream.mqtt.BinaryAcknowledge' event: {_binary_acknowledge.to_json()}")

    # ---- IO.AISstream.mqtt.BinaryBroadcastMessage ----
    # TODO: Supply event data for the IO.AISstream.mqtt.BinaryBroadcastMessage event
    _binary_broadcast_message = BinaryBroadcastMessage()

    # sends the 'IO.AISstream.mqtt.BinaryBroadcastMessage' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_binary_broadcast_message(_mmsi = 'TODO: replace me', data = _binary_broadcast_message)
    print(f"Sent 'IO.AISstream.mqtt.BinaryBroadcastMessage' event: {_binary_broadcast_message.to_json()}")

    # ---- IO.AISstream.mqtt.ChannelManagement ----
    # TODO: Supply event data for the IO.AISstream.mqtt.ChannelManagement event
    _channel_management = ChannelManagement()

    # sends the 'IO.AISstream.mqtt.ChannelManagement' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_channel_management(_mmsi = 'TODO: replace me', data = _channel_management)
    print(f"Sent 'IO.AISstream.mqtt.ChannelManagement' event: {_channel_management.to_json()}")

    # ---- IO.AISstream.mqtt.CoordinatedUTCInquiry ----
    # TODO: Supply event data for the IO.AISstream.mqtt.CoordinatedUTCInquiry event
    _coordinated_utcinquiry = CoordinatedUTCInquiry()

    # sends the 'IO.AISstream.mqtt.CoordinatedUTCInquiry' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_coordinated_utcinquiry(_mmsi = 'TODO: replace me', data = _coordinated_utcinquiry)
    print(f"Sent 'IO.AISstream.mqtt.CoordinatedUTCInquiry' event: {_coordinated_utcinquiry.to_json()}")

    # ---- IO.AISstream.mqtt.DataLinkManagementMessage ----
    # TODO: Supply event data for the IO.AISstream.mqtt.DataLinkManagementMessage event
    _data_link_management_message = DataLinkManagementMessage()

    # sends the 'IO.AISstream.mqtt.DataLinkManagementMessage' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_data_link_management_message(_mmsi = 'TODO: replace me', data = _data_link_management_message)
    print(f"Sent 'IO.AISstream.mqtt.DataLinkManagementMessage' event: {_data_link_management_message.to_json()}")

    # ---- IO.AISstream.mqtt.GnssBroadcastBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.mqtt.GnssBroadcastBinaryMessage event
    _gnss_broadcast_binary_message = GnssBroadcastBinaryMessage()

    # sends the 'IO.AISstream.mqtt.GnssBroadcastBinaryMessage' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_gnss_broadcast_binary_message(_mmsi = 'TODO: replace me', data = _gnss_broadcast_binary_message)
    print(f"Sent 'IO.AISstream.mqtt.GnssBroadcastBinaryMessage' event: {_gnss_broadcast_binary_message.to_json()}")

    # ---- IO.AISstream.mqtt.GroupAssignmentCommand ----
    # TODO: Supply event data for the IO.AISstream.mqtt.GroupAssignmentCommand event
    _group_assignment_command = GroupAssignmentCommand()

    # sends the 'IO.AISstream.mqtt.GroupAssignmentCommand' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_group_assignment_command(_mmsi = 'TODO: replace me', data = _group_assignment_command)
    print(f"Sent 'IO.AISstream.mqtt.GroupAssignmentCommand' event: {_group_assignment_command.to_json()}")

    # ---- IO.AISstream.mqtt.Interrogation ----
    # TODO: Supply event data for the IO.AISstream.mqtt.Interrogation event
    _interrogation = Interrogation()

    # sends the 'IO.AISstream.mqtt.Interrogation' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_interrogation(_mmsi = 'TODO: replace me', data = _interrogation)
    print(f"Sent 'IO.AISstream.mqtt.Interrogation' event: {_interrogation.to_json()}")

    # ---- IO.AISstream.mqtt.MultiSlotBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.mqtt.MultiSlotBinaryMessage event
    _multi_slot_binary_message = MultiSlotBinaryMessage()

    # sends the 'IO.AISstream.mqtt.MultiSlotBinaryMessage' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_multi_slot_binary_message(_mmsi = 'TODO: replace me', data = _multi_slot_binary_message)
    print(f"Sent 'IO.AISstream.mqtt.MultiSlotBinaryMessage' event: {_multi_slot_binary_message.to_json()}")

    # ---- IO.AISstream.mqtt.SingleSlotBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.mqtt.SingleSlotBinaryMessage event
    _single_slot_binary_message = SingleSlotBinaryMessage()

    # sends the 'IO.AISstream.mqtt.SingleSlotBinaryMessage' event to Kafka topic.
    await ioaisstream_mqtt_event_producer.send_io_aisstream_mqtt_single_slot_binary_message(_mmsi = 'TODO: replace me', data = _single_slot_binary_message)
    print(f"Sent 'IO.AISstream.mqtt.SingleSlotBinaryMessage' event: {_single_slot_binary_message.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        ioaisstream_amqp_event_producer = IOAISstreamAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ioaisstream_amqp_event_producer = IOAISstreamAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- IO.AISstream.amqp.PositionReport ----
    # TODO: Supply event data for the IO.AISstream.amqp.PositionReport event
    _position_report = PositionReport()

    # sends the 'IO.AISstream.amqp.PositionReport' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_position_report(_user_id = 'TODO: replace me', data = _position_report)
    print(f"Sent 'IO.AISstream.amqp.PositionReport' event: {_position_report.to_json()}")

    # ---- IO.AISstream.amqp.ShipStaticData ----
    # TODO: Supply event data for the IO.AISstream.amqp.ShipStaticData event
    _ship_static_data = ShipStaticData()

    # sends the 'IO.AISstream.amqp.ShipStaticData' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_ship_static_data(_user_id = 'TODO: replace me', data = _ship_static_data)
    print(f"Sent 'IO.AISstream.amqp.ShipStaticData' event: {_ship_static_data.to_json()}")

    # ---- IO.AISstream.amqp.StandardClassBPositionReport ----
    # TODO: Supply event data for the IO.AISstream.amqp.StandardClassBPositionReport event
    _standard_class_bposition_report = StandardClassBPositionReport()

    # sends the 'IO.AISstream.amqp.StandardClassBPositionReport' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_standard_class_bposition_report(_user_id = 'TODO: replace me', data = _standard_class_bposition_report)
    print(f"Sent 'IO.AISstream.amqp.StandardClassBPositionReport' event: {_standard_class_bposition_report.to_json()}")

    # ---- IO.AISstream.amqp.ExtendedClassBPositionReport ----
    # TODO: Supply event data for the IO.AISstream.amqp.ExtendedClassBPositionReport event
    _extended_class_bposition_report = ExtendedClassBPositionReport()

    # sends the 'IO.AISstream.amqp.ExtendedClassBPositionReport' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_extended_class_bposition_report(_user_id = 'TODO: replace me', data = _extended_class_bposition_report)
    print(f"Sent 'IO.AISstream.amqp.ExtendedClassBPositionReport' event: {_extended_class_bposition_report.to_json()}")

    # ---- IO.AISstream.amqp.AidsToNavigationReport ----
    # TODO: Supply event data for the IO.AISstream.amqp.AidsToNavigationReport event
    _aids_to_navigation_report = AidsToNavigationReport()

    # sends the 'IO.AISstream.amqp.AidsToNavigationReport' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_aids_to_navigation_report(_user_id = 'TODO: replace me', data = _aids_to_navigation_report)
    print(f"Sent 'IO.AISstream.amqp.AidsToNavigationReport' event: {_aids_to_navigation_report.to_json()}")

    # ---- IO.AISstream.amqp.StaticDataReport ----
    # TODO: Supply event data for the IO.AISstream.amqp.StaticDataReport event
    _static_data_report = StaticDataReport()

    # sends the 'IO.AISstream.amqp.StaticDataReport' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_static_data_report(_user_id = 'TODO: replace me', data = _static_data_report)
    print(f"Sent 'IO.AISstream.amqp.StaticDataReport' event: {_static_data_report.to_json()}")

    # ---- IO.AISstream.amqp.BaseStationReport ----
    # TODO: Supply event data for the IO.AISstream.amqp.BaseStationReport event
    _base_station_report = BaseStationReport()

    # sends the 'IO.AISstream.amqp.BaseStationReport' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_base_station_report(_user_id = 'TODO: replace me', data = _base_station_report)
    print(f"Sent 'IO.AISstream.amqp.BaseStationReport' event: {_base_station_report.to_json()}")

    # ---- IO.AISstream.amqp.SafetyBroadcastMessage ----
    # TODO: Supply event data for the IO.AISstream.amqp.SafetyBroadcastMessage event
    _safety_broadcast_message = SafetyBroadcastMessage()

    # sends the 'IO.AISstream.amqp.SafetyBroadcastMessage' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_safety_broadcast_message(_user_id = 'TODO: replace me', data = _safety_broadcast_message)
    print(f"Sent 'IO.AISstream.amqp.SafetyBroadcastMessage' event: {_safety_broadcast_message.to_json()}")

    # ---- IO.AISstream.amqp.StandardSearchAndRescueAircraftReport ----
    # TODO: Supply event data for the IO.AISstream.amqp.StandardSearchAndRescueAircraftReport event
    _standard_search_and_rescue_aircraft_report = StandardSearchAndRescueAircraftReport()

    # sends the 'IO.AISstream.amqp.StandardSearchAndRescueAircraftReport' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_standard_search_and_rescue_aircraft_report(_user_id = 'TODO: replace me', data = _standard_search_and_rescue_aircraft_report)
    print(f"Sent 'IO.AISstream.amqp.StandardSearchAndRescueAircraftReport' event: {_standard_search_and_rescue_aircraft_report.to_json()}")

    # ---- IO.AISstream.amqp.LongRangeAisBroadcastMessage ----
    # TODO: Supply event data for the IO.AISstream.amqp.LongRangeAisBroadcastMessage event
    _long_range_ais_broadcast_message = LongRangeAisBroadcastMessage()

    # sends the 'IO.AISstream.amqp.LongRangeAisBroadcastMessage' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_long_range_ais_broadcast_message(_user_id = 'TODO: replace me', data = _long_range_ais_broadcast_message)
    print(f"Sent 'IO.AISstream.amqp.LongRangeAisBroadcastMessage' event: {_long_range_ais_broadcast_message.to_json()}")

    # ---- IO.AISstream.amqp.AddressedSafetyMessage ----
    # TODO: Supply event data for the IO.AISstream.amqp.AddressedSafetyMessage event
    _addressed_safety_message = AddressedSafetyMessage()

    # sends the 'IO.AISstream.amqp.AddressedSafetyMessage' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_addressed_safety_message(_user_id = 'TODO: replace me', data = _addressed_safety_message)
    print(f"Sent 'IO.AISstream.amqp.AddressedSafetyMessage' event: {_addressed_safety_message.to_json()}")

    # ---- IO.AISstream.amqp.AddressedBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.amqp.AddressedBinaryMessage event
    _addressed_binary_message = AddressedBinaryMessage()

    # sends the 'IO.AISstream.amqp.AddressedBinaryMessage' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_addressed_binary_message(_user_id = 'TODO: replace me', data = _addressed_binary_message)
    print(f"Sent 'IO.AISstream.amqp.AddressedBinaryMessage' event: {_addressed_binary_message.to_json()}")

    # ---- IO.AISstream.amqp.AssignedModeCommand ----
    # TODO: Supply event data for the IO.AISstream.amqp.AssignedModeCommand event
    _assigned_mode_command = AssignedModeCommand()

    # sends the 'IO.AISstream.amqp.AssignedModeCommand' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_assigned_mode_command(_user_id = 'TODO: replace me', data = _assigned_mode_command)
    print(f"Sent 'IO.AISstream.amqp.AssignedModeCommand' event: {_assigned_mode_command.to_json()}")

    # ---- IO.AISstream.amqp.BinaryAcknowledge ----
    # TODO: Supply event data for the IO.AISstream.amqp.BinaryAcknowledge event
    _binary_acknowledge = BinaryAcknowledge()

    # sends the 'IO.AISstream.amqp.BinaryAcknowledge' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_binary_acknowledge(_user_id = 'TODO: replace me', data = _binary_acknowledge)
    print(f"Sent 'IO.AISstream.amqp.BinaryAcknowledge' event: {_binary_acknowledge.to_json()}")

    # ---- IO.AISstream.amqp.BinaryBroadcastMessage ----
    # TODO: Supply event data for the IO.AISstream.amqp.BinaryBroadcastMessage event
    _binary_broadcast_message = BinaryBroadcastMessage()

    # sends the 'IO.AISstream.amqp.BinaryBroadcastMessage' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_binary_broadcast_message(_user_id = 'TODO: replace me', data = _binary_broadcast_message)
    print(f"Sent 'IO.AISstream.amqp.BinaryBroadcastMessage' event: {_binary_broadcast_message.to_json()}")

    # ---- IO.AISstream.amqp.ChannelManagement ----
    # TODO: Supply event data for the IO.AISstream.amqp.ChannelManagement event
    _channel_management = ChannelManagement()

    # sends the 'IO.AISstream.amqp.ChannelManagement' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_channel_management(_user_id = 'TODO: replace me', data = _channel_management)
    print(f"Sent 'IO.AISstream.amqp.ChannelManagement' event: {_channel_management.to_json()}")

    # ---- IO.AISstream.amqp.CoordinatedUTCInquiry ----
    # TODO: Supply event data for the IO.AISstream.amqp.CoordinatedUTCInquiry event
    _coordinated_utcinquiry = CoordinatedUTCInquiry()

    # sends the 'IO.AISstream.amqp.CoordinatedUTCInquiry' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_coordinated_utcinquiry(_user_id = 'TODO: replace me', data = _coordinated_utcinquiry)
    print(f"Sent 'IO.AISstream.amqp.CoordinatedUTCInquiry' event: {_coordinated_utcinquiry.to_json()}")

    # ---- IO.AISstream.amqp.DataLinkManagementMessage ----
    # TODO: Supply event data for the IO.AISstream.amqp.DataLinkManagementMessage event
    _data_link_management_message = DataLinkManagementMessage()

    # sends the 'IO.AISstream.amqp.DataLinkManagementMessage' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_data_link_management_message(_user_id = 'TODO: replace me', data = _data_link_management_message)
    print(f"Sent 'IO.AISstream.amqp.DataLinkManagementMessage' event: {_data_link_management_message.to_json()}")

    # ---- IO.AISstream.amqp.GnssBroadcastBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.amqp.GnssBroadcastBinaryMessage event
    _gnss_broadcast_binary_message = GnssBroadcastBinaryMessage()

    # sends the 'IO.AISstream.amqp.GnssBroadcastBinaryMessage' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_gnss_broadcast_binary_message(_user_id = 'TODO: replace me', data = _gnss_broadcast_binary_message)
    print(f"Sent 'IO.AISstream.amqp.GnssBroadcastBinaryMessage' event: {_gnss_broadcast_binary_message.to_json()}")

    # ---- IO.AISstream.amqp.GroupAssignmentCommand ----
    # TODO: Supply event data for the IO.AISstream.amqp.GroupAssignmentCommand event
    _group_assignment_command = GroupAssignmentCommand()

    # sends the 'IO.AISstream.amqp.GroupAssignmentCommand' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_group_assignment_command(_user_id = 'TODO: replace me', data = _group_assignment_command)
    print(f"Sent 'IO.AISstream.amqp.GroupAssignmentCommand' event: {_group_assignment_command.to_json()}")

    # ---- IO.AISstream.amqp.Interrogation ----
    # TODO: Supply event data for the IO.AISstream.amqp.Interrogation event
    _interrogation = Interrogation()

    # sends the 'IO.AISstream.amqp.Interrogation' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_interrogation(_user_id = 'TODO: replace me', data = _interrogation)
    print(f"Sent 'IO.AISstream.amqp.Interrogation' event: {_interrogation.to_json()}")

    # ---- IO.AISstream.amqp.MultiSlotBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.amqp.MultiSlotBinaryMessage event
    _multi_slot_binary_message = MultiSlotBinaryMessage()

    # sends the 'IO.AISstream.amqp.MultiSlotBinaryMessage' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_multi_slot_binary_message(_user_id = 'TODO: replace me', data = _multi_slot_binary_message)
    print(f"Sent 'IO.AISstream.amqp.MultiSlotBinaryMessage' event: {_multi_slot_binary_message.to_json()}")

    # ---- IO.AISstream.amqp.SingleSlotBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.amqp.SingleSlotBinaryMessage event
    _single_slot_binary_message = SingleSlotBinaryMessage()

    # sends the 'IO.AISstream.amqp.SingleSlotBinaryMessage' event to Kafka topic.
    await ioaisstream_amqp_event_producer.send_io_aisstream_amqp_single_slot_binary_message(_user_id = 'TODO: replace me', data = _single_slot_binary_message)
    print(f"Sent 'IO.AISstream.amqp.SingleSlotBinaryMessage' event: {_single_slot_binary_message.to_json()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer")
    parser.add_argument('--producer-config', default=os.getenv('KAFKA_PRODUCER_CONFIG'), help='Kafka producer config (JSON)', required=False)
    parser.add_argument('--topics', default=os.getenv('KAFKA_TOPICS'), help='Kafka topics to send events to', required=False)
    parser.add_argument('-c', '--connection-string', dest='connection_string', default=os.getenv('FABRIC_CONNECTION_STRING'), help='Fabric connection string', required=False)

    args = parser.parse_args()

    asyncio.run(main(
        args.connection_string,
        args.producer_config,
        args.topics
    ))