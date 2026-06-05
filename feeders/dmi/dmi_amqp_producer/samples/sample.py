
"""
Sample usage of dmi_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from dmi_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = DkDmiMetObsAmqpProducer(
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
        # TODO: Create a MetObsStation instance with actual data
        # data = MetObsStation(...)
        # producer.send_station(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Station message sent successfully!")
        
        
        
        # Send Observation message
        print("Sending Observation message...")
        # TODO: Create a MetObsObservation instance with actual data
        # data = MetObsObservation(...)
        # producer.send_observation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Observation message sent successfully!")
        
        
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
    producer = DkDmiOceanObsAmqpProducer(
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
        # TODO: Create a OceanStation instance with actual data
        # data = OceanStation(...)
        # producer.send_station(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Station message sent successfully!")
        
        
        
        # Send TidewaterStation message
        print("Sending TidewaterStation message...")
        # TODO: Create a TidewaterStation instance with actual data
        # data = TidewaterStation(...)
        # producer.send_tidewater_station(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("TidewaterStation message sent successfully!")
        
        
        
        # Send Observation message
        print("Sending Observation message...")
        # TODO: Create a OceanObservation instance with actual data
        # data = OceanObservation(...)
        # producer.send_observation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Observation message sent successfully!")
        
        
        
        # Send TidewaterPrediction message
        print("Sending TidewaterPrediction message...")
        # TODO: Create a TidewaterPrediction instance with actual data
        # data = TidewaterPrediction(...)
        # producer.send_tidewater_prediction(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("TidewaterPrediction message sent successfully!")
        
        
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
    producer = DkDmiLightningAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Sensor message
        print("Sending Sensor message...")
        # TODO: Create a LightningSensor instance with actual data
        # data = LightningSensor(...)
        # producer.send_sensor(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Sensor message sent successfully!")
        
        
        
        # Send Strike message
        print("Sending Strike message...")
        # TODO: Create a LightningStrike instance with actual data
        # data = LightningStrike(...)
        # producer.send_strike(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Strike message sent successfully!")
        
        
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