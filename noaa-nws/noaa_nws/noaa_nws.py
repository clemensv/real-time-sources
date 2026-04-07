"""
NOAA NWS Weather Alerts Poller
Polls the NWS alerts API and sends alerts to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
from typing import Dict, List
import argparse
import requests
from noaa_nws_producer_data import WeatherAlert, Zone
from noaa_nws_producer_data.observationstation import ObservationStation
from noaa_nws_producer_data.weatherobservation import WeatherObservation
from noaa_nws_producer_kafka_producer.producer import (
    MicrosoftOpenDataUSNOAANWSAlertsEventProducer,
    MicrosoftOpenDataUSNOAANWSZonesEventProducer,
    MicrosoftOpenDataUSNOAANWSObservationsEventProducer,
)


class NWSAlertPoller:
    """
    Polls the NWS Weather Alerts API and sends alerts to Kafka as CloudEvents.
    """
    ALERTS_URL = "https://api.weather.gov/alerts/active"
    ZONES_URL = "https://api.weather.gov/zones?type=forecast"
    STATIONS_URL = "https://api.weather.gov/stations"
    HEADERS = {
        "User-Agent": "(real-time-sources, clemensv@microsoft.com)",
        "Accept": "application/geo+json"
    }
    POLL_INTERVAL_SECONDS = 60
    OBSERVATION_INTERVAL_SECONDS = 300  # Poll observations every 5 minutes

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str):
        """
        Initialize the NWSAlertPoller.

        Args:
            kafka_config: Kafka configuration settings.
            kafka_topic: Kafka topic to send messages to.
            last_polled_file: File to store seen alert IDs for deduplication.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        from confluent_kafka import Producer
        kafka_producer = Producer(kafka_config)
        self.alerts_producer = MicrosoftOpenDataUSNOAANWSAlertsEventProducer(kafka_producer, kafka_topic)
        self.zones_producer = MicrosoftOpenDataUSNOAANWSZonesEventProducer(kafka_producer, kafka_topic)
        self.observations_producer = MicrosoftOpenDataUSNOAANWSObservationsEventProducer(kafka_producer, kafka_topic)
        self.kafka_producer = kafka_producer
        self.station_ids: List[str] = []

    def load_seen_alerts(self) -> Dict:
        """
        Load the set of previously seen alert IDs from the state file.

        Returns:
            Dict with 'seen_ids' list.
        """
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {"seen_ids": []}

    def save_seen_alerts(self, state: Dict):
        """
        Save the set of seen alert IDs to the state file.

        Args:
            state: Dict with 'seen_ids' list.
        """
        try:
            os.makedirs(os.path.dirname(self.last_polled_file) if os.path.dirname(self.last_polled_file) else '.', exist_ok=True)
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Error saving state: {e}")

    def fetch_zones(self):
        """Fetch all NWS forecast zones as reference data."""
        zones = []
        url = self.ZONES_URL
        try:
            while url:
                response = requests.get(url, headers=self.HEADERS, timeout=30)
                response.raise_for_status()
                data = response.json()
                features = data.get("features", [])
                for feature in features:
                    props = feature.get("properties", {})
                    zone = Zone(
                        zone_id=props.get("id", ""),
                        name=props.get("name", ""),
                        type=props.get("type", ""),
                        state=props.get("state", ""),
                        forecast_office=props.get("forecastOffice", ""),
                        timezone=props.get("timeZone", ""),
                        radar_station=props.get("radarStation", "")
                    )
                    zones.append(zone)
                # Handle pagination
                pagination = data.get("pagination", {})
                url = pagination.get("next") if pagination else None
        except Exception as err:
            print(f"Error fetching NWS zones: {err}")
        return zones

    def fetch_observation_stations(self, max_stations: int = 2500) -> List[ObservationStation]:
        """Fetch observation stations from the NWS stations endpoint."""
        stations: List[ObservationStation] = []
        url = f"{self.STATIONS_URL}?limit=500"
        try:
            while url and len(stations) < max_stations:
                response = requests.get(url, headers=self.HEADERS, timeout=30)
                response.raise_for_status()
                data = response.json()
                for feature in data.get("features", []):
                    props = feature.get("properties", {})
                    sid = props.get("stationIdentifier", "")
                    if not sid:
                        continue
                    elev = props.get("elevation", {})
                    elev_val = elev.get("value") if isinstance(elev, dict) else None
                    forecast_url = props.get("forecast", "")
                    forecast_zone = forecast_url.rsplit("/", 1)[-1] if forecast_url else None
                    county_url = props.get("county", "")
                    county_zone = county_url.rsplit("/", 1)[-1] if county_url else None
                    fire_url = props.get("fireWeatherZone", "")
                    fire_zone = fire_url.rsplit("/", 1)[-1] if fire_url else None
                    station = ObservationStation(
                        station_id=sid,
                        name=props.get("name", ""),
                        elevation_m=float(elev_val) if elev_val is not None else None,
                        time_zone=props.get("timeZone"),
                        forecast_zone=forecast_zone,
                        county=county_zone,
                        fire_weather_zone=fire_zone,
                    )
                    stations.append(station)
                pagination = data.get("pagination", {})
                url = pagination.get("next") if pagination else None
        except Exception as err:
            print(f"Error fetching NWS stations: {err}")
        return stations

    @staticmethod
    def _extract_value(quantity) -> float | None:
        """Extract the numeric value from a NWS quantity object like {'value': 11, 'unitCode': 'wmoUnit:degC'}."""
        if quantity is None:
            return None
        if isinstance(quantity, dict):
            v = quantity.get("value")
            return float(v) if v is not None else None
        return None

    def fetch_latest_observation(self, station_id: str) -> WeatherObservation | None:
        """Fetch the latest observation for a single station."""
        url = f"{self.STATIONS_URL}/{station_id}/observations/latest"
        try:
            response = requests.get(url, headers=self.HEADERS, timeout=15)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            props = data.get("properties", {})
            ts = props.get("timestamp")
            if not ts:
                return None
            return WeatherObservation(
                station_id=station_id,
                timestamp=ts,
                text_description=props.get("textDescription"),
                temperature=self._extract_value(props.get("temperature")),
                dewpoint=self._extract_value(props.get("dewpoint")),
                wind_direction=self._extract_value(props.get("windDirection")),
                wind_speed=self._extract_value(props.get("windSpeed")),
                wind_gust=self._extract_value(props.get("windGust")),
                barometric_pressure=self._extract_value(props.get("barometricPressure")),
                sea_level_pressure=self._extract_value(props.get("seaLevelPressure")),
                visibility=self._extract_value(props.get("visibility")),
                relative_humidity=self._extract_value(props.get("relativeHumidity")),
                wind_chill=self._extract_value(props.get("windChill")),
                heat_index=self._extract_value(props.get("heatIndex")),
            )
        except Exception as err:
            print(f"Error fetching observation for {station_id}: {err}")
            return None

    def poll_alerts(self) -> List[dict]:
        """
        Fetch active alerts from the NWS API.

        Returns:
            List of alert feature dicts from the GeoJSON response.
        """
        try:
            response = requests.get(self.ALERTS_URL, headers=self.HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("features", [])
        except Exception as err:
            print(f"Error fetching NWS alerts: {err}")
            return []

    def poll_and_send(self):
        """
        Main polling loop. Fetches alerts, deduplicates, and sends new alerts
        to Kafka as CloudEvents. Polls every POLL_INTERVAL_SECONDS.
        """
        print(f"Starting NWS Weather Alert poller, polling every {self.POLL_INTERVAL_SECONDS}s")
        print(f"  Alerts URL: {self.ALERTS_URL}")
        print(f"  Kafka topic: {self.kafka_topic}")

        # Send reference data (zones) at startup
        print("Sending NWS forecast zones as reference data...")
        zones = self.fetch_zones()
        for zone in zones:
            self.zones_producer.send_microsoft_open_data_us_noaa_nws_zone(
                zone.zone_id, zone, flush_producer=False)
        self.kafka_producer.flush()
        print(f"Sent {len(zones)} zones as reference data")

        # Send observation stations at startup
        print("Sending NWS observation stations as reference data...")
        obs_stations = self.fetch_observation_stations()
        self.station_ids = [s.station_id for s in obs_stations]
        for station in obs_stations:
            self.observations_producer.send_microsoft_open_data_us_noaa_nws_observation_station(
                station.station_id, station, flush_producer=False)
        self.kafka_producer.flush()
        print(f"Sent {len(obs_stations)} observation stations as reference data")

        last_obs_time = 0.0
        obs_seen: Dict[str, str] = {}  # station_id -> last observation timestamp

        while True:
            try:
                state = self.load_seen_alerts()
                seen_ids = set(state.get("seen_ids", []))
                features = self.poll_alerts()

                new_count = 0
                for feature in features:
                    props = feature.get("properties", {})
                    alert_id = props.get("id", "")

                    if not alert_id or alert_id in seen_ids:
                        continue

                    alert = WeatherAlert(
                        alert_id=alert_id,
                        area_desc=props.get("areaDesc", ""),
                        sent=props.get("sent", ""),
                        effective=props.get("effective", ""),
                        expires=props.get("expires", ""),
                        status=props.get("status", ""),
                        message_type=props.get("messageType", ""),
                        category=props.get("category", ""),
                        severity=props.get("severity", ""),
                        certainty=props.get("certainty", ""),
                        urgency=props.get("urgency", ""),
                        event=props.get("event", ""),
                        sender_name=props.get("senderName", ""),
                        headline=props.get("headline", ""),
                        description=props.get("description", "")
                    )

                    self.alerts_producer.send_microsoft_open_data_us_noaa_nws_weather_alert(
                        alert_id, alert, flush_producer=False)
                    seen_ids.add(alert_id)
                    new_count += 1

                if new_count > 0:
                    self.kafka_producer.flush()
                    print(f"Sent {new_count} new alert(s) to Kafka")

                # Keep only the last 10000 seen IDs to prevent unbounded growth
                seen_list = list(seen_ids)
                if len(seen_list) > 10000:
                    seen_list = seen_list[-10000:]
                state["seen_ids"] = seen_list
                self.save_seen_alerts(state)

                # Poll observations on a slower cadence
                now = time.time()
                if now - last_obs_time >= self.OBSERVATION_INTERVAL_SECONDS:
                    obs_count = 0
                    for sid in self.station_ids:
                        obs = self.fetch_latest_observation(sid)
                        if obs and obs.timestamp:
                            obs_key = f"{sid}:{obs.timestamp}"
                            if obs_seen.get(sid) != obs.timestamp:
                                self.observations_producer.send_microsoft_open_data_us_noaa_nws_weather_observation(
                                    sid, obs, flush_producer=False)
                                obs_count += 1
                                obs_seen[sid] = obs.timestamp
                    if obs_count > 0:
                        self.kafka_producer.flush()
                        print(f"Sent {obs_count} weather observation(s)")
                    last_obs_time = now

            except Exception as e:
                print(f"Error in polling loop: {e}")

            time.sleep(self.POLL_INTERVAL_SECONDS)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse an Azure Event Hubs-style connection string and extract Kafka parameters.

    Args:
        connection_string: The connection string.

    Returns:
        Dict with bootstrap.servers, kafka_topic, sasl.username, sasl.password.
    """
    config_dict = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                    '"').replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=')[1].strip('"')
            elif 'SharedAccessKeyName' in part:
                config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part:
                config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if 'sasl.username' in config_dict:
        config_dict['security.protocol'] = 'SASL_SSL'
        config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict


def main():
    """
    Main function to parse arguments and start the NWS alert poller.
    """
    parser = argparse.ArgumentParser(description="NOAA NWS Weather Alerts Poller")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store seen alert IDs for deduplication")
    parser.add_argument('--kafka-bootstrap-servers', type=str,
                        help="Comma separated list of Kafka bootstrap servers")
    parser.add_argument('--kafka-topic', type=str,
                        help="Kafka topic to send messages to")
    parser.add_argument('--sasl-username', type=str,
                        help="Username for SASL PLAIN authentication")
    parser.add_argument('--sasl-password', type=str,
                        help="Password for SASL PLAIN authentication")
    parser.add_argument('--connection-string', type=str,
                        help='Microsoft Event Hubs or Microsoft Fabric Event Stream connection string')

    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.last_polled_file:
        args.last_polled_file = os.getenv('NWS_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.nws_last_polled.json')

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = config_params.get('bootstrap.servers')
        kafka_topic = config_params.get('kafka_topic')
        sasl_username = config_params.get('sasl.username')
        sasl_password = config_params.get('sasl.password')
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided either through the command line or connection string.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided either through the command line or connection string.")
        sys.exit(1)
    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
    kafka_config = {
        'bootstrap.servers': kafka_bootstrap_servers,
    }
    if sasl_username and sasl_password:
        kafka_config.update({
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password
        })
    elif tls_enabled:
        kafka_config['security.protocol'] = 'SSL'

    poller = NWSAlertPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
