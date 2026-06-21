
from __future__ import annotations
import argparse, logging, os, time
from confluent_kafka import Producer
import erddap_producer_data as data_pkg
from erddap_core import ErddapClient, build_kafka_config, load_state, parse_bool, parse_kafka_connection_string, parse_sources, save_state
from erddap_producer_kafka_producer.producer import OrgErddapKafkaDatasetEventProducer, OrgErddapKafkaStationEventProducer
from ._common import _dataset_obj, _observation_obj, _station_obj, build_parser, main_dispatch
logger = logging.getLogger(__name__)

def feed(args: argparse.Namespace) -> None:
    sources = parse_sources(args.erddap_sources)
    if args.connection_string:
        cfg = parse_kafka_connection_string(args.connection_string); bootstrap = cfg.pop('bootstrap.servers', None); topic = cfg.pop('kafka_topic', None) or args.kafka_topic; sasl_username = cfg.get('sasl.username'); sasl_password = cfg.get('sasl.password')
    else:
        bootstrap=args.kafka_bootstrap_servers; topic=args.kafka_topic; sasl_username=args.sasl_username; sasl_password=args.sasl_password
    if not bootstrap: raise SystemExit('Kafka bootstrap servers required')
    producer = Producer(build_kafka_config(bootstrap, sasl_username, sasl_password, parse_bool(os.getenv('KAFKA_ENABLE_TLS'), True)))
    dataset_producer = OrgErddapKafkaDatasetEventProducer(producer, topic)
    station_producer = OrgErddapKafkaStationEventProducer(producer, topic)
    client = ErddapClient(); state = load_state(args.state_file); last_ref = 0.0
    if args.mock: args.once = True
    while True:
        start=time.time(); pending={}
        for src in sources:
            try:
                snap=client.fetch_dataset(src, state, mock=args.mock)
                if last_ref == 0.0 or start-last_ref >= args.reference_refresh_interval:
                    dataset_producer.send_org_erddap_kafka_dataset_metadata(_base_url=src.base_url,_erddap_id=src.erddap_id,_dataset_id=src.dataset_id,data=_dataset_obj(data_pkg,snap.dataset),flush_producer=False)
                    station_producer.send_org_erddap_kafka_station_metadata(_base_url=src.base_url,_erddap_id=src.erddap_id,_dataset_id=src.dataset_id,_station_id=snap.station['station_id'],data=_station_obj(data_pkg,snap.station),flush_producer=False)
                for obs in snap.observations:
                    station_producer.send_org_erddap_kafka_observation(_base_url=src.base_url,_erddap_id=src.erddap_id,_dataset_id=src.dataset_id,_station_id=obs['station_id'],data=_observation_obj(data_pkg,obs),_time=obs['time'],flush_producer=False)
                pending.update(snap.state_updates)
            except Exception as exc:
                logger.warning('ERDDAP slice failed for %s/%s: %s', src.erddap_id, src.dataset_id, exc)
        remaining=producer.flush(120)
        if remaining: raise RuntimeError(f'Kafka flush left {remaining} message(s) unsent')
        state.update(pending); save_state(args.state_file, state); last_ref=start if last_ref == 0.0 or start-last_ref >= args.reference_refresh_interval else last_ref
        if args.once: return
        time.sleep(max(1, args.polling_interval-int(time.time()-start)))

def build_app_parser():
    p=build_parser('ERDDAP tabledap -> Kafka CloudEvents feeder')
    f=p._subparsers._group_actions[0].choices['feed']
    f.add_argument('--kafka-bootstrap-servers', default=os.getenv('KAFKA_BOOTSTRAP_SERVERS'))
    f.add_argument('--kafka-topic', default=os.getenv('KAFKA_TOPIC','erddap'))
    f.add_argument('--sasl-username', default=os.getenv('SASL_USERNAME'))
    f.add_argument('--sasl-password', default=os.getenv('SASL_PASSWORD'))
    f.add_argument('--connection-string', default=os.getenv('CONNECTION_STRING'))
    return p

def main(): main_dispatch(build_app_parser(), feed)
if __name__ == '__main__': main()
