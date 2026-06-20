
"""
Sample usage of erddap_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from erddap_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = OrgErddapAmqpDatasetProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send DatasetMetadata message
        print("Sending DatasetMetadata message...")
        # TODO: Create a DatasetMetadata instance with actual data
        # data = DatasetMetadata(...)
        # producer.send_dataset_metadata(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("DatasetMetadata message sent successfully!")
        
        
        print("\nAll messages sent successfully!")
        
    except Exception as e:
        print(f"Error sending messages: {e}", file=sys.stderr)
        return 1
    finally:
        producer.close()
        print("Producer closed")
    
    return 0
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = OrgErddapAmqpStationProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send StationMetadata message
        print("Sending StationMetadata message...")
        # TODO: Create a StationMetadata instance with actual data
        # data = StationMetadata(...)
        # producer.send_station_metadata(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("StationMetadata message sent successfully!")
        
        
        
        # Send Observation message
        print("Sending Observation message...")
        # TODO: Create a Observation instance with actual data
        # data = Observation(...)
        # producer.send_observation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Observation message sent successfully!")
        
        
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