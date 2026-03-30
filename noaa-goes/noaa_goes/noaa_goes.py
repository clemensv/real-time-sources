"""
NOAA SWPC Space Weather Poller
Polls the Space Weather Prediction Center endpoints for space weather data
and sends it to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
from typing import Dict, List
import argparse
import requests
from noaa_goes.noaa_goes_producer.microsoft.opendata.us.noaa.swpc.spaceweatheralert import SpaceWeatherAlert
from noaa_goes.noaa_goes_producer.microsoft.opendata.us.noaa.swpc.planetarykindex import PlanetaryKIndex
from noaa_goes.noaa_goes_producer.microsoft.opendata.us.noaa.swpc.solarwindsummary import SolarWindSummary
from .noaa_goes_producer.producer_client import MicrosoftOpenDataUSNOAASWPCEventProducer


class SWPCPoller:
    """
    Polls the NOAA Space Weather Prediction Center API endpoints and sends
    space weather data to Kafka as CloudEvents.
    """
    ALERTS_URL = "https://services.swpc.noaa.gov/products/alerts.json"
    K_INDEX_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
    SOLAR_WIND_SPEED_URL = "https://services.swpc.noaa.gov/products/summary/solar-wind-speed.json"
    SOLAR_WIND_MAG_FIELD_URL = "https://services.swpc.noaa.gov/products/summary/solar-wind-mag-field.json"
    POLL_INTERVAL_SECONDS = 60

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str):
        """
        Initialize the SWPCPoller.

        Args:
            kafka_config: Kafka configuration settings.
            kafka_topic: Kafka topic to send messages to.
            last_polled_file: File to store last-seen timestamps for deduplication.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        from confluent_kafka import Producer
        kafka_producer = Producer(kafka_config)
        self.producer = MicrosoftOpenDataUSNOAASWPCEventProducer(kafka_producer, kafka_topic)

    def load_state(self) -> Dict:
        """
        Load the deduplication state from the state file.

        Returns:
            Dict with last-seen timestamps per data type.
        """
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {"last_alert_id": None, "last_kindex_time": None, "last_solar_wind_time": None}

    def save_state(self, state: Dict):
        """
        Save the deduplication state to the state file.

        Args:
            state: Dict with last-seen timestamps per data type.
        """
        try:
            os.makedirs(os.path.dirname(self.last_polled_file) if os.path.dirname(self.last_polled_file) else '.', exist_ok=True)
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Error saving state: {e}")

    def poll_alerts(self) -> List[dict]:
        """
        Fetch space weather alerts from the SWPC alerts endpoint.

        Returns:
            List of alert dicts with product_id, issue_datetime, message.
        """
        try:
            response = requests.get(self.ALERTS_URL, timeout=30)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                return data
            return []
        except Exception as err:
            print(f"Error fetching SWPC alerts: {err}")
            return []

    def poll_k_index(self) -> List[list]:
        """
        Fetch planetary K-index data from the SWPC endpoint.
        Skips the header row (first element).

        Returns:
            List of K-index data arrays [time_tag, Kp, Kp_fraction, a_running, station_count].
        """
        try:
            response = requests.get(self.K_INDEX_URL, timeout=30)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and len(data) > 1:
                return data[1:]  # skip header row
            return []
        except Exception as err:
            print(f"Error fetching K-index data: {err}")
            return []

    def poll_solar_wind(self) -> List[dict]:
        """
        Fetch solar wind speed and magnetic field summaries, combining them
        into a single SolarWindSummary record.

        Returns:
            List with a single combined solar wind summary dict, or empty list on error.
        """
        try:
            speed_response = requests.get(self.SOLAR_WIND_SPEED_URL, timeout=30)
            speed_response.raise_for_status()
            speed_data = speed_response.json()

            mag_response = requests.get(self.SOLAR_WIND_MAG_FIELD_URL, timeout=30)
            mag_response.raise_for_status()
            mag_data = mag_response.json()

            timestamp = speed_data.get("TimeStamp") or mag_data.get("TimeStamp") or ""
            wind_speed = speed_data.get("WindSpeed", 0)
            bt = mag_data.get("Bt", 0)
            bz = mag_data.get("Bz", 0)

            return [{
                "timestamp": timestamp,
                "wind_speed": float(wind_speed) if wind_speed else 0.0,
                "bt": float(bt) if bt else 0.0,
                "bz": float(bz) if bz else 0.0
            }]
        except Exception as err:
            print(f"Error fetching solar wind data: {err}")
            return []

    def poll_and_send(self):
        """
        Main polling loop. Fetches all three data types, deduplicates by
        tracking last-seen timestamps, creates dataclass instances and sends
        via the producer. Sleeps POLL_INTERVAL_SECONDS between polls.
        """
        print(f"Starting SWPC Space Weather poller, polling every {self.POLL_INTERVAL_SECONDS}s")
        print(f"  Alerts URL: {self.ALERTS_URL}")
        print(f"  K-Index URL: {self.K_INDEX_URL}")
        print(f"  Solar Wind Speed URL: {self.SOLAR_WIND_SPEED_URL}")
        print(f"  Solar Wind Mag Field URL: {self.SOLAR_WIND_MAG_FIELD_URL}")
        print(f"  Kafka topic: {self.kafka_topic}")

        while True:
            try:
                state = self.load_state()
                new_count = 0

                # Poll and send alerts
                alerts = self.poll_alerts()
                last_alert_id = state.get("last_alert_id")
                for alert_data in alerts:
                    product_id = alert_data.get("product_id", "")
                    if not product_id or product_id == last_alert_id:
                        continue

                    alert = SpaceWeatherAlert(
                        product_id=product_id,
                        issue_datetime=alert_data.get("issue_datetime", ""),
                        message=alert_data.get("message", "")
                    )
                    self.producer.send_microsoft_open_data_us_noaa_swpc_space_weather_alert(
                        alert, product_id, flush_producer=False)
                    state["last_alert_id"] = product_id
                    new_count += 1

                # Poll and send K-index data
                k_index_rows = self.poll_k_index()
                last_kindex_time = state.get("last_kindex_time")
                for row in k_index_rows:
                    if len(row) < 4:
                        continue
                    time_tag = str(row[0])
                    if time_tag == last_kindex_time:
                        continue

                    kindex = PlanetaryKIndex(
                        time_tag=time_tag,
                        kp=float(row[1]) if row[1] else 0.0,
                        a_running=float(row[2]) if row[2] else 0.0,
                        station_count=float(row[3]) if row[3] else 0.0
                    )
                    self.producer.send_microsoft_open_data_us_noaa_swpc_planetary_kindex(
                        kindex, time_tag, flush_producer=False)
                    state["last_kindex_time"] = time_tag
                    new_count += 1

                # Poll and send solar wind data
                solar_wind_records = self.poll_solar_wind()
                last_solar_wind_time = state.get("last_solar_wind_time")
                for record in solar_wind_records:
                    ts = record.get("timestamp", "")
                    if not ts or ts == last_solar_wind_time:
                        continue

                    summary = SolarWindSummary(
                        timestamp=ts,
                        wind_speed=record.get("wind_speed", 0.0),
                        bt=record.get("bt", 0.0),
                        bz=record.get("bz", 0.0)
                    )
                    self.producer.send_microsoft_open_data_us_noaa_swpc_solar_wind_summary(
                        summary, ts, flush_producer=False)
                    state["last_solar_wind_time"] = ts
                    new_count += 1

                if new_count > 0:
                    self.producer.producer.flush()
                    print(f"Sent {new_count} new record(s) to Kafka")

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
    Main function to parse arguments and start the SWPC space weather poller.
    """
    parser = argparse.ArgumentParser(description="NOAA SWPC Space Weather Poller")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store last-polled timestamps for deduplication")
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
        args.last_polled_file = os.getenv('SWPC_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.swpc_last_polled.json')

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

    poller = SWPCPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
