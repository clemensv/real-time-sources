"""EPA UV bridge."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import time
from datetime import datetime
from typing import Dict, List, Tuple

import requests
from confluent_kafka import Producer

from epa_uv_producer_data import DailyForecast, HourlyForecast
from epa_uv_producer_kafka_producer.producer import USEPAUVIndexEventProducer

LOGGER = logging.getLogger(__name__)

HOURLY_URL = "https://data.epa.gov/dmapservice/getEnvirofactsUVHOURLY/CITY/{city}/STATE/{state}/JSON"
DAILY_URL = "https://data.epa.gov/dmapservice/getEnvirofactsUVDAILY/CITY/{city}/STATE/{state}/JSON"
DEFAULT_POLL_INTERVAL_SECONDS = 21600
MAX_SEEN_IDS = 20000


def slugify(text: str) -> str:
    """Convert a location label into a stable slug."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse Event Hubs/Fabric or plain Kafka connection strings."""
    config_dict: Dict[str, str] = {}
    if not connection_string:
        return config_dict
    try:
        for part in connection_string.split(";"):
            if "=" not in part:
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


def parse_locations(raw: str) -> List[Tuple[str, str]]:
    """Parse semicolon-separated CITY,STATE pairs."""
    values = [value.strip() for value in raw.split(";") if value.strip()]
    if not values:
        return [("Seattle", "WA")]
    parsed: List[Tuple[str, str]] = []
    for value in values:
        if "," not in value:
            raise ValueError(f"Invalid EPA_UV_LOCATIONS entry: {value}")
        city, state = value.rsplit(",", 1)
        parsed.append((city.strip(), state.strip().upper()))
    return parsed


def _load_state(state_file: str) -> dict:
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as handle:
                return json.load(handle)
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    if not state_file:
        return
    state_dir = os.path.dirname(state_file)
    if state_dir:
        os.makedirs(state_dir, exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def parse_hourly_row(city: str, state: str, row: dict) -> HourlyForecast:
    """Normalize one hourly API row."""
    location_id = slugify(f"{city}-{state}")
    parsed_dt = datetime.strptime(row["DATE_TIME"], "%b/%d/%Y %I %p")
    return HourlyForecast(
        location_id=location_id,
        city=city,
        state=state,
        forecast_datetime=parsed_dt.strftime("%Y-%m-%dT%H:%M:%S"),
        uv_index=int(row["UV_VALUE"]),
    )


def parse_daily_row(city: str, state: str, row: dict) -> DailyForecast:
    """Normalize one daily API row."""
    location_id = slugify(f"{city}-{state}")
    parsed_date = datetime.strptime(row["DATE"], "%b/%d/%Y")
    return DailyForecast(
        location_id=location_id,
        city=city,
        state=state,
        forecast_date=parsed_date.strftime("%Y-%m-%d"),
        uv_index=int(row["UV_INDEX"]),
        uv_alert=str(row["UV_ALERT"]),
    )


class EPAUVBridge:
    """Poll hourly and daily UV endpoints for configured locations."""

    def __init__(self, locations: List[Tuple[str, str]], state_file: str = ""):
        self.locations = locations
        self.state_file = state_file
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "GitHub-Copilot-CLI/1.0"})
        state = _load_state(state_file)
        self.hourly_order = [str(value) for value in state.get("seen_hourly_ids", [])][-MAX_SEEN_IDS:]
        self.daily_order = [str(value) for value in state.get("seen_daily_ids", [])][-MAX_SEEN_IDS:]
        self.seen_hourly_ids = set(self.hourly_order)
        self.seen_daily_ids = set(self.daily_order)

    def save_state(self) -> None:
        _save_state(
            self.state_file,
            {
                "seen_hourly_ids": self.hourly_order[-MAX_SEEN_IDS:],
                "seen_daily_ids": self.daily_order[-MAX_SEEN_IDS:],
            },
        )

    def _remember(self, order: List[str], seen: set[str], value: str) -> None:
        if value in seen:
            return
        seen.add(value)
        order.append(value)
        if len(order) > MAX_SEEN_IDS:
            removed = order.pop(0)
            seen.discard(removed)

    def fetch_hourly(self, city: str, state: str) -> List[HourlyForecast]:
        """Fetch hourly UV forecasts for one location."""
        response = self.session.get(HOURLY_URL.format(city=city, state=state), timeout=60)
        response.raise_for_status()
        rows = response.json()
        return [parse_hourly_row(city, state, row) for row in rows]

    def fetch_daily(self, city: str, state: str) -> List[DailyForecast]:
        """Fetch daily UV forecasts for one location."""
        response = self.session.get(DAILY_URL.format(city=city, state=state), timeout=60)
        response.raise_for_status()
        rows = response.json()
        return [parse_daily_row(city, state, row) for row in rows]

    def poll_and_send(self, producer: USEPAUVIndexEventProducer, once: bool = False) -> None:
        """Run the polling loop."""
        while True:
            try:
                hourly_sent = 0
                daily_sent = 0
                for city, state in self.locations:
                    for hourly in self.fetch_hourly(city, state):
                        event_id = f"{hourly.location_id}|{hourly.forecast_datetime}"
                        if event_id in self.seen_hourly_ids:
                            continue
                        producer.send_us_epa_uvindex_hourly_forecast(
                            hourly.location_id,
                            hourly,
                            flush_producer=False,
                        )
                        self._remember(self.hourly_order, self.seen_hourly_ids, event_id)
                        hourly_sent += 1
                    for daily in self.fetch_daily(city, state):
                        event_id = f"{daily.location_id}|{daily.forecast_date}"
                        if event_id in self.seen_daily_ids:
                            continue
                        producer.send_us_epa_uvindex_daily_forecast(
                            daily.location_id,
                            daily,
                            flush_producer=False,
                        )
                        self._remember(self.daily_order, self.seen_daily_ids, event_id)
                        daily_sent += 1
                producer.producer.flush()
                self.save_state()
                LOGGER.info("Sent %d hourly forecasts and %d daily forecasts", hourly_sent, daily_sent)
            except Exception as exc:  # pylint: disable=broad-except
                LOGGER.exception("Error during EPA UV poll: %s", exc)

            if once:
                return
            time.sleep(DEFAULT_POLL_INTERVAL_SECONDS)


def main() -> None:
    """CLI entry point."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="EPA UV bridge")
    parser.add_argument(
        "--connection-string",
        default=os.getenv("CONNECTION_STRING", ""),
        help="Kafka/Event Hubs/Fabric connection string",
    )
    parser.add_argument(
        "--locations",
        default=os.getenv("EPA_UV_LOCATIONS", "Seattle,WA"),
        help="Semicolon-separated CITY,STATE pairs",
    )
    parser.add_argument(
        "--state-file",
        default=os.getenv("EPA_UV_STATE_FILE", "/mnt/fileshare/epa_uv_state.json"),
        help="Path to the dedupe state file",
    )
    parser.add_argument("--once", action="store_true", help="Poll once and exit")
    args = parser.parse_args()

    kafka_config = parse_connection_string(args.connection_string)
    kafka_topic = kafka_config.pop("kafka_topic", None)
    if not kafka_config.get("bootstrap.servers") or not kafka_topic:
        raise ValueError("CONNECTION_STRING must provide bootstrap server and EntityPath")

    producer = Producer(kafka_config)
    event_producer = USEPAUVIndexEventProducer(producer, kafka_topic)
    EPAUVBridge(parse_locations(args.locations), state_file=args.state_file).poll_and_send(
        event_producer,
        once=args.once,
    )
