"""
NOAA NDBC Buoy Observations Poller
Polls the NDBC latest observations and sends them to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
import re
from typing import Dict, List, Optional
from datetime import datetime, timezone
import argparse
import requests
from noaa_ndbc.noaa_ndbc_producer.microsoft.opendata.us.noaa.ndbc.buoyobservation import BuoyObservation
from noaa_ndbc.noaa_ndbc_producer.microsoft.opendata.us.noaa.ndbc.buoystation import BuoyStation
from .noaa_ndbc_producer.producer_client import MicrosoftOpenDataUSNOAANDBCEventProducer


def parse_float(value: str) -> Optional[float]:
    """
    Parse a float value from NDBC text data.
    Returns None if the value is "MM" (missing measurement).

    Args:
        value: The string value to parse.

    Returns:
        The float value, or None if missing.
    """
    if value is None or value.strip() == "MM" or value.strip() == "":
        return None
    try:
        return float(value.strip())
    except (ValueError, TypeError):
        return None


class NDBCBuoyPoller:
    """
    Polls the NDBC latest observations endpoint and sends buoy observations
    to Kafka as CloudEvents.
    """
    LATEST_OBS_URL = "https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt"
    STATION_TABLE_URL = "https://www.ndbc.noaa.gov/data/stations/station_table.txt"
    POLL_INTERVAL_SECONDS = 300  # NDBC data updates every ~5 minutes

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str):
        """
        Initialize the NDBCBuoyPoller.

        Args:
            kafka_config: Kafka configuration settings.
            kafka_topic: Kafka topic to send messages to.
            last_polled_file: File to store last seen timestamps per station.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        from confluent_kafka import Producer
        kafka_producer = Producer(kafka_config)
        self.producer = MicrosoftOpenDataUSNOAANDBCEventProducer(kafka_producer, kafka_topic)

    @staticmethod
    def parse_station_location(location: str) -> tuple:
        """
        Parse latitude and longitude from the NDBC station table LOCATION field.

        The format is typically "lat N lon W (deg)" or "lat S lon E (deg)".
        For example: "44.794 N 87.313 W" yields (44.794, -87.313).

        Args:
            location: The LOCATION field string from the station table.

        Returns:
            Tuple of (latitude, longitude) in decimal degrees, or (None, None) on failure.
        """
        try:
            # Remove parenthetical notes like "(deg min sec)" or "(approx)"
            clean = re.sub(r'\([^)]*\)', '', location).strip()
            parts = clean.split()
            if len(parts) < 4:
                return None, None
            lat = float(parts[0])
            lat_dir = parts[1].upper()
            lon = float(parts[2])
            lon_dir = parts[3].upper()
            if lat_dir == 'S':
                lat = -lat
            if lon_dir == 'W':
                lon = -lon
            return lat, lon
        except (ValueError, IndexError):
            return None, None

    def fetch_stations(self) -> List[BuoyStation]:
        """
        Fetch the NDBC station table and parse it into BuoyStation objects.

        Returns:
            List of BuoyStation dataclass instances.
        """
        try:
            response = requests.get(self.STATION_TABLE_URL, timeout=60)
            response.raise_for_status()
        except Exception as err:
            print(f"Error fetching NDBC station table: {err}")
            return []

        stations = []
        for line in response.text.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            fields = [f.strip() for f in line.split('|')]
            if len(fields) < 7:
                continue
            try:
                station_id = fields[0]
                owner = fields[1] if len(fields) > 1 else ""
                station_type = fields[2] if len(fields) > 2 else ""
                hull = fields[3] if len(fields) > 3 else ""
                name = fields[4] if len(fields) > 4 else ""
                location_str = fields[6] if len(fields) > 6 else ""
                tz = fields[7] if len(fields) > 7 else ""
                lat, lon = self.parse_station_location(location_str)
                stations.append(BuoyStation(
                    station_id=station_id,
                    owner=owner,
                    station_type=station_type,
                    hull=hull,
                    name=name,
                    latitude=lat if lat is not None else 0.0,
                    longitude=lon if lon is not None else 0.0,
                    timezone=tz,
                ))
            except (IndexError, ValueError):
                continue
        return stations

    def load_state(self) -> Dict:
        """
        Load the last seen timestamps per station from the state file.

        Returns:
            Dict mapping station IDs to their last seen ISO timestamps.
        """
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {"last_timestamps": {}}

    def save_state(self, state: Dict):
        """
        Save the last seen timestamps per station to the state file.

        Args:
            state: Dict mapping station IDs to their last seen ISO timestamps.
        """
        try:
            os.makedirs(os.path.dirname(self.last_polled_file) if os.path.dirname(self.last_polled_file) else '.', exist_ok=True)
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Error saving state: {e}")

    def parse_observations(self, text: str) -> List[BuoyObservation]:
        """
        Parse the fixed-width text format from latest_obs.txt.

        The first two lines are headers (column names and units).
        Each subsequent line is a station observation. Fields are
        whitespace-separated. Missing values are represented as "MM".

        Args:
            text: The raw text response from the NDBC API.

        Returns:
            List of BuoyObservation dataclass instances.
        """
        lines = text.strip().split('\n')
        if len(lines) < 3:
            return []

        # First line is column headers, second is units – skip both
        # Columns: #STN  LAT    LON   YYYY MM DD hh mm WDIR WSPD GST  WVHT  DPD   APD MWD  PRES  PTDY  ATMP  WTMP  DEWP  VIS  TIDE
        observations = []
        for line in lines[2:]:
            line = line.strip()
            if not line:
                continue

            parts = re.split(r'\s+', line)
            # We need at least the station ID + lat + lon + date/time fields (8 fields)
            if len(parts) < 8:
                continue

            try:
                station_id = parts[0].lstrip('#')
                lat = parse_float(parts[1])
                lon = parse_float(parts[2])

                if lat is None or lon is None:
                    continue

                # Build ISO timestamp from YYYY MM DD hh mm
                year = parts[3]
                month = parts[4]
                day = parts[5]
                hour = parts[6]
                minute = parts[7]

                try:
                    dt = datetime(int(year), int(month), int(day),
                                  int(hour), int(minute), tzinfo=timezone.utc)
                    timestamp = dt.isoformat()
                except (ValueError, IndexError):
                    continue

                # Parse optional fields (may not exist if line is short)
                wind_direction = parse_float(parts[8]) if len(parts) > 8 else None
                wind_speed = parse_float(parts[9]) if len(parts) > 9 else None
                gust = parse_float(parts[10]) if len(parts) > 10 else None
                wave_height = parse_float(parts[11]) if len(parts) > 11 else None
                dominant_wave_period = parse_float(parts[12]) if len(parts) > 12 else None
                average_wave_period = parse_float(parts[13]) if len(parts) > 13 else None
                mean_wave_direction = parse_float(parts[14]) if len(parts) > 14 else None
                pressure = parse_float(parts[15]) if len(parts) > 15 else None
                # parts[16] is PTDY (pressure tendency) – not in our schema
                air_temperature = parse_float(parts[17]) if len(parts) > 17 else None
                water_temperature = parse_float(parts[18]) if len(parts) > 18 else None
                dewpoint = parse_float(parts[19]) if len(parts) > 19 else None
                # parts[20] is VIS, parts[21] is TIDE – not in our schema

                obs = BuoyObservation(
                    station_id=station_id,
                    latitude=lat,
                    longitude=lon,
                    timestamp=timestamp,
                    wind_direction=wind_direction if wind_direction is not None else 0.0,
                    wind_speed=wind_speed if wind_speed is not None else 0.0,
                    gust=gust if gust is not None else 0.0,
                    wave_height=wave_height if wave_height is not None else 0.0,
                    dominant_wave_period=dominant_wave_period if dominant_wave_period is not None else 0.0,
                    average_wave_period=average_wave_period if average_wave_period is not None else 0.0,
                    mean_wave_direction=mean_wave_direction if mean_wave_direction is not None else 0.0,
                    pressure=pressure if pressure is not None else 0.0,
                    air_temperature=air_temperature if air_temperature is not None else 0.0,
                    water_temperature=water_temperature if water_temperature is not None else 0.0,
                    dewpoint=dewpoint if dewpoint is not None else 0.0,
                )
                observations.append(obs)
            except (IndexError, ValueError):
                continue

        return observations

    def poll_observations(self) -> List[BuoyObservation]:
        """
        Fetch latest observations from the NDBC API and parse them.

        Returns:
            List of BuoyObservation dataclass instances.
        """
        try:
            response = requests.get(self.LATEST_OBS_URL, timeout=60)
            response.raise_for_status()
            return self.parse_observations(response.text)
        except Exception as err:
            print(f"Error fetching NDBC observations: {err}")
            return []

    def poll_and_send(self):
        """
        Main polling loop. Fetches buoy observations, deduplicates by
        station timestamp, and sends new observations to Kafka as CloudEvents.
        Polls every POLL_INTERVAL_SECONDS (300s / 5 min).
        """
        print(f"Starting NDBC Buoy Observation poller, polling every {self.POLL_INTERVAL_SECONDS}s")
        print(f"  Observations URL: {self.LATEST_OBS_URL}")
        print(f"  Kafka topic: {self.kafka_topic}")

        # Send reference data (buoy stations) at startup
        print("Sending NDBC buoy stations as reference data...")
        stations = self.fetch_stations()
        for station in stations:
            self.producer.send_microsoft_open_data_us_noaa_ndbc_buoy_station(
                station, flush_producer=False)
        self.producer.producer.flush()
        print(f"Sent {len(stations)} buoy stations as reference data")

        while True:
            try:
                state = self.load_state()
                last_timestamps = state.get("last_timestamps", {})
                observations = self.poll_observations()

                new_count = 0
                for obs in observations:
                    # Skip if we've already seen this station's timestamp
                    if obs.station_id in last_timestamps and last_timestamps[obs.station_id] == obs.timestamp:
                        continue

                    self.producer.send_microsoft_open_data_us_noaa_ndbc_buoy_observation(
                        obs, obs.station_id, flush_producer=False)
                    last_timestamps[obs.station_id] = obs.timestamp
                    new_count += 1

                if new_count > 0:
                    self.producer.producer.flush()
                    print(f"Sent {new_count} new observation(s) to Kafka")

                # Limit state size: keep only stations seen in this cycle
                station_ids_this_cycle = {obs.station_id for obs in observations}
                last_timestamps = {k: v for k, v in last_timestamps.items() if k in station_ids_this_cycle}
                state["last_timestamps"] = last_timestamps
                self.save_state(state)

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
    Main function to parse arguments and start the NDBC buoy observation poller.
    """
    parser = argparse.ArgumentParser(description="NOAA NDBC Buoy Observations Poller")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store last seen timestamps per station")
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
        args.last_polled_file = os.getenv('NDBC_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.ndbc_last_polled.json')

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
    kafka_config = {
        'bootstrap.servers': kafka_bootstrap_servers,
    }
    if sasl_username and sasl_password:
        kafka_config.update({
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password
        })

    poller = NDBCBuoyPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
