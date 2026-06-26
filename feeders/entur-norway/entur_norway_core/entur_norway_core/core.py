"""Transport-neutral SIRI acquisition and parsing for the Entur Norway bridge."""

import datetime


def _parse_iso_dt(s):
    """Parse ISO datetime, handling Z suffix for Python 3.10."""
    if s is None:
        return None
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))

import logging
import os
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple

import requests
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

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-entur-norway/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

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


def _topic_value(value: Optional[str]) -> str:
    value = (value or '').strip()
    if not value or any(char in value for char in ('/', '+', '#', '\x00')):
        return 'unknown'
    return value


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


class EnturNorwayBridge:
    """Polls Entur Norway SIRI feeds; transport-neutral acquisition and parsing."""

    SIRI_BASE = 'https://api.entur.io/realtime/v1/rest'
    CLIENT_NAME = 'real-time-sources/entur-norway'

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({'ET-Client-Name': self.CLIENT_NAME, 'User-Agent': USER_AGENT})
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
            aimed_arrival_time=_parse_iso_dt((call_el.findtext(_siri('AimedArrivalTime')) or None)) if (call_el.findtext(_siri('AimedArrivalTime')) or None) else None,  # type: ignore[attr-defined]
            expected_arrival_time=_parse_iso_dt((call_el.findtext(_siri('ExpectedArrivalTime')) or None)) if (call_el.findtext(_siri('ExpectedArrivalTime')) or None) else None,  # type: ignore[attr-defined]
            aimed_departure_time=_parse_iso_dt((call_el.findtext(_siri('AimedDepartureTime')) or None)) if (call_el.findtext(_siri('AimedDepartureTime')) or None) else None,  # type: ignore[attr-defined]
            expected_departure_time=_parse_iso_dt((call_el.findtext(_siri('ExpectedDepartureTime')) or None)) if (call_el.findtext(_siri('ExpectedDepartureTime')) or None) else None,  # type: ignore[attr-defined]
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
                        operating_day = _topic_value(framed_ref.findtext(_siri('DataFrameRef')) if framed_ref is not None else None)
                        service_journey_id = _topic_value(framed_ref.findtext(_siri('DatedVehicleJourneyRef')) if framed_ref is not None else None)

                        line_ref = _topic_value(jel.findtext(_siri('LineRef')))
                        operator_ref = _topic_value(jel.findtext(_siri('OperatorRef')))
                        if operator_ref == 'unknown' and service_journey_id != 'unknown' and ':' in service_journey_id:
                            operator_ref = _topic_value(service_journey_id.split(':')[0])

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
                            recorded_at_time=_parse_iso_dt((jel.findtext(_siri('RecordedAtTime')) or None)) if (jel.findtext(_siri('RecordedAtTime')) or None) else None,  # type: ignore[attr-defined]
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
                    operating_day = _topic_value(framed_ref.findtext(_siri('DataFrameRef')) if framed_ref is not None else None)
                    service_journey_id = _topic_value(framed_ref.findtext(_siri('DatedVehicleJourneyRef')) if framed_ref is not None else None)

                    line_ref = _topic_value(mvj_el.findtext(_siri('LineRef')))
                    operator_ref = _topic_value(mvj_el.findtext(_siri('OperatorRef')))
                    if operator_ref == 'unknown' and service_journey_id != 'unknown' and ':' in service_journey_id:
                        operator_ref = _topic_value(service_journey_id.split(':')[0])

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
                        recorded_at_time=_parse_iso_dt(recorded_at_time),  # type: ignore[attr-defined]
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
                    situation_number = _topic_value(sit_el.findtext(_siri('SituationNumber')))

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
                            start_time=_parse_iso_dt(start),  # type: ignore[attr-defined]
                            end_time=_parse_iso_dt(end.strip() if end else None),  # type: ignore[attr-defined]
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
                        creation_time=_parse_iso_dt(creation_time),  # type: ignore[attr-defined]
                        source_type=source_type,
                        source_name=source_name,
                        progress=(sit_el.findtext(_siri('Progress')) or None),
                        severity=_topic_value(sit_el.findtext(_siri('Severity'))),
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


__all__ = [
    "USER_AGENT",
    "SIRI_NS",
    "NS",
    "_siri",
    "_find_text",
    "_find_multilingual_text",
    "_bool_text",
    "_topic_value",
    "parse_duration_to_seconds",
    "_has_more_data",
    "EnturNorwayBridge",
]
