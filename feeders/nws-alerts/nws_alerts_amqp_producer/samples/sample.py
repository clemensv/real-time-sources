
"""
Sample usage of nws_alerts_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from nws_alerts_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = NWSAlertsAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send WeatherAlertMinor message
        print("Sending WeatherAlertMinor message...")
        # TODO: Create a WeatherAlert instance with actual data
        # data = WeatherAlert(...)
        # producer.send_weather_alert_minor(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WeatherAlertMinor message sent successfully!")
        
        
        
        # Send WeatherAlertModerate message
        print("Sending WeatherAlertModerate message...")
        # TODO: Create a WeatherAlert instance with actual data
        # data = WeatherAlert(...)
        # producer.send_weather_alert_moderate(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WeatherAlertModerate message sent successfully!")
        
        
        
        # Send WeatherAlertSevere message
        print("Sending WeatherAlertSevere message...")
        # TODO: Create a WeatherAlert instance with actual data
        # data = WeatherAlert(...)
        # producer.send_weather_alert_severe(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WeatherAlertSevere message sent successfully!")
        
        
        
        # Send WeatherAlertExtreme message
        print("Sending WeatherAlertExtreme message...")
        # TODO: Create a WeatherAlert instance with actual data
        # data = WeatherAlert(...)
        # producer.send_weather_alert_extreme(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WeatherAlertExtreme message sent successfully!")
        
        
        
        # Send WeatherAlertUnknown message
        print("Sending WeatherAlertUnknown message...")
        # TODO: Create a WeatherAlert instance with actual data
        # data = WeatherAlert(...)
        # producer.send_weather_alert_unknown(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WeatherAlertUnknown message sent successfully!")
        
        
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