
"""
This is sample code to use the MQTT clients contained in this project.

The sample demonstrates both publishing and subscribing to MQTT messages with
the
producer and dispatcher functionality.

There is a handler for each defined message type. The handler is an async
function that takes the following parameters:
- mqtt_message: The paho.mqtt.client.MQTTMessage object (message context).
- cloud_event: The CloudEvent data (if using CloudEvents).
- message_data: The deserialized message data.The main function creates clients
for each message group that can both produce and consume messages.
It starts dispatchers to handle incoming messages and then publishes sample
messages.

The script either reads the configuration from the command line or uses the
environment variables. The following environment variables are recognized:

- MQTT_BROKER_HOST: The MQTT broker hostname.
- MQTT_BROKER_PORT: The MQTT broker port (default: 1883).
- MQTT_TOPIC: The MQTT topic to publish/subscribe to.
- MQTT_USERNAME: The MQTT username (optional).
- MQTT_PASSWORD: The MQTT password (optional).

Alternatively, you can pass the configuration as command-line arguments.

python sample.py --broker-host <broker_host> --broker-port <broker_port> --topic
<topic>

The main function waits for a signal (Press Ctrl+C) to stop.
"""

import argparse
import asyncio
import os
import signal
from usgs_iv_mqtt_producer_data import *
from usgs_iv_mqtt_producer_mqtt_client.client import USGSSitesMqttProducer, USGSSitesMqttDispatcher

async def handle_usgs_sites_mqtt_site(mqtt_msg,cloud_event, usgs_sites_mqtt_site_data):
    """ Handles the USGS.Sites.mqtt.Site message """
    print(f"Received USGS.Sites.mqtt.Site on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_sites_mqtt_site_data}")
from usgs_iv_mqtt_producer_mqtt_client.client import USGSSiteTimeseriesMqttProducer, USGSSiteTimeseriesMqttDispatcher

async def handle_usgs_site_timeseries_mqtt_site_timeseries(mqtt_msg,cloud_event, usgs_site_timeseries_mqtt_site_timeseries_data):
    """ Handles the USGS.SiteTimeseries.mqtt.SiteTimeseries message """
    print(f"Received USGS.SiteTimeseries.mqtt.SiteTimeseries on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_site_timeseries_mqtt_site_timeseries_data}")
from usgs_iv_mqtt_producer_mqtt_client.client import USGSInstantaneousValuesMqttProducer, USGSInstantaneousValuesMqttDispatcher

async def handle_usgs_instantaneous_values_mqtt_other_parameter(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_other_parameter_data):
    """ Handles the USGS.InstantaneousValues.mqtt.OtherParameter message """
    print(f"Received USGS.InstantaneousValues.mqtt.OtherParameter on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_other_parameter_data}")

async def handle_usgs_instantaneous_values_mqtt_precipitation(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_precipitation_data):
    """ Handles the USGS.InstantaneousValues.mqtt.Precipitation message """
    print(f"Received USGS.InstantaneousValues.mqtt.Precipitation on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_precipitation_data}")

async def handle_usgs_instantaneous_values_mqtt_streamflow(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_streamflow_data):
    """ Handles the USGS.InstantaneousValues.mqtt.Streamflow message """
    print(f"Received USGS.InstantaneousValues.mqtt.Streamflow on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_streamflow_data}")

async def handle_usgs_instantaneous_values_mqtt_gage_height(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_gage_height_data):
    """ Handles the USGS.InstantaneousValues.mqtt.GageHeight message """
    print(f"Received USGS.InstantaneousValues.mqtt.GageHeight on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_gage_height_data}")

async def handle_usgs_instantaneous_values_mqtt_water_temperature(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_water_temperature_data):
    """ Handles the USGS.InstantaneousValues.mqtt.WaterTemperature message """
    print(f"Received USGS.InstantaneousValues.mqtt.WaterTemperature on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_water_temperature_data}")

async def handle_usgs_instantaneous_values_mqtt_dissolved_oxygen(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_dissolved_oxygen_data):
    """ Handles the USGS.InstantaneousValues.mqtt.DissolvedOxygen message """
    print(f"Received USGS.InstantaneousValues.mqtt.DissolvedOxygen on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_dissolved_oxygen_data}")

async def handle_usgs_instantaneous_values_mqtt_p_h(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_p_h_data):
    """ Handles the USGS.InstantaneousValues.mqtt.pH message """
    print(f"Received USGS.InstantaneousValues.mqtt.pH on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_p_h_data}")

async def handle_usgs_instantaneous_values_mqtt_specific_conductance(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_specific_conductance_data):
    """ Handles the USGS.InstantaneousValues.mqtt.SpecificConductance message """
    print(f"Received USGS.InstantaneousValues.mqtt.SpecificConductance on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_specific_conductance_data}")

async def handle_usgs_instantaneous_values_mqtt_turbidity(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_turbidity_data):
    """ Handles the USGS.InstantaneousValues.mqtt.Turbidity message """
    print(f"Received USGS.InstantaneousValues.mqtt.Turbidity on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_turbidity_data}")

async def handle_usgs_instantaneous_values_mqtt_air_temperature(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_air_temperature_data):
    """ Handles the USGS.InstantaneousValues.mqtt.AirTemperature message """
    print(f"Received USGS.InstantaneousValues.mqtt.AirTemperature on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_air_temperature_data}")

async def handle_usgs_instantaneous_values_mqtt_wind_speed(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_wind_speed_data):
    """ Handles the USGS.InstantaneousValues.mqtt.WindSpeed message """
    print(f"Received USGS.InstantaneousValues.mqtt.WindSpeed on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_wind_speed_data}")

async def handle_usgs_instantaneous_values_mqtt_wind_direction(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_wind_direction_data):
    """ Handles the USGS.InstantaneousValues.mqtt.WindDirection message """
    print(f"Received USGS.InstantaneousValues.mqtt.WindDirection on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_wind_direction_data}")

async def handle_usgs_instantaneous_values_mqtt_relative_humidity(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_relative_humidity_data):
    """ Handles the USGS.InstantaneousValues.mqtt.RelativeHumidity message """
    print(f"Received USGS.InstantaneousValues.mqtt.RelativeHumidity on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_relative_humidity_data}")

async def handle_usgs_instantaneous_values_mqtt_barometric_pressure(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_barometric_pressure_data):
    """ Handles the USGS.InstantaneousValues.mqtt.BarometricPressure message """
    print(f"Received USGS.InstantaneousValues.mqtt.BarometricPressure on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_barometric_pressure_data}")

async def handle_usgs_instantaneous_values_mqtt_turbidity_fnu(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_turbidity_fnu_data):
    """ Handles the USGS.InstantaneousValues.mqtt.TurbidityFNU message """
    print(f"Received USGS.InstantaneousValues.mqtt.TurbidityFNU on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_turbidity_fnu_data}")

async def handle_usgs_instantaneous_values_mqtt_f_dom(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_f_dom_data):
    """ Handles the USGS.InstantaneousValues.mqtt.fDOM message """
    print(f"Received USGS.InstantaneousValues.mqtt.fDOM on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_f_dom_data}")

async def handle_usgs_instantaneous_values_mqtt_reservoir_storage(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_reservoir_storage_data):
    """ Handles the USGS.InstantaneousValues.mqtt.ReservoirStorage message """
    print(f"Received USGS.InstantaneousValues.mqtt.ReservoirStorage on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_reservoir_storage_data}")

async def handle_usgs_instantaneous_values_mqtt_lake_elevation_ngvd29(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_lake_elevation_ngvd29_data):
    """ Handles the USGS.InstantaneousValues.mqtt.LakeElevationNGVD29 message """
    print(f"Received USGS.InstantaneousValues.mqtt.LakeElevationNGVD29 on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_lake_elevation_ngvd29_data}")

async def handle_usgs_instantaneous_values_mqtt_water_depth(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_water_depth_data):
    """ Handles the USGS.InstantaneousValues.mqtt.WaterDepth message """
    print(f"Received USGS.InstantaneousValues.mqtt.WaterDepth on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_water_depth_data}")

async def handle_usgs_instantaneous_values_mqtt_equipment_status(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_equipment_status_data):
    """ Handles the USGS.InstantaneousValues.mqtt.EquipmentStatus message """
    print(f"Received USGS.InstantaneousValues.mqtt.EquipmentStatus on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_equipment_status_data}")

async def handle_usgs_instantaneous_values_mqtt_tidally_filtered_discharge(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_tidally_filtered_discharge_data):
    """ Handles the USGS.InstantaneousValues.mqtt.TidallyFilteredDischarge message """
    print(f"Received USGS.InstantaneousValues.mqtt.TidallyFilteredDischarge on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_tidally_filtered_discharge_data}")

async def handle_usgs_instantaneous_values_mqtt_water_velocity(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_water_velocity_data):
    """ Handles the USGS.InstantaneousValues.mqtt.WaterVelocity message """
    print(f"Received USGS.InstantaneousValues.mqtt.WaterVelocity on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_water_velocity_data}")

async def handle_usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29_data):
    """ Handles the USGS.InstantaneousValues.mqtt.EstuaryElevationNGVD29 message """
    print(f"Received USGS.InstantaneousValues.mqtt.EstuaryElevationNGVD29 on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29_data}")

async def handle_usgs_instantaneous_values_mqtt_lake_elevation_navd88(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_lake_elevation_navd88_data):
    """ Handles the USGS.InstantaneousValues.mqtt.LakeElevationNAVD88 message """
    print(f"Received USGS.InstantaneousValues.mqtt.LakeElevationNAVD88 on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_lake_elevation_navd88_data}")

async def handle_usgs_instantaneous_values_mqtt_salinity(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_salinity_data):
    """ Handles the USGS.InstantaneousValues.mqtt.Salinity message """
    print(f"Received USGS.InstantaneousValues.mqtt.Salinity on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_salinity_data}")

async def handle_usgs_instantaneous_values_mqtt_gate_opening(mqtt_msg,cloud_event, usgs_instantaneous_values_mqtt_gate_opening_data):
    """ Handles the USGS.InstantaneousValues.mqtt.GateOpening message """
    print(f"Received USGS.InstantaneousValues.mqtt.GateOpening on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {usgs_instantaneous_values_mqtt_gate_opening_data}")

async def main(broker_host, broker_port, topic, username=None, password=None):
    """ Main function for MQTT client """
    print(f"Connecting to {broker_host}:{broker_port}...")
    print(f"Topic: {topic}")
    print("Press Ctrl+C to stop\n")
    
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGTERM, lambda: stop_event.set())
    loop.add_signal_handler(signal.SIGINT, lambda: stop_event.set())
    
    await stop_event.wait()
    print("\nStopping...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MQTT Client")
    parser.add_argument('--broker-host', default=os.getenv('MQTT_BROKER_HOST', 'localhost'), help='MQTT broker hostname')
    parser.add_argument('--broker-port', type=int, default=int(os.getenv('MQTT_BROKER_PORT', '1883')), help='MQTT broker port')
    parser.add_argument('--topic', default=os.getenv('MQTT_TOPIC', 'testtopic'), help='MQTT topic')
    parser.add_argument('--username', default=os.getenv('MQTT_USERNAME'), help='MQTT username (optional)')
    parser.add_argument('--password', default=os.getenv('MQTT_PASSWORD'), help='MQTT password (optional)')

    args = parser.parse_args()

    asyncio.run(main(
        args.broker_host,
        args.broker_port,
        args.topic,
        args.username,
        args.password
    ))