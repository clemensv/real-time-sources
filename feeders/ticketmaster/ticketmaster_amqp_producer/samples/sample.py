
"""
Sample usage of ticketmaster_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from ticketmaster_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = TicketmasterEventsAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Event message
        print("Sending Event message...")
        # TODO: Create a Event instance with actual data
        # data = Event(...)
        # producer.send_event(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Event message sent successfully!")
        
        
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
    producer = TicketmasterReferenceAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Venue message
        print("Sending Venue message...")
        # TODO: Create a Venue instance with actual data
        # data = Venue(...)
        # producer.send_venue(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Venue message sent successfully!")
        
        
        
        # Send Attraction message
        print("Sending Attraction message...")
        # TODO: Create a Attraction instance with actual data
        # data = Attraction(...)
        # producer.send_attraction(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Attraction message sent successfully!")
        
        
        
        # Send Classification message
        print("Sending Classification message...")
        # TODO: Create a Classification instance with actual data
        # data = Classification(...)
        # producer.send_classification(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Classification message sent successfully!")
        
        
        
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