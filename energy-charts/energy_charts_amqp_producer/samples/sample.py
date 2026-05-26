
"""
Sample usage of energy_charts_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from energy_charts_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = InfoEnergyChartsAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send PublicPower message
        print("Sending PublicPower message...")
        # TODO: Create a PublicPower instance with actual data
        # data = PublicPower(...)
        # producer.send_public_power(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("PublicPower message sent successfully!")
        
        
        
        # Send SpotPrice message
        print("Sending SpotPrice message...")
        # TODO: Create a SpotPrice instance with actual data
        # data = SpotPrice(...)
        # producer.send_spot_price(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("SpotPrice message sent successfully!")
        
        
        
        # Send GridSignal message
        print("Sending GridSignal message...")
        # TODO: Create a GridSignal instance with actual data
        # data = GridSignal(...)
        # producer.send_grid_signal(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("GridSignal message sent successfully!")
        
        
        
        # Send Info message
        print("Sending Info message...")
        # TODO: Create a Info instance with actual data
        # data = Info(...)
        # producer.send_info(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Info message sent successfully!")
        
        
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