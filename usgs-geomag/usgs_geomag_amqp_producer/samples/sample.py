
"""
Sample usage of usgs_geomag_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from usgs_geomag_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = GovUsgsGeomagAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Observatory message
        print("Sending Observatory message...")
        # TODO: Create a Observatory instance with actual data
        # data = Observatory(...)
        # producer.send_observatory(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Observatory message sent successfully!")
        
        
        
        # Send MagneticFieldReading message
        print("Sending MagneticFieldReading message...")
        # TODO: Create a MagneticFieldReading instance with actual data
        # data = MagneticFieldReading(...)
        # producer.send_magnetic_field_reading(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("MagneticFieldReading message sent successfully!")
        
        
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