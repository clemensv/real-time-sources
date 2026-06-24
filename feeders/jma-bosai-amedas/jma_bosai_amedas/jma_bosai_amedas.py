"""Bridge JMA Bosai AMeDAS station metadata and observations to Kafka CloudEvents."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone, timedelta
import json
import logging
import os
from pathlib import Path
import sys
import time
from typing import Any, Dict, Iterable, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from confluent_kafka import Producer

from jma_bosai_amedas_producer_data.jp.jma.amedas.observation import Observation
from jma_bosai_amedas_producer_data.jp.jma.amedas.station import Station
from jma_bosai_amedas_producer_data.jp.jma.amedas.eventenum import EventEnum
try:
    from jma_bosai_amedas_producer_kafka_producer.producer import JPJMAAmedasEventProducer
except ModuleNotFoundError:
    # The generated Kafka producer package is only installed in the Kafka
    # image. The MQTT/AMQP images reuse this module for the shared
    # build_*/fetch helpers and the generated data classes, so the Kafka
    # producer is an optional dependency there. Only the Kafka bridge
    # references it, and that class never runs in those images.
    JPJMAAmedasEventProducer = None

BASE_URL = "https://www.jma.go.jp/bosai/amedas"
LATEST_TIME_URL = f"{BASE_URL}/data/latest_time.txt"
STATION_TABLE_URL = f"{BASE_URL}/const/amedastable.json"
DEFAULT_TOPIC = "jma-bosai-amedas"
DEFAULT_STATE_FILE = "./state/jma-bosai-amedas.json"
DEFAULT_POINT_REQUEST_DELAY_SECONDS = 0.25
MEASUREMENT_CAPABILITIES = [
    "precipitation", "wind", "temperature", "sunshine_duration",
    "snow_depth", "humidity", "pressure", "visibility",
]
PREFECTURE_BY_PREFIX = {"01":"hokkaido","02":"aomori","03":"iwate","04":"miyagi","05":"akita","06":"yamagata","07":"fukushima","08":"ibaraki","09":"tochigi","10":"gunma","11":"saitama","12":"chiba","13":"tokyo","14":"kanagawa","15":"niigata","16":"toyama","17":"ishikawa","18":"fukui","19":"yamanashi","20":"nagano","21":"gifu","22":"shizuoka","23":"aichi","24":"mie","25":"shiga","26":"kyoto","27":"osaka","28":"hyogo","29":"nara","30":"wakayama","31":"tottori","32":"shimane","33":"okayama","34":"hiroshima","35":"yamaguchi","36":"tokushima","37":"kagawa","38":"ehime","39":"kochi","40":"fukuoka","41":"saga","42":"nagasaki","43":"kumamoto","44":"oita","45":"miyazaki","46":"kagoshima","47":"okinawa"}

def prefecture_for_station(station_code: str) -> str:
    return PREFECTURE_BY_PREFIX.get(str(station_code)[:2], "unknown")

MEASUREMENT_FIELDS = [
    "temp", "humidity", "pressure", "normal_pressure", "wind_speed", "wind_direction",
    "precipitation10m", "precipitation1h", "precipitation3h", "precipitation24h",
    "sun10m", "sun1h", "snow", "snow1h", "snow6h", "snow12h", "snow24h",
    "visibility", "cloud", "weather",
]
POINT_DETAIL_FIELDS = [
    "wind_gust", "wind_gust_qc_flag", "wind_gust_direction", "wind_gust_time",
    "max_temp", "max_temp_time", "min_temp", "min_temp_time",
]

logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)

# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-jma-bosai-amedas/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)


def _load_state(state_file: str) -> dict:
    try:
        if state_file and Path(state_file).exists():
            return json.loads(Path(state_file).read_text(encoding="utf-8"))
    except Exception as exc:  # pylint: disable=broad-except
        logging.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    if not state_file:
        return
    try:
        path = Path(state_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as exc:  # pylint: disable=broad-except
        logging.warning("Could not save state to %s: %s", state_file, exc)


def create_retrying_session() -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def decimal_degrees(value: Any) -> Optional[float]:
    if not isinstance(value, list) or len(value) < 2:
        return None
    degrees = float(value[0])
    minutes = float(value[1])
    sign = -1 if degrees < 0 else 1
    return degrees + sign * (minutes / 60.0)


def wind_direction_to_degrees(code: Any) -> Optional[float]:
    if code is None:
        return None
    try:
        return float(code) * 22.5
    except (TypeError, ValueError):
        return None


def point_file_time(observed_at_local: datetime) -> datetime:
    if observed_at_local.minute == 0 and observed_at_local.second == 0:
        return observed_at_local - timedelta(hours=1)
    return observed_at_local


def point_detail_time_to_utc(observed_at_local: datetime, payload: Any) -> Optional[str]:
    if not isinstance(payload, dict):
        return None
    try:
        candidate = observed_at_local.replace(
            hour=int(payload["hour"]),
            minute=int(payload["minute"]),
            second=0,
            microsecond=0,
        )
    except (KeyError, TypeError, ValueError):
        return None
    if candidate > observed_at_local:
        candidate -= timedelta(days=1)
    return candidate.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_point_station_codes(value: Optional[str]) -> set[str]:
    if not value:
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def enabled_measurements(elems_bitmask: str) -> list[str]:
    result: list[str] = []
    for idx, marker in enumerate(elems_bitmask or ""):
        if idx < len(MEASUREMENT_CAPABILITIES) and marker != "0":
            result.append(MEASUREMENT_CAPABILITIES[idx])
    return result


def _tuple_value(payload: dict, key: str) -> tuple[Any, Any]:
    item = payload.get(key)
    if not isinstance(item, list) or not item:
        return None, None
    value = item[0]
    qc = item[-1] if len(item) > 1 else None
    return value, qc


def _measurement_kwargs() -> dict[str, Any]:
    values: dict[str, Any] = {}
    for field in MEASUREMENT_FIELDS:
        values[field] = None
        values[f"{field}_qc_flag"] = None
    for field in POINT_DETAIL_FIELDS:
        values[field] = None
    return values


def parse_station(station_code: str, payload: dict[str, Any]) -> Station:
    return Station(
        prefecture=prefecture_for_station(station_code),
        event=EventEnum("info"),
        station_code=station_code,
        kj_name=payload.get("kjName", ""),
        kana=payload.get("kana") or payload.get("knName", ""),
        en_name=payload.get("enName", ""),
        latitude=decimal_degrees(payload.get("lat")) or 0.0,
        longitude=decimal_degrees(payload.get("lon")) or 0.0,
        altitude_m=float(payload.get("alt") or 0.0),
        station_type=payload.get("type", ""),
        elems_bitmask=payload.get("elems", ""),
        enabled_measurements=enabled_measurements(payload.get("elems", "")),
    )


def parse_observation(station_code: str, payload: dict[str, Any], observed_at_local: datetime) -> Optional[Observation]:
    if not payload:
        return None
    values = _measurement_kwargs()
    direct_keys = [
        "temp", "humidity", "pressure", "precipitation10m", "precipitation1h",
        "precipitation3h", "precipitation24h", "sun10m", "sun1h", "snow", "snow1h",
        "snow6h", "snow12h", "snow24h", "visibility", "cloud", "weather",
    ]
    for key in direct_keys:
        value, qc = _tuple_value(payload, key)
        values[key] = value
        values[f"{key}_qc_flag"] = qc
    value, qc = _tuple_value(payload, "normalPressure")
    values["normal_pressure"] = value
    values["normal_pressure_qc_flag"] = qc
    wind = payload.get("wind")
    if isinstance(wind, list) and len(wind) >= 3:
        values["wind_speed"] = wind[0]
        values["wind_direction"] = wind_direction_to_degrees(wind[1])
        values["wind_speed_qc_flag"] = wind[2]
        values["wind_direction_qc_flag"] = wind[2]
    else:
        value, qc = _tuple_value(payload, "wind")
        values["wind_speed"] = value
        values["wind_speed_qc_flag"] = qc
        direction, direction_qc = _tuple_value(payload, "windDirection")
        values["wind_direction"] = wind_direction_to_degrees(direction)
        values["wind_direction_qc_flag"] = direction_qc
    gust, gust_qc = _tuple_value(payload, "gust")
    values["wind_gust"] = gust
    values["wind_gust_qc_flag"] = gust_qc
    gust_direction, _ = _tuple_value(payload, "gustDirection")
    values["wind_gust_direction"] = wind_direction_to_degrees(gust_direction)
    values["wind_gust_time"] = point_detail_time_to_utc(observed_at_local, payload.get("gustTime"))
    max_temp, _ = _tuple_value(payload, "maxTemp")
    values["max_temp"] = max_temp
    values["max_temp_time"] = point_detail_time_to_utc(observed_at_local, payload.get("maxTempTime"))
    min_temp, _ = _tuple_value(payload, "minTemp")
    values["min_temp"] = min_temp
    values["min_temp_time"] = point_detail_time_to_utc(observed_at_local, payload.get("minTempTime"))
    if not any(values[field] is not None for field in MEASUREMENT_FIELDS + POINT_DETAIL_FIELDS):
        return None
    utc = observed_at_local.astimezone(timezone.utc)
    return Observation(
        prefecture=prefecture_for_station(station_code),
        event=EventEnum("observation"),
        station_code=station_code,
        observed_at=datetime.fromisoformat(utc.isoformat().replace("+00:00", "Z")),
        observed_at_local=datetime.fromisoformat(observed_at_local.isoformat()),
        **values,
    )


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.strip().split(";"):
            if not part.strip():
                continue
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"')
            if key == "Endpoint":
                config_dict["bootstrap.servers"] = value.replace("sb://", "").rstrip("/") + ":9093"
            elif key == "EntityPath":
                config_dict["kafka_topic"] = value
            elif key == "SharedAccessKeyName":
                config_dict["sasl.username"] = "$ConnectionString"
            elif key == "SharedAccessKey":
                config_dict["sasl.password"] = connection_string.strip()
            elif key == "BootstrapServer":
                config_dict["bootstrap.servers"] = value
    except ValueError as exc:
        raise ValueError("Invalid connection string format") from exc
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


class JmaBosaiAmedasAPI:
    def __init__(
        self,
        session: Optional[requests.Session] = None,
        point_station_codes: Optional[set[str]] = None,
        point_request_delay: float = DEFAULT_POINT_REQUEST_DELAY_SECONDS,
    ):
        self.session = session or create_retrying_session()
        self.stations: dict[str, Station] = {}
        self.point_station_codes = point_station_codes or set()
        self.point_request_delay = max(0.0, point_request_delay)

    def _get_text(self, url: str) -> Optional[str]:
        try:
            response = self.session.get(url, timeout=20)
            if response.status_code >= 400:
                logging.warning("Request to %s failed with status code %s", url, response.status_code)
                return None
            return response.text.strip()
        except requests.RequestException as exc:
            logging.warning("Request to %s failed: %s", url, exc)
            return None

    def _get_json(self, url: str) -> Optional[dict[str, Any]]:
        text = self._get_text(url)
        if text is None:
            return None
        try:
            parsed = json.loads(text)
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError as exc:
            logging.warning("Malformed JSON from %s: %s", url, exc)
            return None

    def fetch_latest_time(self) -> Optional[datetime]:
        text = self._get_text(LATEST_TIME_URL)
        if not text:
            return None
        try:
            return datetime.fromisoformat(text)
        except ValueError as exc:
            logging.warning("Could not parse latest_time.txt value %r: %s", text, exc)
            return None

    def observation_url(self, observed_at_local: datetime) -> str:
        return f"{BASE_URL}/data/map/{observed_at_local.strftime('%Y%m%d%H%M')}00.json"

    def point_observation_url(self, station_code: str, observed_at_local: datetime) -> str:
        file_time = point_file_time(observed_at_local)
        return f"{BASE_URL}/data/point/{station_code}/{file_time.strftime('%Y%m%d_%H')}.json"

    def fetch_station_table(self) -> Optional[dict[str, Station]]:
        raw = self._get_json(STATION_TABLE_URL)
        if raw is None:
            return None
        stations: dict[str, Station] = {}
        for station_code, payload in raw.items():
            try:
                stations[station_code] = parse_station(station_code, payload)
            except Exception as exc:  # pylint: disable=broad-except
                logging.warning("Skipping station %s after parse error: %s", station_code, exc)
        return stations

    def fetch_observation_map(self, observed_at_local: datetime) -> Optional[dict[str, Any]]:
        return self._get_json(self.observation_url(observed_at_local))

    def fetch_point_observation(self, station_code: str, observed_at_local: datetime) -> Optional[dict[str, Any]]:
        raw = self._get_json(self.point_observation_url(station_code, observed_at_local))
        if raw is None:
            return None
        observed_key = observed_at_local.strftime("%Y%m%d%H%M%S")
        if isinstance(raw.get(observed_key), dict):
            return raw[observed_key]
        candidates = [key for key in raw if key <= observed_key and isinstance(raw.get(key), dict)]
        if not candidates:
            return None
        return raw[max(candidates)]

    def iter_observations(
        self,
        observed_at_local: datetime,
        raw_map: dict[str, Any],
        point_details: Optional[dict[str, dict[str, Any]]] = None,
    ) -> Iterable[Observation]:
        point_details = point_details or {}
        for station_code, payload in raw_map.items():
            try:
                if station_code in point_details:
                    payload = {**payload, **point_details[station_code]}
                observation = parse_observation(station_code, payload, observed_at_local)
                if observation:
                    yield observation
            except Exception as exc:  # pylint: disable=broad-except
                logging.warning("Skipping observation for station %s after parse error: %s", station_code, exc)

    def emit_station_reference(self, event_producer: JPJMAAmedasEventProducer, producer: Producer, state: dict, state_file: str, now: datetime) -> bool:
        refreshed = self.fetch_station_table()
        if refreshed is None:
            logging.warning("Station metadata refresh failed; keeping %d cached stations", len(self.stations))
            return False
        for station_code, station in refreshed.items():
            event_producer.send_jp_jma_amedas_station(
                _feedurl=STATION_TABLE_URL,
                _station_code=station_code,
                data=station,
                flush_producer=False,
            )
        if producer.flush(timeout=60) != 0:
            logging.error("Kafka flush did not complete after station metadata batch; state not advanced")
            return False
        self.stations = refreshed
        state["last_station_metadata_refresh"] = now.isoformat()
        _save_state(state_file, state)
        logging.info("Emitted %d JMA AMeDAS station reference events", len(refreshed))
        return True

    def poll_once(self, event_producer: JPJMAAmedasEventProducer, producer: Producer, state: dict, state_file: str) -> int:
        observed_at = self.fetch_latest_time()
        if observed_at is None:
            return 0
        snapshot = observed_at.isoformat()
        if snapshot == state.get("last_snapshot_time"):
            logging.info("Snapshot %s already emitted; skipping", snapshot)
            return 0
        raw_map = self.fetch_observation_map(observed_at)
        if raw_map is None:
            return 0
        point_details: dict[str, dict[str, Any]] = {}
        if self.point_station_codes:
            selected = set(raw_map) if "*" in self.point_station_codes or "all" in self.point_station_codes else set(raw_map).intersection(self.point_station_codes)
            for index, station_code in enumerate(sorted(selected)):
                if index and self.point_request_delay:
                    time.sleep(self.point_request_delay)
                detail = self.fetch_point_observation(station_code, observed_at)
                if detail:
                    point_details[station_code] = detail
        count = 0
        for observation in self.iter_observations(observed_at, raw_map, point_details):
            event_producer.send_jp_jma_amedas_observation(
                _feedurl=self.observation_url(observed_at),
                _station_code=observation.station_code,
                data=observation,
                flush_producer=False,
            )
            count += 1
        if count and producer.flush(timeout=60) != 0:
            logging.error("Kafka flush did not complete after observation batch; state not advanced")
            return 0
        state["last_snapshot_time"] = snapshot
        _save_state(state_file, state)
        logging.info("Emitted %d JMA AMeDAS observations for snapshot %s", count, snapshot)
        return count

    def feed(self, kafka_config: dict, kafka_topic: str, polling_interval: int, metadata_refresh_hours: int, state_file: str, once: bool = False) -> None:
        state = _load_state(state_file)
        producer: Producer = Producer(kafka_config)
        event_producer = JPJMAAmedasEventProducer(producer, kafka_topic)
        while True:
            start = datetime.now(timezone.utc)
            last_refresh_text = state.get("last_station_metadata_refresh")
            last_refresh = datetime.fromisoformat(last_refresh_text) if last_refresh_text else None
            if not last_refresh or start - last_refresh >= timedelta(hours=metadata_refresh_hours):
                self.emit_station_reference(event_producer, producer, state, state_file, start)
            self.poll_once(event_producer, producer, state, state_file)
            if once:
                break
            elapsed = (datetime.now(timezone.utc) - start).total_seconds()
            time.sleep(max(0, polling_interval - elapsed))
        producer.flush(timeout=60)


def build_kafka_config(args: argparse.Namespace) -> tuple[dict[str, str], str]:
    kafka_topic = args.kafka_topic or DEFAULT_TOPIC
    if args.connection_string:
        config = parse_connection_string(args.connection_string)
        kafka_topic = config.pop("kafka_topic", kafka_topic)
    else:
        config = {"bootstrap.servers": args.kafka_bootstrap_servers or ""}
        if args.sasl_username and args.sasl_password:
            config.update({"sasl.username": args.sasl_username, "sasl.password": args.sasl_password})
    if not config.get("bootstrap.servers"):
        raise ValueError("Kafka bootstrap servers must be provided through CONNECTION_STRING or KAFKA_BOOTSTRAP_SERVERS")
    tls_enabled = args.kafka_enable_tls
    if config.get("sasl.username") and config.get("sasl.password"):
        config["sasl.mechanisms"] = "PLAIN"
        config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
    elif tls_enabled:
        config["security.protocol"] = "SSL"
    return config, kafka_topic


def main() -> None:
    parser = argparse.ArgumentParser(description="Bridge JMA Bosai AMeDAS observations to Kafka-compatible CloudEvents endpoints.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Poll JMA Bosai AMeDAS and send station and observation events")
    feed_parser.add_argument("--kafka-bootstrap-servers", default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic", default=os.getenv("KAFKA_TOPIC", DEFAULT_TOPIC))
    feed_parser.add_argument("--sasl-username", default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument("-c", "--connection-string", default=os.getenv("CONNECTION_STRING"))
    feed_parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "600")))
    feed_parser.add_argument("--station-metadata-refresh-hours", type=int, default=int(os.getenv("STATION_METADATA_REFRESH_HOURS", "168")))
    feed_parser.add_argument("--point-station-codes", default=os.getenv("POINT_STATION_CODES", ""), help="Comma-separated station codes, or 'all', for per-station point-detail enrichment")
    feed_parser.add_argument("--point-request-delay", type=float, default=float(os.getenv("POINT_REQUEST_DELAY", str(DEFAULT_POINT_REQUEST_DELAY_SECONDS))))
    feed_parser.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--kafka-enable-tls", action=argparse.BooleanOptionalAction, default=os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no"))
    args = parser.parse_args()
    if args.command == "feed":
        try:
            kafka_config, kafka_topic = build_kafka_config(args)
        except ValueError as exc:
            print(f"Error: {exc}")
            sys.exit(1)
        JmaBosaiAmedasAPI(
            point_station_codes=parse_point_station_codes(args.point_station_codes),
            point_request_delay=args.point_request_delay,
        ).feed(kafka_config, kafka_topic, args.polling_interval, args.station_metadata_refresh_hours, args.state_file, args.once)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
