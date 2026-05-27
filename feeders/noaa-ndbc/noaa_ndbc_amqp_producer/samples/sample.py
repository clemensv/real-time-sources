
"""
Sample usage of noaa_ndbc_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from noaa_ndbc_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = MicrosoftOpenDataUSNOAANDBCAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send BuoyObservation message
        print("Sending BuoyObservation message...")
        # TODO: Create a BuoyObservation instance with actual data
        # data = BuoyObservation(...)
        # producer.send_buoy_observation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("BuoyObservation message sent successfully!")
        
        
        
        # Send BuoyStation message
        print("Sending BuoyStation message...")
        # TODO: Create a BuoyStation instance with actual data
        # data = BuoyStation(...)
        # producer.send_buoy_station(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("BuoyStation message sent successfully!")
        
        
        
        # Send BuoySolarRadiationObservation message
        print("Sending BuoySolarRadiationObservation message...")
        # TODO: Create a BuoySolarRadiationObservation instance with actual data
        # data = BuoySolarRadiationObservation(...)
        # producer.send_buoy_solar_radiation_observation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("BuoySolarRadiationObservation message sent successfully!")
        
        
        
        # Send BuoyOceanographicObservation message
        print("Sending BuoyOceanographicObservation message...")
        # TODO: Create a BuoyOceanographicObservation instance with actual data
        # data = BuoyOceanographicObservation(...)
        # producer.send_buoy_oceanographic_observation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("BuoyOceanographicObservation message sent successfully!")
        
        
        
        # Send BuoyDartMeasurement message
        print("Sending BuoyDartMeasurement message...")
        # TODO: Create a BuoyDartMeasurement instance with actual data
        # data = BuoyDartMeasurement(...)
        # producer.send_buoy_dart_measurement(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("BuoyDartMeasurement message sent successfully!")
        
        
        
        # Send BuoyContinuousWindObservation message
        print("Sending BuoyContinuousWindObservation message...")
        # TODO: Create a BuoyContinuousWindObservation instance with actual data
        # data = BuoyContinuousWindObservation(...)
        # producer.send_buoy_continuous_wind_observation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("BuoyContinuousWindObservation message sent successfully!")
        
        
        
        # Send BuoySupplementalMeasurement message
        print("Sending BuoySupplementalMeasurement message...")
        # TODO: Create a BuoySupplementalMeasurement instance with actual data
        # data = BuoySupplementalMeasurement(...)
        # producer.send_buoy_supplemental_measurement(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("BuoySupplementalMeasurement message sent successfully!")
        
        
        
        # Send BuoyDetailedWaveSummary message
        print("Sending BuoyDetailedWaveSummary message...")
        # TODO: Create a BuoyDetailedWaveSummary instance with actual data
        # data = BuoyDetailedWaveSummary(...)
        # producer.send_buoy_detailed_wave_summary(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("BuoyDetailedWaveSummary message sent successfully!")
        
        
        
        # Send BuoyHourlyRainMeasurement message
        print("Sending BuoyHourlyRainMeasurement message...")
        # TODO: Create a BuoyHourlyRainMeasurement instance with actual data
        # data = BuoyHourlyRainMeasurement(...)
        # producer.send_buoy_hourly_rain_measurement(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("BuoyHourlyRainMeasurement message sent successfully!")
        
        
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