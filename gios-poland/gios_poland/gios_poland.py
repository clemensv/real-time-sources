"""
GIOŚ Poland Air Quality Poller
Polls the Polish Chief Inspectorate of Environmental Protection (GIOŚ) air quality API
and sends station metadata, sensor data, measurements, and air quality indices
to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import argparse
import requests
from gios_poland_producer_data import Station
from gios_poland_producer_data import Sensor
from gios_poland_producer_data import Measurement
from gios_poland_producer_data import AirQualityIndex
from gios_poland_producer_kafka_producer.producer import PlGovGiosAirqualityEventProducer


# Polish-to-English field mappings for each API endpoint
STATION_FIELD_MAP = {
    "Identyfikator stacji": "station_id",
    "Kod stacji": "station_code",
    "Nazwa stacji": "name",
    "WGS84 φ N": "latitude",
    "WGS84 λ E": "longitude",
    "Identyfikator miasta": "city_id",
    "Nazwa miasta": "city_name",
    "Gmina": "commune",
    "Powiat": "district",
    "Województwo": "voivodeship",
    "Ulica": "street",
}

SENSOR_FIELD_MAP = {
    "Identyfikator stanowiska": "sensor_id",
    "Identyfikator stacji": "station_id",
    "Wskaźnik": "parameter_name",
    "Wskaźnik - wzór": "parameter_formula",
    "Wskaźnik - kod": "parameter_code",
    "Id wskaźnika": "parameter_id",
}

MEASUREMENT_FIELD_MAP = {
    "Kod stanowiska": "sensor_code",
    "Data": "timestamp",
    "Wartość": "value",
}

AQI_FIELD_MAP = {
    "Identyfikator stacji pomiarowej": "station_id",
    "Data wykonania obliczeń indeksu": "calculation_timestamp",
    "Wartość indeksu": "index_value",
    "Nazwa kategorii indeksu": "index_category",
    "Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika st": "source_data_timestamp",
    "Data wykonania obliczeń indeksu dla wskaźnika SO2": "so2_calculation_timestamp",
    "Wartość indeksu dla wskaźnika SO2": "so2_index_value",
    "Nazwa kategorii indeksu dla wskażnika SO2": "so2_index_category",
    "Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika SO2": "so2_source_data_timestamp",
    "Data wykonania obliczeń indeksu dla wskaźnika NO2": "no2_calculation_timestamp",
    "Wartość indeksu dla wskaźnika NO2": "no2_index_value",
    "Nazwa kategorii indeksu dla wskażnika NO2": "no2_index_category",
    "Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika NO2": "no2_source_data_timestamp",
    "Data wykonania obliczeń indeksu dla wskaźnika PM10": "pm10_calculation_timestamp",
    "Wartość indeksu dla wskaźnika PM10": "pm10_index_value",
    "Nazwa kategorii indeksu dla wskażnika PM10": "pm10_index_category",
    "Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika PM10": "pm10_source_data_timestamp",
    "Data wykonania obliczeń indeksu dla wskaźnika PM2.5": "pm25_calculation_timestamp",
    "Wartość indeksu dla wskaźnika PM2.5": "pm25_index_value",
    "Nazwa kategorii indeksu dla wskażnika PM2.5": "pm25_index_category",
    "Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika PM2.5": "pm25_source_data_timestamp",
    "Data wykonania obliczeń indeksu dla wskaźnika O3": "o3_calculation_timestamp",
    "Wartość indeksu dla wskaźnika O3": "o3_index_value",
    "Nazwa kategorii indeksu dla wskażnika O3": "o3_index_category",
    "Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika O3": "o3_source_data_timestamp",
    "Status indeksu ogólnego dla stacji pomiarowej": "overall_status",
    "Kod zanieczyszczenia krytycznego": "critical_pollutant_code",
}


def map_polish_fields(data: dict, field_map: dict) -> dict:
    """
    Map Polish field names from the GIOŚ API to English schema names.

    Args:
        data: Dictionary with Polish field names.
        field_map: Mapping from Polish to English field names.

    Returns:
        Dictionary with English field names.
    """
    result = {}
    for polish_key, english_key in field_map.items():
        if polish_key in data:
            result[english_key] = data[polish_key]
    return result


def parse_gios_timestamp(value) -> Optional[datetime]:
    """
    Parse a GIOŚ timestamp string in the format 'YYYY-MM-DD HH:MM:SS' or ISO format.

    Args:
        value: The timestamp string to parse, or None.

    Returns:
        Parsed datetime object, or None if the value is missing or invalid.
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    try:
        ts = str(value).strip()
        if not ts:
            return None
        return datetime.fromisoformat(ts.replace(' ', 'T'))
    except (ValueError, TypeError):
        return None


def parse_optional_float(value) -> Optional[float]:
    """
    Parse an optional float value from the GIOŚ API.

    Args:
        value: The value to parse.

    Returns:
        Float value, or None if missing or invalid.
    """
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def parse_optional_int(value) -> Optional[int]:
    """
    Parse an optional integer value from the GIOŚ API.

    Args:
        value: The value to parse.

    Returns:
        Integer value, or None if missing or invalid.
    """
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def parse_station(raw: dict) -> Optional[Station]:
    """
    Parse a raw station dictionary from the GIOŚ API into a Station dataclass.

    Args:
        raw: Dictionary with Polish field names from /station/findAll.

    Returns:
        Station dataclass instance, or None on failure.
    """
    mapped = map_polish_fields(raw, STATION_FIELD_MAP)
    try:
        return Station(
            station_id=int(mapped["station_id"]),
            station_code=str(mapped["station_code"]),
            name=str(mapped["name"]),
            latitude=parse_optional_float(mapped.get("latitude")),
            longitude=parse_optional_float(mapped.get("longitude")),
            city_id=parse_optional_int(mapped.get("city_id")),
            city_name=mapped.get("city_name"),
            commune=mapped.get("commune"),
            district=mapped.get("district"),
            voivodeship=mapped.get("voivodeship"),
            street=mapped.get("street"),
        )
    except (KeyError, ValueError, TypeError):
        return None


def parse_sensor(raw: dict) -> Optional[Sensor]:
    """
    Parse a raw sensor dictionary from the GIOŚ API into a Sensor dataclass.

    Args:
        raw: Dictionary with Polish field names from /station/sensors/{stationId}.

    Returns:
        Sensor dataclass instance, or None on failure.
    """
    mapped = map_polish_fields(raw, SENSOR_FIELD_MAP)
    try:
        return Sensor(
            sensor_id=int(mapped["sensor_id"]),
            station_id=int(mapped["station_id"]),
            parameter_name=str(mapped["parameter_name"]),
            parameter_formula=mapped.get("parameter_formula"),
            parameter_code=str(mapped["parameter_code"]),
            parameter_id=parse_optional_int(mapped.get("parameter_id")),
        )
    except (KeyError, ValueError, TypeError):
        return None


def parse_measurement(raw: dict, station_id: int, sensor_id: int) -> Optional[Measurement]:
    """
    Parse a raw measurement dictionary from the GIOŚ API into a Measurement dataclass.

    Args:
        raw: Dictionary with Polish field names from /data/getData/{sensorId}.
        station_id: Parent station ID.
        sensor_id: Sensor ID that produced this measurement.

    Returns:
        Measurement dataclass instance, or None on failure.
    """
    mapped = map_polish_fields(raw, MEASUREMENT_FIELD_MAP)
    try:
        timestamp = parse_gios_timestamp(mapped.get("timestamp"))
        if timestamp is None:
            return None
        return Measurement(
            station_id=station_id,
            sensor_id=sensor_id,
            sensor_code=str(mapped.get("sensor_code", "")),
            timestamp=timestamp,
            value=parse_optional_float(mapped.get("value")),
        )
    except (KeyError, ValueError, TypeError):
        return None


def parse_air_quality_index(raw: dict) -> Optional[AirQualityIndex]:
    """
    Parse a raw AQI dictionary from the GIOŚ API into an AirQualityIndex dataclass.

    Args:
        raw: Dictionary with Polish field names from /aqindex/getIndex/{stationId}.

    Returns:
        AirQualityIndex dataclass instance, or None on failure.
    """
    mapped = map_polish_fields(raw, AQI_FIELD_MAP)
    try:
        calc_ts = parse_gios_timestamp(mapped.get("calculation_timestamp"))
        if calc_ts is None:
            return None
        return AirQualityIndex(
            station_id=int(mapped["station_id"]),
            calculation_timestamp=calc_ts,
            index_value=parse_optional_int(mapped.get("index_value")),
            index_category=mapped.get("index_category"),
            source_data_timestamp=parse_gios_timestamp(mapped.get("source_data_timestamp")),
            so2_calculation_timestamp=parse_gios_timestamp(mapped.get("so2_calculation_timestamp")),
            so2_index_value=parse_optional_int(mapped.get("so2_index_value")),
            so2_index_category=mapped.get("so2_index_category"),
            so2_source_data_timestamp=parse_gios_timestamp(mapped.get("so2_source_data_timestamp")),
            no2_calculation_timestamp=parse_gios_timestamp(mapped.get("no2_calculation_timestamp")),
            no2_index_value=parse_optional_int(mapped.get("no2_index_value")),
            no2_index_category=mapped.get("no2_index_category"),
            no2_source_data_timestamp=parse_gios_timestamp(mapped.get("no2_source_data_timestamp")),
            pm10_calculation_timestamp=parse_gios_timestamp(mapped.get("pm10_calculation_timestamp")),
            pm10_index_value=parse_optional_int(mapped.get("pm10_index_value")),
            pm10_index_category=mapped.get("pm10_index_category"),
            pm10_source_data_timestamp=parse_gios_timestamp(mapped.get("pm10_source_data_timestamp")),
            pm25_calculation_timestamp=parse_gios_timestamp(mapped.get("pm25_calculation_timestamp")),
            pm25_index_value=parse_optional_int(mapped.get("pm25_index_value")),
            pm25_index_category=mapped.get("pm25_index_category"),
            pm25_source_data_timestamp=parse_gios_timestamp(mapped.get("pm25_source_data_timestamp")),
            o3_calculation_timestamp=parse_gios_timestamp(mapped.get("o3_calculation_timestamp")),
            o3_index_value=parse_optional_int(mapped.get("o3_index_value")),
            o3_index_category=mapped.get("o3_index_category"),
            o3_source_data_timestamp=parse_gios_timestamp(mapped.get("o3_source_data_timestamp")),
            overall_status=mapped.get("overall_status"),
            critical_pollutant_code=mapped.get("critical_pollutant_code"),
        )
    except (KeyError, ValueError, TypeError):
        return None


class GIOSPolandPoller:
    """
    Polls the GIOŚ air quality API and sends station metadata, sensor data,
    measurements, and air quality indices to Kafka as CloudEvents.
    """
    BASE_URL = "https://api.gios.gov.pl/pjp-api/v1/rest"
    POLL_INTERVAL_SECONDS = 3600  # GIOŚ data updates hourly
    REQUEST_DELAY = 0.05  # 50ms between requests (well within 1500 req/min)

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str):
        """
        Initialize the GIOSPolandPoller.

        Args:
            kafka_config: Kafka configuration settings.
            kafka_topic: Kafka topic to send messages to.
            last_polled_file: File to store last seen timestamps per sensor.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        from confluent_kafka import Producer
        kafka_producer = Producer(kafka_config)
        self.producer = PlGovGiosAirqualityEventProducer(kafka_producer, kafka_topic)

    def fetch_stations(self) -> List[Station]:
        """
        Fetch all monitoring stations from the GIOŚ API.

        Returns:
            List of Station dataclass instances.
        """
        try:
            response = requests.get(f"{self.BASE_URL}/station/findAll", timeout=60)
            response.raise_for_status()
            data = response.json()
            raw_stations = data.get("Lista stacji pomiarowych", [])
            if raw_stations is None:
                return []
            stations = []
            for raw in raw_stations:
                station = parse_station(raw)
                if station is not None:
                    stations.append(station)
            return stations
        except Exception as err:
            print(f"Error fetching GIOŚ stations: {err}")
            return []

    def fetch_sensors(self, station_id: int) -> List[Sensor]:
        """
        Fetch all sensors for a given station from the GIOŚ API.

        Args:
            station_id: The numeric station identifier.

        Returns:
            List of Sensor dataclass instances.
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/station/sensors/{station_id}", timeout=60)
            response.raise_for_status()
            data = response.json()
            raw_sensors = data.get("Lista stanowisk pomiarowych dla podanej stacji", [])
            if raw_sensors is None:
                return []
            sensors = []
            for raw in raw_sensors:
                sensor = parse_sensor(raw)
                if sensor is not None:
                    sensors.append(sensor)
            return sensors
        except Exception as err:
            print(f"Error fetching sensors for station {station_id}: {err}")
            return []

    def fetch_measurements(self, sensor_id: int) -> List[dict]:
        """
        Fetch measurement data for a given sensor from the GIOŚ API.

        Args:
            sensor_id: The numeric sensor identifier.

        Returns:
            List of raw measurement dictionaries.
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/data/getData/{sensor_id}", timeout=60)
            response.raise_for_status()
            data = response.json()
            raw_measurements = data.get("Lista danych pomiarowych", [])
            if raw_measurements is None:
                return []
            return raw_measurements
        except Exception as err:
            print(f"Error fetching measurements for sensor {sensor_id}: {err}")
            return []

    def fetch_air_quality_index(self, station_id: int) -> Optional[dict]:
        """
        Fetch the current air quality index for a given station.

        Args:
            station_id: The numeric station identifier.

        Returns:
            Raw AQI dictionary, or None on failure.
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/aqindex/getIndex/{station_id}", timeout=60)
            response.raise_for_status()
            data = response.json()
            return data.get("AqIndex")
        except Exception as err:
            print(f"Error fetching AQI for station {station_id}: {err}")
            return None

    def load_state(self) -> Dict:
        """
        Load the last seen timestamps per sensor from the state file.

        Returns:
            Dict with measurement_timestamps and aqi_timestamps.
        """
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    if isinstance(state, dict):
                        return {
                            "measurement_timestamps": state.get("measurement_timestamps", {}),
                            "aqi_timestamps": state.get("aqi_timestamps", {}),
                        }
        except Exception:
            pass
        return {"measurement_timestamps": {}, "aqi_timestamps": {}}

    def save_state(self, state: Dict):
        """
        Save the last seen timestamps to the state file.

        Args:
            state: Dict with measurement_timestamps and aqi_timestamps.
        """
        try:
            state_dir = os.path.dirname(self.last_polled_file)
            if state_dir:
                os.makedirs(state_dir, exist_ok=True)
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Error saving state: {e}")

    def poll_and_send(self, once: bool = False):
        """
        Main polling loop. Fetches stations, sensors, measurements, and AQI data,
        deduplicates by timestamp, and sends new events to Kafka as CloudEvents.

        Args:
            once: Run one poll iteration and return. Intended for tests.
        """
        print(f"Starting GIOŚ Poland Air Quality poller, polling every {self.POLL_INTERVAL_SECONDS}s")
        print(f"  API base URL: {self.BASE_URL}")
        print(f"  Kafka topic: {self.kafka_topic}")

        # Emit station reference data at startup
        print("Fetching GIOŚ monitoring stations...")
        stations = self.fetch_stations()
        for station in stations:
            self.producer.send_pl_gov_gios_airquality_station(
                str(station.station_id), station, flush_producer=False)
        self.producer.producer.flush()
        print(f"Sent {len(stations)} station reference events")

        # Build station→sensor mapping and emit sensor reference data
        print("Fetching sensors for all stations...")
        sensor_map: Dict[int, List[Sensor]] = {}
        sensor_station_map: Dict[int, int] = {}
        total_sensors = 0
        for station in stations:
            time.sleep(self.REQUEST_DELAY)
            sensors = self.fetch_sensors(station.station_id)
            sensor_map[station.station_id] = sensors
            for sensor in sensors:
                sensor_station_map[sensor.sensor_id] = station.station_id
                self.producer.send_pl_gov_gios_airquality_sensor(
                    str(station.station_id), str(sensor.sensor_id),
                    sensor, flush_producer=False)
                total_sensors += 1
        self.producer.producer.flush()
        print(f"Sent {total_sensors} sensor reference events")

        while True:
            try:
                state = self.load_state()
                measurement_timestamps = state.get("measurement_timestamps", {})
                aqi_timestamps = state.get("aqi_timestamps", {})
                new_count = 0

                # Poll measurements for each sensor
                for station_id, sensors in sensor_map.items():
                    for sensor in sensors:
                        time.sleep(self.REQUEST_DELAY)
                        raw_measurements = self.fetch_measurements(sensor.sensor_id)
                        for raw in raw_measurements:
                            measurement = parse_measurement(
                                raw, station_id, sensor.sensor_id)
                            if measurement is None:
                                continue
                            ts_key = f"{sensor.sensor_id}:{measurement.timestamp.isoformat()}"
                            if ts_key in measurement_timestamps:
                                continue
                            self.producer.send_pl_gov_gios_airquality_measurement(
                                str(station_id), str(sensor.sensor_id),
                                measurement, flush_producer=False)
                            measurement_timestamps[ts_key] = measurement.timestamp.isoformat()
                            new_count += 1

                # Poll AQI for each station
                for station in stations:
                    time.sleep(self.REQUEST_DELAY)
                    raw_aqi = self.fetch_air_quality_index(station.station_id)
                    if raw_aqi is None:
                        continue
                    aqi = parse_air_quality_index(raw_aqi)
                    if aqi is None:
                        continue
                    aqi_key = f"{station.station_id}:{aqi.calculation_timestamp.isoformat()}"
                    if aqi_key in aqi_timestamps:
                        continue
                    self.producer.send_pl_gov_gios_airquality_air_quality_index(
                        str(station.station_id), aqi, flush_producer=False)
                    aqi_timestamps[aqi_key] = aqi.calculation_timestamp.isoformat()
                    new_count += 1

                if new_count > 0:
                    self.producer.producer.flush()
                    print(f"Sent {new_count} new event(s) to Kafka")

                # Keep state bounded: only retain entries from this cycle
                state["measurement_timestamps"] = measurement_timestamps
                state["aqi_timestamps"] = aqi_timestamps
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
    Main function to parse arguments and start the GIOŚ Poland air quality poller.
    """
    parser = argparse.ArgumentParser(description="GIOŚ Poland Air Quality Poller")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store last seen timestamps per sensor")
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
        args.last_polled_file = os.getenv('GIOS_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.gios_last_polled.json')

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
        kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    if not kafka_topic:
        kafka_topic = os.getenv('KAFKA_TOPIC')
    if not sasl_username:
        sasl_username = os.getenv('SASL_USERNAME')
    if not sasl_password:
        sasl_password = os.getenv('SASL_PASSWORD')

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

    poller = GIOSPolandPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
