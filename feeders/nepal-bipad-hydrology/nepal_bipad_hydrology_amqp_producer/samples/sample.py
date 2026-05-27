
"""
Sample usage of nepal_bipad_hydrology_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from nepal_bipad_hydrology_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = NpGovBipadHydrologyAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send RiverStation message
        print("Sending RiverStation message...")
        # TODO: Create a RiverStation instance with actual data
        # data = RiverStation(...)
        # producer.send_river_station(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RiverStation message sent successfully!")
        
        
        
        # Send WaterLevelReading message
        print("Sending WaterLevelReading message...")
        # TODO: Create a WaterLevelReading instance with actual data
        # data = WaterLevelReading(...)
        # producer.send_water_level_reading(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WaterLevelReading message sent successfully!")
        
        
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