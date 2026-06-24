"""US CBP Border Wait Times - transport-neutral acquisition."""
from __future__ import annotations
import json, logging, os, re
from typing import Any, Dict, List, Optional, Tuple
import requests
from cbp_border_wait_producer_data.gov.cbp.borderwait.port import Port
from cbp_border_wait_producer_data.gov.cbp.borderwait.waittime import WaitTime
USER_AGENT = os.environ.get("USER_AGENT") or ("real-time-sources-cbp-border-wait/0.1.0 " "(+https://github.com/clemensv/real-time-sources; " + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")")
API_URL = "https://bwt.cbp.gov/api/bwtnew"
__all__ = ["USER_AGENT", "API_URL", "_load_state", "_save_state", "slugify_topic_segment", "parse_int_or_none", "parse_delay_minutes", "parse_lanes_open", "parse_operational_status", "_extract_lane", "CbpBorderWaitAPI"]
def _load_state(state_file: str) -> dict:
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, 'r', encoding='utf-8') as f: return json.load(f)
    except Exception as exc: logging.warning('Could not load state from %s: %s', state_file, exc)
    return {}
def _save_state(state_file: str, data: dict) -> None:
    if not state_file: return
    try:
        with open(state_file, 'w', encoding='utf-8') as f: json.dump(data, f)
    except Exception as exc: logging.warning('Could not save state to %s: %s', state_file, exc)
def slugify_topic_segment(value: str, fallback: str = 'unknown') -> str:
    slug = re.sub(r'[^a-z0-9]+', '-', str(value or '').lower()).strip('-'); return slug or fallback
def parse_int_or_none(value: str) -> Optional[int]:
    if value is None: return None
    value = str(value).strip()
    if not value or value.upper() == 'N/A': return None
    try: return int(value)
    except (ValueError, TypeError): return None
def parse_delay_minutes(value: str) -> Optional[int]: return parse_int_or_none(value)
def parse_lanes_open(value: str) -> Optional[int]: return parse_int_or_none(value)
def parse_operational_status(value: str) -> Optional[str]:
    if value is None: return None
    value = str(value).strip(); return value if value else None
def _extract_lane(lane_data: dict) -> Tuple[Optional[int], Optional[int], Optional[str]]:
    if not lane_data: return None, None, None
    return parse_delay_minutes(lane_data.get('delay_minutes', '')), parse_lanes_open(lane_data.get('lanes_open', '')), parse_operational_status(lane_data.get('operational_status', ''))
class CbpBorderWaitAPI:
    def __init__(self, api_url: str = API_URL):
        self.api_url = api_url; self.session = requests.Session(); self.session.headers['User-Agent'] = USER_AGENT
    def fetch_ports(self) -> List[Dict[str, Any]]:
        resp = self.session.get(self.api_url, timeout=60); resp.raise_for_status(); return resp.json()
    @staticmethod
    def parse_port(raw: Dict[str, Any]) -> Port:
        pv = raw.get('passenger_vehicle_lanes', {}); cv = raw.get('commercial_vehicle_lanes', {}); ped = raw.get('pedestrian_lanes', {}); border = raw.get('border', '')
        return Port(port_number=raw.get('port_number', ''), border_slug=slugify_topic_segment(border), port_name=raw.get('port_name', ''), border=border, crossing_name=raw.get('crossing_name', ''), hours=raw.get('hours', ''), passenger_vehicle_max_lanes=parse_int_or_none(pv.get('maximum_lanes', '')), commercial_vehicle_max_lanes=parse_int_or_none(cv.get('maximum_lanes', '')), pedestrian_max_lanes=parse_int_or_none(ped.get('maximum_lanes', '')))  # type: ignore[arg-type]
    @staticmethod
    def parse_wait_time(raw: Dict[str, Any]) -> WaitTime:
        pv = raw.get('passenger_vehicle_lanes', {}); ped = raw.get('pedestrian_lanes', {}); cv = raw.get('commercial_vehicle_lanes', {})
        pv_std_delay, pv_std_lanes, pv_std_status = _extract_lane(pv.get('standard_lanes', {})); pv_ns_delay, pv_ns_lanes, pv_ns_status = _extract_lane(pv.get('NEXUS_SENTRI_lanes', {})); pv_rd_delay, pv_rd_lanes, pv_rd_status = _extract_lane(pv.get('ready_lanes', {})); ped_std_delay, ped_std_lanes, ped_std_status = _extract_lane(ped.get('standard_lanes', {})); ped_rd_delay, ped_rd_lanes, ped_rd_status = _extract_lane(ped.get('ready_lanes', {})); cv_std_delay, cv_std_lanes, cv_std_status = _extract_lane(cv.get('standard_lanes', {})); cv_fast_delay, cv_fast_lanes, cv_fast_status = _extract_lane(cv.get('FAST_lanes', {})); border = raw.get('border', '')
        return WaitTime(port_number=raw.get('port_number', ''), border_slug=slugify_topic_segment(border), port_name=raw.get('port_name', ''), border=border, crossing_name=raw.get('crossing_name', ''), port_status=raw.get('port_status', ''), date=raw.get('date', ''), time=raw.get('time', ''), passenger_vehicle_standard_delay=pv_std_delay, passenger_vehicle_standard_lanes_open=pv_std_lanes, passenger_vehicle_standard_operational_status=pv_std_status, passenger_vehicle_nexus_sentri_delay=pv_ns_delay, passenger_vehicle_nexus_sentri_lanes_open=pv_ns_lanes, passenger_vehicle_nexus_sentri_operational_status=pv_ns_status, passenger_vehicle_ready_delay=pv_rd_delay, passenger_vehicle_ready_lanes_open=pv_rd_lanes, passenger_vehicle_ready_operational_status=pv_rd_status, pedestrian_standard_delay=ped_std_delay, pedestrian_standard_lanes_open=ped_std_lanes, pedestrian_standard_operational_status=ped_std_status, pedestrian_ready_delay=ped_rd_delay, pedestrian_ready_lanes_open=ped_rd_lanes, pedestrian_ready_operational_status=ped_rd_status, commercial_vehicle_standard_delay=cv_std_delay, commercial_vehicle_standard_lanes_open=cv_std_lanes, commercial_vehicle_standard_operational_status=cv_std_status, commercial_vehicle_fast_delay=cv_fast_delay, commercial_vehicle_fast_lanes_open=cv_fast_lanes, commercial_vehicle_fast_operational_status=cv_fast_status, construction_notice=raw.get('construction_notice', '') or None)  # type: ignore[arg-type]
