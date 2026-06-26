from __future__ import annotations
import argparse, asyncio, logging, os
from urllib.parse import urlparse
try:
    from proton import symbol
except Exception:
    symbol=lambda value:value  # type: ignore
from environment_canada_core import ECWeatherAPI, _load_state, _save_state
from environment_canada_amqp_producer_amqp_producer.producer import CAGovECCCWeatherAmqpProducer
logger=logging.getLogger(__name__)
DEFAULT_ENTRA_AUDIENCE_SERVICEBUS="https://servicebus.azure.net/.default"
def _env_bool(name, default=False): value=os.getenv(name); return default if value is None else value.lower() in {"1","true","yes","on"}
def _segment(value):
    text=(str(value) if value is not None else "unknown").strip() or "unknown"
    for forbidden in ("/","+","#","\x00"): text=text.replace(forbidden,"-")
    return "-".join(text.split()) or "unknown"
def _parse(url):
    parsed=urlparse(url if "://" in url else f"amqp://{url}"); scheme=(parsed.scheme or "amqp").lower(); tls=scheme in ("amqps","ssl","tls"); return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or "").lstrip("/") or None
def _apply(producer):
    def stamp(msg):
        props=dict(getattr(msg,'properties',None) or {}); subject=props.get('cloudEvents:subject') or getattr(msg,'subject',None)
        if subject:
            annotations=dict(getattr(msg,'annotations',None) or {}); annotations[symbol('x-opt-partition-key')]=str(subject); msg.annotations=annotations
        return msg
    if getattr(producer,'_sender',None) is not None:
        original=producer._sender.send; producer._sender.send=lambda msg,*a,**kw: original(stamp(msg),*a,**kw)
    if getattr(producer,'_send_queue',None) is not None:
        original=producer._send_via_reactor; producer._send_via_reactor=lambda msg: original(stamp(msg))
    return producer
def _build(args):
    address=args.address
    if args.broker_url:
        host,port,tls,user0,pwd0,path=_parse(args.broker_url); user=args.username or user0; pwd=args.password or pwd0
        if args.port: port=args.port
        if args.tls: tls=True
        address=path or address
    else:
        host=args.host or 'localhost'; tls=bool(args.tls) or args.auth_mode=='entra'; port=args.port or (5671 if tls else 5672); user=args.username; pwd=args.password
    kwargs=dict(host=host,address=address,port=port,content_mode=args.content_mode,use_tls=tls)
    if args.auth_mode=='entra':
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        kwargs.update(credential=ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential(), entra_audience=args.entra_audience)
    elif args.auth_mode=='sas': kwargs.update(sas_key_name=args.sas_key_name, sas_key=args.sas_key)
    else: kwargs.update(username=user,password=pwd)
    return _apply(CAGovECCCWeatherAmqpProducer(**kwargs))
async def _run(args,producer):
    api=ECWeatherAPI(polling_interval=args.polling_interval, station_limit=args.station_limit, obs_limit=args.obs_limit); state=_load_state(args.state_file); provinces={}
    for feature in api.get_stations():
        station=api.parse_station(feature)
        if not station.msc_id: continue
        provinces[station.msc_id]=station.province or station.province_territory
        producer.send_station(data=station,_msc_id=station.msc_id,_province=_segment(station.province or station.province_territory or 'unknown'))
    while True:
        for feature in api.get_recent_observations():
            obs=api.parse_observation(feature)
            if not obs: continue
            key=f"{obs.msc_id}:{obs.observation_time.isoformat()}"
            if key in state: continue
            producer.send_weather_observation(data=obs,_msc_id=obs.msc_id,_province=_segment(obs.province or provinces.get(obs.msc_id) or 'unknown'),_time=obs.observation_time.isoformat())
            state[key]=obs.observation_time.isoformat()
        _save_state(args.state_file,state)
        if args.once: break
        await asyncio.sleep(args.polling_interval)
def main():
    logging.basicConfig(level=os.getenv('LOG_LEVEL','INFO').upper(), format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    p=argparse.ArgumentParser(); p.add_argument('feed_command', nargs='?', default='feed'); p.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL')); p.add_argument('--host', default=os.getenv('AMQP_HOST')); p.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT','0')) or None); p.add_argument('--address', default=os.getenv('AMQP_ADDRESS','environment-canada')); p.add_argument('--username', default=os.getenv('AMQP_USERNAME')); p.add_argument('--password', default=os.getenv('AMQP_PASSWORD')); p.add_argument('--tls', action='store_true', default=_env_bool('AMQP_TLS',False)); p.add_argument('--content-mode', choices=('binary','structured'), default=os.getenv('AMQP_CONTENT_MODE','binary')); p.add_argument('--auth-mode', choices=('password','entra','sas'), default=os.getenv('AMQP_AUTH_MODE','password')); p.add_argument('--entra-audience', default=os.getenv('AMQP_ENTRA_AUDIENCE', DEFAULT_ENTRA_AUDIENCE_SERVICEBUS)); p.add_argument('--entra-client-id', default=os.getenv('AMQP_ENTRA_CLIENT_ID')); p.add_argument('--sas-key-name', default=os.getenv('AMQP_SAS_KEY_NAME')); p.add_argument('--sas-key', default=os.getenv('AMQP_SAS_KEY')); p.add_argument('--state-file', default=os.getenv('STATE_FILE', os.path.expanduser(r'~/.environment_canada_amqp_state.json'))); p.add_argument('--polling-interval', type=int, default=int(os.getenv('POLLING_INTERVAL','900'))); p.add_argument('--station-limit', type=int, default=int(os.getenv('STATION_LIMIT','500'))); p.add_argument('--obs-limit', type=int, default=int(os.getenv('OBS_LIMIT','500'))); p.add_argument('--once', action='store_true', default=_env_bool('ONCE_MODE',False)); a=p.parse_args(); producer=_build(a)
    try: asyncio.run(_run(a,producer))
    finally:
        close=getattr(producer,'close',None)
        if close: close()
if __name__=='__main__': main()
