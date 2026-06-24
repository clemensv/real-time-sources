
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

from nws_forecasts_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAANWSForecastsEventProducer
from nws_forecasts_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAANWSForecastsMqttEventProducer
from nws_forecasts_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAANWSForecastsAmqpEventProducer

# imports for the data classes for each event

from nws_forecasts_producer_data import ForecastZone
from nws_forecasts_producer_data import LandZoneForecast
from nws_forecasts_producer_data import MarineZoneForecast

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
        microsoft_open_data_usnoaanwsforecasts_event_producer = MicrosoftOpenDataUSNOAANWSForecastsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaanwsforecasts_event_producer = MicrosoftOpenDataUSNOAANWSForecastsEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.NWS.ForecastZone ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NWS.ForecastZone event
    _forecast_zone = ForecastZone()

    # sends the 'Microsoft.OpenData.US.NOAA.NWS.ForecastZone' event to Kafka topic.
    await microsoft_open_data_usnoaanwsforecasts_event_producer.send_microsoft_open_data_us_noaa_nws_forecast_zone(_zone_id = 'TODO: replace me', data = _forecast_zone)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NWS.ForecastZone' event: {_forecast_zone.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NWS.LandZoneForecast ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NWS.LandZoneForecast event
    _land_zone_forecast = LandZoneForecast()

    # sends the 'Microsoft.OpenData.US.NOAA.NWS.LandZoneForecast' event to Kafka topic.
    await microsoft_open_data_usnoaanwsforecasts_event_producer.send_microsoft_open_data_us_noaa_nws_land_zone_forecast(_zone_id = 'TODO: replace me', data = _land_zone_forecast)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NWS.LandZoneForecast' event: {_land_zone_forecast.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NWS.MarineZoneForecast ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NWS.MarineZoneForecast event
    _marine_zone_forecast = MarineZoneForecast()

    # sends the 'Microsoft.OpenData.US.NOAA.NWS.MarineZoneForecast' event to Kafka topic.
    await microsoft_open_data_usnoaanwsforecasts_event_producer.send_microsoft_open_data_us_noaa_nws_marine_zone_forecast(_zone_id = 'TODO: replace me', data = _marine_zone_forecast)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NWS.MarineZoneForecast' event: {_marine_zone_forecast.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        microsoft_open_data_usnoaanwsforecasts_mqtt_event_producer = MicrosoftOpenDataUSNOAANWSForecastsMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaanwsforecasts_mqtt_event_producer = MicrosoftOpenDataUSNOAANWSForecastsMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.NWS.Forecasts.ForecastZone.mqtt ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NWS.Forecasts.ForecastZone.mqtt event
    _forecast_zone = ForecastZone()

    # sends the 'Microsoft.OpenData.US.NOAA.NWS.Forecasts.ForecastZone.mqtt' event to Kafka topic.
    await microsoft_open_data_usnoaanwsforecasts_mqtt_event_producer.send_microsoft_open_data_us_noaa_nws_forecasts_forecast_zone_mqtt(_zone_id = 'TODO: replace me', data = _forecast_zone)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NWS.Forecasts.ForecastZone.mqtt' event: {_forecast_zone.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NWS.Forecasts.LandZoneForecast.mqtt ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NWS.Forecasts.LandZoneForecast.mqtt event
    _land_zone_forecast = LandZoneForecast()

    # sends the 'Microsoft.OpenData.US.NOAA.NWS.Forecasts.LandZoneForecast.mqtt' event to Kafka topic.
    await microsoft_open_data_usnoaanwsforecasts_mqtt_event_producer.send_microsoft_open_data_us_noaa_nws_forecasts_land_zone_forecast_mqtt(_zone_id = 'TODO: replace me', data = _land_zone_forecast)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NWS.Forecasts.LandZoneForecast.mqtt' event: {_land_zone_forecast.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NWS.Forecasts.MarineZoneForecast.mqtt ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NWS.Forecasts.MarineZoneForecast.mqtt event
    _marine_zone_forecast = MarineZoneForecast()

    # sends the 'Microsoft.OpenData.US.NOAA.NWS.Forecasts.MarineZoneForecast.mqtt' event to Kafka topic.
    await microsoft_open_data_usnoaanwsforecasts_mqtt_event_producer.send_microsoft_open_data_us_noaa_nws_forecasts_marine_zone_forecast_mqtt(_zone_id = 'TODO: replace me', data = _marine_zone_forecast)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NWS.Forecasts.MarineZoneForecast.mqtt' event: {_marine_zone_forecast.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        microsoft_open_data_usnoaanwsforecasts_amqp_event_producer = MicrosoftOpenDataUSNOAANWSForecastsAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaanwsforecasts_amqp_event_producer = MicrosoftOpenDataUSNOAANWSForecastsAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.NWS.Forecasts.ForecastZone.amqp ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NWS.Forecasts.ForecastZone.amqp event
    _forecast_zone = ForecastZone()

    # sends the 'Microsoft.OpenData.US.NOAA.NWS.Forecasts.ForecastZone.amqp' event to Kafka topic.
    await microsoft_open_data_usnoaanwsforecasts_amqp_event_producer.send_microsoft_open_data_us_noaa_nws_forecasts_forecast_zone_amqp(_zone_id = 'TODO: replace me', data = _forecast_zone)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NWS.Forecasts.ForecastZone.amqp' event: {_forecast_zone.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NWS.Forecasts.LandZoneForecast.amqp ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NWS.Forecasts.LandZoneForecast.amqp event
    _land_zone_forecast = LandZoneForecast()

    # sends the 'Microsoft.OpenData.US.NOAA.NWS.Forecasts.LandZoneForecast.amqp' event to Kafka topic.
    await microsoft_open_data_usnoaanwsforecasts_amqp_event_producer.send_microsoft_open_data_us_noaa_nws_forecasts_land_zone_forecast_amqp(_zone_id = 'TODO: replace me', data = _land_zone_forecast)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NWS.Forecasts.LandZoneForecast.amqp' event: {_land_zone_forecast.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NWS.Forecasts.MarineZoneForecast.amqp ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NWS.Forecasts.MarineZoneForecast.amqp event
    _marine_zone_forecast = MarineZoneForecast()

    # sends the 'Microsoft.OpenData.US.NOAA.NWS.Forecasts.MarineZoneForecast.amqp' event to Kafka topic.
    await microsoft_open_data_usnoaanwsforecasts_amqp_event_producer.send_microsoft_open_data_us_noaa_nws_forecasts_marine_zone_forecast_amqp(_zone_id = 'TODO: replace me', data = _marine_zone_forecast)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NWS.Forecasts.MarineZoneForecast.amqp' event: {_marine_zone_forecast.to_json()}")

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