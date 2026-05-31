
"""
Sample usage of nasa_firms_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from nasa_firms_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = NASAFIRMSAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send FireDetection message
        print("Sending FireDetection message...")
        # TODO: Create a FireDetection instance with actual data
        # data = FireDetection(...)
        # producer.send_fire_detection(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("FireDetection message sent successfully!")
        
        
        
        # Send DataAvailability message
        print("Sending DataAvailability message...")
        # TODO: Create a DataAvailability instance with actual data
        # data = DataAvailability(...)
        # producer.send_data_availability(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("DataAvailability message sent successfully!")
        
        
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