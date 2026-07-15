
"""
Sample usage of open_charge_map_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from open_charge_map_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = IOOpenChargeMapLocationsAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send ChargingLocation message
        print("Sending ChargingLocation message...")
        # TODO: Create a ChargingLocation instance with actual data
        # data = ChargingLocation(...)
        # producer.send_charging_location(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ChargingLocation message sent successfully!")
        
        
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
    producer = IOOpenChargeMapReferenceAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Operator message
        print("Sending Operator message...")
        # TODO: Create a Operator instance with actual data
        # data = Operator(...)
        # producer.send_operator(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Operator message sent successfully!")
        
        
        
        # Send ConnectionType message
        print("Sending ConnectionType message...")
        # TODO: Create a ConnectionType instance with actual data
        # data = ConnectionType(...)
        # producer.send_connection_type(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ConnectionType message sent successfully!")
        
        
        
        # Send CurrentType message
        print("Sending CurrentType message...")
        # TODO: Create a CurrentType instance with actual data
        # data = CurrentType(...)
        # producer.send_current_type(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("CurrentType message sent successfully!")
        
        
        
        # Send ChargerType message
        print("Sending ChargerType message...")
        # TODO: Create a ChargerType instance with actual data
        # data = ChargerType(...)
        # producer.send_charger_type(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ChargerType message sent successfully!")
        
        
        
        # Send Country message
        print("Sending Country message...")
        # TODO: Create a Country instance with actual data
        # data = Country(...)
        # producer.send_country(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Country message sent successfully!")
        
        
        
        # Send DataProvider message
        print("Sending DataProvider message...")
        # TODO: Create a DataProvider instance with actual data
        # data = DataProvider(...)
        # producer.send_data_provider(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("DataProvider message sent successfully!")
        
        
        
        # Send StatusType message
        print("Sending StatusType message...")
        # TODO: Create a StatusType instance with actual data
        # data = StatusType(...)
        # producer.send_status_type(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("StatusType message sent successfully!")
        
        
        
        # Send UsageType message
        print("Sending UsageType message...")
        # TODO: Create a UsageType instance with actual data
        # data = UsageType(...)
        # producer.send_usage_type(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("UsageType message sent successfully!")
        
        
        
        # Send SubmissionStatusType message
        print("Sending SubmissionStatusType message...")
        # TODO: Create a SubmissionStatusType instance with actual data
        # data = SubmissionStatusType(...)
        # producer.send_submission_status_type(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("SubmissionStatusType message sent successfully!")
        
        
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