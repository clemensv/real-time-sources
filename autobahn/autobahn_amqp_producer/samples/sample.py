
"""
Sample usage of autobahn_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from autobahn_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = DEAutobahnAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send RoadworkAppeared message
        print("Sending RoadworkAppeared message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_roadwork_appeared(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RoadworkAppeared message sent successfully!")
        
        
        
        # Send RoadworkUpdated message
        print("Sending RoadworkUpdated message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_roadwork_updated(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RoadworkUpdated message sent successfully!")
        
        
        
        # Send RoadworkResolved message
        print("Sending RoadworkResolved message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_roadwork_resolved(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RoadworkResolved message sent successfully!")
        
        
        
        # Send ShortTermRoadworkAppeared message
        print("Sending ShortTermRoadworkAppeared message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_short_term_roadwork_appeared(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ShortTermRoadworkAppeared message sent successfully!")
        
        
        
        # Send ShortTermRoadworkUpdated message
        print("Sending ShortTermRoadworkUpdated message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_short_term_roadwork_updated(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ShortTermRoadworkUpdated message sent successfully!")
        
        
        
        # Send ShortTermRoadworkResolved message
        print("Sending ShortTermRoadworkResolved message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_short_term_roadwork_resolved(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ShortTermRoadworkResolved message sent successfully!")
        
        
        
        # Send ClosureAppeared message
        print("Sending ClosureAppeared message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_closure_appeared(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ClosureAppeared message sent successfully!")
        
        
        
        # Send ClosureUpdated message
        print("Sending ClosureUpdated message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_closure_updated(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ClosureUpdated message sent successfully!")
        
        
        
        # Send ClosureResolved message
        print("Sending ClosureResolved message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_closure_resolved(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ClosureResolved message sent successfully!")
        
        
        
        # Send EntryExitClosureAppeared message
        print("Sending EntryExitClosureAppeared message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_entry_exit_closure_appeared(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("EntryExitClosureAppeared message sent successfully!")
        
        
        
        # Send EntryExitClosureUpdated message
        print("Sending EntryExitClosureUpdated message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_entry_exit_closure_updated(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("EntryExitClosureUpdated message sent successfully!")
        
        
        
        # Send EntryExitClosureResolved message
        print("Sending EntryExitClosureResolved message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_entry_exit_closure_resolved(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("EntryExitClosureResolved message sent successfully!")
        
        
        
        # Send WarningAppeared message
        print("Sending WarningAppeared message...")
        # TODO: Create a WarningEvent instance with actual data
        # data = WarningEvent(...)
        # producer.send_warning_appeared(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WarningAppeared message sent successfully!")
        
        
        
        # Send WarningUpdated message
        print("Sending WarningUpdated message...")
        # TODO: Create a WarningEvent instance with actual data
        # data = WarningEvent(...)
        # producer.send_warning_updated(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WarningUpdated message sent successfully!")
        
        
        
        # Send WarningResolved message
        print("Sending WarningResolved message...")
        # TODO: Create a WarningEvent instance with actual data
        # data = WarningEvent(...)
        # producer.send_warning_resolved(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WarningResolved message sent successfully!")
        
        
        
        # Send WeightLimit35RestrictionAppeared message
        print("Sending WeightLimit35RestrictionAppeared message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_weight_limit35_restriction_appeared(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WeightLimit35RestrictionAppeared message sent successfully!")
        
        
        
        # Send WeightLimit35RestrictionUpdated message
        print("Sending WeightLimit35RestrictionUpdated message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_weight_limit35_restriction_updated(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WeightLimit35RestrictionUpdated message sent successfully!")
        
        
        
        # Send WeightLimit35RestrictionResolved message
        print("Sending WeightLimit35RestrictionResolved message...")
        # TODO: Create a RoadEvent instance with actual data
        # data = RoadEvent(...)
        # producer.send_weight_limit35_restriction_resolved(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WeightLimit35RestrictionResolved message sent successfully!")
        
        
        
        # Send WebcamAppeared message
        print("Sending WebcamAppeared message...")
        # TODO: Create a Webcam instance with actual data
        # data = Webcam(...)
        # producer.send_webcam_appeared(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WebcamAppeared message sent successfully!")
        
        
        
        # Send WebcamUpdated message
        print("Sending WebcamUpdated message...")
        # TODO: Create a Webcam instance with actual data
        # data = Webcam(...)
        # producer.send_webcam_updated(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WebcamUpdated message sent successfully!")
        
        
        
        # Send WebcamResolved message
        print("Sending WebcamResolved message...")
        # TODO: Create a Webcam instance with actual data
        # data = Webcam(...)
        # producer.send_webcam_resolved(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WebcamResolved message sent successfully!")
        
        
        
        # Send ParkingLorryAppeared message
        print("Sending ParkingLorryAppeared message...")
        # TODO: Create a ParkingLorry instance with actual data
        # data = ParkingLorry(...)
        # producer.send_parking_lorry_appeared(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ParkingLorryAppeared message sent successfully!")
        
        
        
        # Send ParkingLorryUpdated message
        print("Sending ParkingLorryUpdated message...")
        # TODO: Create a ParkingLorry instance with actual data
        # data = ParkingLorry(...)
        # producer.send_parking_lorry_updated(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ParkingLorryUpdated message sent successfully!")
        
        
        
        # Send ParkingLorryResolved message
        print("Sending ParkingLorryResolved message...")
        # TODO: Create a ParkingLorry instance with actual data
        # data = ParkingLorry(...)
        # producer.send_parking_lorry_resolved(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ParkingLorryResolved message sent successfully!")
        
        
        
        # Send ElectricChargingStationAppeared message
        print("Sending ElectricChargingStationAppeared message...")
        # TODO: Create a ChargingStation instance with actual data
        # data = ChargingStation(...)
        # producer.send_electric_charging_station_appeared(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ElectricChargingStationAppeared message sent successfully!")
        
        
        
        # Send ElectricChargingStationUpdated message
        print("Sending ElectricChargingStationUpdated message...")
        # TODO: Create a ChargingStation instance with actual data
        # data = ChargingStation(...)
        # producer.send_electric_charging_station_updated(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ElectricChargingStationUpdated message sent successfully!")
        
        
        
        # Send ElectricChargingStationResolved message
        print("Sending ElectricChargingStationResolved message...")
        # TODO: Create a ChargingStation instance with actual data
        # data = ChargingStation(...)
        # producer.send_electric_charging_station_resolved(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ElectricChargingStationResolved message sent successfully!")
        
        
        
        # Send StrongElectricChargingStationAppeared message
        print("Sending StrongElectricChargingStationAppeared message...")
        # TODO: Create a ChargingStation instance with actual data
        # data = ChargingStation(...)
        # producer.send_strong_electric_charging_station_appeared(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("StrongElectricChargingStationAppeared message sent successfully!")
        
        
        
        # Send StrongElectricChargingStationUpdated message
        print("Sending StrongElectricChargingStationUpdated message...")
        # TODO: Create a ChargingStation instance with actual data
        # data = ChargingStation(...)
        # producer.send_strong_electric_charging_station_updated(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("StrongElectricChargingStationUpdated message sent successfully!")
        
        
        
        # Send StrongElectricChargingStationResolved message
        print("Sending StrongElectricChargingStationResolved message...")
        # TODO: Create a ChargingStation instance with actual data
        # data = ChargingStation(...)
        # producer.send_strong_electric_charging_station_resolved(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("StrongElectricChargingStationResolved message sent successfully!")
        
        
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