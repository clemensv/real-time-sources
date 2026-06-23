"""Nepal BIPAD Hydrology -> AMQP 1.0 bridge.

Polls the Nepal BIPAD Hydrology REST API and publishes events as CloudEvents over AMQP 1.0.
"""

import argparse
import logging
import os
import sys
import time
from typing import Optional, Set, Dict, List, Any
from urllib.parse import urlparse

from nepal_bipad_hydrology.nepal_bipad_hydrology import NepalBipadHydrologyAPI, _load_state, _save_state
from nepal_bipad_hydrology_amqp_producer_data import RiverStation, WaterLevelReading
from nepal_bipad_hydrology_amqp_producer_amqp_producer.producer import NpGovBipadHydrologyAmqpProducer

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
        return NpGovBipadHydrologyAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            credential=cred, entra_audience=entra_audience, use_tls=tls)
    if auth_mode == 'sas':
        return NpGovBipadHydrologyAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            sas_key_name=sas_key_name, sas_key=sas_key, use_tls=tls)
    return NpGovBipadHydrologyAmqpProducer(
        host=host, address=address, port=port, username=username, password=password,
        content_mode=content_mode, use_tls=tls)


def feed(host, port, address='nepal-bipad-hydrology', username=None, password=None, tls=False,
         content_mode='binary', auth_mode='password', entra_audience=DEFAULT_ENTRA_AUDIENCE_SERVICEBUS,
         entra_client_id=None, sas_key_name=None, sas_key=None, once=False,
         polling_interval=300, state_file=''):
    """Poll Nepal BIPAD Hydrology API and emit river station + water level events via AMQP."""
    producer = _retry_producer_init(lambda: _build_producer(
        host, port, address, tls, content_mode, auth_mode, username, password,
        entra_audience, entra_client_id, sas_key_name, sas_key))

    api = NepalBipadHydrologyAPI()
    previous = _load_state(state_file)
    feed_url = api.base_url if hasattr(api, 'base_url') else "https://biframeapi.bipad.gov.np"

    # Emit reference data (stations)
    station_basins: Dict[str, str] = {}
    try:
        stations_raw = api.fetch_all_stations()
        logger.info("Publishing %d river station events", len(stations_raw))
        for s in stations_raw:
            station_id = str(s.get("id", "") or s.get("station_id", ""))
            if not station_id:
                continue
            basin = s.get("basin", "") or s.get("river_basin", "") or "unknown"
            station_basins[station_id] = basin
            station = RiverStation(
                station_id=station_id,
                title=s.get("title", "") or s.get("name", ""),
                basin=basin if basin != "unknown" else None,
                latitude=s.get("latitude") or s.get("lat"),
                longitude=s.get("longitude") or s.get("lng"),
                elevation=s.get("elevation"),
                danger_level=s.get("danger_level"),
                warning_level=s.get("warning_level"),
                description=s.get("description"),
                data_source=s.get("data_source"),
                province=s.get("province"),
                district=s.get("district"),
                municipality=s.get("municipality"),
                ward=s.get("ward"),
            )
            producer.send_river_station(data=station, _feedurl=feed_url, _station_id=station_id, _basin=basin)
        logger.info("Finished publishing stations")
    except Exception as exc:
        logger.error("Failed to fetch stations: %s", exc)

    # Polling loop - re-fetch stations for water level data
    try:
        while True:
            try:
                stations_raw = api.fetch_all_stations()
                count = 0
                for s in stations_raw:
                    station_id = str(s.get("id", "") or s.get("station_id", ""))
                    wl = s.get("water_level") or s.get("latest_water_level")
                    if wl is None:
                        continue
                    ts = s.get("water_level_on", "") or s.get("measured_at", "")
                    obs_key = f"{station_id}:{ts}"
                    if obs_key in previous:
                        continue
                    basin = station_basins.get(station_id, "unknown")
                    reading = WaterLevelReading(
                        station_id=station_id,
                        title=s.get("title", "") or s.get("name", ""),
                        basin=basin if basin != "unknown" else None,
                        water_level=wl,
                        danger_level=s.get("danger_level"),
                        warning_level=s.get("warning_level"),
                        status=s.get("status"),
                        trend=s.get("trend"),
                        water_level_on=ts,
                    )
                    producer.send_water_level_reading(data=reading, _feedurl=feed_url, _station_id=station_id, _basin=basin)
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
    parser = argparse.ArgumentParser(description='Nepal BIPAD Hydrology AMQP 1.0 bridge')
    sub = parser.add_subparsers(dest='command')
    fp = sub.add_parser('feed', help='Feed events as CloudEvents over AMQP')
    fp.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL'))
    fp.add_argument('--host', default=os.getenv('AMQP_HOST', 'localhost'))
    fp.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT', '0')) or None)
    fp.add_argument('--address', default=os.getenv('AMQP_ADDRESS', 'nepal-bipad-hydrology'))
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
    fp.add_argument('--state-file', default=os.getenv('STATE_FILE', os.path.expanduser('~/.nepal_bipad_hydrology_amqp_state.json')))
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
