
"""
Sample usage of mode_s_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from mode_s_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = ModeSAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send ADSB message
        print("Sending ADSB message...")
        # TODO: Create a Record instance with actual data
        # data = Record(...)
        # producer.send_adsb(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ADSB message sent successfully!")
        
        
        
        # Send AltitudeReply message
        print("Sending AltitudeReply message...")
        # TODO: Create a Record instance with actual data
        # data = Record(...)
        # producer.send_altitude_reply(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("AltitudeReply message sent successfully!")
        
        
        
        # Send IdentityReply message
        print("Sending IdentityReply message...")
        # TODO: Create a Record instance with actual data
        # data = Record(...)
        # producer.send_identity_reply(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("IdentityReply message sent successfully!")
        
        
        
        # Send AcquisitionReply message
        print("Sending AcquisitionReply message...")
        # TODO: Create a Record instance with actual data
        # data = Record(...)
        # producer.send_acquisition_reply(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("AcquisitionReply message sent successfully!")
        
        
        
        # Send CommBAltitude message
        print("Sending CommBAltitude message...")
        # TODO: Create a Record instance with actual data
        # data = Record(...)
        # producer.send_comm_baltitude(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("CommBAltitude message sent successfully!")
        
        
        
        # Send CommBIdentity message
        print("Sending CommBIdentity message...")
        # TODO: Create a Record instance with actual data
        # data = Record(...)
        # producer.send_comm_bidentity(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("CommBIdentity message sent successfully!")
        
        
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