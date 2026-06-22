"""NINA/BBK German civil protection warnings bridge."""
from __future__ import annotations
import argparse, asyncio, logging, os, sys
from typing import Dict
from confluent_kafka import Producer
from nina_bbk_core import DEFAULT_POLL_INTERVAL, DEFAULT_STATE_FILE, DEFAULT_TOPIC, NINABBKPoller, PROVIDERS
from nina_bbk_producer_kafka_producer.producer import NINAWarningsEventProducer
if sys.gettrace() is not None: logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else: logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
def parse_connection_string(connection_string: str) -> Dict[str, str]:
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part: config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip('"').replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part: config_dict['kafka_topic'] = part.split('=', 1)[1].strip('"')
            elif 'SharedAccessKeyName' in part: config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part: config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part: config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as e: raise ValueError('Invalid connection string format') from e
    if 'sasl.username' in config_dict: config_dict['security.protocol'] = 'SASL_SSL'; config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict
def main():
    parser = argparse.ArgumentParser(description='NINA/BBK German civil protection warnings bridge'); parser.add_argument('--connection-string', type=str, help='Event Hubs connection string'); parser.add_argument('--bootstrap-servers', type=str, help='Kafka bootstrap servers'); parser.add_argument('--topic', type=str, help='Kafka topic'); parser.add_argument('--sasl-username', type=str, help='SASL username'); parser.add_argument('--sasl-password', type=str, help='SASL password'); parser.add_argument('--state-file', type=str, help='State file path'); parser.add_argument('--poll-interval', type=int, default=DEFAULT_POLL_INTERVAL, help='Poll interval in seconds'); parser.add_argument('--providers', type=str, help='Comma-separated list of providers'); parser.add_argument('--once', action='store_true', help='Poll once and exit'); parser.add_argument('--log-level', type=str, default='INFO', help='Logging level'); _argv = sys.argv[1:]; _argv = _argv[1:] if _argv and _argv[0] == 'feed' else _argv; args = parser.parse_args(_argv)
    args.connection_string = args.connection_string or os.getenv('NINA_BBK_CONNECTION_STRING') or os.getenv('CONNECTION_STRING'); args.bootstrap_servers = args.bootstrap_servers or os.getenv('KAFKA_BOOTSTRAP_SERVERS'); args.topic = args.topic or os.getenv('KAFKA_TOPIC', DEFAULT_TOPIC); args.sasl_username = args.sasl_username or os.getenv('SASL_USERNAME'); args.sasl_password = args.sasl_password or os.getenv('SASL_PASSWORD'); args.state_file = args.state_file or os.getenv('NINA_BBK_STATE_FILE', DEFAULT_STATE_FILE)
    if os.getenv('LOG_LEVEL'): args.log_level = os.getenv('LOG_LEVEL')
    logging.getLogger().setLevel(args.log_level.upper()); providers = [p.strip() for p in args.providers.split(',')] if args.providers else PROVIDERS
    if args.connection_string:
        config_params = parse_connection_string(args.connection_string); bootstrap_servers = config_params.get('bootstrap.servers'); kafka_topic = config_params.get('kafka_topic', args.topic); sasl_username = config_params.get('sasl.username'); sasl_password = config_params.get('sasl.password')
    else:
        bootstrap_servers = args.bootstrap_servers; kafka_topic = args.topic; sasl_username = args.sasl_username; sasl_password = args.sasl_password
    if not bootstrap_servers: print('Error: Kafka bootstrap servers required via --bootstrap-servers, --connection-string, or KAFKA_BOOTSTRAP_SERVERS.'); sys.exit(1)
    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no'); kafka_config: Dict[str, str] = {'bootstrap.servers': bootstrap_servers}
    if sasl_username and sasl_password: kafka_config.update({'sasl.mechanisms': 'PLAIN', 'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT', 'sasl.username': sasl_username, 'sasl.password': sasl_password})
    elif tls_enabled: kafka_config['security.protocol'] = 'SSL'
    poller = NINABBKPoller(state_file=args.state_file, poll_interval=args.poll_interval, providers=providers); producer = Producer(kafka_config); event_producer = NINAWarningsEventProducer(producer, kafka_topic or DEFAULT_TOPIC)
    async def run() -> None:
        while True:
            warnings = await poller.poll_once()
            for warning in warnings: event_producer.send_nina_civil_warning(_warning_id=warning.warning_id, data=warning, flush_producer=False)
            if warnings: event_producer.producer.flush(); logger.info('Processed %d warning(s)', len(warnings))
            else: logger.debug('No new warnings')
            if args.once: return
            await asyncio.sleep(args.poll_interval)
    asyncio.run(run())
if __name__ == '__main__': main()
