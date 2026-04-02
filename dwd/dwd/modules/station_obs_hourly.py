"""Hourly station observation module — polls recent/ directories."""

import logging
from typing import Any, Dict, List, Optional, Set

from dwd.modules.base import BaseModule
from dwd.parsers.csv_parser import parse_dwd_csv
from dwd.util.http_client import DWDHttpClient

logger = logging.getLogger(__name__)

_BASE_PATH = "climate_environment/CDC/observations_germany/climate/hourly"

# Hourly parameter categories and their DWD column mappings
HOURLY_CATEGORIES = {
    "air_temperature": {"TT_TU": "value", "_unit": "°C", "_param": "air_temperature"},
    "precipitation": {"R1": "value", "_unit": "mm", "_param": "precipitation"},
    "wind": {"F": "value", "_unit": "m/s", "_param": "wind_speed"},
    "pressure": {"P0": "value", "_unit": "hPa", "_param": "air_pressure"},
    "cloud_type": {"V_N": "value", "_unit": "okta", "_param": "cloud_cover"},
    "solar": {"FG_LBERG": "value", "_unit": "J/cm²", "_param": "global_radiation"},
    "sun": {"SD_SO": "value", "_unit": "h", "_param": "sunshine_duration"},
    "visibility": {"V_VV": "value", "_unit": "m", "_param": "visibility"},
}


class StationObsHourlyModule(BaseModule):
    """Polls DWD hourly recent/ directories for station observations."""

    def __init__(self, http_client: DWDHttpClient,
                 categories: Optional[List[str]] = None,
                 station_filter: Optional[Set[str]] = None):
        self._http = http_client
        self._categories = categories or ["air_temperature", "precipitation", "wind", "pressure"]
        self._station_filter = station_filter

    @property
    def name(self) -> str:
        return "station_obs_hourly"

    @property
    def default_enabled(self) -> bool:
        return False

    @property
    def default_poll_interval(self) -> int:
        return 3600  # 1 hour

    def poll(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Poll configured hourly categories. Returns HourlyObservation events."""
        events: List[Dict[str, Any]] = []

        for category in self._categories:
            cat_config = HOURLY_CATEGORIES.get(category)
            if not cat_config:
                continue

            cat_state = state.setdefault(category, {})
            recent_path = f"{_BASE_PATH}/{category}/recent/"
            file_timestamps: Dict[str, str] = cat_state.get("file_timestamps", {})

            # List the recent/ directory
            dir_entries = self._http.list_directory(recent_path)
            zip_entries = [e for e in dir_entries if e.name.endswith(".zip") and "Beschreibung" not in e.name]
            if not zip_entries:
                continue

            new_count = 0
            for entry in zip_entries:
                ts_str = entry.modified.isoformat()
                if file_timestamps.get(entry.name) == ts_str:
                    continue  # File hasn't changed

                csv_text = self._http.download_zip_csv(recent_path + entry.name)
                if not csv_text:
                    continue

                rows = parse_dwd_csv(csv_text)
                if not rows:
                    file_timestamps[entry.name] = ts_str
                    continue

                # Track per-station last timestamp
                station_ts: Dict[str, str] = cat_state.get("station_ts", {})

                for row in rows:
                    sid = str(row.get("STATIONS_ID", ""))
                    ts = row.get("MESS_DATUM", "")
                    if not sid or not ts:
                        continue
                    if self._station_filter and sid not in self._station_filter:
                        continue
                    if ts <= station_ts.get(sid, ""):
                        continue

                    # Find the value column
                    value = None
                    for dwd_col, semantic in cat_config.items():
                        if dwd_col.startswith("_"):
                            continue
                        if dwd_col in row and row[dwd_col] is not None:
                            value = row[dwd_col]
                            break

                    if value is None:
                        continue

                    station_ts[sid] = ts
                    events.append({
                        "type": "hourly_observation",
                        "data": {
                            "station_id": sid,
                            "timestamp": ts,
                            "quality_level": row.get("QN_9", row.get("QN_8", row.get("QN_3", 0))) or 0,
                            "parameter": cat_config["_param"],
                            "value": value,
                            "unit": cat_config["_unit"],
                        },
                    })
                    new_count += 1

                file_timestamps[entry.name] = ts_str
                cat_state["station_ts"] = station_ts

            cat_state["file_timestamps"] = file_timestamps
            if new_count:
                logger.info("hourly/%s: emitted %d new observations", category, new_count)

        return events
