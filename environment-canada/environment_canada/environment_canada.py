"""Environment Canada Weather Bridge — fetches SWOB real-time observations via the OGC API."""

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

from environment_canada_producer_kafka_producer.producer import CAGovECCCWeatherEventProducer
from environment_canada_producer_data import Station, WeatherObservation

logger = logging.getLogger(__name__)

EC_API_BASE = "https://api.weather.gc.ca/collections"
SWOB_STATIONS_URL = f"{EC_API_BASE}/swob-stations/items"
SWOB_REALTIME_URL = f"{EC_API_BASE}/swob-realtime/items"

DEFAULT_LIMIT = 500


class ECWeatherAPI:
    """Client for the Environment Canada OGC API (SWOB stations and realtime)."""

    def __init__(self, base_url: str = EC_API_BASE, polling_interval: int = 900,
                 station_limit: int = DEFAULT_LIMIT, obs_limit: int = DEFAULT_LIMIT):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.station_limit = station_limit
        self.obs_limit = obs_limit
        self.session = requests.Session()

    def get_stations(self) -> list[dict]:
        """Fetch station metadata from swob-stations collection."""
        url = f"{self.base_url}/swob-stations/items"
        all_stations = []
        offset = 0
        while True:
            response = self.session.get(
                url, params={"f": "json", "limit": self.station_limit, "offset": offset},
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            features = data.get("features", [])
            if not features:
                break
            all_stations.extend(features)
            if len(features) < self.station_limit:
                break
            offset += len(features)
        return all_stations

    def get_recent_observations(self) -> list[dict]:
        """Fetch recent SWOB realtime observations (last 2 hours)."""
        url = f"{self.base_url}/swob-realtime/items"
        from datetime import timedelta
        two_hours_ago = (datetime.now(timezone.utc) - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        all_obs = []
        offset = 0
        while True:
            response = self.session.get(
                url, params={
                    "f": "json",
                    "limit": self.obs_limit,
                    "offset": offset,
                    "datetime": f"{two_hours_ago}/..",
                },
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            features = data.get("features", [])
            if not features:
                break
            all_obs.extend(features)
            if len(features) < self.obs_limit:
                break
            offset += len(features)
        return all_obs

    @staticmethod
    def parse_station(feature: dict) -> Station:
        """Parse a swob-stations feature into a Station data class."""
        props = feature.get("properties", {})
        geom = feature.get("geometry", {})
        coords = geom.get("coordinates", []) if geom else []
        lon = float(coords[0]) if len(coords) > 0 else None
        lat = float(coords[1]) if len(coords) > 1 else None
        elev = float(coords[2]) if len(coords) > 2 else None

        return Station(
            msc_id=str(props.get("msc_id", "")),
            name=props.get("name", ""),
            iata_id=props.get("iata_id", ""),
            wmo_id=props.get("wmo_id"),
            province_territory=props.get("province_territory", ""),
            data_provider=props.get("data_provider", ""),
            dataset_network=props.get("dataset_network", ""),
            auto_man=props.get("auto_man", ""),
            latitude=lat,
            longitude=lon,
            elevation=elev,
        )

    @staticmethod
    def parse_observation(feature: dict) -> typing.Optional[WeatherObservation]:
        """Parse a swob-realtime feature into a WeatherObservation, extracting core fields."""
        props = feature.get("properties", {})
        msc_id = str(props.get("msc_id-value", props.get("clim_id-value", "")))
        if not msc_id:
            return None
        obs_time_str = props.get("obs_date_tm", "")
        if not obs_time_str:
            return None
        try:
            obs_time = datetime.fromisoformat(obs_time_str.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return None

        station_name = props.get("stn_nam-value", "")

        def _float(key: str) -> typing.Optional[float]:
            v = props.get(key)
            if v is None:
                return None
            try:
                return float(v)
            except (ValueError, TypeError):
                return None

        def _int(key: str) -> typing.Optional[int]:
            v = props.get(key)
            if v is None:
                return None
            try:
                return int(v)
            except (ValueError, TypeError):
                return None

        return WeatherObservation(
            msc_id=msc_id,
            station_name=station_name,
            observation_time=obs_time,
            air_temperature=_float("air_temp"),
            dew_point=_float("dwpt_temp"),
            relative_humidity=_int("rel_hum"),
            station_pressure=_float("stn_pres"),
            wind_speed=_float("avg_wnd_spd_10m_pst1mt"),
            wind_direction=_int("avg_wnd_dir_10m_pst1mt"),
            wind_gust=_float("max_wnd_spd_10m_pst1mt"),
            precipitation_1hr=_float("pcpn_amt_pst1hr"),
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


def send_stations(api: ECWeatherAPI, producer: CAGovECCCWeatherEventProducer) -> int:
    """Fetch and emit station reference data."""
    features = api.get_stations()
    sent = 0
    for f in features:
        try:
            station = api.parse_station(f)
            if not station.msc_id:
                continue
            producer.send_ca_gov_eccc_weather_station(
                station.msc_id, station, flush_producer=False,
            )
            sent += 1
        except Exception as e:
            logger.warning("Failed to parse station: %s", e)
    producer.producer.flush()
    logger.info("Sent %d station reference events", sent)
    return sent


def feed_observations(api: ECWeatherAPI, producer: CAGovECCCWeatherEventProducer,
                      previous_readings: dict) -> int:
    """Fetch and emit observation events."""
    features = api.get_recent_observations()
    sent = 0
    for f in features:
        try:
            obs = api.parse_observation(f)
            if not obs:
                continue
            reading_key = f"{obs.msc_id}:{obs.observation_time.isoformat()}"
            if reading_key in previous_readings:
                continue
            producer.send_ca_gov_eccc_weather_weather_observation(
                obs.msc_id, obs, flush_producer=False,
            )
            sent += 1
            previous_readings[reading_key] = obs.observation_time.isoformat()
        except Exception as e:
            logger.warning("Failed to parse observation: %s", e)
    producer.producer.flush()
    return sent


def main():
    """Main entry point for the Environment Canada Weather bridge."""
    parser = argparse.ArgumentParser(description="Environment Canada Weather Observation Bridge")
    parser.add_argument("--connection-string", required=False,
                        default=os.environ.get("KAFKA_CONNECTION_STRING") or os.environ.get("CONNECTION_STRING"))
    parser.add_argument("--topic", required=False, default=os.environ.get("KAFKA_TOPIC") or None)
    parser.add_argument("--polling-interval", type=int, default=int(os.environ.get("POLLING_INTERVAL", "900")))
    parser.add_argument("--state-file", type=str,
                        default=os.environ.get("STATE_FILE", os.path.expanduser("~/.environment_canada_state.json")))
    parser.add_argument("--station-limit", type=int, default=int(os.environ.get("STATION_LIMIT", "500")))
    parser.add_argument("--obs-limit", type=int, default=int(os.environ.get("OBS_LIMIT", "500")))
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List SWOB stations")
    subparsers.add_parser("feed", help="Feed data to Kafka")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    api = ECWeatherAPI(polling_interval=args.polling_interval,
                       station_limit=args.station_limit, obs_limit=args.obs_limit)

    if args.command == "list":
        features = api.get_stations()
        for f in features:
            station = api.parse_station(f)
            print(f"{station.msc_id}: {station.name} [{station.province_territory}]")
    elif args.command == "feed":
        if not args.connection_string:
            if not os.environ.get("KAFKA_BROKER"):
                print("Error: --connection-string or KAFKA_BROKER required for feed mode")
                sys.exit(1)
            kafka_config: dict[str, str] = {"bootstrap.servers": os.environ["KAFKA_BROKER"]}
        else:
            kafka_config = parse_connection_string(args.connection_string)
        if "_entity_path" in kafka_config and not args.topic:
            args.topic = kafka_config.pop("_entity_path")
        elif "_entity_path" in kafka_config:
            kafka_config.pop("_entity_path")
        if not args.topic:
            args.topic = "environment-canada"
        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        if "sasl.username" in kafka_config:
            kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
        kafka_config["client.id"] = "environment-canada-bridge"
        kafka_producer = Producer(kafka_config)
        event_producer = CAGovECCCWeatherEventProducer(kafka_producer, args.topic)
        logger.info("Starting Environment Canada Weather bridge, polling every %d seconds", args.polling_interval)
        previous_readings = _load_state(args.state_file)
        send_stations(api, event_producer)
        while True:
            try:
                count = feed_observations(api, event_producer, previous_readings)
                _save_state(args.state_file, previous_readings)
                logger.info("Sent %d observation events", count)
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            time.sleep(args.polling_interval)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
