"""BOM Australia transport-neutral acquisition, parsing and state core.

Contains the BOMAustraliaAPI client, all data-parsing helpers, and state
management functions.  No Kafka, MQTT or AMQP runtime dependencies.
"""

import json
import logging
import os
import re
import threading
import typing
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import requests
from dataclasses import dataclass

logger = logging.getLogger(__name__)

BOM_BASE_URL = "http://reg.bom.gov.au/fwo"
BOM_STATIONS_URL = "http://www.bom.gov.au/climate/data/lists_by_element/stations.txt"

STATE_OBSERVATION_PAGES = {
    "NSW": "http://www.bom.gov.au/nsw/observations/nswall.shtml",
    "VIC": "http://www.bom.gov.au/vic/observations/vicall.shtml",
    "QLD": "http://www.bom.gov.au/qld/observations/qldall.shtml",
    "WA": "http://www.bom.gov.au/wa/observations/waall.shtml",
    "SA": "http://www.bom.gov.au/sa/observations/saall.shtml",
    "TAS": "http://www.bom.gov.au/tas/observations/tasall.shtml",
    "NT": "http://www.bom.gov.au/nt/observations/ntall.shtml",
    "ACT": "http://www.bom.gov.au/act/observations/canberra.shtml",
}

STATION_LINK_PATTERN = re.compile(
    r"products/(ID[A-Z]\d{5})/(?:ID[A-Z]\d{5})\.(\d+)\.shtml"
)

STATE_TO_PRODUCT = {
    "NSW": "IDN60801",
    "VIC": "IDV60801",
    "QLD": "IDQ60801",
    "WA": "IDW60801",
    "SA": "IDS60801",
    "TAS": "IDT60801",
    "NT": "IDD60801",
    "ANT": "IDT60801",
}

FALLBACK_STATIONS = [
    ("IDN60801", 94767),
    ("IDV60801", 94866),
    ("IDQ60801", 94576),
    ("IDW60801", 94610),
    ("IDS60801", 94648),
    ("IDT60801", 94970),
    ("IDD60801", 94120),
    ("IDN60903", 94926),
]

WARNING_FEEDS = [
    "https://www.bom.gov.au/fwo/IDZ00054.warnings_nsw.xml",
    "https://www.bom.gov.au/fwo/IDZ00059.warnings_vic.xml",
    "https://www.bom.gov.au/fwo/IDZ00056.warnings_qld.xml",
    "https://www.bom.gov.au/fwo/IDZ00060.warnings_wa.xml",
    "https://www.bom.gov.au/fwo/IDZ00057.warnings_sa.xml",
    "https://www.bom.gov.au/fwo/IDZ00058.warnings_tas.xml",
    "https://www.bom.gov.au/fwo/IDZ00055.warnings_nt.xml",
]

WARNING_TITLE_PATTERN = re.compile(
    r"^(?P<issued_local_time_text>\d{2}/\d{2}:\d{2}\s+[A-Z]{2,4})\s+(?P<warning_type>.+?)(?:\s+for\s+(?P<affected_area_text>.+))?$"
)
WARNING_FEED_STATE_PATTERN = re.compile(r"warnings_(?P<state>[a-z]+)\.xml$", re.IGNORECASE)

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-bom-australia/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)


# ---------------------------------------------------------------------------
# Lightweight transport-neutral data containers
# ---------------------------------------------------------------------------

@dataclass
class Station:
    """Reference metadata for a BOM weather observation station."""
    station_wmo: str
    name: str
    product_id: typing.Optional[str]
    state: typing.Optional[str]
    time_zone: typing.Optional[str]
    latitude: float
    longitude: float


@dataclass
class WeatherObservation:
    """A single half-hourly surface observation record."""
    station_wmo: str
    station_name: str
    observation_time_utc: str
    local_time: str
    air_temp: typing.Optional[float]
    apparent_temp: typing.Optional[float]
    dewpt: typing.Optional[float]
    rel_hum: typing.Optional[int]
    delta_t: typing.Optional[float]
    wind_dir: typing.Optional[str]
    wind_spd_kmh: typing.Optional[int]
    wind_spd_kt: typing.Optional[int]
    gust_kmh: typing.Optional[int]
    gust_kt: typing.Optional[int]
    press: typing.Optional[float]
    press_qnh: typing.Optional[float]
    press_msl: typing.Optional[float]
    press_tend: typing.Optional[str]
    rain_trace: typing.Optional[str]
    cloud: typing.Optional[str]
    cloud_oktas: typing.Optional[int]
    cloud_base_m: typing.Optional[int]
    cloud_type: typing.Optional[str]
    vis_km: typing.Optional[str]
    weather: typing.Optional[str]
    sea_state: typing.Optional[str]
    swell_dir_worded: typing.Optional[str]
    swell_height: typing.Optional[float]
    swell_period: typing.Optional[float]
    latitude: float
    longitude: float
    state: typing.Optional[str]


@dataclass
class WarningBulletin:
    """A BOM weather warning bulletin item from an RSS warning feed."""
    warning_id: str
    warning_url: str
    feed_url: str
    feed_title: str
    title: str
    published_at: str
    issued_local_time_text: typing.Optional[str]
    warning_type: typing.Optional[str]
    affected_area_text: typing.Optional[str]
    severity: typing.Optional[str]
    state: typing.Optional[str]


# ---------------------------------------------------------------------------
# BOM HTTP client
# ---------------------------------------------------------------------------

class BOMAustraliaAPI:
    """Client for the BOM weather observation JSON feeds."""

    def __init__(self, base_url: str = BOM_BASE_URL, polling_interval: int = 600, fetch_workers: int = 12):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.fetch_workers = max(1, fetch_workers)
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT

    def discover_stations(self, state_filter: typing.Optional[str] = None) -> list[tuple[str, int]]:
        """Discover active BOM observing stations."""
        allowed_states: typing.Optional[set[str]] = None
        if state_filter:
            allowed_states = {s.strip().upper() for s in state_filter.split(",") if s.strip()}

        seen: set[tuple[str, int]] = set()
        stations: list[tuple[str, int]] = []

        for state, page_url in STATE_OBSERVATION_PAGES.items():
            if allowed_states and state not in allowed_states:
                continue
            try:
                response = self.session.get(page_url, timeout=30)
                response.raise_for_status()
            except Exception as e:
                logger.warning("Could not fetch %s station listing %s: %s", state, page_url, e)
                continue
            matches = STATION_LINK_PATTERN.findall(response.text)
            state_count = 0
            for product_id, wmo_str in matches:
                try:
                    wmo_id = int(wmo_str)
                except ValueError:
                    continue
                pair = (product_id, wmo_id)
                if pair in seen:
                    continue
                seen.add(pair)
                stations.append(pair)
                state_count += 1
            logger.info("Discovered %d %s observing stations from %s", state_count, state, page_url)

        if stations:
            logger.info("Discovered %d total observing stations", len(stations))
            return stations

        logger.warning("State listing scrape returned no stations; falling back to climate stations.txt")
        legacy = self._discover_from_climate_list(allowed_states)
        if legacy:
            return legacy
        logger.warning("Climate stations.txt fallback empty; using hard-coded capital-city list")
        return list(FALLBACK_STATIONS)

    def _discover_from_climate_list(self, allowed_states: typing.Optional[set[str]]) -> list[tuple[str, int]]:
        """Legacy discovery path that parses the climate stations.txt list."""
        try:
            response = self.session.get(BOM_STATIONS_URL, timeout=60)
            response.raise_for_status()
        except Exception as e:
            logger.warning("Climate station discovery failed: %s", e)
            return []

        stations: list[tuple[str, int]] = []
        lines = response.text.strip().split("\n")
        for line in lines[4:]:
            if len(line) < 131:
                continue
            try:
                end_year = line[63:71].strip()
                wmo_str = line[130:].strip().replace("\r", "")
                state = line[105:110].strip()
                is_active = (end_year in ("", "..") or
                             (end_year.isdigit() and int(end_year) >= 2025))
                has_wmo = wmo_str not in ("", "..") and wmo_str.isdigit()
                if not is_active or not has_wmo:
                    continue
                if allowed_states and state not in allowed_states:
                    continue
                product_id = STATE_TO_PRODUCT.get(state)
                if not product_id:
                    continue
                stations.append((product_id, int(wmo_str)))
            except (ValueError, IndexError):
                continue
        return stations

    def get_station_observations(self, product_id: str, wmo_id: int) -> dict:
        """Fetch the 72-hour observation product for a single station."""
        url = f"{self.base_url}/{product_id}/{product_id}.{wmo_id}.json"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_warning_feed(self, feed_url: str) -> str:
        """Fetch a BOM RSS warning feed as XML text."""
        response = self.session.get(feed_url, timeout=30)
        response.raise_for_status()
        return response.text

    @staticmethod
    def parse_station(product_id: str, obs_data: dict) -> typing.Optional[Station]:
        """Parse station reference data from an observation product response."""
        header = obs_data.get("observations", {}).get("header", [])
        data = obs_data.get("observations", {}).get("data", [])
        if not header or not data:
            return None
        hdr = header[0]
        first_obs = data[0]
        wmo = first_obs.get("wmo")
        if wmo is None:
            return None
        return Station(
            station_wmo=str(wmo),
            name=first_obs.get("name", hdr.get("name", "")),
            product_id=product_id,
            state=hdr.get("state", ""),
            time_zone=hdr.get("time_zone", ""),
            latitude=float(first_obs.get("lat", 0.0)),
            longitude=float(first_obs.get("lon", 0.0)),
        )

    @staticmethod
    def parse_observation(obs_record: dict, default_state: typing.Optional[str] = None) -> typing.Optional[WeatherObservation]:
        """Parse a single observation record from the BOM JSON data array."""
        wmo = obs_record.get("wmo")
        utc_str = obs_record.get("aifstime_utc")
        if wmo is None or not utc_str:
            return None
        try:
            ts = datetime.strptime(utc_str, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc).isoformat()
        except (ValueError, TypeError):
            return None

        def to_float(v):
            if v is None or v == "-" or v == "":
                return None
            try:
                return float(v)
            except (ValueError, TypeError):
                return None

        def to_int(v):
            if v is None or v == "-" or v == "":
                return None
            try:
                return int(v)
            except (ValueError, TypeError):
                return None

        def to_str(v):
            if v is None or v == "-":
                return None
            return str(v)

        return WeatherObservation(
            station_wmo=str(wmo),
            station_name=obs_record.get("name", ""),
            observation_time_utc=ts,
            local_time=obs_record.get("local_date_time_full", ""),
            air_temp=to_float(obs_record.get("air_temp")),
            apparent_temp=to_float(obs_record.get("apparent_t")),
            dewpt=to_float(obs_record.get("dewpt")),
            rel_hum=to_int(obs_record.get("rel_hum")),
            delta_t=to_float(obs_record.get("delta_t")),
            wind_dir=to_str(obs_record.get("wind_dir")),
            wind_spd_kmh=to_int(obs_record.get("wind_spd_kmh")),
            wind_spd_kt=to_int(obs_record.get("wind_spd_kt")),
            gust_kmh=to_int(obs_record.get("gust_kmh")),
            gust_kt=to_int(obs_record.get("gust_kt")),
            press=to_float(obs_record.get("press")),
            press_qnh=to_float(obs_record.get("press_qnh")),
            press_msl=to_float(obs_record.get("press_msl")),
            press_tend=to_str(obs_record.get("press_tend")),
            rain_trace=to_str(obs_record.get("rain_trace")),
            cloud=to_str(obs_record.get("cloud")),
            cloud_oktas=to_int(obs_record.get("cloud_oktas")),
            cloud_base_m=to_int(obs_record.get("cloud_base_m")),
            cloud_type=to_str(obs_record.get("cloud_type")),
            vis_km=to_str(obs_record.get("vis_km")),
            weather=to_str(obs_record.get("weather")),
            sea_state=to_str(obs_record.get("sea_state")),
            swell_dir_worded=to_str(obs_record.get("swell_dir_worded")),
            swell_height=to_float(obs_record.get("swell_height")),
            swell_period=to_float(obs_record.get("swell_period")),
            latitude=float(obs_record.get("lat", 0.0)),
            longitude=float(obs_record.get("lon", 0.0)),
            state=to_str(obs_record.get("state")) or to_str(default_state),
        )

    @staticmethod
    def parse_warning_feed(feed_url: str, feed_xml: str) -> list[WarningBulletin]:
        """Parse a BOM RSS warning feed into WarningBulletin records."""
        try:
            root = ET.fromstring(feed_xml)
        except ET.ParseError:
            return []

        channel = root.find("channel")
        if channel is None:
            return []

        feed_title = " ".join((channel.findtext("title") or "").split())
        warnings: list[WarningBulletin] = []

        for item in channel.findall("item"):
            title = " ".join((item.findtext("title") or "").split())
            warning_url = (item.findtext("link") or "").strip()
            published_text = (item.findtext("pubDate") or "").strip()
            guid = (item.findtext("guid") or warning_url).strip()

            if not title or not warning_url or not published_text:
                continue

            try:
                published_at = parsedate_to_datetime(published_text).astimezone(timezone.utc).isoformat()
            except (TypeError, ValueError, IndexError):
                continue

            warning_id = _warning_id_from_url(guid)
            if not warning_id:
                continue

            match = WARNING_TITLE_PATTERN.match(title)
            warning_type = title
            issued_local_time_text = None
            affected_area_text = None
            if match:
                issued_local_time_text = match.group("issued_local_time_text")
                warning_type = match.group("warning_type")
                affected_area_text = match.group("affected_area_text")

            severity = None
            if warning_type:
                severity_token = warning_type.split()[0].strip().lower()
                severity = re.sub(r"[^a-z0-9]+", "-", severity_token).strip("-") or None

            state = None
            state_match = WARNING_FEED_STATE_PATTERN.search(feed_url)
            if state_match:
                state = state_match.group("state").lower()

            warnings.append(WarningBulletin(
                warning_id=warning_id,
                warning_url=warning_url,
                feed_url=feed_url,
                feed_title=feed_title,
                title=title,
                published_at=published_at,
                issued_local_time_text=issued_local_time_text,
                warning_type=warning_type,
                affected_area_text=affected_area_text,
                severity=severity,
                state=state,
            ))

        return warnings


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------

def _warning_id_from_url(url: str) -> str:
    """Extract a BOM warning identifier from the linked warning product URL."""
    basename = os.path.basename(url.strip().rstrip("/"))
    if basename.endswith(".shtml"):
        basename = basename[:-6]
    return basename


def _parse_warning_feed_list(feed_csv: str) -> list[str]:
    """Parse a comma-separated list of warning feed URLs or relative feed paths."""
    feeds = []
    for entry in feed_csv.split(","):
        entry = entry.strip()
        if not entry:
            continue
        if entry.startswith("http://") or entry.startswith("https://"):
            feeds.append(entry)
        else:
            feeds.append(f"https://www.bom.gov.au{entry}")
    return feeds


def _normalize_state(state: typing.Any) -> dict[str, dict[str, str]]:
    """Normalize persisted state and preserve compatibility with legacy flat observation maps."""
    normalized: dict[str, dict[str, str]] = {"observations": {}, "warnings": {}}
    if not isinstance(state, dict):
        return normalized
    if "observations" in state or "warnings" in state:
        observations = state.get("observations", {})
        warnings = state.get("warnings", {})
        if isinstance(observations, dict):
            normalized["observations"].update(observations)
        if isinstance(warnings, dict):
            normalized["warnings"].update(warnings)
        return normalized
    normalized["observations"].update(state)
    return normalized


def _trim_state_bucket(bucket: dict[str, str]) -> dict[str, str]:
    """Trim a state bucket when it grows beyond the retention threshold."""
    if len(bucket) <= 100000:
        return bucket
    keys = list(bucket.keys())
    return {key: bucket[key] for key in keys[-50000:]}


def _load_state(state_file: str) -> dict:
    """Load persisted dedup state from a JSON file."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                return _normalize_state(json.load(f))
    except Exception as e:
        logging.warning("Could not load state from %s: %s", state_file, e)
    return _normalize_state(None)


def _save_state(state_file: str, data: dict) -> None:
    """Save dedup state to a JSON file, keeping at most 100000 entries."""
    if not state_file:
        return
    try:
        state = _normalize_state(data)
        state["observations"] = _trim_state_bucket(state["observations"])
        state["warnings"] = _trim_state_bucket(state["warnings"])
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f)
    except Exception as e:
        logging.warning("Could not save state to %s: %s", state_file, e)


def _parse_station_list(station_csv: str) -> list[tuple[str, int]]:
    """Parse a comma-separated list of product_id:wmo_id pairs."""
    stations = []
    for entry in station_csv.split(","):
        entry = entry.strip()
        if ":" in entry:
            pid, wmo = entry.split(":", 1)
            stations.append((pid.strip(), int(wmo.strip())))
    return stations


def _is_http_404(exc: Exception) -> bool:
    response = getattr(exc, "response", None)
    return bool(response is not None and getattr(response, "status_code", None) == 404)


# ---------------------------------------------------------------------------
# Parallel acquisition helpers (transport-neutral, accept any duck-typed sender)
# ---------------------------------------------------------------------------

def fetch_stations_parallel(
    api: BOMAustraliaAPI,
    station_list: list[tuple[str, int]],
) -> list[tuple[Station, str]]:
    """Fetch station reference data for all stations in parallel.

    Returns a list of (Station, product_id) tuples for successfully parsed stations.
    """
    results: list[tuple[Station, str]] = []
    lock = threading.Lock()

    def _process(item: tuple[str, int]) -> None:
        product_id, wmo_id = item
        try:
            obs_data = api.get_station_observations(product_id, wmo_id)
        except Exception as e:
            if _is_http_404(e):
                logger.debug("Station product not published for %s/%d (404)", product_id, wmo_id)
            else:
                logger.warning("Failed to fetch station %s/%d: %s", product_id, wmo_id, e)
            return
        try:
            station = api.parse_station(product_id, obs_data)
            if station:
                with lock:
                    results.append((station, product_id))
        except Exception as e:
            logger.warning("Failed to parse station %s/%d: %s", product_id, wmo_id, e)

    with ThreadPoolExecutor(max_workers=api.fetch_workers) as pool:
        list(pool.map(_process, station_list))
    return results


def fetch_latest_observations_parallel(
    api: BOMAustraliaAPI,
    station_list: list[tuple[str, int]],
    previous_readings: dict,
) -> list[tuple[WeatherObservation, str]]:
    """Fetch latest observations for all stations in parallel, applying dedup.

    Returns a list of (WeatherObservation, product_id) tuples for new readings.
    Mutates *previous_readings* in-place to track emitted observation keys.
    """
    results: list[tuple[WeatherObservation, str]] = []
    lock = threading.Lock()

    def _process(item: tuple[str, int]) -> None:
        product_id, wmo_id = item
        try:
            obs_data = api.get_station_observations(product_id, wmo_id)
        except Exception as e:
            if _is_http_404(e):
                logger.debug("Observation product missing for %s/%d (404)", product_id, wmo_id)
            else:
                logger.warning("Failed to fetch observations for %s/%d: %s", product_id, wmo_id, e)
            return
        records = obs_data.get("observations", {}).get("data", [])
        if not records:
            return
        header = (obs_data.get("observations", {}).get("header") or [{}])[0]
        latest = records[0]
        obs = api.parse_observation(latest, default_state=header.get("state"))
        if not obs:
            return
        reading_key = f"{obs.station_wmo}:{obs.observation_time_utc}"
        with lock:
            if reading_key in previous_readings:
                return
            previous_readings[reading_key] = obs.observation_time_utc
            results.append((obs, product_id))

    with ThreadPoolExecutor(max_workers=api.fetch_workers) as pool:
        list(pool.map(_process, station_list))
    return results


def fetch_new_warnings(
    api: BOMAustraliaAPI,
    warning_feeds: list[str],
    previous_warnings: dict,
) -> list[WarningBulletin]:
    """Fetch current warning feeds and return new/updated bulletins.

    Mutates *previous_warnings* in-place to track emitted warning IDs.
    """
    new_bulletins: list[WarningBulletin] = []
    for feed_url in warning_feeds:
        try:
            feed_xml = api.get_warning_feed(feed_url)
            bulletins = api.parse_warning_feed(feed_url, feed_xml)
            for bulletin in bulletins:
                if previous_warnings.get(bulletin.warning_id) == bulletin.published_at:
                    continue
                previous_warnings[bulletin.warning_id] = bulletin.published_at
                new_bulletins.append(bulletin)
        except Exception as e:
            logger.warning("Failed to fetch warnings from %s: %s", feed_url, e)
    return new_bulletins
