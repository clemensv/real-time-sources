"""NWS CAP weather alerts bridge - Kafka transport."""
from __future__ import annotations
import argparse, asyncio, logging, os, sys
from typing import Dict
from confluent_kafka import Producer
from nws_alerts_core import DEFAULT_POLL_INTERVAL, DEFAULT_STATE_FILE, DEFAULT_TOPIC, NWSAlertsPoller
try:
    from nws_alerts_producer_kafka_producer.producer import NWSAlertsEventProducer
except ModuleNotFoundError:
    NWSAlertsEventProducer = None
if sys.gettrace() is not None: logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
else: logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
def parse_connection_string(connection_string: str) -> Dict[str, str]:
    config_dict: Dict[str, str] = {}
    for part in connection_string.split(';'):
        if 'Endpoint' in part: config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip('"').replace('sb://', '').replace('/', '') + ':9093'
        elif 'EntityPath' in part: config_dict['kafka_topic'] = part.split('=', 1)[1].strip('"')
        elif 'SharedAccessKeyName' in part: config_dict['sasl.username'] = '$ConnectionString'
        elif 'SharedAccessKey' in part: config_dict['sasl.password'] = connection_string.strip()
        elif 'BootstrapServer' in part: config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    if 'sasl.username' in config_dict: config_dict['security.protocol'] = 'SASL_SSL'; config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict
def main() -> None:
    parser = argparse.ArgumentParser(description='NWS CAP weather alerts bridge')
    parser.add_argument('--connection-string'); parser.add_argument('--bootstrap-servers'); parser.add_argument('--topic'); parser.add_argument('--sasl-username'); parser.add_argument('--sasl-password'); parser.add_argument('--state-file'); parser.add_argument('--poll-interval', type=int, default=DEFAULT_POLL_INTERVAL); parser.add_argument('--once', action='store_true'); parser.add_argument('--log-level', default='INFO')
    argv = sys.argv[1:]
    if argv and argv[0] == 'feed': argv = argv[1:]
    args = parser.parse_args(argv)
    args.connection_string = args.connection_string or os.getenv('NWS_CONNECTION_STRING') or os.getenv('CONNECTION_STRING'); args.bootstrap_servers = args.bootstrap_servers or os.getenv('KAFKA_BOOTSTRAP_SERVERS'); args.topic = args.topic or os.getenv('KAFKA_TOPIC', DEFAULT_TOPIC); args.sasl_username = args.sasl_username or os.getenv('SASL_USERNAME'); args.sasl_password = args.sasl_password or os.getenv('SASL_PASSWORD'); args.state_file = args.state_file or os.getenv('NWS_STATE_FILE', DEFAULT_STATE_FILE)
    if os.getenv('LOG_LEVEL'): args.log_level = os.getenv('LOG_LEVEL')
    logging.getLogger().setLevel(args.log_level.upper())
    if args.connection_string:
        config_params = parse_connection_string(args.connection_string); bootstrap_servers = config_params.get('bootstrap.servers'); kafka_topic = config_params.get('kafka_topic', args.topic); sasl_username = config_params.get('sasl.username'); sasl_password = config_params.get('sasl.password')
    else:
        bootstrap_servers = args.bootstrap_servers; kafka_topic = args.topic; sasl_username = args.sasl_username; sasl_password = args.sasl_password
    if not bootstrap_servers: print('Error: Kafka bootstrap servers required.'); sys.exit(1)
    if NWSAlertsEventProducer is None: print('Error: nws_alerts_producer_kafka_producer is not installed.'); sys.exit(1)
    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no'); kafka_config: Dict[str, str] = {'bootstrap.servers': bootstrap_servers}
    if sasl_username and sasl_password: kafka_config.update({'sasl.mechanisms':'PLAIN','security.protocol':'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT','sasl.username':sasl_username,'sasl.password':sasl_password})
    elif tls_enabled: kafka_config['security.protocol'] = 'SSL'
    poller = NWSAlertsPoller(state_file=args.state_file, poll_interval=args.poll_interval); producer = Producer(kafka_config); event_producer = NWSAlertsEventProducer(producer, kafka_topic or DEFAULT_TOPIC)
    async def run() -> None:
        while True:
            alerts = await poller.poll_once()
            for alert in alerts: event_producer.send_nws_weather_alert(_alert_id=alert.alert_id, data=alert, flush_producer=False)
            if alerts: producer.flush(); logger.info('Published %d NWS alert(s)', len(alerts))
            if args.once: return
            await asyncio.sleep(args.poll_interval)
    asyncio.run(run())
if __name__ == '__main__': main()
