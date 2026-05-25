
"""
Sample usage of entsoe_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from entsoe_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = EuEntsoeTransparencyByDomainAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send DayAheadPrices message
        print("Sending DayAheadPrices message...")
        # TODO: Create a DayAheadPrices instance with actual data
        # data = DayAheadPrices(...)
        # producer.send_day_ahead_prices(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("DayAheadPrices message sent successfully!")
        
        
        
        # Send ActualTotalLoad message
        print("Sending ActualTotalLoad message...")
        # TODO: Create a ActualTotalLoad instance with actual data
        # data = ActualTotalLoad(...)
        # producer.send_actual_total_load(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ActualTotalLoad message sent successfully!")
        
        
        
        # Send LoadForecastMargin message
        print("Sending LoadForecastMargin message...")
        # TODO: Create a LoadForecastMargin instance with actual data
        # data = LoadForecastMargin(...)
        # producer.send_load_forecast_margin(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("LoadForecastMargin message sent successfully!")
        
        
        
        # Send GenerationForecast message
        print("Sending GenerationForecast message...")
        # TODO: Create a GenerationForecast instance with actual data
        # data = GenerationForecast(...)
        # producer.send_generation_forecast(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("GenerationForecast message sent successfully!")
        
        
        
        # Send ReservoirFillingInformation message
        print("Sending ReservoirFillingInformation message...")
        # TODO: Create a ReservoirFillingInformation instance with actual data
        # data = ReservoirFillingInformation(...)
        # producer.send_reservoir_filling_information(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ReservoirFillingInformation message sent successfully!")
        
        
        
        # Send ActualGeneration message
        print("Sending ActualGeneration message...")
        # TODO: Create a ActualGeneration instance with actual data
        # data = ActualGeneration(...)
        # producer.send_actual_generation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ActualGeneration message sent successfully!")
        
        
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
    producer = EuEntsoeTransparencyByDomainPsrTypeAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send ActualGenerationPerType message
        print("Sending ActualGenerationPerType message...")
        # TODO: Create a ActualGenerationPerType instance with actual data
        # data = ActualGenerationPerType(...)
        # producer.send_actual_generation_per_type(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ActualGenerationPerType message sent successfully!")
        
        
        
        # Send WindSolarForecast message
        print("Sending WindSolarForecast message...")
        # TODO: Create a WindSolarForecast instance with actual data
        # data = WindSolarForecast(...)
        # producer.send_wind_solar_forecast(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WindSolarForecast message sent successfully!")
        
        
        
        # Send WindSolarGeneration message
        print("Sending WindSolarGeneration message...")
        # TODO: Create a WindSolarGeneration instance with actual data
        # data = WindSolarGeneration(...)
        # producer.send_wind_solar_generation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WindSolarGeneration message sent successfully!")
        
        
        
        # Send InstalledGenerationCapacityPerType message
        print("Sending InstalledGenerationCapacityPerType message...")
        # TODO: Create a InstalledGenerationCapacityPerType instance with actual data
        # data = InstalledGenerationCapacityPerType(...)
        # producer.send_installed_generation_capacity_per_type(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("InstalledGenerationCapacityPerType message sent successfully!")
        
        
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
    producer = EuEntsoeTransparencyCrossBorderAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send CrossBorderPhysicalFlows message
        print("Sending CrossBorderPhysicalFlows message...")
        # TODO: Create a CrossBorderPhysicalFlows instance with actual data
        # data = CrossBorderPhysicalFlows(...)
        # producer.send_cross_border_physical_flows(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("CrossBorderPhysicalFlows message sent successfully!")
        
        
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