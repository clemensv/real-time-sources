
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

from erddap_producer_kafka_producer.producer import OrgErddapDatasetEventProducer
from erddap_producer_kafka_producer.producer import OrgErddapStationEventProducer
from erddap_producer_kafka_producer.producer import OrgErddapKafkaDatasetEventProducer
from erddap_producer_kafka_producer.producer import OrgErddapKafkaStationEventProducer
from erddap_producer_kafka_producer.producer import OrgErddapMqttDatasetEventProducer
from erddap_producer_kafka_producer.producer import OrgErddapMqttStationEventProducer
from erddap_producer_kafka_producer.producer import OrgErddapAmqpDatasetEventProducer
from erddap_producer_kafka_producer.producer import OrgErddapAmqpStationEventProducer

# imports for the data classes for each event

from erddap_producer_data import DatasetMetadata
from erddap_producer_data import StationMetadata
from erddap_producer_data import Observation

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
        org_erddap_dataset_event_producer = OrgErddapDatasetEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_erddap_dataset_event_producer = OrgErddapDatasetEventProducer(kafka_producer, topic, 'binary')

    # ---- org.erddap.DatasetMetadata ----
    # TODO: Supply event data for the org.erddap.DatasetMetadata event
    _dataset_metadata = DatasetMetadata()

    # sends the 'org.erddap.DatasetMetadata' event to Kafka topic.
    await org_erddap_dataset_event_producer.send_org_erddap_dataset_metadata(_base_url = 'TODO: replace me', _erddap_id = 'TODO: replace me', _dataset_id = 'TODO: replace me', data = _dataset_metadata)
    print(f"Sent 'org.erddap.DatasetMetadata' event: {_dataset_metadata.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_erddap_station_event_producer = OrgErddapStationEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_erddap_station_event_producer = OrgErddapStationEventProducer(kafka_producer, topic, 'binary')

    # ---- org.erddap.StationMetadata ----
    # TODO: Supply event data for the org.erddap.StationMetadata event
    _station_metadata = StationMetadata()

    # sends the 'org.erddap.StationMetadata' event to Kafka topic.
    await org_erddap_station_event_producer.send_org_erddap_station_metadata(_base_url = 'TODO: replace me', _erddap_id = 'TODO: replace me', _dataset_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_metadata)
    print(f"Sent 'org.erddap.StationMetadata' event: {_station_metadata.to_json()}")

    # ---- org.erddap.Observation ----
    # TODO: Supply event data for the org.erddap.Observation event
    _observation = Observation()

    # sends the 'org.erddap.Observation' event to Kafka topic.
    await org_erddap_station_event_producer.send_org_erddap_observation(_base_url = 'TODO: replace me', _erddap_id = 'TODO: replace me', _dataset_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _observation)
    print(f"Sent 'org.erddap.Observation' event: {_observation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_erddap_kafka_dataset_event_producer = OrgErddapKafkaDatasetEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_erddap_kafka_dataset_event_producer = OrgErddapKafkaDatasetEventProducer(kafka_producer, topic, 'binary')

    # ---- org.erddap.kafka.DatasetMetadata ----
    # TODO: Supply event data for the org.erddap.kafka.DatasetMetadata event
    _dataset_metadata = DatasetMetadata()

    # sends the 'org.erddap.kafka.DatasetMetadata' event to Kafka topic.
    await org_erddap_kafka_dataset_event_producer.send_org_erddap_kafka_dataset_metadata(_base_url = 'TODO: replace me', _erddap_id = 'TODO: replace me', _dataset_id = 'TODO: replace me', data = _dataset_metadata)
    print(f"Sent 'org.erddap.kafka.DatasetMetadata' event: {_dataset_metadata.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_erddap_kafka_station_event_producer = OrgErddapKafkaStationEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_erddap_kafka_station_event_producer = OrgErddapKafkaStationEventProducer(kafka_producer, topic, 'binary')

    # ---- org.erddap.kafka.StationMetadata ----
    # TODO: Supply event data for the org.erddap.kafka.StationMetadata event
    _station_metadata = StationMetadata()

    # sends the 'org.erddap.kafka.StationMetadata' event to Kafka topic.
    await org_erddap_kafka_station_event_producer.send_org_erddap_kafka_station_metadata(_base_url = 'TODO: replace me', _erddap_id = 'TODO: replace me', _dataset_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_metadata)
    print(f"Sent 'org.erddap.kafka.StationMetadata' event: {_station_metadata.to_json()}")

    # ---- org.erddap.kafka.Observation ----
    # TODO: Supply event data for the org.erddap.kafka.Observation event
    _observation = Observation()

    # sends the 'org.erddap.kafka.Observation' event to Kafka topic.
    await org_erddap_kafka_station_event_producer.send_org_erddap_kafka_observation(_base_url = 'TODO: replace me', _erddap_id = 'TODO: replace me', _dataset_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _observation)
    print(f"Sent 'org.erddap.kafka.Observation' event: {_observation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_erddap_mqtt_dataset_event_producer = OrgErddapMqttDatasetEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_erddap_mqtt_dataset_event_producer = OrgErddapMqttDatasetEventProducer(kafka_producer, topic, 'binary')

    # ---- org.erddap.mqtt.DatasetMetadata ----
    # TODO: Supply event data for the org.erddap.mqtt.DatasetMetadata event
    _dataset_metadata = DatasetMetadata()

    # sends the 'org.erddap.mqtt.DatasetMetadata' event to Kafka topic.
    await org_erddap_mqtt_dataset_event_producer.send_org_erddap_mqtt_dataset_metadata(_base_url = 'TODO: replace me', _erddap_id = 'TODO: replace me', _dataset_id = 'TODO: replace me', data = _dataset_metadata)
    print(f"Sent 'org.erddap.mqtt.DatasetMetadata' event: {_dataset_metadata.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_erddap_mqtt_station_event_producer = OrgErddapMqttStationEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_erddap_mqtt_station_event_producer = OrgErddapMqttStationEventProducer(kafka_producer, topic, 'binary')

    # ---- org.erddap.mqtt.StationMetadata ----
    # TODO: Supply event data for the org.erddap.mqtt.StationMetadata event
    _station_metadata = StationMetadata()

    # sends the 'org.erddap.mqtt.StationMetadata' event to Kafka topic.
    await org_erddap_mqtt_station_event_producer.send_org_erddap_mqtt_station_metadata(_base_url = 'TODO: replace me', _erddap_id = 'TODO: replace me', _dataset_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_metadata)
    print(f"Sent 'org.erddap.mqtt.StationMetadata' event: {_station_metadata.to_json()}")

    # ---- org.erddap.mqtt.Observation ----
    # TODO: Supply event data for the org.erddap.mqtt.Observation event
    _observation = Observation()

    # sends the 'org.erddap.mqtt.Observation' event to Kafka topic.
    await org_erddap_mqtt_station_event_producer.send_org_erddap_mqtt_observation(_base_url = 'TODO: replace me', _erddap_id = 'TODO: replace me', _dataset_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _observation)
    print(f"Sent 'org.erddap.mqtt.Observation' event: {_observation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_erddap_amqp_dataset_event_producer = OrgErddapAmqpDatasetEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_erddap_amqp_dataset_event_producer = OrgErddapAmqpDatasetEventProducer(kafka_producer, topic, 'binary')

    # ---- org.erddap.amqp.DatasetMetadata ----
    # TODO: Supply event data for the org.erddap.amqp.DatasetMetadata event
    _dataset_metadata = DatasetMetadata()

    # sends the 'org.erddap.amqp.DatasetMetadata' event to Kafka topic.
    await org_erddap_amqp_dataset_event_producer.send_org_erddap_amqp_dataset_metadata(_base_url = 'TODO: replace me', _erddap_id = 'TODO: replace me', _dataset_id = 'TODO: replace me', data = _dataset_metadata)
    print(f"Sent 'org.erddap.amqp.DatasetMetadata' event: {_dataset_metadata.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_erddap_amqp_station_event_producer = OrgErddapAmqpStationEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_erddap_amqp_station_event_producer = OrgErddapAmqpStationEventProducer(kafka_producer, topic, 'binary')

    # ---- org.erddap.amqp.StationMetadata ----
    # TODO: Supply event data for the org.erddap.amqp.StationMetadata event
    _station_metadata = StationMetadata()

    # sends the 'org.erddap.amqp.StationMetadata' event to Kafka topic.
    await org_erddap_amqp_station_event_producer.send_org_erddap_amqp_station_metadata(_base_url = 'TODO: replace me', _erddap_id = 'TODO: replace me', _dataset_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_metadata)
    print(f"Sent 'org.erddap.amqp.StationMetadata' event: {_station_metadata.to_json()}")

    # ---- org.erddap.amqp.Observation ----
    # TODO: Supply event data for the org.erddap.amqp.Observation event
    _observation = Observation()

    # sends the 'org.erddap.amqp.Observation' event to Kafka topic.
    await org_erddap_amqp_station_event_producer.send_org_erddap_amqp_observation(_base_url = 'TODO: replace me', _erddap_id = 'TODO: replace me', _dataset_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _observation)
    print(f"Sent 'org.erddap.amqp.Observation' event: {_observation.to_json()}")

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