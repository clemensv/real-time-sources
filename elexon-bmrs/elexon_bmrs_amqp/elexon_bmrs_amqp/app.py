"""AMQP companion feeder for elexon-bmrs. Publishes mock/sample CloudEvents for Docker E2E and auth-blocked upstreams."""
from __future__ import annotations
import argparse, inspect, json, os, pathlib, re
from datetime import datetime, timezone
from urllib.parse import urlparse
from proton import symbol
from elexon_bmrs_amqp_producer_amqp_producer import producer as producer_mod
import elexon_bmrs_amqp_producer_data as data_mod
MANIFEST = pathlib.Path(os.getenv('SOURCE_MANIFEST', '/app/xreg/elexon_bmrs.xreg.json'))
def _val(name, typ):
    n=name.lower()
    if 'date' in n and 'time' not in n: return '2026-01-01'
    if 'time' in n or typ == 'datetime': return datetime(2026,1,1,tzinfo=timezone.utc)
    if 'country' in n: return 'gb' if 'elexon-bmrs'=='elexon-bmrs' else ('jp' if 'elexon-bmrs'=='tepco-denkiyoho' else 'dk' if 'elexon-bmrs'=='energidataservice-dk' else 'de' if 'elexon-bmrs'=='energy-charts' else 'nl')
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
    data={}
    for name,p in schema.get('properties',{}).items():
        typ=p.get('type','string')
        if isinstance(typ,list): typ=next((t for t in typ if t!='null'),'string')
        data[name]=[] if typ=='array' else {} if typ in ('object',) or isinstance(typ,dict) else _val(name,typ)
    return data
def _iter_events():
    m=json.loads(MANIFEST.read_text(encoding='utf-8')); schemas={}
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
        if not g.endswith('.amqp'): continue
        for mid,msg in gv.get('messages',{}).items():
            base=msg.get('basemessageurl','').split('/messages/')[-1]; yield (msg.get('name') or mid.split('.')[-1]), _sample(schemas[base])
def _norm(s): return re.sub(r'[^a-z0-9]+','_',s.lower()).strip('_')
def _compact(s): return re.sub(r'[^a-z0-9]+','',s.lower())
def _patch(p):
    def stamp(msg):
        props=dict(getattr(msg,'properties',None) or {}); subj=props.get('cloudEvents:subject') or getattr(msg,'subject',None)
        if subj:
            ann=dict(getattr(msg,'annotations',None) or {}); ann[symbol('x-opt-partition-key')]=subj; msg.annotations=ann
        return msg
    if getattr(p,'_sender',None) is not None:
        old=p._sender.send; p._sender.send=lambda msg,*a,**kw: old(stamp(msg),*a,**kw)
    return p
def _parse(url):
    p=urlparse(url if '://' in url else 'amqp://'+url); tls=(p.scheme or 'amqp').lower() in ('amqps','ssl','tls'); return p.hostname or 'localhost', p.port or (5671 if tls else 5672), tls, p.username, p.password, (p.path or '').lstrip('/') or None
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('feed', nargs='?', default='feed'); ap.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL')); ap.add_argument('--host', default=os.getenv('AMQP_HOST')); ap.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT','0')) or None); ap.add_argument('--address', default=os.getenv('AMQP_ADDRESS','elexon-bmrs')); ap.add_argument('--username', default=os.getenv('AMQP_USERNAME')); ap.add_argument('--password', default=os.getenv('AMQP_PASSWORD')); ap.add_argument('--tls', action='store_true', default=os.getenv('AMQP_TLS','').lower() in ('1','true','yes')); ap.add_argument('--auth-mode', default=os.getenv('AMQP_AUTH_MODE','password')); args=ap.parse_args()
    address=args.address
    if args.broker_url: host,port,tls,user,pwd,path=_parse(args.broker_url); address=path or address; username=args.username or user; password=args.password or pwd
    else: host=args.host or 'localhost'; tls=args.tls; port=args.port or (5671 if tls else 5672); username=args.username; password=args.password
    classes=[v for v in vars(producer_mod).values() if isinstance(v,type) and v.__name__.endswith('Producer')]
    producers=[_patch(cls(host=host,address=address,port=port,username=username,password=password,content_mode='binary',use_tls=tls)) for cls in classes]
    try:
        for sh,payload in _iter_events():
            data=getattr(data_mod, sh)(**payload); values=dict(payload)
            for k,v in list(values.items()):
                if isinstance(v, datetime): values[k]=v.isoformat().replace('+00:00','Z')
            sent=False
            for p in producers:
                for n in dir(p):
                    if n.startswith('send_') and _compact(sh) in _compact(n):
                        meth=getattr(p,n); kwargs={}
                        for pname in inspect.signature(meth).parameters:
                            if pname in ('content_type',):
                                continue
                            if pname=='data': kwargs[pname]=data
                            elif pname in values: kwargs[pname]=values[pname]
                            elif pname.startswith('_') and pname[1:] in values: kwargs[pname]=values[pname[1:]]
                            elif pname.startswith('_'): kwargs[pname]=_val(pname[1:],'string')
                            else: kwargs[pname]=_val(pname,'string')
                        meth(**kwargs); sent=True; break
                if sent: break
            if not sent: raise RuntimeError(f'No AMQP send method for {sh}')
    finally:
        for p in producers:
            try: p.close()
            except Exception: pass
if __name__=='__main__': main()
