
"""
This is sample code to produce events to Apache Kafka with the producer clients
contained in this project. You will still need to supply event data in the
marked
placews below before the program can be run.

The script gets the configuration from the command line or uses the environment
variables. The following environment variables are recognized:

- KAFKA_PRODUCER_CONFIG: The Kafka producer configuration.
- KAFKA_TOPICS: The Kafka topics to send events to.
- FABRIC_CONNECTION_STRING: A Microsoft Fabric or Azure Event Hubs connection
string.

Alternatively, you can pass the configuration as command-line arguments.

- `--producer-config`: The Kafka producer configuration.
- `--topics`: The Kafka topics to send events to.
- `-c` or `--connection-string`: The Microsoft Fabric or Azure Event Hubs
connection string.
"""

import argparse
import os
import asyncio
import json
import uuid
from typing import Optional
from datetime import datetime
from confluent_kafka import Producer as KafkaProducer

# imports the producer clients for the message group(s)

from digitraffic_road_producer_kafka_producer.producer import FiDigitrafficRoadSensorsEventProducer
from digitraffic_road_producer_kafka_producer.producer import FiDigitrafficRoadMessagesEventProducer
from digitraffic_road_producer_kafka_producer.producer import FiDigitrafficRoadMaintenanceEventProducer
from digitraffic_road_producer_kafka_producer.producer import FiDigitrafficRoadStationsEventProducer
from digitraffic_road_producer_kafka_producer.producer import FiDigitrafficRoadMaintenanceTasksEventProducer

# imports for the data classes for each event

from digitraffic_road_producer_data.tmssensordata import TmsSensorData
from digitraffic_road_producer_data.weathersensordata import WeatherSensorData
from digitraffic_road_producer_data.trafficmessage import TrafficMessage
from digitraffic_road_producer_data.maintenancetracking import MaintenanceTracking
from digitraffic_road_producer_data.tmsstation import TmsStation
from digitraffic_road_producer_data.weatherstation import WeatherStation
from digitraffic_road_producer_data.maintenancetasktype import MaintenanceTaskType

async def main(connection_string: Optional[str], producer_config: Optional[str], topic: Optional[str]):
    """
    Main function to produce events to Apache Kafka

    Args:
        connection_string (Optional[str]): The Fabric connection string
        producer_config (Optional[str]): The Kafka producer configuration
        topic (Optional[str]): The Kafka topic to send events to
    """
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_digitraffic_road_sensors_event_producer = FiDigitrafficRoadSensorsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_digitraffic_road_sensors_event_producer = FiDigitrafficRoadSensorsEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.digitraffic.road.sensors.TmsSensorData ----
    # TODO: Supply event data for the fi.digitraffic.road.sensors.TmsSensorData event
    _tms_sensor_data = TmsSensorData()

    # sends the 'fi.digitraffic.road.sensors.TmsSensorData' event to Kafka topic.
    await fi_digitraffic_road_sensors_event_producer.send_fi_digitraffic_road_sensors_tms_sensor_data(_station_id = 'TODO: replace me', _sensor_id = 'TODO: replace me', data = _tms_sensor_data)
    print(f"Sent 'fi.digitraffic.road.sensors.TmsSensorData' event: {_tms_sensor_data.to_json()}")

    # ---- fi.digitraffic.road.sensors.WeatherSensorData ----
    # TODO: Supply event data for the fi.digitraffic.road.sensors.WeatherSensorData event
    _weather_sensor_data = WeatherSensorData()

    # sends the 'fi.digitraffic.road.sensors.WeatherSensorData' event to Kafka topic.
    await fi_digitraffic_road_sensors_event_producer.send_fi_digitraffic_road_sensors_weather_sensor_data(_station_id = 'TODO: replace me', _sensor_id = 'TODO: replace me', data = _weather_sensor_data)
    print(f"Sent 'fi.digitraffic.road.sensors.WeatherSensorData' event: {_weather_sensor_data.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_digitraffic_road_messages_event_producer = FiDigitrafficRoadMessagesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_digitraffic_road_messages_event_producer = FiDigitrafficRoadMessagesEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.digitraffic.road.messages.TrafficAnnouncement ----
    # TODO: Supply event data for the fi.digitraffic.road.messages.TrafficAnnouncement event
    _traffic_message = TrafficMessage()

    # sends the 'fi.digitraffic.road.messages.TrafficAnnouncement' event to Kafka topic.
    await fi_digitraffic_road_messages_event_producer.send_fi_digitraffic_road_messages_traffic_announcement(_situation_id = 'TODO: replace me', data = _traffic_message)
    print(f"Sent 'fi.digitraffic.road.messages.TrafficAnnouncement' event: {_traffic_message.to_json()}")

    # ---- fi.digitraffic.road.messages.RoadWork ----
    # TODO: Supply event data for the fi.digitraffic.road.messages.RoadWork event
    _traffic_message = TrafficMessage()

    # sends the 'fi.digitraffic.road.messages.RoadWork' event to Kafka topic.
    await fi_digitraffic_road_messages_event_producer.send_fi_digitraffic_road_messages_road_work(_situation_id = 'TODO: replace me', data = _traffic_message)
    print(f"Sent 'fi.digitraffic.road.messages.RoadWork' event: {_traffic_message.to_json()}")

    # ---- fi.digitraffic.road.messages.WeightRestriction ----
    # TODO: Supply event data for the fi.digitraffic.road.messages.WeightRestriction event
    _traffic_message = TrafficMessage()

    # sends the 'fi.digitraffic.road.messages.WeightRestriction' event to Kafka topic.
    await fi_digitraffic_road_messages_event_producer.send_fi_digitraffic_road_messages_weight_restriction(_situation_id = 'TODO: replace me', data = _traffic_message)
    print(f"Sent 'fi.digitraffic.road.messages.WeightRestriction' event: {_traffic_message.to_json()}")

    # ---- fi.digitraffic.road.messages.ExemptedTransport ----
    # TODO: Supply event data for the fi.digitraffic.road.messages.ExemptedTransport event
    _traffic_message = TrafficMessage()

    # sends the 'fi.digitraffic.road.messages.ExemptedTransport' event to Kafka topic.
    await fi_digitraffic_road_messages_event_producer.send_fi_digitraffic_road_messages_exempted_transport(_situation_id = 'TODO: replace me', data = _traffic_message)
    print(f"Sent 'fi.digitraffic.road.messages.ExemptedTransport' event: {_traffic_message.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_digitraffic_road_maintenance_event_producer = FiDigitrafficRoadMaintenanceEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_digitraffic_road_maintenance_event_producer = FiDigitrafficRoadMaintenanceEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.digitraffic.road.maintenance.MaintenanceTracking ----
    # TODO: Supply event data for the fi.digitraffic.road.maintenance.MaintenanceTracking event
    _maintenance_tracking = MaintenanceTracking()

    # sends the 'fi.digitraffic.road.maintenance.MaintenanceTracking' event to Kafka topic.
    await fi_digitraffic_road_maintenance_event_producer.send_fi_digitraffic_road_maintenance_maintenance_tracking(_domain = 'TODO: replace me', data = _maintenance_tracking)
    print(f"Sent 'fi.digitraffic.road.maintenance.MaintenanceTracking' event: {_maintenance_tracking.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_digitraffic_road_stations_event_producer = FiDigitrafficRoadStationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_digitraffic_road_stations_event_producer = FiDigitrafficRoadStationsEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.digitraffic.road.stations.TmsStation ----
    # TODO: Supply event data for the fi.digitraffic.road.stations.TmsStation event
    _tms_station = TmsStation()

    # sends the 'fi.digitraffic.road.stations.TmsStation' event to Kafka topic.
    await fi_digitraffic_road_stations_event_producer.send_fi_digitraffic_road_stations_tms_station(_station_id = 'TODO: replace me', data = _tms_station)
    print(f"Sent 'fi.digitraffic.road.stations.TmsStation' event: {_tms_station.to_json()}")

    # ---- fi.digitraffic.road.stations.WeatherStation ----
    # TODO: Supply event data for the fi.digitraffic.road.stations.WeatherStation event
    _weather_station = WeatherStation()

    # sends the 'fi.digitraffic.road.stations.WeatherStation' event to Kafka topic.
    await fi_digitraffic_road_stations_event_producer.send_fi_digitraffic_road_stations_weather_station(_station_id = 'TODO: replace me', data = _weather_station)
    print(f"Sent 'fi.digitraffic.road.stations.WeatherStation' event: {_weather_station.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_digitraffic_road_maintenance_tasks_event_producer = FiDigitrafficRoadMaintenanceTasksEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_digitraffic_road_maintenance_tasks_event_producer = FiDigitrafficRoadMaintenanceTasksEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.digitraffic.road.maintenance.tasks.MaintenanceTaskType ----
    # TODO: Supply event data for the fi.digitraffic.road.maintenance.tasks.MaintenanceTaskType event
    _maintenance_task_type = MaintenanceTaskType()

    # sends the 'fi.digitraffic.road.maintenance.tasks.MaintenanceTaskType' event to Kafka topic.
    await fi_digitraffic_road_maintenance_tasks_event_producer.send_fi_digitraffic_road_maintenance_tasks_maintenance_task_type(_task_id = 'TODO: replace me', data = _maintenance_task_type)
    print(f"Sent 'fi.digitraffic.road.maintenance.tasks.MaintenanceTaskType' event: {_maintenance_task_type.to_json()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer")
    parser.add_argument('--producer-config', default=os.getenv('KAFKA_PRODUCER_CONFIG'), help='Kafka producer config (JSON)', required=False)
    parser.add_argument('--topics', default=os.getenv('KAFKA_TOPICS'), help='Kafka topics to send events to', required=False)
    parser.add_argument('-c|--connection-string', dest='connection_string', default=os.getenv('FABRIC_CONNECTION_STRING'), help='Fabric connection string', required=False)

    args = parser.parse_args()

    asyncio.run(main(
        args.connection_string,
        args.producer_config,
        args.topics
    ))