"""Transport-neutral iRail Belgian railway acquisition and parsing logic."""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from irail_producer_data.be.irail.station import Station
from irail_producer_data.be.irail.arrival import Arrival
from irail_producer_data.be.irail.arrivalboard import ArrivalBoard
from irail_producer_data.be.irail.departure import Departure
from irail_producer_data.be.irail.stationboard import StationBoard

API_BASE = "https://api.irail.be"
FEED_URL = "https://api.irail.be"

# iRail rate limits: 3 requests/sec with 5 burst
REQUEST_DELAY = 0.35  # slightly over 1/3 sec to stay within limits
DEFAULT_HTTP_RETRY_TOTAL = 3

# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-irail/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)


def create_retrying_session(user_agent: str = USER_AGENT) -> requests.Session:
    """Create an HTTP session with bounded retries for transient upstream failures."""
    session = requests.Session()
    session.headers.update({
        "Accept": "application/json",
        "User-Agent": user_agent,
    })
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


class IRailAPI:
    """Client for the iRail REST API."""

    def __init__(self, user_agent: str = USER_AGENT):
        self.session = create_retrying_session(user_agent)

    def fetch_stations(self) -> List[Dict[str, Any]]:
        """Fetch all Belgian railway stations."""
        resp = self.session.get(f"{API_BASE}/stations/", params={"format": "json", "lang": "en"}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("station", [])

    def fetch_liveboard(self, station_id: str, arrdep: str = "departure") -> Optional[Dict[str, Any]]:
        """Fetch the current departure or arrival board for a station by NMBS id."""
        resp = self.session.get(
            f"{API_BASE}/liveboard/",
            params={
                "id": f"BE.NMBS.{station_id}",
                "format": "json",
                "lang": "en",
                "alerts": "false",
                "arrdep": arrdep,
            },
            timeout=30,
        )
        if resp.status_code == 404:
            return None
        if resp.status_code == 429:
            logging.warning("Rate limited, backing off")
            time.sleep(5)
            return None
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def parse_station(raw: Dict[str, Any]) -> Station:
        """Convert a raw station dict from the iRail stations API to a Station data class."""
        station_id = IRailAPI._parse_station_id(raw.get("id", ""))
        return Station(
            station_id=station_id,
            name=raw.get("name", ""),
            standard_name=raw.get("standardname", ""),
            longitude=float(raw.get("locationX", 0.0)),
            latitude=float(raw.get("locationY", 0.0)),
            uri=raw.get("@id", ""),
        )

    @staticmethod
    def _parse_station_id(raw_id: str) -> str:
        """Normalize an iRail station identifier to the nine-digit NMBS id."""
        return raw_id.replace("BE.NMBS.", "") if raw_id.startswith("BE.NMBS.") else raw_id

    @staticmethod
    def _parse_scheduled_time(raw_unix: str) -> str:
        """Convert an iRail Unix timestamp string to an ISO 8601 UTC datetime."""
        return datetime.fromtimestamp(int(raw_unix), tz=timezone.utc).isoformat()

    @staticmethod
    def _parse_vehicle_details(vehicle_info: Dict[str, Any]) -> Tuple[str, str]:
        """Extract vehicle type and number from the liveboard payload."""
        vehicle_type = vehicle_info.get("type", "")
        vehicle_number = vehicle_info.get("number", "")
        if vehicle_type or vehicle_number:
            return vehicle_type, vehicle_number

        shortname = vehicle_info.get("shortname", "")
        parts = shortname.split(" ", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        if parts:
            return parts[0], ""
        return "", ""

    @staticmethod
    def _parse_platform_details(raw: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        """Extract the platform and whether it is the scheduled one."""
        platform = raw.get("platform", None)
        if platform in ("", "?"):
            platform = None

        platform_info = raw.get("platforminfo", {})
        is_normal = platform_info.get("normal", "1") == "1"
        return platform, is_normal

    @staticmethod
    def _parse_occupancy(raw: Dict[str, Any]) -> str:
        """Normalize the optional occupancy term emitted by iRail."""
        occupancy_info = raw.get("occupancy", {})
        occupancy = occupancy_info.get("name", "unknown")
        if occupancy not in ("low", "medium", "high", "unknown"):
            return "unknown"
        return occupancy

    @staticmethod
    def _parse_connection_uri(raw: Dict[str, Any], *keys: str) -> str:
        """Return the first non-empty connection URI field from the payload."""
        for key in keys:
            value = raw.get(key)
            if value:
                return str(value)
        return ""

    @staticmethod
    def _normalize_board_entries(raw_entries: Any) -> List[Dict[str, Any]]:
        """Normalize liveboard entry collections to a list."""
        if isinstance(raw_entries, list):
            return raw_entries
        if isinstance(raw_entries, dict):
            return [raw_entries]
        return []

    @staticmethod
    def parse_departure(raw: Dict[str, Any]) -> Departure:
        """Convert a raw departure dict from the iRail liveboard API to a Departure data class."""
        station_info = raw.get("stationinfo", {})
        dest_station_id = IRailAPI._parse_station_id(station_info.get("id", ""))
        scheduled_time = IRailAPI._parse_scheduled_time(raw.get("time", "0"))

        vehicle_info = raw.get("vehicleinfo", {})
        vehicle_type, vehicle_number = IRailAPI._parse_vehicle_details(vehicle_info)
        platform, is_normal = IRailAPI._parse_platform_details(raw)
        occupancy = IRailAPI._parse_occupancy(raw)

        return Departure(
            destination_station_id=dest_station_id,
            destination_name=raw.get("station", station_info.get("name", "")),
            scheduled_time=scheduled_time,
            delay_seconds=int(raw.get("delay", "0")),
            is_canceled=str(raw.get("canceled", "0")) == "1",
            has_left=str(raw.get("left", "0")) == "1",
            is_extra_stop=str(raw.get("isExtra", "0")) == "1",
            vehicle_id=raw.get("vehicle", vehicle_info.get("name", "")),
            vehicle_short_name=vehicle_info.get("shortname", ""),
            vehicle_type=vehicle_type,
            vehicle_number=vehicle_number,
            platform=platform,
            is_normal_platform=is_normal,
            occupancy=occupancy,  # type: ignore[arg-type]
            departure_connection_uri=IRailAPI._parse_connection_uri(raw, "departureConnection", "connection"),
        )

    @staticmethod
    def parse_arrival(raw: Dict[str, Any]) -> Arrival:
        """Convert a raw arrival dict from the iRail liveboard API to an Arrival data class."""
        station_info = raw.get("stationinfo", {})
        origin_station_id = IRailAPI._parse_station_id(station_info.get("id", ""))
        scheduled_time = IRailAPI._parse_scheduled_time(raw.get("time", "0"))

        vehicle_info = raw.get("vehicleinfo", {})
        vehicle_type, vehicle_number = IRailAPI._parse_vehicle_details(vehicle_info)
        platform, is_normal = IRailAPI._parse_platform_details(raw)
        occupancy = IRailAPI._parse_occupancy(raw)

        return Arrival(
            origin_station_id=origin_station_id,
            origin_name=raw.get("station", station_info.get("name", "")),
            scheduled_time=scheduled_time,
            delay_seconds=int(raw.get("delay", "0")),
            is_canceled=str(raw.get("canceled", "0")) == "1",
            has_arrived=str(raw.get("arrived", "0")) == "1",
            is_extra_stop=str(raw.get("isExtra", "0")) == "1",
            vehicle_id=raw.get("vehicle", vehicle_info.get("name", "")),
            vehicle_short_name=vehicle_info.get("shortname", ""),
            vehicle_type=vehicle_type,
            vehicle_number=vehicle_number,
            platform=platform,
            is_normal_platform=is_normal,
            occupancy=occupancy,  # type: ignore[arg-type]
            connection_uri=IRailAPI._parse_connection_uri(raw, "arrivalConnection", "departureConnection", "connection"),
        )

    @staticmethod
    def parse_liveboard(raw: Dict[str, Any], station_id: str) -> StationBoard:
        """Convert a raw liveboard response to a StationBoard data class."""
        timestamp_unix = int(raw.get("timestamp", "0"))
        retrieved_at = datetime.fromtimestamp(timestamp_unix, tz=timezone.utc).isoformat()

        departures_obj = raw.get("departures", {})
        raw_departures = IRailAPI._normalize_board_entries(departures_obj.get("departure", []))
        departures = []
        for dep in raw_departures:
            try:
                departures.append(IRailAPI.parse_departure(dep))
            except Exception as e:
                logging.debug("Skipping malformed departure: %s", e)

        station_info_raw = raw.get("stationinfo", {})
        station_name = raw.get("station", station_info_raw.get("name", ""))

        return StationBoard(
            station_id=station_id,
            station_name=station_name,
            retrieved_at=retrieved_at,
            departure_count=len(departures),
            departures=departures,
        )

    @staticmethod
    def parse_arrivalboard(raw: Dict[str, Any], station_id: str) -> ArrivalBoard:
        """Convert a raw liveboard response to an ArrivalBoard data class."""
        timestamp_unix = int(raw.get("timestamp", "0"))
        retrieved_at = datetime.fromtimestamp(timestamp_unix, tz=timezone.utc).isoformat()

        arrivals_obj = raw.get("arrivals", {})
        raw_arrivals = IRailAPI._normalize_board_entries(arrivals_obj.get("arrival", []))
        arrivals = []
        for arr in raw_arrivals:
            try:
                arrivals.append(IRailAPI.parse_arrival(arr))
            except Exception as e:
                logging.debug("Skipping malformed arrival: %s", e)

        station_info_raw = raw.get("stationinfo", {})
        station_name = raw.get("station", station_info_raw.get("name", ""))

        return ArrivalBoard(
            station_id=station_id,
            station_name=station_name,
            retrieved_at=retrieved_at,
            arrival_count=len(arrivals),
            arrivals=arrivals,
        )
