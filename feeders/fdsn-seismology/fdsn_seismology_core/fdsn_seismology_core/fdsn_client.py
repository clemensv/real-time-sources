from __future__ import annotations

import csv
import io
import json
import logging
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Iterable
from urllib.parse import urlencode

import requests

logger = logging.getLogger(__name__)

USER_AGENT = os.getenv("USER_AGENT") or (
    "real-time-sources-fdsn-seismology/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources)"
)

DEFAULT_LIMIT = 500
DEFAULT_TIMEOUT = 30
DEFAULT_OVERLAP_SECONDS = 5
DEFAULT_BOOTSTRAP_LOOKBACK_SECONDS = 86400
TEXT_COLUMNS = [
    "EventID",
    "Time",
    "Latitude",
    "Longitude",
    "Depth/km",
    "Author",
    "Catalog",
    "Contributor",
    "ContributorID",
    "MagType",
    "Magnitude",
    "MagAuthor",
    "EventLocationName",
    "EventType",
]


@dataclass(slots=True)
class EarthquakeRecord:
    event_id: str
    time: str
    latitude: float
    longitude: float
    depth_km: float | None
    author: str | None
    catalog: str | None
    contributor: str
    contributor_id: str | None
    magnitude_type: str | None
    magnitude: float | None
    magnitude_author: str | None
    event_location_name: str | None
    event_type: str | None
    node_url: str

    @property
    def dedupe_key(self) -> str:
        return f"{self.contributor}/{self.event_id}"


@dataclass(slots=True)
class BridgeState:
    last_poll_times: dict[str, str] = field(default_factory=dict)
    seen_event_times: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, dict[str, str]]:
        return {
            "last_poll_times": dict(self.last_poll_times),
            "seen_event_times": dict(self.seen_event_times),
        }



def parse_optional_str(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    if not text or text == "--":
        return None
    return text



def parse_optional_float(value: str | None) -> float | None:
    text = parse_optional_str(value)
    if text is None:
        return None
    return float(text)



def parse_datetime(value: str) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)



def format_datetime(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")



def build_query_url(
    base_url: str,
    *,
    starttime: str,
    endtime: str | None = None,
    min_magnitude: float | None = None,
    limit: int = DEFAULT_LIMIT,
    orderby: str = "time",
    bounds: dict[str, float] | None = None,
) -> str:
    params: dict[str, str | int | float] = {
        "format": "text",
        "orderby": orderby,
        "starttime": starttime,
        "limit": limit,
    }
    if endtime:
        params["endtime"] = endtime
    if min_magnitude is not None and min_magnitude > 0:
        params["minmagnitude"] = min_magnitude
    if bounds:
        for key in ("minlatitude", "maxlatitude", "minlongitude", "maxlongitude"):
            if key in bounds and bounds[key] is not None:
                params[key] = bounds[key]
    return f"{base_url.rstrip('/')}/query?{urlencode(params)}"



def parse_fdsn_text(text: str, node_id: str, node_url: str) -> list[EarthquakeRecord]:
    rows = [line for line in text.splitlines() if line.strip()]
    if not rows:
        return []

    header = TEXT_COLUMNS
    body_rows = rows
    if rows[0].startswith("#"):
        discovered = rows[0].lstrip("#").split("|")
        header = discovered + TEXT_COLUMNS[len(discovered):]
        body_rows = rows[1:]

    records: list[EarthquakeRecord] = []
    reader = csv.reader(io.StringIO("\n".join(body_rows)), delimiter="|")
    for row in reader:
        if not row or row[0].startswith("#"):
            continue
        if len(row) < len(header):
            row = row + [""] * (len(header) - len(row))
        values = {header[index]: (row[index].strip() if index < len(row) else "") for index in range(len(header))}
        try:
            event_id = parse_optional_str(values.get("EventID"))
            event_time = parse_optional_str(values.get("Time"))
            latitude = parse_optional_float(values.get("Latitude"))
            longitude = parse_optional_float(values.get("Longitude"))
            if not event_id or event_time is None or latitude is None or longitude is None:
                logger.debug("Skipping incomplete row from %s: %s", node_id, row)
                continue
            normalized_time = format_datetime(parse_datetime(event_time))
            contributor = parse_optional_str(values.get("Contributor")) or node_id.upper()
            records.append(
                EarthquakeRecord(
                    event_id=event_id,
                    time=normalized_time,
                    latitude=latitude,
                    longitude=longitude,
                    depth_km=parse_optional_float(values.get("Depth/km")),
                    author=parse_optional_str(values.get("Author")),
                    catalog=parse_optional_str(values.get("Catalog")),
                    contributor=contributor,
                    contributor_id=parse_optional_str(values.get("ContributorID")),
                    magnitude_type=parse_optional_str(values.get("MagType")),
                    magnitude=parse_optional_float(values.get("Magnitude")),
                    magnitude_author=parse_optional_str(values.get("MagAuthor")),
                    event_location_name=parse_optional_str(values.get("EventLocationName")),
                    event_type=parse_optional_str(values.get("EventType")),
                    node_url=node_url,
                )
            )
        except ValueError as exc:
            logger.warning("Skipping unparsable row from %s: %s (%s)", node_id, row, exc)
    return records



def _record_score(record: EarthquakeRecord) -> int:
    return sum(1 for value in asdict(record).values() if value not in (None, ""))



def deduplicate_events(events: Iterable[EarthquakeRecord]) -> list[EarthquakeRecord]:
    deduped: dict[str, EarthquakeRecord] = {}
    for event in events:
        existing = deduped.get(event.dedupe_key)
        if existing is None or _record_score(event) > _record_score(existing):
            deduped[event.dedupe_key] = event
    return sorted(deduped.values(), key=lambda item: (item.time, item.contributor, item.event_id))



def load_state(state_file: str | None) -> BridgeState:
    if not state_file or not os.path.exists(state_file):
        return BridgeState()
    with open(state_file, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return BridgeState(
        last_poll_times=dict(payload.get("last_poll_times") or {}),
        seen_event_times=dict(payload.get("seen_event_times") or {}),
    )



def save_state(state_file: str | None, state: BridgeState) -> None:
    if not state_file:
        return
    os.makedirs(os.path.dirname(state_file) or ".", exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as handle:
        json.dump(state.to_dict(), handle, indent=2, sort_keys=True)



def initial_start_time(
    poll_interval_seconds: int,
    *,
    now: datetime | None = None,
) -> str:
    baseline = now or datetime.now(timezone.utc)
    lookback = max(DEFAULT_BOOTSTRAP_LOOKBACK_SECONDS, poll_interval_seconds)
    return format_datetime(baseline - timedelta(seconds=lookback))



def ensure_state_for_nodes(
    state: BridgeState,
    node_ids: Iterable[str],
    poll_interval_seconds: int,
    *,
    now: datetime | None = None,
) -> None:
    for node_id in node_ids:
        state.last_poll_times.setdefault(node_id, initial_start_time(poll_interval_seconds, now=now))



def fetch_events_for_node(
    session: requests.Session,
    node_id: str,
    node: dict[str, str | None],
    *,
    starttime: str,
    endtime: str | None = None,
    min_magnitude: float | None = None,
    limit: int = DEFAULT_LIMIT,
    bounds: dict[str, float] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> list[EarthquakeRecord]:
    url = build_query_url(
        str(node["base_url"]),
        starttime=starttime,
        endtime=endtime,
        min_magnitude=min_magnitude,
        limit=limit,
        bounds=bounds,
    )
    logger.debug("Polling %s via %s", node_id, url)
    response = session.get(url, timeout=timeout, headers={"User-Agent": USER_AGENT})
    if response.status_code in (204, 404):
        return []
    response.raise_for_status()
    return parse_fdsn_text(response.text, node_id=node_id, node_url=str(node["base_url"]))



def should_publish_event(event: EarthquakeRecord, state: BridgeState) -> bool:
    return state.seen_event_times.get(event.dedupe_key) != event.time



def prune_seen_events(state: BridgeState, *, older_than_days: int = 14) -> None:
    cutoff = datetime.now(timezone.utc) - timedelta(days=older_than_days)
    state.seen_event_times = {
        key: value
        for key, value in state.seen_event_times.items()
        if parse_datetime(value) >= cutoff
    }



def poll_nodes(
    session: requests.Session,
    active_nodes: dict[str, dict[str, str | None]],
    state: BridgeState,
    *,
    poll_interval_seconds: int,
    min_magnitude: float | None = None,
    limit: int = DEFAULT_LIMIT,
    bounds: dict[str, float] | None = None,
    overlap_seconds: int = DEFAULT_OVERLAP_SECONDS,
) -> list[EarthquakeRecord]:
    cycle_start = datetime.now(timezone.utc)
    ensure_state_for_nodes(state, active_nodes.keys(), poll_interval_seconds, now=cycle_start)
    collected: list[EarthquakeRecord] = []
    for node_id, node in active_nodes.items():
        starttime = state.last_poll_times[node_id]
        try:
            collected.extend(
                fetch_events_for_node(
                    session,
                    node_id,
                    node,
                    starttime=starttime,
                    min_magnitude=min_magnitude,
                    limit=limit,
                    bounds=bounds,
                )
            )
        except requests.RequestException as exc:
            logger.warning("FDSN node %s request failed: %s", node_id, exc)
        next_start = cycle_start - timedelta(seconds=overlap_seconds)
        state.last_poll_times[node_id] = format_datetime(next_start)
    return deduplicate_events(collected)
