
"""
Sample usage of aisstream_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from aisstream_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = IOAISstreamAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send PositionReport message
        print("Sending PositionReport message...")
        # TODO: Create a PositionReport instance with actual data
        # data = PositionReport(...)
        # producer.send_position_report(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("PositionReport message sent successfully!")
        
        
        
        # Send ShipStaticData message
        print("Sending ShipStaticData message...")
        # TODO: Create a ShipStaticData instance with actual data
        # data = ShipStaticData(...)
        # producer.send_ship_static_data(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ShipStaticData message sent successfully!")
        
        
        
        # Send StandardClassBPositionReport message
        print("Sending StandardClassBPositionReport message...")
        # TODO: Create a StandardClassBPositionReport instance with actual data
        # data = StandardClassBPositionReport(...)
        # producer.send_standard_class_bposition_report(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("StandardClassBPositionReport message sent successfully!")
        
        
        
        # Send ExtendedClassBPositionReport message
        print("Sending ExtendedClassBPositionReport message...")
        # TODO: Create a ExtendedClassBPositionReport instance with actual data
        # data = ExtendedClassBPositionReport(...)
        # producer.send_extended_class_bposition_report(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ExtendedClassBPositionReport message sent successfully!")
        
        
        
        # Send AidsToNavigationReport message
        print("Sending AidsToNavigationReport message...")
        # TODO: Create a AidsToNavigationReport instance with actual data
        # data = AidsToNavigationReport(...)
        # producer.send_aids_to_navigation_report(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("AidsToNavigationReport message sent successfully!")
        
        
        
        # Send StaticDataReport message
        print("Sending StaticDataReport message...")
        # TODO: Create a StaticDataReport instance with actual data
        # data = StaticDataReport(...)
        # producer.send_static_data_report(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("StaticDataReport message sent successfully!")
        
        
        
        # Send BaseStationReport message
        print("Sending BaseStationReport message...")
        # TODO: Create a BaseStationReport instance with actual data
        # data = BaseStationReport(...)
        # producer.send_base_station_report(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("BaseStationReport message sent successfully!")
        
        
        
        # Send SafetyBroadcastMessage message
        print("Sending SafetyBroadcastMessage message...")
        # TODO: Create a SafetyBroadcastMessage instance with actual data
        # data = SafetyBroadcastMessage(...)
        # producer.send_safety_broadcast_message(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("SafetyBroadcastMessage message sent successfully!")
        
        
        
        # Send StandardSearchAndRescueAircraftReport message
        print("Sending StandardSearchAndRescueAircraftReport message...")
        # TODO: Create a StandardSearchAndRescueAircraftReport instance with actual data
        # data = StandardSearchAndRescueAircraftReport(...)
        # producer.send_standard_search_and_rescue_aircraft_report(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("StandardSearchAndRescueAircraftReport message sent successfully!")
        
        
        
        # Send LongRangeAisBroadcastMessage message
        print("Sending LongRangeAisBroadcastMessage message...")
        # TODO: Create a LongRangeAisBroadcastMessage instance with actual data
        # data = LongRangeAisBroadcastMessage(...)
        # producer.send_long_range_ais_broadcast_message(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("LongRangeAisBroadcastMessage message sent successfully!")
        
        
        
        # Send AddressedSafetyMessage message
        print("Sending AddressedSafetyMessage message...")
        # TODO: Create a AddressedSafetyMessage instance with actual data
        # data = AddressedSafetyMessage(...)
        # producer.send_addressed_safety_message(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("AddressedSafetyMessage message sent successfully!")
        
        
        
        # Send AddressedBinaryMessage message
        print("Sending AddressedBinaryMessage message...")
        # TODO: Create a AddressedBinaryMessage instance with actual data
        # data = AddressedBinaryMessage(...)
        # producer.send_addressed_binary_message(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("AddressedBinaryMessage message sent successfully!")
        
        
        
        # Send AssignedModeCommand message
        print("Sending AssignedModeCommand message...")
        # TODO: Create a AssignedModeCommand instance with actual data
        # data = AssignedModeCommand(...)
        # producer.send_assigned_mode_command(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("AssignedModeCommand message sent successfully!")
        
        
        
        # Send BinaryAcknowledge message
        print("Sending BinaryAcknowledge message...")
        # TODO: Create a BinaryAcknowledge instance with actual data
        # data = BinaryAcknowledge(...)
        # producer.send_binary_acknowledge(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("BinaryAcknowledge message sent successfully!")
        
        
        
        # Send BinaryBroadcastMessage message
        print("Sending BinaryBroadcastMessage message...")
        # TODO: Create a BinaryBroadcastMessage instance with actual data
        # data = BinaryBroadcastMessage(...)
        # producer.send_binary_broadcast_message(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("BinaryBroadcastMessage message sent successfully!")
        
        
        
        # Send ChannelManagement message
        print("Sending ChannelManagement message...")
        # TODO: Create a ChannelManagement instance with actual data
        # data = ChannelManagement(...)
        # producer.send_channel_management(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ChannelManagement message sent successfully!")
        
        
        
        # Send CoordinatedUTCInquiry message
        print("Sending CoordinatedUTCInquiry message...")
        # TODO: Create a CoordinatedUTCInquiry instance with actual data
        # data = CoordinatedUTCInquiry(...)
        # producer.send_coordinated_utcinquiry(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("CoordinatedUTCInquiry message sent successfully!")
        
        
        
        # Send DataLinkManagementMessage message
        print("Sending DataLinkManagementMessage message...")
        # TODO: Create a DataLinkManagementMessage instance with actual data
        # data = DataLinkManagementMessage(...)
        # producer.send_data_link_management_message(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("DataLinkManagementMessage message sent successfully!")
        
        
        
        # Send GnssBroadcastBinaryMessage message
        print("Sending GnssBroadcastBinaryMessage message...")
        # TODO: Create a GnssBroadcastBinaryMessage instance with actual data
        # data = GnssBroadcastBinaryMessage(...)
        # producer.send_gnss_broadcast_binary_message(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("GnssBroadcastBinaryMessage message sent successfully!")
        
        
        
        # Send GroupAssignmentCommand message
        print("Sending GroupAssignmentCommand message...")
        # TODO: Create a GroupAssignmentCommand instance with actual data
        # data = GroupAssignmentCommand(...)
        # producer.send_group_assignment_command(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("GroupAssignmentCommand message sent successfully!")
        
        
        
        # Send Interrogation message
        print("Sending Interrogation message...")
        # TODO: Create a Interrogation instance with actual data
        # data = Interrogation(...)
        # producer.send_interrogation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Interrogation message sent successfully!")
        
        
        
        # Send MultiSlotBinaryMessage message
        print("Sending MultiSlotBinaryMessage message...")
        # TODO: Create a MultiSlotBinaryMessage instance with actual data
        # data = MultiSlotBinaryMessage(...)
        # producer.send_multi_slot_binary_message(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("MultiSlotBinaryMessage message sent successfully!")
        
        
        
        # Send SingleSlotBinaryMessage message
        print("Sending SingleSlotBinaryMessage message...")
        # TODO: Create a SingleSlotBinaryMessage instance with actual data
        # data = SingleSlotBinaryMessage(...)
        # producer.send_single_slot_binary_message(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("SingleSlotBinaryMessage message sent successfully!")
        
        
        print("\nAll messages sent successfully!")
        
    except Exception as e:
        print(f"Error sending messages: {e}", file=sys.stderr)
        return 1
    finally:
        producer.close()
        print("Producer closed")
    
    return 0
    

if __name__ == "__main__":
    sys.exit(main())