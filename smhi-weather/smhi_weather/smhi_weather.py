"""SMHI Weather Observation Bridge - fetches meteorological observations from the Swedish Meteorological and Hydrological Institute."""

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

from smhi_weather_producer_kafka_producer.producer import SEGovSMHIWeatherEventProducer
from smhi_weather_producer_data import Station, WeatherObservation

logger = logging.getLogger(__name__)

SMHI_BASE_URL = "https://opendata-download-metobs.smhi.se/api/version/1.0"

# SMHI parameter IDs for hourly weather observations
PARAM_AIR_TEMP = 1        # Lufttemperatur, momentanvärde, 1 gång/tim
PARAM_WIND_GUST = 21      # Byvind, max 1 gång/tim
PARAM_DEW_POINT = 39      # Daggpunktstemperatur, momentanvärde
PARAM_PRESSURE = 9        # Lufttryck reducerat havsytans nivå
PARAM_HUMIDITY = 6        # Relativ Luftfuktighet
PARAM_PRECIP = 7          # Nederbördsmängd, summa 1 timme
PARAM_WIND_DIR = 3        # Vindriktning
PARAM_WIND_SPEED = 4      # Vindhastighet
PARAM_MAX_WIND_SPEED = 25 # Max av MedelVindhastighet
PARAM_VISIBILITY = 12     # Sikt
PARAM_CLOUD_COVER = 16    # Total molnmängd
PARAM_PRESENT_WX = 13     # Rådande väder (WMO ww code)
PARAM_SUNSHINE = 10       # Solskenstid
PARAM_IRRADIANCE = 11     # Global Irradians
PARAM_PRECIP_INTENSITY = 38  # Nederbördsintensitet

ALL_PARAMS = [
    PARAM_AIR_TEMP, PARAM_WIND_GUST, PARAM_DEW_POINT, PARAM_PRESSURE,
    PARAM_HUMIDITY, PARAM_PRECIP, PARAM_WIND_DIR, PARAM_WIND_SPEED,
    PARAM_MAX_WIND_SPEED, PARAM_VISIBILITY, PARAM_CLOUD_COVER,
    PARAM_PRESENT_WX, PARAM_SUNSHINE, PARAM_IRRADIANCE, PARAM_PRECIP_INTENSITY,
]


class SMHIWeatherAPI:
    """Client for the SMHI open data meteorological observation API."""

    def __init__(self, base_url: str = SMHI_BASE_URL, polling_interval: int = 900):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.session = requests.Session()

    def get_stations_for_parameter(self, parameter_id: int) -> list[dict]:
        """Fetch the station list for a given parameter."""
        url = f"{self.base_url}/parameter/{parameter_id}.json"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json().get("station", [])

    def get_bulk_latest(self, parameter_id: int) -> dict:
        """Fetch bulk latest-hour data for all stations for a given parameter."""
        url = f"{self.base_url}/parameter/{parameter_id}/station-set/all/period/latest-hour/data.json"
        response = self.session.get(url, timeout=60)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def parse_station(station_data: dict) -> Station:
        """Parse a station entry from the parameter station list."""
        summary = station_data.get("summary", "")
        lat = 0.0
        lon = 0.0
        for part in summary.split():
            if part.startswith("Latitud:"):
                continue
            if part.startswith("Longitud:"):
                continue
        # Parse lat/lon from summary like "Latitud: 65.53 Longitud: 14.97 Höjd: 665.0"
        parts = summary.split()
        for i, p in enumerate(parts):
            if p == "Latitud:" and i + 1 < len(parts):
                try:
                    lat = float(parts[i + 1])
                except ValueError:
                    pass
            elif p == "Longitud:" and i + 1 < len(parts):
                try:
                    lon = float(parts[i + 1])
                except ValueError:
                    pass

        title = station_data.get("title", "")
        name = title.split(" - ", 1)[-1] if " - " in title else title

        return Station(
            station_id=str(station_data["key"]),
            name=name,
            owner=station_data.get("owner", ""),
            owner_category=station_data.get("ownerCategory", ""),
            measuring_stations=station_data.get("measuringStations", ""),
            height=float(station_data.get("height", 0.0)),
            latitude=lat,
            longitude=lon,
        )

    @staticmethod
    def parse_bulk_observations(bulk_data: dict) -> dict[str, WeatherObservation]:
        """Parse bulk latest-hour data into a dict of station_id -> partial observation.
        Returns only stations that have a value in this parameter."""
        result: dict[str, WeatherObservation] = {}
        for station_data in bulk_data.get("station", []):
            values = station_data.get("value", [])
            if not values:
                continue
            latest = values[-1]
            val = latest.get("value")
            if val is None:
                continue
            sid = str(station_data["key"])
            epoch_ms = latest["date"]
            ts = datetime.fromtimestamp(epoch_ms / 1000.0, tz=timezone.utc)
            quality = latest.get("quality", "")
            result[sid] = {
                "station_id": sid,
                "station_name": station_data.get("name", ""),
                "observation_time": ts,
                "quality": quality,
                "value": float(val),
            }
        return result


def _merge_observations(param_data: dict[int, dict[str, dict]]) -> list[WeatherObservation]:
    """Merge per-parameter observations into WeatherObservation objects per station."""
    all_stations: set[str] = set()
    for pdata in param_data.values():
        all_stations.update(pdata.keys())

    observations = []
    for sid in all_stations:
        temp_data = param_data.get(PARAM_AIR_TEMP, {}).get(sid)
        if not temp_data:
            # Use any available parameter as base
            for pdata in param_data.values():
                if sid in pdata:
                    temp_data = pdata[sid]
                    break
        if not temp_data:
            continue

        obs = WeatherObservation(
            station_id=sid,
            station_name=temp_data.get("station_name", ""),
            observation_time=temp_data.get("observation_time", ""),
            air_temperature=param_data.get(PARAM_AIR_TEMP, {}).get(sid, {}).get("value"),
            wind_gust=param_data.get(PARAM_WIND_GUST, {}).get(sid, {}).get("value"),
            dew_point=param_data.get(PARAM_DEW_POINT, {}).get(sid, {}).get("value"),
            air_pressure=param_data.get(PARAM_PRESSURE, {}).get(sid, {}).get("value"),
            relative_humidity=_to_int(param_data.get(PARAM_HUMIDITY, {}).get(sid, {}).get("value")),
            precipitation_last_hour=param_data.get(PARAM_PRECIP, {}).get(sid, {}).get("value"),
            wind_direction=param_data.get(PARAM_WIND_DIR, {}).get(sid, {}).get("value"),
            wind_speed=param_data.get(PARAM_WIND_SPEED, {}).get(sid, {}).get("value"),
            max_wind_speed=param_data.get(PARAM_MAX_WIND_SPEED, {}).get(sid, {}).get("value"),
            visibility=param_data.get(PARAM_VISIBILITY, {}).get(sid, {}).get("value"),
            total_cloud_cover=_to_int(param_data.get(PARAM_CLOUD_COVER, {}).get(sid, {}).get("value")),
            present_weather=_to_int(param_data.get(PARAM_PRESENT_WX, {}).get(sid, {}).get("value")),
            sunshine_duration=param_data.get(PARAM_SUNSHINE, {}).get(sid, {}).get("value"),
            global_irradiance=param_data.get(PARAM_IRRADIANCE, {}).get(sid, {}).get("value"),
            precipitation_intensity=param_data.get(PARAM_PRECIP_INTENSITY, {}).get(sid, {}).get("value"),
            quality=temp_data.get("quality", ""),
        )
        observations.append(obs)
    return observations


def _to_int(v) -> typing.Optional[int]:
    if v is None:
        return None
    try:
        return int(v)
    except (ValueError, TypeError):
        return None


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


def send_stations(api: SMHIWeatherAPI, producer: SEGovSMHIWeatherEventProducer) -> int:
    """Fetch and emit station reference data."""
    stations = api.get_stations_for_parameter(PARAM_AIR_TEMP)
    sent = 0
    for sdata in stations:
        try:
            station = api.parse_station(sdata)
            producer.send_se_gov_smhi_weather_station(
                station.station_id, station, flush_producer=False,
            )
            sent += 1
        except Exception as e:
            logger.warning("Failed to parse station %s: %s", sdata.get("key", "?"), e)
    producer.producer.flush()
    logger.info("Sent %d station reference events", sent)
    return sent


def feed_observations(api: SMHIWeatherAPI, producer: SEGovSMHIWeatherEventProducer,
                      previous_readings: dict) -> int:
    """Fetch latest observations for all parameters and emit merged observations."""
    param_data: dict[int, dict[str, dict]] = {}
    for param_id in ALL_PARAMS:
        try:
            bulk = api.get_bulk_latest(param_id)
            param_data[param_id] = api.parse_bulk_observations(bulk)
        except Exception as e:
            logger.warning("Failed to fetch parameter %d: %s", param_id, e)

    observations = _merge_observations(param_data)
    sent = 0
    for obs in observations:
        reading_key = f"{obs.station_id}:{obs.observation_time.isoformat()}"
        if reading_key in previous_readings:
            continue
        producer.send_se_gov_smhi_weather_weather_observation(
            obs.station_id, obs, flush_producer=False,
        )
        sent += 1
        previous_readings[reading_key] = obs.observation_time.isoformat()

    producer.producer.flush()
    return sent


def main():
    """Main entry point for the SMHI Weather bridge."""
    parser = argparse.ArgumentParser(description="SMHI Weather Observation Bridge")
    parser.add_argument("--connection-string", required=False,
                        default=os.environ.get("KAFKA_CONNECTION_STRING") or os.environ.get("CONNECTION_STRING"))
    parser.add_argument("--topic", required=False, default=os.environ.get("KAFKA_TOPIC") or None)
    parser.add_argument("--polling-interval", type=int, default=int(os.environ.get("POLLING_INTERVAL", "900")))
    parser.add_argument("--state-file", type=str,
                        default=os.environ.get("STATE_FILE", os.path.expanduser("~/.smhi_weather_state.json")))
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List active stations")
    subparsers.add_parser("feed", help="Feed data to Kafka")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    api = SMHIWeatherAPI(polling_interval=args.polling_interval)

    if args.command == "list":
        stations = api.get_stations_for_parameter(PARAM_AIR_TEMP)
        for sdata in stations:
            station = api.parse_station(sdata)
            print(f"{station.station_id}: {station.name} [{station.latitude}, {station.longitude}]")
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
            args.topic = "smhi-weather"
        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        if "sasl.username" in kafka_config:
            kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
        kafka_config["client.id"] = "smhi-weather-bridge"
        kafka_producer = Producer(kafka_config)
        event_producer = SEGovSMHIWeatherEventProducer(kafka_producer, args.topic)
        logger.info("Starting SMHI Weather bridge, polling every %d seconds", args.polling_interval)
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
