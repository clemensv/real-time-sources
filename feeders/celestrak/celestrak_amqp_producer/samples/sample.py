
"""
Sample usage of celestrak_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from celestrak_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = OrgCelestrakAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send SatelliteCatalogEntry message
        print("Sending SatelliteCatalogEntry message...")
        # TODO: Create a SatelliteCatalogEntry instance with actual data
        # data = SatelliteCatalogEntry(...)
        # producer.send_satellite_catalog_entry(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("SatelliteCatalogEntry message sent successfully!")
        
        
        
        # Send OrbitMeanElements message
        print("Sending OrbitMeanElements message...")
        # TODO: Create a OrbitMeanElements instance with actual data
        # data = OrbitMeanElements(...)
        # producer.send_orbit_mean_elements(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("OrbitMeanElements message sent successfully!")
        
        
        
        # Send SupplementalOrbitMeanElements message
        print("Sending SupplementalOrbitMeanElements message...")
        # TODO: Create a SupplementalOrbitMeanElements instance with actual data
        # data = SupplementalOrbitMeanElements(...)
        # producer.send_supplemental_orbit_mean_elements(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("SupplementalOrbitMeanElements message sent successfully!")
        
        
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