"""DWD radar products module — emits radar product catalog and file metadata events."""

import logging
from typing import Any, Dict, List, Optional

from dwd.modules.base import BaseModule
from dwd.util.http_client import DWDHttpClient

logger = logging.getLogger(__name__)

_RADAR_COMPOSITE_PATH = "weather/radar/composite/"


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


class RadarProductsModule(BaseModule):
    """Poll DWD radar product directories and emit file metadata events."""

    def __init__(self, http_client: DWDHttpClient):
        self._http = http_client

    @property
    def name(self) -> str:
        return "radar_products"

    @property
    def default_enabled(self) -> bool:
        return False

    @property
    def default_poll_interval(self) -> int:
        return 300

    def poll(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []
        file_watermarks: Dict[str, str] = state.setdefault("files", {})

        product_entries = self._http.list_directory(_RADAR_COMPOSITE_PATH)
        if not product_entries:
            return events

        product_dirs = [e.name for e in product_entries if e.name.endswith("/") and e.name not in ("../", "/")]
        if not product_dirs:
            product_dirs = [""]

        if not state.get("catalog_emitted"):
            for product_dir in product_dirs:
                product = product_dir.rstrip("/") if product_dir else "composite"
                rel_dir = f"{_RADAR_COMPOSITE_PATH}{product_dir}".rstrip("/")
                events.append({
                    "type": "radar_product_catalog",
                    "data": {
                        "file_url": f"{self._http.base_url}/{rel_dir}/",
                        "product": product,
                        "description": f"DWD radar product directory {product}",
                    },
                })
            state["catalog_emitted"] = True

        for product_dir in product_dirs:
            product = product_dir.rstrip("/") if product_dir else "composite"
            rel_dir = f"{_RADAR_COMPOSITE_PATH}{product_dir}"
            file_entries = self._http.list_directory(rel_dir)
            for entry in file_entries:
                if entry.name.endswith("/"):
                    continue
                file_path = f"{rel_dir}{entry.name}"
                modified = entry.modified.isoformat()
                if file_watermarks.get(file_path) == modified:
                    continue
                file_watermarks[file_path] = modified
                events.append({
                    "type": "radar_file_product",
                    "data": {
                        "file_url": f"{self._http.base_url}/{file_path}",
                        "product": product,
                        "file_name": entry.name,
                        "modified": modified,
                        "size_bytes": _parse_size_bytes(entry.size_str),
                    },
                })

        return events
