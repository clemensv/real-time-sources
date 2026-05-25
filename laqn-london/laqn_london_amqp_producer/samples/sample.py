
"""
Sample usage of laqn_london_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from laqn_london_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = UkKclLaqnAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Site message
        print("Sending Site message...")
        # TODO: Create a Site instance with actual data
        # data = Site(...)
        # producer.send_site(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Site message sent successfully!")
        
        
        
        # Send Measurement message
        print("Sending Measurement message...")
        # TODO: Create a Measurement instance with actual data
        # data = Measurement(...)
        # producer.send_measurement(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Measurement message sent successfully!")
        
        
        
        # Send DailyIndex message
        print("Sending DailyIndex message...")
        # TODO: Create a DailyIndex instance with actual data
        # data = DailyIndex(...)
        # producer.send_daily_index(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("DailyIndex message sent successfully!")
        
        
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
    producer = UkKclLaqnSpeciesAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Species message
        print("Sending Species message...")
        # TODO: Create a Species instance with actual data
        # data = Species(...)
        # producer.send_species(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Species message sent successfully!")
        
        
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