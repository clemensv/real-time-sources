"""File-backed JSON state storage for dedupe and conditional-GET metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, MutableMapping, Optional


class JsonFileStateStore:
    """Load and save small JSON state documents used by pollers.

    Args:
        path: State file path. Parent directories are created on save. A missing
            or invalid file is treated as an empty state, matching existing
            feeder dedupe-state behavior in this repository.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> Dict[str, Any]:
        """Return the stored JSON object, or an empty dict when unavailable."""
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return {}
        return data if isinstance(data, dict) else {}

    def save(self, state: MutableMapping[str, Any]) -> None:
        """Persist a JSON-serializable state object to disk atomically enough for pollers."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(dict(state), handle, indent=2, sort_keys=True)

    def load_namespace(self, name: str) -> Dict[str, Any]:
        """Return one named sub-dictionary from the state document."""
        value = self.load().get(name, {})
        return value if isinstance(value, dict) else {}

    def save_namespace(self, name: str, value: MutableMapping[str, Any]) -> None:
        """Update one named sub-dictionary in the state document."""
        state = self.load()
        state[name] = dict(value)
        self.save(state)

    def conditional_headers(self) -> Dict[str, str]:
        """Return If-None-Match/If-Modified-Since headers from saved metadata."""
        headers: Dict[str, str] = {}
        metadata = self.load_namespace("http")
        etag = metadata.get("etag")
        last_modified = metadata.get("last_modified")
        if isinstance(etag, str) and etag:
            headers["If-None-Match"] = etag
        if isinstance(last_modified, str) and last_modified:
            headers["If-Modified-Since"] = last_modified
        return headers

    def save_http_metadata(self, *, etag: Optional[str], last_modified: Optional[str]) -> None:
        """Persist ETag and Last-Modified values returned by an upstream."""
        existing = self.load_namespace("http")
        if etag:
            existing["etag"] = etag
        if last_modified:
            existing["last_modified"] = last_modified
        self.save_namespace("http", existing)
