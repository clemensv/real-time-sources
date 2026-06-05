
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

from xceed_producer_kafka_producer.producer import XceedEventProducer
from xceed_producer_kafka_producer.producer import XceedAdmissionsEventProducer
from xceed_producer_kafka_producer.producer import XceedMqttEventProducer
from xceed_producer_kafka_producer.producer import XceedAmqpEventProducer
from xceed_producer_kafka_producer.producer import XceedAdmissionsMqttEventProducer
from xceed_producer_kafka_producer.producer import XceedAdmissionsAmqpEventProducer

# imports for the data classes for each event

from xceed_producer_data import Event
from xceed_producer_data import EventAdmission

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
        xceed_event_producer = XceedEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        xceed_event_producer = XceedEventProducer(kafka_producer, topic, 'binary')

    # ---- xceed.Event ----
    # TODO: Supply event data for the xceed.Event event
    _event = Event()

    # sends the 'xceed.Event' event to Kafka topic.
    await xceed_event_producer.send_xceed_event(_feedurl = 'TODO: replace me', _event_id = 'TODO: replace me', data = _event)
    print(f"Sent 'xceed.Event' event: {_event.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        xceed_admissions_event_producer = XceedAdmissionsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        xceed_admissions_event_producer = XceedAdmissionsEventProducer(kafka_producer, topic, 'binary')

    # ---- xceed.EventAdmission ----
    # TODO: Supply event data for the xceed.EventAdmission event
    _event_admission = EventAdmission()

    # sends the 'xceed.EventAdmission' event to Kafka topic.
    await xceed_admissions_event_producer.send_xceed_event_admission(_feedurl = 'TODO: replace me', _event_id = 'TODO: replace me', _admission_id = 'TODO: replace me', data = _event_admission)
    print(f"Sent 'xceed.EventAdmission' event: {_event_admission.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        xceed_mqtt_event_producer = XceedMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        xceed_mqtt_event_producer = XceedMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- xceed.mqtt.Event ----
    # TODO: Supply event data for the xceed.mqtt.Event event
    _event = Event()

    # sends the 'xceed.mqtt.Event' event to Kafka topic.
    await xceed_mqtt_event_producer.send_xceed_mqtt_event(_feedurl = 'TODO: replace me', _event_id = 'TODO: replace me', data = _event)
    print(f"Sent 'xceed.mqtt.Event' event: {_event.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        xceed_amqp_event_producer = XceedAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        xceed_amqp_event_producer = XceedAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- xceed.amqp.Event ----
    # TODO: Supply event data for the xceed.amqp.Event event
    _event = Event()

    # sends the 'xceed.amqp.Event' event to Kafka topic.
    await xceed_amqp_event_producer.send_xceed_amqp_event(_feedurl = 'TODO: replace me', _event_id = 'TODO: replace me', data = _event)
    print(f"Sent 'xceed.amqp.Event' event: {_event.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        xceed_admissions_mqtt_event_producer = XceedAdmissionsMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        xceed_admissions_mqtt_event_producer = XceedAdmissionsMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- xceed.admissions.mqtt.EventAdmission ----
    # TODO: Supply event data for the xceed.admissions.mqtt.EventAdmission event
    _event_admission = EventAdmission()

    # sends the 'xceed.admissions.mqtt.EventAdmission' event to Kafka topic.
    await xceed_admissions_mqtt_event_producer.send_xceed_admissions_mqtt_event_admission(_feedurl = 'TODO: replace me', _event_id = 'TODO: replace me', _admission_id = 'TODO: replace me', data = _event_admission)
    print(f"Sent 'xceed.admissions.mqtt.EventAdmission' event: {_event_admission.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        xceed_admissions_amqp_event_producer = XceedAdmissionsAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        xceed_admissions_amqp_event_producer = XceedAdmissionsAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- xceed.admissions.amqp.EventAdmission ----
    # TODO: Supply event data for the xceed.admissions.amqp.EventAdmission event
    _event_admission = EventAdmission()

    # sends the 'xceed.admissions.amqp.EventAdmission' event to Kafka topic.
    await xceed_admissions_amqp_event_producer.send_xceed_admissions_amqp_event_admission(_feedurl = 'TODO: replace me', _event_id = 'TODO: replace me', _admission_id = 'TODO: replace me', data = _event_admission)
    print(f"Sent 'xceed.admissions.amqp.EventAdmission' event: {_event_admission.to_json()}")

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