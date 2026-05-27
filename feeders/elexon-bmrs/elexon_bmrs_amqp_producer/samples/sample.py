
"""
Sample usage of elexon_bmrs_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from elexon_bmrs_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = UKCoElexonBMRSAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send GenerationMix message
        print("Sending GenerationMix message...")
        # TODO: Create a GenerationMix instance with actual data
        # data = GenerationMix(...)
        # producer.send_generation_mix(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("GenerationMix message sent successfully!")
        
        
        
        # Send DemandOutturn message
        print("Sending DemandOutturn message...")
        # TODO: Create a DemandOutturn instance with actual data
        # data = DemandOutturn(...)
        # producer.send_demand_outturn(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("DemandOutturn message sent successfully!")
        
        
        
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