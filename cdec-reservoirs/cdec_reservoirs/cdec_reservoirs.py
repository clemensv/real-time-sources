"""Bridge for the California Data Exchange Center (CDEC) reservoir data API.

Polls the CDEC JSON Data Servlet for hourly reservoir readings (storage,
elevation, inflow, outflow) and emits them as CloudEvents to a Kafka topic.
"""

from datetime import datetime, timedelta, timezone
import os
from typing import Any, Dict, List, Optional, Set
import asyncio
import logging
import sys
import time
import argparse
import json
import re
import requests

from confluent_kafka import Producer
from cdec_reservoirs_producer_data.gov.ca.water.cdec.reservoirreading import ReservoirReading
from cdec_reservoirs_producer_kafka_producer.producer import GovCaWaterCdecEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# CDEC always reports in PST (UTC-8), never PDT
PST = timezone(timedelta(hours=-8))

BASE_URL = "https://cdec.water.ca.gov/dynamicapp/req/JSONDataServlet"

# Default major California reservoir stations
DEFAULT_STATIONS = "SHA,ORO,FOL,NML,DNP,HTC,SON,MIL,PNF"

# Standard reservoir sensor numbers
DEFAULT_SENSORS = "15,6,76,23"

SENTINEL_VALUE = -9999


def parse_cdec_timestamp(raw: str) -> str:
    """Parse a CDEC timestamp string into ISO 8601 with PST offset.

    CDEC returns timestamps like '2026-4-1 0:00' (always PST).
    Returns ISO 8601 format like '2026-04-01T00:00:00-08:00'.
    """
    raw = raw.strip()
    # Match 'YYYY-M-D H:MM' or 'YYYY-M-D HH:MM' patterns
    match = re.match(r'(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{2})', raw)
    if not match:
        raise ValueError(f"Cannot parse CDEC timestamp: {raw!r}")
    year, month, day, hour, minute = (int(g) for g in match.groups())
    dt = datetime(year, month, day, hour, minute, tzinfo=PST)
    return dt.isoformat()


def normalize_value(raw_value: Any) -> Optional[float]:
    """Normalize a CDEC measurement value.

    Returns None for missing data (None or sentinel -9999).
    """
    if raw_value is None:
        return None
    try:
        val = float(raw_value)
    except (TypeError, ValueError):
        return None
    if val == SENTINEL_VALUE:
        return None
    return val


class CdecReservoirsAPI:
    """Client for the CDEC JSON Data Servlet."""

    def __init__(self, stations: str = DEFAULT_STATIONS,
                 sensors: str = DEFAULT_SENSORS,
                 dur_code: str = "H"):
        self.stations = stations
        self.sensors = sensors
        self.dur_code = dur_code
        self.session = requests.Session()

    def build_url(self, start_date: str, end_date: str) -> str:
        """Build the CDEC JSON Data Servlet URL.

        Args:
            start_date: Start date in YYYY-MM-DD format.
            end_date: End date in YYYY-MM-DD format.
        """
        return (
            f"{BASE_URL}?Stations={self.stations}"
            f"&SensorNums={self.sensors}"
            f"&dur_code={self.dur_code}"
            f"&Start={start_date}&End={end_date}"
        )

    def fetch_readings(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Fetch readings from CDEC for the configured stations and sensors.

        Returns a list of raw reading dicts from the API.
        """
        url = self.build_url(start_date, end_date)
        logging.debug("Fetching CDEC data: %s", url)
        response = self.session.get(url, timeout=60)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return data
        logging.warning("Unexpected CDEC response type: %s", type(data))
        return []

    def parse_connection_string(self, connection_string: str) -> Dict[str, str]:
        """Parse an Event Hubs / Kafka connection string.

        Args:
            connection_string: The connection string.

        Returns:
            Dict with Kafka config keys and a 'kafka_topic' entry.
        """
        config_dict: Dict[str, str] = {}
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = (
                        part.split('=')[1].strip('"').strip()
                        .replace('sb://', '').replace('/', '') + ':9093'
                    )
                elif 'EntityPath' in part:
                    config_dict['kafka_topic'] = part.split('=')[1].strip('"').strip()
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

    async def feed_readings(self, kafka_config: dict, kafka_topic: str,
                            polling_interval: int, state_file: str = '') -> None:
        """Poll CDEC and emit reservoir readings to Kafka."""
        seen_keys: Set[str] = set()
        if state_file:
            seen_keys = _load_state(state_file)

        producer = Producer(kafka_config)
        cdec_producer = GovCaWaterCdecEventProducer(producer, kafka_topic)

        logging.info("Starting CDEC reservoir feed to Kafka topic %s at %s",
                     kafka_topic, kafka_config['bootstrap.servers'])
        logging.info("Stations: %s | Sensors: %s | Duration: %s",
                     self.stations, self.sensors, self.dur_code)

        while True:
            try:
                count = 0
                start_time = datetime.now(timezone.utc)

                # Query the last 2 hours to catch late-arriving data
                end_dt = datetime.now(PST)
                start_dt = end_dt - timedelta(hours=2)
                start_date = start_dt.strftime("%Y-%m-%d")
                end_date = end_dt.strftime("%Y-%m-%d")

                readings = self.fetch_readings(start_date, end_date)

                for raw in readings:
                    station_id = raw.get("stationId", "").strip()
                    sensor_num = raw.get("SENSOR_NUM")
                    raw_date = raw.get("date", "")

                    if not station_id or sensor_num is None or not raw_date:
                        continue

                    # Dedup key: station + sensor + timestamp
                    dedup_key = f"{station_id}/{sensor_num}/{raw_date}"
                    if dedup_key in seen_keys:
                        continue

                    value = normalize_value(raw.get("value"))
                    try:
                        iso_date = parse_cdec_timestamp(raw_date)
                    except ValueError:
                        logging.warning("Skipping unparseable timestamp: %s", raw_date)
                        continue

                    reading = ReservoirReading(
                        station_id=station_id,
                        sensor_num=int(sensor_num),
                        sensor_type=raw.get("sensorType", "").strip(),
                        value=value,
                        units=raw.get("units", "").strip(),
                        date=iso_date,
                        dur_code=raw.get("durCode", "").strip(),
                        data_flag=raw.get("dataFlag", " "),
                    )

                    cdec_producer.send_gov_ca_water_cdec_reservoir_reading(
                        _feedurl=BASE_URL,
                        _station_id=station_id,
                        _sensor_num=str(sensor_num),
                        data=reading,
                        flush_producer=False,
                    )
                    count += 1
                    seen_keys.add(dedup_key)

                producer.flush()
                end_time = datetime.now(timezone.utc)
                elapsed = (end_time - start_time).total_seconds()
                effective_interval = max(0, polling_interval - elapsed)
                logging.info(
                    "Sent %d readings in %.1fs. Next poll in %.0fs.",
                    count, elapsed, effective_interval,
                )
                _save_state(state_file, seen_keys)
                if effective_interval > 0:
                    time.sleep(effective_interval)
            except KeyboardInterrupt:
                logging.info("Exiting...")
                break
            except Exception as e:
                logging.error("Error occurred: %s", e)
                logging.info("Retrying in %d seconds...", polling_interval)
                time.sleep(polling_interval)
        producer.flush()


def _load_state(state_file: str) -> Set[str]:
    """Load dedup state from a JSON file."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return set(data)
    except Exception as e:
        logging.warning("Could not load state from %s: %s", state_file, e)
    return set()


def _save_state(state_file: str, seen_keys: Set[str]) -> None:
    """Save dedup state to a JSON file."""
    if not state_file:
        return
    try:
        # Keep only recent keys to avoid unbounded growth
        recent = sorted(seen_keys)[-50000:]
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(recent, f)
    except Exception as e:
        logging.warning("Could not save state to %s: %s", state_file, e)


def main() -> None:
    """Entry point for the CDEC Reservoirs bridge."""
    parser = argparse.ArgumentParser(
        description='Bridge for California Data Exchange Center (CDEC) reservoir data to Kafka.')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list', help='Fetch and display current readings')

    feed_parser = subparsers.add_parser('feed', help='Feed reservoir data as CloudEvents to Kafka')
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str,
                             help="Comma-separated Kafka bootstrap servers",
                             default=os.getenv('KAFKA_BOOTSTRAP_SERVERS'))
    feed_parser.add_argument('--kafka-topic', type=str,
                             help="Kafka topic name",
                             default=os.getenv('KAFKA_TOPIC'))
    feed_parser.add_argument('--sasl-username', type=str,
                             help="SASL PLAIN username",
                             default=os.getenv('SASL_USERNAME'))
    feed_parser.add_argument('--sasl-password', type=str,
                             help="SASL PLAIN password",
                             default=os.getenv('SASL_PASSWORD'))
    feed_parser.add_argument('-c', '--connection-string', type=str,
                             help='Event Hubs / Fabric Event Stream connection string',
                             default=os.getenv('CONNECTION_STRING'))
    polling_interval_default = 3600
    if os.getenv('POLLING_INTERVAL'):
        polling_interval_default = int(os.getenv('POLLING_INTERVAL'))
    feed_parser.add_argument('-i', '--polling-interval', type=int,
                             help='Polling interval in seconds (default: 3600)',
                             default=polling_interval_default)
    feed_parser.add_argument('--stations', type=str,
                             help='Comma-separated CDEC station IDs',
                             default=os.getenv('STATIONS', DEFAULT_STATIONS))
    feed_parser.add_argument('--sensors', type=str,
                             help='Comma-separated CDEC sensor numbers',
                             default=os.getenv('SENSORS', DEFAULT_SENSORS))
    feed_parser.add_argument('--dur-code', type=str,
                             help='Duration code (H=hourly, D=daily)',
                             default=os.getenv('DUR_CODE', 'H'))
    feed_parser.add_argument('--state-file', type=str,
                             default=os.getenv('STATE_FILE',
                                               os.path.expanduser('~/.cdec_reservoirs_state.json')))

    args = parser.parse_args()
    api = CdecReservoirsAPI(
        stations=getattr(args, 'stations', DEFAULT_STATIONS),
        sensors=getattr(args, 'sensors', DEFAULT_SENSORS),
        dur_code=getattr(args, 'dur_code', 'H'),
    )

    if args.command == 'list':
        end_dt = datetime.now(PST)
        start_dt = end_dt - timedelta(hours=2)
        readings = api.fetch_readings(
            start_dt.strftime("%Y-%m-%d"),
            end_dt.strftime("%Y-%m-%d"),
        )
        for r in readings:
            print(json.dumps(r, indent=2))
    elif args.command == 'feed':
        if args.connection_string:
            config_params = api.parse_connection_string(args.connection_string)
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
            print("Error: Kafka bootstrap servers must be provided.")
            sys.exit(1)
        if not kafka_topic:
            print("Error: Kafka topic must be provided.")
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

        asyncio.run(api.feed_readings(
            kafka_config, kafka_topic, args.polling_interval, args.state_file))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
