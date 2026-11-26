
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

from usgs_waterdata_producer_kafka_producer.producer import USGSWaterDataKafkaEventProducer

# imports for the data classes for each event

from usgs_waterdata_producer_data import ContinuousObservation
from usgs_waterdata_producer_data import TimeSeries
from usgs_waterdata_producer_data import MonitoringLocation
from usgs_waterdata_producer_data import Parameter

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
        usgswater_data_kafka_event_producer = USGSWaterDataKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        usgswater_data_kafka_event_producer = USGSWaterDataKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- USGS.WaterData.kafka.ContinuousObservation ----
    # TODO: Supply event data for the USGS.WaterData.kafka.ContinuousObservation event
    _continuous_observation = ContinuousObservation()

    # sends the 'USGS.WaterData.kafka.ContinuousObservation' event to Kafka topic.
    await usgswater_data_kafka_event_producer.send_usgs_water_data_kafka_continuous_observation(_time_series_id = 'TODO: replace me', data = _continuous_observation)
    print(f"Sent 'USGS.WaterData.kafka.ContinuousObservation' event: {_continuous_observation.to_json()}")

    # ---- USGS.WaterData.kafka.TimeSeries ----
    # TODO: Supply event data for the USGS.WaterData.kafka.TimeSeries event
    _time_series = TimeSeries()

    # sends the 'USGS.WaterData.kafka.TimeSeries' event to Kafka topic.
    await usgswater_data_kafka_event_producer.send_usgs_water_data_kafka_time_series(_time_series_id = 'TODO: replace me', data = _time_series)
    print(f"Sent 'USGS.WaterData.kafka.TimeSeries' event: {_time_series.to_json()}")

    # ---- USGS.WaterData.kafka.MonitoringLocation ----
    # TODO: Supply event data for the USGS.WaterData.kafka.MonitoringLocation event
    _monitoring_location = MonitoringLocation()

    # sends the 'USGS.WaterData.kafka.MonitoringLocation' event to Kafka topic.
    await usgswater_data_kafka_event_producer.send_usgs_water_data_kafka_monitoring_location(_time_series_id = 'TODO: replace me', data = _monitoring_location)
    print(f"Sent 'USGS.WaterData.kafka.MonitoringLocation' event: {_monitoring_location.to_json()}")

    # ---- USGS.WaterData.kafka.Parameter ----
    # TODO: Supply event data for the USGS.WaterData.kafka.Parameter event
    _parameter = Parameter()

    # sends the 'USGS.WaterData.kafka.Parameter' event to Kafka topic.
    await usgswater_data_kafka_event_producer.send_usgs_water_data_kafka_parameter(_time_series_id = 'TODO: replace me', data = _parameter)
    print(f"Sent 'USGS.WaterData.kafka.Parameter' event: {_parameter.to_json()}")

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