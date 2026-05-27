"""MQTT feeder for JMA Bosai AMeDAS."""
from __future__ import annotations
import argparse, asyncio, logging, os, time
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from jma_bosai_amedas.jma_bosai_amedas import JmaBosaiAmedasAPI, STATION_TABLE_URL, DEFAULT_STATE_FILE, _load_state, _save_state, parse_point_station_codes
from jma_bosai_amedas_mqtt_producer_data import Station, Observation
from jma_bosai_amedas_mqtt_producer_mqtt_client.client import JPJMAAmedasMqttMqttClient
log=logging.getLogger(__name__)
class MockAPI(JmaBosaiAmedasAPI):
    def fetch_station_table(self):
        from jma_bosai_amedas.jma_bosai_amedas import parse_station
        return {'44132': parse_station('44132', {'kjName':'東京','knName':'トウキョウ','enName':'Tokyo','lat':[35,41.4],'lon':[139,45.6],'alt':25,'type':'A','elems':'11111111'})}
    def fetch_latest_time(self): return datetime(2026,1,1,0,0,tzinfo=timezone(timedelta(hours=9)))
    def fetch_observation_map(self, observed_at_local): return {'44132': {'temp':[12.3,0], 'humidity':[55,0], 'precipitation10m':[0,0], 'wind':[2.1,8,0]}}
async def cycle(api,client,state,state_file,refresh_hours):
    now=datetime.now(timezone.utc); last=state.get('last_station_metadata_refresh')
    if not last or now-datetime.fromisoformat(last) >= timedelta(hours=refresh_hours):
        stations=api.fetch_station_table() or {}
        for code, st in stations.items():
            d=Station(**st.to_serializer_dict()); await client.publish_jp_jma_amedas_mqtt_station(feedurl=STATION_TABLE_URL,prefecture=d.prefecture,station_code=code,event=d.event,data=d)
        api.stations=stations; state['last_station_metadata_refresh']=now.isoformat(); _save_state(state_file,state)
    observed=api.fetch_latest_time(); raw=api.fetch_observation_map(observed) if observed else None
    if observed and raw and observed.isoformat()!=state.get('last_snapshot_time'):
        for obs in api.iter_observations(observed, raw):
            d=Observation(**obs.to_serializer_dict()); await client.publish_jp_jma_amedas_mqtt_observation(feedurl=api.observation_url(observed),prefecture=d.prefecture,station_code=d.station_code,event=d.event,data=d)
        state['last_snapshot_time']=observed.isoformat(); _save_state(state_file,state)
async def feed(api,host,port,*,state_file,polling_interval,metadata_refresh_hours,username=None,password=None,tls=False,client_id=None,content_mode='binary',once=False):
    pc=mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=client_id or '', protocol=MQTTv5)
    if username: pc.username_pw_set(username,password or '')
    if tls: pc.tls_set()
    client=JPJMAAmedasMqttMqttClient(client=pc,content_mode=content_mode,loop=asyncio.get_running_loop()); await client.connect(host,port)
    state=_load_state(state_file)
    try:
        while True:
            start=time.monotonic(); await cycle(api,client,state,state_file,metadata_refresh_hours)
            if once: break
            await asyncio.sleep(max(0,polling_interval-(time.monotonic()-start)))
    finally: await client.disconnect()
def parse_url(url):
    p=urlparse(url if '://' in url else 'mqtt://'+url); tls=(p.scheme or 'mqtt').lower() in ('mqtts','ssl','tls'); return p.hostname or 'localhost', p.port or (8883 if tls else 1883), tls
def main():
    logging.basicConfig(level=os.getenv('LOG_LEVEL','INFO').upper())
    parser=argparse.ArgumentParser(); parser.add_argument('feed_command',nargs='?',default='feed'); parser.add_argument('--broker-url',default=os.getenv('MQTT_BROKER_URL','mqtt://localhost:1883')); parser.add_argument('--state-file',default=os.getenv('STATE_FILE',DEFAULT_STATE_FILE)); parser.add_argument('--polling-interval',type=int,default=int(os.getenv('POLLING_INTERVAL','600'))); parser.add_argument('--station-metadata-refresh-hours',type=int,default=int(os.getenv('STATION_METADATA_REFRESH_HOURS','168'))); parser.add_argument('--once',action='store_true',default=os.getenv('ONCE_MODE','').lower() in ('1','true','yes')); parser.add_argument('--username',default=os.getenv('MQTT_USERNAME','')); parser.add_argument('--password',default=os.getenv('MQTT_PASSWORD','')); parser.add_argument('--client-id',default=os.getenv('MQTT_CLIENT_ID','')); parser.add_argument('--content-mode',choices=('binary','structured'),default=os.getenv('MQTT_CONTENT_MODE','binary'))
    a=parser.parse_args(); h,p,t=parse_url(a.broker_url); api=MockAPI() if os.getenv('JMA_BOSAI_AMEDAS_MOCK','').lower() in ('1','true','yes') else JmaBosaiAmedasAPI(point_station_codes=parse_point_station_codes(os.getenv('POINT_STATION_CODES','')))
    asyncio.run(feed(api,h,p,state_file=a.state_file,polling_interval=a.polling_interval,metadata_refresh_hours=a.station_metadata_refresh_hours,username=a.username or None,password=a.password or None,tls=t,client_id=a.client_id or None,content_mode=a.content_mode,once=a.once))
