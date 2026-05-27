
"""
Sample usage of usgs_iv_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from usgs_iv_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = USGSSitesAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Site message
        print("Sending Site message...")
        # TODO: Create a Site instance with actual data
        # data = Site(...)
        # producer.send_site(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Site message sent successfully!")
        
        
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
    producer = USGSSiteTimeseriesAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send SiteTimeseries message
        print("Sending SiteTimeseries message...")
        # TODO: Create a SiteTimeseries instance with actual data
        # data = SiteTimeseries(...)
        # producer.send_site_timeseries(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("SiteTimeseries message sent successfully!")
        
        
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
    producer = USGSInstantaneousValuesAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send OtherParameter message
        print("Sending OtherParameter message...")
        # TODO: Create a OtherParameter instance with actual data
        # data = OtherParameter(...)
        # producer.send_other_parameter(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("OtherParameter message sent successfully!")
        
        
        
        # Send Precipitation message
        print("Sending Precipitation message...")
        # TODO: Create a Precipitation instance with actual data
        # data = Precipitation(...)
        # producer.send_precipitation(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Precipitation message sent successfully!")
        
        
        
        # Send Streamflow message
        print("Sending Streamflow message...")
        # TODO: Create a Streamflow instance with actual data
        # data = Streamflow(...)
        # producer.send_streamflow(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Streamflow message sent successfully!")
        
        
        
        # Send GageHeight message
        print("Sending GageHeight message...")
        # TODO: Create a GageHeight instance with actual data
        # data = GageHeight(...)
        # producer.send_gage_height(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("GageHeight message sent successfully!")
        
        
        
        # Send WaterTemperature message
        print("Sending WaterTemperature message...")
        # TODO: Create a WaterTemperature instance with actual data
        # data = WaterTemperature(...)
        # producer.send_water_temperature(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WaterTemperature message sent successfully!")
        
        
        
        # Send DissolvedOxygen message
        print("Sending DissolvedOxygen message...")
        # TODO: Create a DissolvedOxygen instance with actual data
        # data = DissolvedOxygen(...)
        # producer.send_dissolved_oxygen(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("DissolvedOxygen message sent successfully!")
        
        
        
        # Send PH message
        print("Sending PH message...")
        # TODO: Create a PH instance with actual data
        # data = PH(...)
        # producer.send_ph(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("PH message sent successfully!")
        
        
        
        # Send SpecificConductance message
        print("Sending SpecificConductance message...")
        # TODO: Create a SpecificConductance instance with actual data
        # data = SpecificConductance(...)
        # producer.send_specific_conductance(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("SpecificConductance message sent successfully!")
        
        
        
        # Send Turbidity message
        print("Sending Turbidity message...")
        # TODO: Create a Turbidity instance with actual data
        # data = Turbidity(...)
        # producer.send_turbidity(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Turbidity message sent successfully!")
        
        
        
        # Send AirTemperature message
        print("Sending AirTemperature message...")
        # TODO: Create a AirTemperature instance with actual data
        # data = AirTemperature(...)
        # producer.send_air_temperature(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("AirTemperature message sent successfully!")
        
        
        
        # Send WindSpeed message
        print("Sending WindSpeed message...")
        # TODO: Create a WindSpeed instance with actual data
        # data = WindSpeed(...)
        # producer.send_wind_speed(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WindSpeed message sent successfully!")
        
        
        
        # Send WindDirection message
        print("Sending WindDirection message...")
        # TODO: Create a WindDirection instance with actual data
        # data = WindDirection(...)
        # producer.send_wind_direction(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WindDirection message sent successfully!")
        
        
        
        # Send RelativeHumidity message
        print("Sending RelativeHumidity message...")
        # TODO: Create a RelativeHumidity instance with actual data
        # data = RelativeHumidity(...)
        # producer.send_relative_humidity(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RelativeHumidity message sent successfully!")
        
        
        
        # Send BarometricPressure message
        print("Sending BarometricPressure message...")
        # TODO: Create a BarometricPressure instance with actual data
        # data = BarometricPressure(...)
        # producer.send_barometric_pressure(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("BarometricPressure message sent successfully!")
        
        
        
        # Send TurbidityFNU message
        print("Sending TurbidityFNU message...")
        # TODO: Create a TurbidityFNU instance with actual data
        # data = TurbidityFNU(...)
        # producer.send_turbidity_fnu(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("TurbidityFNU message sent successfully!")
        
        
        
        # Send FDOM message
        print("Sending FDOM message...")
        # TODO: Create a FDOM instance with actual data
        # data = FDOM(...)
        # producer.send_fdom(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("FDOM message sent successfully!")
        
        
        
        # Send ReservoirStorage message
        print("Sending ReservoirStorage message...")
        # TODO: Create a ReservoirStorage instance with actual data
        # data = ReservoirStorage(...)
        # producer.send_reservoir_storage(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ReservoirStorage message sent successfully!")
        
        
        
        # Send LakeElevationNGVD29 message
        print("Sending LakeElevationNGVD29 message...")
        # TODO: Create a LakeElevationNGVD29 instance with actual data
        # data = LakeElevationNGVD29(...)
        # producer.send_lake_elevation_ngvd29(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("LakeElevationNGVD29 message sent successfully!")
        
        
        
        # Send WaterDepth message
        print("Sending WaterDepth message...")
        # TODO: Create a WaterDepth instance with actual data
        # data = WaterDepth(...)
        # producer.send_water_depth(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WaterDepth message sent successfully!")
        
        
        
        # Send EquipmentStatus message
        print("Sending EquipmentStatus message...")
        # TODO: Create a EquipmentStatus instance with actual data
        # data = EquipmentStatus(...)
        # producer.send_equipment_status(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("EquipmentStatus message sent successfully!")
        
        
        
        # Send TidallyFilteredDischarge message
        print("Sending TidallyFilteredDischarge message...")
        # TODO: Create a TidallyFilteredDischarge instance with actual data
        # data = TidallyFilteredDischarge(...)
        # producer.send_tidally_filtered_discharge(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("TidallyFilteredDischarge message sent successfully!")
        
        
        
        # Send WaterVelocity message
        print("Sending WaterVelocity message...")
        # TODO: Create a WaterVelocity instance with actual data
        # data = WaterVelocity(...)
        # producer.send_water_velocity(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WaterVelocity message sent successfully!")
        
        
        
        # Send EstuaryElevationNGVD29 message
        print("Sending EstuaryElevationNGVD29 message...")
        # TODO: Create a EstuaryElevationNGVD29 instance with actual data
        # data = EstuaryElevationNGVD29(...)
        # producer.send_estuary_elevation_ngvd29(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("EstuaryElevationNGVD29 message sent successfully!")
        
        
        
        # Send LakeElevationNAVD88 message
        print("Sending LakeElevationNAVD88 message...")
        # TODO: Create a LakeElevationNAVD88 instance with actual data
        # data = LakeElevationNAVD88(...)
        # producer.send_lake_elevation_navd88(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("LakeElevationNAVD88 message sent successfully!")
        
        
        
        # Send Salinity message
        print("Sending Salinity message...")
        # TODO: Create a Salinity instance with actual data
        # data = Salinity(...)
        # producer.send_salinity(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Salinity message sent successfully!")
        
        
        
        # Send GateOpening message
        print("Sending GateOpening message...")
        # TODO: Create a GateOpening instance with actual data
        # data = GateOpening(...)
        # producer.send_gate_opening(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("GateOpening message sent successfully!")
        
        
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