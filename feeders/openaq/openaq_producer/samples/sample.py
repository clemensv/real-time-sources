
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

from openaq_producer_kafka_producer.producer import OrgOpenaqLocationsEventProducer
from openaq_producer_kafka_producer.producer import OrgOpenaqSensorsEventProducer
from openaq_producer_kafka_producer.producer import OrgOpenaqLocationsKafkaEventProducer
from openaq_producer_kafka_producer.producer import OrgOpenaqSensorsKafkaEventProducer
from openaq_producer_kafka_producer.producer import OrgOpenaqLocationsMqttEventProducer
from openaq_producer_kafka_producer.producer import OrgOpenaqSensorsMqttEventProducer
from openaq_producer_kafka_producer.producer import OrgOpenaqLocationsAmqpEventProducer
from openaq_producer_kafka_producer.producer import OrgOpenaqSensorsAmqpEventProducer

# imports for the data classes for each event

from openaq_producer_data import Location
from openaq_producer_data import Sensor
from openaq_producer_data import Measurement

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
        org_openaq_locations_event_producer = OrgOpenaqLocationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_openaq_locations_event_producer = OrgOpenaqLocationsEventProducer(kafka_producer, topic, 'binary')

    # ---- org.openaq.Location ----
    # TODO: Supply event data for the org.openaq.Location event
    _location = Location()

    # sends the 'org.openaq.Location' event to Kafka topic.
    await org_openaq_locations_event_producer.send_org_openaq_location(_location_id = 'TODO: replace me', data = _location)
    print(f"Sent 'org.openaq.Location' event: {_location.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_openaq_sensors_event_producer = OrgOpenaqSensorsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_openaq_sensors_event_producer = OrgOpenaqSensorsEventProducer(kafka_producer, topic, 'binary')

    # ---- org.openaq.Sensor ----
    # TODO: Supply event data for the org.openaq.Sensor event
    _sensor = Sensor()

    # sends the 'org.openaq.Sensor' event to Kafka topic.
    await org_openaq_sensors_event_producer.send_org_openaq_sensor(_location_id = 'TODO: replace me', _sensor_id = 'TODO: replace me', data = _sensor)
    print(f"Sent 'org.openaq.Sensor' event: {_sensor.to_json()}")

    # ---- org.openaq.Measurement ----
    # TODO: Supply event data for the org.openaq.Measurement event
    _measurement = Measurement()

    # sends the 'org.openaq.Measurement' event to Kafka topic.
    await org_openaq_sensors_event_producer.send_org_openaq_measurement(_location_id = 'TODO: replace me', _sensor_id = 'TODO: replace me', data = _measurement)
    print(f"Sent 'org.openaq.Measurement' event: {_measurement.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_openaq_locations_kafka_event_producer = OrgOpenaqLocationsKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_openaq_locations_kafka_event_producer = OrgOpenaqLocationsKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- org.openaq.kafka.Location ----
    # TODO: Supply event data for the org.openaq.kafka.Location event
    _location = Location()

    # sends the 'org.openaq.kafka.Location' event to Kafka topic.
    await org_openaq_locations_kafka_event_producer.send_org_openaq_kafka_location(_location_id = 'TODO: replace me', data = _location)
    print(f"Sent 'org.openaq.kafka.Location' event: {_location.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_openaq_sensors_kafka_event_producer = OrgOpenaqSensorsKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_openaq_sensors_kafka_event_producer = OrgOpenaqSensorsKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- org.openaq.kafka.Sensor ----
    # TODO: Supply event data for the org.openaq.kafka.Sensor event
    _sensor = Sensor()

    # sends the 'org.openaq.kafka.Sensor' event to Kafka topic.
    await org_openaq_sensors_kafka_event_producer.send_org_openaq_kafka_sensor(_location_id = 'TODO: replace me', _sensor_id = 'TODO: replace me', data = _sensor)
    print(f"Sent 'org.openaq.kafka.Sensor' event: {_sensor.to_json()}")

    # ---- org.openaq.kafka.Measurement ----
    # TODO: Supply event data for the org.openaq.kafka.Measurement event
    _measurement = Measurement()

    # sends the 'org.openaq.kafka.Measurement' event to Kafka topic.
    await org_openaq_sensors_kafka_event_producer.send_org_openaq_kafka_measurement(_location_id = 'TODO: replace me', _sensor_id = 'TODO: replace me', data = _measurement)
    print(f"Sent 'org.openaq.kafka.Measurement' event: {_measurement.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_openaq_locations_mqtt_event_producer = OrgOpenaqLocationsMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_openaq_locations_mqtt_event_producer = OrgOpenaqLocationsMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- org.openaq.mqtt.Location ----
    # TODO: Supply event data for the org.openaq.mqtt.Location event
    _location = Location()

    # sends the 'org.openaq.mqtt.Location' event to Kafka topic.
    await org_openaq_locations_mqtt_event_producer.send_org_openaq_mqtt_location(_location_id = 'TODO: replace me', data = _location)
    print(f"Sent 'org.openaq.mqtt.Location' event: {_location.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_openaq_sensors_mqtt_event_producer = OrgOpenaqSensorsMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_openaq_sensors_mqtt_event_producer = OrgOpenaqSensorsMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- org.openaq.mqtt.Sensor ----
    # TODO: Supply event data for the org.openaq.mqtt.Sensor event
    _sensor = Sensor()

    # sends the 'org.openaq.mqtt.Sensor' event to Kafka topic.
    await org_openaq_sensors_mqtt_event_producer.send_org_openaq_mqtt_sensor(_location_id = 'TODO: replace me', _sensor_id = 'TODO: replace me', data = _sensor)
    print(f"Sent 'org.openaq.mqtt.Sensor' event: {_sensor.to_json()}")

    # ---- org.openaq.mqtt.Measurement ----
    # TODO: Supply event data for the org.openaq.mqtt.Measurement event
    _measurement = Measurement()

    # sends the 'org.openaq.mqtt.Measurement' event to Kafka topic.
    await org_openaq_sensors_mqtt_event_producer.send_org_openaq_mqtt_measurement(_location_id = 'TODO: replace me', _sensor_id = 'TODO: replace me', data = _measurement)
    print(f"Sent 'org.openaq.mqtt.Measurement' event: {_measurement.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_openaq_locations_amqp_event_producer = OrgOpenaqLocationsAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_openaq_locations_amqp_event_producer = OrgOpenaqLocationsAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- org.openaq.amqp.Location ----
    # TODO: Supply event data for the org.openaq.amqp.Location event
    _location = Location()

    # sends the 'org.openaq.amqp.Location' event to Kafka topic.
    await org_openaq_locations_amqp_event_producer.send_org_openaq_amqp_location(_location_id = 'TODO: replace me', data = _location)
    print(f"Sent 'org.openaq.amqp.Location' event: {_location.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_openaq_sensors_amqp_event_producer = OrgOpenaqSensorsAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_openaq_sensors_amqp_event_producer = OrgOpenaqSensorsAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- org.openaq.amqp.Sensor ----
    # TODO: Supply event data for the org.openaq.amqp.Sensor event
    _sensor = Sensor()

    # sends the 'org.openaq.amqp.Sensor' event to Kafka topic.
    await org_openaq_sensors_amqp_event_producer.send_org_openaq_amqp_sensor(_location_id = 'TODO: replace me', _sensor_id = 'TODO: replace me', data = _sensor)
    print(f"Sent 'org.openaq.amqp.Sensor' event: {_sensor.to_json()}")

    # ---- org.openaq.amqp.Measurement ----
    # TODO: Supply event data for the org.openaq.amqp.Measurement event
    _measurement = Measurement()

    # sends the 'org.openaq.amqp.Measurement' event to Kafka topic.
    await org_openaq_sensors_amqp_event_producer.send_org_openaq_amqp_measurement(_location_id = 'TODO: replace me', _sensor_id = 'TODO: replace me', data = _measurement)
    print(f"Sent 'org.openaq.amqp.Measurement' event: {_measurement.to_json()}")

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