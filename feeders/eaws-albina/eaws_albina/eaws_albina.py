"""EAWS ALBINA Avalanche Bulletin Poller."""
from __future__ import annotations
import argparse, datetime, os, sys, time
from typing import Dict
from confluent_kafka import Producer as KafkaProducer
from eaws_albina_core import DEFAULT_LANG, DEFAULT_REGIONS, POLL_INTERVAL_SECONDS, AlbinaPoller
from eaws_albina_producer_kafka_producer.producer import OrgEAWSALBINABulletinsEventProducer

def parse_connection_string(connection_string: str) -> Dict[str, str]:
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part: config_dict['bootstrap.servers'] = part.split('=')[1].strip('"').replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part: config_dict['kafka_topic'] = part.split('=')[1].strip('"')
            elif 'SharedAccessKeyName' in part: config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part: config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part: config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as e: raise ValueError('Invalid connection string format') from e
    if 'sasl.username' in config_dict: config_dict['security.protocol'] = 'SASL_SSL'; config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict

def main():
    parser = argparse.ArgumentParser(description='EAWS ALBINA Avalanche Bulletin Poller'); parser.add_argument('--last-polled-file', type=str, help='State file for deduplication'); parser.add_argument('--kafka-bootstrap-servers', type=str, help='Kafka bootstrap servers'); parser.add_argument('--kafka-topic', type=str, help='Kafka topic'); parser.add_argument('--sasl-username', type=str, help='SASL PLAIN username'); parser.add_argument('--sasl-password', type=str, help='SASL PLAIN password'); parser.add_argument('--connection-string', type=str, help='Azure Event Hubs or Fabric Event Stream connection string'); parser.add_argument('--regions', type=str, help='Comma-separated region codes'); parser.add_argument('--lang', type=str, default='en', help='Language code (default: en)'); parser.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE', '').lower() in ('1', 'true', 'yes')); args = parser.parse_args()
    args.connection_string = args.connection_string or os.getenv('CONNECTION_STRING'); args.last_polled_file = args.last_polled_file or os.getenv('ALBINA_LAST_POLLED_FILE') or os.path.expanduser('~/.albina_last_polled.json')
    regions = [r.strip() for r in args.regions.split(',')] if args.regions else ([r.strip() for r in os.getenv('ALBINA_REGIONS', '').split(',') if r.strip()] or DEFAULT_REGIONS)
    lang = args.lang or os.getenv('ALBINA_LANG', DEFAULT_LANG)
    if args.connection_string:
        config_params = parse_connection_string(args.connection_string); kafka_bootstrap_servers = config_params.get('bootstrap.servers'); kafka_topic = config_params.get('kafka_topic'); sasl_username = config_params.get('sasl.username'); sasl_password = config_params.get('sasl.password')
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers; kafka_topic = args.kafka_topic; sasl_username = args.sasl_username; sasl_password = args.sasl_password
    if not kafka_bootstrap_servers: print('Error: Kafka bootstrap servers must be provided.'); sys.exit(1)
    if not kafka_topic: print('Error: Kafka topic must be provided.'); sys.exit(1)
    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no'); kafka_config: Dict[str, str] = {'bootstrap.servers': kafka_bootstrap_servers}
    if sasl_username and sasl_password: kafka_config.update({'sasl.mechanisms': 'PLAIN', 'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT', 'sasl.username': sasl_username, 'sasl.password': sasl_password})
    elif tls_enabled: kafka_config['security.protocol'] = 'SSL'
    poller = AlbinaPoller(last_polled_file=args.last_polled_file, regions=regions, lang=lang); kafka_producer = KafkaProducer(kafka_config); producer = OrgEAWSALBINABulletinsEventProducer(kafka_producer, kafka_topic)
    for ref in poller.get_region_catalog(): producer.send_org_eaws_albina_avalanche_region(ref.region_id, ref, flush_producer=False)
    kafka_producer.flush()
    while True:
        try:
            today = datetime.date.today(); total = 0
            for d in [today, today - datetime.timedelta(days=1)]:
                for event in poller.fetch_for_date(d.isoformat()): producer.send_org_eaws_albina_avalanche_bulletin(event.region_id, event, flush_producer=False); total += 1
            if total: kafka_producer.flush(); print(f'Sent {total} bulletin event(s)')
        except Exception as e: print(f'Error in polling loop: {e}')
        if args.once: print('--once mode: exiting after first polling cycle'); return
        time.sleep(POLL_INTERVAL_SECONDS)
if __name__ == '__main__': main()
