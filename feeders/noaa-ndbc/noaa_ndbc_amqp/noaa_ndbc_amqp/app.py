"""NOAA NDBC -> AMQP 1.0 bridge.

Polls the NOAA National Data Buoy Center for buoy observations and publishes them as CloudEvents over AMQP 1.0.
"""

import argparse
import logging
import os
import sys
import time
import json
import requests
from datetime import datetime, timezone
from typing import Optional, Dict, List
from urllib.parse import urlparse

from noaa_ndbc.noaa_ndbc import (
    NDBCBuoyPoller, parse_float
)
from noaa_ndbc_amqp_producer_data import (
    BuoyStation, BuoyObservation
)
from noaa_ndbc_amqp_producer_amqp_producer.producer import MicrosoftOpenDataUSNOAANDBCAmqpProducer

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
logger = logging.getLogger(__name__)

REALTIME2_INDEX_URL = "https://www.ndbc.noaa.gov/data/realtime2/"
STATIONS_URL = "https://www.ndbc.noaa.gov/activestations.xml"


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
        return MicrosoftOpenDataUSNOAANDBCAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            credential=cred, entra_audience=entra_audience, use_tls=tls)
    if auth_mode == 'sas':
        return MicrosoftOpenDataUSNOAANDBCAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            sas_key_name=sas_key_name, sas_key=sas_key, use_tls=tls)
    return MicrosoftOpenDataUSNOAANDBCAmqpProducer(
        host=host, address=address, port=port, username=username, password=password,
        content_mode=content_mode, use_tls=tls)


def _fetch_stations_xml() -> List[Dict]:
    """Fetch active station list from NDBC XML."""
    import xml.etree.ElementTree as ET
    resp = requests.get(STATIONS_URL, timeout=60)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    stations = []
    for station_elem in root.iter('station'):
        attrs = station_elem.attrib
        stations.append({
            "station_id": attrs.get("id", ""),
            "name": attrs.get("name", ""),
            "owner": attrs.get("owner", ""),
            "type": attrs.get("type", ""),
            "lat": attrs.get("lat"),
            "lon": attrs.get("lon"),
            "region": attrs.get("pgm", "") or "unknown",
        })
    return stations


def _fetch_latest_observations(station_ids: List[str]) -> List[Dict]:
    """Fetch latest standard meteorological observations for given stations."""
    observations = []
    for sid in station_ids[:50]:  # Limit to avoid overwhelming the API
        try:
            url = f"https://www.ndbc.noaa.gov/data/realtime2/{sid}.txt"
            resp = requests.get(url, timeout=30)
            if resp.status_code != 200:
                continue
            lines = resp.text.strip().split("\n")
            if len(lines) < 3:
                continue
            # Parse header and first data line (most recent)
            headers = lines[0].replace("#", "").split()
            data_line = lines[2].split()  # Skip units line
            if len(data_line) < len(headers):
                continue
            obs = dict(zip(headers, data_line))
            obs["station_id"] = sid
            observations.append(obs)
        except Exception:
            continue
    return observations


def feed(host, port, address='noaa-ndbc', username=None, password=None, tls=False,
         content_mode='binary', auth_mode='password', entra_audience=DEFAULT_ENTRA_AUDIENCE_SERVICEBUS,
         entra_client_id=None, sas_key_name=None, sas_key=None, once=False,
         polling_interval=600, state_file=''):
    """Poll NOAA NDBC and emit buoy station + observation events via AMQP."""
    producer = _retry_producer_init(lambda: _build_producer(
        host, port, address, tls, content_mode, auth_mode, username, password,
        entra_audience, entra_client_id, sas_key_name, sas_key))

    state: Dict = {}
    if state_file and os.path.exists(state_file):
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
        except Exception:
            pass

    # Emit station reference data
    station_regions: Dict[str, str] = {}
    try:
        stations_raw = _fetch_stations_xml()
        logger.info("Publishing %d buoy station reference events", len(stations_raw))
        for s in stations_raw:
            sid = s["station_id"]
            region = s.get("region", "unknown") or "unknown"
            station_regions[sid] = region
            station = BuoyStation(
                station_id=sid,
                name=s.get("name", ""),
                owner=s.get("owner", ""),
                station_type=s.get("type", ""),
                hull=None,
                latitude=float(s["lat"]) if s.get("lat") else None,
                longitude=float(s["lon"]) if s.get("lon") else None,
                timezone=None,
                region=region,
            )
            producer.send_buoy_station(data=station, _station_id=sid, _region=region)
        logger.info("Finished publishing stations")
    except Exception as exc:
        logger.error("Failed to fetch stations: %s", exc)

    # Polling loop
    station_ids = list(station_regions.keys()) or [s["station_id"] for s in stations_raw[:50]]
    try:
        while True:
            try:
                obs_list = _fetch_latest_observations(station_ids)
                count = 0
                for obs_raw in obs_list:
                    sid = obs_raw.get("station_id", "")
                    yr = obs_raw.get("YY", "")
                    mo = obs_raw.get("MM", "")
                    dd = obs_raw.get("DD", "")
                    hh = obs_raw.get("hh", "")
                    mm_val = obs_raw.get("mm", "00")
                    obs_key = f"{sid}:{yr}{mo}{dd}{hh}{mm_val}"
                    if obs_key in state.get("seen", {}):
                        continue
                    region = station_regions.get(sid, "unknown")
                    try:
                        ts = datetime(int(yr), int(mo), int(dd), int(hh), int(mm_val), tzinfo=timezone.utc)
                    except (ValueError, TypeError):
                        ts = None
                    obs = BuoyObservation(
                        station_id=sid,
                        latitude=parse_float(obs_raw.get("LAT", "")) if obs_raw.get("LAT") else None,
                        longitude=parse_float(obs_raw.get("LON", "")) if obs_raw.get("LON") else None,
                        timestamp=ts,
                        wind_direction=parse_float(obs_raw.get("WDIR", "")),
                        wind_speed=parse_float(obs_raw.get("WSPD", "")),
                        gust=parse_float(obs_raw.get("GST", "")),
                        wave_height=parse_float(obs_raw.get("WVHT", "")),
                        dominant_wave_period=parse_float(obs_raw.get("DPD", "")),
                        average_wave_period=parse_float(obs_raw.get("APD", "")),
                        mean_wave_direction=parse_float(obs_raw.get("MWD", "")),
                        pressure=parse_float(obs_raw.get("PRES", "")),
                        air_temperature=parse_float(obs_raw.get("ATMP", "")),
                        water_temperature=parse_float(obs_raw.get("WTMP", "")),
                        dewpoint=parse_float(obs_raw.get("DEWP", "")),
                        pressure_tendency=parse_float(obs_raw.get("PTDY", "")),
                        visibility=parse_float(obs_raw.get("VIS", "")),
                        tide=parse_float(obs_raw.get("TIDE", "")),
                        region=region,
                    )
                    producer.send_buoy_observation(data=obs, _station_id=sid, _region=region)
                    state.setdefault("seen", {})[obs_key] = "1"
                    count += 1
                # Trim state
                seen = state.get("seen", {})
                if len(seen) > 50000:
                    state["seen"] = dict(list(seen.items())[-25000:])
                if state_file:
                    try:
                        with open(state_file, 'w') as f:
                            json.dump(state, f)
                    except Exception:
                        pass
                logger.info("Published %d buoy observations", count)
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
    parser = argparse.ArgumentParser(description='NOAA NDBC AMQP 1.0 bridge')
    sub = parser.add_subparsers(dest='command')
    fp = sub.add_parser('feed', help='Feed events as CloudEvents over AMQP')
    fp.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL'))
    fp.add_argument('--host', default=os.getenv('AMQP_HOST', 'localhost'))
    fp.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT', '0')) or None)
    fp.add_argument('--address', default=os.getenv('AMQP_ADDRESS', 'noaa-ndbc'))
    fp.add_argument('--tls', action='store_true', default=os.getenv('AMQP_TLS', '').lower() in ('1', 'true', 'yes'))
    fp.add_argument('--username', default=os.getenv('AMQP_USERNAME'))
    fp.add_argument('--password', default=os.getenv('AMQP_PASSWORD'))
    fp.add_argument('--content-mode', default=os.getenv('AMQP_CONTENT_MODE', 'binary'), choices=['binary', 'structured'])
    fp.add_argument('--auth-mode', default=os.getenv('AMQP_AUTH_MODE', 'password'), choices=['password', 'entra', 'sas'])
    fp.add_argument('--entra-audience', default=os.getenv('AMQP_ENTRA_AUDIENCE', DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    fp.add_argument('--entra-client-id', default=os.getenv('AMQP_ENTRA_CLIENT_ID'))
    fp.add_argument('--sas-key-name', default=os.getenv('AMQP_SAS_KEY_NAME'))
    fp.add_argument('--sas-key', default=os.getenv('AMQP_SAS_KEY'))
    fp.add_argument('-i', '--polling-interval', type=int, default=int(os.getenv('POLLING_INTERVAL', '600')))
    fp.add_argument('--state-file', default=os.getenv('STATE_FILE', os.path.expanduser('~/.noaa_ndbc_amqp_state.json')))
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
