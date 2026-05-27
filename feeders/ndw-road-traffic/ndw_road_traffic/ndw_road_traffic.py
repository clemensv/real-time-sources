"""NDW Netherlands Road Traffic bridge.

Polls gzip-compressed DATEX II XML files from the Dutch NDW open-data
platform and emits CloudEvents for traffic speed, travel time, situations,
DRIP, and MSI sign data onto Kafka topics.
"""

from __future__ import annotations

import argparse
import gzip
import json
import logging
import os
import sys
import time
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from confluent_kafka import Producer

from ndw_road_traffic_producer_data import (
    PointMeasurementSite,
    RouteMeasurementSite,
    TrafficObservation,
    TravelTimeObservation,
    DripSign,
    DripDisplayState,
    MsiSign,
    MsiDisplayState,
    Roadwork,
    BridgeOpening,
    TemporaryClosure,
    TemporarySpeedLimit,
    SafetyRelatedMessage,
)
from ndw_road_traffic_producer_kafka_producer.producer import (
    NLNDWAVGEventProducer,
    NLNDWDRIPEventProducer,
    NLNDWMSIEventProducer,
    NLNDWSituationsEventProducer,
)

BASE_URL = "https://opendata.ndw.nu"
MEASUREMENT_CURRENT_FILE = "measurement_current.xml.gz"
SPEED_FILE = "trafficspeed.xml.gz"
TRAVELTIME_FILE = "traveltime.xml.gz"
DRIP_FILE = "dynamische_route_informatie_paneel.xml.gz"
MSI_FILE = "Matrixsignaalinformatie.xml.gz"

SITUATION_FEEDS: List[Tuple[str, str]] = [
    ("planningsfeed_wegwerkzaamheden_en_evenementen.xml.gz", "roadwork"),
    ("planningsfeed_brugopeningen.xml.gz", "bridge_opening"),
    ("tijdelijke_verkeersmaatregelen_afsluitingen.xml.gz", "temporary_closure"),
    ("tijdelijke_verkeersmaatregelen_maximum_snelheden.xml.gz", "temporary_speed_limit"),
    ("veiligheidsgerelateerde_berichten_srti.xml.gz", "safety_related_message"),
]

DEFAULT_TOPIC = "ndw-road-traffic"
DEFAULT_POLL_INTERVAL_SECONDS = 60
DEFAULT_REFERENCE_REFRESH_SECONDS = 3600
DEFAULT_SITUATION_INTERVAL_SECONDS = 300
DEFAULT_STATE_FILE = os.path.expanduser("~/.ndw_road_traffic_state.json")
REFERENCE_FLUSH_BATCH_SIZE = 200
DEFAULT_MAX_RECORDS_PER_FAMILY: Optional[int] = None

# DATEX II v2 namespaces (trafficspeed, traveltime)
DATEX2_V2 = "http://datex2.eu/schema/2/2_0"

# DATEX II v3 namespaces
D3_COM = "http://datex2.eu/schema/3/common"
D3_MST = "http://datex2.eu/schema/3/measurementSiteTable"
D3_VMS = "http://datex2.eu/schema/3/vms"
D3_SIT = "http://datex2.eu/schema/3/situation"
D3_MC = "http://datex2.eu/schema/3/messageContainer"
XSI = "http://www.w3.org/2001/XMLSchema-instance"

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _make_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def download_gzip_xml(session: requests.Session, url: str, timeout: int = 120) -> bytes:
    resp = session.get(url, timeout=timeout)
    resp.raise_for_status()
    return gzip.decompress(resp.content)


# ---------------------------------------------------------------------------
# Connection string / Kafka helpers
# ---------------------------------------------------------------------------

def parse_connection_string(connection_string: str) -> Dict[str, str]:
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=", 1)[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                config_dict["entity_path"] = part.split("=", 1)[1].strip('"')
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = part.split("=", 1)[1].strip('"')
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = part.split("=", 1)[1].strip('"')
    except (IndexError, ValueError) as exc:
        raise ValueError("Invalid connection string format") from exc
    return config_dict


def _build_kafka_config(connection_string: str, enable_tls: bool = True) -> Tuple[Dict[str, str], Optional[str]]:
    topic: Optional[str] = None

    if "BootstrapServer=" in connection_string:
        parts: Dict[str, str] = {}
        for part in connection_string.split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                parts[k.strip()] = v.strip().strip('"')
        config: Dict[str, str] = {"bootstrap.servers": parts.get("BootstrapServer", "")}
        topic = parts.get("EntityPath")
    else:
        parsed = parse_connection_string(connection_string)
        config = {
            "bootstrap.servers": parsed.get("bootstrap.servers", ""),
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "sasl.username": "$ConnectionString",
            "sasl.password": connection_string.strip(),
        }
        topic = parsed.get("entity_path")

    if not enable_tls and "security.protocol" not in config:
        config["security.protocol"] = "PLAINTEXT"

    return config, topic


# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------

def _text(elem: Optional[ET.Element], tag: str, ns: str) -> Optional[str]:
    if elem is None:
        return None
    node = elem.find(f"{{{ns}}}{tag}")
    return node.text.strip() if node is not None and node.text else None


def _local(tag: str) -> str:
    """Return local name stripping any namespace."""
    return tag.split("}")[-1] if "}" in tag else tag


def _find_by_local(elem: ET.Element, local_name: str) -> Optional[ET.Element]:
    for child in elem:
        if _local(child.tag) == local_name:
            return child
    return None


def _iter_by_local(root: ET.Element, local_name: str):
    for elem in root.iter():
        if _local(elem.tag) == local_name:
            yield elem


# ---------------------------------------------------------------------------
# DATEX II v2 parsers (trafficspeed + traveltime)
# ---------------------------------------------------------------------------

def parse_traffic_speed_xml(xml_bytes: bytes) -> List[Dict[str, Any]]:
    root = ET.fromstring(xml_bytes)
    results: List[Dict[str, Any]] = []

    for sm in root.iter(f"{{{DATEX2_V2}}}siteMeasurements"):
        ref = sm.find(f"{{{DATEX2_V2}}}measurementSiteReference")
        if ref is None:
            continue
        site_id = ref.get("id", "")
        time_elem = sm.find(f"{{{DATEX2_V2}}}measurementTimeDefault")
        mtime = time_elem.text.strip() if time_elem is not None and time_elem.text else ""

        speeds: List[float] = []
        flows: List[int] = []

        for mv in sm.findall(f"{{{DATEX2_V2}}}measuredValue"):
            inner = mv.find(f"{{{DATEX2_V2}}}measuredValue")
            if inner is None:
                continue
            bd = inner.find(f"{{{DATEX2_V2}}}basicData")
            if bd is None:
                continue
            xsi_type = bd.get(f"{{{XSI}}}type", "")
            if xsi_type == "TrafficSpeed":
                avg_elem = bd.find(f"{{{DATEX2_V2}}}averageVehicleSpeed")
                if avg_elem is not None:
                    spd_elem = avg_elem.find(f"{{{DATEX2_V2}}}speed")
                    if spd_elem is not None and spd_elem.text:
                        val = float(spd_elem.text)
                        if val > 0:
                            speeds.append(val)
            elif xsi_type == "TrafficFlow":
                vf_elem = bd.find(f"{{{DATEX2_V2}}}vehicleFlow")
                if vf_elem is not None:
                    rate_elem = vf_elem.find(f"{{{DATEX2_V2}}}vehicleFlowRate")
                    if rate_elem is not None and rate_elem.text:
                        flows.append(int(rate_elem.text))

        lanes = max(len(speeds), len(flows))
        avg_speed: Optional[float] = round(sum(speeds) / len(speeds), 2) if speeds else None
        total_flow: Optional[int] = sum(flows) if flows else None

        results.append({
            "measurement_site_id": site_id,
            "measurement_time": mtime,
            "average_speed": avg_speed,
            "vehicle_flow_rate": total_flow,
            "number_of_lanes_with_data": lanes,
        })

    return results


def parse_travel_time_xml(xml_bytes: bytes) -> List[Dict[str, Any]]:
    root = ET.fromstring(xml_bytes)
    results: List[Dict[str, Any]] = []

    for sm in root.iter(f"{{{DATEX2_V2}}}siteMeasurements"):
        ref = sm.find(f"{{{DATEX2_V2}}}measurementSiteReference")
        if ref is None:
            continue
        site_id = ref.get("id", "")
        time_elem = sm.find(f"{{{DATEX2_V2}}}measurementTimeDefault")
        mtime = time_elem.text.strip() if time_elem is not None and time_elem.text else ""

        duration: Optional[float] = None
        ref_duration: Optional[float] = None
        accuracy: Optional[float] = None
        data_quality: Optional[float] = None
        n_input: Optional[int] = None

        for mv in sm.findall(f"{{{DATEX2_V2}}}measuredValue"):
            inner = mv.find(f"{{{DATEX2_V2}}}measuredValue")
            if inner is None:
                continue
            bd = inner.find(f"{{{DATEX2_V2}}}basicData")
            if bd is None:
                continue
            xsi_type = bd.get(f"{{{XSI}}}type", "")
            if xsi_type != "TravelTimeData":
                continue

            tt_elem = bd.find(f"{{{DATEX2_V2}}}travelTime")
            if tt_elem is not None:
                dur_elem = tt_elem.find(f"{{{DATEX2_V2}}}duration")
                if dur_elem is not None and dur_elem.text:
                    val = float(dur_elem.text)
                    duration = val if val >= 0 else None
                acc_val = tt_elem.get("accuracy")
                if acc_val is not None:
                    accuracy = float(acc_val)
                niv = tt_elem.get("numberOfInputValuesUsed")
                if niv is not None:
                    n_input = int(niv)
                dq_val = tt_elem.get("supplierCalculatedDataQuality")
                if dq_val is not None:
                    data_quality = float(dq_val)

            ext = inner.find(f"{{{DATEX2_V2}}}measuredValueExtension")
            if ext is not None:
                ext2 = ext.find(f"{{{DATEX2_V2}}}measuredValueExtended")
                if ext2 is not None:
                    brv = ext2.find(f"{{{DATEX2_V2}}}basicDataReferenceValue")
                    if brv is not None:
                        ttd = brv.find(f"{{{DATEX2_V2}}}travelTimeData")
                        if ttd is not None:
                            rtt = ttd.find(f"{{{DATEX2_V2}}}travelTime")
                            if rtt is not None:
                                rd = rtt.find(f"{{{DATEX2_V2}}}duration")
                                if rd is not None and rd.text:
                                    rdv = float(rd.text)
                                    ref_duration = rdv if rdv >= 0 else None

        results.append({
            "measurement_site_id": site_id,
            "measurement_time": mtime,
            "duration": duration,
            "reference_duration": ref_duration,
            "accuracy": accuracy,
            "data_quality": data_quality,
            "number_of_input_values": n_input,
        })

    return results


# ---------------------------------------------------------------------------
# DATEX II v3 parser – measurement sites
# ---------------------------------------------------------------------------

def _parse_coords_v3(site_rec: ET.Element) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]:
    """Extract lat/lon from a DATEX II v3 measurementSiteRecord element.

    Returns (lat, lon, None, None) for point sites, (start_lat, start_lon, end_lat, end_lon) for routes.
    """
    lat = lon = None
    start_lat = start_lon = end_lat = end_lon = None

    # Try to find coordinates in any sub-element
    for elem in site_rec.iter():
        local = _local(elem.tag)
        if local == "latitude" and elem.text:
            try:
                lat = float(elem.text)
                start_lat = lat
            except ValueError:
                pass
        elif local == "longitude" and elem.text:
            try:
                lon = float(elem.text)
                start_lon = lon
            except ValueError:
                pass

    # For route sites, try to find start/end pairs
    coords_list: List[Tuple[float, float]] = []
    for pc in _iter_by_local(site_rec, "pointCoordinates"):
        lat_e = _find_by_local(pc, "latitude")
        lon_e = _find_by_local(pc, "longitude")
        if lat_e is not None and lon_e is not None and lat_e.text and lon_e.text:
            try:
                coords_list.append((float(lat_e.text), float(lon_e.text)))
            except ValueError:
                pass

    if len(coords_list) >= 2:
        start_lat, start_lon = coords_list[0]
        end_lat, end_lon = coords_list[-1]
    elif len(coords_list) == 1:
        lat, lon = coords_list[0]
        start_lat, start_lon = lat, lon

    return lat, lon, start_lat, start_lon, end_lat, end_lon


def parse_measurement_site_xml(xml_bytes: bytes) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Parse measurement_current DATEX II v3 XML into point and route site dicts."""
    root = ET.fromstring(xml_bytes)
    point_sites: List[Dict[str, Any]] = []
    route_sites: List[Dict[str, Any]] = []

    for sr in _iter_by_local(root, "measurementSiteRecord"):
        site_id = sr.get("id", "") or sr.get(f"{{{D3_MST}}}id", "")
        if not site_id:
            continue

        xsi_type = sr.get(f"{{{XSI}}}type", "")
        is_route = "Route" in xsi_type or "route" in xsi_type.lower()

        # Name
        name: Optional[str] = None
        for elem in _iter_by_local(sr, "measurementSiteName"):
            for child in elem.iter():
                if _local(child.tag) in ("value", "name") and child.text:
                    name = child.text.strip()
                    break
            if name:
                break

        # Equipment type
        eq_type: Optional[str] = None
        for elem in _iter_by_local(sr, "measurementEquipmentTypeUsed"):
            if elem.text:
                eq_type = elem.text.strip()
                break

        # Period
        period: Optional[int] = None
        for elem in _iter_by_local(sr, "period"):
            if elem.text:
                try:
                    period = int(float(elem.text))
                except ValueError:
                    pass
                break

        # Road name
        road_name: Optional[str] = None
        for elem in _iter_by_local(sr, "roadName"):
            for child in elem.iter():
                if _local(child.tag) == "value" and child.text:
                    road_name = child.text.strip()
                    break
            if road_name:
                break

        # Carriageway type
        cw_type: Optional[str] = None
        for elem in _iter_by_local(sr, "carriageWayType"):
            if elem.text:
                cw_type = elem.text.strip()
                break

        # Lane count
        lane_count: Optional[int] = 0
        lane_elems = list(_iter_by_local(sr, "measurementSpecificCharacteristics"))
        if lane_elems:
            lane_count = len(lane_elems)

        # Coordinates
        coords = _parse_coords_v3(sr)
        lat, lon = coords[0], coords[1]
        start_lat, start_lon = coords[2], coords[3]
        end_lat, end_lon = coords[4], coords[5]

        # Length
        length: Optional[float] = None
        for elem in _iter_by_local(sr, "length"):
            if elem.text:
                try:
                    length = float(elem.text)
                except ValueError:
                    pass
                break

        if is_route:
            route_sites.append({
                "measurement_site_id": site_id,
                "name": name,
                "measurement_site_type": eq_type,
                "period": period,
                "start_latitude": start_lat,
                "start_longitude": start_lon,
                "end_latitude": end_lat,
                "end_longitude": end_lon,
                "road_name": road_name,
                "length_metres": length,
            })
        else:
            point_sites.append({
                "measurement_site_id": site_id,
                "name": name,
                "measurement_site_type": eq_type,
                "period": period,
                "latitude": lat,
                "longitude": lon,
                "road_name": road_name,
                "lane_count": lane_count if lane_count else None,
                "carriageway_type": cw_type,
            })

    return point_sites, route_sites


# ---------------------------------------------------------------------------
# DATEX II v3 parser – DRIP (VMS)
# ---------------------------------------------------------------------------

def parse_drip_xml(xml_bytes: bytes) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Parse DRIP DATEX II v3 XML into DripSign and DripDisplayState dicts."""
    root = ET.fromstring(xml_bytes)
    signs: List[Dict[str, Any]] = []
    states: List[Dict[str, Any]] = []

    # Publication time
    pub_time: Optional[str] = None
    for elem in _iter_by_local(root, "publicationTime"):
        if elem.text:
            pub_time = elem.text.strip()
            break
    if pub_time is None:
        pub_time = ""

    for controller in _iter_by_local(root, "vmsUnitRecord"):
        controller_id = controller.get("id", "")
        if not controller_id:
            controller_id = controller.get(f"{{{D3_VMS}}}id", "")
        if not controller_id:
            continue

        # Location for the controller (used for individual signs too)
        ctrl_lat: Optional[float] = None
        ctrl_lon: Optional[float] = None
        for pc in _iter_by_local(controller, "pointCoordinates"):
            lat_e = _find_by_local(pc, "latitude")
            lon_e = _find_by_local(pc, "longitude")
            if lat_e is not None and lon_e is not None and lat_e.text and lon_e.text:
                try:
                    ctrl_lat = float(lat_e.text)
                    ctrl_lon = float(lon_e.text)
                except ValueError:
                    pass
                break

        # Road name
        ctrl_road: Optional[str] = None
        for elem in _iter_by_local(controller, "roadName"):
            for child in elem.iter():
                if _local(child.tag) == "value" and child.text:
                    ctrl_road = child.text.strip()
                    break
            if ctrl_road:
                break

        # Description
        ctrl_desc: Optional[str] = None
        for elem in _iter_by_local(controller, "description"):
            for child in elem.iter():
                if _local(child.tag) == "value" and child.text:
                    ctrl_desc = child.text.strip()
                    break
            if ctrl_desc:
                break

        for vms_rec in _iter_by_local(controller, "vmsRecord"):
            # VMS index
            vms_index: Optional[str] = None
            idx_elem = _find_by_local(vms_rec, "vmsIndex")
            if idx_elem is not None and idx_elem.text:
                vms_index = idx_elem.text.strip()
            if vms_index is None:
                vms_index = vms_rec.get("index", "")
                if not vms_index:
                    vms_index = vms_rec.get(f"{{{D3_VMS}}}index", "0")
            if not vms_index:
                vms_index = "0"

            # VMS type
            vms_type: Optional[str] = None
            for elem in _iter_by_local(vms_rec, "vmsType"):
                if elem.text:
                    vms_type = elem.text.strip()
                    break

            signs.append({
                "vms_controller_id": controller_id,
                "vms_index": str(vms_index),
                "vms_type": vms_type,
                "latitude": ctrl_lat,
                "longitude": ctrl_lon,
                "road_name": ctrl_road,
                "description": ctrl_desc,
            })

            # Display state
            active: Optional[bool] = None
            for elem in _iter_by_local(vms_rec, "vmsWorking"):
                if elem.text:
                    active = elem.text.strip().lower() == "true"
                    break

            vms_text: Optional[str] = None
            text_parts: List[str] = []
            for line in _iter_by_local(vms_rec, "vmsTextLine"):
                if line.text:
                    text_parts.append(line.text.strip())
            if text_parts:
                vms_text = " ".join(text_parts)

            pictogram_code: Optional[str] = None
            for elem in _iter_by_local(vms_rec, "vmsPicktogramDescription"):
                if elem.text:
                    pictogram_code = elem.text.strip()
                    break
            if pictogram_code is None:
                for elem in _iter_by_local(vms_rec, "pictogramDescription"):
                    if elem.text:
                        pictogram_code = elem.text.strip()
                        break

            state: Optional[str] = None
            for elem in _iter_by_local(vms_rec, "operationalState"):
                if elem.text:
                    state = elem.text.strip()
                    break

            states.append({
                "vms_controller_id": controller_id,
                "vms_index": str(vms_index),
                "publication_time": pub_time,
                "active": active,
                "vms_text": vms_text,
                "pictogram_code": pictogram_code,
                "state": state,
            })

    return signs, states


# ---------------------------------------------------------------------------
# DATEX II v3 parser – MSI (Matrix Signal Installation)
# ---------------------------------------------------------------------------

def parse_msi_xml(xml_bytes: bytes) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Parse MSI DATEX II v3 XML into MsiSign and MsiDisplayState dicts."""
    root = ET.fromstring(xml_bytes)
    signs: List[Dict[str, Any]] = []
    states: List[Dict[str, Any]] = []

    pub_time: Optional[str] = None
    for elem in _iter_by_local(root, "publicationTime"):
        if elem.text:
            pub_time = elem.text.strip()
            break
    if pub_time is None:
        pub_time = ""

    for sign_rec in _iter_by_local(root, "vmsUnitRecord"):
        sign_id = sign_rec.get("id", "")
        if not sign_id:
            sign_id = sign_rec.get(f"{{{D3_VMS}}}id", "")
        if not sign_id:
            continue

        # Sign type
        sign_type: Optional[str] = None
        for elem in _iter_by_local(sign_rec, "vmsType"):
            if elem.text:
                sign_type = elem.text.strip()
                break

        # Location
        sign_lat: Optional[float] = None
        sign_lon: Optional[float] = None
        for pc in _iter_by_local(sign_rec, "pointCoordinates"):
            lat_e = _find_by_local(pc, "latitude")
            lon_e = _find_by_local(pc, "longitude")
            if lat_e is not None and lon_e is not None and lat_e.text and lon_e.text:
                try:
                    sign_lat = float(lat_e.text)
                    sign_lon = float(lon_e.text)
                except ValueError:
                    pass
                break

        # Road name
        road_name: Optional[str] = None
        for elem in _iter_by_local(sign_rec, "roadName"):
            for child in elem.iter():
                if _local(child.tag) == "value" and child.text:
                    road_name = child.text.strip()
                    break
            if road_name:
                break

        # Lane
        lane: Optional[str] = None
        for elem in _iter_by_local(sign_rec, "laneNumber"):
            if elem.text:
                lane = elem.text.strip()
                break

        # Description
        description: Optional[str] = None
        for elem in _iter_by_local(sign_rec, "description"):
            for child in elem.iter():
                if _local(child.tag) == "value" and child.text:
                    description = child.text.strip()
                    break
            if description:
                break

        signs.append({
            "sign_id": sign_id,
            "sign_type": sign_type,
            "latitude": sign_lat,
            "longitude": sign_lon,
            "road_name": road_name,
            "lane": lane,
            "description": description,
        })

        # Display state
        image_code: Optional[str] = None
        for elem in _iter_by_local(sign_rec, "imageCode"):
            if elem.text:
                image_code = elem.text.strip()
                break
        if image_code is None:
            for line in _iter_by_local(sign_rec, "vmsTextLine"):
                if line.text:
                    image_code = line.text.strip()
                    break

        state: Optional[str] = None
        speed_limit: Optional[int] = None
        if image_code is not None:
            if image_code.isdigit():
                state = "speed_limit"
                speed_limit = int(image_code)
            elif image_code.lower() in ("blank", ""):
                state = "open"
                image_code = "blank"
            elif image_code.lower() in ("closed", "cross", "afgesloten"):
                state = "closed"

        for elem in _iter_by_local(sign_rec, "operationalState"):
            if elem.text:
                state = elem.text.strip()
                break

        states.append({
            "sign_id": sign_id,
            "publication_time": pub_time,
            "image_code": image_code,
            "state": state,
            "speed_limit": speed_limit,
        })

    return signs, states


# ---------------------------------------------------------------------------
# DATEX II v3 parser – situation feeds
# ---------------------------------------------------------------------------

def _extract_situation_base(sr: ET.Element) -> Dict[str, Any]:
    """Extract base fields common to all situation record types."""
    rec_id = sr.get("id", "")

    version_time: Optional[str] = None
    for elem in _iter_by_local(sr, "situationRecordVersionTime"):
        if elem.text:
            version_time = elem.text.strip()
            break

    validity_status: Optional[str] = None
    for elem in _iter_by_local(sr, "validityStatus"):
        if elem.text:
            validity_status = elem.text.strip()
            break

    start_time: Optional[str] = None
    end_time: Optional[str] = None
    for elem in _iter_by_local(sr, "overallStartTime"):
        if elem.text:
            start_time = elem.text.strip()
            break
    for elem in _iter_by_local(sr, "overallEndTime"):
        if elem.text:
            end_time = elem.text.strip()
            break

    road_name: Optional[str] = None
    for elem in _iter_by_local(sr, "roadName"):
        for child in elem.iter():
            if _local(child.tag) == "value" and child.text:
                road_name = child.text.strip()
                break
        if road_name:
            break

    description: Optional[str] = None
    for elem in _iter_by_local(sr, "comment"):
        for child in elem.iter():
            if _local(child.tag) == "value" and child.text:
                description = child.text.strip()
                break
        if description:
            break
    if description is None:
        for elem in _iter_by_local(sr, "description"):
            for child in elem.iter():
                if _local(child.tag) == "value" and child.text:
                    description = child.text.strip()
                    break
            if description:
                break

    location_description: Optional[str] = None
    for elem in _iter_by_local(sr, "locationDescriptor"):
        for child in elem.iter():
            if _local(child.tag) == "value" and child.text:
                location_description = child.text.strip()
                break
        if location_description:
            break

    return {
        "situation_record_id": rec_id,
        "version_time": version_time or "",
        "validity_status": validity_status,
        "start_time": start_time,
        "end_time": end_time,
        "road_name": road_name,
        "description": description,
        "location_description": location_description,
    }


def parse_situation_xml(xml_bytes: bytes, feed_type: str) -> List[Dict[str, Any]]:
    """Parse a situation feed DATEX II v3 XML."""
    root = ET.fromstring(xml_bytes)
    results: List[Dict[str, Any]] = []

    for sit in _iter_by_local(root, "situation"):
        sit_id = sit.get("id", "")
        for sr in _iter_by_local(sit, "situationRecord"):
            base = _extract_situation_base(sr)
            # Use situationRecord id if available, else situationId:record index
            rec_id = base["situation_record_id"]
            if not rec_id:
                rec_id = sit_id

            base["situation_record_id"] = rec_id

            if feed_type == "roadwork":
                severity: Optional[str] = None
                for elem in _iter_by_local(sr, "severity"):
                    if elem.text:
                        severity = elem.text.strip()
                        break
                probability: Optional[str] = None
                for elem in _iter_by_local(sr, "probabilityOfOccurrence"):
                    if elem.text:
                        probability = elem.text.strip()
                        break
                mgmt_type: Optional[str] = None
                for elem in _iter_by_local(sr, "roadMaintenanceType"):
                    if elem.text:
                        mgmt_type = elem.text.strip()
                        break
                if mgmt_type is None:
                    for elem in _iter_by_local(sr, "managementType"):
                        if elem.text:
                            mgmt_type = elem.text.strip()
                            break
                base.update({"severity": severity, "probability": probability, "management_type": mgmt_type})

            elif feed_type == "bridge_opening":
                bridge_name: Optional[str] = None
                for elem in _iter_by_local(sr, "bridgeName"):
                    for child in elem.iter():
                        if _local(child.tag) == "value" and child.text:
                            bridge_name = child.text.strip()
                            break
                    if bridge_name:
                        break
                if bridge_name is None:
                    for elem in _iter_by_local(sr, "locationName"):
                        for child in elem.iter():
                            if _local(child.tag) == "value" and child.text:
                                bridge_name = child.text.strip()
                                break
                        if bridge_name:
                            break
                base["bridge_name"] = bridge_name

            elif feed_type == "temporary_closure":
                sev: Optional[str] = None
                for elem in _iter_by_local(sr, "severity"):
                    if elem.text:
                        sev = elem.text.strip()
                        break
                base["severity"] = sev

            elif feed_type == "temporary_speed_limit":
                speed_limit_kmh: Optional[int] = None
                for elem in _iter_by_local(sr, "maximumSpeedLimit"):
                    if elem.text:
                        try:
                            speed_limit_kmh = int(float(elem.text))
                        except ValueError:
                            pass
                        break
                if speed_limit_kmh is None:
                    for elem in _iter_by_local(sr, "speedLimit"):
                        if elem.text:
                            try:
                                speed_limit_kmh = int(float(elem.text))
                            except ValueError:
                                pass
                            break
                base["speed_limit_kmh"] = speed_limit_kmh

            elif feed_type == "safety_related_message":
                xsi_type = sr.get(f"{{{XSI}}}type", "")
                msg_type: Optional[str] = None
                if xsi_type:
                    # Strip namespace prefix like "sit:", "s:"
                    msg_type = xsi_type.split(":")[-1] if ":" in xsi_type else xsi_type
                urgency: Optional[str] = None
                for elem in _iter_by_local(sr, "urgency"):
                    if elem.text:
                        urgency = elem.text.strip()
                        break
                base.update({"message_type": msg_type, "urgency": urgency})

            results.append(base)

    return results


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

class StateManager:
    def __init__(self, state_file: str):
        self.state_file = state_file
        self.state: Dict[str, Dict[str, str]] = {
            "speed": {}, "traveltime": {}, "situation": {}, "drip": {}, "msi": {}
        }
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    for k in self.state:
                        if k in loaded:
                            self.state[k] = loaded[k]
            except (json.JSONDecodeError, OSError):
                logger.warning("Could not load state file, starting fresh")

    def save(self) -> None:
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f)
        except OSError:
            logger.warning("Could not save state file")

    def is_new(self, bucket: str, key: str, value: str) -> bool:
        b = self.state.setdefault(bucket, {})
        if b.get(key) == value:
            return False
        b[key] = value
        return True


# ---------------------------------------------------------------------------
# Poller
# ---------------------------------------------------------------------------

class NdwPoller:
    def __init__(
        self,
        avg_producer: NLNDWAVGEventProducer,
        drip_producer: NLNDWDRIPEventProducer,
        msi_producer: NLNDWMSIEventProducer,
        situations_producer: NLNDWSituationsEventProducer,
        state: StateManager,
        poll_interval: int = DEFAULT_POLL_INTERVAL_SECONDS,
        reference_refresh_interval: int = DEFAULT_REFERENCE_REFRESH_SECONDS,
        situation_interval: int = DEFAULT_SITUATION_INTERVAL_SECONDS,
        base_url: str = BASE_URL,
        max_records_per_family: Optional[int] = DEFAULT_MAX_RECORDS_PER_FAMILY,
    ):
        self.avg_producer = avg_producer
        self.drip_producer = drip_producer
        self.msi_producer = msi_producer
        self.situations_producer = situations_producer
        self.state = state
        self.poll_interval = poll_interval
        self.reference_refresh_interval = reference_refresh_interval
        self.situation_interval = situation_interval
        self.base_url = base_url
        self.max_records_per_family = max_records_per_family
        self.session = _make_session()

        self._point_sites_cache: List[Dict[str, Any]] = []
        self._route_sites_cache: List[Dict[str, Any]] = []
        self._drip_signs_cache: List[Dict[str, Any]] = []
        self._msi_signs_cache: List[Dict[str, Any]] = []

        self._last_reference_emit: float = 0
        self._last_situation_poll: float = 0

    def _flush_and_check(self, producer_obj: Any) -> bool:
        remainder = producer_obj.producer.flush(timeout=60)
        if remainder != 0:
            logger.warning("Kafka flush had %d undelivered messages", remainder)
            return False
        return True

    def _flush_reference_batch(self, producer_obj: Any, count: int, label: str) -> bool:
        if count and count % REFERENCE_FLUSH_BATCH_SIZE == 0:
            if not self._flush_and_check(producer_obj):
                logger.warning(
                    "Flush failed for %s after %d queued reference records; keeping old cache",
                    label,
                    count,
                )
                return False
        return True

    def _limit_records(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if self.max_records_per_family is None:
            return records
        return records[: self.max_records_per_family]

    def emit_reference_data(self) -> None:
        logger.info("Fetching reference data (measurement sites, DRIP signs, MSI signs)")
        self._refresh_measurement_sites()
        self._refresh_drip_signs()
        self._refresh_msi_signs()
        self._last_reference_emit = time.time()

    def _refresh_measurement_sites(self) -> None:
        url = f"{self.base_url}/{MEASUREMENT_CURRENT_FILE}"
        try:
            xml_bytes = download_gzip_xml(self.session, url)
        except Exception:
            logger.exception("Failed to download measurement site data")
            return

        try:
            new_point, new_route = parse_measurement_site_xml(xml_bytes)
        except Exception:
            logger.exception("Failed to parse measurement site XML")
            return

        new_point = self._limit_records(new_point)
        new_route = self._limit_records(new_route)

        # Emit point sites
        count = 0
        for rec in new_point:
            data = PointMeasurementSite(
                measurement_site_id=rec["measurement_site_id"],
                name=rec["name"],
                measurement_site_type=rec["measurement_site_type"],
                period=rec["period"],
                latitude=rec["latitude"],
                longitude=rec["longitude"],
                road_name=rec["road_name"],
                lane_count=rec["lane_count"],
                carriageway_type=rec["carriageway_type"],
            )
            self.avg_producer.send_nl_ndw_avg_point_measurement_site(
                rec["measurement_site_id"], data, flush_producer=False
            )
            count += 1
            if not self._flush_reference_batch(self.avg_producer, count, "PointMeasurementSite"):
                return

        if count:
            if self._flush_and_check(self.avg_producer):
                self._point_sites_cache = new_point
                logger.info("Emitted %d PointMeasurementSite reference events", count)
            else:
                logger.warning("Flush failed for PointMeasurementSite; keeping old cache")
        else:
            logger.info("No point measurement sites found in feed")

        # Emit route sites
        count = 0
        for rec in new_route:
            data = RouteMeasurementSite(
                measurement_site_id=rec["measurement_site_id"],
                name=rec["name"],
                measurement_site_type=rec["measurement_site_type"],
                period=rec["period"],
                start_latitude=rec["start_latitude"],
                start_longitude=rec["start_longitude"],
                end_latitude=rec["end_latitude"],
                end_longitude=rec["end_longitude"],
                road_name=rec["road_name"],
                length_metres=rec["length_metres"],
            )
            self.avg_producer.send_nl_ndw_avg_route_measurement_site(
                rec["measurement_site_id"], data, flush_producer=False
            )
            count += 1
            if not self._flush_reference_batch(self.avg_producer, count, "RouteMeasurementSite"):
                return

        if count:
            if self._flush_and_check(self.avg_producer):
                self._route_sites_cache = new_route
                logger.info("Emitted %d RouteMeasurementSite reference events", count)
            else:
                logger.warning("Flush failed for RouteMeasurementSite; keeping old cache")

    def _refresh_drip_signs(self) -> None:
        url = f"{self.base_url}/{DRIP_FILE}"
        try:
            xml_bytes = download_gzip_xml(self.session, url)
        except Exception:
            logger.exception("Failed to download DRIP sign data")
            return

        try:
            new_signs, _ = parse_drip_xml(xml_bytes)
        except Exception:
            logger.exception("Failed to parse DRIP XML")
            return

        new_signs = self._limit_records(new_signs)

        count = 0
        for rec in new_signs:
            data = DripSign(
                vms_controller_id=rec["vms_controller_id"],
                vms_index=rec["vms_index"],
                vms_type=rec["vms_type"],
                latitude=rec["latitude"],
                longitude=rec["longitude"],
                road_name=rec["road_name"],
                description=rec["description"],
            )
            self.drip_producer.send_nl_ndw_drip_drip_sign(
                rec["vms_controller_id"], rec["vms_index"], data, flush_producer=False
            )
            count += 1
            if not self._flush_reference_batch(self.drip_producer, count, "DripSign"):
                return

        if count:
            if self._flush_and_check(self.drip_producer):
                self._drip_signs_cache = new_signs
                logger.info("Emitted %d DripSign reference events", count)
            else:
                logger.warning("Flush failed for DripSign; keeping old cache")

    def _refresh_msi_signs(self) -> None:
        url = f"{self.base_url}/{MSI_FILE}"
        try:
            xml_bytes = download_gzip_xml(self.session, url)
        except Exception:
            logger.exception("Failed to download MSI sign data")
            return

        try:
            new_signs, _ = parse_msi_xml(xml_bytes)
        except Exception:
            logger.exception("Failed to parse MSI XML")
            return

        new_signs = self._limit_records(new_signs)

        count = 0
        for rec in new_signs:
            data = MsiSign(
                sign_id=rec["sign_id"],
                sign_type=rec["sign_type"],
                latitude=rec["latitude"],
                longitude=rec["longitude"],
                road_name=rec["road_name"],
                lane=rec["lane"],
                description=rec["description"],
            )
            self.msi_producer.send_nl_ndw_msi_msi_sign(
                rec["sign_id"], data, flush_producer=False
            )
            count += 1
            if not self._flush_reference_batch(self.msi_producer, count, "MsiSign"):
                return

        if count:
            if self._flush_and_check(self.msi_producer):
                self._msi_signs_cache = new_signs
                logger.info("Emitted %d MsiSign reference events", count)
            else:
                logger.warning("Flush failed for MsiSign; keeping old cache")

    def _poll_speed(self) -> int:
        url = f"{self.base_url}/{SPEED_FILE}"
        try:
            xml_bytes = download_gzip_xml(self.session, url)
        except Exception:
            logger.exception("Failed to download traffic speed data")
            return 0

        records = self._limit_records(parse_traffic_speed_xml(xml_bytes))
        pending_state: Dict[str, str] = {}
        count = 0
        for rec in records:
            sid = rec["measurement_site_id"]
            mtime = rec["measurement_time"]
            if self.state.state.get("speed", {}).get(sid) == mtime:
                continue
            data = TrafficObservation(
                measurement_site_id=sid,
                measurement_time=mtime,
                average_speed=rec["average_speed"],
                vehicle_flow_rate=rec["vehicle_flow_rate"],
                number_of_lanes_with_data=rec["number_of_lanes_with_data"],
            )
            self.avg_producer.send_nl_ndw_avg_traffic_observation(
                sid, data, flush_producer=False
            )
            pending_state[sid] = mtime
            count += 1

        if count:
            if self._flush_and_check(self.avg_producer):
                self.state.state.setdefault("speed", {}).update(pending_state)
            else:
                logger.warning("Flush failed for TrafficObservation; state not advanced")
                count = 0

        logger.info("Emitted %d TrafficObservation events (of %d sites)", count, len(records))
        return count

    def _poll_traveltime(self) -> int:
        url = f"{self.base_url}/{TRAVELTIME_FILE}"
        try:
            xml_bytes = download_gzip_xml(self.session, url)
        except Exception:
            logger.exception("Failed to download travel time data")
            return 0

        records = self._limit_records(parse_travel_time_xml(xml_bytes))
        pending_state: Dict[str, str] = {}
        count = 0
        for rec in records:
            sid = rec["measurement_site_id"]
            mtime = rec["measurement_time"]
            if self.state.state.get("traveltime", {}).get(sid) == mtime:
                continue
            data = TravelTimeObservation(
                measurement_site_id=sid,
                measurement_time=mtime,
                duration=rec["duration"],
                reference_duration=rec["reference_duration"],
                accuracy=rec["accuracy"],
                data_quality=rec["data_quality"],
                number_of_input_values=rec["number_of_input_values"],
            )
            self.avg_producer.send_nl_ndw_avg_travel_time_observation(
                sid, data, flush_producer=False
            )
            pending_state[sid] = mtime
            count += 1

        if count:
            if self._flush_and_check(self.avg_producer):
                self.state.state.setdefault("traveltime", {}).update(pending_state)
            else:
                logger.warning("Flush failed for TravelTimeObservation; state not advanced")
                count = 0

        logger.info("Emitted %d TravelTimeObservation events (of %d sites)", count, len(records))
        return count

    def _poll_drip_states(self) -> int:
        url = f"{self.base_url}/{DRIP_FILE}"
        try:
            xml_bytes = download_gzip_xml(self.session, url)
        except Exception:
            logger.exception("Failed to download DRIP display states")
            return 0

        _, states = parse_drip_xml(xml_bytes)
        states = self._limit_records(states)
        pending_state: Dict[str, str] = {}
        count = 0
        for rec in states:
            key = f"{rec['vms_controller_id']}/{rec['vms_index']}"
            pub_time = rec["publication_time"]
            if self.state.state.get("drip", {}).get(key) == pub_time:
                continue
            data = DripDisplayState(
                vms_controller_id=rec["vms_controller_id"],
                vms_index=rec["vms_index"],
                publication_time=pub_time,
                active=rec["active"],
                vms_text=rec["vms_text"],
                pictogram_code=rec["pictogram_code"],
                state=rec["state"],
            )
            self.drip_producer.send_nl_ndw_drip_drip_display_state(
                rec["vms_controller_id"], rec["vms_index"], data, flush_producer=False
            )
            pending_state[key] = pub_time
            count += 1

        if count:
            if self._flush_and_check(self.drip_producer):
                self.state.state.setdefault("drip", {}).update(pending_state)
            else:
                logger.warning("Flush failed for DripDisplayState; state not advanced")
                count = 0

        logger.info("Emitted %d DripDisplayState events", count)
        return count

    def _poll_msi_states(self) -> int:
        url = f"{self.base_url}/{MSI_FILE}"
        try:
            xml_bytes = download_gzip_xml(self.session, url)
        except Exception:
            logger.exception("Failed to download MSI display states")
            return 0

        _, states = parse_msi_xml(xml_bytes)
        states = self._limit_records(states)
        pending_state: Dict[str, str] = {}
        count = 0
        for rec in states:
            sid = rec["sign_id"]
            pub_time = rec["publication_time"]
            if self.state.state.get("msi", {}).get(sid) == pub_time:
                continue
            data = MsiDisplayState(
                sign_id=sid,
                publication_time=pub_time,
                image_code=rec["image_code"],
                state=rec["state"],
                speed_limit=rec["speed_limit"],
            )
            self.msi_producer.send_nl_ndw_msi_msi_display_state(
                sid, data, flush_producer=False
            )
            pending_state[sid] = pub_time
            count += 1

        if count:
            if self._flush_and_check(self.msi_producer):
                self.state.state.setdefault("msi", {}).update(pending_state)
            else:
                logger.warning("Flush failed for MsiDisplayState; state not advanced")
                count = 0

        logger.info("Emitted %d MsiDisplayState events", count)
        return count

    def _poll_situations(self) -> int:
        total = 0
        for feed_file, feed_type in SITUATION_FEEDS:
            url = f"{self.base_url}/{feed_file}"
            try:
                xml_bytes = download_gzip_xml(self.session, url)
            except Exception:
                logger.exception("Failed to download situation feed: %s", feed_file)
                continue

            try:
                records = parse_situation_xml(xml_bytes, feed_type)
            except Exception:
                logger.exception("Failed to parse situation feed: %s", feed_file)
                continue

            records = self._limit_records(records)

            pending_state: Dict[str, str] = {}
            count = 0
            for rec in records:
                rid = rec["situation_record_id"]
                vtime = rec["version_time"]
                if self.state.state.get("situation", {}).get(rid) == vtime:
                    continue

                try:
                    if feed_type == "roadwork":
                        data = Roadwork(
                            situation_record_id=rid,
                            version_time=vtime,
                            validity_status=rec.get("validity_status"),
                            start_time=rec.get("start_time"),
                            end_time=rec.get("end_time"),
                            road_name=rec.get("road_name"),
                            description=rec.get("description"),
                            location_description=rec.get("location_description"),
                            probability=rec.get("probability"),
                            severity=rec.get("severity"),
                            management_type=rec.get("management_type"),
                        )
                        self.situations_producer.send_nl_ndw_situations_roadwork(
                            rid, data, flush_producer=False
                        )
                    elif feed_type == "bridge_opening":
                        data = BridgeOpening(
                            situation_record_id=rid,
                            version_time=vtime,
                            validity_status=rec.get("validity_status"),
                            start_time=rec.get("start_time"),
                            end_time=rec.get("end_time"),
                            bridge_name=rec.get("bridge_name"),
                            road_name=rec.get("road_name"),
                            description=rec.get("description"),
                        )
                        self.situations_producer.send_nl_ndw_situations_bridge_opening(
                            rid, data, flush_producer=False
                        )
                    elif feed_type == "temporary_closure":
                        data = TemporaryClosure(
                            situation_record_id=rid,
                            version_time=vtime,
                            validity_status=rec.get("validity_status"),
                            start_time=rec.get("start_time"),
                            end_time=rec.get("end_time"),
                            road_name=rec.get("road_name"),
                            description=rec.get("description"),
                            location_description=rec.get("location_description"),
                            severity=rec.get("severity"),
                        )
                        self.situations_producer.send_nl_ndw_situations_temporary_closure(
                            rid, data, flush_producer=False
                        )
                    elif feed_type == "temporary_speed_limit":
                        data = TemporarySpeedLimit(
                            situation_record_id=rid,
                            version_time=vtime,
                            validity_status=rec.get("validity_status"),
                            start_time=rec.get("start_time"),
                            end_time=rec.get("end_time"),
                            road_name=rec.get("road_name"),
                            speed_limit_kmh=rec.get("speed_limit_kmh"),
                            description=rec.get("description"),
                            location_description=rec.get("location_description"),
                        )
                        self.situations_producer.send_nl_ndw_situations_temporary_speed_limit(
                            rid, data, flush_producer=False
                        )
                    elif feed_type == "safety_related_message":
                        data = SafetyRelatedMessage(
                            situation_record_id=rid,
                            version_time=vtime,
                            validity_status=rec.get("validity_status"),
                            start_time=rec.get("start_time"),
                            end_time=rec.get("end_time"),
                            road_name=rec.get("road_name"),
                            message_type=rec.get("message_type"),
                            description=rec.get("description"),
                            urgency=rec.get("urgency"),
                        )
                        self.situations_producer.send_nl_ndw_situations_safety_related_message(
                            rid, data, flush_producer=False
                        )
                except Exception:
                    logger.exception("Failed to emit situation record %s", rid)
                    continue

                pending_state[rid] = vtime
                count += 1

            if count:
                if self._flush_and_check(self.situations_producer):
                    self.state.state.setdefault("situation", {}).update(pending_state)
                    logger.info("Emitted %d %s situation events", count, feed_type)
                    total += count
                else:
                    logger.warning("Flush failed for %s situations; state not advanced", feed_type)

        return total

    def poll_cycle(self) -> None:
        now = time.time()

        if now - self._last_reference_emit >= self.reference_refresh_interval:
            self.emit_reference_data()

        self._poll_speed()
        self._poll_traveltime()
        self._poll_drip_states()
        self._poll_msi_states()

        if now - self._last_situation_poll >= self.situation_interval:
            self._poll_situations()
            self._last_situation_poll = now

        self.state.save()

    def run_forever(self) -> None:
        logger.info("Starting NDW Road Traffic poller (interval=%ds)", self.poll_interval)
        self._last_reference_emit = 0
        self._last_situation_poll = 0
        while True:
            try:
                self.poll_cycle()
            except Exception:
                logger.exception("Error during poll cycle")
            time.sleep(self.poll_interval)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="NDW Netherlands Road Traffic bridge")
    parser.add_argument("--topic", default=None, help="Kafka topic for all messages")
    parser.add_argument("--poll-interval", type=int, default=None, help="Telemetry poll interval in seconds")
    parser.add_argument("--state-file", default=None, help="Path to state file")
    args = parser.parse_args()

    connection_string = os.environ.get("CONNECTION_STRING", "")
    if not connection_string:
        logger.error("CONNECTION_STRING environment variable is required")
        sys.exit(1)

    enable_tls = os.environ.get("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config, conn_topic = _build_kafka_config(connection_string, enable_tls)

    topic = (
        args.topic
        or os.environ.get("KAFKA_TOPIC", "")
        or conn_topic
        or DEFAULT_TOPIC
    )

    poll_interval = args.poll_interval or int(
        os.environ.get("POLLING_INTERVAL", DEFAULT_POLL_INTERVAL_SECONDS)
    )
    state_file = args.state_file or os.environ.get("STATE_FILE", DEFAULT_STATE_FILE)
    max_records_per_family = os.environ.get("MAX_RECORDS_PER_FAMILY")

    producer = Producer(kafka_config)

    avg_prod = NLNDWAVGEventProducer(producer, topic)
    drip_prod = NLNDWDRIPEventProducer(producer, topic)
    msi_prod = NLNDWMSIEventProducer(producer, topic)
    situations_prod = NLNDWSituationsEventProducer(producer, topic)

    state = StateManager(state_file)
    poller = NdwPoller(
        avg_prod,
        drip_prod,
        msi_prod,
        situations_prod,
        state,
        poll_interval,
        max_records_per_family=int(max_records_per_family) if max_records_per_family else None,
    )
    poller.run_forever()


if __name__ == "__main__":
    main()
