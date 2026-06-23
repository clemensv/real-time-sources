"""USGS NWIS Water Quality -> AMQP 1.0 bridge.

Polls the USGS Water Services API for water quality data and publishes them as CloudEvents over AMQP 1.0.
"""

import argparse
import logging
import os
import sys
import time
import json
import requests
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, List, Any
from urllib.parse import urlparse

from usgs_nwis_wq_amqp_producer_data import MonitoringSite, WaterQualityReading
from usgs_nwis_wq_amqp_producer_amqp_producer.producer import (
    USGSWaterQualitySitesAmqpProducer,
    USGSWaterQualityReadingsAmqpProducer,
)

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
BASE_URL = "https://waterservices.usgs.gov/nwis/iv/"
DEFAULT_STATES = ["CA", "TX", "FL", "NY", "CO"]
DEFAULT_PARAM_CODES = "00010,00060,00065,00095,00300,00400"
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


def _build_sites_producer(host, port, address, tls, content_mode, auth_mode, username, password,
                          entra_audience, entra_client_id, sas_key_name, sas_key):
    if auth_mode == 'entra':
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        cred = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return USGSWaterQualitySitesAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            credential=cred, entra_audience=entra_audience, use_tls=tls)
    if auth_mode == 'sas':
        return USGSWaterQualitySitesAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            sas_key_name=sas_key_name, sas_key=sas_key, use_tls=tls)
    return USGSWaterQualitySitesAmqpProducer(
        host=host, address=address, port=port, username=username, password=password,
        content_mode=content_mode, use_tls=tls)


def _build_readings_producer(host, port, address, tls, content_mode, auth_mode, username, password,
                             entra_audience, entra_client_id, sas_key_name, sas_key):
    if auth_mode == 'entra':
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        cred = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return USGSWaterQualityReadingsAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            credential=cred, entra_audience=entra_audience, use_tls=tls)
    if auth_mode == 'sas':
        return USGSWaterQualityReadingsAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            sas_key_name=sas_key_name, sas_key=sas_key, use_tls=tls)
    return USGSWaterQualityReadingsAmqpProducer(
        host=host, address=address, port=port, username=username, password=password,
        content_mode=content_mode, use_tls=tls)


def _fetch_waterml(state_code: str, param_codes: str) -> Optional[Dict]:
    """Fetch WaterML JSON from USGS for a given state."""
    params = {
        "format": "json",
        "stateCd": state_code,
        "parameterCd": param_codes,
        "siteStatus": "active",
        "period": "PT2H",
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=120)
        if resp.status_code == 200:
            return resp.json()
    except Exception as exc:
        logger.warning("Failed to fetch data for state %s: %s", state_code, exc)
    return None


def _parse_waterml(data: Dict) -> tuple:
    """Parse WaterML JSON into sites and readings."""
    sites: List[Dict] = []
    readings: List[Dict] = []
    ts_list = data.get("value", {}).get("timeSeries", [])
    seen_sites = set()
    for ts in ts_list:
        source_info = ts.get("sourceInfo", {})
        site_code = source_info.get("siteCode", [{}])[0].get("value", "")
        site_name = source_info.get("siteName", "")
        geo = source_info.get("geoLocation", {}).get("geogLocation", {})
        variable = ts.get("variable", {})
        param_code = variable.get("variableCode", [{}])[0].get("value", "")
        param_name = variable.get("variableName", "")
        unit = variable.get("unit", {}).get("unitCode", "")

        if site_code and site_code not in seen_sites:
            seen_sites.add(site_code)
            sites.append({
                "site_number": site_code,
                "site_name": site_name,
                "latitude": geo.get("latitude"),
                "longitude": geo.get("longitude"),
                "site_type": source_info.get("siteProperty", [{}])[0].get("value", ""),
                "parameter_code": param_code,
            })

        values = ts.get("values", [{}])[0].get("value", [])
        for v in values[-5:]:  # Only last 5 readings per time series
            readings.append({
                "site_number": site_code,
                "site_name": site_name,
                "parameter_code": param_code,
                "parameter_name": param_name,
                "value": v.get("value"),
                "unit": unit,
                "qualifier": ",".join(v.get("qualifiers", [])),
                "date_time": v.get("dateTime", ""),
            })
    return sites, readings


def feed(host, port, address='usgs-nwis-wq', username=None, password=None, tls=False,
         content_mode='binary', auth_mode='password', entra_audience=DEFAULT_ENTRA_AUDIENCE_SERVICEBUS,
         entra_client_id=None, sas_key_name=None, sas_key=None, once=False,
         polling_interval=600, state_file='', states=None, param_codes=None):
    """Poll USGS NWIS API and emit monitoring site + water quality reading events via AMQP."""
    site_producer = _retry_producer_init(lambda: _build_sites_producer(
        host, port, address, tls, content_mode, auth_mode, username, password,
        entra_audience, entra_client_id, sas_key_name, sas_key))
    readings_producer = _retry_producer_init(lambda: _build_readings_producer(
        host, port, address, tls, content_mode, auth_mode, username, password,
        entra_audience, entra_client_id, sas_key_name, sas_key))

    poll_states = states or DEFAULT_STATES
    poll_params = param_codes or DEFAULT_PARAM_CODES
    previous = {}
    if state_file and os.path.exists(state_file):
        try:
            with open(state_file, 'r') as f:
                previous = json.load(f)
        except Exception:
            pass

    try:
        while True:
            total_sites = 0
            total_readings = 0
            for state_code in poll_states:
                try:
                    data = _fetch_waterml(state_code, poll_params)
                    if not data:
                        continue
                    sites, readings = _parse_waterml(data)
                    # Emit sites
                    for s in sites:
                        site = MonitoringSite(
                            site_number=s["site_number"],
                            site_name=s.get("site_name", ""),
                            agency_code="USGS",
                            latitude=s.get("latitude"),
                            longitude=s.get("longitude"),
                            site_type=s.get("site_type", ""),
                            state_code=state_code,
                            county_code=None,
                            huc_code=None,
                            state=state_code,
                            parameter_code=s.get("parameter_code", ""),
                        )
                        site_producer.send_monitoring_site(
                            data=site, _source_uri=BASE_URL,
                            _site_number=s["site_number"], _state=state_code)
                        total_sites += 1
                    # Emit readings
                    for r in readings:
                        obs_key = f"{r['site_number']}:{r['parameter_code']}:{r['date_time']}"
                        if obs_key in previous:
                            continue
                        reading = WaterQualityReading(
                            site_number=r["site_number"],
                            site_name=r.get("site_name", ""),
                            parameter_code=r["parameter_code"],
                            parameter_name=r.get("parameter_name", ""),
                            value=r.get("value"),
                            unit=r.get("unit", ""),
                            qualifier=r.get("qualifier", ""),
                            date_time=r.get("date_time", ""),
                            state=state_code,
                        )
                        readings_producer.send_water_quality_reading(
                            data=reading, _source_uri=BASE_URL,
                            _site_number=r["site_number"],
                            _parameter_code=r["parameter_code"],
                            _state=state_code)
                        previous[obs_key] = "1"
                        total_readings += 1
                except Exception as exc:
                    logger.warning("Error polling state %s: %s", state_code, exc)
            if len(previous) > 100000:
                previous = dict(list(previous.items())[-50000:])
            if state_file:
                try:
                    with open(state_file, 'w') as f:
                        json.dump(previous, f)
                except Exception:
                    pass
            logger.info("Published %d sites, %d readings", total_sites, total_readings)
            if once:
                break
            time.sleep(polling_interval)
    finally:
        for p in (site_producer, readings_producer):
            try:
                p.close()
            except Exception:
                pass


def _parse_broker_url(url):
    parsed = urlparse(url if '://' in url else f'amqp://{url}')
    tls = (parsed.scheme or 'amqp').lower() in ('amqps', 'ssl', 'tls')
    return parsed.hostname or 'localhost', parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or '').lstrip('/') or None


def main(argv=None):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    parser = argparse.ArgumentParser(description='USGS NWIS Water Quality AMQP 1.0 bridge')
    sub = parser.add_subparsers(dest='command')
    fp = sub.add_parser('feed', help='Feed events as CloudEvents over AMQP')
    fp.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL'))
    fp.add_argument('--host', default=os.getenv('AMQP_HOST', 'localhost'))
    fp.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT', '0')) or None)
    fp.add_argument('--address', default=os.getenv('AMQP_ADDRESS', 'usgs-nwis-wq'))
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
    fp.add_argument('--state-file', default=os.getenv('STATE_FILE', os.path.expanduser('~/.usgs_nwis_wq_amqp_state.json')))
    fp.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE', '').lower() in ('1', 'true', 'yes'))
    fp.add_argument('--states', default=os.getenv('USGS_WQ_STATES', ''))
    fp.add_argument('--param-codes', default=os.getenv('USGS_WQ_PARAMETER_CODES', ''))
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

    states_list = [s.strip() for s in args.states.split(",") if s.strip()] if args.states else None
    param_codes = args.param_codes if args.param_codes else None

    feed(host, port, address=address, username=username, password=password, tls=tls,
         content_mode=args.content_mode, auth_mode=args.auth_mode,
         entra_audience=args.entra_audience, entra_client_id=args.entra_client_id,
         sas_key_name=args.sas_key_name, sas_key=args.sas_key,
         once=args.once, polling_interval=args.polling_interval, state_file=args.state_file,
         states=states_list, param_codes=param_codes)


if __name__ == '__main__':
    main()
