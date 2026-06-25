from __future__ import annotations

import argparse
import logging
import os
import time
from urllib.parse import urlparse

from jma_bosai_volcano_amqp_producer_amqp_producer.producer import JPJMAVolcanoAmqpProducer
from jma_bosai_volcano_amqp_producer_data import VolcanicEruption, VolcanicWarning, Volcano
from jma_bosai_volcano_amqp_producer_data.conditionenum import ConditionEnum
from jma_bosai_volcano_amqp_producer_data.eruptiontypeenum import EruptionTypeenum
from jma_bosai_volcano_core.jma_bosai_volcano import (
    DEFAULT_STATE_FILE,
    ERUPTION_URL,
    JMABosaiVolcanoSource,
    MockSource,
    VOLCANO_LIST_URL,
    WARNING_URL,
    _mock_enabled,
    load_state,
)

logger = logging.getLogger(__name__)


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _parse_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or "").lstrip("/") or None


def _build_amqp_producer(args):
    address = args.address
    if args.broker_url:
        host, port, tls, url_user, url_pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or url_user
        password = args.password or url_pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        address = path or address
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    kwargs = dict(host=host, address=address, port=port, content_mode=args.content_mode, use_tls=tls)
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

        kwargs.update(credential=ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential(), entra_audience=args.entra_audience)
    elif args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        kwargs.update(sas_key_name=args.sas_key_name, sas_key=args.sas_key)
    else:
        kwargs.update(username=username, password=password)
    return JPJMAVolcanoAmqpProducer(**kwargs)


def _volcano(record: dict) -> Volcano:
    return Volcano(**record)


def _warning(record: dict) -> VolcanicWarning:
    payload = dict(record)
    payload["condition"] = ConditionEnum[payload["condition"]]
    return VolcanicWarning(**payload)


def _eruption(record: dict) -> VolcanicEruption:
    payload = dict(record)
    if payload.get("eruption_type") is not None:
        payload["eruption_type"] = EruptionTypeenum[payload["eruption_type"]]
    return VolcanicEruption(**payload)


def _publish_cycle(source: JMABosaiVolcanoSource, state: dict[str, object], state_file: str, refresh_hours: int, producer: JPJMAVolcanoAmqpProducer) -> None:
    if source.should_refresh_reference(state, refresh_hours):
        for record in source.build_reference_records():
            data = _volcano(record)
            producer.send_volcano(data=data, _feedurl=VOLCANO_LIST_URL, _volcano_code=data.volcano_code, _prefecture=data.prefecture, _event=data.event)
        source.commit_reference_refresh(state, state_file)
    pending = source.collect_pending_telemetry(state)
    for record in pending.warnings:
        data = _warning(record)
        producer.send_volcanic_warning(data=data, _feedurl=WARNING_URL, _volcano_code=data.volcano_code, _prefecture=data.prefecture, _event=data.event)
    for record in pending.eruptions:
        data = _eruption(record)
        producer.send_volcanic_eruption(data=data, _feedurl=ERUPTION_URL, _volcano_code=data.volcano_code, _prefecture=data.prefecture, _event=data.event)
    if pending.warning_keys or pending.eruption_keys:
        source.commit_telemetry_state(state, state_file, pending.warning_keys, pending.eruption_keys)


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="jma-bosai-volcano AMQP 1.0 bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", "jma-bosai-volcano"))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("AMQP_TLS", False))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", "https://servicebus.azure.net/.default"))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "60")))
    parser.add_argument("--metadata-refresh-hours", type=int, default=int(os.getenv("VOLCANO_METADATA_REFRESH_HOURS", "720")))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE))
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")

    source = MockSource() if _mock_enabled() else JMABosaiVolcanoSource()
    state = load_state(args.state_file)
    producer = _build_amqp_producer(args)
    try:
        while True:
            _publish_cycle(source, state, args.state_file, args.metadata_refresh_hours, producer)
            if args.once or _mock_enabled():
                break
            time.sleep(args.polling_interval)
    finally:
        producer.close()
