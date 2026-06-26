"""Transport-neutral acquisition and state handling for Seattle Fire 911."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import List, Optional
from zoneinfo import ZoneInfo

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from seattle_911_producer_data import Incident

LOGGER = logging.getLogger(__name__)

DATASET_URL = "https://data.seattle.gov/resource/kzjm-xkqj.json"
DATASET_PAGE_URL = "https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj"
DEFAULT_POLL_INTERVAL_SECONDS = 300
DEFAULT_LOOKBACK_HOURS = 24
DEFAULT_OVERLAP_MINUTES = 10
MAX_SEEN_IDS = 50000
DEFAULT_CONNECT_TIMEOUT_SECONDS = 10
DEFAULT_READ_TIMEOUT_SECONDS = 120
DEFAULT_KAFKA_FLUSH_TIMEOUT_SECONDS = 30
DEFAULT_HTTP_RETRY_TOTAL = 3
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-seattle-911/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com")
    + ")"
)


def _build_retrying_session() -> requests.Session:
    """Create an HTTP session with bounded retries for transient upstream failures."""
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    retry = Retry(
        total=DEFAULT_HTTP_RETRY_TOTAL,
        connect=DEFAULT_HTTP_RETRY_TOTAL,
        read=DEFAULT_HTTP_RETRY_TOTAL,
        status=DEFAULT_HTTP_RETRY_TOTAL,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _load_state(state_file: str) -> dict:
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as handle:
                return json.load(handle)
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    if not state_file:
        return
    state_dir = os.path.dirname(state_file)
    if state_dir:
        os.makedirs(state_dir, exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def _incident_type_slug(value: str) -> str:
    """Normalize an incident type into a deterministic transport segment."""
    raw = (value or "unknown").lower().strip()
    out: List[str] = []
    previous_dash = False
    for ch in raw:
        if ch.isalnum():
            out.append(ch)
            previous_dash = False
        elif not previous_dash:
            out.append("-")
            previous_dash = True
    return "".join(out).strip("-") or "unknown"


def _incident_datetime_utc(value: str) -> datetime:
    """Convert the upstream Seattle local timestamp into UTC."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=ZoneInfo("America/Los_Angeles"))
    return parsed.astimezone(timezone.utc)


def parse_incident(record: dict) -> Incident:
    """Map a Socrata row into the generated Incident data class."""
    incident_type = record.get("type", "")
    incident_datetime = record.get("datetime", "")
    return Incident(
        incident_number=str(record.get("incident_number", "")),
        incident_type=incident_type,
        incident_type_slug=_incident_type_slug(incident_type),
        incident_datetime=incident_datetime,
        incident_datetime_utc=_incident_datetime_utc(incident_datetime),
        address=record.get("address"),
        latitude=float(record["latitude"]) if record.get("latitude") not in (None, "") else None,
        longitude=float(record["longitude"]) if record.get("longitude") not in (None, "") else None,
    )


class SeattleFire911Bridge:
    """Poll the Seattle Fire 911 dataset and manage dedupe state."""

    def __init__(self, state_file: str = ""):
        self.state_file = state_file
        self.session = _build_retrying_session()
        state = _load_state(state_file)
        sent_ids = [str(value) for value in state.get("sent_incident_numbers", [])]
        self.sent_incident_numbers = set(sent_ids[-MAX_SEEN_IDS:])
        self.sent_incident_order = sent_ids[-MAX_SEEN_IDS:]
        self.last_seen_datetime = state.get("last_seen_datetime")

    def save_state(self) -> None:
        _save_state(
            self.state_file,
            {
                "last_seen_datetime": self.last_seen_datetime,
                "sent_incident_numbers": self.sent_incident_order[-MAX_SEEN_IDS:],
            },
        )

    def fetch_incidents(self, since: Optional[datetime] = None) -> List[Incident]:
        """Fetch recent incident rows from the SODA endpoint."""
        incidents: List[Incident] = []
        offset = 0
        limit = 1000
        while True:
            params = {
                "$select": "address,type,datetime,latitude,longitude,incident_number",
                "$order": "datetime ASC",
                "$limit": limit,
                "$offset": offset,
            }
            if since is not None:
                params["$where"] = f"datetime >= '{since.strftime('%Y-%m-%dT%H:%M:%S')}'"
            response = self.session.get(
                DATASET_URL,
                params=params,  # type: ignore[arg-type]
                timeout=(DEFAULT_CONNECT_TIMEOUT_SECONDS, DEFAULT_READ_TIMEOUT_SECONDS),
            )
            response.raise_for_status()
            rows = response.json()
            if not rows:
                break
            incidents.extend(parse_incident(row) for row in rows if row.get("incident_number"))
            if len(rows) < limit:
                break
            offset += limit
        return incidents

    def _remember_incident(self, incident_number: str) -> None:
        if incident_number in self.sent_incident_numbers:
            return
        self.sent_incident_numbers.add(incident_number)
        self.sent_incident_order.append(incident_number)
        if len(self.sent_incident_order) > MAX_SEEN_IDS:
            removed = self.sent_incident_order.pop(0)
            self.sent_incident_numbers.discard(removed)

    def _remember_incidents(self, incident_numbers: List[str]) -> None:
        for incident_number in incident_numbers:
            self._remember_incident(incident_number)


__all__ = [
    "DATASET_PAGE_URL",
    "DATASET_URL",
    "DEFAULT_CONNECT_TIMEOUT_SECONDS",
    "DEFAULT_HTTP_RETRY_TOTAL",
    "DEFAULT_KAFKA_FLUSH_TIMEOUT_SECONDS",
    "DEFAULT_LOOKBACK_HOURS",
    "DEFAULT_OVERLAP_MINUTES",
    "DEFAULT_POLL_INTERVAL_SECONDS",
    "DEFAULT_READ_TIMEOUT_SECONDS",
    "LOGGER",
    "MAX_SEEN_IDS",
    "SeattleFire911Bridge",
    "USER_AGENT",
    "_build_retrying_session",
    "_incident_datetime_utc",
    "_incident_type_slug",
    "_load_state",
    "_save_state",
    "parse_incident",
]
