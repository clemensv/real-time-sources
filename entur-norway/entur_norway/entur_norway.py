"""Entur Norway national real-time transit SIRI bridge to Apache Kafka."""

import argparse
import datetime
import logging
import os
import re
import sys
import time
import uuid
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple

import requests
from confluent_kafka import Producer
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from entur_norway_producer_data import (
    DatedServiceJourney,
    EstimatedCall,
    EstimatedVehicleJourney,
    MonitoredVehicleJourney,
    PtSituationElement,
    ValidityPeriod,
)
from entur_norway_producer_kafka_producer.producer import (
    NoEnturJourneysEventProducer,
    NoEnturSituationsEventProducer,
)

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

SIRI_NS = 'http://www.siri.org.uk/siri'
NS = {'s': SIRI_NS}


def _siri(local_name: str) -> str:
    """Return Clark-notation SIRI tag."""
    return f'{{{SIRI_NS}}}{local_name}'


def _find_text(element: ET.Element, path: str) -> Optional[str]:
    """Find element text via namespace-prefixed path, return None if not found."""
    el = element.find(path, NS)
    return el.text.strip() if el is not None and el.text else None


def _find_multilingual_text(element: ET.Element, tag: str) -> Optional[str]:
    """Pick English text first; fall back to first occurrence."""
    els = element.findall(f's:{tag}', NS)
    if not els:
        return None
    for el in els:
        lang = el.get('{http://www.w3.org/XML/1998/namespace}lang', '')
        if lang.lower() in ('en', 'eng'):
            return el.text.strip() if el.text else None
    return els[0].text.strip() if els[0].text else None


def _bool_text(text: Optional[str]) -> Optional[bool]:
    """Convert a string 'true'/'false' to bool, returning None if absent."""
    if text is None:
        return None
    return text.strip().lower() in ('true', '1')


def parse_duration_to_seconds(duration: Optional[str]) -> Optional[int]:
    """Parse an ISO 8601 duration string like PT2M30S or -PT2M into total seconds."""
    if not duration:
        return None
    duration = duration.strip()
    negative = duration.startswith('-')
    duration = duration.lstrip('-')
    match = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?').match(duration)
    if not match:
        return None
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(float(match.group(3) or 0))
    total = hours * 3600 + minutes * 60 + seconds
    return -total if negative else total


def _has_more_data(root: ET.Element) -> bool:
    """Return True if the SIRI response indicates more pages are available."""
    more = root.find('s:ServiceDelivery/s:MoreData', NS)
    return more is not None and more.text is not None and more.text.strip().lower() == 'true'


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


class EnturNorwayBridge:
    """Polls Entur Norway SIRI feeds and emits CloudEvents to Kafka."""

    SIRI_BASE = 'https://api.entur.io/realtime/v1/rest'
    CLIENT_NAME = 'real-time-sources/entur-norway'

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({'ET-Client-Name': self.CLIENT_NAME})
        retry = Retry(
            total=3,
            connect=3,
            read=3,
            status=3,
            backoff_factor=1,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({'GET'}),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        return session

    def fetch_siri(
        self,
        feed: str,
        requestor_id: Optional[str] = None,
        max_size: int = 1000,
    ) -> Optional[ET.Element]:
        """Fetch a SIRI feed and return the parsed XML root, or None on error."""
        url = f'{self.SIRI_BASE}/{feed}'
        params: Dict[str, str] = {'maxSize': str(max_size)}
        if requestor_id:
            params['requestorId'] = requestor_id
        try:
            resp = self.session.get(url, params=params, timeout=60)
            resp.raise_for_status()
            return ET.fromstring(resp.content)
        except Exception as exc:
            logging.error('Error fetching SIRI %s: %s', feed, exc)
            return None

    def _parse_estimated_call(self, call_el: ET.Element) -> Optional[EstimatedCall]:
        """Parse a single EstimatedCall XML element into a data object."""
        stop_ref = (call_el.findtext(_siri('StopPointRef')) or '').strip()
        if not stop_ref:
            return None
        order_text = (call_el.findtext(_siri('Order')) or '0').strip()
        try:
            order = int(order_text)
        except ValueError:
            order = 0

        cancel_text = (call_el.findtext(_siri('Cancellation')) or '').strip().lower()
        extra_text = (call_el.findtext(_siri('ExtraCall')) or '').strip().lower()

        return EstimatedCall(
            stop_point_ref=stop_ref,
            order=order,
            stop_point_name=_find_multilingual_text(call_el, 'StopPointName'),
            aimed_arrival_time=(call_el.findtext(_siri('AimedArrivalTime')) or None),
            expected_arrival_time=(call_el.findtext(_siri('ExpectedArrivalTime')) or None),
            aimed_departure_time=(call_el.findtext(_siri('AimedDepartureTime')) or None),
            expected_departure_time=(call_el.findtext(_siri('ExpectedDepartureTime')) or None),
            arrival_status=(call_el.findtext(_siri('ArrivalStatus')) or None),
            departure_status=(call_el.findtext(_siri('DepartureStatus')) or None),
            departure_platform_name=_find_multilingual_text(call_el, 'DeparturePlatformName'),
            arrival_boarding_activity=(call_el.findtext(_siri('ArrivalBoardingActivity')) or None),
            departure_boarding_activity=(call_el.findtext(_siri('DepartureBoardingActivity')) or None),
            is_cancellation=bool(cancel_text in ('true', '1')) if cancel_text else None,
            is_extra_stop=bool(extra_text in ('true', '1')) if extra_text else None,
        )

    def parse_et_journeys(
        self, root: ET.Element
    ) -> List[Tuple[str, str, EstimatedVehicleJourney]]:
        """Parse EstimatedVehicleJourney elements from an ET SIRI response.

        Returns a list of (operating_day, service_journey_id, EstimatedVehicleJourney).
        """
        results: List[Tuple[str, str, EstimatedVehicleJourney]] = []
        for delivery in root.findall('.//s:EstimatedTimetableDelivery', NS):
            for frame in delivery.findall('.//s:EstimatedJourneyVersionFrame', NS):
                for jel in frame.findall('s:EstimatedVehicleJourney', NS):
                    try:
                        framed_ref = jel.find('s:FramedVehicleJourneyRef', NS)
                        if framed_ref is None:
                            continue
                        operating_day = (framed_ref.findtext(_siri('DataFrameRef')) or '').strip()
                        service_journey_id = (framed_ref.findtext(_siri('DatedVehicleJourneyRef')) or '').strip()
                        if not service_journey_id or not operating_day:
                            continue

                        line_ref = (jel.findtext(_siri('LineRef')) or '').strip()
                        operator_ref = (jel.findtext(_siri('OperatorRef')) or '').strip()
                        if not operator_ref and service_journey_id and ':' in service_journey_id:
                            operator_ref = service_journey_id.split(':')[0]

                        cancel_text = (jel.findtext(_siri('Cancellation')) or 'false').strip().lower()
                        is_cancellation = cancel_text in ('true', '1')

                        estimated_calls: List[EstimatedCall] = []
                        for call_el in jel.findall('.//s:EstimatedCall', NS):
                            call = self._parse_estimated_call(call_el)
                            if call:
                                estimated_calls.append(call)

                        evj = EstimatedVehicleJourney(
                            service_journey_id=service_journey_id,
                            operating_day=operating_day,
                            line_ref=line_ref,
                            operator_ref=operator_ref,
                            direction_ref=(jel.findtext(_siri('DirectionRef')) or None),
                            vehicle_mode=(jel.findtext(_siri('VehicleMode')) or None),
                            published_line_name=_find_multilingual_text(jel, 'PublishedLineName'),
                            route_ref=(jel.findtext(_siri('RouteRef')) or None),
                            origin_name=_find_multilingual_text(jel, 'OriginName'),
                            destination_name=_find_multilingual_text(jel, 'DestinationName'),
                            is_cancellation=is_cancellation,
                            is_extra_journey=_bool_text(jel.findtext(_siri('ExtraJourney'))),
                            is_complete_stop_sequence=_bool_text(jel.findtext(_siri('IsCompleteStopSequence'))),
                            monitored=_bool_text(jel.findtext(_siri('Monitored'))),
                            data_source=(jel.findtext(_siri('DataSource')) or None),
                            recorded_at_time=(jel.findtext(_siri('RecordedAtTime')) or None),
                            estimated_calls=estimated_calls,
                        )
                        results.append((operating_day, service_journey_id, evj))
                    except Exception as exc:
                        logging.debug('Error parsing EstimatedVehicleJourney: %s', exc)
        return results

    def parse_vm_journeys(
        self, root: ET.Element
    ) -> List[Tuple[str, str, MonitoredVehicleJourney]]:
        """Parse MonitoredVehicleJourney elements from a VM SIRI response.

        Returns a list of (operating_day, service_journey_id, MonitoredVehicleJourney).
        """
        results: List[Tuple[str, str, MonitoredVehicleJourney]] = []
        for delivery in root.findall('.//s:VehicleMonitoringDelivery', NS):
            for activity_el in delivery.findall('s:VehicleActivity', NS):
                try:
                    recorded_at_time = (activity_el.findtext(_siri('RecordedAtTime')) or '').strip()
                    mvj_el = activity_el.find('s:MonitoredVehicleJourney', NS)
                    if mvj_el is None:
                        continue

                    framed_ref = mvj_el.find('s:FramedVehicleJourneyRef', NS)
                    if framed_ref is None:
                        continue
                    operating_day = (framed_ref.findtext(_siri('DataFrameRef')) or '').strip()
                    service_journey_id = (framed_ref.findtext(_siri('DatedVehicleJourneyRef')) or '').strip()
                    if not service_journey_id or not operating_day:
                        continue

                    line_ref = (mvj_el.findtext(_siri('LineRef')) or '').strip()
                    operator_ref = (mvj_el.findtext(_siri('OperatorRef')) or '').strip()
                    if not line_ref:
                        continue

                    lat: Optional[float] = None
                    lon: Optional[float] = None
                    loc_el = mvj_el.find('s:VehicleLocation', NS)
                    if loc_el is not None:
                        lat_text = loc_el.findtext(_siri('Latitude'))
                        lon_text = loc_el.findtext(_siri('Longitude'))
                        try:
                            lat = float(lat_text) if lat_text else None
                        except (ValueError, TypeError):
                            lat = None
                        try:
                            lon = float(lon_text) if lon_text else None
                        except (ValueError, TypeError):
                            lon = None

                    bearing_text = mvj_el.findtext(_siri('Bearing'))
                    try:
                        bearing: Optional[float] = float(bearing_text) if bearing_text else None
                    except (ValueError, TypeError):
                        bearing = None

                    delay_seconds = parse_duration_to_seconds(mvj_el.findtext(_siri('Delay')))

                    monitored_text = (mvj_el.findtext(_siri('Monitored')) or 'false').strip().lower()
                    monitored = monitored_text in ('true', '1')

                    if not recorded_at_time:
                        logging.warning(
                            'VehicleActivity missing RecordedAtTime for %s/%s; using current time',
                            operating_day, service_journey_id,
                        )
                        recorded_at_time = datetime.datetime.now(datetime.timezone.utc).isoformat()

                    mvj = MonitoredVehicleJourney(
                        service_journey_id=service_journey_id,
                        operating_day=operating_day,
                        recorded_at_time=recorded_at_time,
                        line_ref=line_ref,
                        operator_ref=operator_ref,
                        direction_ref=(mvj_el.findtext(_siri('DirectionRef')) or None),
                        vehicle_mode=(mvj_el.findtext(_siri('VehicleMode')) or None),
                        published_line_name=_find_multilingual_text(mvj_el, 'PublishedLineName'),
                        origin_name=_find_multilingual_text(mvj_el, 'OriginName'),
                        destination_name=_find_multilingual_text(mvj_el, 'DestinationName'),
                        vehicle_ref=(mvj_el.findtext(_siri('VehicleRef')) or None),
                        latitude=lat,
                        longitude=lon,
                        bearing=bearing,
                        delay_seconds=delay_seconds,
                        occupancy_status=(mvj_el.findtext(_siri('OccupancyStatus')) or None),
                        progress_status=(mvj_el.findtext(_siri('ProgressStatus')) or None),
                        monitored=monitored,
                    )
                    results.append((operating_day, service_journey_id, mvj))
                except Exception as exc:
                    logging.debug('Error parsing MonitoredVehicleJourney: %s', exc)
        return results

    def parse_sx_situations(
        self, root: ET.Element
    ) -> List[Tuple[str, PtSituationElement]]:
        """Parse PtSituationElement records from an SX SIRI response.

        Returns a list of (situation_number, PtSituationElement).
        """
        results: List[Tuple[str, PtSituationElement]] = []
        for delivery in root.findall('.//s:SituationExchangeDelivery', NS):
            situations_el = delivery.find('s:Situations', NS)
            if situations_el is None:
                continue
            for sit_el in situations_el.findall('s:PtSituationElement', NS):
                try:
                    situation_number = (sit_el.findtext(_siri('SituationNumber')) or '').strip()
                    if not situation_number:
                        continue

                    creation_time_raw = sit_el.findtext(_siri('CreationTime'))
                    if not creation_time_raw:
                        logging.warning(
                            'PtSituationElement %s missing CreationTime; using current time',
                            situation_number,
                        )
                        creation_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
                    else:
                        creation_time = creation_time_raw

                    validity_periods: List[ValidityPeriod] = []
                    for vp_el in sit_el.findall('s:ValidityPeriod', NS):
                        start = vp_el.findtext(_siri('StartTime')) or ''
                        end = vp_el.findtext(_siri('EndTime'))
                        validity_periods.append(ValidityPeriod(
                            start_time=start,
                            end_time=end.strip() if end else None,
                        ))

                    affects_line_refs: List[str] = []
                    affects_stop_refs: List[str] = []
                    affects_el = sit_el.find('s:Affects', NS)
                    if affects_el is not None:
                        for line_el in affects_el.findall('.//s:AffectedLine/s:LineRef', NS):
                            if line_el.text:
                                affects_line_refs.append(line_el.text.strip())
                        for stop_el in affects_el.findall('.//s:AffectedStopPoint/s:StopPointRef', NS):
                            if stop_el.text:
                                affects_stop_refs.append(stop_el.text.strip())

                    source_el = sit_el.find('s:Source', NS)
                    source_type: Optional[str] = None
                    source_name: Optional[str] = None
                    if source_el is not None:
                        source_type = (source_el.findtext(_siri('SourceType')) or None)
                        source_name = (source_el.findtext(_siri('Name')) or None)

                    sit = PtSituationElement(
                        situation_number=situation_number,
                        version=(sit_el.findtext(_siri('Version')) or None),
                        creation_time=creation_time,
                        source_type=source_type,
                        source_name=source_name,
                        progress=(sit_el.findtext(_siri('Progress')) or None),
                        severity=(sit_el.findtext(_siri('Severity')) or None),
                        keywords=(sit_el.findtext(_siri('Keywords')) or None),
                        summary=_find_multilingual_text(sit_el, 'Summary'),
                        description=_find_multilingual_text(sit_el, 'Description'),
                        validity_periods=validity_periods,
                        affects_line_refs=affects_line_refs,
                        affects_stop_point_refs=affects_stop_refs,
                    )
                    results.append((situation_number, sit))
                except Exception as exc:
                    logging.debug('Error parsing PtSituationElement: %s', exc)
        return results

    def extract_reference_journeys(
        self,
        et_journeys: List[Tuple[str, str, EstimatedVehicleJourney]],
    ) -> List[Tuple[str, str, DatedServiceJourney]]:
        """Derive unique DatedServiceJourney reference records from ET journeys."""
        seen: set = set()
        results: List[Tuple[str, str, DatedServiceJourney]] = []
        for op_day, sj_id, evj in et_journeys:
            key = (op_day, sj_id)
            if key in seen:
                continue
            seen.add(key)
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
            results.append((op_day, sj_id, dsj))
        return results

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
