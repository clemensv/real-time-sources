
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

# imports for the data classes for each event

from wsdot_producer_data.trafficflowstation import TrafficFlowStation
from wsdot_producer_data.trafficflowreading import TrafficFlowReading
from wsdot_producer_data.traveltimeroute import TravelTimeRoute
from wsdot_producer_data.mountainpasscondition import MountainPassCondition
from wsdot_producer_data.weatherstation import WeatherStation
from wsdot_producer_data.weatherreading import WeatherReading
from wsdot_producer_data.tollrate import TollRate
from wsdot_producer_data.commercialvehiclerestriction import CommercialVehicleRestriction
from wsdot_producer_data.bordercrossing import BorderCrossing
from wsdot_producer_data.vessellocation import VesselLocation

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