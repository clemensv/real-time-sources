"""KMI Belgium Weather Observation Bridge - fetches automatic weather station observations from the Royal Meteorological Institute of Belgium."""

import argparse
import json
import sys
import os
import time
import logging
from datetime import datetime, timezone
from typing import Any

import requests
from confluent_kafka import Producer

from kmi_belgium_producer_kafka_producer.producer import BEGovKMIWeatherEventProducer
from kmi_belgium_producer_data import Station, WeatherObservation

logger = logging.getLogger(__name__)

KMI_AWS_WFS_URL = "https://opendata.meteo.be/service/aws/ows"
FEATURE_TYPE = "aws:aws_10min"
LATEST_FETCH_COUNT = 200
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-kmi-belgium/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)
OBSERVATION_FIELDS = (
    "precip_quantity",
    "temp_dry_shelter_avg",
    "temp_grass_pt100_avg",
    "temp_soil_avg",
    "temp_soil_avg_5cm",
    "temp_soil_avg_10cm",
    "temp_soil_avg_20cm",
    "temp_soil_avg_50cm",
    "wind_speed_10m",
    "wind_speed_avg_30m",
    "wind_direction",
    "wind_gusts_speed",
    "humidity_rel_shelter_avg",
    "pressure",
    "sun_duration",
    "short_wave_from_sky_avg",
    "sun_int_avg",
)


class KMIBelgiumAPI:
    """Client for the KMI/RMI automatic weather station WFS API."""

    def __init__(self, base_url: str = KMI_AWS_WFS_URL, polling_interval: int = 600):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT

    def get_observations(self, last_timestamp: str | None = None, count: int | None = None) -> list[dict[str, Any]]:
        """Fetch aws:aws_10min observations as GeoJSON features."""
        params: dict[str, str] = {
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "typeNames": FEATURE_TYPE,
            "outputFormat": "application/json",
            "sortBy": "timestamp D",
        }
        if count is not None:
            params["count"] = str(count)
        if last_timestamp:
            params["CQL_FILTER"] = f"timestamp >= '{last_timestamp}'"
        response = self.session.get(self.base_url, params=params, timeout=60)
        response.raise_for_status()
        payload = response.json()
        return payload.get("features", [])

    def get_latest_observations(self, count: int = LATEST_FETCH_COUNT) -> list[dict[str, Any]]:
        """Fetch the latest observation slice and keep only the newest timestamp batch."""
        features = self.get_observations(count=count)
        if not features:
            return []
        latest_timestamp = features[0].get("properties", {}).get("timestamp")
        if not latest_timestamp:
            return features
        return [
            feature
            for feature in features
            if feature.get("properties", {}).get("timestamp") == latest_timestamp
        ]

    @staticmethod
    def parse_station(feature: dict[str, Any]) -> Station:
        """Parse a GeoJSON feature into a Station event payload."""
        properties = feature.get("properties", {})
        longitude, latitude = KMIBelgiumAPI._coordinates(feature)
        return Station(
            station_code=str(properties["code"]),
            latitude=latitude,
            longitude=longitude,
            region=None,
        )

    @staticmethod
    def parse_observation(feature: dict[str, Any]) -> WeatherObservation:
        """Parse a GeoJSON feature into a WeatherObservation event payload."""
        properties = feature.get("properties", {})
        observation = {
            "station_code": str(properties["code"]),
            "observation_time": _parse_timestamp(properties["timestamp"]),
        }
        for field_name in OBSERVATION_FIELDS:
            observation[field_name] = _to_float(properties.get(field_name))
        observation["region"] = None
        return WeatherObservation(**observation)

    @staticmethod
    def _coordinates(feature: dict[str, Any]) -> tuple[float, float]:
        geometry = feature.get("geometry") or {}
        coordinates = geometry.get("coordinates") or []
        if len(coordinates) < 2:
            raise ValueError("GeoJSON feature is missing [longitude, latitude] coordinates")
        return float(coordinates[0]), float(coordinates[1])


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None



def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)



def _format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")



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
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logging.warning("Could not load state from %s: %s", state_file, e)
    return {}



def _save_state(state_file: str, data: dict) -> None:
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



def extract_stations(features: list[dict[str, Any]]) -> list[Station]:
    """Extract unique stations from observation features."""
    stations: dict[str, Station] = {}
    for feature in features:
        station = KMIBelgiumAPI.parse_station(feature)
        stations.setdefault(station.station_code, station)
    return sorted(stations.values(), key=lambda station: station.station_code)



def send_stations(api: KMIBelgiumAPI, producer: BEGovKMIWeatherEventProducer) -> int:
    """Fetch and emit station reference data."""
    features = api.get_latest_observations()
    stations = extract_stations(features)
    sent = 0
    for station in stations:
        producer.send_be_gov_kmi_weather_station(
            station.station_code, station, flush_producer=False,
        )
        sent += 1
    producer.producer.flush()
    logger.info("Sent %d station reference events", sent)
    return sent



def feed_observations(api: KMIBelgiumAPI, producer: BEGovKMIWeatherEventProducer,
                      previous_readings: dict) -> int:
    """Fetch observations and emit only new readings."""
    last_timestamp = previous_readings.get("__last_timestamp__")
    if last_timestamp:
        features = api.get_observations(last_timestamp=last_timestamp)
    else:
        features = api.get_latest_observations()

    sent = 0
    latest_observation_time: datetime | None = None

    for feature in features:
        obs = api.parse_observation(feature)
        if latest_observation_time is None or obs.observation_time > latest_observation_time:
            latest_observation_time = obs.observation_time
        reading_timestamp = _format_timestamp(obs.observation_time)
        reading_key = f"{obs.station_code}:{reading_timestamp}"
        if reading_key in previous_readings:
            continue
        producer.send_be_gov_kmi_weather_weather_observation(
            obs.station_code, obs, flush_producer=False,
        )
        sent += 1
        previous_readings[reading_key] = reading_timestamp

    if latest_observation_time is not None:
        previous_readings["__last_timestamp__"] = _format_timestamp(latest_observation_time)

    producer.producer.flush()
    return sent



def main():
    """Main entry point for the KMI Belgium Weather bridge."""
    parser = argparse.ArgumentParser(description="KMI Belgium Weather Observation Bridge")
    parser.add_argument("--connection-string", required=False,
                        default=os.environ.get("KAFKA_CONNECTION_STRING") or os.environ.get("CONNECTION_STRING"))
    parser.add_argument("--topic", required=False, default=os.environ.get("KAFKA_TOPIC") or None)
    parser.add_argument("--polling-interval", type=int, default=int(os.environ.get("POLLING_INTERVAL", "600")))
    parser.add_argument("--state-file", type=str,
                        default=os.environ.get("STATE_FILE", os.path.expanduser("~/.kmi_belgium_state.json")))
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List active stations")
    feed_parser = subparsers.add_parser("feed", help="Feed data to Kafka")
    feed_parser.add_argument("--once", action="store_true",
                             default=os.environ.get("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                             help="Exit after one polling cycle (also via ONCE_MODE env var). "
                                  "Useful for scheduled execution in Fabric notebooks.")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    api = KMIBelgiumAPI(polling_interval=args.polling_interval)

    if args.command == "list":
        stations = extract_stations(api.get_latest_observations())
        for station in stations:
            logger.info("%s: [%s, %s]", station.station_code, station.latitude, station.longitude)
    elif args.command == "feed":
        if not args.connection_string:
            if not os.environ.get("KAFKA_BROKER"):
                logger.error("Error: --connection-string or KAFKA_BROKER required for feed mode")
                sys.exit(1)
            kafka_config: dict[str, str] = {"bootstrap.servers": os.environ["KAFKA_BROKER"]}
        else:
            kafka_config = parse_connection_string(args.connection_string)
        if "_entity_path" in kafka_config and not args.topic:
            args.topic = kafka_config.pop("_entity_path")
        elif "_entity_path" in kafka_config:
            kafka_config.pop("_entity_path")
        if not args.topic:
            args.topic = "kmi-belgium"
        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        if "sasl.username" in kafka_config:
            kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
        kafka_config["client.id"] = "kmi-belgium-bridge"
        kafka_producer = Producer(kafka_config)
        event_producer = BEGovKMIWeatherEventProducer(kafka_producer, args.topic)
        logger.info("Starting KMI Belgium Weather bridge, polling every %d seconds", args.polling_interval)
        previous_readings = _load_state(args.state_file)
        send_stations(api, event_producer)
        while True:
            try:
                count = feed_observations(api, event_producer, previous_readings)
                _save_state(args.state_file, previous_readings)
                logger.info("Sent %d observation events", count)
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            if getattr(args, "once", False):
                logger.info("--once mode: exiting after first polling cycle")
                break
            time.sleep(args.polling_interval)
    else:
        logger.info("%s", parser.format_help().rstrip())


if __name__ == "__main__":
    main()
