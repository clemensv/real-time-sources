
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

from autobahn_producer_kafka_producer.producer import DEAutobahnEventProducer

# imports for the data classes for each event

from autobahn_producer_data.roadevent import RoadEvent
from autobahn_producer_data.warningevent import WarningEvent
from autobahn_producer_data.parkinglorry import ParkingLorry
from autobahn_producer_data.chargingstation import ChargingStation
from autobahn_producer_data.webcam import Webcam

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
        deautobahn_event_producer = DEAutobahnEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        deautobahn_event_producer = DEAutobahnEventProducer(kafka_producer, topic, 'binary')

    # ---- DE.Autobahn.RoadworkAppeared ----
    # TODO: Supply event data for the DE.Autobahn.RoadworkAppeared event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.RoadworkAppeared' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_roadwork_appeared(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.RoadworkAppeared' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.RoadworkUpdated ----
    # TODO: Supply event data for the DE.Autobahn.RoadworkUpdated event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.RoadworkUpdated' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_roadwork_updated(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.RoadworkUpdated' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.RoadworkResolved ----
    # TODO: Supply event data for the DE.Autobahn.RoadworkResolved event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.RoadworkResolved' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_roadwork_resolved(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.RoadworkResolved' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.ShortTermRoadworkAppeared ----
    # TODO: Supply event data for the DE.Autobahn.ShortTermRoadworkAppeared event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.ShortTermRoadworkAppeared' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_short_term_roadwork_appeared(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.ShortTermRoadworkAppeared' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.ShortTermRoadworkUpdated ----
    # TODO: Supply event data for the DE.Autobahn.ShortTermRoadworkUpdated event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.ShortTermRoadworkUpdated' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_short_term_roadwork_updated(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.ShortTermRoadworkUpdated' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.ShortTermRoadworkResolved ----
    # TODO: Supply event data for the DE.Autobahn.ShortTermRoadworkResolved event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.ShortTermRoadworkResolved' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_short_term_roadwork_resolved(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.ShortTermRoadworkResolved' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.WarningAppeared ----
    # TODO: Supply event data for the DE.Autobahn.WarningAppeared event
    _warning_event = WarningEvent()

    # sends the 'DE.Autobahn.WarningAppeared' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_warning_appeared(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _warning_event)
    print(f"Sent 'DE.Autobahn.WarningAppeared' event: {_warning_event.to_json()}")

    # ---- DE.Autobahn.WarningUpdated ----
    # TODO: Supply event data for the DE.Autobahn.WarningUpdated event
    _warning_event = WarningEvent()

    # sends the 'DE.Autobahn.WarningUpdated' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_warning_updated(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _warning_event)
    print(f"Sent 'DE.Autobahn.WarningUpdated' event: {_warning_event.to_json()}")

    # ---- DE.Autobahn.WarningResolved ----
    # TODO: Supply event data for the DE.Autobahn.WarningResolved event
    _warning_event = WarningEvent()

    # sends the 'DE.Autobahn.WarningResolved' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_warning_resolved(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _warning_event)
    print(f"Sent 'DE.Autobahn.WarningResolved' event: {_warning_event.to_json()}")

    # ---- DE.Autobahn.ClosureAppeared ----
    # TODO: Supply event data for the DE.Autobahn.ClosureAppeared event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.ClosureAppeared' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_closure_appeared(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.ClosureAppeared' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.ClosureUpdated ----
    # TODO: Supply event data for the DE.Autobahn.ClosureUpdated event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.ClosureUpdated' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_closure_updated(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.ClosureUpdated' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.ClosureResolved ----
    # TODO: Supply event data for the DE.Autobahn.ClosureResolved event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.ClosureResolved' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_closure_resolved(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.ClosureResolved' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.EntryExitClosureAppeared ----
    # TODO: Supply event data for the DE.Autobahn.EntryExitClosureAppeared event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.EntryExitClosureAppeared' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_entry_exit_closure_appeared(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.EntryExitClosureAppeared' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.EntryExitClosureUpdated ----
    # TODO: Supply event data for the DE.Autobahn.EntryExitClosureUpdated event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.EntryExitClosureUpdated' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_entry_exit_closure_updated(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.EntryExitClosureUpdated' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.EntryExitClosureResolved ----
    # TODO: Supply event data for the DE.Autobahn.EntryExitClosureResolved event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.EntryExitClosureResolved' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_entry_exit_closure_resolved(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.EntryExitClosureResolved' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.WeightLimit35RestrictionAppeared ----
    # TODO: Supply event data for the DE.Autobahn.WeightLimit35RestrictionAppeared event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.WeightLimit35RestrictionAppeared' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_weight_limit35_restriction_appeared(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.WeightLimit35RestrictionAppeared' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.WeightLimit35RestrictionUpdated ----
    # TODO: Supply event data for the DE.Autobahn.WeightLimit35RestrictionUpdated event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.WeightLimit35RestrictionUpdated' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_weight_limit35_restriction_updated(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.WeightLimit35RestrictionUpdated' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.WeightLimit35RestrictionResolved ----
    # TODO: Supply event data for the DE.Autobahn.WeightLimit35RestrictionResolved event
    _road_event = RoadEvent()

    # sends the 'DE.Autobahn.WeightLimit35RestrictionResolved' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_weight_limit35_restriction_resolved(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _road_event)
    print(f"Sent 'DE.Autobahn.WeightLimit35RestrictionResolved' event: {_road_event.to_json()}")

    # ---- DE.Autobahn.ParkingLorryAppeared ----
    # TODO: Supply event data for the DE.Autobahn.ParkingLorryAppeared event
    _parking_lorry = ParkingLorry()

    # sends the 'DE.Autobahn.ParkingLorryAppeared' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_parking_lorry_appeared(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _parking_lorry)
    print(f"Sent 'DE.Autobahn.ParkingLorryAppeared' event: {_parking_lorry.to_json()}")

    # ---- DE.Autobahn.ParkingLorryUpdated ----
    # TODO: Supply event data for the DE.Autobahn.ParkingLorryUpdated event
    _parking_lorry = ParkingLorry()

    # sends the 'DE.Autobahn.ParkingLorryUpdated' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_parking_lorry_updated(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _parking_lorry)
    print(f"Sent 'DE.Autobahn.ParkingLorryUpdated' event: {_parking_lorry.to_json()}")

    # ---- DE.Autobahn.ParkingLorryResolved ----
    # TODO: Supply event data for the DE.Autobahn.ParkingLorryResolved event
    _parking_lorry = ParkingLorry()

    # sends the 'DE.Autobahn.ParkingLorryResolved' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_parking_lorry_resolved(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _parking_lorry)
    print(f"Sent 'DE.Autobahn.ParkingLorryResolved' event: {_parking_lorry.to_json()}")

    # ---- DE.Autobahn.ElectricChargingStationAppeared ----
    # TODO: Supply event data for the DE.Autobahn.ElectricChargingStationAppeared event
    _charging_station = ChargingStation()

    # sends the 'DE.Autobahn.ElectricChargingStationAppeared' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_electric_charging_station_appeared(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _charging_station)
    print(f"Sent 'DE.Autobahn.ElectricChargingStationAppeared' event: {_charging_station.to_json()}")

    # ---- DE.Autobahn.ElectricChargingStationUpdated ----
    # TODO: Supply event data for the DE.Autobahn.ElectricChargingStationUpdated event
    _charging_station = ChargingStation()

    # sends the 'DE.Autobahn.ElectricChargingStationUpdated' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_electric_charging_station_updated(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _charging_station)
    print(f"Sent 'DE.Autobahn.ElectricChargingStationUpdated' event: {_charging_station.to_json()}")

    # ---- DE.Autobahn.ElectricChargingStationResolved ----
    # TODO: Supply event data for the DE.Autobahn.ElectricChargingStationResolved event
    _charging_station = ChargingStation()

    # sends the 'DE.Autobahn.ElectricChargingStationResolved' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_electric_charging_station_resolved(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _charging_station)
    print(f"Sent 'DE.Autobahn.ElectricChargingStationResolved' event: {_charging_station.to_json()}")

    # ---- DE.Autobahn.StrongElectricChargingStationAppeared ----
    # TODO: Supply event data for the DE.Autobahn.StrongElectricChargingStationAppeared event
    _charging_station = ChargingStation()

    # sends the 'DE.Autobahn.StrongElectricChargingStationAppeared' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_strong_electric_charging_station_appeared(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _charging_station)
    print(f"Sent 'DE.Autobahn.StrongElectricChargingStationAppeared' event: {_charging_station.to_json()}")

    # ---- DE.Autobahn.StrongElectricChargingStationUpdated ----
    # TODO: Supply event data for the DE.Autobahn.StrongElectricChargingStationUpdated event
    _charging_station = ChargingStation()

    # sends the 'DE.Autobahn.StrongElectricChargingStationUpdated' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_strong_electric_charging_station_updated(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _charging_station)
    print(f"Sent 'DE.Autobahn.StrongElectricChargingStationUpdated' event: {_charging_station.to_json()}")

    # ---- DE.Autobahn.StrongElectricChargingStationResolved ----
    # TODO: Supply event data for the DE.Autobahn.StrongElectricChargingStationResolved event
    _charging_station = ChargingStation()

    # sends the 'DE.Autobahn.StrongElectricChargingStationResolved' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_strong_electric_charging_station_resolved(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _charging_station)
    print(f"Sent 'DE.Autobahn.StrongElectricChargingStationResolved' event: {_charging_station.to_json()}")

    # ---- DE.Autobahn.WebcamAppeared ----
    # TODO: Supply event data for the DE.Autobahn.WebcamAppeared event
    _webcam = Webcam()

    # sends the 'DE.Autobahn.WebcamAppeared' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_webcam_appeared(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _webcam)
    print(f"Sent 'DE.Autobahn.WebcamAppeared' event: {_webcam.to_json()}")

    # ---- DE.Autobahn.WebcamUpdated ----
    # TODO: Supply event data for the DE.Autobahn.WebcamUpdated event
    _webcam = Webcam()

    # sends the 'DE.Autobahn.WebcamUpdated' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_webcam_updated(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _webcam)
    print(f"Sent 'DE.Autobahn.WebcamUpdated' event: {_webcam.to_json()}")

    # ---- DE.Autobahn.WebcamResolved ----
    # TODO: Supply event data for the DE.Autobahn.WebcamResolved event
    _webcam = Webcam()

    # sends the 'DE.Autobahn.WebcamResolved' event to Kafka topic.
    await deautobahn_event_producer.send_de_autobahn_webcam_resolved(_identifier = 'TODO: replace me', _event_time = 'TODO: replace me', data = _webcam)
    print(f"Sent 'DE.Autobahn.WebcamResolved' event: {_webcam.to_json()}")

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