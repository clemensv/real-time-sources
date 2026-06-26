"""Transport-agnostic acquisition and state handling for NWS forecasts."""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, Iterable, List, Optional
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


LOGGER = logging.getLogger(__name__)

DEFAULT_ZONES = "WAZ312,WAZ315,WAZ316,WAZ317,PZZ130,PZZ131,PZZ132,PZZ133,PZZ134,PZZ135"
ZONE_DETAIL_URL = "https://api.weather.gov/zones/forecast/{zone_id}"
LAND_FORECAST_URL = "https://api.weather.gov/zones/forecast/{zone_id}/forecast"
MARINE_PRODUCTS_URL = "https://api.weather.gov/products?type=CWF&location={office}&limit=1"
MARINE_PRODUCT_URL = "https://api.weather.gov/products/{product_id}"
DEFAULT_POLL_INTERVAL_SECONDS = 900
DEFAULT_REFERENCE_REFRESH_SECONDS = 21600
DEFAULT_STATE_FILE = "/mnt/fileshare/nws_forecasts_state.json"

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-nws-forecasts/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/geo+json",
}
MARINE_PERIOD_RE = re.compile(r"^\.(?P<name>[A-Z0-9 /]+)\.\.\.(?P<body>.*)$")
ZONE_HEADER_RE = re.compile(r"^(?P<zone_id>[A-Z]{3}[0-9]{3})-[0-9]{6,}-?$")


# ---------------------------------------------------------------------------
# Transport-neutral dataclasses mirroring the generated producer_data shapes.
# Both Kafka and AMQP producers expose identically-named fields, so callers
# can pass NWSForecastZone / NWSLandZoneForecast / NWSMarineZoneForecast
# instances directly to either producer after a trivial field-copy shim.
# ---------------------------------------------------------------------------

@dataclass
class NWSForecastPeriod:
    period_number: Optional[int]
    period_name: str
    detailed_forecast: str


@dataclass
class NWSMarinePeriod:
    period_name: str
    forecast_text: str


@dataclass
class NWSForecastZone:
    zone_id: str
    zone_type: str          # "public" | "marine" (raw string avoids cross-import)
    name: str
    state: str
    forecast_office_url: str
    grid_identifier: Optional[str]
    awips_location_identifier: Optional[str]
    cwa_ids: List[str]
    forecast_office_urls: List[str]
    time_zones: List[str]
    observation_station_ids: List[str]
    radar_station: Optional[str]
    effective_date: datetime
    expiration_date: datetime


@dataclass
class NWSLandZoneForecast:
    zone_id: str
    updated: datetime
    periods: List[NWSForecastPeriod]


@dataclass
class NWSMarineZoneForecast:
    zone_id: str
    zone_name: Optional[str]
    product_title: Optional[str]
    office_name: Optional[str]
    issued_at_text: Optional[str]
    expires_text: Optional[str]
    wmo_header: Optional[str]
    bulletin_awips_id: Optional[str]
    synopsis: Optional[str]
    periods: List[NWSMarinePeriod]
    bulletin_text: Optional[str]


@dataclass
class PendingState:
    land_updates: Dict[str, str]
    marine_hashes: Dict[str, str]


def build_retrying_session() -> requests.Session:
    """Create a requests session with bounded retries for transient failures."""
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(HEADERS)
    return session


def parse_zone_list(raw: str) -> List[str]:
    zones = [zone.strip().upper() for zone in raw.split(",") if zone.strip()]
    if not zones:
        raise ValueError("At least one zone ID must be configured.")
    return zones


class NWSForecastFetcher:
    """
    Transport-neutral NWS forecast acquisition and state management.

    Callers supply three optional callbacks:
      on_zone(zone_id, zone)               – called when reference data is ready
      on_land_forecast(zone_id, forecast)  – called for each new land forecast
      on_marine_forecast(zone_id, forecast)– called for each new marine forecast

    The callbacks receive the transport-neutral NWSForecastZone /
    NWSLandZoneForecast / NWSMarineZoneForecast dataclasses defined in this
    module.  Each transport adapter (Kafka, AMQP, MQTT) is responsible for
    converting those to its own generated producer_data types and sending them.
    """

    def __init__(
        self,
        zones: List[str],
        state_file: str,
        poll_interval_seconds: int = DEFAULT_POLL_INTERVAL_SECONDS,
        reference_refresh_seconds: int = DEFAULT_REFERENCE_REFRESH_SECONDS,
        session: Optional[requests.Session] = None,
        on_zone: Optional[Callable[[str, NWSForecastZone], None]] = None,
        on_land_forecast: Optional[Callable[[str, NWSLandZoneForecast], None]] = None,
        on_marine_forecast: Optional[Callable[[str, NWSMarineZoneForecast], None]] = None,
        flush_callback: Optional[Callable[[], None]] = None,
    ) -> None:
        self.zones = zones
        self.state_file = state_file
        self.poll_interval_seconds = poll_interval_seconds
        self.reference_refresh_seconds = reference_refresh_seconds
        self.session = session or build_retrying_session()
        self.on_zone = on_zone or (lambda _zid, _z: None)
        self.on_land_forecast = on_land_forecast or (lambda _zid, _f: None)
        self.on_marine_forecast = on_marine_forecast or (lambda _zid, _f: None)
        self.flush_callback = flush_callback or (lambda: None)
        self.zone_cache: Dict[str, NWSForecastZone] = {}
        self._last_reference_refresh = 0.0
        self._marine_offices: Dict[str, List[str]] = {}

    # ------------------------------------------------------------------
    # State persistence
    # ------------------------------------------------------------------

    def load_state(self) -> Dict[str, Dict[str, str]]:
        if not os.path.exists(self.state_file):
            return {"land_updates": {}, "marine_hashes": {}}
        with open(self.state_file, "r", encoding="utf-8") as handle:
            raw = handle.read().strip()
        if not raw:
            return {"land_updates": {}, "marine_hashes": {}}
        return json.loads(raw)

    def save_state(self, state: Dict[str, Dict[str, str]]) -> None:
        directory = os.path.dirname(self.state_file)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(self.state_file, "w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, sort_keys=True)

    # ------------------------------------------------------------------
    # HTTP helpers
    # ------------------------------------------------------------------

    def _get_json(self, url: str) -> Dict[str, Any]:
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _station_ids(urls: Iterable[str]) -> List[str]:
        station_ids: List[str] = []
        for url in urls:
            path = urlparse(url).path.rstrip("/")
            station_ids.append(path.split("/")[-1])
        return station_ids

    # ------------------------------------------------------------------
    # Zone reference data
    # ------------------------------------------------------------------

    def fetch_zone(self, zone_id: str) -> NWSForecastZone:
        data = self._get_json(ZONE_DETAIL_URL.format(zone_id=zone_id))
        props = data["properties"]
        return NWSForecastZone(
            zone_id=props["id"],
            zone_type=props["type"],
            name=props["name"],
            state=props["state"],
            forecast_office_url=props["forecastOffice"],
            grid_identifier=props.get("gridIdentifier"),
            awips_location_identifier=props.get("awipsLocationIdentifier"),
            cwa_ids=props.get("cwa", []),
            forecast_office_urls=props.get("forecastOffices", []),
            time_zones=props.get("timeZone", []),
            observation_station_ids=self._station_ids(props.get("observationStations", [])),
            radar_station=props.get("radarStation"),
            effective_date=datetime.fromisoformat(props["effectiveDate"].replace("Z", "+00:00")),
            expiration_date=datetime.fromisoformat(props["expirationDate"].replace("Z", "+00:00")),
        )

    def refresh_zone_cache(self) -> None:
        next_cache = dict(self.zone_cache)
        marine_offices: Dict[str, List[str]] = {}
        for zone_id in self.zones:
            try:
                next_cache[zone_id] = self.fetch_zone(zone_id)
            except (requests.RequestException, ValueError, KeyError) as exc:
                if zone_id in next_cache:
                    LOGGER.warning("Keeping cached zone %s after refresh failure: %s", zone_id, exc)
                else:
                    LOGGER.error("Failed to fetch zone %s: %s", zone_id, exc)
        self.zone_cache = next_cache
        for zone_id, zone in self.zone_cache.items():
            if zone.zone_type != "public":
                for cwa in (zone.cwa_ids or []):
                    marine_offices.setdefault(cwa, []).append(zone_id)
        self._marine_offices = marine_offices
        self._last_reference_refresh = time.time()

    def emit_reference_data(self) -> None:
        if not self.zone_cache:
            self.refresh_zone_cache()
        for zone_id in self.zones:
            zone = self.zone_cache.get(zone_id)
            if zone is None:
                continue
            self.on_zone(zone_id, zone)
        self.flush_callback()

    # ------------------------------------------------------------------
    # Land forecast
    # ------------------------------------------------------------------

    def fetch_land_forecast(self, zone_id: str) -> NWSLandZoneForecast:
        data = self._get_json(LAND_FORECAST_URL.format(zone_id=zone_id))
        props = data["properties"]
        periods = [
            NWSForecastPeriod(
                period_number=period["number"],
                period_name=period["name"],
                detailed_forecast=period["detailedForecast"],
            )
            for period in props.get("periods", [])
        ]
        return NWSLandZoneForecast(
            zone_id=zone_id,
            updated=datetime.fromisoformat(props["updated"].replace("Z", "+00:00")),
            periods=periods,
        )

    # ------------------------------------------------------------------
    # Marine forecast
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_whitespace(value: str) -> str:
        return re.sub(r"\s+", " ", value.strip())

    def parse_marine_forecast(self, zone_id: str, text: str) -> NWSMarineZoneForecast:
        lines = [line.rstrip() for line in text.splitlines()]
        expires_text = lines[0][len("Expires:"):].strip() if lines and lines[0].startswith("Expires:") else None
        non_empty = [line for line in lines if line.strip()]

        header_start = 0
        for idx, line in enumerate(non_empty):
            if len(line.strip()) >= 10 and " " in line.strip():
                header_start = idx
                break
        wmo_header = non_empty[header_start] if len(non_empty) > header_start else None
        bulletin_awips_id = non_empty[header_start + 1] if len(non_empty) > header_start + 1 else None
        product_title = non_empty[header_start + 2] if len(non_empty) > header_start + 2 else None
        office_name = non_empty[header_start + 3] if len(non_empty) > header_start + 3 else None

        zone_header_index = next(
            (index for index, line in enumerate(lines) if ZONE_HEADER_RE.match(line.strip()) and line.startswith(zone_id)),
            None,
        )
        if zone_header_index is None:
            raise ValueError(f"Marine bulletin for {zone_id} did not contain a zone header.")

        zone_name_line = lines[zone_header_index + 1].strip()
        issued_at_text = lines[zone_header_index + 2].strip()
        first_zone_header = next(
            (index for index, line in enumerate(lines) if ZONE_HEADER_RE.match(line.strip())),
            zone_header_index,
        )
        synopsis_lines = [
            line.strip()
            for line in lines[first_zone_header:zone_header_index]
            if line.strip() and not ZONE_HEADER_RE.match(line.strip())
        ]
        synopsis = "\n".join(synopsis_lines) if synopsis_lines else None

        period_items: List[NWSMarinePeriod] = []
        current_name: Optional[str] = None
        current_lines: List[str] = []
        zone_body_lines: List[str] = []

        for line in lines[zone_header_index + 3:]:
            if line.strip() == "$$":
                break
            zone_body_lines.append(line)
            match = MARINE_PERIOD_RE.match(line.strip())
            if match:
                if current_name is not None:
                    period_items.append(
                        NWSMarinePeriod(
                            period_name=current_name,
                            forecast_text=self._normalize_whitespace(" ".join(current_lines)),
                        )
                    )
                current_name = match.group("name")
                current_lines = [match.group("body").strip()]
            elif current_name is not None:
                current_lines.append(line.strip())

        if current_name is not None:
            period_items.append(
                NWSMarinePeriod(
                    period_name=current_name,
                    forecast_text=self._normalize_whitespace(" ".join(current_lines)),
                )
            )

        if not period_items:
            raise ValueError(f"Marine bulletin for {zone_id} did not contain any forecast periods.")

        bulletin_text = "\n".join(zone_body_lines).strip()
        return NWSMarineZoneForecast(
            zone_id=zone_id,
            zone_name=zone_name_line.rstrip("-"),
            product_title=product_title,
            office_name=office_name,
            issued_at_text=issued_at_text,
            expires_text=expires_text,
            wmo_header=wmo_header,
            bulletin_awips_id=bulletin_awips_id,
            synopsis=synopsis,
            periods=period_items,
            bulletin_text=bulletin_text,
        )

    def fetch_marine_forecast(self, zone_id: str) -> NWSMarineZoneForecast:
        zone = self.zone_cache.get(zone_id)
        if zone is None:
            raise ValueError(f"No cached zone metadata for {zone_id}")
        offices = zone.cwa_ids or []
        if not offices:
            raise ValueError(f"Zone {zone_id} has no CWA office identifier")
        office = offices[0]
        products_data = self._get_json(MARINE_PRODUCTS_URL.format(office=office))
        products = products_data.get("@graph", [])
        if not products:
            raise ValueError(f"No CWF product found for office {office}")
        product_id = products[0]["id"]
        product_data = self._get_json(MARINE_PRODUCT_URL.format(product_id=product_id))
        text = product_data.get("productText", "")
        if not text:
            raise ValueError(f"CWF product {product_id} has no text content")
        return self.parse_marine_forecast(zone_id, text)

    @staticmethod
    def _marine_digest(forecast: NWSMarineZoneForecast) -> str:
        return hashlib.sha256((forecast.bulletin_text or "").encode("utf-8")).hexdigest()

    # ------------------------------------------------------------------
    # Polling loop
    # ------------------------------------------------------------------

    def poll_once(self) -> int:
        """
        Fetch all zones once, call the on_* callbacks for changed forecasts,
        call flush_callback after all sends, persist state, and return the
        number of new/changed events emitted.
        """
        state = self.load_state()
        current_land = dict(state.get("land_updates", {}))
        current_marine = dict(state.get("marine_hashes", {}))
        pending = PendingState(land_updates=dict(current_land), marine_hashes=dict(current_marine))
        emitted = 0

        for zone_id in self.zones:
            zone = self.zone_cache.get(zone_id)
            if zone is None:
                LOGGER.warning("Skipping %s because no zone metadata is cached yet.", zone_id)
                continue
            try:
                if zone.zone_type == "public":
                    land_forecast = self.fetch_land_forecast(zone_id)
                    updated_value = land_forecast.updated.isoformat()
                    if current_land.get(zone_id) == updated_value:
                        continue
                    self.on_land_forecast(zone_id, land_forecast)
                    pending.land_updates[zone_id] = updated_value
                    emitted += 1
                else:
                    marine_forecast = self.fetch_marine_forecast(zone_id)
                    digest = self._marine_digest(marine_forecast)
                    if current_marine.get(zone_id) == digest:
                        continue
                    self.on_marine_forecast(zone_id, marine_forecast)
                    pending.marine_hashes[zone_id] = digest
                    emitted += 1
            except (requests.RequestException, ValueError, KeyError) as exc:
                LOGGER.error("Failed to process forecast slice %s: %s", zone_id, exc)

        self.flush_callback()

        if emitted > 0:
            self.save_state(
                {
                    "land_updates": pending.land_updates,
                    "marine_hashes": pending.marine_hashes,
                }
            )
        return emitted

    def run(
        self,
        once: bool = False,
        emit_reference_with_backoff: Optional[Callable[[], None]] = None,
    ) -> None:
        """
        Main polling loop.  Optionally accepts an ``emit_reference_with_backoff``
        hook so the caller can wrap emit_reference_data with its own error
        tolerance (e.g. Kafka flush retries).
        """
        _emit_ref = emit_reference_with_backoff or self._default_emit_reference_with_backoff
        LOGGER.info("Starting NWS forecast poller for zones: %s", ", ".join(self.zones))
        self.refresh_zone_cache()
        _emit_ref()

        consecutive_failures = 0
        max_consecutive_failures = 5

        while True:
            now = time.time()
            if now - self._last_reference_refresh >= self.reference_refresh_seconds:
                self.refresh_zone_cache()
                _emit_ref()

            try:
                emitted = self.poll_once()
                consecutive_failures = 0
                LOGGER.info("Completed forecast poll; emitted %s changed forecast snapshot(s).", emitted)
            except RuntimeError as exc:
                consecutive_failures += 1
                LOGGER.error("Poll cycle failed (%d/%d): %s", consecutive_failures, max_consecutive_failures, exc)
                if consecutive_failures >= max_consecutive_failures:
                    raise RuntimeError(
                        f"Delivery failed {max_consecutive_failures} consecutive times, giving up."
                    ) from exc

            if once:
                return
            time.sleep(self.poll_interval_seconds)

    def _default_emit_reference_with_backoff(self) -> None:
        try:
            self.emit_reference_data()
        except Exception as exc:
            LOGGER.warning("Reference data emission failed (will retry next refresh): %s", exc)
