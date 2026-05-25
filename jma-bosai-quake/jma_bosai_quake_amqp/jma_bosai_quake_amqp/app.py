
from __future__ import annotations
import argparse, os, logging
from urllib.parse import urlparse
def parse_broker_url(url: str):
    p=urlparse(url if '://' in url else f'amqp://{url}'); tls=(p.scheme or 'amqp').lower() in ('amqps','ssl','tls')
    return p.hostname or 'localhost', p.port or (5671 if tls else 5672), p.path.lstrip('/') or '', p.username, p.password, tls
def build_parser(desc, default_address):
    parser=argparse.ArgumentParser(description=desc); parser.add_argument('feed_command',nargs='?',default='feed'); parser.add_argument('--broker-url',default=os.getenv('AMQP_BROKER_URL','')); parser.add_argument('--host',default=os.getenv('AMQP_HOST','localhost')); parser.add_argument('--port',type=int,default=int(os.getenv('AMQP_PORT','5672'))); parser.add_argument('--address',default=os.getenv('AMQP_ADDRESS',default_address)); parser.add_argument('--username',default=os.getenv('AMQP_USERNAME','')); parser.add_argument('--password',default=os.getenv('AMQP_PASSWORD','')); parser.add_argument('--tls',action=argparse.BooleanOptionalAction,default=os.getenv('AMQP_TLS','false').lower() in ('1','true','yes')); parser.add_argument('--content-mode',default=os.getenv('AMQP_CONTENT_MODE','binary')); parser.add_argument('--state-file',default=os.getenv('STATE_FILE','')); parser.add_argument('--once',action='store_true',default=os.getenv('ONCE_MODE','').lower() in ('1','true','yes')); return parser
def make_producer(cls,args):
    if args.broker_url:
        h,p,a,u,pw,t=parse_broker_url(args.broker_url); args.host=h; args.port=p; args.address=a or args.address; args.username=args.username or (u or ''); args.password=args.password or (pw or ''); args.tls=args.tls or t
    return cls(host=args.host,address=args.address,port=args.port,username=args.username or None,password=args.password or None,content_mode=args.content_mode,use_tls=args.tls)

import requests
from jma_bosai_quake.jma_bosai_quake import JmaBosaiQuakeAPI, LIST_URL, DEFAULT_STATE_FILE, SUPPORTED_BULLETIN_TYPES, bulletin_type_from_filename
from jma_bosai_quake_amqp_producer_data import EarthquakeReport
from jma_bosai_quake_amqp_producer_amqp_producer.producer import JPJMAQuakeAmqpProducer
SAMPLE_ENTRY={"eid":"20260101000000","ser":"1","json":"20260101000100_20260101000000_VXSE53_1.json","ift":"発表","rdt":"2026-01-01T00:01:00+09:00","ctt":"20260101000100","at":"2026-01-01T00:00:00+09:00","ttl":"震源・震度情報","en_ttl":"Earthquake information","mag":"4.2","cod":"+35.0+135.5-10000/","anm":"京都府南部","en_anm":"Southern Kyoto Prefecture","maxi":"3"}
class MockAPI(JmaBosaiQuakeAPI):
    def list_reports(self): return [SAMPLE_ENTRY]
    def fetch_detail(self, filename): return {"Body":{"Comments":{"Text":"津波の心配はありません"}}}
def run(api,prod):
    for entry in reversed(api.list_reports()):
        if bulletin_type_from_filename(entry.get('json')) not in SUPPORTED_BULLETIN_TYPES: continue
        key=api.state_key(entry)
        if key in api.seen: continue
        try: detail=api.fetch_detail(entry.get('json',''))
        except requests.RequestException: detail=None
        data=api.normalize_report(entry,detail); d=EarthquakeReport(**data.to_serializer_dict())
        prod.send_earthquake_report(data=d,_feedurl=LIST_URL,_event_id=d.event_id,_serial=str(d.serial),_prefecture=d.prefecture,_magnitude_bucket=d.magnitude_bucket)
        api.mark_seen([key])
def main():
    logging.basicConfig(level=os.getenv('LOG_LEVEL','INFO').upper()); p=build_parser('JMA Bosai Quake AMQP bridge','jma-bosai-quake'); a=p.parse_args(); api=MockAPI(state_file=a.state_file or DEFAULT_STATE_FILE) if os.getenv('JMA_BOSAI_QUAKE_MOCK','').lower() in ('1','true','yes') else JmaBosaiQuakeAPI(state_file=a.state_file or DEFAULT_STATE_FILE); prod=make_producer(JPJMAQuakeAmqpProducer,a)
    try: run(api,prod)
    finally: prod.close()

