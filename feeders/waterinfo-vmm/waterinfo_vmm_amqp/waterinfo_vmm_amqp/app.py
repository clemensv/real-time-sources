"""Waterinfo VMM (Belgium) -> AMQP 1.0 bridge.

Polls the Waterinfo VMM (Belgium) REST API and publishes events as CloudEvents over AMQP 1.0.
"""

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Optional, Set, Dict, List, Any
from urllib.parse import urlparse

from waterinfo_vmm.waterinfo_vmm import WaterinfoVMMAPI, _load_state, _save_state
from waterinfo_vmm_amqp_producer_data import Station, WaterLevelReading
from waterinfo_vmm_amqp_producer_amqp_producer.producer import BEVlaanderenWaterinfoVMMAmqpProducer

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
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
        return BEVlaanderenWaterinfoVMMAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            credential=cred, entra_audience=entra_audience, use_tls=tls)
    if auth_mode == 'sas':
        return BEVlaanderenWaterinfoVMMAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            sas_key_name=sas_key_name, sas_key=sas_key, use_tls=tls)
    return BEVlaanderenWaterinfoVMMAmqpProducer(
        host=host, address=address, port=port, username=username, password=password,
        content_mode=content_mode, use_tls=tls)


def feed(host, port, address='waterinfo-vmm', username=None, password=None, tls=False,
         content_mode='binary', auth_mode='password', entra_audience=DEFAULT_ENTRA_AUDIENCE_SERVICEBUS,
         entra_client_id=None, sas_key_name=None, sas_key=None, once=False,
         polling_interval=300, state_file=''):
    """Poll Waterinfo VMM API and emit station + water level events via AMQP."""
    producer = _retry_producer_init(lambda: _build_producer(
        host, port, address, tls, content_mode, auth_mode, username, password,
        entra_audience, entra_client_id, sas_key_name, sas_key))

    api = WaterinfoVMMAPI()
    previous = _load_state(state_file)

    # Emit reference data (stations)
    station_water_bodies: Dict[str, str] = {}
    try:
        stations_raw = api.list_stations()
        logger.info("Publishing %d station reference events", len(stations_raw))
        for row in stations_raw:
            station_no = str(row[0]) if row else ""
            if not station_no:
                continue
            name = row[1] if len(row) > 1 else ""
            water_body = row[2] if len(row) > 2 else "unknown"
            station_water_bodies[station_no] = water_body or "unknown"
            station = Station(
                station_no=station_no,
                station_name=name,
                station_id=None,
                station_latitude=0.0,
                station_longitude=0.0,
                water_body=water_body or None,
                river_name=water_body or None,
                stationparameter_name=None,
                ts_id=None,
                ts_unitname=None,
            )
            producer.send_station(data=station, _station_no=station_no, _water_body=water_body or "unknown")
        logger.info("Finished publishing stations")
    except Exception as exc:
        logger.error("Failed to fetch stations: %s", exc)

    # Polling loop
    try:
        while True:
            try:
                levels = api.get_latest_water_levels()
                count = 0
                for record in levels:
                    station_no = str(record.get("station_no", ""))
                    ts_raw = record.get("timestamp", "") or record.get("Timestamp", "")
                    obs_key = f"{station_no}:{ts_raw}"
                    if obs_key in previous:
                        continue
                    ts = datetime.fromisoformat(ts_raw) if ts_raw else datetime.now(timezone.utc)
                    water_body = station_water_bodies.get(station_no, record.get("water_body", "unknown"))
                    raw_value = record.get("value") or record.get("Value") or 0
                    reading = WaterLevelReading(
                        ts_id=record.get("ts_id", "") or "",
                        station_no=station_no,
                        station_name=record.get("station_name"),
                        timestamp=ts,
                        value=float(raw_value),
                        unit_name=record.get("unit_name") or record.get("ts_unitname"),
                        parameter_name=record.get("parameter_name") or record.get("stationparameter_name"),
                        water_body=water_body if water_body != "unknown" else None,
                    )
                    producer.send_water_level_reading(data=reading, _station_no=station_no, _water_body=water_body)
                    previous[obs_key] = "1"
                    count += 1
                if len(previous) > 100000:
                    previous = dict(list(previous.items())[-50000:])
                _save_state(state_file, previous)
                logger.info("Published %d water level readings", count)
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
    parser = argparse.ArgumentParser(description='Waterinfo VMM (Belgium) AMQP 1.0 bridge')
    sub = parser.add_subparsers(dest='command')
    fp = sub.add_parser('feed', help='Feed events as CloudEvents over AMQP')
    fp.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL'))
    fp.add_argument('--host', default=os.getenv('AMQP_HOST', 'localhost'))
    fp.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT', '0')) or None)
    fp.add_argument('--address', default=os.getenv('AMQP_ADDRESS', 'waterinfo-vmm'))
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
    fp.add_argument('--state-file', default=os.getenv('STATE_FILE', os.path.expanduser('~/.waterinfo_vmm_amqp_state.json')))
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
