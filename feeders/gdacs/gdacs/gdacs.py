"""
GDACS Disaster Alert Poller
Polls the Global Disaster Alert and Coordination System RSS feed and sends
disaster alert events to a Kafka topic using SASL PLAIN authentication.
"""

import argparse
import asyncio
import logging
import os
import sys
from typing import Dict, Optional

from confluent_kafka import Producer

from gdacs_producer_data.disasteralert import DisasterAlert  # pylint: disable=import-error
from gdacs_producer_kafka_producer.producer import GDACSAlertsEventProducer  # pylint: disable=import-error

try:
    from gdacs_core import (
        GDACS_RSS_URL,
        NAMESPACES,
        USER_AGENT,
        GDACSPoller as _CoreGDACSPoller,
        _env_bool,
        parse_rss_item,
    )
except ImportError:
    from gdacs_core.gdacs import (
        GDACS_RSS_URL,
        NAMESPACES,
        USER_AGENT,
        GDACSPoller as _CoreGDACSPoller,
        _env_bool,
        parse_rss_item,
    )

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class GDACSPoller(_CoreGDACSPoller):
    """Polls the GDACS RSS feed and sends disaster alert events to Kafka."""

    def __init__(self, kafka_config: Optional[Dict[str, str]] = None,
                 kafka_topic: Optional[str] = None,
                 state_file: Optional[str] = None,
                 poll_interval: int = 300):
        super().__init__(state_file=state_file, poll_interval=poll_interval)
        self.kafka_topic = kafka_topic
        self.event_producer: Optional[GDACSAlertsEventProducer] = None
        if kafka_config is not None:
            producer = Producer(kafka_config)
            self.event_producer = GDACSAlertsEventProducer(producer, kafka_topic)  # type: ignore[arg-type]

    async def poll_and_send(self, once: bool = False):
        """Main poll loop. Downloads the feed, detects new/updated episodes, and emits events."""
        state = self.load_state()

        while True:
            try:
                xml_text = await self.fetch_feed()
                alerts = self.parse_feed(xml_text)
            except Exception:
                logger.exception("Error fetching or parsing GDACS feed")
                if once:
                    return
                await asyncio.sleep(self.poll_interval)
                continue

            count_new = 0
            count_updated = 0

            for alert in alerts:
                key = self._state_key(alert)
                prev_version = state.get(key)
                current_version = alert.version if alert.version is not None else 0

                if prev_version is not None and prev_version >= current_version:
                    continue

                if prev_version is None:
                    count_new += 1
                else:
                    count_updated += 1

                if self.event_producer:
                    self.event_producer.send_gdacs_disaster_alert(
                        _event_type=alert.event_type,
                        _event_id=alert.event_id,
                        data=alert,
                        flush_producer=False,
                    )

                state[key] = current_version

            if self.event_producer:
                self.event_producer.producer.flush()
            self.save_state(state)

            if count_new > 0 or count_updated > 0:
                logger.info("Processed %d new and %d updated disaster alerts", count_new, count_updated)
            else:
                logger.debug("No new disaster alerts")

            if once:
                return

            await asyncio.sleep(self.poll_interval)


def emit_mock_alert(event_producer: GDACSAlertsEventProducer) -> None:
    """Publish one deterministic sample alert for local and container smoke tests."""
    alert = DisasterAlert.create_instance()
    event_type = alert.event_type.value if hasattr(alert.event_type, 'value') else str(alert.event_type)
    event_producer.send_gdacs_disaster_alert(
        _event_type=event_type,
        _event_id=alert.event_id,
        data=alert,
        flush_producer=True,
    )


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse an Azure Event Hubs or Fabric Event Stream connection string and
    extract bootstrap server, topic name, username, and password.
    """
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip(
                    '"').replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=', 1)[1].strip('"')
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
    """Main entry point — parse arguments and start the GDACS poller."""
    parser = argparse.ArgumentParser(description="GDACS Disaster Alert Poller")
    parser.add_argument('--connection-string', type=str,
                        help='Azure Event Hubs or Fabric Event Stream connection string')
    parser.add_argument('--bootstrap-servers', type=str,
                        help='Comma-separated list of Kafka bootstrap servers')
    parser.add_argument('--topic', type=str,
                        help='Kafka topic to send messages to')
    parser.add_argument('--sasl-username', type=str,
                        help='SASL PLAIN username')
    parser.add_argument('--sasl-password', type=str,
                        help='SASL PLAIN password')
    parser.add_argument('--state-file', type=str,
                        help='File to persist seen event state across restarts')
    parser.add_argument('--poll-interval', type=int, default=300,
                        help='Polling interval in seconds (default: 300)')
    parser.add_argument('--once', action='store_true', default=_env_bool('ONCE_MODE', False),
                        help='Poll once and exit')
    parser.add_argument('--mock-mode', action='store_true',
                        default=_env_bool('GDACS_MOCK', False) or _env_bool('GDACS_SAMPLE_MODE', False),
                        help='Publish one deterministic mock alert and exit')
    parser.add_argument('--log-level', type=str, default='INFO',
                        help='Logging level (default: INFO)')
    _argv = sys.argv[1:]
    if _argv and _argv[0] == 'feed':
        _argv = _argv[1:]
    args = parser.parse_args(_argv)

    # Environment variable fallbacks
    if not args.connection_string:
        args.connection_string = os.getenv('GDACS_CONNECTION_STRING') or os.getenv('CONNECTION_STRING')
    if not args.bootstrap_servers:
        args.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    if not args.topic:
        args.topic = os.getenv('KAFKA_TOPIC')
    if not args.sasl_username:
        args.sasl_username = os.getenv('SASL_USERNAME')
    if not args.sasl_password:
        args.sasl_password = os.getenv('SASL_PASSWORD')
    if not args.state_file:
        args.state_file = os.getenv('GDACS_STATE_FILE')
        if not args.state_file:
            args.state_file = os.path.expanduser('~/.gdacs_state.json')
    if os.getenv('LOG_LEVEL'):
        args.log_level = os.getenv('LOG_LEVEL')

    logging.getLogger().setLevel(args.log_level.upper())

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        bootstrap_servers = config_params.get('bootstrap.servers')
        kafka_topic = config_params.get('kafka_topic')
        sasl_username = config_params.get('sasl.username')
        sasl_password = config_params.get('sasl.password')
    else:
        bootstrap_servers = args.bootstrap_servers
        kafka_topic = args.topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided via --bootstrap-servers, --connection-string, or KAFKA_BOOTSTRAP_SERVERS.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided via --topic, --connection-string, or KAFKA_TOPIC.")
        sys.exit(1)

    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
    kafka_config: Dict[str, str] = {
        'bootstrap.servers': bootstrap_servers,
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

    poller = GDACSPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        state_file=args.state_file,
        poll_interval=args.poll_interval,
    )

    if args.mock_mode:
        emit_mock_alert(poller.event_producer)
        logger.info("Published 1 mock GDACS alert")
        return

    asyncio.run(poller.poll_and_send(once=args.once))


if __name__ == "__main__":
    main()
