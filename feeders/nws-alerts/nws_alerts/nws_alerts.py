"""NWS CAP weather alerts bridge."""

import argparse
import asyncio
import json
import logging
import os
import sys
import unicodedata
from typing import Any, Dict, List, Optional

import aiohttp
from confluent_kafka import Producer

from nws_alerts_producer_data.weatheralert import WeatherAlert  # pylint: disable=import-error
from nws_alerts_producer_kafka_producer.producer import NWSAlertsEventProducer  # pylint: disable=import-error

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

NWS_API_URL = "https://api.weather.gov/alerts/active"
# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-nws-alerts/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

DEFAULT_POLL_INTERVAL = 60
DEFAULT_STATE_FILE = os.path.expanduser("~/.nws_alerts_state.json")
DEFAULT_TOPIC = "nws-alerts"

US_STATE_CODES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
    "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
    "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC", "PR", "VI", "GU", "AS", "MP",
}

FIPS_STATE_TO_POSTAL = {
    "01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA", "08": "CO", "09": "CT", "10": "DE",
    "11": "DC", "12": "FL", "13": "GA", "15": "HI", "16": "ID", "17": "IL", "18": "IN", "19": "IA",
    "20": "KS", "21": "KY", "22": "LA", "23": "ME", "24": "MD", "25": "MA", "26": "MI", "27": "MN",
    "28": "MS", "29": "MO", "30": "MT", "31": "NE", "32": "NV", "33": "NH", "34": "NJ", "35": "NM",
    "36": "NY", "37": "NC", "38": "ND", "39": "OH", "40": "OK", "41": "OR", "42": "PA", "44": "RI",
    "45": "SC", "46": "SD", "47": "TN", "48": "TX", "49": "UT", "50": "VT", "51": "VA", "53": "WA",
    "54": "WV", "55": "WI", "56": "WY", "60": "AS", "66": "GU", "69": "MP", "72": "PR", "78": "VI",
}


def _safe_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    s = str(value).strip()
    return s if s else None


def _join_codes(geocode: dict, key: str) -> Optional[str]:
    """Join geocode array values into semicolon-separated string."""
    values = geocode.get(key) if geocode else None
    if not values:
        return None
    return "; ".join(str(v) for v in values)


def uns_slug(value: Any) -> str:
    raw = unicodedata.normalize("NFKD", str(value or "unknown")).encode("ascii", "ignore").decode("ascii")
    raw = raw.lower().strip()
    out = [ch if ch.isalnum() else "-" for ch in raw]
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "unknown"


def normalize_cap_severity(value: Any) -> str:
    severity = uns_slug(value)
    return severity if severity in {"minor", "moderate", "severe", "extreme", "unknown"} else "unknown"


def derive_state(props: dict) -> str:
    explicit = _safe_str(props.get("state"))
    if explicit and explicit.upper() in US_STATE_CODES:
        return explicit.lower()

    geocode = props.get("geocode", {}) or {}
    for ugc in geocode.get("UGC") or []:
        code = str(ugc).strip().upper()
        if len(code) >= 2 and code[:2] in US_STATE_CODES:
            return code[:2].lower()

    for same in geocode.get("SAME") or []:
        digits = "".join(ch for ch in str(same) if ch.isdigit())
        fips_state = digits[1:3] if len(digits) >= 6 else digits[:2]
        state = FIPS_STATE_TO_POSTAL.get(fips_state)
        if state:
            return state.lower()

    sender_name = _safe_str(props.get("senderName"))
    if sender_name:
        maybe_state = sender_name.split()[-1].upper()
        if maybe_state in US_STATE_CODES:
            return maybe_state.lower()
    return "nostate"


def _find_nws_headline(params: dict) -> Optional[str]:
    """Extract NWSheadline from parameters."""
    if not params:
        return None
    for key in ("NWSheadline", "nwsheadline"):
        val = params.get(key)
        if val:
            return val[0] if isinstance(val, list) else str(val)
    return None


def _find_vtec(params: dict) -> Optional[str]:
    """Extract VTEC string from parameters."""
    if not params:
        return None
    val = params.get("VTEC")
    if val:
        return val[0] if isinstance(val, list) else str(val)
    return None


def normalize_alert(props: dict) -> Optional[WeatherAlert]:
    """Normalize a GeoJSON feature's properties into a WeatherAlert."""
    alert_id = _safe_str(props.get("id"))
    event = _safe_str(props.get("event"))
    severity = _safe_str(props.get("severity")) or "Unknown"
    if severity not in {"Extreme", "Severe", "Moderate", "Minor", "Unknown"}:
        severity = "Unknown"
    urgency = _safe_str(props.get("urgency"))
    certainty = _safe_str(props.get("certainty"))
    sent = _safe_str(props.get("sent"))
    status = _safe_str(props.get("status"))
    message_type = _safe_str(props.get("messageType"))

    if not alert_id or not event or not sent or not status:
        return None

    geocode = props.get("geocode", {})
    params = props.get("parameters", {})

    return WeatherAlert(
        alert_id=alert_id,
        state=derive_state(props),
        event_type=uns_slug(event),
        area_desc=_safe_str(props.get("areaDesc")),
        same_codes=_join_codes(geocode, "SAME"),
        ugc_codes=_join_codes(geocode, "UGC"),
        sent=sent,
        effective=_safe_str(props.get("effective")),
        onset=_safe_str(props.get("onset")),
        expires=_safe_str(props.get("expires")),
        ends=_safe_str(props.get("ends")),
        status=status,
        message_type=message_type,
        category=_safe_str(props.get("category")),
        severity=severity,
        certainty=certainty,
        urgency=urgency,
        event=event,
        sender=_safe_str(props.get("sender")),
        sender_name=_safe_str(props.get("senderName")),
        headline=_safe_str(props.get("headline")),
        description=_safe_str(props.get("description")),
        instruction=_safe_str(props.get("instruction")),
        response=_safe_str(props.get("response")),
        scope=_safe_str(props.get("scope")),
        code=_safe_str(props.get("code")),
        nws_headline=_find_nws_headline(params),
        vtec=_find_vtec(params),
        web=_safe_str(props.get("web")),
    )


class NWSAlertsPoller:
    """Polls the NWS alerts API and sends events to Kafka."""

    def __init__(self, kafka_config: Optional[Dict[str, str]] = None,
                 kafka_topic: str = DEFAULT_TOPIC,
                 state_file: str = DEFAULT_STATE_FILE,
                 poll_interval: int = DEFAULT_POLL_INTERVAL):
        self.kafka_topic = kafka_topic
        self.state_file = state_file
        self.poll_interval = poll_interval
        self.event_producer: Optional[NWSAlertsEventProducer] = None
        if kafka_config is not None:
            producer = Producer(kafka_config)
            self.event_producer = NWSAlertsEventProducer(producer, kafka_topic)

    async def fetch_alerts(self) -> List[dict]:
        """Fetch active alerts from the NWS API."""
        headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60), headers=headers) as session:
            async with session.get(NWS_API_URL) as response:
                response.raise_for_status()
                data = await response.json(content_type=None)
                return data.get("features", [])

    def load_state(self) -> Dict[str, str]:
        if self.state_file and os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def save_state(self, state: Dict[str, str]):
        if self.state_file:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(state, f)

    async def poll_and_send(self, once: bool = False):
        state = self.load_state()

        while True:
            try:
                features = await self.fetch_alerts()
            except Exception:
                logger.exception("Error fetching NWS alerts")
                if once:
                    return
                await asyncio.sleep(self.poll_interval)
                continue

            count_new = 0
            count_updated = 0

            for feature in features:
                props = feature.get("properties", {})
                alert = normalize_alert(props)
                if alert is None:
                    continue

                sent_str = alert.sent or ""
                prev_sent = state.get(alert.alert_id)
                if prev_sent is not None and prev_sent >= sent_str:
                    continue

                if prev_sent is None:
                    count_new += 1
                else:
                    count_updated += 1

                if self.event_producer:
                    self.event_producer.send_nws_weather_alert(
                        _alert_id=alert.alert_id,
                        data=alert,
                        flush_producer=False,
                    )

                state[alert.alert_id] = sent_str

            if self.event_producer:
                self.event_producer.producer.flush()
            self.save_state(state)

            if count_new > 0 or count_updated > 0:
                logger.info("Processed %d new and %d updated alerts", count_new, count_updated)
            else:
                logger.debug("No new alerts")

            if once:
                return

            await asyncio.sleep(self.poll_interval)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    config_dict: Dict[str, str] = {}
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
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


def main():
    parser = argparse.ArgumentParser(description="NWS CAP weather alerts bridge")
    parser.add_argument("--connection-string", type=str, help="Event Hubs connection string")
    parser.add_argument("--bootstrap-servers", type=str, help="Kafka bootstrap servers")
    parser.add_argument("--topic", type=str, help="Kafka topic")
    parser.add_argument("--sasl-username", type=str, help="SASL username")
    parser.add_argument("--sasl-password", type=str, help="SASL password")
    parser.add_argument("--state-file", type=str, help="State file path")
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL, help="Poll interval in seconds")
    parser.add_argument("--once", action="store_true", help="Poll once and exit")
    parser.add_argument("--log-level", type=str, default="INFO", help="Logging level")
    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv("NWS_CONNECTION_STRING") or os.getenv("CONNECTION_STRING")
    if not args.bootstrap_servers:
        args.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    if not args.topic:
        args.topic = os.getenv("KAFKA_TOPIC", DEFAULT_TOPIC)
    if not args.sasl_username:
        args.sasl_username = os.getenv("SASL_USERNAME")
    if not args.sasl_password:
        args.sasl_password = os.getenv("SASL_PASSWORD")
    if not args.state_file:
        args.state_file = os.getenv("NWS_STATE_FILE", DEFAULT_STATE_FILE)
    if os.getenv("LOG_LEVEL"):
        args.log_level = os.getenv("LOG_LEVEL")

    logging.getLogger().setLevel(args.log_level.upper())

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
        print("Error: Kafka bootstrap servers required.")
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

    poller = NWSAlertsPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        state_file=args.state_file,
        poll_interval=args.poll_interval,
    )

    asyncio.run(poller.poll_and_send(once=args.once))


if __name__ == "__main__":
    main()
