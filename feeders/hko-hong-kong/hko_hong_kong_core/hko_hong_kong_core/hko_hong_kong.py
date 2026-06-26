"""HKO Hong Kong Weather Observation Bridge — fetches current weather from the Hong Kong Observatory."""

from __future__ import annotations

import json
import logging
import os
import re
from datetime import datetime, timezone

import requests

from hko_hong_kong_producer_data import Station, WeatherObservation

logger = logging.getLogger(__name__)

# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-hko-hong-kong/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

HKO_API_URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"


def slugify(name: str) -> str:
    """Convert a place name to a URL-safe slug identifier."""
    s = name.lower()
    s = s.replace("'", "")
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


class HKOWeatherAPI:
    """Client for the HKO open data weather API."""

    def __init__(self, base_url: str = HKO_API_URL, polling_interval: int = 600):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT

    def get_current_weather(self) -> dict:
        """Fetch the rhrread (Regional Weather in Hong Kong) endpoint."""
        response = self.session.get(
            self.base_url, params={"dataType": "rhrread", "lang": "en"}, timeout=30
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _section_entries(data: dict, section: str) -> list[dict]:
        """Return the `data` list for a top-level section, tolerating HKO quirks.

        The HKO rhrread endpoint occasionally returns empty strings (e.g. ``""``)
        for a section instead of an object — most commonly for ``uvindex`` at
        night, or for ``warningMessage``/``tcmessage`` when nothing is in force.
        Defensively normalize any non-dict / missing section to an empty list.
        """
        section_val = data.get(section)
        if not isinstance(section_val, dict):
            return []
        entries = section_val.get("data", [])
        if not isinstance(entries, list):
            return []
        return [e for e in entries if isinstance(e, dict) and "place" in e]

    @staticmethod
    def extract_places(data: dict) -> dict[str, Station]:
        """Extract all unique places from the rhrread response as Station reference data."""
        places: dict[str, dict] = {}

        for section in ("temperature", "rainfall", "humidity", "uvindex"):
            for entry in HKOWeatherAPI._section_entries(data, section):
                name = entry["place"]
                pid = slugify(name)
                if pid not in places:
                    places[pid] = {"name": name, "types": set()}
                places[pid]["types"].add(section)

        stations: dict[str, Station] = {}
        for pid, info in places.items():
            stations[pid] = Station(
                place_id=pid,
                name=info["name"],
                data_types=",".join(sorted(info["types"])),
                district=None,
            )
        return stations

    @staticmethod
    def extract_observations(data: dict) -> list[WeatherObservation]:
        """Extract per-place observations from the rhrread response."""
        update_time_str = data.get("updateTime", "")
        try:
            update_time = datetime.fromisoformat(update_time_str.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            update_time = datetime.now(timezone.utc)

        temp_map: dict[str, float] = {}
        for entry in HKOWeatherAPI._section_entries(data, "temperature"):
            try:
                temp_map[slugify(entry["place"])] = float(entry["value"])
            except (KeyError, TypeError, ValueError):
                continue

        rain_map: dict[str, float] = {}
        for entry in HKOWeatherAPI._section_entries(data, "rainfall"):
            try:
                rain_map[slugify(entry["place"])] = float(entry["max"])
            except (KeyError, TypeError, ValueError):
                continue

        humidity_map: dict[str, int] = {}
        for entry in HKOWeatherAPI._section_entries(data, "humidity"):
            try:
                humidity_map[slugify(entry["place"])] = int(entry["value"])
            except (KeyError, TypeError, ValueError):
                continue

        uv_map: dict[str, tuple[float, str]] = {}
        for entry in HKOWeatherAPI._section_entries(data, "uvindex"):
            try:
                uv_map[slugify(entry["place"])] = (
                    float(entry.get("value", 0)),
                    entry.get("desc", ""),
                )
            except (TypeError, ValueError):
                continue

        all_pids: set[str] = set()
        name_map: dict[str, str] = {}
        for section in ("temperature", "rainfall", "humidity", "uvindex"):
            for entry in HKOWeatherAPI._section_entries(data, section):
                pid = slugify(entry["place"])
                all_pids.add(pid)
                name_map[pid] = entry["place"]

        observations = []
        for pid in sorted(all_pids):
            uv = uv_map.get(pid)
            obs = WeatherObservation(
                place_id=pid,
                place_name=name_map.get(pid, pid),
                observation_time=update_time,
                temperature=temp_map.get(pid),
                rainfall_max=rain_map.get(pid),
                humidity=humidity_map.get(pid),
                uv_index=uv[0] if uv else None,
                uv_description=uv[1] if uv else None,
                district=None,
            )
            observations.append(obs)
        return observations

def _load_state(state_file: str) -> dict:
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logging.warning("Could not load state from %s: %s", state_file, e)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    if not state_file:
        return
    try:
        if len(data) > 100000:
            keys = list(data.keys())
            data = {k: data[k] for k in keys[-50000:]}
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as e:
        logging.warning("Could not save state to %s: %s", state_file, e)
