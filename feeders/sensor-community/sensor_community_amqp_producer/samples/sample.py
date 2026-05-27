
"""
Sample usage of sensor_community_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from sensor_community_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = IoSensorCommunityAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send SensorInfo message
        print("Sending SensorInfo message...")
        # TODO: Create a SensorInfo instance with actual data
        # data = SensorInfo(...)
        # producer.send_sensor_info(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("SensorInfo message sent successfully!")
        
        
        
        # Send SensorReading message
        print("Sending SensorReading message...")
        # TODO: Create a SensorReading instance with actual data
        # data = SensorReading(...)
        # producer.send_sensor_reading(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("SensorReading message sent successfully!")
        
        
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