"""Bridge LAQN London Air Quality Network data into Kafka as CloudEvents."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests
from confluent_kafka import Producer

from laqn_london_producer_data import DailyIndex, Measurement, Site, Species
from laqn_london_producer_kafka_producer.producer import (
    UkKclLaqnEventProducer,
    UkKclLaqnSpeciesEventProducer,
)

BASE_URL = "http://api.erg.ic.ac.uk/AirQuality/"
SITES_PATH = "Information/MonitoringSites/GroupName=All/Json"
SPECIES_PATH = "Information/Species/Json"
DAILY_INDEX_PATH = "Daily/MonitoringIndex/Latest/GroupName=London/Json"

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def _coerce_list(value: Any) -> List[Any]:
    """Normalize API fields that may be absent, singular, list, or whitespace."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [] if not value.strip() else [value]
    return [value]


def _format_api_date(day: date) -> str:
    """Format a date for the LAQN site data endpoint."""
    return day.strftime("%Y-%m-%d")


def _parse_float_or_none(value: Any) -> Optional[float]:
    """Parse an LAQN numeric string, treating blank values as missing."""
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return float(text)


def _load_state(state_file: str) -> Dict[str, Dict[str, bool]]:
    """Load persisted dedupe state from disk."""
    default_state: Dict[str, Dict[str, bool]] = {
        "measurements": {},
        "daily_index": {},
    }
    if not state_file or not os.path.exists(state_file):
        return default_state
    try:
        with open(state_file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:  # pylint: disable=broad-except
        logging.warning("Could not load state from %s: %s", state_file, exc)
        return default_state
    for key in default_state:
        value = data.get(key, {})
        default_state[key] = value if isinstance(value, dict) else {}
    return default_state


def _save_state(state_file: str, state: Dict[str, Dict[str, bool]]) -> None:
    """Persist dedupe state to disk."""
    if not state_file:
        return
    try:
        with open(state_file, "w", encoding="utf-8") as handle:
            json.dump(state, handle)
    except Exception as exc:  # pylint: disable=broad-except
        logging.warning("Could not save state to %s: %s", state_file, exc)


class LAQNLondonAPI:
    """Client and poller for the LAQN London Air Quality Network API."""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip("/") + "/"
        self.session = requests.Session()

    def _get_json(self, path: str) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}{path}", timeout=60)
        response.raise_for_status()
        return response.json()

    def list_sites(self) -> List[Dict[str, Any]]:
        """Fetch all monitoring sites."""
        payload = self._get_json(SITES_PATH)
        return _coerce_list(payload.get("Sites", {}).get("Site"))

    def list_species(self) -> List[Dict[str, Any]]:
        """Fetch the species catalog."""
        payload = self._get_json(SPECIES_PATH)
        return _coerce_list(payload.get("AirQualitySpecies", {}).get("Species"))

    def get_daily_index(self) -> Dict[str, Any]:
        """Fetch the latest London-wide Daily AQI bulletin."""
        return self._get_json(DAILY_INDEX_PATH)

    def get_site_measurements(self, site_code: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Fetch hourly site measurements for the requested date range."""
        payload = self._get_json(
            f"Data/Site/SiteCode={site_code}/StartDate={start_date}/EndDate={end_date}/Json"
        )
        return _coerce_list(payload.get("AirQualityData", {}).get("Data"))

    @staticmethod
    def parse_connection_string(connection_string: str) -> Dict[str, str]:
        """Parse Event Hubs/Fabric or plain BootstrapServer connection strings."""
        config_dict: Dict[str, str] = {}
        try:
            for part in connection_string.split(";"):
                if "Endpoint" in part:
                    config_dict["bootstrap.servers"] = (
                        part.split("=")[1].strip('"').strip().replace("sb://", "").replace("/", "") + ":9093"
                    )
                elif "EntityPath" in part:
                    config_dict["kafka_topic"] = part.split("=")[1].strip('"').strip()
                elif "SharedAccessKeyName" in part:
                    config_dict["sasl.username"] = "$ConnectionString"
                elif "SharedAccessKey" in part:
                    config_dict["sasl.password"] = connection_string.strip()
                elif "BootstrapServer" in part:
                    config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
        except IndexError as exc:
            raise ValueError("Invalid connection string format") from exc
        if "sasl.username" in config_dict:
            config_dict["security.protocol"] = "SASL_SSL"
            config_dict["sasl.mechanism"] = "PLAIN"
        return config_dict

    @staticmethod
    def is_active_site(site: Dict[str, Any]) -> bool:
        """Return whether the site is active based on the absence of DateClosed."""
        return not str(site.get("@DateClosed", "")).strip()

    @staticmethod
    def normalize_site(site: Dict[str, Any]) -> Site:
        """Normalize a raw site payload into the generated data class."""
        date_closed = str(site.get("@DateClosed", "")).strip() or None
        return Site(
            site_code=str(site.get("@SiteCode", "")).strip(),
            site_name=str(site.get("@SiteName", "")).strip(),
            site_type=str(site.get("@SiteType", "")).strip(),
            local_authority_code=str(site.get("@LocalAuthorityCode", "")).strip(),
            local_authority_name=str(site.get("@LocalAuthorityName", "")).strip(),
            latitude=_parse_float_or_none(site.get("@Latitude")),
            longitude=_parse_float_or_none(site.get("@Longitude")),
            date_opened=str(site.get("@DateOpened", "")).strip(),
            date_closed=date_closed,
            data_owner=str(site.get("@DataOwner", "")).strip(),
            data_manager=str(site.get("@DataManager", "")).strip(),
        )

    @staticmethod
    def normalize_species(species: Dict[str, Any]) -> Species:
        """Normalize a raw species payload into the generated data class."""
        return Species(
            species_code=str(species.get("@SpeciesCode", "")).strip(),
            species_name=str(species.get("@SpeciesName", "")).strip(),
            description=str(species.get("@Description", "")).strip(),
            health_effect=str(species.get("@HealthEffect", "")).strip(),
            link=str(species.get("@Link", "")).strip(),
        )

    @staticmethod
    def normalize_measurement(site_code: str, measurement: Dict[str, Any]) -> Optional[Measurement]:
        """Normalize a raw measurement payload. Blank values are skipped."""
        value = _parse_float_or_none(measurement.get("@Value"))
        if value is None:
            return None
        species_code = str(measurement.get("@SpeciesCode", "")).strip()
        measurement_date_gmt = str(measurement.get("@MeasurementDateGMT", "")).strip()
        if not species_code or not measurement_date_gmt:
            return None
        return Measurement(
            site_code=site_code,
            species_code=species_code,
            measurement_date_gmt=measurement_date_gmt,
            value=value,
        )

    @staticmethod
    def extract_daily_index_records(payload: Dict[str, Any]) -> List[DailyIndex]:
        """Flatten the nested Daily AQI response into event records."""
        records: List[DailyIndex] = []
        daily_index = payload.get("DailyAirQualityIndex", {})
        for local_authority in _coerce_list(daily_index.get("LocalAuthority")):
            if not isinstance(local_authority, dict):
                continue
            for site in _coerce_list(local_authority.get("Site")):
                if not isinstance(site, dict):
                    continue
                site_code = str(site.get("@SiteCode", "")).strip()
                bulletin_date = str(site.get("@BulletinDate", "")).strip()
                if not site_code or not bulletin_date:
                    continue
                species_entries = site.get("Species")
                if isinstance(species_entries, str):
                    if not species_entries.strip():
                        continue
                    logging.debug("Skipping non-structured species payload for site %s", site_code)
                    continue
                for species in _coerce_list(species_entries):
                    if not isinstance(species, dict):
                        continue
                    species_code = str(species.get("@SpeciesCode", "")).strip()
                    air_quality_index = str(species.get("@AirQualityIndex", "")).strip()
                    air_quality_band = str(species.get("@AirQualityBand", "")).strip()
                    index_source = str(species.get("@IndexSource", "")).strip()
                    if not species_code or not air_quality_index or not air_quality_band or not index_source:
                        continue
                    try:
                        records.append(
                            DailyIndex(
                                site_code=site_code,
                                bulletin_date=bulletin_date,
                                species_code=species_code,
                                air_quality_index=int(air_quality_index),
                                air_quality_band=air_quality_band,
                                index_source=index_source,
                            )
                        )
                    except ValueError:
                        logging.warning(
                            "Skipping Daily AQI record for site %s species %s with invalid index %s",
                            site_code,
                            species_code,
                            air_quality_index,
                        )
        return records

    @staticmethod
    def _flush_producer(*wrappers: Any) -> None:
        for wrapper in wrappers:
            producer = getattr(wrapper, "producer", None)
            if producer is not None:
                producer.flush()
                return

    def emit_reference_data(
        self,
        site_producer: UkKclLaqnEventProducer,
        species_producer: UkKclLaqnSpeciesEventProducer,
    ) -> List[str]:
        """Fetch and emit all reference records, returning active site codes."""
        active_site_codes: List[str] = []
        site_count = 0
        species_count = 0

        for raw_site in self.list_sites():
            site = self.normalize_site(raw_site)
            site_producer.send_uk_kcl_laqn_site(
                _site_code=site.site_code,
                data=site,
                flush_producer=False,
            )
            site_count += 1
            if self.is_active_site(raw_site):
                active_site_codes.append(site.site_code)

        for raw_species in self.list_species():
            species = self.normalize_species(raw_species)
            species_producer.send_uk_kcl_laqn_species(
                _species_code=species.species_code,
                data=species,
                flush_producer=False,
            )
            species_count += 1

        self._flush_producer(site_producer, species_producer)
        logging.info(
            "Emitted %s site reference events and %s species reference events; %s active sites",
            site_count,
            species_count,
            len(active_site_codes),
        )
        return active_site_codes

    def emit_measurements(
        self,
        site_codes: List[str],
        producer: UkKclLaqnEventProducer,
        measurement_state: Dict[str, bool],
        start_day: date,
        end_day: date,
    ) -> int:
        """Fetch and emit new hourly measurement events."""
        emitted = 0
        start_date = _format_api_date(start_day)
        end_date = _format_api_date(end_day)

        for site_code in site_codes:
            try:
                raw_measurements = self.get_site_measurements(site_code, start_date, end_date)
            except requests.RequestException as exc:
                logging.warning("Skipping measurements for site %s after upstream error: %s", site_code, exc)
                continue

            for raw_measurement in raw_measurements:
                measurement = self.normalize_measurement(site_code, raw_measurement)
                if measurement is None:
                    continue
                dedupe_key = (
                    f"{measurement.site_code}:{measurement.species_code}:{measurement.measurement_date_gmt}"
                )
                if dedupe_key in measurement_state:
                    continue
                producer.send_uk_kcl_laqn_measurement(
                    _site_code=measurement.site_code,
                    data=measurement,
                    flush_producer=False,
                )
                measurement_state[dedupe_key] = True
                emitted += 1

        if emitted:
            self._flush_producer(producer)
        return emitted

    def emit_daily_index(
        self,
        producer: UkKclLaqnEventProducer,
        daily_index_state: Dict[str, bool],
    ) -> int:
        """Fetch and emit new Daily AQI records."""
        emitted = 0
        for record in self.extract_daily_index_records(self.get_daily_index()):
            dedupe_key = f"{record.site_code}:{record.species_code}:{record.bulletin_date}"
            if dedupe_key in daily_index_state:
                continue
            producer.send_uk_kcl_laqn_daily_index(
                _site_code=record.site_code,
                data=record,
                flush_producer=False,
            )
            daily_index_state[dedupe_key] = True
            emitted += 1

        if emitted:
            self._flush_producer(producer)
        return emitted

    async def feed(
        self,
        kafka_config: Dict[str, str],
        kafka_topic: str,
        polling_interval: int,
        state_file: str = "",
        reference_refresh_polls: int = 24,
    ) -> None:
        """Emit reference data first and then poll telemetry forever."""
        state = _load_state(state_file)
        kafka_producer = Producer(kafka_config)
        site_event_producer = UkKclLaqnEventProducer(kafka_producer, kafka_topic)
        species_event_producer = UkKclLaqnSpeciesEventProducer(kafka_producer, kafka_topic)

        logging.info(
            "Starting LAQN feed for Kafka topic %s at bootstrap servers %s",
            kafka_topic,
            kafka_config["bootstrap.servers"],
        )

        active_site_codes = self.emit_reference_data(site_event_producer, species_event_producer)
        poll_count = 0

        while True:
            cycle_started = time.monotonic()
            try:
                if poll_count > 0 and poll_count % reference_refresh_polls == 0:
                    active_site_codes = self.emit_reference_data(site_event_producer, species_event_producer)

                today = datetime.now(timezone.utc).date()
                yesterday = today - timedelta(days=1)

                measurement_count = self.emit_measurements(
                    active_site_codes,
                    site_event_producer,
                    state["measurements"],
                    yesterday,
                    today,
                )
                daily_index_count = self.emit_daily_index(site_event_producer, state["daily_index"])

                kafka_producer.flush()
                _save_state(state_file, state)

                poll_count += 1
                elapsed = time.monotonic() - cycle_started
                wait_seconds = max(0.0, polling_interval - elapsed)
                logging.info(
                    "Poll %s emitted %s measurements and %s Daily AQI events in %.2f seconds; waiting %.2f seconds",
                    poll_count,
                    measurement_count,
                    daily_index_count,
                    elapsed,
                    wait_seconds,
                )
                if wait_seconds:
                    await asyncio.sleep(wait_seconds)
            except KeyboardInterrupt:
                logging.info("Stopping LAQN feed")
                break
            except Exception as exc:  # pylint: disable=broad-except
                logging.exception("Error in LAQN poll loop: %s", exc)
                _save_state(state_file, state)
                await asyncio.sleep(polling_interval)

        kafka_producer.flush()
        _save_state(state_file, state)


def main() -> None:
    """CLI entrypoint for the LAQN London bridge."""
    parser = argparse.ArgumentParser(
        description="Interact with the LAQN London Air Quality Network API."
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sites", help="List all monitoring sites")
    subparsers.add_parser("species", help="List all pollutant species")
    subparsers.add_parser("daily-index", help="Fetch the latest Daily AQI bulletin")

    feed_parser = subparsers.add_parser(
        "feed",
        help="Feed LAQN reference data and telemetry to Kafka as CloudEvents",
    )
    feed_parser.add_argument(
        "--kafka-bootstrap-servers",
        type=str,
        help="Comma separated list of Kafka bootstrap servers",
        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    )
    feed_parser.add_argument(
        "--kafka-topic",
        type=str,
        help="Kafka topic to send messages to",
        default=os.getenv("KAFKA_TOPIC"),
    )
    feed_parser.add_argument(
        "--sasl-username",
        type=str,
        help="Username for SASL PLAIN authentication",
        default=os.getenv("SASL_USERNAME"),
    )
    feed_parser.add_argument(
        "--sasl-password",
        type=str,
        help="Password for SASL PLAIN authentication",
        default=os.getenv("SASL_PASSWORD"),
    )
    feed_parser.add_argument(
        "-c",
        "--connection-string",
        type=str,
        help="Microsoft Event Hubs or Microsoft Fabric Event Stream connection string",
        default=os.getenv("CONNECTION_STRING"),
    )
    feed_parser.add_argument(
        "-i",
        "--polling-interval",
        type=int,
        help="Polling interval in seconds",
        default=int(os.getenv("POLLING_INTERVAL", "3600")),
    )
    feed_parser.add_argument(
        "--state-file",
        type=str,
        default=os.getenv("STATE_FILE", os.path.expanduser("~/.laqn_london_state.json")),
        help="Path to the persisted dedupe state file",
    )

    args = parser.parse_args()
    api = LAQNLondonAPI()

    if args.command == "sites":
        print(json.dumps(api.list_sites(), indent=2))
        return
    if args.command == "species":
        print(json.dumps(api.list_species(), indent=2))
        return
    if args.command == "daily-index":
        print(json.dumps(api.get_daily_index(), indent=2))
        return
    if args.command != "feed":
        parser.print_help()
        return

    if args.connection_string:
        config_params = api.parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = config_params.get("bootstrap.servers")
        kafka_topic = config_params.get("kafka_topic")
        sasl_username = config_params.get("sasl.username")
        sasl_password = config_params.get("sasl.password")
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not kafka_bootstrap_servers:
        print(
            "Error: Kafka bootstrap servers must be provided either through the command line or connection string."
        )
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided either through the command line or connection string.")
        sys.exit(1)

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config: Dict[str, str] = {
        "bootstrap.servers": kafka_bootstrap_servers,
    }
    if sasl_username and sasl_password:
        kafka_config.update(
            {
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_username,
                "sasl.password": sasl_password,
            }
        )
    elif tls_enabled:
        kafka_config["security.protocol"] = "SSL"

    asyncio.run(api.feed(kafka_config, kafka_topic, args.polling_interval, args.state_file))
