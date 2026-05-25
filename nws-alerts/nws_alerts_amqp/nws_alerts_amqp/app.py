"""NWS CAP alerts -> AMQP 1.0 bridge."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any, Optional
from urllib.parse import urlparse

from nws_alerts.nws_alerts import DEFAULT_POLL_INTERVAL, DEFAULT_STATE_FILE, NWSAlertsPoller, normalize_alert, normalize_cap_severity, uns_slug
from nws_alerts_amqp_producer_data import WeatherAlert
from nws_alerts_amqp_producer_amqp_producer.producer import NWSAlertsAmqpProducer

logger = logging.getLogger("nws_alerts_amqp")
DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _parse_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in {"amqps", "ssl", "tls"}
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or "").lstrip("/") or None


def _to_amqp_alert(alert: Any) -> WeatherAlert:
    return WeatherAlert(**alert.to_serializer_dict())


def _build_producer(args: argparse.Namespace) -> NWSAlertsAmqpProducer:
    address = args.address
    if args.broker_url:
        host, port, tls, url_user, url_password, path = _parse_broker_url(args.broker_url)
        username = args.username or url_user
        password = args.password or url_password
        if path:
            address = path
        if args.port:
            port = args.port
        if args.tls:
            tls = True
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential()
        return NWSAlertsAmqpProducer(host=host, port=port, address=address, use_tls=tls, content_mode=args.content_mode, credential=credential, entra_audience=args.entra_audience)
    if args.auth_mode == "sas":
        return NWSAlertsAmqpProducer(host=host, port=port, address=address, use_tls=tls, content_mode=args.content_mode, sas_key_name=args.sas_key_name, sas_key=args.sas_key)
    return NWSAlertsAmqpProducer(host=host, port=port, address=address, username=username, password=password, use_tls=tls, content_mode=args.content_mode)


class NWSAlertsAmqpBridge:
    def __init__(self, producer: NWSAlertsAmqpProducer, *, state_file: str, poll_interval: int) -> None:
        self.producer = producer
        self.poller = NWSAlertsPoller(kafka_config=None, state_file=state_file, poll_interval=poll_interval)

    def _publish_alert(self, alert: Any) -> None:
        self.producer.send_amqp(
            data=_to_amqp_alert(alert),
            _alert_id=uns_slug(alert.alert_id),
            _state=uns_slug(alert.state),
            _severity=normalize_cap_severity(alert.severity),
            _event_type=uns_slug(alert.event_type),
        )

    async def poll_and_publish(self, once: bool = False) -> None:
        state = self.poller.load_state()
        while True:
            try:
                features = await self.poller.fetch_alerts()
            except Exception:
                logger.exception("Error fetching NWS alerts")
                if once:
                    return
                await asyncio.sleep(self.poller.poll_interval)
                continue
            published = 0
            for feature in features:
                alert = normalize_alert(feature.get("properties", {}))
                if alert is None:
                    continue
                sent_str = str(alert.sent or "")
                prev_sent = state.get(alert.alert_id)
                if prev_sent is not None and prev_sent >= sent_str:
                    continue
                self._publish_alert(alert)
                state[alert.alert_id] = sent_str
                published += 1
            self.poller.save_state(state)
            logger.info("Published %d NWS alert AMQP events", published)
            if once:
                return
            await asyncio.sleep(self.poller.poll_interval)

    def emit_mock_corpus(self) -> None:
        for props in _mock_alert_props():
            alert = normalize_alert(props)
            if alert is not None:
                self._publish_alert(alert)


def _mock_alert_props() -> list[dict[str, Any]]:
    now = datetime(2026, 4, 7, 10, 0, tzinfo=timezone.utc).isoformat()
    severities = ["Minor", "Moderate", "Severe", "Extreme", "Unexpected"]
    events = ["Wind Advisory", "Flood Watch", "Tornado Warning", "Extreme Wind Warning", "Special Weather Statement"]
    states = ["CA", "TX", "MD", "OK", "AK"]
    return [{
        "id": f"urn:oid:2.49.0.1.840.0.mock-{i}", "areaDesc": f"Mock {state} alert area",
        "geocode": {"UGC": [f"{state}C001"], "SAME": ["006001"]}, "sent": now, "effective": now, "onset": now,
        "expires": datetime(2026, 4, 7, 20, 0, tzinfo=timezone.utc).isoformat(), "ends": datetime(2026, 4, 7, 22, 0, tzinfo=timezone.utc).isoformat(),
        "status": "Actual", "messageType": "Alert", "category": "Met", "severity": severity,
        "certainty": "Likely" if severity != "Unexpected" else "Unknown", "urgency": "Immediate", "event": event,
        "sender": "w-nws.webmaster@noaa.gov", "senderName": f"NWS Mock {state}", "headline": f"{event} for mock {state}",
        "description": "Synthetic NWS AMQP E2E alert.", "instruction": "This is a test alert.", "response": "None", "scope": "Public",
        "code": "IPAWSv1.0", "web": "https://api.weather.gov/alerts/mock", "parameters": {"NWSheadline": [event], "VTEC": [f"/O.NEW.KXXX.MOCK.{i:04d}/"]},
    } for i, (severity, event, state) in enumerate(zip(severities, events, states), start=1)]


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NWS CAP alerts -> AMQP 1.0 bridge")
    sub = parser.add_subparsers(dest="command")
    feed = sub.add_parser("feed")
    feed.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    feed.add_argument("--host", default=os.getenv("AMQP_HOST"))
    feed.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    feed.add_argument("--address", default=os.getenv("AMQP_ADDRESS", "nws-alerts"))
    feed.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    feed.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    feed.add_argument("--tls", action="store_true", default=_env_bool("AMQP_TLS", False))
    feed.add_argument("--content-mode", choices=["binary", "structured"], default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    feed.add_argument("--auth-mode", choices=["password", "entra", "sas"], default=os.getenv("AMQP_AUTH_MODE", "password"))
    feed.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    feed.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    feed.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    feed.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    feed.add_argument("--state-file", default=os.getenv("NWS_STATE_FILE", DEFAULT_STATE_FILE))
    feed.add_argument("--poll-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", str(DEFAULT_POLL_INTERVAL))))
    feed.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    feed.add_argument("--emit-mock-corpus", action="store_true", default=_env_bool("NWS_ALERTS_AMQP_EMIT_MOCK_CORPUS", False))
    feed.add_argument("--log-level", default=os.getenv("LOG_LEVEL", "INFO"))
    return parser


async def _run(args: argparse.Namespace) -> None:
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
    producer = _build_producer(args)
    try:
        bridge = NWSAlertsAmqpBridge(producer, state_file=args.state_file, poll_interval=args.poll_interval)
        if args.emit_mock_corpus:
            bridge.emit_mock_corpus()
            return
        await bridge.poll_and_publish(once=args.once)
    finally:
        producer.close()


def main(argv: Optional[list[str]] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.print_help()
        return
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
