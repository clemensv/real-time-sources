
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

from entsoe_producer_kafka_producer.producer import EuEntsoeTransparencyByDomainEventProducer
from entsoe_producer_kafka_producer.producer import EuEntsoeTransparencyByDomainPsrTypeEventProducer
from entsoe_producer_kafka_producer.producer import EuEntsoeTransparencyCrossBorderEventProducer
from entsoe_producer_kafka_producer.producer import EuEntsoeTransparencyByDomainMqttEventProducer
from entsoe_producer_kafka_producer.producer import EuEntsoeTransparencyByDomainPsrTypeMqttEventProducer
from entsoe_producer_kafka_producer.producer import EuEntsoeTransparencyCrossBorderMqttEventProducer
from entsoe_producer_kafka_producer.producer import EuEntsoeTransparencyByDomainAmqpEventProducer
from entsoe_producer_kafka_producer.producer import EuEntsoeTransparencyByDomainPsrTypeAmqpEventProducer
from entsoe_producer_kafka_producer.producer import EuEntsoeTransparencyCrossBorderAmqpEventProducer

# imports for the data classes for each event

from entsoe_producer_data import DayAheadPrices
from entsoe_producer_data import ActualTotalLoad
from entsoe_producer_data import LoadForecastMargin
from entsoe_producer_data import GenerationForecast
from entsoe_producer_data import ReservoirFillingInformation
from entsoe_producer_data import ActualGeneration
from entsoe_producer_data import ActualGenerationPerType
from entsoe_producer_data import WindSolarForecast
from entsoe_producer_data import WindSolarGeneration
from entsoe_producer_data import InstalledGenerationCapacityPerType
from entsoe_producer_data import CrossBorderPhysicalFlows

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
        eu_entsoe_transparency_by_domain_event_producer = EuEntsoeTransparencyByDomainEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        eu_entsoe_transparency_by_domain_event_producer = EuEntsoeTransparencyByDomainEventProducer(kafka_producer, topic, 'binary')

    # ---- eu.entsoe.transparency.DayAheadPrices ----
    # TODO: Supply event data for the eu.entsoe.transparency.DayAheadPrices event
    _day_ahead_prices = DayAheadPrices()

    # sends the 'eu.entsoe.transparency.DayAheadPrices' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_event_producer.send_eu_entsoe_transparency_day_ahead_prices(_in_domain = 'TODO: replace me', data = _day_ahead_prices)
    print(f"Sent 'eu.entsoe.transparency.DayAheadPrices' event: {_day_ahead_prices.to_json()}")

    # ---- eu.entsoe.transparency.ActualTotalLoad ----
    # TODO: Supply event data for the eu.entsoe.transparency.ActualTotalLoad event
    _actual_total_load = ActualTotalLoad()

    # sends the 'eu.entsoe.transparency.ActualTotalLoad' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_event_producer.send_eu_entsoe_transparency_actual_total_load(_in_domain = 'TODO: replace me', data = _actual_total_load)
    print(f"Sent 'eu.entsoe.transparency.ActualTotalLoad' event: {_actual_total_load.to_json()}")

    # ---- eu.entsoe.transparency.LoadForecastMargin ----
    # TODO: Supply event data for the eu.entsoe.transparency.LoadForecastMargin event
    _load_forecast_margin = LoadForecastMargin()

    # sends the 'eu.entsoe.transparency.LoadForecastMargin' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_event_producer.send_eu_entsoe_transparency_load_forecast_margin(_in_domain = 'TODO: replace me', data = _load_forecast_margin)
    print(f"Sent 'eu.entsoe.transparency.LoadForecastMargin' event: {_load_forecast_margin.to_json()}")

    # ---- eu.entsoe.transparency.GenerationForecast ----
    # TODO: Supply event data for the eu.entsoe.transparency.GenerationForecast event
    _generation_forecast = GenerationForecast()

    # sends the 'eu.entsoe.transparency.GenerationForecast' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_event_producer.send_eu_entsoe_transparency_generation_forecast(_in_domain = 'TODO: replace me', data = _generation_forecast)
    print(f"Sent 'eu.entsoe.transparency.GenerationForecast' event: {_generation_forecast.to_json()}")

    # ---- eu.entsoe.transparency.ReservoirFillingInformation ----
    # TODO: Supply event data for the eu.entsoe.transparency.ReservoirFillingInformation event
    _reservoir_filling_information = ReservoirFillingInformation()

    # sends the 'eu.entsoe.transparency.ReservoirFillingInformation' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_event_producer.send_eu_entsoe_transparency_reservoir_filling_information(_in_domain = 'TODO: replace me', data = _reservoir_filling_information)
    print(f"Sent 'eu.entsoe.transparency.ReservoirFillingInformation' event: {_reservoir_filling_information.to_json()}")

    # ---- eu.entsoe.transparency.ActualGeneration ----
    # TODO: Supply event data for the eu.entsoe.transparency.ActualGeneration event
    _actual_generation = ActualGeneration()

    # sends the 'eu.entsoe.transparency.ActualGeneration' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_event_producer.send_eu_entsoe_transparency_actual_generation(_in_domain = 'TODO: replace me', data = _actual_generation)
    print(f"Sent 'eu.entsoe.transparency.ActualGeneration' event: {_actual_generation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        eu_entsoe_transparency_by_domain_psr_type_event_producer = EuEntsoeTransparencyByDomainPsrTypeEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        eu_entsoe_transparency_by_domain_psr_type_event_producer = EuEntsoeTransparencyByDomainPsrTypeEventProducer(kafka_producer, topic, 'binary')

    # ---- eu.entsoe.transparency.ActualGenerationPerType ----
    # TODO: Supply event data for the eu.entsoe.transparency.ActualGenerationPerType event
    _actual_generation_per_type = ActualGenerationPerType()

    # sends the 'eu.entsoe.transparency.ActualGenerationPerType' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_psr_type_event_producer.send_eu_entsoe_transparency_actual_generation_per_type(_in_domain = 'TODO: replace me', _psr_type = 'TODO: replace me', data = _actual_generation_per_type)
    print(f"Sent 'eu.entsoe.transparency.ActualGenerationPerType' event: {_actual_generation_per_type.to_json()}")

    # ---- eu.entsoe.transparency.WindSolarForecast ----
    # TODO: Supply event data for the eu.entsoe.transparency.WindSolarForecast event
    _wind_solar_forecast = WindSolarForecast()

    # sends the 'eu.entsoe.transparency.WindSolarForecast' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_psr_type_event_producer.send_eu_entsoe_transparency_wind_solar_forecast(_in_domain = 'TODO: replace me', _psr_type = 'TODO: replace me', data = _wind_solar_forecast)
    print(f"Sent 'eu.entsoe.transparency.WindSolarForecast' event: {_wind_solar_forecast.to_json()}")

    # ---- eu.entsoe.transparency.WindSolarGeneration ----
    # TODO: Supply event data for the eu.entsoe.transparency.WindSolarGeneration event
    _wind_solar_generation = WindSolarGeneration()

    # sends the 'eu.entsoe.transparency.WindSolarGeneration' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_psr_type_event_producer.send_eu_entsoe_transparency_wind_solar_generation(_in_domain = 'TODO: replace me', _psr_type = 'TODO: replace me', data = _wind_solar_generation)
    print(f"Sent 'eu.entsoe.transparency.WindSolarGeneration' event: {_wind_solar_generation.to_json()}")

    # ---- eu.entsoe.transparency.InstalledGenerationCapacityPerType ----
    # TODO: Supply event data for the eu.entsoe.transparency.InstalledGenerationCapacityPerType event
    _installed_generation_capacity_per_type = InstalledGenerationCapacityPerType()

    # sends the 'eu.entsoe.transparency.InstalledGenerationCapacityPerType' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_psr_type_event_producer.send_eu_entsoe_transparency_installed_generation_capacity_per_type(_in_domain = 'TODO: replace me', _psr_type = 'TODO: replace me', data = _installed_generation_capacity_per_type)
    print(f"Sent 'eu.entsoe.transparency.InstalledGenerationCapacityPerType' event: {_installed_generation_capacity_per_type.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        eu_entsoe_transparency_cross_border_event_producer = EuEntsoeTransparencyCrossBorderEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        eu_entsoe_transparency_cross_border_event_producer = EuEntsoeTransparencyCrossBorderEventProducer(kafka_producer, topic, 'binary')

    # ---- eu.entsoe.transparency.CrossBorderPhysicalFlows ----
    # TODO: Supply event data for the eu.entsoe.transparency.CrossBorderPhysicalFlows event
    _cross_border_physical_flows = CrossBorderPhysicalFlows()

    # sends the 'eu.entsoe.transparency.CrossBorderPhysicalFlows' event to Kafka topic.
    await eu_entsoe_transparency_cross_border_event_producer.send_eu_entsoe_transparency_cross_border_physical_flows(_in_domain = 'TODO: replace me', _out_domain = 'TODO: replace me', data = _cross_border_physical_flows)
    print(f"Sent 'eu.entsoe.transparency.CrossBorderPhysicalFlows' event: {_cross_border_physical_flows.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        eu_entsoe_transparency_by_domain_mqtt_event_producer = EuEntsoeTransparencyByDomainMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        eu_entsoe_transparency_by_domain_mqtt_event_producer = EuEntsoeTransparencyByDomainMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- eu.entsoe.transparency.ByDomain.mqtt.DayAheadPrices ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomain.mqtt.DayAheadPrices event
    _day_ahead_prices = DayAheadPrices()

    # sends the 'eu.entsoe.transparency.ByDomain.mqtt.DayAheadPrices' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_mqtt_event_producer.send_eu_entsoe_transparency_by_domain_mqtt_day_ahead_prices(_in_domain = 'TODO: replace me', data = _day_ahead_prices)
    print(f"Sent 'eu.entsoe.transparency.ByDomain.mqtt.DayAheadPrices' event: {_day_ahead_prices.to_json()}")

    # ---- eu.entsoe.transparency.ByDomain.mqtt.ActualTotalLoad ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomain.mqtt.ActualTotalLoad event
    _actual_total_load = ActualTotalLoad()

    # sends the 'eu.entsoe.transparency.ByDomain.mqtt.ActualTotalLoad' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_mqtt_event_producer.send_eu_entsoe_transparency_by_domain_mqtt_actual_total_load(_in_domain = 'TODO: replace me', data = _actual_total_load)
    print(f"Sent 'eu.entsoe.transparency.ByDomain.mqtt.ActualTotalLoad' event: {_actual_total_load.to_json()}")

    # ---- eu.entsoe.transparency.ByDomain.mqtt.LoadForecastMargin ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomain.mqtt.LoadForecastMargin event
    _load_forecast_margin = LoadForecastMargin()

    # sends the 'eu.entsoe.transparency.ByDomain.mqtt.LoadForecastMargin' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_mqtt_event_producer.send_eu_entsoe_transparency_by_domain_mqtt_load_forecast_margin(_in_domain = 'TODO: replace me', data = _load_forecast_margin)
    print(f"Sent 'eu.entsoe.transparency.ByDomain.mqtt.LoadForecastMargin' event: {_load_forecast_margin.to_json()}")

    # ---- eu.entsoe.transparency.ByDomain.mqtt.GenerationForecast ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomain.mqtt.GenerationForecast event
    _generation_forecast = GenerationForecast()

    # sends the 'eu.entsoe.transparency.ByDomain.mqtt.GenerationForecast' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_mqtt_event_producer.send_eu_entsoe_transparency_by_domain_mqtt_generation_forecast(_in_domain = 'TODO: replace me', data = _generation_forecast)
    print(f"Sent 'eu.entsoe.transparency.ByDomain.mqtt.GenerationForecast' event: {_generation_forecast.to_json()}")

    # ---- eu.entsoe.transparency.ByDomain.mqtt.ReservoirFillingInformation ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomain.mqtt.ReservoirFillingInformation event
    _reservoir_filling_information = ReservoirFillingInformation()

    # sends the 'eu.entsoe.transparency.ByDomain.mqtt.ReservoirFillingInformation' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_mqtt_event_producer.send_eu_entsoe_transparency_by_domain_mqtt_reservoir_filling_information(_in_domain = 'TODO: replace me', data = _reservoir_filling_information)
    print(f"Sent 'eu.entsoe.transparency.ByDomain.mqtt.ReservoirFillingInformation' event: {_reservoir_filling_information.to_json()}")

    # ---- eu.entsoe.transparency.ByDomain.mqtt.ActualGeneration ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomain.mqtt.ActualGeneration event
    _actual_generation = ActualGeneration()

    # sends the 'eu.entsoe.transparency.ByDomain.mqtt.ActualGeneration' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_mqtt_event_producer.send_eu_entsoe_transparency_by_domain_mqtt_actual_generation(_in_domain = 'TODO: replace me', data = _actual_generation)
    print(f"Sent 'eu.entsoe.transparency.ByDomain.mqtt.ActualGeneration' event: {_actual_generation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        eu_entsoe_transparency_by_domain_psr_type_mqtt_event_producer = EuEntsoeTransparencyByDomainPsrTypeMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        eu_entsoe_transparency_by_domain_psr_type_mqtt_event_producer = EuEntsoeTransparencyByDomainPsrTypeMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- eu.entsoe.transparency.ByDomainPsrType.mqtt.ActualGenerationPerType ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomainPsrType.mqtt.ActualGenerationPerType event
    _actual_generation_per_type = ActualGenerationPerType()

    # sends the 'eu.entsoe.transparency.ByDomainPsrType.mqtt.ActualGenerationPerType' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_psr_type_mqtt_event_producer.send_eu_entsoe_transparency_by_domain_psr_type_mqtt_actual_generation_per_type(_in_domain = 'TODO: replace me', _psr_type = 'TODO: replace me', data = _actual_generation_per_type)
    print(f"Sent 'eu.entsoe.transparency.ByDomainPsrType.mqtt.ActualGenerationPerType' event: {_actual_generation_per_type.to_json()}")

    # ---- eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarForecast ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarForecast event
    _wind_solar_forecast = WindSolarForecast()

    # sends the 'eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarForecast' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_psr_type_mqtt_event_producer.send_eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_forecast(_in_domain = 'TODO: replace me', _psr_type = 'TODO: replace me', data = _wind_solar_forecast)
    print(f"Sent 'eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarForecast' event: {_wind_solar_forecast.to_json()}")

    # ---- eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarGeneration ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarGeneration event
    _wind_solar_generation = WindSolarGeneration()

    # sends the 'eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarGeneration' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_psr_type_mqtt_event_producer.send_eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_generation(_in_domain = 'TODO: replace me', _psr_type = 'TODO: replace me', data = _wind_solar_generation)
    print(f"Sent 'eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarGeneration' event: {_wind_solar_generation.to_json()}")

    # ---- eu.entsoe.transparency.ByDomainPsrType.mqtt.InstalledGenerationCapacityPerType ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomainPsrType.mqtt.InstalledGenerationCapacityPerType event
    _installed_generation_capacity_per_type = InstalledGenerationCapacityPerType()

    # sends the 'eu.entsoe.transparency.ByDomainPsrType.mqtt.InstalledGenerationCapacityPerType' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_psr_type_mqtt_event_producer.send_eu_entsoe_transparency_by_domain_psr_type_mqtt_installed_generation_capacity_per_type(_in_domain = 'TODO: replace me', _psr_type = 'TODO: replace me', data = _installed_generation_capacity_per_type)
    print(f"Sent 'eu.entsoe.transparency.ByDomainPsrType.mqtt.InstalledGenerationCapacityPerType' event: {_installed_generation_capacity_per_type.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        eu_entsoe_transparency_cross_border_mqtt_event_producer = EuEntsoeTransparencyCrossBorderMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        eu_entsoe_transparency_cross_border_mqtt_event_producer = EuEntsoeTransparencyCrossBorderMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- eu.entsoe.transparency.CrossBorder.mqtt.CrossBorderPhysicalFlows ----
    # TODO: Supply event data for the eu.entsoe.transparency.CrossBorder.mqtt.CrossBorderPhysicalFlows event
    _cross_border_physical_flows = CrossBorderPhysicalFlows()

    # sends the 'eu.entsoe.transparency.CrossBorder.mqtt.CrossBorderPhysicalFlows' event to Kafka topic.
    await eu_entsoe_transparency_cross_border_mqtt_event_producer.send_eu_entsoe_transparency_cross_border_mqtt_cross_border_physical_flows(_in_domain = 'TODO: replace me', _out_domain = 'TODO: replace me', data = _cross_border_physical_flows)
    print(f"Sent 'eu.entsoe.transparency.CrossBorder.mqtt.CrossBorderPhysicalFlows' event: {_cross_border_physical_flows.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        eu_entsoe_transparency_by_domain_amqp_event_producer = EuEntsoeTransparencyByDomainAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        eu_entsoe_transparency_by_domain_amqp_event_producer = EuEntsoeTransparencyByDomainAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- eu.entsoe.transparency.ByDomain.amqp.DayAheadPrices ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomain.amqp.DayAheadPrices event
    _day_ahead_prices = DayAheadPrices()

    # sends the 'eu.entsoe.transparency.ByDomain.amqp.DayAheadPrices' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_amqp_event_producer.send_eu_entsoe_transparency_by_domain_amqp_day_ahead_prices(_in_domain = 'TODO: replace me', data = _day_ahead_prices)
    print(f"Sent 'eu.entsoe.transparency.ByDomain.amqp.DayAheadPrices' event: {_day_ahead_prices.to_json()}")

    # ---- eu.entsoe.transparency.ByDomain.amqp.ActualTotalLoad ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomain.amqp.ActualTotalLoad event
    _actual_total_load = ActualTotalLoad()

    # sends the 'eu.entsoe.transparency.ByDomain.amqp.ActualTotalLoad' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_amqp_event_producer.send_eu_entsoe_transparency_by_domain_amqp_actual_total_load(_in_domain = 'TODO: replace me', data = _actual_total_load)
    print(f"Sent 'eu.entsoe.transparency.ByDomain.amqp.ActualTotalLoad' event: {_actual_total_load.to_json()}")

    # ---- eu.entsoe.transparency.ByDomain.amqp.LoadForecastMargin ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomain.amqp.LoadForecastMargin event
    _load_forecast_margin = LoadForecastMargin()

    # sends the 'eu.entsoe.transparency.ByDomain.amqp.LoadForecastMargin' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_amqp_event_producer.send_eu_entsoe_transparency_by_domain_amqp_load_forecast_margin(_in_domain = 'TODO: replace me', data = _load_forecast_margin)
    print(f"Sent 'eu.entsoe.transparency.ByDomain.amqp.LoadForecastMargin' event: {_load_forecast_margin.to_json()}")

    # ---- eu.entsoe.transparency.ByDomain.amqp.GenerationForecast ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomain.amqp.GenerationForecast event
    _generation_forecast = GenerationForecast()

    # sends the 'eu.entsoe.transparency.ByDomain.amqp.GenerationForecast' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_amqp_event_producer.send_eu_entsoe_transparency_by_domain_amqp_generation_forecast(_in_domain = 'TODO: replace me', data = _generation_forecast)
    print(f"Sent 'eu.entsoe.transparency.ByDomain.amqp.GenerationForecast' event: {_generation_forecast.to_json()}")

    # ---- eu.entsoe.transparency.ByDomain.amqp.ReservoirFillingInformation ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomain.amqp.ReservoirFillingInformation event
    _reservoir_filling_information = ReservoirFillingInformation()

    # sends the 'eu.entsoe.transparency.ByDomain.amqp.ReservoirFillingInformation' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_amqp_event_producer.send_eu_entsoe_transparency_by_domain_amqp_reservoir_filling_information(_in_domain = 'TODO: replace me', data = _reservoir_filling_information)
    print(f"Sent 'eu.entsoe.transparency.ByDomain.amqp.ReservoirFillingInformation' event: {_reservoir_filling_information.to_json()}")

    # ---- eu.entsoe.transparency.ByDomain.amqp.ActualGeneration ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomain.amqp.ActualGeneration event
    _actual_generation = ActualGeneration()

    # sends the 'eu.entsoe.transparency.ByDomain.amqp.ActualGeneration' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_amqp_event_producer.send_eu_entsoe_transparency_by_domain_amqp_actual_generation(_in_domain = 'TODO: replace me', data = _actual_generation)
    print(f"Sent 'eu.entsoe.transparency.ByDomain.amqp.ActualGeneration' event: {_actual_generation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        eu_entsoe_transparency_by_domain_psr_type_amqp_event_producer = EuEntsoeTransparencyByDomainPsrTypeAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        eu_entsoe_transparency_by_domain_psr_type_amqp_event_producer = EuEntsoeTransparencyByDomainPsrTypeAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- eu.entsoe.transparency.ByDomainPsrType.amqp.ActualGenerationPerType ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomainPsrType.amqp.ActualGenerationPerType event
    _actual_generation_per_type = ActualGenerationPerType()

    # sends the 'eu.entsoe.transparency.ByDomainPsrType.amqp.ActualGenerationPerType' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_psr_type_amqp_event_producer.send_eu_entsoe_transparency_by_domain_psr_type_amqp_actual_generation_per_type(_in_domain = 'TODO: replace me', _psr_type = 'TODO: replace me', data = _actual_generation_per_type)
    print(f"Sent 'eu.entsoe.transparency.ByDomainPsrType.amqp.ActualGenerationPerType' event: {_actual_generation_per_type.to_json()}")

    # ---- eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarForecast ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarForecast event
    _wind_solar_forecast = WindSolarForecast()

    # sends the 'eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarForecast' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_psr_type_amqp_event_producer.send_eu_entsoe_transparency_by_domain_psr_type_amqp_wind_solar_forecast(_in_domain = 'TODO: replace me', _psr_type = 'TODO: replace me', data = _wind_solar_forecast)
    print(f"Sent 'eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarForecast' event: {_wind_solar_forecast.to_json()}")

    # ---- eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarGeneration ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarGeneration event
    _wind_solar_generation = WindSolarGeneration()

    # sends the 'eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarGeneration' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_psr_type_amqp_event_producer.send_eu_entsoe_transparency_by_domain_psr_type_amqp_wind_solar_generation(_in_domain = 'TODO: replace me', _psr_type = 'TODO: replace me', data = _wind_solar_generation)
    print(f"Sent 'eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarGeneration' event: {_wind_solar_generation.to_json()}")

    # ---- eu.entsoe.transparency.ByDomainPsrType.amqp.InstalledGenerationCapacityPerType ----
    # TODO: Supply event data for the eu.entsoe.transparency.ByDomainPsrType.amqp.InstalledGenerationCapacityPerType event
    _installed_generation_capacity_per_type = InstalledGenerationCapacityPerType()

    # sends the 'eu.entsoe.transparency.ByDomainPsrType.amqp.InstalledGenerationCapacityPerType' event to Kafka topic.
    await eu_entsoe_transparency_by_domain_psr_type_amqp_event_producer.send_eu_entsoe_transparency_by_domain_psr_type_amqp_installed_generation_capacity_per_type(_in_domain = 'TODO: replace me', _psr_type = 'TODO: replace me', data = _installed_generation_capacity_per_type)
    print(f"Sent 'eu.entsoe.transparency.ByDomainPsrType.amqp.InstalledGenerationCapacityPerType' event: {_installed_generation_capacity_per_type.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        eu_entsoe_transparency_cross_border_amqp_event_producer = EuEntsoeTransparencyCrossBorderAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        eu_entsoe_transparency_cross_border_amqp_event_producer = EuEntsoeTransparencyCrossBorderAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- eu.entsoe.transparency.CrossBorder.amqp.CrossBorderPhysicalFlows ----
    # TODO: Supply event data for the eu.entsoe.transparency.CrossBorder.amqp.CrossBorderPhysicalFlows event
    _cross_border_physical_flows = CrossBorderPhysicalFlows()

    # sends the 'eu.entsoe.transparency.CrossBorder.amqp.CrossBorderPhysicalFlows' event to Kafka topic.
    await eu_entsoe_transparency_cross_border_amqp_event_producer.send_eu_entsoe_transparency_cross_border_amqp_cross_border_physical_flows(_in_domain = 'TODO: replace me', _out_domain = 'TODO: replace me', data = _cross_border_physical_flows)
    print(f"Sent 'eu.entsoe.transparency.CrossBorder.amqp.CrossBorderPhysicalFlows' event: {_cross_border_physical_flows.to_json()}")

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