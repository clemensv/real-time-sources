
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

from vatsim_producer_kafka_producer.producer import NetVatsimPilotsEventProducer
from vatsim_producer_kafka_producer.producer import NetVatsimControllersEventProducer
from vatsim_producer_kafka_producer.producer import NetVatsimStatusEventProducer
from vatsim_producer_kafka_producer.producer import NetVatsimMqttEventProducer
from vatsim_producer_kafka_producer.producer import NetVatsimAmqpEventProducer

# imports for the data classes for each event

from vatsim_producer_data import PilotPosition
from vatsim_producer_data import ControllerPosition
from vatsim_producer_data import NetworkStatus

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
        net_vatsim_pilots_event_producer = NetVatsimPilotsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        net_vatsim_pilots_event_producer = NetVatsimPilotsEventProducer(kafka_producer, topic, 'binary')

    # ---- net.vatsim.PilotPosition ----
    # TODO: Supply event data for the net.vatsim.PilotPosition event
    _pilot_position = PilotPosition()

    # sends the 'net.vatsim.PilotPosition' event to Kafka topic.
    await net_vatsim_pilots_event_producer.send_net_vatsim_pilot_position(_callsign = 'TODO: replace me', data = _pilot_position)
    print(f"Sent 'net.vatsim.PilotPosition' event: {_pilot_position.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        net_vatsim_controllers_event_producer = NetVatsimControllersEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        net_vatsim_controllers_event_producer = NetVatsimControllersEventProducer(kafka_producer, topic, 'binary')

    # ---- net.vatsim.ControllerPosition ----
    # TODO: Supply event data for the net.vatsim.ControllerPosition event
    _controller_position = ControllerPosition()

    # sends the 'net.vatsim.ControllerPosition' event to Kafka topic.
    await net_vatsim_controllers_event_producer.send_net_vatsim_controller_position(_callsign = 'TODO: replace me', data = _controller_position)
    print(f"Sent 'net.vatsim.ControllerPosition' event: {_controller_position.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        net_vatsim_status_event_producer = NetVatsimStatusEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        net_vatsim_status_event_producer = NetVatsimStatusEventProducer(kafka_producer, topic, 'binary')

    # ---- net.vatsim.NetworkStatus ----
    # TODO: Supply event data for the net.vatsim.NetworkStatus event
    _network_status = NetworkStatus()

    # sends the 'net.vatsim.NetworkStatus' event to Kafka topic.
    await net_vatsim_status_event_producer.send_net_vatsim_network_status(_callsign = 'TODO: replace me', data = _network_status)
    print(f"Sent 'net.vatsim.NetworkStatus' event: {_network_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        net_vatsim_mqtt_event_producer = NetVatsimMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        net_vatsim_mqtt_event_producer = NetVatsimMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- net.vatsim.mqtt.PilotPosition ----
    # TODO: Supply event data for the net.vatsim.mqtt.PilotPosition event
    _pilot_position = PilotPosition()

    # sends the 'net.vatsim.mqtt.PilotPosition' event to Kafka topic.
    await net_vatsim_mqtt_event_producer.send_net_vatsim_mqtt_pilot_position(_callsign = 'TODO: replace me', data = _pilot_position)
    print(f"Sent 'net.vatsim.mqtt.PilotPosition' event: {_pilot_position.to_json()}")

    # ---- net.vatsim.mqtt.ControllerPosition ----
    # TODO: Supply event data for the net.vatsim.mqtt.ControllerPosition event
    _controller_position = ControllerPosition()

    # sends the 'net.vatsim.mqtt.ControllerPosition' event to Kafka topic.
    await net_vatsim_mqtt_event_producer.send_net_vatsim_mqtt_controller_position(_callsign = 'TODO: replace me', data = _controller_position)
    print(f"Sent 'net.vatsim.mqtt.ControllerPosition' event: {_controller_position.to_json()}")

    # ---- net.vatsim.mqtt.FacilityStatus ----
    # TODO: Supply event data for the net.vatsim.mqtt.FacilityStatus event
    _network_status = NetworkStatus()

    # sends the 'net.vatsim.mqtt.FacilityStatus' event to Kafka topic.
    await net_vatsim_mqtt_event_producer.send_net_vatsim_mqtt_facility_status(_callsign = 'TODO: replace me', data = _network_status)
    print(f"Sent 'net.vatsim.mqtt.FacilityStatus' event: {_network_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        net_vatsim_amqp_event_producer = NetVatsimAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        net_vatsim_amqp_event_producer = NetVatsimAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- net.vatsim.amqp.PilotPosition ----
    # TODO: Supply event data for the net.vatsim.amqp.PilotPosition event
    _pilot_position = PilotPosition()

    # sends the 'net.vatsim.amqp.PilotPosition' event to Kafka topic.
    await net_vatsim_amqp_event_producer.send_net_vatsim_amqp_pilot_position(_callsign = 'TODO: replace me', data = _pilot_position)
    print(f"Sent 'net.vatsim.amqp.PilotPosition' event: {_pilot_position.to_json()}")

    # ---- net.vatsim.amqp.ControllerPosition ----
    # TODO: Supply event data for the net.vatsim.amqp.ControllerPosition event
    _controller_position = ControllerPosition()

    # sends the 'net.vatsim.amqp.ControllerPosition' event to Kafka topic.
    await net_vatsim_amqp_event_producer.send_net_vatsim_amqp_controller_position(_callsign = 'TODO: replace me', data = _controller_position)
    print(f"Sent 'net.vatsim.amqp.ControllerPosition' event: {_controller_position.to_json()}")

    # ---- net.vatsim.amqp.FacilityStatus ----
    # TODO: Supply event data for the net.vatsim.amqp.FacilityStatus event
    _network_status = NetworkStatus()

    # sends the 'net.vatsim.amqp.FacilityStatus' event to Kafka topic.
    await net_vatsim_amqp_event_producer.send_net_vatsim_amqp_facility_status(_callsign = 'TODO: replace me', data = _network_status)
    print(f"Sent 'net.vatsim.amqp.FacilityStatus' event: {_network_status.to_json()}")

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