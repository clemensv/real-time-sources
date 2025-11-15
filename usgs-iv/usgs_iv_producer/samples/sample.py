
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

from usgs-iv-producer_kafka_producer.producer import USGSSitesEventProducer
from usgs-iv-producer_kafka_producer.producer import USGSInstantaneousValuesEventProducer

# imports for the data classes for each event

from usgs-iv-producer_data.usgs.sites.site import Site
from usgs-iv-producer_data.usgs.sites.sitetimeseries import SiteTimeseries
from usgs-iv-producer_data.usgs.instantaneousvalues.otherparameter import OtherParameter
from usgs-iv-producer_data.usgs.instantaneousvalues.precipitation import Precipitation
from usgs-iv-producer_data.usgs.instantaneousvalues.streamflow import Streamflow
from usgs-iv-producer_data.usgs.instantaneousvalues.gageheight import GageHeight
from usgs-iv-producer_data.usgs.instantaneousvalues.watertemperature import WaterTemperature
from usgs-iv-producer_data.usgs.instantaneousvalues.dissolvedoxygen import DissolvedOxygen
from usgs-iv-producer_data.usgs.instantaneousvalues.ph import PH
from usgs-iv-producer_data.usgs.instantaneousvalues.specificconductance import SpecificConductance
from usgs-iv-producer_data.usgs.instantaneousvalues.turbidity import Turbidity
from usgs-iv-producer_data.usgs.instantaneousvalues.airtemperature import AirTemperature
from usgs-iv-producer_data.usgs.instantaneousvalues.windspeed import WindSpeed
from usgs-iv-producer_data.usgs.instantaneousvalues.winddirection import WindDirection
from usgs-iv-producer_data.usgs.instantaneousvalues.relativehumidity import RelativeHumidity
from usgs-iv-producer_data.usgs.instantaneousvalues.barometricpressure import BarometricPressure
from usgs-iv-producer_data.usgs.instantaneousvalues.turbidityfnu import TurbidityFNU
from usgs-iv-producer_data.usgs.instantaneousvalues.fdom import FDOM
from usgs-iv-producer_data.usgs.instantaneousvalues.reservoirstorage import ReservoirStorage
from usgs-iv-producer_data.usgs.instantaneousvalues.lakeelevationngvd29 import LakeElevationNGVD29
from usgs-iv-producer_data.usgs.instantaneousvalues.waterdepth import WaterDepth
from usgs-iv-producer_data.usgs.instantaneousvalues.equipmentstatus import EquipmentStatus
from usgs-iv-producer_data.usgs.instantaneousvalues.tidallyfiltereddischarge import TidallyFilteredDischarge
from usgs-iv-producer_data.usgs.instantaneousvalues.watervelocity import WaterVelocity
from usgs-iv-producer_data.usgs.instantaneousvalues.estuaryelevationngvd29 import EstuaryElevationNGVD29
from usgs-iv-producer_data.usgs.instantaneousvalues.lakeelevationnavd88 import LakeElevationNAVD88
from usgs-iv-producer_data.usgs.instantaneousvalues.salinity import Salinity
from usgs-iv-producer_data.usgs.instantaneousvalues.gateopening import GateOpening

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
    await usgssites_event_producer.send_usgs_sites_site(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', data = _site)
    print(f"Sent 'USGS.Sites.Site' event: {_site.to_json()}")

    # ---- USGS.Sites.SiteTimeseries ----
    # TODO: Supply event data for the USGS.Sites.SiteTimeseries event
    _site_timeseries = SiteTimeseries()

    # sends the 'USGS.Sites.SiteTimeseries' event to Kafka topic.
    await usgssites_event_producer.send_usgs_sites_site_timeseries(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', data = _site_timeseries)
    print(f"Sent 'USGS.Sites.SiteTimeseries' event: {_site_timeseries.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        usgsinstantaneous_values_event_producer = USGSInstantaneousValuesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        usgsinstantaneous_values_event_producer = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')

    # ---- USGS.InstantaneousValues.OtherParameter ----
    # TODO: Supply event data for the USGS.InstantaneousValues.OtherParameter event
    _other_parameter = OtherParameter()

    # sends the 'USGS.InstantaneousValues.OtherParameter' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_other_parameter(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _other_parameter)
    print(f"Sent 'USGS.InstantaneousValues.OtherParameter' event: {_other_parameter.to_json()}")

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

    # ---- USGS.InstantaneousValues.AirTemperature ----
    # TODO: Supply event data for the USGS.InstantaneousValues.AirTemperature event
    _air_temperature = AirTemperature()

    # sends the 'USGS.InstantaneousValues.AirTemperature' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_air_temperature(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _air_temperature)
    print(f"Sent 'USGS.InstantaneousValues.AirTemperature' event: {_air_temperature.to_json()}")

    # ---- USGS.InstantaneousValues.WindSpeed ----
    # TODO: Supply event data for the USGS.InstantaneousValues.WindSpeed event
    _wind_speed = WindSpeed()

    # sends the 'USGS.InstantaneousValues.WindSpeed' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_wind_speed(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _wind_speed)
    print(f"Sent 'USGS.InstantaneousValues.WindSpeed' event: {_wind_speed.to_json()}")

    # ---- USGS.InstantaneousValues.WindDirection ----
    # TODO: Supply event data for the USGS.InstantaneousValues.WindDirection event
    _wind_direction = WindDirection()

    # sends the 'USGS.InstantaneousValues.WindDirection' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_wind_direction(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _wind_direction)
    print(f"Sent 'USGS.InstantaneousValues.WindDirection' event: {_wind_direction.to_json()}")

    # ---- USGS.InstantaneousValues.RelativeHumidity ----
    # TODO: Supply event data for the USGS.InstantaneousValues.RelativeHumidity event
    _relative_humidity = RelativeHumidity()

    # sends the 'USGS.InstantaneousValues.RelativeHumidity' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_relative_humidity(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _relative_humidity)
    print(f"Sent 'USGS.InstantaneousValues.RelativeHumidity' event: {_relative_humidity.to_json()}")

    # ---- USGS.InstantaneousValues.BarometricPressure ----
    # TODO: Supply event data for the USGS.InstantaneousValues.BarometricPressure event
    _barometric_pressure = BarometricPressure()

    # sends the 'USGS.InstantaneousValues.BarometricPressure' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_barometric_pressure(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _barometric_pressure)
    print(f"Sent 'USGS.InstantaneousValues.BarometricPressure' event: {_barometric_pressure.to_json()}")

    # ---- USGS.InstantaneousValues.TurbidityFNU ----
    # TODO: Supply event data for the USGS.InstantaneousValues.TurbidityFNU event
    _turbidity_fnu = TurbidityFNU()

    # sends the 'USGS.InstantaneousValues.TurbidityFNU' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_turbidity_fnu(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _turbidity_fnu)
    print(f"Sent 'USGS.InstantaneousValues.TurbidityFNU' event: {_turbidity_fnu.to_json()}")

    # ---- USGS.InstantaneousValues.fDOM ----
    # TODO: Supply event data for the USGS.InstantaneousValues.fDOM event
    _fdom = FDOM()

    # sends the 'USGS.InstantaneousValues.fDOM' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_f_dom(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _fdom)
    print(f"Sent 'USGS.InstantaneousValues.fDOM' event: {_fdom.to_json()}")

    # ---- USGS.InstantaneousValues.ReservoirStorage ----
    # TODO: Supply event data for the USGS.InstantaneousValues.ReservoirStorage event
    _reservoir_storage = ReservoirStorage()

    # sends the 'USGS.InstantaneousValues.ReservoirStorage' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_reservoir_storage(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _reservoir_storage)
    print(f"Sent 'USGS.InstantaneousValues.ReservoirStorage' event: {_reservoir_storage.to_json()}")

    # ---- USGS.InstantaneousValues.LakeElevationNGVD29 ----
    # TODO: Supply event data for the USGS.InstantaneousValues.LakeElevationNGVD29 event
    _lake_elevation_ngvd29 = LakeElevationNGVD29()

    # sends the 'USGS.InstantaneousValues.LakeElevationNGVD29' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_lake_elevation_ngvd29(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _lake_elevation_ngvd29)
    print(f"Sent 'USGS.InstantaneousValues.LakeElevationNGVD29' event: {_lake_elevation_ngvd29.to_json()}")

    # ---- USGS.InstantaneousValues.WaterDepth ----
    # TODO: Supply event data for the USGS.InstantaneousValues.WaterDepth event
    _water_depth = WaterDepth()

    # sends the 'USGS.InstantaneousValues.WaterDepth' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_water_depth(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _water_depth)
    print(f"Sent 'USGS.InstantaneousValues.WaterDepth' event: {_water_depth.to_json()}")

    # ---- USGS.InstantaneousValues.EquipmentStatus ----
    # TODO: Supply event data for the USGS.InstantaneousValues.EquipmentStatus event
    _equipment_status = EquipmentStatus()

    # sends the 'USGS.InstantaneousValues.EquipmentStatus' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_equipment_status(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _equipment_status)
    print(f"Sent 'USGS.InstantaneousValues.EquipmentStatus' event: {_equipment_status.to_json()}")

    # ---- USGS.InstantaneousValues.TidallyFilteredDischarge ----
    # TODO: Supply event data for the USGS.InstantaneousValues.TidallyFilteredDischarge event
    _tidally_filtered_discharge = TidallyFilteredDischarge()

    # sends the 'USGS.InstantaneousValues.TidallyFilteredDischarge' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_tidally_filtered_discharge(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _tidally_filtered_discharge)
    print(f"Sent 'USGS.InstantaneousValues.TidallyFilteredDischarge' event: {_tidally_filtered_discharge.to_json()}")

    # ---- USGS.InstantaneousValues.WaterVelocity ----
    # TODO: Supply event data for the USGS.InstantaneousValues.WaterVelocity event
    _water_velocity = WaterVelocity()

    # sends the 'USGS.InstantaneousValues.WaterVelocity' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_water_velocity(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _water_velocity)
    print(f"Sent 'USGS.InstantaneousValues.WaterVelocity' event: {_water_velocity.to_json()}")

    # ---- USGS.InstantaneousValues.EstuaryElevationNGVD29 ----
    # TODO: Supply event data for the USGS.InstantaneousValues.EstuaryElevationNGVD29 event
    _estuary_elevation_ngvd29 = EstuaryElevationNGVD29()

    # sends the 'USGS.InstantaneousValues.EstuaryElevationNGVD29' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_estuary_elevation_ngvd29(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _estuary_elevation_ngvd29)
    print(f"Sent 'USGS.InstantaneousValues.EstuaryElevationNGVD29' event: {_estuary_elevation_ngvd29.to_json()}")

    # ---- USGS.InstantaneousValues.LakeElevationNAVD88 ----
    # TODO: Supply event data for the USGS.InstantaneousValues.LakeElevationNAVD88 event
    _lake_elevation_navd88 = LakeElevationNAVD88()

    # sends the 'USGS.InstantaneousValues.LakeElevationNAVD88' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_lake_elevation_navd88(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _lake_elevation_navd88)
    print(f"Sent 'USGS.InstantaneousValues.LakeElevationNAVD88' event: {_lake_elevation_navd88.to_json()}")

    # ---- USGS.InstantaneousValues.Salinity ----
    # TODO: Supply event data for the USGS.InstantaneousValues.Salinity event
    _salinity = Salinity()

    # sends the 'USGS.InstantaneousValues.Salinity' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_salinity(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _salinity)
    print(f"Sent 'USGS.InstantaneousValues.Salinity' event: {_salinity.to_json()}")

    # ---- USGS.InstantaneousValues.GateOpening ----
    # TODO: Supply event data for the USGS.InstantaneousValues.GateOpening event
    _gate_opening = GateOpening()

    # sends the 'USGS.InstantaneousValues.GateOpening' event to Kafka topic.
    await usgsinstantaneous_values_event_producer.send_usgs_instantaneous_values_gate_opening(_source_uri = 'TODO: replace me', _agency_cd = 'TODO: replace me', _site_no = 'TODO: replace me', _parameter_cd = 'TODO: replace me', _timeseries_cd = 'TODO: replace me', _datetime = 'TODO: replace me', data = _gate_opening)
    print(f"Sent 'USGS.InstantaneousValues.GateOpening' event: {_gate_opening.to_json()}")

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