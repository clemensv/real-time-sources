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
from noaa_ndbc_producer_data import BuoyDartMeasurement
from noaa_ndbc_producer_data import BuoyObservation
from noaa_ndbc_producer_data import BuoyOceanographicObservation
from noaa_ndbc_producer_data import BuoySolarRadiationObservation
from noaa_ndbc_producer_data import BuoyStation
from noaa_ndbc_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAANDBCEventProducer


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
    REALTIME2_INDEX_URL = "https://www.ndbc.noaa.gov/data/realtime2/"
    REALTIME2_EXTENSIONS = ("srad", "ocean", "dart")
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

    @classmethod
    def _empty_state(cls) -> Dict:
        """
        Return the default persisted state shape.

        Returns:
            Dict containing latest observation timestamps and realtime2 family state.
        """
        return {
            "last_timestamps": {},
            "latest_obs": {},
            "realtime2": {extension: {} for extension in cls.REALTIME2_EXTENSIONS},
        }

    @classmethod
    def _normalize_state(cls, state: Optional[Dict]) -> Dict:
        """
        Normalize persisted state and preserve backward compatibility with the
        legacy last_timestamps-only format.

        Args:
            state: Raw state loaded from disk.

        Returns:
            Normalized state dictionary.
        """
        normalized = cls._empty_state()
        if not isinstance(state, dict):
            return normalized

        latest_obs = state.get("latest_obs", state.get("last_timestamps", {}))
        if isinstance(latest_obs, dict):
            normalized["latest_obs"].update(latest_obs)

        realtime2 = state.get("realtime2", {})
        if isinstance(realtime2, dict):
            for extension in cls.REALTIME2_EXTENSIONS:
                family_state = realtime2.get(extension, {})
                if isinstance(family_state, dict):
                    normalized["realtime2"][extension].update(family_state)

        normalized["last_timestamps"] = dict(normalized["latest_obs"])
        return normalized

    @staticmethod
    def parse_timestamp(parts: List[str], include_seconds: bool = False) -> Optional[str]:
        """
        Parse a UTC timestamp from split NDBC date/time columns.

        Args:
            parts: Timestamp columns beginning with year.
            include_seconds: Whether the timestamp includes a seconds column.

        Returns:
            ISO 8601 UTC timestamp string, or None on failure.
        """
        expected_parts = 6 if include_seconds else 5
        if len(parts) < expected_parts:
            return None

        try:
            if include_seconds:
                dt = datetime(
                    int(parts[0]),
                    int(parts[1]),
                    int(parts[2]),
                    int(parts[3]),
                    int(parts[4]),
                    int(parts[5]),
                    tzinfo=timezone.utc,
                )
            else:
                dt = datetime(
                    int(parts[0]),
                    int(parts[1]),
                    int(parts[2]),
                    int(parts[3]),
                    int(parts[4]),
                    tzinfo=timezone.utc,
                )
        except ValueError:
            return None

        return dt.isoformat()

    @staticmethod
    def iter_data_rows(text: str):
        """
        Yield parsed data rows from an NDBC text product.

        Args:
            text: Raw text file content.

        Yields:
            Whitespace-split data rows, excluding comments and blank lines.
        """
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            yield re.split(r'\s+', line)

    def parse_realtime2_file_index(self, text: str) -> Dict[str, List[str]]:
        """
        Parse the realtime2 directory listing and group station IDs by family.

        Args:
            text: Directory listing HTML.

        Returns:
            Dict mapping family extensions to sorted station ID lists.
        """
        station_ids = {extension: set() for extension in self.REALTIME2_EXTENSIONS}
        for match in re.finditer(r'href="([^"]+)\.(srad|ocean|dart)"', text, re.IGNORECASE):
            station_id = match.group(1)
            extension = match.group(2).lower()
            station_ids[extension].add(station_id)

        return {
            extension: sorted(values)
            for extension, values in station_ids.items()
        }

    def fetch_realtime2_file_index(self) -> Dict[str, List[str]]:
        """
        Fetch the realtime2 directory index and discover available families.

        Returns:
            Dict mapping family extensions to station ID lists.
        """
        try:
            response = requests.get(self.REALTIME2_INDEX_URL, timeout=60)
            response.raise_for_status()
            return self.parse_realtime2_file_index(response.text)
        except Exception as err:
            print(f"Error fetching NDBC realtime2 index: {err}")
            return {extension: [] for extension in self.REALTIME2_EXTENSIONS}

    def fetch_realtime2_product(self, station_id: str, extension: str) -> Optional[str]:
        """
        Fetch a station-scoped realtime2 product file.

        Args:
            station_id: NDBC station identifier.
            extension: Product family suffix such as srad, ocean, or dart.

        Returns:
            Raw file text, or None on failure.
        """
        try:
            response = requests.get(f"{self.REALTIME2_INDEX_URL}{station_id}.{extension}", timeout=60)
            response.raise_for_status()
            return response.text
        except Exception as err:
            print(f"Error fetching NDBC realtime2 product {station_id}.{extension}: {err}")
            return None

    def parse_solar_radiation_observation(self, station_id: str, text: str) -> Optional[BuoySolarRadiationObservation]:
        """
        Parse the newest solar radiation observation for one station.

        Args:
            station_id: NDBC station identifier.
            text: Raw .srad file content.

        Returns:
            Parsed solar radiation observation, or None if no valid row exists.
        """
        for parts in self.iter_data_rows(text):
            if len(parts) < 8:
                continue
            timestamp = self.parse_timestamp(parts[:5])
            if timestamp is None:
                continue

            return BuoySolarRadiationObservation(
                station_id=station_id,
                timestamp=timestamp,
                shortwave_radiation_licor=parse_float(parts[5]),
                shortwave_radiation_eppley=parse_float(parts[6]),
                longwave_radiation=parse_float(parts[7]),
            )

        return None

    def parse_oceanographic_observation(self, station_id: str, text: str) -> Optional[BuoyOceanographicObservation]:
        """
        Parse the newest oceanographic observation for one station.

        Args:
            station_id: NDBC station identifier.
            text: Raw .ocean file content.

        Returns:
            Parsed oceanographic observation, or None if no valid row exists.
        """
        for parts in self.iter_data_rows(text):
            if len(parts) < 15:
                continue
            timestamp = self.parse_timestamp(parts[:5])
            if timestamp is None:
                continue

            depth = parse_float(parts[5])
            if depth is None:
                continue

            return BuoyOceanographicObservation(
                station_id=station_id,
                timestamp=timestamp,
                depth=depth,
                ocean_temperature=parse_float(parts[6]),
                conductivity=parse_float(parts[7]),
                salinity=parse_float(parts[8]),
                oxygen_saturation=parse_float(parts[9]),
                oxygen_concentration=parse_float(parts[10]),
                chlorophyll_concentration=parse_float(parts[11]),
                turbidity=parse_float(parts[12]),
                ph=parse_float(parts[13]),
                redox_potential=parse_float(parts[14]),
            )

        return None

    def parse_dart_measurement(self, station_id: str, text: str) -> Optional[BuoyDartMeasurement]:
        """
        Parse the newest DART measurement for one station.

        Args:
            station_id: NDBC station identifier.
            text: Raw .dart file content.

        Returns:
            Parsed DART measurement, or None if no valid row exists.
        """
        for parts in self.iter_data_rows(text):
            if len(parts) < 8:
                continue
            timestamp = self.parse_timestamp(parts[:6], include_seconds=True)
            if timestamp is None:
                continue

            water_column_height = parse_float(parts[7])
            if water_column_height is None:
                continue

            try:
                measurement_type_code = int(parts[6])
            except ValueError:
                continue

            return BuoyDartMeasurement(
                station_id=station_id,
                timestamp=timestamp,
                measurement_type_code=measurement_type_code,
                water_column_height=water_column_height,
            )

        return None

    def poll_solar_radiation_observations(self, station_ids: List[str]) -> List[BuoySolarRadiationObservation]:
        """
        Fetch the newest solar radiation observation for each station in the index.

        Args:
            station_ids: Station IDs with available .srad files.

        Returns:
            Parsed solar radiation observations.
        """
        observations = []
        for station_id in station_ids:
            text = self.fetch_realtime2_product(station_id, "srad")
            if text is None:
                continue
            observation = self.parse_solar_radiation_observation(station_id, text)
            if observation is not None:
                observations.append(observation)
        return observations

    def poll_oceanographic_observations(self, station_ids: List[str]) -> List[BuoyOceanographicObservation]:
        """
        Fetch the newest oceanographic observation for each station in the index.

        Args:
            station_ids: Station IDs with available .ocean files.

        Returns:
            Parsed oceanographic observations.
        """
        observations = []
        for station_id in station_ids:
            text = self.fetch_realtime2_product(station_id, "ocean")
            if text is None:
                continue
            observation = self.parse_oceanographic_observation(station_id, text)
            if observation is not None:
                observations.append(observation)
        return observations

    def poll_dart_measurements(self, station_ids: List[str]) -> List[BuoyDartMeasurement]:
        """
        Fetch the newest DART measurement for each station in the index.

        Args:
            station_ids: Station IDs with available .dart files.

        Returns:
            Parsed DART measurements.
        """
        measurements = []
        for station_id in station_ids:
            text = self.fetch_realtime2_product(station_id, "dart")
            if text is None:
                continue
            measurement = self.parse_dart_measurement(station_id, text)
            if measurement is not None:
                measurements.append(measurement)
        return measurements

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
                    return self._normalize_state(json.load(f))
        except Exception:
            pass
        return self._empty_state()

    def save_state(self, state: Dict):
        """
        Save the last seen timestamps per station to the state file.

        Args:
            state: Dict mapping station IDs to their last seen ISO timestamps.
        """
        state_to_save = self._normalize_state(state)
        try:
            os.makedirs(os.path.dirname(self.last_polled_file) if os.path.dirname(self.last_polled_file) else '.', exist_ok=True)
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(state_to_save, f, indent=2)
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
                pressure_tendency = parse_float(parts[16]) if len(parts) > 16 else None
                air_temperature = parse_float(parts[17]) if len(parts) > 17 else None
                water_temperature = parse_float(parts[18]) if len(parts) > 18 else None
                dewpoint = parse_float(parts[19]) if len(parts) > 19 else None
                visibility = parse_float(parts[20]) if len(parts) > 20 else None
                tide = parse_float(parts[21]) if len(parts) > 21 else None

                obs = BuoyObservation(
                    station_id=station_id,
                    latitude=lat,
                    longitude=lon,
                    timestamp=timestamp,
                    wind_direction=wind_direction,
                    wind_speed=wind_speed,
                    gust=gust,
                    wave_height=wave_height,
                    dominant_wave_period=dominant_wave_period,
                    average_wave_period=average_wave_period,
                    mean_wave_direction=mean_wave_direction,
                    pressure=pressure,
                    air_temperature=air_temperature,
                    water_temperature=water_temperature,
                    dewpoint=dewpoint,
                    pressure_tendency=pressure_tendency,
                    visibility=visibility,
                    tide=tide,
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

    def poll_and_send(self, once: bool = False):
        """
        Main polling loop. Fetches buoy observations, deduplicates by
        station timestamp, and sends new observations to Kafka as CloudEvents.

        Args:
            once: Run one poll iteration and return. Intended for tests.
        """
        print(f"Starting NDBC Buoy Observation poller, polling every {self.POLL_INTERVAL_SECONDS}s")
        print(f"  Observations URL: {self.LATEST_OBS_URL}")
        print(f"  Realtime2 index URL: {self.REALTIME2_INDEX_URL}")
        print(f"  Kafka topic: {self.kafka_topic}")

        # Send reference data (buoy stations) at startup
        print("Sending NDBC buoy stations as reference data...")
        stations = self.fetch_stations()
        for station in stations:
            self.producer.send_microsoft_open_data_us_noaa_ndbc_buoy_station(
                station.station_id, station, flush_producer=False)
        self.producer.producer.flush()
        print(f"Sent {len(stations)} buoy stations as reference data")

        while True:
            try:
                state = self.load_state()
                last_timestamps = state.get("latest_obs", {})
                realtime2_state = state.get("realtime2", {})
                solar_radiation_timestamps = realtime2_state.get("srad", {})
                oceanographic_timestamps = realtime2_state.get("ocean", {})
                dart_timestamps = realtime2_state.get("dart", {})

                observations = self.poll_observations()
                realtime2_file_index = self.fetch_realtime2_file_index()
                solar_radiation_observations = self.poll_solar_radiation_observations(realtime2_file_index.get("srad", []))
                oceanographic_observations = self.poll_oceanographic_observations(realtime2_file_index.get("ocean", []))
                dart_measurements = self.poll_dart_measurements(realtime2_file_index.get("dart", []))

                new_count = 0
                for obs in observations:
                    # Skip if we've already seen this station's timestamp
                    if obs.station_id in last_timestamps and last_timestamps[obs.station_id] == obs.timestamp:
                        continue

                    self.producer.send_microsoft_open_data_us_noaa_ndbc_buoy_observation(
                        obs.station_id, obs, flush_producer=False)
                    last_timestamps[obs.station_id] = obs.timestamp
                    new_count += 1

                for observation in solar_radiation_observations:
                    if solar_radiation_timestamps.get(observation.station_id) == observation.timestamp:
                        continue

                    self.producer.send_microsoft_open_data_us_noaa_ndbc_buoy_solar_radiation_observation(
                        observation.station_id, observation, flush_producer=False)
                    solar_radiation_timestamps[observation.station_id] = observation.timestamp
                    new_count += 1

                for observation in oceanographic_observations:
                    if oceanographic_timestamps.get(observation.station_id) == observation.timestamp:
                        continue

                    self.producer.send_microsoft_open_data_us_noaa_ndbc_buoy_oceanographic_observation(
                        observation.station_id, observation, flush_producer=False)
                    oceanographic_timestamps[observation.station_id] = observation.timestamp
                    new_count += 1

                for measurement in dart_measurements:
                    if dart_timestamps.get(measurement.station_id) == measurement.timestamp:
                        continue

                    self.producer.send_microsoft_open_data_us_noaa_ndbc_buoy_dart_measurement(
                        measurement.station_id, measurement, flush_producer=False)
                    dart_timestamps[measurement.station_id] = measurement.timestamp
                    new_count += 1

                if new_count > 0:
                    self.producer.producer.flush()
                    print(f"Sent {new_count} new event(s) to Kafka")

                # Limit state size: keep only stations seen in this cycle
                station_ids_this_cycle = {obs.station_id for obs in observations}
                solar_station_ids_this_cycle = {observation.station_id for observation in solar_radiation_observations}
                ocean_station_ids_this_cycle = {observation.station_id for observation in oceanographic_observations}
                dart_station_ids_this_cycle = {measurement.station_id for measurement in dart_measurements}

                state["latest_obs"] = {k: v for k, v in last_timestamps.items() if k in station_ids_this_cycle}
                state["last_timestamps"] = dict(state["latest_obs"])
                state["realtime2"] = {
                    "srad": {k: v for k, v in solar_radiation_timestamps.items() if k in solar_station_ids_this_cycle},
                    "ocean": {k: v for k, v in oceanographic_timestamps.items() if k in ocean_station_ids_this_cycle},
                    "dart": {k: v for k, v in dart_timestamps.items() if k in dart_station_ids_this_cycle},
                }
                self.save_state(state)

            except Exception as e:
                print(f"Error in polling loop: {e}")

            if once:
                break

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

    poller = NDBCBuoyPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
