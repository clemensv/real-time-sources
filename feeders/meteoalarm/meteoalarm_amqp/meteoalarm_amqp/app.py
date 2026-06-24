"""AMQP 1.0 feeder application for Meteoalarm warnings."""

from __future__ import annotations


import argparse
import logging
import os
from typing import Optional
from urllib.parse import urlparse

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


def _parse_amqp_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    return parsed.hostname or "localhost", port, tls, parsed.username or None, parsed.password or None, (parsed.path or "").lstrip("/") or None


def _build_amqp_producer(producer_cls, *, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username: Optional[str], password: Optional[str], entra_audience: str, entra_client_id: Optional[str], sas_key_name: Optional[str], sas_key: Optional[str]):
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return producer_cls(host=host, address=address, port=port, content_mode=content_mode, credential=credential, entra_audience=entra_audience, use_tls=use_tls)
    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return producer_cls(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)
    return producer_cls(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=use_tls)


def add_amqp_arguments(parser: argparse.ArgumentParser, default_address: str) -> None:
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", default_address))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))


def create_amqp_producer(args: argparse.Namespace, producer_cls):
    address = args.address
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_amqp_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        if path:
            address = path
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    if not address:
        raise RuntimeError("AMQP address is required")
    logging.info("Connecting AMQP producer to %s:%s/%s auth=%s tls=%s", host, port, address, args.auth_mode, tls)
    return _build_amqp_producer(producer_cls, host=host, port=port, address=address, use_tls=tls, content_mode=args.content_mode, auth_mode=args.auth_mode, username=username, password=password, entra_audience=args.entra_audience, entra_client_id=args.entra_client_id, sas_key_name=args.sas_key_name, sas_key=args.sas_key)


import argparse
import asyncio
import logging
import os
import time
from datetime import datetime, timezone

import aiohttp

from meteoalarm.meteoalarm import DEFAULT_COUNTRIES, DEFAULT_POLL_INTERVAL, DEFAULT_STATE_FILE, MeteoalarmPoller, normalize_warning
def _topic_segment(value):
    text = (str(value) if value is not None else "unknown").strip() or "unknown"
    for forbidden in ("/", "+", "#", "\x00"):
        text = text.replace(forbidden, "-")
    return "-".join(text.split()) or "unknown"
from meteoalarm_amqp_producer_data import CategoryEnum, CertaintyEnum, MsgTypeenum, ScopeEnum, SeverityEnum, StatusEnum, UrgencyEnum, WeatherWarning
from meteoalarm_amqp_producer_amqp_producer.producer import MeteoalarmWarningsAmqpProducer

logger = logging.getLogger(__name__)
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-meteoalarm/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)


def _sample_warning() -> WeatherWarning:
    return WeatherWarning(identifier="sample-warning", sender="sample@example.invalid", sent=datetime(2026, 1, 1, tzinfo=timezone.utc), status=StatusEnum.Actual, msg_type=MsgTypeenum.Alert, scope=ScopeEnum.Public, country="germany", event="Wind", category=CategoryEnum.Met, severity=SeverityEnum.Severe, urgency=UrgencyEnum.Expected, certainty=CertaintyEnum.Likely, headline="Sample wind warning", description="Sample warning for AMQP Docker E2E validation.", instruction="Avoid exposed areas.", effective=datetime(2026, 1, 1, tzinfo=timezone.utc), onset=datetime(2026, 1, 1, tzinfo=timezone.utc), expires=datetime(2026, 1, 2, tzinfo=timezone.utc), web="https://feeds.meteoalarm.org", contact=None, awareness_level="3; orange", awareness_type="wind", area_desc="Sample area", geocodes="DE000", language="en", awareness_type_raw="wind")


def _send(producer: MeteoalarmWarningsAmqpProducer, warning) -> None:
    producer.send_weather_warning(data=warning, _identifier=_topic_segment(warning.identifier), _country=_topic_segment(warning.country), _severity=_topic_segment(warning.severity.value if hasattr(warning.severity, "value") else warning.severity), _awareness_type=_topic_segment(warning.awareness_type))


async def _poll_once(poller: MeteoalarmPoller, producer: MeteoalarmWarningsAmqpProducer) -> int:
    state = poller.load_state()
    count = 0
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=60),
        headers={"User-Agent": USER_AGENT},
    ) as session:
        for country in poller.countries:
            raw_warnings = await poller.fetch_country(session, country)
            for item in raw_warnings:
                alert_obj = item.get("alert", item)
                warning = normalize_warning(alert_obj, country)
                if warning is None:
                    continue
                sent_str = warning.sent.isoformat() if warning.sent else ""
                if state.get(warning.identifier) is not None and state[warning.identifier] >= sent_str:
                    continue
                _send(producer, warning)
                state[warning.identifier] = sent_str
                count += 1
    poller.save_state(state)
    return count


async def feed(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args, MeteoalarmWarningsAmqpProducer)
    try:
        if args.mock_mode:
            _send(producer, _sample_warning())
            return
        poller = MeteoalarmPoller(kafka_config=None, kafka_topic="amqp", state_file=args.state_file, poll_interval=args.polling_interval, countries=args.countries)
        while True:
            started = time.monotonic()
            count = await _poll_once(poller, producer)
            logger.info("Published %d Meteoalarm warning(s) to AMQP", count)
            if args.once:
                break
            await asyncio.sleep(max(0, args.polling_interval - (time.monotonic() - started)))
    finally:
        producer.close()


def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            import time; time.sleep(delay)
def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Meteoalarm AMQP 1.0 bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    add_amqp_arguments(parser, "meteoalarm")
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", os.getenv("METEOALARM_POLL_INTERVAL", str(DEFAULT_POLL_INTERVAL)))))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE.replace(".json", "_amqp.json")))
    parser.add_argument("--countries", default=os.getenv("METEOALARM_COUNTRIES", ",".join(DEFAULT_COUNTRIES)))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--mock-mode", action="store_true", default=os.getenv("METEOALARM_MOCK", "").lower() in ("1", "true", "yes"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    args.countries = [part.strip() for part in args.countries.split(",") if part.strip()]
    asyncio.run(feed(args))


if __name__ == "__main__":
    main()
