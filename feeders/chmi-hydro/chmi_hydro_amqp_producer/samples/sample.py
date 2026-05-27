
"""
Sample usage of chmi_hydro_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from chmi_hydro_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = CZGovCHMIHydroAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Station message
        print("Sending Station message...")
        # TODO: Create a Station instance with actual data
        # data = Station(...)
        # producer.send_station(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Station message sent successfully!")
        
        
        
        # Send WaterLevelObservation message
        print("Sending WaterLevelObservation message...")
        # TODO: Create a WaterLevelObservation instance with actual data
        # data = WaterLevelObservation(...)
        # producer.send_water_level_observation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WaterLevelObservation message sent successfully!")
        
        
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