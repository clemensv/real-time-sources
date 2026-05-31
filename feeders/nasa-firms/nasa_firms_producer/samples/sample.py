
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

from nasa_firms_producer_kafka_producer.producer import NASAFIRMSEventProducer
from nasa_firms_producer_kafka_producer.producer import NASAFIRMSMqttEventProducer
from nasa_firms_producer_kafka_producer.producer import NASAFIRMSAmqpEventProducer

# imports for the data classes for each event

from nasa_firms_producer_data.firedetection import FireDetection
from nasa_firms_producer_data.dataavailability import DataAvailability

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
        nasafirmsevent_producer = NASAFIRMSEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nasafirmsevent_producer = NASAFIRMSEventProducer(kafka_producer, topic, 'binary')

    # ---- NASA.FIRMS.FireDetection ----
    # TODO: Supply event data for the NASA.FIRMS.FireDetection event
    _fire_detection = FireDetection()

    # sends the 'NASA.FIRMS.FireDetection' event to Kafka topic.
    await nasafirmsevent_producer.send_nasa_firms_fire_detection(_source_uri = 'TODO: replace me', _source = 'TODO: replace me', _record_id = 'TODO: replace me', data = _fire_detection)
    print(f"Sent 'NASA.FIRMS.FireDetection' event: {_fire_detection.to_json()}")

    # ---- NASA.FIRMS.DataAvailability ----
    # TODO: Supply event data for the NASA.FIRMS.DataAvailability event
    _data_availability = DataAvailability()

    # sends the 'NASA.FIRMS.DataAvailability' event to Kafka topic.
    await nasafirmsevent_producer.send_nasa_firms_data_availability(_source_uri = 'TODO: replace me', _source = 'TODO: replace me', _record_id = 'TODO: replace me', data = _data_availability)
    print(f"Sent 'NASA.FIRMS.DataAvailability' event: {_data_availability.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nasafirmsmqtt_event_producer = NASAFIRMSMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nasafirmsmqtt_event_producer = NASAFIRMSMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- NASA.FIRMS.mqtt.FireDetection ----
    # TODO: Supply event data for the NASA.FIRMS.mqtt.FireDetection event
    _fire_detection = FireDetection()

    # sends the 'NASA.FIRMS.mqtt.FireDetection' event to Kafka topic.
    await nasafirmsmqtt_event_producer.send_nasa_firms_mqtt_fire_detection(_source_uri = 'TODO: replace me', _source = 'TODO: replace me', _record_id = 'TODO: replace me', data = _fire_detection)
    print(f"Sent 'NASA.FIRMS.mqtt.FireDetection' event: {_fire_detection.to_json()}")

    # ---- NASA.FIRMS.mqtt.DataAvailability ----
    # TODO: Supply event data for the NASA.FIRMS.mqtt.DataAvailability event
    _data_availability = DataAvailability()

    # sends the 'NASA.FIRMS.mqtt.DataAvailability' event to Kafka topic.
    await nasafirmsmqtt_event_producer.send_nasa_firms_mqtt_data_availability(_source_uri = 'TODO: replace me', _source = 'TODO: replace me', _record_id = 'TODO: replace me', data = _data_availability)
    print(f"Sent 'NASA.FIRMS.mqtt.DataAvailability' event: {_data_availability.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nasafirmsamqp_event_producer = NASAFIRMSAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nasafirmsamqp_event_producer = NASAFIRMSAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- NASA.FIRMS.amqp.FireDetection ----
    # TODO: Supply event data for the NASA.FIRMS.amqp.FireDetection event
    _fire_detection = FireDetection()

    # sends the 'NASA.FIRMS.amqp.FireDetection' event to Kafka topic.
    await nasafirmsamqp_event_producer.send_nasa_firms_amqp_fire_detection(_source_uri = 'TODO: replace me', _source = 'TODO: replace me', _record_id = 'TODO: replace me', data = _fire_detection)
    print(f"Sent 'NASA.FIRMS.amqp.FireDetection' event: {_fire_detection.to_json()}")

    # ---- NASA.FIRMS.amqp.DataAvailability ----
    # TODO: Supply event data for the NASA.FIRMS.amqp.DataAvailability event
    _data_availability = DataAvailability()

    # sends the 'NASA.FIRMS.amqp.DataAvailability' event to Kafka topic.
    await nasafirmsamqp_event_producer.send_nasa_firms_amqp_data_availability(_source_uri = 'TODO: replace me', _source = 'TODO: replace me', _record_id = 'TODO: replace me', data = _data_availability)
    print(f"Sent 'NASA.FIRMS.amqp.DataAvailability' event: {_data_availability.to_json()}")

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