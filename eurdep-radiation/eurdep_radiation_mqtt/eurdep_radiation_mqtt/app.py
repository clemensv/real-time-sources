
"""MQTT feeder for EURDEP radiation dose-rate events."""
from __future__ import annotations
import argparse, asyncio, logging, os
from typing import Optional
from urllib.parse import urlparse
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from eurdep_radiation.eurdep_radiation import EurdepAPI, FEED_URL
from eurdep_radiation_mqtt_producer_data.eu.jrc.eurdep.station import Station
from eurdep_radiation_mqtt_producer_data.eu.jrc.eurdep.doseratereading import DoseRateReading
from eurdep_radiation_mqtt_producer_mqtt_client.client import EuJrcEurdepMqttMqttClient
logger=logging.getLogger(__name__)

def _parse_broker_url(url: str):
    p=urlparse(url if '://' in url else f'mqtt://{url}'); tls=(p.scheme or 'mqtt').lower() in ('mqtts','ssl','tls')
    return p.hostname or 'localhost', p.port or (8883 if tls else 1883), tls

def _sample():
    station=Station(station_id='DE0123', country='de', name='Sample EURDEP Station', latitude=52.5, longitude=13.4, height_above_sea=35.0, site_status=1, site_status_text='in operation')
    reading=DoseRateReading(station_id='DE0123', country='de', name='Sample EURDEP Station', value=0.09, unit='µSv/h', start_measure='2026-01-01T00:00:00Z', end_measure='2026-01-01T01:00:00Z', nuclide='Gamma-ODL-Brutto', duration='1h', validated=1)
    return [station],[reading]

async def feed(host:str, port:int, *, username:Optional[str]=None, password:Optional[str]=None, tls:bool=False, client_id:Optional[str]=None, once:bool=False, content_mode:str='binary', polling_interval:int=3600):
    paho=mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=client_id or '', protocol=MQTTv5)
    if username: paho.username_pw_set(username, password or '')
    if tls: paho.tls_set()
    client=EuJrcEurdepMqttMqttClient(client=paho, content_mode=content_mode, loop=asyncio.get_running_loop())
    await client.connect(host, port)
    try:
        while True:
            if os.getenv('EURDEP_RADIATION_SAMPLE_MODE','').lower() in ('1','true','yes'):
                stations, readings = _sample()
            else:
                api=EurdepAPI(); features=api.fetch_all_features(); stations=list(api.extract_stations(features).values()); readings=api.extract_readings(features)
            for s in stations:
                await client.publish_eu_jrc_eurdep_mqtt_station(feedurl=FEED_URL, station_id=s.station_id, country=s.country, data=s)
            for r in readings:
                await client.publish_eu_jrc_eurdep_mqtt_dose_rate_reading(feedurl=FEED_URL, station_id=r.station_id, country=r.country, data=r)
            logger.info('Published %d EURDEP stations and %d readings to MQTT', len(stations), len(readings))
            if once: break
            await asyncio.sleep(max(1,polling_interval))
    finally:
        await client.disconnect()

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    ap=argparse.ArgumentParser(); ap.add_argument('command', nargs='?', default='feed'); ap.add_argument('--broker-url', default=os.getenv('MQTT_BROKER_URL','mqtt://localhost:1883')); ap.add_argument('--username', default=os.getenv('MQTT_USERNAME','')); ap.add_argument('--password', default=os.getenv('MQTT_PASSWORD','')); ap.add_argument('--client-id', default=os.getenv('MQTT_CLIENT_ID','')); ap.add_argument('--content-mode', choices=('binary','structured'), default=os.getenv('MQTT_CONTENT_MODE','binary')); ap.add_argument('--polling-interval', type=int, default=int(os.getenv('POLLING_INTERVAL','3600'))); ap.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE','').lower() in ('1','true','yes'))
    a=ap.parse_args();
    if a.command!='feed': ap.error("only the 'feed' command is supported")
    host,port,tls=_parse_broker_url(a.broker_url); asyncio.run(feed(host,port,username=a.username or None,password=a.password or None,tls=tls,client_id=a.client_id or None,content_mode=a.content_mode,polling_interval=a.polling_interval,once=a.once))
if __name__=='__main__': main()
