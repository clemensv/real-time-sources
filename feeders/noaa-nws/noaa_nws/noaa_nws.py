"""
NOAA NWS Weather Alerts Poller
Polls the NWS alerts API and sends alerts to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import sys
import time
from typing import Dict, List
import argparse
from noaa_nws_core import NWSFetcher, parse_connection_string
from noaa_nws_core.noaa_nws import (
    ALERTS_URL,
    POLL_INTERVAL_SECONDS,
    OBSERVATION_INTERVAL_SECONDS,
)
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
    Delegates data acquisition to NWSFetcher from noaa_nws_core.
    """

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str):
        """
        Initialize the NWSAlertPoller.

        Args:
            kafka_config: Kafka configuration settings.
            kafka_topic: Kafka topic to send messages to.
            last_polled_file: File to store seen alert IDs for deduplication.
        """
        self.kafka_topic = kafka_topic
        self.fetcher = NWSFetcher(last_polled_file=last_polled_file)
        from confluent_kafka import Producer
        kafka_producer = Producer(kafka_config)
        self.alerts_producer = MicrosoftOpenDataUSNOAANWSAlertsEventProducer(kafka_producer, kafka_topic)
        self.zones_producer = MicrosoftOpenDataUSNOAANWSZonesEventProducer(kafka_producer, kafka_topic)
        self.observations_producer = MicrosoftOpenDataUSNOAANWSObservationsEventProducer(kafka_producer, kafka_topic)
        self.kafka_producer = kafka_producer

    def poll_and_send(self, once: bool = False):
        """
        Main polling loop. Fetches alerts, deduplicates, and sends new alerts
        to Kafka as CloudEvents. Polls every POLL_INTERVAL_SECONDS.

        Args:
            once: If True, exit after one polling cycle (alerts + observations).
                Used for scheduled execution in Fabric notebooks.
        """
        print(f"Starting NWS Weather Alert poller, polling every {POLL_INTERVAL_SECONDS}s")
        print(f"  Alerts URL: {ALERTS_URL}")
        print(f"  Kafka topic: {self.kafka_topic}")

        # Send reference data (zones) at startup
        print("Sending NWS forecast zones as reference data...")
        zone_dicts = self.fetcher.fetch_zones()
        for d in zone_dicts:
            zone = Zone(**d)
            self.zones_producer.send_microsoft_open_data_us_noaa_nws_zone(
                zone.zone_id or "", zone, flush_producer=False)
        self.kafka_producer.flush()
        print(f"Sent {len(zone_dicts)} zones as reference data")

        # Send observation stations at startup
        print("Sending NWS observation stations as reference data...")
        station_dicts = self.fetcher.fetch_observation_stations()
        for d in station_dicts:
            station = ObservationStation(**d)
            self.observations_producer.send_microsoft_open_data_us_noaa_nws_observation_station(
                station.station_id, station, flush_producer=False)
        self.kafka_producer.flush()
        print(f"Sent {len(station_dicts)} observation stations as reference data")

        last_obs_time = 0.0
        obs_seen: Dict[str, str] = {}  # station_id -> last observation timestamp

        while True:
            try:
                state = self.fetcher.load_seen_alerts()
                seen_ids = set(state.get("seen_ids", []))
                features = self.fetcher.poll_alerts()

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
                        description=props.get("description", ""),
                        zone_id=None,
                        state=None,
                        event_type=props.get("event", "") or None,
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
                self.fetcher.save_seen_alerts(state)

                # Poll observations on a slower cadence
                now = time.time()
                if now - last_obs_time >= OBSERVATION_INTERVAL_SECONDS:
                    obs_count = 0
                    for sid in self.fetcher.station_ids:
                        obs_dict = self.fetcher.fetch_latest_observation(sid)
                        if obs_dict and obs_dict.get("timestamp"):
                            if obs_seen.get(sid) != obs_dict["timestamp"]:
                                obs = WeatherObservation(**obs_dict)
                                self.observations_producer.send_microsoft_open_data_us_noaa_nws_weather_observation(
                                    sid, obs, flush_producer=False)
                                obs_count += 1
                                obs_seen[sid] = obs_dict["timestamp"]
                    if obs_count > 0:
                        self.kafka_producer.flush()
                        print(f"Sent {obs_count} weather observation(s)")
                    last_obs_time = now

            except Exception as e:
                print(f"Error in polling loop: {e}")

            if once:
                print("--once mode: exiting after first polling cycle")
                break

            time.sleep(POLL_INTERVAL_SECONDS)


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
    parser.add_argument('--once', action='store_true',
                        default=os.getenv('ONCE_MODE', '').lower() in ('1', 'true', 'yes'),
                        help='Exit after one polling cycle (also via ONCE_MODE env var). '
                             'Useful for scheduled execution in Fabric notebooks.')

    _argv = sys.argv[1:]
    if _argv and _argv[0] == 'feed':
        _argv = _argv[1:]
    args = parser.parse_args(_argv)

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
    poller.poll_and_send(once=args.once)


if __name__ == "__main__":
    main()
