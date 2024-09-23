
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

from usgs_iv_producer_kafka_producer.producer import USGSSitesEventProducer
from usgs_iv_producer_kafka_producer.producer import USGSInstantaneousValuesEventProducer

# imports for the data classes for each event

from usgs_iv_producer_data.usgs.sites.site import Site
from usgs_iv_producer_data.usgs.instantaneousvalues.precipitation import Precipitation
from usgs_iv_producer_data.usgs.instantaneousvalues.streamflow import Streamflow
from usgs_iv_producer_data.usgs.instantaneousvalues.gageheight import GageHeight
from usgs_iv_producer_data.usgs.instantaneousvalues.watertemperature import WaterTemperature
from usgs_iv_producer_data.usgs.instantaneousvalues.dissolvedoxygen import DissolvedOxygen
from usgs_iv_producer_data.usgs.instantaneousvalues.ph import PH
from usgs_iv_producer_data.usgs.instantaneousvalues.specificconductance import SpecificConductance
from usgs_iv_producer_data.usgs.instantaneousvalues.turbidity import Turbidity

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
        usgssites_event_producer = USGSSitesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        usgssites_event_producer = USGSSitesEventProducer(kafka_producer, topic, 'binary')

    # ---- USGS.Sites.Site ----
    # TODO: Supply event data for the USGS.Sites.Site event
    _site = Site()

    # sends the 'USGS.Sites.Site' event to Kafka topic.
    await usgssites_event_producer.send_usgs_sites_site(_source_uri = 'TODO: replace me', data = _site)
    print(f"Sent 'USGS.Sites.Site' event: {_site.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        usgsinstantaneous_values_event_producer = USGSInstantaneousValuesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        usgsinstantaneous_values_event_producer = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')

    # ---- USGS.InstantaneousValues.Precipitation ----
    # TODO: Supply event data for the USGS.InstantaneousValues.Precipitation event
    _precipitation = Precipitation()

    # sends the 'USGS.InstantaneousValues.Precipitation' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_precipitation(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _precipitation)
    print(f"Sent 'USGS.InstantaneousValues.Precipitation' event: {_precipitation.to_json()}")

    # ---- USGS.InstantaneousValues.Streamflow ----
    # TODO: Supply event data for the USGS.InstantaneousValues.Streamflow event
    _streamflow = Streamflow()

    # sends the 'USGS.InstantaneousValues.Streamflow' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_streamflow(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _streamflow)
    print(f"Sent 'USGS.InstantaneousValues.Streamflow' event: {_streamflow.to_json()}")

    # ---- USGS.InstantaneousValues.GageHeight ----
    # TODO: Supply event data for the USGS.InstantaneousValues.GageHeight event
    _gage_height = GageHeight()

    # sends the 'USGS.InstantaneousValues.GageHeight' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_gage_height(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _gage_height)
    print(f"Sent 'USGS.InstantaneousValues.GageHeight' event: {_gage_height.to_json()}")

    # ---- USGS.InstantaneousValues.WaterTemperature ----
    # TODO: Supply event data for the USGS.InstantaneousValues.WaterTemperature event
    _water_temperature = WaterTemperature()

    # sends the 'USGS.InstantaneousValues.WaterTemperature' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_water_temperature(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _water_temperature)
    print(f"Sent 'USGS.InstantaneousValues.WaterTemperature' event: {_water_temperature.to_json()}")

    # ---- USGS.InstantaneousValues.DissolvedOxygen ----
    # TODO: Supply event data for the USGS.InstantaneousValues.DissolvedOxygen event
    _dissolved_oxygen = DissolvedOxygen()

    # sends the 'USGS.InstantaneousValues.DissolvedOxygen' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_dissolved_oxygen(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _dissolved_oxygen)
    print(f"Sent 'USGS.InstantaneousValues.DissolvedOxygen' event: {_dissolved_oxygen.to_json()}")

    # ---- USGS.InstantaneousValues.pH ----
    # TODO: Supply event data for the USGS.InstantaneousValues.pH event
    _ph = PH()

    # sends the 'USGS.InstantaneousValues.pH' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_p_h(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _ph)
    print(f"Sent 'USGS.InstantaneousValues.pH' event: {_ph.to_json()}")

    # ---- USGS.InstantaneousValues.SpecificConductance ----
    # TODO: Supply event data for the USGS.InstantaneousValues.SpecificConductance event
    _specific_conductance = SpecificConductance()

    # sends the 'USGS.InstantaneousValues.SpecificConductance' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_specific_conductance(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _specific_conductance)
    print(f"Sent 'USGS.InstantaneousValues.SpecificConductance' event: {_specific_conductance.to_json()}")

    # ---- USGS.InstantaneousValues.Turbidity ----
    # TODO: Supply event data for the USGS.InstantaneousValues.Turbidity event
    _turbidity = Turbidity()

    # sends the 'USGS.InstantaneousValues.Turbidity' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_turbidity(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _turbidity)
    print(f"Sent 'USGS.InstantaneousValues.Turbidity' event: {_turbidity.to_json()}")

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