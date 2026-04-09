"""Bridge for Ireland OPW waterlevel.ie — real-time water level, temperature, and rainfall data."""

import os
import sys
import time
import json
import logging
import argparse
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Set

import requests
from confluent_kafka import Producer
from ireland_opw_waterlevel_producer_data.ie.gov.opw.waterlevel.station import Station
from ireland_opw_waterlevel_producer_data.ie.gov.opw.waterlevel.waterlevelreading import WaterLevelReading
from ireland_opw_waterlevel_producer_kafka_producer.producer import IeGovOpwWaterlevelEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

FEED_URL = "https://waterlevel.ie/geojson/latest/"


def _load_state(state_file: str) -> dict:
    """Load persisted dedup state from a JSON file."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logging.warning("Could not load state from %s: %s", state_file, e)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    """Save dedup state to a JSON file."""
    if not state_file:
        return
    try:
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception as e:
        logging.warning("Could not save state to %s: %s", state_file, e)


def parse_value(raw: str) -> Optional[float]:
    """Parse a string numeric value to float, returning None on failure."""
    if raw is None:
        return None
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None


def extract_stations(features: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Extract unique stations from GeoJSON features.

    Returns a dict keyed by station_ref with station metadata.
    """
    stations: Dict[str, Dict[str, Any]] = {}
    for feature in features:
        props = feature.get("properties", {})
        station_ref = props.get("station_ref", "")
        if station_ref and station_ref not in stations:
            coords = feature.get("geometry", {}).get("coordinates", [0.0, 0.0])
            stations[station_ref] = {
                "station_ref": station_ref,
                "station_name": props.get("station_name", ""),
                "region_id": int(props.get("region_id", 0)),
                "longitude": float(coords[0]) if len(coords) > 0 else 0.0,
                "latitude": float(coords[1]) if len(coords) > 1 else 0.0,
            }
    return stations


def extract_readings(features: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract sensor readings from GeoJSON features."""
    readings = []
    for feature in features:
        props = feature.get("properties", {})
        readings.append({
            "station_ref": props.get("station_ref", ""),
            "station_name": props.get("station_name", ""),
            "sensor_ref": props.get("sensor_ref", ""),
            "value": parse_value(props.get("value")),
            "datetime": props.get("datetime", ""),
            "err_code": int(props.get("err_code", 0)),
        })
    return readings


def dedup_key(reading: Dict[str, Any]) -> str:
    """Build a deduplication key from station_ref + sensor_ref + datetime."""
    return f"{reading['station_ref']}|{reading['sensor_ref']}|{reading['datetime']}"


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse a connection string and extract Kafka config.

    Supports Azure Event Hubs / Fabric Event Streams format and
    simple BootstrapServer=host:port;EntityPath=topic format.
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


def fetch_geojson(session: requests.Session, url: str = FEED_URL) -> List[Dict[str, Any]]:
    """Fetch GeoJSON from waterlevel.ie and return the list of features."""
    response = session.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("features", [])


def emit_stations(
    producer_client: IeGovOpwWaterlevelEventProducer,
    stations: Dict[str, Dict[str, Any]],
    kafka_producer: Producer,
) -> int:
    """Emit Station reference events. Returns count of stations emitted."""
    count = 0
    for station_ref, info in stations.items():
        station_data = Station(
            station_ref=info["station_ref"],
            station_name=info["station_name"],
            region_id=info["region_id"],
            longitude=info["longitude"],
            latitude=info["latitude"],
        )
        producer_client.send_ie_gov_opw_waterlevel_station(
            _feedurl=FEED_URL,
            _station_ref=station_ref,
            data=station_data,
            flush_producer=False,
        )
        count += 1
    kafka_producer.flush()
    return count


def emit_readings(
    producer_client: IeGovOpwWaterlevelEventProducer,
    readings: List[Dict[str, Any]],
    seen_keys: Set[str],
    kafka_producer: Producer,
) -> int:
    """Emit WaterLevelReading events, deduplicating by station+sensor+datetime.

    Returns count of new readings emitted. Updates seen_keys in place.
    """
    count = 0
    for reading in readings:
        key = dedup_key(reading)
        if key in seen_keys:
            continue
        try:
            reading_data = WaterLevelReading(
                station_ref=reading["station_ref"],
                station_name=reading["station_name"],
                sensor_ref=reading["sensor_ref"],
                value=reading["value"],
                datetime=reading["datetime"],
                err_code=reading["err_code"],
            )
            producer_client.send_ie_gov_opw_waterlevel_water_level_reading(
                _feedurl=FEED_URL,
                _station_ref=reading["station_ref"],
                data=reading_data,
                flush_producer=False,
            )
            seen_keys.add(key)
            count += 1
        except Exception as e:
            logging.error("Error sending reading for %s/%s: %s",
                          reading.get("station_ref"), reading.get("sensor_ref"), e)
    kafka_producer.flush()
    return count


def feed(kafka_config: dict, kafka_topic: str, polling_interval: int,
         state_file: str = '') -> None:
    """Main polling loop: emit stations then poll readings."""
    seen_keys: Set[str] = set(_load_state(state_file).get("seen_keys", []))
    session = requests.Session()
    kafka_producer = Producer(kafka_config)
    producer_client = IeGovOpwWaterlevelEventProducer(kafka_producer, kafka_topic)

    logging.info("Starting OPW waterlevel.ie bridge to topic %s at %s",
                 kafka_topic, kafka_config.get('bootstrap.servers'))

    # Emit reference data at startup
    try:
        features = fetch_geojson(session)
        stations = extract_stations(features)
        n = emit_stations(producer_client, stations, kafka_producer)
        logging.info("Emitted %d station reference events", n)
    except Exception as e:
        logging.error("Error fetching initial station data: %s", e)

    last_station_refresh = datetime.now(timezone.utc)
    station_refresh_interval = timedelta(hours=6)

    while True:
        try:
            start_time = datetime.now(timezone.utc)
            features = fetch_geojson(session)

            # Periodically refresh station reference data
            if datetime.now(timezone.utc) - last_station_refresh > station_refresh_interval:
                stations = extract_stations(features)
                n = emit_stations(producer_client, stations, kafka_producer)
                logging.info("Refreshed %d station reference events", n)
                last_station_refresh = datetime.now(timezone.utc)

            readings = extract_readings(features)
            count = emit_readings(producer_client, readings, seen_keys, kafka_producer)

            end_time = datetime.now(timezone.utc)
            elapsed = (end_time - start_time).total_seconds()
            effective_interval = max(0, polling_interval - elapsed)

            # Trim seen_keys to prevent unbounded growth (keep last 50000)
            if len(seen_keys) > 50000:
                seen_keys_list = sorted(seen_keys)
                seen_keys = set(seen_keys_list[-25000:])

            _save_state(state_file, {"seen_keys": list(seen_keys)})

            logging.info("Emitted %d readings in %.1fs. Waiting %.0fs.",
                         count, elapsed, effective_interval)
            if effective_interval > 0:
                time.sleep(effective_interval)
        except KeyboardInterrupt:
            logging.info("Exiting...")
            break
        except Exception as e:
            logging.error("Error in polling loop: %s", e)
            logging.info("Retrying in %d seconds...", polling_interval)
            time.sleep(polling_interval)

    kafka_producer.flush()


def main() -> None:
    """CLI entry point for the Ireland OPW waterlevel.ie bridge."""
    parser = argparse.ArgumentParser(
        description='Ireland OPW waterlevel.ie bridge — fetch water level data and emit to Kafka.'
    )
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list', help='List stations from the latest GeoJSON feed')

    feed_parser = subparsers.add_parser('feed', help='Poll and emit events to Kafka')
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str,
                             help="Comma separated Kafka bootstrap servers",
                             default=os.getenv('KAFKA_BOOTSTRAP_SERVERS'))
    feed_parser.add_argument('--kafka-topic', type=str,
                             help="Kafka topic",
                             default=os.getenv('KAFKA_TOPIC'))
    feed_parser.add_argument('--sasl-username', type=str,
                             help="SASL PLAIN username",
                             default=os.getenv('SASL_USERNAME'))
    feed_parser.add_argument('--sasl-password', type=str,
                             help="SASL PLAIN password",
                             default=os.getenv('SASL_PASSWORD'))
    feed_parser.add_argument('-c', '--connection-string', type=str,
                             help='Event Hubs or Fabric connection string',
                             default=os.getenv('CONNECTION_STRING'))
    polling_interval_default = int(os.getenv('POLLING_INTERVAL', '300'))
    feed_parser.add_argument('-i', '--polling-interval', type=int,
                             help='Polling interval in seconds (default: 300)',
                             default=polling_interval_default)
    feed_parser.add_argument('--state-file', type=str,
                             default=os.getenv('STATE_FILE',
                                               os.path.expanduser('~/.ireland_opw_waterlevel_state.json')))

    args = parser.parse_args()

    if args.command == 'list':
        session = requests.Session()
        features = fetch_geojson(session)
        stations = extract_stations(features)
        for ref, info in sorted(stations.items()):
            print(f"{ref}: {info['station_name']} (region {info['region_id']})")
    elif args.command == 'feed':
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
            print("Error: Kafka bootstrap servers required (via --connection-string or --kafka-bootstrap-servers).")
            sys.exit(1)
        if not kafka_topic:
            print("Error: Kafka topic required (via --connection-string or --kafka-topic).")
            sys.exit(1)

        tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
        kafka_config: Dict[str, Any] = {
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

        feed(kafka_config, kafka_topic, args.polling_interval, args.state_file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
