"""PTWC/NTWC tsunami bulletins - transport-neutral acquisition."""
from __future__ import annotations
import json, logging, os, re, xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional
import aiohttp
from ptwc_tsunami_producer_data.tsunamibulletin import TsunamiBulletin
from datetime import datetime
from ptwc_tsunami_producer_data.basinenum import BasinEnum
from ptwc_tsunami_producer_data.categoryenum import CategoryEnum
from ptwc_tsunami_producer_data.feedenum import FeedEnum
from ptwc_tsunami_producer_data.ptwclevelenum import PtwcLevelenum
logger = logging.getLogger(__name__)
FEEDS = {"PAAQ":"https://www.tsunami.gov/events/xml/PAAQAtom.xml","PHEB":"https://www.tsunami.gov/events/xml/PHEBAtom.xml"}
NS = {"atom":"http://www.w3.org/2005/Atom","geo":"http://www.w3.org/2003/01/geo/wgs84_pos#","xhtml":"http://www.w3.org/1999/xhtml"}
DEFAULT_POLL_INTERVAL = 300
DEFAULT_STATE_FILE = os.path.expanduser("~/.ptwc_tsunami_state.json")
DEFAULT_TOPIC = "ptwc-tsunami"
USER_AGENT = os.environ.get("USER_AGENT") or ("real-time-sources-ptwc-tsunami/0.1.0 " "(+https://github.com/clemensv/real-time-sources; " + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")")
FEED_BASINS = {"PAAQ":"alaska","PHEB":"pacific"}
__all__ = ["FEEDS","NS","DEFAULT_POLL_INTERVAL","DEFAULT_STATE_FILE","DEFAULT_TOPIC","USER_AGENT","FEED_BASINS","_safe_str","_text","_parse_summary_field","_parse_note","_basin_for_feed","_ptwc_level","_get_summary_html","parse_entry","PTWCTsunamiPoller"]
def _safe_str(value: Any) -> Optional[str]:
    if value is None: return None
    text = str(value).strip(); return text if text else None
def _text(element: Optional[ET.Element]) -> Optional[str]:
    return element.text.strip() if element is not None and element.text else None
def _parse_summary_field(summary_html: str, field_name: str) -> Optional[str]:
    match = re.search(r"<strong>\s*" + re.escape(field_name) + r"\s*:?\s*</strong>\s*(.+?)(?:<br\s*/?>|$)", summary_html, re.I)
    if match:
        value = re.sub(r"<[^>]+>", "", match.group(1)).strip(); return value if value else None
    return None
def _parse_note(summary_html: str) -> Optional[str]:
    match = re.search(r"<b>Note:</b>\s*(.+?)(?:<br\s*/?>|<strong>|$)", summary_html, re.I)
    if match:
        value = re.sub(r"<[^>]+>", "", match.group(1)).strip().rstrip("*").strip(); return value if value else None
    return None
def _basin_for_feed(feed_name: str) -> str: return FEED_BASINS.get(feed_name, "unknown")
def _ptwc_level(category: Optional[str]) -> str:
    text = (category or "unknown").strip().lower(); return text if text in {"warning","advisory","watch","information"} else "unknown"
def _get_summary_html(entry: ET.Element) -> str:
    summary_el = entry.find("atom:summary", NS)
    if summary_el is None: return ""
    raw = ET.tostring(summary_el, encoding="unicode", method="html")
    raw = re.sub(r"^<[^>]+>", "", raw, count=1); raw = re.sub(r"</[^>]+>$", "", raw.rstrip(), count=1); raw = re.sub(r"<(/?)(?:\w+:)", r"<", raw); raw = re.sub(r'\s+xmlns:\w+="[^"]*"', "", raw); raw = re.sub(r'\s+xmlns="[^"]*"', "", raw)
    return raw
def parse_entry(entry: ET.Element, feed_name: str, center: Optional[str] = None) -> Optional[TsunamiBulletin]:
    bulletin_id = _text(entry.find("atom:id", NS)); title = _text(entry.find("atom:title", NS)); updated = _text(entry.find("atom:updated", NS))
    if not bulletin_id or not title or not updated: return None
    lat_el = entry.find("geo:lat", NS); lon_el = entry.find("geo:long", NS); latitude = float(lat_el.text.strip()) if lat_el is not None and lat_el.text else None; longitude = float(lon_el.text.strip()) if lon_el is not None and lon_el.text else None
    summary_html = _get_summary_html(entry); category = _parse_summary_field(summary_html, "Category"); magnitude = _parse_summary_field(summary_html, "Preliminary Magnitude"); affected_region = _parse_summary_field(summary_html, "Affected Region"); note = _parse_note(summary_html)
    bulletin_url = None; cap_url = None
    for link in entry.findall("atom:link", NS):
        rel = link.get("rel", ""); link_type = link.get("type", ""); href = link.get("href", "").strip()
        if rel == "alternate" and href: bulletin_url = href
        elif rel == "related" and "cap" in link_type and href: cap_url = href
    return TsunamiBulletin(bulletin_id=bulletin_id,feed=FeedEnum(feed_name),basin=BasinEnum(_basin_for_feed(feed_name)),ptwc_level=PtwcLevelenum(_ptwc_level(category)),center=center,title=title,updated=datetime.fromisoformat(updated),latitude=latitude,longitude=longitude,category=CategoryEnum(category) if category else None,magnitude=magnitude,affected_region=affected_region,note=note,bulletin_url=bulletin_url,cap_url=cap_url)
class PTWCTsunamiPoller:
    def __init__(self, state_file: str = DEFAULT_STATE_FILE, poll_interval: int = DEFAULT_POLL_INTERVAL, feeds: Optional[List[str]] = None):
        self.state_file = state_file; self.poll_interval = poll_interval; self.feeds = feeds or list(FEEDS.keys())
    async def fetch_feed(self, session: aiohttp.ClientSession, feed_name: str) -> Optional[ET.Element]:
        url = FEEDS.get(feed_name)
        if not url: return None
        try:
            async with session.get(url) as response:
                if response.status == 404: return None
                response.raise_for_status(); return ET.fromstring(await response.read())
        except Exception:
            logger.warning("Failed to fetch feed %s", feed_name, exc_info=True); return None
    def load_state(self) -> Dict[str, str]:
        if self.state_file and os.path.exists(self.state_file):
            try: return json.loads(open(self.state_file, 'r', encoding='utf-8').read())
            except (json.JSONDecodeError, OSError): return {}
        return {}
    def save_state(self, state: Dict[str, str]) -> None:
        if not self.state_file: return
        state_dir = os.path.dirname(self.state_file)
        if state_dir: os.makedirs(state_dir, exist_ok=True)
        open(self.state_file, 'w', encoding='utf-8').write(json.dumps(state))
    async def poll_once(self) -> List[TsunamiBulletin]:
        state = self.load_state(); bulletins: List[TsunamiBulletin] = []
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60), headers={"User-Agent": USER_AGENT}) as session:
            for feed_name in self.feeds:
                root = await self.fetch_feed(session, feed_name)
                if root is None: continue
                center = _text(root.find("atom:author/atom:name", NS))
                for entry in root.findall("atom:entry", NS):
                    bulletin = parse_entry(entry, feed_name, center)
                    if bulletin is None: continue
                    updated_str = bulletin.updated or ""; prev_updated = state.get(bulletin.bulletin_id)
                    if prev_updated is not None and prev_updated >= updated_str: continue
                    bulletins.append(bulletin); state[bulletin.bulletin_id] = updated_str
        self.save_state(state); return bulletins
