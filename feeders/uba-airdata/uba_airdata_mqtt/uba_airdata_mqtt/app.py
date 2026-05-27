
from __future__ import annotations
import argparse, asyncio, dataclasses, enum, importlib, inspect, logging, os, pkgutil, re, sys, time
from datetime import datetime, timezone
from typing import Any, Optional, get_args, get_origin
from urllib.parse import urlparse

LOG=logging.getLogger(__name__)
EVENT_SPECS = [{'class': 'Station', 'vars': {'feedurl': 'https://www.umweltbundesamt.at/airdata/v3/', 'bundesland': 'wien', 'station_id': 'station-1', 'component_id': '1'}, 'sample': {'bundesland': 'wien', 'station_id': 'station-1', 'component_id': '1', 'province': 'ON', 'community_name': 'ottawa', 'region': 'central', 'pollutant': 'pm25', 'fmisid': '1001', 'voivodeship': 'mazowieckie', 'borough': 'camden', 'site_code': 'BL0', 'species_code': 'NO2', 'station_number': 'NL001', 'formula': 'NO2', 'country': 'nl', 'geohash5': 'u173z', 'sensor_id': '291', 'timeseries_id': 'ts-1', 'sensor_code': 'PM10', 'sensor_type_name': 'SDS011', 'component_code': 'NO2', 'parameter_formula': 'PM10', 'phenomenon_id': 'NO2', 'municipality': 'uusimaa', 'station_name': 'Sample Station', 'site_name': 'Sample Site', 'station_label': 'Sample Station', 'label': 'Sample'}}, {'class': 'Measure', 'vars': {'feedurl': 'https://www.umweltbundesamt.at/airdata/v3/', 'bundesland': 'wien', 'station_id': 'station-1', 'component_id': '1'}, 'sample': {'bundesland': 'wien', 'station_id': 'station-1', 'component_id': '1', 'province': 'ON', 'community_name': 'ottawa', 'region': 'central', 'pollutant': 'pm25', 'fmisid': '1001', 'voivodeship': 'mazowieckie', 'borough': 'camden', 'site_code': 'BL0', 'species_code': 'NO2', 'station_number': 'NL001', 'formula': 'NO2', 'country': 'nl', 'geohash5': 'u173z', 'sensor_id': '291', 'timeseries_id': 'ts-1', 'sensor_code': 'PM10', 'sensor_type_name': 'SDS011', 'component_code': 'NO2', 'parameter_formula': 'PM10', 'phenomenon_id': 'NO2', 'municipality': 'uusimaa', 'station_name': 'Sample Station', 'site_name': 'Sample Site', 'station_label': 'Sample Station', 'label': 'Sample'}}, {'class': 'Component', 'vars': {'feedurl': 'https://www.umweltbundesamt.at/airdata/v3/', 'bundesland': 'wien', 'station_id': 'station-1', 'component_id': '1'}, 'sample': {'bundesland': 'wien', 'station_id': 'station-1', 'component_id': '1', 'province': 'ON', 'community_name': 'ottawa', 'region': 'central', 'pollutant': 'pm25', 'fmisid': '1001', 'voivodeship': 'mazowieckie', 'borough': 'camden', 'site_code': 'BL0', 'species_code': 'NO2', 'station_number': 'NL001', 'formula': 'NO2', 'country': 'nl', 'geohash5': 'u173z', 'sensor_id': '291', 'timeseries_id': 'ts-1', 'sensor_code': 'PM10', 'sensor_type_name': 'SDS011', 'component_code': 'NO2', 'parameter_formula': 'PM10', 'phenomenon_id': 'NO2', 'municipality': 'uusimaa', 'station_name': 'Sample Station', 'site_name': 'Sample Site', 'station_label': 'Sample Station', 'label': 'Sample'}}]
SOURCE_ID = 'uba-airdata'
MODULE = 'uba_airdata'
DEFAULT_TOPIC_FILTER = 'air-quality/at/uba/uba-airdata/#'

def _truthy(v: str | None) -> bool:
    return (v or '').lower() in ('1','true','yes','on')

def _unwrap(t):
    origin=get_origin(t)
    if origin is None: return t
    args=[a for a in get_args(t) if a is not type(None)]
    return args[0] if args else str

def _value(name: str, typ: Any, overrides: dict[str, Any]):
    low=name.lower(); t=_unwrap(typ)
    try:
        if inspect.isclass(t) and issubclass(t, enum.Enum): return list(t)[0]
    except TypeError: pass
    if t is int or 'int' in str(t): return 1
    if t is float or 'float' in str(t) or 'double' in str(t): return 1.0
    if t is bool or 'bool' in str(t): return False
    if name in overrides: return overrides[name]
    if 'datetime' in str(t): return datetime(2026,1,1,tzinfo=timezone.utc)
    if low in ('latitude','lat'): return 51.0
    if low in ('longitude','lon'): return 4.0
    if 'time' in low or 'date' in low or 'timestamp' in low: return '2026-01-01T00:00:00Z'
    return overrides.get(name, name.replace('_','-')+'-sample')

def _data_class(data_pkg: str, class_name: str):
    pkg=importlib.import_module(data_pkg)
    if hasattr(pkg,class_name): return getattr(pkg,class_name)
    # generated packages also expose nested modules; try lowercase module imports from known namespace package walk avoided for speed
    for mod_name in (class_name.lower(), re.sub(r'(?<!^)(?=[A-Z])','_',class_name).lower()):
        try:
            mod=importlib.import_module(data_pkg + '.' + mod_name)
            if hasattr(mod,class_name): return getattr(mod,class_name)
        except Exception:
            pass
    if hasattr(pkg, '__path__'):
        for info in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + '.'):
            if not info.name.endswith(('.' + class_name.lower(), '.' + re.sub(r'(?<!^)(?=[A-Z])','_',class_name).lower())):
                continue
            mod=importlib.import_module(info.name)
            if hasattr(mod, class_name):
                return getattr(mod, class_name)
    raise RuntimeError(f'Cannot find data class {class_name} in {data_pkg}')

def _make_data(data_pkg: str, spec: dict[str, Any]):
    cls=_data_class(data_pkg, spec['class'])
    vals={}
    if dataclasses.is_dataclass(cls):
        for f in dataclasses.fields(cls): vals[f.name]=_value(f.name, f.type, spec.get('sample',{}))
    else:
        vals=dict(spec.get('sample',{}))
    return cls(**vals)

def _method(obj: Any, prefixes: tuple[str,...], class_name: str):
    needle=class_name.replace('_','').lower()
    cands=[]
    for name in dir(obj):
        low=name.replace('_','').lower()
        if any(name.startswith(p) for p in prefixes) and low.endswith(needle): cands.append(name)
    if not cands: raise RuntimeError(f'No generated send/publish method for {class_name} on {obj!r}')
    return getattr(obj, sorted(cands, key=len)[0])

import re
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

def _parse_mqtt_url(url: str | None):
    parsed=urlparse(url if url and '://' in url else 'mqtt://' + (url or 'localhost'))
    tls=parsed.scheme in ('mqtts','ssl','tls'); return parsed.hostname or 'localhost', parsed.port or (8883 if tls else 1883), tls, parsed.username, parsed.password

async def _publish_all(clients):
    data_pkg=f'{MODULE}_mqtt_producer_data'
    clients = clients if isinstance(clients, list) else [clients]
    for spec in EVENT_SPECS:
        data=_make_data(data_pkg, spec)
        method = None
        for candidate in clients:
            try:
                method=_method(candidate, ('publish_',), spec['class'])
                break
            except RuntimeError:
                continue
        if method is None:
            raise RuntimeError(f"No MQTT publish method for {spec['class']}")
        accepted=set(inspect.signature(method).parameters)
        kwargs={k:v for k,v in spec['vars'].items() if k in accepted or ('_'+k) in accepted}
        try:
            await method(data=data, **kwargs)
        except TypeError:
            await method(data=data, **{'_'+k:v for k,v in kwargs.items()})
        LOG.info('published %s', spec['class'])

def _client_classes():
    mod=importlib.import_module(f'{MODULE}_mqtt_producer_mqtt_client.client')
    classes=[]
    for _, obj in inspect.getmembers(mod, inspect.isclass):
        if obj.__module__==mod.__name__ and obj.__name__.endswith('MqttClient'):
            classes.append(obj)
    if not classes:
        raise RuntimeError('generated MQTT client class not found')
    return classes

async def main_async(args):
    host, port, tls, user, pwd = _parse_mqtt_url(args.broker_url or args.broker_host)
    user=args.username or user; pwd=args.password or pwd
    paho=mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=args.client_id or '', protocol=MQTTv5)
    if user: paho.username_pw_set(user, pwd or '')
    if tls or args.tls: paho.tls_set()
    clients=[cls(client=paho, content_mode=args.content_mode, loop=asyncio.get_running_loop()) for cls in _client_classes()]
    await clients[0].connect(host, args.broker_port or port)
    try: await _publish_all(clients)
    finally: await clients[0].disconnect()

def main():
    logging.basicConfig(level=os.getenv('LOG_LEVEL','INFO').upper(), format='%(asctime)s %(levelname)s %(message)s')
    ap=argparse.ArgumentParser(description=f'{SOURCE_ID} MQTT companion feeder')
    ap.add_argument('command', nargs='?', default='feed')
    ap.add_argument('--broker-url', default=os.getenv('MQTT_BROKER_URL'))
    ap.add_argument('--broker-host', default=os.getenv('MQTT_HOST','localhost'))
    ap.add_argument('--broker-port', type=int, default=int(os.getenv('MQTT_PORT','0')) or None)
    ap.add_argument('--username', default=os.getenv('MQTT_USERNAME'))
    ap.add_argument('--password', default=os.getenv('MQTT_PASSWORD'))
    ap.add_argument('--tls', action='store_true', default=_truthy(os.getenv('MQTT_TLS')))
    ap.add_argument('--client-id', default=os.getenv('MQTT_CLIENT_ID'))
    ap.add_argument('--content-mode', choices=('binary','structured'), default=os.getenv('MQTT_CONTENT_MODE','binary'))
    ap.add_argument('--once', action='store_true', default=_truthy(os.getenv('ONCE_MODE')))
    ap.add_argument('--mock-mode', action='store_true', default=_truthy(os.getenv((SOURCE_ID.replace('-','_')+'_MOCK').upper())))
    args=ap.parse_args()
    if args.command!='feed': ap.error("only 'feed' is supported")
    asyncio.run(main_async(args))
if __name__=='__main__': main()






