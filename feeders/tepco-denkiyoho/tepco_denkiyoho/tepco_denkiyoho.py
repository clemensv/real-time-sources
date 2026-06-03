"""Bridge for TEPCO Electricity Supply and Demand (Denki Yoho) CSV data."""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
import time as time_module
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from io import StringIO
from pathlib import Path
from typing import Any, Iterable

import requests
from confluent_kafka import Producer
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from tepco_denkiyoho_producer_data import DemandActual, DemandForecast, PeakDemandForecast, SupplyCapacity
from tepco_denkiyoho_producer_kafka_producer.producer import JPTEPCODenkiyohoKafkaEventProducer

DAILY_CSV_URL = "https://www.tepco.co.jp/forecast/html/images/juyo-d1-j.csv"
# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-tepco-denkiyoho/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)
DEFAULT_TOPIC = "tepco-denkiyoho"
DEFAULT_STATE_FILE = "./state/tepco-denkiyoho.json"
JST = timezone(timedelta(hours=9))
AREA_CODE = "TEPCO"
AREA_NAME_JP = "東京電力エリア"
AREA_NAME_EN = "TEPCO Service Area (Kanto)"
SUPPLY_CAPACITY_TIME_SENTINEL = "_supply_capacity_"
PEAK_FORECAST_TIME_SENTINEL = "_peak_forecast_"
STATE_CAP = 2000

logging.basicConfig(level=logging.DEBUG if sys.gettrace() is not None else logging.INFO)
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class SupplyCapacityRecord:
    date: str
    time: str
    peak_supply_capacity_mw: float
    peak_supply_capacity_jp_unit_value: int
    peak_time_slot: str
    peak_reserve_margin_pct: float
    peak_usage_pct: float
    daily_max_usage_pct: float | None
    daily_max_usage_time_slot: str | None
    update_datetime: str
    update_datetime_local: str
    area_code: str = AREA_CODE
    area_name_jp: str = AREA_NAME_JP
    area_name_en: str = AREA_NAME_EN


@dataclass(frozen=True)
class PeakDemandForecastRecord:
    date: str
    time: str
    peak_demand_forecast_mw: float
    peak_demand_forecast_jp_unit_value: int
    peak_time_slot: str
    update_datetime: str
    update_datetime_local: str
    area_code: str = AREA_CODE
    area_name_jp: str = AREA_NAME_JP
    area_name_en: str = AREA_NAME_EN


@dataclass(frozen=True)
class DemandActualRecord:
    date: str
    time: str
    datetime: str
    datetime_local: str
    actual_demand_mw: float
    actual_demand_jp_unit_value: int
    solar_generation_mw: float | None
    solar_generation_jp_unit_value: int | None
    solar_share_pct: float | None
    usage_pct: float | None
    supply_capacity_mw: float | None
    supply_capacity_jp_unit_value: int | None
    area_code: str = AREA_CODE


@dataclass(frozen=True)
class DemandForecastRecord:
    date: str
    time: str
    datetime: str
    datetime_local: str
    forecast_demand_mw: float
    forecast_demand_jp_unit_value: int
    usage_pct: float | None
    supply_capacity_mw: float | None
    supply_capacity_jp_unit_value: int | None
    area_code: str = AREA_CODE


@dataclass(frozen=True)
class DenkiyohoCsv:
    supply_capacity: SupplyCapacityRecord
    peak_demand_forecast: PeakDemandForecastRecord
    actuals: list[DemandActualRecord]
    forecasts: list[DemandForecastRecord]


@dataclass
class DenkiyohoState:
    supply_capacity_seen: list[str] = field(default_factory=list)
    peak_forecast_seen: list[str] = field(default_factory=list)
    actual_seen: list[str] = field(default_factory=list)
    forecast_seen: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DenkiyohoState":
        return cls(
            supply_capacity_seen=list(data.get("supply_capacity_seen", []))[-STATE_CAP:],
            peak_forecast_seen=list(data.get("peak_forecast_seen", []))[-STATE_CAP:],
            actual_seen=list(data.get("actual_seen", []))[-STATE_CAP:],
            forecast_seen=list(data.get("forecast_seen", []))[-STATE_CAP:],
        )

    def to_dict(self) -> dict[str, list[str]]:
        return {
            "supply_capacity_seen": self.supply_capacity_seen[-STATE_CAP:],
            "peak_forecast_seen": self.peak_forecast_seen[-STATE_CAP:],
            "actual_seen": self.actual_seen[-STATE_CAP:],
            "forecast_seen": self.forecast_seen[-STATE_CAP:],
        }

    def clone(self) -> "DenkiyohoState":
        return DenkiyohoState.from_dict(self.to_dict())

    @staticmethod
    def _append_capped(items: list[str], value: str) -> None:
        if value in items:
            return
        items.append(value)
        if len(items) > STATE_CAP:
            del items[: len(items) - STATE_CAP]

    def mark_supply_capacity(self, record: SupplyCapacityRecord) -> None:
        self._append_capped(self.supply_capacity_seen, supply_capacity_key(record))

    def mark_peak_forecast(self, record: PeakDemandForecastRecord) -> None:
        self._append_capped(self.peak_forecast_seen, peak_forecast_key(record))

    def mark_actual(self, record: DemandActualRecord) -> None:
        self._append_capped(self.actual_seen, actual_key(record))

    def mark_forecast(self, record: DemandForecastRecord) -> None:
        self._append_capped(self.forecast_seen, forecast_key(record))


def create_retrying_session() -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    retry = Retry(
        total=5,
        connect=3,
        read=3,
        status=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def decode_shift_jis_csv(content: bytes) -> str:
    return content.decode("cp932")


def jp_unit_to_mw(value: int | str) -> float:
    return float(int(str(value).strip()) * 10)


def _parse_int(value: str) -> int | None:
    value = value.strip()
    if not value:
        return None
    return int(value)


def _parse_float(value: str) -> float | None:
    value = value.strip()
    if not value:
        return None
    return float(value)


def _normalize_date(value: str, year_hint: int | None = None) -> str:
    value = value.strip()
    parts = value.split("/")
    if len(parts) == 2 and year_hint is not None:
        parts.insert(0, str(year_hint))
    if len(parts) != 3:
        raise ValueError(f"Unsupported TEPCO date value: {value!r}")
    return datetime(int(parts[0]), int(parts[1]), int(parts[2]), tzinfo=JST).date().isoformat()


def _normalize_time(value: str) -> str:
    hour, minute = value.strip().split(":", 1)
    return f"{int(hour):02d}:{int(minute):02d}"


def _normalize_time_slot(value: str) -> str:
    return value.strip().replace("～", "-").replace("〜", "-").replace("－", "-").replace("―", "-")


def jst_to_rfc3339(date_value: str, time_value: str) -> tuple[str, str]:
    local_dt = datetime.strptime(f"{date_value} {_normalize_time(time_value)}", "%Y-%m-%d %H:%M").replace(tzinfo=JST)
    return local_dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"), local_dt.isoformat()


def _parse_update_line(line: str) -> tuple[str, str, int]:
    timestamp = line.replace("UPDATE", "").strip()
    local_dt = datetime.strptime(timestamp, "%Y/%m/%d %H:%M").replace(tzinfo=JST)
    return local_dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"), local_dt.isoformat(), local_dt.year


def _parse_section_update(date_value: str, time_value: str, year_hint: int) -> tuple[str, str]:
    return jst_to_rfc3339(_normalize_date(date_value, year_hint), time_value)


def _read_csv_rows(lines: Iterable[str]) -> list[list[str]]:
    return list(csv.reader(StringIO("\n".join(lines))))


def _nonempty_csv_rows(text: str) -> tuple[list[list[str]], list[str]]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return _read_csv_rows(lines), lines


def _is_five_minute_header(row: list[str]) -> bool:
    return len(row) >= 3 and row[0] == "DATE" and row[1] == "TIME" and "5分間隔" in row[2].replace("５", "5")


def _is_hourly_header(row: list[str]) -> bool:
    return len(row) >= 6 and row[0] == "DATE" and row[1] == "TIME" and row[2] == "当日実績(万kW)"


def _find_row_index(rows: list[list[str]], predicate: Any) -> int:
    for index, row in enumerate(rows):
        if predicate(row):
            return index
    raise ValueError("TEPCO CSV is missing an expected section")


def _row_after(rows: list[list[str]], index: int) -> list[str]:
    if index + 1 >= len(rows):
        raise ValueError("TEPCO CSV section header is missing a data row")
    return rows[index + 1]


def split_sections(text: str) -> tuple[list[list[str]], list[list[str]], list[str]]:
    rows, lines = _nonempty_csv_rows(text)
    hourly_start = _find_row_index(rows, _is_hourly_header)
    five_minute_start = _find_row_index(rows, _is_five_minute_header)
    hourly_end = min(
        (idx for idx in range(hourly_start + 1, len(rows)) if idx == five_minute_start or rows[idx][0] == "最大使用率(%)"),
        default=five_minute_start,
    )
    hourly_rows = rows[hourly_start:hourly_end]
    actual_rows = rows[five_minute_start:]
    return hourly_rows, actual_rows, lines


def parse_denkiyoho_csv(text: str) -> DenkiyohoCsv:
    rows, lines = _nonempty_csv_rows(text)
    hourly_rows, actual_rows, _ = split_sections(text)
    _, _, update_year = _parse_update_line(lines[0])

    supply_header = _find_row_index(rows, lambda row: bool(row and row[0].startswith("ピーク時供給力(万kW)")))
    supply_row = _row_after(rows, supply_header)
    if len(supply_row) < 6:
        raise ValueError("TEPCO CSV section 1 peak supply row is incomplete")
    supply_value = _parse_int(supply_row[0])
    reserve_pct = _parse_float(supply_row[4])
    usage_pct = _parse_float(supply_row[5])
    if supply_value is None or reserve_pct is None or usage_pct is None:
        raise ValueError("TEPCO CSV section 1 peak supply row has blank required values")

    peak_forecast_header = _find_row_index(rows, lambda row: bool(row and row[0].startswith("予想最大電力(万kW)")))
    peak_forecast_row = _row_after(rows, peak_forecast_header)
    if len(peak_forecast_row) < 4:
        raise ValueError("TEPCO CSV section 2 peak demand forecast row is incomplete")
    peak_forecast_value = _parse_int(peak_forecast_row[0])
    if peak_forecast_value is None:
        raise ValueError("TEPCO CSV section 2 peak demand forecast value is blank")

    daily_max_usage_pct: float | None = None
    daily_max_usage_time_slot: str | None = None
    try:
        daily_max_header = _find_row_index(rows, lambda row: bool(row and row[0] == "最大使用率(%)"))
        daily_row = _row_after(rows, daily_max_header)
        daily_max_usage_pct = _parse_float(daily_row[0]) if daily_row else None
        daily_max_usage_time_slot = _normalize_time_slot(daily_row[1]) if len(daily_row) > 1 and daily_row[1].strip() else None
    except ValueError:
        pass

    service_date = _normalize_date(hourly_rows[1][0], update_year) if len(hourly_rows) > 1 else _normalize_date(supply_row[2], update_year)
    supply_update_utc, supply_update_local = _parse_section_update(supply_row[2], supply_row[3], update_year)
    supply_capacity = SupplyCapacityRecord(
        date=service_date,
        time=SUPPLY_CAPACITY_TIME_SENTINEL,
        peak_supply_capacity_mw=jp_unit_to_mw(supply_value),
        peak_supply_capacity_jp_unit_value=supply_value,
        peak_time_slot=_normalize_time_slot(supply_row[1]),
        peak_reserve_margin_pct=reserve_pct,
        peak_usage_pct=usage_pct,
        daily_max_usage_pct=daily_max_usage_pct,
        daily_max_usage_time_slot=daily_max_usage_time_slot,
        update_datetime=supply_update_utc,
        update_datetime_local=supply_update_local,
    )

    peak_update_utc, peak_update_local = _parse_section_update(peak_forecast_row[2], peak_forecast_row[3], update_year)
    peak_demand_forecast = PeakDemandForecastRecord(
        date=service_date,
        time=PEAK_FORECAST_TIME_SENTINEL,
        peak_demand_forecast_mw=jp_unit_to_mw(peak_forecast_value),
        peak_demand_forecast_jp_unit_value=peak_forecast_value,
        peak_time_slot=_normalize_time_slot(peak_forecast_row[1]),
        update_datetime=peak_update_utc,
        update_datetime_local=peak_update_local,
    )

    actuals: list[DemandActualRecord] = []
    forecasts: list[DemandForecastRecord] = []
    for row in hourly_rows[1:]:
        if len(row) < 6:
            continue
        date_value = _normalize_date(row[0], update_year)
        time_value = _normalize_time(row[1])
        utc_dt, local_dt = jst_to_rfc3339(date_value, time_value)
        hourly_usage_pct = _parse_float(row[4])
        supply_capacity_value = _parse_int(row[5])
        supply_capacity_mw = jp_unit_to_mw(supply_capacity_value) if supply_capacity_value is not None else None

        actual_value = _parse_int(row[2])
        if actual_value is not None and actual_value > 0:
            actuals.append(DemandActualRecord(
                date=date_value,
                time=time_value,
                datetime=utc_dt,
                datetime_local=local_dt,
                actual_demand_mw=jp_unit_to_mw(actual_value),
                actual_demand_jp_unit_value=actual_value,
                solar_generation_mw=None,
                solar_generation_jp_unit_value=None,
                solar_share_pct=None,
                usage_pct=hourly_usage_pct,
                supply_capacity_mw=supply_capacity_mw,
                supply_capacity_jp_unit_value=supply_capacity_value,
            ))

        forecast_value = _parse_int(row[3])
        if forecast_value is not None:
            forecasts.append(DemandForecastRecord(
                date=date_value,
                time=time_value,
                datetime=utc_dt,
                datetime_local=local_dt,
                forecast_demand_mw=jp_unit_to_mw(forecast_value),
                forecast_demand_jp_unit_value=forecast_value,
                usage_pct=hourly_usage_pct,
                supply_capacity_mw=supply_capacity_mw,
                supply_capacity_jp_unit_value=supply_capacity_value,
            ))

    for row in actual_rows[1:]:
        if len(row) < 3:
            continue
        actual_value = _parse_int(row[2])
        if actual_value is None or actual_value <= 0:
            continue
        date_value = _normalize_date(row[0], update_year)
        time_value = _normalize_time(row[1])
        utc_dt, local_dt = jst_to_rfc3339(date_value, time_value)
        solar_value = _parse_int(row[3]) if len(row) > 3 else None
        solar_share_pct = _parse_float(row[4]) if len(row) > 4 else None
        actuals.append(DemandActualRecord(
            date=date_value,
            time=time_value,
            datetime=utc_dt,
            datetime_local=local_dt,
            actual_demand_mw=jp_unit_to_mw(actual_value),
            actual_demand_jp_unit_value=actual_value,
            solar_generation_mw=jp_unit_to_mw(solar_value) if solar_value is not None else None,
            solar_generation_jp_unit_value=solar_value,
            solar_share_pct=solar_share_pct,
            usage_pct=None,
            supply_capacity_mw=None,
            supply_capacity_jp_unit_value=None,
        ))

    return DenkiyohoCsv(supply_capacity=supply_capacity, peak_demand_forecast=peak_demand_forecast, actuals=actuals, forecasts=forecasts)


def load_state(state_file: str) -> DenkiyohoState:
    try:
        path = Path(state_file)
        if path.exists():
            return DenkiyohoState.from_dict(json.loads(path.read_text(encoding="utf-8")))
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Could not load state from %s: %s", state_file, exc)
    return DenkiyohoState()


def save_state(state_file: str, state: DenkiyohoState) -> None:
    path = Path(state_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")


def supply_capacity_key(record: SupplyCapacityRecord) -> str:
    return f"{record.date}|{record.update_datetime}|{record.peak_supply_capacity_jp_unit_value}|{record.daily_max_usage_pct}"


def peak_forecast_key(record: PeakDemandForecastRecord) -> str:
    return f"{record.date}|{record.update_datetime}|{record.peak_demand_forecast_jp_unit_value}"


def actual_key(record: DemandActualRecord) -> str:
    return "|".join(str(value) for value in (
        record.date,
        record.time,
        record.actual_demand_jp_unit_value,
        record.solar_generation_jp_unit_value,
        record.solar_share_pct,
        record.usage_pct,
        record.supply_capacity_jp_unit_value,
    ))


def forecast_key(record: DemandForecastRecord) -> str:
    return f"{record.date}|{record.time}|{record.forecast_demand_jp_unit_value}|{record.usage_pct}|{record.supply_capacity_jp_unit_value}"


def _generated_kwargs(record: Any) -> dict[str, Any]:
    return dict(record.__dict__)


def _flush(producer: Any, timeout: float = 30.0) -> None:
    flush = getattr(producer, "flush", None)
    if flush is None and hasattr(producer, "producer"):
        flush = producer.producer.flush
    if flush is None:
        return
    remaining = flush(timeout=timeout)
    if remaining not in (None, 0):
        raise RuntimeError(f"Kafka producer flush left {remaining} message(s) undelivered")


class TepcoDenkiyohoAPI:
    def __init__(self, url: str = DAILY_CSV_URL, session: requests.Session | None = None):
        self.url = url
        self.session = session or create_retrying_session()
        self.session.headers["User-Agent"] = USER_AGENT

    def fetch_daily_csv(self) -> bytes:
        response = self.session.get(self.url, timeout=30)
        response.raise_for_status()
        return response.content

    def poll_once(self, event_producer: Any, state: DenkiyohoState) -> DenkiyohoState:
        parsed = parse_denkiyoho_csv(decode_shift_jis_csv(self.fetch_daily_csv()))
        next_state = state.clone()
        sent_counts = {"supply_capacity": 0, "peak_forecast": 0, "actual": 0, "forecast": 0}

        supply = parsed.supply_capacity
        if supply_capacity_key(supply) not in next_state.supply_capacity_seen:
            event_producer.send_jp_tepco_denkiyoho_kafka_supply_capacity(
                _feedurl=self.url,
                _area_code=supply.area_code,
                data=SupplyCapacity(**_generated_kwargs(supply)),
                flush_producer=False,
            )
            next_state.mark_supply_capacity(supply)
            sent_counts["supply_capacity"] += 1

        peak = parsed.peak_demand_forecast
        if peak_forecast_key(peak) not in next_state.peak_forecast_seen:
            event_producer.send_jp_tepco_denkiyoho_kafka_peak_demand_forecast(
                _feedurl=self.url,
                _area_code=peak.area_code,
                data=PeakDemandForecast(**_generated_kwargs(peak)),
                flush_producer=False,
            )
            next_state.mark_peak_forecast(peak)
            sent_counts["peak_forecast"] += 1

        for actual in parsed.actuals:
            if actual_key(actual) in next_state.actual_seen:
                continue
            event_producer.send_jp_tepco_denkiyoho_kafka_demand_actual(
                _feedurl=self.url,
                _area_code=actual.area_code,
                data=DemandActual(**_generated_kwargs(actual)),
                flush_producer=False,
            )
            next_state.mark_actual(actual)
            sent_counts["actual"] += 1

        for forecast in parsed.forecasts:
            if forecast_key(forecast) in next_state.forecast_seen:
                continue
            event_producer.send_jp_tepco_denkiyoho_kafka_demand_forecast(
                _feedurl=self.url,
                _area_code=forecast.area_code,
                data=DemandForecast(**_generated_kwargs(forecast)),
                flush_producer=False,
            )
            next_state.mark_forecast(forecast)
            sent_counts["forecast"] += 1

        _flush(event_producer)
        LOGGER.info(
            "Sent %(supply_capacity)d supply, %(peak_forecast)d peak forecast, %(actual)d actual, and %(forecast)d forecast events",
            sent_counts,
        )
        return next_state

    def parse_connection_string(self, connection_string: str) -> dict[str, str]:
        config: dict[str, str] = {}
        try:
            for part in connection_string.split(";"):
                if "Endpoint" in part:
                    config["bootstrap.servers"] = part.split("=", 1)[1].strip('"').strip().replace("sb://", "").replace("/", "") + ":9093"
                elif "EntityPath" in part:
                    config["kafka_topic"] = part.split("=", 1)[1].strip('"').strip()
                elif "SharedAccessKeyName" in part:
                    config["sasl.username"] = "$ConnectionString"
                elif "SharedAccessKey" in part:
                    config["sasl.password"] = connection_string.strip()
                elif "BootstrapServer" in part:
                    config["bootstrap.servers"] = part.split("=", 1)[1].strip()
        except IndexError as exc:
            raise ValueError("Invalid connection string format") from exc
        if "sasl.username" in config:
            config["security.protocol"] = "SASL_SSL"
            config["sasl.mechanisms"] = "PLAIN"
        return config

    def feed(self, kafka_config: dict[str, str], kafka_topic: str, polling_interval: int, state_file: str, once: bool = False) -> None:
        producer = Producer(kafka_config)
        event_producer = JPTEPCODenkiyohoKafkaEventProducer(producer, kafka_topic)
        state = load_state(state_file)
        while True:
            start = time_module.monotonic()
            try:
                state = self.poll_once(event_producer, state)
                save_state(state_file, state)
            except KeyboardInterrupt:
                LOGGER.info("Exiting...")
                break
            except Exception as exc:  # pylint: disable=broad-except
                LOGGER.exception("Polling cycle failed: %s", exc)
            if once:
                break
            sleep_seconds = max(0, polling_interval - (time_module.monotonic() - start))
            time_module.sleep(sleep_seconds)
        producer.flush()


def build_kafka_config(args: argparse.Namespace, api: TepcoDenkiyohoAPI) -> tuple[dict[str, str], str]:
    if args.connection_string:
        parsed = api.parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = parsed.get("bootstrap.servers")
        kafka_topic = parsed.get("kafka_topic") or args.kafka_topic
        sasl_username = parsed.get("sasl.username")
        sasl_password = parsed.get("sasl.password")
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not kafka_bootstrap_servers:
        raise ValueError("Kafka bootstrap servers must be provided either through arguments or CONNECTION_STRING")
    if not kafka_topic:
        kafka_topic = DEFAULT_TOPIC

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config: dict[str, str] = {"bootstrap.servers": kafka_bootstrap_servers}
    if sasl_username and sasl_password:
        kafka_config.update({
            "sasl.mechanisms": "PLAIN",
            "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
            "sasl.username": sasl_username,
            "sasl.password": sasl_password,
        })
    elif tls_enabled:
        kafka_config["security.protocol"] = "SSL"
    return kafka_config, kafka_topic


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch TEPCO Electricity Forecast CSV data and publish CloudEvents to Kafka.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Poll TEPCO CSV data and send CloudEvents")
    feed_parser.add_argument("--kafka-bootstrap-servers", default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic", default=os.getenv("KAFKA_TOPIC", DEFAULT_TOPIC))
    feed_parser.add_argument("--sasl-username", default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument("-c", "--connection-string", default=os.getenv("CONNECTION_STRING"))
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "300")))
    feed_parser.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE))
    feed_parser.add_argument("--url", default=os.getenv("TEPCO_DENKIYOHO_URL", DAILY_CSV_URL))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))

    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        return

    api = TepcoDenkiyohoAPI(url=args.url)
    try:
        kafka_config, kafka_topic = build_kafka_config(args, api)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    api.feed(kafka_config, kafka_topic, args.polling_interval, args.state_file, args.once)


if __name__ == "__main__":
    main()
