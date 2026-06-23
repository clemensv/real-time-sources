"""UK EA Flood Monitoring -> AMQP 1.0 bridge.

Polls the UK EA Flood Monitoring REST API and publishes events as CloudEvents over AMQP 1.0.
"""

import argparse
import logging
import os
import sys
import time
from typing import Optional, Set, Dict, List, Any
from urllib.parse import urlparse

from uk_ea_flood_monitoring.uk_ea_flood_monitoring import EAFloodMonitoringAPI, _load_state, _save_state
from uk_ea_flood_monitoring_amqp_producer_data import Station, Reading
from uk_ea_flood_monitoring_amqp_producer_amqp_producer.producer import UKGovEnvironmentEAFloodMonitoringAmqpProducer

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
        return UKGovEnvironmentEAFloodMonitoringAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            credential=cred, entra_audience=entra_audience, use_tls=tls)
    if auth_mode == 'sas':
        return UKGovEnvironmentEAFloodMonitoringAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            sas_key_name=sas_key_name, sas_key=sas_key, use_tls=tls)
    return UKGovEnvironmentEAFloodMonitoringAmqpProducer(
        host=host, address=address, port=port, username=username, password=password,
        content_mode=content_mode, use_tls=tls)


def feed(host, port, address='uk-ea-flood-monitoring', username=None, password=None, tls=False,
         content_mode='binary', auth_mode='password', entra_audience=DEFAULT_ENTRA_AUDIENCE_SERVICEBUS,
         entra_client_id=None, sas_key_name=None, sas_key=None, once=False,
         polling_interval=300, state_file=''):
    """Poll UK EA Flood Monitoring API and emit station + reading events via AMQP."""
    producer = _retry_producer_init(lambda: _build_producer(
        host, port, address, tls, content_mode, auth_mode, username, password,
        entra_audience, entra_client_id, sas_key_name, sas_key))

    api = EAFloodMonitoringAPI()
    previous = _load_state(state_file)

    # Emit reference data (stations)
    station_rivers: Dict[str, str] = {}
    try:
        stations = api.list_stations()
        logger.info("Publishing %d station reference events", len(stations))
        for s in stations:
            station_ref = s.get("stationReference", "") or s.get("notation", "")
            if not station_ref:
                continue
            river = s.get("riverName", "") or s.get("river", "") or "unknown"
            station_rivers[station_ref] = river
            station = Station(
                station_reference=station_ref,
                label=s.get("label", ""),
                river_name=river if river != "unknown" else None,
                catchment_name=s.get("catchmentName"),
                town=s.get("town"),
                lat=s.get("lat", 0.0) or 0.0,
                long=s.get("long", 0.0) or 0.0,
                notation=s.get("notation", station_ref) or station_ref,
                status=s.get("status"),
                date_opened=s.get("dateOpened"),
                river=river if river != "unknown" else None,
            )
            producer.send_station(data=station, _station_reference=station_ref, _river=river)
        logger.info("Finished publishing stations")
    except Exception as exc:
        logger.error("Failed to fetch stations: %s", exc)

    # Polling loop
    try:
        while True:
            try:
                readings = api.get_latest_readings()
                count = 0
                for r in readings:
                    measure = r.get("measure", "")
                    station_ref = r.get("stationReference", "")
                    if not station_ref and measure:
                        # Extract station ref from measure URI
                        parts = measure.rstrip("/").split("/")
                        station_ref = parts[-2] if len(parts) >= 2 else ""
                    ts = r.get("dateTime", "") or r.get("date", "")
                    obs_key = f"{station_ref}:{measure}:{ts}"
                    if obs_key in previous:
                        continue
                    river = station_rivers.get(station_ref, "unknown")
                    reading = Reading(
                        station_reference=station_ref,
                        date_time=ts,
                        value=r.get("value"),
                        measure=measure,
                        river=river if river != "unknown" else None,
                    )
                    producer.send_reading(data=reading, _station_reference=station_ref, _river=river)
                    previous[obs_key] = "1"
                    count += 1
                if len(previous) > 100000:
                    previous = dict(list(previous.items())[-50000:])
                _save_state(state_file, previous)
                logger.info("Published %d readings", count)
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
    parser = argparse.ArgumentParser(description='UK EA Flood Monitoring AMQP 1.0 bridge')
    sub = parser.add_subparsers(dest='command')
    fp = sub.add_parser('feed', help='Feed events as CloudEvents over AMQP')
    fp.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL'))
    fp.add_argument('--host', default=os.getenv('AMQP_HOST', 'localhost'))
    fp.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT', '0')) or None)
    fp.add_argument('--address', default=os.getenv('AMQP_ADDRESS', 'uk-ea-flood-monitoring'))
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
    fp.add_argument('--state-file', default=os.getenv('STATE_FILE', os.path.expanduser('~/.uk_ea_flood_monitoring_amqp_state.json')))
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
