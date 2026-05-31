
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

from tokyo_docomo_bikeshare_producer_kafka_producer.producer import JPODPTDocomoBikeshareSystemEventProducer
from tokyo_docomo_bikeshare_producer_kafka_producer.producer import JPODPTDocomoBikeshareStationsEventProducer
from tokyo_docomo_bikeshare_producer_kafka_producer.producer import JPODPTDocomoBikeshareSystemMqttEventProducer
from tokyo_docomo_bikeshare_producer_kafka_producer.producer import JPODPTDocomoBikeshareStationsMqttEventProducer
from tokyo_docomo_bikeshare_producer_kafka_producer.producer import JPODPTDocomoBikeshareSystemAmqpEventProducer
from tokyo_docomo_bikeshare_producer_kafka_producer.producer import JPODPTDocomoBikeshareStationsAmqpEventProducer

# imports for the data classes for each event

from tokyo_docomo_bikeshare_producer_data.bikesharesystem import BikeshareSystem
from tokyo_docomo_bikeshare_producer_data.bikesharestation import BikeshareStation
from tokyo_docomo_bikeshare_producer_data.bikesharestationstatus import BikeshareStationStatus

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
        jpodptdocomo_bikeshare_system_event_producer = JPODPTDocomoBikeshareSystemEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        jpodptdocomo_bikeshare_system_event_producer = JPODPTDocomoBikeshareSystemEventProducer(kafka_producer, topic, 'binary')

    # ---- JP.ODPT.DocomoBikeshare.BikeshareSystem ----
    # TODO: Supply event data for the JP.ODPT.DocomoBikeshare.BikeshareSystem event
    _bikeshare_system = BikeshareSystem()

    # sends the 'JP.ODPT.DocomoBikeshare.BikeshareSystem' event to Kafka topic.
    await jpodptdocomo_bikeshare_system_event_producer.send_jp_odpt_docomo_bikeshare_bikeshare_system(_system_id = 'TODO: replace me', data = _bikeshare_system)
    print(f"Sent 'JP.ODPT.DocomoBikeshare.BikeshareSystem' event: {_bikeshare_system.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        jpodptdocomo_bikeshare_stations_event_producer = JPODPTDocomoBikeshareStationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        jpodptdocomo_bikeshare_stations_event_producer = JPODPTDocomoBikeshareStationsEventProducer(kafka_producer, topic, 'binary')

    # ---- JP.ODPT.DocomoBikeshare.BikeshareStation ----
    # TODO: Supply event data for the JP.ODPT.DocomoBikeshare.BikeshareStation event
    _bikeshare_station = BikeshareStation()

    # sends the 'JP.ODPT.DocomoBikeshare.BikeshareStation' event to Kafka topic.
    await jpodptdocomo_bikeshare_stations_event_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station(_system_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _bikeshare_station)
    print(f"Sent 'JP.ODPT.DocomoBikeshare.BikeshareStation' event: {_bikeshare_station.to_json()}")

    # ---- JP.ODPT.DocomoBikeshare.BikeshareStationStatus ----
    # TODO: Supply event data for the JP.ODPT.DocomoBikeshare.BikeshareStationStatus event
    _bikeshare_station_status = BikeshareStationStatus()

    # sends the 'JP.ODPT.DocomoBikeshare.BikeshareStationStatus' event to Kafka topic.
    await jpodptdocomo_bikeshare_stations_event_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station_status(_system_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _bikeshare_station_status)
    print(f"Sent 'JP.ODPT.DocomoBikeshare.BikeshareStationStatus' event: {_bikeshare_station_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        jpodptdocomo_bikeshare_system_mqtt_event_producer = JPODPTDocomoBikeshareSystemMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        jpodptdocomo_bikeshare_system_mqtt_event_producer = JPODPTDocomoBikeshareSystemMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- JP.ODPT.DocomoBikeshare.BikeshareSystem.mqtt ----
    # TODO: Supply event data for the JP.ODPT.DocomoBikeshare.BikeshareSystem.mqtt event
    _bikeshare_system = BikeshareSystem()

    # sends the 'JP.ODPT.DocomoBikeshare.BikeshareSystem.mqtt' event to Kafka topic.
    await jpodptdocomo_bikeshare_system_mqtt_event_producer.send_jp_odpt_docomo_bikeshare_bikeshare_system_mqtt(_system_id = 'TODO: replace me', data = _bikeshare_system)
    print(f"Sent 'JP.ODPT.DocomoBikeshare.BikeshareSystem.mqtt' event: {_bikeshare_system.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        jpodptdocomo_bikeshare_stations_mqtt_event_producer = JPODPTDocomoBikeshareStationsMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        jpodptdocomo_bikeshare_stations_mqtt_event_producer = JPODPTDocomoBikeshareStationsMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- JP.ODPT.DocomoBikeshare.BikeshareStation.mqtt ----
    # TODO: Supply event data for the JP.ODPT.DocomoBikeshare.BikeshareStation.mqtt event
    _bikeshare_station = BikeshareStation()

    # sends the 'JP.ODPT.DocomoBikeshare.BikeshareStation.mqtt' event to Kafka topic.
    await jpodptdocomo_bikeshare_stations_mqtt_event_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station_mqtt(_system_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _bikeshare_station)
    print(f"Sent 'JP.ODPT.DocomoBikeshare.BikeshareStation.mqtt' event: {_bikeshare_station.to_json()}")

    # ---- JP.ODPT.DocomoBikeshare.BikeshareStationStatus.mqtt ----
    # TODO: Supply event data for the JP.ODPT.DocomoBikeshare.BikeshareStationStatus.mqtt event
    _bikeshare_station_status = BikeshareStationStatus()

    # sends the 'JP.ODPT.DocomoBikeshare.BikeshareStationStatus.mqtt' event to Kafka topic.
    await jpodptdocomo_bikeshare_stations_mqtt_event_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station_status_mqtt(_system_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _bikeshare_station_status)
    print(f"Sent 'JP.ODPT.DocomoBikeshare.BikeshareStationStatus.mqtt' event: {_bikeshare_station_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        jpodptdocomo_bikeshare_system_amqp_event_producer = JPODPTDocomoBikeshareSystemAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        jpodptdocomo_bikeshare_system_amqp_event_producer = JPODPTDocomoBikeshareSystemAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- JP.ODPT.DocomoBikeshare.BikeshareSystem.amqp ----
    # TODO: Supply event data for the JP.ODPT.DocomoBikeshare.BikeshareSystem.amqp event
    _bikeshare_system = BikeshareSystem()

    # sends the 'JP.ODPT.DocomoBikeshare.BikeshareSystem.amqp' event to Kafka topic.
    await jpodptdocomo_bikeshare_system_amqp_event_producer.send_jp_odpt_docomo_bikeshare_bikeshare_system_amqp(_system_id = 'TODO: replace me', data = _bikeshare_system)
    print(f"Sent 'JP.ODPT.DocomoBikeshare.BikeshareSystem.amqp' event: {_bikeshare_system.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        jpodptdocomo_bikeshare_stations_amqp_event_producer = JPODPTDocomoBikeshareStationsAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        jpodptdocomo_bikeshare_stations_amqp_event_producer = JPODPTDocomoBikeshareStationsAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- JP.ODPT.DocomoBikeshare.BikeshareStation.amqp ----
    # TODO: Supply event data for the JP.ODPT.DocomoBikeshare.BikeshareStation.amqp event
    _bikeshare_station = BikeshareStation()

    # sends the 'JP.ODPT.DocomoBikeshare.BikeshareStation.amqp' event to Kafka topic.
    await jpodptdocomo_bikeshare_stations_amqp_event_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station_amqp(_system_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _bikeshare_station)
    print(f"Sent 'JP.ODPT.DocomoBikeshare.BikeshareStation.amqp' event: {_bikeshare_station.to_json()}")

    # ---- JP.ODPT.DocomoBikeshare.BikeshareStationStatus.amqp ----
    # TODO: Supply event data for the JP.ODPT.DocomoBikeshare.BikeshareStationStatus.amqp event
    _bikeshare_station_status = BikeshareStationStatus()

    # sends the 'JP.ODPT.DocomoBikeshare.BikeshareStationStatus.amqp' event to Kafka topic.
    await jpodptdocomo_bikeshare_stations_amqp_event_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station_status_amqp(_system_id = 'TODO: replace me', _station_id = 'TODO: replace me', data = _bikeshare_station_status)
    print(f"Sent 'JP.ODPT.DocomoBikeshare.BikeshareStationStatus.amqp' event: {_bikeshare_station_status.to_json()}")

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