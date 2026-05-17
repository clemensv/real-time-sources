
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

from dwd_producer_kafka_producer.producer import DEDWDCDCEventProducer
from dwd_producer_kafka_producer.producer import DEDWDWeatherEventProducer
from dwd_producer_kafka_producer.producer import DEDWDRadarEventProducer
from dwd_producer_kafka_producer.producer import DEDWDForecastEventProducer

# imports for the data classes for each event

from dwd_producer_data.stationmetadata import StationMetadata
from dwd_producer_data.airtemperature10min import AirTemperature10Min
from dwd_producer_data.precipitation10min import Precipitation10Min
from dwd_producer_data.wind10min import Wind10Min
from dwd_producer_data.solar10min import Solar10Min
from dwd_producer_data.hourlyobservation import HourlyObservation
from dwd_producer_data.extremewind10min import ExtremeWind10Min
from dwd_producer_data.extremetemperature10min import ExtremeTemperature10Min
from dwd_producer_data.alert import Alert
from dwd_producer_data.radarproductcatalog import RadarProductCatalog
from dwd_producer_data.radarfileproduct import RadarFileProduct
from dwd_producer_data.forecastmodelcatalog import ForecastModelCatalog
from dwd_producer_data.icond2forecastfile import IconD2ForecastFile

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
        dedwdcdcevent_producer = DEDWDCDCEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        dedwdcdcevent_producer = DEDWDCDCEventProducer(kafka_producer, topic, 'binary')

    # ---- DE.DWD.CDC.StationMetadata ----
    # TODO: Supply event data for the DE.DWD.CDC.StationMetadata event
    _station_metadata = StationMetadata()

    # sends the 'DE.DWD.CDC.StationMetadata' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_cdc_station_metadata(_station_id = 'TODO: replace me', data = _station_metadata)
    print(f"Sent 'DE.DWD.CDC.StationMetadata' event: {_station_metadata.to_json()}")

    # ---- DE.DWD.CDC.AirTemperature10Min ----
    # TODO: Supply event data for the DE.DWD.CDC.AirTemperature10Min event
    _air_temperature10_min = AirTemperature10Min()

    # sends the 'DE.DWD.CDC.AirTemperature10Min' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_cdc_air_temperature10_min(_station_id = 'TODO: replace me', data = _air_temperature10_min)
    print(f"Sent 'DE.DWD.CDC.AirTemperature10Min' event: {_air_temperature10_min.to_json()}")

    # ---- DE.DWD.CDC.Precipitation10Min ----
    # TODO: Supply event data for the DE.DWD.CDC.Precipitation10Min event
    _precipitation10_min = Precipitation10Min()

    # sends the 'DE.DWD.CDC.Precipitation10Min' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_cdc_precipitation10_min(_station_id = 'TODO: replace me', data = _precipitation10_min)
    print(f"Sent 'DE.DWD.CDC.Precipitation10Min' event: {_precipitation10_min.to_json()}")

    # ---- DE.DWD.CDC.Wind10Min ----
    # TODO: Supply event data for the DE.DWD.CDC.Wind10Min event
    _wind10_min = Wind10Min()

    # sends the 'DE.DWD.CDC.Wind10Min' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_cdc_wind10_min(_station_id = 'TODO: replace me', data = _wind10_min)
    print(f"Sent 'DE.DWD.CDC.Wind10Min' event: {_wind10_min.to_json()}")

    # ---- DE.DWD.CDC.Solar10Min ----
    # TODO: Supply event data for the DE.DWD.CDC.Solar10Min event
    _solar10_min = Solar10Min()

    # sends the 'DE.DWD.CDC.Solar10Min' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_cdc_solar10_min(_station_id = 'TODO: replace me', data = _solar10_min)
    print(f"Sent 'DE.DWD.CDC.Solar10Min' event: {_solar10_min.to_json()}")

    # ---- DE.DWD.CDC.HourlyObservation ----
    # TODO: Supply event data for the DE.DWD.CDC.HourlyObservation event
    _hourly_observation = HourlyObservation()

    # sends the 'DE.DWD.CDC.HourlyObservation' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_cdc_hourly_observation(_station_id = 'TODO: replace me', data = _hourly_observation)
    print(f"Sent 'DE.DWD.CDC.HourlyObservation' event: {_hourly_observation.to_json()}")

    # ---- DE.DWD.CDC.ExtremeWind10Min ----
    # TODO: Supply event data for the DE.DWD.CDC.ExtremeWind10Min event
    _extreme_wind10_min = ExtremeWind10Min()

    # sends the 'DE.DWD.CDC.ExtremeWind10Min' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_cdc_extreme_wind10_min(_station_id = 'TODO: replace me', data = _extreme_wind10_min)
    print(f"Sent 'DE.DWD.CDC.ExtremeWind10Min' event: {_extreme_wind10_min.to_json()}")

    # ---- DE.DWD.CDC.ExtremeTemperature10Min ----
    # TODO: Supply event data for the DE.DWD.CDC.ExtremeTemperature10Min event
    _extreme_temperature10_min = ExtremeTemperature10Min()

    # sends the 'DE.DWD.CDC.ExtremeTemperature10Min' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_cdc_extreme_temperature10_min(_station_id = 'TODO: replace me', data = _extreme_temperature10_min)
    print(f"Sent 'DE.DWD.CDC.ExtremeTemperature10Min' event: {_extreme_temperature10_min.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        dedwdweather_event_producer = DEDWDWeatherEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        dedwdweather_event_producer = DEDWDWeatherEventProducer(kafka_producer, topic, 'binary')

    # ---- DE.DWD.Weather.Alert ----
    # TODO: Supply event data for the DE.DWD.Weather.Alert event
    _alert = Alert()

    # sends the 'DE.DWD.Weather.Alert' event to Kafka topic.
    await dedwdweather_event_producer.send_de_dwd_weather_alert(_identifier = 'TODO: replace me', data = _alert)
    print(f"Sent 'DE.DWD.Weather.Alert' event: {_alert.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        dedwdradar_event_producer = DEDWDRadarEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        dedwdradar_event_producer = DEDWDRadarEventProducer(kafka_producer, topic, 'binary')

    # ---- DE.DWD.Radar.RadarProductCatalog ----
    # TODO: Supply event data for the DE.DWD.Radar.RadarProductCatalog event
    _radar_product_catalog = RadarProductCatalog()

    # sends the 'DE.DWD.Radar.RadarProductCatalog' event to Kafka topic.
    await dedwdradar_event_producer.send_de_dwd_radar_radar_product_catalog(_file_path = 'TODO: replace me', data = _radar_product_catalog)
    print(f"Sent 'DE.DWD.Radar.RadarProductCatalog' event: {_radar_product_catalog.to_json()}")

    # ---- DE.DWD.Radar.RadarFileProduct ----
    # TODO: Supply event data for the DE.DWD.Radar.RadarFileProduct event
    _radar_file_product = RadarFileProduct()

    # sends the 'DE.DWD.Radar.RadarFileProduct' event to Kafka topic.
    await dedwdradar_event_producer.send_de_dwd_radar_radar_file_product(_file_path = 'TODO: replace me', data = _radar_file_product)
    print(f"Sent 'DE.DWD.Radar.RadarFileProduct' event: {_radar_file_product.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        dedwdforecast_event_producer = DEDWDForecastEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        dedwdforecast_event_producer = DEDWDForecastEventProducer(kafka_producer, topic, 'binary')

    # ---- DE.DWD.Forecast.ForecastModelCatalog ----
    # TODO: Supply event data for the DE.DWD.Forecast.ForecastModelCatalog event
    _forecast_model_catalog = ForecastModelCatalog()

    # sends the 'DE.DWD.Forecast.ForecastModelCatalog' event to Kafka topic.
    await dedwdforecast_event_producer.send_de_dwd_forecast_forecast_model_catalog(_file_path = 'TODO: replace me', data = _forecast_model_catalog)
    print(f"Sent 'DE.DWD.Forecast.ForecastModelCatalog' event: {_forecast_model_catalog.to_json()}")

    # ---- DE.DWD.Forecast.IconD2ForecastFile ----
    # TODO: Supply event data for the DE.DWD.Forecast.IconD2ForecastFile event
    _icon_d2_forecast_file = IconD2ForecastFile()

    # sends the 'DE.DWD.Forecast.IconD2ForecastFile' event to Kafka topic.
    await dedwdforecast_event_producer.send_de_dwd_forecast_icon_d2_forecast_file(_file_path = 'TODO: replace me', data = _icon_d2_forecast_file)
    print(f"Sent 'DE.DWD.Forecast.IconD2ForecastFile' event: {_icon_d2_forecast_file.to_json()}")

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