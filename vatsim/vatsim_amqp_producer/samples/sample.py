
"""
Sample usage of vatsim_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from vatsim_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = NetVatsimAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send PilotPosition message
        print("Sending PilotPosition message...")
        # TODO: Create a PilotPosition instance with actual data
        # data = PilotPosition(...)
        # producer.send_pilot_position(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("PilotPosition message sent successfully!")
        
        
        
        # Send ControllerPosition message
        print("Sending ControllerPosition message...")
        # TODO: Create a ControllerPosition instance with actual data
        # data = ControllerPosition(...)
        # producer.send_controller_position(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ControllerPosition message sent successfully!")
        
        
        
        # Send FacilityStatus message
        print("Sending FacilityStatus message...")
        # TODO: Create a NetworkStatus instance with actual data
        # data = NetworkStatus(...)
        # producer.send_facility_status(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("FacilityStatus message sent successfully!")
        
        
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