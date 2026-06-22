"""Transport-agnostic acquisition layer for the DWD Pollenflug bridge."""

import json
import os
from typing import Dict, List, Optional

import requests

from dwd_pollenflug_producer_data import Region, PollenForecast

# German-to-English pollen name mapping
POLLEN_NAME_MAP = {
    "Hasel": "hazel",
    "Erle": "alder",
    "Birke": "birch",
    "Esche": "ash",
    "Graeser": "grasses",
    "Roggen": "rye",
    "Beifuss": "mugwort",
    "Ambrosia": "ragweed",
}

# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-dwd-pollenflug/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

FORECAST_API_URL = "https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json"
POLL_INTERVAL_SECONDS = 3600  # 1 hour


def get_region_id(item: dict) -> str:
    """Derive the unique region identifier for a forecast area."""
    partregion_id = item.get("partregion_id", -1)
    if partregion_id is not None and partregion_id > 0:
        return str(int(partregion_id))
    return str(int(item["region_id"]))


def get_region_display_name(item: dict) -> str:
    """Return the best display name for a forecast area."""
    partregion_name = item.get("partregion_name", "")
    if partregion_name:
        return partregion_name
    return item.get("region_name", "")


def parse_regions(data: dict) -> List[Region]:
    """Parse region reference data from the DWD API response."""
    regions = []
    for item in data.get("content", []):
        rid = get_region_id(item)
        partregion_id_raw = item.get("partregion_id", -1)
        partregion_name_raw = item.get("partregion_name", "")
        regions.append(Region(
            region_id=rid,
            region_name=item.get("region_name", ""),
            partregion_id=None if partregion_id_raw == -1 else int(partregion_id_raw),
            partregion_name=None if not partregion_name_raw else partregion_name_raw,
        ))
    return regions


def parse_forecasts(data: dict) -> List[PollenForecast]:
    """Parse pollen forecasts from the DWD API response, mapping German names to English."""
    forecasts = []
    last_update = data.get("last_update", "")
    next_update = data.get("next_update", "")
    sender = data.get("sender")

    for item in data.get("content", []):
        rid = get_region_id(item)
        display_name = get_region_display_name(item)
        pollen = item.get("Pollen", {})

        kwargs: Dict[str, Optional[str]] = {}
        for german_name, english_name in POLLEN_NAME_MAP.items():
            pollen_data = pollen.get(german_name, {})
            if not isinstance(pollen_data, dict):
                pollen_data = {}
            kwargs[f"{english_name}_today"] = pollen_data.get("today")
            kwargs[f"{english_name}_tomorrow"] = pollen_data.get("tomorrow")
            kwargs[f"{english_name}_dayafter_to"] = pollen_data.get("dayafter_to")

        forecasts.append(PollenForecast(
            region_id=rid,
            region_name=display_name,
            last_update=last_update,
            next_update=next_update,
            sender=sender,
            pollen_type=None,
            **kwargs,
        ))
    return forecasts


def fetch_data() -> Optional[dict]:
    """Fetch the DWD pollen forecast JSON."""
    try:
        response = requests.get(FORECAST_API_URL, headers={"User-Agent": USER_AGENT}, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        print(f"Error fetching DWD pollen forecast: {err}")
        return None


def load_state(state_file: str) -> dict:
    """Load persisted state from disk."""
    try:
        if os.path.exists(state_file):
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, OSError) as err:
        print(f"Warning: could not load state file: {err}")
    return {}


def save_state(state_file: str, state: dict) -> None:
    """Persist state to disk."""
    try:
        state_dir = os.path.dirname(state_file)
        if state_dir:
            os.makedirs(state_dir, exist_ok=True)
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f)
    except OSError as err:
        print(f"Warning: could not save state file: {err}")
