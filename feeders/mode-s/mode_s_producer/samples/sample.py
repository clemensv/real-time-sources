
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

from mode_s_producer_kafka_producer.producer import ModeSKafkaEventProducer

# imports for the data classes for each event

from mode_s_producer_data import Record

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
        mode_skafka_event_producer = ModeSKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        mode_skafka_event_producer = ModeSKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- Mode_S.kafka.ADSB ----
    # TODO: Supply event data for the Mode_S.kafka.ADSB event
    _record = Record()

    # sends the 'Mode_S.kafka.ADSB' event to Kafka topic.
    await mode_skafka_event_producer.send_mode_s_kafka_adsb(_feedurl = 'TODO: replace me', _icao24 = 'TODO: replace me', _receiver_id = 'TODO: replace me', data = _record)
    print(f"Sent 'Mode_S.kafka.ADSB' event: {_record.to_json()}")

    # ---- Mode_S.kafka.AltitudeReply ----
    # TODO: Supply event data for the Mode_S.kafka.AltitudeReply event
    _record = Record()

    # sends the 'Mode_S.kafka.AltitudeReply' event to Kafka topic.
    await mode_skafka_event_producer.send_mode_s_kafka_altitude_reply(_feedurl = 'TODO: replace me', _icao24 = 'TODO: replace me', _receiver_id = 'TODO: replace me', data = _record)
    print(f"Sent 'Mode_S.kafka.AltitudeReply' event: {_record.to_json()}")

    # ---- Mode_S.kafka.IdentityReply ----
    # TODO: Supply event data for the Mode_S.kafka.IdentityReply event
    _record = Record()

    # sends the 'Mode_S.kafka.IdentityReply' event to Kafka topic.
    await mode_skafka_event_producer.send_mode_s_kafka_identity_reply(_feedurl = 'TODO: replace me', _icao24 = 'TODO: replace me', _receiver_id = 'TODO: replace me', data = _record)
    print(f"Sent 'Mode_S.kafka.IdentityReply' event: {_record.to_json()}")

    # ---- Mode_S.kafka.AcquisitionReply ----
    # TODO: Supply event data for the Mode_S.kafka.AcquisitionReply event
    _record = Record()

    # sends the 'Mode_S.kafka.AcquisitionReply' event to Kafka topic.
    await mode_skafka_event_producer.send_mode_s_kafka_acquisition_reply(_feedurl = 'TODO: replace me', _icao24 = 'TODO: replace me', _receiver_id = 'TODO: replace me', data = _record)
    print(f"Sent 'Mode_S.kafka.AcquisitionReply' event: {_record.to_json()}")

    # ---- Mode_S.kafka.CommBAltitude ----
    # TODO: Supply event data for the Mode_S.kafka.CommBAltitude event
    _record = Record()

    # sends the 'Mode_S.kafka.CommBAltitude' event to Kafka topic.
    await mode_skafka_event_producer.send_mode_s_kafka_comm_baltitude(_feedurl = 'TODO: replace me', _icao24 = 'TODO: replace me', _receiver_id = 'TODO: replace me', data = _record)
    print(f"Sent 'Mode_S.kafka.CommBAltitude' event: {_record.to_json()}")

    # ---- Mode_S.kafka.CommBIdentity ----
    # TODO: Supply event data for the Mode_S.kafka.CommBIdentity event
    _record = Record()

    # sends the 'Mode_S.kafka.CommBIdentity' event to Kafka topic.
    await mode_skafka_event_producer.send_mode_s_kafka_comm_bidentity(_feedurl = 'TODO: replace me', _icao24 = 'TODO: replace me', _receiver_id = 'TODO: replace me', data = _record)
    print(f"Sent 'Mode_S.kafka.CommBIdentity' event: {_record.to_json()}")

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