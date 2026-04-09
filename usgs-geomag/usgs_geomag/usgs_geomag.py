"""
USGS Geomagnetism Program Bridge
Polls the USGS geomagnetic web-service for 1-minute variation data from
US observatories and sends readings to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
from typing import Dict, List, Optional
from datetime import datetime, timezone, timedelta
import argparse
import requests
from usgs_geomag_producer_data import Observatory, MagneticFieldReading
from usgs_geomag_producer_kafka_producer.producer import GovUsgsGeomagEventProducer

# Observatories to poll (USGS-operated, non-test stations)
DEFAULT_OBSERVATORIES = [
    "BOU", "BRW", "BSL", "CMO", "DED", "FRD", "FRN",
    "GUA", "HON", "NEW", "SHU", "SIT", "SJG", "TUC",
]

OBSERVATORIES_URL = "https://geomag.usgs.gov/ws/observatories/"
DATA_URL = "https://geomag.usgs.gov/ws/data/"
POLL_INTERVAL_SECONDS = 300
REFERENCE_REFRESH_HOURS = 12


class USGSGeomagPoller:
    """
    Polls the USGS Geomagnetism web-service for 1-minute variation data
    and emits Observatory reference events and MagneticFieldReading telemetry.
    """

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str,
                 last_polled_file: str, observatories: Optional[List[str]] = None):
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        self.observatories = observatories or DEFAULT_OBSERVATORIES
        from confluent_kafka import Producer
        kafka_producer = Producer(kafka_config)
        self.producer = GovUsgsGeomagEventProducer(kafka_producer, kafka_topic)

    def load_state(self) -> Dict:
        """Load persisted state from disk."""
        try:
            with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                if isinstance(state, dict):
                    state.setdefault("last_timestamps", {})
                    state.setdefault("last_reference_emit", None)
                    return state
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return {"last_timestamps": {}, "last_reference_emit": None}

    def save_state(self, state: Dict):
        """Persist state to disk."""
        try:
            os.makedirs(os.path.dirname(self.last_polled_file) or '.', exist_ok=True)
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(state, f)
        except OSError as err:
            print(f"Warning: could not save state: {err}")

    @staticmethod
    def fetch_observatories() -> List[Dict]:
        """
        Fetch the GeoJSON FeatureCollection of observatories.

        Returns:
            List of observatory feature dicts from the API.
        """
        try:
            response = requests.get(OBSERVATORIES_URL, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data.get("features", [])
        except Exception as err:
            print(f"Error fetching observatories: {err}")
            return []

    @staticmethod
    def parse_observatory(feature: Dict) -> Observatory:
        """Convert a GeoJSON feature to an Observatory data class."""
        props = feature.get("properties", {})
        coords = feature.get("geometry", {}).get("coordinates", [None, None, None])
        longitude = coords[0] if len(coords) > 0 else None
        latitude = coords[1] if len(coords) > 1 else None
        elevation = coords[2] if len(coords) > 2 else None
        return Observatory(
            iaga_code=feature.get("id", ""),
            name=props.get("name", ""),
            agency=props.get("agency"),
            agency_name=props.get("agency_name"),
            latitude=latitude,
            longitude=longitude,
            elevation=elevation,
            sensor_orientation=props.get("sensor_orientation"),
            sensor_sampling_rate=props.get("sensor_sampling_rate"),
            declination_base=props.get("declination_base"),
        )

    @staticmethod
    def fetch_variation_data(iaga_code: str, start_time: str, end_time: str) -> Optional[Dict]:
        """
        Fetch 1-minute variation data for one observatory.

        Args:
            iaga_code: Observatory IAGA code.
            start_time: ISO 8601 start time.
            end_time: ISO 8601 end time.

        Returns:
            Parsed JSON response dict, or None on failure.
        """
        params = {
            "id": iaga_code,
            "type": "variation",
            "elements": "H,D,Z,F",
            "sampling_period": "60",
            "format": "json",
            "starttime": start_time,
            "endtime": end_time,
        }
        try:
            response = requests.get(DATA_URL, params=params, timeout=120)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            print(f"Error fetching data for {iaga_code}: {err}")
            return None

    @staticmethod
    def parse_timeseries(iaga_code: str, data: Dict) -> List[MagneticFieldReading]:
        """
        Transform the parallel-array timeseries response into individual readings.

        The API returns:
            times: ["2024-01-01T00:00:00.000Z", ...]
            values: [{id: "H", values: [...]}, {id: "D", values: [...]}, ...]

        We zip these into per-timestamp MagneticFieldReading objects.
        """
        times = data.get("times", [])
        values_list = data.get("values", [])
        if not times:
            return []

        element_map: Dict[str, List] = {}
        for element_block in values_list:
            elem_id = element_block.get("id", "").upper()
            elem_values = element_block.get("values", [])
            element_map[elem_id] = elem_values

        readings = []
        for i, time_str in enumerate(times):
            try:
                ts = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                continue

            def _get_value(element: str, index: int) -> Optional[float]:
                vals = element_map.get(element, [])
                if index < len(vals) and vals[index] is not None:
                    return float(vals[index])
                return None

            reading = MagneticFieldReading(
                iaga_code=iaga_code,
                timestamp=ts,
                h=_get_value("H", i),
                d=_get_value("D", i),
                z=_get_value("Z", i),
                f=_get_value("F", i),
            )
            readings.append(reading)
        return readings

    def emit_reference_data(self, observatory_ids: Optional[List[str]] = None):
        """Fetch and emit observatory reference data."""
        features = self.fetch_observatories()
        count = 0
        for feature in features:
            obs = self.parse_observatory(feature)
            if observatory_ids and obs.iaga_code not in observatory_ids:
                continue
            self.producer.send_gov_usgs_geomag_observatory(
                obs.iaga_code, obs, flush_producer=False)
            count += 1
        self.producer.producer.flush()
        print(f"Sent {count} observatory reference events")

    def poll_and_send(self, once: bool = False):
        """
        Main polling loop. Emits reference data at startup, then polls
        each observatory for new 1-minute variation data.

        Args:
            once: Run one poll iteration and return. Intended for tests.
        """
        print(f"Starting USGS Geomagnetism poller, polling every {POLL_INTERVAL_SECONDS}s")
        print(f"  Observatories: {', '.join(self.observatories)}")
        print(f"  Kafka topic: {self.kafka_topic}")

        state = self.load_state()

        # Emit reference data at startup
        print("Sending observatory reference data...")
        self.emit_reference_data(self.observatories)
        state["last_reference_emit"] = datetime.now(timezone.utc).isoformat()

        while True:
            try:
                last_timestamps = state.get("last_timestamps", {})

                # Check if reference data needs refresh
                last_ref = state.get("last_reference_emit")
                if last_ref:
                    try:
                        last_ref_dt = datetime.fromisoformat(last_ref)
                        if datetime.now(timezone.utc) - last_ref_dt > timedelta(hours=REFERENCE_REFRESH_HOURS):
                            print("Refreshing observatory reference data...")
                            self.emit_reference_data(self.observatories)
                            state["last_reference_emit"] = datetime.now(timezone.utc).isoformat()
                    except (ValueError, TypeError):
                        pass

                # Determine time window: last 10 minutes or since last poll
                now = datetime.now(timezone.utc)
                end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
                default_start = (now - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")

                new_count = 0
                for iaga_code in self.observatories:
                    start_time = last_timestamps.get(iaga_code, default_start)
                    data = self.fetch_variation_data(iaga_code, start_time, end_time)
                    if data is None:
                        continue

                    readings = self.parse_timeseries(iaga_code, data)
                    latest_ts = last_timestamps.get(iaga_code)

                    for reading in readings:
                        reading_ts = reading.timestamp.isoformat()
                        # Deduplicate by observatory + timestamp
                        if latest_ts and reading_ts <= latest_ts:
                            continue
                        self.producer.send_gov_usgs_geomag_magnetic_field_reading(
                            reading.iaga_code, reading, flush_producer=False)
                        new_count += 1
                        latest_ts = reading_ts

                    if latest_ts:
                        last_timestamps[iaga_code] = latest_ts

                if new_count > 0:
                    self.producer.producer.flush()
                    print(f"Sent {new_count} new magnetic field reading(s) to Kafka")

                state["last_timestamps"] = last_timestamps
                self.save_state(state)

            except Exception as e:
                print(f"Error in polling loop: {e}")

            if once:
                break

            time.sleep(POLL_INTERVAL_SECONDS)


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
    """Main function to parse arguments and start the USGS Geomagnetism poller."""
    parser = argparse.ArgumentParser(description="USGS Geomagnetism Program Bridge")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store last seen timestamps per observatory")
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
    parser.add_argument('--observatories', type=str,
                        help='Comma-separated list of IAGA observatory codes to poll (default: all USGS)')

    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.last_polled_file:
        args.last_polled_file = os.getenv('GEOMAG_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.usgs_geomag_last_polled.json')

    observatories = None
    obs_env = os.getenv('GEOMAG_OBSERVATORIES')
    if args.observatories:
        observatories = [o.strip() for o in args.observatories.split(',')]
    elif obs_env:
        observatories = [o.strip() for o in obs_env.split(',')]

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

    poller = USGSGeomagPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file,
        observatories=observatories
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
