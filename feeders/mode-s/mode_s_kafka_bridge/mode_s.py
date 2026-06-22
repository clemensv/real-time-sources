import argparse
import asyncio
import logging
import os
import sys
from typing import Dict

from confluent_kafka import Producer
from mode_s_core import ModeSBridge
from mode_s_producer_data import Record as KafkaRecord
from mode_s_producer_kafka_producer.producer import ModeSKafkaEventProducer

logger = logging.getLogger(__name__)
logger.handlers = []
logger.setLevel(logging.DEBUG if sys.gettrace() else logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(stream_handler)
logger.propagate = False


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    config_dict = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                endpoint = part.split('=')[1].replace('sb://', '').rstrip('/')
                if ':' not in endpoint:
                    endpoint += ':9093'
                config_dict['bootstrap.servers'] = endpoint
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=')[1]
            elif 'SharedAccessKeyName' in part:
                config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part:
                config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as exc:
        raise ValueError('Invalid connection string format') from exc
    if 'sasl.username' in config_dict:
        config_dict['security.protocol'] = 'SASL_SSL'
        config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict


class ModeSKafkaClientAdapter:
    def __init__(self, producer: ModeSKafkaEventProducer):
        self._producer = producer

    @staticmethod
    def _data(rec) -> KafkaRecord:
        return KafkaRecord(**rec.__dict__)

    async def publish_adsb(self, *, feedurl, icao24, receiver_id, data):
        self._producer.send_mode_s_kafka_adsb(_feedurl=feedurl, _icao24=icao24, _receiver_id=receiver_id, data=self._data(data), content_type='application/json', flush_producer=False)

    async def publish_altitude_reply(self, *, feedurl, icao24, receiver_id, data):
        self._producer.send_mode_s_kafka_altitude_reply(_feedurl=feedurl, _icao24=icao24, _receiver_id=receiver_id, data=self._data(data), content_type='application/json', flush_producer=False)

    async def publish_identity_reply(self, *, feedurl, icao24, receiver_id, data):
        self._producer.send_mode_s_kafka_identity_reply(_feedurl=feedurl, _icao24=icao24, _receiver_id=receiver_id, data=self._data(data), content_type='application/json', flush_producer=False)

    async def publish_acquisition_reply(self, *, feedurl, icao24, receiver_id, data):
        self._producer.send_mode_s_kafka_acquisition_reply(_feedurl=feedurl, _icao24=icao24, _receiver_id=receiver_id, data=self._data(data), content_type='application/json', flush_producer=False)

    async def publish_comm_baltitude(self, *, feedurl, icao24, receiver_id, data):
        self._producer.send_mode_s_kafka_comm_baltitude(_feedurl=feedurl, _icao24=icao24, _receiver_id=receiver_id, data=self._data(data), content_type='application/json', flush_producer=False)

    async def publish_comm_bidentity(self, *, feedurl, icao24, receiver_id, data):
        self._producer.send_mode_s_kafka_comm_bidentity(_feedurl=feedurl, _icao24=icao24, _receiver_id=receiver_id, data=self._data(data), content_type='application/json', flush_producer=False)


async def run():
    parser = argparse.ArgumentParser(description='Mode-S ADS-B Client')
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')
    feed_parser = subparsers.add_parser('feed', help='Poll ADS-B data and feed it to Kafka')
    feed_parser.add_argument('--host', type=str, default=os.environ.get('DUMP1090_HOST'))
    feed_parser.add_argument('--port', type=int, default=os.environ.get('DUMP1090_PORT'))
    feed_parser.add_argument('--ref-lat', type=float, default=os.environ.get('REF_LAT'))
    feed_parser.add_argument('--ref-lon', type=float, default=os.environ.get('REF_LON'))
    feed_parser.add_argument('--stationid', type=str, default=os.environ.get('STATIONID', 'station1'))
    feed_parser.add_argument('--feedurl', type=str, default=os.environ.get('MODE_S_FEEDURL'))
    feed_parser.add_argument('--connection-string', type=str, default=os.environ.get('CONNECTION_STRING'))
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str, default=os.environ.get('KAFKA_BOOTSTRAP_SERVERS'))
    feed_parser.add_argument('--kafka-topic', type=str, default=os.environ.get('KAFKA_TOPIC'))
    feed_parser.add_argument('--sasl-username', type=str, default=os.environ.get('SASL_USERNAME'))
    feed_parser.add_argument('--sasl-password', type=str, default=os.environ.get('SASL_PASSWORD'))
    feed_parser.add_argument('--content-mode', type=str, choices=['structured', 'binary'], default='structured')
    args = parser.parse_args()
    if args.subcommand != 'feed':
        parser.print_help()
        return
    if not args.host or not args.port:
        print('Error: Dump1090 host/port are required')
        return
    if args.ref_lat is None or args.ref_lon is None:
        print('Error: REF_LAT and REF_LON are required')
        return
    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = config_params.get('bootstrap.servers')
        kafka_topic = config_params.get('kafka_topic')
        sasl_username = config_params.get('sasl.username')
        sasl_password = config_params.get('sasl.password')
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password
    if not kafka_bootstrap_servers or not kafka_topic:
        print('Error: Kafka bootstrap servers and topic are required')
        return
    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
    kafka_config = {'bootstrap.servers': kafka_bootstrap_servers}
    if sasl_username and sasl_password:
        kafka_config.update({'sasl.mechanisms': 'PLAIN', 'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT', 'sasl.username': sasl_username, 'sasl.password': sasl_password})
    elif tls_enabled:
        kafka_config['security.protocol'] = 'SSL'
    kafka_producer = Producer(kafka_config)
    producer = ModeSKafkaEventProducer(kafka_producer, topic=kafka_topic, content_mode=args.content_mode)
    feedurl = args.feedurl or f'dump1090://{args.host}:{args.port}'
    bridge = ModeSBridge(ModeSKafkaClientAdapter(producer), feedurl=feedurl, receiver_id=args.stationid, ref_lat=float(args.ref_lat), ref_lon=float(args.ref_lon))
    try:
        await bridge.run_from_dump1090(args.host, int(args.port))
    finally:
        kafka_producer.flush()


def main():
    asyncio.run(run())


if __name__ == '__main__':
    main()
