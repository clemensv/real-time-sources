"""ENTSO-E Kafka feeder application."""
from __future__ import annotations

import argparse
import logging
import os
from typing import Dict

from confluent_kafka import Producer
from entsoe_core import EntsoeAPI, EntsoePoller, TimeSeriesPoint, parse_cross_border_pairs, parse_document_types, parse_domain_list, sample_points
from entsoe_producer_data.eu.entsoe.transparency.actualgenerationpertype import ActualGenerationPerType
from entsoe_producer_data.eu.entsoe.transparency.dayaheadprices import DayAheadPrices
from entsoe_producer_data.eu.entsoe.transparency.actualtotalload import ActualTotalLoad
from entsoe_producer_data.eu.entsoe.transparency.windsolarforecast import WindSolarForecast
from entsoe_producer_data.eu.entsoe.transparency.loadforecastmargin import LoadForecastMargin
from entsoe_producer_data.eu.entsoe.transparency.generationforecast import GenerationForecast
from entsoe_producer_data.eu.entsoe.transparency.reservoirfillinginformation import ReservoirFillingInformation
from entsoe_producer_data.eu.entsoe.transparency.actualgeneration import ActualGeneration
from entsoe_producer_data.eu.entsoe.transparency.windsolargeneration import WindSolarGeneration
from entsoe_producer_data.eu.entsoe.transparency.installedgenerationcapacitypertype import InstalledGenerationCapacityPerType
from entsoe_producer_data.eu.entsoe.transparency.crossborderphysicalflows import CrossBorderPhysicalFlows
from entsoe_producer_kafka_producer.producer import EuEntsoeTransparencyByDomainEventProducer, EuEntsoeTransparencyByDomainPsrTypeEventProducer, EuEntsoeTransparencyCrossBorderEventProducer

logger = logging.getLogger(__name__)

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


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    config = {}
    for part in connection_string.split(';'):
        if 'Endpoint' in part:
            config['bootstrap.servers'] = part.split('=',1)[1].strip('"').replace('sb://','').replace('/','') + ':9093'
        elif 'EntityPath' in part:
            config['kafka_topic'] = part.split('=',1)[1].strip('"')
        elif 'SharedAccessKeyName' in part:
            config['sasl.username'] = '$ConnectionString'
        elif 'SharedAccessKey' in part:
            config['sasl.password'] = connection_string.strip()
        elif 'BootstrapServer' in part:
            config['bootstrap.servers'] = part.split('=',1)[1].strip()
    if 'sasl.username' in config:
        config['security.protocol'] = 'SASL_SSL'
        config['sasl.mechanism'] = 'PLAIN'
    return config

class _KafkaProducerWithDelivery:
    def __init__(self, producer, callback):
        self._producer = producer
        self._callback = callback
    def produce(self, *args, **kwargs):
        kwargs.setdefault('on_delivery', self._callback)
        return self._producer.produce(*args, **kwargs)
    def flush(self, *args, **kwargs):
        return self._producer.flush(*args, **kwargs)
    def poll(self, *args, **kwargs):
        return self._producer.poll(*args, **kwargs)

class KafkaPublisher:
    def __init__(self, producer, topic):
        self.kafka_producer = producer
        self._delivery_errors = []
        producer_with_delivery = _KafkaProducerWithDelivery(producer, self._delivery_report)
        self.domain = EuEntsoeTransparencyByDomainEventProducer(producer_with_delivery, topic)
        self.psr = EuEntsoeTransparencyByDomainPsrTypeEventProducer(producer_with_delivery, topic)
        self.cross = EuEntsoeTransparencyCrossBorderEventProducer(producer_with_delivery, topic)
    def _delivery_report(self, err, _msg):
        if err is not None:
            self._delivery_errors.append(err)
    def emit_point(self, point: TimeSeriesPoint) -> None:
        data = _build_data(point)
        dt = point.document_type
        if dt == 'A75': self.psr.send_eu_entsoe_transparency_actual_generation_per_type(point.in_domain, point.psr_type, data, flush_producer=False)
        elif dt == 'A44': self.domain.send_eu_entsoe_transparency_day_ahead_prices(point.in_domain, data, flush_producer=False)
        elif dt == 'A65': self.domain.send_eu_entsoe_transparency_actual_total_load(point.in_domain, data, flush_producer=False)
        elif dt == 'A69': self.psr.send_eu_entsoe_transparency_wind_solar_forecast(point.in_domain, point.psr_type, data, flush_producer=False)
        elif dt == 'A70': self.domain.send_eu_entsoe_transparency_load_forecast_margin(point.in_domain, data, flush_producer=False)
        elif dt == 'A71': self.domain.send_eu_entsoe_transparency_generation_forecast(point.in_domain, data, flush_producer=False)
        elif dt == 'A72': self.domain.send_eu_entsoe_transparency_reservoir_filling_information(point.in_domain, data, flush_producer=False)
        elif dt == 'A73': self.domain.send_eu_entsoe_transparency_actual_generation(point.in_domain, data, flush_producer=False)
        elif dt == 'A74': self.psr.send_eu_entsoe_transparency_wind_solar_generation(point.in_domain, point.psr_type, data, flush_producer=False)
        elif dt == 'A68': self.psr.send_eu_entsoe_transparency_installed_generation_capacity_per_type(point.in_domain, point.psr_type, data, flush_producer=False)
        elif dt == 'A11': self.cross.send_eu_entsoe_transparency_cross_border_physical_flows(point.in_domain, point.out_domain or '', data, flush_producer=False)
    def flush(self):
        self.kafka_producer.flush()
        if self._delivery_errors:
            errors = self._delivery_errors
            self._delivery_errors = []
            raise RuntimeError(f'Kafka delivery failed: {errors[0]}')
    def close(self): self.kafka_producer.flush()

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
    parser = _common_parser('ENTSO-E Transparency Platform Kafka bridge')
    feed = parser._subparsers._group_actions[0].choices['feed']
    feed.add_argument('--kafka-bootstrap-servers', default=os.getenv('KAFKA_BOOTSTRAP_SERVERS'))
    feed.add_argument('--kafka-topic', default=os.getenv('KAFKA_TOPIC'))
    feed.add_argument('--sasl-username', default=os.getenv('SASL_USERNAME'))
    feed.add_argument('--sasl-password', default=os.getenv('SASL_PASSWORD'))
    feed.add_argument('--connection-string', default=os.getenv('CONNECTION_STRING'))
    args = parser.parse_args()
    if args.command != 'feed': parser.print_help(); return
    if args.connection_string:
        cfg = parse_connection_string(args.connection_string); bootstrap=cfg.get('bootstrap.servers'); topic=cfg.get('kafka_topic'); user=cfg.get('sasl.username'); pwd=cfg.get('sasl.password')
    else:
        bootstrap=args.kafka_bootstrap_servers; topic=args.kafka_topic; user=args.sasl_username; pwd=args.sasl_password; cfg={}
    if not bootstrap: raise SystemExit('Kafka bootstrap servers required')
    if not topic: raise SystemExit('Kafka topic required')
    kafka_config={'bootstrap.servers': bootstrap, 'enable.idempotence': 'true', 'acks': 'all', 'compression.type': 'lz4', 'linger.ms': '20'}; kafka_config.update({k:v for k,v in cfg.items() if k not in ('kafka_topic',)})
    if user and pwd:
        kafka_config.update({'sasl.mechanisms':'PLAIN','security.protocol':'SASL_SSL' if os.getenv('KAFKA_ENABLE_TLS','true').lower() not in ('false','0','no') else 'SASL_PLAINTEXT','sasl.username':user,'sasl.password':pwd})
    elif os.getenv('KAFKA_ENABLE_TLS','true').lower() not in ('false','0','no'):
        kafka_config['security.protocol']='SSL'
    _run_or_sample(args, KafkaPublisher(Producer(kafka_config), topic))
