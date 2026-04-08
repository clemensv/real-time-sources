
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

from noaa_goes_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAASWPCAlertsEventProducer
from noaa_goes_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAASWPCObservationsEventProducer
from noaa_goes_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAASWPCGOESParticleFluxEventProducer
from noaa_goes_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAASWPCGOESMagnetometerEventProducer
from noaa_goes_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAASWPCSolarFlaresEventProducer

# imports for the data classes for each event

from noaa_goes_producer_data.spaceweatheralert import SpaceWeatherAlert
from noaa_goes_producer_data.planetarykindex import PlanetaryKIndex
from noaa_goes_producer_data.solarwindsummary import SolarWindSummary
from noaa_goes_producer_data.solarwindplasma import SolarWindPlasma
from noaa_goes_producer_data.solarwindmagfield import SolarWindMagField
from noaa_goes_producer_data.goesxrayflux import GoesXrayFlux
from noaa_goes_producer_data.goesprotonflux import GoesProtonFlux
from noaa_goes_producer_data.goeselectronflux import GoesElectronFlux
from noaa_goes_producer_data.goesmagnetometer import GoesMagnetometer
from noaa_goes_producer_data.xrayflare import XrayFlare

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
        microsoft_open_data_usnoaaswpcalerts_event_producer = MicrosoftOpenDataUSNOAASWPCAlertsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaaswpcalerts_event_producer = MicrosoftOpenDataUSNOAASWPCAlertsEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert event
    _space_weather_alert = SpaceWeatherAlert()

    # sends the 'Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert' event to Kafka topic.
    await microsoft_open_data_usnoaaswpcalerts_event_producer.send_microsoft_open_data_us_noaa_swpc_space_weather_alert(_product_id = 'TODO: replace me', data = _space_weather_alert)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert' event: {_space_weather_alert.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        microsoft_open_data_usnoaaswpcobservations_event_producer = MicrosoftOpenDataUSNOAASWPCObservationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaaswpcobservations_event_producer = MicrosoftOpenDataUSNOAASWPCObservationsEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex event
    _planetary_kindex = PlanetaryKIndex()

    # sends the 'Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex' event to Kafka topic.
    await microsoft_open_data_usnoaaswpcobservations_event_producer.send_microsoft_open_data_us_noaa_swpc_planetary_kindex(_observation_time = 'TODO: replace me', data = _planetary_kindex)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex' event: {_planetary_kindex.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary event
    _solar_wind_summary = SolarWindSummary()

    # sends the 'Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary' event to Kafka topic.
    await microsoft_open_data_usnoaaswpcobservations_event_producer.send_microsoft_open_data_us_noaa_swpc_solar_wind_summary(_observation_time = 'TODO: replace me', data = _solar_wind_summary)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary' event: {_solar_wind_summary.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.SWPC.SolarWindPlasma ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.SWPC.SolarWindPlasma event
    _solar_wind_plasma = SolarWindPlasma()

    # sends the 'Microsoft.OpenData.US.NOAA.SWPC.SolarWindPlasma' event to Kafka topic.
    await microsoft_open_data_usnoaaswpcobservations_event_producer.send_microsoft_open_data_us_noaa_swpc_solar_wind_plasma(_observation_time = 'TODO: replace me', data = _solar_wind_plasma)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.SWPC.SolarWindPlasma' event: {_solar_wind_plasma.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.SWPC.SolarWindMagField ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.SWPC.SolarWindMagField event
    _solar_wind_mag_field = SolarWindMagField()

    # sends the 'Microsoft.OpenData.US.NOAA.SWPC.SolarWindMagField' event to Kafka topic.
    await microsoft_open_data_usnoaaswpcobservations_event_producer.send_microsoft_open_data_us_noaa_swpc_solar_wind_mag_field(_observation_time = 'TODO: replace me', data = _solar_wind_mag_field)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.SWPC.SolarWindMagField' event: {_solar_wind_mag_field.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        microsoft_open_data_usnoaaswpcgoesparticle_flux_event_producer = MicrosoftOpenDataUSNOAASWPCGOESParticleFluxEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaaswpcgoesparticle_flux_event_producer = MicrosoftOpenDataUSNOAASWPCGOESParticleFluxEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux event
    _goes_xray_flux = GoesXrayFlux()

    # sends the 'Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux' event to Kafka topic.
    await microsoft_open_data_usnoaaswpcgoesparticle_flux_event_producer.send_microsoft_open_data_us_noaa_swpc_goes_xray_flux(_satellite = 'TODO: replace me', _energy = 'TODO: replace me', _time_tag = 'TODO: replace me', data = _goes_xray_flux)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux' event: {_goes_xray_flux.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux event
    _goes_proton_flux = GoesProtonFlux()

    # sends the 'Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux' event to Kafka topic.
    await microsoft_open_data_usnoaaswpcgoesparticle_flux_event_producer.send_microsoft_open_data_us_noaa_swpc_goes_proton_flux(_satellite = 'TODO: replace me', _energy = 'TODO: replace me', _time_tag = 'TODO: replace me', data = _goes_proton_flux)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux' event: {_goes_proton_flux.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux event
    _goes_electron_flux = GoesElectronFlux()

    # sends the 'Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux' event to Kafka topic.
    await microsoft_open_data_usnoaaswpcgoesparticle_flux_event_producer.send_microsoft_open_data_us_noaa_swpc_goes_electron_flux(_satellite = 'TODO: replace me', _energy = 'TODO: replace me', _time_tag = 'TODO: replace me', data = _goes_electron_flux)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux' event: {_goes_electron_flux.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        microsoft_open_data_usnoaaswpcgoesmagnetometer_event_producer = MicrosoftOpenDataUSNOAASWPCGOESMagnetometerEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaaswpcgoesmagnetometer_event_producer = MicrosoftOpenDataUSNOAASWPCGOESMagnetometerEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer event
    _goes_magnetometer = GoesMagnetometer()

    # sends the 'Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer' event to Kafka topic.
    await microsoft_open_data_usnoaaswpcgoesmagnetometer_event_producer.send_microsoft_open_data_us_noaa_swpc_goes_magnetometer(_satellite = 'TODO: replace me', _time_tag = 'TODO: replace me', data = _goes_magnetometer)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer' event: {_goes_magnetometer.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        microsoft_open_data_usnoaaswpcsolar_flares_event_producer = MicrosoftOpenDataUSNOAASWPCSolarFlaresEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaaswpcsolar_flares_event_producer = MicrosoftOpenDataUSNOAASWPCSolarFlaresEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.SWPC.XrayFlare ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.SWPC.XrayFlare event
    _xray_flare = XrayFlare()

    # sends the 'Microsoft.OpenData.US.NOAA.SWPC.XrayFlare' event to Kafka topic.
    await microsoft_open_data_usnoaaswpcsolar_flares_event_producer.send_microsoft_open_data_us_noaa_swpc_xray_flare(_satellite = 'TODO: replace me', _begin_time = 'TODO: replace me', data = _xray_flare)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.SWPC.XrayFlare' event: {_xray_flare.to_json()}")

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