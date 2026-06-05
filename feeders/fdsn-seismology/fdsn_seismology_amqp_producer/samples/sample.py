
"""
Sample usage of fdsn_seismology_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from fdsn_seismology_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = OrgFdsnEventAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Earthquake message
        print("Sending Earthquake message...")
        # TODO: Create a Earthquake instance with actual data
        # data = Earthquake(...)
        # producer.send_earthquake(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Earthquake message sent successfully!")
        
        
        
        # Send Node message
        print("Sending Node message...")
        # TODO: Create a Node instance with actual data
        # data = Node(...)
        # producer.send_node(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Node message sent successfully!")
        
        
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