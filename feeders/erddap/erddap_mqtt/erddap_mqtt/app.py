
from __future__ import annotations
import argparse, asyncio, logging, os, time
import paho.mqtt.client as mqtt
import erddap_mqtt_producer_data as data_pkg
from erddap_core import ErddapClient, load_state, parse_bool, parse_sources, save_state
from erddap_mqtt_producer_mqtt_client.client import OrgErddapMqttDatasetMqttClient, OrgErddapMqttStationMqttClient
from ._common import _dataset_obj, _observation_obj, _station_obj, build_parser, main_dispatch
logger=logging.getLogger(__name__)

def _split_broker(url: str):
    host, _, port = url.partition(':'); return host, int(port or '1883')
async def _run(args):
    sources=parse_sources(args.erddap_sources, mock=args.mock, sources_file=args.erddap_sources_file, selector=args.erddap_select); host,port=_split_broker(args.mqtt_broker_url)
    c1=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=args.mqtt_client_id+'-dataset', protocol=mqtt.MQTTv5); c2=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=args.mqtt_client_id+'-station', protocol=mqtt.MQTTv5)
    if args.mqtt_username: c1.username_pw_set(args.mqtt_username,args.mqtt_password); c2.username_pw_set(args.mqtt_username,args.mqtt_password)
    if parse_bool(args.mqtt_enable_tls, False): c1.tls_set(ca_certs=args.mqtt_ca_file or None); c2.tls_set(ca_certs=args.mqtt_ca_file or None)
    ds=OrgErddapMqttDatasetMqttClient(c1, content_mode='binary'); st=OrgErddapMqttStationMqttClient(c2, content_mode='binary')
    await ds.connect(host,port); await st.connect(host,port)
    client=ErddapClient(); state=load_state(args.state_file); last_ref=0.0
    if args.mock: args.once=True
    try:
      while True:
        start=time.time(); pending={}
        for src in sources:
          snap=client.fetch_dataset(src,state,mock=args.mock)
          if last_ref==0.0 or start-last_ref>=args.reference_refresh_interval:
            await ds.publish_org_erddap_mqtt_dataset_metadata(src.base_url,src.erddap_id,src.dataset_id,_dataset_obj(data_pkg,snap.dataset))
            await st.publish_org_erddap_mqtt_station_metadata(src.base_url,src.erddap_id,src.dataset_id,snap.station['station_id'],_station_obj(data_pkg,snap.station))
          for obs in snap.observations:
            await st.publish_org_erddap_mqtt_observation(src.base_url,src.erddap_id,src.dataset_id,obs['station_id'],_observation_obj(data_pkg,obs),_time=obs['time'])
          pending.update(snap.state_updates)
        state.update(pending); save_state(args.state_file,state); last_ref=start if last_ref==0.0 or start-last_ref>=args.reference_refresh_interval else last_ref
        if args.once: return
        await asyncio.sleep(max(1,args.polling_interval-int(time.time()-start)))
    finally:
      await ds.disconnect(); await st.disconnect()
def feed(args: argparse.Namespace) -> None: asyncio.run(_run(args))
def build_app_parser():
    p=build_parser('ERDDAP tabledap -> MQTT CloudEvents feeder'); f=p._subparsers._group_actions[0].choices['feed']
    f.add_argument('--mqtt-broker-url', default=os.getenv('MQTT_BROKER_URL','localhost:1883'))
    f.add_argument('--mqtt-enable-tls', default=os.getenv('MQTT_ENABLE_TLS','false'))
    f.add_argument('--mqtt-username', default=os.getenv('MQTT_USERNAME'))
    f.add_argument('--mqtt-password', default=os.getenv('MQTT_PASSWORD'))
    f.add_argument('--mqtt-ca-file', default=os.getenv('MQTT_CA_FILE'))
    f.add_argument('--mqtt-client-id', default=os.getenv('MQTT_CLIENT_ID','erddap'))
    return p
def main(): main_dispatch(build_app_parser(), feed)
if __name__=='__main__': main()

