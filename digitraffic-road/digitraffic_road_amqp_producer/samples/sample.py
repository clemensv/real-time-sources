
"""
Sample usage of digitraffic_road_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from digitraffic_road_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = FiDigitrafficRoadAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send TmsSensorData message
        print("Sending TmsSensorData message...")
        # TODO: Create a TmsSensorData instance with actual data
        # data = TmsSensorData(...)
        # producer.send_tms_sensor_data(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("TmsSensorData message sent successfully!")
        
        
        
        # Send WeatherSensorData message
        print("Sending WeatherSensorData message...")
        # TODO: Create a WeatherSensorData instance with actual data
        # data = WeatherSensorData(...)
        # producer.send_weather_sensor_data(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WeatherSensorData message sent successfully!")
        
        
        
        # Send TrafficAnnouncement message
        print("Sending TrafficAnnouncement message...")
        # TODO: Create a TrafficMessage instance with actual data
        # data = TrafficMessage(...)
        # producer.send_traffic_announcement(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("TrafficAnnouncement message sent successfully!")
        
        
        
        # Send RoadWork message
        print("Sending RoadWork message...")
        # TODO: Create a TrafficMessage instance with actual data
        # data = TrafficMessage(...)
        # producer.send_road_work(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("RoadWork message sent successfully!")
        
        
        
        # Send WeightRestriction message
        print("Sending WeightRestriction message...")
        # TODO: Create a TrafficMessage instance with actual data
        # data = TrafficMessage(...)
        # producer.send_weight_restriction(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WeightRestriction message sent successfully!")
        
        
        
        # Send ExemptedTransport message
        print("Sending ExemptedTransport message...")
        # TODO: Create a TrafficMessage instance with actual data
        # data = TrafficMessage(...)
        # producer.send_exempted_transport(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("ExemptedTransport message sent successfully!")
        
        
        
        # Send MaintenanceTracking message
        print("Sending MaintenanceTracking message...")
        # TODO: Create a MaintenanceTracking instance with actual data
        # data = MaintenanceTracking(...)
        # producer.send_maintenance_tracking(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("MaintenanceTracking message sent successfully!")
        
        
        
        # Send TmsStation message
        print("Sending TmsStation message...")
        # TODO: Create a TmsStation instance with actual data
        # data = TmsStation(...)
        # producer.send_tms_station(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("TmsStation message sent successfully!")
        
        
        
        # Send WeatherStation message
        print("Sending WeatherStation message...")
        # TODO: Create a WeatherStation instance with actual data
        # data = WeatherStation(...)
        # producer.send_weather_station(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("WeatherStation message sent successfully!")
        
        
        
        # Send MaintenanceTaskType message
        print("Sending MaintenanceTaskType message...")
        # TODO: Create a MaintenanceTaskType instance with actual data
        # data = MaintenanceTaskType(...)
        # producer.send_maintenance_task_type(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("MaintenanceTaskType message sent successfully!")
        
        
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