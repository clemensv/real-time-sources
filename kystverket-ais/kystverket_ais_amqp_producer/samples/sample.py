
"""
Sample usage of kystverket_ais_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from kystverket_ais_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = NOKystverketAISAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send PositionReport message
        print("Sending PositionReport message...")
        # TODO: Create a PositionReport instance with actual data
        # data = PositionReport(...)
        # producer.send_position_report(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("PositionReport message sent successfully!")
        
        
        
        # Send ShipStatic message
        print("Sending ShipStatic message...")
        # TODO: Create a ShipStatic instance with actual data
        # data = ShipStatic(...)
        # producer.send_ship_static(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ShipStatic message sent successfully!")
        
        
        
        # Send AidToNavigation message
        print("Sending AidToNavigation message...")
        # TODO: Create a AidToNavigation instance with actual data
        # data = AidToNavigation(...)
        # producer.send_aid_to_navigation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("AidToNavigation message sent successfully!")
        
        
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