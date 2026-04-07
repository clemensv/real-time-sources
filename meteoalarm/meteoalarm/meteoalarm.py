"""Meteoalarm European weather warnings bridge."""

import argparse
import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import aiohttp
from confluent_kafka import Producer

from meteoalarm_producer_data.weatherwarning import WeatherWarning  # pylint: disable=import-error
from meteoalarm_producer_kafka_producer.producer import MeteoalarmWarningsEventProducer  # pylint: disable=import-error

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

BASE_URL = "https://feeds.meteoalarm.org/api/v1/warnings/feeds-{country}"

DEFAULT_COUNTRIES = [
    "austria", "belgium", "bosnia-herzegovina", "bulgaria", "croatia",
    "cyprus", "czechia", "denmark", "estonia", "finland", "france",
    "germany", "greece", "hungary", "iceland", "ireland", "israel",
    "italy", "latvia", "lithuania", "luxembourg", "malta",
    "moldova", "montenegro", "netherlands", "north-macedonia", "norway",
    "poland", "portugal", "romania", "serbia", "slovakia", "slovenia",
    "spain", "sweden", "switzerland", "united-kingdom",
]

DEFAULT_POLL_INTERVAL = 300
DEFAULT_STATE_FILE = os.path.expanduser("~/.meteoalarm_state.json")
DEFAULT_TOPIC = "meteoalarm"


def _safe_str(value: Any) -> Optional[str]:
    """Convert a value to string if not None."""
    if value is None:
        return None
    s = str(value).strip()
    return s if s else None


def _first_info(alert_obj: dict) -> Optional[dict]:
    """Get the first info block from a CAP alert, preferring English."""
    infos = alert_obj.get("info", [])
    if not infos:
        return None
    # Prefer English info block
    for info in infos:
        lang = (info.get("language") or "").lower()
        if lang.startswith("en"):
            return info
    return infos[0]


def _collect_areas(info: dict) -> tuple[str, str]:
    """Collect area descriptions and geocodes from an info block."""
    areas = info.get("area", [])
    descs = []
    codes = []
    for area in areas:
        desc = area.get("areaDesc")
        if desc:
            descs.append(desc)
        for gc in area.get("geocode", []):
            val = gc.get("value")
            if val:
                codes.append(val)
    return "; ".join(descs), "; ".join(codes)


def _find_param(info: dict, name: str) -> Optional[str]:
    """Find a parameter value by valueName in an info block."""
    for param in info.get("parameter", []):
        if param.get("valueName") == name:
            return param.get("value")
    return None


def normalize_warning(alert_obj: dict, country: str) -> Optional[WeatherWarning]:
    """Normalize a Meteoalarm CAP alert JSON into a WeatherWarning data class."""
    identifier = _safe_str(alert_obj.get("identifier"))
    if not identifier:
        return None

    info = _first_info(alert_obj)
    if not info:
        return None

    sender = _safe_str(alert_obj.get("sender"))
    sent = _safe_str(alert_obj.get("sent"))
    status = _safe_str(alert_obj.get("status"))
    msg_type = _safe_str(alert_obj.get("msgType"))
    scope = _safe_str(alert_obj.get("scope"))

    event = _safe_str(info.get("event"))
    categories = info.get("category", [])
    category = categories[0] if categories else None
    severity = _safe_str(info.get("severity"))
    urgency = _safe_str(info.get("urgency"))
    certainty = _safe_str(info.get("certainty"))
    headline = _safe_str(info.get("headline"))
    description = _safe_str(info.get("description"))
    instruction = _safe_str(info.get("instruction"))
    effective = _safe_str(info.get("effective"))
    onset = _safe_str(info.get("onset"))
    expires = _safe_str(info.get("expires"))
    web = _safe_str(info.get("web"))
    contact = _safe_str(info.get("contact"))
    language = _safe_str(info.get("language"))

    awareness_level = _find_param(info, "awareness_level")
    awareness_type = _find_param(info, "awareness_type")

    area_desc, geocodes = _collect_areas(info)

    if not event or not severity or not urgency or not certainty:
        return None

    return WeatherWarning(
        identifier=identifier,
        sender=sender,
        sent=sent,
        status=status,
        msg_type=msg_type,
        scope=scope,
        country=country,
        event=event,
        category=category,
        severity=severity,
        urgency=urgency,
        certainty=certainty,
        headline=headline,
        description=description,
        instruction=instruction,
        effective=effective,
        onset=onset,
        expires=expires,
        web=web,
        contact=contact,
        awareness_level=awareness_level,
        awareness_type=awareness_type,
        area_desc=area_desc if area_desc else None,
        geocodes=geocodes if geocodes else None,
        language=language,
    )


class MeteoalarmPoller:
    """Polls Meteoalarm feeds and sends weather warnings to Kafka."""

    def __init__(self, kafka_config: Optional[Dict[str, str]] = None,
                 kafka_topic: str = DEFAULT_TOPIC,
                 state_file: str = DEFAULT_STATE_FILE,
                 poll_interval: int = DEFAULT_POLL_INTERVAL,
                 countries: Optional[List[str]] = None):
        self.kafka_topic = kafka_topic
        self.state_file = state_file
        self.poll_interval = poll_interval
        self.countries = countries or DEFAULT_COUNTRIES
        self.event_producer: Optional[MeteoalarmWarningsEventProducer] = None
        if kafka_config is not None:
            producer = Producer(kafka_config)
            self.event_producer = MeteoalarmWarningsEventProducer(producer, kafka_topic)

    async def fetch_country(self, session: aiohttp.ClientSession, country: str) -> List[dict]:
        """Fetch warnings for a single country."""
        url = BASE_URL.format(country=country)
        try:
            async with session.get(url) as response:
                if response.status == 404:
                    return []
                response.raise_for_status()
                data = await response.json(content_type=None)
                if isinstance(data, list):
                    return data
                return data.get("warnings", data) if isinstance(data, dict) else []
        except Exception:
            logger.warning("Failed to fetch %s", country, exc_info=True)
            return []

    def load_state(self) -> Dict[str, str]:
        """Load state tracking seen warning identifiers."""
        if self.state_file and os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def save_state(self, state: Dict[str, str]):
        """Persist state to disk."""
        if self.state_file:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(state, f)

    async def poll_and_send(self, once: bool = False):
        """Main poll loop."""
        state = self.load_state()

        while True:
            count_new = 0
            count_updated = 0

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
                for country in self.countries:
                    try:
                        raw_warnings = await self.fetch_country(session, country)
                    except Exception:
                        logger.exception("Error fetching %s", country)
                        continue

                    for item in raw_warnings:
                        alert_obj = item.get("alert", item)
                        warning = normalize_warning(alert_obj, country)
                        if warning is None:
                            continue

                        sent_str = warning.sent or ""
                        prev_sent = state.get(warning.identifier)
                        if prev_sent is not None and prev_sent >= sent_str:
                            continue

                        if prev_sent is None:
                            count_new += 1
                        else:
                            count_updated += 1

                        if self.event_producer:
                            await self.event_producer.send_meteoalarm_weather_warning(
                                _identifier=warning.identifier,
                                data=warning,
                                flush_producer=False,
                            )

                        state[warning.identifier] = sent_str

            if self.event_producer:
                self.event_producer.producer.flush()
            self.save_state(state)

            if count_new > 0 or count_updated > 0:
                logger.info("Processed %d new and %d updated warnings", count_new, count_updated)
            else:
                logger.debug("No new warnings")

            if once:
                return

            await asyncio.sleep(self.poll_interval)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Azure Event Hubs or Fabric Event Stream connection string."""
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=", 1)[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=", 1)[1].strip('"')
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = "$ConnectionString"
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = connection_string.strip()
            elif "BootstrapServer" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Meteoalarm European weather warnings bridge")
    parser.add_argument("--connection-string", type=str, help="Event Hubs connection string")
    parser.add_argument("--bootstrap-servers", type=str, help="Kafka bootstrap servers")
    parser.add_argument("--topic", type=str, help="Kafka topic")
    parser.add_argument("--sasl-username", type=str, help="SASL username")
    parser.add_argument("--sasl-password", type=str, help="SASL password")
    parser.add_argument("--state-file", type=str, help="State file path")
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL, help="Poll interval in seconds")
    parser.add_argument("--countries", type=str, help="Comma-separated list of countries")
    parser.add_argument("--once", action="store_true", help="Poll once and exit")
    parser.add_argument("--log-level", type=str, default="INFO", help="Logging level")
    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv("METEOALARM_CONNECTION_STRING") or os.getenv("CONNECTION_STRING")
    if not args.bootstrap_servers:
        args.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    if not args.topic:
        args.topic = os.getenv("KAFKA_TOPIC", DEFAULT_TOPIC)
    if not args.sasl_username:
        args.sasl_username = os.getenv("SASL_USERNAME")
    if not args.sasl_password:
        args.sasl_password = os.getenv("SASL_PASSWORD")
    if not args.state_file:
        args.state_file = os.getenv("METEOALARM_STATE_FILE", DEFAULT_STATE_FILE)
    if os.getenv("LOG_LEVEL"):
        args.log_level = os.getenv("LOG_LEVEL")

    logging.getLogger().setLevel(args.log_level.upper())

    countries = None
    if args.countries:
        countries = [c.strip() for c in args.countries.split(",")]

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        bootstrap_servers = config_params.get("bootstrap.servers")
        kafka_topic = config_params.get("kafka_topic", args.topic)
        sasl_username = config_params.get("sasl.username")
        sasl_password = config_params.get("sasl.password")
    else:
        bootstrap_servers = args.bootstrap_servers
        kafka_topic = args.topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not bootstrap_servers:
        print("Error: Kafka bootstrap servers required via --bootstrap-servers, --connection-string, or KAFKA_BOOTSTRAP_SERVERS.")
        sys.exit(1)
    if not kafka_topic:
        kafka_topic = DEFAULT_TOPIC

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config: Dict[str, str] = {"bootstrap.servers": bootstrap_servers}
    if sasl_username and sasl_password:
        kafka_config.update({
            "sasl.mechanisms": "PLAIN",
            "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
            "sasl.username": sasl_username,
            "sasl.password": sasl_password,
        })
    elif tls_enabled:
        kafka_config["security.protocol"] = "SSL"

    poller = MeteoalarmPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        state_file=args.state_file,
        poll_interval=args.poll_interval,
        countries=countries,
    )

    asyncio.run(poller.poll_and_send(once=args.once))


if __name__ == "__main__":
    main()
