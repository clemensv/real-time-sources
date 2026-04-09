
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

from french_road_traffic_producer_kafka_producer.producer import FrGouvTransportBisonFuteTrafficFlowEventProducer
from french_road_traffic_producer_kafka_producer.producer import FrGouvTransportBisonFuteRoadEventEventProducer

# imports for the data classes for each event

from french_road_traffic_producer_data.trafficflowmeasurement import TrafficFlowMeasurement
from french_road_traffic_producer_data.roadevent import RoadEvent

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
        fr_gouv_transport_bison_fute_traffic_flow_event_producer = FrGouvTransportBisonFuteTrafficFlowEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fr_gouv_transport_bison_fute_traffic_flow_event_producer = FrGouvTransportBisonFuteTrafficFlowEventProducer(kafka_producer, topic, 'binary')

    # ---- fr.gouv.transport.bison_fute.TrafficFlowMeasurement ----
    # TODO: Supply event data for the fr.gouv.transport.bison_fute.TrafficFlowMeasurement event
    _traffic_flow_measurement = TrafficFlowMeasurement()

    # sends the 'fr.gouv.transport.bison_fute.TrafficFlowMeasurement' event to Kafka topic.
    await fr_gouv_transport_bison_fute_traffic_flow_event_producer.send_fr_gouv_transport_bison_fute_traffic_flow_measurement(_feedurl = 'TODO: replace me', _site_id = 'TODO: replace me', data = _traffic_flow_measurement)
    print(f"Sent 'fr.gouv.transport.bison_fute.TrafficFlowMeasurement' event: {_traffic_flow_measurement.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        fr_gouv_transport_bison_fute_road_event_event_producer = FrGouvTransportBisonFuteRoadEventEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fr_gouv_transport_bison_fute_road_event_event_producer = FrGouvTransportBisonFuteRoadEventEventProducer(kafka_producer, topic, 'binary')

    # ---- fr.gouv.transport.bison_fute.RoadEvent ----
    # TODO: Supply event data for the fr.gouv.transport.bison_fute.RoadEvent event
    _road_event = RoadEvent()

    # sends the 'fr.gouv.transport.bison_fute.RoadEvent' event to Kafka topic.
    await fr_gouv_transport_bison_fute_road_event_event_producer.send_fr_gouv_transport_bison_fute_road_event(_feedurl = 'TODO: replace me', _situation_id = 'TODO: replace me', data = _road_event)
    print(f"Sent 'fr.gouv.transport.bison_fute.RoadEvent' event: {_road_event.to_json()}")

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