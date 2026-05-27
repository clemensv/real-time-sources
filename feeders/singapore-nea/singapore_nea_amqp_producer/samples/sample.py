
"""
Sample usage of singapore_nea_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from singapore_nea_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = SGGovNEAWeatherAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Station instance with actual data
        # data = Station(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a WeatherObservation instance with actual data
        # data = WeatherObservation(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
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
    producer = SGGovNEAAirQualityAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Region instance with actual data
        # data = Region(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a PSIReading instance with actual data
        # data = PSIReading(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a PM25Reading instance with actual data
        # data = PM25Reading(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
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