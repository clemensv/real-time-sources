from __future__ import annotations

import argparse
import asyncio
import logging
import os
import json
from urllib.parse import urlparse
from typing import Any, Dict, Optional

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from kiwis_core import KiWISClient, load_endpoints, load_state, save_state
from kiwis_core.core import normalize_station, normalize_timeseries, normalize_value
from kiwis_mqtt_producer_data import Station, Timeseries, TimeseriesValue
from kiwis_mqtt_producer_mqtt_client.client import OrgKiwisStationMqttMqttClient, OrgKiwisTimeseriesMqttMqttClient

logger = logging.getLogger(__name__)

def _broker(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if '://' in url else 'mqtt://' + url)
    return parsed.hostname or 'localhost', parsed.port or (8883 if parsed.scheme == 'mqtts' else 1883), parsed.scheme == 'mqtts'

def _imds_token(audience: str, client_id: Optional[str]) -> str:
    import urllib.parse, urllib.request
    params = {'api-version': '2018-02-01', 'resource': audience}
    if client_id:
        params['client_id'] = client_id
    req = urllib.request.Request('http://169.254.169.254/metadata/identity/oauth2/token?' + urllib.parse.urlencode(params), headers={'Metadata': 'true'})
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.loads(response.read().decode('utf-8'))
    return str(payload.get('access_token') or payload.get('accessToken') or '')

async def _emit_cycle(station_client: OrgKiwisStationMqttMqttClient, ts_client: OrgKiwisTimeseriesMqttMqttClient, endpoint, client: KiWISClient, state: Dict[str, str]) -> Dict[str, str]:
    for raw in client.stations():
        data = normalize_station(endpoint, raw)
        if data['station_id']:
            await station_client.publish_org_kiwis_station_mqtt_station(base_url=endpoint.base_url, kiwis_id=endpoint.kiwis_id, station_id=data['station_id'], data=Station(**data))
    metadata = client.timeseries(); meta_by_id: Dict[str, Dict[str, Any]] = {}
    for raw in metadata:
        data = normalize_timeseries(endpoint, raw)
        if data['ts_id']:
            meta_by_id[data['ts_id']] = raw
            await ts_client.publish_org_kiwis_timeseries_mqtt_timeseries(base_url=endpoint.base_url, kiwis_id=endpoint.kiwis_id, ts_id=data['ts_id'], data=Timeseries(**data))
    for ts_id, rows in client.values(list(meta_by_id)).items():
        meta = meta_by_id.get(ts_id)
        if not meta: continue
        for row in rows:
            data = normalize_value(endpoint, meta, row)
            key = f"{endpoint.kiwis_id}/{ts_id}/{data['timestamp'].isoformat()}"; digest=f"{data.get('value')}|{data.get('quality_code')}"
            if state.get(key) == digest: continue
            await ts_client.publish_org_kiwis_timeseries_mqtt_timeseries_value(base_url=endpoint.base_url, kiwis_id=endpoint.kiwis_id, ts_id=ts_id, data=TimeseriesValue(**data))
            state[key] = digest
    return state

async def feed(args: argparse.Namespace) -> None:
    client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5, client_id=args.client_id or "kiwis-mqtt")
    connect_props = None
    if args.auth_mode == 'entra':
        from paho.mqtt.packettypes import PacketTypes
        from paho.mqtt.properties import Properties
        token = _imds_token(args.entra_audience, args.entra_client_id)
        client.username_pw_set(args.client_id or args.username or 'kiwis-mqtt', token)
        connect_props = Properties(PacketTypes.CONNECT)
        connect_props.AuthenticationMethod = 'OAUTH2-JWT'
        connect_props.AuthenticationData = token.encode('utf-8')
    elif args.username or args.password:
        client.username_pw_set(args.username, args.password)
    host, port, tls = _broker(args.broker_url)
    if args.enable_tls or tls:
        client.tls_set()
    client.connect(host, port, 60, clean_start=True, properties=connect_props); client.loop_start()
    station_client = OrgKiwisStationMqttMqttClient(client, content_mode='binary')
    ts_client = OrgKiwisTimeseriesMqttMqttClient(client, content_mode='binary')
    state = load_state(args.state_file)
    try:
        while True:
            pending = dict(state)
            for endpoint in load_endpoints(args.kiwis_endpoints, mock=args.mock):
                await _emit_cycle(station_client, ts_client, endpoint, KiWISClient(endpoint, mock=args.mock), pending)
            state = pending; save_state(args.state_file, state)
            if args.once: break
            await asyncio.sleep(args.polling_interval)
    finally:
        client.loop_stop(); client.disconnect()

def _parser() -> argparse.ArgumentParser:
    parser=argparse.ArgumentParser(description='Generalized KiWIS → MQTT feeder'); sub=parser.add_subparsers(dest='command'); p=sub.add_parser('feed')
    p.add_argument('--kiwis-endpoints', default=os.getenv('KIWIS_ENDPOINTS','')); p.add_argument('--mock', action='store_true', default=os.getenv('KIWIS_MOCK','').lower()=='true'); p.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE','').lower()=='true')
    p.add_argument('--state-file', default=os.getenv('KIWIS_STATE_FILE', os.getenv('STATE_FILE',''))); p.add_argument('-i','--polling-interval', type=int, default=int(os.getenv('POLLING_INTERVAL','300')))
    p.add_argument('--broker-url', default=os.getenv('MQTT_BROKER_URL','localhost:1883')); p.add_argument('--username', default=os.getenv('MQTT_USERNAME')); p.add_argument('--password', default=os.getenv('MQTT_PASSWORD')); p.add_argument('--client-id', default=os.getenv('MQTT_CLIENT_ID'))
    p.add_argument('--auth-mode', choices=['anonymous','userpass','tls-cert','entra'], default=os.getenv('MQTT_AUTH_MODE','anonymous').lower())
    p.add_argument('--enable-tls', action='store_true', default=os.getenv('MQTT_ENABLE_TLS','').lower()=='true')
    p.add_argument('--entra-audience', default=os.getenv('MQTT_ENTRA_AUDIENCE','https://eventgrid.azure.net/'))
    p.add_argument('--entra-client-id', default=os.getenv('MQTT_ENTRA_CLIENT_ID'))
    return parser

def main() -> None:
    logging.basicConfig(level=os.getenv('LOG_LEVEL','INFO')); parser=_parser(); args=parser.parse_args();
    if args.command != 'feed': args=parser.parse_args(['feed'])
    asyncio.run(feed(args))
