"""DWD ICON-D2 forecast module — emits model reference and file metadata events."""

import re
from typing import Any, Dict, List, Optional

from dwd.modules.base import BaseModule
from dwd.util.http_client import DWDHttpClient

_ICON_D2_BASE_PATH = "weather/nwp/icon-d2/grib/"

_RUN_FORECAST_RE = re.compile(r"_(\d{10})_(\d{3})_")


def _parse_size_bytes(size_str: str) -> Optional[int]:
    value = size_str.strip()
    if not value or value == "-":
        return None
    try:
        suffix = value[-1].upper()
        if suffix in {"K", "M", "G"}:
            num = float(value[:-1])
            factor = {"K": 1024, "M": 1024 * 1024, "G": 1024 * 1024 * 1024}[suffix]
            return int(num * factor)
        return int(float(value))
    except ValueError:
        return None


def _extract_metadata(file_name: str) -> Dict[str, Optional[Any]]:
    run = None
    forecast_hour: Optional[int] = None
    m = _RUN_FORECAST_RE.search(file_name)
    if m:
        run = m.group(1)
        forecast_hour = int(m.group(2))

    parts = file_name.split("_")
    parameter = parts[2] if len(parts) > 2 and parts[2] else None
    level_type = parts[3] if len(parts) > 3 and parts[3] else None
    level = parts[4] if len(parts) > 4 and parts[4] else None

    return {
        "run": run,
        "forecast_hour": forecast_hour,
        "parameter": parameter,
        "level_type": level_type,
        "level": level,
    }


class IconD2ForecastModule(BaseModule):
    """Poll DWD ICON-D2 directories and emit forecast file metadata events."""

    def __init__(self, http_client: DWDHttpClient):
        self._http = http_client

    @property
    def name(self) -> str:
        return "icon_d2_forecast"

    @property
    def default_enabled(self) -> bool:
        return False

    @property
    def default_poll_interval(self) -> int:
        return 300

    def poll(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []
        file_watermarks: Dict[str, str] = state.setdefault("files", {})

        if not state.get("catalog_emitted"):
            events.append({
                "type": "forecast_model_catalog",
                "data": {
                    "file_url": f"{self._http.base_url}/{_ICON_D2_BASE_PATH}",
                    "model": "icon-d2",
                    "description": "DWD ICON-D2 NWP model forecast feed from Open Data directories.",
                },
            })
            state["catalog_emitted"] = True

        root_entries = self._http.list_directory(_ICON_D2_BASE_PATH)
        if not root_entries:
            return events

        paths_to_scan = [_ICON_D2_BASE_PATH]
        for entry in root_entries:
            if entry.name.endswith("/") and entry.name not in ("../", "/"):
                paths_to_scan.append(f"{_ICON_D2_BASE_PATH}{entry.name}")

        for rel_dir in paths_to_scan:
            file_entries = self._http.list_directory(rel_dir)
            for entry in file_entries:
                if entry.name.endswith("/"):
                    continue
                file_path = f"{rel_dir}{entry.name}"
                modified = entry.modified.isoformat()
                if file_watermarks.get(file_path) == modified:
                    continue
                file_watermarks[file_path] = modified
                meta = _extract_metadata(entry.name)
                events.append({
                    "type": "icon_d2_forecast_file",
                    "data": {
                        "file_url": f"{self._http.base_url}/{file_path}",
                        "model": "icon-d2",
                        "file_name": entry.name,
                        "run": meta["run"],
                        "forecast_hour": meta["forecast_hour"],
                        "parameter": meta["parameter"],
                        "level_type": meta["level_type"],
                        "level": meta["level"],
                        "modified": modified,
                        "size_bytes": _parse_size_bytes(entry.size_str),
                    },
                })

        return events
