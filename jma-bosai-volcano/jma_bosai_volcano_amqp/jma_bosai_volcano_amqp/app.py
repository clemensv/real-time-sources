
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

from jma_bosai_volcano.jma_bosai_volcano import JMABosaiVolcanoAPI, VOLCANO_LIST_URL, WARNING_URL, ERUPTION_URL, parse_volcano_catalog, parse_warning_record, parse_eruption_record
from jma_bosai_volcano_amqp_producer_data import Volcano, VolcanicWarning, VolcanicEruption
from jma_bosai_volcano_amqp_producer_amqp_producer.producer import JPJMAVolcanoAmqpProducer
class MockAPI(JMABosaiVolcanoAPI):
    def fetch_volcano_catalog(self): return parse_volcano_catalog([{'code':'101','nameJp':'桜島','nameEn':'Sakurajima','lat':31.58,'lon':130.66,'elevation':1117,'levelOperation':True}])
    def fetch_warnings(self): return [{'eventId':'v1','reportDatetime':'2026-01-01T00:00:00+09:00','volcanoInfos':[{'type':'噴火警報・予報（対象火山）','items':[{'code':'11','name':'活火山であることに留意','condition':'発表','areas':[{'code':'101'}]}]}]}]
    def fetch_eruptions(self): return [{'eventId':'e1','reportDatetime':'2026-01-01T00:05:00+09:00','volcanoInfos':[{'items':[{'type':'噴火','areas':[{'code':'101'}],'description':'噴火しました'}]}]}]
def run(api,p):
    for v in api.fetch_volcano_catalog().values():
        d=Volcano(**v.to_serializer_dict()); p.send_volcano(data=d,_feedurl=VOLCANO_LIST_URL,_volcano_code=d.volcano_code,_prefecture=d.prefecture,_event=d.event)
    for rec in api.fetch_warnings():
        for w in parse_warning_record(rec):
            d=VolcanicWarning(**w.to_serializer_dict()); p.send_volcanic_warning(data=d,_feedurl=WARNING_URL,_volcano_code=d.volcano_code,_prefecture=d.prefecture,_event=d.event)
    for rec in api.fetch_eruptions():
        for e in parse_eruption_record(rec):
            d=VolcanicEruption(**e.to_serializer_dict()); p.send_volcanic_eruption(data=d,_feedurl=ERUPTION_URL,_volcano_code=d.volcano_code,_prefecture=d.prefecture,_event=d.event)
def main():
    logging.basicConfig(level=os.getenv('LOG_LEVEL','INFO').upper()); a=build_parser('JMA Bosai Volcano AMQP bridge','jma-bosai-volcano').parse_args(); api=MockAPI() if os.getenv('JMA_BOSAI_VOLCANO_MOCK','').lower() in ('1','true','yes') else JMABosaiVolcanoAPI(); prod=make_producer(JPJMAVolcanoAmqpProducer,a)
    try: run(api,prod)
    finally: prod.close()
