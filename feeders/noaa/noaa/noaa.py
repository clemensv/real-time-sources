"""
NOAA Data Poller
Polls NOAA data and sends it to a Kafka topic using SASL PLAIN authentication.
"""

# pylint: disable=line-too-long


import os
import json
import sys
from datetime import datetime, timedelta, timezone
from typing import Dict, List
import argparse
import requests
from noaa_producer_data import AirPressure
from noaa_producer_data import AirTemperature
from noaa_producer_data import Conductivity
from noaa_producer_data import Humidity
from noaa_producer_data import Predictions
from noaa_producer_data import Salinity
from noaa_producer_data import Station
from noaa_producer_data import Visibility
from noaa_producer_data import WaterLevel
from noaa_producer_data import WaterTemperature
from noaa_producer_data import Wind
from noaa_producer_data import Currents
from noaa_producer_data import CurrentPredictions
from noaa_producer_data import QualityLevel
from noaa_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAAEventProducer


# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-noaa/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

VISIBILITY_DATASCHEMA = "#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/Microsoft.OpenData.US.NOAA.Visibility"
VISIBILITY_DATACONTENTTYPE = "application/json"


# --- Outbound request pacing -------------------------------------------------
# NOAA CO-OPS publishes no numeric rate limit for the `datagetter` API, but its
# AWS API Gateway *will* hard-ban a source IP that polls abusively, returning
# `403 ForbiddenException` for every subsequent request. An unthrottled poller
# iterating stations x products in a tight `while True:` loop trivially reaches
# several requests per second sustained around the clock, which is what earned
# this feeder an IP ban. Every knob below is overridable so operators can slow
# the feeder further without a rebuild.

# Minimum wall-clock spacing between two outbound datagetter requests.
MIN_REQUEST_INTERVAL = float(os.environ.get("NOAA_MIN_REQUEST_INTERVAL", "1.0"))
# Idle time between full poll cycles. NOAA data is 6-minute-interval at best,
# so polling more often than this cannot yield new observations anyway.
POLL_INTERVAL = float(os.environ.get("NOAA_POLL_INTERVAL", "900"))
# How long to stand down after the API signals rate limiting / forbids us.
RATE_LIMIT_COOLDOWN = float(os.environ.get("NOAA_RATE_LIMIT_COOLDOWN", "300"))
MAX_RATE_LIMIT_COOLDOWN = float(os.environ.get("NOAA_MAX_RATE_LIMIT_COOLDOWN", "3600"))
# Adaptive skipping: most stations do not offer most products, so those
# requests are guaranteed-empty pure waste. After this many consecutive empty
# responses for a (product, station) pair, start skipping it for a growing
# number of cycles, capped by MAX_EMPTY_BACKOFF.
EMPTY_BACKOFF_THRESHOLD = int(os.environ.get("NOAA_EMPTY_BACKOFF_THRESHOLD", "3"))
MAX_EMPTY_BACKOFF = int(os.environ.get("NOAA_MAX_EMPTY_BACKOFF", "32"))


class _RateLimiter:
    """
    Simple monotonic-clock spacing gate shared by every outbound NOAA request.

    `wait()` blocks until at least `min_interval` seconds have elapsed since
    the previous call, guaranteeing a hard ceiling on outbound request rate
    regardless of how fast the poll loop iterates.
    """

    def __init__(self, min_interval: float):
        self.min_interval = max(0.0, min_interval)
        self._last_call = 0.0

    def wait(self) -> None:
        """Block until the configured minimum spacing has elapsed."""
        if self.min_interval <= 0:
            return
        import time
        now = time.monotonic()
        elapsed = now - self._last_call
        if 0 <= elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_call = time.monotonic()


def _atomic_write_json(path: str, data: Dict, retries: int = 5, backoff_seconds: float = 0.5) -> None:
    """
    Write JSON to `path` resiliently against transient BlockingIOError/OSError
    from shared network filesystems (e.g. Azure Files/NFS lock contention),
    and atomically (write-to-temp-then-rename) so a failed or interrupted
    write never leaves a truncated/corrupt state file behind.
    """
    import errno
    import time
    import uuid

    tmp_path = f"{path}.{uuid.uuid4().hex}.tmp"
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with open(tmp_path, 'w', encoding='utf-8') as file:
                json.dump(data, file)
            os.replace(tmp_path, path)
            return
        except (BlockingIOError, OSError) as exc:
            last_exc = exc
            transient = isinstance(exc, BlockingIOError) or getattr(exc, "errno", None) in (
                errno.EAGAIN,
                errno.EWOULDBLOCK,
                errno.EBUSY,
            )
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except OSError:
                pass
            if not transient or attempt >= retries:
                raise
            time.sleep(backoff_seconds * (2 ** attempt))
    if last_exc is not None:
        raise last_exc

class NOAADataPoller:
    """
    Class to poll NOAA data and send it to a Kafka topic.
    """
    BASE_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
    COMMON_PARAMS = "&units=metric&time_zone=gmt&application=web_services&format=json"

    PRODUCTS = {
        "water_level": "product=water_level",
        "predictions": "product=predictions",
        "air_temperature": "product=air_temperature",
        "wind": "product=wind",
        "air_pressure": "product=air_pressure",
        "water_temperature": "product=water_temperature",
        "conductivity": "product=conductivity",
        "visibility": "product=visibility",
        "humidity": "product=humidity",
        "salinity": "product=salinity",
        "currents": "product=currents",
        "currents_predictions": "product=currents_predictions"
    }

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str, station: str = None):
        """
        Initialize the NOAADataPoller class.

        Args:
            kafka_config (Dict[str, str]): Kafka configuration settings.
            kafka_topic (str): Kafka topic to send messages to.
            last_polled_file (str): File to store the last polled times for each station and product.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        self.rate_limiter = _RateLimiter(MIN_REQUEST_INTERVAL)
        # Current stand-down window after a 403/429; grows on repeat offences.
        self.rate_limit_cooldown = RATE_LIMIT_COOLDOWN
        # (product, station_id) -> consecutive-empty count / cycles left to skip
        self.empty_streak: Dict[tuple, int] = {}
        self.skip_cycles: Dict[tuple, int] = {}
        from confluent_kafka import Producer
        kafka_producer = Producer(kafka_config)
        self.producer = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, kafka_topic)
        self.stations = self.fetch_all_stations()
        if station:
            requested = [s.strip() for s in str(station).split(',') if s.strip()]
            self.selected_stations = [s for s in self.stations if s.station_id in requested]
            found_ids = {s.station_id for s in self.selected_stations}
            missing = [r for r in requested if r not in found_ids]
            if missing:
                print(f"Station(s) not found: {', '.join(missing)}")
            if not self.selected_stations:
                print(f"None of the requested stations were found: {', '.join(requested)}")
                sys.exit(1)
        else:
            self.selected_stations = None

    def fetch_all_stations(self) -> List[Station]:
        """
        Fetch all NOAA stations.

        Returns:
            list: List of all NOAA stations.
        """
        url = "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json"
        try:
            self.rate_limiter.wait()
            response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
            response.raise_for_status()
            stations_data = response.json()
            raw_stations = stations_data.get('stations', [])
            for s in raw_stations:
                if s.get('portscode') is None:
                    s['portscode'] = ''
                s['station_id'] = s.pop('id', '')
                # The generated Station schema models every nested link object
                # with the generic UnnamedClass, whose optional `region` and
                # `station_id` fields are emitted without a `None` default.
                # dataclasses_json therefore requires those keys on every nested
                # object, but the NOAA station list returns bare `{"self": ...}`
                # link stubs that omit them. Backfill the optional keys so the
                # decode succeeds. The JsonStructure schema types both keys as
                # `string`, so backfill an empty string (not None) to keep the
                # emitted CloudEvent schema-valid. (Upstream codegen bug:
                # optional string fields must default to "".)
                for value in s.values():
                    for item in (value if isinstance(value, list) else [value]):
                        if isinstance(item, dict):
                            item.setdefault('region', '')
                            item.setdefault('station_id', '')
# pylint: disable=no-member
            stations = Station.schema().load(raw_stations, many=True)  # type: ignore[attr-defined]
# pylint: enable=no-member
            return stations
        except requests.RequestException as err:
            print(f"Error fetching stations: {err}")
            return []

    def get_datum_for_station(self, station_id: str) -> str:
        """
        Determine the datum value for a station based on its tideType.

        Args:
            station_id (str): The ID of the station.

        Returns:
            str: The datum value (either "MLLW" or "IGLD").
        """
        station_info: Station = next((station for station in self.stations if station.station_id == station_id), {})
        tide_type = station_info.tideType
        return "IGLD" if tide_type == "Great Lakes" else "MLLW"

    def poll_noaa_api(self, product: str, station_id: str, last_polled_time: datetime) -> list:
        """
        Poll the NOAA API for new data.

        Args:
            product (str): The product to poll.
            station_id (str): The ID of the station.
            last_polled_time (datetime): The last time data was polled.

        Returns:
            list: List of new data records.
        """
        datum = self.get_datum_for_station(station_id)
        if datum == "IGLD" and "predictions" in product:
            return []  # Great Lakes stations don't have prediction data
        
        # Clamp date range to NOAA API limits
        # 6-minute interval data (water_level, met data): max 1 month
        # Predictions: max 1 year
        now = datetime.now(timezone.utc)
        if product in ["predictions", "currents_predictions"]:
            # Predictions can go back 1 year
            max_begin_date = now - timedelta(days=365)
        else:
            # 6-minute interval data: max 1 month
            max_begin_date = now - timedelta(days=30)
        
        # Use the more recent of last_polled_time or max_begin_date
        begin_date = max(last_polled_time, max_begin_date)
        
        product_url = f"{self.BASE_URL}?{self.PRODUCTS[product]}{self.COMMON_PARAMS}&station={station_id}"
        if product != "currents_predictions" and product != "currents":
            product_url += f"&datum={datum}"
        if product in ["currents", "currents_predictions"]:
            product_url += "&bin=1"
        product_url += f"&begin_date={begin_date.strftime('%Y%m%d %H:%M')}&end_date={now.strftime('%Y%m%d %H:%M')}"
        if product == "currents_predictions":
            data_key = None
        elif "predictions" in product:
            data_key = "predictions"
        else:
            data_key = "data"
        try:
            self.rate_limiter.wait()
            response = requests.get(product_url, headers={"User-Agent": USER_AGENT}, timeout=10)
            if response.status_code in (403, 429):
                # NOAA's API Gateway blocks abusive callers at the IP level and
                # keeps returning 403 long after the offending traffic stops.
                # Stand down for a growing window rather than hammering on and
                # deepening the ban.
                import time
                print(
                    f"NOAA API returned {response.status_code} for station {station_id} "
                    f"({product}); backing off {self.rate_limit_cooldown:.0f}s. If this "
                    f"persists across all stations, this source IP is likely blocked "
                    f"by NOAA and must be changed or unblocked."
                )
                time.sleep(self.rate_limit_cooldown)
                self.rate_limit_cooldown = min(
                    self.rate_limit_cooldown * 2, MAX_RATE_LIMIT_COOLDOWN)
                return []
            response.raise_for_status()
            # Successful call -- reset the escalating cooldown.
            self.rate_limit_cooldown = RATE_LIMIT_COOLDOWN
            if data_key is None:
                data = response.json().get("current_predictions", {}).get("cp", [])
            else:
                data = response.json().get(data_key, [])
            new_data = []
            for record in data:
                new_data.append(record)

            return new_data
        except requests.RequestException as err:
            print(f"Error fetching data for station {station_id}: {err}")
            return []

    def pascal(self, s: str) -> str:
        """
        Convert a snake_case string to PascalCase.

        Args:
            s (str): The snake_case string.

        Returns:
            str: The PascalCase string.
        """
        return ''.join([part.capitalize() for part in s.split('_')])

    def load_last_polled_times(self) -> Dict:
        """
        Load the last polled times from a file.

        Returns:
            Dict: The last polled times for each station and product.
        """
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, 'r', encoding='utf-8') as file:
                    saved_times: Dict[str, Dict[str, str]] = json.load(file)
                    last_polled_times: Dict[str, Dict[str, datetime]] = {}
                    for product, stations in saved_times.items():
                        for station, timestamp in stations.items():
                            if product not in last_polled_times:
                                last_polled_times[product] = {}
                            last_polled_times[product][station] = datetime.fromisoformat(timestamp)
                    return last_polled_times
        except Exception:
            print("Error loading last polled times")
        return {}

    def save_last_polled_times(self, last_polled_times: Dict):
        """
        Save the last polled times to a file.

        Args:
            last_polled_times (Dict): The last polled times for each station and product.
        """
        # convert all datetime objects to string for serialization
        saved_times: Dict[str, Dict[str, str]] = {}
        for product, stations in last_polled_times.items():
            for station, timestamp in stations.items():
                if product not in saved_times:
                    saved_times[product] = {}
                saved_times[product][station] = timestamp.isoformat()
        os.makedirs(os.path.dirname(self.last_polled_file), exist_ok=True)
        _atomic_write_json(self.last_polled_file, saved_times)

    def poll_and_send(self):
        """
        Poll NOAA data and send it to Kafka.
        """
        last_polled_times = self.load_last_polled_times()

        stations_to_poll = self.selected_stations if self.selected_stations else self.stations

        for station in stations_to_poll:
            self.producer.send_microsoft_open_data_us_noaa_station(station.station_id, station, flush_producer=False)
        self.producer.producer.flush()

        while True:
            for station in stations_to_poll:
                station_id = station.station_id
                station_region = getattr(station, "region", None) or "unknown"
                for product in self.PRODUCTS:
                    pair = (product, station_id)
                    # Most stations do not offer most products. Skip pairs that
                    # have repeatedly come back empty so we spend our limited
                    # request budget on pairs that actually carry data.
                    remaining = self.skip_cycles.get(pair, 0)
                    if remaining > 0:
                        self.skip_cycles[pair] = remaining - 1
                        continue
                    print(f"Polling {product} data for station {station_id}: {station.name}:", end='')
                    last_polled_time = last_polled_times.get(product, {}).get(
                        station_id, datetime.now(timezone.utc) - timedelta(hours=24))
                    new_data_records = self.poll_noaa_api(product, station_id, last_polled_time)
                    print(f" {len(new_data_records)} new records found since {last_polled_time}")

                    if new_data_records:
                        self.empty_streak.pop(pair, None)
                    else:
                        streak = self.empty_streak.get(pair, 0) + 1
                        self.empty_streak[pair] = streak
                        if streak >= EMPTY_BACKOFF_THRESHOLD:
                            # Exponential in the number of empties past the
                            # threshold, capped so a pair is always retried
                            # eventually (a station may start reporting later).
                            self.skip_cycles[pair] = min(
                                2 ** (streak - EMPTY_BACKOFF_THRESHOLD + 1),
                                MAX_EMPTY_BACKOFF)

                    max_timestamp = last_polled_time
                    for record in new_data_records:
                        ts_field = 'Time' if product == "currents_predictions" else 't'
                        ts_parsed = datetime.strptime(record[ts_field], "%Y-%m-%d %H:%M")
                        timestamp = ts_parsed.replace(tzinfo=timezone.utc)

                        if product == "water_level":
                            water_level = WaterLevel(
                                station_id=station_id,
                                region=station_region,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                                stddev=float(record['s']) if 's' in record and record['s'] else 0.0,
                                outside_sigma_band=bool(record.get('f', '').split(',')[0] == '1'),
                                flat_tolerance_limit=bool(record.get('f', '').split(',')[1] == '1'),
                                rate_of_change_limit=bool(record.get('f', '').split(',')[2] == '1'),
                                max_min_expected_height=bool(record.get('f', '').split(',')[3] == '1'),
                                quality=QualityLevel.Preliminary if record.get(
                                    'q', '') == 'p' else QualityLevel.Verified
                            )
                            self.producer.send_microsoft_open_data_us_noaa_water_level(
                                station_id, water_level, flush_producer=False)
                        elif product == "predictions":
                            prediction = Predictions(
                                station_id=station_id,
                                region=station_region,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                            )
                            self.producer.send_microsoft_open_data_us_noaa_predictions(
                                station_id, prediction, flush_producer=False)
                        elif product == "air_temperature":
                            air_temperature = AirTemperature(
                                station_id=station_id,
                                region=station_region,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                                max_temp_exceeded=bool(record.get('f', '').split(',')[0] == '1'),
                                min_temp_exceeded=bool(record.get('f', '').split(',')[1] == '1'),
                                rate_of_change_exceeded=bool(record.get('f', '').split(',')[2] == '1')
                            )
                            self.producer.send_microsoft_open_data_us_noaa_air_temperature(
                                station_id, air_temperature, flush_producer=False)
                        elif product == "wind":
                            wind = Wind(
                                station_id=station_id,
                                region=station_region,
                                timestamp=timestamp.isoformat(),
                                speed=float(record['s']) if 's' in record and record['s'] else 0.0,
                                direction_degrees=record['d'] if 'd' in record and record['d'] else 0.0,
                                direction_text=record['dr'] if 'dr' in record and record['dr'] else '',
                                gusts=float(record['g']) if 'g' in record and record['g'] else 0.0,
                                max_wind_speed_exceeded=bool(record.get('f', '').split(',')[0] == '1'),
                                rate_of_change_exceeded=bool(record.get('f', '').split(',')[1] == '1')
                            )
                            self.producer.send_microsoft_open_data_us_noaa_wind(station_id, wind, flush_producer=False)
                        elif product == "air_pressure":
                            air_pressure = AirPressure(
                                station_id=station_id,
                                region=station_region,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                                max_pressure_exceeded=bool(record.get('f', '').split(',')[0] == '1'),
                                min_pressure_exceeded=bool(record.get('f', '').split(',')[1] == '1'),
                                rate_of_change_exceeded=bool(record.get('f', '').split(',')[2] == '1')
                            )
                            self.producer.send_microsoft_open_data_us_noaa_air_pressure(
                                station_id, air_pressure, flush_producer=False)
                        elif product == "water_temperature":
                            water_temperature = WaterTemperature(
                                station_id=station_id,
                                region=station_region,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                                max_temp_exceeded=bool(record.get('f', '').split(',')[0] == '1'),
                                min_temp_exceeded=bool(record.get('f', '').split(',')[1] == '1'),
                                rate_of_change_exceeded=bool(record.get('f', '').split(',')[2] == '1')
                            )
                            self.producer.send_microsoft_open_data_us_noaa_water_temperature(
                                station_id, water_temperature, flush_producer=False)
                        elif product == "conductivity":
                            conductivity = Conductivity(
                                station_id=station_id,
                                region=station_region,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                                max_conductivity_exceeded=bool(record.get('f', '').split(',')[0] == '1'),
                                min_conductivity_exceeded=bool(record.get('f', '').split(',')[1] == '1'),
                                rate_of_change_exceeded=bool(record.get('f', '').split(',')[2] == '1')
                            )
                            self.producer.send_microsoft_open_data_us_noaa_conductivity(
                                station_id, conductivity, flush_producer=False)
                        elif product == "visibility":
                            visibility = Visibility(
                                station_id=station_id,
                                region=station_region,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                                max_visibility_exceeded=bool(record.get('f', '').split(',')[0] == '1'),
                                min_visibility_exceeded=bool(record.get('f', '').split(',')[1] == '1'),
                                rate_of_change_exceeded=bool(record.get('f', '').split(',')[2] == '1')
                            )
                            self.producer.send_microsoft_open_data_us_noaa_visibility(
                                _datacontenttype=VISIBILITY_DATACONTENTTYPE,
                                _dataschema=VISIBILITY_DATASCHEMA,
                                _station_id=station_id,
                                data=visibility,
                                _time=visibility.timestamp,
                                flush_producer=False)
                        elif product == "humidity":
                            humidity = Humidity(
                                station_id=station_id,
                                region=station_region,
                                timestamp=timestamp.isoformat(),
                                value=float(record['v']) if 'v' in record and record['v'] else 0.0,
                                max_humidity_exceeded=bool(record.get('f', '').split(',')[0] == '1'),
                                min_humidity_exceeded=bool(record.get('f', '').split(',')[1] == '1'),
                                rate_of_change_exceeded=bool(record.get('f', '').split(',')[2] == '1')
                            )
                            self.producer.send_microsoft_open_data_us_noaa_humidity(
                                station_id, humidity, flush_producer=False)
                        elif product == "salinity":
                            salinity = Salinity(
                                station_id=station_id,
                                region=station_region,
                                timestamp=timestamp.isoformat(),
                                salinity=float(record['s']) if 's' in record and record['s'] else 0.0,
                                grams_per_kg=float(record['g']) if 'g' in record and record['g'] else 0.0,
                            )
                            self.producer.send_microsoft_open_data_us_noaa_salinity(
                                station_id, salinity, flush_producer=False)
                        elif product == "currents":
                            currents_record = Currents(
                                station_id=station_id,
                                region=station_region,
                                timestamp=timestamp.isoformat(),
                                speed=float(record['s']) if 's' in record and record['s'] else 0.0,
                                direction_degrees=float(record['d']) if 'd' in record and record['d'] else 0.0,
                                bin=record.get('b', '1')
                            )
                            self.producer.send_microsoft_open_data_us_noaa_currents(
                                station_id, currents_record, flush_producer=False)
                        elif product == "currents_predictions":
                            current_prediction = CurrentPredictions(
                                station_id=station_id,
                                region=station_region,
                                timestamp=timestamp.isoformat(),
                                velocity_major=float(record['Velocity_Major']) if 'Velocity_Major' in record and record['Velocity_Major'] else 0.0,
                                mean_flood_dir=float(record['meanFloodDir']) if 'meanFloodDir' in record and record['meanFloodDir'] else 0.0,
                                mean_ebb_dir=float(record['meanEbbDir']) if 'meanEbbDir' in record and record['meanEbbDir'] else 0.0,
                                depth=float(record['Depth']) if 'Depth' in record and record['Depth'] else 0.0,
                                bin=record.get('Bin', '1')
                            )
                            self.producer.send_microsoft_open_data_us_noaa_current_predictions(
                                station_id, current_prediction, flush_producer=False)

                        if timestamp > max_timestamp:
                            max_timestamp = timestamp
                    self.producer.producer.flush()
                    if new_data_records:
                        if product not in last_polled_times:
                            last_polled_times[product] = {}
                        last_polled_times[product][station_id] = max_timestamp
                        try:
                            self.save_last_polled_times(last_polled_times)
                        except OSError as exc:
                            # Do not let a transient state-file write failure
                            # (e.g. shared fileshare lock contention) crash
                            # the whole poller -- log and retry on the next
                            # cycle instead.
                            print(f"Failed to save last-polled state (will retry next cycle): {exc}")

            if os.getenv('ONCE_MODE', 'false').lower() in ('true', '1', 'yes'):
                break

            # NOAA observations are 6-minute-interval at best, so re-polling
            # sooner than this cannot surface new data and only burns request
            # budget against an API that IP-bans abusive callers.
            if POLL_INTERVAL > 0:
                import time
                print(f"Poll cycle complete; sleeping {POLL_INTERVAL:.0f}s before next cycle.")
                time.sleep(POLL_INTERVAL)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse the connection string and extract bootstrap server, topic name, username, and password.

    Args:
        connection_string (str): The connection string.

    Returns:
        Dict[str, str]: Extracted connection parameters.
    """
    config_dict = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                    '"').replace('sb://', '').replace('/', '')+':9093'
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
    Main function to parse arguments and start the NOAA data poller.
    """
    parser = argparse.ArgumentParser(description="NOAA Data Poller")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store the last polled times for each station and product")
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
    parser.add_argument('--station', type=str,
                        help='Comma-separated list of station IDs to poll. If not provided, data for all stations will be polled.')

    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.station:
        args.station = os.getenv('NOAA_STATIONS') or os.getenv('NOAA_STATION')
    if not args.last_polled_file:
        args.last_polled_file = os.getenv('NOAA_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.noaa_last_polled.json')

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

    # Check if required parameters are provided
    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided either through the command line or connection string.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided either through the command line or connection string.")
        sys.exit(1)
    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
    kafka_config = {
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

    poller = NOAADataPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file,
        station=args.station
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
