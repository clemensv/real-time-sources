
"""
Sample usage of bluesky_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from bluesky_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = BlueskyFirehoseAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Post message
        print("Sending Post message...")
        # TODO: Create a Post instance with actual data
        # data = Post(...)
        # producer.send_post(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Post message sent successfully!")
        
        
        
        # Send Like message
        print("Sending Like message...")
        # TODO: Create a Like instance with actual data
        # data = Like(...)
        # producer.send_like(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Like message sent successfully!")
        
        
        
        # Send Repost message
        print("Sending Repost message...")
        # TODO: Create a Repost instance with actual data
        # data = Repost(...)
        # producer.send_repost(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Repost message sent successfully!")
        
        
        
        # Send Follow message
        print("Sending Follow message...")
        # TODO: Create a Follow instance with actual data
        # data = Follow(...)
        # producer.send_follow(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Follow message sent successfully!")
        
        
        
        # Send Block message
        print("Sending Block message...")
        # TODO: Create a Block instance with actual data
        # data = Block(...)
        # producer.send_block(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Block message sent successfully!")
        
        
        
        # Send Profile message
        print("Sending Profile message...")
        # TODO: Create a Profile instance with actual data
        # data = Profile(...)
        # producer.send_profile(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Profile message sent successfully!")
        
        
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