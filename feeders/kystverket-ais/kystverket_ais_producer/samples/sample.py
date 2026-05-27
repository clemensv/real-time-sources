
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

from kystverket_ais_producer_kafka_producer.producer import NOKystverketAISEventProducer
from kystverket_ais_producer_kafka_producer.producer import NOKystverketAISMqttEventProducer

# imports for the data classes for each event

from kystverket_ais_producer_data.positionreportclassa import PositionReportClassA
from kystverket_ais_producer_data.staticvoyagedata import StaticVoyageData
from kystverket_ais_producer_data.positionreportclassb import PositionReportClassB
from kystverket_ais_producer_data.staticdataclassb import StaticDataClassB
from kystverket_ais_producer_data.aidtonavigation import AidToNavigation
from kystverket_ais_producer_data.positionreport import PositionReport
from kystverket_ais_producer_data.shipstatic import ShipStatic

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
        nokystverket_aisevent_producer = NOKystverketAISEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nokystverket_aisevent_producer = NOKystverketAISEventProducer(kafka_producer, topic, 'binary')

    # ---- NO.Kystverket.AIS.PositionReportClassA ----
    # TODO: Supply event data for the NO.Kystverket.AIS.PositionReportClassA event
    _position_report_class_a = PositionReportClassA()

    # sends the 'NO.Kystverket.AIS.PositionReportClassA' event to Kafka topic.
    await nokystverket_aisevent_producer.send_no_kystverket_ais_position_report_class_a(_mmsi = 'TODO: replace me', data = _position_report_class_a)
    print(f"Sent 'NO.Kystverket.AIS.PositionReportClassA' event: {_position_report_class_a.to_json()}")

    # ---- NO.Kystverket.AIS.StaticVoyageData ----
    # TODO: Supply event data for the NO.Kystverket.AIS.StaticVoyageData event
    _static_voyage_data = StaticVoyageData()

    # sends the 'NO.Kystverket.AIS.StaticVoyageData' event to Kafka topic.
    await nokystverket_aisevent_producer.send_no_kystverket_ais_static_voyage_data(_mmsi = 'TODO: replace me', data = _static_voyage_data)
    print(f"Sent 'NO.Kystverket.AIS.StaticVoyageData' event: {_static_voyage_data.to_json()}")

    # ---- NO.Kystverket.AIS.PositionReportClassB ----
    # TODO: Supply event data for the NO.Kystverket.AIS.PositionReportClassB event
    _position_report_class_b = PositionReportClassB()

    # sends the 'NO.Kystverket.AIS.PositionReportClassB' event to Kafka topic.
    await nokystverket_aisevent_producer.send_no_kystverket_ais_position_report_class_b(_mmsi = 'TODO: replace me', data = _position_report_class_b)
    print(f"Sent 'NO.Kystverket.AIS.PositionReportClassB' event: {_position_report_class_b.to_json()}")

    # ---- NO.Kystverket.AIS.StaticDataClassB ----
    # TODO: Supply event data for the NO.Kystverket.AIS.StaticDataClassB event
    _static_data_class_b = StaticDataClassB()

    # sends the 'NO.Kystverket.AIS.StaticDataClassB' event to Kafka topic.
    await nokystverket_aisevent_producer.send_no_kystverket_ais_static_data_class_b(_mmsi = 'TODO: replace me', data = _static_data_class_b)
    print(f"Sent 'NO.Kystverket.AIS.StaticDataClassB' event: {_static_data_class_b.to_json()}")

    # ---- NO.Kystverket.AIS.AidToNavigation ----
    # TODO: Supply event data for the NO.Kystverket.AIS.AidToNavigation event
    _aid_to_navigation = AidToNavigation()

    # sends the 'NO.Kystverket.AIS.AidToNavigation' event to Kafka topic.
    await nokystverket_aisevent_producer.send_no_kystverket_ais_aid_to_navigation(_mmsi = 'TODO: replace me', data = _aid_to_navigation)
    print(f"Sent 'NO.Kystverket.AIS.AidToNavigation' event: {_aid_to_navigation.to_json()}")

    # ---- NO.Kystverket.AIS.PositionReport ----
    # TODO: Supply event data for the NO.Kystverket.AIS.PositionReport event
    _position_report = PositionReport()

    # sends the 'NO.Kystverket.AIS.PositionReport' event to Kafka topic.
    await nokystverket_aisevent_producer.send_no_kystverket_ais_position_report(_mmsi = 'TODO: replace me', data = _position_report)
    print(f"Sent 'NO.Kystverket.AIS.PositionReport' event: {_position_report.to_json()}")

    # ---- NO.Kystverket.AIS.ShipStatic ----
    # TODO: Supply event data for the NO.Kystverket.AIS.ShipStatic event
    _ship_static = ShipStatic()

    # sends the 'NO.Kystverket.AIS.ShipStatic' event to Kafka topic.
    await nokystverket_aisevent_producer.send_no_kystverket_ais_ship_static(_mmsi = 'TODO: replace me', data = _ship_static)
    print(f"Sent 'NO.Kystverket.AIS.ShipStatic' event: {_ship_static.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nokystverket_aismqtt_event_producer = NOKystverketAISMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nokystverket_aismqtt_event_producer = NOKystverketAISMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- NO.Kystverket.AIS.mqtt.PositionReport ----
    # TODO: Supply event data for the NO.Kystverket.AIS.mqtt.PositionReport event
    _position_report = PositionReport()

    # sends the 'NO.Kystverket.AIS.mqtt.PositionReport' event to Kafka topic.
    await nokystverket_aismqtt_event_producer.send_no_kystverket_ais_mqtt_position_report(_mmsi = 'TODO: replace me', data = _position_report)
    print(f"Sent 'NO.Kystverket.AIS.mqtt.PositionReport' event: {_position_report.to_json()}")

    # ---- NO.Kystverket.AIS.mqtt.ShipStatic ----
    # TODO: Supply event data for the NO.Kystverket.AIS.mqtt.ShipStatic event
    _ship_static = ShipStatic()

    # sends the 'NO.Kystverket.AIS.mqtt.ShipStatic' event to Kafka topic.
    await nokystverket_aismqtt_event_producer.send_no_kystverket_ais_mqtt_ship_static(_mmsi = 'TODO: replace me', data = _ship_static)
    print(f"Sent 'NO.Kystverket.AIS.mqtt.ShipStatic' event: {_ship_static.to_json()}")

    # ---- NO.Kystverket.AIS.mqtt.AidToNavigation ----
    # TODO: Supply event data for the NO.Kystverket.AIS.mqtt.AidToNavigation event
    _aid_to_navigation = AidToNavigation()

    # sends the 'NO.Kystverket.AIS.mqtt.AidToNavigation' event to Kafka topic.
    await nokystverket_aismqtt_event_producer.send_no_kystverket_ais_mqtt_aid_to_navigation(_mmsi = 'TODO: replace me', data = _aid_to_navigation)
    print(f"Sent 'NO.Kystverket.AIS.mqtt.AidToNavigation' event: {_aid_to_navigation.to_json()}")

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