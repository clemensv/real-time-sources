
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

from open_charge_map_producer_kafka_producer.producer import IOOpenChargeMapLocationsEventProducer
from open_charge_map_producer_kafka_producer.producer import IOOpenChargeMapReferenceEventProducer
from open_charge_map_producer_kafka_producer.producer import IOOpenChargeMapLocationsMqttEventProducer
from open_charge_map_producer_kafka_producer.producer import IOOpenChargeMapReferenceMqttEventProducer
from open_charge_map_producer_kafka_producer.producer import IOOpenChargeMapLocationsAmqpEventProducer
from open_charge_map_producer_kafka_producer.producer import IOOpenChargeMapReferenceAmqpEventProducer

# imports for the data classes for each event

from open_charge_map_producer_data import ChargingLocation
from open_charge_map_producer_data import Operator
from open_charge_map_producer_data import ConnectionType
from open_charge_map_producer_data import CurrentType
from open_charge_map_producer_data import ChargerType
from open_charge_map_producer_data import Country
from open_charge_map_producer_data import DataProvider
from open_charge_map_producer_data import StatusType
from open_charge_map_producer_data import UsageType
from open_charge_map_producer_data import SubmissionStatusType

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
        ioopen_charge_map_locations_event_producer = IOOpenChargeMapLocationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ioopen_charge_map_locations_event_producer = IOOpenChargeMapLocationsEventProducer(kafka_producer, topic, 'binary')

    # ---- IO.OpenChargeMap.ChargingLocation ----
    # TODO: Supply event data for the IO.OpenChargeMap.ChargingLocation event
    _charging_location = ChargingLocation()

    # sends the 'IO.OpenChargeMap.ChargingLocation' event to Kafka topic.
    await ioopen_charge_map_locations_event_producer.send_io_open_charge_map_charging_location(_feedurl = 'TODO: replace me', _poi_id = 'TODO: replace me', data = _charging_location)
    print(f"Sent 'IO.OpenChargeMap.ChargingLocation' event: {_charging_location.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        ioopen_charge_map_reference_event_producer = IOOpenChargeMapReferenceEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ioopen_charge_map_reference_event_producer = IOOpenChargeMapReferenceEventProducer(kafka_producer, topic, 'binary')

    # ---- IO.OpenChargeMap.Operator ----
    # TODO: Supply event data for the IO.OpenChargeMap.Operator event
    _operator = Operator()

    # sends the 'IO.OpenChargeMap.Operator' event to Kafka topic.
    await ioopen_charge_map_reference_event_producer.send_io_open_charge_map_operator(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _operator)
    print(f"Sent 'IO.OpenChargeMap.Operator' event: {_operator.to_json()}")

    # ---- IO.OpenChargeMap.ConnectionType ----
    # TODO: Supply event data for the IO.OpenChargeMap.ConnectionType event
    _connection_type = ConnectionType()

    # sends the 'IO.OpenChargeMap.ConnectionType' event to Kafka topic.
    await ioopen_charge_map_reference_event_producer.send_io_open_charge_map_connection_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _connection_type)
    print(f"Sent 'IO.OpenChargeMap.ConnectionType' event: {_connection_type.to_json()}")

    # ---- IO.OpenChargeMap.CurrentType ----
    # TODO: Supply event data for the IO.OpenChargeMap.CurrentType event
    _current_type = CurrentType()

    # sends the 'IO.OpenChargeMap.CurrentType' event to Kafka topic.
    await ioopen_charge_map_reference_event_producer.send_io_open_charge_map_current_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _current_type)
    print(f"Sent 'IO.OpenChargeMap.CurrentType' event: {_current_type.to_json()}")

    # ---- IO.OpenChargeMap.ChargerType ----
    # TODO: Supply event data for the IO.OpenChargeMap.ChargerType event
    _charger_type = ChargerType()

    # sends the 'IO.OpenChargeMap.ChargerType' event to Kafka topic.
    await ioopen_charge_map_reference_event_producer.send_io_open_charge_map_charger_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _charger_type)
    print(f"Sent 'IO.OpenChargeMap.ChargerType' event: {_charger_type.to_json()}")

    # ---- IO.OpenChargeMap.Country ----
    # TODO: Supply event data for the IO.OpenChargeMap.Country event
    _country = Country()

    # sends the 'IO.OpenChargeMap.Country' event to Kafka topic.
    await ioopen_charge_map_reference_event_producer.send_io_open_charge_map_country(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _country)
    print(f"Sent 'IO.OpenChargeMap.Country' event: {_country.to_json()}")

    # ---- IO.OpenChargeMap.DataProvider ----
    # TODO: Supply event data for the IO.OpenChargeMap.DataProvider event
    _data_provider = DataProvider()

    # sends the 'IO.OpenChargeMap.DataProvider' event to Kafka topic.
    await ioopen_charge_map_reference_event_producer.send_io_open_charge_map_data_provider(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _data_provider)
    print(f"Sent 'IO.OpenChargeMap.DataProvider' event: {_data_provider.to_json()}")

    # ---- IO.OpenChargeMap.StatusType ----
    # TODO: Supply event data for the IO.OpenChargeMap.StatusType event
    _status_type = StatusType()

    # sends the 'IO.OpenChargeMap.StatusType' event to Kafka topic.
    await ioopen_charge_map_reference_event_producer.send_io_open_charge_map_status_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _status_type)
    print(f"Sent 'IO.OpenChargeMap.StatusType' event: {_status_type.to_json()}")

    # ---- IO.OpenChargeMap.UsageType ----
    # TODO: Supply event data for the IO.OpenChargeMap.UsageType event
    _usage_type = UsageType()

    # sends the 'IO.OpenChargeMap.UsageType' event to Kafka topic.
    await ioopen_charge_map_reference_event_producer.send_io_open_charge_map_usage_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _usage_type)
    print(f"Sent 'IO.OpenChargeMap.UsageType' event: {_usage_type.to_json()}")

    # ---- IO.OpenChargeMap.SubmissionStatusType ----
    # TODO: Supply event data for the IO.OpenChargeMap.SubmissionStatusType event
    _submission_status_type = SubmissionStatusType()

    # sends the 'IO.OpenChargeMap.SubmissionStatusType' event to Kafka topic.
    await ioopen_charge_map_reference_event_producer.send_io_open_charge_map_submission_status_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _submission_status_type)
    print(f"Sent 'IO.OpenChargeMap.SubmissionStatusType' event: {_submission_status_type.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        ioopen_charge_map_locations_mqtt_event_producer = IOOpenChargeMapLocationsMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ioopen_charge_map_locations_mqtt_event_producer = IOOpenChargeMapLocationsMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- IO.OpenChargeMap.mqtt.ChargingLocation ----
    # TODO: Supply event data for the IO.OpenChargeMap.mqtt.ChargingLocation event
    _charging_location = ChargingLocation()

    # sends the 'IO.OpenChargeMap.mqtt.ChargingLocation' event to Kafka topic.
    await ioopen_charge_map_locations_mqtt_event_producer.send_io_open_charge_map_mqtt_charging_location(_feedurl = 'TODO: replace me', _poi_id = 'TODO: replace me', data = _charging_location)
    print(f"Sent 'IO.OpenChargeMap.mqtt.ChargingLocation' event: {_charging_location.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        ioopen_charge_map_reference_mqtt_event_producer = IOOpenChargeMapReferenceMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ioopen_charge_map_reference_mqtt_event_producer = IOOpenChargeMapReferenceMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- IO.OpenChargeMap.mqtt.Operator ----
    # TODO: Supply event data for the IO.OpenChargeMap.mqtt.Operator event
    _operator = Operator()

    # sends the 'IO.OpenChargeMap.mqtt.Operator' event to Kafka topic.
    await ioopen_charge_map_reference_mqtt_event_producer.send_io_open_charge_map_mqtt_operator(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _operator)
    print(f"Sent 'IO.OpenChargeMap.mqtt.Operator' event: {_operator.to_json()}")

    # ---- IO.OpenChargeMap.mqtt.ConnectionType ----
    # TODO: Supply event data for the IO.OpenChargeMap.mqtt.ConnectionType event
    _connection_type = ConnectionType()

    # sends the 'IO.OpenChargeMap.mqtt.ConnectionType' event to Kafka topic.
    await ioopen_charge_map_reference_mqtt_event_producer.send_io_open_charge_map_mqtt_connection_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _connection_type)
    print(f"Sent 'IO.OpenChargeMap.mqtt.ConnectionType' event: {_connection_type.to_json()}")

    # ---- IO.OpenChargeMap.mqtt.CurrentType ----
    # TODO: Supply event data for the IO.OpenChargeMap.mqtt.CurrentType event
    _current_type = CurrentType()

    # sends the 'IO.OpenChargeMap.mqtt.CurrentType' event to Kafka topic.
    await ioopen_charge_map_reference_mqtt_event_producer.send_io_open_charge_map_mqtt_current_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _current_type)
    print(f"Sent 'IO.OpenChargeMap.mqtt.CurrentType' event: {_current_type.to_json()}")

    # ---- IO.OpenChargeMap.mqtt.ChargerType ----
    # TODO: Supply event data for the IO.OpenChargeMap.mqtt.ChargerType event
    _charger_type = ChargerType()

    # sends the 'IO.OpenChargeMap.mqtt.ChargerType' event to Kafka topic.
    await ioopen_charge_map_reference_mqtt_event_producer.send_io_open_charge_map_mqtt_charger_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _charger_type)
    print(f"Sent 'IO.OpenChargeMap.mqtt.ChargerType' event: {_charger_type.to_json()}")

    # ---- IO.OpenChargeMap.mqtt.Country ----
    # TODO: Supply event data for the IO.OpenChargeMap.mqtt.Country event
    _country = Country()

    # sends the 'IO.OpenChargeMap.mqtt.Country' event to Kafka topic.
    await ioopen_charge_map_reference_mqtt_event_producer.send_io_open_charge_map_mqtt_country(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _country)
    print(f"Sent 'IO.OpenChargeMap.mqtt.Country' event: {_country.to_json()}")

    # ---- IO.OpenChargeMap.mqtt.DataProvider ----
    # TODO: Supply event data for the IO.OpenChargeMap.mqtt.DataProvider event
    _data_provider = DataProvider()

    # sends the 'IO.OpenChargeMap.mqtt.DataProvider' event to Kafka topic.
    await ioopen_charge_map_reference_mqtt_event_producer.send_io_open_charge_map_mqtt_data_provider(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _data_provider)
    print(f"Sent 'IO.OpenChargeMap.mqtt.DataProvider' event: {_data_provider.to_json()}")

    # ---- IO.OpenChargeMap.mqtt.StatusType ----
    # TODO: Supply event data for the IO.OpenChargeMap.mqtt.StatusType event
    _status_type = StatusType()

    # sends the 'IO.OpenChargeMap.mqtt.StatusType' event to Kafka topic.
    await ioopen_charge_map_reference_mqtt_event_producer.send_io_open_charge_map_mqtt_status_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _status_type)
    print(f"Sent 'IO.OpenChargeMap.mqtt.StatusType' event: {_status_type.to_json()}")

    # ---- IO.OpenChargeMap.mqtt.UsageType ----
    # TODO: Supply event data for the IO.OpenChargeMap.mqtt.UsageType event
    _usage_type = UsageType()

    # sends the 'IO.OpenChargeMap.mqtt.UsageType' event to Kafka topic.
    await ioopen_charge_map_reference_mqtt_event_producer.send_io_open_charge_map_mqtt_usage_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _usage_type)
    print(f"Sent 'IO.OpenChargeMap.mqtt.UsageType' event: {_usage_type.to_json()}")

    # ---- IO.OpenChargeMap.mqtt.SubmissionStatusType ----
    # TODO: Supply event data for the IO.OpenChargeMap.mqtt.SubmissionStatusType event
    _submission_status_type = SubmissionStatusType()

    # sends the 'IO.OpenChargeMap.mqtt.SubmissionStatusType' event to Kafka topic.
    await ioopen_charge_map_reference_mqtt_event_producer.send_io_open_charge_map_mqtt_submission_status_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _submission_status_type)
    print(f"Sent 'IO.OpenChargeMap.mqtt.SubmissionStatusType' event: {_submission_status_type.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        ioopen_charge_map_locations_amqp_event_producer = IOOpenChargeMapLocationsAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ioopen_charge_map_locations_amqp_event_producer = IOOpenChargeMapLocationsAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- IO.OpenChargeMap.amqp.ChargingLocation ----
    # TODO: Supply event data for the IO.OpenChargeMap.amqp.ChargingLocation event
    _charging_location = ChargingLocation()

    # sends the 'IO.OpenChargeMap.amqp.ChargingLocation' event to Kafka topic.
    await ioopen_charge_map_locations_amqp_event_producer.send_io_open_charge_map_amqp_charging_location(_feedurl = 'TODO: replace me', _poi_id = 'TODO: replace me', data = _charging_location)
    print(f"Sent 'IO.OpenChargeMap.amqp.ChargingLocation' event: {_charging_location.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        ioopen_charge_map_reference_amqp_event_producer = IOOpenChargeMapReferenceAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ioopen_charge_map_reference_amqp_event_producer = IOOpenChargeMapReferenceAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- IO.OpenChargeMap.amqp.Operator ----
    # TODO: Supply event data for the IO.OpenChargeMap.amqp.Operator event
    _operator = Operator()

    # sends the 'IO.OpenChargeMap.amqp.Operator' event to Kafka topic.
    await ioopen_charge_map_reference_amqp_event_producer.send_io_open_charge_map_amqp_operator(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _operator)
    print(f"Sent 'IO.OpenChargeMap.amqp.Operator' event: {_operator.to_json()}")

    # ---- IO.OpenChargeMap.amqp.ConnectionType ----
    # TODO: Supply event data for the IO.OpenChargeMap.amqp.ConnectionType event
    _connection_type = ConnectionType()

    # sends the 'IO.OpenChargeMap.amqp.ConnectionType' event to Kafka topic.
    await ioopen_charge_map_reference_amqp_event_producer.send_io_open_charge_map_amqp_connection_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _connection_type)
    print(f"Sent 'IO.OpenChargeMap.amqp.ConnectionType' event: {_connection_type.to_json()}")

    # ---- IO.OpenChargeMap.amqp.CurrentType ----
    # TODO: Supply event data for the IO.OpenChargeMap.amqp.CurrentType event
    _current_type = CurrentType()

    # sends the 'IO.OpenChargeMap.amqp.CurrentType' event to Kafka topic.
    await ioopen_charge_map_reference_amqp_event_producer.send_io_open_charge_map_amqp_current_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _current_type)
    print(f"Sent 'IO.OpenChargeMap.amqp.CurrentType' event: {_current_type.to_json()}")

    # ---- IO.OpenChargeMap.amqp.ChargerType ----
    # TODO: Supply event data for the IO.OpenChargeMap.amqp.ChargerType event
    _charger_type = ChargerType()

    # sends the 'IO.OpenChargeMap.amqp.ChargerType' event to Kafka topic.
    await ioopen_charge_map_reference_amqp_event_producer.send_io_open_charge_map_amqp_charger_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _charger_type)
    print(f"Sent 'IO.OpenChargeMap.amqp.ChargerType' event: {_charger_type.to_json()}")

    # ---- IO.OpenChargeMap.amqp.Country ----
    # TODO: Supply event data for the IO.OpenChargeMap.amqp.Country event
    _country = Country()

    # sends the 'IO.OpenChargeMap.amqp.Country' event to Kafka topic.
    await ioopen_charge_map_reference_amqp_event_producer.send_io_open_charge_map_amqp_country(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _country)
    print(f"Sent 'IO.OpenChargeMap.amqp.Country' event: {_country.to_json()}")

    # ---- IO.OpenChargeMap.amqp.DataProvider ----
    # TODO: Supply event data for the IO.OpenChargeMap.amqp.DataProvider event
    _data_provider = DataProvider()

    # sends the 'IO.OpenChargeMap.amqp.DataProvider' event to Kafka topic.
    await ioopen_charge_map_reference_amqp_event_producer.send_io_open_charge_map_amqp_data_provider(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _data_provider)
    print(f"Sent 'IO.OpenChargeMap.amqp.DataProvider' event: {_data_provider.to_json()}")

    # ---- IO.OpenChargeMap.amqp.StatusType ----
    # TODO: Supply event data for the IO.OpenChargeMap.amqp.StatusType event
    _status_type = StatusType()

    # sends the 'IO.OpenChargeMap.amqp.StatusType' event to Kafka topic.
    await ioopen_charge_map_reference_amqp_event_producer.send_io_open_charge_map_amqp_status_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _status_type)
    print(f"Sent 'IO.OpenChargeMap.amqp.StatusType' event: {_status_type.to_json()}")

    # ---- IO.OpenChargeMap.amqp.UsageType ----
    # TODO: Supply event data for the IO.OpenChargeMap.amqp.UsageType event
    _usage_type = UsageType()

    # sends the 'IO.OpenChargeMap.amqp.UsageType' event to Kafka topic.
    await ioopen_charge_map_reference_amqp_event_producer.send_io_open_charge_map_amqp_usage_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _usage_type)
    print(f"Sent 'IO.OpenChargeMap.amqp.UsageType' event: {_usage_type.to_json()}")

    # ---- IO.OpenChargeMap.amqp.SubmissionStatusType ----
    # TODO: Supply event data for the IO.OpenChargeMap.amqp.SubmissionStatusType event
    _submission_status_type = SubmissionStatusType()

    # sends the 'IO.OpenChargeMap.amqp.SubmissionStatusType' event to Kafka topic.
    await ioopen_charge_map_reference_amqp_event_producer.send_io_open_charge_map_amqp_submission_status_type(_feedurl = 'TODO: replace me', _reference_type = 'TODO: replace me', _reference_id = 'TODO: replace me', data = _submission_status_type)
    print(f"Sent 'IO.OpenChargeMap.amqp.SubmissionStatusType' event: {_submission_status_type.to_json()}")

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