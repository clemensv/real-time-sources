"""Hub'Eau Hydrométrie → AMQP 1.0 bridge.

Polls the Hub'Eau Hydrométrie REST API for station reference data and
water level observations, publishing them as CloudEvents over AMQP 1.0.
"""

import argparse
import dataclasses
import inspect
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

from hubeau_hydrometrie.hubeau_hydrometrie import HubEauHydrometrieAPI, _load_state, _save_state
from hubeau_hydrometrie_amqp_producer_data import Station, Observation
from hubeau_hydrometrie_amqp_producer_amqp_producer.producer import FRGovEaufranceHubEauHydrometrieAmqpProducer

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
        return FRGovEaufranceHubEauHydrometrieAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            credential=cred, entra_audience=entra_audience, use_tls=tls)
    if auth_mode == 'sas':
        return FRGovEaufranceHubEauHydrometrieAmqpProducer(
            host=host, address=address, port=port, content_mode=content_mode,
            sas_key_name=sas_key_name, sas_key=sas_key, use_tls=tls)
    return FRGovEaufranceHubEauHydrometrieAmqpProducer(
        host=host, address=address, port=port, username=username, password=password,
        content_mode=content_mode, use_tls=tls)


def _basin_slug(station_data):
    """Extract basin/river name for the _basin key parameter."""
    raw = getattr(station_data, 'libelle_cours_eau', None) or getattr(station_data, 'basin', None) or 'unknown'
    return str(raw).strip() or 'unknown'


def feed(host, port, address='hubeau-hydrometrie', username=None, password=None, tls=False,
         content_mode='binary', auth_mode='password', entra_audience=DEFAULT_ENTRA_AUDIENCE_SERVICEBUS,
         entra_client_id=None, sas_key_name=None, sas_key=None, once=False,
         polling_interval=300, state_file=''):
    """Poll Hub'Eau API and emit station + observation events via AMQP."""
    producer = _retry_producer_init(lambda: _build_producer(
        host, port, address, tls, content_mode, auth_mode, username, password,
        entra_audience, entra_client_id, sas_key_name, sas_key))

    api = HubEauHydrometrieAPI()
    previous_observations = _load_state(state_file)
    station_basins = {}

    # Emit reference data (stations)
    try:
        stations = api.list_stations()
        logger.info("Publishing %d station info events", len(stations))
        for s in stations:
            code = s.get("code_station", "")
            basin = s.get("libelle_cours_eau", "") or s.get("libelle_bassin", "") or "unknown"
            station_basins[code] = basin
            data = Station(
                code_station=code,
                libelle_station=s.get("libelle_station", ""),
                code_site=str(s.get("code_site") or "") or None,
                longitude_station=s.get("longitude_station", 0.0) or 0.0,
                latitude_station=s.get("latitude_station", 0.0) or 0.0,
                libelle_cours_eau=s.get("libelle_cours_eau", "") or "",
                libelle_commune=s.get("libelle_commune", "") or "",
                code_departement=str(s.get("code_departement") or "") or None,
                en_service=s.get("en_service", False) or False,
                date_ouverture_station=s.get("date_ouverture_station", "") or "",
                basin=s.get("libelle_bassin", None),
            )
            producer.send_station(data=data, _code_station=code, _basin=basin)
        logger.info("Finished publishing station catalog")
    except Exception as exc:
        logger.error("Failed to fetch/emit stations: %s", exc)

    # Polling loop
    try:
        while True:
            try:
                start_time = time.time()
                observations = api.get_latest_observations()
                count = 0
                for obs in observations:
                    code = obs.get("code_station", "")
                    date_obs = obs.get("date_obs", "")
                    obs_key = f"{code}:{date_obs}"
                    if obs_key in previous_observations:
                        continue
                    basin = station_basins.get(code, "unknown")
                    data = Observation(
                        code_station=code,
                        date_obs=date_obs,
                        resultat_obs=obs.get("resultat_obs"),
                        grandeur_hydro=obs.get("grandeur_hydro", ""),
                        libelle_methode_obs=obs.get("libelle_methode_obs"),
                        libelle_qualification_obs=obs.get("libelle_qualification_obs"),
                        basin=basin if basin != "unknown" else None,
                    )
                    producer.send_observation(data=data, _code_station=code, _basin=basin)
                    previous_observations[obs_key] = date_obs
                    count += 1

                elapsed = time.time() - start_time
                logger.info("Published %d observations in %.1fs", count, elapsed)
                _save_state(state_file, previous_observations)
            except KeyboardInterrupt:
                break
            except Exception as exc:
                logger.error("Error in polling loop: %s", exc)

            if once:
                logger.info("--once mode: exiting after first cycle")
                break
            effective = max(1, polling_interval - (time.time() - start_time))
            time.sleep(effective)
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
    parser = argparse.ArgumentParser(description='Hub\'Eau Hydrométrie → AMQP 1.0 bridge')
    sub = parser.add_subparsers(dest='command')
    fp = sub.add_parser('feed', help='Feed stations and observations as CloudEvents over AMQP')
    fp.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL'))
    fp.add_argument('--host', default=os.getenv('AMQP_HOST', 'localhost'))
    fp.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT', '0')) or None)
    fp.add_argument('--address', default=os.getenv('AMQP_ADDRESS', 'hubeau-hydrometrie'))
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
    fp.add_argument('--state-file', default=os.getenv('STATE_FILE', os.path.expanduser('~/.hubeau_hydrometrie_amqp_state.json')))
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