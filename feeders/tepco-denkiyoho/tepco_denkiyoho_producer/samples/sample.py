
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

from tepco_denkiyoho_producer_kafka_producer.producer import JPTEPCODenkiyohoEventProducer
from tepco_denkiyoho_producer_kafka_producer.producer import JPTEPCODenkiyohoMqttEventProducer
from tepco_denkiyoho_producer_kafka_producer.producer import JPTEPCODenkiyohoAmqpEventProducer

# imports for the data classes for each event

from tepco_denkiyoho_producer_data.supplycapacity import SupplyCapacity
from tepco_denkiyoho_producer_data.peakdemandforecast import PeakDemandForecast
from tepco_denkiyoho_producer_data.demandactual import DemandActual
from tepco_denkiyoho_producer_data.demandforecast import DemandForecast
from tepco_denkiyoho_producer_data.info import Info

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
        jptepcodenkiyoho_event_producer = JPTEPCODenkiyohoEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        jptepcodenkiyoho_event_producer = JPTEPCODenkiyohoEventProducer(kafka_producer, topic, 'binary')

    # ---- jp.tepco.denkiyoho.SupplyCapacity ----
    # TODO: Supply event data for the jp.tepco.denkiyoho.SupplyCapacity event
    _supply_capacity = SupplyCapacity()

    # sends the 'jp.tepco.denkiyoho.SupplyCapacity' event to Kafka topic.
    await jptepcodenkiyoho_event_producer.send_jp_tepco_denkiyoho_supply_capacity(_feedurl = 'TODO: replace me', _date = 'TODO: replace me', _time = 'TODO: replace me', data = _supply_capacity)
    print(f"Sent 'jp.tepco.denkiyoho.SupplyCapacity' event: {_supply_capacity.to_json()}")

    # ---- jp.tepco.denkiyoho.PeakDemandForecast ----
    # TODO: Supply event data for the jp.tepco.denkiyoho.PeakDemandForecast event
    _peak_demand_forecast = PeakDemandForecast()

    # sends the 'jp.tepco.denkiyoho.PeakDemandForecast' event to Kafka topic.
    await jptepcodenkiyoho_event_producer.send_jp_tepco_denkiyoho_peak_demand_forecast(_feedurl = 'TODO: replace me', _date = 'TODO: replace me', _time = 'TODO: replace me', data = _peak_demand_forecast)
    print(f"Sent 'jp.tepco.denkiyoho.PeakDemandForecast' event: {_peak_demand_forecast.to_json()}")

    # ---- jp.tepco.denkiyoho.DemandActual ----
    # TODO: Supply event data for the jp.tepco.denkiyoho.DemandActual event
    _demand_actual = DemandActual()

    # sends the 'jp.tepco.denkiyoho.DemandActual' event to Kafka topic.
    await jptepcodenkiyoho_event_producer.send_jp_tepco_denkiyoho_demand_actual(_feedurl = 'TODO: replace me', _date = 'TODO: replace me', _time = 'TODO: replace me', data = _demand_actual)
    print(f"Sent 'jp.tepco.denkiyoho.DemandActual' event: {_demand_actual.to_json()}")

    # ---- jp.tepco.denkiyoho.DemandForecast ----
    # TODO: Supply event data for the jp.tepco.denkiyoho.DemandForecast event
    _demand_forecast = DemandForecast()

    # sends the 'jp.tepco.denkiyoho.DemandForecast' event to Kafka topic.
    await jptepcodenkiyoho_event_producer.send_jp_tepco_denkiyoho_demand_forecast(_feedurl = 'TODO: replace me', _date = 'TODO: replace me', _time = 'TODO: replace me', data = _demand_forecast)
    print(f"Sent 'jp.tepco.denkiyoho.DemandForecast' event: {_demand_forecast.to_json()}")

    # ---- JP.TEPCO.Denkiyoho.Info ----
    # TODO: Supply event data for the JP.TEPCO.Denkiyoho.Info event
    _info = Info()

    # sends the 'JP.TEPCO.Denkiyoho.Info' event to Kafka topic.
    await jptepcodenkiyoho_event_producer.send_jp_tepco_denkiyoho_info(_area_code = 'TODO: replace me', data = _info)
    print(f"Sent 'JP.TEPCO.Denkiyoho.Info' event: {_info.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        jptepcodenkiyoho_mqtt_event_producer = JPTEPCODenkiyohoMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        jptepcodenkiyoho_mqtt_event_producer = JPTEPCODenkiyohoMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- JP.TEPCO.Denkiyoho.mqtt.SupplyCapacity ----
    # TODO: Supply event data for the JP.TEPCO.Denkiyoho.mqtt.SupplyCapacity event
    _supply_capacity = SupplyCapacity()

    # sends the 'JP.TEPCO.Denkiyoho.mqtt.SupplyCapacity' event to Kafka topic.
    await jptepcodenkiyoho_mqtt_event_producer.send_jp_tepco_denkiyoho_mqtt_supply_capacity(_feedurl = 'TODO: replace me', _date = 'TODO: replace me', _time = 'TODO: replace me', data = _supply_capacity)
    print(f"Sent 'JP.TEPCO.Denkiyoho.mqtt.SupplyCapacity' event: {_supply_capacity.to_json()}")

    # ---- JP.TEPCO.Denkiyoho.mqtt.PeakDemandForecast ----
    # TODO: Supply event data for the JP.TEPCO.Denkiyoho.mqtt.PeakDemandForecast event
    _peak_demand_forecast = PeakDemandForecast()

    # sends the 'JP.TEPCO.Denkiyoho.mqtt.PeakDemandForecast' event to Kafka topic.
    await jptepcodenkiyoho_mqtt_event_producer.send_jp_tepco_denkiyoho_mqtt_peak_demand_forecast(_feedurl = 'TODO: replace me', _date = 'TODO: replace me', _time = 'TODO: replace me', data = _peak_demand_forecast)
    print(f"Sent 'JP.TEPCO.Denkiyoho.mqtt.PeakDemandForecast' event: {_peak_demand_forecast.to_json()}")

    # ---- JP.TEPCO.Denkiyoho.mqtt.DemandActual ----
    # TODO: Supply event data for the JP.TEPCO.Denkiyoho.mqtt.DemandActual event
    _demand_actual = DemandActual()

    # sends the 'JP.TEPCO.Denkiyoho.mqtt.DemandActual' event to Kafka topic.
    await jptepcodenkiyoho_mqtt_event_producer.send_jp_tepco_denkiyoho_mqtt_demand_actual(_feedurl = 'TODO: replace me', _date = 'TODO: replace me', _time = 'TODO: replace me', data = _demand_actual)
    print(f"Sent 'JP.TEPCO.Denkiyoho.mqtt.DemandActual' event: {_demand_actual.to_json()}")

    # ---- JP.TEPCO.Denkiyoho.mqtt.DemandForecast ----
    # TODO: Supply event data for the JP.TEPCO.Denkiyoho.mqtt.DemandForecast event
    _demand_forecast = DemandForecast()

    # sends the 'JP.TEPCO.Denkiyoho.mqtt.DemandForecast' event to Kafka topic.
    await jptepcodenkiyoho_mqtt_event_producer.send_jp_tepco_denkiyoho_mqtt_demand_forecast(_feedurl = 'TODO: replace me', _date = 'TODO: replace me', _time = 'TODO: replace me', data = _demand_forecast)
    print(f"Sent 'JP.TEPCO.Denkiyoho.mqtt.DemandForecast' event: {_demand_forecast.to_json()}")

    # ---- JP.TEPCO.Denkiyoho.mqtt.Info ----
    # TODO: Supply event data for the JP.TEPCO.Denkiyoho.mqtt.Info event
    _info = Info()

    # sends the 'JP.TEPCO.Denkiyoho.mqtt.Info' event to Kafka topic.
    await jptepcodenkiyoho_mqtt_event_producer.send_jp_tepco_denkiyoho_mqtt_info(_area_code = 'TODO: replace me', data = _info)
    print(f"Sent 'JP.TEPCO.Denkiyoho.mqtt.Info' event: {_info.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        jptepcodenkiyoho_amqp_event_producer = JPTEPCODenkiyohoAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        jptepcodenkiyoho_amqp_event_producer = JPTEPCODenkiyohoAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- JP.TEPCO.Denkiyoho.amqp.SupplyCapacity ----
    # TODO: Supply event data for the JP.TEPCO.Denkiyoho.amqp.SupplyCapacity event
    _supply_capacity = SupplyCapacity()

    # sends the 'JP.TEPCO.Denkiyoho.amqp.SupplyCapacity' event to Kafka topic.
    await jptepcodenkiyoho_amqp_event_producer.send_jp_tepco_denkiyoho_amqp_supply_capacity(_feedurl = 'TODO: replace me', _date = 'TODO: replace me', _time = 'TODO: replace me', data = _supply_capacity)
    print(f"Sent 'JP.TEPCO.Denkiyoho.amqp.SupplyCapacity' event: {_supply_capacity.to_json()}")

    # ---- JP.TEPCO.Denkiyoho.amqp.PeakDemandForecast ----
    # TODO: Supply event data for the JP.TEPCO.Denkiyoho.amqp.PeakDemandForecast event
    _peak_demand_forecast = PeakDemandForecast()

    # sends the 'JP.TEPCO.Denkiyoho.amqp.PeakDemandForecast' event to Kafka topic.
    await jptepcodenkiyoho_amqp_event_producer.send_jp_tepco_denkiyoho_amqp_peak_demand_forecast(_feedurl = 'TODO: replace me', _date = 'TODO: replace me', _time = 'TODO: replace me', data = _peak_demand_forecast)
    print(f"Sent 'JP.TEPCO.Denkiyoho.amqp.PeakDemandForecast' event: {_peak_demand_forecast.to_json()}")

    # ---- JP.TEPCO.Denkiyoho.amqp.DemandActual ----
    # TODO: Supply event data for the JP.TEPCO.Denkiyoho.amqp.DemandActual event
    _demand_actual = DemandActual()

    # sends the 'JP.TEPCO.Denkiyoho.amqp.DemandActual' event to Kafka topic.
    await jptepcodenkiyoho_amqp_event_producer.send_jp_tepco_denkiyoho_amqp_demand_actual(_feedurl = 'TODO: replace me', _date = 'TODO: replace me', _time = 'TODO: replace me', data = _demand_actual)
    print(f"Sent 'JP.TEPCO.Denkiyoho.amqp.DemandActual' event: {_demand_actual.to_json()}")

    # ---- JP.TEPCO.Denkiyoho.amqp.DemandForecast ----
    # TODO: Supply event data for the JP.TEPCO.Denkiyoho.amqp.DemandForecast event
    _demand_forecast = DemandForecast()

    # sends the 'JP.TEPCO.Denkiyoho.amqp.DemandForecast' event to Kafka topic.
    await jptepcodenkiyoho_amqp_event_producer.send_jp_tepco_denkiyoho_amqp_demand_forecast(_feedurl = 'TODO: replace me', _date = 'TODO: replace me', _time = 'TODO: replace me', data = _demand_forecast)
    print(f"Sent 'JP.TEPCO.Denkiyoho.amqp.DemandForecast' event: {_demand_forecast.to_json()}")

    # ---- JP.TEPCO.Denkiyoho.amqp.Info ----
    # TODO: Supply event data for the JP.TEPCO.Denkiyoho.amqp.Info event
    _info = Info()

    # sends the 'JP.TEPCO.Denkiyoho.amqp.Info' event to Kafka topic.
    await jptepcodenkiyoho_amqp_event_producer.send_jp_tepco_denkiyoho_amqp_info(_area_code = 'TODO: replace me', data = _info)
    print(f"Sent 'JP.TEPCO.Denkiyoho.amqp.Info' event: {_info.to_json()}")

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