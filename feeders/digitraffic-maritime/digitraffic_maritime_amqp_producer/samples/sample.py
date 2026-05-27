
"""
Sample usage of digitraffic_maritime_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from digitraffic_maritime_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = FiDigitrafficMarineAisAmqpProducer(
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
        # TODO: Create a VesselLocation instance with actual data
        # data = VesselLocation(...)
        # producer.send_location(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Location message sent successfully!")
        
        
        
        # Send Metadata message
        print("Sending Metadata message...")
        # TODO: Create a VesselMetadata instance with actual data
        # data = VesselMetadata(...)
        # producer.send_metadata(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Metadata message sent successfully!")
        
        
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
    producer = FiDigitrafficMarinePortcallAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send PortCall message
        print("Sending PortCall message...")
        # TODO: Create a PortCall instance with actual data
        # data = PortCall(...)
        # producer.send_port_call(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("PortCall message sent successfully!")
        
        
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
    producer = FiDigitrafficMarinePortcallVesseldetailsAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send VesselDetails message
        print("Sending VesselDetails message...")
        # TODO: Create a VesselDetails instance with actual data
        # data = VesselDetails(...)
        # producer.send_vessel_details(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("VesselDetails message sent successfully!")
        
        
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
    producer = FiDigitrafficMarinePortcallPortlocationAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send PortLocation message
        print("Sending PortLocation message...")
        # TODO: Create a PortLocation instance with actual data
        # data = PortLocation(...)
        # producer.send_port_location(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("PortLocation message sent successfully!")
        
        
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