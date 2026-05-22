
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

from dmi_producer_kafka_producer.producer import DkDmiMetObsKafkaEventProducer
from dmi_producer_kafka_producer.producer import DkDmiOceanObsKafkaEventProducer
from dmi_producer_kafka_producer.producer import DkDmiLightningKafkaEventProducer

# imports for the data classes for each event

from dmi_producer_data.station import Station
from dmi_producer_data.observation import Observation
from dmi_producer_data.tidewaterstation import TidewaterStation
from dmi_producer_data.tidewaterprediction import TidewaterPrediction
from dmi_producer_data.sensor import Sensor
from dmi_producer_data.strike import Strike

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
        dk_dmi_met_obs_kafka_event_producer = DkDmiMetObsKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        dk_dmi_met_obs_kafka_event_producer = DkDmiMetObsKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- dk.dmi.metObs.kafka.Station ----
    # TODO: Supply event data for the dk.dmi.metObs.kafka.Station event
    _station = Station()

    # sends the 'dk.dmi.metObs.kafka.Station' event to Kafka topic.
    await dk_dmi_met_obs_kafka_event_producer.send_dk_dmi_met_obs_kafka_station(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'dk.dmi.metObs.kafka.Station' event: {_station.to_json()}")

    # ---- dk.dmi.metObs.kafka.Observation ----
    # TODO: Supply event data for the dk.dmi.metObs.kafka.Observation event
    _observation = Observation()

    # sends the 'dk.dmi.metObs.kafka.Observation' event to Kafka topic.
    await dk_dmi_met_obs_kafka_event_producer.send_dk_dmi_met_obs_kafka_observation(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', _parameter_id = 'TODO: replace me', data = _observation)
    print(f"Sent 'dk.dmi.metObs.kafka.Observation' event: {_observation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        dk_dmi_ocean_obs_kafka_event_producer = DkDmiOceanObsKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        dk_dmi_ocean_obs_kafka_event_producer = DkDmiOceanObsKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- dk.dmi.oceanObs.kafka.Station ----
    # TODO: Supply event data for the dk.dmi.oceanObs.kafka.Station event
    _station = Station()

    # sends the 'dk.dmi.oceanObs.kafka.Station' event to Kafka topic.
    await dk_dmi_ocean_obs_kafka_event_producer.send_dk_dmi_ocean_obs_kafka_station(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'dk.dmi.oceanObs.kafka.Station' event: {_station.to_json()}")

    # ---- dk.dmi.oceanObs.kafka.TidewaterStation ----
    # TODO: Supply event data for the dk.dmi.oceanObs.kafka.TidewaterStation event
    _tidewater_station = TidewaterStation()

    # sends the 'dk.dmi.oceanObs.kafka.TidewaterStation' event to Kafka topic.
    await dk_dmi_ocean_obs_kafka_event_producer.send_dk_dmi_ocean_obs_kafka_tidewater_station(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _tidewater_station)
    print(f"Sent 'dk.dmi.oceanObs.kafka.TidewaterStation' event: {_tidewater_station.to_json()}")

    # ---- dk.dmi.oceanObs.kafka.Observation ----
    # TODO: Supply event data for the dk.dmi.oceanObs.kafka.Observation event
    _observation = Observation()

    # sends the 'dk.dmi.oceanObs.kafka.Observation' event to Kafka topic.
    await dk_dmi_ocean_obs_kafka_event_producer.send_dk_dmi_ocean_obs_kafka_observation(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', _parameter_id = 'TODO: replace me', data = _observation)
    print(f"Sent 'dk.dmi.oceanObs.kafka.Observation' event: {_observation.to_json()}")

    # ---- dk.dmi.oceanObs.kafka.TidewaterPrediction ----
    # TODO: Supply event data for the dk.dmi.oceanObs.kafka.TidewaterPrediction event
    _tidewater_prediction = TidewaterPrediction()

    # sends the 'dk.dmi.oceanObs.kafka.TidewaterPrediction' event to Kafka topic.
    await dk_dmi_ocean_obs_kafka_event_producer.send_dk_dmi_ocean_obs_kafka_tidewater_prediction(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _tidewater_prediction)
    print(f"Sent 'dk.dmi.oceanObs.kafka.TidewaterPrediction' event: {_tidewater_prediction.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        dk_dmi_lightning_kafka_event_producer = DkDmiLightningKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        dk_dmi_lightning_kafka_event_producer = DkDmiLightningKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- dk.dmi.lightning.kafka.Sensor ----
    # TODO: Supply event data for the dk.dmi.lightning.kafka.Sensor event
    _sensor = Sensor()

    # sends the 'dk.dmi.lightning.kafka.Sensor' event to Kafka topic.
    await dk_dmi_lightning_kafka_event_producer.send_dk_dmi_lightning_kafka_sensor(_feedurl = 'TODO: replace me', _sensor_id = 'TODO: replace me', data = _sensor)
    print(f"Sent 'dk.dmi.lightning.kafka.Sensor' event: {_sensor.to_json()}")

    # ---- dk.dmi.lightning.kafka.Strike ----
    # TODO: Supply event data for the dk.dmi.lightning.kafka.Strike event
    _strike = Strike()

    # sends the 'dk.dmi.lightning.kafka.Strike' event to Kafka topic.
    await dk_dmi_lightning_kafka_event_producer.send_dk_dmi_lightning_kafka_strike(_feedurl = 'TODO: replace me', _strike_id = 'TODO: replace me', data = _strike)
    print(f"Sent 'dk.dmi.lightning.kafka.Strike' event: {_strike.to_json()}")

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