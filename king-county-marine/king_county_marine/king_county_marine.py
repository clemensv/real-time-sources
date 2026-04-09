"""King County marine bridge."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import time
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

import requests
from confluent_kafka import Producer
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from king_county_marine_producer_data import Station, WaterQualityReading
from king_county_marine_producer_kafka_producer.producer import USWAKingCountyMarineEventProducer

LOGGER = logging.getLogger(__name__)

CATALOG_URL = "https://api.us.socrata.com/api/catalog/v1?search_context=data.kingcounty.gov&q=buoy&limit=50"
VIEW_URL = "https://data.kingcounty.gov/api/views/{dataset_id}"
ROWS_URL = "https://data.kingcounty.gov/resource/{dataset_id}.json"
DEFAULT_POLL_INTERVAL_SECONDS = 900
REFERENCE_REFRESH_SECONDS = 86400
MAX_SEEN_IDS = 50000
PST_FIXED = timezone(timedelta(hours=-8))
HTTP_TIMEOUT = (15, 60)
HTTP_RETRY_STATUS_CODES = (429, 500, 502, 503, 504)
HTTP_RETRY_TOTAL = 5
HTTP_RETRY_BACKOFF_FACTOR = 2.0


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse Event Hubs/Fabric or plain Kafka connection strings."""
    config_dict: Dict[str, str] = {}
    if not connection_string:
        return config_dict
    try:
        for part in connection_string.split(";"):
            if "=" not in part:
                continue
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"')
            if key == "Endpoint":
                config_dict["bootstrap.servers"] = value.replace("sb://", "").rstrip("/") + ":9093"
            elif key == "EntityPath":
                config_dict["kafka_topic"] = value
            elif key == "SharedAccessKeyName":
                config_dict["sasl.username"] = "$ConnectionString"
            elif key == "SharedAccessKey":
                config_dict["sasl.password"] = connection_string.strip()
            elif key == "BootstrapServer":
                config_dict["bootstrap.servers"] = value
    except ValueError as exc:
        raise ValueError("Invalid connection string format") from exc
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


def slugify(text: str) -> str:
    """Convert a label into a stable slug."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _load_state(state_file: str) -> dict:
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as handle:
                return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
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


def parse_float(value: object) -> Optional[float]:
    """Parse a numeric field while suppressing NA/sentinel values."""
    if value in (None, "", "NA", "NaN"):
        return None
    number = float(value)
    if number <= -99.99:
        return None
    return number


def parse_station_location(description: str) -> tuple[Optional[float], Optional[float]]:
    """Extract latitude and longitude from dataset description text."""
    match = re.search(r"Latitude\s+([-0-9.]+)\s+and\s+Longitude\s+([-0-9.]+)", description or "")
    if not match:
        return None, None
    return float(match.group(1)), float(match.group(2))


def infer_station_id(name: str) -> str:
    """Derive a stable station identifier from the dataset name."""
    normalized = name.replace("Raw Data Output", "")
    normalized = normalized.replace("(Dec 20, 2023 - present)", "")
    normalized = normalized.replace("- Surface", " Surface")
    normalized = normalized.replace("- Bottom", " Bottom")
    return slugify(normalized)


def infer_sensor_level(name: str) -> str:
    """Infer the sensor level from the dataset name."""
    lowered = name.lower()
    if "surface" in lowered:
        return "surface"
    if "bottom" in lowered:
        return "bottom"
    if "wharf" in lowered or "mooring" in lowered:
        return "water-column"
    return "surface"


def create_retrying_session() -> requests.Session:
    """Create an HTTP session with retry policy for transient upstream failures."""
    session = requests.Session()
    retry = Retry(
        total=HTTP_RETRY_TOTAL,
        connect=HTTP_RETRY_TOTAL,
        read=HTTP_RETRY_TOTAL,
        status=HTTP_RETRY_TOTAL,
        backoff_factor=HTTP_RETRY_BACKOFF_FACTOR,
        allowed_methods=frozenset({"GET", "HEAD", "OPTIONS"}),
        status_forcelist=HTTP_RETRY_STATUS_CODES,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({"User-Agent": "GitHub-Copilot-CLI/1.0"})
    return session


def is_current_buoy_dataset(item: dict) -> bool:
    """Filter catalog search results down to active raw buoy/mooring datasets."""
    resource = item.get("resource", {})
    name = resource.get("name", "")
    if "Raw Data Output" not in name and "Mooring Raw Data Output" not in name:
        return False
    if "(Feb 3, 2022 - Dec 20, 2023)" in name:
        return False
    return resource.get("type") == "dataset"


def parse_observation_time(record: dict) -> str:
    """Normalize upstream timestamps to UTC ISO strings."""
    unix_ts = record.get("unixtimestamp")
    if unix_ts not in (None, ""):
        dt = datetime.fromtimestamp(int(unix_ts) / 1000, tz=timezone.utc)
        return dt.isoformat().replace("+00:00", "Z")
    dt_text = record.get("datetime")
    if dt_text:
        dt = datetime.fromisoformat(dt_text).replace(tzinfo=PST_FIXED).astimezone(timezone.utc)
        return dt.isoformat().replace("+00:00", "Z")
    date_text = record.get("date_america_los_angeles")
    time_text = record.get("time_america_los_angeles")
    if date_text and time_text:
        dt = datetime.fromisoformat(f"{date_text}T{time_text}").replace(tzinfo=PST_FIXED).astimezone(timezone.utc)
        return dt.isoformat().replace("+00:00", "Z")
    raise ValueError("Could not determine observation time")


class KingCountyMarineBridge:
    """Discover and poll current King County buoy datasets."""

    def __init__(self, state_file: str = ""):
        self.state_file = state_file
        self.session = create_retrying_session()
        state = _load_state(state_file)
        seen_ids = [str(value) for value in state.get("seen_reading_ids", [])][-MAX_SEEN_IDS:]
        self.seen_reading_ids = set(seen_ids)
        self.seen_reading_order = seen_ids
        self.last_reference_refresh = state.get("last_reference_refresh")
        self.station_metadata: "OrderedDict[str, dict]" = OrderedDict()

    def save_state(self) -> None:
        _save_state(
            self.state_file,
            {
                "seen_reading_ids": self.seen_reading_order[-MAX_SEEN_IDS:],
                "last_reference_refresh": self.last_reference_refresh,
            },
        )

    def _remember(self, reading_id: str) -> None:
        if reading_id in self.seen_reading_ids:
            return
        self.seen_reading_ids.add(reading_id)
        self.seen_reading_order.append(reading_id)
        if len(self.seen_reading_order) > MAX_SEEN_IDS:
            removed = self.seen_reading_order.pop(0)
            self.seen_reading_ids.discard(removed)

    def discover_datasets(self) -> List[dict]:
        """Discover active King County raw buoy datasets from the Socrata catalog."""
        response = self.session.get(CATALOG_URL, timeout=HTTP_TIMEOUT)
        response.raise_for_status()
        payload = response.json()
        datasets = []
        for item in payload.get("results", []):
            if not is_current_buoy_dataset(item):
                continue
            datasets.append(item["resource"])
        return datasets

    def fetch_view(self, dataset_id: str) -> dict:
        """Fetch Socrata view metadata for one dataset."""
        response = self.session.get(VIEW_URL.format(dataset_id=dataset_id), timeout=HTTP_TIMEOUT)
        response.raise_for_status()
        return response.json()

    def build_station(self, view: dict) -> Station:
        """Build station reference metadata from a Socrata view."""
        latitude, longitude = parse_station_location(view.get("description", ""))
        station_name = view.get("name", "")
        station_id = infer_station_id(station_name)
        dataset_id = view["id"]
        dataset_url = f"https://data.kingcounty.gov/d/{dataset_id}"
        sensor_level = infer_sensor_level(station_name)
        return Station(
            station_id=station_id,
            station_name=station_name,
            dataset_id=dataset_id,
            dataset_name=station_name,
            dataset_url=dataset_url,
            sensor_level=sensor_level,
            latitude=latitude,
            longitude=longitude,
        )

    def fetch_rows(self, dataset_id: str, limit: int = 200) -> List[dict]:
        """Fetch the latest rows for one dataset."""
        params = {"$limit": limit}
        if dataset_id == "fkix-9yyf":
            params["$order"] = "datetime DESC"
        else:
            params["$order"] = "unixtimestamp DESC"
        response = self.session.get(ROWS_URL.format(dataset_id=dataset_id), params=params, timeout=HTTP_TIMEOUT)
        response.raise_for_status()
        return response.json()

    def build_reading(self, dataset_id: str, row: dict) -> WaterQualityReading:
        """Normalize one upstream row into the generated reading class."""
        meta = self.station_metadata[dataset_id]
        return WaterQualityReading(
            station_id=meta["station_id"],
            station_name=meta["station_name"],
            observation_time=parse_observation_time(row),
            water_temperature_c=parse_float(row.get("water_temp_c", row.get("hcep_temp", row.get("temperature_c")))),
            conductivity_s_m=parse_float(row.get("cond_sm", row.get("hcep_cond", row.get("conductivity_sm")))),
            pressure_dbar=parse_float(row.get("pres_db", row.get("hcep_pres", row.get("pressure_dbar")))),
            dissolved_oxygen_mg_l=parse_float(row.get("do_mgl", row.get("hcep_oxy", row.get("oxygen_mgl")))),
            ph=parse_float(row.get("sonde_ph", row.get("hcep_ph", row.get("ph")))),
            chlorophyll_ug_l=parse_float(row.get("chl_fluor_ugl", row.get("hcep_fl", row.get("chlorophyll_ugl")))),
            turbidity_ntu=parse_float(row.get("turb_ntu", row.get("hcep_turb", row.get("turbidity_ntu")))),
            chlorophyll_stddev_ug_l=parse_float(row.get("std_dev_chl_fluor", row.get("hcep_fsd", row.get("chlorophyll_sd_ugl")))),
            turbidity_stddev_ntu=parse_float(row.get("std_dev_turb", row.get("hcep_tsd", row.get("turbidity_sd_ugl")))),
            salinity_psu=parse_float(row.get("sal_psu", row.get("hcep_sal", row.get("salinity_psu")))),
            specific_conductivity_s_m=parse_float(row.get("hcep_spc", row.get("spec_conductivity_sm"))),
            dissolved_oxygen_saturation_pct=parse_float(row.get("do_pct_sat", row.get("hcep_osat", row.get("oxygen_sat")))),
            nitrate_umol=parse_float(row.get("suna_nitraten_um", row.get("suna_m_parameter1", row.get("no3_umol")))),
            nitrate_mg_l=parse_float(row.get("suna_nitraten_mgl", row.get("suna_m_parameter2", row.get("no3_mgnl")))),
            wind_direction_deg=parse_float(row.get("winddirection")),
            wind_speed_m_s=parse_float(row.get("windspeed")),
            photosynthetically_active_radiation_umol_s_m2=parse_float(row.get("par_par_sq_421x")),
            air_temperature_f=parse_float(row.get("sdi_12sensor_m_parameter1", row.get("wtx534_temp"))),
            air_humidity_pct=parse_float(row.get("sdi_12sensor_m_parameter2", row.get("wtx534_humidity"))),
            air_pressure_in_hg=parse_float(row.get("sdi_12sensor_m_parameter3", row.get("wtx534_pressure"))),
            system_battery_v=parse_float(row.get("systembattery")),
            sensor_battery_v=parse_float(row.get("sonde_batt_v", row.get("hcep_volt"))),
        )

    def emit_reference_data(self, producer: USWAKingCountyMarineEventProducer) -> int:
        """Discover stations and emit reference events."""
        count = 0
        refreshed_metadata: "OrderedDict[str, dict]" = OrderedDict()
        for dataset in self.discover_datasets():
            dataset_id = dataset["id"]
            try:
                view = self.fetch_view(dataset_id)
                station = self.build_station(view)
            except (KeyError, ValueError, requests.RequestException) as exc:
                LOGGER.warning("Skipping station metadata for dataset %s: %s", dataset_id, exc)
                continue
            producer.send_us_wa_king_county_marine_station(
                station.station_id,
                station,
                flush_producer=False,
            )
            refreshed_metadata[dataset_id] = {
                "station_id": station.station_id,
                "station_name": station.station_name,
                "sensor_level": station.sensor_level,
            }
            count += 1
        if refreshed_metadata:
            self.station_metadata = refreshed_metadata
            producer.producer.flush()
            self.last_reference_refresh = datetime.now(timezone.utc).isoformat()
        elif self.station_metadata:
            LOGGER.warning("Station refresh produced no usable datasets; continuing with cached metadata")
        return count

    def poll_and_send(self, producer: USWAKingCountyMarineEventProducer, once: bool = False) -> None:
        """Run the polling loop."""
        while True:
            try:
                refresh_references = True
                if self.last_reference_refresh:
                    last = datetime.fromisoformat(self.last_reference_refresh)
                    refresh_references = (datetime.now(timezone.utc) - last).total_seconds() >= REFERENCE_REFRESH_SECONDS
                if refresh_references or not self.station_metadata:
                    try:
                        sent_stations = self.emit_reference_data(producer)
                        if sent_stations:
                            LOGGER.info("Sent %d station reference events", sent_stations)
                    except requests.RequestException as exc:
                        if self.station_metadata:
                            LOGGER.warning("Station refresh failed; continuing with cached metadata: %s", exc)
                        else:
                            raise

                sent = 0
                for dataset_id in list(self.station_metadata.keys()):
                    try:
                        rows = self.fetch_rows(dataset_id)
                    except requests.RequestException as exc:
                        LOGGER.warning("Skipping dataset %s after row fetch failure: %s", dataset_id, exc)
                        continue

                    for row in rows:
                        reading = self.build_reading(dataset_id, row)
                        reading_id = f"{reading.station_id}|{reading.observation_time}"
                        if reading_id in self.seen_reading_ids:
                            continue
                        producer.send_us_wa_king_county_marine_water_quality_reading(
                            reading.station_id,
                            reading,
                            flush_producer=False,
                        )
                        self._remember(reading_id)
                        sent += 1
                producer.producer.flush()
                self.save_state()
                LOGGER.info("Sent %d King County marine readings", sent)
            except (KeyError, OSError, ValueError, requests.RequestException) as exc:
                LOGGER.exception("Error during King County marine poll: %s", exc)

            if once:
                return
            time.sleep(DEFAULT_POLL_INTERVAL_SECONDS)


def main() -> None:
    """CLI entry point."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="King County marine bridge")
    parser.add_argument(
        "--connection-string",
        default=os.getenv("CONNECTION_STRING", ""),
        help="Kafka/Event Hubs/Fabric connection string",
    )
    parser.add_argument(
        "--state-file",
        default=os.getenv(
            "KING_COUNTY_MARINE_STATE_FILE",
            "/mnt/fileshare/king_county_marine_state.json",
        ),
        help="Path to the dedupe state file",
    )
    parser.add_argument("--once", action="store_true", help="Poll once and exit")
    args = parser.parse_args()

    kafka_config = parse_connection_string(args.connection_string)
    kafka_topic = kafka_config.pop("kafka_topic", None)
    if not kafka_config.get("bootstrap.servers") or not kafka_topic:
        raise ValueError("CONNECTION_STRING must provide bootstrap server and EntityPath")

    producer = Producer(kafka_config)
    event_producer = USWAKingCountyMarineEventProducer(producer, kafka_topic)
    KingCountyMarineBridge(state_file=args.state_file).poll_and_send(event_producer, once=args.once)
