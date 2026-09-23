"""NVE Hydrological Data Bridge - fetches water level and discharge data from the Norwegian Water Resources and Energy Directorate."""

import argparse
import json
import sys
import os
import time
import logging
import threading
import requests
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from confluent_kafka import Producer
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from nve_hydro_producer_data import Station
from nve_hydro_producer_data import WaterLevelObservation
from nve_hydro_producer_kafka_producer.producer import NONVEHydrologyEventProducer

logger = logging.getLogger(__name__)

NVE_BASE_URL = "https://hydapi.nve.no/api/v1"
# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-nve-hydro/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

PARAM_STAGE = 1000       # Water level / Vannstand (m)
PARAM_DISCHARGE = 1001   # Discharge / Vannføring (m³/s)

MAX_WORKERS = 4
MAX_SERIES_PER_REQUEST = 10
MIN_REQUEST_INTERVAL_SECONDS = 0.21
REFERENCE_REFRESH_SECONDS = int(os.environ.get("REFERENCE_REFRESH_INTERVAL", "14400"))


class NVEHydroAPI:
    """Client for the NVE HydAPI."""

    def __init__(self, api_key: str, base_url: str = NVE_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        self.session.headers['X-API-Key'] = api_key
        self.session.headers['Accept'] = 'application/json'
        retry = Retry(
            total=4,
            connect=4,
            read=4,
            status=4,
            backoff_factor=1.0,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET"}),
            respect_retry_after_header=True,
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=MAX_WORKERS, pool_maxsize=MAX_WORKERS)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self._rate_lock = threading.Lock()
        self._last_request_at = 0.0

    def _get(self, path: str, *, params: dict, timeout: int) -> requests.Response:
        with self._rate_lock:
            delay = MIN_REQUEST_INTERVAL_SECONDS - (time.monotonic() - self._last_request_at)
            if delay > 0:
                time.sleep(delay)
            self._last_request_at = time.monotonic()
        response = self.session.get(f"{self.base_url}/{path}", params=params, timeout=timeout)
        if response.status_code == 429:
            logger.warning("NVE HydAPI throttled request to %s; retries exhausted", path)
        response.raise_for_status()
        return response

    def get_stations(self) -> list:
        """Fetch all active stations."""
        response = self._get("Stations", params={"Active": "1"}, timeout=60)
        return response.json().get('data', [])

    def get_observations(self, station_ids: str | list[str], parameters: int | list[int]) -> list:
        """Fetch the latest observations for at most ten station/parameter series."""
        station_id = station_ids if isinstance(station_ids, str) else ",".join(station_ids)
        parameter = str(parameters) if isinstance(parameters, int) else ",".join(str(p) for p in parameters)
        params = {
            "StationId": station_id,
            "Parameter": parameter,
            "ResolutionTime": "0",
        }
        try:
            response = self._get("Observations", params=params, timeout=60)
            return response.json().get('data', [])
        except requests.RequestException as e:
            logger.warning(
                "Failed to fetch observations for stations %s and parameters %s: %s",
                station_id,
                parameter,
                e,
            )
            return []


def parse_connection_string(connection_string: str) -> dict:
    """Parse a Kafka connection string into a config dict."""
    config = {}
    for part in connection_string.split(';'):
        part = part.strip()
        if '=' in part:
            key, value = part.split('=', 1)
            key = key.strip()
            value = value.strip()
            if key == 'Endpoint':
                config['bootstrap.servers'] = value.replace('sb://', '').rstrip('/') + ':9093'
            elif key == 'SharedAccessKeyName':
                config['sasl.username'] = '$ConnectionString'
            elif key == 'SharedAccessKey':
                config['sasl.password'] = connection_string
            elif key == 'BootstrapServer':
                config['bootstrap.servers'] = value
            elif key == 'EntityPath':
                config['_entity_path'] = value
    if 'sasl.username' in config:
        config['security.protocol'] = 'SASL_SSL'
        config['sasl.mechanism'] = 'PLAIN'
    return config


def _load_state(state_file: str) -> dict:
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logging.warning("Could not load state from %s: %s", state_file, e)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    if not state_file:
        return
    try:
        if len(data) > 100000:
            keys = list(data.keys())
            data = {k: data[k] for k in keys[-50000:]}
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception as e:
        logging.warning("Could not save state to %s: %s", state_file, e)


def _parse_datetime(value: str | None) -> datetime | None:
    """Parse an upstream ISO 8601 timestamp, including the UTC ``Z`` suffix."""
    if not value:
        return None
    text = value.strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text)


def _station_has_parameter(station: dict, param_id: int) -> bool:
    """Check if a station has a specific parameter in its series list."""
    for series in station.get('seriesList') or []:
        if series.get('parameter') == param_id:
            return True
    return False


def _fetch_station_observations(api: NVEHydroAPI, station_id: str, params: list) -> dict:
    """Fetch latest observations for a station across multiple parameters."""
    result = {}
    for param_id in params:
        obs_list = api.get_observations(station_id, param_id)
        for item in obs_list:
            observations = item.get('observations', [])
            if observations:
                latest = observations[-1]
                if latest.get('value') is not None:
                    result[param_id] = latest
                    break
    return result


def _build_observation_batches(station_params: dict[str, list[int]]) -> list[list[str]]:
    """Group stations into requests that stay within HydAPI's ten-series limit."""
    batches: list[list[str]] = []
    current: list[str] = []
    series_count = 0
    for station_id, params in station_params.items():
        station_series = len(params)
        if current and series_count + station_series > MAX_SERIES_PER_REQUEST:
            batches.append(current)
            current = []
            series_count = 0
        current.append(station_id)
        series_count += station_series
    if current:
        batches.append(current)
    return batches


def _fetch_observation_batch(
    api: NVEHydroAPI,
    station_ids: list[str],
    station_params: dict[str, list[int]],
) -> dict[str, dict[int, dict]]:
    parameters = sorted({param for sid in station_ids for param in station_params[sid]})
    result: dict[str, dict[int, dict]] = {}
    for item in api.get_observations(station_ids, parameters):
        station_id = item.get("stationId")
        parameter = item.get("parameter")
        if not station_id or parameter not in station_params.get(station_id, []):
            continue
        for observation in reversed(item.get("observations") or []):
            if observation.get("value") is None:
                continue
            result.setdefault(station_id, {})[parameter] = {
                **observation,
                "unit": item.get("unit"),
                "method": item.get("method"),
                "series_version": item.get("serieVersionNo"),
            }
            break
    return result


def fetch_observation_batches(
    api: NVEHydroAPI,
    station_params: dict[str, list[int]],
) -> dict[str, dict[int, dict]]:
    """Fetch current observations with bounded concurrency and HydAPI-sized batches."""
    observations: dict[str, dict[int, dict]] = {}
    batches = _build_observation_batches(station_params)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(_fetch_observation_batch, api, batch, station_params): batch
            for batch in batches
        }
        for future in as_completed(futures):
            try:
                observations.update(future.result())
            except Exception as exc:
                logger.warning("Failed NVE observation batch %s: %s", futures[future], exc)
    return observations


def send_stations(api: NVEHydroAPI, producer: NONVEHydrologyEventProducer) -> tuple:
    """Fetch stations and send station reference events. Returns (station_params, station_river) tuple."""
    stations = api.get_stations()
    sent_count = 0
    station_params = {}
    station_river: dict = {}
    for station in stations:
        sid = station.get('stationId')
        if not sid:
            continue
        params = []
        if _station_has_parameter(station, PARAM_STAGE):
            params.append(PARAM_STAGE)
        if _station_has_parameter(station, PARAM_DISCHARGE):
            params.append(PARAM_DISCHARGE)
        if params:
            station_params[sid] = params
        station_river[sid] = station.get('riverName', '') or ''

        station_data = Station(
            station_id=sid,
            station_name=station.get('stationName', ''),
            river_name=station.get('riverName'),
            latitude=station.get('latitude', 0.0),
            longitude=station.get('longitude', 0.0),
            masl=station.get('masl'),
            council_name=station.get('councilName'),
            county_name=station.get('countyName'),
            drainage_basin_area=station.get('drainageBasinArea'),
        )
        producer.send_no_nve_hydrology_station(_station_id=sid, data=station_data, flush_producer=False)
        sent_count += 1
        if sent_count % 100 == 0 and producer.producer.flush(timeout=120) != 0:
            raise RuntimeError("Kafka flush failed while emitting NVE station reference events")

    if producer.producer.flush(timeout=120) != 0:
        raise RuntimeError("Kafka flush failed while emitting NVE station reference events")
    logger.info("Sent %d station events", sent_count)
    return station_params, station_river


def feed_observations(api: NVEHydroAPI, producer: NONVEHydrologyEventProducer,
                      station_params: dict, station_river: dict, previous_readings: dict) -> int:
    """Fetch observations and send measurement events to Kafka."""
    sent_count = 0
    pending_readings: dict[str, str] = {}
    for sid, obs_by_param in fetch_observation_batches(api, station_params).items():
        if not obs_by_param:
            continue

        wl_val = None
        wl_ts = ""
        q_val = None
        q_ts = ""

        if PARAM_STAGE in obs_by_param:
            stage = obs_by_param[PARAM_STAGE]
            wl_val = float(stage["value"])
            wl_ts = stage.get("time", "")

        if PARAM_DISCHARGE in obs_by_param:
            discharge = obs_by_param[PARAM_DISCHARGE]
            q_val = float(discharge["value"])
            q_ts = discharge.get("time", "")

        if wl_val is None and q_val is None:
            continue

        reading_key = f"{sid}:{wl_ts}:{q_ts}"
        if reading_key in previous_readings:
            continue

        stage = obs_by_param.get(PARAM_STAGE, {})
        discharge = obs_by_param.get(PARAM_DISCHARGE, {})
        obs_data = WaterLevelObservation(
            station_id=sid,
            river_name=station_river.get(sid, '') or '',
            water_level=wl_val,
            water_level_unit=stage.get("unit") if wl_val is not None else None,
            water_level_timestamp=_parse_datetime(wl_ts),
            water_level_quality=stage.get("quality"),
            water_level_correction=stage.get("correction"),
            water_level_series_version=stage.get("series_version"),
            water_level_method=stage.get("method"),
            discharge=q_val,
            discharge_unit=discharge.get("unit") if q_val is not None else None,
            discharge_timestamp=_parse_datetime(q_ts),
            discharge_quality=discharge.get("quality"),
            discharge_correction=discharge.get("correction"),
            discharge_series_version=discharge.get("series_version"),
            discharge_method=discharge.get("method"),
        )
        producer.send_no_nve_hydrology_water_level_observation(
            _station_id=sid,
            data=obs_data,
            flush_producer=False,
        )
        sent_count += 1
        pending_readings[reading_key] = wl_ts or q_ts

    if producer.producer.flush(timeout=120) != 0:
        raise RuntimeError("Kafka flush failed while emitting NVE observations")
    previous_readings.update(pending_readings)
    return sent_count


def main():
    parser = argparse.ArgumentParser(description="NVE Hydrological Data Bridge")
    parser.add_argument('--connection-string', required=False,
                        default=os.environ.get('KAFKA_CONNECTION_STRING') or os.environ.get('CONNECTION_STRING'))
    parser.add_argument('--topic', required=False, default=os.environ.get('KAFKA_TOPIC'))
    parser.add_argument('--polling-interval', type=int,
                        default=int(os.environ.get('POLLING_INTERVAL', '600')))
    parser.add_argument('--state-file', type=str,
                        default=os.environ.get('STATE_FILE', os.path.expanduser('~/.nve_hydro_state.json')))
    parser.add_argument('--api-key', type=str,
                        default=os.environ.get('NVE_API_KEY'))
    parser.add_argument('--once', action='store_true', dest='root_once',
                        default=os.environ.get('ONCE_MODE', '').lower() in ('1', 'true', 'yes'),
                        help='Exit after one polling cycle (also via ONCE_MODE env var). Useful for scheduled execution in Fabric notebooks.')
    subparsers = parser.add_subparsers(dest='command')
    feed_parser = subparsers.add_parser('feed', help='Feed data to Kafka')
    feed_parser.add_argument('--once', action='store_true', dest='feed_once',
                             default=False,
                             help='Exit after one polling cycle (also via ONCE_MODE env var).')
    subparsers.add_parser('list', help='List all stations')

    args = parser.parse_args()
    args.once = bool(getattr(args, 'root_once', False) or getattr(args, 'feed_once', False))
    logging.basicConfig(level=logging.INFO)

    if not args.api_key:
        print("Error: NVE_API_KEY environment variable or --api-key required")
        sys.exit(1)

    api = NVEHydroAPI(args.api_key)

    if args.command == 'list':
        stations = api.get_stations()
        for s in stations:
            params = [str(p.get('parameter', '?')) for p in (s.get('seriesList') or [])]
            print(f"{s.get('stationId')}: {s.get('stationName')} ({s.get('riverName', '')}) "
                  f"[{s.get('latitude')}, {s.get('longitude')}] params={','.join(params)}")
    elif args.command == 'feed':
        if not args.connection_string:
            if not os.environ.get('KAFKA_BROKER'):
                print("Error: --connection-string or KAFKA_BROKER required for feed mode")
                sys.exit(1)
            kafka_config = {'bootstrap.servers': os.environ['KAFKA_BROKER']}
        else:
            kafka_config = parse_connection_string(args.connection_string)
        if '_entity_path' in kafka_config and not args.topic:
            args.topic = kafka_config.pop('_entity_path')
        elif '_entity_path' in kafka_config:
            kafka_config.pop('_entity_path')
        if not args.topic:
            args.topic = 'nve-hydro'
        tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
        if 'sasl.username' in kafka_config:
            kafka_config['security.protocol'] = 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT'
        elif tls_enabled:
            kafka_config['security.protocol'] = 'SSL'
        kafka_config['client.id'] = 'nve-hydro-bridge'
        kafka_producer = Producer(kafka_config)
        nve_producer = NONVEHydrologyEventProducer(kafka_producer, args.topic)
        logger.info("Starting NVE Hydro bridge, polling every %d seconds", args.polling_interval)
        previous_readings = _load_state(args.state_file)
        station_params, station_river = send_stations(api, nve_producer)
        last_station_refresh = time.monotonic()
        while True:
            try:
                count = feed_observations(api, nve_producer, station_params, station_river, previous_readings)
                _save_state(args.state_file, previous_readings)
                logger.info("Sent %d events", count)
                if time.monotonic() - last_station_refresh >= REFERENCE_REFRESH_SECONDS:
                    refreshed_params, refreshed_river = send_stations(api, nve_producer)
                    station_params = refreshed_params
                    station_river = refreshed_river
                    last_station_refresh = time.monotonic()
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            if args.once:
                logger.info("--once mode: exiting after first polling cycle")
                break
            time.sleep(args.polling_interval)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
