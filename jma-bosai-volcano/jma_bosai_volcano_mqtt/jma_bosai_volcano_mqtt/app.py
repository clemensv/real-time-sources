from __future__ import annotations
import argparse, asyncio, logging, os, time
from urllib.parse import urlparse
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from jma_bosai_volcano.jma_bosai_volcano import JMABosaiVolcanoAPI, VOLCANO_LIST_URL, WARNING_URL, ERUPTION_URL, DEFAULT_STATE_FILE, Volcano, VolcanicWarning, VolcanicEruption, parse_volcano_catalog, parse_warning_record, parse_eruption_record
from jma_bosai_volcano_mqtt_producer_data import Volcano as MVolcano, VolcanicWarning as MWarning, VolcanicEruption as MEruption
from jma_bosai_volcano_mqtt_producer_mqtt_client.client import JPJMAVolcanoMqttMqttClient
class MockAPI(JMABosaiVolcanoAPI):
    def fetch_volcano_catalog(self): return parse_volcano_catalog([{'code':'101','nameJp':'桜島','nameEn':'Sakurajima','lat':31.58,'lon':130.66,'elevation':1117,'levelOperation':True}])
    def fetch_warnings(self): return [{'eventId':'v1','reportDatetime':'2026-01-01T00:00:00+09:00','volcanoInfos':[{'type':'噴火警報・予報（対象火山）','items':[{'code':'11','name':'活火山であることに留意','condition':'発表','areas':[{'code':'101'}]}]}]}]
    def fetch_eruptions(self): return [{'eventId':'e1','reportDatetime':'2026-01-01T00:05:00+09:00','volcanoInfos':[{'items':[{'type':'噴火','areas':[{'code':'101'}],'description':'噴火しました'}]}]}]
async def run(api,c):
    for v in api.fetch_volcano_catalog().values():
        d=MVolcano(**v.to_serializer_dict()); await c.publish_jp_jma_volcano_mqtt_volcano(feedurl=VOLCANO_LIST_URL,prefecture=d.prefecture,volcano_code=d.volcano_code,event=d.event,data=d)
    for rec in api.fetch_warnings():
        for w in parse_warning_record(rec):
            d=MWarning(**w.to_serializer_dict()); await c.publish_jp_jma_volcano_mqtt_volcanic_warning(feedurl=WARNING_URL,prefecture=d.prefecture,volcano_code=d.volcano_code,event=d.event,data=d)
    for rec in api.fetch_eruptions():
        for e in parse_eruption_record(rec):
            d=MEruption(**e.to_serializer_dict()); await c.publish_jp_jma_volcano_mqtt_volcanic_eruption(feedurl=ERUPTION_URL,prefecture=d.prefecture,volcano_code=d.volcano_code,event=d.event,data=d)
def parse_url(u):
    p=urlparse(u if '://' in u else 'mqtt://'+u); t=(p.scheme or 'mqtt').lower() in ('mqtts','ssl','tls'); return p.hostname or 'localhost', p.port or (8883 if t else 1883), t
async def feed(api,h,p,tls=False,username=None,password=None,content_mode='binary'):
    pc=mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2,protocol=MQTTv5);
    if username: pc.username_pw_set(username,password or '')
    if tls: pc.tls_set()
    c=JPJMAVolcanoMqttMqttClient(client=pc,content_mode=content_mode,loop=asyncio.get_running_loop()); await c.connect(h,p)
    try: await run(api,c)
    finally: await c.disconnect()
def main():
    logging.basicConfig(level=os.getenv('LOG_LEVEL','INFO').upper()); pa=argparse.ArgumentParser(); pa.add_argument('feed_command',nargs='?',default='feed'); pa.add_argument('--broker-url',default=os.getenv('MQTT_BROKER_URL','mqtt://localhost:1883')); pa.add_argument('--username',default=os.getenv('MQTT_USERNAME','')); pa.add_argument('--password',default=os.getenv('MQTT_PASSWORD','')); pa.add_argument('--content-mode',default=os.getenv('MQTT_CONTENT_MODE','binary')); a=pa.parse_args(); h,p,t=parse_url(a.broker_url); api=MockAPI() if os.getenv('JMA_BOSAI_VOLCANO_MOCK','').lower() in ('1','true','yes') else JMABosaiVolcanoAPI(); asyncio.run(feed(api,h,p,tls=t,username=a.username or None,password=a.password or None,content_mode=a.content_mode))
