"""ENTSO-E MQTT/UNS feeder application."""
from __future__ import annotations

import argparse
import asyncio
import logging
import os
import threading
import time
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

from entsoe_core import EntsoeAPI, EntsoePoller, TimeSeriesPoint, parse_cross_border_pairs, parse_document_types, parse_domain_list, sample_points
from entsoe_mqtt_producer_data.eu.entsoe.transparency.actualgenerationpertype import ActualGenerationPerType
from entsoe_mqtt_producer_data.eu.entsoe.transparency.dayaheadprices import DayAheadPrices
from entsoe_mqtt_producer_data.eu.entsoe.transparency.actualtotalload import ActualTotalLoad
from entsoe_mqtt_producer_data.eu.entsoe.transparency.windsolarforecast import WindSolarForecast
from entsoe_mqtt_producer_data.eu.entsoe.transparency.loadforecastmargin import LoadForecastMargin
from entsoe_mqtt_producer_data.eu.entsoe.transparency.generationforecast import GenerationForecast
from entsoe_mqtt_producer_data.eu.entsoe.transparency.reservoirfillinginformation import ReservoirFillingInformation
from entsoe_mqtt_producer_data.eu.entsoe.transparency.actualgeneration import ActualGeneration
from entsoe_mqtt_producer_data.eu.entsoe.transparency.windsolargeneration import WindSolarGeneration
from entsoe_mqtt_producer_data.eu.entsoe.transparency.installedgenerationcapacitypertype import InstalledGenerationCapacityPerType
from entsoe_mqtt_producer_data.eu.entsoe.transparency.crossborderphysicalflows import CrossBorderPhysicalFlows
from entsoe_mqtt_producer_mqtt_client.client import EuEntsoeTransparencyByDomainMqttMqttClient, EuEntsoeTransparencyByDomainPsrTypeMqttMqttClient, EuEntsoeTransparencyCrossBorderMqttMqttClient

DEFAULT_ENTRA_AUDIENCE = 'https://eventgrid.azure.net/'
ENTRA_MQTT_AUTH_METHOD = 'OAUTH2-JWT'
logger = logging.getLogger(__name__)

def _build_data(point: TimeSeriesPoint):
    dt = point.document_type
    if dt == 'A75': return ActualGenerationPerType(inDomain=point.in_domain, psrType=point.psr_type, quantity=point.quantity or 0.0, resolution=point.resolution, businessType=point.business_type, documentType=dt, unitName=point.unit_name or 'MAW')
    if dt == 'A44': return DayAheadPrices(inDomain=point.in_domain, price=point.price or 0.0, currency=point.currency or 'EUR', unitName=point.unit_name or 'MWH', resolution=point.resolution, documentType=dt)
    if dt == 'A65': return ActualTotalLoad(inDomain=point.in_domain, quantity=point.quantity or 0.0, resolution=point.resolution, outDomain=point.out_domain or "not-applicable", documentType=dt)
    if dt == 'A69': return WindSolarForecast(inDomain=point.in_domain, psrType=point.psr_type, quantity=point.quantity or 0.0, resolution=point.resolution, businessType=point.business_type, documentType=dt, unitName=point.unit_name or 'MAW')
    if dt == 'A70': return LoadForecastMargin(inDomain=point.in_domain, quantity=point.quantity or 0.0, resolution=point.resolution, documentType=dt, unitName=point.unit_name or 'MAW')
    if dt == 'A71': return GenerationForecast(inDomain=point.in_domain, quantity=point.quantity or 0.0, resolution=point.resolution, documentType=dt, unitName=point.unit_name or 'MAW')
    if dt == 'A72': return ReservoirFillingInformation(inDomain=point.in_domain, quantity=point.quantity or 0.0, resolution=point.resolution, documentType=dt, unitName=point.unit_name or 'MWH')
    if dt == 'A73': return ActualGeneration(inDomain=point.in_domain, quantity=point.quantity or 0.0, resolution=point.resolution, documentType=dt, unitName=point.unit_name or 'MAW')
    if dt == 'A74': return WindSolarGeneration(inDomain=point.in_domain, psrType=point.psr_type, quantity=point.quantity or 0.0, resolution=point.resolution, businessType=point.business_type, documentType=dt, unitName=point.unit_name or 'MAW')
    if dt == 'A68': return InstalledGenerationCapacityPerType(inDomain=point.in_domain, psrType=point.psr_type, quantity=point.quantity or 0.0, resolution=point.resolution, businessType=point.business_type, documentType=dt, unitName=point.unit_name or 'MAW')
    if dt == 'A11': return CrossBorderPhysicalFlows(inDomain=point.in_domain, outDomain=point.out_domain or '', quantity=point.quantity or 0.0, resolution=point.resolution, documentType=dt, unitName=point.unit_name or 'MAW')
    raise ValueError(dt)


def _acquire_entra_token(audience: str, client_id: Optional[str]):
    from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
    credential = ManagedIdentityCredential(client_id=client_id) if client_id else DefaultAzureCredential()
    scope = audience if audience.endswith('/.default') else f'{audience}/.default'
    token = credential.get_token(scope)
    return token.token, datetime.fromtimestamp(token.expires_on, tz=timezone.utc)


def _start_entra_refresh_thread(paho_client, host: str, port: int, audience: str, client_id: Optional[str], expires_at: datetime):
    stop_event = threading.Event()

    def refresh_loop():
        nonlocal expires_at
        while not stop_event.wait(max(60.0, (expires_at - datetime.now(timezone.utc)).total_seconds() - 300.0)):
            try:
                token, expires_at = _acquire_entra_token(audience, client_id)
                props = Properties(PacketTypes.CONNECT)
                props.AuthenticationMethod = ENTRA_MQTT_AUTH_METHOD
                props.AuthenticationData = token.encode('utf-8')
                try:
                    paho_client.disconnect()
                except Exception:
                    pass
                paho_client.connect(host, port, keepalive=60, clean_start=True, properties=props)
                logger.info('Refreshed MQTT Entra JWT and reconnected (expires=%s)', expires_at.isoformat())
            except Exception as exc:
                logger.warning('Failed to refresh MQTT Entra JWT: %s', exc)
                time.sleep(60)

    thread = threading.Thread(target=refresh_loop, name='entsoe-mqtt-entra-refresh', daemon=True)
    thread.start()
    return stop_event

class MqttPublisher:
    def __init__(self, domain_client, psr_client, cross_client, loop, refresh_stop=None):
        self.domain = domain_client
        self.psr = psr_client
        self.cross = cross_client
        self.loop = loop
        self._refresh_stop = refresh_stop
        self._pending = []
        paho_client = self.domain.client
        original_publish = paho_client.publish
        def publish_with_tracking(*args, **kwargs):
            info = original_publish(*args, **kwargs)
            self._pending.append(info)
            return info
        paho_client.publish = publish_with_tracking
    def _run(self, coro): self.loop.run_until_complete(coro)
    def emit_point(self, point: TimeSeriesPoint) -> None:
        data = _build_data(point); dt = point.document_type
        if dt == 'A75': self._run(self.psr.publish_eu_entsoe_transparency_by_domain_psr_type_mqtt_actual_generation_per_type(point.in_domain, point.psr_type, data))
        elif dt == 'A44': self._run(self.domain.publish_eu_entsoe_transparency_by_domain_mqtt_day_ahead_prices(point.in_domain, data))
        elif dt == 'A65': self._run(self.domain.publish_eu_entsoe_transparency_by_domain_mqtt_actual_total_load(point.in_domain, data))
        elif dt == 'A69': self._run(self.psr.publish_eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_forecast(point.in_domain, point.psr_type, data))
        elif dt == 'A70': self._run(self.domain.publish_eu_entsoe_transparency_by_domain_mqtt_load_forecast_margin(point.in_domain, data))
        elif dt == 'A71': self._run(self.domain.publish_eu_entsoe_transparency_by_domain_mqtt_generation_forecast(point.in_domain, data))
        elif dt == 'A72': self._run(self.domain.publish_eu_entsoe_transparency_by_domain_mqtt_reservoir_filling_information(point.in_domain, data))
        elif dt == 'A73': self._run(self.domain.publish_eu_entsoe_transparency_by_domain_mqtt_actual_generation(point.in_domain, data))
        elif dt == 'A74': self._run(self.psr.publish_eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_generation(point.in_domain, point.psr_type, data))
        elif dt == 'A68': self._run(self.psr.publish_eu_entsoe_transparency_by_domain_psr_type_mqtt_installed_generation_capacity_per_type(point.in_domain, point.psr_type, data))
        elif dt == 'A11': self._run(self.cross.publish_eu_entsoe_transparency_cross_border_mqtt_cross_border_physical_flows(point.in_domain, point.out_domain or '', data))
    def flush(self):
        pending, self._pending = self._pending, []
        for info in pending:
            info.wait_for_publish(timeout=30)
            if getattr(info, 'rc', 0) != 0:
                raise RuntimeError(f'MQTT publish failed with rc={info.rc}')
    def close(self):
        if self._refresh_stop is not None:
            self._refresh_stop.set()
        self._run(self.domain.disconnect())

def _parse_broker_url(url: str):
    parsed = urlparse(url if '://' in url else f'mqtt://{url}')
    tls = (parsed.scheme or 'mqtt').lower() in ('mqtts','ssl','tls')
    return parsed.hostname or 'localhost', parsed.port or (8883 if tls else 1883), tls, parsed.username, parsed.password

def _common_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    sub = parser.add_subparsers(dest='command')
    feed = sub.add_parser('feed')
    feed.add_argument('--security-token', default=os.getenv('ENTSOE_SECURITY_TOKEN'))
    feed.add_argument('--domains', default=os.getenv('ENTSOE_DOMAINS'))
    feed.add_argument('--document-types', default=os.getenv('ENTSOE_DOCUMENT_TYPES'))
    feed.add_argument('--cross-border-pairs', default=os.getenv('ENTSOE_CROSS_BORDER_PAIRS'))
    feed.add_argument('--polling-interval', type=int, default=int(os.getenv('POLLING_INTERVAL', '900')))
    feed.add_argument('--lookback-hours', type=int, default=int(os.getenv('ENTSOE_LOOKBACK_HOURS', '24')))
    feed.add_argument('--state-file', default=os.getenv('STATE_FILE', os.path.expanduser('~/.entsoe_state.json')))
    feed.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE', '').lower() in ('1','true','yes'))
    feed.add_argument('--sample-mode', action='store_true', default=os.getenv('ENTSOE_SAMPLE_MODE', '').lower() in ('1','true','yes'))
    return parser

def _run_or_sample(args, publisher):
    if args.sample_mode:
        for point in sample_points():
            publisher.emit_point(point)
        publisher.flush(); publisher.close(); return
    if not args.security_token:
        raise SystemExit('ENTSOE_SECURITY_TOKEN or --security-token is required unless ENTSOE_SAMPLE_MODE=true')
    api = EntsoeAPI(args.security_token)
    poller = EntsoePoller(api, publisher, args.state_file, parse_domain_list(args.domains), parse_document_types(args.document_types), parse_cross_border_pairs(args.cross_border_pairs), args.lookback_hours, args.polling_interval)
    poller.run(once=args.once)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    parser = _common_parser('ENTSO-E Transparency Platform MQTT/UNS bridge')
    feed = parser._subparsers._group_actions[0].choices['feed']
    feed.add_argument('--broker-url', default=os.getenv('MQTT_BROKER_URL'))
    feed.add_argument('--broker-host', default=os.getenv('MQTT_HOST'))
    feed.add_argument('--broker-port', type=int, default=int(os.getenv('MQTT_PORT','0')) or None)
    feed.add_argument('--username', default=os.getenv('MQTT_USERNAME'))
    feed.add_argument('--password', default=os.getenv('MQTT_PASSWORD'))
    feed.add_argument('--tls', action='store_true', default=os.getenv('MQTT_TLS', os.getenv('MQTT_ENABLE_TLS','')).lower() in ('1','true','yes'))
    feed.add_argument('--client-id', default=os.getenv('MQTT_CLIENT_ID'))
    feed.add_argument('--auth-mode', default=os.getenv('MQTT_AUTH_MODE','anonymous'), choices=['anonymous','password','userpass','entra'])
    feed.add_argument('--entra-audience', default=os.getenv('MQTT_ENTRA_AUDIENCE', DEFAULT_ENTRA_AUDIENCE))
    feed.add_argument('--entra-client-id', default=os.getenv('MQTT_ENTRA_CLIENT_ID'))
    args = parser.parse_args()
    if args.command != 'feed': parser.print_help(); return
    if args.broker_url:
        host, port, tls, user, pwd = _parse_broker_url(args.broker_url); username = args.username or user; password = args.password or pwd
    else:
        host = args.broker_host or 'localhost'; tls = bool(args.tls) or args.auth_mode == 'entra'; port = args.broker_port or (8883 if tls else 1883); username = args.username; password = args.password
    paho = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=args.client_id or '', protocol=MQTTv5)
    props = None; refresh_stop = None
    if args.auth_mode in ('password','userpass') and username: paho.username_pw_set(username, password or '')
    if args.auth_mode == 'entra':
        token, expires_at = _acquire_entra_token(args.entra_audience, args.entra_client_id)
        props = Properties(PacketTypes.CONNECT); props.AuthenticationMethod = ENTRA_MQTT_AUTH_METHOD; props.AuthenticationData = token.encode('utf-8')
    if tls or args.auth_mode == 'entra': paho.tls_set()
    loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
    domain_client = EuEntsoeTransparencyByDomainMqttMqttClient(client=paho, content_mode='binary', loop=loop)
    psr_client = EuEntsoeTransparencyByDomainPsrTypeMqttMqttClient(client=paho, content_mode='binary', loop=loop)
    cross_client = EuEntsoeTransparencyCrossBorderMqttMqttClient(client=paho, content_mode='binary', loop=loop)
    if args.auth_mode == 'entra':
        paho.connect(host, port, keepalive=60, clean_start=True, properties=props); paho.loop_start()
        refresh_stop = _start_entra_refresh_thread(paho, host, port, args.entra_audience, args.entra_client_id, expires_at)
    else: loop.run_until_complete(domain_client.connect(host, port))
    _run_or_sample(args, MqttPublisher(domain_client, psr_client, cross_client, loop, refresh_stop))

if __name__ == '__main__':
    main()
