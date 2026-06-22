
from __future__ import annotations
import argparse, logging, os, time
from urllib.parse import urlparse
import erddap_amqp_producer_data as data_pkg
from erddap_core import ErddapClient, load_state, parse_bool, parse_sources, save_state
from erddap_amqp_producer_amqp_producer.producer import OrgErddapAmqpDatasetProducer, OrgErddapAmqpStationProducer
from ._common import _dataset_obj, _observation_obj, _station_obj, build_parser, main_dispatch
logger=logging.getLogger(__name__)
def _parts(args):
    if args.amqp_broker_url:
        u=urlparse(args.amqp_broker_url); return u.hostname or args.amqp_host, u.port or args.amqp_port, (u.path or '/erddap').lstrip('/'), u.scheme=='amqps', u.username or args.amqp_username, u.password or args.amqp_password
    return args.amqp_host,args.amqp_port,args.amqp_address,parse_bool(args.amqp_tls,False),args.amqp_username,args.amqp_password
def _producer(cls, host, port, address, tls, user, pwd, args):
    if args.amqp_auth_mode=='entra':
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        cred=ManagedIdentityCredential(client_id=args.amqp_entra_client_id) if args.amqp_entra_client_id else DefaultAzureCredential()
        return cls(host=host, port=port, address=address, credential=cred, entra_audience=args.amqp_entra_audience, use_tls=True, content_mode="binary")
    return cls(host=host, port=port, address=address, username=user, password=pwd, use_tls=tls, content_mode="binary")
def feed(args: argparse.Namespace) -> None:
    sources=parse_sources(args.erddap_sources, mock=args.mock, sources_file=args.erddap_sources_file, selector=args.erddap_select); host,port,address,tls,user,pwd=_parts(args)
    ds=_producer(OrgErddapAmqpDatasetProducer,host,port,address,tls,user,pwd,args); st=_producer(OrgErddapAmqpStationProducer,host,port,address,tls,user,pwd,args)
    client=ErddapClient(); state=load_state(args.state_file); last_ref=0.0
    if args.mock: args.once=True
    while True:
        start=time.time(); pending={}
        for src in sources:
            snap=client.fetch_dataset(src,state,mock=args.mock)
            if last_ref==0.0 or start-last_ref>=args.reference_refresh_interval:
                ds.send_dataset_metadata(data=_dataset_obj(data_pkg,snap.dataset), _base_url=src.base_url, _erddap_id=src.erddap_id, _dataset_id=src.dataset_id)
                st.send_station_metadata(data=_station_obj(data_pkg,snap.station), _base_url=src.base_url, _erddap_id=src.erddap_id, _dataset_id=src.dataset_id, _station_id=snap.station['station_id'])
            for obs in snap.observations:
                st.send_observation(data=_observation_obj(data_pkg,obs), _base_url=src.base_url, _erddap_id=src.erddap_id, _dataset_id=src.dataset_id, _station_id=obs['station_id'], _time=obs['time'])
            pending.update(snap.state_updates)
        state.update(pending); save_state(args.state_file,state); last_ref=start if last_ref==0.0 or start-last_ref>=args.reference_refresh_interval else last_ref
        if args.once: return
        time.sleep(max(1,args.polling_interval-int(time.time()-start)))
def build_app_parser():
    p=build_parser('ERDDAP tabledap -> AMQP 1.0 CloudEvents feeder'); f=p._subparsers._group_actions[0].choices['feed']
    f.add_argument('--amqp-broker-url', default=os.getenv('AMQP_BROKER_URL'))
    f.add_argument('--amqp-host', default=os.getenv('AMQP_HOST','localhost'))
    f.add_argument('--amqp-port', type=int, default=int(os.getenv('AMQP_PORT','5672')))
    f.add_argument('--amqp-address', default=os.getenv('AMQP_ADDRESS','erddap'))
    f.add_argument('--amqp-tls', default=os.getenv('AMQP_TLS','false'))
    f.add_argument('--amqp-username', default=os.getenv('AMQP_USERNAME'))
    f.add_argument('--amqp-password', default=os.getenv('AMQP_PASSWORD'))
    f.add_argument('--amqp-auth-mode', choices=['password','entra'], default=os.getenv('AMQP_AUTH_MODE','password'))
    f.add_argument('--amqp-entra-audience', default=os.getenv('AMQP_ENTRA_AUDIENCE','https://servicebus.azure.net/.default'))
    f.add_argument('--amqp-entra-client-id', default=os.getenv('AMQP_ENTRA_CLIENT_ID'))
    return p
def main(): main_dispatch(build_app_parser(), feed)
if __name__=='__main__': main()

