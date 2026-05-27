from __future__ import annotations
import argparse, asyncio, os
from urllib.parse import urlparse
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from noaa_goes_mqtt_producer_data import GoesXrayFlux, GoesProtonFlux, GoesElectronFlux, GoesMagnetometer, SpaceWeatherAlert, XrayFlare
from noaa_goes_mqtt_producer_mqtt_client.client import MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient

def _parse(url):
    p=urlparse(url if '://' in url else 'mqtt://'+url); return p.hostname or 'localhost', p.port or 1883
async def _mock(c):
    ts='2026-04-07T10:00:00Z'; sat='goes-18'
    await c.publish_microsoft_open_data_us_noaa_swpc_goes_xray_flux_mqtt(satellite=sat, energy='0.1-0.8nm', time_tag=ts, event='xrs', data=GoesXrayFlux(time_tag=ts, satellite=18, flux=1.2e-6, energy='0.1-0.8nm'))
    await c.publish_microsoft_open_data_us_noaa_swpc_goes_proton_flux_mqtt(satellite=sat, energy='>=10MeV', time_tag=ts, event='sgps', data=GoesProtonFlux(time_tag=ts, satellite=18, flux=3.0, energy='>=10MeV'))
    await c.publish_microsoft_open_data_us_noaa_swpc_goes_electron_flux_mqtt(satellite=sat, energy='>=2MeV', time_tag=ts, event='exis', data=GoesElectronFlux(time_tag=ts, satellite=18, flux=900.0, energy='>=2MeV'))
    await c.publish_microsoft_open_data_us_noaa_swpc_goes_magnetometer_mqtt(satellite=sat, time_tag=ts, event='magnetometer', data=GoesMagnetometer(time_tag=ts, satellite=18, he=1.0, hp=2.0, hn=3.0, total=3.7, arcjet_flag=False))
    await c.publish_microsoft_open_data_us_noaa_swpc_space_weather_alert_mqtt(product_id='ALTXMF-20260407', data=SpaceWeatherAlert(product_id='ALTXMF-20260407', issue_datetime='2026 Apr 07 1000 UTC', message='Synthetic SWPC alert.'))
    await c.publish_microsoft_open_data_us_noaa_swpc_xray_flare_mqtt(satellite=sat, begin_time='2026-04-07T09:58:00Z', flare_class='M1', data=XrayFlare(time_tag=ts, begin_time='2026-04-07T09:58:00Z', begin_class='C9.0', max_time=ts, max_class='M1.0', max_xrlong=1e-5, max_ratio=0.2, max_ratio_time=ts, current_int_xrlong=1e-3, end_time='2026-04-07T10:10:00Z', end_class='C2.0', satellite=18))

def main(argv=None):
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='command'); f=sub.add_parser('feed'); f.add_argument('--mqtt-broker-url', default=os.getenv('MQTT_BROKER_URL','mqtt://localhost:1883'))
    a=ap.parse_args(argv)
    if a.command!='feed': ap.print_help(); return
    async def run():
        host,port=_parse(a.mqtt_broker_url); p=mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5); c=MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient(client=p, content_mode='binary', loop=asyncio.get_running_loop()); await c.connect(host,port); await _mock(c); await asyncio.sleep(1); await c.disconnect()
    asyncio.run(run())
if __name__=='__main__': main()
