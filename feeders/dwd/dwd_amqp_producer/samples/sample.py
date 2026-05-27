
"""
Sample usage of dwd_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from dwd_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = DEDWDCDCAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send StationMetadata message
        print("Sending StationMetadata message...")
        # TODO: Create a StationMetadata instance with actual data
        # data = StationMetadata(...)
        # producer.send_station_metadata(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("StationMetadata message sent successfully!")
        
        
        
        # Send AirTemperature10Min message
        print("Sending AirTemperature10Min message...")
        # TODO: Create a AirTemperature10Min instance with actual data
        # data = AirTemperature10Min(...)
        # producer.send_air_temperature10_min(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("AirTemperature10Min message sent successfully!")
        
        
        
        # Send Precipitation10Min message
        print("Sending Precipitation10Min message...")
        # TODO: Create a Precipitation10Min instance with actual data
        # data = Precipitation10Min(...)
        # producer.send_precipitation10_min(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Precipitation10Min message sent successfully!")
        
        
        
        # Send Wind10Min message
        print("Sending Wind10Min message...")
        # TODO: Create a Wind10Min instance with actual data
        # data = Wind10Min(...)
        # producer.send_wind10_min(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Wind10Min message sent successfully!")
        
        
        
        # Send Solar10Min message
        print("Sending Solar10Min message...")
        # TODO: Create a Solar10Min instance with actual data
        # data = Solar10Min(...)
        # producer.send_solar10_min(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Solar10Min message sent successfully!")
        
        
        
        # Send HourlyObservation message
        print("Sending HourlyObservation message...")
        # TODO: Create a HourlyObservation instance with actual data
        # data = HourlyObservation(...)
        # producer.send_hourly_observation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("HourlyObservation message sent successfully!")
        
        
        
        # Send ExtremeWind10Min message
        print("Sending ExtremeWind10Min message...")
        # TODO: Create a ExtremeWind10Min instance with actual data
        # data = ExtremeWind10Min(...)
        # producer.send_extreme_wind10_min(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ExtremeWind10Min message sent successfully!")
        
        
        
        # Send ExtremeTemperature10Min message
        print("Sending ExtremeTemperature10Min message...")
        # TODO: Create a ExtremeTemperature10Min instance with actual data
        # data = ExtremeTemperature10Min(...)
        # producer.send_extreme_temperature10_min(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ExtremeTemperature10Min message sent successfully!")
        
        
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
    producer = DEDWDWeatherAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Alert message
        print("Sending Alert message...")
        # TODO: Create a Alert instance with actual data
        # data = Alert(...)
        # producer.send_alert(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Alert message sent successfully!")
        
        
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
    producer = DEDWDRadarAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send RadarProductCatalog message
        print("Sending RadarProductCatalog message...")
        # TODO: Create a RadarProductCatalog instance with actual data
        # data = RadarProductCatalog(...)
        # producer.send_radar_product_catalog(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RadarProductCatalog message sent successfully!")
        
        
        
        # Send RadarFileProduct message
        print("Sending RadarFileProduct message...")
        # TODO: Create a RadarFileProduct instance with actual data
        # data = RadarFileProduct(...)
        # producer.send_radar_file_product(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RadarFileProduct message sent successfully!")
        
        
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
    producer = DEDWDForecastAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send ForecastModelCatalog message
        print("Sending ForecastModelCatalog message...")
        # TODO: Create a ForecastModelCatalog instance with actual data
        # data = ForecastModelCatalog(...)
        # producer.send_forecast_model_catalog(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ForecastModelCatalog message sent successfully!")
        
        
        
        # Send IconD2ForecastFile message
        print("Sending IconD2ForecastFile message...")
        # TODO: Create a IconD2ForecastFile instance with actual data
        # data = IconD2ForecastFile(...)
        # producer.send_icon_d2_forecast_file(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("IconD2ForecastFile message sent successfully!")
        
        
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