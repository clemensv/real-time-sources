
"""
Sample usage of tfl_road_traffic_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from tfl_road_traffic_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = UkGovTflRoadAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send RoadCorridor message
        print("Sending RoadCorridor message...")
        # TODO: Create a RoadCorridor instance with actual data
        # data = RoadCorridor(...)
        # producer.send_road_corridor(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RoadCorridor message sent successfully!")
        
        
        
        # Send RoadStatus message
        print("Sending RoadStatus message...")
        # TODO: Create a RoadStatus instance with actual data
        # data = RoadStatus(...)
        # producer.send_road_status(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RoadStatus message sent successfully!")
        
        
        
        # Send RoadDisruptionSerious message
        print("Sending RoadDisruptionSerious message...")
        # TODO: Create a RoadDisruption instance with actual data
        # data = RoadDisruption(...)
        # producer.send_road_disruption_serious(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RoadDisruptionSerious message sent successfully!")
        
        
        
        # Send RoadDisruptionSevere message
        print("Sending RoadDisruptionSevere message...")
        # TODO: Create a RoadDisruption instance with actual data
        # data = RoadDisruption(...)
        # producer.send_road_disruption_severe(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RoadDisruptionSevere message sent successfully!")
        
        
        
        # Send RoadDisruptionModerate message
        print("Sending RoadDisruptionModerate message...")
        # TODO: Create a RoadDisruption instance with actual data
        # data = RoadDisruption(...)
        # producer.send_road_disruption_moderate(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RoadDisruptionModerate message sent successfully!")
        
        
        
        # Send RoadDisruptionMinor message
        print("Sending RoadDisruptionMinor message...")
        # TODO: Create a RoadDisruption instance with actual data
        # data = RoadDisruption(...)
        # producer.send_road_disruption_minor(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RoadDisruptionMinor message sent successfully!")
        
        
        
        # Send RoadDisruptionInformation message
        print("Sending RoadDisruptionInformation message...")
        # TODO: Create a RoadDisruption instance with actual data
        # data = RoadDisruption(...)
        # producer.send_road_disruption_information(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RoadDisruptionInformation message sent successfully!")
        
        
        
        # Send RoadDisruptionClosure message
        print("Sending RoadDisruptionClosure message...")
        # TODO: Create a RoadDisruption instance with actual data
        # data = RoadDisruption(...)
        # producer.send_road_disruption_closure(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RoadDisruptionClosure message sent successfully!")
        
        
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