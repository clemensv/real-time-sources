"""
USDA NRCS SNOTEL Snow and Weather Data Poller

Polls hourly snow and weather observations from SNOTEL stations via the
NRCS Report Generator and sends them to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
import logging
import argparse
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone

import requests
from snotel_producer_data import Station, SnowObservation
from snotel_producer_kafka_producer.producer import GovUsdaNrcsSnotelEventProducer


if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

REPORT_GENERATOR_BASE = "https://wcc.sc.egov.usda.gov/reportGenerator/view_csv"

# Representative set of SNOTEL stations across western US states
DEFAULT_STATION_TRIPLETS = [
    "838:CO:SNTL",   # University Camp, CO
    "669:CO:SNTL",   # Schofield Pass, CO
    "415:MT:SNTL",   # Flattop Mtn, MT
    "787:UT:SNTL",   # Trial Lake, UT
    "515:WY:SNTL",   # Kendall R.S., WY
    "679:ID:SNTL",   # Sheep Mountain, ID
    "910:WA:SNTL",   # Waterhole, WA
    "526:OR:SNTL",   # King Mountain, OR
    "473:CA:SNTL",   # Independence Camp, CA
    "1107:AK:SNTL",  # Upper Tsaina River, AK
    "572:NV:SNTL",   # Lee Canyon, NV
    "922:AZ:SNTL",   # White Horse Lake, AZ
    "604:NM:SNTL",   # Moreno Valley, NM
]

# Hardcoded reference data for the default station set
STATION_METADATA: Dict[str, Dict] = {
    "838:CO:SNTL":  {"name": "University Camp",     "state": "CO", "elevation": 10330.0, "latitude": 40.03, "longitude": -105.57},
    "669:CO:SNTL":  {"name": "Schofield Pass",      "state": "CO", "elevation": 10700.0, "latitude": 39.01, "longitude": -107.05},
    "415:MT:SNTL":  {"name": "Flattop Mountain",    "state": "MT", "elevation": 6400.0,  "latitude": 48.77, "longitude": -114.38},
    "787:UT:SNTL":  {"name": "Trial Lake",          "state": "UT", "elevation": 9980.0,  "latitude": 40.68, "longitude": -110.95},
    "515:WY:SNTL":  {"name": "Kendall R.S.",        "state": "WY", "elevation": 7800.0,  "latitude": 42.78, "longitude": -110.02},
    "679:ID:SNTL":  {"name": "Sheep Mountain",      "state": "ID", "elevation": 6850.0,  "latitude": 44.65, "longitude": -114.67},
    "910:WA:SNTL":  {"name": "Waterhole",           "state": "WA", "elevation": 5550.0,  "latitude": 48.10, "longitude": -120.67},
    "526:OR:SNTL":  {"name": "King Mountain",       "state": "OR", "elevation": 5060.0,  "latitude": 42.52, "longitude": -122.57},
    "473:CA:SNTL":  {"name": "Independence Camp",   "state": "CA", "elevation": 7000.0,  "latitude": 39.45, "longitude": -120.30},
    "1107:AK:SNTL": {"name": "Upper Tsaina River",  "state": "AK", "elevation": 2750.0,  "latitude": 61.18, "longitude": -145.62},
    "572:NV:SNTL":  {"name": "Lee Canyon",          "state": "NV", "elevation": 8600.0,  "latitude": 36.31, "longitude": -115.68},
    "922:AZ:SNTL":  {"name": "White Horse Lake",    "state": "AZ", "elevation": 6800.0,  "latitude": 35.15, "longitude": -112.10},
    "604:NM:SNTL":  {"name": "Moreno Valley",       "state": "NM", "elevation": 8420.0,  "latitude": 36.58, "longitude": -105.32},
}

POLL_INTERVAL_SECONDS = 3600  # SNOTEL data updates hourly


def parse_connection_string(connection_string: str) -> Tuple[Dict[str, str], str]:
    """
    Parse a Kafka or Event Hubs connection string into config dict and topic.

    Supports two formats:
      1. Event Hubs: ``Endpoint=sb://host/;...;EntityPath=topic``
      2. Plain Kafka: ``BootstrapServer=host:port;EntityPath=topic``

    Args:
        connection_string: The connection string to parse.

    Returns:
        Tuple of (kafka_config_dict, topic_name).
    """
    config_dict: Dict[str, str] = {}
    kafka_topic: Optional[str] = None

    parts = connection_string.split(';')
    kv: Dict[str, str] = {}
    for part in parts:
        if '=' in part:
            key, _, value = part.partition('=')
            kv[key.strip()] = value.strip().strip('"')

    if 'BootstrapServer' in kv:
        config_dict['bootstrap.servers'] = kv['BootstrapServer']
    elif 'Endpoint' in kv:
        endpoint = kv['Endpoint'].replace('sb://', '').replace('/', '')
        config_dict['bootstrap.servers'] = endpoint + ':9093'
        config_dict['security.protocol'] = 'SASL_SSL'
        config_dict['sasl.mechanisms'] = 'PLAIN'
        config_dict['sasl.username'] = '$ConnectionString'
        config_dict['sasl.password'] = connection_string.strip()

    kafka_topic = kv.get('EntityPath')

    enable_tls = os.environ.get('KAFKA_ENABLE_TLS', '').lower()
    if enable_tls == 'false' and 'security.protocol' not in config_dict:
        config_dict['security.protocol'] = 'PLAINTEXT'

    return config_dict, kafka_topic or ''


def parse_float(value: str) -> Optional[float]:
    """
    Parse a numeric value from SNOTEL CSV data.

    Returns None if the cell is empty or non-numeric (sensor offline / missing).

    Args:
        value: The raw CSV cell string.

    Returns:
        The float value, or None if missing.
    """
    if value is None:
        return None
    value = value.strip()
    if value == '' or value.lower() == 'nan':
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def build_station_csv_url(station_triplet: str) -> str:
    """
    Build the NRCS Report Generator URL for a single station's hourly observations.

    Requests the last 24 hours of data (``-1,0`` = yesterday to today).

    Args:
        station_triplet: Station triplet, e.g. '838:CO:SNTL'.

    Returns:
        The full URL string.
    """
    return (
        f"{REPORT_GENERATOR_BASE}/customSingleStationReport/hourly/"
        f"start_of_period/{station_triplet}/-1,0/"
        f"WTEQ::value,PREC::value,TOBS::value,SNWD::value"
    )


def parse_csv_response(csv_text: str) -> Tuple[List[str], List[List[str]]]:
    """
    Parse a SNOTEL CSV response.

    Skips comment lines (starting with '#') and empty lines.
    Returns the header row and data rows.

    Args:
        csv_text: The raw CSV text from the Report Generator.

    Returns:
        Tuple of (header_fields, list_of_data_rows).
    """
    headers: List[str] = []
    rows: List[List[str]] = []

    for line in csv_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        fields = [f.strip() for f in stripped.split(',')]
        if not headers:
            headers = fields
        else:
            rows.append(fields)

    return headers, rows


def parse_observation_row(station_triplet: str, row: List[str]) -> Optional[SnowObservation]:
    """
    Parse a single CSV data row into a SnowObservation.

    Expected column order (matching the Report Generator request):
        Date, SWE, Precip Accum, Air Temp, Snow Depth

    Args:
        station_triplet: The station identifier.
        row: The split CSV fields for one row.

    Returns:
        A SnowObservation instance, or None if the row is unparseable.
    """
    if len(row) < 2:
        return None
    try:
        dt = datetime.fromisoformat(row[0])
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
    except (ValueError, IndexError):
        return None

    swe = parse_float(row[1]) if len(row) > 1 else None
    prec = parse_float(row[2]) if len(row) > 2 else None
    tobs = parse_float(row[3]) if len(row) > 3 else None
    snwd = parse_float(row[4]) if len(row) > 4 else None

    return SnowObservation(
        station_triplet=station_triplet,
        date_time=dt,
        snow_water_equivalent=swe,
        snow_depth=snwd,
        precipitation=prec,
        air_temperature=tobs,
    )


class SnotelPoller:
    """
    Polls SNOTEL stations and sends observations to Kafka as CloudEvents.
    """

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str):
        """
        Initialize the SnotelPoller.

        Args:
            kafka_config: Kafka producer configuration dict.
            kafka_topic: The Kafka topic to produce to.
            last_polled_file: Path to the JSON state file for dedup tracking.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        from confluent_kafka import Producer
        kafka_producer = Producer(kafka_config)
        self.producer = GovUsdaNrcsSnotelEventProducer(kafka_producer, kafka_topic)

    def load_state(self) -> Dict:
        """Load last-seen timestamps from the state file."""
        if os.path.exists(self.last_polled_file):
            try:
                with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    if isinstance(state, dict):
                        return state
            except (json.JSONDecodeError, IOError):
                pass
        return {"last_timestamps": {}}

    def save_state(self, state: Dict) -> None:
        """Persist the state dict to disk."""
        try:
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except IOError as e:
            logger.error("Failed to save state: %s", e)

    def emit_station_reference(self, station_triplets: List[str]) -> int:
        """
        Emit Station reference events for all configured stations.

        Args:
            station_triplets: List of station triplet identifiers.

        Returns:
            Number of station events emitted.
        """
        count = 0
        for triplet in station_triplets:
            meta = STATION_METADATA.get(triplet)
            if not meta:
                logger.warning("No metadata for station %s, skipping reference emit", triplet)
                continue

            station = Station(
                station_triplet=triplet,
                name=meta["name"],
                state=meta["state"],
                elevation=meta["elevation"],
                latitude=meta["latitude"],
                longitude=meta["longitude"],
            )
            try:
                self.producer.send_gov_usda_nrcs_snotel_station(
                    triplet, station, flush_producer=False
                )
                count += 1
            except Exception as e:
                logger.error("Failed to emit station %s: %s", triplet, e)

        self.producer.producer.flush()
        logger.info("Emitted %d station reference events", count)
        return count

    def fetch_station_observations(self, station_triplet: str) -> str:
        """
        Fetch the CSV observation data for a single station.

        Args:
            station_triplet: The station triplet.

        Returns:
            The raw CSV text.

        Raises:
            requests.RequestException: On HTTP failure.
        """
        url = build_station_csv_url(station_triplet)
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        return response.text

    def poll_station(self, station_triplet: str, state: Dict) -> int:
        """
        Poll a single station and emit new observations.

        Args:
            station_triplet: The station triplet.
            state: The dedup state dict (mutated in place).

        Returns:
            Number of observations emitted.
        """
        try:
            csv_text = self.fetch_station_observations(station_triplet)
        except requests.RequestException as e:
            logger.warning("Failed to fetch data for %s: %s", station_triplet, e)
            return 0

        _, rows = parse_csv_response(csv_text)
        last_ts = state.get("last_timestamps", {}).get(station_triplet)
        count = 0

        for row in rows:
            obs = parse_observation_row(station_triplet, row)
            if obs is None:
                continue

            obs_ts = obs.date_time.isoformat()
            if last_ts and obs_ts <= last_ts:
                continue

            try:
                self.producer.send_gov_usda_nrcs_snotel_snow_observation(
                    station_triplet, obs, flush_producer=False
                )
                count += 1
            except Exception as e:
                logger.error("Failed to emit observation for %s at %s: %s",
                             station_triplet, obs_ts, e)
                continue

            if not last_ts or obs_ts > last_ts:
                state.setdefault("last_timestamps", {})[station_triplet] = obs_ts
                last_ts = obs_ts

        if count > 0:
            self.producer.producer.flush()
        return count

    def poll_all(self, station_triplets: List[str]) -> int:
        """
        Poll all configured stations and emit new observations.

        Args:
            station_triplets: The list of station triplets to poll.

        Returns:
            Total number of observations emitted.
        """
        state = self.load_state()
        total = 0

        for triplet in station_triplets:
            emitted = self.poll_station(triplet, state)
            total += emitted

        self.save_state(state)
        logger.info("Poll cycle complete: emitted %d observations across %d stations",
                     total, len(station_triplets))
        return total

    def run(self, station_triplets: List[str]) -> None:
        """
        Main run loop: emit reference data, then poll continuously.

        Args:
            station_triplets: The list of station triplets to monitor.
        """
        logger.info("Starting SNOTEL bridge with %d stations", len(station_triplets))
        self.emit_station_reference(station_triplets)

        while True:
            try:
                self.poll_all(station_triplets)
            except Exception as e:
                logger.error("Error during poll cycle: %s", e)
            time.sleep(POLL_INTERVAL_SECONDS)


def main():
    """Entry point for the SNOTEL bridge."""
    parser = argparse.ArgumentParser(description="SNOTEL Snow and Weather Data Bridge")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Start polling SNOTEL stations")
    feed_parser.add_argument("--stations", nargs="*",
                             help="Station triplets to poll (default: built-in set)")

    args = parser.parse_args()

    if args.command != "feed":
        parser.print_help()
        sys.exit(1)

    connection_string = os.environ.get("CONNECTION_STRING", "")
    if not connection_string:
        kafka_servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "")
        kafka_topic = os.environ.get("KAFKA_TOPIC", "snotel")
        sasl_user = os.environ.get("SASL_USERNAME", "")
        sasl_pass = os.environ.get("SASL_PASSWORD", "")

        if not kafka_servers:
            logger.error("CONNECTION_STRING or KAFKA_BOOTSTRAP_SERVERS must be set")
            sys.exit(1)

        kafka_config: Dict[str, str] = {
            'bootstrap.servers': kafka_servers,
        }
        if sasl_user and sasl_pass:
            kafka_config.update({
                'security.protocol': 'SASL_SSL',
                'sasl.mechanisms': 'PLAIN',
                'sasl.username': sasl_user,
                'sasl.password': sasl_pass,
            })

        enable_tls = os.environ.get('KAFKA_ENABLE_TLS', '').lower()
        if enable_tls == 'false' and 'security.protocol' not in kafka_config:
            kafka_config['security.protocol'] = 'PLAINTEXT'
    else:
        kafka_config, kafka_topic = parse_connection_string(connection_string)
        if not kafka_topic:
            kafka_topic = os.environ.get("KAFKA_TOPIC", "snotel")

    station_triplets = args.stations if args.stations else DEFAULT_STATION_TRIPLETS
    state_file = os.environ.get("STATE_FILE", "snotel_state.json")

    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logging.getLogger().setLevel(getattr(logging, log_level, logging.INFO))

    poller = SnotelPoller(kafka_config, kafka_topic, state_file)
    poller.run(station_triplets)
