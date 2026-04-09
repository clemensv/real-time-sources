"""
AviationWeather.gov Bridge
Polls the AviationWeather.gov API for METAR observations, SIGMET advisories,
and station reference data, then sends them to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timezone
import argparse
import requests
from aviationweather_producer_data import Metar, Sigmet, Station
from aviationweather_producer_kafka_producer.producer import GovNoaaAviationweatherEventProducer


API_BASE = "https://aviationweather.gov/api/data"
DEFAULT_STATIONS = "KJFK,KLAX,KORD,KATL,EGLL,LFPG,EDDF,RJTT,YSSY,ZBAA"
METAR_POLL_INTERVAL = 60
SIGMET_POLL_INTERVAL = 120
STATION_REFRESH_HOURS = 24


class AviationWeatherPoller:
    """
    Polls AviationWeather.gov API for METAR observations, SIGMETs, and
    station reference data, sending them to Kafka as CloudEvents.
    """

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str,
                 last_polled_file: str, station_ids: str = DEFAULT_STATIONS,
                 metar_poll_interval: int = METAR_POLL_INTERVAL,
                 sigmet_poll_interval: int = SIGMET_POLL_INTERVAL):
        """
        Initialize the AviationWeatherPoller.

        Args:
            kafka_config: Kafka configuration settings.
            kafka_topic: Kafka topic to send messages to.
            last_polled_file: File to store last seen timestamps for deduplication.
            station_ids: Comma-separated list of ICAO station IDs to monitor.
            metar_poll_interval: Seconds between METAR polls.
            sigmet_poll_interval: Seconds between SIGMET polls.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        self.station_ids = station_ids
        self.metar_poll_interval = metar_poll_interval
        self.sigmet_poll_interval = sigmet_poll_interval
        from confluent_kafka import Producer as KafkaProducer
        kafka_producer = KafkaProducer(kafka_config)
        self.producer = GovNoaaAviationweatherEventProducer(kafka_producer, kafka_topic)

    @staticmethod
    def epoch_to_iso(epoch_val) -> Optional[str]:
        """
        Convert a Unix epoch timestamp (int or float) to an ISO 8601 UTC string.

        Args:
            epoch_val: Unix timestamp in seconds.

        Returns:
            ISO 8601 UTC datetime string, or None on failure.
        """
        if epoch_val is None:
            return None
        try:
            dt = datetime.fromtimestamp(int(epoch_val), tz=timezone.utc)
            return dt.isoformat()
        except (ValueError, TypeError, OSError):
            return None

    @staticmethod
    def safe_int(value) -> Optional[int]:
        """Safely convert a value to int, returning None on failure."""
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def safe_float(value) -> Optional[float]:
        """Safely convert a value to float, returning None on failure."""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def fetch_metar_json(station_ids: str) -> List[dict]:
        """
        Fetch METAR observations from the AviationWeather.gov API.

        Args:
            station_ids: Comma-separated ICAO station identifiers.

        Returns:
            List of METAR dictionaries from the API.
        """
        try:
            url = f"{API_BASE}/metar?ids={station_ids}&format=json"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                return data
            return []
        except Exception as err:
            print(f"Error fetching METARs: {err}")
            return []

    @staticmethod
    def fetch_station_json(station_ids: str) -> List[dict]:
        """
        Fetch station metadata from the AviationWeather.gov API.

        Args:
            station_ids: Comma-separated ICAO station identifiers.

        Returns:
            List of station info dictionaries from the API.
        """
        try:
            url = f"{API_BASE}/stationinfo?ids={station_ids}&format=json"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                return data
            return []
        except Exception as err:
            print(f"Error fetching station info: {err}")
            return []

    @staticmethod
    def fetch_airsigmet_json() -> List[dict]:
        """
        Fetch US domestic SIGMETs (AIRMETs/SIGMETs) from the API.

        Returns:
            List of SIGMET dictionaries.
        """
        try:
            url = f"{API_BASE}/airsigmet?format=json"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                return data
            return []
        except Exception as err:
            print(f"Error fetching US SIGMETs: {err}")
            return []

    @staticmethod
    def fetch_isigmet_json() -> List[dict]:
        """
        Fetch international SIGMETs from the API.

        Returns:
            List of international SIGMET dictionaries.
        """
        try:
            url = f"{API_BASE}/isigmet?format=json"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                return data
            return []
        except Exception as err:
            print(f"Error fetching international SIGMETs: {err}")
            return []

    @classmethod
    def parse_station(cls, raw: dict) -> Optional[Station]:
        """
        Parse a station info API response dict into a Station dataclass.

        Args:
            raw: Station info dictionary from the API.

        Returns:
            Station dataclass or None if required fields are missing.
        """
        icao_id = raw.get("icaoId")
        if not icao_id:
            return None
        name = raw.get("site") or raw.get("name") or icao_id
        lat = cls.safe_float(raw.get("lat"))
        lon = cls.safe_float(raw.get("lon"))
        if lat is None or lon is None:
            return None
        site_type_list = raw.get("siteType")
        site_type = ",".join(site_type_list) if isinstance(site_type_list, list) else None
        return Station(
            icao_id=icao_id,
            iata_id=raw.get("iataId"),
            faa_id=raw.get("faaId"),
            wmo_id=raw.get("wmoId"),
            name=name,
            latitude=lat,
            longitude=lon,
            elevation=cls.safe_float(raw.get("elev")),
            state=raw.get("state"),
            country=raw.get("country"),
            site_type=site_type,
        )

    @classmethod
    def parse_metar(cls, raw: dict) -> Optional[Metar]:
        """
        Parse a METAR API response dict into a Metar dataclass.

        Args:
            raw: METAR dictionary from the API.

        Returns:
            Metar dataclass or None if required fields are missing.
        """
        icao_id = raw.get("icaoId")
        if not icao_id:
            return None
        raw_ob = raw.get("rawOb")
        if not raw_ob:
            return None

        obs_time_epoch = raw.get("obsTime")
        obs_time = cls.epoch_to_iso(obs_time_epoch)
        if not obs_time:
            return None

        report_time = raw.get("reportTime")
        if isinstance(report_time, str):
            try:
                datetime.fromisoformat(report_time.replace("Z", "+00:00"))
            except ValueError:
                report_time = None

        clouds_raw = raw.get("clouds")
        clouds_str = json.dumps(clouds_raw) if clouds_raw is not None else None

        visib = raw.get("visib")
        visib_str = str(visib) if visib is not None else None

        return Metar(
            icao_id=icao_id,
            obs_time=obs_time,
            report_time=report_time,
            temp=cls.safe_float(raw.get("temp")),
            dewp=cls.safe_float(raw.get("dewp")),
            wdir=cls.safe_int(raw.get("wdir")),
            wspd=cls.safe_int(raw.get("wspd")),
            wgst=cls.safe_int(raw.get("wgst")),
            visib=visib_str,
            altim=cls.safe_float(raw.get("altim")),
            slp=cls.safe_float(raw.get("slp")),
            qc_field=cls.safe_int(raw.get("qcField")),
            wx_string=raw.get("wxString"),
            metar_type=raw.get("metarType"),
            raw_ob=raw_ob,
            latitude=cls.safe_float(raw.get("lat")),
            longitude=cls.safe_float(raw.get("lon")),
            elevation=cls.safe_float(raw.get("elev")),
            flt_cat=raw.get("fltCat"),
            clouds=clouds_str,
            name=raw.get("name"),
        )

    @classmethod
    def parse_us_sigmet(cls, raw: dict) -> Optional[Sigmet]:
        """
        Parse a US domestic SIGMET API response dict into a Sigmet dataclass.

        Args:
            raw: US SIGMET dictionary from the API.

        Returns:
            Sigmet dataclass or None if required fields are missing.
        """
        icao_id = raw.get("icaoId")
        series_id = raw.get("seriesId")
        if not icao_id or not series_id:
            return None

        valid_from = cls.epoch_to_iso(raw.get("validTimeFrom"))
        valid_to = cls.epoch_to_iso(raw.get("validTimeTo"))
        if not valid_from or not valid_to:
            return None

        coords_raw = raw.get("coords")
        coords_str = json.dumps(coords_raw) if coords_raw is not None else None

        movement_dir = raw.get("movementDir")
        movement_spd = raw.get("movementSpd")

        return Sigmet(
            icao_id=icao_id,
            series_id=series_id,
            valid_time_from=valid_from,
            valid_time_to=valid_to,
            hazard=raw.get("hazard"),
            qualifier=None,
            sigmet_type=raw.get("airSigmetType", "SIGMET"),
            altitude_hi=cls.safe_int(raw.get("altitudeHi1")),
            altitude_low=cls.safe_int(raw.get("altitudeLow1")),
            movement_dir=str(movement_dir) if movement_dir is not None else None,
            movement_spd=str(movement_spd) if movement_spd is not None else None,
            severity=cls.safe_int(raw.get("severity")),
            raw_sigmet=raw.get("rawAirSigmet"),
            coords=coords_str,
        )

    @classmethod
    def parse_intl_sigmet(cls, raw: dict) -> Optional[Sigmet]:
        """
        Parse an international SIGMET API response dict into a Sigmet dataclass.

        Args:
            raw: International SIGMET dictionary from the API.

        Returns:
            Sigmet dataclass or None if required fields are missing.
        """
        icao_id = raw.get("icaoId")
        series_id = raw.get("seriesId")
        if not icao_id or not series_id:
            return None

        valid_from = cls.epoch_to_iso(raw.get("validTimeFrom"))
        valid_to = cls.epoch_to_iso(raw.get("validTimeTo"))
        if not valid_from or not valid_to:
            return None

        coords_raw = raw.get("coords")
        coords_str = json.dumps(coords_raw) if coords_raw is not None else None

        return Sigmet(
            icao_id=icao_id,
            series_id=series_id,
            valid_time_from=valid_from,
            valid_time_to=valid_to,
            hazard=raw.get("hazard"),
            qualifier=raw.get("qualifier"),
            sigmet_type="ISIGMET",
            altitude_hi=cls.safe_int(raw.get("top")),
            altitude_low=cls.safe_int(raw.get("base")),
            movement_dir=raw.get("dir"),
            movement_spd=raw.get("spd"),
            severity=None,
            raw_sigmet=raw.get("rawSigmet"),
            coords=coords_str,
        )

    @staticmethod
    def sigmet_dedup_key(sigmet: Sigmet) -> str:
        """
        Generate a deduplication key for a SIGMET.

        Args:
            sigmet: Sigmet dataclass.

        Returns:
            A string key unique to this SIGMET.
        """
        return f"{sigmet.icao_id}:{sigmet.series_id}:{sigmet.valid_time_from}:{sigmet.valid_time_to}"

    def load_state(self) -> Dict:
        """
        Load the persisted state from disk.

        Returns:
            State dict with metar_timestamps and sigmet_keys.
        """
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    if isinstance(state, dict):
                        return {
                            "metar_timestamps": state.get("metar_timestamps", {}),
                            "sigmet_keys": state.get("sigmet_keys", []),
                        }
        except Exception:
            pass
        return {"metar_timestamps": {}, "sigmet_keys": []}

    def save_state(self, state: Dict):
        """
        Save the current state to disk for deduplication across restarts.

        Args:
            state: State dictionary.
        """
        try:
            dir_name = os.path.dirname(self.last_polled_file)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Error saving state: {e}")

    def emit_stations(self) -> int:
        """
        Fetch and emit station reference data.

        Returns:
            Number of stations emitted.
        """
        raw_stations = self.fetch_station_json(self.station_ids)
        count = 0
        for raw in raw_stations:
            station = self.parse_station(raw)
            if station:
                self.producer.send_gov_noaa_aviationweather_station(
                    station.icao_id, station, flush_producer=False)
                count += 1
        if count > 0:
            self.producer.producer.flush()
        return count

    def emit_metars(self, metar_timestamps: Dict[str, str]) -> Tuple[int, Dict[str, str]]:
        """
        Fetch, deduplicate, and emit METAR observations.

        Args:
            metar_timestamps: Dict of icao_id -> last obs_time for dedup.

        Returns:
            Tuple of (new events count, updated timestamps dict).
        """
        raw_metars = self.fetch_metar_json(self.station_ids)
        count = 0
        for raw in raw_metars:
            metar = self.parse_metar(raw)
            if metar is None:
                continue
            if metar_timestamps.get(metar.icao_id) == metar.obs_time:
                continue
            self.producer.send_gov_noaa_aviationweather_metar(
                metar.icao_id, metar, flush_producer=False)
            metar_timestamps[metar.icao_id] = metar.obs_time
            count += 1
        if count > 0:
            self.producer.producer.flush()
        return count, metar_timestamps

    def emit_sigmets(self, seen_keys: Set[str]) -> Tuple[int, Set[str]]:
        """
        Fetch, deduplicate, and emit SIGMETs (both US and international).

        Args:
            seen_keys: Set of previously seen SIGMET dedup keys.

        Returns:
            Tuple of (new events count, updated seen keys set).
        """
        all_sigmets: List[Sigmet] = []

        for raw in self.fetch_airsigmet_json():
            sigmet = self.parse_us_sigmet(raw)
            if sigmet:
                all_sigmets.append(sigmet)

        for raw in self.fetch_isigmet_json():
            sigmet = self.parse_intl_sigmet(raw)
            if sigmet:
                all_sigmets.append(sigmet)

        count = 0
        current_keys: Set[str] = set()
        for sigmet in all_sigmets:
            key = self.sigmet_dedup_key(sigmet)
            current_keys.add(key)
            if key in seen_keys:
                continue
            self.producer.send_gov_noaa_aviationweather_sigmet(
                sigmet.icao_id, sigmet, flush_producer=False)
            count += 1
        if count > 0:
            self.producer.producer.flush()
        return count, current_keys

    def poll_and_send(self, once: bool = False):
        """
        Main polling loop. Emits station reference data at startup, then
        polls for METARs and SIGMETs, deduplicating by observation time
        and SIGMET identity.

        Args:
            once: Run one poll iteration and return. Intended for tests.
        """
        print(f"Starting AviationWeather.gov poller")
        print(f"  Stations: {self.station_ids}")
        print(f"  METAR poll interval: {self.metar_poll_interval}s")
        print(f"  SIGMET poll interval: {self.sigmet_poll_interval}s")
        print(f"  Kafka topic: {self.kafka_topic}")

        # Emit reference data at startup
        print("Fetching and sending station reference data...")
        station_count = self.emit_stations()
        print(f"Sent {station_count} station(s) as reference data")

        state = self.load_state()
        metar_timestamps = state.get("metar_timestamps", {})
        seen_sigmet_keys: Set[str] = set(state.get("sigmet_keys", []))
        last_sigmet_poll = 0.0
        last_station_refresh = time.time()

        while True:
            try:
                now = time.time()

                # Poll METARs
                metar_count, metar_timestamps = self.emit_metars(metar_timestamps)
                if metar_count > 0:
                    print(f"Sent {metar_count} new METAR(s)")

                # Poll SIGMETs at their own interval
                if now - last_sigmet_poll >= self.sigmet_poll_interval:
                    sigmet_count, seen_sigmet_keys = self.emit_sigmets(seen_sigmet_keys)
                    if sigmet_count > 0:
                        print(f"Sent {sigmet_count} new SIGMET(s)")
                    last_sigmet_poll = now

                # Re-emit station reference data periodically
                if now - last_station_refresh >= STATION_REFRESH_HOURS * 3600:
                    print("Refreshing station reference data...")
                    refresh_count = self.emit_stations()
                    print(f"Refreshed {refresh_count} station(s)")
                    last_station_refresh = now

                # Save state
                state = {
                    "metar_timestamps": metar_timestamps,
                    "sigmet_keys": list(seen_sigmet_keys),
                }
                self.save_state(state)

            except Exception as e:
                print(f"Error in polling loop: {e}")

            if once:
                break

            time.sleep(self.metar_poll_interval)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse an Azure Event Hubs-style connection string and extract Kafka parameters.

    Args:
        connection_string: The connection string.

    Returns:
        Dict with bootstrap.servers, kafka_topic, sasl.username, sasl.password.
    """
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                    '"').replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=')[1].strip('"')
            elif 'SharedAccessKeyName' in part:
                config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part:
                config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if 'sasl.username' in config_dict:
        config_dict['security.protocol'] = 'SASL_SSL'
        config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict


def main():
    """
    Main function to parse arguments and start the AviationWeather.gov poller.
    """
    parser = argparse.ArgumentParser(description="AviationWeather.gov METAR/SIGMET Bridge")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store last seen state for deduplication")
    parser.add_argument('--kafka-bootstrap-servers', type=str,
                        help="Comma separated list of Kafka bootstrap servers")
    parser.add_argument('--kafka-topic', type=str,
                        help="Kafka topic to send messages to")
    parser.add_argument('--sasl-username', type=str,
                        help="Username for SASL PLAIN authentication")
    parser.add_argument('--sasl-password', type=str,
                        help="Password for SASL PLAIN authentication")
    parser.add_argument('--connection-string', type=str,
                        help='Microsoft Event Hubs or Microsoft Fabric Event Stream connection string')
    parser.add_argument('--stations', type=str,
                        help=f"Comma-separated list of ICAO station IDs (default: {DEFAULT_STATIONS})")
    parser.add_argument('--metar-poll-interval', type=int, default=METAR_POLL_INTERVAL,
                        help=f"METAR poll interval in seconds (default: {METAR_POLL_INTERVAL})")
    parser.add_argument('--sigmet-poll-interval', type=int, default=SIGMET_POLL_INTERVAL,
                        help=f"SIGMET poll interval in seconds (default: {SIGMET_POLL_INTERVAL})")

    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.last_polled_file:
        args.last_polled_file = os.getenv('AVIATIONWEATHER_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.aviationweather_last_polled.json')
    if not args.stations:
        args.stations = os.getenv('AVIATIONWEATHER_STATIONS', DEFAULT_STATIONS)

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = config_params.get('bootstrap.servers')
        kafka_topic = config_params.get('kafka_topic')
        sasl_username = config_params.get('sasl.username')
        sasl_password = config_params.get('sasl.password')
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided either through the command line or connection string.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided either through the command line or connection string.")
        sys.exit(1)

    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
    kafka_config: Dict[str, str] = {
        'bootstrap.servers': kafka_bootstrap_servers,
    }
    if sasl_username and sasl_password:
        kafka_config.update({
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password
        })
    elif tls_enabled:
        kafka_config['security.protocol'] = 'SSL'

    poller = AviationWeatherPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file,
        station_ids=args.stations,
        metar_poll_interval=args.metar_poll_interval,
        sigmet_poll_interval=args.sigmet_poll_interval,
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
