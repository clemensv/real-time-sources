
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

from aviationweather_producer_kafka_producer.producer import GovNoaaAviationweatherEventProducer
from aviationweather_producer_kafka_producer.producer import GovNoaaAviationweatherMqttEventProducer
from aviationweather_producer_kafka_producer.producer import GovNoaaAviationweatherAmqpEventProducer

# imports for the data classes for each event

from aviationweather_producer_data import Station
from aviationweather_producer_data import Metar
from aviationweather_producer_data import Sigmet

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
        gov_noaa_aviationweather_event_producer = GovNoaaAviationweatherEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        gov_noaa_aviationweather_event_producer = GovNoaaAviationweatherEventProducer(kafka_producer, topic, 'binary')

    # ---- gov.noaa.aviationweather.Station ----
    # TODO: Supply event data for the gov.noaa.aviationweather.Station event
    _station = Station()

    # sends the 'gov.noaa.aviationweather.Station' event to Kafka topic.
    await gov_noaa_aviationweather_event_producer.send_gov_noaa_aviationweather_station(_icao_id = 'TODO: replace me', data = _station)
    print(f"Sent 'gov.noaa.aviationweather.Station' event: {_station.to_json()}")

    # ---- gov.noaa.aviationweather.Metar ----
    # TODO: Supply event data for the gov.noaa.aviationweather.Metar event
    _metar = Metar()

    # sends the 'gov.noaa.aviationweather.Metar' event to Kafka topic.
    await gov_noaa_aviationweather_event_producer.send_gov_noaa_aviationweather_metar(_icao_id = 'TODO: replace me', data = _metar)
    print(f"Sent 'gov.noaa.aviationweather.Metar' event: {_metar.to_json()}")

    # ---- gov.noaa.aviationweather.Sigmet ----
    # TODO: Supply event data for the gov.noaa.aviationweather.Sigmet event
    _sigmet = Sigmet()

    # sends the 'gov.noaa.aviationweather.Sigmet' event to Kafka topic.
    await gov_noaa_aviationweather_event_producer.send_gov_noaa_aviationweather_sigmet(_icao_id = 'TODO: replace me', data = _sigmet)
    print(f"Sent 'gov.noaa.aviationweather.Sigmet' event: {_sigmet.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        gov_noaa_aviationweather_mqtt_event_producer = GovNoaaAviationweatherMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        gov_noaa_aviationweather_mqtt_event_producer = GovNoaaAviationweatherMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- gov.noaa.aviationweather.mqtt.Station ----
    # TODO: Supply event data for the gov.noaa.aviationweather.mqtt.Station event
    _station = Station()

    # sends the 'gov.noaa.aviationweather.mqtt.Station' event to Kafka topic.
    await gov_noaa_aviationweather_mqtt_event_producer.send_gov_noaa_aviationweather_mqtt_station(_icao_id = 'TODO: replace me', data = _station)
    print(f"Sent 'gov.noaa.aviationweather.mqtt.Station' event: {_station.to_json()}")

    # ---- gov.noaa.aviationweather.mqtt.Metar ----
    # TODO: Supply event data for the gov.noaa.aviationweather.mqtt.Metar event
    _metar = Metar()

    # sends the 'gov.noaa.aviationweather.mqtt.Metar' event to Kafka topic.
    await gov_noaa_aviationweather_mqtt_event_producer.send_gov_noaa_aviationweather_mqtt_metar(_icao_id = 'TODO: replace me', data = _metar)
    print(f"Sent 'gov.noaa.aviationweather.mqtt.Metar' event: {_metar.to_json()}")

    # ---- gov.noaa.aviationweather.mqtt.Sigmet ----
    # TODO: Supply event data for the gov.noaa.aviationweather.mqtt.Sigmet event
    _sigmet = Sigmet()

    # sends the 'gov.noaa.aviationweather.mqtt.Sigmet' event to Kafka topic.
    await gov_noaa_aviationweather_mqtt_event_producer.send_gov_noaa_aviationweather_mqtt_sigmet(_region = 'TODO: replace me', _sigmet_id = 'TODO: replace me', data = _sigmet)
    print(f"Sent 'gov.noaa.aviationweather.mqtt.Sigmet' event: {_sigmet.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        gov_noaa_aviationweather_amqp_event_producer = GovNoaaAviationweatherAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        gov_noaa_aviationweather_amqp_event_producer = GovNoaaAviationweatherAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- gov.noaa.aviationweather.amqp.Station ----
    # TODO: Supply event data for the gov.noaa.aviationweather.amqp.Station event
    _station = Station()

    # sends the 'gov.noaa.aviationweather.amqp.Station' event to Kafka topic.
    await gov_noaa_aviationweather_amqp_event_producer.send_gov_noaa_aviationweather_amqp_station(_icao_id = 'TODO: replace me', data = _station)
    print(f"Sent 'gov.noaa.aviationweather.amqp.Station' event: {_station.to_json()}")

    # ---- gov.noaa.aviationweather.amqp.Metar ----
    # TODO: Supply event data for the gov.noaa.aviationweather.amqp.Metar event
    _metar = Metar()

    # sends the 'gov.noaa.aviationweather.amqp.Metar' event to Kafka topic.
    await gov_noaa_aviationweather_amqp_event_producer.send_gov_noaa_aviationweather_amqp_metar(_icao_id = 'TODO: replace me', data = _metar)
    print(f"Sent 'gov.noaa.aviationweather.amqp.Metar' event: {_metar.to_json()}")

    # ---- gov.noaa.aviationweather.amqp.Sigmet ----
    # TODO: Supply event data for the gov.noaa.aviationweather.amqp.Sigmet event
    _sigmet = Sigmet()

    # sends the 'gov.noaa.aviationweather.amqp.Sigmet' event to Kafka topic.
    await gov_noaa_aviationweather_amqp_event_producer.send_gov_noaa_aviationweather_amqp_sigmet(_region = 'TODO: replace me', _sigmet_id = 'TODO: replace me', data = _sigmet)
    print(f"Sent 'gov.noaa.aviationweather.amqp.Sigmet' event: {_sigmet.to_json()}")

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