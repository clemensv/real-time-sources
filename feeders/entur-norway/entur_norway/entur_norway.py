"""Entur Norway national real-time transit SIRI bridge to Apache Kafka."""

import argparse
import logging
import os
import sys
import time
import uuid
from typing import Dict, List, Optional, Tuple

from confluent_kafka import Producer

from entur_norway_core import (
    EnturNorwayBridge as _CoreEnturNorwayBridge,
    _bool_text,
    _find_multilingual_text,
    _find_text,
    _has_more_data,
    _siri,
    _topic_value,
    parse_duration_to_seconds,
)
from entur_norway_producer_data import (
    DatedServiceJourney,
    EstimatedVehicleJourney,
)
from entur_norway_producer_kafka_producer.producer import (
    NoEnturJourneysEventProducer,
    NoEnturSituationsEventProducer,
)

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def parse_connection_string(connection_string: str) -> Tuple[Dict[str, str], Optional[str]]:
    """Parse both plain-Kafka and Event Hubs connection strings into a Kafka config dict.

    Supports:
      - ``BootstrapServer=host:port;EntityPath=topic`` (plain / TLS-disabled)
      - Event Hubs ``Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=topic``
    """
    config: Dict[str, str] = {}
    kafka_topic: Optional[str] = None

    for part in connection_string.split(';'):
        part = part.strip()
        if not part or '=' not in part:
            continue
        key, _, value = part.partition('=')
        key = key.strip()
        value = value.strip().strip('"')
        if key == 'BootstrapServer':
            config['bootstrap.servers'] = value
        elif key == 'Endpoint':
            config['bootstrap.servers'] = value.replace('sb://', '').rstrip('/') + ':9093'
            config['security.protocol'] = 'SASL_SSL'
            config['sasl.mechanisms'] = 'PLAIN'
            config['sasl.username'] = '$ConnectionString'
            config['sasl.password'] = connection_string.strip()
        elif key == 'EntityPath':
            kafka_topic = value

    if 'bootstrap.servers' not in config:
        raise ValueError(f'Could not parse bootstrap servers from connection string: {connection_string!r}')

    # Allow caller to override TLS via environment variable
    if os.environ.get('KAFKA_ENABLE_TLS', '').lower() == 'false':
        config.pop('security.protocol', None)
        config.pop('sasl.mechanisms', None)
        config.pop('sasl.username', None)
        config.pop('sasl.password', None)

    return config, kafka_topic


class EnturNorwayBridge(_CoreEnturNorwayBridge):
    """Extends the core bridge with a Kafka-specific feed loop."""

    def feed(
        self,
        kafka_config: Dict[str, str],
        kafka_topic: str,
        polling_interval: int = 30,
        max_size: int = 1000,
    ) -> None:
        """Main feed loop: poll Entur SIRI feeds and emit CloudEvents to Kafka."""
        producer = Producer(kafka_config)
        journeys_ep = NoEnturJourneysEventProducer(producer, kafka_topic)
        situations_ep = NoEnturSituationsEventProducer(producer, kafka_topic)

        et_requestor_id = str(uuid.uuid4())
        vm_requestor_id = str(uuid.uuid4())
        sx_requestor_id = str(uuid.uuid4())

        first_run = True

        while True:
            try:
                poll_start = time.monotonic()

                # ── ET: Estimated Timetable ────────────────────────────────────
                # First run: omit requestorId to get full dataset for reference emission.
                # Subsequent runs: include requestorId for incremental updates.
                et_req_id: Optional[str] = None if first_run else et_requestor_id
                et_count = 0
                ref_count = 0
                seen_journeys: set = set()

                more_et = True
                while more_et:
                    et_root = self.fetch_siri('et', et_req_id, max_size)
                    if et_root is None:
                        break
                    more_et = _has_more_data(et_root)
                    et_req_id = et_requestor_id  # switch to incremental for pagination

                    et_journeys = self.parse_et_journeys(et_root)

                    if first_run:
                        for op_day, sj_id, evj in et_journeys:
                            key = (op_day, sj_id)
                            if key not in seen_journeys:
                                seen_journeys.add(key)
                                dsj = DatedServiceJourney(
                                    service_journey_id=sj_id,
                                    operating_day=op_day,
                                    line_ref=evj.line_ref,
                                    operator_ref=evj.operator_ref,
                                    direction_ref=evj.direction_ref,
                                    vehicle_mode=evj.vehicle_mode,
                                    route_ref=evj.route_ref,
                                    published_line_name=evj.published_line_name,
                                    external_line_ref=None,
                                    origin_name=evj.origin_name,
                                    destination_name=evj.destination_name,
                                    data_source=evj.data_source,
                                )
                                try:
                                    journeys_ep.send_no_entur_dated_service_journey(
                                        _operating_day=op_day,
                                        _service_journey_id=sj_id,
                                        data=dsj,
                                        flush_producer=False,
                                    )
                                    ref_count += 1
                                except Exception as exc:
                                    logging.error(
                                        'Error sending DatedServiceJourney %s/%s: %s',
                                        op_day, sj_id, exc,
                                    )

                    for op_day, sj_id, evj in et_journeys:
                        try:
                            journeys_ep.send_no_entur_estimated_vehicle_journey(
                                _operating_day=op_day,
                                _service_journey_id=sj_id,
                                data=evj,
                                flush_producer=False,
                            )
                            et_count += 1
                        except Exception as exc:
                            logging.error(
                                'Error sending EstimatedVehicleJourney %s/%s: %s',
                                op_day, sj_id, exc,
                            )

                producer.flush()
                if first_run:
                    logging.info(
                        'Emitted %d DatedServiceJourney reference and %d EstimatedVehicleJourney events',
                        ref_count, et_count,
                    )
                else:
                    logging.info('Emitted %d EstimatedVehicleJourney events (incremental)', et_count)

                # ── VM: Vehicle Monitoring ─────────────────────────────────────
                vm_req_id: Optional[str] = None if first_run else vm_requestor_id
                vm_count = 0
                more_vm = True
                while more_vm:
                    vm_root = self.fetch_siri('vm', vm_req_id, max_size)
                    if vm_root is None:
                        break
                    more_vm = _has_more_data(vm_root)
                    vm_req_id = vm_requestor_id

                    for op_day, sj_id, mvj in self.parse_vm_journeys(vm_root):
                        try:
                            journeys_ep.send_no_entur_monitored_vehicle_journey(
                                _operating_day=op_day,
                                _service_journey_id=sj_id,
                                data=mvj,
                                flush_producer=False,
                            )
                            vm_count += 1
                        except Exception as exc:
                            logging.error(
                                'Error sending MonitoredVehicleJourney %s/%s: %s',
                                op_day, sj_id, exc,
                            )

                producer.flush()
                logging.info('Emitted %d MonitoredVehicleJourney events', vm_count)

                # ── SX: Situation Exchange ─────────────────────────────────────
                sx_req_id: Optional[str] = None if first_run else sx_requestor_id
                sx_count = 0
                more_sx = True
                while more_sx:
                    sx_root = self.fetch_siri('sx', sx_req_id, max_size)
                    if sx_root is None:
                        break
                    more_sx = _has_more_data(sx_root)
                    sx_req_id = sx_requestor_id

                    for sit_num, sit in self.parse_sx_situations(sx_root):
                        try:
                            situations_ep.send_no_entur_pt_situation_element(
                                _situation_number=sit_num,
                                data=sit,
                                flush_producer=False,
                            )
                            sx_count += 1
                        except Exception as exc:
                            logging.error('Error sending PtSituationElement %s: %s', sit_num, exc)

                producer.flush()
                logging.info('Emitted %d PtSituationElement events', sx_count)

                first_run = False

                elapsed = time.monotonic() - poll_start
                sleep_time = max(0.0, polling_interval - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)

            except KeyboardInterrupt:
                logging.info('Shutting down...')
                break
            except Exception as exc:
                logging.error('Unhandled error in feed loop: %s', exc)
                time.sleep(polling_interval)


def main() -> None:
    """Entry point: parse CLI arguments and start the SIRI feed bridge."""
    parser = argparse.ArgumentParser(
        description='Entur Norway SIRI real-time bridge to Apache Kafka'
    )
    subparsers = parser.add_subparsers(dest='command')

    feed_parser = subparsers.add_parser('feed', help='Start the SIRI feed loop')
    feed_parser.add_argument('--connection-string', help='Kafka connection string')
    feed_parser.add_argument(
        '--polling-interval',
        type=int,
        default=None,
        help='Polling interval in seconds (default: 30)',
    )
    feed_parser.add_argument(
        '--max-size',
        type=int,
        default=None,
        help='Maximum records per SIRI request (default: 1000)',
    )

    args = parser.parse_args()
    if args.command == 'feed':
        connection_string = args.connection_string or os.environ.get('CONNECTION_STRING', '')
        polling_interval = (
            args.polling_interval
            if args.polling_interval is not None
            else int(os.environ.get('POLLING_INTERVAL', '30'))
        )
        max_size = (
            args.max_size
            if args.max_size is not None
            else int(os.environ.get('MAX_SIZE', '1000'))
        )

        if not connection_string:
            logging.error('CONNECTION_STRING is required')
            sys.exit(1)

        try:
            kafka_config, kafka_topic = parse_connection_string(connection_string)
        except ValueError as exc:
            logging.error('Invalid connection string: %s', exc)
            sys.exit(1)

        if not kafka_topic:
            logging.error('Kafka topic (EntityPath) not found in connection string')
            sys.exit(1)

        bridge = EnturNorwayBridge()
        bridge.feed(
            kafka_config=kafka_config,
            kafka_topic=kafka_topic,
            polling_interval=polling_interval,
            max_size=max_size,
        )
    else:
        parser.print_help()
