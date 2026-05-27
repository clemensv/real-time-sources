
"""
Sample usage of wikimedia_osm_diffs_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from wikimedia_osm_diffs_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = OrgOpenStreetMapDiffsAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send MapChange message
        print("Sending MapChange message...")
        # TODO: Create a MapChange instance with actual data
        # data = MapChange(...)
        # producer.send_map_change(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("MapChange message sent successfully!")
        
        
        
        # Send ReplicationState message
        print("Sending ReplicationState message...")
        # TODO: Create a ReplicationState instance with actual data
        # data = ReplicationState(...)
        # producer.send_replication_state(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ReplicationState message sent successfully!")
        
        
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