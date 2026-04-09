"""Bridge between the VATSIM live data feed and Apache Kafka."""

import datetime
import json
import logging
import os
import sys
import time
import argparse
from typing import Any, Dict, List, Optional

import requests
from confluent_kafka import Producer

from vatsim_producer_data.net.vatsim.pilotposition import PilotPosition
from vatsim_producer_data.net.vatsim.controllerposition import ControllerPosition
from vatsim_producer_data.net.vatsim.networkstatus import NetworkStatus
from vatsim_producer_kafka_producer.producer import (
    NetVatsimPilotsEventProducer,
    NetVatsimControllersEventProducer,
    NetVatsimStatusEventProducer,
)

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

VATSIM_DATA_URL = "https://data.vatsim.net/v3/vatsim-data.json"


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


class VatsimBridge:
    """Polls the VATSIM v3 data feed and emits CloudEvents."""

    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()

    def fetch_data(self) -> Dict[str, Any]:
        """Fetch the current VATSIM data snapshot."""
        response = self.session.get(VATSIM_DATA_URL, timeout=30)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def parse_pilot(pilot: Dict[str, Any]) -> PilotPosition:
        """Convert a raw pilot dict from the VATSIM feed to a PilotPosition."""
        fp = pilot.get("flight_plan") or {}
        return PilotPosition(
            cid=pilot["cid"],
            callsign=pilot["callsign"],
            latitude=pilot["latitude"],
            longitude=pilot["longitude"],
            altitude=pilot["altitude"],
            groundspeed=pilot["groundspeed"],
            heading=pilot["heading"],
            transponder=pilot["transponder"],
            qnh_mb=pilot.get("qnh_mb", 0),
            flight_rules=fp.get("flight_rules"),
            aircraft_short=fp.get("aircraft_short"),
            departure=fp.get("departure"),
            arrival=fp.get("arrival"),
            route=fp.get("route"),
            cruise_altitude=fp.get("altitude"),
            pilot_rating=pilot.get("pilot_rating", 0),
            last_updated=datetime.datetime.fromisoformat(pilot["last_updated"]),
        )

    @staticmethod
    def parse_controller(ctrl: Dict[str, Any]) -> ControllerPosition:
        """Convert a raw controller dict from the VATSIM feed to a ControllerPosition."""
        text_atis_raw = ctrl.get("text_atis")
        if isinstance(text_atis_raw, list):
            text_atis = "\n".join(text_atis_raw) if text_atis_raw else None
        else:
            text_atis = text_atis_raw

        return ControllerPosition(
            cid=ctrl["cid"],
            callsign=ctrl["callsign"],
            frequency=ctrl["frequency"],
            facility=ctrl["facility"],
            rating=ctrl["rating"],
            text_atis=text_atis,
            last_updated=datetime.datetime.fromisoformat(ctrl["last_updated"]),
        )

    @staticmethod
    def build_network_status(general: Dict[str, Any], pilot_count: int, controller_count: int) -> NetworkStatus:
        """Build a NetworkStatus from the general section."""
        return NetworkStatus(
            callsign="status",
            update_timestamp=datetime.datetime.fromisoformat(general["update_timestamp"]),
            connected_clients=general.get("connected_clients", 0),
            unique_users=general.get("unique_users", 0),
            pilot_count=pilot_count,
            controller_count=controller_count,
        )

    @staticmethod
    def pilot_fingerprint(pilot: Dict[str, Any]) -> str:
        """Create a dedup fingerprint from pilot position fields."""
        return f"{pilot.get('latitude')},{pilot.get('longitude')},{pilot.get('altitude')},{pilot.get('groundspeed')},{pilot.get('heading')},{pilot.get('last_updated')}"

    @staticmethod
    def controller_fingerprint(ctrl: Dict[str, Any]) -> str:
        """Create a dedup fingerprint from controller fields."""
        return f"{ctrl.get('frequency')},{ctrl.get('facility')},{ctrl.get('rating')},{ctrl.get('text_atis')},{ctrl.get('last_updated')}"

    def parse_connection_string(self, connection_string: str) -> Dict[str, str]:
        """Parse the connection string and extract Kafka config parameters."""
        config_dict: Dict[str, str] = {}
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').strip().replace('sb://', '').replace('/', '') + ':9093'
                elif 'EntityPath' in part:
                    config_dict['kafka_topic'] = part.split('=', 1)[1].strip('"').strip()
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

    def feed(self, kafka_config: dict, kafka_topic: str, polling_interval: int, state_file: str = '') -> None:
        """Poll VATSIM and emit events to Kafka."""
        previous_pilots: Dict[str, str] = _load_state(state_file).get('pilots', {})
        previous_controllers: Dict[str, str] = _load_state(state_file).get('controllers', {})

        producer = Producer(kafka_config)
        pilots_producer = NetVatsimPilotsEventProducer(producer, kafka_topic)
        controllers_producer = NetVatsimControllersEventProducer(producer, kafka_topic)
        status_producer = NetVatsimStatusEventProducer(producer, kafka_topic)

        logging.info("Starting VATSIM feed to Kafka topic %s at %s",
                      kafka_topic, kafka_config.get('bootstrap.servers'))

        while True:
            try:
                start_time = datetime.datetime.now(datetime.timezone.utc)
                data = self.fetch_data()
                general = data.get("general", {})
                pilots: List[Dict[str, Any]] = data.get("pilots", [])
                controllers: List[Dict[str, Any]] = data.get("controllers", [])

                # Emit network status first
                status = self.build_network_status(general, len(pilots), len(controllers))
                status_producer.send_net_vatsim_network_status(
                    _callsign="status",
                    data=status,
                    flush_producer=False,
                )

                # Emit pilot positions with dedup
                pilot_count = 0
                for raw_pilot in pilots:
                    cs = raw_pilot.get("callsign", "")
                    fp = self.pilot_fingerprint(raw_pilot)
                    if previous_pilots.get(cs) != fp:
                        try:
                            pilot_data = self.parse_pilot(raw_pilot)
                            pilots_producer.send_net_vatsim_pilot_position(
                                _callsign=cs,
                                data=pilot_data,
                                flush_producer=False,
                            )
                            pilot_count += 1
                        except Exception as e:
                            logging.error("Error sending pilot %s: %s", cs, e)
                        previous_pilots[cs] = fp

                # Emit controller positions with dedup
                ctrl_count = 0
                for raw_ctrl in controllers:
                    cs = raw_ctrl.get("callsign", "")
                    fp = self.controller_fingerprint(raw_ctrl)
                    if previous_controllers.get(cs) != fp:
                        try:
                            ctrl_data = self.parse_controller(raw_ctrl)
                            controllers_producer.send_net_vatsim_controller_position(
                                _callsign=cs,
                                data=ctrl_data,
                                flush_producer=False,
                            )
                            ctrl_count += 1
                        except Exception as e:
                            logging.error("Error sending controller %s: %s", cs, e)
                        previous_controllers[cs] = fp

                producer.flush()
                end_time = datetime.datetime.now(datetime.timezone.utc)
                elapsed = (end_time - start_time).total_seconds()
                effective_interval = max(0, polling_interval - elapsed)
                logging.info(
                    "Emitted 1 status, %d pilots, %d controllers in %.1fs. Sleeping %.0fs.",
                    pilot_count, ctrl_count, elapsed, effective_interval
                )
                _save_state(state_file, {'pilots': previous_pilots, 'controllers': previous_controllers})
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


def main() -> None:
    """CLI entry point for the VATSIM bridge."""
    parser = argparse.ArgumentParser(description='VATSIM live data feed bridge to Kafka.')
    subparsers = parser.add_subparsers(dest='command')

    feed_parser = subparsers.add_parser('feed', help='Poll VATSIM and emit CloudEvents to Kafka')
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str,
                             help="Comma separated Kafka bootstrap servers",
                             default=os.getenv('KAFKA_BOOTSTRAP_SERVERS'))
    feed_parser.add_argument('--kafka-topic', type=str,
                             help="Kafka topic to send messages to",
                             default=os.getenv('KAFKA_TOPIC'))
    feed_parser.add_argument('--sasl-username', type=str,
                             help="SASL PLAIN username",
                             default=os.getenv('SASL_USERNAME'))
    feed_parser.add_argument('--sasl-password', type=str,
                             help="SASL PLAIN password",
                             default=os.getenv('SASL_PASSWORD'))
    feed_parser.add_argument('-c', '--connection-string', type=str,
                             help='Event Hubs / Fabric connection string',
                             default=os.getenv('CONNECTION_STRING'))
    polling_interval_default = 60
    if os.getenv('POLLING_INTERVAL'):
        polling_interval_default = int(os.getenv('POLLING_INTERVAL'))
    feed_parser.add_argument('-i', '--polling-interval', type=int,
                             help='Polling interval in seconds',
                             default=polling_interval_default)
    feed_parser.add_argument('--state-file', type=str,
                             default=os.getenv('STATE_FILE', os.path.expanduser('~/.vatsim_state.json')))

    args = parser.parse_args()
    bridge = VatsimBridge()

    if args.command == 'feed':
        if args.connection_string:
            config_params = bridge.parse_connection_string(args.connection_string)
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

        bridge.feed(kafka_config, kafka_topic, args.polling_interval, args.state_file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
