"""
Tokyo Docomo Bikeshare GBFS 2.3 poller.

Polls the GBFS autodiscovery endpoint for the Tokyo Docomo Bikeshare system
(docomo-cycle-tokyo) and emits three event families:
  - BikeshareSystem (reference data, from system_information.json)
  - BikeshareStation (reference data, from station_information.json)
  - BikeshareStationStatus (telemetry, from station_status.json)
"""

# pylint: disable=line-too-long

import os
import sys
import json
import time
import argparse
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from tokyo_docomo_bikeshare_producer_data import BikeshareSystem, BikeshareStation, BikeshareStationStatus
from tokyo_docomo_bikeshare_producer_kafka_producer.producer import (
    JPODPTDocomoBikeshareSystemEventProducer,
    JPODPTDocomoBikeshareStationsEventProducer,
)

GBFS_AUTODISCOVERY_URL = "https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/gbfs.json"
SYSTEM_ID = "docomo-cycle-tokyo"

# Re-fetch reference data every hour
REFERENCE_REFRESH_INTERVAL_SECONDS = 3600

# Fallback poll interval if TTL cannot be parsed from the GBFS feed
DEFAULT_POLL_INTERVAL_SECONDS = 60


def _make_session() -> requests.Session:
    """Create a requests Session with bounded retry handling for transient failures."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse an Azure Event Hubs or plain Kafka connection string.

    Supports both the Azure Event Hubs format
    (``Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=...``)
    and the simpler plain format
    (``BootstrapServer=host:port;EntityPath=topic``).

    Args:
        connection_string: The connection string to parse.

    Returns:
        Dict containing bootstrap.servers, kafka_topic, and optionally
        sasl.username and sasl.password.
    """
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = (
                    part.split('=', 1)[1].strip('"')
                    .replace('sb://', '')
                    .replace('/', '')
                    + ':9093'
                )
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=', 1)[1].strip('"')
            elif 'SharedAccessKeyName' in part:
                config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part:
                config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc
    if 'sasl.username' in config_dict:
        config_dict['security.protocol'] = 'SASL_SSL'
        config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict


class DocomoBikesharePoller:
    """
    Polls the Tokyo Docomo Bikeshare GBFS 2.3 feeds and emits CloudEvents
    to Kafka for system information, station information, and station status.
    """

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str) -> None:
        """
        Initialize the poller with Kafka configuration.

        Args:
            kafka_config: Confluent Kafka producer configuration dict.
            kafka_topic: Kafka topic to produce messages to.
        """
        from confluent_kafka import Producer
        self.kafka_topic = kafka_topic
        self._session = _make_session()

        kafka_producer = Producer(kafka_config)
        self.system_producer = JPODPTDocomoBikeshareSystemEventProducer(kafka_producer, kafka_topic)
        self.stations_producer = JPODPTDocomoBikeshareStationsEventProducer(kafka_producer, kafka_topic)

        # Reference data cache: replaced atomically on successful refresh
        self._cached_stations: Optional[List[Dict]] = None
        self._last_reference_emit: float = 0.0

        # Telemetry dedupe: station_id → last_reported value
        self._last_status: Dict[str, Optional[int]] = {}

    # ------------------------------------------------------------------
    # GBFS autodiscovery
    # ------------------------------------------------------------------

    def _fetch_feed_urls(self) -> Dict[str, str]:
        """
        Fetch the GBFS autodiscovery manifest and return a map of
        feed_name → URL.

        Returns:
            Dict mapping feed names (e.g. 'station_status') to their URLs.
        """
        try:
            resp = self._session.get(GBFS_AUTODISCOVERY_URL, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            feeds = (
                data.get('data', {})
                .get('en', data.get('data', {}).get('ja', {}))
                .get('feeds', [])
            )
            return {f['name']: f['url'] for f in feeds if 'name' in f and 'url' in f}
        except Exception as exc:
            print(f"Warning: could not fetch GBFS autodiscovery: {exc}", flush=True)
            # Fall back to well-known paths
            base = "https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo"
            return {
                'system_information': f"{base}/system_information.json",
                'station_information': f"{base}/station_information.json",
                'station_status': f"{base}/station_status.json",
            }

    # ------------------------------------------------------------------
    # Reference data: system_information
    # ------------------------------------------------------------------

    def _fetch_system_information(self, url: str) -> Optional[Dict]:
        """
        Fetch system_information.json and return the parsed data dict.

        Args:
            url: URL for system_information.json.

        Returns:
            Parsed system information dict, or None on failure.
        """
        try:
            resp = self._session.get(url, timeout=30)
            resp.raise_for_status()
            payload = resp.json()
            return payload.get('data', payload)
        except Exception as exc:
            print(f"Warning: could not fetch system_information: {exc}", flush=True)
            return None

    def _emit_system(self, info: Dict) -> None:
        """
        Emit a BikeshareSystem CloudEvent from the system_information payload.

        Args:
            info: Parsed system_information.json data dict.
        """
        system = BikeshareSystem(
            system_id=info.get('system_id', SYSTEM_ID),
            language=info.get('language', 'ja'),
            name=info.get('name', ''),
            short_name=info.get('short_name'),
            operator=info.get('operator'),
            url=info.get('url'),
            purchase_url=info.get('purchase_url'),
            start_date=info.get('start_date'),
            phone_number=info.get('phone_number'),
            email=info.get('email'),
            feed_contact_email=info.get('feed_contact_email'),
            timezone=info.get('timezone', 'Asia/Tokyo'),
            license_url=info.get('license_url'),
        )
        self.system_producer.send_jp_odpt_docomo_bikeshare_bikeshare_system(
            system.system_id, system, flush_producer=False
        )

    # ------------------------------------------------------------------
    # Reference data: station_information
    # ------------------------------------------------------------------

    def _fetch_station_information(self, url: str) -> Optional[List[Dict]]:
        """
        Fetch station_information.json and return the list of station dicts.

        Args:
            url: URL for station_information.json.

        Returns:
            List of station dicts, or None on failure.
        """
        try:
            resp = self._session.get(url, timeout=30)
            resp.raise_for_status()
            payload = resp.json()
            stations = payload.get('data', {}).get('stations', [])
            return stations
        except Exception as exc:
            print(f"Warning: could not fetch station_information: {exc}", flush=True)
            return None

    def _emit_stations(self, stations: List[Dict]) -> None:
        """
        Emit BikeshareStation CloudEvents for all stations.

        Args:
            stations: List of station dicts from station_information.json.
        """
        for s in stations:
            station_id = s.get('station_id', '')
            if not station_id:
                continue
            station = BikeshareStation(
                system_id=SYSTEM_ID,
                station_id=station_id,
                name=s.get('name', ''),
                short_name=s.get('short_name'),
                lat=float(s.get('lat', 0.0)),
                lon=float(s.get('lon', 0.0)),
                address=s.get('address'),
                cross_street=s.get('cross_street'),
                region_id=s.get('region_id'),
                post_code=s.get('post_code'),
                capacity=s.get('capacity'),
                is_virtual_station=s.get('is_virtual_station'),
            )
            self.stations_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station(
                SYSTEM_ID, station_id, station, flush_producer=False
            )

    # ------------------------------------------------------------------
    # Telemetry: station_status
    # ------------------------------------------------------------------

    def _fetch_station_status(self, url: str) -> Tuple[Optional[List[Dict]], int]:
        """
        Fetch station_status.json and return (list of status dicts, ttl seconds).

        Args:
            url: URL for station_status.json.

        Returns:
            Tuple of (status list or None, TTL in seconds).
        """
        try:
            resp = self._session.get(url, timeout=30)
            resp.raise_for_status()
            payload = resp.json()
            statuses = payload.get('data', {}).get('stations', [])
            ttl = int(payload.get('ttl', DEFAULT_POLL_INTERVAL_SECONDS))
            return statuses, ttl
        except Exception as exc:
            print(f"Warning: could not fetch station_status: {exc}", flush=True)
            return None, DEFAULT_POLL_INTERVAL_SECONDS

    def _emit_station_statuses(self, statuses: List[Dict]) -> int:
        """
        Emit BikeshareStationStatus CloudEvents for stations with new data.

        Only emits records where last_reported has changed since the last
        successful flush.  Returns the count of new events staged for sending.

        Args:
            statuses: List of station status dicts from station_status.json.

        Returns:
            Count of new status events staged.
        """
        pending_state: Dict[str, Optional[int]] = {}
        count = 0
        for s in statuses:
            station_id = s.get('station_id', '')
            if not station_id:
                continue
            last_reported = s.get('last_reported')
            # Dedupe: skip if last_reported hasn't changed
            if self._last_status.get(station_id) == last_reported:
                continue
            status = BikeshareStationStatus(
                system_id=SYSTEM_ID,
                station_id=station_id,
                num_bikes_available=int(s.get('num_bikes_available', 0)),
                num_bikes_disabled=s.get('num_bikes_disabled'),
                num_docks_available=s.get('num_docks_available'),
                num_docks_disabled=s.get('num_docks_disabled'),
                is_installed=bool(s.get('is_installed', False)),
                is_renting=bool(s.get('is_renting', False)),
                is_returning=bool(s.get('is_returning', False)),
                last_reported=last_reported,
            )
            self.stations_producer.send_jp_odpt_docomo_bikeshare_bikeshare_station_status(
                SYSTEM_ID, station_id, status, flush_producer=False
            )
            pending_state[station_id] = last_reported
            count += 1
        # Dedupe state is committed in the caller only after flush succeeds
        return count, pending_state

    # ------------------------------------------------------------------
    # Main poll loop
    # ------------------------------------------------------------------

    def poll_and_send(self, once: bool = False) -> None:
        """
        Run the poll loop: emit reference data at startup then telemetry on TTL.

        Args:
            once: If True, run only one cycle then return (used in tests).
        """
        feed_urls = self._fetch_feed_urls()
        system_info_url = feed_urls.get(
            'system_information',
            f"https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/system_information.json"
        )
        station_info_url = feed_urls.get(
            'station_information',
            f"https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/station_information.json"
        )
        station_status_url = feed_urls.get(
            'station_status',
            f"https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/station_status.json"
        )

        poll_interval = DEFAULT_POLL_INTERVAL_SECONDS

        while True:
            try:
                now = time.monotonic()
                need_reference_refresh = (
                    now - self._last_reference_emit >= REFERENCE_REFRESH_INTERVAL_SECONDS
                )

                new_count = 0
                pending_status_state: Dict[str, Optional[int]] = {}

                # --- Reference data ---
                if need_reference_refresh:
                    # System information
                    sys_info = self._fetch_system_information(system_info_url)
                    if sys_info is not None:
                        self._emit_system(sys_info)
                        new_count += 1

                    # Station information — build snapshot, swap in only on success
                    new_stations = self._fetch_station_information(station_info_url)
                    if new_stations is not None:
                        self._cached_stations = new_stations
                        self._emit_stations(self._cached_stations)
                        new_count += len(self._cached_stations)
                    elif self._cached_stations is not None:
                        # Refresh failed: keep using old cache (already emitted, skip re-emit)
                        print("Warning: station_information refresh failed; continuing with cached data", flush=True)

                # --- Telemetry ---
                statuses, ttl = self._fetch_station_status(station_status_url)
                poll_interval = max(10, ttl)

                if statuses is not None:
                    status_count, pending_status_state = self._emit_station_statuses(statuses)
                    new_count += status_count

                # --- Flush and advance state ---
                if new_count > 0:
                    remainder = self.system_producer.producer.flush(timeout=30)
                    if remainder > 0:
                        print(
                            f"Warning: Kafka flush incomplete ({remainder} message(s) undelivered); "
                            "dedupe state not advanced",
                            flush=True,
                        )
                    else:
                        # Commit reference-emit timestamp and telemetry dedupe state
                        if need_reference_refresh:
                            self._last_reference_emit = now
                        self._last_status.update(pending_status_state)
                        print(f"Sent {new_count} new event(s) to Kafka", flush=True)
                else:
                    if need_reference_refresh:
                        self._last_reference_emit = now

            except Exception as exc:  # pylint: disable=broad-except
                print(f"Error in poll cycle: {exc}", flush=True)

            if once:
                break

            time.sleep(poll_interval)


def main() -> None:
    """Entry point: parse CLI args / env vars and start the poll loop."""
    parser = argparse.ArgumentParser(description="Tokyo Docomo Bikeshare GBFS poller")
    parser.add_argument(
        '--kafka-bootstrap-servers', type=str,
        help="Comma-separated list of Kafka bootstrap servers"
    )
    parser.add_argument('--kafka-topic', type=str, help="Kafka topic to send messages to")
    parser.add_argument('--sasl-username', type=str, help="Username for SASL PLAIN authentication")
    parser.add_argument('--sasl-password', type=str, help="Password for SASL PLAIN authentication")
    parser.add_argument(
        '--connection-string', type=str,
        help="Azure Event Hubs or plain Kafka connection string"
    )
    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')

    if args.connection_string:
        cfg = parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = cfg.get('bootstrap.servers')
        kafka_topic = cfg.get('kafka_topic')
        sasl_username = cfg.get('sasl.username')
        sasl_password = cfg.get('sasl.password')
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided.", flush=True)
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided.", flush=True)
        sys.exit(1)

    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')

    kafka_config: Dict[str, str] = {'bootstrap.servers': kafka_bootstrap_servers}
    if sasl_username and sasl_password:
        kafka_config.update({
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password,
        })
    elif tls_enabled:
        kafka_config['security.protocol'] = 'SSL'

    poller = DocomoBikesharePoller(kafka_config=kafka_config, kafka_topic=kafka_topic)
    poller.poll_and_send()


if __name__ == '__main__':
    main()
