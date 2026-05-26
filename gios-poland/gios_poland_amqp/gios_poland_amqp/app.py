
from __future__ import annotations
import argparse, asyncio, dataclasses, enum, importlib, inspect, logging, os, pkgutil, re, sys, time
from datetime import datetime, timezone
from typing import Any, Optional, get_args, get_origin
from urllib.parse import urlparse

LOG=logging.getLogger(__name__)
EVENT_SPECS = [{'class': 'Station', 'vars': {'voivodeship': 'mazowieckie', 'station_id': 'station-1', 'pollutant': 'pm25'}, 'sample': {'voivodeship': 'mazowieckie', 'station_id': 'station-1', 'pollutant': 'pm25', 'province': 'ON', 'community_name': 'ottawa', 'region': 'central', 'fmisid': '1001', 'borough': 'camden', 'site_code': 'BL0', 'species_code': 'NO2', 'station_number': 'NL001', 'formula': 'NO2', 'country': 'nl', 'geohash5': 'u173z', 'sensor_id': '291', 'bundesland': 'wien', 'component_id': '1', 'timeseries_id': 'ts-1', 'sensor_code': 'PM10', 'sensor_type_name': 'SDS011', 'component_code': 'NO2', 'parameter_formula': 'PM10', 'phenomenon_id': 'NO2', 'municipality': 'uusimaa', 'station_name': 'Sample Station', 'site_name': 'Sample Site', 'station_label': 'Sample Station', 'label': 'Sample'}}, {'class': 'Sensor', 'vars': {'voivodeship': 'mazowieckie', 'station_id': 'station-1', 'pollutant': 'pm25', 'sensor_id': '291'}, 'sample': {'voivodeship': 'mazowieckie', 'station_id': 'station-1', 'pollutant': 'pm25', 'sensor_id': '291', 'province': 'ON', 'community_name': 'ottawa', 'region': 'central', 'fmisid': '1001', 'borough': 'camden', 'site_code': 'BL0', 'species_code': 'NO2', 'station_number': 'NL001', 'formula': 'NO2', 'country': 'nl', 'geohash5': 'u173z', 'bundesland': 'wien', 'component_id': '1', 'timeseries_id': 'ts-1', 'sensor_code': 'PM10', 'sensor_type_name': 'SDS011', 'component_code': 'NO2', 'parameter_formula': 'PM10', 'phenomenon_id': 'NO2', 'municipality': 'uusimaa', 'station_name': 'Sample Station', 'site_name': 'Sample Site', 'station_label': 'Sample Station', 'label': 'Sample'}}, {'class': 'Measurement', 'vars': {'voivodeship': 'mazowieckie', 'station_id': 'station-1', 'pollutant': 'pm25', 'sensor_id': '291'}, 'sample': {'voivodeship': 'mazowieckie', 'station_id': 'station-1', 'pollutant': 'pm25', 'sensor_id': '291', 'province': 'ON', 'community_name': 'ottawa', 'region': 'central', 'fmisid': '1001', 'borough': 'camden', 'site_code': 'BL0', 'species_code': 'NO2', 'station_number': 'NL001', 'formula': 'NO2', 'country': 'nl', 'geohash5': 'u173z', 'bundesland': 'wien', 'component_id': '1', 'timeseries_id': 'ts-1', 'sensor_code': 'PM10', 'sensor_type_name': 'SDS011', 'component_code': 'NO2', 'parameter_formula': 'PM10', 'phenomenon_id': 'NO2', 'municipality': 'uusimaa', 'station_name': 'Sample Station', 'site_name': 'Sample Site', 'station_label': 'Sample Station', 'label': 'Sample'}}, {'class': 'AirQualityIndex', 'vars': {'voivodeship': 'mazowieckie', 'station_id': 'station-1', 'pollutant': 'pm25'}, 'sample': {'voivodeship': 'mazowieckie', 'station_id': 'station-1', 'pollutant': 'pm25', 'province': 'ON', 'community_name': 'ottawa', 'region': 'central', 'fmisid': '1001', 'borough': 'camden', 'site_code': 'BL0', 'species_code': 'NO2', 'station_number': 'NL001', 'formula': 'NO2', 'country': 'nl', 'geohash5': 'u173z', 'sensor_id': '291', 'bundesland': 'wien', 'component_id': '1', 'timeseries_id': 'ts-1', 'sensor_code': 'PM10', 'sensor_type_name': 'SDS011', 'component_code': 'NO2', 'parameter_formula': 'PM10', 'phenomenon_id': 'NO2', 'municipality': 'uusimaa', 'station_name': 'Sample Station', 'site_name': 'Sample Site', 'station_label': 'Sample Station', 'label': 'Sample'}}]
SOURCE_ID = 'gios-poland'
MODULE = 'gios_poland'
DEFAULT_TOPIC_FILTER = 'air-quality/pl/gios/gios-poland/#'

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

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS='https://servicebus.azure.net/.default'

def _parse_amqp_url(url: str | None):
    parsed=urlparse(url if url and '://' in url else 'amqp://' + (url or 'localhost'))
    tls=parsed.scheme in ('amqps','ssl','tls'); return parsed.hostname or 'localhost', parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or '').lstrip('/') or None

def _producer_classes():
    mod=importlib.import_module(f'{MODULE}_amqp_producer_amqp_producer.producer')
    classes=[]
    for _, obj in inspect.getmembers(mod, inspect.isclass):
        if obj.__module__==mod.__name__ and obj.__name__.endswith('AmqpProducer'):
            classes.append(obj)
    if not classes:
        raise RuntimeError('generated AMQP producer class not found')
    return classes

def _build_producer(args):
    host, port, tls, user, pwd, path = _parse_amqp_url(args.broker_url or args.host)
    address=args.address or path or SOURCE_ID
    classes=_producer_classes()
    def make(cls):
        if args.auth_mode=='entra':
            from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
            cred=ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential()
            return cls(host=host, address=address, port=args.port or port, content_mode=args.content_mode, credential=cred, entra_audience=args.entra_audience, use_tls=True)
        if args.auth_mode=='sas':
            return cls(host=host, address=address, port=args.port or port, content_mode=args.content_mode, sas_key_name=args.sas_key_name, sas_key=args.sas_key, use_tls=True)
        return cls(host=host, address=address, port=args.port or port, username=args.username or user, password=args.password or pwd, content_mode=args.content_mode, use_tls=args.tls or tls)
    return [make(cls) for cls in classes]

def _publish_all(producers):
    data_pkg=f'{MODULE}_amqp_producer_data'
    producers = producers if isinstance(producers, list) else [producers]
    for spec in EVENT_SPECS:
        data=_make_data(data_pkg, spec)
        method = None
        for candidate in producers:
            try:
                method=_method(candidate, ('send_',), spec['class'])
                break
            except RuntimeError:
                continue
        if method is None:
            raise RuntimeError(f"No AMQP send method for {spec['class']}")
        accepted=set(inspect.signature(method).parameters)
        kwargs={k:v for k,v in spec['vars'].items() if k in accepted or ('_'+k) in accepted}
        try:
            method(data=data, **{'_'+k:v for k,v in kwargs.items()})
        except TypeError:
            method(data=data, **kwargs)
        LOG.info('sent %s', spec['class'])

def main():
    logging.basicConfig(level=os.getenv('LOG_LEVEL','INFO').upper(), format='%(asctime)s %(levelname)s %(message)s')
    ap=argparse.ArgumentParser(description=f'{SOURCE_ID} AMQP companion feeder')
    ap.add_argument('command', nargs='?', default='feed')
    ap.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL'))
    ap.add_argument('--host', default=os.getenv('AMQP_HOST','localhost'))
    ap.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT','0')) or None)
    ap.add_argument('--address', default=os.getenv('AMQP_ADDRESS', SOURCE_ID))
    ap.add_argument('--username', default=os.getenv('AMQP_USERNAME'))
    ap.add_argument('--password', default=os.getenv('AMQP_PASSWORD'))
    ap.add_argument('--tls', action='store_true', default=_truthy(os.getenv('AMQP_TLS')))
    ap.add_argument('--content-mode', choices=('binary','structured'), default=os.getenv('AMQP_CONTENT_MODE','binary'))
    ap.add_argument('--auth-mode', choices=('password','entra','sas'), default=os.getenv('AMQP_AUTH_MODE','password'))
    ap.add_argument('--entra-audience', default=os.getenv('AMQP_ENTRA_AUDIENCE', DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    ap.add_argument('--entra-client-id', default=os.getenv('AMQP_ENTRA_CLIENT_ID'))
    ap.add_argument('--sas-key-name', default=os.getenv('AMQP_SAS_KEY_NAME'))
    ap.add_argument('--sas-key', default=os.getenv('AMQP_SAS_KEY'))
    ap.add_argument('--once', action='store_true', default=_truthy(os.getenv('ONCE_MODE')))
    ap.add_argument('--mock-mode', action='store_true', default=_truthy(os.getenv((SOURCE_ID.replace('-','_')+'_MOCK').upper())))
    args=ap.parse_args()
    if args.command!='feed': ap.error("only 'feed' is supported")
    producers=_build_producer(args)
    try: _publish_all(producers)
    finally:
        for producer in (producers if isinstance(producers, list) else [producers]):
            producer.close()
if __name__=='__main__': main()






