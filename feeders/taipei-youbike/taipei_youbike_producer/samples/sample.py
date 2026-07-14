
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

from taipei_youbike_producer_kafka_producer.producer import TWYouBikeStationsEventProducer
from taipei_youbike_producer_kafka_producer.producer import TWYouBikeKafkaStationsEventProducer
from taipei_youbike_producer_kafka_producer.producer import TWYouBikeMqttStationsEventProducer
from taipei_youbike_producer_kafka_producer.producer import TWYouBikeAmqpStationsEventProducer

# imports for the data classes for each event

from taipei_youbike_producer_data import StationInformation
from taipei_youbike_producer_data import StationStatus

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
        twyou_bike_stations_event_producer = TWYouBikeStationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        twyou_bike_stations_event_producer = TWYouBikeStationsEventProducer(kafka_producer, topic, 'binary')

    # ---- TW.YouBike.StationInformation ----
    # TODO: Supply event data for the TW.YouBike.StationInformation event
    _station_information = StationInformation()

    # sends the 'TW.YouBike.StationInformation' event to Kafka topic.
    await twyou_bike_stations_event_producer.send_tw_you_bike_station_information(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_information)
    print(f"Sent 'TW.YouBike.StationInformation' event: {_station_information.to_json()}")

    # ---- TW.YouBike.StationStatus ----
    # TODO: Supply event data for the TW.YouBike.StationStatus event
    _station_status = StationStatus()

    # sends the 'TW.YouBike.StationStatus' event to Kafka topic.
    await twyou_bike_stations_event_producer.send_tw_you_bike_station_status(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_status)
    print(f"Sent 'TW.YouBike.StationStatus' event: {_station_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        twyou_bike_kafka_stations_event_producer = TWYouBikeKafkaStationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        twyou_bike_kafka_stations_event_producer = TWYouBikeKafkaStationsEventProducer(kafka_producer, topic, 'binary')

    # ---- TW.YouBike.kafka.StationInformation ----
    # TODO: Supply event data for the TW.YouBike.kafka.StationInformation event
    _station_information = StationInformation()

    # sends the 'TW.YouBike.kafka.StationInformation' event to Kafka topic.
    await twyou_bike_kafka_stations_event_producer.send_tw_you_bike_kafka_station_information(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_information)
    print(f"Sent 'TW.YouBike.kafka.StationInformation' event: {_station_information.to_json()}")

    # ---- TW.YouBike.kafka.StationStatus ----
    # TODO: Supply event data for the TW.YouBike.kafka.StationStatus event
    _station_status = StationStatus()

    # sends the 'TW.YouBike.kafka.StationStatus' event to Kafka topic.
    await twyou_bike_kafka_stations_event_producer.send_tw_you_bike_kafka_station_status(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_status)
    print(f"Sent 'TW.YouBike.kafka.StationStatus' event: {_station_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        twyou_bike_mqtt_stations_event_producer = TWYouBikeMqttStationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        twyou_bike_mqtt_stations_event_producer = TWYouBikeMqttStationsEventProducer(kafka_producer, topic, 'binary')

    # ---- TW.YouBike.mqtt.StationInformation ----
    # TODO: Supply event data for the TW.YouBike.mqtt.StationInformation event
    _station_information = StationInformation()

    # sends the 'TW.YouBike.mqtt.StationInformation' event to Kafka topic.
    await twyou_bike_mqtt_stations_event_producer.send_tw_you_bike_mqtt_station_information(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_information)
    print(f"Sent 'TW.YouBike.mqtt.StationInformation' event: {_station_information.to_json()}")

    # ---- TW.YouBike.mqtt.StationStatus ----
    # TODO: Supply event data for the TW.YouBike.mqtt.StationStatus event
    _station_status = StationStatus()

    # sends the 'TW.YouBike.mqtt.StationStatus' event to Kafka topic.
    await twyou_bike_mqtt_stations_event_producer.send_tw_you_bike_mqtt_station_status(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_status)
    print(f"Sent 'TW.YouBike.mqtt.StationStatus' event: {_station_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        twyou_bike_amqp_stations_event_producer = TWYouBikeAmqpStationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        twyou_bike_amqp_stations_event_producer = TWYouBikeAmqpStationsEventProducer(kafka_producer, topic, 'binary')

    # ---- TW.YouBike.amqp.StationInformation ----
    # TODO: Supply event data for the TW.YouBike.amqp.StationInformation event
    _station_information = StationInformation()

    # sends the 'TW.YouBike.amqp.StationInformation' event to Kafka topic.
    await twyou_bike_amqp_stations_event_producer.send_tw_you_bike_amqp_station_information(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_information)
    print(f"Sent 'TW.YouBike.amqp.StationInformation' event: {_station_information.to_json()}")

    # ---- TW.YouBike.amqp.StationStatus ----
    # TODO: Supply event data for the TW.YouBike.amqp.StationStatus event
    _station_status = StationStatus()

    # sends the 'TW.YouBike.amqp.StationStatus' event to Kafka topic.
    await twyou_bike_amqp_stations_event_producer.send_tw_you_bike_amqp_station_status(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_status)
    print(f"Sent 'TW.YouBike.amqp.StationStatus' event: {_station_status.to_json()}")

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