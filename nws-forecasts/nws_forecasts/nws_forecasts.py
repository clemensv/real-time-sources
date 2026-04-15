"""NWS forecast zone bridge."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urlparse

import requests
from confluent_kafka import Producer
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from nws_forecasts_producer_data import (
    ForecastZone,
    LandForecastPeriod,
    LandZoneForecast,
    MarineForecastPeriod,
    MarineZoneForecast,
    ZoneTypeenum,
)
from nws_forecasts_producer_kafka_producer.producer import (
    MicrosoftOpenDataUSNOAANWSForecastsEventProducer,
)


LOGGER = logging.getLogger(__name__)
DEFAULT_ZONES = "WAZ312,WAZ315,WAZ316,WAZ317,PZZ130,PZZ131,PZZ132,PZZ133,PZZ134,PZZ135"
ZONE_DETAIL_URL = "https://api.weather.gov/zones/forecast/{zone_id}"
LAND_FORECAST_URL = "https://api.weather.gov/zones/forecast/{zone_id}/forecast"
MARINE_FORECAST_URL = "https://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/pz/{zone_id}.txt"
DEFAULT_POLL_INTERVAL_SECONDS = 900
DEFAULT_REFERENCE_REFRESH_SECONDS = 21600
DEFAULT_STATE_FILE = "/mnt/fileshare/nws_forecasts_state.json"
HEADERS = {
    "User-Agent": "(real-time-sources, clemensv@microsoft.com)",
    "Accept": "application/geo+json",
}
MARINE_PERIOD_RE = re.compile(r"^\.(?P<name>[A-Z0-9 /]+)\.\.\.(?P<body>.*)$")
ZONE_HEADER_RE = re.compile(r"^(?P<zone_id>[A-Z]{3}[0-9]{3})-[0-9]{6,}-?$")


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


def parse_connection_string(connection_string: str, enable_tls: bool = True) -> Dict[str, str]:
    """Parse Event Hubs/Fabric or BootstrapServer connection strings into Kafka config."""
    parts: Dict[str, str] = {}
    for item in connection_string.split(";"):
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        parts[key] = value

    if "Endpoint" in parts:
        endpoint = parts["Endpoint"].replace("sb://", "").rstrip("/")
        config = {
            "bootstrap.servers": f"{endpoint}:9093",
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "sasl.username": "$ConnectionString",
            "sasl.password": connection_string.strip(),
        }
    elif "BootstrapServer" in parts:
        config = {
            "bootstrap.servers": parts["BootstrapServer"],
            "security.protocol": "SSL" if enable_tls else "PLAINTEXT",
        }
    else:
        raise ValueError("Connection string must contain Endpoint or BootstrapServer.")

    if "EntityPath" in parts:
        config["kafka_topic"] = parts["EntityPath"]
    return config


def build_kafka_config(args: argparse.Namespace) -> tuple[Dict[str, str], str]:
    """Build Kafka config and resolve the destination topic."""
    if args.connection_string:
        config = parse_connection_string(args.connection_string, enable_tls=args.kafka_enable_tls)
        parsed_topic = config.pop("kafka_topic", None)
        topic = args.kafka_topic or parsed_topic
        if not topic:
            raise ValueError("Kafka topic must be provided in KAFKA_TOPIC or EntityPath.")
        return config, topic

    if not args.kafka_bootstrap_servers or not args.kafka_topic:
        raise ValueError("Provide CONNECTION_STRING or both KAFKA_BOOTSTRAP_SERVERS and KAFKA_TOPIC.")

    config: Dict[str, str] = {
        "bootstrap.servers": args.kafka_bootstrap_servers,
        "security.protocol": "SASL_SSL" if args.sasl_username and args.kafka_enable_tls else (
            "SASL_PLAINTEXT" if args.sasl_username else ("SSL" if args.kafka_enable_tls else "PLAINTEXT")
        ),
    }
    if args.sasl_username:
        config["sasl.mechanisms"] = "PLAIN"
        config["sasl.username"] = args.sasl_username
        if not args.sasl_password:
            raise ValueError("SASL_PASSWORD is required when SASL_USERNAME is set.")
        config["sasl.password"] = args.sasl_password
    return config, args.kafka_topic


def parse_zone_list(raw: str) -> List[str]:
    zones = [zone.strip().upper() for zone in raw.split(",") if zone.strip()]
    if not zones:
        raise ValueError("At least one zone ID must be configured.")
    return zones


class NWSForecastPoller:
    """Poll NWS land-zone and marine-zone forecasts and emit them as CloudEvents."""

    def __init__(
        self,
        kafka_config: Dict[str, str],
        kafka_topic: str,
        zones: List[str],
        state_file: str,
        poll_interval_seconds: int = DEFAULT_POLL_INTERVAL_SECONDS,
        reference_refresh_seconds: int = DEFAULT_REFERENCE_REFRESH_SECONDS,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.zones = zones
        self.state_file = state_file
        self.poll_interval_seconds = poll_interval_seconds
        self.reference_refresh_seconds = reference_refresh_seconds
        self.session = session or build_retrying_session()
        self.kafka_client = Producer(kafka_config)
        self.producer = MicrosoftOpenDataUSNOAANWSForecastsEventProducer(self.kafka_client, kafka_topic)
        self.zone_cache: Dict[str, ForecastZone] = {}
        self._last_reference_refresh = 0.0

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

    def _get_json(self, url: str) -> Dict[str, Any]:
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def _get_text(self, url: str) -> str:
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    @staticmethod
    def _station_ids(urls: Iterable[str]) -> List[str]:
        station_ids: List[str] = []
        for url in urls:
            path = urlparse(url).path.rstrip("/")
            station_ids.append(path.split("/")[-1])
        return station_ids

    def fetch_zone(self, zone_id: str) -> ForecastZone:
        data = self._get_json(ZONE_DETAIL_URL.format(zone_id=zone_id))
        props = data["properties"]
        return ForecastZone(
            zone_id=props["id"],
            zone_type=ZoneTypeenum(props["type"]),
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
            effective_date=datetime.fromisoformat(props["effectiveDate"]),
            expiration_date=datetime.fromisoformat(props["expirationDate"]),
        )

    def refresh_zone_cache(self) -> None:
        next_cache = dict(self.zone_cache)
        for zone_id in self.zones:
            try:
                next_cache[zone_id] = self.fetch_zone(zone_id)
            except (requests.RequestException, ValueError, KeyError) as exc:
                if zone_id in next_cache:
                    LOGGER.warning("Keeping cached zone %s after refresh failure: %s", zone_id, exc)
                else:
                    LOGGER.error("Failed to fetch zone %s: %s", zone_id, exc)
        self.zone_cache = next_cache
        self._last_reference_refresh = time.time()

    def emit_reference_data(self) -> None:
        if not self.zone_cache:
            self.refresh_zone_cache()

        for zone_id in self.zones:
            zone = self.zone_cache.get(zone_id)
            if zone is None:
                continue
            self.producer.send_microsoft_open_data_us_noaa_nws_forecast_zone(
                zone_id, zone, flush_producer=False
            )

        remaining = self.kafka_client.flush(timeout=30)
        if remaining != 0:
            raise RuntimeError(f"Kafka flush left {remaining} reference messages unsent.")

    def fetch_land_forecast(self, zone_id: str) -> LandZoneForecast:
        data = self._get_json(LAND_FORECAST_URL.format(zone_id=zone_id))
        props = data["properties"]
        periods = [
            LandForecastPeriod(
                period_number=period["number"],
                period_name=period["name"],
                detailed_forecast=period["detailedForecast"],
            )
            for period in props.get("periods", [])
        ]
        return LandZoneForecast(
            zone_id=zone_id,
            updated=datetime.fromisoformat(props["updated"]),
            periods=periods,
        )

    @staticmethod
    def _normalize_whitespace(value: str) -> str:
        return re.sub(r"\s+", " ", value.strip())

    def parse_marine_forecast(self, zone_id: str, text: str) -> MarineZoneForecast:
        lines = [line.rstrip() for line in text.splitlines()]
        expires_text = lines[0][len("Expires:"):].strip() if lines and lines[0].startswith("Expires:") else None
        non_empty = [line for line in lines if line.strip()]

        wmo_header = non_empty[1] if len(non_empty) > 1 else None
        bulletin_awips_id = non_empty[2] if len(non_empty) > 2 else None
        product_title = non_empty[3] if len(non_empty) > 3 else None
        office_name = non_empty[4] if len(non_empty) > 4 else None

        zone_header_index = next(
            (index for index, line in enumerate(lines) if ZONE_HEADER_RE.match(line.strip()) and line.startswith(zone_id)),
            None,
        )
        if zone_header_index is None:
            raise ValueError(f"Marine bulletin for {zone_id} did not contain a zone header.")

        zone_name_line = lines[zone_header_index + 1].strip()
        issued_at_text = lines[zone_header_index + 2].strip()
        synopsis_lines = [
            line.strip()
            for line in lines[5:zone_header_index]
            if line.strip()
        ]
        synopsis = "\n".join(synopsis_lines) if synopsis_lines else None

        period_items: List[MarineForecastPeriod] = []
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
                        MarineForecastPeriod(
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
                MarineForecastPeriod(
                    period_name=current_name,
                    forecast_text=self._normalize_whitespace(" ".join(current_lines)),
                )
            )

        if not period_items:
            raise ValueError(f"Marine bulletin for {zone_id} did not contain any forecast periods.")

        bulletin_text = "\n".join(zone_body_lines).strip()
        return MarineZoneForecast(
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

    def fetch_marine_forecast(self, zone_id: str) -> MarineZoneForecast:
        text = self._get_text(MARINE_FORECAST_URL.format(zone_id=zone_id.lower()))
        return self.parse_marine_forecast(zone_id, text)

    @staticmethod
    def _marine_digest(forecast: MarineZoneForecast) -> str:
        return hashlib.sha256(forecast.bulletin_text.encode("utf-8")).hexdigest()

    def poll_once(self) -> int:
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
                if zone.zone_type == ZoneTypeenum.public:
                    forecast = self.fetch_land_forecast(zone_id)
                    updated_value = forecast.updated.isoformat()
                    if current_land.get(zone_id) == updated_value:
                        continue
                    self.producer.send_microsoft_open_data_us_noaa_nws_land_zone_forecast(
                        zone_id, forecast, flush_producer=False
                    )
                    pending.land_updates[zone_id] = updated_value
                    emitted += 1
                else:
                    forecast = self.fetch_marine_forecast(zone_id)
                    digest = self._marine_digest(forecast)
                    if current_marine.get(zone_id) == digest:
                        continue
                    self.producer.send_microsoft_open_data_us_noaa_nws_marine_zone_forecast(
                        zone_id, forecast, flush_producer=False
                    )
                    pending.marine_hashes[zone_id] = digest
                    emitted += 1
            except (requests.RequestException, ValueError, KeyError) as exc:
                LOGGER.error("Failed to process forecast slice %s: %s", zone_id, exc)

        remaining = self.kafka_client.flush(timeout=30)
        if remaining != 0:
            raise RuntimeError(f"Kafka flush left {remaining} forecast messages unsent.")

        if emitted > 0:
            self.save_state(
                {
                    "land_updates": pending.land_updates,
                    "marine_hashes": pending.marine_hashes,
                }
            )
        return emitted

    def run(self) -> None:
        LOGGER.info("Starting NWS forecast poller for zones: %s", ", ".join(self.zones))
        self.refresh_zone_cache()
        self.emit_reference_data()

        while True:
            now = time.time()
            if now - self._last_reference_refresh >= self.reference_refresh_seconds:
                self.refresh_zone_cache()
                self.emit_reference_data()

            emitted = self.poll_once()
            LOGGER.info("Completed forecast poll; emitted %s changed forecast snapshot(s).", emitted)
            time.sleep(self.poll_interval_seconds)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NWS forecast zone bridge")
    parser.add_argument("--zones", default=os.getenv("NWS_FORECAST_ZONES", DEFAULT_ZONES))
    parser.add_argument("--state-file", default=os.getenv("NWS_FORECAST_STATE_FILE", DEFAULT_STATE_FILE))
    parser.add_argument(
        "--poll-interval-seconds",
        type=int,
        default=int(os.getenv("NWS_FORECAST_POLL_INTERVAL_SECONDS", DEFAULT_POLL_INTERVAL_SECONDS)),
    )
    parser.add_argument(
        "--reference-refresh-seconds",
        type=int,
        default=int(os.getenv("NWS_FORECAST_REFERENCE_REFRESH_SECONDS", DEFAULT_REFERENCE_REFRESH_SECONDS)),
    )
    parser.add_argument("--connection-string", default=os.getenv("CONNECTION_STRING"))
    parser.add_argument("--kafka-bootstrap-servers", default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    parser.add_argument("--kafka-topic", default=os.getenv("KAFKA_TOPIC"))
    parser.add_argument("--sasl-username", default=os.getenv("SASL_USERNAME"))
    parser.add_argument("--sasl-password", default=os.getenv("SASL_PASSWORD"))
    parser.add_argument(
        "--kafka-enable-tls",
        default=os.getenv("KAFKA_ENABLE_TLS", "true").lower() != "false",
        type=lambda value: str(value).lower() != "false",
    )
    return parser


def main() -> None:
    logging.basicConfig(
        level=logging.INFO if sys.gettrace() is None else logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    args = build_argument_parser().parse_args()
    kafka_config, kafka_topic = build_kafka_config(args)
    poller = NWSForecastPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        zones=parse_zone_list(args.zones),
        state_file=args.state_file,
        poll_interval_seconds=args.poll_interval_seconds,
        reference_refresh_seconds=args.reference_refresh_seconds,
    )
    poller.run()


if __name__ == "__main__":
    main()
