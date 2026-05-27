
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

from ndw_road_traffic_producer_kafka_producer.producer import NLNDWAVGEventProducer

# imports for the data classes for each event

from ndw_road_traffic_producer_data.pointmeasurementsite import PointMeasurementSite
from ndw_road_traffic_producer_data.routemeasurementsite import RouteMeasurementSite
from ndw_road_traffic_producer_data.trafficobservation import TrafficObservation
from ndw_road_traffic_producer_data.traveltimeobservation import TravelTimeObservation

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
        nlndwavgevent_producer = NLNDWAVGEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwavgevent_producer = NLNDWAVGEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.AVG.PointMeasurementSite ----
    # TODO: Supply event data for the NL.NDW.AVG.PointMeasurementSite event
    _point_measurement_site = PointMeasurementSite()

    # sends the 'NL.NDW.AVG.PointMeasurementSite' event to Kafka topic.
    await nlndwavgevent_producer.send_nl_ndw_avg_point_measurement_site(_measurement_site_id = 'TODO: replace me', data = _point_measurement_site)
    print(f"Sent 'NL.NDW.AVG.PointMeasurementSite' event: {_point_measurement_site.to_json()}")

    # ---- NL.NDW.AVG.RouteMeasurementSite ----
    # TODO: Supply event data for the NL.NDW.AVG.RouteMeasurementSite event
    _route_measurement_site = RouteMeasurementSite()

    # sends the 'NL.NDW.AVG.RouteMeasurementSite' event to Kafka topic.
    await nlndwavgevent_producer.send_nl_ndw_avg_route_measurement_site(_measurement_site_id = 'TODO: replace me', data = _route_measurement_site)
    print(f"Sent 'NL.NDW.AVG.RouteMeasurementSite' event: {_route_measurement_site.to_json()}")

    # ---- NL.NDW.AVG.TrafficObservation ----
    # TODO: Supply event data for the NL.NDW.AVG.TrafficObservation event
    _traffic_observation = TrafficObservation()

    # sends the 'NL.NDW.AVG.TrafficObservation' event to Kafka topic.
    await nlndwavgevent_producer.send_nl_ndw_avg_traffic_observation(_measurement_site_id = 'TODO: replace me', data = _traffic_observation)
    print(f"Sent 'NL.NDW.AVG.TrafficObservation' event: {_traffic_observation.to_json()}")

    # ---- NL.NDW.AVG.TravelTimeObservation ----
    # TODO: Supply event data for the NL.NDW.AVG.TravelTimeObservation event
    _travel_time_observation = TravelTimeObservation()

    # sends the 'NL.NDW.AVG.TravelTimeObservation' event to Kafka topic.
    await nlndwavgevent_producer.send_nl_ndw_avg_travel_time_observation(_measurement_site_id = 'TODO: replace me', data = _travel_time_observation)
    print(f"Sent 'NL.NDW.AVG.TravelTimeObservation' event: {_travel_time_observation.to_json()}")

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