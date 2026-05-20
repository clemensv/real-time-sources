
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

from tfl_road_traffic_producer_kafka_producer.producer import UkGovTflRoadCorridorsEventProducer
from tfl_road_traffic_producer_kafka_producer.producer import UkGovTflRoadDisruptionsEventProducer

# imports for the data classes for each event

from tfl_road_traffic_producer_data.roadcorridor import RoadCorridor
from tfl_road_traffic_producer_data.roadstatus import RoadStatus
from tfl_road_traffic_producer_data.roaddisruption import RoadDisruption

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
        uk_gov_tfl_road_corridors_event_producer = UkGovTflRoadCorridorsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        uk_gov_tfl_road_corridors_event_producer = UkGovTflRoadCorridorsEventProducer(kafka_producer, topic, 'binary')

    # ---- uk.gov.tfl.road.RoadCorridor ----
    # TODO: Supply event data for the uk.gov.tfl.road.RoadCorridor event
    _road_corridor = RoadCorridor()

    # sends the 'uk.gov.tfl.road.RoadCorridor' event to Kafka topic.
    await uk_gov_tfl_road_corridors_event_producer.send_uk_gov_tfl_road_road_corridor(_road_id = 'TODO: replace me', data = _road_corridor)
    print(f"Sent 'uk.gov.tfl.road.RoadCorridor' event: {_road_corridor.to_json()}")

    # ---- uk.gov.tfl.road.RoadStatus ----
    # TODO: Supply event data for the uk.gov.tfl.road.RoadStatus event
    _road_status = RoadStatus()

    # sends the 'uk.gov.tfl.road.RoadStatus' event to Kafka topic.
    await uk_gov_tfl_road_corridors_event_producer.send_uk_gov_tfl_road_road_status(_road_id = 'TODO: replace me', data = _road_status)
    print(f"Sent 'uk.gov.tfl.road.RoadStatus' event: {_road_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        uk_gov_tfl_road_disruptions_event_producer = UkGovTflRoadDisruptionsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        uk_gov_tfl_road_disruptions_event_producer = UkGovTflRoadDisruptionsEventProducer(kafka_producer, topic, 'binary')

    # ---- uk.gov.tfl.road.RoadDisruption ----
    # TODO: Supply event data for the uk.gov.tfl.road.RoadDisruption event
    _road_disruption = RoadDisruption()

    # sends the 'uk.gov.tfl.road.RoadDisruption' event to Kafka topic.
    await uk_gov_tfl_road_disruptions_event_producer.send_uk_gov_tfl_road_road_disruption(_disruption_id = 'TODO: replace me', data = _road_disruption)
    print(f"Sent 'uk.gov.tfl.road.RoadDisruption' event: {_road_disruption.to_json()}")

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