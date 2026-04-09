
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

from carbon_intensity_producer_kafka_producer.producer import UkOrgCarbonintensityEventProducer
from carbon_intensity_producer_kafka_producer.producer import UkOrgCarbonintensityRegionalEventProducer

# imports for the data classes for each event

from carbon_intensity_producer_data.intensity import Intensity
from carbon_intensity_producer_data.generationmix import GenerationMix
from carbon_intensity_producer_data.regionalintensity import RegionalIntensity

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
        uk_org_carbonintensity_event_producer = UkOrgCarbonintensityEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        uk_org_carbonintensity_event_producer = UkOrgCarbonintensityEventProducer(kafka_producer, topic, 'binary')

    # ---- uk.org.carbonintensity.Intensity ----
    # TODO: Supply event data for the uk.org.carbonintensity.Intensity event
    _intensity = Intensity()

    # sends the 'uk.org.carbonintensity.Intensity' event to Kafka topic.
    await uk_org_carbonintensity_event_producer.send_uk_org_carbonintensity_intensity(_period_from = 'TODO: replace me', data = _intensity)
    print(f"Sent 'uk.org.carbonintensity.Intensity' event: {_intensity.to_json()}")

    # ---- uk.org.carbonintensity.GenerationMix ----
    # TODO: Supply event data for the uk.org.carbonintensity.GenerationMix event
    _generation_mix = GenerationMix()

    # sends the 'uk.org.carbonintensity.GenerationMix' event to Kafka topic.
    await uk_org_carbonintensity_event_producer.send_uk_org_carbonintensity_generation_mix(_period_from = 'TODO: replace me', data = _generation_mix)
    print(f"Sent 'uk.org.carbonintensity.GenerationMix' event: {_generation_mix.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        uk_org_carbonintensity_regional_event_producer = UkOrgCarbonintensityRegionalEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        uk_org_carbonintensity_regional_event_producer = UkOrgCarbonintensityRegionalEventProducer(kafka_producer, topic, 'binary')

    # ---- uk.org.carbonintensity.RegionalIntensity ----
    # TODO: Supply event data for the uk.org.carbonintensity.RegionalIntensity event
    _regional_intensity = RegionalIntensity()

    # sends the 'uk.org.carbonintensity.RegionalIntensity' event to Kafka topic.
    await uk_org_carbonintensity_regional_event_producer.send_uk_org_carbonintensity_regional_intensity(_region_id = 'TODO: replace me', data = _regional_intensity)
    print(f"Sent 'uk.org.carbonintensity.RegionalIntensity' event: {_regional_intensity.to_json()}")

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