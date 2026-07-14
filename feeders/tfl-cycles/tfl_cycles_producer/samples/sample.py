
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

from tfl_cycles_producer_kafka_producer.producer import UKGovTfLCyclesStationsEventProducer
from tfl_cycles_producer_kafka_producer.producer import UKGovTfLCyclesKafkaStationsEventProducer
from tfl_cycles_producer_kafka_producer.producer import UKGovTfLCyclesMqttStationsEventProducer
from tfl_cycles_producer_kafka_producer.producer import UKGovTfLCyclesAmqpStationsEventProducer

# imports for the data classes for each event

from tfl_cycles_producer_data import StationInformation
from tfl_cycles_producer_data import StationStatus

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
        ukgov_tf_lcycles_stations_event_producer = UKGovTfLCyclesStationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ukgov_tf_lcycles_stations_event_producer = UKGovTfLCyclesStationsEventProducer(kafka_producer, topic, 'binary')

    # ---- UK.Gov.TfL.Cycles.StationInformation ----
    # TODO: Supply event data for the UK.Gov.TfL.Cycles.StationInformation event
    _station_information = StationInformation()

    # sends the 'UK.Gov.TfL.Cycles.StationInformation' event to Kafka topic.
    await ukgov_tf_lcycles_stations_event_producer.send_uk_gov_tf_l_cycles_station_information(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_information)
    print(f"Sent 'UK.Gov.TfL.Cycles.StationInformation' event: {_station_information.to_json()}")

    # ---- UK.Gov.TfL.Cycles.StationStatus ----
    # TODO: Supply event data for the UK.Gov.TfL.Cycles.StationStatus event
    _station_status = StationStatus()

    # sends the 'UK.Gov.TfL.Cycles.StationStatus' event to Kafka topic.
    await ukgov_tf_lcycles_stations_event_producer.send_uk_gov_tf_l_cycles_station_status(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_status)
    print(f"Sent 'UK.Gov.TfL.Cycles.StationStatus' event: {_station_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        ukgov_tf_lcycles_kafka_stations_event_producer = UKGovTfLCyclesKafkaStationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ukgov_tf_lcycles_kafka_stations_event_producer = UKGovTfLCyclesKafkaStationsEventProducer(kafka_producer, topic, 'binary')

    # ---- UK.Gov.TfL.Cycles.kafka.StationInformation ----
    # TODO: Supply event data for the UK.Gov.TfL.Cycles.kafka.StationInformation event
    _station_information = StationInformation()

    # sends the 'UK.Gov.TfL.Cycles.kafka.StationInformation' event to Kafka topic.
    await ukgov_tf_lcycles_kafka_stations_event_producer.send_uk_gov_tf_l_cycles_kafka_station_information(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_information)
    print(f"Sent 'UK.Gov.TfL.Cycles.kafka.StationInformation' event: {_station_information.to_json()}")

    # ---- UK.Gov.TfL.Cycles.kafka.StationStatus ----
    # TODO: Supply event data for the UK.Gov.TfL.Cycles.kafka.StationStatus event
    _station_status = StationStatus()

    # sends the 'UK.Gov.TfL.Cycles.kafka.StationStatus' event to Kafka topic.
    await ukgov_tf_lcycles_kafka_stations_event_producer.send_uk_gov_tf_l_cycles_kafka_station_status(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_status)
    print(f"Sent 'UK.Gov.TfL.Cycles.kafka.StationStatus' event: {_station_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        ukgov_tf_lcycles_mqtt_stations_event_producer = UKGovTfLCyclesMqttStationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ukgov_tf_lcycles_mqtt_stations_event_producer = UKGovTfLCyclesMqttStationsEventProducer(kafka_producer, topic, 'binary')

    # ---- UK.Gov.TfL.Cycles.mqtt.StationInformation ----
    # TODO: Supply event data for the UK.Gov.TfL.Cycles.mqtt.StationInformation event
    _station_information = StationInformation()

    # sends the 'UK.Gov.TfL.Cycles.mqtt.StationInformation' event to Kafka topic.
    await ukgov_tf_lcycles_mqtt_stations_event_producer.send_uk_gov_tf_l_cycles_mqtt_station_information(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_information)
    print(f"Sent 'UK.Gov.TfL.Cycles.mqtt.StationInformation' event: {_station_information.to_json()}")

    # ---- UK.Gov.TfL.Cycles.mqtt.StationStatus ----
    # TODO: Supply event data for the UK.Gov.TfL.Cycles.mqtt.StationStatus event
    _station_status = StationStatus()

    # sends the 'UK.Gov.TfL.Cycles.mqtt.StationStatus' event to Kafka topic.
    await ukgov_tf_lcycles_mqtt_stations_event_producer.send_uk_gov_tf_l_cycles_mqtt_station_status(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_status)
    print(f"Sent 'UK.Gov.TfL.Cycles.mqtt.StationStatus' event: {_station_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        ukgov_tf_lcycles_amqp_stations_event_producer = UKGovTfLCyclesAmqpStationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ukgov_tf_lcycles_amqp_stations_event_producer = UKGovTfLCyclesAmqpStationsEventProducer(kafka_producer, topic, 'binary')

    # ---- UK.Gov.TfL.Cycles.amqp.StationInformation ----
    # TODO: Supply event data for the UK.Gov.TfL.Cycles.amqp.StationInformation event
    _station_information = StationInformation()

    # sends the 'UK.Gov.TfL.Cycles.amqp.StationInformation' event to Kafka topic.
    await ukgov_tf_lcycles_amqp_stations_event_producer.send_uk_gov_tf_l_cycles_amqp_station_information(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_information)
    print(f"Sent 'UK.Gov.TfL.Cycles.amqp.StationInformation' event: {_station_information.to_json()}")

    # ---- UK.Gov.TfL.Cycles.amqp.StationStatus ----
    # TODO: Supply event data for the UK.Gov.TfL.Cycles.amqp.StationStatus event
    _station_status = StationStatus()

    # sends the 'UK.Gov.TfL.Cycles.amqp.StationStatus' event to Kafka topic.
    await ukgov_tf_lcycles_amqp_stations_event_producer.send_uk_gov_tf_l_cycles_amqp_station_status(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station_status)
    print(f"Sent 'UK.Gov.TfL.Cycles.amqp.StationStatus' event: {_station_status.to_json()}")

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