from __future__ import annotations
import argparse, asyncio, os
from datetime import datetime, timezone
from urllib.parse import urlparse
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from singapore_nea_mqtt_producer_data import Station, WeatherObservation, Region, PSIReading, PM25Reading
from singapore_nea_mqtt_producer_mqtt_client.client import SGGovNEAWeatherMqttMqttClient, SGGovNEAAirQualityMqttMqttClient

def _parse(url):
    p=urlparse(url if '://' in url else 'mqtt://'+url); return p.hostname or 'localhost', p.port or 1883
async def _mock(w, aq):
    now=datetime(2026,4,7,10,0,tzinfo=timezone.utc)
    st=Station(station_id='S109', device_id='S109', name='Ang Mo Kio Avenue 5', latitude=1.3764, longitude=103.8492, data_types='air_temperature,rainfall')
    obs=WeatherObservation(station_id='S109', station_name='Ang Mo Kio Avenue 5', observation_time=now, air_temperature=30.5, rainfall=0.0, relative_humidity=75.0, wind_speed=2.1, wind_direction=180.0)
    reg=Region(region='central', latitude=1.357, longitude=103.82)
    psi=PSIReading(region='central', timestamp=now, update_timestamp=now, psi_twenty_four_hourly=52, o3_sub_index=10, pm10_sub_index=20, pm10_twenty_four_hourly=25, pm25_sub_index=30, pm25_twenty_four_hourly=12, co_sub_index=5, co_eight_hour_max=1, so2_sub_index=2, so2_twenty_four_hourly=3, no2_one_hour_max=8, o3_eight_hour_max=10)
    pm=PM25Reading(region='central', timestamp=now, update_timestamp=now, pm25_one_hourly=11)
    await w.publish_sg_gov_nea_weather_station_mqtt(station_id='S109', region='central', event='info', data=st)
    await w.publish_sg_gov_nea_weather_weather_observation_mqtt(station_id='S109', region='central', event='weather', data=obs)
    await aq.publish_sg_gov_nea_air_quality_region_mqtt(region='central', station_id='central', event='info', data=reg)
    await aq.publish_sg_gov_nea_air_quality_psireading_mqtt(region='central', station_id='central', event='psi', data=psi)
    await aq.publish_sg_gov_nea_air_quality_pm25_reading_mqtt(region='central', station_id='central', event='pm25', data=pm)

def main(argv=None):
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='command'); f=sub.add_parser('feed'); f.add_argument('--mqtt-broker-url', default=os.getenv('MQTT_BROKER_URL','mqtt://localhost:1883'))
    a=ap.parse_args(argv)
    if a.command!='feed': ap.print_help(); return
    async def run():
        host,port=_parse(a.mqtt_broker_url); p=mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5); w=SGGovNEAWeatherMqttMqttClient(client=p, content_mode='binary', loop=asyncio.get_running_loop()); aq=SGGovNEAAirQualityMqttMqttClient(client=p, content_mode='binary', loop=asyncio.get_running_loop()); await w.connect(host,port); await _mock(w,aq); await asyncio.sleep(1); await w.disconnect()
    asyncio.run(run())
if __name__=='__main__': main()
