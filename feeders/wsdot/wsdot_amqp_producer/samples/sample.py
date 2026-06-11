
"""
Sample usage of wsdot_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from wsdot_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = UsWaWsdotTrafficAmqpProducer(
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
        # TODO: Create a TrafficFlowStation instance with actual data
        # data = TrafficFlowStation(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a TrafficFlowReading instance with actual data
        # data = TrafficFlowReading(...)
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
    producer = UsWaWsdotTraveltimesAmqpProducer(
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
        # TODO: Create a TravelTimeRoute instance with actual data
        # data = TravelTimeRoute(...)
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
    producer = UsWaWsdotMountainpassAmqpProducer(
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
        # TODO: Create a MountainPassCondition instance with actual data
        # data = MountainPassCondition(...)
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
    producer = UsWaWsdotWeatherAmqpProducer(
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
        # TODO: Create a WeatherStation instance with actual data
        # data = WeatherStation(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a WeatherReading instance with actual data
        # data = WeatherReading(...)
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
    producer = UsWaWsdotTollsAmqpProducer(
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
        # TODO: Create a TollRate instance with actual data
        # data = TollRate(...)
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
    producer = UsWaWsdotCvrestrictionsAmqpProducer(
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
        # TODO: Create a CommercialVehicleRestriction instance with actual data
        # data = CommercialVehicleRestriction(...)
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
    producer = UsWaWsdotBorderAmqpProducer(
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
        # TODO: Create a BorderCrossing instance with actual data
        # data = BorderCrossing(...)
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
    producer = UsWaWsdotFerriesAmqpProducer(
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
        # TODO: Create a VesselLocation instance with actual data
        # data = VesselLocation(...)
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
    producer = UsWaWsdotRoadweatherAmqpProducer(
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
        # TODO: Create a RoadWeatherStation instance with actual data
        # data = RoadWeatherStation(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a RoadWeatherReading instance with actual data
        # data = RoadWeatherReading(...)
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
    producer = UsWaWsdotAlertsAmqpProducer(
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
        # TODO: Create a HighwayAlert instance with actual data
        # data = HighwayAlert(...)
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
    producer = UsWaWsdotCamerasAmqpProducer(
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
        # TODO: Create a HighwayCamera instance with actual data
        # data = HighwayCamera(...)
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
    producer = UsWaWsdotBridgeclearancesAmqpProducer(
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
        # TODO: Create a BridgeClearance instance with actual data
        # data = BridgeClearance(...)
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
    producer = UsWaWsdotFerryterminalsAmqpProducer(
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
        # TODO: Create a TerminalSailingSpace instance with actual data
        # data = TerminalSailingSpace(...)
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