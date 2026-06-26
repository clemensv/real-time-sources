"""Transport-neutral acquisition for Paris bicycle counters."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple

import requests

from paris_bicycle_counters_producer_data import BicycleCount, Counter

COUNTER_DATA_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-donnees-compteurs/records"
COUNTER_LOCATIONS_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-compteurs/records"
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-paris-bicycle-counters/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)


def ce_datetime(value: datetime) -> str:
    """Return a stable UTC-ish timestamp string for CloudEvents ids."""
    return value.isoformat().replace("+00:00", "Z")


def is_topic_safe_segment(value: str) -> bool:
    return bool(value) and not any(ch in value for ch in ("/", "+", "#", "\x00"))


def counter_info_ce_id(counter_id: str, fields: Dict[str, object]) -> str:
    encoded = json.dumps(fields, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:12]
    return f"{counter_id}/info/{digest}"


class ParisBicycleCounterPoller:
    """Poll the Paris Open Data bicycle counter APIs without transport concerns."""

    POLL_INTERVAL_SECONDS = 3600

    def __init__(self, last_polled_file: str):
        self.last_polled_file = last_polled_file

    def load_state(self) -> Dict:
        """Load the last polled state from the state file."""
        if os.path.exists(self.last_polled_file):
            try:
                with open(self.last_polled_file, "r", encoding="utf-8") as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def save_state(self, state: Dict):
        """Save the last polled state to the state file."""
        directory = os.path.dirname(self.last_polled_file) or "."
        os.makedirs(directory, exist_ok=True)
        with open(self.last_polled_file, "w", encoding="utf-8") as file:
            json.dump(state, file)

    @staticmethod
    def fetch_counter_locations() -> List[Counter]:
        """Fetch counter location reference data from the Paris Open Data API."""
        counters: List[Counter] = []
        offset = 0
        limit = 100
        while True:
            params = {"limit": limit, "offset": offset}
            response = requests.get(COUNTER_LOCATIONS_URL, params=params, headers={"User-Agent": USER_AGENT}, timeout=30)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            if not results:
                break
            for record in results:
                coords = record.get("coordinates") or {}
                counter_id = record.get("id_compteur", "")
                if not is_topic_safe_segment(counter_id):
                    print(f"Skipping counter with MQTT-unsafe id_compteur={counter_id!r}", file=sys.stderr)
                    continue
                fields = {
                    "counter_name": record.get("nom_compteur", ""),
                    "channel_name": record.get("channel_name"),
                    "installation_date": record.get("installation_date"),
                    "longitude": coords.get("lon"),
                    "latitude": coords.get("lat"),
                }
                counters.append(
                    Counter(
                        ce_id=counter_info_ce_id(counter_id, fields),
                        counter_id=counter_id,
                        **fields,
                    )
                )
            if len(results) < limit:
                break
            offset += limit
        return counters

    @staticmethod
    def fetch_bicycle_counts(since: Optional[datetime] = None) -> List[BicycleCount]:
        """Fetch bicycle count data from the Paris Open Data API."""
        counts: List[BicycleCount] = []
        offset = 0
        limit = 100
        max_offset = 10000 - limit
        while True:
            params: Dict[str, object] = {"limit": limit, "offset": offset}
            if since:
                params["where"] = f"date >= '{since.strftime('%Y-%m-%dT%H:%M:%S')}'"
            try:
                response = requests.get(COUNTER_DATA_URL, params=params, headers={"User-Agent": USER_AGENT}, timeout=30)  # type: ignore[arg-type]
                response.raise_for_status()
            except requests.HTTPError as error:
                print(f"Stopping pagination at offset {offset}: {error}", file=sys.stderr)
                break
            data = response.json()
            results = data.get("results", [])
            if not results:
                break
            for record in results:
                coords = record.get("coordinates") or {}
                date_str = record.get("date")
                if not date_str:
                    continue
                try:
                    date_val = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                except (ValueError, TypeError):
                    continue
                counter_id = record.get("id_compteur", "")
                if not is_topic_safe_segment(counter_id):
                    print(f"Skipping count with MQTT-unsafe id_compteur={counter_id!r}", file=sys.stderr)
                    continue
                counts.append(
                    BicycleCount(
                        ce_id=f"{counter_id}/{ce_datetime(date_val)}/count",
                        counter_id=counter_id,
                        counter_name=record.get("nom_compteur", ""),
                        count=record.get("sum_counts"),
                        date=date_val,
                        longitude=coords.get("lon"),
                        latitude=coords.get("lat"),
                    )
                )
            if len(results) < limit:
                break
            offset += limit
            if offset > max_offset:
                break
        return counts

    @staticmethod
    def dedup_counts(counts: List[BicycleCount], seen_keys: Set[str]) -> Tuple[List[BicycleCount], Set[str]]:
        """Deduplicate bicycle counts using counter_id + date as the key."""
        new_counts: List[BicycleCount] = []
        new_keys: Set[str] = set(seen_keys)
        for bicycle_count in counts:
            date_str = bicycle_count.date.isoformat() if isinstance(bicycle_count.date, datetime) else str(bicycle_count.date)
            key = f"{bicycle_count.counter_id}|{date_str}"
            if key not in new_keys:
                new_keys.add(key)
                new_counts.append(bicycle_count)
        return new_counts, new_keys
