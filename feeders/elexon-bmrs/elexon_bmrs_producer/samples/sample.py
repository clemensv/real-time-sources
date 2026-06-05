
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

from elexon_bmrs_producer_kafka_producer.producer import UKCoElexonBMRSEventProducer
from elexon_bmrs_producer_kafka_producer.producer import UKCoElexonBMRSMqttEventProducer
from elexon_bmrs_producer_kafka_producer.producer import UKCoElexonBMRSAmqpEventProducer

# imports for the data classes for each event

from elexon_bmrs_producer_data import GenerationMix
from elexon_bmrs_producer_data import DemandOutturn
from elexon_bmrs_producer_data import Info

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
        ukco_elexon_bmrsevent_producer = UKCoElexonBMRSEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ukco_elexon_bmrsevent_producer = UKCoElexonBMRSEventProducer(kafka_producer, topic, 'binary')

    # ---- UK.Co.Elexon.BMRS.GenerationMix ----
    # TODO: Supply event data for the UK.Co.Elexon.BMRS.GenerationMix event
    _generation_mix = GenerationMix()

    # sends the 'UK.Co.Elexon.BMRS.GenerationMix' event to Kafka topic.
    await ukco_elexon_bmrsevent_producer.send_uk_co_elexon_bmrs_generation_mix(_settlement_period = 'TODO: replace me', data = _generation_mix)
    print(f"Sent 'UK.Co.Elexon.BMRS.GenerationMix' event: {_generation_mix.to_json()}")

    # ---- UK.Co.Elexon.BMRS.DemandOutturn ----
    # TODO: Supply event data for the UK.Co.Elexon.BMRS.DemandOutturn event
    _demand_outturn = DemandOutturn()

    # sends the 'UK.Co.Elexon.BMRS.DemandOutturn' event to Kafka topic.
    await ukco_elexon_bmrsevent_producer.send_uk_co_elexon_bmrs_demand_outturn(_settlement_period = 'TODO: replace me', data = _demand_outturn)
    print(f"Sent 'UK.Co.Elexon.BMRS.DemandOutturn' event: {_demand_outturn.to_json()}")

    # ---- UK.Co.Elexon.BMRS.Info ----
    # TODO: Supply event data for the UK.Co.Elexon.BMRS.Info event
    _info = Info()

    # sends the 'UK.Co.Elexon.BMRS.Info' event to Kafka topic.
    await ukco_elexon_bmrsevent_producer.send_uk_co_elexon_bmrs_info(_settlement_period = 'TODO: replace me', data = _info)
    print(f"Sent 'UK.Co.Elexon.BMRS.Info' event: {_info.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        ukco_elexon_bmrsmqtt_event_producer = UKCoElexonBMRSMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ukco_elexon_bmrsmqtt_event_producer = UKCoElexonBMRSMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- UK.Co.Elexon.BMRS.mqtt.GenerationMix ----
    # TODO: Supply event data for the UK.Co.Elexon.BMRS.mqtt.GenerationMix event
    _generation_mix = GenerationMix()

    # sends the 'UK.Co.Elexon.BMRS.mqtt.GenerationMix' event to Kafka topic.
    await ukco_elexon_bmrsmqtt_event_producer.send_uk_co_elexon_bmrs_mqtt_generation_mix(_settlement_period = 'TODO: replace me', data = _generation_mix)
    print(f"Sent 'UK.Co.Elexon.BMRS.mqtt.GenerationMix' event: {_generation_mix.to_json()}")

    # ---- UK.Co.Elexon.BMRS.mqtt.DemandOutturn ----
    # TODO: Supply event data for the UK.Co.Elexon.BMRS.mqtt.DemandOutturn event
    _demand_outturn = DemandOutturn()

    # sends the 'UK.Co.Elexon.BMRS.mqtt.DemandOutturn' event to Kafka topic.
    await ukco_elexon_bmrsmqtt_event_producer.send_uk_co_elexon_bmrs_mqtt_demand_outturn(_settlement_period = 'TODO: replace me', data = _demand_outturn)
    print(f"Sent 'UK.Co.Elexon.BMRS.mqtt.DemandOutturn' event: {_demand_outturn.to_json()}")

    # ---- UK.Co.Elexon.BMRS.mqtt.Info ----
    # TODO: Supply event data for the UK.Co.Elexon.BMRS.mqtt.Info event
    _info = Info()

    # sends the 'UK.Co.Elexon.BMRS.mqtt.Info' event to Kafka topic.
    await ukco_elexon_bmrsmqtt_event_producer.send_uk_co_elexon_bmrs_mqtt_info(_settlement_period = 'TODO: replace me', data = _info)
    print(f"Sent 'UK.Co.Elexon.BMRS.mqtt.Info' event: {_info.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        ukco_elexon_bmrsamqp_event_producer = UKCoElexonBMRSAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ukco_elexon_bmrsamqp_event_producer = UKCoElexonBMRSAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- UK.Co.Elexon.BMRS.amqp.GenerationMix ----
    # TODO: Supply event data for the UK.Co.Elexon.BMRS.amqp.GenerationMix event
    _generation_mix = GenerationMix()

    # sends the 'UK.Co.Elexon.BMRS.amqp.GenerationMix' event to Kafka topic.
    await ukco_elexon_bmrsamqp_event_producer.send_uk_co_elexon_bmrs_amqp_generation_mix(_settlement_period = 'TODO: replace me', data = _generation_mix)
    print(f"Sent 'UK.Co.Elexon.BMRS.amqp.GenerationMix' event: {_generation_mix.to_json()}")

    # ---- UK.Co.Elexon.BMRS.amqp.DemandOutturn ----
    # TODO: Supply event data for the UK.Co.Elexon.BMRS.amqp.DemandOutturn event
    _demand_outturn = DemandOutturn()

    # sends the 'UK.Co.Elexon.BMRS.amqp.DemandOutturn' event to Kafka topic.
    await ukco_elexon_bmrsamqp_event_producer.send_uk_co_elexon_bmrs_amqp_demand_outturn(_settlement_period = 'TODO: replace me', data = _demand_outturn)
    print(f"Sent 'UK.Co.Elexon.BMRS.amqp.DemandOutturn' event: {_demand_outturn.to_json()}")

    # ---- UK.Co.Elexon.BMRS.amqp.Info ----
    # TODO: Supply event data for the UK.Co.Elexon.BMRS.amqp.Info event
    _info = Info()

    # sends the 'UK.Co.Elexon.BMRS.amqp.Info' event to Kafka topic.
    await ukco_elexon_bmrsamqp_event_producer.send_uk_co_elexon_bmrs_amqp_info(_settlement_period = 'TODO: replace me', data = _info)
    print(f"Sent 'UK.Co.Elexon.BMRS.amqp.Info' event: {_info.to_json()}")

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