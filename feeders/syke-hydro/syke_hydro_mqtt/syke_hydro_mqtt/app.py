
import dataclasses, importlib, inspect, os, pkgutil, sys, typing
from datetime import datetime, timezone

import json

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

def _slug(v):
    return str(v or 'unknown').replace('/', '-').replace(' ', '-').lower()

def _sample_value(name, annotation):
    lname = name.lower().rstrip('_')
    if lname in ('station_id','station_number','code_station','station_ref','station_reference','site_number'):
        return 'mock-station'
    if lname in ('sensor_num',): return 1
    if lname in ('parameter_code',): return '00010'
    if lname in ('state',): return 'CA'
    if lname in ('region',): return 'PACIFIC'
    if lname in ('basin','river','water_body','water_body_name','river_name','libelle_cours_eau','water_area_name'):
        return 'mock-basin'
    if 'time' in lname or 'date' in lname: return datetime.now(timezone.utc).isoformat()
    if 'lat' in lname: return 45.0
    if lname in ('longitude','long','lng') or 'lon' in lname: return -75.0
    if any(x in lname for x in ('level','value','temperature','speed','pressure','height','depth','salinity','conductivity','humidity','visibility','discharge','flow','elevation','latitude')): return 1.0
    if any(x in lname for x in ('code',)): return '01'
    if any(x in lname for x in ('count','num','bin','direction','timezonecorr')): return 1
    if lname.startswith('is_') or lname in ('tidal','greatlakes','observedst','stormsurge','forecast','outlook','nonNavigational'.lower(),'en_service','outside_sigma_band','flat_tolerance_limit','rate_of_change_limit','max_min_expected_height','max_pressure_exceeded','min_pressure_exceeded','rate_of_change_exceeded','max_temp_exceeded','min_temp_exceeded','max_humidity_exceeded','min_humidity_exceeded','max_conductivity_exceeded','min_conductivity_exceeded'):
        return False
    return 'mock'

def _make_instance(cls):
    kwargs={}
    for f in dataclasses.fields(cls):
        if not f.init: continue
        ann=f.type
        origin=typing.get_origin(ann)
        args=typing.get_args(ann)
        if origin in (typing.Union, getattr(typing, 'Optional', object)) and args:
            ann=next((a for a in args if a is not type(None)), args[0])
        try:
            if dataclasses.is_dataclass(ann):
                kwargs[f.name]=_make_instance(ann); continue
        except Exception:
            pass
        kwargs[f.name]=_sample_value(f.name, ann)
    return cls(**kwargs)

def _required_call_kwargs(method, data_pkg):
    sig=inspect.signature(method)
    out={}
    data_obj=None
    for name,param in sig.parameters.items():
        if name in ('self','topic','qos','retain','content_type','flush_producer'): continue
        if name == 'data':
            ann=param.annotation
            if isinstance(ann, str): ann=None
            if ann is inspect._empty or ann is None:
                raise RuntimeError(f'No data annotation for {method}')
            data_obj=_make_instance(ann)
            out[name]=data_obj
        else:
            key=name[1:] if name.startswith('_') else name
            out[name]=_sample_value(key, str(param.annotation))
    return out

import argparse, asyncio, logging
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
import syke_hydro_mqtt_producer_data
from syke_hydro_mqtt_producer_mqtt_client.client import *

async def _publish_mock(client):
    methods=[getattr(client,n) for n in dir(client) if n.startswith('publish_')]
    for method in methods:
        await method(**_required_call_kwargs(method, syke_hydro_mqtt_producer_data))

async def feed(host, port, username=None, password=None, tls=False, client_id=None, once=False, content_mode='binary'):
    resolved_client_id, resolved_username, resolved_password, _entra_props = _resolve_mqtt_connection_settings(
        username=username,
        password=password or '',
        client_id=client_id or '',
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho_client=mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if _entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls: paho_client.tls_set()
    client_cls=next(obj for obj in globals().values() if isinstance(obj,type) and obj.__name__.endswith('MqttClient'))
    client=client_cls(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    if _entra_props is not None:
        paho_client.connect(host, port, keepalive=60, clean_start=True, properties=_entra_props)
        paho_client.loop_start()
    else:
        await client.connect(host, port)
    try:
        await _publish_mock(client)
    finally:
        await client.disconnect()

def _parse_broker_url(url):
    parsed=urlparse(url if '://' in url else f'mqtt://{url}')
    tls=(parsed.scheme or 'mqtt').lower() in ('mqtts','ssl','tls')
    return parsed.hostname or 'localhost', parsed.port or (8883 if tls else 1883), tls, parsed.username, parsed.password

def main(argv=None):
    logging.basicConfig(level=logging.INFO)
    p=argparse.ArgumentParser(description='syke-hydro MQTT/UNS bridge')
    sub=p.add_subparsers(dest='command'); f=sub.add_parser('feed')
    f.add_argument('--broker-url', default=os.getenv('MQTT_BROKER_URL'))
    f.add_argument('--broker-host', default=os.getenv('MQTT_HOST'))
    f.add_argument('--broker-port', type=int, default=int(os.getenv('MQTT_PORT','0')) or None)
    f.add_argument('--username', default=os.getenv('MQTT_USERNAME'))
    f.add_argument('--password', default=os.getenv('MQTT_PASSWORD'))
    f.add_argument('--tls', action='store_true', default=os.getenv('MQTT_TLS','').lower() in ('1','true','yes'))
    f.add_argument('--client-id', default=os.getenv('MQTT_CLIENT_ID'))
    f.add_argument('--content-mode', default=os.getenv('MQTT_CONTENT_MODE','binary'), choices=['binary','structured'])
    f.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE','').lower() in ('1','true','yes'))
    args=p.parse_args(argv)
    if args.command!='feed': p.print_help(); return
    if args.broker_url:
        host, port, tls, user, pwd=_parse_broker_url(args.broker_url); username=args.username or user; password=args.password or pwd; port=args.broker_port or port; tls=tls or args.tls
    else:
        tls=args.tls; host=args.broker_host or 'localhost'; port=args.broker_port or (8883 if tls else 1883); username=args.username; password=args.password
    asyncio.run(feed(host, port, username=username, password=password, tls=tls, client_id=args.client_id, once=args.once, content_mode=args.content_mode))
