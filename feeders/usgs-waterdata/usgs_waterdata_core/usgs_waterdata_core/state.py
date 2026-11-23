"""Atomic snapshots and content-based observation checkpoints."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any

from .client import utc_datetime


def write_json(path: Path, data: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as stream:
            temporary = stream.name
            json.dump(data, stream, indent=2, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and os.path.exists(temporary):
            os.unlink(temporary)


def observation_key(properties: Mapping[str, Any]) -> str:
    series = properties.get("time_series_id")
    instant = properties.get("time")
    if not isinstance(series, str) or not series or not isinstance(instant, str):
        raise ValueError("USGS observation lacks time_series_id/time")
    return f"{series}/{utc_datetime(instant).isoformat()}"


def fingerprint(properties: Mapping[str, Any]) -> str:
    # Database refreshes change last_modified/feature IDs without changing science data.
    content = {key: value for key, value in properties.items() if key not in {"last_modified", "id"}}
    if "time" in content:
        content["time"] = utc_datetime(content["time"]).isoformat()
    encoded = json.dumps(content, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


class DeliveryState:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path
        self.data: dict[str, Any] = {"version": 1, "observations": {}}
        if path is not None and path.exists():
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if (
                not isinstance(loaded, dict)
                or loaded.get("version") != 1
                or not isinstance(loaded.get("observations"), dict)
                or not all(
                    isinstance(key, str)
                    and isinstance(value, str)
                    and len(value) == 64
                    for key, value in loaded.get("observations", {}).items()
                )
            ):
                raise ValueError("Unsupported or corrupt USGS delivery state")
            self.data = loaded

    def deliver(
        self,
        features: Iterable[dict[str, Any]],
        send: Callable[[dict[str, Any]], None],
        flush: Callable[[], int | None],
        *,
        retain_since: datetime | None = None,
    ) -> int:
        pending = deepcopy(self.data)
        observations = pending["observations"]
        count = 0
        for feature in features:
            properties = feature["properties"]
            key = observation_key(properties)
            digest = fingerprint(properties)
            if observations.get(key) == digest:
                continue
            send(feature)
            observations[key] = digest
            count += 1
        remaining = flush()
        if remaining is not None and remaining != 0:
            raise RuntimeError(f"USGS delivery left {remaining} messages unacknowledged")
        if retain_since is not None:
            if retain_since.tzinfo is None:
                raise ValueError("State retention requires an offset-aware datetime")
            observations = {
                key: value
                for key, value in observations.items()
                if utc_datetime(key.split("/", 1)[1]) >= retain_since
            }
            pending["observations"] = observations
        pending["committed_at"] = datetime.now(timezone.utc).isoformat()
        if self.path is not None:
            write_json(self.path, pending)
        self.data = pending
        return count
