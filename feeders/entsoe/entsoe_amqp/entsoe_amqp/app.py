"""ENTSO-E AMQP 1.0 feeder application."""
from __future__ import annotations

import argparse
import logging
import os
from typing import Optional
from urllib.parse import urlparse
from proton import symbol

from entsoe_core import EntsoeAPI, EntsoePoller, TimeSeriesPoint, parse_cross_border_pairs, parse_document_types, parse_domain_list, sample_points
from entsoe_amqp_producer_data.eu.entsoe.transparency.actualgenerationpertype import ActualGenerationPerType
from entsoe_amqp_producer_data.eu.entsoe.transparency.dayaheadprices import DayAheadPrices
from entsoe_amqp_producer_data.eu.entsoe.transparency.actualtotalload import ActualTotalLoad
from entsoe_amqp_producer_data.eu.entsoe.transparency.windsolarforecast import WindSolarForecast
from entsoe_amqp_producer_data.eu.entsoe.transparency.loadforecastmargin import LoadForecastMargin
from entsoe_amqp_producer_data.eu.entsoe.transparency.generationforecast import GenerationForecast
from entsoe_amqp_producer_data.eu.entsoe.transparency.reservoirfillinginformation import ReservoirFillingInformation
from entsoe_amqp_producer_data.eu.entsoe.transparency.actualgeneration import ActualGeneration
from entsoe_amqp_producer_data.eu.entsoe.transparency.windsolargeneration import WindSolarGeneration
from entsoe_amqp_producer_data.eu.entsoe.transparency.installedgenerationcapacitypertype import InstalledGenerationCapacityPerType
from entsoe_amqp_producer_data.eu.entsoe.transparency.crossborderphysicalflows import CrossBorderPhysicalFlows
from entsoe_amqp_producer_amqp_producer.producer import EuEntsoeTransparencyByDomainAmqpProducer, EuEntsoeTransparencyByDomainPsrTypeAmqpProducer, EuEntsoeTransparencyCrossBorderAmqpProducer

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS='https://servicebus.azure.net/.default'
logger=logging.getLogger(__name__)

def _build_data(point: TimeSeriesPoint):
    dt = point.document_type
    if dt == "A75":
        return ActualGenerationPerType(inDomain=point.in_domain, psrType=point.psr_type, quantity=point.quantity or 0.0, resolution=point.resolution, businessType=point.business_type, documentType=dt, unitName=point.unit_name or "MAW")
    if dt == "A44":
        return DayAheadPrices(inDomain=point.in_domain, price=point.price or 0.0, currency=point.currency or "EUR", unitName=point.unit_name or "MWH", resolution=point.resolution, documentType=dt)
    if dt == "A65":
        return ActualTotalLoad(inDomain=point.in_domain, quantity=point.quantity or 0.0, resolution=point.resolution, outDomain=point.out_domain or "not-applicable", documentType=dt)
    if dt == "A69":
        return WindSolarForecast(inDomain=point.in_domain, psrType=point.psr_type, quantity=point.quantity or 0.0, resolution=point.resolution, businessType=point.business_type, documentType=dt, unitName=point.unit_name or "MAW")
    if dt == "A70":
        return LoadForecastMargin(inDomain=point.in_domain, quantity=point.quantity or 0.0, resolution=point.resolution, documentType=dt, unitName=point.unit_name or "MAW")
    if dt == "A71":
        return GenerationForecast(inDomain=point.in_domain, quantity=point.quantity or 0.0, resolution=point.resolution, documentType=dt, unitName=point.unit_name or "MAW")
    if dt == "A72":
        return ReservoirFillingInformation(inDomain=point.in_domain, quantity=point.quantity or 0.0, resolution=point.resolution, documentType=dt, unitName=point.unit_name or "MWH")
    if dt == "A73":
        return ActualGeneration(inDomain=point.in_domain, quantity=point.quantity or 0.0, resolution=point.resolution, documentType=dt, unitName=point.unit_name or "MAW")
    if dt == "A74":
        return WindSolarGeneration(inDomain=point.in_domain, psrType=point.psr_type, quantity=point.quantity or 0.0, resolution=point.resolution, businessType=point.business_type, documentType=dt, unitName=point.unit_name or "MAW")
    if dt == "A68":
        return InstalledGenerationCapacityPerType(inDomain=point.in_domain, psrType=point.psr_type, quantity=point.quantity or 0.0, resolution=point.resolution, businessType=point.business_type, documentType=dt, unitName=point.unit_name or "MAW")
    if dt == "A11":
        return CrossBorderPhysicalFlows(inDomain=point.in_domain, outDomain=point.out_domain or "", quantity=point.quantity or 0.0, resolution=point.resolution, documentType=dt, unitName=point.unit_name or "MAW")
    raise ValueError(f"Unsupported document type {dt}")

class AmqpPublisher:
    def __init__(self, domain, psr, cross): self.domain=domain; self.psr=psr; self.cross=cross
    def emit_point(self, point: TimeSeriesPoint) -> None:
        data=_build_data(point); dt=point.document_type
        if dt == 'A75': self.psr.send_actual_generation_per_type(data, point.in_domain, point.psr_type)
        elif dt == 'A44': self.domain.send_day_ahead_prices(data, point.in_domain)
        elif dt == 'A65': self.domain.send_actual_total_load(data, point.in_domain)
        elif dt == 'A69': self.psr.send_wind_solar_forecast(data, point.in_domain, point.psr_type)
        elif dt == 'A70': self.domain.send_load_forecast_margin(data, point.in_domain)
        elif dt == 'A71': self.domain.send_generation_forecast(data, point.in_domain)
        elif dt == 'A72': self.domain.send_reservoir_filling_information(data, point.in_domain)
        elif dt == 'A73': self.domain.send_actual_generation(data, point.in_domain)
        elif dt == 'A74': self.psr.send_wind_solar_generation(data, point.in_domain, point.psr_type)
        elif dt == 'A68': self.psr.send_installed_generation_capacity_per_type(data, point.in_domain, point.psr_type)
        elif dt == 'A11': self.cross.send_cross_border_physical_flows(data, point.in_domain, point.out_domain or '')
    def flush(self): pass
    def close(self):
        for p in (self.domain,self.psr,self.cross):
            try: p.close()
            except Exception: pass

def _parse_broker_url(url: str):
    parsed=urlparse(url if '://' in url else f'amqp://{url}'); scheme=(parsed.scheme or 'amqp').lower(); tls=scheme in ('amqps','ssl','tls')
    return parsed.hostname or 'localhost', parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or '').lstrip('/') or None

def _apply_partition_key_workaround(producer):
    # WORKAROUND(xregistry/codegen#294): xrcg declares AMQP message_annotations but does not emit them yet.
    def stamp(msg):
        app_props = dict(getattr(msg, 'properties', None) or {})
        ce_subject = app_props.get('cloudEvents:subject') or getattr(msg, 'subject', None)
        if ce_subject:
            annotations = dict(getattr(msg, 'annotations', None) or {})
            annotations[symbol('x-opt-partition-key')] = ce_subject
            msg.annotations = annotations
        return msg
    if getattr(producer, '_sender', None) is not None:
        original_send = producer._sender.send
        producer._sender.send = lambda msg, *a, **kw: original_send(stamp(msg), *a, **kw)
    if hasattr(producer, '_send_via_reactor'):
        original_reactor_send = producer._send_via_reactor
        producer._send_via_reactor = lambda msg: original_reactor_send(stamp(msg))
    return producer

def _build_producers(host, port, address, use_tls, content_mode, auth_mode, username, password, entra_audience, entra_client_id, sas_key_name, sas_key):
    kwargs=dict(host=host, address=address, port=port, content_mode=content_mode, use_tls=use_tls)
    if auth_mode=='entra':
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        kwargs.update(credential=ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential(), entra_audience=entra_audience)
    elif auth_mode=='sas': kwargs.update(sas_key_name=sas_key_name, sas_key=sas_key)
    else: kwargs.update(username=username, password=password)
    return tuple(_apply_partition_key_workaround(p) for p in (EuEntsoeTransparencyByDomainAmqpProducer(**kwargs), EuEntsoeTransparencyByDomainPsrTypeAmqpProducer(**kwargs), EuEntsoeTransparencyCrossBorderAmqpProducer(**kwargs)))

def _common_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    sub = parser.add_subparsers(dest="command")
    feed = sub.add_parser("feed")
    feed.add_argument("--security-token", default=os.getenv("ENTSOE_SECURITY_TOKEN"))
    feed.add_argument("--domains", default=os.getenv("ENTSOE_DOMAINS"))
    feed.add_argument("--document-types", default=os.getenv("ENTSOE_DOCUMENT_TYPES"))
    feed.add_argument("--cross-border-pairs", default=os.getenv("ENTSOE_CROSS_BORDER_PAIRS"), help="Comma-separated in>out EIC pairs")
    feed.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "900")))
    feed.add_argument("--lookback-hours", type=int, default=int(os.getenv("ENTSOE_LOOKBACK_HOURS", "24")))
    feed.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser("~/.entsoe_state.json")))
    feed.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    feed.add_argument("--sample-mode", action="store_true", default=os.getenv("ENTSOE_SAMPLE_MODE", "").lower() in ("1", "true", "yes"))
    return parser


def _run_or_sample(args, publisher):
    if args.sample_mode:
        for point in sample_points():
            publisher.emit_point(point)
        publisher.flush()
        publisher.close()
        return
    if not args.security_token:
        raise SystemExit("ENTSOE_SECURITY_TOKEN or --security-token is required unless ENTSOE_SAMPLE_MODE=true")
    api = EntsoeAPI(args.security_token)
    poller = EntsoePoller(api, publisher, args.state_file, parse_domain_list(args.domains), parse_document_types(args.document_types), parse_cross_border_pairs(args.cross_border_pairs), args.lookback_hours, args.polling_interval)
    poller.run(once=args.once)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    parser=_common_parser('ENTSO-E Transparency Platform AMQP 1.0 bridge')
    feed=parser._subparsers._group_actions[0].choices['feed']
    feed.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL'))
    feed.add_argument('--host', default=os.getenv('AMQP_HOST'))
    feed.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT','0')) or None)
    feed.add_argument('--address', default=os.getenv('AMQP_ADDRESS','entsoe'))
    feed.add_argument('--username', default=os.getenv('AMQP_USERNAME'))
    feed.add_argument('--password', default=os.getenv('AMQP_PASSWORD'))
    feed.add_argument('--tls', action='store_true', default=os.getenv('AMQP_TLS','').lower() in ('1','true','yes'))
    feed.add_argument('--content-mode', default='binary', choices=['binary'], help='CloudEvents content mode; AMQP feeder supports binary mode only.')
    feed.add_argument('--auth-mode', default=os.getenv('AMQP_AUTH_MODE','password'), choices=['password','entra','sas'])
    feed.add_argument('--entra-audience', default=os.getenv('AMQP_ENTRA_AUDIENCE', DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    feed.add_argument('--entra-client-id', default=os.getenv('AMQP_ENTRA_CLIENT_ID'))
    feed.add_argument('--sas-key-name', default=os.getenv('AMQP_SAS_KEY_NAME'))
    feed.add_argument('--sas-key', default=os.getenv('AMQP_SAS_KEY'))
    args=parser.parse_args();
    if args.command!='feed': parser.print_help(); return
    address=args.address
    if args.broker_url:
        host,port,tls,user,pwd,path=_parse_broker_url(args.broker_url); username=args.username or user; password=args.password or pwd; address=path or address
    else:
        host=args.host or 'localhost'; tls=bool(args.tls) or args.auth_mode=='entra'; port=args.port or (5671 if tls else 5672); username=args.username; password=args.password
    producers=_build_producers(host,port,address,tls,args.content_mode,args.auth_mode,username,password,args.entra_audience,args.entra_client_id,args.sas_key_name,args.sas_key)
    _run_or_sample(args, AmqpPublisher(*producers))
