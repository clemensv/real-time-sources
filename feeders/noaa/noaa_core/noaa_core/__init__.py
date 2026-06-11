"""Transport-agnostic core for the NOAA Tides & Currents bridge.

This module holds the upstream acquisition and record-normalisation logic that
is shared by every transport-specific feeder app (Kafka, MQTT, AMQP). It has
**no** dependency on any generated producer or data-class package, so each
transport app imports it, receives raw upstream dicts plus normalised
measurement field dictionaries, and builds *its own* generated data classes
before emitting via *its own* generated producer/client.

The Kafka feeder (``noaa/noaa.py``) predates this module and keeps its own
inline copy of the same logic; this module is the canonical home used by the
MQTT and AMQP feeders.
"""

import json
import os
from datetime import datetime, timedelta, timezone
from typing import Callable, Dict, List, Optional

import requests

# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-noaa/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

SOURCE_URI = "https://api.tidesandcurrents.noaa.gov"
STATIONS_URL = "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json"

VISIBILITY_DATASCHEMA = (
    "#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/"
    "Microsoft.OpenData.US.NOAA.Visibility"
)
VISIBILITY_DATACONTENTTYPE = "application/json"

# Ordered list of products polled per station. The MQTT/AMQP apps iterate this
# in order so behaviour matches the Kafka feeder.
PRODUCT_ORDER: List[str] = [
    "water_level",
    "predictions",
    "air_temperature",
    "wind",
    "air_pressure",
    "water_temperature",
    "conductivity",
    "visibility",
    "humidity",
    "salinity",
    "currents",
    "currents_predictions",
]


class NOAAClient:
    """HTTP acquisition client for the NOAA Tides & Currents APIs."""

    BASE_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
    COMMON_PARAMS = "&units=metric&time_zone=gmt&application=web_services&format=json"

    PRODUCTS = {
        "water_level": "product=water_level",
        "predictions": "product=predictions",
        "air_temperature": "product=air_temperature",
        "wind": "product=wind",
        "air_pressure": "product=air_pressure",
        "water_temperature": "product=water_temperature",
        "conductivity": "product=conductivity",
        "visibility": "product=visibility",
        "humidity": "product=humidity",
        "salinity": "product=salinity",
        "currents": "product=currents",
        "currents_predictions": "product=currents_predictions",
    }

    def __init__(self, user_agent: str = USER_AGENT, request_timeout: float = 10.0):
        self.user_agent = user_agent
        self.request_timeout = request_timeout

    def _headers(self) -> Dict[str, str]:
        return {"User-Agent": self.user_agent}

    def fetch_stations_raw(self) -> List[dict]:
        """Fetch the full NOAA station list as sanitised raw dicts.

        The returned dicts are ready to be loaded by a transport-specific
        ``Station.schema().load(..., many=True)`` call. ``id`` is renamed to
        ``station_id`` and optional keys on nested link objects are backfilled
        so the generated schema (whose optional fields lack ``None`` defaults)
        decodes cleanly.
        """
        try:
            response = requests.get(
                STATIONS_URL, headers=self._headers(), timeout=self.request_timeout
            )
            response.raise_for_status()
            raw_stations = response.json().get("stations", [])
        except requests.RequestException as err:
            print(f"Error fetching stations: {err}")
            return []

        for s in raw_stations:
            if s.get("portscode") is None:
                s["portscode"] = ""
            s["station_id"] = s.pop("id", "")
            # The generated Station schema models every nested link object with
            # the generic UnnamedClass, whose optional `region` and
            # `station_id` fields are emitted without a `None` default.
            # dataclasses_json therefore requires those keys on every nested
            # object, but the NOAA station list returns bare `{"self": ...}`
            # link stubs that omit them. Backfill the optional keys so the
            # decode succeeds. The JsonStructure schema types both keys as
            # `string`, so backfill an empty string (not None) to keep the
            # emitted CloudEvent schema-valid. (Upstream codegen bug: optional
            # string fields must default to "".)
            for value in s.values():
                for item in (value if isinstance(value, list) else [value]):
                    if isinstance(item, dict):
                        item.setdefault("region", "")
                        item.setdefault("station_id", "")
        return raw_stations

    @staticmethod
    def datum_for_tide_type(tide_type: Optional[str]) -> str:
        """Return the tidal datum to request for a station's tide type."""
        return "IGLD" if tide_type == "Great Lakes" else "MLLW"

    def poll_product(
        self, product: str, station_id: str, datum: str, last_polled_time: datetime
    ) -> List[dict]:
        """Poll the NOAA datagetter API for one product/station, returning raw records."""
        if datum == "IGLD" and "predictions" in product:
            return []  # Great Lakes stations don't have prediction data

        # Clamp date range to NOAA API limits:
        #   predictions: max 1 year; 6-minute interval data: max 1 month.
        now = datetime.now(timezone.utc)
        if product in ("predictions", "currents_predictions"):
            max_begin_date = now - timedelta(days=365)
        else:
            max_begin_date = now - timedelta(days=30)
        begin_date = max(last_polled_time, max_begin_date)

        product_url = (
            f"{self.BASE_URL}?{self.PRODUCTS[product]}{self.COMMON_PARAMS}"
            f"&station={station_id}"
        )
        if product not in ("currents_predictions", "currents"):
            product_url += f"&datum={datum}"
        if product in ("currents", "currents_predictions"):
            product_url += "&bin=1"
        product_url += (
            f"&begin_date={begin_date.strftime('%Y%m%d %H:%M')}"
            f"&end_date={now.strftime('%Y%m%d %H:%M')}"
        )

        if product == "currents_predictions":
            data_key = None
        elif "predictions" in product:
            data_key = "predictions"
        else:
            data_key = "data"

        try:
            response = requests.get(
                product_url, headers=self._headers(), timeout=self.request_timeout
            )
            response.raise_for_status()
            if data_key is None:
                return response.json().get("current_predictions", {}).get("cp", [])
            return response.json().get(data_key, [])
        except requests.RequestException as err:
            print(f"Error fetching data for station {station_id}: {err}")
            return []


def record_timestamp(product: str, record: dict) -> datetime:
    """Parse the UTC timestamp from a NOAA record for the given product."""
    ts_field = "Time" if product == "currents_predictions" else "t"
    return datetime.strptime(record[ts_field], "%Y-%m-%d %H:%M").replace(
        tzinfo=timezone.utc
    )


def _f(record: dict, idx: int) -> bool:
    """Return the boolean value of the idx-th NOAA quality flag in field 'f'."""
    return bool(record.get("f", "").split(",")[idx] == "1")


def _v(record: dict, key: str) -> float:
    """Return a record value as float, defaulting to 0.0 when absent/empty."""
    return float(record[key]) if key in record and record[key] else 0.0


def _extract_water_level(record: dict) -> dict:
    return {
        "value": _v(record, "v"),
        "stddev": _v(record, "s"),
        "outside_sigma_band": _f(record, 0),
        "flat_tolerance_limit": _f(record, 1),
        "rate_of_change_limit": _f(record, 2),
        "max_min_expected_height": _f(record, 3),
        # Map the raw NOAA 'q' quality flag ('p' = preliminary) to a bool so the
        # transport app can pick its own package's QualityLevel enum member.
        "quality_preliminary": record.get("q", "") == "p",
    }


def _extract_predictions(record: dict) -> dict:
    return {"value": _v(record, "v")}


def _extract_air_temperature(record: dict) -> dict:
    return {
        "value": _v(record, "v"),
        "max_temp_exceeded": _f(record, 0),
        "min_temp_exceeded": _f(record, 1),
        "rate_of_change_exceeded": _f(record, 2),
    }


def _extract_wind(record: dict) -> dict:
    return {
        "speed": _v(record, "s"),
        "direction_degrees": record["d"] if "d" in record and record["d"] else 0.0,
        "direction_text": record["dr"] if "dr" in record and record["dr"] else "",
        "gusts": _v(record, "g"),
        "max_wind_speed_exceeded": _f(record, 0),
        "rate_of_change_exceeded": _f(record, 1),
    }


def _extract_air_pressure(record: dict) -> dict:
    return {
        "value": _v(record, "v"),
        "max_pressure_exceeded": _f(record, 0),
        "min_pressure_exceeded": _f(record, 1),
        "rate_of_change_exceeded": _f(record, 2),
    }


def _extract_water_temperature(record: dict) -> dict:
    return {
        "value": _v(record, "v"),
        "max_temp_exceeded": _f(record, 0),
        "min_temp_exceeded": _f(record, 1),
        "rate_of_change_exceeded": _f(record, 2),
    }


def _extract_conductivity(record: dict) -> dict:
    return {
        "value": _v(record, "v"),
        "max_conductivity_exceeded": _f(record, 0),
        "min_conductivity_exceeded": _f(record, 1),
        "rate_of_change_exceeded": _f(record, 2),
    }


def _extract_visibility(record: dict) -> dict:
    return {
        "value": _v(record, "v"),
        "max_visibility_exceeded": _f(record, 0),
        "min_visibility_exceeded": _f(record, 1),
        "rate_of_change_exceeded": _f(record, 2),
    }


def _extract_humidity(record: dict) -> dict:
    return {
        "value": _v(record, "v"),
        "max_humidity_exceeded": _f(record, 0),
        "min_humidity_exceeded": _f(record, 1),
        "rate_of_change_exceeded": _f(record, 2),
    }


def _extract_salinity(record: dict) -> dict:
    return {
        "salinity": _v(record, "s"),
        "grams_per_kg": _v(record, "g"),
    }


def _extract_currents(record: dict) -> dict:
    return {
        "speed": _v(record, "s"),
        "direction_degrees": _v(record, "d"),
        "bin": record.get("b", "1"),
    }


def _extract_currents_predictions(record: dict) -> dict:
    return {
        "velocity_major": _v(record, "Velocity_Major"),
        "mean_flood_dir": _v(record, "meanFloodDir"),
        "mean_ebb_dir": _v(record, "meanEbbDir"),
        "depth": _v(record, "Depth"),
        "bin": record.get("Bin", "1"),
    }


EXTRACTORS: Dict[str, Callable[[dict], dict]] = {
    "water_level": _extract_water_level,
    "predictions": _extract_predictions,
    "air_temperature": _extract_air_temperature,
    "wind": _extract_wind,
    "air_pressure": _extract_air_pressure,
    "water_temperature": _extract_water_temperature,
    "conductivity": _extract_conductivity,
    "visibility": _extract_visibility,
    "humidity": _extract_humidity,
    "salinity": _extract_salinity,
    "currents": _extract_currents,
    "currents_predictions": _extract_currents_predictions,
}


def extract_fields(product: str, record: dict) -> dict:
    """Return the measurement-specific data-class kwargs for a NOAA record.

    The returned dict excludes ``station_id``, ``region`` and ``timestamp`` —
    the caller adds those. For ``water_level`` the dict carries
    ``quality_preliminary`` (bool) instead of an enum so each transport app can
    map it onto its own generated ``QualityLevel`` member.
    """
    return EXTRACTORS[product](record)


def select_stations(stations: list, station_arg: Optional[str]) -> list:
    """Filter loaded Station objects by a comma-separated list of station IDs.

    Returns the full list when ``station_arg`` is falsy. Prints any missing IDs
    and returns an empty list when specific stations were requested but none
    matched (the caller should treat that as a fatal error).
    """
    if not station_arg:
        return list(stations)
    requested = [s.strip() for s in str(station_arg).split(",") if s.strip()]
    selected = [s for s in stations if s.station_id in requested]
    found_ids = {s.station_id for s in selected}
    missing = [r for r in requested if r not in found_ids]
    if missing:
        print(f"Station(s) not found: {', '.join(missing)}")
    if not selected:
        print(f"None of the requested stations were found: {', '.join(requested)}")
    return selected


def default_last_polled_file() -> str:
    """Resolve the default last-polled state file path."""
    return os.getenv("NOAA_LAST_POLLED_FILE") or os.path.expanduser(
        "~/.noaa_last_polled.json"
    )


def load_last_polled_times(path: str) -> Dict[str, Dict[str, datetime]]:
    """Load per-product/per-station last-polled timestamps from a JSON file."""
    try:
        if path and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                saved: Dict[str, Dict[str, str]] = json.load(file)
            result: Dict[str, Dict[str, datetime]] = {}
            for product, stations in saved.items():
                for station, timestamp in stations.items():
                    result.setdefault(product, {})[station] = datetime.fromisoformat(
                        timestamp
                    )
            return result
    except Exception:
        print("Error loading last polled times")
    return {}


def save_last_polled_times(path: str, last_polled_times: Dict[str, Dict[str, datetime]]) -> None:
    """Persist per-product/per-station last-polled timestamps to a JSON file."""
    if not path:
        return
    saved: Dict[str, Dict[str, str]] = {}
    for product, stations in last_polled_times.items():
        for station, timestamp in stations.items():
            saved.setdefault(product, {})[station] = timestamp.isoformat()
    with open(path, "w", encoding="utf-8") as file:
        json.dump(saved, file)
