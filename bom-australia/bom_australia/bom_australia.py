"""BOM Australia Weather Observation Bridge - fetches real-time weather observations from the Australian Bureau of Meteorology."""

import argparse
import json
import sys
import os
import time
import typing
import logging
import requests
from datetime import datetime, timezone
from confluent_kafka import Producer

from bom_australia_producer_kafka_producer.producer import AUGovBOMWeatherEventProducer
from bom_australia_producer_data import Station, WeatherObservation

logger = logging.getLogger(__name__)

BOM_BASE_URL = "http://reg.bom.gov.au/fwo"
BOM_STATIONS_URL = "http://www.bom.gov.au/climate/data/lists_by_element/stations.txt"

# Mapping from state abbreviation (in stations.txt) to BOM product ID prefix
STATE_TO_PRODUCT = {
    "NSW": "IDN60901",
    "VIC": "IDV60901",
    "QLD": "IDQ60901",
    "WA": "IDW60901",
    "SA": "IDS60901",
    "TAS": "IDT60901",
    "NT": "IDD60901",
    "ANT": "IDT60901",  # Antarctic stations routed through Tasmania product
}

# Fallback capital-city stations used only when station discovery fails
FALLBACK_STATIONS = [
    ("IDN60901", 94767),   # Sydney Airport, NSW
    ("IDV60901", 94866),   # Melbourne Airport, VIC
    ("IDQ60901", 94576),   # Brisbane Airport, QLD
    ("IDW60901", 94610),   # Perth Airport, WA
    ("IDS60901", 94648),   # Adelaide (West Terrace), SA
    ("IDT60901", 94970),   # Hobart Airport, TAS
    ("IDD60901", 94120),   # Darwin Airport, NT
    ("IDC60901", 94926),   # Canberra Airport, ACT
]


class BOMAustraliaAPI:
    """Client for the BOM weather observation JSON feeds."""

    def __init__(self, base_url: str = BOM_BASE_URL, polling_interval: int = 600):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "real-time-sources-bom-bridge/1.0"})

    def discover_stations(self, state_filter: typing.Optional[str] = None) -> list[tuple[str, int]]:
        """Discover active BOM stations from the bureau station list.

        Downloads the fixed-width stations.txt and returns (product_id, wmo_id) pairs
        for all active stations that have a WMO number. Optionally filters by state.
        """
        try:
            response = self.session.get(BOM_STATIONS_URL, timeout=60)
            response.raise_for_status()
        except Exception as e:
            logger.warning("Station discovery failed, using fallback list: %s", e)
            return FALLBACK_STATIONS

        stations: list[tuple[str, int]] = []
        allowed_states = None
        if state_filter:
            allowed_states = {s.strip().upper() for s in state_filter.split(",")}

        lines = response.text.strip().split("\n")
        for line in lines[4:]:  # skip header rows
            if len(line) < 131:
                continue
            try:
                end_year = line[63:71].strip()
                wmo_str = line[130:].strip().replace("\r", "")
                state = line[105:110].strip()

                # Active = end year is empty/.. or >= current year - 1
                is_active = (end_year in ("", "..") or
                             (end_year.isdigit() and int(end_year) >= 2025))
                has_wmo = wmo_str not in ("", "..") and wmo_str.isdigit()

                if not is_active or not has_wmo:
                    continue

                if allowed_states and state not in allowed_states:
                    continue

                product_id = STATE_TO_PRODUCT.get(state)
                if not product_id:
                    continue

                stations.append((product_id, int(wmo_str)))
            except (ValueError, IndexError):
                continue

        if not stations:
            logger.warning("No stations discovered, using fallback list")
            return FALLBACK_STATIONS

        logger.info("Discovered %d active stations with WMO numbers", len(stations))
        return stations

    def get_station_observations(self, product_id: str, wmo_id: int) -> dict:
        """Fetch the 72-hour observation product for a single station."""
        url = f"{self.base_url}/{product_id}/{product_id}.{wmo_id}.json"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def parse_station(product_id: str, obs_data: dict) -> typing.Optional[Station]:
        """Parse station reference data from an observation product response."""
        header = obs_data.get("observations", {}).get("header", [])
        data = obs_data.get("observations", {}).get("data", [])
        if not header or not data:
            return None
        hdr = header[0]
        first_obs = data[0]
        wmo = first_obs.get("wmo")
        if wmo is None:
            return None
        return Station(
            station_wmo=int(wmo),
            name=first_obs.get("name", hdr.get("name", "")),
            product_id=product_id,
            state=hdr.get("state", ""),
            time_zone=hdr.get("time_zone", ""),
            latitude=float(first_obs.get("lat", 0.0)),
            longitude=float(first_obs.get("lon", 0.0)),
        )

    @staticmethod
    def parse_observation(obs_record: dict) -> typing.Optional[WeatherObservation]:
        """Parse a single observation record from the BOM JSON data array."""
        wmo = obs_record.get("wmo")
        utc_str = obs_record.get("aifstime_utc")
        if wmo is None or not utc_str:
            return None
        try:
            ts = datetime.strptime(utc_str, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc).isoformat()
        except (ValueError, TypeError):
            return None

        def to_float(v):
            if v is None or v == "-" or v == "":
                return None
            try:
                return float(v)
            except (ValueError, TypeError):
                return None

        def to_int(v):
            if v is None or v == "-" or v == "":
                return None
            try:
                return int(v)
            except (ValueError, TypeError):
                return None

        def to_str(v):
            if v is None or v == "-":
                return None
            return str(v)

        return WeatherObservation(
            station_wmo=int(wmo),
            station_name=obs_record.get("name", ""),
            observation_time_utc=ts,
            local_time=obs_record.get("local_date_time_full", ""),
            air_temp=to_float(obs_record.get("air_temp")),
            apparent_temp=to_float(obs_record.get("apparent_t")),
            dewpt=to_float(obs_record.get("dewpt")),
            rel_hum=to_int(obs_record.get("rel_hum")),
            delta_t=to_float(obs_record.get("delta_t")),
            wind_dir=to_str(obs_record.get("wind_dir")),
            wind_spd_kmh=to_int(obs_record.get("wind_spd_kmh")),
            wind_spd_kt=to_int(obs_record.get("wind_spd_kt")),
            gust_kmh=to_int(obs_record.get("gust_kmh")),
            gust_kt=to_int(obs_record.get("gust_kt")),
            press=to_float(obs_record.get("press")),
            press_qnh=to_float(obs_record.get("press_qnh")),
            press_msl=to_float(obs_record.get("press_msl")),
            press_tend=to_str(obs_record.get("press_tend")),
            rain_trace=to_str(obs_record.get("rain_trace")),
            cloud=to_str(obs_record.get("cloud")),
            cloud_oktas=to_int(obs_record.get("cloud_oktas")),
            cloud_base_m=to_int(obs_record.get("cloud_base_m")),
            cloud_type=to_str(obs_record.get("cloud_type")),
            vis_km=to_str(obs_record.get("vis_km")),
            weather=to_str(obs_record.get("weather")),
            sea_state=to_str(obs_record.get("sea_state")),
            swell_dir_worded=to_str(obs_record.get("swell_dir_worded")),
            swell_height=to_float(obs_record.get("swell_height")),
            swell_period=to_float(obs_record.get("swell_period")),
            latitude=float(obs_record.get("lat", 0.0)),
            longitude=float(obs_record.get("lon", 0.0)),
        )


def parse_connection_string(connection_string: str) -> dict:
    """Parse a Kafka connection string into a config dict."""
    config: dict[str, str] = {}
    for part in connection_string.split(";"):
        part = part.strip()
        if "=" in part:
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key == "Endpoint":
                config["bootstrap.servers"] = value.replace("sb://", "").rstrip("/") + ":9093"
            elif key == "SharedAccessKeyName":
                config["sasl.username"] = "$ConnectionString"
            elif key == "SharedAccessKey":
                config["sasl.password"] = connection_string
            elif key == "BootstrapServer":
                config["bootstrap.servers"] = value
            elif key == "EntityPath":
                config["_entity_path"] = value
    if "sasl.username" in config:
        config["security.protocol"] = "SASL_SSL"
        config["sasl.mechanism"] = "PLAIN"
    return config


def _load_state(state_file: str) -> dict:
    """Load persisted dedup state from a JSON file."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logging.warning("Could not load state from %s: %s", state_file, e)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    """Save dedup state to a JSON file, keeping at most 100000 entries."""
    if not state_file:
        return
    try:
        if len(data) > 100000:
            keys = list(data.keys())
            data = {k: data[k] for k in keys[-50000:]}
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as e:
        logging.warning("Could not save state to %s: %s", state_file, e)


def _parse_station_list(station_csv: str) -> list[tuple[str, int]]:
    """Parse a comma-separated list of product_id:wmo_id pairs."""
    stations = []
    for entry in station_csv.split(","):
        entry = entry.strip()
        if ":" in entry:
            pid, wmo = entry.split(":", 1)
            stations.append((pid.strip(), int(wmo.strip())))
    return stations


def send_stations(api: BOMAustraliaAPI, producer: AUGovBOMWeatherEventProducer, station_list: list[tuple[str, int]]) -> int:
    """Fetch and emit station reference data for all configured stations."""
    sent = 0
    for product_id, wmo_id in station_list:
        try:
            obs_data = api.get_station_observations(product_id, wmo_id)
            station = api.parse_station(product_id, obs_data)
            if station:
                producer.send_au_gov_bom_weather_station(
                    str(station.station_wmo),
                    station,
                    flush_producer=False,
                )
                sent += 1
        except Exception as e:
            logger.warning("Failed to fetch station %s/%d: %s", product_id, wmo_id, e)
    producer.producer.flush()
    logger.info("Sent %d station reference events", sent)
    return sent


def feed_observations(api: BOMAustraliaAPI, producer: AUGovBOMWeatherEventProducer,
                      station_list: list[tuple[str, int]], previous_readings: dict) -> int:
    """Fetch latest observations for all stations and emit new ones."""
    sent = 0
    for product_id, wmo_id in station_list:
        try:
            obs_data = api.get_station_observations(product_id, wmo_id)
            records = obs_data.get("observations", {}).get("data", [])
            if not records:
                continue
            # Only emit the latest observation (sort_order == 0)
            latest = records[0]
            obs = api.parse_observation(latest)
            if obs:
                reading_key = f"{obs.station_wmo}:{obs.observation_time_utc}"
                if reading_key not in previous_readings:
                    producer.send_au_gov_bom_weather_weather_observation(
                        str(obs.station_wmo),
                        obs,
                        flush_producer=False,
                    )
                    sent += 1
                    previous_readings[reading_key] = obs.observation_time_utc
        except Exception as e:
            logger.warning("Failed to fetch observations for %s/%d: %s", product_id, wmo_id, e)
    producer.producer.flush()
    return sent


def main():
    """Main entry point for the BOM Australia bridge."""
    parser = argparse.ArgumentParser(description="BOM Australia Weather Observation Bridge")
    parser.add_argument("--connection-string", required=False, help="Kafka/Event Hubs connection string",
                        default=os.environ.get("KAFKA_CONNECTION_STRING") or os.environ.get("CONNECTION_STRING"))
    parser.add_argument("--topic", required=False, help="Kafka topic", default=os.environ.get("KAFKA_TOPIC") or None)
    parser.add_argument("--polling-interval", type=int, default=int(os.environ.get("POLLING_INTERVAL", "600")),
                        help="Polling interval in seconds (default: 600)")
    parser.add_argument("--state-file", type=str,
                        default=os.environ.get("STATE_FILE", os.path.expanduser("~/.bom_australia_state.json")))
    parser.add_argument("--stations", type=str, default=os.environ.get("BOM_STATIONS", ""),
                        help="Comma-separated product_id:wmo_id pairs (overrides station discovery)")
    parser.add_argument("--state-filter", type=str, default=os.environ.get("BOM_STATE_FILTER", ""),
                        help="Comma-separated state abbreviations to filter (e.g. NSW,VIC)")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List configured stations")
    subparsers.add_parser("feed", help="Feed data to Kafka")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    api = BOMAustraliaAPI(polling_interval=args.polling_interval)
    if args.stations:
        station_list = _parse_station_list(args.stations)
    else:
        station_list = api.discover_stations(args.state_filter or None)

    if args.command == "list":
        for product_id, wmo_id in station_list:
            try:
                obs_data = api.get_station_observations(product_id, wmo_id)
                station = api.parse_station(product_id, obs_data)
                if station:
                    print(f"{station.station_wmo}: {station.name} ({station.state}) [{station.latitude}, {station.longitude}]")
            except Exception as e:
                print(f"{product_id}/{wmo_id}: Error - {e}")
    elif args.command == "feed":
        if not args.connection_string:
            if not os.environ.get("KAFKA_BROKER"):
                print("Error: --connection-string or KAFKA_BROKER environment variable required for feed mode")
                sys.exit(1)
            kafka_config: dict[str, str] = {"bootstrap.servers": os.environ["KAFKA_BROKER"]}
        else:
            kafka_config = parse_connection_string(args.connection_string)
        if "_entity_path" in kafka_config and not args.topic:
            args.topic = kafka_config.pop("_entity_path")
        elif "_entity_path" in kafka_config:
            kafka_config.pop("_entity_path")
        if not args.topic:
            args.topic = "bom-australia"
        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        if "sasl.username" in kafka_config:
            kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
        elif tls_enabled and "security.protocol" not in kafka_config:
            pass  # don't force SSL for plain bootstrap
        kafka_config["client.id"] = "bom-australia-bridge"
        kafka_producer = Producer(kafka_config)
        event_producer = AUGovBOMWeatherEventProducer(kafka_producer, args.topic)
        logger.info("Starting BOM Australia bridge, polling every %d seconds, %d stations",
                     args.polling_interval, len(station_list))
        previous_readings = _load_state(args.state_file)
        send_stations(api, event_producer, station_list)
        while True:
            try:
                count = feed_observations(api, event_producer, station_list, previous_readings)
                _save_state(args.state_file, previous_readings)
                logger.info("Sent %d observation events", count)
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            time.sleep(args.polling_interval)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
