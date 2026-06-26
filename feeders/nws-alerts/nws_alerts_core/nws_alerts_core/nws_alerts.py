"""NWS CAP weather alerts - transport-neutral acquisition."""
from __future__ import annotations
import json, logging, os, unicodedata
from typing import Any, Dict, List, Optional
import aiohttp
from nws_alerts_producer_data.weatheralert import WeatherAlert
from datetime import datetime
from nws_alerts_producer_data.certaintyenum import CertaintyEnum
from nws_alerts_producer_data.messagetypeenum import MessageTypeenum
from nws_alerts_producer_data.severityenum import SeverityEnum
from nws_alerts_producer_data.statusenum import StatusEnum
from nws_alerts_producer_data.urgencyenum import UrgencyEnum
logger = logging.getLogger(__name__)
NWS_API_URL = "https://api.weather.gov/alerts/active"
USER_AGENT = os.environ.get("USER_AGENT") or ("real-time-sources-nws-alerts/0.1.0 " "(+https://github.com/clemensv/real-time-sources; " + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")")
DEFAULT_POLL_INTERVAL = 60
DEFAULT_STATE_FILE = os.path.expanduser("~/.nws_alerts_state.json")
DEFAULT_TOPIC = "nws-alerts"
US_STATE_CODES = {"AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC","PR","VI","GU","AS","MP"}
FIPS_STATE_TO_POSTAL = {"01":"AL","02":"AK","04":"AZ","05":"AR","06":"CA","08":"CO","09":"CT","10":"DE","11":"DC","12":"FL","13":"GA","15":"HI","16":"ID","17":"IL","18":"IN","19":"IA","20":"KS","21":"KY","22":"LA","23":"ME","24":"MD","25":"MA","26":"MI","27":"MN","28":"MS","29":"MO","30":"MT","31":"NE","32":"NV","33":"NH","34":"NJ","35":"NM","36":"NY","37":"NC","38":"ND","39":"OH","40":"OK","41":"OR","42":"PA","44":"RI","45":"SC","46":"SD","47":"TN","48":"TX","49":"UT","50":"VT","51":"VA","53":"WA","54":"WV","55":"WI","56":"WY","60":"AS","66":"GU","69":"MP","72":"PR","78":"VI"}
__all__ = ["NWS_API_URL","USER_AGENT","DEFAULT_POLL_INTERVAL","DEFAULT_STATE_FILE","DEFAULT_TOPIC","US_STATE_CODES","FIPS_STATE_TO_POSTAL","_safe_str","_join_codes","uns_slug","normalize_cap_severity","derive_state","_find_nws_headline","_find_vtec","normalize_alert","NWSAlertsPoller"]
def _safe_str(value: Any) -> Optional[str]:
    if value is None: return None
    text = str(value).strip(); return text if text else None
def _join_codes(geocode: dict, key: str) -> Optional[str]:
    values = geocode.get(key) if geocode else None
    return "; ".join(str(v) for v in values) if values else None
def uns_slug(value: Any) -> str:
    raw = unicodedata.normalize("NFKD", str(value or "unknown")).encode("ascii", "ignore").decode("ascii").lower().strip()
    slug = "".join(ch if ch.isalnum() else "-" for ch in raw).strip("-")
    while "--" in slug: slug = slug.replace("--", "-")
    return slug or "unknown"
def normalize_cap_severity(value: Any) -> str:
    from enum import Enum
    raw = value.value if isinstance(value, Enum) else value
    severity = uns_slug(raw)
    return severity if severity in {"minor","moderate","severe","extreme","unknown"} else "unknown"
def derive_state(props: dict) -> str:
    explicit = _safe_str(props.get("state"))
    if explicit and explicit.upper() in US_STATE_CODES: return explicit.lower()
    geocode = props.get("geocode", {}) or {}
    for ugc in geocode.get("UGC") or []:
        code = str(ugc).strip().upper()
        if len(code) >= 2 and code[:2] in US_STATE_CODES: return code[:2].lower()
    for same in geocode.get("SAME") or []:
        digits = "".join(ch for ch in str(same) if ch.isdigit())
        fips_state = digits[1:3] if len(digits) >= 6 else digits[:2]
        state = FIPS_STATE_TO_POSTAL.get(fips_state)
        if state: return state.lower()
    sender_name = _safe_str(props.get("senderName"))
    if sender_name:
        maybe_state = sender_name.split()[-1].upper()
        if maybe_state in US_STATE_CODES: return maybe_state.lower()
    return "nostate"
def _find_nws_headline(params: dict) -> Optional[str]:
    if not params: return None
    for key in ("NWSheadline","nwsheadline"):
        value = params.get(key)
        if value: return value[0] if isinstance(value, list) else str(value)
    return None
def _find_vtec(params: dict) -> Optional[str]:
    if not params: return None
    value = params.get("VTEC")
    return value[0] if isinstance(value, list) else str(value) if value else None
def normalize_alert(props: dict) -> Optional[WeatherAlert]:
    alert_id = _safe_str(props.get("id")); event = _safe_str(props.get("event")); severity = _safe_str(props.get("severity")) or "Unknown"
    if severity not in {"Extreme","Severe","Moderate","Minor","Unknown"}: severity = "Unknown"
    urgency = _safe_str(props.get("urgency")); certainty = _safe_str(props.get("certainty")); sent = _safe_str(props.get("sent")); status = _safe_str(props.get("status")); message_type = _safe_str(props.get("messageType"))
    if not alert_id or not event or not sent or not status: return None
    geocode = props.get("geocode", {}); params = props.get("parameters", {})
    return WeatherAlert(alert_id=alert_id,state=derive_state(props),event_type=uns_slug(event),area_desc=_safe_str(props.get("areaDesc")),same_codes=_join_codes(geocode,"SAME"),ugc_codes=_join_codes(geocode,"UGC"),sent=datetime.fromisoformat(sent.replace("Z","+00:00")),effective=datetime.fromisoformat(_safe_str(props.get("effective")).replace("Z","+00:00")) if _safe_str(props.get("effective")) else None,onset=datetime.fromisoformat(_safe_str(props.get("onset")).replace("Z","+00:00")) if _safe_str(props.get("onset")) else None,expires=datetime.fromisoformat(_safe_str(props.get("expires")).replace("Z","+00:00")) if _safe_str(props.get("expires")) else None,ends=datetime.fromisoformat(_safe_str(props.get("ends")).replace("Z","+00:00")) if _safe_str(props.get("ends")) else None,status=StatusEnum(status),message_type=MessageTypeenum(message_type) if message_type else None,category=_safe_str(props.get("category")),severity=SeverityEnum(severity),certainty=CertaintyEnum(certainty) if certainty else None,urgency=UrgencyEnum(urgency) if urgency else None,event=event,sender=_safe_str(props.get("sender")),sender_name=_safe_str(props.get("senderName")),headline=_safe_str(props.get("headline")),description=_safe_str(props.get("description")),instruction=_safe_str(props.get("instruction")),response=_safe_str(props.get("response")),scope=_safe_str(props.get("scope")),code=_safe_str(props.get("code")),nws_headline=_find_nws_headline(params),vtec=_find_vtec(params),web=_safe_str(props.get("web")))  # type: ignore[arg-type]
class NWSAlertsPoller:
    def __init__(self, state_file: str = DEFAULT_STATE_FILE, poll_interval: int = DEFAULT_POLL_INTERVAL):
        self.state_file = state_file; self.poll_interval = poll_interval
    async def fetch_alerts(self) -> List[dict]:
        headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60), headers=headers) as session:
            async with session.get(NWS_API_URL) as response:
                response.raise_for_status(); data = await response.json(content_type=None); return data.get("features", [])
    def load_state(self) -> Dict[str, str]:
        if self.state_file and os.path.exists(self.state_file):
            try:
                return json.loads(open(self.state_file, "r", encoding="utf-8").read())
            except (json.JSONDecodeError, OSError):
                return {}
        return {}
    def save_state(self, state: Dict[str, str]) -> None:
        if not self.state_file: return
        state_dir = os.path.dirname(self.state_file)
        if state_dir: os.makedirs(state_dir, exist_ok=True)
        open(self.state_file, "w", encoding="utf-8").write(json.dumps(state))
    async def poll_once(self) -> List[WeatherAlert]:
        state = self.load_state()
        try: features = await self.fetch_alerts()
        except Exception:
            logger.exception("Error fetching NWS alerts"); return []
        alerts: List[WeatherAlert] = []
        for feature in features:
            alert = normalize_alert(feature.get("properties", {}))
            if alert is None: continue
            sent_str = alert.sent.isoformat() if alert.sent else ""; prev_sent = state.get(alert.alert_id)
            if prev_sent is not None and prev_sent >= sent_str: continue
            alerts.append(alert); state[alert.alert_id] = sent_str
        self.save_state(state); return alerts
