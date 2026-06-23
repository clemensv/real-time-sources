"""SNOTEL -> AMQP 1.0 bridge.

Polls the USDA NRCS SNOTEL stations and publishes snow observations as CloudEvents over AMQP 1.0.
"""

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Optional, Dict, List
from urllib.parse import urlparse

from snotel.snotel import (
    SnotelPoller, STATION_METADATA, DEFAULT_STATION_TRIPLETS,
    parse_csv_response, parse_observation_row, parse_float
)
from snotel_amqp_producer_data import Station, SnowObservation
from snotel_amqp_producer_amqp_producer.producer import GovUsdaNrcsSnotelAmqpProducer

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
SNOTEL_REPORT_URL = "https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customSingleStationReport/daily"
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
        return GovUsdaNrcsSnotelAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            credential=cred, entra_audience=entra_audience, use_tls=tls)
    if auth_mode == 'sas':
        return GovUsdaNrcsSnotelAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            sas_key_name=sas_key_name, sas_key=sas_key, use_tls=tls)
    return GovUsdaNrcsSnotelAmqpProducer(
        host=host, address=address, port=port, username=username, password=password,
        content_mode=content_mode, use_tls=tls)


def _fetch_station_csv(triplet: str) -> str:
    """Fetch SNOTEL CSV report for a station."""
    import requests
    url = f"{SNOTEL_REPORT_URL}/{triplet}/-7,0/WTEQ::value,PREC::value,TOBS::value,SNWD::value"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return resp.text


def feed(host, port, address='snotel', username=None, password=None, tls=False,
         content_mode='binary', auth_mode='password', entra_audience=DEFAULT_ENTRA_AUDIENCE_SERVICEBUS,
         entra_client_id=None, sas_key_name=None, sas_key=None, once=False,
         polling_interval=3600, state_file=''):
    """Poll SNOTEL stations and emit station + snow observation events via AMQP."""
    producer = _retry_producer_init(lambda: _build_producer(
        host, port, address, tls, content_mode, auth_mode, username, password,
        entra_audience, entra_client_id, sas_key_name, sas_key))

    station_triplets = DEFAULT_STATION_TRIPLETS
    import json
    state: Dict = {}
    if state_file and os.path.exists(state_file):
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
        except Exception:
            pass

    # Emit station reference data
    try:
        for triplet in station_triplets:
            meta = STATION_METADATA.get(triplet)
            if not meta:
                continue
            station = Station(
                station_triplet=triplet,
                name=meta["name"],
                state=meta["state"],
                elevation=meta.get("elevation"),
                latitude=meta.get("latitude"),
                longitude=meta.get("longitude"),
            )
            producer.send_station(data=station, _station_triplet=triplet, _state=meta["state"])
        logger.info("Emitted %d station reference events", len(station_triplets))
    except Exception as exc:
        logger.error("Failed to emit stations: %s", exc)

    # Polling loop
    try:
        while True:
            total_count = 0
            for triplet in station_triplets:
                try:
                    csv_text = _fetch_station_csv(triplet)
                    _, rows = parse_csv_response(csv_text)
                    last_ts = state.get("last_timestamps", {}).get(triplet)
                    for row in rows:
                        obs = parse_observation_row(triplet, row)
                        if obs is None:
                            continue
                        obs_ts = obs.date_time.isoformat() if obs.date_time else ""
                        if last_ts and obs_ts <= last_ts:
                            continue
                        st = obs.state or STATION_METADATA.get(triplet, {}).get("state", "")
                        producer.send_snow_observation(data=obs, _station_triplet=triplet, _state=st)
                        total_count += 1
                        if not last_ts or obs_ts > last_ts:
                            state.setdefault("last_timestamps", {})[triplet] = obs_ts
                            last_ts = obs_ts
                except Exception as exc:
                    logger.warning("Failed to poll %s: %s", triplet, exc)
            if state_file:
                try:
                    with open(state_file, 'w') as f:
                        json.dump(state, f)
                except Exception:
                    pass
            logger.info("Published %d snow observations", total_count)
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
    parser = argparse.ArgumentParser(description='SNOTEL AMQP 1.0 bridge')
    sub = parser.add_subparsers(dest='command')
    fp = sub.add_parser('feed', help='Feed events as CloudEvents over AMQP')
    fp.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL'))
    fp.add_argument('--host', default=os.getenv('AMQP_HOST', 'localhost'))
    fp.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT', '0')) or None)
    fp.add_argument('--address', default=os.getenv('AMQP_ADDRESS', 'snotel'))
    fp.add_argument('--tls', action='store_true', default=os.getenv('AMQP_TLS', '').lower() in ('1', 'true', 'yes'))
    fp.add_argument('--username', default=os.getenv('AMQP_USERNAME'))
    fp.add_argument('--password', default=os.getenv('AMQP_PASSWORD'))
    fp.add_argument('--content-mode', default=os.getenv('AMQP_CONTENT_MODE', 'binary'), choices=['binary', 'structured'])
    fp.add_argument('--auth-mode', default=os.getenv('AMQP_AUTH_MODE', 'password'), choices=['password', 'entra', 'sas'])
    fp.add_argument('--entra-audience', default=os.getenv('AMQP_ENTRA_AUDIENCE', DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    fp.add_argument('--entra-client-id', default=os.getenv('AMQP_ENTRA_CLIENT_ID'))
    fp.add_argument('--sas-key-name', default=os.getenv('AMQP_SAS_KEY_NAME'))
    fp.add_argument('--sas-key', default=os.getenv('AMQP_SAS_KEY'))
    fp.add_argument('-i', '--polling-interval', type=int, default=int(os.getenv('POLLING_INTERVAL', '3600')))
    fp.add_argument('--state-file', default=os.getenv('STATE_FILE', os.path.expanduser('~/.snotel_amqp_state.json')))
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
