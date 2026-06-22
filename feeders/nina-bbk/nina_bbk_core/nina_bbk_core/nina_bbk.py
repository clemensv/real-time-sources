"""NINA/BBK German civil protection warnings - transport-neutral acquisition."""
from __future__ import annotations
import json, logging, os
from typing import Any, Dict, List, Optional
import aiohttp
from nina_bbk_producer_data.civilwarning import CivilWarning
logger = logging.getLogger(__name__)
USER_AGENT = os.environ.get("USER_AGENT") or ("real-time-sources-nina-bbk/0.1.0 " "(+https://github.com/clemensv/real-time-sources; " + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")")
MAP_DATA_URL = "https://warnung.bund.de/api31/{provider}/mapData.json"
DETAIL_URL = "https://warnung.bund.de/api31/warnings/{warning_id}.json"
PROVIDERS = ["mowas", "katwarn", "biwapp", "dwd", "lhp", "police"]
DEFAULT_POLL_INTERVAL = 300
DEFAULT_STATE_FILE = os.path.expanduser("~/.nina_bbk_state.json")
DEFAULT_TOPIC = "nina-bbk"
AGS_STATE_CODES = {"01":"schleswig-holstein","02":"hamburg","03":"niedersachsen","04":"bremen","05":"nordrhein-westfalen","06":"hessen","07":"rheinland-pfalz","08":"baden-wuerttemberg","09":"bayern","10":"saarland","11":"berlin","12":"brandenburg","13":"mecklenburg-vorpommern","14":"sachsen","15":"sachsen-anhalt","16":"thueringen"}
SENDER_STATE_CODES = {"SH":"schleswig-holstein","HH":"hamburg","NI":"niedersachsen","HB":"bremen","NW":"nordrhein-westfalen","HE":"hessen","RP":"rheinland-pfalz","BW":"baden-wuerttemberg","BY":"bayern","SL":"saarland","BE":"berlin","BB":"brandenburg","MV":"mecklenburg-vorpommern","SN":"sachsen","ST":"sachsen-anhalt","TH":"thueringen"}
__all__ = ["USER_AGENT","MAP_DATA_URL","DETAIL_URL","PROVIDERS","DEFAULT_POLL_INTERVAL","DEFAULT_STATE_FILE","DEFAULT_TOPIC","AGS_STATE_CODES","SENDER_STATE_CODES","_safe_str","_first_info","_find_param","_find_event_code","_state_from_areas","_collect_areas","normalize_warning","NINABBKPoller"]
def _safe_str(value: Any) -> Optional[str]:
    if value is None: return None
    s = str(value).strip(); return s if s else None
def _first_info(detail: dict) -> Optional[dict]:
    infos = detail.get('info', [])
    if not infos: return None
    for info in infos:
        lang = (info.get('language') or '').lower()
        if lang in ('de', 'de-de'): return info
    for info in infos:
        lang = (info.get('language') or '').lower()
        if lang.startswith('en'): return info
    return infos[0]
def _find_param(info: dict, name: str) -> Optional[str]:
    for param in info.get('parameter', []):
        if param.get('valueName') == name: return param.get('value')
    return None
def _find_event_code(info: dict) -> Optional[str]:
    for ec in info.get('eventCode', []):
        if ec.get('valueName') == 'profile:DE-BBK-EVENTCODE': return ec.get('value')
    return None
def _state_from_areas(info: dict, sender: Optional[str] = None) -> str:
    codes = _find_param(info, 'warnVerwaltungsbereiche') or ''
    for code in codes.replace(';', ',').split(','):
        digits = ''.join(ch for ch in code.strip() if ch.isdigit())
        if len(digits) >= 2 and digits[:2] in AGS_STATE_CODES: return AGS_STATE_CODES[digits[:2]]
    if sender:
        parts = sender.split('-')
        if len(parts) > 1: return SENDER_STATE_CODES.get(parts[1].upper(), 'unknown')
    return 'unknown'
def _collect_areas(info: dict) -> str:
    descs = []
    for area in info.get('area', []):
        desc = area.get('areaDesc')
        if desc: descs.append(desc)
    return '; '.join(descs)
def normalize_warning(detail: dict, provider: str, map_version: Optional[int] = None) -> Optional[CivilWarning]:
    warning_id = _safe_str(detail.get('identifier'))
    if not warning_id: return None
    info = _first_info(detail)
    if not info: return None
    sender = _safe_str(detail.get('sender')); sent = _safe_str(detail.get('sent')); status = _safe_str(detail.get('status')); msg_type = _safe_str(detail.get('msgType')); scope = _safe_str(detail.get('scope')); references = _safe_str(detail.get('references')); event = _safe_str(info.get('event')); event_code = _find_event_code(info); categories = info.get('category', []); category = categories[0] if categories else None; severity = _safe_str(info.get('severity')); urgency = _safe_str(info.get('urgency')); certainty = _safe_str(info.get('certainty')); headline = _safe_str(info.get('headline')); description = _safe_str(info.get('description')); instruction = _safe_str(info.get('instruction')); web = _safe_str(info.get('web')); contact = _safe_str(info.get('contact')); language = _safe_str(info.get('language')); sender_name = _find_param(info, 'sender_langname'); verwaltungsbereiche = _find_param(info, 'warnVerwaltungsbereiche'); state = _state_from_areas(info, sender); area_desc = _collect_areas(info)
    if not event or not severity or not urgency or not certainty: return None
    return CivilWarning(warning_id=warning_id, provider=provider, state=state, version=map_version, sender=sender, sender_name=sender_name, sent=sent, status=status, msg_type=msg_type, scope=scope, references=references, event=event, event_code=event_code, category=category, severity=severity, urgency=urgency, certainty=certainty, headline=headline, description=description, instruction=instruction, web=web, contact=contact, area_desc=area_desc if area_desc else None, verwaltungsbereiche=verwaltungsbereiche, language=language)
class NINABBKPoller:
    def __init__(self, state_file: str = DEFAULT_STATE_FILE, poll_interval: int = DEFAULT_POLL_INTERVAL, providers: Optional[List[str]] = None):
        self.state_file = state_file; self.poll_interval = poll_interval; self.providers = providers or PROVIDERS
    async def fetch_map_data(self, session: aiohttp.ClientSession, provider: str) -> List[dict]:
        url = MAP_DATA_URL.format(provider=provider)
        try:
            async with session.get(url) as response:
                if response.status == 404: return []
                response.raise_for_status(); data = await response.json(content_type=None); return data if isinstance(data, list) else []
        except Exception:
            logger.warning('Failed to fetch map data for %s', provider, exc_info=True); return []
    async def fetch_detail(self, session: aiohttp.ClientSession, warning_id: str) -> Optional[dict]:
        url = DETAIL_URL.format(warning_id=warning_id)
        try:
            async with session.get(url) as response:
                if response.status == 404: return None
                response.raise_for_status(); return await response.json(content_type=None)
        except Exception:
            logger.warning('Failed to fetch detail for %s', warning_id, exc_info=True); return None
    def load_state(self) -> Dict[str, str]:
        if self.state_file and os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f: return json.load(f)
            except (json.JSONDecodeError, OSError): return {}
        return {}
    def save_state(self, state: Dict[str, str]):
        if self.state_file:
            with open(self.state_file, 'w', encoding='utf-8') as f: json.dump(state, f)
    async def poll_once(self):
        state = self.load_state(); new_warnings = []
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60), headers={'User-Agent': USER_AGENT}) as session:
            for provider in self.providers:
                try: stubs = await self.fetch_map_data(session, provider)
                except Exception: logger.exception('Error fetching %s', provider); continue
                for stub in stubs:
                    wid = stub.get('id')
                    if not wid: continue
                    version = stub.get('version'); version_str = str(version) if version is not None else ''; prev_version = state.get(wid)
                    if prev_version is not None and prev_version >= version_str: continue
                    detail = await self.fetch_detail(session, wid)
                    if detail is None: continue
                    warning = normalize_warning(detail, provider, version)
                    if warning is None: continue
                    new_warnings.append(warning); state[wid] = version_str
        self.save_state(state); return new_warnings
