
"""
Sample usage of gbfs_bikeshare_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from gbfs_bikeshare_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = OrgGbfsAmqpSystemProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send SystemInformation message
        print("Sending SystemInformation message...")
        # TODO: Create a SystemInformation instance with actual data
        # data = SystemInformation(...)
        # producer.send_system_information(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("SystemInformation message sent successfully!")
        
        
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
    producer = OrgGbfsAmqpStationsProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send StationInformation message
        print("Sending StationInformation message...")
        # TODO: Create a StationInformation instance with actual data
        # data = StationInformation(...)
        # producer.send_station_information(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("StationInformation message sent successfully!")
        
        
        
        # Send StationStatus message
        print("Sending StationStatus message...")
        # TODO: Create a StationStatus instance with actual data
        # data = StationStatus(...)
        # producer.send_station_status(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("StationStatus message sent successfully!")
        
        
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
    producer = OrgGbfsAmqpFreeBikesProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send FreeBikeStatus message
        print("Sending FreeBikeStatus message...")
        # TODO: Create a FreeBikeStatus instance with actual data
        # data = FreeBikeStatus(...)
        # producer.send_free_bike_status(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("FreeBikeStatus message sent successfully!")
        
        
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