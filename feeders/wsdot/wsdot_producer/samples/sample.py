
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

from wsdot_producer_kafka_producer.producer import UsWaWsdotTrafficEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotTraveltimesEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotMountainpassEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotWeatherEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotTollsEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotCvrestrictionsEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotBorderEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotFerriesEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotTrafficMqttEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotTraveltimesMqttEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotMountainpassMqttEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotWeatherMqttEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotTollsMqttEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotCvrestrictionsMqttEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotBorderMqttEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotFerriesMqttEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotTrafficAmqpEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotTraveltimesAmqpEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotMountainpassAmqpEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotWeatherAmqpEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotTollsAmqpEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotCvrestrictionsAmqpEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotBorderAmqpEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotFerriesAmqpEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotRoadweatherEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotAlertsEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotCamerasEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotBridgeclearancesEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotFerryterminalsEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotRoadweatherMqttEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotAlertsMqttEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotCamerasMqttEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotBridgeclearancesMqttEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotFerryterminalsMqttEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotRoadweatherAmqpEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotAlertsAmqpEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotCamerasAmqpEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotBridgeclearancesAmqpEventProducer
from wsdot_producer_kafka_producer.producer import UsWaWsdotFerryterminalsAmqpEventProducer

# imports for the data classes for each event

from wsdot_producer_data import TrafficFlowStation
from wsdot_producer_data import TrafficFlowReading
from wsdot_producer_data import TravelTimeRoute
from wsdot_producer_data import MountainPassCondition
from wsdot_producer_data import WeatherStation
from wsdot_producer_data import WeatherReading
from wsdot_producer_data import TollRate
from wsdot_producer_data import CommercialVehicleRestriction
from wsdot_producer_data import BorderCrossing
from wsdot_producer_data import VesselLocation
from wsdot_producer_data import RoadWeatherStation
from wsdot_producer_data import RoadWeatherReading
from wsdot_producer_data import HighwayAlert
from wsdot_producer_data import HighwayCamera
from wsdot_producer_data import BridgeClearance
from wsdot_producer_data import TerminalSailingSpace

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
        us_wa_wsdot_traffic_event_producer = UsWaWsdotTrafficEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_traffic_event_producer = UsWaWsdotTrafficEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.traffic.TrafficFlowStation ----
    # TODO: Supply event data for the us.wa.wsdot.traffic.TrafficFlowStation event
    _traffic_flow_station = TrafficFlowStation()

    # sends the 'us.wa.wsdot.traffic.TrafficFlowStation' event to Kafka topic.
    await us_wa_wsdot_traffic_event_producer.send_us_wa_wsdot_traffic_traffic_flow_station(_feedurl = 'TODO: replace me', _flow_data_id = 'TODO: replace me', data = _traffic_flow_station)
    print(f"Sent 'us.wa.wsdot.traffic.TrafficFlowStation' event: {_traffic_flow_station.to_json()}")

    # ---- us.wa.wsdot.traffic.TrafficFlowReading ----
    # TODO: Supply event data for the us.wa.wsdot.traffic.TrafficFlowReading event
    _traffic_flow_reading = TrafficFlowReading()

    # sends the 'us.wa.wsdot.traffic.TrafficFlowReading' event to Kafka topic.
    await us_wa_wsdot_traffic_event_producer.send_us_wa_wsdot_traffic_traffic_flow_reading(_feedurl = 'TODO: replace me', _flow_data_id = 'TODO: replace me', data = _traffic_flow_reading)
    print(f"Sent 'us.wa.wsdot.traffic.TrafficFlowReading' event: {_traffic_flow_reading.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_traveltimes_event_producer = UsWaWsdotTraveltimesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_traveltimes_event_producer = UsWaWsdotTraveltimesEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.traveltimes.TravelTimeRoute ----
    # TODO: Supply event data for the us.wa.wsdot.traveltimes.TravelTimeRoute event
    _travel_time_route = TravelTimeRoute()

    # sends the 'us.wa.wsdot.traveltimes.TravelTimeRoute' event to Kafka topic.
    await us_wa_wsdot_traveltimes_event_producer.send_us_wa_wsdot_traveltimes_travel_time_route(_feedurl = 'TODO: replace me', _travel_time_id = 'TODO: replace me', data = _travel_time_route)
    print(f"Sent 'us.wa.wsdot.traveltimes.TravelTimeRoute' event: {_travel_time_route.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_mountainpass_event_producer = UsWaWsdotMountainpassEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_mountainpass_event_producer = UsWaWsdotMountainpassEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.mountainpass.MountainPassCondition ----
    # TODO: Supply event data for the us.wa.wsdot.mountainpass.MountainPassCondition event
    _mountain_pass_condition = MountainPassCondition()

    # sends the 'us.wa.wsdot.mountainpass.MountainPassCondition' event to Kafka topic.
    await us_wa_wsdot_mountainpass_event_producer.send_us_wa_wsdot_mountainpass_mountain_pass_condition(_feedurl = 'TODO: replace me', _mountain_pass_id = 'TODO: replace me', data = _mountain_pass_condition)
    print(f"Sent 'us.wa.wsdot.mountainpass.MountainPassCondition' event: {_mountain_pass_condition.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_weather_event_producer = UsWaWsdotWeatherEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_weather_event_producer = UsWaWsdotWeatherEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.weather.WeatherStation ----
    # TODO: Supply event data for the us.wa.wsdot.weather.WeatherStation event
    _weather_station = WeatherStation()

    # sends the 'us.wa.wsdot.weather.WeatherStation' event to Kafka topic.
    await us_wa_wsdot_weather_event_producer.send_us_wa_wsdot_weather_weather_station(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _weather_station)
    print(f"Sent 'us.wa.wsdot.weather.WeatherStation' event: {_weather_station.to_json()}")

    # ---- us.wa.wsdot.weather.WeatherReading ----
    # TODO: Supply event data for the us.wa.wsdot.weather.WeatherReading event
    _weather_reading = WeatherReading()

    # sends the 'us.wa.wsdot.weather.WeatherReading' event to Kafka topic.
    await us_wa_wsdot_weather_event_producer.send_us_wa_wsdot_weather_weather_reading(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _weather_reading)
    print(f"Sent 'us.wa.wsdot.weather.WeatherReading' event: {_weather_reading.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_tolls_event_producer = UsWaWsdotTollsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_tolls_event_producer = UsWaWsdotTollsEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.tolls.TollRate ----
    # TODO: Supply event data for the us.wa.wsdot.tolls.TollRate event
    _toll_rate = TollRate()

    # sends the 'us.wa.wsdot.tolls.TollRate' event to Kafka topic.
    await us_wa_wsdot_tolls_event_producer.send_us_wa_wsdot_tolls_toll_rate(_feedurl = 'TODO: replace me', _trip_name = 'TODO: replace me', data = _toll_rate)
    print(f"Sent 'us.wa.wsdot.tolls.TollRate' event: {_toll_rate.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_cvrestrictions_event_producer = UsWaWsdotCvrestrictionsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_cvrestrictions_event_producer = UsWaWsdotCvrestrictionsEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction ----
    # TODO: Supply event data for the us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction event
    _commercial_vehicle_restriction = CommercialVehicleRestriction()

    # sends the 'us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction' event to Kafka topic.
    await us_wa_wsdot_cvrestrictions_event_producer.send_us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction(_feedurl = 'TODO: replace me', _state_route_id = 'TODO: replace me', _bridge_number = 'TODO: replace me', data = _commercial_vehicle_restriction)
    print(f"Sent 'us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction' event: {_commercial_vehicle_restriction.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_border_event_producer = UsWaWsdotBorderEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_border_event_producer = UsWaWsdotBorderEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.border.BorderCrossing ----
    # TODO: Supply event data for the us.wa.wsdot.border.BorderCrossing event
    _border_crossing = BorderCrossing()

    # sends the 'us.wa.wsdot.border.BorderCrossing' event to Kafka topic.
    await us_wa_wsdot_border_event_producer.send_us_wa_wsdot_border_border_crossing(_feedurl = 'TODO: replace me', _crossing_name = 'TODO: replace me', data = _border_crossing)
    print(f"Sent 'us.wa.wsdot.border.BorderCrossing' event: {_border_crossing.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_ferries_event_producer = UsWaWsdotFerriesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_ferries_event_producer = UsWaWsdotFerriesEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.ferries.VesselLocation ----
    # TODO: Supply event data for the us.wa.wsdot.ferries.VesselLocation event
    _vessel_location = VesselLocation()

    # sends the 'us.wa.wsdot.ferries.VesselLocation' event to Kafka topic.
    await us_wa_wsdot_ferries_event_producer.send_us_wa_wsdot_ferries_vessel_location(_feedurl = 'TODO: replace me', _vessel_id = 'TODO: replace me', data = _vessel_location)
    print(f"Sent 'us.wa.wsdot.ferries.VesselLocation' event: {_vessel_location.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_traffic_mqtt_event_producer = UsWaWsdotTrafficMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_traffic_mqtt_event_producer = UsWaWsdotTrafficMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.traffic.TrafficFlowStation.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.traffic.TrafficFlowStation.mqtt event
    _traffic_flow_station = TrafficFlowStation()

    # sends the 'us.wa.wsdot.traffic.TrafficFlowStation.mqtt' event to Kafka topic.
    await us_wa_wsdot_traffic_mqtt_event_producer.send_us_wa_wsdot_traffic_traffic_flow_station_mqtt(_feedurl = 'TODO: replace me', _flow_data_id = 'TODO: replace me', data = _traffic_flow_station)
    print(f"Sent 'us.wa.wsdot.traffic.TrafficFlowStation.mqtt' event: {_traffic_flow_station.to_json()}")

    # ---- us.wa.wsdot.traffic.TrafficFlowReading.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.traffic.TrafficFlowReading.mqtt event
    _traffic_flow_reading = TrafficFlowReading()

    # sends the 'us.wa.wsdot.traffic.TrafficFlowReading.mqtt' event to Kafka topic.
    await us_wa_wsdot_traffic_mqtt_event_producer.send_us_wa_wsdot_traffic_traffic_flow_reading_mqtt(_feedurl = 'TODO: replace me', _flow_data_id = 'TODO: replace me', data = _traffic_flow_reading)
    print(f"Sent 'us.wa.wsdot.traffic.TrafficFlowReading.mqtt' event: {_traffic_flow_reading.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_traveltimes_mqtt_event_producer = UsWaWsdotTraveltimesMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_traveltimes_mqtt_event_producer = UsWaWsdotTraveltimesMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.traveltimes.TravelTimeRoute.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.traveltimes.TravelTimeRoute.mqtt event
    _travel_time_route = TravelTimeRoute()

    # sends the 'us.wa.wsdot.traveltimes.TravelTimeRoute.mqtt' event to Kafka topic.
    await us_wa_wsdot_traveltimes_mqtt_event_producer.send_us_wa_wsdot_traveltimes_travel_time_route_mqtt(_feedurl = 'TODO: replace me', _travel_time_id = 'TODO: replace me', data = _travel_time_route)
    print(f"Sent 'us.wa.wsdot.traveltimes.TravelTimeRoute.mqtt' event: {_travel_time_route.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_mountainpass_mqtt_event_producer = UsWaWsdotMountainpassMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_mountainpass_mqtt_event_producer = UsWaWsdotMountainpassMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.mountainpass.MountainPassCondition.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.mountainpass.MountainPassCondition.mqtt event
    _mountain_pass_condition = MountainPassCondition()

    # sends the 'us.wa.wsdot.mountainpass.MountainPassCondition.mqtt' event to Kafka topic.
    await us_wa_wsdot_mountainpass_mqtt_event_producer.send_us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt(_feedurl = 'TODO: replace me', _mountain_pass_id = 'TODO: replace me', data = _mountain_pass_condition)
    print(f"Sent 'us.wa.wsdot.mountainpass.MountainPassCondition.mqtt' event: {_mountain_pass_condition.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_weather_mqtt_event_producer = UsWaWsdotWeatherMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_weather_mqtt_event_producer = UsWaWsdotWeatherMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.weather.WeatherStation.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.weather.WeatherStation.mqtt event
    _weather_station = WeatherStation()

    # sends the 'us.wa.wsdot.weather.WeatherStation.mqtt' event to Kafka topic.
    await us_wa_wsdot_weather_mqtt_event_producer.send_us_wa_wsdot_weather_weather_station_mqtt(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _weather_station)
    print(f"Sent 'us.wa.wsdot.weather.WeatherStation.mqtt' event: {_weather_station.to_json()}")

    # ---- us.wa.wsdot.weather.WeatherReading.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.weather.WeatherReading.mqtt event
    _weather_reading = WeatherReading()

    # sends the 'us.wa.wsdot.weather.WeatherReading.mqtt' event to Kafka topic.
    await us_wa_wsdot_weather_mqtt_event_producer.send_us_wa_wsdot_weather_weather_reading_mqtt(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _weather_reading)
    print(f"Sent 'us.wa.wsdot.weather.WeatherReading.mqtt' event: {_weather_reading.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_tolls_mqtt_event_producer = UsWaWsdotTollsMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_tolls_mqtt_event_producer = UsWaWsdotTollsMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.tolls.TollRate.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.tolls.TollRate.mqtt event
    _toll_rate = TollRate()

    # sends the 'us.wa.wsdot.tolls.TollRate.mqtt' event to Kafka topic.
    await us_wa_wsdot_tolls_mqtt_event_producer.send_us_wa_wsdot_tolls_toll_rate_mqtt(_feedurl = 'TODO: replace me', _trip_name = 'TODO: replace me', data = _toll_rate)
    print(f"Sent 'us.wa.wsdot.tolls.TollRate.mqtt' event: {_toll_rate.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_cvrestrictions_mqtt_event_producer = UsWaWsdotCvrestrictionsMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_cvrestrictions_mqtt_event_producer = UsWaWsdotCvrestrictionsMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.mqtt event
    _commercial_vehicle_restriction = CommercialVehicleRestriction()

    # sends the 'us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.mqtt' event to Kafka topic.
    await us_wa_wsdot_cvrestrictions_mqtt_event_producer.send_us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt(_feedurl = 'TODO: replace me', _state_route_id = 'TODO: replace me', _bridge_number = 'TODO: replace me', data = _commercial_vehicle_restriction)
    print(f"Sent 'us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.mqtt' event: {_commercial_vehicle_restriction.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_border_mqtt_event_producer = UsWaWsdotBorderMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_border_mqtt_event_producer = UsWaWsdotBorderMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.border.BorderCrossing.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.border.BorderCrossing.mqtt event
    _border_crossing = BorderCrossing()

    # sends the 'us.wa.wsdot.border.BorderCrossing.mqtt' event to Kafka topic.
    await us_wa_wsdot_border_mqtt_event_producer.send_us_wa_wsdot_border_border_crossing_mqtt(_feedurl = 'TODO: replace me', _crossing_name = 'TODO: replace me', data = _border_crossing)
    print(f"Sent 'us.wa.wsdot.border.BorderCrossing.mqtt' event: {_border_crossing.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_ferries_mqtt_event_producer = UsWaWsdotFerriesMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_ferries_mqtt_event_producer = UsWaWsdotFerriesMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.ferries.VesselLocation.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.ferries.VesselLocation.mqtt event
    _vessel_location = VesselLocation()

    # sends the 'us.wa.wsdot.ferries.VesselLocation.mqtt' event to Kafka topic.
    await us_wa_wsdot_ferries_mqtt_event_producer.send_us_wa_wsdot_ferries_vessel_location_mqtt(_feedurl = 'TODO: replace me', _vessel_id = 'TODO: replace me', data = _vessel_location)
    print(f"Sent 'us.wa.wsdot.ferries.VesselLocation.mqtt' event: {_vessel_location.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_traffic_amqp_event_producer = UsWaWsdotTrafficAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_traffic_amqp_event_producer = UsWaWsdotTrafficAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.traffic.TrafficFlowStation.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.traffic.TrafficFlowStation.amqp event
    _traffic_flow_station = TrafficFlowStation()

    # sends the 'us.wa.wsdot.traffic.TrafficFlowStation.amqp' event to Kafka topic.
    await us_wa_wsdot_traffic_amqp_event_producer.send_us_wa_wsdot_traffic_traffic_flow_station_amqp(_feedurl = 'TODO: replace me', _flow_data_id = 'TODO: replace me', data = _traffic_flow_station)
    print(f"Sent 'us.wa.wsdot.traffic.TrafficFlowStation.amqp' event: {_traffic_flow_station.to_json()}")

    # ---- us.wa.wsdot.traffic.TrafficFlowReading.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.traffic.TrafficFlowReading.amqp event
    _traffic_flow_reading = TrafficFlowReading()

    # sends the 'us.wa.wsdot.traffic.TrafficFlowReading.amqp' event to Kafka topic.
    await us_wa_wsdot_traffic_amqp_event_producer.send_us_wa_wsdot_traffic_traffic_flow_reading_amqp(_feedurl = 'TODO: replace me', _flow_data_id = 'TODO: replace me', data = _traffic_flow_reading)
    print(f"Sent 'us.wa.wsdot.traffic.TrafficFlowReading.amqp' event: {_traffic_flow_reading.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_traveltimes_amqp_event_producer = UsWaWsdotTraveltimesAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_traveltimes_amqp_event_producer = UsWaWsdotTraveltimesAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.traveltimes.TravelTimeRoute.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.traveltimes.TravelTimeRoute.amqp event
    _travel_time_route = TravelTimeRoute()

    # sends the 'us.wa.wsdot.traveltimes.TravelTimeRoute.amqp' event to Kafka topic.
    await us_wa_wsdot_traveltimes_amqp_event_producer.send_us_wa_wsdot_traveltimes_travel_time_route_amqp(_feedurl = 'TODO: replace me', _travel_time_id = 'TODO: replace me', data = _travel_time_route)
    print(f"Sent 'us.wa.wsdot.traveltimes.TravelTimeRoute.amqp' event: {_travel_time_route.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_mountainpass_amqp_event_producer = UsWaWsdotMountainpassAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_mountainpass_amqp_event_producer = UsWaWsdotMountainpassAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.mountainpass.MountainPassCondition.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.mountainpass.MountainPassCondition.amqp event
    _mountain_pass_condition = MountainPassCondition()

    # sends the 'us.wa.wsdot.mountainpass.MountainPassCondition.amqp' event to Kafka topic.
    await us_wa_wsdot_mountainpass_amqp_event_producer.send_us_wa_wsdot_mountainpass_mountain_pass_condition_amqp(_feedurl = 'TODO: replace me', _mountain_pass_id = 'TODO: replace me', data = _mountain_pass_condition)
    print(f"Sent 'us.wa.wsdot.mountainpass.MountainPassCondition.amqp' event: {_mountain_pass_condition.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_weather_amqp_event_producer = UsWaWsdotWeatherAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_weather_amqp_event_producer = UsWaWsdotWeatherAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.weather.WeatherStation.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.weather.WeatherStation.amqp event
    _weather_station = WeatherStation()

    # sends the 'us.wa.wsdot.weather.WeatherStation.amqp' event to Kafka topic.
    await us_wa_wsdot_weather_amqp_event_producer.send_us_wa_wsdot_weather_weather_station_amqp(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _weather_station)
    print(f"Sent 'us.wa.wsdot.weather.WeatherStation.amqp' event: {_weather_station.to_json()}")

    # ---- us.wa.wsdot.weather.WeatherReading.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.weather.WeatherReading.amqp event
    _weather_reading = WeatherReading()

    # sends the 'us.wa.wsdot.weather.WeatherReading.amqp' event to Kafka topic.
    await us_wa_wsdot_weather_amqp_event_producer.send_us_wa_wsdot_weather_weather_reading_amqp(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _weather_reading)
    print(f"Sent 'us.wa.wsdot.weather.WeatherReading.amqp' event: {_weather_reading.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_tolls_amqp_event_producer = UsWaWsdotTollsAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_tolls_amqp_event_producer = UsWaWsdotTollsAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.tolls.TollRate.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.tolls.TollRate.amqp event
    _toll_rate = TollRate()

    # sends the 'us.wa.wsdot.tolls.TollRate.amqp' event to Kafka topic.
    await us_wa_wsdot_tolls_amqp_event_producer.send_us_wa_wsdot_tolls_toll_rate_amqp(_feedurl = 'TODO: replace me', _trip_name = 'TODO: replace me', data = _toll_rate)
    print(f"Sent 'us.wa.wsdot.tolls.TollRate.amqp' event: {_toll_rate.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_cvrestrictions_amqp_event_producer = UsWaWsdotCvrestrictionsAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_cvrestrictions_amqp_event_producer = UsWaWsdotCvrestrictionsAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.amqp event
    _commercial_vehicle_restriction = CommercialVehicleRestriction()

    # sends the 'us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.amqp' event to Kafka topic.
    await us_wa_wsdot_cvrestrictions_amqp_event_producer.send_us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_amqp(_feedurl = 'TODO: replace me', _state_route_id = 'TODO: replace me', _bridge_number = 'TODO: replace me', data = _commercial_vehicle_restriction)
    print(f"Sent 'us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.amqp' event: {_commercial_vehicle_restriction.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_border_amqp_event_producer = UsWaWsdotBorderAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_border_amqp_event_producer = UsWaWsdotBorderAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.border.BorderCrossing.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.border.BorderCrossing.amqp event
    _border_crossing = BorderCrossing()

    # sends the 'us.wa.wsdot.border.BorderCrossing.amqp' event to Kafka topic.
    await us_wa_wsdot_border_amqp_event_producer.send_us_wa_wsdot_border_border_crossing_amqp(_feedurl = 'TODO: replace me', _crossing_name = 'TODO: replace me', data = _border_crossing)
    print(f"Sent 'us.wa.wsdot.border.BorderCrossing.amqp' event: {_border_crossing.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_ferries_amqp_event_producer = UsWaWsdotFerriesAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_ferries_amqp_event_producer = UsWaWsdotFerriesAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.ferries.VesselLocation.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.ferries.VesselLocation.amqp event
    _vessel_location = VesselLocation()

    # sends the 'us.wa.wsdot.ferries.VesselLocation.amqp' event to Kafka topic.
    await us_wa_wsdot_ferries_amqp_event_producer.send_us_wa_wsdot_ferries_vessel_location_amqp(_feedurl = 'TODO: replace me', _vessel_id = 'TODO: replace me', data = _vessel_location)
    print(f"Sent 'us.wa.wsdot.ferries.VesselLocation.amqp' event: {_vessel_location.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_roadweather_event_producer = UsWaWsdotRoadweatherEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_roadweather_event_producer = UsWaWsdotRoadweatherEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.roadweather.RoadWeatherStation ----
    # TODO: Supply event data for the us.wa.wsdot.roadweather.RoadWeatherStation event
    _road_weather_station = RoadWeatherStation()

    # sends the 'us.wa.wsdot.roadweather.RoadWeatherStation' event to Kafka topic.
    await us_wa_wsdot_roadweather_event_producer.send_us_wa_wsdot_roadweather_road_weather_station(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _road_weather_station)
    print(f"Sent 'us.wa.wsdot.roadweather.RoadWeatherStation' event: {_road_weather_station.to_json()}")

    # ---- us.wa.wsdot.roadweather.RoadWeatherReading ----
    # TODO: Supply event data for the us.wa.wsdot.roadweather.RoadWeatherReading event
    _road_weather_reading = RoadWeatherReading()

    # sends the 'us.wa.wsdot.roadweather.RoadWeatherReading' event to Kafka topic.
    await us_wa_wsdot_roadweather_event_producer.send_us_wa_wsdot_roadweather_road_weather_reading(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _road_weather_reading)
    print(f"Sent 'us.wa.wsdot.roadweather.RoadWeatherReading' event: {_road_weather_reading.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_alerts_event_producer = UsWaWsdotAlertsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_alerts_event_producer = UsWaWsdotAlertsEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.alerts.HighwayAlert ----
    # TODO: Supply event data for the us.wa.wsdot.alerts.HighwayAlert event
    _highway_alert = HighwayAlert()

    # sends the 'us.wa.wsdot.alerts.HighwayAlert' event to Kafka topic.
    await us_wa_wsdot_alerts_event_producer.send_us_wa_wsdot_alerts_highway_alert(_feedurl = 'TODO: replace me', _alert_id = 'TODO: replace me', data = _highway_alert)
    print(f"Sent 'us.wa.wsdot.alerts.HighwayAlert' event: {_highway_alert.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_cameras_event_producer = UsWaWsdotCamerasEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_cameras_event_producer = UsWaWsdotCamerasEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.cameras.HighwayCamera ----
    # TODO: Supply event data for the us.wa.wsdot.cameras.HighwayCamera event
    _highway_camera = HighwayCamera()

    # sends the 'us.wa.wsdot.cameras.HighwayCamera' event to Kafka topic.
    await us_wa_wsdot_cameras_event_producer.send_us_wa_wsdot_cameras_highway_camera(_feedurl = 'TODO: replace me', _camera_id = 'TODO: replace me', data = _highway_camera)
    print(f"Sent 'us.wa.wsdot.cameras.HighwayCamera' event: {_highway_camera.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_bridgeclearances_event_producer = UsWaWsdotBridgeclearancesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_bridgeclearances_event_producer = UsWaWsdotBridgeclearancesEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.bridgeclearances.BridgeClearance ----
    # TODO: Supply event data for the us.wa.wsdot.bridgeclearances.BridgeClearance event
    _bridge_clearance = BridgeClearance()

    # sends the 'us.wa.wsdot.bridgeclearances.BridgeClearance' event to Kafka topic.
    await us_wa_wsdot_bridgeclearances_event_producer.send_us_wa_wsdot_bridgeclearances_bridge_clearance(_feedurl = 'TODO: replace me', _crossing_location_id = 'TODO: replace me', data = _bridge_clearance)
    print(f"Sent 'us.wa.wsdot.bridgeclearances.BridgeClearance' event: {_bridge_clearance.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_ferryterminals_event_producer = UsWaWsdotFerryterminalsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_ferryterminals_event_producer = UsWaWsdotFerryterminalsEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.ferryterminals.TerminalSailingSpace ----
    # TODO: Supply event data for the us.wa.wsdot.ferryterminals.TerminalSailingSpace event
    _terminal_sailing_space = TerminalSailingSpace()

    # sends the 'us.wa.wsdot.ferryterminals.TerminalSailingSpace' event to Kafka topic.
    await us_wa_wsdot_ferryterminals_event_producer.send_us_wa_wsdot_ferryterminals_terminal_sailing_space(_feedurl = 'TODO: replace me', _terminal_id = 'TODO: replace me', data = _terminal_sailing_space)
    print(f"Sent 'us.wa.wsdot.ferryterminals.TerminalSailingSpace' event: {_terminal_sailing_space.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_roadweather_mqtt_event_producer = UsWaWsdotRoadweatherMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_roadweather_mqtt_event_producer = UsWaWsdotRoadweatherMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.roadweather.RoadWeatherStation.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.roadweather.RoadWeatherStation.mqtt event
    _road_weather_station = RoadWeatherStation()

    # sends the 'us.wa.wsdot.roadweather.RoadWeatherStation.mqtt' event to Kafka topic.
    await us_wa_wsdot_roadweather_mqtt_event_producer.send_us_wa_wsdot_roadweather_road_weather_station_mqtt(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _road_weather_station)
    print(f"Sent 'us.wa.wsdot.roadweather.RoadWeatherStation.mqtt' event: {_road_weather_station.to_json()}")

    # ---- us.wa.wsdot.roadweather.RoadWeatherReading.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.roadweather.RoadWeatherReading.mqtt event
    _road_weather_reading = RoadWeatherReading()

    # sends the 'us.wa.wsdot.roadweather.RoadWeatherReading.mqtt' event to Kafka topic.
    await us_wa_wsdot_roadweather_mqtt_event_producer.send_us_wa_wsdot_roadweather_road_weather_reading_mqtt(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _road_weather_reading)
    print(f"Sent 'us.wa.wsdot.roadweather.RoadWeatherReading.mqtt' event: {_road_weather_reading.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_alerts_mqtt_event_producer = UsWaWsdotAlertsMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_alerts_mqtt_event_producer = UsWaWsdotAlertsMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.alerts.HighwayAlert.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.alerts.HighwayAlert.mqtt event
    _highway_alert = HighwayAlert()

    # sends the 'us.wa.wsdot.alerts.HighwayAlert.mqtt' event to Kafka topic.
    await us_wa_wsdot_alerts_mqtt_event_producer.send_us_wa_wsdot_alerts_highway_alert_mqtt(_feedurl = 'TODO: replace me', _alert_id = 'TODO: replace me', data = _highway_alert)
    print(f"Sent 'us.wa.wsdot.alerts.HighwayAlert.mqtt' event: {_highway_alert.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_cameras_mqtt_event_producer = UsWaWsdotCamerasMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_cameras_mqtt_event_producer = UsWaWsdotCamerasMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.cameras.HighwayCamera.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.cameras.HighwayCamera.mqtt event
    _highway_camera = HighwayCamera()

    # sends the 'us.wa.wsdot.cameras.HighwayCamera.mqtt' event to Kafka topic.
    await us_wa_wsdot_cameras_mqtt_event_producer.send_us_wa_wsdot_cameras_highway_camera_mqtt(_feedurl = 'TODO: replace me', _camera_id = 'TODO: replace me', data = _highway_camera)
    print(f"Sent 'us.wa.wsdot.cameras.HighwayCamera.mqtt' event: {_highway_camera.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_bridgeclearances_mqtt_event_producer = UsWaWsdotBridgeclearancesMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_bridgeclearances_mqtt_event_producer = UsWaWsdotBridgeclearancesMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.bridgeclearances.BridgeClearance.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.bridgeclearances.BridgeClearance.mqtt event
    _bridge_clearance = BridgeClearance()

    # sends the 'us.wa.wsdot.bridgeclearances.BridgeClearance.mqtt' event to Kafka topic.
    await us_wa_wsdot_bridgeclearances_mqtt_event_producer.send_us_wa_wsdot_bridgeclearances_bridge_clearance_mqtt(_feedurl = 'TODO: replace me', _crossing_location_id = 'TODO: replace me', data = _bridge_clearance)
    print(f"Sent 'us.wa.wsdot.bridgeclearances.BridgeClearance.mqtt' event: {_bridge_clearance.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_ferryterminals_mqtt_event_producer = UsWaWsdotFerryterminalsMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_ferryterminals_mqtt_event_producer = UsWaWsdotFerryterminalsMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.ferryterminals.TerminalSailingSpace.mqtt ----
    # TODO: Supply event data for the us.wa.wsdot.ferryterminals.TerminalSailingSpace.mqtt event
    _terminal_sailing_space = TerminalSailingSpace()

    # sends the 'us.wa.wsdot.ferryterminals.TerminalSailingSpace.mqtt' event to Kafka topic.
    await us_wa_wsdot_ferryterminals_mqtt_event_producer.send_us_wa_wsdot_ferryterminals_terminal_sailing_space_mqtt(_feedurl = 'TODO: replace me', _terminal_id = 'TODO: replace me', data = _terminal_sailing_space)
    print(f"Sent 'us.wa.wsdot.ferryterminals.TerminalSailingSpace.mqtt' event: {_terminal_sailing_space.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_roadweather_amqp_event_producer = UsWaWsdotRoadweatherAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_roadweather_amqp_event_producer = UsWaWsdotRoadweatherAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.roadweather.RoadWeatherStation.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.roadweather.RoadWeatherStation.amqp event
    _road_weather_station = RoadWeatherStation()

    # sends the 'us.wa.wsdot.roadweather.RoadWeatherStation.amqp' event to Kafka topic.
    await us_wa_wsdot_roadweather_amqp_event_producer.send_us_wa_wsdot_roadweather_road_weather_station_amqp(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _road_weather_station)
    print(f"Sent 'us.wa.wsdot.roadweather.RoadWeatherStation.amqp' event: {_road_weather_station.to_json()}")

    # ---- us.wa.wsdot.roadweather.RoadWeatherReading.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.roadweather.RoadWeatherReading.amqp event
    _road_weather_reading = RoadWeatherReading()

    # sends the 'us.wa.wsdot.roadweather.RoadWeatherReading.amqp' event to Kafka topic.
    await us_wa_wsdot_roadweather_amqp_event_producer.send_us_wa_wsdot_roadweather_road_weather_reading_amqp(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _road_weather_reading)
    print(f"Sent 'us.wa.wsdot.roadweather.RoadWeatherReading.amqp' event: {_road_weather_reading.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_alerts_amqp_event_producer = UsWaWsdotAlertsAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_alerts_amqp_event_producer = UsWaWsdotAlertsAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.alerts.HighwayAlert.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.alerts.HighwayAlert.amqp event
    _highway_alert = HighwayAlert()

    # sends the 'us.wa.wsdot.alerts.HighwayAlert.amqp' event to Kafka topic.
    await us_wa_wsdot_alerts_amqp_event_producer.send_us_wa_wsdot_alerts_highway_alert_amqp(_feedurl = 'TODO: replace me', _alert_id = 'TODO: replace me', data = _highway_alert)
    print(f"Sent 'us.wa.wsdot.alerts.HighwayAlert.amqp' event: {_highway_alert.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_cameras_amqp_event_producer = UsWaWsdotCamerasAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_cameras_amqp_event_producer = UsWaWsdotCamerasAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.cameras.HighwayCamera.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.cameras.HighwayCamera.amqp event
    _highway_camera = HighwayCamera()

    # sends the 'us.wa.wsdot.cameras.HighwayCamera.amqp' event to Kafka topic.
    await us_wa_wsdot_cameras_amqp_event_producer.send_us_wa_wsdot_cameras_highway_camera_amqp(_feedurl = 'TODO: replace me', _camera_id = 'TODO: replace me', data = _highway_camera)
    print(f"Sent 'us.wa.wsdot.cameras.HighwayCamera.amqp' event: {_highway_camera.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_bridgeclearances_amqp_event_producer = UsWaWsdotBridgeclearancesAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_bridgeclearances_amqp_event_producer = UsWaWsdotBridgeclearancesAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.bridgeclearances.BridgeClearance.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.bridgeclearances.BridgeClearance.amqp event
    _bridge_clearance = BridgeClearance()

    # sends the 'us.wa.wsdot.bridgeclearances.BridgeClearance.amqp' event to Kafka topic.
    await us_wa_wsdot_bridgeclearances_amqp_event_producer.send_us_wa_wsdot_bridgeclearances_bridge_clearance_amqp(_feedurl = 'TODO: replace me', _crossing_location_id = 'TODO: replace me', data = _bridge_clearance)
    print(f"Sent 'us.wa.wsdot.bridgeclearances.BridgeClearance.amqp' event: {_bridge_clearance.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        us_wa_wsdot_ferryterminals_amqp_event_producer = UsWaWsdotFerryterminalsAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        us_wa_wsdot_ferryterminals_amqp_event_producer = UsWaWsdotFerryterminalsAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- us.wa.wsdot.ferryterminals.TerminalSailingSpace.amqp ----
    # TODO: Supply event data for the us.wa.wsdot.ferryterminals.TerminalSailingSpace.amqp event
    _terminal_sailing_space = TerminalSailingSpace()

    # sends the 'us.wa.wsdot.ferryterminals.TerminalSailingSpace.amqp' event to Kafka topic.
    await us_wa_wsdot_ferryterminals_amqp_event_producer.send_us_wa_wsdot_ferryterminals_terminal_sailing_space_amqp(_feedurl = 'TODO: replace me', _terminal_id = 'TODO: replace me', data = _terminal_sailing_space)
    print(f"Sent 'us.wa.wsdot.ferryterminals.TerminalSailingSpace.amqp' event: {_terminal_sailing_space.to_json()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer")
    parser.add_argument('--producer-config', default=os.getenv('KAFKA_PRODUCER_CONFIG'), help='Kafka producer config (JSON)', required=False)
    parser.add_argument('--topics', default=os.getenv('KAFKA_TOPICS'), help='Kafka topics to send events to', required=False)
    parser.add_argument('-c', '--connection-string', dest='connection_string', default=os.getenv('FABRIC_CONNECTION_STRING'), help='Fabric connection string', required=False)

    args = parser.parse_args()

    asyncio.run(main(
        args.connection_string,
        args.producer_config,
        args.topics
    ))