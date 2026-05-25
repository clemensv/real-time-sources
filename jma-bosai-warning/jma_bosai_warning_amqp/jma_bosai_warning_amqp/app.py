
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

from jma_bosai_warning.jma_bosai_warning import AREA_CATALOG_URL, WARNING_URL_TEMPLATE, TSUNAMI_LIST_URL, TSUNAMI_DETAIL_BASE, WARNING_OFFICE_CODES, BridgeState, JmaBosaiWarningAPI, parse_weather_warning_payload, parse_tsunami_alert, _load_state, _save_state
from jma_bosai_warning_amqp_producer_data import Office, WeatherWarning, TsunamiAlert
from jma_bosai_warning_amqp_producer_amqp_producer.producer import JPJMAWarningAmqpProducer
class MockAPI(JmaBosaiWarningAPI):
    def refresh_area_catalog(self): self.area_catalog={'offices':{'130000':{'name':'東京都','enName':'Tokyo','parent':None}}}; self.area_names={'130000':'東京都','130010':'東京地方'}; return True
    def fetch_warning_payload(self, office_code): return {'reportDatetime':'2026-01-01T00:00:00+09:00','timeSeries':[{'timeDefines':['2026-01-01T00:00:00+09:00'],'areas':[{'code':'130010','name':'東京地方','warnings':[{'code':'03','status':'警報'}]}]}]}
    def fetch_tsunami_list(self): return [{'eid':'20260101000000','ser':'1','json':'VTSE41.json','ift':'発表','rdt':'2026-01-01T00:01:00+09:00','ttl':'津波警報・注意報・予報'}]
    def fetch_tsunami_detail(self, filename): return {'Body': {'Tsunami': {'Forecast': [{'Area': {'Code':'100','Name':'東京湾内湾'}, 'Category':'津波警報'}]}}}
def run(api,p,state_file):
    api.refresh_area_catalog(); st=BridgeState.from_dict(_load_state(state_file));
    for r in api.office_records(): p.send_office(data=Office(**r),_feedurl=AREA_CATALOG_URL,_office_code=r['office_code'],_area_code=r['area_code'],_prefecture=r['prefecture'],_severity=r['severity'],_event=r['event'])
    for r in parse_weather_warning_payload('130000', api.fetch_warning_payload('130000'), api.area_names): p.send_weather_warning(data=WeatherWarning(**r),_feedurl=WARNING_URL_TEMPLATE.format(office_code='130000'),_office_code=r['office_code'],_area_code=r['area_code'],_prefecture=r['prefecture'],_severity=r['severity'],_event=r['event'])
    for e in api.fetch_tsunami_list():
        r=parse_tsunami_alert(e, api.fetch_tsunami_detail(e.get('json',''))); p.send_tsunami_alert(data=TsunamiAlert(**r),_feedurl=r['detail_url'] or TSUNAMI_LIST_URL,_event_id=r['event_id'],_serial=str(r['serial']),_prefecture=r['prefecture'],_severity=r['severity'])
    _save_state(state_file, st.as_dict())
def main():
    logging.basicConfig(level=os.getenv('LOG_LEVEL','INFO').upper()); a=build_parser('JMA Bosai Warning AMQP bridge','jma-bosai-warning').parse_args(); api=MockAPI() if os.getenv('JMA_BOSAI_WARNING_MOCK','').lower() in ('1','true','yes') else JmaBosaiWarningAPI(); prod=make_producer(JPJMAWarningAmqpProducer,a)
    try: run(api,prod,a.state_file or './state/jma-bosai-warning-amqp.json')
    finally: prod.close()
