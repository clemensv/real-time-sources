"""JMA Bosai weather warnings and tsunami alert bridge."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import time
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from confluent_kafka import Producer
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .office_codes import WARNING_OFFICE_CODES, WARNING_OFFICES

LOGGER = logging.getLogger(__name__)
AREA_CATALOG_URL = "https://www.jma.go.jp/bosai/common/const/area.json"
WARNING_URL_TEMPLATE = "https://www.jma.go.jp/bosai/warning/data/warning/{office_code}.json"
TSUNAMI_LIST_URL = "https://www.jma.go.jp/bosai/tsunami/data/list.json"
TSUNAMI_DETAIL_BASE = "https://www.jma.go.jp/bosai/tsunami/data/"
STATE_CAP = 5000
OFFICE_AREA_CODE = None

WARNING_CODE_DESCRIPTIONS: dict[str, tuple[str, str]] = {
    "03": ("大雨", "Heavy rain"), "04": ("洪水", "Flood"), "05": ("暴風", "Storm"),
    "06": ("暴風雪", "Snow storm"), "07": ("大雪", "Heavy snow"), "08": ("波浪", "High waves"),
    "10": ("雷", "Thunderstorm"), "12": ("強風", "Strong wind"), "13": ("風雪", "Snow and wind"),
    "14": ("濃霧", "Dense fog"), "15": ("乾燥", "Dry air"), "16": ("なだれ", "Avalanche"),
    "17": ("着氷", "Ice accretion"), "18": ("着雪", "Snow accretion"), "19": ("融雪", "Snow melt"),
    "20": ("高潮", "Storm surge"), "21": ("低温", "Low temperature"), "22": ("霜", "Frost"),
    "23": ("着氷・着雪", "Ice and snow accretion"), "24": ("大雨・洪水", "Heavy rain and flood"),
    "25": ("大雨・強風", "Heavy rain and strong wind"), "32": ("大雨特別警報", "Emergency heavy rain warning"),
    "33": ("大雪特別警報", "Emergency heavy snow warning"), "35": ("暴風特別警報", "Emergency storm warning"),
    "36": ("暴風雪特別警報", "Emergency snow storm warning"), "37": ("波浪特別警報", "Emergency high wave warning"),
    "38": ("高潮特別警報", "Emergency storm surge warning"), "W": ("注意報・警報", "Advisory or warning aggregate"),
}
SPECIAL_WARNING_CODES = {"32", "33", "35", "36", "37", "38"}
INFO_TYPE_MAP = {"発表": "ISSUED", "訂正": "CORRECTED", "取消": "CANCELLED", "キャンセル": "CANCELLED"}
WARNING_STATUS_MAP = {"発表": "ISSUED", "継続": "CONTINUED", "解除": "CANCELLED", "発表警報・注意報はなし": "NO_WARNINGS_OR_ADVISORIES", "警報": "WARNING", "注意報": "ADVISORY", "特別警報": "EMERGENCY_WARNING"}
TITLE_EN_MAP = {"津波警報・注意報・予報": "Tsunami warnings, advisories and forecasts", "津波情報": "Tsunami information"}
PREFECTURE_BY_PREFIX = {
    "01": "hokkaido", "02": "aomori", "03": "iwate", "04": "miyagi", "05": "akita", "06": "yamagata", "07": "fukushima",
    "08": "ibaraki", "09": "tochigi", "10": "gunma", "11": "saitama", "12": "chiba", "13": "tokyo", "14": "kanagawa",
    "15": "niigata", "16": "toyama", "17": "ishikawa", "18": "fukui", "19": "yamanashi", "20": "nagano", "21": "gifu",
    "22": "shizuoka", "23": "aichi", "24": "mie", "25": "shiga", "26": "kyoto", "27": "osaka", "28": "hyogo",
    "29": "nara", "30": "wakayama", "31": "tottori", "32": "shimane", "33": "okayama", "34": "hiroshima", "35": "yamaguchi",
    "36": "tokushima", "37": "kagawa", "38": "ehime", "39": "kochi", "40": "fukuoka", "41": "saga", "42": "nagasaki",
    "43": "kumamoto", "44": "oita", "45": "miyazaki", "46": "kagoshima", "47": "okinawa",
}
SEVERITY_RANK = {"NONE": 0, "ADVISORY": 1, "WARNING": 2, "EMERGENCY_WARNING": 3}


def make_retrying_session() -> requests.Session:
    retry = Retry(total=3, connect=3, read=3, status=3, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=("GET",))
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def parse_connection_string(connection_string: str) -> dict[str, str]:
    config: dict[str, str] = {}
    for part in filter(None, (p.strip() for p in connection_string.split(";"))):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        value = value.strip('\" ')
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
        config["sasl.mechanism"] = "PLAIN"
    return config


def jst_to_utc(value: str | None) -> str | None:
    if not value:
        return None
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def status_to_severity(status: str | None, code: str | None = None) -> str:
    status = status or ""
    if status in {"発表警報・注意報はなし", "NO_WARNINGS_OR_ADVISORIES"}:
        return "NONE"
    if code in SPECIAL_WARNING_CODES or "特別警報" in status:
        return "EMERGENCY_WARNING"
    if "注意報" in status:
        return "ADVISORY"
    return "WARNING"


def _topic_segment(value: str | None) -> str:
    text = (value or "unknown").strip().lower() or "unknown"
    text = re.sub(r"[^a-z0-9-]+", "-", text)
    return text.strip("-") or "unknown"


def prefecture_for_office(office_code: str, name_en: str | None = None) -> str:
    return PREFECTURE_BY_PREFIX.get(str(office_code)[:2]) or _topic_segment(name_en)


def warning_record_severity(warnings: list[dict[str, Any]]) -> str:
    if not warnings:
        return "NONE"
    return max((str(item.get("severity") or "NONE") for item in warnings), key=lambda value: SEVERITY_RANK.get(value, 0))


def _load_state(path: str) -> dict[str, Any]:
    try:
        if path and Path(path).exists():
            return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        LOGGER.warning("Could not load state file %s: %s", path, exc)
    return {}


def _save_state(path: str, state: dict[str, Any]) -> None:
    if not path:
        return
    try:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as exc:
        LOGGER.warning("Could not save state file %s: %s", path, exc)


def _cap_list(items: list[str], cap: int = STATE_CAP) -> list[str]:
    return items[-cap:]


@dataclass
class BridgeState:
    seen_weather: list[str] = field(default_factory=list)
    seen_tsunami: list[str] = field(default_factory=list)
    last_metadata_refresh: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BridgeState":
        return cls(list(data.get("seen_weather", []))[-STATE_CAP:], list(data.get("seen_tsunami", []))[-STATE_CAP:], data.get("last_metadata_refresh"))

    def as_dict(self) -> dict[str, Any]:
        return {"seen_weather": _cap_list(self.seen_weather), "seen_tsunami": _cap_list(self.seen_tsunami), "last_metadata_refresh": self.last_metadata_refresh}


def _extract_area_names(area_catalog: dict[str, Any]) -> dict[str, str]:
    names: dict[str, str] = {}
    for section in ("offices", "class10s", "class15s", "class20s", "centers"):
        for code, record in area_catalog.get(section, {}).items():
            names[code] = record.get("name") or record.get("enName") or code
    return names


def _iter_warning_area_blocks(time_series_item: dict[str, Any]) -> Iterable[dict[str, Any]]:
    if isinstance(time_series_item.get("areas"), list):
        yield from time_series_item["areas"]
    for area_type in time_series_item.get("areaTypes", []) or []:
        yield from area_type.get("areas", []) or []


def parse_weather_warning_payload(office_code: str, payload: dict[str, Any], area_names: dict[str, str] | None = None) -> list[dict[str, Any]]:
    area_names = area_names or {}
    local_report = payload.get("reportDatetime") or payload.get("reportDateTime")
    records: list[dict[str, Any]] = []
    for series in payload.get("timeSeries", []) or []:
        time_defines = [jst_to_utc(t) or t for t in series.get("timeDefines", [])]
        for area in _iter_warning_area_blocks(series):
            area_code = str(area.get("code") or "")
            if not area_code:
                continue
            warnings = []
            for item in area.get("warnings", []) or []:
                raw_code = item.get("code")
                code = str(raw_code) if raw_code not in (None, "") else None
                status = item.get("status") or item.get("condition") or item.get("displayStatus")
                if not status:
                    status = "特別警報" if code in SPECIAL_WARNING_CODES else "継続"
                status_text = str(status)
                if code is None and status_text == "発表警報・注意報はなし":
                    jp, en = "発表警報・注意報はなし", "No warnings or advisories"
                else:
                    jp, en = WARNING_CODE_DESCRIPTIONS.get(code or "", (code or "", code or ""))
                warnings.append({"code": code, "code_description_jp": jp, "code_description_en": en, "status": WARNING_STATUS_MAP.get(status_text, "CONTINUED"), "severity": status_to_severity(status_text, code)})
            records.append({
                "prefecture": prefecture_for_office(office_code), "severity": warning_record_severity(warnings), "event": "warning",
                "office_code": office_code, "area_code": area_code, "area_name": area.get("name") or area_names.get(area_code, area_code),
                "report_datetime": jst_to_utc(local_report) or "1970-01-01T00:00:00Z", "report_datetime_local": local_report or "1970-01-01T00:00:00+09:00",
                "headline_text": payload.get("headlineText"), "warnings": warnings, "time_defines": time_defines,
            })
    return records


def _info_type(value: str | None) -> str:
    return INFO_TYPE_MAP.get(value or "", "ISSUED")


def _serial(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 1


def _bulletin_type(filename: str) -> str:
    match = re.search(r"(VTSE\d{2})", filename or "", re.IGNORECASE)
    return match.group(1).upper() if match else Path(filename or "").stem.split("_")[0]


def _height_to_m(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"(\d+(?:\.\d+)?)", str(value))
    return float(match.group(1)) if match else None


def _find_first(record: dict[str, Any], names: set[str]) -> Any:
    lowered = {n.lower() for n in names}
    for key, value in record.items():
        if str(key) in names or str(key).lower() in lowered:
            return value
    return None


def _walk_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_dicts(child)


def _tsunami_category(item: dict[str, Any]) -> str:
    text = json.dumps(item, ensure_ascii=False)
    if "大津波警報" in text:
        return "MAJOR_WARNING"
    if "津波警報" in text:
        return "WARNING"
    if "津波注意報" in text:
        return "ADVISORY"
    return "FORECAST"


def parse_tsunami_detail_regions(detail: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not detail:
        return []
    regions: dict[str, dict[str, Any]] = {}
    for item in _walk_dicts(detail):
        area = item.get("Area") if isinstance(item.get("Area"), dict) else item
        code = _find_first(area, {"Code", "code", "areaCode"})
        name = _find_first(area, {"Name", "name", "areaName"})
        if not code or not name:
            continue
        height = _find_first(item, {"MaxHeight", "maxHeight", "Height", "height", "condition"})
        arrival = _find_first(item, {"ArrivalTime", "arrivalTime", "firstHeightArrivalTime", "FirstHeightArrivalTime", "arrival_time"})
        key = str(code)
        candidate = {"code": key, "name": str(name), "category": _tsunami_category(item), "expected_max_wave_height_m": _height_to_m(height), "expected_arrival_datetime": jst_to_utc(str(arrival)) if arrival else None, "expected_arrival_datetime_local": str(arrival) if arrival else None}
        if key not in regions or candidate["expected_max_wave_height_m"] is not None or candidate["expected_arrival_datetime"] is not None:
            regions[key] = candidate
    return list(regions.values())


def _observation_status(item: dict[str, Any], observed_height: float | None, observed_time: Any) -> str:
    text = json.dumps(item, ensure_ascii=False).lower()
    if observed_height is not None or "最大" in text or "max" in text:
        return "MAX_WAVE_OBSERVED"
    if observed_time or "第１波" in text or "first" in text:
        return "FIRST_WAVE_OBSERVED"
    return "ESTIMATED"


def parse_tsunami_observations(detail: dict[str, Any] | None, bulletin_type: str | None = None) -> list[dict[str, Any]]:
    if not detail or bulletin_type not in {"VTSE51", "VTSE52"}:
        return []
    observations: dict[str, dict[str, Any]] = {}
    for item in _walk_dicts(detail):
        station = None
        for key in ("Station", "station", "Point", "point", "ObservationPoint", "observationPoint"):
            if isinstance(item.get(key), dict):
                station = item[key]
                break
        if station is None:
            continue
        name = _find_first(station, {"Name", "name", "stationName", "StationName"})
        if not name:
            continue
        code = _find_first(station, {"Code", "code", "stationCode", "StationCode"})
        height = _find_first(item, {"MaxHeight", "maxHeight", "Height", "height", "observedMaxWaveHeight", "ObservedMaxWaveHeight"})
        observed_time = _find_first(item, {"DateTime", "datetime", "Time", "time", "ArrivalTime", "arrivalTime", "FirstHeightArrivalTime", "MaxHeightArrivalTime", "maxHeightArrivalTime"})
        observed_height = _height_to_m(height)
        record = {"station_code": str(code) if code else None, "station_name_jp": str(name), "station_name_en": None, "observed_max_wave_height_m": observed_height, "observed_at": jst_to_utc(str(observed_time)) if observed_time else None, "observed_at_local": str(observed_time) if observed_time else None, "arrival_status": _observation_status(item, observed_height, observed_time)}
        observations[record["station_code"] or record["station_name_jp"]] = record
    return list(observations.values())


def parse_tsunami_alert(entry: dict[str, Any], detail: dict[str, Any] | None = None) -> dict[str, Any]:
    filename = entry.get("json") or ""
    local_report = entry.get("rdt") or entry.get("reportDatetime")
    event_id = str(entry.get("eid") or (detail or {}).get("Head", {}).get("EventID") or "00000000000000")
    bulletin_type = _bulletin_type(filename)
    return {
        "event_id": event_id, "serial": _serial(entry.get("ser") or entry.get("serial") or (detail or {}).get("Head", {}).get("Serial")), "info_type": _info_type(entry.get("ift") or entry.get("infoType")),
        "report_datetime": jst_to_utc(local_report) or "1970-01-01T00:00:00Z", "report_datetime_local": local_report or "1970-01-01T00:00:00+09:00",
        "title_jp": entry.get("ttl") or "津波情報", "title_en": entry.get("en_ttl") or TITLE_EN_MAP.get(entry.get("ttl"), "Tsunami alert"),
        "bulletin_type": bulletin_type, "detail_url": TSUNAMI_DETAIL_BASE + filename if filename and not filename.startswith("http") else filename,
        "affected_coastal_regions": parse_tsunami_detail_regions(detail), "observations": parse_tsunami_observations(detail, bulletin_type),
    }


def _construct_data(class_obj: Any, payload: dict[str, Any]) -> Any:
    return class_obj(**payload)


def _call_send(producer: Any, candidates: tuple[str, ...], **kwargs: Any) -> None:
    for name in candidates:
        method = getattr(producer, name, None)
        if method:
            method(**kwargs)
            return
    available = ", ".join(name for name in dir(producer) if name.startswith("send_"))
    raise AttributeError(f"None of {candidates!r} found on producer; available send methods: {available}")


class JmaBosaiWarningAPI:
    def __init__(self, session: requests.Session | None = None):
        self.session = session or make_retrying_session()
        self.area_catalog: dict[str, Any] = {}
        self.area_names: dict[str, str] = {}

    def fetch_area_catalog(self) -> dict[str, Any]:
        response = self.session.get(AREA_CATALOG_URL, timeout=20)
        response.raise_for_status()
        return response.json()

    def refresh_area_catalog(self) -> bool:
        try:
            catalog = self.fetch_area_catalog()
            self.area_catalog = catalog
            self.area_names = _extract_area_names(catalog)
            return True
        except Exception as exc:
            LOGGER.warning("Area catalog refresh failed; keeping cached catalog if present: %s", exc)
            if not self.area_catalog:
                self.area_catalog = {"offices": {o["code"]: {"name": o["name_jp"], "enName": o["name_en"], "parent": o["parent_office_code"]} for o in WARNING_OFFICES}}
                self.area_names = {o["code"]: o["name_jp"] for o in WARNING_OFFICES}
            return False

    def office_records(self) -> list[dict[str, Any]]:
        offices = self.area_catalog.get("offices") if self.area_catalog else None
        if offices:
            return [{"prefecture": prefecture_for_office(code, item.get("enName")), "severity": "REFERENCE", "event": "office", "office_code": code, "area_code": code, "name_jp": item.get("name", code), "name_en": item.get("enName", code), "parent_office_code": item.get("parent"), "office_type": "PREFECTURE" if code.endswith("0000") and not code.startswith("01") else "SUBREGION"} for code, item in offices.items()]
        return [{**o, "prefecture": prefecture_for_office(o["code"], o.get("name_en")), "severity": "REFERENCE", "event": "office", "area_code": o["code"]} for o in WARNING_OFFICES]

    def fetch_warning_payload(self, office_code: str) -> dict[str, Any]:
        response = self.session.get(WARNING_URL_TEMPLATE.format(office_code=office_code), timeout=20)
        response.raise_for_status()
        return response.json()

    def fetch_tsunami_list(self) -> list[dict[str, Any]]:
        response = self.session.get(TSUNAMI_LIST_URL, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, list) else []

    def fetch_tsunami_detail(self, filename: str) -> dict[str, Any] | None:
        if not filename:
            return None
        response = self.session.get(filename if filename.startswith("http") else TSUNAMI_DETAIL_BASE + filename, timeout=20)
        response.raise_for_status()
        return response.json()

    def emit_offices(self, warning_producer: Any, office_class: Any, kafka_producer: Any) -> int:
        count = 0
        for record in self.office_records():
            _call_send(warning_producer, ("send_jp_jma_warning_office", "send_office"), _feedurl=AREA_CATALOG_URL, _office_code=record["office_code"], _area_code=record["area_code"], data=_construct_data(office_class, record), flush_producer=False)
            count += 1
            if count % 100 == 0:
                kafka_producer.poll(0)
                if kafka_producer.flush(timeout=120) != 0:
                    raise RuntimeError("Kafka flush failed while emitting office reference records")
        if kafka_producer.flush(timeout=120) != 0:
            raise RuntimeError("Kafka flush failed while emitting office reference records")
        return count

    def emit_warning_cycle(self, warning_producer: Any, weather_class: Any, kafka_producer: Any, state: BridgeState, office_codes: list[str] | None = None) -> int:
        pending: list[str] = []
        emitted = 0
        seen = set(state.seen_weather)
        for office_code in office_codes or WARNING_OFFICE_CODES:
            try:
                records = parse_weather_warning_payload(office_code, self.fetch_warning_payload(office_code), self.area_names)
            except Exception as exc:
                LOGGER.warning("Skipping warning office %s after fetch/parse failure: %s", office_code, exc)
                continue
            for record in records:
                dedupe_key = f"{record['office_code']}|{record['area_code']}|{record['report_datetime']}"
                if dedupe_key in seen:
                    continue
                _call_send(warning_producer, ("send_jp_jma_warning_weather_warning", "send_weather_warning"), _feedurl=WARNING_URL_TEMPLATE.format(office_code=office_code), _office_code=record["office_code"], _area_code=record["area_code"], data=_construct_data(weather_class, record), flush_producer=False)
                pending.append(dedupe_key)
                emitted += 1
        if emitted and kafka_producer.flush(timeout=120) != 0:
            raise RuntimeError("Kafka flush failed while emitting weather warnings")
        state.seen_weather = _cap_list(state.seen_weather + pending)
        return emitted

    def emit_tsunami_cycle(self, tsunami_producer: Any, tsunami_class: Any, kafka_producer: Any, state: BridgeState) -> int:
        pending: list[str] = []
        emitted = 0
        seen = set(state.seen_tsunami)
        try:
            entries = self.fetch_tsunami_list()
        except Exception as exc:
            LOGGER.warning("Skipping tsunami cycle after list fetch failure: %s", exc)
            return 0
        for entry in entries:
            try:
                detail = self.fetch_tsunami_detail(entry.get("json", ""))
            except Exception as exc:
                LOGGER.warning("Could not fetch tsunami detail %s: %s", entry.get("json"), exc)
                detail = None
            record = parse_tsunami_alert(entry, detail)
            dedupe_key = f"{record['event_id']}|{record['serial']}"
            if dedupe_key in seen:
                continue
            _call_send(tsunami_producer, ("send_jp_jma_tsunami_tsunami_alert", "send_tsunami_alert"), _feedurl=record["detail_url"] or TSUNAMI_LIST_URL, _event_id=record["event_id"], _serial=record["serial"], data=_construct_data(tsunami_class, record), flush_producer=False)
            pending.append(dedupe_key)
            emitted += 1
        if emitted and kafka_producer.flush(timeout=120) != 0:
            raise RuntimeError("Kafka flush failed while emitting tsunami alerts")
        state.seen_tsunami = _cap_list(state.seen_tsunami + pending)
        return emitted


def _import_generated() -> tuple[Any, Any, Any, Any, Any]:
    from jma_bosai_warning_producer_data import Office, TsunamiAlert, WeatherWarning
    from jma_bosai_warning_producer_kafka_producer.producer import JPJMATsunamiEventProducer, JPJMAWarningEventProducer
    return Office, WeatherWarning, TsunamiAlert, JPJMAWarningEventProducer, JPJMATsunamiEventProducer


def run_feed(args: argparse.Namespace) -> None:
    kafka_config: dict[str, Any] = {}
    if args.connection_string:
        kafka_config.update(parse_connection_string(args.connection_string))
    if args.kafka_bootstrap_servers:
        kafka_config["bootstrap.servers"] = args.kafka_bootstrap_servers
    if args.sasl_username:
        kafka_config.update({"sasl.username": args.sasl_username, "sasl.mechanism": "PLAIN", "security.protocol": "SASL_SSL"})
    if args.sasl_password:
        kafka_config["sasl.password"] = args.sasl_password
    if os.getenv("KAFKA_ENABLE_TLS", "true").lower() in ("0", "false", "no") and "sasl.username" not in kafka_config:
        kafka_config.pop("security.protocol", None)
    if "bootstrap.servers" not in kafka_config:
        raise ValueError("Kafka bootstrap servers are required via --kafka-bootstrap-servers or CONNECTION_STRING")
    entity_topic = kafka_config.pop("kafka_topic", None)
    topic_warning = entity_topic or args.kafka_topic_warning or "jma-bosai-warning"
    topic_tsunami = entity_topic or args.kafka_topic_tsunami or "jma-bosai-tsunami"

    Office, WeatherWarning, TsunamiAlert, WarningProducer, TsunamiProducer = _import_generated()
    producer = Producer(kafka_config)
    warning_producer = WarningProducer(producer, topic_warning)
    tsunami_producer = TsunamiProducer(producer, topic_tsunami)
    api = JmaBosaiWarningAPI()
    state = BridgeState.from_dict(_load_state(args.state_file))
    next_warning = next_tsunami = 0.0
    metadata_interval = max(1, args.office_metadata_refresh_hours) * 3600
    while True:
        start = time.monotonic()
        now_utc = datetime.now(timezone.utc)
        should_refresh = not state.last_metadata_refresh
        if state.last_metadata_refresh:
            try:
                should_refresh = (now_utc - datetime.fromisoformat(state.last_metadata_refresh.replace("Z", "+00:00"))).total_seconds() >= metadata_interval
            except ValueError:
                should_refresh = True
        if should_refresh:
            api.refresh_area_catalog()
            api.emit_offices(warning_producer, Office, producer)
            state.last_metadata_refresh = now_utc.isoformat().replace("+00:00", "Z")
            _save_state(args.state_file, state.as_dict())
        if start >= next_warning:
            LOGGER.info("Emitted %d weather warning records", api.emit_warning_cycle(warning_producer, WeatherWarning, producer, state))
            next_warning = start + args.polling_interval_warning
            _save_state(args.state_file, state.as_dict())
        if start >= next_tsunami:
            LOGGER.info("Emitted %d tsunami alert records", api.emit_tsunami_cycle(tsunami_producer, TsunamiAlert, producer, state))
            next_tsunami = start + args.polling_interval_tsunami
            _save_state(args.state_file, state.as_dict())
        if args.once:
            break
        time.sleep(max(1.0, min(next_warning, next_tsunami) - time.monotonic()))
    producer.flush(timeout=30)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bridge JMA Bosai weather warnings and tsunami alerts to Kafka as CloudEvents.")
    sub = parser.add_subparsers(dest="command")
    feed = sub.add_parser("feed", help="Poll JMA Bosai feeds and publish CloudEvents")
    feed.add_argument("--kafka-bootstrap-servers", default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed.add_argument("--kafka-topic-warning", default=os.getenv("KAFKA_TOPIC_WARNING", "jma-bosai-warning"))
    feed.add_argument("--kafka-topic-tsunami", default=os.getenv("KAFKA_TOPIC_TSUNAMI", "jma-bosai-tsunami"))
    feed.add_argument("--sasl-username", default=os.getenv("SASL_USERNAME"))
    feed.add_argument("--sasl-password", default=os.getenv("SASL_PASSWORD"))
    feed.add_argument("-c", "--connection-string", default=os.getenv("CONNECTION_STRING"))
    feed.add_argument("--polling-interval-warning", type=int, default=int(os.getenv("POLLING_INTERVAL_WARNING", "60")))
    feed.add_argument("--polling-interval-tsunami", type=int, default=int(os.getenv("POLLING_INTERVAL_TSUNAMI", "30")))
    feed.add_argument("--office-metadata-refresh-hours", type=int, default=int(os.getenv("OFFICE_METADATA_REFRESH_HOURS", "720")))
    feed.add_argument("--state-file", default=os.getenv("STATE_FILE", ".\\state\\jma-bosai-warning.json"))
    feed.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    return parser


def main(argv: list[str] | None = None) -> None:
    logging.basicConfig(level=logging.DEBUG if os.getenv("DEBUG") else logging.INFO)
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "feed":
        run_feed(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
