
"""
Sample usage of paris_bicycle_counters_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from paris_bicycle_counters_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = FRParisOpenDataVeloAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Counter message
        print("Sending Counter message...")
        # TODO: Create a Counter instance with actual data
        # data = Counter(...)
        # producer.send_counter(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Counter message sent successfully!")
        
        
        
        # Send BicycleCount message
        print("Sending BicycleCount message...")
        # TODO: Create a BicycleCount instance with actual data
        # data = BicycleCount(...)
        # producer.send_bicycle_count(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("BicycleCount message sent successfully!")
        
        
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