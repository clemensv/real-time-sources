
"""
Sample usage of ndw_road_traffic_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from ndw_road_traffic_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = NLNDWAVGAmqpProducer(
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
        # TODO: Create a PointMeasurementSite instance with actual data
        # data = PointMeasurementSite(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a RouteMeasurementSite instance with actual data
        # data = RouteMeasurementSite(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a TrafficObservation instance with actual data
        # data = TrafficObservation(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a TravelTimeObservation instance with actual data
        # data = TravelTimeObservation(...)
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
    producer = NLNDWDRIPAmqpProducer(
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
        # TODO: Create a DripSign instance with actual data
        # data = DripSign(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a DripDisplayState instance with actual data
        # data = DripDisplayState(...)
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
    producer = NLNDWMSIAmqpProducer(
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
        # TODO: Create a MsiSign instance with actual data
        # data = MsiSign(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a MsiDisplayState instance with actual data
        # data = MsiDisplayState(...)
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
    producer = NLNDWSituationsAmqpProducer(
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
        # TODO: Create a Roadwork instance with actual data
        # data = Roadwork(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a BridgeOpening instance with actual data
        # data = BridgeOpening(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a TemporaryClosure instance with actual data
        # data = TemporaryClosure(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a TemporarySpeedLimit instance with actual data
        # data = TemporarySpeedLimit(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a SafetyRelatedMessage instance with actual data
        # data = SafetyRelatedMessage(...)
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