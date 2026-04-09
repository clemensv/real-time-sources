
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

from ndl_netherlands_producer_kafka_producer.producer import NLNDWTrafficMeasurementsEventProducer
from ndl_netherlands_producer_kafka_producer.producer import NLNDWTrafficSituationsEventProducer

# imports for the data classes for each event

from ndl_netherlands_producer_data.trafficspeed import TrafficSpeed
from ndl_netherlands_producer_data.traveltime import TravelTime
from ndl_netherlands_producer_data.trafficsituation import TrafficSituation

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
        nlndwtraffic_measurements_event_producer = NLNDWTrafficMeasurementsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwtraffic_measurements_event_producer = NLNDWTrafficMeasurementsEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.Traffic.TrafficSpeed ----
    # TODO: Supply event data for the NL.NDW.Traffic.TrafficSpeed event
    _traffic_speed = TrafficSpeed()

    # sends the 'NL.NDW.Traffic.TrafficSpeed' event to Kafka topic.
    await nlndwtraffic_measurements_event_producer.send_nl_ndw_traffic_traffic_speed(_site_id = 'TODO: replace me', data = _traffic_speed)
    print(f"Sent 'NL.NDW.Traffic.TrafficSpeed' event: {_traffic_speed.to_json()}")

    # ---- NL.NDW.Traffic.TravelTime ----
    # TODO: Supply event data for the NL.NDW.Traffic.TravelTime event
    _travel_time = TravelTime()

    # sends the 'NL.NDW.Traffic.TravelTime' event to Kafka topic.
    await nlndwtraffic_measurements_event_producer.send_nl_ndw_traffic_travel_time(_site_id = 'TODO: replace me', data = _travel_time)
    print(f"Sent 'NL.NDW.Traffic.TravelTime' event: {_travel_time.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nlndwtraffic_situations_event_producer = NLNDWTrafficSituationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwtraffic_situations_event_producer = NLNDWTrafficSituationsEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.Traffic.TrafficSituation ----
    # TODO: Supply event data for the NL.NDW.Traffic.TrafficSituation event
    _traffic_situation = TrafficSituation()

    # sends the 'NL.NDW.Traffic.TrafficSituation' event to Kafka topic.
    await nlndwtraffic_situations_event_producer.send_nl_ndw_traffic_traffic_situation(_situation_id = 'TODO: replace me', data = _traffic_situation)
    print(f"Sent 'NL.NDW.Traffic.TrafficSituation' event: {_traffic_situation.to_json()}")

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