
"""
Sample usage of epa_uv_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from epa_uv_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = USEPAUVIndexAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send HourlyForecast message
        print("Sending HourlyForecast message...")
        # TODO: Create a HourlyForecast instance with actual data
        # data = HourlyForecast(...)
        # producer.send_hourly_forecast(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("HourlyForecast message sent successfully!")
        
        
        
        # Send DailyForecast message
        print("Sending DailyForecast message...")
        # TODO: Create a DailyForecast instance with actual data
        # data = DailyForecast(...)
        # producer.send_daily_forecast(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("DailyForecast message sent successfully!")
        
        
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