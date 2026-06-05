
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

from gbfs_bikeshare_producer_kafka_producer.producer import OrgGbfsSystemEventProducer
from gbfs_bikeshare_producer_kafka_producer.producer import OrgGbfsStationsEventProducer
from gbfs_bikeshare_producer_kafka_producer.producer import OrgGbfsFreeBikesEventProducer
from gbfs_bikeshare_producer_kafka_producer.producer import OrgGbfsKafkaSystemEventProducer
from gbfs_bikeshare_producer_kafka_producer.producer import OrgGbfsKafkaStationsEventProducer
from gbfs_bikeshare_producer_kafka_producer.producer import OrgGbfsKafkaFreeBikesEventProducer
from gbfs_bikeshare_producer_kafka_producer.producer import OrgGbfsMqttSystemEventProducer
from gbfs_bikeshare_producer_kafka_producer.producer import OrgGbfsMqttStationsEventProducer
from gbfs_bikeshare_producer_kafka_producer.producer import OrgGbfsMqttFreeBikesEventProducer
from gbfs_bikeshare_producer_kafka_producer.producer import OrgGbfsAmqpSystemEventProducer
from gbfs_bikeshare_producer_kafka_producer.producer import OrgGbfsAmqpStationsEventProducer
from gbfs_bikeshare_producer_kafka_producer.producer import OrgGbfsAmqpFreeBikesEventProducer

# imports for the data classes for each event

from gbfs_bikeshare_producer_data.systeminformation import SystemInformation
from gbfs_bikeshare_producer_data.stationinformation import StationInformation
from gbfs_bikeshare_producer_data.stationstatus import StationStatus
from gbfs_bikeshare_producer_data.freebikestatus import FreeBikeStatus

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
        org_gbfs_system_event_producer = OrgGbfsSystemEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_gbfs_system_event_producer = OrgGbfsSystemEventProducer(kafka_producer, topic, 'binary')

    # ---- org.gbfs.SystemInformation ----
    # TODO: Supply event data for the org.gbfs.SystemInformation event
    _system_information = SystemInformation()

    # sends the 'org.gbfs.SystemInformation' event to Kafka topic.
    await org_gbfs_system_event_producer.send_org_gbfs_system_information(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', data = _system_information)
    print(f"Sent 'org.gbfs.SystemInformation' event: {_system_information.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_gbfs_stations_event_producer = OrgGbfsStationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_gbfs_stations_event_producer = OrgGbfsStationsEventProducer(kafka_producer, topic, 'binary')

    # ---- org.gbfs.StationInformation ----
    # TODO: Supply event data for the org.gbfs.StationInformation event
    _station_information = StationInformation()

    # sends the 'org.gbfs.StationInformation' event to Kafka topic.
    await org_gbfs_stations_event_producer.send_org_gbfs_station_information(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_information)
    print(f"Sent 'org.gbfs.StationInformation' event: {_station_information.to_json()}")

    # ---- org.gbfs.StationStatus ----
    # TODO: Supply event data for the org.gbfs.StationStatus event
    _station_status = StationStatus()

    # sends the 'org.gbfs.StationStatus' event to Kafka topic.
    await org_gbfs_stations_event_producer.send_org_gbfs_station_status(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_status)
    print(f"Sent 'org.gbfs.StationStatus' event: {_station_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_gbfs_free_bikes_event_producer = OrgGbfsFreeBikesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_gbfs_free_bikes_event_producer = OrgGbfsFreeBikesEventProducer(kafka_producer, topic, 'binary')

    # ---- org.gbfs.FreeBikeStatus ----
    # TODO: Supply event data for the org.gbfs.FreeBikeStatus event
    _free_bike_status = FreeBikeStatus()

    # sends the 'org.gbfs.FreeBikeStatus' event to Kafka topic.
    await org_gbfs_free_bikes_event_producer.send_org_gbfs_free_bike_status(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', _bike_id = 'TODO: replace me', data = _free_bike_status)
    print(f"Sent 'org.gbfs.FreeBikeStatus' event: {_free_bike_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_gbfs_kafka_system_event_producer = OrgGbfsKafkaSystemEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_gbfs_kafka_system_event_producer = OrgGbfsKafkaSystemEventProducer(kafka_producer, topic, 'binary')

    # ---- org.gbfs.kafka.SystemInformation ----
    # TODO: Supply event data for the org.gbfs.kafka.SystemInformation event
    _system_information = SystemInformation()

    # sends the 'org.gbfs.kafka.SystemInformation' event to Kafka topic.
    await org_gbfs_kafka_system_event_producer.send_org_gbfs_kafka_system_information(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', data = _system_information)
    print(f"Sent 'org.gbfs.kafka.SystemInformation' event: {_system_information.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_gbfs_kafka_stations_event_producer = OrgGbfsKafkaStationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_gbfs_kafka_stations_event_producer = OrgGbfsKafkaStationsEventProducer(kafka_producer, topic, 'binary')

    # ---- org.gbfs.kafka.StationInformation ----
    # TODO: Supply event data for the org.gbfs.kafka.StationInformation event
    _station_information = StationInformation()

    # sends the 'org.gbfs.kafka.StationInformation' event to Kafka topic.
    await org_gbfs_kafka_stations_event_producer.send_org_gbfs_kafka_station_information(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_information)
    print(f"Sent 'org.gbfs.kafka.StationInformation' event: {_station_information.to_json()}")

    # ---- org.gbfs.kafka.StationStatus ----
    # TODO: Supply event data for the org.gbfs.kafka.StationStatus event
    _station_status = StationStatus()

    # sends the 'org.gbfs.kafka.StationStatus' event to Kafka topic.
    await org_gbfs_kafka_stations_event_producer.send_org_gbfs_kafka_station_status(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_status)
    print(f"Sent 'org.gbfs.kafka.StationStatus' event: {_station_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_gbfs_kafka_free_bikes_event_producer = OrgGbfsKafkaFreeBikesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_gbfs_kafka_free_bikes_event_producer = OrgGbfsKafkaFreeBikesEventProducer(kafka_producer, topic, 'binary')

    # ---- org.gbfs.kafka.FreeBikeStatus ----
    # TODO: Supply event data for the org.gbfs.kafka.FreeBikeStatus event
    _free_bike_status = FreeBikeStatus()

    # sends the 'org.gbfs.kafka.FreeBikeStatus' event to Kafka topic.
    await org_gbfs_kafka_free_bikes_event_producer.send_org_gbfs_kafka_free_bike_status(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', _bike_id = 'TODO: replace me', data = _free_bike_status)
    print(f"Sent 'org.gbfs.kafka.FreeBikeStatus' event: {_free_bike_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_gbfs_mqtt_system_event_producer = OrgGbfsMqttSystemEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_gbfs_mqtt_system_event_producer = OrgGbfsMqttSystemEventProducer(kafka_producer, topic, 'binary')

    # ---- org.gbfs.mqtt.SystemInformation ----
    # TODO: Supply event data for the org.gbfs.mqtt.SystemInformation event
    _system_information = SystemInformation()

    # sends the 'org.gbfs.mqtt.SystemInformation' event to Kafka topic.
    await org_gbfs_mqtt_system_event_producer.send_org_gbfs_mqtt_system_information(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', data = _system_information)
    print(f"Sent 'org.gbfs.mqtt.SystemInformation' event: {_system_information.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_gbfs_mqtt_stations_event_producer = OrgGbfsMqttStationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_gbfs_mqtt_stations_event_producer = OrgGbfsMqttStationsEventProducer(kafka_producer, topic, 'binary')

    # ---- org.gbfs.mqtt.StationInformation ----
    # TODO: Supply event data for the org.gbfs.mqtt.StationInformation event
    _station_information = StationInformation()

    # sends the 'org.gbfs.mqtt.StationInformation' event to Kafka topic.
    await org_gbfs_mqtt_stations_event_producer.send_org_gbfs_mqtt_station_information(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_information)
    print(f"Sent 'org.gbfs.mqtt.StationInformation' event: {_station_information.to_json()}")

    # ---- org.gbfs.mqtt.StationStatus ----
    # TODO: Supply event data for the org.gbfs.mqtt.StationStatus event
    _station_status = StationStatus()

    # sends the 'org.gbfs.mqtt.StationStatus' event to Kafka topic.
    await org_gbfs_mqtt_stations_event_producer.send_org_gbfs_mqtt_station_status(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_status)
    print(f"Sent 'org.gbfs.mqtt.StationStatus' event: {_station_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_gbfs_mqtt_free_bikes_event_producer = OrgGbfsMqttFreeBikesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_gbfs_mqtt_free_bikes_event_producer = OrgGbfsMqttFreeBikesEventProducer(kafka_producer, topic, 'binary')

    # ---- org.gbfs.mqtt.FreeBikeStatus ----
    # TODO: Supply event data for the org.gbfs.mqtt.FreeBikeStatus event
    _free_bike_status = FreeBikeStatus()

    # sends the 'org.gbfs.mqtt.FreeBikeStatus' event to Kafka topic.
    await org_gbfs_mqtt_free_bikes_event_producer.send_org_gbfs_mqtt_free_bike_status(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', _bike_id = 'TODO: replace me', data = _free_bike_status)
    print(f"Sent 'org.gbfs.mqtt.FreeBikeStatus' event: {_free_bike_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_gbfs_amqp_system_event_producer = OrgGbfsAmqpSystemEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_gbfs_amqp_system_event_producer = OrgGbfsAmqpSystemEventProducer(kafka_producer, topic, 'binary')

    # ---- org.gbfs.amqp.SystemInformation ----
    # TODO: Supply event data for the org.gbfs.amqp.SystemInformation event
    _system_information = SystemInformation()

    # sends the 'org.gbfs.amqp.SystemInformation' event to Kafka topic.
    await org_gbfs_amqp_system_event_producer.send_org_gbfs_amqp_system_information(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', data = _system_information)
    print(f"Sent 'org.gbfs.amqp.SystemInformation' event: {_system_information.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_gbfs_amqp_stations_event_producer = OrgGbfsAmqpStationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_gbfs_amqp_stations_event_producer = OrgGbfsAmqpStationsEventProducer(kafka_producer, topic, 'binary')

    # ---- org.gbfs.amqp.StationInformation ----
    # TODO: Supply event data for the org.gbfs.amqp.StationInformation event
    _station_information = StationInformation()

    # sends the 'org.gbfs.amqp.StationInformation' event to Kafka topic.
    await org_gbfs_amqp_stations_event_producer.send_org_gbfs_amqp_station_information(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_information)
    print(f"Sent 'org.gbfs.amqp.StationInformation' event: {_station_information.to_json()}")

    # ---- org.gbfs.amqp.StationStatus ----
    # TODO: Supply event data for the org.gbfs.amqp.StationStatus event
    _station_status = StationStatus()

    # sends the 'org.gbfs.amqp.StationStatus' event to Kafka topic.
    await org_gbfs_amqp_stations_event_producer.send_org_gbfs_amqp_station_status(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_status)
    print(f"Sent 'org.gbfs.amqp.StationStatus' event: {_station_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_gbfs_amqp_free_bikes_event_producer = OrgGbfsAmqpFreeBikesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_gbfs_amqp_free_bikes_event_producer = OrgGbfsAmqpFreeBikesEventProducer(kafka_producer, topic, 'binary')

    # ---- org.gbfs.amqp.FreeBikeStatus ----
    # TODO: Supply event data for the org.gbfs.amqp.FreeBikeStatus event
    _free_bike_status = FreeBikeStatus()

    # sends the 'org.gbfs.amqp.FreeBikeStatus' event to Kafka topic.
    await org_gbfs_amqp_free_bikes_event_producer.send_org_gbfs_amqp_free_bike_status(_feed_url = 'TODO: replace me', _system_id = 'TODO: replace me', _bike_id = 'TODO: replace me', data = _free_bike_status)
    print(f"Sent 'org.gbfs.amqp.FreeBikeStatus' event: {_free_bike_status.to_json()}")

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