"""
Madrid Real-Time Traffic (Informo) Bridge

Polls the Madrid Informo pm.xml endpoint for traffic sensor data and sends
measurement point reference data and traffic readings to Kafka as CloudEvents.
"""

import os
import sys
import time
import argparse
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone

import requests
from madrid_traffic_producer_data import MeasurementPoint, TrafficReading
from madrid_traffic_producer_kafka_producer.producer import EsMadridInformoEventProducer


PM_XML_URL = "https://informo.madrid.es/informo/tmadrid/pm.xml"
POLL_INTERVAL_SECONDS = 300
REFERENCE_REFRESH_SECONDS = 3600


def parse_european_float(value: str) -> Optional[float]:
    """
    Parse a float from a string using European comma decimal separators.

    Args:
        value: String with comma as decimal separator, e.g. '438339,375874991'.

    Returns:
        Float value, or None on failure.
    """
    if not value or not value.strip():
        return None
    try:
        return float(value.strip().replace(',', '.'))
    except (ValueError, TypeError):
        return None


def safe_int(value: str) -> Optional[int]:
    """
    Parse an integer from a string, returning None on failure.

    Args:
        value: String integer value.

    Returns:
        Integer value, or None on failure.
    """
    if not value or not value.strip():
        return None
    try:
        return int(value.strip())
    except (ValueError, TypeError):
        return None


def round_to_5min(dt: datetime) -> datetime:
    """
    Round a datetime down to the nearest 5-minute boundary.

    Args:
        dt: The datetime to round.

    Returns:
        A datetime rounded down to the nearest 5-minute interval.
    """
    minute = (dt.minute // 5) * 5
    return dt.replace(minute=minute, second=0, microsecond=0)


def parse_pm_xml(xml_text: str) -> Tuple[List[dict], Optional[str]]:
    """
    Parse the Madrid Informo pm.xml response.

    Extracts all <pm> elements and the top-level <fecha_hora> timestamp.

    Args:
        xml_text: Raw XML response text.

    Returns:
        Tuple of (list of sensor dicts, fecha_hora string or None).
    """
    root = ET.fromstring(xml_text)
    fecha_hora = None
    fecha_hora_elem = root.find('fecha_hora')
    if fecha_hora_elem is not None and fecha_hora_elem.text:
        fecha_hora = fecha_hora_elem.text.strip()

    sensors = []
    for pm in root.findall('pm'):
        sensor = {}
        for child in pm:
            sensor[child.tag] = child.text.strip() if child.text else ''
        sensors.append(sensor)

    return sensors, fecha_hora


def build_measurement_point(sensor: dict) -> MeasurementPoint:
    """
    Convert a raw sensor dict from XML into a MeasurementPoint data class.

    Maps Spanish upstream field names to English schema field names.

    Args:
        sensor: Dict with raw XML tag names as keys.

    Returns:
        MeasurementPoint instance.
    """
    st_x = parse_european_float(sensor.get('st_x', ''))
    st_y = parse_european_float(sensor.get('st_y', ''))

    return MeasurementPoint(
        sensor_id=sensor.get('idelem', ''),
        description=sensor.get('descripcion', ''),
        element_type=sensor.get('tipo_elem', None),
        subarea=sensor.get('subarea', None) or None,
        longitude=st_x,
        latitude=st_y,
        saturation_intensity=safe_int(sensor.get('intensidadSat', '')),
    )


def build_traffic_reading(sensor: dict, timestamp: datetime) -> TrafficReading:
    """
    Convert a raw sensor dict from XML into a TrafficReading data class.

    Maps Spanish upstream field names to English schema field names.

    Args:
        sensor: Dict with raw XML tag names as keys.
        timestamp: UTC timestamp for this reading (poll time rounded to 5-min).

    Returns:
        TrafficReading instance.
    """
    return TrafficReading(
        sensor_id=sensor.get('idelem', ''),
        intensity=safe_int(sensor.get('intensidad', '')),
        occupancy=safe_int(sensor.get('ocupacion', '')),
        load=safe_int(sensor.get('carga', '')),
        service_level=safe_int(sensor.get('nivelServicio', '')),
        error_flag=sensor.get('error', None) or None,
        timestamp=timestamp,
    )


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse an Azure Event Hubs-style or plain Kafka connection string.

    Supports:
        - BootstrapServer=host:port;EntityPath=topic
        - Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=...

    Args:
        connection_string: The connection string.

    Returns:
        Dict with bootstrap.servers, kafka_topic, and optional SASL params.
    """
    config_dict: Dict[str, str] = {}
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


class MadridTrafficPoller:
    """
    Polls the Madrid Informo pm.xml endpoint and sends traffic data
    to Kafka as CloudEvents.
    """

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str):
        """
        Initialize the poller.

        Args:
            kafka_config: Kafka producer configuration dict.
            kafka_topic: Kafka topic to send messages to.
        """
        self.kafka_topic = kafka_topic
        from confluent_kafka import Producer
        kafka_producer = Producer(kafka_config)
        self.producer = EsMadridInformoEventProducer(kafka_producer, kafka_topic)
        self._last_dedup_key: Optional[str] = None
        self._last_reference_time: float = 0.0

    def fetch_xml(self) -> Optional[str]:
        """
        Fetch the pm.xml feed from the Madrid Informo API.

        Returns:
            Raw XML text, or None on failure.
        """
        try:
            response = requests.get(PM_XML_URL, timeout=60)
            response.raise_for_status()
            return response.text
        except Exception as err:
            print(f"Error fetching Madrid traffic data: {err}")
            return None

    def emit_reference_data(self, sensors: List[dict]) -> int:
        """
        Emit MeasurementPoint reference events for all sensors.

        Args:
            sensors: List of raw sensor dicts from XML.

        Returns:
            Number of reference events emitted.
        """
        count = 0
        for sensor in sensors:
            mp = build_measurement_point(sensor)
            if not mp.sensor_id:
                continue
            self.producer.send_es_madrid_informo_measurement_point(
                mp.sensor_id, mp, flush_producer=False)
            count += 1
        self.producer.producer.flush()
        return count

    def emit_traffic_readings(self, sensors: List[dict], poll_time: datetime) -> int:
        """
        Emit TrafficReading telemetry events, skipping sensors with errors.

        Args:
            sensors: List of raw sensor dicts from XML.
            poll_time: UTC poll timestamp (will be rounded to 5-min boundary).

        Returns:
            Number of telemetry events emitted.
        """
        timestamp = round_to_5min(poll_time)
        dedup_key = timestamp.isoformat()

        if dedup_key == self._last_dedup_key:
            return 0

        count = 0
        for sensor in sensors:
            error = sensor.get('error', 'N')
            if error and error.upper() in ('S', 'Y'):
                continue

            reading = build_traffic_reading(sensor, timestamp)
            if not reading.sensor_id:
                continue

            self.producer.send_es_madrid_informo_traffic_reading(
                reading.sensor_id, reading, flush_producer=False)
            count += 1

        if count > 0:
            self.producer.producer.flush()
        self._last_dedup_key = dedup_key
        return count

    def poll_and_send(self, once: bool = False):
        """
        Main polling loop.

        Emits reference data at startup and periodically, then emits
        telemetry readings each cycle.

        Args:
            once: Run one poll iteration and return. Intended for tests.
        """
        print(f"Starting Madrid Traffic poller, polling every {POLL_INTERVAL_SECONDS}s")
        print(f"  URL: {PM_XML_URL}")
        print(f"  Kafka topic: {self.kafka_topic}")

        while True:
            try:
                xml_text = self.fetch_xml()
                if xml_text is None:
                    if once:
                        break
                    time.sleep(POLL_INTERVAL_SECONDS)
                    continue

                sensors, _ = parse_pm_xml(xml_text)
                poll_time = datetime.now(timezone.utc)

                now = time.monotonic()
                if now - self._last_reference_time >= REFERENCE_REFRESH_SECONDS or self._last_reference_time == 0.0:
                    print("Sending measurement point reference data...")
                    ref_count = self.emit_reference_data(sensors)
                    print(f"Sent {ref_count} measurement point(s) as reference data")
                    self._last_reference_time = now

                reading_count = self.emit_traffic_readings(sensors, poll_time)
                if reading_count > 0:
                    print(f"Sent {reading_count} traffic reading(s) to Kafka")

            except Exception as e:
                print(f"Error in polling loop: {e}")

            if once:
                break

            time.sleep(POLL_INTERVAL_SECONDS)


def main():
    """
    Main entry point. Parses arguments and starts the poller.
    """
    parser = argparse.ArgumentParser(description="Madrid Real-Time Traffic (Informo) Bridge")
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
        print("Error: Kafka bootstrap servers must be provided via --kafka-bootstrap-servers or CONNECTION_STRING.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided via --kafka-topic or CONNECTION_STRING.")
        sys.exit(1)

    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
    kafka_config: Dict[str, str] = {
        'bootstrap.servers': kafka_bootstrap_servers,
    }
    if sasl_username and sasl_password:
        kafka_config.update({
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password,
        })
    elif tls_enabled:
        kafka_config['security.protocol'] = 'SSL'

    poller = MadridTrafficPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
