
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

from ndl_netherlands_producer_kafka_producer.producer import NLNDWChargingLocationsEventProducer
from ndl_netherlands_producer_kafka_producer.producer import NLNDWChargingEvseEventProducer
from ndl_netherlands_producer_kafka_producer.producer import NLNDWChargingTariffsEventProducer

# imports for the data classes for each event

from ndl_netherlands_producer_data.charginglocation import ChargingLocation
from ndl_netherlands_producer_data.evsestatus import EvseStatus
from ndl_netherlands_producer_data.chargingtariff import ChargingTariff

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
        nlndwcharging_locations_event_producer = NLNDWChargingLocationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwcharging_locations_event_producer = NLNDWChargingLocationsEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.Charging.ChargingLocation ----
    # TODO: Supply event data for the NL.NDW.Charging.ChargingLocation event
    _charging_location = ChargingLocation()

    # sends the 'NL.NDW.Charging.ChargingLocation' event to Kafka topic.
    await nlndwcharging_locations_event_producer.send_nl_ndw_charging_charging_location(_location_id = 'TODO: replace me', _last_updated = 'TODO: replace me', data = _charging_location)
    print(f"Sent 'NL.NDW.Charging.ChargingLocation' event: {_charging_location.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nlndwcharging_evse_event_producer = NLNDWChargingEvseEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwcharging_evse_event_producer = NLNDWChargingEvseEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.Charging.EvseStatus ----
    # TODO: Supply event data for the NL.NDW.Charging.EvseStatus event
    _evse_status = EvseStatus()

    # sends the 'NL.NDW.Charging.EvseStatus' event to Kafka topic.
    await nlndwcharging_evse_event_producer.send_nl_ndw_charging_evse_status(_location_id = 'TODO: replace me', _evse_uid = 'TODO: replace me', _last_updated = 'TODO: replace me', data = _evse_status)
    print(f"Sent 'NL.NDW.Charging.EvseStatus' event: {_evse_status.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nlndwcharging_tariffs_event_producer = NLNDWChargingTariffsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwcharging_tariffs_event_producer = NLNDWChargingTariffsEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.Charging.ChargingTariff ----
    # TODO: Supply event data for the NL.NDW.Charging.ChargingTariff event
    _charging_tariff = ChargingTariff()

    # sends the 'NL.NDW.Charging.ChargingTariff' event to Kafka topic.
    await nlndwcharging_tariffs_event_producer.send_nl_ndw_charging_charging_tariff(_tariff_id = 'TODO: replace me', _last_updated = 'TODO: replace me', data = _charging_tariff)
    print(f"Sent 'NL.NDW.Charging.ChargingTariff' event: {_charging_tariff.to_json()}")

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