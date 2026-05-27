
"""
Sample usage of luchtmeetnet_nl_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from luchtmeetnet_nl_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = NlRivmLuchtmeetnetAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Station message
        print("Sending Station message...")
        # TODO: Create a Station instance with actual data
        # data = Station(...)
        # producer.send_station(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Station message sent successfully!")
        
        
        
        # Send Measurement message
        print("Sending Measurement message...")
        # TODO: Create a Measurement instance with actual data
        # data = Measurement(...)
        # producer.send_measurement(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Measurement message sent successfully!")
        
        
        
        # Send LKI message
        print("Sending LKI message...")
        # TODO: Create a LKI instance with actual data
        # data = LKI(...)
        # producer.send_lki(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("LKI message sent successfully!")
        
        
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
    producer = NlRivmLuchtmeetnetComponentsAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Component message
        print("Sending Component message...")
        # TODO: Create a Component instance with actual data
        # data = Component(...)
        # producer.send_component(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Component message sent successfully!")
        
        
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