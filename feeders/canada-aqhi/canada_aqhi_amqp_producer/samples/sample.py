
"""
Sample usage of canada_aqhi_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from canada_aqhi_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = CaGcWeatherAqhiAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Community message
        print("Sending Community message...")
        # TODO: Create a Community instance with actual data
        # data = Community(...)
        # producer.send_community(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Community message sent successfully!")
        
        
        
        # Send Observation message
        print("Sending Observation message...")
        # TODO: Create a Observation instance with actual data
        # data = Observation(...)
        # producer.send_observation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Observation message sent successfully!")
        
        
        
        # Send Forecast message
        print("Sending Forecast message...")
        # TODO: Create a Forecast instance with actual data
        # data = Forecast(...)
        # producer.send_forecast(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Forecast message sent successfully!")
        
        
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