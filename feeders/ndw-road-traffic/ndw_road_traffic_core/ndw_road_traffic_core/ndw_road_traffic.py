"""Transport-neutral NDW Netherlands Road Traffic acquisition core.

Provides constants, HTTP helpers, DATEX II parsers, state management, and
an NdwAcquirer that fetches/parses all NDW feeds.  No Kafka, MQTT, or AMQP
dependencies live here.
"""

from __future__ import annotations

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

# ---------------------------------------------------------------------------
# URL / feed constants
# ---------------------------------------------------------------------------

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
D3_MC  = "http://datex2.eu/schema/3/messageContainer"
XSI    = "http://www.w3.org/2001/XMLSchema-instance"

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-ndw-road-traffic/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _make_session() -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
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
# XML helpers
# ---------------------------------------------------------------------------

def _text(elem: Optional[ET.Element], tag: str, ns: str) -> Optional[str]:
    if elem is None:
        return None
    node = elem.find(f"{{{ns}}}{tag}")
    return node.text.strip() if node is not None and node.text else None


def _local(tag: str) -> str:
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

def _parse_coords_v3(site_rec: ET.Element) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float]]:
    lat = lon = None
    start_lat = start_lon = end_lat = end_lon = None

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
    root = ET.fromstring(xml_bytes)
    point_sites: List[Dict[str, Any]] = []
    route_sites: List[Dict[str, Any]] = []

    for sr in _iter_by_local(root, "measurementSiteRecord"):
        site_id = sr.get("id", "") or sr.get(f"{{{D3_MST}}}id", "")
        if not site_id:
            continue

        xsi_type = sr.get(f"{{{XSI}}}type", "")
        is_route = "Route" in xsi_type or "route" in xsi_type.lower()

        name: Optional[str] = None
        for elem in _iter_by_local(sr, "measurementSiteName"):
            for child in elem.iter():
                if _local(child.tag) in ("value", "name") and child.text:
                    name = child.text.strip()
                    break
            if name:
                break

        eq_type: Optional[str] = None
        for elem in _iter_by_local(sr, "measurementEquipmentTypeUsed"):
            if elem.text:
                eq_type = elem.text.strip()
                break

        period: Optional[int] = None
        for elem in _iter_by_local(sr, "period"):
            if elem.text:
                try:
                    period = int(float(elem.text))
                except ValueError:
                    pass
                break

        road_name: Optional[str] = None
        for elem in _iter_by_local(sr, "roadName"):
            for child in elem.iter():
                if _local(child.tag) == "value" and child.text:
                    road_name = child.text.strip()
                    break
            if road_name:
                break

        cw_type: Optional[str] = None
        for elem in _iter_by_local(sr, "carriageWayType"):
            if elem.text:
                cw_type = elem.text.strip()
                break

        lane_count: Optional[int] = 0
        lane_elems = list(_iter_by_local(sr, "measurementSpecificCharacteristics"))
        if lane_elems:
            lane_count = len(lane_elems)

        coords = _parse_coords_v3(sr)
        lat, lon = coords[0], coords[1]
        start_lat, start_lon = coords[2], coords[3]
        end_lat, end_lon = coords[4], coords[5]

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

    for controller in _iter_by_local(root, "vmsUnitRecord"):
        controller_id = controller.get("id", "")
        if not controller_id:
            controller_id = controller.get(f"{{{D3_VMS}}}id", "")
        if not controller_id:
            continue

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

        ctrl_road: Optional[str] = None
        for elem in _iter_by_local(controller, "roadName"):
            for child in elem.iter():
                if _local(child.tag) == "value" and child.text:
                    ctrl_road = child.text.strip()
                    break
            if ctrl_road:
                break

        ctrl_desc: Optional[str] = None
        for elem in _iter_by_local(controller, "description"):
            for child in elem.iter():
                if _local(child.tag) == "value" and child.text:
                    ctrl_desc = child.text.strip()
                    break
            if ctrl_desc:
                break

        for vms_rec in _iter_by_local(controller, "vmsRecord"):
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

            active: Optional[bool] = None
            for elem in _iter_by_local(vms_rec, "vmsWorking"):
                if elem.text:
                    active = elem.text.strip().lower() == "true"
                    break

            text_parts: List[str] = []
            for line in _iter_by_local(vms_rec, "vmsTextLine"):
                if line.text:
                    text_parts.append(line.text.strip())
            vms_text: Optional[str] = " ".join(text_parts) if text_parts else None

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

        sign_type: Optional[str] = None
        for elem in _iter_by_local(sign_rec, "vmsType"):
            if elem.text:
                sign_type = elem.text.strip()
                break

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

        road_name: Optional[str] = None
        for elem in _iter_by_local(sign_rec, "roadName"):
            for child in elem.iter():
                if _local(child.tag) == "value" and child.text:
                    road_name = child.text.strip()
                    break
            if road_name:
                break

        lane: Optional[str] = None
        for elem in _iter_by_local(sign_rec, "laneNumber"):
            if elem.text:
                lane = elem.text.strip()
                break

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
    root = ET.fromstring(xml_bytes)
    results: List[Dict[str, Any]] = []

    for sit in _iter_by_local(root, "situation"):
        sit_id = sit.get("id", "")
        for sr in _iter_by_local(sit, "situationRecord"):
            base = _extract_situation_base(sr)
            rec_id = base["situation_record_id"] or sit_id
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
# NdwAcquirer — fetches and parses NDW feeds, returns structured dicts
# ---------------------------------------------------------------------------

class NdwAcquirer:
    """Fetches and parses NDW data feeds.

    Returns raw Python dicts.  No producer classes, no transport deps.
    Each caller (Kafka / MQTT / AMQP bridge) converts dicts to its own
    data-class instances and emits them.
    """

    def __init__(
        self,
        base_url: str = BASE_URL,
        max_records_per_family: Optional[int] = DEFAULT_MAX_RECORDS_PER_FAMILY,
    ):
        self.base_url = base_url.rstrip("/")
        self.max_records_per_family = max_records_per_family
        self.session = _make_session()

    def _limit(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if self.max_records_per_family is None:
            return records
        return records[: self.max_records_per_family]

    def fetch_measurement_sites(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Returns (point_sites, route_sites). Raises on download/parse failure."""
        url = f"{self.base_url}/{MEASUREMENT_CURRENT_FILE}"
        xml_bytes = download_gzip_xml(self.session, url)
        pts, rts = parse_measurement_site_xml(xml_bytes)
        return self._limit(pts), self._limit(rts)

    def fetch_speed_observations(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/{SPEED_FILE}"
        xml_bytes = download_gzip_xml(self.session, url)
        return self._limit(parse_traffic_speed_xml(xml_bytes))

    def fetch_traveltime_observations(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/{TRAVELTIME_FILE}"
        xml_bytes = download_gzip_xml(self.session, url)
        return self._limit(parse_travel_time_xml(xml_bytes))

    def fetch_drip(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Returns (drip_signs, drip_display_states)."""
        url = f"{self.base_url}/{DRIP_FILE}"
        xml_bytes = download_gzip_xml(self.session, url)
        signs, states = parse_drip_xml(xml_bytes)
        return self._limit(signs), self._limit(states)

    def fetch_msi(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Returns (msi_signs, msi_display_states)."""
        url = f"{self.base_url}/{MSI_FILE}"
        xml_bytes = download_gzip_xml(self.session, url)
        signs, states = parse_msi_xml(xml_bytes)
        return self._limit(signs), self._limit(states)

    def fetch_situations(self, feed_file: str, feed_type: str) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/{feed_file}"
        xml_bytes = download_gzip_xml(self.session, url)
        return self._limit(parse_situation_xml(xml_bytes, feed_type))
