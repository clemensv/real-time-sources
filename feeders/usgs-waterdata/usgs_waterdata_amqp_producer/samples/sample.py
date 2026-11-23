
"""
Sample usage of usgs_waterdata_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from usgs_waterdata_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = USGSWaterDataAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send ContinuousObservation message
        print("Sending ContinuousObservation message...")
        # TODO: Create a ContinuousObservation instance with actual data
        # data = ContinuousObservation(...)
        # producer.send_continuous_observation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ContinuousObservation message sent successfully!")
        
        
        
        # Send TimeSeries message
        print("Sending TimeSeries message...")
        # TODO: Create a TimeSeries instance with actual data
        # data = TimeSeries(...)
        # producer.send_time_series(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("TimeSeries message sent successfully!")
        
        
        
        # Send MonitoringLocation message
        print("Sending MonitoringLocation message...")
        # TODO: Create a MonitoringLocation instance with actual data
        # data = MonitoringLocation(...)
        # producer.send_monitoring_location(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("MonitoringLocation message sent successfully!")
        
        
        
        # Send Parameter message
        print("Sending Parameter message...")
        # TODO: Create a Parameter instance with actual data
        # data = Parameter(...)
        # producer.send_parameter(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Parameter message sent successfully!")
        
        
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