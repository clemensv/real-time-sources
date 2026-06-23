"""CDEC Reservoirs -> AMQP 1.0 bridge.

Polls the California CDEC API for reservoir readings and publishes them as CloudEvents over AMQP 1.0.
"""

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, List, Any
from urllib.parse import urlparse

from cdec_reservoirs.cdec_reservoirs import CdecReservoirsAPI
from cdec_reservoirs_amqp_producer_data import ReservoirReading
from cdec_reservoirs_amqp_producer_amqp_producer.producer import GovCaWaterCdecAmqpProducer

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
BASE_URL = "https://cdec.water.ca.gov/dynamicapp/req/JSONDataServlet"
logger = logging.getLogger(__name__)


def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logger.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            time.sleep(delay)


def _build_producer(host, port, address, tls, content_mode, auth_mode, username, password,
                    entra_audience, entra_client_id, sas_key_name, sas_key):
    if auth_mode == 'entra':
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        cred = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return GovCaWaterCdecAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            credential=cred, entra_audience=entra_audience, use_tls=tls)
    if auth_mode == 'sas':
        return GovCaWaterCdecAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            sas_key_name=sas_key_name, sas_key=sas_key, use_tls=tls)
    return GovCaWaterCdecAmqpProducer(
        host=host, address=address, port=port, username=username, password=password,
        content_mode=content_mode, use_tls=tls)


def feed(host, port, address='cdec-reservoirs', username=None, password=None, tls=False,
         content_mode='binary', auth_mode='password', entra_audience=DEFAULT_ENTRA_AUDIENCE_SERVICEBUS,
         entra_client_id=None, sas_key_name=None, sas_key=None, once=False,
         polling_interval=300, state_file=''):
    """Poll CDEC API and emit reservoir readings via AMQP."""
    producer = _retry_producer_init(lambda: _build_producer(
        host, port, address, tls, content_mode, auth_mode, username, password,
        entra_audience, entra_client_id, sas_key_name, sas_key))

    api = CdecReservoirsAPI()
    previous_keys = set()
    if state_file and os.path.exists(state_file):
        import json
        try:
            with open(state_file, 'r') as f:
                previous_keys = set(json.load(f).get("seen", []))
        except Exception:
            pass

    try:
        while True:
            try:
                end = datetime.now(timezone.utc)
                start = end - timedelta(hours=24)
                readings = api.fetch_readings(
                    start.strftime("%Y-%m-%d"),
                    end.strftime("%Y-%m-%d")
                )
                count = 0
                for r in readings:
                    station_id = r.get("stationId", "") or r.get("station_id", "")
                    sensor_num = str(r.get("sensorNumber", "") or r.get("sensor_num", ""))
                    date_str = r.get("date", "") or r.get("obsDate", "")
                    obs_key = f"{station_id}:{sensor_num}:{date_str}"
                    if obs_key in previous_keys:
                        continue
                    basin = r.get("basin", "") or "unknown"
                    reading = ReservoirReading(
                        station_id=station_id,
                        sensor_num=sensor_num,
                        sensor_type=r.get("sensorType", "") or r.get("sensor_type", ""),
                        value=r.get("value"),
                        units=r.get("units", ""),
                        date=date_str,
                        dur_code=r.get("durCode", "") or r.get("dur_code", ""),
                        data_flag=r.get("dataFlag", "") or r.get("data_flag", ""),
                        basin=basin if basin != "unknown" else None,
                    )
                    producer.send_reservoir_reading(
                        data=reading, _feedurl=BASE_URL,
                        _station_id=station_id, _sensor_num=sensor_num,
                        _basin=basin)
                    previous_keys.add(obs_key)
                    count += 1
                if len(previous_keys) > 100000:
                    previous_keys = set(list(previous_keys)[-50000:])
                if state_file:
                    import json
                    with open(state_file, 'w') as f:
                        json.dump({"seen": list(previous_keys)[-50000:]}, f)
                logger.info("Published %d reservoir readings", count)
            except KeyboardInterrupt:
                break
            except Exception as exc:
                logger.error("Error in polling loop: %s", exc)
            if once:
                break
            time.sleep(polling_interval)
    finally:
        try:
            producer.close()
        except Exception:
            pass


def _parse_broker_url(url):
    parsed = urlparse(url if '://' in url else f'amqp://{url}')
    tls = (parsed.scheme or 'amqp').lower() in ('amqps', 'ssl', 'tls')
    return parsed.hostname or 'localhost', parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or '').lstrip('/') or None


def main(argv=None):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    parser = argparse.ArgumentParser(description='CDEC Reservoirs AMQP 1.0 bridge')
    sub = parser.add_subparsers(dest='command')
    fp = sub.add_parser('feed', help='Feed events as CloudEvents over AMQP')
    fp.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL'))
    fp.add_argument('--host', default=os.getenv('AMQP_HOST', 'localhost'))
    fp.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT', '0')) or None)
    fp.add_argument('--address', default=os.getenv('AMQP_ADDRESS', 'cdec-reservoirs'))
    fp.add_argument('--tls', action='store_true', default=os.getenv('AMQP_TLS', '').lower() in ('1', 'true', 'yes'))
    fp.add_argument('--username', default=os.getenv('AMQP_USERNAME'))
    fp.add_argument('--password', default=os.getenv('AMQP_PASSWORD'))
    fp.add_argument('--content-mode', default=os.getenv('AMQP_CONTENT_MODE', 'binary'), choices=['binary', 'structured'])
    fp.add_argument('--auth-mode', default=os.getenv('AMQP_AUTH_MODE', 'password'), choices=['password', 'entra', 'sas'])
    fp.add_argument('--entra-audience', default=os.getenv('AMQP_ENTRA_AUDIENCE', DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    fp.add_argument('--entra-client-id', default=os.getenv('AMQP_ENTRA_CLIENT_ID'))
    fp.add_argument('--sas-key-name', default=os.getenv('AMQP_SAS_KEY_NAME'))
    fp.add_argument('--sas-key', default=os.getenv('AMQP_SAS_KEY'))
    fp.add_argument('-i', '--polling-interval', type=int, default=int(os.getenv('POLLING_INTERVAL', '300')))
    fp.add_argument('--state-file', default=os.getenv('STATE_FILE', os.path.expanduser('~/.cdec_reservoirs_amqp_state.json')))
    fp.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE', '').lower() in ('1', 'true', 'yes'))
    args = parser.parse_args(argv)

    if args.command != 'feed':
        parser.print_help()
        return

    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port: port = args.port
        if args.tls: tls = True
        address = path or args.address
    else:
        host = args.host
        tls = args.tls or args.auth_mode == 'entra'
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
        address = args.address

    feed(host, port, address=address, username=username, password=password, tls=tls,
         content_mode=args.content_mode, auth_mode=args.auth_mode,
         entra_audience=args.entra_audience, entra_client_id=args.entra_client_id,
         sas_key_name=args.sas_key_name, sas_key=args.sas_key,
         once=args.once, polling_interval=args.polling_interval, state_file=args.state_file)


if __name__ == '__main__':
    main()
