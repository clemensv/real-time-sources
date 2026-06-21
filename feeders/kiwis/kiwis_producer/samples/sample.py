
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

from kiwis_producer_kafka_producer.producer import OrgKiwisStationEventProducer
from kiwis_producer_kafka_producer.producer import OrgKiwisTimeseriesEventProducer
from kiwis_producer_kafka_producer.producer import OrgKiwisStationKafkaEventProducer
from kiwis_producer_kafka_producer.producer import OrgKiwisStationMqttEventProducer
from kiwis_producer_kafka_producer.producer import OrgKiwisStationAmqpEventProducer
from kiwis_producer_kafka_producer.producer import OrgKiwisTimeseriesKafkaEventProducer
from kiwis_producer_kafka_producer.producer import OrgKiwisTimeseriesMqttEventProducer
from kiwis_producer_kafka_producer.producer import OrgKiwisTimeseriesAmqpEventProducer

# imports for the data classes for each event

from kiwis_producer_data import Station
from kiwis_producer_data import Timeseries
from kiwis_producer_data import TimeseriesValue

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
        org_kiwis_station_event_producer = OrgKiwisStationEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_kiwis_station_event_producer = OrgKiwisStationEventProducer(kafka_producer, topic, 'binary')

    # ---- org.kiwis.Station ----
    # TODO: Supply event data for the org.kiwis.Station event
    _station = Station()

    # sends the 'org.kiwis.Station' event to Kafka topic.
    await org_kiwis_station_event_producer.send_org_kiwis_station(_base_url = 'TODO: replace me', _kiwis_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'org.kiwis.Station' event: {_station.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_kiwis_timeseries_event_producer = OrgKiwisTimeseriesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_kiwis_timeseries_event_producer = OrgKiwisTimeseriesEventProducer(kafka_producer, topic, 'binary')

    # ---- org.kiwis.Timeseries ----
    # TODO: Supply event data for the org.kiwis.Timeseries event
    _timeseries = Timeseries()

    # sends the 'org.kiwis.Timeseries' event to Kafka topic.
    await org_kiwis_timeseries_event_producer.send_org_kiwis_timeseries(_base_url = 'TODO: replace me', _kiwis_id = 'TODO: replace me', _ts_id = 'TODO: replace me', data = _timeseries)
    print(f"Sent 'org.kiwis.Timeseries' event: {_timeseries.to_json()}")

    # ---- org.kiwis.TimeseriesValue ----
    # TODO: Supply event data for the org.kiwis.TimeseriesValue event
    _timeseries_value = TimeseriesValue()

    # sends the 'org.kiwis.TimeseriesValue' event to Kafka topic.
    await org_kiwis_timeseries_event_producer.send_org_kiwis_timeseries_value(_base_url = 'TODO: replace me', _kiwis_id = 'TODO: replace me', _ts_id = 'TODO: replace me', data = _timeseries_value)
    print(f"Sent 'org.kiwis.TimeseriesValue' event: {_timeseries_value.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_kiwis_station_kafka_event_producer = OrgKiwisStationKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_kiwis_station_kafka_event_producer = OrgKiwisStationKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- org.kiwis.station.kafka.Station ----
    # TODO: Supply event data for the org.kiwis.station.kafka.Station event
    _station = Station()

    # sends the 'org.kiwis.station.kafka.Station' event to Kafka topic.
    await org_kiwis_station_kafka_event_producer.send_org_kiwis_station_kafka_station(_base_url = 'TODO: replace me', _kiwis_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'org.kiwis.station.kafka.Station' event: {_station.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_kiwis_station_mqtt_event_producer = OrgKiwisStationMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_kiwis_station_mqtt_event_producer = OrgKiwisStationMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- org.kiwis.station.mqtt.Station ----
    # TODO: Supply event data for the org.kiwis.station.mqtt.Station event
    _station = Station()

    # sends the 'org.kiwis.station.mqtt.Station' event to Kafka topic.
    await org_kiwis_station_mqtt_event_producer.send_org_kiwis_station_mqtt_station(_base_url = 'TODO: replace me', _kiwis_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'org.kiwis.station.mqtt.Station' event: {_station.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_kiwis_station_amqp_event_producer = OrgKiwisStationAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_kiwis_station_amqp_event_producer = OrgKiwisStationAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- org.kiwis.station.amqp.Station ----
    # TODO: Supply event data for the org.kiwis.station.amqp.Station event
    _station = Station()

    # sends the 'org.kiwis.station.amqp.Station' event to Kafka topic.
    await org_kiwis_station_amqp_event_producer.send_org_kiwis_station_amqp_station(_base_url = 'TODO: replace me', _kiwis_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'org.kiwis.station.amqp.Station' event: {_station.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_kiwis_timeseries_kafka_event_producer = OrgKiwisTimeseriesKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_kiwis_timeseries_kafka_event_producer = OrgKiwisTimeseriesKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- org.kiwis.timeseries.kafka.Timeseries ----
    # TODO: Supply event data for the org.kiwis.timeseries.kafka.Timeseries event
    _timeseries = Timeseries()

    # sends the 'org.kiwis.timeseries.kafka.Timeseries' event to Kafka topic.
    await org_kiwis_timeseries_kafka_event_producer.send_org_kiwis_timeseries_kafka_timeseries(_base_url = 'TODO: replace me', _kiwis_id = 'TODO: replace me', _ts_id = 'TODO: replace me', data = _timeseries)
    print(f"Sent 'org.kiwis.timeseries.kafka.Timeseries' event: {_timeseries.to_json()}")

    # ---- org.kiwis.timeseries.kafka.TimeseriesValue ----
    # TODO: Supply event data for the org.kiwis.timeseries.kafka.TimeseriesValue event
    _timeseries_value = TimeseriesValue()

    # sends the 'org.kiwis.timeseries.kafka.TimeseriesValue' event to Kafka topic.
    await org_kiwis_timeseries_kafka_event_producer.send_org_kiwis_timeseries_kafka_timeseries_value(_base_url = 'TODO: replace me', _kiwis_id = 'TODO: replace me', _ts_id = 'TODO: replace me', data = _timeseries_value)
    print(f"Sent 'org.kiwis.timeseries.kafka.TimeseriesValue' event: {_timeseries_value.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_kiwis_timeseries_mqtt_event_producer = OrgKiwisTimeseriesMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_kiwis_timeseries_mqtt_event_producer = OrgKiwisTimeseriesMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- org.kiwis.timeseries.mqtt.Timeseries ----
    # TODO: Supply event data for the org.kiwis.timeseries.mqtt.Timeseries event
    _timeseries = Timeseries()

    # sends the 'org.kiwis.timeseries.mqtt.Timeseries' event to Kafka topic.
    await org_kiwis_timeseries_mqtt_event_producer.send_org_kiwis_timeseries_mqtt_timeseries(_base_url = 'TODO: replace me', _kiwis_id = 'TODO: replace me', _ts_id = 'TODO: replace me', data = _timeseries)
    print(f"Sent 'org.kiwis.timeseries.mqtt.Timeseries' event: {_timeseries.to_json()}")

    # ---- org.kiwis.timeseries.mqtt.TimeseriesValue ----
    # TODO: Supply event data for the org.kiwis.timeseries.mqtt.TimeseriesValue event
    _timeseries_value = TimeseriesValue()

    # sends the 'org.kiwis.timeseries.mqtt.TimeseriesValue' event to Kafka topic.
    await org_kiwis_timeseries_mqtt_event_producer.send_org_kiwis_timeseries_mqtt_timeseries_value(_base_url = 'TODO: replace me', _kiwis_id = 'TODO: replace me', _ts_id = 'TODO: replace me', data = _timeseries_value)
    print(f"Sent 'org.kiwis.timeseries.mqtt.TimeseriesValue' event: {_timeseries_value.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_kiwis_timeseries_amqp_event_producer = OrgKiwisTimeseriesAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_kiwis_timeseries_amqp_event_producer = OrgKiwisTimeseriesAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- org.kiwis.timeseries.amqp.Timeseries ----
    # TODO: Supply event data for the org.kiwis.timeseries.amqp.Timeseries event
    _timeseries = Timeseries()

    # sends the 'org.kiwis.timeseries.amqp.Timeseries' event to Kafka topic.
    await org_kiwis_timeseries_amqp_event_producer.send_org_kiwis_timeseries_amqp_timeseries(_base_url = 'TODO: replace me', _kiwis_id = 'TODO: replace me', _ts_id = 'TODO: replace me', data = _timeseries)
    print(f"Sent 'org.kiwis.timeseries.amqp.Timeseries' event: {_timeseries.to_json()}")

    # ---- org.kiwis.timeseries.amqp.TimeseriesValue ----
    # TODO: Supply event data for the org.kiwis.timeseries.amqp.TimeseriesValue event
    _timeseries_value = TimeseriesValue()

    # sends the 'org.kiwis.timeseries.amqp.TimeseriesValue' event to Kafka topic.
    await org_kiwis_timeseries_amqp_event_producer.send_org_kiwis_timeseries_amqp_timeseries_value(_base_url = 'TODO: replace me', _kiwis_id = 'TODO: replace me', _ts_id = 'TODO: replace me', data = _timeseries_value)
    print(f"Sent 'org.kiwis.timeseries.amqp.TimeseriesValue' event: {_timeseries_value.to_json()}")

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