
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

# imports for the data classes for each event

from aisstream_producer_data.positionreport import PositionReport
from aisstream_producer_data.shipstaticdata import ShipStaticData
from aisstream_producer_data.standardclassbpositionreport import StandardClassBPositionReport
from aisstream_producer_data.extendedclassbpositionreport import ExtendedClassBPositionReport
from aisstream_producer_data.aidstonavigationreport import AidsToNavigationReport
from aisstream_producer_data.staticdatareport import StaticDataReport
from aisstream_producer_data.basestationreport import BaseStationReport
from aisstream_producer_data.safetybroadcastmessage import SafetyBroadcastMessage
from aisstream_producer_data.standardsearchandrescueaircraftreport import StandardSearchAndRescueAircraftReport
from aisstream_producer_data.longrangeaisbroadcastmessage import LongRangeAisBroadcastMessage
from aisstream_producer_data.addressedsafetymessage import AddressedSafetyMessage
from aisstream_producer_data.addressedbinarymessage import AddressedBinaryMessage
from aisstream_producer_data.assignedmodecommand import AssignedModeCommand
from aisstream_producer_data.binaryacknowledge import BinaryAcknowledge
from aisstream_producer_data.binarybroadcastmessage import BinaryBroadcastMessage
from aisstream_producer_data.channelmanagement import ChannelManagement
from aisstream_producer_data.coordinatedutcinquiry import CoordinatedUTCInquiry
from aisstream_producer_data.datalinkmanagementmessage import DataLinkManagementMessage
from aisstream_producer_data.gnssbroadcastbinarymessage import GnssBroadcastBinaryMessage
from aisstream_producer_data.groupassignmentcommand import GroupAssignmentCommand
from aisstream_producer_data.interrogation import Interrogation
from aisstream_producer_data.multislotbinarymessage import MultiSlotBinaryMessage
from aisstream_producer_data.singleslotbinarymessage import SingleSlotBinaryMessage

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
    await ioaisstream_event_producer.send_io_aisstream_position_report(data = _position_report)
    print(f"Sent 'IO.AISstream.PositionReport' event: {_position_report.to_json()}")

    # ---- IO.AISstream.ShipStaticData ----
    # TODO: Supply event data for the IO.AISstream.ShipStaticData event
    _ship_static_data = ShipStaticData()

    # sends the 'IO.AISstream.ShipStaticData' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_ship_static_data(data = _ship_static_data)
    print(f"Sent 'IO.AISstream.ShipStaticData' event: {_ship_static_data.to_json()}")

    # ---- IO.AISstream.StandardClassBPositionReport ----
    # TODO: Supply event data for the IO.AISstream.StandardClassBPositionReport event
    _standard_class_bposition_report = StandardClassBPositionReport()

    # sends the 'IO.AISstream.StandardClassBPositionReport' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_standard_class_bposition_report(data = _standard_class_bposition_report)
    print(f"Sent 'IO.AISstream.StandardClassBPositionReport' event: {_standard_class_bposition_report.to_json()}")

    # ---- IO.AISstream.ExtendedClassBPositionReport ----
    # TODO: Supply event data for the IO.AISstream.ExtendedClassBPositionReport event
    _extended_class_bposition_report = ExtendedClassBPositionReport()

    # sends the 'IO.AISstream.ExtendedClassBPositionReport' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_extended_class_bposition_report(data = _extended_class_bposition_report)
    print(f"Sent 'IO.AISstream.ExtendedClassBPositionReport' event: {_extended_class_bposition_report.to_json()}")

    # ---- IO.AISstream.AidsToNavigationReport ----
    # TODO: Supply event data for the IO.AISstream.AidsToNavigationReport event
    _aids_to_navigation_report = AidsToNavigationReport()

    # sends the 'IO.AISstream.AidsToNavigationReport' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_aids_to_navigation_report(data = _aids_to_navigation_report)
    print(f"Sent 'IO.AISstream.AidsToNavigationReport' event: {_aids_to_navigation_report.to_json()}")

    # ---- IO.AISstream.StaticDataReport ----
    # TODO: Supply event data for the IO.AISstream.StaticDataReport event
    _static_data_report = StaticDataReport()

    # sends the 'IO.AISstream.StaticDataReport' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_static_data_report(data = _static_data_report)
    print(f"Sent 'IO.AISstream.StaticDataReport' event: {_static_data_report.to_json()}")

    # ---- IO.AISstream.BaseStationReport ----
    # TODO: Supply event data for the IO.AISstream.BaseStationReport event
    _base_station_report = BaseStationReport()

    # sends the 'IO.AISstream.BaseStationReport' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_base_station_report(data = _base_station_report)
    print(f"Sent 'IO.AISstream.BaseStationReport' event: {_base_station_report.to_json()}")

    # ---- IO.AISstream.SafetyBroadcastMessage ----
    # TODO: Supply event data for the IO.AISstream.SafetyBroadcastMessage event
    _safety_broadcast_message = SafetyBroadcastMessage()

    # sends the 'IO.AISstream.SafetyBroadcastMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_safety_broadcast_message(data = _safety_broadcast_message)
    print(f"Sent 'IO.AISstream.SafetyBroadcastMessage' event: {_safety_broadcast_message.to_json()}")

    # ---- IO.AISstream.StandardSearchAndRescueAircraftReport ----
    # TODO: Supply event data for the IO.AISstream.StandardSearchAndRescueAircraftReport event
    _standard_search_and_rescue_aircraft_report = StandardSearchAndRescueAircraftReport()

    # sends the 'IO.AISstream.StandardSearchAndRescueAircraftReport' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_standard_search_and_rescue_aircraft_report(data = _standard_search_and_rescue_aircraft_report)
    print(f"Sent 'IO.AISstream.StandardSearchAndRescueAircraftReport' event: {_standard_search_and_rescue_aircraft_report.to_json()}")

    # ---- IO.AISstream.LongRangeAisBroadcastMessage ----
    # TODO: Supply event data for the IO.AISstream.LongRangeAisBroadcastMessage event
    _long_range_ais_broadcast_message = LongRangeAisBroadcastMessage()

    # sends the 'IO.AISstream.LongRangeAisBroadcastMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_long_range_ais_broadcast_message(data = _long_range_ais_broadcast_message)
    print(f"Sent 'IO.AISstream.LongRangeAisBroadcastMessage' event: {_long_range_ais_broadcast_message.to_json()}")

    # ---- IO.AISstream.AddressedSafetyMessage ----
    # TODO: Supply event data for the IO.AISstream.AddressedSafetyMessage event
    _addressed_safety_message = AddressedSafetyMessage()

    # sends the 'IO.AISstream.AddressedSafetyMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_addressed_safety_message(data = _addressed_safety_message)
    print(f"Sent 'IO.AISstream.AddressedSafetyMessage' event: {_addressed_safety_message.to_json()}")

    # ---- IO.AISstream.AddressedBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.AddressedBinaryMessage event
    _addressed_binary_message = AddressedBinaryMessage()

    # sends the 'IO.AISstream.AddressedBinaryMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_addressed_binary_message(data = _addressed_binary_message)
    print(f"Sent 'IO.AISstream.AddressedBinaryMessage' event: {_addressed_binary_message.to_json()}")

    # ---- IO.AISstream.AssignedModeCommand ----
    # TODO: Supply event data for the IO.AISstream.AssignedModeCommand event
    _assigned_mode_command = AssignedModeCommand()

    # sends the 'IO.AISstream.AssignedModeCommand' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_assigned_mode_command(data = _assigned_mode_command)
    print(f"Sent 'IO.AISstream.AssignedModeCommand' event: {_assigned_mode_command.to_json()}")

    # ---- IO.AISstream.BinaryAcknowledge ----
    # TODO: Supply event data for the IO.AISstream.BinaryAcknowledge event
    _binary_acknowledge = BinaryAcknowledge()

    # sends the 'IO.AISstream.BinaryAcknowledge' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_binary_acknowledge(data = _binary_acknowledge)
    print(f"Sent 'IO.AISstream.BinaryAcknowledge' event: {_binary_acknowledge.to_json()}")

    # ---- IO.AISstream.BinaryBroadcastMessage ----
    # TODO: Supply event data for the IO.AISstream.BinaryBroadcastMessage event
    _binary_broadcast_message = BinaryBroadcastMessage()

    # sends the 'IO.AISstream.BinaryBroadcastMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_binary_broadcast_message(data = _binary_broadcast_message)
    print(f"Sent 'IO.AISstream.BinaryBroadcastMessage' event: {_binary_broadcast_message.to_json()}")

    # ---- IO.AISstream.ChannelManagement ----
    # TODO: Supply event data for the IO.AISstream.ChannelManagement event
    _channel_management = ChannelManagement()

    # sends the 'IO.AISstream.ChannelManagement' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_channel_management(data = _channel_management)
    print(f"Sent 'IO.AISstream.ChannelManagement' event: {_channel_management.to_json()}")

    # ---- IO.AISstream.CoordinatedUTCInquiry ----
    # TODO: Supply event data for the IO.AISstream.CoordinatedUTCInquiry event
    _coordinated_utcinquiry = CoordinatedUTCInquiry()

    # sends the 'IO.AISstream.CoordinatedUTCInquiry' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_coordinated_utcinquiry(data = _coordinated_utcinquiry)
    print(f"Sent 'IO.AISstream.CoordinatedUTCInquiry' event: {_coordinated_utcinquiry.to_json()}")

    # ---- IO.AISstream.DataLinkManagementMessage ----
    # TODO: Supply event data for the IO.AISstream.DataLinkManagementMessage event
    _data_link_management_message = DataLinkManagementMessage()

    # sends the 'IO.AISstream.DataLinkManagementMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_data_link_management_message(data = _data_link_management_message)
    print(f"Sent 'IO.AISstream.DataLinkManagementMessage' event: {_data_link_management_message.to_json()}")

    # ---- IO.AISstream.GnssBroadcastBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.GnssBroadcastBinaryMessage event
    _gnss_broadcast_binary_message = GnssBroadcastBinaryMessage()

    # sends the 'IO.AISstream.GnssBroadcastBinaryMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_gnss_broadcast_binary_message(data = _gnss_broadcast_binary_message)
    print(f"Sent 'IO.AISstream.GnssBroadcastBinaryMessage' event: {_gnss_broadcast_binary_message.to_json()}")

    # ---- IO.AISstream.GroupAssignmentCommand ----
    # TODO: Supply event data for the IO.AISstream.GroupAssignmentCommand event
    _group_assignment_command = GroupAssignmentCommand()

    # sends the 'IO.AISstream.GroupAssignmentCommand' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_group_assignment_command(data = _group_assignment_command)
    print(f"Sent 'IO.AISstream.GroupAssignmentCommand' event: {_group_assignment_command.to_json()}")

    # ---- IO.AISstream.Interrogation ----
    # TODO: Supply event data for the IO.AISstream.Interrogation event
    _interrogation = Interrogation()

    # sends the 'IO.AISstream.Interrogation' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_interrogation(data = _interrogation)
    print(f"Sent 'IO.AISstream.Interrogation' event: {_interrogation.to_json()}")

    # ---- IO.AISstream.MultiSlotBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.MultiSlotBinaryMessage event
    _multi_slot_binary_message = MultiSlotBinaryMessage()

    # sends the 'IO.AISstream.MultiSlotBinaryMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_multi_slot_binary_message(data = _multi_slot_binary_message)
    print(f"Sent 'IO.AISstream.MultiSlotBinaryMessage' event: {_multi_slot_binary_message.to_json()}")

    # ---- IO.AISstream.SingleSlotBinaryMessage ----
    # TODO: Supply event data for the IO.AISstream.SingleSlotBinaryMessage event
    _single_slot_binary_message = SingleSlotBinaryMessage()

    # sends the 'IO.AISstream.SingleSlotBinaryMessage' event to Kafka topic.
    await ioaisstream_event_producer.send_io_aisstream_single_slot_binary_message(data = _single_slot_binary_message)
    print(f"Sent 'IO.AISstream.SingleSlotBinaryMessage' event: {_single_slot_binary_message.to_json()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer")
    parser.add_argument('--producer-config', default=os.getenv('KAFKA_PRODUCER_CONFIG'), help='Kafka producer config (JSON)', required=False)
    parser.add_argument('--topics', default=os.getenv('KAFKA_TOPICS'), help='Kafka topics to send events to', required=False)
    parser.add_argument('-c|--connection-string', dest='connection_string', default=os.getenv('FABRIC_CONNECTION_STRING'), help='Fabric connection string', required=False)

    args = parser.parse_args()

    asyncio.run(main(
        args.connection_string,
        args.producer_config,
        args.topics
    ))