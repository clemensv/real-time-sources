
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

from hsl_hfp_producer_kafka_producer.producer import FiHslHfpEventProducer
from hsl_hfp_producer_kafka_producer.producer import FiHslGtfsOperatorEventProducer
from hsl_hfp_producer_kafka_producer.producer import FiHslGtfsRouteEventProducer
from hsl_hfp_producer_kafka_producer.producer import FiHslGtfsStopEventProducer
from hsl_hfp_producer_kafka_producer.producer import FiHslHfpMqttEventProducer
from hsl_hfp_producer_kafka_producer.producer import FiHslHfpAmqpEventProducer
from hsl_hfp_producer_kafka_producer.producer import FiHslGtfsOperatorMqttEventProducer
from hsl_hfp_producer_kafka_producer.producer import FiHslGtfsOperatorAmqpEventProducer
from hsl_hfp_producer_kafka_producer.producer import FiHslGtfsRouteMqttEventProducer
from hsl_hfp_producer_kafka_producer.producer import FiHslGtfsRouteAmqpEventProducer
from hsl_hfp_producer_kafka_producer.producer import FiHslGtfsStopMqttEventProducer
from hsl_hfp_producer_kafka_producer.producer import FiHslGtfsStopAmqpEventProducer

# imports for the data classes for each event

from hsl_hfp_producer_data import VehicleEvent
from hsl_hfp_producer_data import TrafficLightEvent
from hsl_hfp_producer_data import DriverBlockEvent
from hsl_hfp_producer_data import Operator
from hsl_hfp_producer_data import Route
from hsl_hfp_producer_data import Stop

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
        fi_hsl_hfp_event_producer = FiHslHfpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_hsl_hfp_event_producer = FiHslHfpEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.hsl.hfp.vp ----
    # TODO: Supply event data for the fi.hsl.hfp.vp event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.vp' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_vp(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.vp' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.due ----
    # TODO: Supply event data for the fi.hsl.hfp.due event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.due' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_due(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.due' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.arr ----
    # TODO: Supply event data for the fi.hsl.hfp.arr event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.arr' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_arr(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.arr' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.dep ----
    # TODO: Supply event data for the fi.hsl.hfp.dep event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.dep' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_dep(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.dep' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.ars ----
    # TODO: Supply event data for the fi.hsl.hfp.ars event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.ars' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_ars(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.ars' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.pde ----
    # TODO: Supply event data for the fi.hsl.hfp.pde event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.pde' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_pde(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.pde' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.pas ----
    # TODO: Supply event data for the fi.hsl.hfp.pas event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.pas' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_pas(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.pas' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.wait ----
    # TODO: Supply event data for the fi.hsl.hfp.wait event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.wait' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_wait(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.wait' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.doo ----
    # TODO: Supply event data for the fi.hsl.hfp.doo event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.doo' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_doo(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.doo' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.doc ----
    # TODO: Supply event data for the fi.hsl.hfp.doc event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.doc' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_doc(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.doc' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.vja ----
    # TODO: Supply event data for the fi.hsl.hfp.vja event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.vja' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_vja(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.vja' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.vjout ----
    # TODO: Supply event data for the fi.hsl.hfp.vjout event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.vjout' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_vjout(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.vjout' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.tlr ----
    # TODO: Supply event data for the fi.hsl.hfp.tlr event
    _traffic_light_event = TrafficLightEvent()

    # sends the 'fi.hsl.hfp.tlr' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_tlr(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _traffic_light_event)
    print(f"Sent 'fi.hsl.hfp.tlr' event: {_traffic_light_event.to_json()}")

    # ---- fi.hsl.hfp.tla ----
    # TODO: Supply event data for the fi.hsl.hfp.tla event
    _traffic_light_event = TrafficLightEvent()

    # sends the 'fi.hsl.hfp.tla' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_tla(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _traffic_light_event)
    print(f"Sent 'fi.hsl.hfp.tla' event: {_traffic_light_event.to_json()}")

    # ---- fi.hsl.hfp.da ----
    # TODO: Supply event data for the fi.hsl.hfp.da event
    _driver_block_event = DriverBlockEvent()

    # sends the 'fi.hsl.hfp.da' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_da(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _driver_block_event)
    print(f"Sent 'fi.hsl.hfp.da' event: {_driver_block_event.to_json()}")

    # ---- fi.hsl.hfp.dout ----
    # TODO: Supply event data for the fi.hsl.hfp.dout event
    _driver_block_event = DriverBlockEvent()

    # sends the 'fi.hsl.hfp.dout' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_dout(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _driver_block_event)
    print(f"Sent 'fi.hsl.hfp.dout' event: {_driver_block_event.to_json()}")

    # ---- fi.hsl.hfp.ba ----
    # TODO: Supply event data for the fi.hsl.hfp.ba event
    _driver_block_event = DriverBlockEvent()

    # sends the 'fi.hsl.hfp.ba' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_ba(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _driver_block_event)
    print(f"Sent 'fi.hsl.hfp.ba' event: {_driver_block_event.to_json()}")

    # ---- fi.hsl.hfp.bout ----
    # TODO: Supply event data for the fi.hsl.hfp.bout event
    _driver_block_event = DriverBlockEvent()

    # sends the 'fi.hsl.hfp.bout' event to Kafka topic.
    await fi_hsl_hfp_event_producer.send_fi_hsl_hfp_bout(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _driver_block_event)
    print(f"Sent 'fi.hsl.hfp.bout' event: {_driver_block_event.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_hsl_gtfs_operator_event_producer = FiHslGtfsOperatorEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_hsl_gtfs_operator_event_producer = FiHslGtfsOperatorEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.hsl.gtfs.operator.Operator ----
    # TODO: Supply event data for the fi.hsl.gtfs.operator.Operator event
    _operator = Operator()

    # sends the 'fi.hsl.gtfs.operator.Operator' event to Kafka topic.
    await fi_hsl_gtfs_operator_event_producer.send_fi_hsl_gtfs_operator_operator(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', data = _operator)
    print(f"Sent 'fi.hsl.gtfs.operator.Operator' event: {_operator.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_hsl_gtfs_route_event_producer = FiHslGtfsRouteEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_hsl_gtfs_route_event_producer = FiHslGtfsRouteEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.hsl.gtfs.route.Route ----
    # TODO: Supply event data for the fi.hsl.gtfs.route.Route event
    _route = Route()

    # sends the 'fi.hsl.gtfs.route.Route' event to Kafka topic.
    await fi_hsl_gtfs_route_event_producer.send_fi_hsl_gtfs_route_route(_feedurl = 'TODO: replace me', _route_id = 'TODO: replace me', data = _route)
    print(f"Sent 'fi.hsl.gtfs.route.Route' event: {_route.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_hsl_gtfs_stop_event_producer = FiHslGtfsStopEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_hsl_gtfs_stop_event_producer = FiHslGtfsStopEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.hsl.gtfs.stop.Stop ----
    # TODO: Supply event data for the fi.hsl.gtfs.stop.Stop event
    _stop = Stop()

    # sends the 'fi.hsl.gtfs.stop.Stop' event to Kafka topic.
    await fi_hsl_gtfs_stop_event_producer.send_fi_hsl_gtfs_stop_stop(_feedurl = 'TODO: replace me', _stop_id = 'TODO: replace me', data = _stop)
    print(f"Sent 'fi.hsl.gtfs.stop.Stop' event: {_stop.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_hsl_hfp_mqtt_event_producer = FiHslHfpMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_hsl_hfp_mqtt_event_producer = FiHslHfpMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.hsl.hfp.mqtt.vp ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.vp event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.mqtt.vp' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_vp(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.vp' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.due ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.due event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.mqtt.due' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_due(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.due' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.arr ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.arr event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.mqtt.arr' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_arr(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.arr' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.dep ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.dep event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.mqtt.dep' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_dep(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.dep' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.ars ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.ars event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.mqtt.ars' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_ars(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.ars' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.pde ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.pde event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.mqtt.pde' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_pde(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.pde' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.pas ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.pas event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.mqtt.pas' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_pas(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.pas' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.wait ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.wait event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.mqtt.wait' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_wait(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.wait' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.doo ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.doo event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.mqtt.doo' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_doo(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.doo' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.doc ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.doc event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.mqtt.doc' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_doc(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.doc' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.vja ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.vja event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.mqtt.vja' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_vja(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.vja' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.vjout ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.vjout event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.mqtt.vjout' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_vjout(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.vjout' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.tlr ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.tlr event
    _traffic_light_event = TrafficLightEvent()

    # sends the 'fi.hsl.hfp.mqtt.tlr' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_tlr(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _traffic_light_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.tlr' event: {_traffic_light_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.tla ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.tla event
    _traffic_light_event = TrafficLightEvent()

    # sends the 'fi.hsl.hfp.mqtt.tla' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_tla(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _traffic_light_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.tla' event: {_traffic_light_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.da ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.da event
    _driver_block_event = DriverBlockEvent()

    # sends the 'fi.hsl.hfp.mqtt.da' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_da(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _driver_block_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.da' event: {_driver_block_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.dout ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.dout event
    _driver_block_event = DriverBlockEvent()

    # sends the 'fi.hsl.hfp.mqtt.dout' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_dout(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _driver_block_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.dout' event: {_driver_block_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.ba ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.ba event
    _driver_block_event = DriverBlockEvent()

    # sends the 'fi.hsl.hfp.mqtt.ba' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_ba(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _driver_block_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.ba' event: {_driver_block_event.to_json()}")

    # ---- fi.hsl.hfp.mqtt.bout ----
    # TODO: Supply event data for the fi.hsl.hfp.mqtt.bout event
    _driver_block_event = DriverBlockEvent()

    # sends the 'fi.hsl.hfp.mqtt.bout' event to Kafka topic.
    await fi_hsl_hfp_mqtt_event_producer.send_fi_hsl_hfp_mqtt_bout(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _driver_block_event)
    print(f"Sent 'fi.hsl.hfp.mqtt.bout' event: {_driver_block_event.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_hsl_hfp_amqp_event_producer = FiHslHfpAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_hsl_hfp_amqp_event_producer = FiHslHfpAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.hsl.hfp.amqp.vp ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.vp event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.amqp.vp' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_vp(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.amqp.vp' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.due ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.due event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.amqp.due' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_due(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.amqp.due' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.arr ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.arr event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.amqp.arr' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_arr(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.amqp.arr' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.dep ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.dep event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.amqp.dep' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_dep(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.amqp.dep' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.ars ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.ars event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.amqp.ars' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_ars(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.amqp.ars' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.pde ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.pde event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.amqp.pde' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_pde(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.amqp.pde' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.pas ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.pas event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.amqp.pas' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_pas(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.amqp.pas' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.wait ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.wait event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.amqp.wait' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_wait(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.amqp.wait' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.doo ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.doo event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.amqp.doo' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_doo(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.amqp.doo' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.doc ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.doc event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.amqp.doc' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_doc(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.amqp.doc' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.vja ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.vja event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.amqp.vja' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_vja(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.amqp.vja' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.vjout ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.vjout event
    _vehicle_event = VehicleEvent()

    # sends the 'fi.hsl.hfp.amqp.vjout' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_vjout(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _vehicle_event)
    print(f"Sent 'fi.hsl.hfp.amqp.vjout' event: {_vehicle_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.tlr ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.tlr event
    _traffic_light_event = TrafficLightEvent()

    # sends the 'fi.hsl.hfp.amqp.tlr' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_tlr(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _traffic_light_event)
    print(f"Sent 'fi.hsl.hfp.amqp.tlr' event: {_traffic_light_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.tla ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.tla event
    _traffic_light_event = TrafficLightEvent()

    # sends the 'fi.hsl.hfp.amqp.tla' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_tla(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _traffic_light_event)
    print(f"Sent 'fi.hsl.hfp.amqp.tla' event: {_traffic_light_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.da ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.da event
    _driver_block_event = DriverBlockEvent()

    # sends the 'fi.hsl.hfp.amqp.da' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_da(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _driver_block_event)
    print(f"Sent 'fi.hsl.hfp.amqp.da' event: {_driver_block_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.dout ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.dout event
    _driver_block_event = DriverBlockEvent()

    # sends the 'fi.hsl.hfp.amqp.dout' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_dout(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _driver_block_event)
    print(f"Sent 'fi.hsl.hfp.amqp.dout' event: {_driver_block_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.ba ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.ba event
    _driver_block_event = DriverBlockEvent()

    # sends the 'fi.hsl.hfp.amqp.ba' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_ba(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _driver_block_event)
    print(f"Sent 'fi.hsl.hfp.amqp.ba' event: {_driver_block_event.to_json()}")

    # ---- fi.hsl.hfp.amqp.bout ----
    # TODO: Supply event data for the fi.hsl.hfp.amqp.bout event
    _driver_block_event = DriverBlockEvent()

    # sends the 'fi.hsl.hfp.amqp.bout' event to Kafka topic.
    await fi_hsl_hfp_amqp_event_producer.send_fi_hsl_hfp_amqp_bout(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', _vehicle_number = 'TODO: replace me', data = _driver_block_event)
    print(f"Sent 'fi.hsl.hfp.amqp.bout' event: {_driver_block_event.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_hsl_gtfs_operator_mqtt_event_producer = FiHslGtfsOperatorMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_hsl_gtfs_operator_mqtt_event_producer = FiHslGtfsOperatorMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.hsl.gtfs.operator.mqtt.Operator ----
    # TODO: Supply event data for the fi.hsl.gtfs.operator.mqtt.Operator event
    _operator = Operator()

    # sends the 'fi.hsl.gtfs.operator.mqtt.Operator' event to Kafka topic.
    await fi_hsl_gtfs_operator_mqtt_event_producer.send_fi_hsl_gtfs_operator_mqtt_operator(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', data = _operator)
    print(f"Sent 'fi.hsl.gtfs.operator.mqtt.Operator' event: {_operator.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_hsl_gtfs_operator_amqp_event_producer = FiHslGtfsOperatorAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_hsl_gtfs_operator_amqp_event_producer = FiHslGtfsOperatorAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.hsl.gtfs.operator.amqp.Operator ----
    # TODO: Supply event data for the fi.hsl.gtfs.operator.amqp.Operator event
    _operator = Operator()

    # sends the 'fi.hsl.gtfs.operator.amqp.Operator' event to Kafka topic.
    await fi_hsl_gtfs_operator_amqp_event_producer.send_fi_hsl_gtfs_operator_amqp_operator(_feedurl = 'TODO: replace me', _operator_id = 'TODO: replace me', data = _operator)
    print(f"Sent 'fi.hsl.gtfs.operator.amqp.Operator' event: {_operator.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_hsl_gtfs_route_mqtt_event_producer = FiHslGtfsRouteMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_hsl_gtfs_route_mqtt_event_producer = FiHslGtfsRouteMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.hsl.gtfs.route.mqtt.Route ----
    # TODO: Supply event data for the fi.hsl.gtfs.route.mqtt.Route event
    _route = Route()

    # sends the 'fi.hsl.gtfs.route.mqtt.Route' event to Kafka topic.
    await fi_hsl_gtfs_route_mqtt_event_producer.send_fi_hsl_gtfs_route_mqtt_route(_feedurl = 'TODO: replace me', _route_id = 'TODO: replace me', data = _route)
    print(f"Sent 'fi.hsl.gtfs.route.mqtt.Route' event: {_route.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_hsl_gtfs_route_amqp_event_producer = FiHslGtfsRouteAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_hsl_gtfs_route_amqp_event_producer = FiHslGtfsRouteAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.hsl.gtfs.route.amqp.Route ----
    # TODO: Supply event data for the fi.hsl.gtfs.route.amqp.Route event
    _route = Route()

    # sends the 'fi.hsl.gtfs.route.amqp.Route' event to Kafka topic.
    await fi_hsl_gtfs_route_amqp_event_producer.send_fi_hsl_gtfs_route_amqp_route(_feedurl = 'TODO: replace me', _route_id = 'TODO: replace me', data = _route)
    print(f"Sent 'fi.hsl.gtfs.route.amqp.Route' event: {_route.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_hsl_gtfs_stop_mqtt_event_producer = FiHslGtfsStopMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_hsl_gtfs_stop_mqtt_event_producer = FiHslGtfsStopMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.hsl.gtfs.stop.mqtt.Stop ----
    # TODO: Supply event data for the fi.hsl.gtfs.stop.mqtt.Stop event
    _stop = Stop()

    # sends the 'fi.hsl.gtfs.stop.mqtt.Stop' event to Kafka topic.
    await fi_hsl_gtfs_stop_mqtt_event_producer.send_fi_hsl_gtfs_stop_mqtt_stop(_feedurl = 'TODO: replace me', _stop_id = 'TODO: replace me', data = _stop)
    print(f"Sent 'fi.hsl.gtfs.stop.mqtt.Stop' event: {_stop.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fi_hsl_gtfs_stop_amqp_event_producer = FiHslGtfsStopAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_hsl_gtfs_stop_amqp_event_producer = FiHslGtfsStopAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.hsl.gtfs.stop.amqp.Stop ----
    # TODO: Supply event data for the fi.hsl.gtfs.stop.amqp.Stop event
    _stop = Stop()

    # sends the 'fi.hsl.gtfs.stop.amqp.Stop' event to Kafka topic.
    await fi_hsl_gtfs_stop_amqp_event_producer.send_fi_hsl_gtfs_stop_amqp_stop(_feedurl = 'TODO: replace me', _stop_id = 'TODO: replace me', data = _stop)
    print(f"Sent 'fi.hsl.gtfs.stop.amqp.Stop' event: {_stop.to_json()}")

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