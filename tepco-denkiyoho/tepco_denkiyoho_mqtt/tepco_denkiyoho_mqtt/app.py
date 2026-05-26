"""MQTT companion feeder for tepco-denkiyoho. Publishes mock/sample CloudEvents for Docker E2E and auth-blocked upstreams."""
from __future__ import annotations
import argparse, asyncio, inspect, json, os, pathlib, re
from datetime import datetime, timezone
from urllib.parse import urlparse
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from tepco_denkiyoho_mqtt_producer_mqtt_client import client as client_mod
import tepco_denkiyoho_mqtt_producer_data as data_mod

MANIFEST = pathlib.Path(os.getenv('SOURCE_MANIFEST', '/app/xreg/tepco-denkiyoho.xreg.json'))

def _val(name, typ):
    n=name.lower()
    if 'date' in n and 'time' not in n: return '2026-01-01'
    if 'time' in n or typ == 'datetime': return datetime(2026,1,1,tzinfo=timezone.utc)
    if 'country' in n: return 'gb' if 'tepco-denkiyoho'=='elexon-bmrs' else ('jp' if 'tepco-denkiyoho'=='tepco-denkiyoho' else 'dk' if 'tepco-denkiyoho'=='energidataservice-dk' else 'de' if 'tepco-denkiyoho'=='energy-charts' else 'nl')
    if 'city' in n: return 'amsterdam'
    if 'category' in n: return 'music'
    if 'segment' in n: return 'music'
    if 'venue_id' in n: return 'venue-1'
    if 'event_id' in n: return 'event-1'
    if 'entity_id' in n or 'info_id' in n: return 'info-1'
    if 'price_area' in n: return 'DK1'
    if 'area_code' in n: return 'TEPCO'
    if 'settlement_period' in n: return 1
    if typ in ('int32','int64','integer'): return 1
    if typ in ('double','float','number'): return 1.0
    if typ == 'boolean': return True
    return name.replace('_','-')+'-sample'

def _sample(schema):
    props=schema.get('properties',{}); data={}
    for name,p in props.items():
        typ=p.get('type','string')
        if isinstance(typ,list): typ=next((t for t in typ if t!='null'),'string')
        if isinstance(typ,dict): data[name]={}
        elif typ == 'array': data[name]=[]
        elif typ == 'object': data[name]={}
        else: data[name]=_val(name, typ)
    return data

def _iter_events():
    m=json.loads(MANIFEST.read_text(encoding='utf-8'))
    schemas={}
    for sg in m.get('schemagroups',{}).values():
        for sid,sv in sg.get('schemas',{}).items():
            schema = sv['versions']['1']['schema']
            if isinstance(schema, dict) and 'properties' not in schema and schema.get('$root'):
                node = schema
                for part in schema['$root'].lstrip('#/').split('/'):
                    node = node.get(part, {}) if isinstance(node, dict) else {}
                if isinstance(node, dict) and 'properties' in node:
                    schema = node
            if isinstance(schema, dict) and 'properties' in schema:
                schemas[sid]=schema
    for g,gv in m.get('messagegroups',{}).items():
        if not g.endswith('.mqtt'): continue
        for mid,msg in gv.get('messages',{}).items():
            base=msg.get('basemessageuri','').split('/messages/')[-1]
            sh=msg.get('name') or mid.split('.')[-1]
            yield sh, _sample(schemas[base]), msg['protocoloptions']['topic_name']

def _norm(s): return re.sub(r'[^a-z0-9]+','_',s.lower()).strip('_')
def _compact(s): return re.sub(r'[^a-z0-9]+','',s.lower())
async def _publish_one(clients, sh, payload):
    cls=getattr(data_mod, sh)
    data=cls(**payload)
    values=dict(payload)
    for k,v in list(values.items()):
        if isinstance(v, datetime): values[k]=v.isoformat().replace('+00:00','Z')
    for c in clients:
        methods=[(n,getattr(c,n)) for n in dir(c) if n.startswith('publish_') and _compact(sh) in _compact(n)]
        for _,meth in methods:
            sig=inspect.signature(meth); kwargs={}
            for pname in sig.parameters:
                if pname in ('topic','qos','retain','content_type'):
                    continue
                if pname=='data': kwargs[pname]=data
                elif pname in values: kwargs[pname]=values[pname]
                elif pname.startswith('_') and pname[1:] in values: kwargs[pname]=values[pname[1:]]
                elif pname.startswith('_'): kwargs[pname]=_val(pname[1:],'string')
                else: kwargs[pname]=_val(pname,'string')
            await meth(**kwargs); return
    raise RuntimeError(f'No MQTT publish method for {sh}')

def _parse(url):
    p=urlparse(url if '://' in url else 'mqtt://'+url); tls=(p.scheme or 'mqtt').lower() in ('mqtts','ssl','tls'); return p.hostname or 'localhost', p.port or (8883 if tls else 1883), tls
async def run(args):
    host,port,tls=_parse(args.broker_url)
    paho=mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=args.client_id or '', protocol=MQTTv5)
    if args.username: paho.username_pw_set(args.username,args.password or '')
    if tls: paho.tls_set()
    loop=asyncio.get_running_loop()
    classes=[v for v in vars(client_mod).values() if isinstance(v,type) and v.__name__.endswith('MqttClient')]
    clients=[cls(client=paho, content_mode='binary', loop=loop) for cls in classes]
    await clients[0].connect(host,port)
    try:
        for sh,payload,_ in _iter_events(): await _publish_one(clients,sh,payload)
    finally:
        await clients[0].disconnect()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('feed', nargs='?', default='feed'); ap.add_argument('--broker-url', default=os.getenv('MQTT_BROKER_URL','mqtt://localhost:1883')); ap.add_argument('--username', default=os.getenv('MQTT_USERNAME','')); ap.add_argument('--password', default=os.getenv('MQTT_PASSWORD','')); ap.add_argument('--client-id', default=os.getenv('MQTT_CLIENT_ID','')); args=ap.parse_args(); asyncio.run(run(args))
if __name__=='__main__': main()
