
"""Bridge for JMA Bosai volcanic warnings and eruptions."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from confluent_kafka import Producer

from jma_bosai_volcano_producer_data import Volcano, VolcanicWarning, VolcanicEruption
from jma_bosai_volcano_producer_data.conditionenum import ConditionEnum
from jma_bosai_volcano_producer_data.eruptiontypeenum import EruptionTypeenum
try:
    from jma_bosai_volcano_producer_kafka_producer.producer import JPJMAVolcanoEventProducer
except ModuleNotFoundError:
    # The generated Kafka producer package is only installed in the Kafka
    # image. The MQTT/AMQP images reuse this module for the shared
    # build_*/fetch helpers and the generated data classes, so the Kafka
    # producer is an optional dependency there. Only the Kafka bridge
    # references it, and that class never runs in those images.
    JPJMAVolcanoEventProducer = None

WARNING_URL = "https://www.jma.go.jp/bosai/volcano/data/warning.json"
ERUPTION_URL = "https://www.jma.go.jp/bosai/volcano/data/eruption.json"
VOLCANO_LIST_URL = "https://www.jma.go.jp/bosai/volcano/const/volcano_list.json"
DEFAULT_TOPIC = "jma-bosai-volcano"
DEFAULT_STATE_FILE = "./state/jma-bosai-volcano.json"
TARGET_VOLCANO_INFO = "噴火警報・予報（対象火山）"
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-jma-bosai-volcano/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

logging.basicConfig(level=logging.INFO)

CONDITION_MAP = {
    "発表": ConditionEnum.ISSUED,
    "引上げ": ConditionEnum.RAISED,
    "引下げ": ConditionEnum.LOWERED,
    "継続": ConditionEnum.CONTINUED,
    "切替": ConditionEnum.SWITCHED,
    "解除": ConditionEnum.CANCELLED,
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
    "噴火": EruptionTypeenum.ERUPTION,
    "爆発": EruptionTypeenum.EXPLOSION,
    "連続噴火継続": EruptionTypeenum.CONTINUOUS_ERUPTION_CONTINUING,
    "連続噴火停止": EruptionTypeenum.CONTINUOUS_ERUPTION_STOPPED,
}


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
        logging.warning("Could not load state from %s: %s", state_file, exc)
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


def map_condition(value: str | None) -> ConditionEnum:
    return CONDITION_MAP.get(value or "", ConditionEnum.ISSUED)


def alert_level_description(code: str | None) -> str | None:
    return ALERT_LEVEL_CODES.get(code or "")


def parse_connection_string(connection_string: str) -> dict[str, str]:
    config: dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if part.startswith("Endpoint="):
                config["bootstrap.servers"] = part.split("=", 1)[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
                config["sasl.username"] = "$ConnectionString"
                config["sasl.password"] = connection_string.strip()
            elif part.startswith("EntityPath="):
                config["kafka_topic"] = part.split("=", 1)[1].strip('"')
            elif part.startswith("BootstrapServer="):
                config["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc
    if "sasl.username" in config:
        config["security.protocol"] = "SASL_SSL"
        config["sasl.mechanisms"] = "PLAIN"
    return config


def build_kafka_config(args: argparse.Namespace) -> tuple[dict[str, str], str]:
    if args.connection_string:
        parsed = parse_connection_string(args.connection_string)
        bootstrap = parsed.get("bootstrap.servers")
        topic = parsed.get("kafka_topic") or args.kafka_topic or DEFAULT_TOPIC
        sasl_username = parsed.get("sasl.username")
        sasl_password = parsed.get("sasl.password")
    else:
        bootstrap = args.kafka_bootstrap_servers
        topic = args.kafka_topic or DEFAULT_TOPIC
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password
    if not bootstrap:
        raise ValueError("Kafka bootstrap servers must be provided by KAFKA_BOOTSTRAP_SERVERS or CONNECTION_STRING")
    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    config = {"bootstrap.servers": bootstrap}
    if sasl_username and sasl_password:
        config.update({
            "sasl.mechanisms": "PLAIN",
            "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
            "sasl.username": sasl_username,
            "sasl.password": sasl_password,
        })
    elif tls_enabled:
        config["security.protocol"] = "SSL"
    return config, topic


class JMABosaiVolcanoAPI:
    def __init__(self, session: requests.Session | None = None):
        self.session = session or make_retrying_session()
        self.volcano_catalog: dict[str, Volcano] = {}

    def fetch_json(self, url: str) -> Any:
        response = self.session.get(url, timeout=20)
        response.raise_for_status()
        return response.json()

    def fetch_volcano_catalog(self) -> dict[str, Volcano]:
        payload = self.fetch_json(VOLCANO_LIST_URL)
        return parse_volcano_catalog(payload)

    def fetch_warnings(self) -> list[dict[str, Any]]:
        payload = self.fetch_json(WARNING_URL)
        return payload if isinstance(payload, list) else []

    def fetch_eruptions(self) -> list[dict[str, Any]]:
        payload = self.fetch_json(ERUPTION_URL)
        return payload if isinstance(payload, list) else []

    def refresh_catalog(self) -> dict[str, Volcano]:
        catalog = self.fetch_volcano_catalog()
        self.volcano_catalog = catalog
        return catalog

    def emit_reference_data(self, producer: JPJMAVolcanoEventProducer, state: dict[str, Any], state_file: str) -> None:
        catalog = self.refresh_catalog()
        for volcano in catalog.values():
            producer.send_jp_jma_volcano_volcano(
                _feedurl=VOLCANO_LIST_URL,
                _volcano_code=volcano.volcano_code,
                data=volcano,
                flush_producer=False,
            )
        remainder = producer.producer.flush(timeout=30)
        if remainder:
            raise RuntimeError(f"Kafka flush left {remainder} reference events queued")
        state["last_metadata_refresh"] = datetime.now(timezone.utc).isoformat()
        save_state(state_file, state)

    def maybe_refresh_reference_data(self, producer: JPJMAVolcanoEventProducer, state: dict[str, Any], state_file: str, refresh_hours: int) -> None:
        last = state.get("last_metadata_refresh")
        should_refresh = True
        if last:
            try:
                elapsed = datetime.now(timezone.utc) - datetime.fromisoformat(last)
                should_refresh = elapsed.total_seconds() >= refresh_hours * 3600
            except ValueError:
                should_refresh = True
        if should_refresh or not self.volcano_catalog:
            try:
                self.emit_reference_data(producer, state, state_file)
            except Exception as exc:  # pylint: disable=broad-except
                if self.volcano_catalog:
                    logging.warning("Keeping cached volcano catalog after refresh failure: %s", exc)
                else:
                    raise

    def poll_once(self, producer: JPJMAVolcanoEventProducer, state: dict[str, Any], state_file: str) -> tuple[int, int]:
        seen_warnings = set(state.get("warnings", []))
        seen_eruptions = set(state.get("eruptions", []))
        pending_warnings: set[str] = set()
        pending_eruptions: set[str] = set()
        warning_count = 0
        eruption_count = 0

        try:
            for record in self.fetch_warnings():
                key = dedupe_key(record)
                if key in seen_warnings:
                    continue
                for warning in parse_warning_record(record):
                    producer.send_jp_jma_volcano_volcanic_warning(
                        _feedurl=WARNING_URL,
                        _volcano_code=warning.volcano_code,
                        data=warning,
                        flush_producer=False,
                    )
                    warning_count += 1
                if key:
                    pending_warnings.add(key)
        except Exception as exc:  # pylint: disable=broad-except
            logging.warning("Skipping warning endpoint for this cycle: %s", exc)

        try:
            for record in self.fetch_eruptions():
                key = dedupe_key(record)
                if key in seen_eruptions:
                    continue
                for eruption in parse_eruption_record(record):
                    producer.send_jp_jma_volcano_volcanic_eruption(
                        _feedurl=ERUPTION_URL,
                        _volcano_code=eruption.volcano_code,
                        data=eruption,
                        flush_producer=False,
                    )
                    eruption_count += 1
                if key:
                    pending_eruptions.add(key)
        except Exception as exc:  # pylint: disable=broad-except
            logging.warning("Skipping eruption endpoint for this cycle: %s", exc)

        remainder = producer.producer.flush(timeout=30)
        if remainder:
            raise RuntimeError(f"Kafka flush left {remainder} telemetry events queued")
        if pending_warnings or pending_eruptions:
            state["warnings"] = sorted(seen_warnings | pending_warnings)
            state["eruptions"] = sorted(seen_eruptions | pending_eruptions)
            save_state(state_file, state)
        return warning_count, eruption_count

    def feed(self, kafka_config: dict[str, str], kafka_topic: str, polling_interval: int, state_file: str, metadata_refresh_hours: int, once: bool = False) -> None:
        producer = JPJMAVolcanoEventProducer(Producer(kafka_config), kafka_topic)
        state = load_state(state_file)
        self.emit_reference_data(producer, state, state_file)
        while True:
            started = time.monotonic()
            self.maybe_refresh_reference_data(producer, state, state_file, metadata_refresh_hours)
            warnings, eruptions = self.poll_once(producer, state, state_file)
            logging.info("Emitted %d warning and %d eruption events", warnings, eruptions)
            if once:
                break
            sleep_for = max(0.0, polling_interval - (time.monotonic() - started))
            time.sleep(sleep_for)


def _mock_enabled() -> bool:
    return os.getenv("JMA_BOSAI_VOLCANO_MOCK", "").lower() in ("1", "true", "yes")


class MockAPI(JMABosaiVolcanoAPI):
    """Deterministic offline volcano source for the Docker E2E flow tests.

    Returns a fixed catalog, warning, and eruption so the test does not depend
    on JMA publishing a live volcanic warning during the test window. Canned
    payloads mirror the MQTT/AMQP MockAPI so all three transports emit the same
    reference + telemetry shapes.
    """

    def fetch_volcano_catalog(self) -> dict[str, Volcano]:
        return parse_volcano_catalog([
            {'code': '101', 'nameJp': '桜島', 'nameEn': 'Sakurajima',
             'lat': 31.58, 'lon': 130.66, 'elevation': 1117, 'levelOperation': True},
        ])

    def fetch_warnings(self) -> list[dict[str, Any]]:
        return [{
            'eventId': 'v1', 'reportDatetime': '2026-01-01T00:00:00+09:00',
            'volcanoInfos': [{'type': '噴火警報・予報（対象火山）',
                'items': [{'code': '11', 'name': '活火山であることに留意',
                    'condition': '発表', 'areas': [{'code': '101'}]}]}],
        }]

    def fetch_eruptions(self) -> list[dict[str, Any]]:
        return [{
            'eventId': 'e1', 'reportDatetime': '2026-01-01T00:05:00+09:00',
            'volcanoInfos': [{'items': [{'type': '噴火',
                'areas': [{'code': '101'}], 'description': '噴火しました'}]}],
        }]


def parse_volcano_catalog(payload: Any) -> dict[str, Volcano]:
    entries: Iterable[Any]
    if isinstance(payload, dict):
        entries = [dict(value, code=code) for code, value in payload.items() if isinstance(value, dict)]
    elif isinstance(payload, list):
        entries = payload
    else:
        return {}
    catalog: dict[str, Volcano] = {}
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
        catalog[code] = Volcano(
            prefecture="japan",
            event="info",
            volcano_code=code,
            name_jp=item.get("nameJp") or item.get("name_jp") or "",
            name_en=item.get("nameEn") or item.get("name_en") or "",
            latitude=latitude,
            longitude=longitude,
            elevation_m=float(item["elevation"]) if item.get("elevation") is not None else None,
            level_operation=bool(item.get("levelOperation", False)),
        )
    return catalog


def dedupe_key(record: dict[str, Any]) -> str:
    return f"{record.get('eventId', '')}|{record.get('reportDatetime', '')}"


def parse_warning_record(record: dict[str, Any]) -> list[VolcanicWarning]:
    try:
        report_local = parse_jma_datetime(record.get("reportDatetime"))
        report_utc = to_utc(report_local)
    except ValueError:
        return []
    if report_local is None or report_utc is None:
        return []
    events: list[VolcanicWarning] = []
    for info in record.get("volcanoInfos", []) or []:
        info_type = info.get("type", "")
        if info_type != TARGET_VOLCANO_INFO:
            continue
        for item in info.get("items", []) or []:
            for area in item.get("areas", []) or []:
                volcano_code = str(area.get("code", "")).zfill(3)
                if not volcano_code or volcano_code == "000":
                    continue
                events.append(VolcanicWarning(
                    prefecture="japan",
                    event="warning",
                    volcano_code=volcano_code,
                    event_id=str(record.get("eventId", "")),
                    report_datetime=report_utc,
                    report_datetime_local=report_local,
                    alert_level_code=str(item.get("code", "")),
                    alert_level_name=str(item.get("name", "")),
                    previous_level_code=str(item.get("lastCode")) if item.get("lastCode") is not None else None,
                    condition=map_condition(item.get("condition")),
                    info_type_jp=info_type,
                    area_codes=[str(code) for code in record.get("areas", []) or []],
                ))
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


def map_eruption_type(value: str | None) -> EruptionTypeenum | None:
    if not value:
        return None
    normalized = value.strip()
    if normalized in ERUPTION_TYPE_MAP:
        return ERUPTION_TYPE_MAP[normalized]
    for jp, enum_value in ERUPTION_TYPE_MAP.items():
        if jp in normalized:
            return enum_value
    return EruptionTypeenum.UNKNOWN


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


def parse_eruption_record(record: dict[str, Any]) -> list[VolcanicEruption]:
    try:
        report_local = parse_jma_datetime(record.get("reportDatetime"))
        report_utc = to_utc(report_local)
    except ValueError:
        return []
    if report_local is None or report_utc is None:
        return []
    events: list[VolcanicEruption] = []
    infos = record.get("volcanoInfos", []) or []
    if not infos and (record.get("eventId") or record.get("description")):
        infos = [{"type": None, "items": [record]}]
    for info in infos:
        for item in info.get("items", []) or []:
            areas = item.get("areas") or record.get("areas") or []
            area_dicts = [a for a in areas if isinstance(a, dict)]
            if not area_dicts and record.get("eventId"):
                area_dicts = [{"code": record.get("eventId")}]
            occurrence_local = _find_datetime(item)
            combined_text = _combined_text(item, record)
            description = combined_text or json.dumps(item, ensure_ascii=False, sort_keys=True)
            phenomenon = _first_key_text(item, "phenomenon", "eventType", "type") or item.get("name")
            colored_plume_height = _extract_height_m(description, "有色噴煙")
            white_plume_height = _extract_height_m(description, "白色噴煙")
            maximum_plume_height = _extract_height_m(description, "噴火開始以降の最高噴煙高度")
            for area in area_dicts:
                volcano_code = str(area.get("code", "")).zfill(3)
                if not volcano_code or volcano_code == "000":
                    continue
                events.append(VolcanicEruption(
                    prefecture="japan",
                    event="eruption",
                    volcano_code=volcano_code,
                    event_id=str(record.get("eventId", "")),
                    report_datetime=report_utc,
                    report_datetime_local=report_local,
                    eruption_datetime=to_utc(occurrence_local),
                    eruption_datetime_local=occurrence_local,
                    eruption_type=map_eruption_type(phenomenon if isinstance(phenomenon, str) else None),
                    crater_name=_first_key_text(item, "craterName", "crater") or _extract_labeled_text(description, "火口"),
                    colored_plume_height_m=colored_plume_height,
                    white_plume_height_m=white_plume_height,
                    maximum_plume_height_since_start_m=maximum_plume_height,
                    plume_direction=_first_key_text(item, "plumeDirection", "flowDirection") or _extract_labeled_text(description, "流向"),
                    ash_dispersal_direction=_first_key_text(item, "ashDispersalDirection", "ashDirection"),
                    pyroclastic_flow_observed=_extract_pyroclastic_flow(description),
                    plume_amount_jp=_first_key_text(item, "plumeAmount") or _extract_labeled_text(description, "噴煙量"),
                    description=description,
                    info_type_jp=info.get("type"),
                    area_codes=[str(code) for code in record.get("areas", []) or []],
                ))
    return events


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Feed JMA Bosai volcanic warnings and eruptions to Kafka.")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("catalog", help="Fetch and print volcano catalog metadata")
    feed_parser = subparsers.add_parser("feed", help="Feed JMA volcano events to Kafka")
    feed_parser.add_argument("--kafka-bootstrap-servers", default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic", default=os.getenv("KAFKA_TOPIC", DEFAULT_TOPIC))
    feed_parser.add_argument("--sasl-username", default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument("-c", "--connection-string", default=os.getenv("CONNECTION_STRING"))
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "60")))
    feed_parser.add_argument("--metadata-refresh-hours", type=int, default=int(os.getenv("VOLCANO_METADATA_REFRESH_HOURS", "720")))
    feed_parser.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    args = parser.parse_args()

    api = MockAPI() if _mock_enabled() else JMABosaiVolcanoAPI()
    if args.command == "catalog":
        print(json.dumps([v.to_serializer_dict() for v in api.fetch_volcano_catalog().values()], ensure_ascii=False, indent=2))
    elif args.command == "feed":
        kafka_config, topic = build_kafka_config(args)
        once = args.once or _mock_enabled()
        api.feed(kafka_config, topic, args.polling_interval, args.state_file, args.metadata_refresh_hours, once)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
