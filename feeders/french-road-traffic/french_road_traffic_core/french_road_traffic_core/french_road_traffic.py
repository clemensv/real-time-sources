"""Transport-neutral acquisition for French national road traffic feeds."""

from __future__ import annotations

import logging
import os
import xml.etree.ElementTree as ET
from typing import Any, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

LOGGER = logging.getLogger(__name__)
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-french-road-traffic/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com")
    + ")"
)
DATEX2_NS = "http://datex2.eu/schema/2/2_0"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
SOAP_NS = "http://www.w3.org/2003/05/soap-envelope"
TRAFFIC_FLOW_URL = "http://tipi.bison-fute.gouv.fr/bison-fute-ouvert/publicationsDIR/QTV-DIR/qtvDir.xml"
ROAD_EVENTS_URL = "http://tipi.bison-fute.gouv.fr/bison-fute-ouvert/publicationsDIR/Evenementiel-DIR/grt/RRN/content.xml"
FEED_SOURCE_FLOW = "https://transport.data.gouv.fr/datasets/etat-de-circulation-en-temps-reel-sur-le-reseau-national-routier-non-concede"
FEED_SOURCE_EVENTS = "https://transport.data.gouv.fr/datasets/evenements-routiers-sur-le-reseau-routier-national-non-concede"
DEFAULT_POLL_INTERVAL_SECONDS = 360
DEFAULT_HTTP_RETRY_TOTAL = 3
DEFAULT_REQUEST_TIMEOUT_SECONDS = 60


def _find(element: ET.Element, path: str, ns: Optional[str] = DATEX2_NS) -> Optional[ET.Element]:
    if ns:
        qualified = path.replace("/", f"/{{{ns}}}").replace("//", f"//{{{ns}}}") if "/" in path else f"{{{ns}}}{path}"
        return element.find(qualified)
    return element.find(path)


def _findall(element: ET.Element, path: str, ns: Optional[str] = DATEX2_NS) -> list[ET.Element]:
    if ns:
        qualified = path.replace("/", f"/{{{ns}}}").replace("//", f"//{{{ns}}}") if "/" in path else f"{{{ns}}}{path}"
        return element.findall(qualified)
    return element.findall(path)


def _text(element: ET.Element, path: str, ns: Optional[str] = DATEX2_NS) -> Optional[str]:
    found = _find(element, path, ns)
    return found.text if found is not None else None


def build_retrying_session() -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    retry = Retry(
        total=DEFAULT_HTTP_RETRY_TOTAL,
        connect=DEFAULT_HTTP_RETRY_TOTAL,
        read=DEFAULT_HTTP_RETRY_TOTAL,
        status=DEFAULT_HTTP_RETRY_TOTAL,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def parse_traffic_flow_xml(xml_bytes: bytes) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_bytes)
    payload = _find(root, "payloadPublication")
    if payload is None:
        return []

    results: list[dict[str, Any]] = []
    for site_measurement in _findall(payload, "siteMeasurements"):
        site_ref = _find(site_measurement, "measurementSiteReference")
        site_id = site_ref.get("id", "") if site_ref is not None else ""
        measurement_time = _text(site_measurement, "measurementTimeDefault")
        if not site_id or not measurement_time:
            continue

        flow_rate = None
        average_speed = None
        input_values_flow = None
        input_values_speed = None
        for measured_value in _findall(site_measurement, "measuredValue"):
            inner = _find(measured_value, "measuredValue")
            if inner is None:
                continue
            basic_data = _find(inner, "basicData")
            if basic_data is None:
                continue
            xsi_type = basic_data.get(f"{{{XSI_NS}}}type", "")
            if "TrafficFlow" in xsi_type:
                vehicle_flow = _find(basic_data, "vehicleFlow")
                if vehicle_flow is not None:
                    rate_text = _text(vehicle_flow, "vehicleFlowRate")
                    if rate_text is not None:
                        try:
                            flow_rate = int(rate_text)
                        except (TypeError, ValueError):
                            pass
                    input_count = vehicle_flow.get("numberOfInputValuesUsed")
                    if input_count is not None:
                        try:
                            input_values_flow = int(input_count)
                        except (TypeError, ValueError):
                            pass
            elif "TrafficSpeed" in xsi_type:
                average_vehicle_speed = _find(basic_data, "averageVehicleSpeed")
                if average_vehicle_speed is not None:
                    speed_text = _text(average_vehicle_speed, "speed")
                    if speed_text is not None:
                        try:
                            average_speed = float(speed_text)
                        except (TypeError, ValueError):
                            pass
                    input_count = average_vehicle_speed.get("numberOfInputValuesUsed")
                    if input_count is not None:
                        try:
                            input_values_speed = int(input_count)
                        except (TypeError, ValueError):
                            pass
        results.append(
            {
                "site_id": site_id,
                "measurement_time": measurement_time,
                "vehicle_flow_rate": flow_rate,
                "average_speed": average_speed,
                "input_values_flow": input_values_flow,
                "input_values_speed": input_values_speed,
            }
        )
    return results


def _extract_ns2_text(element: ET.Element, local_name: str) -> Optional[str]:
    child = element.find(f"{{{DATEX2_NS}}}{local_name}")
    return child.text if child is not None else None


def _extract_comments(record: ET.Element) -> tuple[Optional[str], Optional[str]]:
    description = None
    location_parts: list[str] = []
    for comment_element in _findall(record, "generalPublicComment"):
        comment_type = _text(comment_element, "commentType") or ""
        value_element = comment_element.find(f".//{{{DATEX2_NS}}}value")
        value_text = value_element.text if value_element is not None else None
        if comment_type == "description" and value_text:
            description = value_text
        elif comment_type == "locationDescriptor" and value_text:
            location_parts.append(value_text)
    return description, " | ".join(location_parts) if location_parts else None


def _extract_location(record: ET.Element) -> tuple[Optional[float], Optional[float], Optional[str], Optional[str], Optional[str]]:
    latitude = None
    longitude = None
    road_number = None
    town_name = None
    direction = None
    group = _find(record, "groupOfLocations")
    if group is None:
        return latitude, longitude, road_number, town_name, direction

    coordinates = group.find(f".//{{{DATEX2_NS}}}pointCoordinates")
    if coordinates is not None:
        lat_text = _extract_ns2_text(coordinates, "latitude")
        lon_text = _extract_ns2_text(coordinates, "longitude")
        if lat_text:
            try:
                latitude = float(lat_text)
            except (TypeError, ValueError):
                pass
        if lon_text:
            try:
                longitude = float(lon_text)
            except (TypeError, ValueError):
                pass

    road_element = group.find(f".//{{{DATEX2_NS}}}roadNumber")
    if road_element is not None and road_element.text:
        road_number = road_element.text
    direction_element = group.find(f".//{{{DATEX2_NS}}}tpegDirection")
    if direction_element is not None and direction_element.text:
        direction = direction_element.text
    for name_element in group.findall(f".//{{{DATEX2_NS}}}name"):
        descriptor_type = _text(name_element, "tpegOtherPointDescriptorType")
        value_element = name_element.find(f".//{{{DATEX2_NS}}}value")
        value_text = value_element.text if value_element is not None else None
        if descriptor_type == "townName" and value_text:
            town_name = value_text
            break
        if road_number is None and descriptor_type == "linkName" and value_text:
            road_number = value_text
    return latitude, longitude, road_number, town_name, direction


def parse_road_events_xml(xml_bytes: bytes) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_bytes)
    body = root.find(f"{{{SOAP_NS}}}Body")
    model = None
    if body is not None:
        model = body.find("d2LogicalModel") or body.find(f"{{{DATEX2_NS}}}d2LogicalModel")
        if model is None:
            for child in body:
                if "d2LogicalModel" in child.tag:
                    model = child
                    break
    else:
        model = root
    if model is None:
        return []

    payload = _find(model, "payloadPublication")
    if payload is None:
        for child in model:
            if "payloadPublication" in child.tag:
                payload = child
                break
    if payload is None:
        return []

    results: list[dict[str, Any]] = []
    for situation in _findall(payload, "situation"):
        situation_id = situation.get("id", "")
        situation_version = situation.get("version", "")
        severity = _extract_ns2_text(situation, "overallSeverity")
        for record in _findall(situation, "situationRecord"):
            record_id = record.get("id", "")
            record_type_raw = record.get(f"{{{XSI_NS}}}type", "")
            record_type = record_type_raw.split(":")[-1] if ":" in record_type_raw else record_type_raw
            creation_time = _extract_ns2_text(record, "situationRecordCreationTime") or ""
            observation_time = _extract_ns2_text(record, "situationRecordObservationTime")
            probability = _extract_ns2_text(record, "probabilityOfOccurrence")
            source_name = None
            source = _find(record, "source")
            if source is not None:
                source_name = _extract_ns2_text(source, "sourceIdentification")
            validity = _find(record, "validity")
            validity_status = None
            overall_start_time = None
            overall_end_time = None
            if validity is not None:
                validity_status = _extract_ns2_text(validity, "validityStatus")
                validity_time = _find(validity, "validityTimeSpecification")
                if validity_time is not None:
                    overall_start_time = _extract_ns2_text(validity_time, "overallStartTime")
                    overall_end_time = _extract_ns2_text(validity_time, "overallEndTime")
            description, location_description = _extract_comments(record)
            latitude, longitude, road_number, town_name, direction = _extract_location(record)
            if not situation_id or not record_id or not creation_time:
                continue
            results.append(
                {
                    "situation_id": situation_id,
                    "record_id": record_id,
                    "version": situation_version,
                    "severity": severity,
                    "record_type": record_type,
                    "probability": probability,
                    "latitude": latitude,
                    "longitude": longitude,
                    "road_number": road_number,
                    "town_name": town_name,
                    "direction": direction,
                    "description": description,
                    "location_description": location_description,
                    "source_name": source_name,
                    "validity_status": validity_status,
                    "overall_start_time": overall_start_time,
                    "overall_end_time": overall_end_time,
                    "creation_time": creation_time,
                    "observation_time": observation_time,
                }
            )
    return results


def normalize_road_segment(value: Any) -> str:
    text = str(value or "unknown").strip() or "unknown"
    for forbidden in ("/", "+", "#", "\x00"):
        text = text.replace(forbidden, "-")
    return "-".join(text.split()) or "unknown"


class FrenchRoadTrafficSource:
    def __init__(self, session: Optional[requests.Session] = None, timeout: int = DEFAULT_REQUEST_TIMEOUT_SECONDS) -> None:
        self.session = session or build_retrying_session()
        self.timeout = timeout

    def fetch_xml(self, url: str, timeout: Optional[int] = None) -> bytes:
        response = self.session.get(url, timeout=timeout or self.timeout)
        response.raise_for_status()
        return response.content

    def fetch_traffic_flow(self, url: str = TRAFFIC_FLOW_URL) -> list[dict[str, Any]]:
        return parse_traffic_flow_xml(self.fetch_xml(url))

    def fetch_road_events(self, url: str = ROAD_EVENTS_URL) -> list[dict[str, Any]]:
        return parse_road_events_xml(self.fetch_xml(url))


__all__ = [
    "DATEX2_NS",
    "DEFAULT_HTTP_RETRY_TOTAL",
    "DEFAULT_POLL_INTERVAL_SECONDS",
    "DEFAULT_REQUEST_TIMEOUT_SECONDS",
    "FEED_SOURCE_EVENTS",
    "FEED_SOURCE_FLOW",
    "FrenchRoadTrafficSource",
    "LOGGER",
    "ROAD_EVENTS_URL",
    "SOAP_NS",
    "TRAFFIC_FLOW_URL",
    "USER_AGENT",
    "XSI_NS",
    "_extract_comments",
    "_extract_location",
    "_find",
    "_findall",
    "_text",
    "build_retrying_session",
    "normalize_road_segment",
    "parse_road_events_xml",
    "parse_traffic_flow_xml",
]
