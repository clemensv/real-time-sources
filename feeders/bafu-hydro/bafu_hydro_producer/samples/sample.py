
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

from bafu_hydro_producer_kafka_producer.producer import CHBAFUHydrologyEventProducer
from bafu_hydro_producer_kafka_producer.producer import CHBAFUHydrologyMqttEventProducer
from bafu_hydro_producer_kafka_producer.producer import CHBAFUHydrologyAmqpEventProducer

# imports for the data classes for each event

from bafu_hydro_producer_data import Station
from bafu_hydro_producer_data import WaterLevelObservation

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
        chbafuhydrology_event_producer = CHBAFUHydrologyEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        chbafuhydrology_event_producer = CHBAFUHydrologyEventProducer(kafka_producer, topic, 'binary')

    # ---- CH.BAFU.Hydrology.Station ----
    # TODO: Supply event data for the CH.BAFU.Hydrology.Station event
    _station = Station()

    # sends the 'CH.BAFU.Hydrology.Station' event to Kafka topic.
    await chbafuhydrology_event_producer.send_ch_bafu_hydrology_station(_station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'CH.BAFU.Hydrology.Station' event: {_station.to_json()}")

    # ---- CH.BAFU.Hydrology.WaterLevelObservation ----
    # TODO: Supply event data for the CH.BAFU.Hydrology.WaterLevelObservation event
    _water_level_observation = WaterLevelObservation()

    # sends the 'CH.BAFU.Hydrology.WaterLevelObservation' event to Kafka topic.
    await chbafuhydrology_event_producer.send_ch_bafu_hydrology_water_level_observation(_station_id = 'TODO: replace me', data = _water_level_observation)
    print(f"Sent 'CH.BAFU.Hydrology.WaterLevelObservation' event: {_water_level_observation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        chbafuhydrology_mqtt_event_producer = CHBAFUHydrologyMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        chbafuhydrology_mqtt_event_producer = CHBAFUHydrologyMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- CH.BAFU.Hydrology.mqtt.Station ----
    # TODO: Supply event data for the CH.BAFU.Hydrology.mqtt.Station event
    _station = Station()

    # sends the 'CH.BAFU.Hydrology.mqtt.Station' event to Kafka topic.
    await chbafuhydrology_mqtt_event_producer.send_ch_bafu_hydrology_mqtt_station(_station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'CH.BAFU.Hydrology.mqtt.Station' event: {_station.to_json()}")

    # ---- CH.BAFU.Hydrology.mqtt.WaterLevelObservation ----
    # TODO: Supply event data for the CH.BAFU.Hydrology.mqtt.WaterLevelObservation event
    _water_level_observation = WaterLevelObservation()

    # sends the 'CH.BAFU.Hydrology.mqtt.WaterLevelObservation' event to Kafka topic.
    await chbafuhydrology_mqtt_event_producer.send_ch_bafu_hydrology_mqtt_water_level_observation(_station_id = 'TODO: replace me', data = _water_level_observation)
    print(f"Sent 'CH.BAFU.Hydrology.mqtt.WaterLevelObservation' event: {_water_level_observation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        chbafuhydrology_amqp_event_producer = CHBAFUHydrologyAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        chbafuhydrology_amqp_event_producer = CHBAFUHydrologyAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- CH.BAFU.Hydrology.amqp.Station ----
    # TODO: Supply event data for the CH.BAFU.Hydrology.amqp.Station event
    _station = Station()

    # sends the 'CH.BAFU.Hydrology.amqp.Station' event to Kafka topic.
    await chbafuhydrology_amqp_event_producer.send_ch_bafu_hydrology_amqp_station(_station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'CH.BAFU.Hydrology.amqp.Station' event: {_station.to_json()}")

    # ---- CH.BAFU.Hydrology.amqp.WaterLevelObservation ----
    # TODO: Supply event data for the CH.BAFU.Hydrology.amqp.WaterLevelObservation event
    _water_level_observation = WaterLevelObservation()

    # sends the 'CH.BAFU.Hydrology.amqp.WaterLevelObservation' event to Kafka topic.
    await chbafuhydrology_amqp_event_producer.send_ch_bafu_hydrology_amqp_water_level_observation(_station_id = 'TODO: replace me', data = _water_level_observation)
    print(f"Sent 'CH.BAFU.Hydrology.amqp.WaterLevelObservation' event: {_water_level_observation.to_json()}")

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