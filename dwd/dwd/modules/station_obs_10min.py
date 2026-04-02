"""10-minute station observation module — the core real-time dataset."""

import logging
from typing import Any, Dict, List, Optional, Set

from dwd.modules.base import BaseModule
from dwd.parsers.csv_parser import map_row, parse_dwd_csv
from dwd.util.http_client import DWDHttpClient, DirEntry

logger = logging.getLogger(__name__)

# Base path for 10-minute now/ data
_BASE_PATH = "climate_environment/CDC/observations_germany/climate/10_minutes"

# Category → subdirectory name
CATEGORIES = {
    "air_temperature": "air_temperature",
    "precipitation": "precipitation",
    "wind": "wind",
    "solar": "solar",
    "extreme_wind": "extreme_wind",
    "extreme_temperature": "extreme_temperature",
}

# Map categories to event types
CATEGORY_EVENT_TYPES = {
    "air_temperature": "air_temperature_10min",
    "precipitation": "precipitation_10min",
    "wind": "wind_10min",
    "solar": "solar_10min",
    "extreme_wind": "wind_10min",
    "extreme_temperature": "air_temperature_10min",
}


class StationObs10MinModule(BaseModule):
    """Polls DWD 10-minute now/ directories for station observations."""

    def __init__(self, http_client: DWDHttpClient,
                 categories: Optional[List[str]] = None,
                 station_filter: Optional[Set[str]] = None):
        self._http = http_client
        self._categories = categories or ["air_temperature", "precipitation", "wind", "solar"]
        self._station_filter = station_filter

    @property
    def name(self) -> str:
        return "station_obs_10min"

    @property
    def default_enabled(self) -> bool:
        return True

    @property
    def default_poll_interval(self) -> int:
        return 600  # 10 minutes

    def poll(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Poll all configured categories. Returns new observation events."""
        events: List[Dict[str, Any]] = []

        for category in self._categories:
            subdir = CATEGORIES.get(category)
            if not subdir:
                continue

            cat_state = state.setdefault(category, {})
            now_path = f"{_BASE_PATH}/{subdir}/now/"

            # Check if directory has new files via listing
            dir_entries = self._http.list_directory(now_path)
            if not dir_entries:
                continue

            # Filter to ZIP files only
            zip_entries = [e for e in dir_entries if e.name.endswith(".zip")]
            if not zip_entries:
                continue

            # Check if anything changed since last poll by comparing the newest timestamp
            newest_ts = max(e.modified for e in zip_entries).isoformat()
            if cat_state.get("dir_timestamp") == newest_ts:
                logger.debug("%s: no changes since last poll", category)
                continue

            logger.info("%s: directory updated (%d files), downloading...", category, len(zip_entries))
            station_timestamps: Dict[str, str] = cat_state.get("stations", {})
            new_count = 0

            for entry in zip_entries:
                csv_text = self._http.download_zip_csv(now_path + entry.name)
                if not csv_text:
                    continue

                rows = parse_dwd_csv(csv_text)
                if not rows:
                    continue

                # Each file has rows for one station over the current day
                for row in rows:
                    mapped = map_row(row, category)
                    sid = mapped.get("station_id", "")
                    ts = mapped.get("timestamp", "")

                    if not sid or not ts:
                        continue
                    if self._station_filter and sid not in self._station_filter:
                        continue

                    # Dedup: only emit if timestamp is newer than last seen
                    prev_ts = station_timestamps.get(sid, "")
                    if ts <= prev_ts:
                        continue

                    station_timestamps[sid] = ts
                    event_type = CATEGORY_EVENT_TYPES.get(category, category)
                    events.append({"type": event_type, "data": mapped})
                    new_count += 1

            cat_state["stations"] = station_timestamps
            cat_state["dir_timestamp"] = newest_ts
            logger.info("%s: emitted %d new observations", category, new_count)

        return events
