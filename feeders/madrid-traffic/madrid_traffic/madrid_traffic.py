"""Madrid Real-Time Traffic (Informo) Bridge."""
from __future__ import annotations
import argparse, os, sys, time
from datetime import datetime, timezone
from typing import Dict
from confluent_kafka import Producer
from madrid_traffic_core import POLL_INTERVAL_SECONDS, REFERENCE_REFRESH_SECONDS, MadridTrafficPoller, parse_pm_xml
from madrid_traffic_producer_kafka_producer.producer import EsMadridInformoEventProducer

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
    parser = argparse.ArgumentParser(description='Madrid Real-Time Traffic (Informo) Bridge'); parser.add_argument('--kafka-bootstrap-servers', type=str); parser.add_argument('--kafka-topic', type=str); parser.add_argument('--sasl-username', type=str); parser.add_argument('--sasl-password', type=str); parser.add_argument('--connection-string', type=str); parser.add_argument('--once', action='store_true'); _argv = sys.argv[1:]; _argv = _argv[1:] if _argv and _argv[0] == 'feed' else _argv; args = parser.parse_args(_argv)
    once_mode = args.once or os.getenv('ONCE_MODE', '').lower() in ('true', '1', 'yes'); args.connection_string = args.connection_string or os.getenv('CONNECTION_STRING')
    if args.connection_string:
        config_params = parse_connection_string(args.connection_string); kafka_bootstrap_servers = config_params.get('bootstrap.servers'); kafka_topic = config_params.get('kafka_topic'); sasl_username = config_params.get('sasl.username'); sasl_password = config_params.get('sasl.password')
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers; kafka_topic = args.kafka_topic; sasl_username = args.sasl_username; sasl_password = args.sasl_password
    if not kafka_bootstrap_servers: print('Error: Kafka bootstrap servers must be provided via --kafka-bootstrap-servers or CONNECTION_STRING.'); sys.exit(1)
    if not kafka_topic: print('Error: Kafka topic must be provided via --kafka-topic or CONNECTION_STRING.'); sys.exit(1)
    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no'); kafka_config: Dict[str, str] = {'bootstrap.servers': kafka_bootstrap_servers}
    if sasl_username and sasl_password: kafka_config.update({'sasl.mechanisms': 'PLAIN', 'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT', 'sasl.username': sasl_username, 'sasl.password': sasl_password})
    elif tls_enabled: kafka_config['security.protocol'] = 'SSL'
    poller = MadridTrafficPoller(); producer = Producer(kafka_config); event_producer = EsMadridInformoEventProducer(producer, kafka_topic)
    while True:
        try:
            xml_text = poller.fetch_xml()
            if xml_text is None:
                if once_mode: break
                time.sleep(POLL_INTERVAL_SECONDS); continue
            sensors, _ = parse_pm_xml(xml_text); poll_time = datetime.now(timezone.utc); now = time.monotonic()
            if now - poller._last_reference_time >= REFERENCE_REFRESH_SECONDS or poller._last_reference_time == 0.0:
                for mp in poller.get_reference_data(sensors): event_producer.send_es_madrid_informo_measurement_point(mp.sensor_id, mp, flush_producer=False)
                producer.flush(); poller._last_reference_time = now
            _, readings = poller.get_traffic_readings(sensors, poll_time)
            for reading in readings: event_producer.send_es_madrid_informo_traffic_reading(reading.sensor_id, reading, flush_producer=False)
            if readings: producer.flush()
        except Exception as e: print(f'Error in polling loop: {e}')
        if once_mode: break
        time.sleep(POLL_INTERVAL_SECONDS)
if __name__ == '__main__': main()
