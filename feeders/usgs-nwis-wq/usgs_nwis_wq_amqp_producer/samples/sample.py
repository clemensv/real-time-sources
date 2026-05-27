
"""
Sample usage of usgs_nwis_wq_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from usgs_nwis_wq_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = USGSWaterQualitySitesAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send MonitoringSite message
        print("Sending MonitoringSite message...")
        # TODO: Create a MonitoringSite instance with actual data
        # data = MonitoringSite(...)
        # producer.send_monitoring_site(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("MonitoringSite message sent successfully!")
        
        
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
    producer = USGSWaterQualityReadingsAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send WaterQualityReading message
        print("Sending WaterQualityReading message...")
        # TODO: Create a WaterQualityReading instance with actual data
        # data = WaterQualityReading(...)
        # producer.send_water_quality_reading(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WaterQualityReading message sent successfully!")
        
        
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