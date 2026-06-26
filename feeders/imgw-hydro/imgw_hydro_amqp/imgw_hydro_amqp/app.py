"""IMGW Hydrology (Poland) -> AMQP 1.0 bridge.

Polls the IMGW Hydrology (Poland) REST API and publishes events as CloudEvents over AMQP 1.0.
"""

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Optional, Set, Dict, List, Any
from urllib.parse import urlparse

from imgw_hydro.imgw_hydro import IMGWHydroAPI, _load_state, _save_state
from imgw_hydro_amqp_producer_data import Station, WaterLevelObservation
from imgw_hydro_amqp_producer_amqp_producer.producer import PLGovIMGWHydroAmqpProducer

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
        return PLGovIMGWHydroAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            credential=cred, entra_audience=entra_audience, use_tls=tls)
    if auth_mode == 'sas':
        return PLGovIMGWHydroAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            sas_key_name=sas_key_name, sas_key=sas_key, use_tls=tls)
    return PLGovIMGWHydroAmqpProducer(
        host=host, address=address, port=port, username=username, password=password,
        content_mode=content_mode, use_tls=tls)


def feed(host, port, address='imgw-hydro', username=None, password=None, tls=False,
         content_mode='binary', auth_mode='password', entra_audience=DEFAULT_ENTRA_AUDIENCE_SERVICEBUS,
         entra_client_id=None, sas_key_name=None, sas_key=None, once=False,
         polling_interval=300, state_file=''):
    """Poll IMGW API and emit station + observation events via AMQP."""
    producer = _retry_producer_init(lambda: _build_producer(
        host, port, address, tls, content_mode, auth_mode, username, password,
        entra_audience, entra_client_id, sas_key_name, sas_key))

    api = IMGWHydroAPI()
    previous = _load_state(state_file)

    # Emit reference data (stations)
    try:
        data_list = api.get_all_data()
        seen_stations = set()
        for item in data_list:
            station_id = str(item.get("id_stacji", "") or item.get("station_id", ""))
            if not station_id or station_id in seen_stations:
                continue
            seen_stations.add(station_id)
            station = Station(
                station_id=station_id,
                station_name=item.get("stacja", "") or item.get("station_name", ""),
                river=item.get("rzeka", None) or item.get("river", None),
                voivodeship=item.get("wojewodztwo", None) or item.get("voivodeship", None),
                basin=item.get("dorzecze", None) or item.get("basin", None),
                latitude=item.get("latitude"),
                longitude=item.get("longitude"),
            )
            basin = str(station.basin or 'unknown')
            producer.send_station(data=station, _station_id=station_id, _basin=basin)
        logger.info("Published %d stations", len(seen_stations))
    except Exception as exc:
        logger.error("Failed to fetch stations: %s", exc)

    # Polling loop
    try:
        while True:
            try:
                data_list = api.get_all_data()
                count = 0
                for item in data_list:
                    station_id = str(item.get("id_stacji", "") or item.get("station_id", ""))
                    obs_key = f"{station_id}:{item.get('stan_wody_data_pomiaru', item.get('date', ''))}"
                    if obs_key in previous:
                        continue
                    wl_ts_raw = item.get("stan_wody_data_pomiaru", "") or item.get("date", "")
                    wl_ts = datetime.fromisoformat(wl_ts_raw.replace("Z", "+00:00")) if wl_ts_raw else datetime.now(timezone.utc)
                    wt_raw = item.get("temperatura_wody_data_pomiaru") or item.get("water_temperature_timestamp")
                    wt_ts = datetime.fromisoformat(wt_raw.replace("Z", "+00:00")) if wt_raw else None
                    disch_raw = item.get("przeplyw_data_pomiaru") or item.get("discharge_timestamp")
                    disch_ts = datetime.fromisoformat(disch_raw.replace("Z", "+00:00")) if disch_raw else None
                    obs = WaterLevelObservation(
                        station_id=station_id,
                        station_name=item.get("stacja", "") or item.get("station_name", ""),
                        water_level=float(item["stan_wody"]) if item.get("stan_wody") is not None else float(item.get("water_level", 0) or 0),
                        water_level_timestamp=wl_ts,
                        water_temperature=float(item["temperatura_wody"]) if item.get("temperatura_wody") is not None else (float(item["water_temperature"]) if item.get("water_temperature") is not None else None),
                        water_temperature_timestamp=wt_ts,
                        discharge=float(item["przeplyw"]) if item.get("przeplyw") is not None else (float(item["discharge"]) if item.get("discharge") is not None else None),
                        discharge_timestamp=disch_ts,
                        ice_phenomenon_code=item.get("zjawisko_lodowe") or item.get("ice_phenomenon_code"),
                        overgrowth_code=item.get("zjawisko_zarastania") or item.get("overgrowth_code"),
                        river=item.get("rzeka", None) or item.get("river", None),
                        voivodeship=item.get("wojewodztwo", None) or item.get("voivodeship", None),
                        basin=item.get("dorzecze", None) or item.get("basin", None),
                    )
                    basin = str(obs.basin or 'unknown')
                    producer.send_water_level_observation(data=obs, _station_id=station_id, _basin=basin)
                    previous[obs_key] = "1"
                    count += 1
                if len(previous) > 100000:
                    keys = list(previous.keys())[-50000:]
                    previous = {k: previous[k] for k in keys}
                _save_state(state_file, previous)
                logger.info("Published %d observations", count)
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
    parser = argparse.ArgumentParser(description='IMGW Hydrology (Poland) AMQP 1.0 bridge')
    sub = parser.add_subparsers(dest='command')
    fp = sub.add_parser('feed', help='Feed events as CloudEvents over AMQP')
    fp.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL'))
    fp.add_argument('--host', default=os.getenv('AMQP_HOST', 'localhost'))
    fp.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT', '0')) or None)
    fp.add_argument('--address', default=os.getenv('AMQP_ADDRESS', 'imgw-hydro'))
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
    fp.add_argument('--state-file', default=os.getenv('STATE_FILE', os.path.expanduser('~/.imgw_hydro_amqp_state.json')))
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
