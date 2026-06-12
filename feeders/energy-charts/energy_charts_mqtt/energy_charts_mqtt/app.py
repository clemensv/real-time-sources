"""MQTT companion feeder for energy-charts. Publishes mock/sample CloudEvents for Docker E2E and auth-blocked upstreams."""
from __future__ import annotations
import argparse, asyncio, inspect, json, os, pathlib, re
from datetime import datetime, timezone
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from energy_charts_mqtt_producer_mqtt_client import client as client_mod
import energy_charts_mqtt_producer_data as data_mod

def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
    params = {
        "api-version": "2018-02-01",
        "resource": audience or "https://eventgrid.azure.net/",
    }
    if managed_identity_client_id:
        params["client_id"] = managed_identity_client_id

    request = Request(
        "http://169.254.169.254/metadata/identity/oauth2/token?" + urlencode(params),
        headers={"Metadata": "true"},
    )
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    token = payload.get("accessToken") or payload.get("access_token")
    if not token:
        raise RuntimeError("IMDS token response did not contain an access token")
    return str(token)

def _resolve_mqtt_connection_settings(*, username=None, password=None, client_id=None, auth_mode=None):
    resolved_client_id = str(client_id or os.getenv("MQTT_CLIENT_ID") or "").strip()
    auth_mode = str(auth_mode or os.getenv("MQTT_AUTH_MODE", "password")).strip().lower() or "password"

    if auth_mode != "entra":
        return resolved_client_id, str(username or ""), str(password or ""), None

    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    resolved_username = resolved_client_id or str(username or "").strip()
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")

    resolved_password = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    from paho.mqtt.properties import Properties as _MqttConnProps
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    _connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
    _connect_props.AuthenticationMethod = "OAUTH2-JWT"
    _connect_props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, _connect_props

MANIFEST = pathlib.Path(os.getenv('SOURCE_MANIFEST', '/app/xreg/energy_charts.xreg.json'))

def _val(name, typ):
    n=name.lower()
    if 'date' in n and 'time' not in n: return '2026-01-01'
    if 'time' in n or typ == 'datetime': return datetime(2026,1,1,tzinfo=timezone.utc)
    if 'country' in n: return 'gb' if 'energy-charts'=='elexon-bmrs' else ('jp' if 'energy-charts'=='tepco-denkiyoho' else 'dk' if 'energy-charts'=='energidataservice-dk' else 'de' if 'energy-charts'=='energy-charts' else 'nl')
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
    resolved_client_id, resolved_username, resolved_password, _entra_props = _resolve_mqtt_connection_settings(
        username=args.username,
        password=args.password or '',
        client_id=args.client_id or '',
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho=mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if _entra_props is None and (resolved_username or resolved_password):
        paho.username_pw_set(resolved_username, resolved_password)
    if tls or _entra_props is not None: paho.tls_set()
    loop=asyncio.get_running_loop()
    classes=[v for v in vars(client_mod).values() if isinstance(v,type) and v.__name__.endswith('MqttClient')]
    clients=[cls(client=paho, content_mode='binary', loop=loop) for cls in classes]
    # WORKAROUND(xregistry/codegen#432): pass Entra JWT CONNECT properties directly to paho
    if _entra_props is not None:
        paho.connect(host, port, keepalive=60, clean_start=True, properties=_entra_props)
        paho.loop_start()
    else:
        await clients[0].connect(host,port)
    try:
        for sh,payload,_ in _iter_events(): await _publish_one(clients,sh,payload)
    finally:
        await clients[0].disconnect()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('feed', nargs='?', default='feed'); ap.add_argument('--broker-url', default=os.getenv('MQTT_BROKER_URL','mqtt://localhost:1883')); ap.add_argument('--username', default=os.getenv('MQTT_USERNAME','')); ap.add_argument('--password', default=os.getenv('MQTT_PASSWORD','')); ap.add_argument('--client-id', default=os.getenv('MQTT_CLIENT_ID','')); args=ap.parse_args(); asyncio.run(run(args))
if __name__=='__main__': main()
