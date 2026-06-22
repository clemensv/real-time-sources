"""US CBP Border Wait Times bridge to Kafka."""
from __future__ import annotations
import argparse, logging, os, sys, time
from datetime import datetime, timedelta, timezone
from typing import Dict
from confluent_kafka import Producer
from cbp_border_wait_core import CbpBorderWaitAPI, _load_state, _save_state
from cbp_border_wait_producer_kafka_producer.producer import GovCbpBorderwaitEventProducer
if sys.gettrace() is not None: logging.basicConfig(level=logging.DEBUG)
else: logging.basicConfig(level=logging.INFO)
def _parse_connection_string(connection_string: str):
    config_dict = {}; kafka_topic = None
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part: config_dict['bootstrap.servers'] = part.split('=')[1].strip('"').replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part: kafka_topic = part.split('=')[1].strip('"')
            elif 'SharedAccessKeyName' in part: config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part: config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part: config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as exc: raise ValueError('Invalid connection string format') from exc
    if 'sasl.username' in config_dict: config_dict['security.protocol'] = 'SASL_SSL'; config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict, kafka_topic
def feed(args):
    connection_string = args.connection_string or os.environ.get('CONNECTION_STRING', '')
    if not connection_string: logging.error('CONNECTION_STRING is required'); sys.exit(1)
    kafka_config, kafka_topic = _parse_connection_string(connection_string)
    tls_enabled = os.environ.get('KAFKA_ENABLE_TLS', 'true').lower()
    if tls_enabled == 'false' and 'security.protocol' not in kafka_config: kafka_config['security.protocol'] = 'PLAINTEXT'
    polling_interval = int(args.polling_interval or os.environ.get('POLLING_INTERVAL', '3600')); state_file = args.state_file or os.environ.get('STATE_FILE', ''); once = bool(getattr(args, 'once', False)); previous_timestamps: Dict[str, str] = _load_state(state_file)
    producer = Producer(kafka_config); event_producer = GovCbpBorderwaitEventProducer(producer, kafka_topic); api = CbpBorderWaitAPI()
    logging.info('Starting CBP Border Wait Times feed to Kafka topic %s at %s', kafka_topic, kafka_config.get('bootstrap.servers', 'unknown'))
    try:
        raw_ports = api.fetch_ports()
        for raw in raw_ports:
            try:
                port = api.parse_port(raw); event_producer.send_gov_cbp_borderwait_port(_port_number=port.port_number, data=port, flush_producer=False)
            except Exception as exc: logging.error('Error sending port %s: %s', raw.get('port_number', '?'), exc)
        producer.flush(); logging.info('Sent %d port reference records', len(raw_ports))
    except Exception as exc: logging.error('Failed to fetch port reference data: %s', exc)
    while True:
        try:
            count = 0; start_time = datetime.now(timezone.utc); raw_ports = api.fetch_ports()
            for raw in raw_ports:
                port_num = raw.get('port_number', ''); dedup_key = f"{raw.get('date', '')}T{raw.get('time', '')}"
                if previous_timestamps.get(port_num) == dedup_key: continue
                try:
                    wait_time = api.parse_wait_time(raw); event_producer.send_gov_cbp_borderwait_wait_time(_port_number=wait_time.port_number, data=wait_time, flush_producer=False); count += 1; previous_timestamps[port_num] = dedup_key
                except Exception as exc: logging.error('Error sending wait time for port %s: %s', port_num, exc)
            producer.flush(); elapsed = (datetime.now(timezone.utc) - start_time).total_seconds(); effective_interval = max(0, polling_interval - elapsed); logging.info('Sent %d wait time updates in %.1f s. Next poll at %s.', count, elapsed, (datetime.now(timezone.utc) + timedelta(seconds=effective_interval)).isoformat()); _save_state(state_file, previous_timestamps)
            if once: logging.info('--once mode: exiting after first polling cycle'); break
            if effective_interval > 0: time.sleep(effective_interval)
        except KeyboardInterrupt:
            logging.info('Exiting...'); break
        except Exception as exc:
            logging.error('Error occurred: %s', exc)
            if once: logging.info('--once mode: exiting after first polling cycle (with error)'); break
            logging.info('Retrying in %d seconds...', polling_interval); time.sleep(polling_interval)
def main():
    parser = argparse.ArgumentParser(description='US CBP Border Wait Times bridge to Kafka'); subparsers = parser.add_subparsers(dest='command'); feed_parser = subparsers.add_parser('feed', help='Start the feed loop'); feed_parser.add_argument('--connection-string', help='Kafka connection string'); feed_parser.add_argument('--polling-interval', type=int, default=3600, help='Polling interval in seconds (default: 3600)'); feed_parser.add_argument('--state-file', help='Path to state persistence file'); feed_parser.add_argument('--once', action='store_true', default=os.environ.get('ONCE_MODE', '').lower() in ('1', 'true', 'yes'), help='Exit after one polling cycle (also via ONCE_MODE env var). Useful for scheduled execution in Fabric notebooks.'); args = parser.parse_args(); feed(args) if args.command == 'feed' else parser.print_help()
if __name__ == '__main__': main()
