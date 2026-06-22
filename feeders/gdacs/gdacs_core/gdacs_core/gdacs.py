"""Transport-agnostic acquisition and state handling for the GDACS disaster alert bridge."""

from __future__ import annotations

import asyncio
import importlib
import json
import logging
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import aiohttp

logger = logging.getLogger(__name__)

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-gdacs/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

GDACS_RSS_URL = "https://www.gdacs.org/xml/rss.xml"

NAMESPACES = {
    'gdacs': 'http://www.gdacs.org',
    'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
    'georss': 'http://www.georss.org/georss',
}

_DisasterAlert: Any = None


def _get_alert_class() -> Any:
    """Lazily resolve the first available DisasterAlert data class."""
    for mod_name in (
        "gdacs_producer_data.disasteralert",
        "gdacs_amqp_producer_data.disasteralert",
        "gdacs_mqtt_producer_data.disasteralert",
    ):
        try:
            mod = importlib.import_module(mod_name)
            return getattr(mod, "DisasterAlert")
        except (ImportError, AttributeError):
            pass
    raise ImportError(
        "No gdacs producer data package found. "
        "Install gdacs_producer, gdacs_amqp_producer, or gdacs_mqtt_producer."
    )


def _disaster_alert_class() -> Any:
    global _DisasterAlert
    if _DisasterAlert is None:
        _DisasterAlert = _get_alert_class()
    return _DisasterAlert


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in ('1', 'true', 'yes', 'on')


def _text(element: ET.Element, tag: str, ns: Optional[str] = None) -> Optional[str]:
    """Extract text content from an XML child element."""
    if ns:
        child = element.find(f'{{{NAMESPACES[ns]}}}{tag}')
    else:
        child = element.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    return None


def _attr(element: ET.Element, tag: str, ns: str, attr: str) -> Optional[str]:
    """Extract an attribute value from an XML child element."""
    child = element.find(f'{{{NAMESPACES[ns]}}}{tag}')
    if child is not None:
        return child.get(attr)
    return None


def _parse_float(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _parse_int(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _parse_bool(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None
    return value.lower() in ('true', '1', 'yes')


def _parse_datetime(value: Optional[str]) -> Optional[str]:
    """Parse a date string into ISO-8601 format. Returns None if unparseable."""
    if value is None:
        return None
    for fmt in (
        '%a, %d %b %Y %H:%M:%S %Z',
        '%a, %d %b %Y %H:%M:%S %z',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%d %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
    ):
        try:
            dt = datetime.strptime(value.strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat()
        except ValueError:
            continue
    return value.strip()


def _parse_bbox(value: Optional[str]):
    """Parse a GDACS bounding box string into (min_lon, max_lon, min_lat, max_lat)."""
    if not value:
        return None, None, None, None
    parts = value.replace(',', ' ').split()
    floats = []
    for p in parts:
        try:
            floats.append(float(p))
        except ValueError:
            pass
    if len(floats) == 4:
        return floats[0], floats[1], floats[2], floats[3]
    return None, None, None, None


def _alert_color(alert_level: str) -> str:
    return alert_level.strip().lower()


def _is_known_alert_level(alert_level: str) -> bool:
    return _alert_color(alert_level) in {'green', 'orange', 'red'}


def _is_known_event_type(event_type: str) -> bool:
    return event_type in {'EQ', 'TC', 'FL', 'VO', 'FF', 'DR'}


def parse_rss_item(item: ET.Element) -> Optional[Any]:
    """Parse a single RSS item element into a DisasterAlert data class."""
    event_type = _text(item, 'eventtype', 'gdacs')
    event_id = _text(item, 'eventid', 'gdacs')
    alert_level = _text(item, 'alertlevel', 'gdacs')
    lat_str = _text(item, 'lat', 'geo')
    lon_str = _text(item, 'long', 'geo')
    from_date_str = _text(item, 'fromdate', 'gdacs')
    severity_value_str = _attr(item, 'severity', 'gdacs', 'value')
    severity_unit = _attr(item, 'severity', 'gdacs', 'unit')

    latitude = _parse_float(lat_str)
    longitude = _parse_float(lon_str)
    severity_value = _parse_float(severity_value_str)

    if not event_type or not event_id or not alert_level:
        return None
    if not _is_known_event_type(event_type):
        return None
    if not _is_known_alert_level(alert_level):
        return None
    if latitude is None or longitude is None:
        return None
    if severity_value is None or severity_unit is None:
        return None

    from_date = _parse_datetime(from_date_str)
    if from_date is None:
        return None

    episode_id = _text(item, 'episodeid', 'gdacs')
    alert_score = _parse_float(_text(item, 'alertscore', 'gdacs'))
    episode_alert_level = _text(item, 'episodealertlevel', 'gdacs')
    episode_alert_score = _parse_float(_text(item, 'episodealertscore', 'gdacs'))
    event_name = _text(item, 'eventname', 'gdacs')
    country = _text(item, 'country', 'gdacs') or 'unknown'
    iso3 = _text(item, 'iso3', 'gdacs')
    to_date = _parse_datetime(_text(item, 'todate', 'gdacs'))
    vulnerability = _parse_float(_text(item, 'vulnerability', 'gdacs'))
    is_current = _parse_bool(_text(item, 'iscurrent', 'gdacs'))
    version = _parse_int(_text(item, 'version', 'gdacs'))
    description_text = _text(item, 'description')
    link = _text(item, 'link')
    pub_date = _parse_datetime(_text(item, 'pubDate'))

    population_value = _parse_float(_attr(item, 'population', 'gdacs', 'value'))
    population_unit = _attr(item, 'population', 'gdacs', 'unit')

    severity_elem = item.find(f'{{{NAMESPACES["gdacs"]}}}severity')
    severity_text = severity_elem.text.strip() if severity_elem is not None and severity_elem.text else None

    bbox_str = _text(item, 'bbox', 'gdacs')
    bbox_min_lon, bbox_max_lon, bbox_min_lat, bbox_max_lat = _parse_bbox(bbox_str)

    DisasterAlert = _disaster_alert_class()
    return DisasterAlert(
        event_type=event_type,
        event_id=event_id,
        alert_level=alert_level,
        alert_color=_alert_color(alert_level),
        latitude=latitude,
        longitude=longitude,
        from_date=from_date,
        severity_value=severity_value,
        severity_unit=severity_unit,
        episode_id=episode_id,
        alert_score=alert_score,
        episode_alert_level=episode_alert_level,
        episode_alert_score=episode_alert_score,
        event_name=event_name,
        country=country,
        iso3=iso3,
        to_date=to_date,
        population_value=population_value,
        population_unit=population_unit,
        vulnerability=vulnerability,
        bbox_min_lon=bbox_min_lon,
        bbox_max_lon=bbox_max_lon,
        bbox_min_lat=bbox_min_lat,
        bbox_max_lat=bbox_max_lat,
        severity_text=severity_text,
        is_current=is_current,
        version=version,
        description=description_text,
        link=link,
        pub_date=pub_date,
    )


class GDACSPoller:
    """Transport-neutral GDACS RSS poller: fetches, parses, and tracks state."""

    def __init__(self, state_file: Optional[str] = None, poll_interval: int = 300):
        self.state_file = state_file
        self.poll_interval = poll_interval

    async def fetch_feed(self) -> str:
        """Download the GDACS RSS feed XML."""
        async with aiohttp.ClientSession(
            headers={"User-Agent": USER_AGENT},
            timeout=aiohttp.ClientTimeout(total=60),
        ) as session:
            async with session.get(GDACS_RSS_URL) as response:
                response.raise_for_status()
                return await response.text()

    def parse_feed(self, xml_text: str):
        """Parse the RSS XML and return a list of DisasterAlert objects."""
        root = ET.fromstring(xml_text)
        channel = root.find('channel')
        if channel is None:
            return []
        alerts = []
        for item in channel.findall('item'):
            alert = parse_rss_item(item)
            if alert is not None:
                alerts.append(alert)
        return alerts

    def load_state(self) -> Dict[str, int]:
        """Load the state file tracking seen event+episode combinations and versions."""
        if self.state_file and os.path.exists(self.state_file):
            with open(self.state_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    logger.error("Error decoding state file")
                    return {}
        return {}

    def save_state(self, state: Dict[str, int]):
        """Persist the state dict to disk."""
        if self.state_file:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f)

    @staticmethod
    def _state_key(alert: Any) -> str:
        """Build a state key from event_type, event_id, and episode_id."""
        episode = alert.episode_id or '0'
        return f"{alert.event_type}_{alert.event_id}_{episode}"
