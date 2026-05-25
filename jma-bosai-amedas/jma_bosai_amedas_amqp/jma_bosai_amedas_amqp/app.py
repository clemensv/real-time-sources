
from __future__ import annotations
import argparse, os, logging
from urllib.parse import urlparse

def parse_broker_url(url: str):
    p=urlparse(url if '://' in url else f'amqp://{url}')
    tls=(p.scheme or 'amqp').lower() in ('amqps','ssl','tls')
    return p.hostname or 'localhost', p.port or (5671 if tls else 5672), p.path.lstrip('/') or '', p.username, p.password, tls

def build_parser(desc: str, default_address: str):
    parser=argparse.ArgumentParser(description=desc)
    parser.add_argument('feed_command', nargs='?', default='feed')
    parser.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL',''))
    parser.add_argument('--host', default=os.getenv('AMQP_HOST','localhost'))
    parser.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT','5672')))
    parser.add_argument('--address', default=os.getenv('AMQP_ADDRESS', default_address))
    parser.add_argument('--username', default=os.getenv('AMQP_USERNAME',''))
    parser.add_argument('--password', default=os.getenv('AMQP_PASSWORD',''))
    parser.add_argument('--auth-mode', default=os.getenv('AMQP_AUTH_MODE','password'), choices=('password','entra','sas'))
    parser.add_argument('--tls', action=argparse.BooleanOptionalAction, default=os.getenv('AMQP_TLS','false').lower() in ('1','true','yes'))
    parser.add_argument('--content-mode', default=os.getenv('AMQP_CONTENT_MODE','binary'), choices=('binary','structured'))
    parser.add_argument('--polling-interval', type=int, default=int(os.getenv('POLLING_INTERVAL','60')))
    parser.add_argument('--state-file', default=os.getenv('STATE_FILE',''))
    parser.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE','').lower() in ('1','true','yes'))
    return parser

def make_producer(cls,args):
    if args.broker_url:
        h,p,a,u,pw,t=parse_broker_url(args.broker_url); args.host=h; args.port=p; args.address=a or args.address; args.username=args.username or (u or ''); args.password=args.password or (pw or ''); args.tls=args.tls or t
    return cls(host=args.host, address=args.address, port=args.port, username=args.username or None, password=args.password or None, content_mode=args.content_mode, use_tls=args.tls)

from datetime import datetime, timezone, timedelta
from jma_bosai_amedas.jma_bosai_amedas import JmaBosaiAmedasAPI, STATION_TABLE_URL, DEFAULT_STATE_FILE, _load_state, _save_state, parse_point_station_codes
from jma_bosai_amedas_amqp_producer_data import Station, Observation
from jma_bosai_amedas_amqp_producer_amqp_producer.producer import JPJMAAmedasAmqpProducer
class MockAPI(JmaBosaiAmedasAPI):
    def fetch_station_table(self):
        from jma_bosai_amedas.jma_bosai_amedas import parse_station
        return {'44132': parse_station('44132', {'kjName':'東京','knName':'トウキョウ','enName':'Tokyo','lat':[35,41.4],'lon':[139,45.6],'alt':25,'type':'A','elems':'11111111'})}
    def fetch_latest_time(self): return datetime(2026,1,1,0,0,tzinfo=timezone(timedelta(hours=9)))
    def fetch_observation_map(self, observed_at_local): return {'44132': {'temp':[12.3,0], 'humidity':[55,0], 'precipitation10m':[0,0], 'wind':[2.1,8,0]}}
def run(api, producer, state_file, once):
    state=_load_state(state_file)
    stations=api.fetch_station_table() or {}
    for code, st in stations.items():
        d=Station(**st.to_serializer_dict()); producer.send_station(data=d,_feedurl=STATION_TABLE_URL,_station_code=code,_prefecture=d.prefecture,_event=d.event)
    observed=api.fetch_latest_time(); raw=api.fetch_observation_map(observed) if observed else None
    if observed and raw:
        for obs in api.iter_observations(observed, raw):
            d=Observation(**obs.to_serializer_dict()); producer.send_observation(data=d,_feedurl=api.observation_url(observed),_station_code=d.station_code,_prefecture=d.prefecture,_event=d.event)
    _save_state(state_file,state)
def main():
    logging.basicConfig(level=os.getenv('LOG_LEVEL','INFO').upper()); parser=build_parser('JMA Bosai AMeDAS AMQP bridge','jma-bosai-amedas'); a=parser.parse_args();
    api=MockAPI() if os.getenv('JMA_BOSAI_AMEDAS_MOCK','').lower() in ('1','true','yes') else JmaBosaiAmedasAPI(point_station_codes=parse_point_station_codes(os.getenv('POINT_STATION_CODES',''))); prod=make_producer(JPJMAAmedasAmqpProducer,a)
    try: run(api,prod,a.state_file or DEFAULT_STATE_FILE,a.once)
    finally: prod.close()
