
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

from entur_norway_producer_kafka_producer.producer import NoEnturJourneysEventProducer
from entur_norway_producer_kafka_producer.producer import NoEnturSituationsEventProducer

# imports for the data classes for each event

from entur_norway_producer_data.datedservicejourney import DatedServiceJourney
from entur_norway_producer_data.estimatedvehiclejourney import EstimatedVehicleJourney
from entur_norway_producer_data.monitoredvehiclejourney import MonitoredVehicleJourney
from entur_norway_producer_data.ptsituationelement import PtSituationElement

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
        no_entur_journeys_event_producer = NoEnturJourneysEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        no_entur_journeys_event_producer = NoEnturJourneysEventProducer(kafka_producer, topic, 'binary')

    # ---- no.entur.DatedServiceJourney ----
    # TODO: Supply event data for the no.entur.DatedServiceJourney event
    _dated_service_journey = DatedServiceJourney()

    # sends the 'no.entur.DatedServiceJourney' event to Kafka topic.
    await no_entur_journeys_event_producer.send_no_entur_dated_service_journey(_operating_day = 'TODO: replace me', _service_journey_id = 'TODO: replace me', data = _dated_service_journey)
    print(f"Sent 'no.entur.DatedServiceJourney' event: {_dated_service_journey.to_json()}")

    # ---- no.entur.EstimatedVehicleJourney ----
    # TODO: Supply event data for the no.entur.EstimatedVehicleJourney event
    _estimated_vehicle_journey = EstimatedVehicleJourney()

    # sends the 'no.entur.EstimatedVehicleJourney' event to Kafka topic.
    await no_entur_journeys_event_producer.send_no_entur_estimated_vehicle_journey(_operating_day = 'TODO: replace me', _service_journey_id = 'TODO: replace me', data = _estimated_vehicle_journey)
    print(f"Sent 'no.entur.EstimatedVehicleJourney' event: {_estimated_vehicle_journey.to_json()}")

    # ---- no.entur.MonitoredVehicleJourney ----
    # TODO: Supply event data for the no.entur.MonitoredVehicleJourney event
    _monitored_vehicle_journey = MonitoredVehicleJourney()

    # sends the 'no.entur.MonitoredVehicleJourney' event to Kafka topic.
    await no_entur_journeys_event_producer.send_no_entur_monitored_vehicle_journey(_operating_day = 'TODO: replace me', _service_journey_id = 'TODO: replace me', data = _monitored_vehicle_journey)
    print(f"Sent 'no.entur.MonitoredVehicleJourney' event: {_monitored_vehicle_journey.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        no_entur_situations_event_producer = NoEnturSituationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        no_entur_situations_event_producer = NoEnturSituationsEventProducer(kafka_producer, topic, 'binary')

    # ---- no.entur.PtSituationElement ----
    # TODO: Supply event data for the no.entur.PtSituationElement event
    _pt_situation_element = PtSituationElement()

    # sends the 'no.entur.PtSituationElement' event to Kafka topic.
    await no_entur_situations_event_producer.send_no_entur_pt_situation_element(_situation_number = 'TODO: replace me', data = _pt_situation_element)
    print(f"Sent 'no.entur.PtSituationElement' event: {_pt_situation_element.to_json()}")

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