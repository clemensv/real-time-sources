from __future__ import annotations

import argparse
import logging
import os
import time
from typing import Any, Dict
from urllib.parse import urlparse

from kiwis_core import KiWISClient, load_endpoints, load_state, save_state
from kiwis_core.core import normalize_station, normalize_timeseries, normalize_value
from kiwis_amqp_producer_data import Station, Timeseries, TimeseriesValue
from kiwis_amqp_producer_amqp_producer.producer import OrgKiwisStationAmqpProducer, OrgKiwisTimeseriesAmqpProducer

logger = logging.getLogger(__name__)

def _parse_broker(url: str) -> Dict[str, Any]:
    parsed = urlparse(url if '://' in url else 'amqp://' + url)
    return {'host': parsed.hostname or 'localhost', 'port': parsed.port or (5671 if parsed.scheme == 'amqps' else 5672), 'address': (parsed.path or '/kiwis').lstrip('/'), 'use_tls': parsed.scheme == 'amqps', 'username': parsed.username, 'password': parsed.password}

def _emit_cycle(station_producer: OrgKiwisStationAmqpProducer, ts_producer: OrgKiwisTimeseriesAmqpProducer, endpoint, client: KiWISClient, state: Dict[str, str]) -> Dict[str, str]:
    for raw in client.stations():
        data = normalize_station(endpoint, raw)
        if data['station_id']:
            station_producer.send_station(data=Station(**data), _base_url=endpoint.base_url, _kiwis_id=endpoint.kiwis_id, _station_id=data['station_id'])
    metadata = client.timeseries(); meta_by_id: Dict[str, Dict[str, Any]] = {}
    for raw in metadata:
        data = normalize_timeseries(endpoint, raw)
        if data['ts_id']:
            meta_by_id[data['ts_id']] = raw
            ts_producer.send_timeseries(data=Timeseries(**data), _base_url=endpoint.base_url, _kiwis_id=endpoint.kiwis_id, _ts_id=data['ts_id'])
    for ts_id, rows in client.values(list(meta_by_id)).items():
        meta = meta_by_id.get(ts_id)
        if not meta: continue
        for row in rows:
            data = normalize_value(endpoint, meta, row)
            key = f"{endpoint.kiwis_id}/{ts_id}/{data['timestamp'].isoformat()}"; digest=f"{data.get('value')}|{data.get('quality_code')}"
            if state.get(key) == digest: continue
            ts_producer.send_timeseries_value(data=TimeseriesValue(**data), _base_url=endpoint.base_url, _kiwis_id=endpoint.kiwis_id, _ts_id=ts_id)
            state[key] = digest
    return state

def feed(args: argparse.Namespace) -> None:
    settings = _parse_broker(args.broker_url)
    settings.update({'host': args.host or settings['host'], 'port': args.port or settings['port'], 'address': args.address or settings['address'], 'username': args.username or settings['username'], 'password': args.password or settings['password'], 'use_tls': args.tls or settings['use_tls']})
    if args.auth_mode == 'entra':
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential()
        settings.update({'credential': credential, 'entra_audience': args.entra_audience, 'username': None, 'password': None, 'use_tls': True})
    station_producer = OrgKiwisStationAmqpProducer(content_mode=args.content_mode, **settings)
    ts_producer = OrgKiwisTimeseriesAmqpProducer(content_mode=args.content_mode, **settings)
    state = load_state(args.state_file)
    while True:
        pending = dict(state)
        for endpoint in load_endpoints(args.kiwis_endpoints, mock=args.mock):
            _emit_cycle(station_producer, ts_producer, endpoint, KiWISClient(endpoint, mock=args.mock), pending)
        state = pending; save_state(args.state_file, state)
        if args.once: break
        time.sleep(args.polling_interval)

def _parser() -> argparse.ArgumentParser:
    parser=argparse.ArgumentParser(description='Generalized KiWIS → AMQP feeder'); sub=parser.add_subparsers(dest='command'); p=sub.add_parser('feed')
    p.add_argument('--kiwis-endpoints', default=os.getenv('KIWIS_ENDPOINTS','')); p.add_argument('--mock', action='store_true', default=os.getenv('KIWIS_MOCK','').lower()=='true'); p.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE','').lower()=='true')
    p.add_argument('--state-file', default=os.getenv('KIWIS_STATE_FILE', os.getenv('STATE_FILE',''))); p.add_argument('-i','--polling-interval', type=int, default=int(os.getenv('POLLING_INTERVAL','300')))
    p.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL','amqp://localhost:5672/kiwis')); p.add_argument('--host', default=os.getenv('AMQP_HOST')); p.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT','0')) or None); p.add_argument('--address', default=os.getenv('AMQP_ADDRESS'))
    p.add_argument('--username', default=os.getenv('AMQP_USERNAME')); p.add_argument('--password', default=os.getenv('AMQP_PASSWORD')); p.add_argument('--tls', action='store_true', default=os.getenv('AMQP_TLS','').lower()=='true')
    p.add_argument('--auth-mode', choices=['password','entra'], default=os.getenv('AMQP_AUTH_MODE','password').lower())
    p.add_argument('--entra-audience', default=os.getenv('AMQP_ENTRA_AUDIENCE','https://servicebus.azure.net/.default'))
    p.add_argument('--entra-client-id', default=os.getenv('AMQP_ENTRA_CLIENT_ID'))
    p.add_argument('--content-mode', choices=['binary','structured'], default=os.getenv('AMQP_CONTENT_MODE','binary'))
    return parser

def main() -> None:
    logging.basicConfig(level=os.getenv('LOG_LEVEL','INFO')); parser=_parser(); args=parser.parse_args();
    if args.command != 'feed': args=parser.parse_args(['feed'])
    feed(args)
