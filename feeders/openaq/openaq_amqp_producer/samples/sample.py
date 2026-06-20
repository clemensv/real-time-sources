
"""
Sample usage of openaq_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from openaq_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = OrgOpenaqLocationsAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Location message
        print("Sending Location message...")
        # TODO: Create a Location instance with actual data
        # data = Location(...)
        # producer.send_location(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Location message sent successfully!")
        
        
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
    producer = OrgOpenaqSensorsAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Sensor message
        print("Sending Sensor message...")
        # TODO: Create a Sensor instance with actual data
        # data = Sensor(...)
        # producer.send_sensor(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Sensor message sent successfully!")
        
        
        
        # Send Measurement message
        print("Sending Measurement message...")
        # TODO: Create a Measurement instance with actual data
        # data = Measurement(...)
        # producer.send_measurement(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Measurement message sent successfully!")
        
        
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