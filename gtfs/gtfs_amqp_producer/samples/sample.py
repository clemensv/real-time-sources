
"""
Sample usage of gtfs_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from gtfs_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = GeneralTransitFeedRealTimeAmqpProducer(
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
        # TODO: Create a VehiclePosition instance with actual data
        # data = VehiclePosition(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a TripUpdate instance with actual data
        # data = TripUpdate(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Alert instance with actual data
        # data = Alert(...)
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
    producer = GeneralTransitFeedStaticAmqpProducer(
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
        # TODO: Create a Agency instance with actual data
        # data = Agency(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Areas instance with actual data
        # data = Areas(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Attributions instance with actual data
        # data = Attributions(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a BookingRules instance with actual data
        # data = BookingRules(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a FareAttributes instance with actual data
        # data = FareAttributes(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a FareLegRules instance with actual data
        # data = FareLegRules(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a FareMedia instance with actual data
        # data = FareMedia(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a FareProducts instance with actual data
        # data = FareProducts(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a FareRules instance with actual data
        # data = FareRules(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a FareTransferRules instance with actual data
        # data = FareTransferRules(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a FeedInfo instance with actual data
        # data = FeedInfo(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Frequencies instance with actual data
        # data = Frequencies(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Levels instance with actual data
        # data = Levels(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a LocationGeoJson instance with actual data
        # data = LocationGeoJson(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a LocationGroups instance with actual data
        # data = LocationGroups(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a LocationGroupStores instance with actual data
        # data = LocationGroupStores(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Networks instance with actual data
        # data = Networks(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Pathways instance with actual data
        # data = Pathways(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a RouteNetworks instance with actual data
        # data = RouteNetworks(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Routes instance with actual data
        # data = Routes(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Shapes instance with actual data
        # data = Shapes(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a StopAreas instance with actual data
        # data = StopAreas(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Stops instance with actual data
        # data = Stops(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a StopTimes instance with actual data
        # data = StopTimes(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Timeframes instance with actual data
        # data = Timeframes(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Transfers instance with actual data
        # data = Transfers(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Translations instance with actual data
        # data = Translations(...)
        # producer.send_amqp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Amqp message sent successfully!")
        
        
        
        # Send Amqp message
        print("Sending Amqp message...")
        # TODO: Create a Trips instance with actual data
        # data = Trips(...)
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