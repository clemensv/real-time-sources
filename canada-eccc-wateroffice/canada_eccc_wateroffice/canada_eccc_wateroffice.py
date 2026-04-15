"""Canada ECCC Water Office Hydrometric Data Bridge.

Fetches hydrometric station reference data and real-time observations from
Environment and Climate Change Canada (ECCC) Water Survey of Canada OGC API
and emits them as CloudEvents to Apache Kafka.
"""

import argparse
import datetime
import json
import os
import sys
import time
import typing
import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from confluent_kafka import Producer

from canada_eccc_wateroffice_producer_kafka_producer.producer import CAGovECCCHydroEventProducer
from canada_eccc_wateroffice_producer_data import Station
from canada_eccc_wateroffice_producer_data import Observation

logger = logging.getLogger(__name__)

ECCC_STATIONS_URL = "https://api.weather.gc.ca/collections/hydrometric-stations/items"
ECCC_REALTIME_URL = "https://api.weather.gc.ca/collections/hydrometric-realtime/items"

OBSERVATION_WINDOW_SECONDS = 7200   # 2-hour sliding window
STATION_REFRESH_INTERVAL = 86400    # 24 hours


def _make_session() -> requests.Session:
    """Create a requests session with retry handling for transient failures."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


class ECCCWaterOfficeAPI:
    """Client for the ECCC OGC API hydrometric services."""

    def __init__(self, polling_interval: int = 300):
        self.polling_interval = polling_interval
        self.session = _make_session()

    def get_stations(self, offset: int = 0, limit: int = 500) -> typing.List[dict]:
        """Fetch a page of station features from the hydrometric-stations collection."""
        params = {"f": "json", "limit": limit, "offset": offset}
        response = self.session.get(ECCC_STATIONS_URL, params=params, timeout=60)
        response.raise_for_status()
        return response.json().get("features", [])

    def get_all_stations(self) -> typing.List[dict]:
        """Fetch all station features via pagination."""
        all_features = []
        offset = 0
        limit = 500
        while True:
            features = self.get_stations(offset=offset, limit=limit)
            all_features.extend(features)
            if len(features) < limit:
                break
            offset += limit
        return all_features

    def get_observations(self, start_dt: datetime.datetime, limit: int = 500) -> typing.List[dict]:
        """Fetch real-time observations starting from start_dt."""
        start_str = start_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        params = {"f": "json", "limit": limit, "datetime": f"{start_str}/.."}
        response = self.session.get(ECCC_REALTIME_URL, params=params, timeout=60)
        response.raise_for_status()
        return response.json().get("features", [])

    @staticmethod
    def parse_station(feature: dict) -> Station:
        """Map a GeoJSON feature from hydrometric-stations to a Station data class."""
        props = feature.get("properties", {})
        geometry = feature.get("geometry") or {}
        coords = geometry.get("coordinates") or []
        longitude = float(coords[0]) if len(coords) >= 2 else None
        latitude = float(coords[1]) if len(coords) >= 2 else None

        rhbn_raw = props.get("RHBN")
        real_time_raw = props.get("REAL_TIME")

        return Station(
            station_number=str(props["STATION_NUMBER"]),
            station_name=str(props["STATION_NAME"]),
            prov_terr_state_loc=str(props["PROV_TERR_STATE_LOC"]),
            status_en=props.get("STATUS_EN"),
            contributor_en=props.get("CONTRIBUTOR_EN"),
            drainage_area_gross=float(props["DRAINAGE_AREA_GROSS"]) if props.get("DRAINAGE_AREA_GROSS") is not None else None,
            drainage_area_effect=float(props["DRAINAGE_AREA_EFFECT"]) if props.get("DRAINAGE_AREA_EFFECT") is not None else None,
            rhbn=bool(rhbn_raw) if rhbn_raw is not None else None,
            real_time=bool(real_time_raw) if real_time_raw is not None else None,
            latitude=latitude,
            longitude=longitude,
        )

    @staticmethod
    def parse_observation(feature: dict) -> typing.Optional[Observation]:
        """Map a GeoJSON feature from hydrometric-realtime to an Observation data class."""
        props = feature.get("properties", {})
        if not props.get("STATION_NUMBER") or not props.get("IDENTIFIER") or not props.get("DATETIME"):
            return None

        geometry = feature.get("geometry") or {}
        coords = geometry.get("coordinates") or []
        longitude = float(coords[0]) if len(coords) >= 2 else None
        latitude = float(coords[1]) if len(coords) >= 2 else None

        dt_str = props["DATETIME"]
        try:
            obs_dt = datetime.datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            logger.debug("Could not parse datetime '%s'", dt_str)
            return None

        level_raw = props.get("LEVEL")
        discharge_raw = props.get("DISCHARGE")

        return Observation(
            station_number=str(props["STATION_NUMBER"]),
            identifier=str(props["IDENTIFIER"]),
            station_name=str(props.get("STATION_NAME", "")),
            prov_terr_state_loc=str(props.get("PROV_TERR_STATE_LOC", "")),
            observation_datetime=obs_dt,
            level=float(level_raw) if level_raw is not None else None,
            discharge=float(discharge_raw) if discharge_raw is not None else None,
            latitude=latitude,
            longitude=longitude,
        )


def parse_connection_string(connection_string: str) -> dict:
    """Parse a Kafka connection string into a confluent-kafka config dict."""
    config = {}
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


def send_stations(
    api: ECCCWaterOfficeAPI,
    producer: CAGovECCCHydroEventProducer,
) -> typing.Dict[str, Station]:
    """Fetch all stations, emit Station events, and return them keyed by station_number."""
    features = api.get_all_stations()
    stations: typing.Dict[str, Station] = {}
    sent = 0
    for feature in features:
        try:
            station = api.parse_station(feature)
        except (KeyError, TypeError, ValueError) as exc:
            logger.debug("Skipping malformed station feature: %s", exc)
            continue
        stations[station.station_number] = station
        producer.send_ca_gov_eccc_hydro_station(
            station.station_number,
            station,
            flush_producer=False,
        )
        sent += 1
    producer.producer.flush()
    logger.info("Sent %d station events", sent)
    return stations


def feed(
    api: ECCCWaterOfficeAPI,
    producer: CAGovECCCHydroEventProducer,
    seen_ids: typing.Set[str],
    stations: typing.Dict[str, Station],
) -> int:
    """Fetch observations for the last OBSERVATION_WINDOW_SECONDS and emit new ones.

    Returns the number of new observation events sent.
    Defers advancing seen_ids until after a successful flush.
    """
    start_dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        seconds=OBSERVATION_WINDOW_SECONDS
    )
    try:
        features = api.get_observations(start_dt)
    except requests.RequestException as exc:
        logger.error("Failed to fetch observations: %s", exc)
        return 0

    pending_ids: typing.List[str] = []
    sent = 0
    for feature in features:
        try:
            obs = api.parse_observation(feature)
        except Exception as exc:
            logger.debug("Skipping malformed observation feature: %s", exc)
            continue
        if obs is None:
            continue
        if obs.identifier in seen_ids:
            continue
        producer.send_ca_gov_eccc_hydro_observation(
            obs.station_number,
            obs,
            flush_producer=False,
        )
        pending_ids.append(obs.identifier)
        sent += 1

    if sent > 0:
        unflushed = producer.producer.flush(timeout=30)
        if unflushed != 0:
            logger.error("Kafka flush incomplete: %d messages not delivered; dedupe state not advanced", unflushed)
            return 0
        seen_ids.update(pending_ids)

    return sent


def main():
    """Main entry point for the Canada ECCC Water Office bridge."""
    parser = argparse.ArgumentParser(description="Canada ECCC Water Office Hydrometric Bridge")
    parser.add_argument(
        "--connection-string",
        required=False,
        help="Kafka/Event Hubs connection string",
        default=os.environ.get("KAFKA_CONNECTION_STRING") or os.environ.get("CONNECTION_STRING"),
    )
    parser.add_argument(
        "--topic",
        required=False,
        help="Kafka topic",
        default=os.environ.get("KAFKA_TOPIC") or None,
    )
    parser.add_argument(
        "--polling-interval",
        type=int,
        default=int(os.environ.get("POLLING_INTERVAL", "300")),
        help="Observation polling interval in seconds (default: 300)",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List all stations to stdout")
    observe_parser = subparsers.add_parser("observe", help="Print recent observations to stdout")
    observe_parser.add_argument(
        "--window",
        type=int,
        default=OBSERVATION_WINDOW_SECONDS,
        help="Lookback window in seconds",
    )
    subparsers.add_parser("feed", help="Feed data continuously to Kafka")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    api = ECCCWaterOfficeAPI(polling_interval=args.polling_interval)

    if args.command == "list":
        features = api.get_all_stations()
        for feature in features:
            try:
                station = api.parse_station(feature)
                print(f"{station.station_number}: {station.station_name} [{station.prov_terr_state_loc}] lat={station.latitude} lon={station.longitude}")
            except Exception as exc:
                logger.debug("Skipping feature: %s", exc)

    elif args.command == "observe":
        window = getattr(args, "window", OBSERVATION_WINDOW_SECONDS)
        start_dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=window)
        features = api.get_observations(start_dt)
        for feature in features:
            obs = api.parse_observation(feature)
            if obs:
                print(f"{obs.station_number} | {obs.observation_datetime.isoformat()} | level={obs.level} | discharge={obs.discharge}")

    elif args.command == "feed":
        if not args.connection_string:
            if not os.environ.get("KAFKA_BROKER"):
                print("Error: --connection-string or KAFKA_BROKER environment variable required for feed mode", file=sys.stderr)
                sys.exit(1)
            kafka_config = {"bootstrap.servers": os.environ["KAFKA_BROKER"]}
        else:
            kafka_config = parse_connection_string(args.connection_string)

        if "_entity_path" in kafka_config and not args.topic:
            args.topic = kafka_config.pop("_entity_path")
        elif "_entity_path" in kafka_config:
            kafka_config.pop("_entity_path")

        if not args.topic:
            args.topic = "canada-eccc-wateroffice"

        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        if "sasl.username" in kafka_config:
            kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
        elif tls_enabled:
            kafka_config["security.protocol"] = "SSL"

        kafka_config["client.id"] = "canada-eccc-wateroffice-bridge"
        producer = Producer(kafka_config)
        event_producer = CAGovECCCHydroEventProducer(producer, args.topic)

        logger.info("Starting ECCC Water Office bridge, polling every %d seconds", args.polling_interval)

        stations = send_stations(api, event_producer)
        seen_ids: typing.Set[str] = set()
        last_station_refresh = time.time()

        while True:
            try:
                if time.time() - last_station_refresh >= STATION_REFRESH_INTERVAL:
                    try:
                        new_stations = send_stations(api, event_producer)
                        stations = new_stations
                        last_station_refresh = time.time()
                        logger.info("Station catalog refreshed: %d stations", len(stations))
                    except Exception as exc:
                        logger.error("Station refresh failed, keeping cached catalog: %s", exc)

                count = feed(api, event_producer, seen_ids, stations)
                logger.info("Sent %d new observation events", count)
            except Exception as exc:
                logger.error("Error in feed loop: %s", exc)

            time.sleep(args.polling_interval)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
