
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

from usgs_nwis_wq_producer_kafka_producer.producer import USGSWaterQualitySitesEventProducer
from usgs_nwis_wq_producer_kafka_producer.producer import USGSWaterQualityReadingsEventProducer

# imports for the data classes for each event

from usgs_nwis_wq_producer_data.monitoringsite import MonitoringSite
from usgs_nwis_wq_producer_data.waterqualityreading import WaterQualityReading

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
        usgswater_quality_sites_event_producer = USGSWaterQualitySitesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        usgswater_quality_sites_event_producer = USGSWaterQualitySitesEventProducer(kafka_producer, topic, 'binary')

    # ---- USGS.WaterQuality.Sites.MonitoringSite ----
    # TODO: Supply event data for the USGS.WaterQuality.Sites.MonitoringSite event
    _monitoring_site = MonitoringSite()

    # sends the 'USGS.WaterQuality.Sites.MonitoringSite' event to Kafka topic.
    await usgswater_quality_sites_event_producer.send_usgs_water_quality_sites_monitoring_site(_source_uri = 'TODO: replace me', _site_number = 'TODO: replace me', data = _monitoring_site)
    print(f"Sent 'USGS.WaterQuality.Sites.MonitoringSite' event: {_monitoring_site.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        usgswater_quality_readings_event_producer = USGSWaterQualityReadingsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        usgswater_quality_readings_event_producer = USGSWaterQualityReadingsEventProducer(kafka_producer, topic, 'binary')

    # ---- USGS.WaterQuality.Readings.WaterQualityReading ----
    # TODO: Supply event data for the USGS.WaterQuality.Readings.WaterQualityReading event
    _water_quality_reading = WaterQualityReading()

    # sends the 'USGS.WaterQuality.Readings.WaterQualityReading' event to Kafka topic.
    await usgswater_quality_readings_event_producer.send_usgs_water_quality_readings_water_quality_reading(_source_uri = 'TODO: replace me', _site_number = 'TODO: replace me', _parameter_code = 'TODO: replace me', data = _water_quality_reading)
    print(f"Sent 'USGS.WaterQuality.Readings.WaterQualityReading' event: {_water_quality_reading.to_json()}")

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