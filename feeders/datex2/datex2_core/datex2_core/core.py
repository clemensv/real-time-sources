from __future__ import annotations

import gzip
import json
import logging
import os
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

LOGGER = logging.getLogger(__name__)
USER_AGENT = os.getenv("USER_AGENT", "real-time-sources-datex2/0.1.0 (+https://github.com/clemensv/real-time-sources)")
DEFAULT_ENDPOINTS = [
    {"id": "ndw", "url": "https://opendata.ndw.nu/measurement_current.xml.gz", "publication": "MeasurementSiteTablePublication", "country": "nl", "operator": "ndw"},
    {"id": "ndw", "url": "https://opendata.ndw.nu/trafficspeed.xml.gz", "publication": "MeasuredDataPublication", "country": "nl", "operator": "ndw"},
    {"id": "ndw", "url": "https://opendata.ndw.nu/traveltime.xml.gz", "publication": "MeasuredDataPublication", "country": "nl", "operator": "ndw"},
    {"id": "ndw", "url": "https://opendata.ndw.nu/planningsfeed_wegwerkzaamheden_en_evenementen.xml.gz", "publication": "SituationPublication", "country": "nl", "operator": "ndw"},
]

# Packaged source catalog shipped inside the wheel/Docker image. Override at
# runtime with DATEX2_SOURCES_FILE (a path to a copy of this JSON document).
DEFAULT_SOURCES_FILE = os.path.join(os.path.dirname(__file__), "sources", "datex2.sources.json")

# ${ENV_VAR} placeholders in catalog string fields are expanded from the
# process environment at load time so secrets never live in the file.
_ENV_REF = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


@dataclass(frozen=True)
class Datex2Endpoint:
    id: str
    url: str
    publication: str
    country: str = "eu"
    operator: str = "datex2"
    auth_header: Optional[str] = None


@dataclass
class Datex2Batch:
    measurement_sites: List[Dict[str, Any]]
    traffic_measurements: List[Dict[str, Any]]
    situation_records: List[Dict[str, Any]]

    @classmethod
    def empty(cls) -> "Datex2Batch":
        return cls([], [], [])


def build_retry_session() -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    retry = Retry(total=3, backoff_factor=1.0, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET"])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def _interpolate_env(value: Any) -> Any:
    """Expand ${ENV_VAR} placeholders in strings (recursing into lists/dicts)."""
    if isinstance(value, str):
        return _ENV_REF.sub(lambda m: os.environ.get(m.group(1), ""), value)
    if isinstance(value, list):
        return [_interpolate_env(item) for item in value]
    if isinstance(value, dict):
        return {key: _interpolate_env(item) for key, item in value.items()}
    return value


def _read_config_text(raw: str) -> str:
    """Resolve an inline-config string: JSON literal, @path, or bare path."""
    raw = raw.strip()
    if raw.startswith("@"):
        with open(raw[1:].strip(), "r", encoding="utf-8") as handle:
            return handle.read()
    if raw.startswith("[") or raw.startswith("{"):
        return raw
    if os.path.exists(raw):
        with open(raw, "r", encoding="utf-8") as handle:
            return handle.read()
    return raw


def _coerce_entries(data: Any) -> List[Dict[str, Any]]:
    """Accept either a {"sources": [...]} catalog or a bare list of entries."""
    if isinstance(data, dict):
        data = data.get("sources", [])
    if not isinstance(data, list):
        return []
    return [dict(item) for item in data if isinstance(item, dict)]


def select_entries(entries: List[Dict[str, Any]], selector: str = "") -> List[Dict[str, Any]]:
    """Filter catalog entries by the DATEX2_SOURCES selector.

    Empty selector -> every entry whose ``enabled`` flag is true (default true).
    ``*`` -> every entry, including disabled templates.
    Otherwise a comma-separated allow-list of entry ``name`` values, returned in
    the order requested. An unknown name raises ``ValueError``.
    """
    selector = (selector or "").strip()
    if selector == "*":
        return list(entries)
    if not selector:
        return [entry for entry in entries if entry.get("enabled", True)]
    by_name = {entry["name"]: entry for entry in entries if entry.get("name")}
    chosen: List[Dict[str, Any]] = []
    unknown: List[str] = []
    for token in (part.strip() for part in selector.split(",")):
        if not token:
            continue
        if token in by_name:
            chosen.append(by_name[token])
        else:
            unknown.append(token)
    if unknown:
        known = ", ".join(sorted(by_name)) or "(none)"
        raise ValueError(f"Unknown DATEX2_SOURCES entries: {', '.join(unknown)}. Known names: {known}")
    return chosen


def _entries_to_endpoints(entries: Iterable[Dict[str, Any]]) -> List[Datex2Endpoint]:
    endpoints: List[Datex2Endpoint] = []
    for raw_item in entries:
        item = _interpolate_env(raw_item)
        endpoints.append(Datex2Endpoint(
            id=str(item.get("id") or item.get("supplier_id") or "datex2"),
            url=str(item.get("url") or item.get("base_url") or item.get("endpoint") or ""),
            publication=str(item.get("publication") or item.get("profile") or "auto"),
            country=str(item.get("country") or item.get("country_code") or "eu").lower(),
            operator=str(item.get("operator") or item.get("operator_id") or item.get("id") or "datex2").lower(),
            auth_header=item.get("auth_header") or item.get("authorization"),
        ))
    return [endpoint for endpoint in endpoints if endpoint.url]


def load_endpoints(raw: str = "", mock: bool = False, sources_file: str = "", selector: str = "") -> List[Datex2Endpoint]:
    """Resolve the DATEX II endpoints to poll.

    Resolution order: ``mock`` -> inline ``raw`` (legacy DATEX2_ENDPOINTS: a JSON
    array, a ``{"sources": [...]}`` object, or ``@/path/to/file.json``) -> the
    catalog file (``sources_file`` override or the packaged default). The
    ``selector`` (DATEX2_SOURCES) then narrows which catalog entries run.
    """
    if mock:
        return _entries_to_endpoints([{"id": "sample", "url": "https://example.invalid/datex2/sample", "publication": "mock", "country": "eu", "operator": "datex2"}])
    if raw and raw.strip():
        entries = _coerce_entries(json.loads(_read_config_text(raw)))
    else:
        path = sources_file.strip() if sources_file and sources_file.strip() else DEFAULT_SOURCES_FILE
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as handle:
                entries = _coerce_entries(json.load(handle))
        else:
            entries = [dict(item) for item in DEFAULT_ENDPOINTS]
    return _entries_to_endpoints(select_entries(entries, selector))


def load_state(path: str) -> Dict[str, str]:
    if not path or not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return {}


def save_state(path: str, state: Dict[str, str]) -> None:
    if not path:
        return
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(state, handle, sort_keys=True)


def _local(tag: str) -> str:
    return tag.split("}")[-1] if "}" in tag else tag


def _iter(root: ET.Element, local_name: str):
    for elem in root.iter():
        if _local(elem.tag) == local_name:
            yield elem


def _child(elem: ET.Element, local_name: str) -> Optional[ET.Element]:
    for child in elem:
        if _local(child.tag) == local_name:
            return child
    return None


def _text_in(elem: Optional[ET.Element], local_name: str) -> Optional[str]:
    child = _child(elem, local_name) if elem is not None else None
    return child.text.strip() if child is not None and child.text else None


def _first_text(elem: ET.Element, names: Iterable[str]) -> Optional[str]:
    wanted = set(names)
    for node in elem.iter():
        if _local(node.tag) in wanted and node.text and node.text.strip():
            return node.text.strip()
    return None


def _float(value: Optional[str]) -> Optional[float]:
    try:
        return float(value) if value is not None and value != "" else None
    except Exception:
        return None


def _int(value: Optional[str]) -> Optional[int]:
    try:
        return int(float(value)) if value is not None and value != "" else None
    except Exception:
        return None


def _timestamp_key(timestamp: str) -> str:
    return re.sub(r"[^0-9A-Za-z]+", "-", timestamp).strip("-") or "unknown"


def mock_batch() -> Datex2Batch:
    feed = "https://example.invalid/datex2/sample"
    return Datex2Batch(
        measurement_sites=[dict(supplier_id="sample", measurement_site_id="site-1", feed_url=feed, country_code="eu", operator_id="datex2", name="Sample loop detector", measurement_site_type="inductionLoop", period_seconds=60, latitude=52.1, longitude=4.3, road_number="A1", carriageway="mainCarriageway", lane="lane1", specific_measurements="speed,flow")],
        traffic_measurements=[dict(supplier_id="sample", measurement_site_id="site-1", feed_url=feed, measurement_time="2026-01-01T00:00:00Z", measurement_time_key="2026-01-01T00-00-00Z", country_code="eu", operator_id="datex2", road_number="A1", average_speed_kmh=83.5, vehicle_flow_rate_veh_per_hour=1200, occupancy_percent=18.2, travel_time_seconds=None, free_flow_travel_time_seconds=None, input_value_count=12, quality_status="reliable", vehicle_type="allVehicles", lane="lane1", raw_measurements=None)],
        situation_records=[dict(supplier_id="sample", situation_id="sit-1", situation_record_id="rec-1", feed_url=feed, country_code="eu", operator_id="datex2", version="1", record_type="ConstructionWorks", severity="medium", probability="certain", validity_status="active", creation_time="2026-01-01T00:00:00Z", observation_time="2026-01-01T00:01:00Z", overall_start_time="2026-01-01T00:00:00Z", overall_end_time=None, latitude=52.2, longitude=4.4, road_number="A1", direction="positive", location_description="Sample road section", description="Sample roadworks", source_name="Sample DATEX II", cause="roadworks", management_type="laneManagement", raw_record=None)],
    )


def _xml_from_response(response: requests.Response) -> bytes:
    data = response.content
    if response.headers.get("content-encoding", "").lower() == "gzip" or response.url.endswith(".gz") or data[:2] == b"\x1f\x8b":
        return gzip.decompress(data)
    return data


def fetch_endpoint(session: requests.Session, endpoint: Datex2Endpoint) -> bytes:
    headers = {"Authorization": endpoint.auth_header} if endpoint.auth_header else {}
    response = session.get(endpoint.url, timeout=120, headers=headers)
    response.raise_for_status()
    return _xml_from_response(response)


def parse_xml(endpoint: Datex2Endpoint, xml_bytes: bytes, max_records: Optional[int] = None) -> Datex2Batch:
    root = ET.fromstring(xml_bytes)
    batch = Datex2Batch.empty()
    for record in _iter(root, "measurementSiteRecord"):
        site_id = record.get("id") or record.get("versionedObjectId")
        if not site_id:
            continue
        batch.measurement_sites.append(dict(supplier_id=endpoint.id, measurement_site_id=site_id, feed_url=endpoint.url, country_code=endpoint.country, operator_id=endpoint.operator, name=_first_text(record, ["measurementSiteName", "name"]), measurement_site_type=_first_text(record, ["measurementEquipmentTypeUsed", "measurementSiteType"]), period_seconds=_int(_first_text(record, ["period"])), latitude=_float(_first_text(record, ["latitude"])), longitude=_float(_first_text(record, ["longitude"])), road_number=_first_text(record, ["roadName", "roadNumber"]), carriageway=_first_text(record, ["carriageway", "carriagewayType"]), lane=_first_text(record, ["lane", "specificLane"]), specific_measurements=None))
        if max_records and len(batch.measurement_sites) >= max_records:
            break
    for site_measurements in _iter(root, "siteMeasurements"):
        ref = _child(site_measurements, "measurementSiteReference")
        site_id = ref.get("id") if ref is not None else None
        if not site_id:
            continue
        ts = _text_in(site_measurements, "measurementTimeDefault") or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        speed = flow = occupancy = travel_time = free_flow = count = None
        for measured_value in _iter(site_measurements, "measuredValue"):
            texts = {_local(node.tag): (node.text.strip() if node.text else "") for node in measured_value.iter()}
            speed = speed if speed is not None else _float(texts.get("speed"))
            flow = flow if flow is not None else _int(texts.get("vehicleFlowRate"))
            occupancy = occupancy if occupancy is not None else _float(texts.get("occupancy"))
            travel_time = travel_time if travel_time is not None else _float(texts.get("travelTime"))
            free_flow = free_flow if free_flow is not None else _float(texts.get("freeFlowTravelTime"))
            count = count if count is not None else _int(measured_value.get("numberOfInputValuesUsed"))
        batch.traffic_measurements.append(dict(supplier_id=endpoint.id, measurement_site_id=site_id, feed_url=endpoint.url, measurement_time=ts, measurement_time_key=_timestamp_key(ts), country_code=endpoint.country, operator_id=endpoint.operator, road_number=None, average_speed_kmh=speed, vehicle_flow_rate_veh_per_hour=flow, occupancy_percent=occupancy, travel_time_seconds=travel_time, free_flow_travel_time_seconds=free_flow, input_value_count=count, quality_status=None, vehicle_type=None, lane=None, raw_measurements=None))
        if max_records and len(batch.traffic_measurements) >= max_records:
            break
    for situation in _iter(root, "situation"):
        situation_id = situation.get("id") or situation.get("versionedObjectId") or "situation"
        records = list(_iter(situation, "situationRecord")) or [situation]
        for record in records:
            record_id = record.get("id") or record.get("versionedObjectId") or situation_id
            record_type = record.get("{http://www.w3.org/2001/XMLSchema-instance}type") or _local(record.tag)
            batch.situation_records.append(dict(supplier_id=endpoint.id, situation_id=situation_id, situation_record_id=record_id, feed_url=endpoint.url, country_code=endpoint.country, operator_id=endpoint.operator, version=record.get("version") or situation.get("version"), record_type=record_type, severity=_first_text(record, ["overallSeverity", "severity"]), probability=_first_text(record, ["probabilityOfOccurrence"]), validity_status=_first_text(record, ["validityStatus"]), creation_time=_first_text(record, ["situationRecordCreationTime"]), observation_time=_first_text(record, ["situationRecordObservationTime"]), overall_start_time=_first_text(record, ["overallStartTime"]), overall_end_time=_first_text(record, ["overallEndTime"]), latitude=_float(_first_text(record, ["latitude"])), longitude=_float(_first_text(record, ["longitude"])), road_number=_first_text(record, ["roadNumber", "roadName"]), direction=_first_text(record, ["tpegDirection", "directionBound"]), location_description=_first_text(record, ["locationDescriptor", "value"]), description=_first_text(record, ["comment", "value"]), source_name=_first_text(record, ["sourceIdentification", "sourceName"]), cause=_first_text(record, ["causeType", "cause"]), management_type=_first_text(record, ["managementType"]), raw_record=None))
            if max_records and len(batch.situation_records) >= max_records:
                break
    return batch


def collect_batches(endpoints: List[Datex2Endpoint], mock: bool = False, max_records: Optional[int] = None) -> Datex2Batch:
    if mock:
        return mock_batch()
    session = build_retry_session()
    result = Datex2Batch.empty()
    for endpoint in endpoints:
        try:
            batch = parse_xml(endpoint, fetch_endpoint(session, endpoint), max_records=max_records)
            result.measurement_sites.extend(batch.measurement_sites)
            result.traffic_measurements.extend(batch.traffic_measurements)
            result.situation_records.extend(batch.situation_records)
        except Exception as exc:
            LOGGER.warning("Skipping DATEX II endpoint %s (%s): %s", endpoint.id, endpoint.url, exc)
    return result
