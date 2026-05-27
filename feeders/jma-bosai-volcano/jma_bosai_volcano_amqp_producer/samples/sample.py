
"""
Sample usage of jma_bosai_volcano_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from jma_bosai_volcano_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = JPJMAVolcanoAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Volcano message
        print("Sending Volcano message...")
        # TODO: Create a Volcano instance with actual data
        # data = Volcano(...)
        # producer.send_volcano(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Volcano message sent successfully!")
        
        
        
        # Send VolcanicWarning message
        print("Sending VolcanicWarning message...")
        # TODO: Create a VolcanicWarning instance with actual data
        # data = VolcanicWarning(...)
        # producer.send_volcanic_warning(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("VolcanicWarning message sent successfully!")
        
        
        
        # Send VolcanicEruption message
        print("Sending VolcanicEruption message...")
        # TODO: Create a VolcanicEruption instance with actual data
        # data = VolcanicEruption(...)
        # producer.send_volcanic_eruption(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("VolcanicEruption message sent successfully!")
        
        
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