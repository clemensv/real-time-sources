"""Transport-neutral acquisition for JMA Bosai volcanic warnings and eruptions."""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

WARNING_URL = "https://www.jma.go.jp/bosai/volcano/data/warning.json"
ERUPTION_URL = "https://www.jma.go.jp/bosai/volcano/data/eruption.json"
VOLCANO_LIST_URL = "https://www.jma.go.jp/bosai/volcano/const/volcano_list.json"
DEFAULT_STATE_FILE = "./state/jma-bosai-volcano.json"
TARGET_VOLCANO_INFO = "噴火警報・予報（対象火山）"
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-jma-bosai-volcano/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com")
    + ")"
)

LOGGER = logging.getLogger(__name__)

CONDITION_MAP = {
    "発表": "ISSUED",
    "引上げ": "RAISED",
    "引下げ": "LOWERED",
    "継続": "CONTINUED",
    "切替": "SWITCHED",
    "解除": "CANCELLED",
}
ALERT_LEVEL_CODES = {
    "02": "Crater-area warning",
    "03": "Eruption warning for surrounding sea area",
    "04": "Eruption forecast: warning lifted",
    "11": "Active volcano; pay attention",
    "12": "Crater area restriction",
    "13": "Mountain access restriction",
    "22": "Crater vicinity danger",
    "23": "Mountain access danger",
    "36": "Surrounding waters warning for submarine or island volcanoes",
    "43": "Crater-area warning: entry restrictions and similar measures",
    "44": "Eruption warning for surrounding sea area: surrounding sea area warning",
    "45": "Active volcano; pay attention",
    "49": "Crater-area warning: caution around the crater",
}
ERUPTION_TYPE_MAP = {
    "噴火": "ERUPTION",
    "爆発": "EXPLOSION",
    "連続噴火継続": "CONTINUOUS_ERUPTION_CONTINUING",
    "連続噴火停止": "CONTINUOUS_ERUPTION_STOPPED",
}


@dataclass
class PendingTelemetry:
    warnings: list[dict[str, Any]]
    eruptions: list[dict[str, Any]]
    warning_keys: set[str]
    eruption_keys: set[str]


def make_retrying_session() -> requests.Session:
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


def load_state(state_file: str) -> dict[str, Any]:
    try:
        path = Path(state_file)
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            data.setdefault("warnings", [])
            data.setdefault("eruptions", [])
            data.setdefault("last_metadata_refresh", None)
            return data
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Could not load state from %s: %s", state_file, exc)
    return {"warnings": [], "eruptions": [], "last_metadata_refresh": None}


def save_state(state_file: str, state: dict[str, Any]) -> None:
    if not state_file:
        return
    path = Path(state_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def decimal_degrees(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float, str)):
        return float(value)
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        return float(value[0]) + float(value[1]) / 60.0
    raise ValueError(f"Unsupported coordinate value: {value!r}")


def parse_jma_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)


def to_utc(value: str | datetime | None) -> datetime | None:
    if value is None:
        return None
    dt = parse_jma_datetime(value) if isinstance(value, str) else value
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def map_condition_name(value: str | None) -> str:
    return CONDITION_MAP.get(value or "", "ISSUED")


def alert_level_description(code: str | None) -> str | None:
    return ALERT_LEVEL_CODES.get(code or "")


def _mock_enabled() -> bool:
    return os.getenv("JMA_BOSAI_VOLCANO_MOCK", "").lower() in ("1", "true", "yes")


class JMABosaiVolcanoSource:
    def __init__(self, session: requests.Session | None = None):
        self.session = session or make_retrying_session()
        self.volcano_catalog: dict[str, dict[str, Any]] = {}

    def fetch_json(self, url: str) -> Any:
        response = self.session.get(url, timeout=20)
        response.raise_for_status()
        return response.json()

    def fetch_volcano_catalog_data(self) -> dict[str, dict[str, Any]]:
        return parse_volcano_catalog(self.fetch_json(VOLCANO_LIST_URL))

    def fetch_warnings(self) -> list[dict[str, Any]]:
        payload = self.fetch_json(WARNING_URL)
        return payload if isinstance(payload, list) else []

    def fetch_eruptions(self) -> list[dict[str, Any]]:
        payload = self.fetch_json(ERUPTION_URL)
        return payload if isinstance(payload, list) else []

    def refresh_catalog(self) -> dict[str, dict[str, Any]]:
        self.volcano_catalog = self.fetch_volcano_catalog_data()
        return self.volcano_catalog

    def build_reference_records(self) -> list[dict[str, Any]]:
        return list(self.refresh_catalog().values())

    def should_refresh_reference(self, state: dict[str, Any], refresh_hours: int) -> bool:
        last = state.get("last_metadata_refresh")
        if not last or not self.volcano_catalog:
            return True
        try:
            elapsed = datetime.now(timezone.utc) - datetime.fromisoformat(last)
        except ValueError:
            return True
        return elapsed.total_seconds() >= refresh_hours * 3600

    def commit_reference_refresh(self, state: dict[str, Any], state_file: str) -> None:
        state["last_metadata_refresh"] = datetime.now(timezone.utc).isoformat()
        save_state(state_file, state)

    def collect_pending_telemetry(
        self,
        state: dict[str, Any],
        warning_payloads: list[dict[str, Any]] | None = None,
        eruption_payloads: list[dict[str, Any]] | None = None,
    ) -> PendingTelemetry:
        seen_warnings = set(state.get("warnings", []))
        seen_eruptions = set(state.get("eruptions", []))
        warnings: list[dict[str, Any]] = []
        eruptions: list[dict[str, Any]] = []
        warning_keys: set[str] = set()
        eruption_keys: set[str] = set()

        for record in warning_payloads if warning_payloads is not None else self.fetch_warnings():
            key = dedupe_key(record)
            if key in seen_warnings:
                continue
            warnings.extend(parse_warning_record(record))
            if key:
                warning_keys.add(key)
        for record in eruption_payloads if eruption_payloads is not None else self.fetch_eruptions():
            key = dedupe_key(record)
            if key in seen_eruptions:
                continue
            eruptions.extend(parse_eruption_record(record))
            if key:
                eruption_keys.add(key)
        return PendingTelemetry(warnings, eruptions, warning_keys, eruption_keys)

    def commit_telemetry_state(self, state: dict[str, Any], state_file: str, warning_keys: set[str], eruption_keys: set[str]) -> None:
        if warning_keys:
            state["warnings"] = sorted(set(state.get("warnings", [])) | warning_keys)
        if eruption_keys:
            state["eruptions"] = sorted(set(state.get("eruptions", [])) | eruption_keys)
        save_state(state_file, state)


class MockSource(JMABosaiVolcanoSource):
    def fetch_volcano_catalog_data(self) -> dict[str, dict[str, Any]]:
        return parse_volcano_catalog(
            [
                {"code": "101", "nameJp": "桜島", "nameEn": "Sakurajima", "lat": 31.58, "lon": 130.66, "elevation": 1117, "levelOperation": True}
            ]
        )

    def fetch_warnings(self) -> list[dict[str, Any]]:
        return [
            {
                "eventId": "v1",
                "reportDatetime": "2026-01-01T00:00:00+09:00",
                "volcanoInfos": [
                    {
                        "type": "噴火警報・予報（対象火山）",
                        "items": [{"code": "11", "name": "活火山であることに留意", "condition": "発表", "areas": [{"code": "101"}]}],
                    }
                ],
            }
        ]

    def fetch_eruptions(self) -> list[dict[str, Any]]:
        return [
            {
                "eventId": "e1",
                "reportDatetime": "2026-01-01T00:05:00+09:00",
                "volcanoInfos": [{"items": [{"type": "噴火", "areas": [{"code": "101"}], "description": "噴火しました"}]}],
            }
        ]


def parse_volcano_catalog(payload: Any) -> dict[str, dict[str, Any]]:
    entries: Iterable[Any]
    if isinstance(payload, dict):
        entries = [dict(value, code=code) for code, value in payload.items() if isinstance(value, dict)]
    elif isinstance(payload, list):
        entries = payload
    else:
        return {}
    catalog: dict[str, dict[str, Any]] = {}
    for item in entries:
        code = str(item.get("code", "")).zfill(3)
        if not code or code == "000":
            continue
        lat = item.get("lat") if "lat" in item else None
        lon = item.get("lon") if "lon" in item else None
        if "latlon" in item:
            lat, lon = item.get("latlon", [None, None])[:2]
        latitude = decimal_degrees(lat)
        longitude = decimal_degrees(lon)
        if latitude is None or longitude is None:
            continue
        catalog[code] = {
            "prefecture": "japan",
            "event": "info",
            "volcano_code": code,
            "name_jp": item.get("nameJp") or item.get("name_jp") or "",
            "name_en": item.get("nameEn") or item.get("name_en") or "",
            "latitude": latitude,
            "longitude": longitude,
            "elevation_m": float(item["elevation"]) if item.get("elevation") is not None else None,
            "level_operation": bool(item.get("levelOperation", False)),
        }
    return catalog


def dedupe_key(record: dict[str, Any]) -> str:
    return f"{record.get('eventId', '')}|{record.get('reportDatetime', '')}"


def parse_warning_record(record: dict[str, Any]) -> list[dict[str, Any]]:
    try:
        report_local = parse_jma_datetime(record.get("reportDatetime"))
        report_utc = to_utc(report_local)
    except ValueError:
        return []
    if report_local is None or report_utc is None:
        return []
    events: list[dict[str, Any]] = []
    for info in record.get("volcanoInfos", []) or []:
        if info.get("type", "") != TARGET_VOLCANO_INFO:
            continue
        for item in info.get("items", []) or []:
            for area in item.get("areas", []) or []:
                volcano_code = str(area.get("code", "")).zfill(3)
                if not volcano_code or volcano_code == "000":
                    continue
                events.append(
                    {
                        "prefecture": "japan",
                        "event": "warning",
                        "volcano_code": volcano_code,
                        "event_id": str(record.get("eventId", "")),
                        "report_datetime": report_utc,
                        "report_datetime_local": report_local,
                        "alert_level_code": str(item.get("code", "")),
                        "alert_level_name": str(item.get("name", "")),
                        "previous_level_code": str(item.get("lastCode")) if item.get("lastCode") is not None else None,
                        "condition": map_condition_name(item.get("condition")),
                        "info_type_jp": info.get("type"),
                        "area_codes": [str(code) for code in record.get("areas", []) or []],
                    }
                )
    return events


def _first_text(*values: Any) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _find_datetime(value: Any) -> datetime | None:
    if isinstance(value, str):
        try:
            return parse_jma_datetime(value)
        except ValueError:
            return None
    if isinstance(value, dict):
        for key in ("eruptionDatetime", "eruptionDateTime", "eventDatetime", "eventDateTime", "datetime", "dateTime"):
            result = _find_datetime(value.get(key))
            if result:
                return result
    return None


def map_eruption_type_name(value: str | None) -> str | None:
    if not value:
        return None
    normalized = value.strip()
    if normalized in ERUPTION_TYPE_MAP:
        return ERUPTION_TYPE_MAP[normalized]
    for jp, enum_value in ERUPTION_TYPE_MAP.items():
        if jp in normalized:
            return enum_value
    return "UNKNOWN"


def _combined_text(item: dict[str, Any], record: dict[str, Any]) -> str:
    parts: list[str] = []
    for source in (item, record):
        for key in ("description", "text", "content", "title", "name"):
            value = source.get(key)
            if isinstance(value, str) and value.strip():
                parts.append(value.strip())
    return "\n".join(dict.fromkeys(parts))


def _first_key_text(item: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _extract_height_m(text: str, *labels: str) -> float | None:
    for label in labels:
        match = re.search(rf"{re.escape(label)}[^\n\r：:]*[：:]?\s*火口上\s*([0-9,]+(?:\.[0-9]+)?)\s*m", text, re.IGNORECASE)
        if match:
            return float(match.group(1).replace(",", ""))
    return None


def _extract_labeled_text(text: str, label: str) -> str | None:
    normalized = text.replace("　", "")
    match = re.search(rf"{re.escape(label)}\s*[：:]\s*([^\n\r]+)", normalized)
    return match.group(1).strip() if match else None


def _extract_pyroclastic_flow(text: str) -> bool | None:
    if "火砕流" not in text:
        return None
    if re.search(r"火砕流[^\n\r]*(なし|観測されず|確認されず|発生していない)", text):
        return False
    return True


def parse_eruption_record(record: dict[str, Any]) -> list[dict[str, Any]]:
    try:
        report_local = parse_jma_datetime(record.get("reportDatetime"))
        report_utc = to_utc(report_local)
    except ValueError:
        return []
    if report_local is None or report_utc is None:
        return []
    events: list[dict[str, Any]] = []
    infos = record.get("volcanoInfos", []) or []
    if not infos and (record.get("eventId") or record.get("description")):
        infos = [{"type": None, "items": [record]}]
    for info in infos:
        for item in info.get("items", []) or []:
            areas = item.get("areas") or record.get("areas") or []
            area_dicts = [area for area in areas if isinstance(area, dict)]
            if not area_dicts and record.get("eventId"):
                area_dicts = [{"code": record.get("eventId")}]
            occurrence_local = _find_datetime(item)
            description = _combined_text(item, record) or json.dumps(item, ensure_ascii=False, sort_keys=True)
            phenomenon = _first_key_text(item, "phenomenon", "eventType", "type") or item.get("name")
            colored_plume_height = _extract_height_m(description, "有色噴煙")
            white_plume_height = _extract_height_m(description, "白色噴煙")
            maximum_plume_height = _extract_height_m(description, "噴火開始以降の最高噴煙高度")
            for area in area_dicts:
                volcano_code = str(area.get("code", "")).zfill(3)
                if not volcano_code or volcano_code == "000":
                    continue
                events.append(
                    {
                        "prefecture": "japan",
                        "event": "eruption",
                        "volcano_code": volcano_code,
                        "event_id": str(record.get("eventId", "")),
                        "report_datetime": report_utc,
                        "report_datetime_local": report_local,
                        "eruption_datetime": to_utc(occurrence_local),
                        "eruption_datetime_local": occurrence_local,
                        "eruption_type": map_eruption_type_name(phenomenon if isinstance(phenomenon, str) else None),
                        "crater_name": _first_key_text(item, "craterName", "crater") or _extract_labeled_text(description, "火口"),
                        "colored_plume_height_m": colored_plume_height,
                        "white_plume_height_m": white_plume_height,
                        "maximum_plume_height_since_start_m": maximum_plume_height,
                        "plume_direction": _first_key_text(item, "plumeDirection", "flowDirection") or _extract_labeled_text(description, "流向"),
                        "ash_dispersal_direction": _first_key_text(item, "ashDispersalDirection", "ashDirection"),
                        "pyroclastic_flow_observed": _extract_pyroclastic_flow(description),
                        "plume_amount_jp": _first_key_text(item, "plumeAmount") or _extract_labeled_text(description, "噴煙量"),
                        "description": description,
                        "info_type_jp": info.get("type"),
                        "area_codes": [str(code) for code in record.get("areas", []) or []],
                    }
                )
    return events


__all__ = [
    "ALERT_LEVEL_CODES",
    "DEFAULT_STATE_FILE",
    "ERUPTION_TYPE_MAP",
    "ERUPTION_URL",
    "JMABosaiVolcanoSource",
    "LOGGER",
    "MockSource",
    "PendingTelemetry",
    "TARGET_VOLCANO_INFO",
    "USER_AGENT",
    "VOLCANO_LIST_URL",
    "WARNING_URL",
    "_mock_enabled",
    "alert_level_description",
    "decimal_degrees",
    "dedupe_key",
    "load_state",
    "make_retrying_session",
    "map_condition_name",
    "map_eruption_type_name",
    "parse_eruption_record",
    "parse_jma_datetime",
    "parse_volcano_catalog",
    "parse_warning_record",
    "save_state",
    "to_utc",
]
