from __future__ import annotations

import argparse
import logging
import os
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from digitraffic_maritime.bridge import DigitraficBridge, DigitrafficPortCallPoller
from digitraffic_maritime.mqtt_source import MQTTSource
from digitraffic_maritime_amqp_producer_data import PortCall, PortLocation, VesselDetails, VesselLocation, VesselMetadata
from digitraffic_maritime_amqp_producer_amqp_producer.producer import (
    FiDigitrafficMarineAisAmqpProducer,
    FiDigitrafficMarinePortcallAmqpProducer,
    FiDigitrafficMarinePortcallPortlocationAmqpProducer,
    FiDigitrafficMarinePortcallVesseldetailsAmqpProducer,
)

logger = logging.getLogger(__name__)

DEFAULT_ENTRA_AUDIENCE = 'https://servicebus.azure.net/.default'


class _NoopFlush:
    def flush(self) -> None:
        return


class _AisAdapter:
    def __init__(self, producer: FiDigitrafficMarineAisAmqpProducer):
        self._producer = producer

    def send_fi_digitraffic_marine_ais_vessel_location(self, *, _mmsi: str, data: VesselLocation, flush_producer: bool = False):
        self._producer.send_location(_mmsi=_mmsi, data=data)

    def send_fi_digitraffic_marine_ais_vessel_metadata(self, *, _mmsi: str, data: VesselMetadata, flush_producer: bool = False):
        self._producer.send_metadata(_mmsi=_mmsi, data=data)


class _PortCallAdapter:
    def __init__(
        self,
        port_call_producer: FiDigitrafficMarinePortcallAmqpProducer,
        vessel_details_producer: FiDigitrafficMarinePortcallVesseldetailsAmqpProducer,
        port_location_producer: FiDigitrafficMarinePortcallPortlocationAmqpProducer,
    ):
        self._port_call_producer = port_call_producer
        self._vessel_details_producer = vessel_details_producer
        self._port_location_producer = port_location_producer

    def send_fi_digitraffic_marine_portcall_port_call(self, *, _port_call_id: str, data: PortCall, flush_producer: bool = False):
        self._port_call_producer.send_port_call(_port_call_id=_port_call_id, data=data)

    def send_fi_digitraffic_marine_portcall_vessel_details(self, *, _vessel_id: str, data: VesselDetails, flush_producer: bool = False):
        self._vessel_details_producer.send_vessel_details(_vessel_id=_vessel_id, data=data)

    def send_fi_digitraffic_marine_portcall_port_location(self, *, _locode: str, data: PortLocation, flush_producer: bool = False):
        self._port_location_producer.send_port_location(_locode=_locode, data=data)


def _parse_broker_url(url: str) -> tuple[str, int, str, Optional[str], Optional[str], bool]:
    parsed = urlparse(url if '://' in url else f'amqp://{url}')
    scheme = (parsed.scheme or 'amqp').lower()
    tls = scheme in ('amqps', 'ssl', 'tls')
    host = parsed.hostname or 'localhost'
    port = parsed.port or (5671 if tls else 5672)
    address = parsed.path.lstrip('/') if parsed.path else ''
    return host, port, address, parsed.username, parsed.password, tls


def _build_common_kwargs(args: argparse.Namespace) -> tuple[Dict[str, Any], str]:
    host = args.host
    port = args.port
    address = args.address
    tls = args.tls
    username = args.username
    password = args.password

    if args.broker_url:
        parsed_host, parsed_port, parsed_address, parsed_user, parsed_password, parsed_tls = _parse_broker_url(args.broker_url)
        host = host or parsed_host
        port = port or parsed_port
        address = address or parsed_address
        tls = tls or parsed_tls
        username = username or parsed_user
        password = password or parsed_password

    host = host or 'localhost'
    port = int(port or (5671 if tls else 5672))
    address = address or 'digitraffic-maritime'

    kwargs: Dict[str, Any] = {
        'host': host,
        'port': port,
        'address': address,
        'content_mode': args.content_mode,
        'use_tls': tls,
    }

    if args.auth_mode == 'entra':
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

        credential = ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential()
        kwargs['credential'] = credential
        kwargs['entra_audience'] = args.entra_audience
        kwargs['use_tls'] = True
    elif username or password:
        kwargs['username'] = username
        kwargs['password'] = password

    return kwargs, address


def _run_stream(args: argparse.Namespace, ais_adapter: _AisAdapter):
    subs = [s.strip() for s in args.subscribe.split(',') if s.strip()]
    mmsi_filter_set = set(int(m.strip()) for m in args.mmsi_filter.split(',') if m.strip()) if args.mmsi_filter else None
    bridge = DigitraficBridge(
        mqtt_source=MQTTSource(
            subscribe_locations='location' in subs,
            subscribe_metadata='metadata' in subs,
            mmsi_filter=mmsi_filter_set,
        ),
        kafka_producer=_NoopFlush(),  # type: ignore[arg-type]
        event_producer=ais_adapter,  # type: ignore[arg-type]
        mmsi_filter=mmsi_filter_set,
        flush_interval=max(1, args.flush_interval),
    )

    if not args.once:
        bridge.run()
        return

    emitted = {'count': 0}
    original = bridge._on_message

    def _once_on_message(topic_type: str, mmsi: int, payload: Dict[str, Any]) -> None:
        original(topic_type, mmsi, payload)
        if bridge._total > 0:
            emitted['count'] += 1
            raise KeyboardInterrupt

    bridge._on_message = _once_on_message  # type: ignore[assignment]
    try:
        bridge.run()
    except KeyboardInterrupt:
        if emitted['count']:
            logger.info('ONCE_MODE enabled: exiting after first emitted AIS message')


def _run_port_calls(args: argparse.Namespace, port_call_adapter: _PortCallAdapter):
    poller = DigitrafficPortCallPoller(
        kafka_producer=_NoopFlush(),  # type: ignore[arg-type]
        event_producer=port_call_adapter,  # type: ignore[arg-type]
        vessel_details_event_producer=port_call_adapter,  # type: ignore[arg-type]
        port_location_event_producer=port_call_adapter,  # type: ignore[arg-type]
        state_file=args.state_file,
        poll_interval=args.poll_interval,
    )
    poller.poll_and_send(once=args.once)



def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            import time; time.sleep(delay)
def main() -> None:
    parser = argparse.ArgumentParser(description='Digitraffic Maritime AMQP feeder')
    parser.add_argument('command', nargs='?', default='feed', choices=['feed'])
    parser.add_argument('--mode', choices=['stream', 'port-calls'], default=os.getenv('DIGITRAFFIC_MODE', 'stream'))
    parser.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL', ''))
    parser.add_argument('--host', default=os.getenv('AMQP_HOST'))
    parser.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT', '0') or 0))
    parser.add_argument('--address', default=os.getenv('AMQP_ADDRESS', 'digitraffic-maritime'))
    parser.add_argument('--username', default=os.getenv('AMQP_USERNAME'))
    parser.add_argument('--password', default=os.getenv('AMQP_PASSWORD'))
    parser.add_argument('--auth-mode', choices=['password', 'entra'], default=os.getenv('AMQP_AUTH_MODE', 'password'))
    parser.add_argument('--entra-audience', default=os.getenv('AMQP_ENTRA_AUDIENCE', DEFAULT_ENTRA_AUDIENCE))
    parser.add_argument('--entra-client-id', default=os.getenv('AMQP_ENTRA_CLIENT_ID'))
    parser.add_argument('--tls', action='store_true', default=os.getenv('AMQP_TLS', 'false').lower() in ('1', 'true', 'yes'))
    parser.add_argument('--content-mode', choices=['binary', 'structured'], default=os.getenv('AMQP_CONTENT_MODE', 'binary'))
    parser.add_argument('--subscribe', default=os.getenv('DIGITRAFFIC_SUBSCRIBE', 'location,metadata'))
    parser.add_argument('--mmsi-filter', default=os.getenv('DIGITRAFFIC_FILTER_MMSI'))
    parser.add_argument('--flush-interval', type=int, default=int(os.getenv('DIGITRAFFIC_FLUSH_INTERVAL', '1000')))
    parser.add_argument('--poll-interval', type=int, default=int(os.getenv('DIGITRAFFIC_PORTCALL_POLL_INTERVAL', '300')))
    parser.add_argument('--state-file', default=os.getenv('DIGITRAFFIC_PORTCALL_STATE_FILE', os.path.expanduser('~/.digitraffic_portcalls_state.json')))
    parser.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE', 'false').lower() in ('1', 'true', 'yes'))
    args = parser.parse_args()

    logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO').upper(), format='%(asctime)s %(levelname)s %(name)s: %(message)s')

    kwargs, _ = _build_common_kwargs(args)
    ais_producer = _retry_producer_init(lambda: FiDigitrafficMarineAisAmqpProducer(**kwargs))
    port_call_producer = _retry_producer_init(lambda: FiDigitrafficMarinePortcallAmqpProducer(**kwargs))
    vessel_details_producer = _retry_producer_init(lambda: FiDigitrafficMarinePortcallVesseldetailsAmqpProducer(**kwargs))
    port_location_producer = _retry_producer_init(lambda: FiDigitrafficMarinePortcallPortlocationAmqpProducer(**kwargs))

    try:
        if args.mode == 'stream':
            _run_stream(args, _AisAdapter(ais_producer))
        else:
            _run_port_calls(args, _PortCallAdapter(port_call_producer, vessel_details_producer, port_location_producer))
    finally:
        for producer in (ais_producer, port_call_producer, vessel_details_producer, port_location_producer):
            try:
                producer.close()
            except Exception:
                pass


if __name__ == '__main__':
    main()
