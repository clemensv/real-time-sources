"""NINA/BBK German civil protection warnings bridge."""

import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional

import aiohttp
from confluent_kafka import Producer

from nina_bbk_producer_data.civilwarning import CivilWarning  # pylint: disable=import-error
from nina_bbk_producer_kafka_producer.producer import NINAWarningsEventProducer  # pylint: disable=import-error

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

MAP_DATA_URL = "https://warnung.bund.de/api31/{provider}/mapData.json"
DETAIL_URL = "https://warnung.bund.de/api31/warnings/{warning_id}.json"

PROVIDERS = ["mowas", "katwarn", "biwapp", "dwd", "lhp", "police"]

DEFAULT_POLL_INTERVAL = 300
DEFAULT_STATE_FILE = os.path.expanduser("~/.nina_bbk_state.json")
DEFAULT_TOPIC = "nina-bbk"


def _safe_str(value: Any) -> Optional[str]:
    """Convert a value to string if not None."""
    if value is None:
        return None
    s = str(value).strip()
    return s if s else None


def _first_info(detail: dict) -> Optional[dict]:
    """Get the first info block from a CAP alert, preferring German then English."""
    infos = detail.get("info", [])
    if not infos:
        return None
    for info in infos:
        lang = (info.get("language") or "").lower()
        if lang in ("de", "de-de"):
            return info
    for info in infos:
        lang = (info.get("language") or "").lower()
        if lang.startswith("en"):
            return info
    return infos[0]


def _find_param(info: dict, name: str) -> Optional[str]:
    """Find a parameter value by valueName in an info block."""
    for param in info.get("parameter", []):
        if param.get("valueName") == name:
            return param.get("value")
    return None


def _find_event_code(info: dict) -> Optional[str]:
    """Find the BBK event code from an info block's eventCode list."""
    for ec in info.get("eventCode", []):
        if ec.get("valueName") == "profile:DE-BBK-EVENTCODE":
            return ec.get("value")
    return None


def _collect_areas(info: dict) -> str:
    """Collect area descriptions from an info block."""
    areas = info.get("area", [])
    descs = []
    for area in areas:
        desc = area.get("areaDesc")
        if desc:
            descs.append(desc)
    return "; ".join(descs)


def normalize_warning(detail: dict, provider: str, map_version: Optional[int] = None) -> Optional[CivilWarning]:
    """Normalize a NINA/BBK CAP detail into a CivilWarning data class."""
    warning_id = _safe_str(detail.get("identifier"))
    if not warning_id:
        return None

    info = _first_info(detail)
    if not info:
        return None

    sender = _safe_str(detail.get("sender"))
    sent = _safe_str(detail.get("sent"))
    status = _safe_str(detail.get("status"))
    msg_type = _safe_str(detail.get("msgType"))
    scope = _safe_str(detail.get("scope"))
    references = _safe_str(detail.get("references"))

    event = _safe_str(info.get("event"))
    event_code = _find_event_code(info)
    categories = info.get("category", [])
    category = categories[0] if categories else None
    severity = _safe_str(info.get("severity"))
    urgency = _safe_str(info.get("urgency"))
    certainty = _safe_str(info.get("certainty"))
    headline = _safe_str(info.get("headline"))
    description = _safe_str(info.get("description"))
    instruction = _safe_str(info.get("instruction"))
    web = _safe_str(info.get("web"))
    contact = _safe_str(info.get("contact"))
    language = _safe_str(info.get("language"))

    sender_name = _find_param(info, "sender_langname")
    verwaltungsbereiche = _find_param(info, "warnVerwaltungsbereiche")
    area_desc = _collect_areas(info)

    if not event or not severity or not urgency or not certainty:
        return None

    return CivilWarning(
        warning_id=warning_id,
        provider=provider,
        version=map_version,
        sender=sender,
        sender_name=sender_name,
        sent=sent,
        status=status,
        msg_type=msg_type,
        scope=scope,
        references=references,
        event=event,
        event_code=event_code,
        category=category,
        severity=severity,
        urgency=urgency,
        certainty=certainty,
        headline=headline,
        description=description,
        instruction=instruction,
        web=web,
        contact=contact,
        area_desc=area_desc if area_desc else None,
        verwaltungsbereiche=verwaltungsbereiche,
        language=language,
    )


class NINABBKPoller:
    """Polls NINA/BBK feeds and sends civil protection warnings to Kafka."""

    def __init__(self, kafka_config: Optional[Dict[str, str]] = None,
                 kafka_topic: str = DEFAULT_TOPIC,
                 state_file: str = DEFAULT_STATE_FILE,
                 poll_interval: int = DEFAULT_POLL_INTERVAL,
                 providers: Optional[List[str]] = None):
        self.kafka_topic = kafka_topic
        self.state_file = state_file
        self.poll_interval = poll_interval
        self.providers = providers or PROVIDERS
        self.event_producer: Optional[NINAWarningsEventProducer] = None
        if kafka_config is not None:
            producer = Producer(kafka_config)
            self.event_producer = NINAWarningsEventProducer(producer, kafka_topic)

    async def fetch_map_data(self, session: aiohttp.ClientSession, provider: str) -> List[dict]:
        """Fetch the map data (list of warning stubs) for a provider."""
        url = MAP_DATA_URL.format(provider=provider)
        try:
            async with session.get(url) as response:
                if response.status == 404:
                    return []
                response.raise_for_status()
                data = await response.json(content_type=None)
                return data if isinstance(data, list) else []
        except Exception:
            logger.warning("Failed to fetch map data for %s", provider, exc_info=True)
            return []

    async def fetch_detail(self, session: aiohttp.ClientSession, warning_id: str) -> Optional[dict]:
        """Fetch the full CAP detail for a warning."""
        url = DETAIL_URL.format(warning_id=warning_id)
        try:
            async with session.get(url) as response:
                if response.status == 404:
                    return None
                response.raise_for_status()
                return await response.json(content_type=None)
        except Exception:
            logger.warning("Failed to fetch detail for %s", warning_id, exc_info=True)
            return None

    def load_state(self) -> Dict[str, str]:
        """Load state tracking seen warning identifiers and versions."""
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

            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=60),
                headers={"User-Agent": "nina-bbk-bridge/1.0"}
            ) as session:
                for provider in self.providers:
                    try:
                        stubs = await self.fetch_map_data(session, provider)
                    except Exception:
                        logger.exception("Error fetching %s", provider)
                        continue

                    for stub in stubs:
                        wid = stub.get("id")
                        if not wid:
                            continue

                        version = stub.get("version")
                        version_str = str(version) if version is not None else ""
                        prev_version = state.get(wid)
                        if prev_version is not None and prev_version >= version_str:
                            continue

                        detail = await self.fetch_detail(session, wid)
                        if detail is None:
                            continue

                        warning = normalize_warning(detail, provider, version)
                        if warning is None:
                            continue

                        if prev_version is None:
                            count_new += 1
                        else:
                            count_updated += 1

                        if self.event_producer:
                            self.event_producer.send_nina_civil_warning(
                                _warning_id=warning.warning_id,
                                data=warning,
                                flush_producer=False,
                            )

                        state[wid] = version_str

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
    parser = argparse.ArgumentParser(description="NINA/BBK German civil protection warnings bridge")
    parser.add_argument("--connection-string", type=str, help="Event Hubs connection string")
    parser.add_argument("--bootstrap-servers", type=str, help="Kafka bootstrap servers")
    parser.add_argument("--topic", type=str, help="Kafka topic")
    parser.add_argument("--sasl-username", type=str, help="SASL username")
    parser.add_argument("--sasl-password", type=str, help="SASL password")
    parser.add_argument("--state-file", type=str, help="State file path")
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL, help="Poll interval in seconds")
    parser.add_argument("--providers", type=str, help="Comma-separated list of providers")
    parser.add_argument("--once", action="store_true", help="Poll once and exit")
    parser.add_argument("--log-level", type=str, default="INFO", help="Logging level")
    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv("NINA_BBK_CONNECTION_STRING") or os.getenv("CONNECTION_STRING")
    if not args.bootstrap_servers:
        args.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    if not args.topic:
        args.topic = os.getenv("KAFKA_TOPIC", DEFAULT_TOPIC)
    if not args.sasl_username:
        args.sasl_username = os.getenv("SASL_USERNAME")
    if not args.sasl_password:
        args.sasl_password = os.getenv("SASL_PASSWORD")
    if not args.state_file:
        args.state_file = os.getenv("NINA_BBK_STATE_FILE", DEFAULT_STATE_FILE)
    if os.getenv("LOG_LEVEL"):
        args.log_level = os.getenv("LOG_LEVEL")

    logging.getLogger().setLevel(args.log_level.upper())

    providers = None
    if args.providers:
        providers = [p.strip() for p in args.providers.split(",")]

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

    poller = NINABBKPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        state_file=args.state_file,
        poll_interval=args.poll_interval,
        providers=providers,
    )

    asyncio.run(poller.poll_and_send(once=args.once))


if __name__ == "__main__":
    main()
