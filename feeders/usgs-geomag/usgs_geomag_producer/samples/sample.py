
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

from usgs_geomag_producer_kafka_producer.producer import GovUsgsGeomagEventProducer
from usgs_geomag_producer_kafka_producer.producer import GovUsgsGeomagMqttEventProducer
from usgs_geomag_producer_kafka_producer.producer import GovUsgsGeomagAmqpEventProducer

# imports for the data classes for each event

from usgs_geomag_producer_data import Observatory
from usgs_geomag_producer_data import MagneticFieldReading

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
        gov_usgs_geomag_event_producer = GovUsgsGeomagEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        gov_usgs_geomag_event_producer = GovUsgsGeomagEventProducer(kafka_producer, topic, 'binary')

    # ---- gov.usgs.geomag.Observatory ----
    # TODO: Supply event data for the gov.usgs.geomag.Observatory event
    _observatory = Observatory()

    # sends the 'gov.usgs.geomag.Observatory' event to Kafka topic.
    await gov_usgs_geomag_event_producer.send_gov_usgs_geomag_observatory(_iaga_code = 'TODO: replace me', data = _observatory)
    print(f"Sent 'gov.usgs.geomag.Observatory' event: {_observatory.to_json()}")

    # ---- gov.usgs.geomag.MagneticFieldReading ----
    # TODO: Supply event data for the gov.usgs.geomag.MagneticFieldReading event
    _magnetic_field_reading = MagneticFieldReading()

    # sends the 'gov.usgs.geomag.MagneticFieldReading' event to Kafka topic.
    await gov_usgs_geomag_event_producer.send_gov_usgs_geomag_magnetic_field_reading(_iaga_code = 'TODO: replace me', data = _magnetic_field_reading)
    print(f"Sent 'gov.usgs.geomag.MagneticFieldReading' event: {_magnetic_field_reading.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        gov_usgs_geomag_mqtt_event_producer = GovUsgsGeomagMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        gov_usgs_geomag_mqtt_event_producer = GovUsgsGeomagMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- gov.usgs.geomag.mqtt.Observatory ----
    # TODO: Supply event data for the gov.usgs.geomag.mqtt.Observatory event
    _observatory = Observatory()

    # sends the 'gov.usgs.geomag.mqtt.Observatory' event to Kafka topic.
    await gov_usgs_geomag_mqtt_event_producer.send_gov_usgs_geomag_mqtt_observatory(_iaga_code = 'TODO: replace me', data = _observatory)
    print(f"Sent 'gov.usgs.geomag.mqtt.Observatory' event: {_observatory.to_json()}")

    # ---- gov.usgs.geomag.mqtt.MagneticFieldReading ----
    # TODO: Supply event data for the gov.usgs.geomag.mqtt.MagneticFieldReading event
    _magnetic_field_reading = MagneticFieldReading()

    # sends the 'gov.usgs.geomag.mqtt.MagneticFieldReading' event to Kafka topic.
    await gov_usgs_geomag_mqtt_event_producer.send_gov_usgs_geomag_mqtt_magnetic_field_reading(_iaga_code = 'TODO: replace me', data = _magnetic_field_reading)
    print(f"Sent 'gov.usgs.geomag.mqtt.MagneticFieldReading' event: {_magnetic_field_reading.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        gov_usgs_geomag_amqp_event_producer = GovUsgsGeomagAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        gov_usgs_geomag_amqp_event_producer = GovUsgsGeomagAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- gov.usgs.geomag.amqp.Observatory ----
    # TODO: Supply event data for the gov.usgs.geomag.amqp.Observatory event
    _observatory = Observatory()

    # sends the 'gov.usgs.geomag.amqp.Observatory' event to Kafka topic.
    await gov_usgs_geomag_amqp_event_producer.send_gov_usgs_geomag_amqp_observatory(_iaga_code = 'TODO: replace me', data = _observatory)
    print(f"Sent 'gov.usgs.geomag.amqp.Observatory' event: {_observatory.to_json()}")

    # ---- gov.usgs.geomag.amqp.MagneticFieldReading ----
    # TODO: Supply event data for the gov.usgs.geomag.amqp.MagneticFieldReading event
    _magnetic_field_reading = MagneticFieldReading()

    # sends the 'gov.usgs.geomag.amqp.MagneticFieldReading' event to Kafka topic.
    await gov_usgs_geomag_amqp_event_producer.send_gov_usgs_geomag_amqp_magnetic_field_reading(_iaga_code = 'TODO: replace me', data = _magnetic_field_reading)
    print(f"Sent 'gov.usgs.geomag.amqp.MagneticFieldReading' event: {_magnetic_field_reading.to_json()}")

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