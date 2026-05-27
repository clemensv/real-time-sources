
"""
Sample usage of noaa_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from noaa_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = MicrosoftOpenDataUSNOAAAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send WaterLevel message
        print("Sending WaterLevel message...")
        # TODO: Create a WaterLevel instance with actual data
        # data = WaterLevel(...)
        # producer.send_water_level(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WaterLevel message sent successfully!")
        
        
        
        # Send Predictions message
        print("Sending Predictions message...")
        # TODO: Create a Predictions instance with actual data
        # data = Predictions(...)
        # producer.send_predictions(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Predictions message sent successfully!")
        
        
        
        # Send AirPressure message
        print("Sending AirPressure message...")
        # TODO: Create a AirPressure instance with actual data
        # data = AirPressure(...)
        # producer.send_air_pressure(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("AirPressure message sent successfully!")
        
        
        
        # Send AirTemperature message
        print("Sending AirTemperature message...")
        # TODO: Create a AirTemperature instance with actual data
        # data = AirTemperature(...)
        # producer.send_air_temperature(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("AirTemperature message sent successfully!")
        
        
        
        # Send WaterTemperature message
        print("Sending WaterTemperature message...")
        # TODO: Create a WaterTemperature instance with actual data
        # data = WaterTemperature(...)
        # producer.send_water_temperature(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WaterTemperature message sent successfully!")
        
        
        
        # Send Wind message
        print("Sending Wind message...")
        # TODO: Create a Wind instance with actual data
        # data = Wind(...)
        # producer.send_wind(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Wind message sent successfully!")
        
        
        
        # Send Humidity message
        print("Sending Humidity message...")
        # TODO: Create a Humidity instance with actual data
        # data = Humidity(...)
        # producer.send_humidity(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Humidity message sent successfully!")
        
        
        
        # Send Conductivity message
        print("Sending Conductivity message...")
        # TODO: Create a Conductivity instance with actual data
        # data = Conductivity(...)
        # producer.send_conductivity(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Conductivity message sent successfully!")
        
        
        
        # Send Salinity message
        print("Sending Salinity message...")
        # TODO: Create a Salinity instance with actual data
        # data = Salinity(...)
        # producer.send_salinity(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Salinity message sent successfully!")
        
        
        
        # Send Station message
        print("Sending Station message...")
        # TODO: Create a Station instance with actual data
        # data = Station(...)
        # producer.send_station(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Station message sent successfully!")
        
        
        
        # Send Visibility message
        print("Sending Visibility message...")
        # TODO: Create a Visibility instance with actual data
        # data = Visibility(...)
        # producer.send_visibility(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Visibility message sent successfully!")
        
        
        
        # Send Currents message
        print("Sending Currents message...")
        # TODO: Create a Currents instance with actual data
        # data = Currents(...)
        # producer.send_currents(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Currents message sent successfully!")
        
        
        
        # Send CurrentPredictions message
        print("Sending CurrentPredictions message...")
        # TODO: Create a CurrentPredictions instance with actual data
        # data = CurrentPredictions(...)
        # producer.send_current_predictions(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("CurrentPredictions message sent successfully!")
        
        
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