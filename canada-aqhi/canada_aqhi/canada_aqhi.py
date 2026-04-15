"""Canada AQHI bridge for Apache Kafka using CloudEvents."""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, Optional, Sequence

import requests
from confluent_kafka import Producer
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from canada_aqhi_producer_data.ca.gc.weather.aqhi.community import Community
from canada_aqhi_producer_data.ca.gc.weather.aqhi.forecast import Forecast
from canada_aqhi_producer_data.ca.gc.weather.aqhi.observation import Observation
from canada_aqhi_producer_kafka_producer.producer import CaGcWeatherAqhiEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger(__name__)

AQHI_BASE_URL = "https://dd.weather.gc.ca/today/air_quality/aqhi"
COMMUNITY_GEOJSON_URL = (
    "https://collaboration.cmc.ec.gc.ca/cmc/cmos/public_doc/msc-data/aqhi/aqhi_community.geojson"
)
STATION_GEOJSON_URL = (
    "https://collaboration.cmc.ec.gc.ca/cmc/cmos/public_doc/msc-data/aqhi/aqhi_station.geojson"
)
GEOLOCATOR_URL = "https://geolocator.api.geo.ca/"
PROVINCES = ["AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT"]
AQHI_REGION_TO_PROVINCES = {
    "atl": frozenset({"NB", "NL", "NS", "PE"}),
    "ont": frozenset({"ON"}),
    "pnr": frozenset({"AB", "MB", "NT", "NU", "SK"}),
    "pyr": frozenset({"BC", "YT"}),
}
PROVINCE_NAME_TO_CODE = {
    "Alberta": "AB",
    "British Columbia": "BC",
    "Manitoba": "MB",
    "New Brunswick": "NB",
    "Newfoundland and Labrador": "NL",
    "Nova Scotia": "NS",
    "Northwest Territories": "NT",
    "Nunavut": "NU",
    "Ontario": "ON",
    "Prince Edward Island": "PE",
    "Quebec": "QC",
    "Saskatchewan": "SK",
    "Yukon": "YT",
}
FORECAST_LABELS = {
    1: "Today",
    2: "Tonight",
    3: "Tomorrow",
    4: "Tomorrow Night",
}
DEFAULT_REFERENCE_REFRESH_INTERVAL = 24 * 60 * 60
DEFAULT_MAX_COMMUNITIES = 0
MAX_OBSERVATION_IDS = 50000
MAX_FORECAST_IDS = 20000
DEFAULT_HTTP_RETRY_TOTAL = 3


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse Event Hubs/Fabric or plain Kafka connection strings."""
    config: Dict[str, str] = {}
    try:
        for raw_part in connection_string.split(";"):
            part = raw_part.strip()
            if not part:
                continue
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"')
            if key == "Endpoint":
                config["bootstrap.servers"] = value.replace("sb://", "").rstrip("/") + ":9093"
            elif key == "EntityPath":
                config["kafka_topic"] = value
            elif key == "SharedAccessKeyName":
                config["sasl.username"] = "$ConnectionString"
            elif key == "SharedAccessKey":
                config["sasl.password"] = connection_string.strip()
            elif key == "BootstrapServer":
                config["bootstrap.servers"] = value
    except ValueError as exc:
        raise ValueError("Invalid connection string format") from exc

    if "sasl.username" in config:
        config["security.protocol"] = "SASL_SSL"
        config["sasl.mechanism"] = "PLAIN"
    return config


def aqhi_category(aqhi_val: Optional[float]) -> str:
    """Map AQHI values to the public health-risk categories."""
    if aqhi_val is None:
        return "Unknown"
    if aqhi_val <= 3:
        return "Low"
    if aqhi_val <= 6:
        return "Moderate"
    if aqhi_val <= 10:
        return "High"
    return "Very High"


def normalize_provinces(provinces: str | Sequence[str]) -> list[str]:
    """Normalize a comma-separated province list."""
    if isinstance(provinces, str):
        values = [value.strip().upper() for value in provinces.split(",") if value.strip()]
    else:
        values = [value.strip().upper() for value in provinces if value.strip()]
    invalid = sorted(set(value for value in values if value not in PROVINCES))
    if invalid:
        raise ValueError(f"Unsupported provinces: {', '.join(invalid)}")
    return sorted(dict.fromkeys(values)) or PROVINCES.copy()


def forecast_date_for_period(publication_datetime: datetime, forecast_period: int) -> str:
    """Derive the YYYYMMDD date for the public forecast period."""
    if forecast_period not in FORECAST_LABELS:
        raise ValueError(f"Unsupported forecast period: {forecast_period}")
    base_date = publication_datetime.date()
    if forecast_period in (1, 2):
        return base_date.strftime("%Y%m%d")
    return (base_date + timedelta(days=1)).strftime("%Y%m%d")


def parse_utcstamp(text: str) -> datetime:
    """Parse AQHI UTCStamp values."""
    clean = text.strip()
    if len(clean) == 12:
        return datetime.strptime(clean, "%Y%m%d%H%M").replace(tzinfo=timezone.utc)
    if len(clean) == 14:
        return datetime.strptime(clean, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    raise ValueError(f"Unsupported UTCStamp format: {text}")


def province_candidates_for_feed(feed_url: str | None) -> frozenset[str]:
    """Infer candidate provinces from the AQHI feed partition path."""
    if not feed_url or "/aqhi/" not in feed_url:
        return frozenset()
    region = feed_url.split("/aqhi/", 1)[1].split("/", 1)[0]
    return AQHI_REGION_TO_PROVINCES.get(region, frozenset())


def canonicalize_feed_url(feed_url: str | None) -> str | None:
    """Rewrite catalog feed URLs onto the live HTTPS AQHI base."""
    if not feed_url or "/aqhi/" not in feed_url:
        return feed_url
    suffix = feed_url.split("/aqhi/", 1)[1]
    return f"{AQHI_BASE_URL}/{suffix}"


def create_retrying_session() -> requests.Session:
    """Create an HTTP session with bounded retries for transient upstream failures."""
    session = requests.Session()
    session.headers.update({"User-Agent": "GitHub-Copilot-CLI/1.0"})
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
    try:
        with open(state_file, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Could not save state to %s: %s", state_file, exc)


class CanadaAQHIBridge:
    """Bridge that polls AQHI reference, observation, and forecast feeds."""

    def __init__(self, state_file: str = ""):
        self.state_file = state_file
        self.session = create_retrying_session()
        state = _load_state(state_file)
        self.province_cache: dict[str, str] = dict(state.get("province_cache", {}))
        observation_ids = state.get("observation_ids", [])
        forecast_ids = state.get("forecast_ids", [])
        self._observation_order = [str(value) for value in observation_ids][-MAX_OBSERVATION_IDS:]
        self._forecast_order = [str(value) for value in forecast_ids][-MAX_FORECAST_IDS:]
        self.seen_observations = set(self._observation_order)
        self.seen_forecasts = set(self._forecast_order)
        last_reference_refresh = state.get("last_reference_refresh")
        self.last_reference_refresh = (
            datetime.fromisoformat(last_reference_refresh) if last_reference_refresh else None
        )
        self.communities: dict[str, dict[str, Any]] = {}

    def save_state(self) -> None:
        _save_state(
            self.state_file,
            {
                "province_cache": self.province_cache,
                "observation_ids": self._observation_order[-MAX_OBSERVATION_IDS:],
                "forecast_ids": self._forecast_order[-MAX_FORECAST_IDS:],
                "last_reference_refresh": self.last_reference_refresh.isoformat()
                if self.last_reference_refresh
                else None,
            },
        )

    @staticmethod
    def _distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

    def fetch_json(self, url: str, **kwargs: Any) -> Any:
        response = self.session.get(url, timeout=60, **kwargs)
        response.raise_for_status()
        return response.json()

    def fetch_text(self, url: str) -> Optional[str]:
        try:
            response = self.session.get(url, timeout=60)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.text
        except Exception as exc:  # pylint: disable=broad-except
            LOGGER.warning("Failed to fetch %s: %s", url, exc)
            return None

    def resolve_province_code(self, cgndb_code: str, latitude: float, longitude: float) -> Optional[str]:
        """Resolve a CGNDB community to a province/territory code using NRCan geolocation."""
        if cgndb_code in self.province_cache:
            return self.province_cache[cgndb_code]

        try:
            results = self.fetch_json(
                GEOLOCATOR_URL,
                params={"q": f"{latitude},{longitude}", "lang": "en"},
            )
        except Exception as exc:  # pylint: disable=broad-except
            LOGGER.warning("Failed to resolve province for %s: %s", cgndb_code, exc)
            return None

        best_match: tuple[float, str] | None = None
        for result in results:
            province_name = result.get("province")
            if province_name not in PROVINCE_NAME_TO_CODE:
                continue
            result_lat = result.get("lat")
            result_lon = result.get("lng")
            if result_lat is None or result_lon is None:
                continue
            distance = self._distance(latitude, longitude, float(result_lat), float(result_lon))
            province_code = PROVINCE_NAME_TO_CODE[province_name]
            if best_match is None or distance < best_match[0]:
                best_match = (distance, province_code)

        if best_match:
            self.province_cache[cgndb_code] = best_match[1]
            return best_match[1]

        LOGGER.warning("No province match found for %s", cgndb_code)
        return None

    @staticmethod
    def merge_community_catalogs(
        community_geojson: dict[str, Any],
        station_geojson: dict[str, Any],
    ) -> dict[str, dict[str, Any]]:
        """Merge AQHI community coordinates with station feed metadata."""
        merged: dict[str, dict[str, Any]] = {}
        for feature in community_geojson.get("features", []):
            properties = feature.get("properties", {})
            cgndb_code = properties.get("cgndb_key")
            if not cgndb_code:
                continue
            merged[cgndb_code] = {
                "cgndb_code": cgndb_code,
                "community_name": properties.get("region_name_en") or properties.get("region_name_fr") or cgndb_code,
                "latitude": float(properties.get("Latitude", 0.0)),
                "longitude": float(properties.get("Longitude", 0.0)),
                "observation_url": None,
                "forecast_url": None,
            }

        for feature in station_geojson.get("features", []):
            properties = feature.get("properties", {})
            cgndb_code = properties.get("cgndb")
            if not cgndb_code:
                continue
            entry = merged.setdefault(
                cgndb_code,
                {
                    "cgndb_code": cgndb_code,
                    "community_name": properties.get("name", {}).get("en")
                    or properties.get("name", {}).get("fr")
                    or cgndb_code,
                    "latitude": 0.0,
                    "longitude": 0.0,
                    "observation_url": None,
                    "forecast_url": None,
                },
            )
            name_info = properties.get("name", {})
            if isinstance(name_info, dict):
                entry["community_name"] = name_info.get("en") or name_info.get("fr") or entry["community_name"]
            entry["observation_url"] = canonicalize_feed_url(properties.get("path_to_current_observation"))
            entry["forecast_url"] = canonicalize_feed_url(properties.get("path_to_current_forecast"))
        return merged

    def load_reference_catalogs(self, selected_provinces: set[str]) -> dict[str, dict[str, Any]]:
        """Load and enrich AQHI community metadata."""
        community_geojson = self.fetch_json(COMMUNITY_GEOJSON_URL)
        station_geojson = self.fetch_json(STATION_GEOJSON_URL)
        communities = self.merge_community_catalogs(community_geojson, station_geojson)
        filtered: dict[str, dict[str, Any]] = {}

        for cgndb_code, entry in communities.items():
            province = self.province_cache.get(cgndb_code)
            candidate_provinces = (
                province_candidates_for_feed(entry.get("observation_url"))
                or province_candidates_for_feed(entry.get("forecast_url"))
            )
            if not province and len(candidate_provinces) == 1:
                province = next(iter(candidate_provinces))
                self.province_cache[cgndb_code] = province
            if not province and candidate_provinces and candidate_provinces.isdisjoint(selected_provinces):
                continue
            if not province:
                province = self.resolve_province_code(
                    cgndb_code,
                    float(entry.get("latitude", 0.0)),
                    float(entry.get("longitude", 0.0)),
                )
            if not province or province not in selected_provinces:
                continue
            entry["province"] = province
            filtered[cgndb_code] = entry

        self.communities = filtered
        return filtered

    @staticmethod
    def parse_observation_xml(xml_text: str) -> dict[str, Any]:
        """Parse a current AQHI observation XML payload."""
        root = ET.fromstring(xml_text)
        region_node = root.find("region")
        region = ""
        if region_node is not None:
            region = (region_node.attrib.get("nameEn") or region_node.text or "").strip()
        observed_at = parse_utcstamp(root.find("dateStamp/UTCStamp").text or "")
        aqhi_text = root.findtext("airQualityHealthIndex", default="").strip()
        aqhi_value = float(aqhi_text) if aqhi_text else None
        return {
            "community_name": region,
            "observation_datetime": observed_at.isoformat().replace("+00:00", "Z"),
            "aqhi": aqhi_value,
            "aqhi_category": aqhi_category(aqhi_value),
        }

    @staticmethod
    def parse_forecast_xml(xml_text: str) -> dict[str, Any]:
        """Parse the AQHI public-forecast XML payload."""
        root = ET.fromstring(xml_text)
        publication_datetime = parse_utcstamp(root.find("dateStamp/UTCStamp").text or "")
        region_node = root.find("region")
        region = ""
        if region_node is not None:
            region = (region_node.attrib.get("nameEn") or region_node.text or "").strip()
        status = root.attrib.get("status", "issued")
        periods: list[dict[str, Any]] = []

        for forecast_node in root.findall("forecastGroup/forecast"):
            period_id = int(forecast_node.attrib["periodID"])
            label = FORECAST_LABELS.get(period_id)
            if label is None:
                LOGGER.warning("Skipping unsupported AQHI forecast periodID=%s", period_id)
                continue
            aqhi_text = forecast_node.findtext("airQualityHealthIndex", default="").strip()
            aqhi_value = int(aqhi_text) if aqhi_text else None
            periods.append(
                {
                    "forecast_period": period_id,
                    "forecast_period_label": label,
                    "forecast_date": forecast_date_for_period(publication_datetime, period_id),
                    "aqhi": aqhi_value,
                    "aqhi_category": aqhi_category(aqhi_value),
                }
            )

        return {
            "community_name": region,
            "publication_datetime": publication_datetime.isoformat().replace("+00:00", "Z"),
            "status": status,
            "periods": periods,
        }

    def _remember_observation(self, observation_id: str) -> None:
        if observation_id in self.seen_observations:
            return
        self.seen_observations.add(observation_id)
        self._observation_order.append(observation_id)
        if len(self._observation_order) > MAX_OBSERVATION_IDS:
            removed = self._observation_order.pop(0)
            self.seen_observations.discard(removed)

    def _remember_forecast(self, forecast_id: str) -> None:
        if forecast_id in self.seen_forecasts:
            return
        self.seen_forecasts.add(forecast_id)
        self._forecast_order.append(forecast_id)
        if len(self._forecast_order) > MAX_FORECAST_IDS:
            removed = self._forecast_order.pop(0)
            self.seen_forecasts.discard(removed)

    def emit_reference_data(
        self,
        producer: CaGcWeatherAqhiEventProducer,
        communities: dict[str, dict[str, Any]],
    ) -> int:
        sent = 0
        for entry in sorted(communities.values(), key=lambda value: (value["province"], value["community_name"])):
            producer.send_ca_gc_weather_aqhi_community(
                _province=entry["province"],
                _community_name=entry["community_name"],
                data=Community(
                    province=entry["province"],
                    community_name=entry["community_name"],
                    cgndb_code=entry["cgndb_code"],
                    latitude=float(entry["latitude"]),
                    longitude=float(entry["longitude"]),
                    observation_url=entry.get("observation_url"),
                    forecast_url=entry.get("forecast_url"),
                ),
                flush_producer=False,
            )
            sent += 1
        producer.producer.flush()
        self.last_reference_refresh = datetime.now(timezone.utc)
        return sent

    def emit_observations(
        self,
        producer: CaGcWeatherAqhiEventProducer,
        communities: Iterable[dict[str, Any]],
    ) -> int:
        sent = 0
        for entry in communities:
            observation_url = entry.get("observation_url")
            if not observation_url:
                continue
            xml_text = self.fetch_text(observation_url)
            if not xml_text:
                continue
            parsed = self.parse_observation_xml(xml_text)
            observation_id = f"{entry['province']}|{entry['community_name']}|{parsed['observation_datetime']}"
            if observation_id in self.seen_observations:
                continue
            producer.send_ca_gc_weather_aqhi_observation(
                _province=entry["province"],
                _community_name=entry["community_name"],
                data=Observation(
                    province=entry["province"],
                    community_name=entry["community_name"],
                    cgndb_code=entry["cgndb_code"],
                    observation_datetime=parsed["observation_datetime"],
                    aqhi=parsed["aqhi"],
                    aqhi_category=parsed["aqhi_category"],
                ),
                flush_producer=False,
            )
            self._remember_observation(observation_id)
            sent += 1
        producer.producer.flush()
        return sent

    def emit_forecasts(
        self,
        producer: CaGcWeatherAqhiEventProducer,
        communities: Iterable[dict[str, Any]],
    ) -> int:
        sent = 0
        for entry in communities:
            forecast_url = entry.get("forecast_url")
            if not forecast_url:
                continue
            xml_text = self.fetch_text(forecast_url)
            if not xml_text:
                continue
            parsed = self.parse_forecast_xml(xml_text)
            for period in parsed["periods"]:
                forecast_id = (
                    f"{entry['province']}|{entry['community_name']}|"
                    f"{parsed['publication_datetime']}|{period['forecast_period']}"
                )
                if forecast_id in self.seen_forecasts:
                    continue
                producer.send_ca_gc_weather_aqhi_forecast(
                    _province=entry["province"],
                    _community_name=entry["community_name"],
                    data=Forecast(
                        province=entry["province"],
                        community_name=entry["community_name"],
                        cgndb_code=entry["cgndb_code"],
                        publication_datetime=parsed["publication_datetime"],
                        forecast_date=period["forecast_date"],
                        forecast_period=period["forecast_period"],
                        forecast_period_label=period["forecast_period_label"],
                        aqhi=period["aqhi"],
                        aqhi_category=period["aqhi_category"],
                    ),
                    flush_producer=False,
                )
                self._remember_forecast(forecast_id)
                sent += 1
        producer.producer.flush()
        return sent

    @staticmethod
    def limit_communities(
        communities: dict[str, dict[str, Any]],
        max_communities: int = DEFAULT_MAX_COMMUNITIES,
    ) -> dict[str, dict[str, Any]]:
        """Return a stable subset of communities when an opt-in cap is configured."""
        if max_communities <= 0 or len(communities) <= max_communities:
            return communities

        ordered_keys = sorted(
            communities,
            key=lambda key: (communities[key]["province"], communities[key]["community_name"]),
        )
        return {key: communities[key] for key in ordered_keys[:max_communities]}

    def poll_once(
        self,
        producer: CaGcWeatherAqhiEventProducer,
        selected_provinces: set[str],
        reference_refresh_interval: int = DEFAULT_REFERENCE_REFRESH_INTERVAL,
        max_communities: int = DEFAULT_MAX_COMMUNITIES,
    ) -> dict[str, int]:
        """Run one reference/observation/forecast cycle."""
        now = datetime.now(timezone.utc)
        communities = self.communities
        needs_reference_refresh = (
            not communities
            or not self.last_reference_refresh
            or (now - self.last_reference_refresh).total_seconds() >= reference_refresh_interval
        )

        reference_count = 0
        if needs_reference_refresh:
            try:
                communities = self.load_reference_catalogs(selected_provinces)
                communities = self.limit_communities(communities, max_communities=max_communities)
                self.communities = communities
                reference_count = self.emit_reference_data(producer, communities)
            except requests.RequestException as exc:
                if communities:
                    LOGGER.warning("Community refresh failed; continuing with cached metadata: %s", exc)
                else:
                    raise
        else:
            communities = self.limit_communities(communities, max_communities=max_communities)

        ordered_communities = [communities[key] for key in sorted(communities)]
        observation_count = self.emit_observations(producer, ordered_communities)
        forecast_count = self.emit_forecasts(producer, ordered_communities)
        self.save_state()
        return {
            "communities": reference_count,
            "observations": observation_count,
            "forecasts": forecast_count,
        }


def build_kafka_config(args: argparse.Namespace) -> tuple[dict[str, str], str]:
    """Build confluent-kafka config and resolve the target topic."""
    kafka_config: dict[str, str] = {}
    topic = args.kafka_topic

    if args.connection_string:
        kafka_config = parse_connection_string(args.connection_string)
        topic = topic or kafka_config.pop("kafka_topic", None)
    else:
        bootstrap_servers = args.kafka_bootstrap_servers or os.getenv("KAFKA_BROKER")
        if not bootstrap_servers:
            raise ValueError("Kafka bootstrap servers or a connection string are required.")
        kafka_config["bootstrap.servers"] = bootstrap_servers
        if args.sasl_username:
            kafka_config["sasl.username"] = args.sasl_username
        if args.sasl_password:
            kafka_config["sasl.password"] = args.sasl_password

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    if "sasl.username" in kafka_config:
        kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
        kafka_config["sasl.mechanism"] = "PLAIN"
    elif tls_enabled:
        kafka_config["security.protocol"] = "SSL"
    else:
        kafka_config["security.protocol"] = "PLAINTEXT"

    kafka_config["client.id"] = "canada-aqhi-bridge"
    return kafka_config, topic or "canada-aqhi"


def create_argument_parser() -> argparse.ArgumentParser:
    """Create the CLI parser."""
    parser = argparse.ArgumentParser(description="Canada AQHI bridge to Kafka/CloudEvents")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Poll AQHI data and send CloudEvents to Kafka")
    feed_parser.add_argument(
        "--connection-string",
        "-c",
        type=str,
        default=os.getenv("CONNECTION_STRING"),
        help="Event Hubs or Fabric Eventstream connection string",
    )
    feed_parser.add_argument(
        "--kafka-bootstrap-servers",
        type=str,
        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        help="Comma-separated Kafka bootstrap servers",
    )
    feed_parser.add_argument(
        "--kafka-topic",
        type=str,
        default=os.getenv("KAFKA_TOPIC"),
        help="Kafka topic override",
    )
    feed_parser.add_argument(
        "--sasl-username",
        type=str,
        default=os.getenv("SASL_USERNAME"),
        help="Kafka SASL username",
    )
    feed_parser.add_argument(
        "--sasl-password",
        type=str,
        default=os.getenv("SASL_PASSWORD"),
        help="Kafka SASL password",
    )
    feed_parser.add_argument(
        "--polling-interval",
        "-i",
        type=int,
        default=int(os.getenv("POLLING_INTERVAL", "3600")),
        help="Polling interval in seconds",
    )
    feed_parser.add_argument(
        "--reference-refresh-interval",
        type=int,
        default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", str(DEFAULT_REFERENCE_REFRESH_INTERVAL))),
        help="Reference refresh interval in seconds",
    )
    feed_parser.add_argument(
        "--max-communities",
        type=int,
        default=int(os.getenv("MAX_COMMUNITIES", str(DEFAULT_MAX_COMMUNITIES))),
        help="Optional cap on emitted communities; 0 disables the limit",
    )
    feed_parser.add_argument(
        "--state-file",
        type=str,
        default=os.getenv("STATE_FILE", os.path.expanduser("~/.canada_aqhi_state.json")),
        help="JSON file for dedupe and province cache state",
    )
    feed_parser.add_argument(
        "--provinces",
        type=str,
        default=os.getenv("PROVINCES", ",".join(PROVINCES)),
        help="Comma-separated province/territory codes to emit",
    )

    list_parser = subparsers.add_parser("list", help="List AQHI communities known to the bridge")
    list_parser.add_argument(
        "--provinces",
        type=str,
        default=os.getenv("PROVINCES", ",".join(PROVINCES)),
        help="Comma-separated province/territory codes to list",
    )
    list_parser.add_argument(
        "--state-file",
        type=str,
        default=os.getenv("STATE_FILE", os.path.expanduser("~/.canada_aqhi_state.json")),
        help="JSON file for dedupe and province cache state",
    )
    return parser


def main() -> None:
    """CLI entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()

    if args.command not in {"feed", "list"}:
        parser.print_help()
        return

    selected_provinces = set(normalize_provinces(args.provinces))
    bridge = CanadaAQHIBridge(state_file=args.state_file)

    if args.command == "list":
        communities = bridge.load_reference_catalogs(selected_provinces)
        for community in sorted(communities.values(), key=lambda value: (value["province"], value["community_name"])):
            print(f"{community['province']},{community['community_name']},{community['cgndb_code']}")
        bridge.save_state()
        return

    kafka_config, kafka_topic = build_kafka_config(args)
    producer = Producer(kafka_config)
    aqhi_producer = CaGcWeatherAqhiEventProducer(producer, kafka_topic)

    LOGGER.info(
        "Starting Canada AQHI bridge for provinces %s, polling every %d seconds",
        ",".join(sorted(selected_provinces)),
        args.polling_interval,
    )
    while True:
        try:
            counts = bridge.poll_once(
                aqhi_producer,
                selected_provinces,
                reference_refresh_interval=args.reference_refresh_interval,
                max_communities=args.max_communities,
            )
            LOGGER.info(
                "Sent %d community, %d observation, and %d forecast events",
                counts["communities"],
                counts["observations"],
                counts["forecasts"],
            )
        except KeyboardInterrupt:
            LOGGER.info("Exiting Canada AQHI bridge")
            break
        except Exception as exc:  # pylint: disable=broad-except
            LOGGER.error("Error during AQHI poll cycle: %s", exc)
        time.sleep(args.polling_interval)

    producer.flush()


if __name__ == "__main__":
    main()
