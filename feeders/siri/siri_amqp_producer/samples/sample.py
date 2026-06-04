
"""
Sample usage of siri_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from siri_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = OrgSiriAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send VehiclePosition message
        print("Sending VehiclePosition message...")
        # TODO: Create a VehiclePosition instance with actual data
        # data = VehiclePosition(...)
        # producer.send_vehicle_position(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("VehiclePosition message sent successfully!")
        
        
        
        # Send Operator message
        print("Sending Operator message...")
        # TODO: Create a Operator instance with actual data
        # data = Operator(...)
        # producer.send_operator(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Operator message sent successfully!")
        
        
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