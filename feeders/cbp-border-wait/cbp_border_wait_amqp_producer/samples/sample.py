
"""
Sample usage of cbp_border_wait_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from cbp_border_wait_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = GovCbpBorderwaitAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Port message
        print("Sending Port message...")
        # TODO: Create a Port instance with actual data
        # data = Port(...)
        # producer.send_port(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Port message sent successfully!")
        
        
        
        # Send WaitTime message
        print("Sending WaitTime message...")
        # TODO: Create a WaitTime instance with actual data
        # data = WaitTime(...)
        # producer.send_wait_time(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WaitTime message sent successfully!")
        
        
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