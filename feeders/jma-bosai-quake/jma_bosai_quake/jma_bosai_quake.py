"""Bridge JMA Bosai earthquake reports to Kafka as CloudEvents."""

from __future__ import annotations

import argparse
from collections import deque
from datetime import datetime, timedelta, timezone
import json
import logging
import os
from pathlib import Path
import re
import sys
import time
from typing import Any, Deque, Dict, Iterable, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from confluent_kafka import Producer
from jma_bosai_quake_producer_data import (
    AffectedCity,
    AffectedPrefecture,
    BulletinTypeenum,
    EarthquakeReport,
    InfoTypeenum,
    MaxIntensityenum,
)
from jma_bosai_quake_producer_kafka_producer.producer import JPJMAQuakeEventProducer

LIST_URL = "https://www.jma.go.jp/bosai/quake/data/list.json"
DETAIL_BASE_URL = "https://www.jma.go.jp/bosai/quake/data/"
DEFAULT_TOPIC = "jma-bosai-quake"
DEFAULT_STATE_FILE = ".\\state\\jma-bosai-quake.json"
STATE_LIMIT = 1000
SUPPORTED_BULLETIN_TYPES = {"VXSE51", "VXSE52", "VXSE53", "VXSE5k", "VXSE61", "VYSE52"}
_JST = timezone(timedelta(hours=9))

logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)

_ISO6709_RE = re.compile(r"^([+-]\d+(?:\.\d+)?)([+-]\d+(?:\.\d+)?)([+-]\d+(?:\.\d+)?)/$")
_INFO_TYPE_MAP = {"発表": "ISSUED", "訂正": "CORRECTED", "取消": "CANCELLED"}
_NO_TSUNAMI_MARKERS = (
    "津波の心配はありません",
    "津波の心配なし",
    "no tsunami risk",
    "no concern of tsunami",
    "does not pose a tsunami",
)
_TSUNAMI_MARKERS = ("津波", "tsunami")
_MAX_INTENSITY_MAP = {
    "1": MaxIntensityenum.INTENSITY_1,
    "2": MaxIntensityenum.INTENSITY_2,
    "3": MaxIntensityenum.INTENSITY_3,
    "4": MaxIntensityenum.INTENSITY_4,
    "5-": MaxIntensityenum.INTENSITY_5_MINUS,
    "5+": MaxIntensityenum.INTENSITY_5_PLUS,
    "6-": MaxIntensityenum.INTENSITY_6_MINUS,
    "6+": MaxIntensityenum.INTENSITY_6_PLUS,
    "7": MaxIntensityenum.INTENSITY_7,
}
_PREFECTURE_BY_CODE = {
    "01": "hokkaido", "02": "aomori", "03": "iwate", "04": "miyagi", "05": "akita", "06": "yamagata", "07": "fukushima",
    "08": "ibaraki", "09": "tochigi", "10": "gunma", "11": "saitama", "12": "chiba", "13": "tokyo", "14": "kanagawa",
    "15": "niigata", "16": "toyama", "17": "ishikawa", "18": "fukui", "19": "yamanashi", "20": "nagano", "21": "gifu",
    "22": "shizuoka", "23": "aichi", "24": "mie", "25": "shiga", "26": "kyoto", "27": "osaka", "28": "hyogo",
    "29": "nara", "30": "wakayama", "31": "tottori", "32": "shimane", "33": "okayama", "34": "hiroshima", "35": "yamaguchi",
    "36": "tokushima", "37": "kagawa", "38": "ehime", "39": "kochi", "40": "fukuoka", "41": "saga", "42": "nagasaki",
    "43": "kumamoto", "44": "oita", "45": "miyazaki", "46": "kagoshima", "47": "okinawa",
}
_PREFECTURE_NAMES = set(_PREFECTURE_BY_CODE.values())


def create_retry_session() -> requests.Session:
    """Create a requests session with bounded retries for public HTTP polling."""
    session = requests.Session()
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def parse_iso6709_location(value: str | None) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """Parse JMA ISO 6709 coordinate strings into latitude, longitude, and depth km."""
    if not value:
        return None, None, None
    match = _ISO6709_RE.match(value.strip())
    if not match:
        raise ValueError(f"Invalid JMA ISO 6709 coordinate: {value}")
    latitude = float(match.group(1))
    longitude = float(match.group(2))
    depth_km = abs(float(match.group(3))) / 1000.0
    return latitude, longitude, depth_km


def to_utc_rfc3339(value: str) -> str:
    """Convert an offset timestamp from the JMA feed to RFC3339 UTC."""
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds")


def parse_control_datetime(value: str) -> Tuple[str, str]:
    """Convert compact JMA ctt control timestamp from JST to UTC and local RFC3339 strings."""
    dt = datetime.strptime(value, "%Y%m%d%H%M%S").replace(tzinfo=_JST)
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds"), dt.isoformat(timespec="seconds")


def map_info_type(value: str) -> str:
    """Map Japanese JMA information type labels to the xreg enum."""
    try:
        return _INFO_TYPE_MAP[value]
    except KeyError as exc:
        raise ValueError(f"Unsupported JMA information type: {value}") from exc


def map_max_intensity(value: Any) -> Optional[MaxIntensityenum]:
    if value in (None, ""):
        return None
    try:
        return _MAX_INTENSITY_MAP[str(value)]
    except KeyError as exc:
        raise ValueError(f"Unsupported JMA max intensity: {value}") from exc


def bulletin_type_from_filename(filename: str | None) -> str:
    if not filename:
        return ""
    parts = filename.split("_")
    return parts[2] if len(parts) >= 3 else ""


def parse_optional_float(value: Any) -> Optional[float]:
    if value in (None, "", "NaN", "不明"):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_optional_string(value: Any) -> Optional[str]:
    if value in (None, ""):
        return None
    return str(value)


def _topic_segment(value: str | None) -> str:
    text = (value or "unknown").strip().lower() or "unknown"
    text = re.sub(r"[^a-z0-9-]+", "-", text)
    return text.strip("-") or "unknown"


def prefecture_slug(epicenter_area_en: str | None, affected_prefectures: List[AffectedPrefecture]) -> str:
    words = re.findall(r"[A-Za-z]+", epicenter_area_en or "")
    lowered = [word.lower() for word in words]
    for name in _PREFECTURE_NAMES:
        if name in lowered:
            return name
    if affected_prefectures:
        return _PREFECTURE_BY_CODE.get(affected_prefectures[0].code[:2], "unknown")
    return "unknown"


def magnitude_bucket(magnitude: Optional[float]) -> str:
    if magnitude is None:
        return "mx"
    bucket = int(magnitude)
    if bucket < 0:
        return "mx"
    return f"m{min(bucket, 9)}"


def extract_tsunami_possible(detail: Optional[Dict[str, Any]]) -> Optional[bool]:
    """Extract a conservative tsunami possibility flag from detail bulletin comments."""
    if not detail:
        return None

    texts: List[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key.lower() in ("text", "entext") and isinstance(value, str):
                    texts.append(value)
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(detail.get("Body", {}).get("Comments", {}))
    combined = "\n".join(texts).lower()
    if not combined:
        return None
    if any(marker.lower() in combined for marker in _NO_TSUNAMI_MARKERS):
        return False
    if any(marker.lower() in combined for marker in _TSUNAMI_MARKERS):
        return True
    return None


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    config: Dict[str, str] = {}
    for part in connection_string.split(";"):
        if not part or "=" not in part:
            continue
        key, value = part.split("=", 1)
        value = value.strip('"').strip()
        if key == "Endpoint":
            config["bootstrap.servers"] = value.replace("sb://", "").rstrip("/") + ":9093"
        elif key == "EntityPath":
            config["kafka_topic"] = value
        elif key == "SharedAccessKeyName":
            config["sasl.username"] = "$ConnectionString"
        elif key == "SharedAccessKey":
            config["sasl.password"] = connection_string.strip()
        elif key == "BootstrapServer":
            config["bootstrap.servers"] = value
    if "sasl.username" in config:
        config["security.protocol"] = "SASL_SSL"
        config["sasl.mechanisms"] = "PLAIN"
    return config


def _load_state(state_file: str) -> Deque[Tuple[str, int]]:
    if not state_file or not Path(state_file).exists():
        return deque(maxlen=STATE_LIMIT)
    try:
        data = json.loads(Path(state_file).read_text(encoding="utf-8"))
        items = data.get("seen", []) if isinstance(data, dict) else []
        parsed = deque(maxlen=STATE_LIMIT)
        for item in items[-STATE_LIMIT:]:
            if isinstance(item, dict):
                parsed.append((str(item["event_id"]), int(item["serial"])))
            elif isinstance(item, list) and len(item) == 2:
                parsed.append((str(item[0]), int(item[1])))
        return parsed
    except Exception as exc:  # pylint: disable=broad-except
        logging.warning("Could not load state from %s: %s", state_file, exc)
        return deque(maxlen=STATE_LIMIT)


def _save_state(state_file: str, seen: Iterable[Tuple[str, int]]) -> None:
    if not state_file:
        return
    path = Path(state_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"seen": [{"event_id": event_id, "serial": serial} for event_id, serial in seen]}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


class JmaBosaiQuakeAPI:
    def __init__(self, state_file: str = DEFAULT_STATE_FILE, session: Optional[requests.Session] = None):
        self.session = session or create_retry_session()
        self.state_file = state_file
        self.seen_order: Deque[Tuple[str, int]] = _load_state(state_file)
        self.seen = set(self.seen_order)

    def list_reports(self) -> List[Dict[str, Any]]:
        response = self.session.get(LIST_URL, timeout=20)
        response.raise_for_status()
        return response.json()

    def fetch_detail(self, filename: str) -> Optional[Dict[str, Any]]:
        if not filename:
            return None
        response = self.session.get(DETAIL_BASE_URL + filename, timeout=20)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def normalize_report(self, entry: Dict[str, Any], detail: Optional[Dict[str, Any]] = None) -> EarthquakeReport:
        latitude, longitude, depth_km = parse_iso6709_location(entry.get("cod"))
        serial = int(entry.get("ser", 0))
        event_id = str(entry["eid"])
        detail_filename = entry.get("json", "")
        control_datetime, control_datetime_local = parse_control_datetime(str(entry["ctt"]))
        affected_prefectures: List[AffectedPrefecture] = []
        affected_cities: List[AffectedCity] = []
        for pref in entry.get("int") or []:
            pref_code = str(pref.get("code", ""))
            if pref_code and pref.get("maxi"):
                affected_prefectures.append(AffectedPrefecture(code=pref_code, max_intensity=map_max_intensity(pref.get("maxi"))))
            for city in pref.get("city") or []:
                if city.get("code") and city.get("maxi"):
                    affected_cities.append(
                        AffectedCity(
                            prefecture_code=pref_code,
                            city_code=str(city.get("code")),
                            max_intensity=map_max_intensity(city.get("maxi")),
                        )
                    )

        magnitude = parse_optional_float(entry.get("mag"))
        epicenter_area_en = parse_optional_string(entry.get("en_anm"))
        return EarthquakeReport(
            prefecture=prefecture_slug(epicenter_area_en, affected_prefectures),
            magnitude_bucket=magnitude_bucket(magnitude),
            event_id=event_id,
            report_id=f"{event_id}_{serial}",
            serial=serial,
            info_type=InfoTypeenum(map_info_type(str(entry.get("ift", "")))),
            report_datetime=to_utc_rfc3339(str(entry["rdt"])),
            report_datetime_local=str(entry["rdt"]),
            control_datetime=control_datetime,
            control_datetime_local=control_datetime_local,
            origin_datetime=to_utc_rfc3339(str(entry["at"])),
            origin_datetime_local=str(entry["at"]),
            title_jp=str(entry.get("ttl", "")),
            title_en=parse_optional_string(entry.get("en_ttl")),
            epicenter_area_code=parse_optional_string(entry.get("acd")),
            epicenter_area_jp=parse_optional_string(entry.get("anm")),
            epicenter_area_en=epicenter_area_en,
            latitude=latitude,
            longitude=longitude,
            depth_km=depth_km,
            magnitude=magnitude,
            max_intensity=map_max_intensity(entry.get("maxi")),
            bulletin_type=BulletinTypeenum(bulletin_type_from_filename(detail_filename)),
            detail_url=DETAIL_BASE_URL + detail_filename,
            affected_prefectures=affected_prefectures,
            affected_cities=affected_cities,
            tsunami_possible=extract_tsunami_possible(detail),
        )

    @staticmethod
    def state_key(entry: Dict[str, Any]) -> Tuple[str, int]:
        return str(entry["eid"]), int(entry.get("ser", 0))

    def mark_seen(self, keys: Iterable[Tuple[str, int]]) -> None:
        for key in keys:
            if key in self.seen:
                continue
            self.seen.add(key)
            self.seen_order.append(key)
        self.seen = set(self.seen_order)
        _save_state(self.state_file, self.seen_order)

    def poll_once(self, event_producer: Any, kafka_producer: Any, flush_timeout: float = 30.0) -> int:
        reports = self.list_reports()
        pending_keys: List[Tuple[str, int]] = []
        emitted = 0
        for entry in reversed(reports):
            bulletin_type = bulletin_type_from_filename(entry.get("json"))
            if bulletin_type not in SUPPORTED_BULLETIN_TYPES:
                logging.warning("Skipping unsupported JMA earthquake bulletin type %s from %s", bulletin_type or "<missing>", entry.get("json"))
                continue
            key = self.state_key(entry)
            if key in self.seen:
                continue
            detail = None
            try:
                detail = self.fetch_detail(entry.get("json", ""))
            except requests.RequestException as exc:
                logging.warning("Detail fetch failed for %s: %s", entry.get("json"), exc)
            try:
                data = self.normalize_report(entry, detail)
                event_producer.send_jp_jma_quake_earthquake_report(
                    _feedurl=LIST_URL,
                    _event_id=data.event_id,
                    _serial=str(data.serial),
                    data=data,
                    flush_producer=False,
                )
                pending_keys.append(key)
                emitted += 1
            except Exception as exc:  # pylint: disable=broad-except
                logging.error("Skipping malformed earthquake report %s: %s", entry.get("eid"), exc)
        if pending_keys:
            remainder = kafka_producer.flush(timeout=flush_timeout)
            if remainder:
                raise RuntimeError(f"Kafka producer still has {remainder} queued messages after flush")
            self.mark_seen(pending_keys)
        return emitted

    def feed(self, kafka_config: Dict[str, Any], kafka_topic: str, polling_interval: int, once: bool = False) -> None:
        producer = Producer(kafka_config)
        event_producer = JPJMAQuakeEventProducer(producer, kafka_topic)
        logging.info("Starting JMA Bosai earthquake feed to topic %s at %s", kafka_topic, kafka_config.get("bootstrap.servers"))
        while True:
            start = time.monotonic()
            try:
                count = self.poll_once(event_producer, producer)
                logging.info("Sent %d new JMA earthquake reports", count)
                if once:
                    break
                sleep_for = max(0.0, polling_interval - (time.monotonic() - start))
                time.sleep(sleep_for)
            except KeyboardInterrupt:
                logging.info("Exiting...")
                break
            except Exception as exc:  # pylint: disable=broad-except
                logging.error("Polling cycle failed: %s", exc)
                if once:
                    raise
                time.sleep(polling_interval)
        producer.flush()


def build_kafka_config(args: argparse.Namespace) -> Tuple[Dict[str, Any], str]:
    if args.connection_string:
        parsed = parse_connection_string(args.connection_string)
        bootstrap_servers = parsed.get("bootstrap.servers")
        kafka_topic = parsed.get("kafka_topic") or args.kafka_topic or DEFAULT_TOPIC
        sasl_username = parsed.get("sasl.username")
        sasl_password = parsed.get("sasl.password")
    else:
        bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic or DEFAULT_TOPIC
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not bootstrap_servers:
        raise ValueError("Kafka bootstrap servers must be provided via command line or CONNECTION_STRING")

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config: Dict[str, Any] = {"bootstrap.servers": bootstrap_servers}
    if sasl_username and sasl_password:
        kafka_config.update(
            {
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_username,
                "sasl.password": sasl_password,
            }
        )
    elif tls_enabled:
        kafka_config["security.protocol"] = "SSL"
    return kafka_config, kafka_topic


def main() -> None:
    parser = argparse.ArgumentParser(description="Bridge JMA Bosai earthquake reports to Kafka as CloudEvents.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Poll JMA Bosai earthquake reports and send new reports to Kafka")
    feed_parser.add_argument("--kafka-bootstrap-servers", default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic", default=os.getenv("KAFKA_TOPIC", DEFAULT_TOPIC))
    feed_parser.add_argument("--sasl-username", default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument("-c", "--connection-string", default=os.getenv("CONNECTION_STRING"))
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "60")))
    feed_parser.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE))
    feed_parser.add_argument(
        "--once",
        action="store_true",
        default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
        help="Exit after one polling cycle.",
    )
    args = parser.parse_args()

    if args.command == "feed":
        try:
            kafka_config, kafka_topic = build_kafka_config(args)
            JmaBosaiQuakeAPI(state_file=args.state_file).feed(kafka_config, kafka_topic, args.polling_interval, args.once)
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
