
import dataclasses, importlib, inspect, os, pkgutil, sys, typing
from datetime import datetime, timezone

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
    if any(x in lname for x in ('count','code','num','bin','direction','timezonecorr')): return 1
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

import argparse, logging
from urllib.parse import urlparse
import waterinfo_vmm_amqp_producer_data
from waterinfo_vmm_amqp_producer_amqp_producer.producer import *

def _build_producer(cls, host, port, address, tls, content_mode, auth_mode, username, password, entra_audience, entra_client_id, sas_key_name, sas_key):
    if auth_mode == 'entra':
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        cred=ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return cls(host=host, address=address, port=port, content_mode=content_mode, credential=cred, entra_audience=entra_audience, use_tls=tls)
    if auth_mode == 'sas':
        return cls(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=tls)
    return cls(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=tls)

def feed(host, port, address='waterinfo-vmm', username=None, password=None, tls=False, content_mode='binary', auth_mode='password', entra_audience='https://servicebus.azure.net/.default', entra_client_id=None, sas_key_name=None, sas_key=None, once=False):
    cls=next(obj for obj in globals().values() if isinstance(obj,type) and obj.__name__.endswith('AmqpProducer'))
    producer=_build_producer(cls, host, port, address, tls, content_mode, auth_mode, username, password, entra_audience, entra_client_id, sas_key_name, sas_key)
    try:
        for method in [getattr(producer,n) for n in dir(producer) if n.startswith('send_') and not n.endswith('_batch')]:
            method(**_required_call_kwargs(method, waterinfo_vmm_amqp_producer_data))
    finally:
        close=getattr(producer,'close',None)
        if close: close()

def _parse_broker_url(url):
    parsed=urlparse(url if '://' in url else f'amqp://{url}')
    tls=(parsed.scheme or 'amqp').lower() in ('amqps','ssl','tls')
    return parsed.hostname or 'localhost', parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or '').lstrip('/') or None

def main(argv=None):
    logging.basicConfig(level=logging.INFO)
    p=argparse.ArgumentParser(description='waterinfo-vmm AMQP 1.0 bridge')
    sub=p.add_subparsers(dest='command'); f=sub.add_parser('feed')
    f.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL'))
    f.add_argument('--broker-host', default=os.getenv('AMQP_HOST'))
    f.add_argument('--broker-port', type=int, default=int(os.getenv('AMQP_PORT','0')) or None)
    f.add_argument('--address', default=os.getenv('AMQP_ADDRESS','waterinfo-vmm'))
    f.add_argument('--username', default=os.getenv('AMQP_USERNAME'))
    f.add_argument('--password', default=os.getenv('AMQP_PASSWORD'))
    f.add_argument('--tls', action='store_true', default=os.getenv('AMQP_TLS','').lower() in ('1','true','yes'))
    f.add_argument('--content-mode', default=os.getenv('AMQP_CONTENT_MODE','binary'), choices=['binary','structured'])
    f.add_argument('--auth-mode', default=os.getenv('AMQP_AUTH_MODE','password'), choices=['password','entra','sas'])
    f.add_argument('--entra-audience', default=os.getenv('AMQP_ENTRA_AUDIENCE','https://servicebus.azure.net/.default'))
    f.add_argument('--entra-client-id', default=os.getenv('AMQP_ENTRA_CLIENT_ID'))
    f.add_argument('--sas-key-name', default=os.getenv('AMQP_SAS_KEY_NAME'))
    f.add_argument('--sas-key', default=os.getenv('AMQP_SAS_KEY'))
    f.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE','').lower() in ('1','true','yes'))
    args=p.parse_args(argv)
    if args.command!='feed': p.print_help(); return
    if args.broker_url:
        host, port, tls, user, pwd, path=_parse_broker_url(args.broker_url); username=args.username or user; password=args.password or pwd; port=args.broker_port or port; tls=tls or args.tls; address=path or args.address
    else:
        tls=args.tls or args.auth_mode in ('entra','sas'); host=args.broker_host or 'localhost'; port=args.broker_port or (5671 if tls else 5672); username=args.username; password=args.password; address=args.address
    feed(host, port, address=address, username=username, password=password, tls=tls, content_mode=args.content_mode, auth_mode=args.auth_mode, entra_audience=args.entra_audience, entra_client_id=args.entra_client_id, sas_key_name=args.sas_key_name, sas_key=args.sas_key, once=args.once)

