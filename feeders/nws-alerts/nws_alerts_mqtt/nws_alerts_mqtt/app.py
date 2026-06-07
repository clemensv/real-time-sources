"""NWS CAP alerts -> MQTT/UNS bridge."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any, Optional
from urllib.parse import urlparse

import aiohttp
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from nws_alerts.nws_alerts import (
    DEFAULT_POLL_INTERVAL,
    DEFAULT_STATE_FILE,
    NWSAlertsPoller,
    normalize_alert,
    normalize_cap_severity,
    uns_slug,
)
from nws_alerts_mqtt_producer_data import WeatherAlert
from nws_alerts_mqtt_producer_mqtt_client.client import NWSAlertsMqttMqttClient

logger = logging.getLogger("nws_alerts_mqtt")

SEVERITY_METHODS = {
    "minor": "publish_nws_weather_alert_minor_mqtt",
    "moderate": "publish_nws_weather_alert_moderate_mqtt",
    "severe": "publish_nws_weather_alert_severe_mqtt",
    "extreme": "publish_nws_weather_alert_extreme_mqtt",
    "unknown": "publish_nws_weather_alert_unknown_mqtt",
}


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _parse_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in {"mqtts", "ssl", "tls"}
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls, parsed.username, parsed.password


def _to_mqtt_alert(alert: Any) -> WeatherAlert:
    return WeatherAlert(**alert.to_serializer_dict())


class NWSAlertsMqttBridge:
    """Polls NWS CAP alerts and publishes MQTT binary-mode CloudEvents."""

    def __init__(
        self,
        client: NWSAlertsMqttMqttClient,
        *,
        state_file: str = DEFAULT_STATE_FILE,
        poll_interval: int = DEFAULT_POLL_INTERVAL,
    ) -> None:
        self.client = client
        self.poller = NWSAlertsPoller(kafka_config=None, state_file=state_file, poll_interval=poll_interval)

    async def _publish_alert(self, alert: Any) -> None:
        severity = normalize_cap_severity(alert.severity)
        method = getattr(self.client, SEVERITY_METHODS[severity])
        await method(
            alert_id=uns_slug(alert.alert_id),
            state=uns_slug(alert.state),
            event_type=uns_slug(alert.event_type),
            data=_to_mqtt_alert(alert),
            qos=1,
            retain=False,
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
                await self._publish_alert(alert)
                state[alert.alert_id] = sent_str
                published += 1

            self.poller.save_state(state)
            logger.info("Published %d NWS alert MQTT events", published)
            if once:
                return
            await asyncio.sleep(self.poller.poll_interval)

    async def emit_mock_corpus(self) -> None:
        for props in _mock_alert_props():
            alert = normalize_alert(props)
            if alert is not None:
                await self._publish_alert(alert)


def _mock_alert_props() -> list[dict[str, Any]]:
    now = datetime(2026, 4, 7, 10, 0, tzinfo=timezone.utc).isoformat()
    severities = ["Minor", "Moderate", "Severe", "Extreme", "Unexpected"]
    events = ["Wind Advisory", "Flood Watch", "Tornado Warning", "Extreme Wind Warning", "Special Weather Statement"]
    states = ["CA", "TX", "MD", "OK", "AK"]
    corpus = []
    for index, (severity, event, state) in enumerate(zip(severities, events, states), start=1):
        corpus.append({
            "id": f"urn:oid:2.49.0.1.840.0.mock-{index}",
            "areaDesc": f"Mock {state} alert area",
            "geocode": {"UGC": [f"{state}C001"], "SAME": ["006001"]},
            "sent": now,
            "effective": now,
            "onset": now,
            "expires": datetime(2026, 4, 7, 20, 0, tzinfo=timezone.utc).isoformat(),
            "ends": datetime(2026, 4, 7, 22, 0, tzinfo=timezone.utc).isoformat(),
            "status": "Actual",
            "messageType": "Alert",
            "category": "Met",
            "severity": severity,
            "certainty": "Likely" if severity != "Unexpected" else "Unknown",
            "urgency": "Immediate",
            "event": event,
            "sender": "w-nws.webmaster@noaa.gov",
            "senderName": f"NWS Mock {state}",
            "headline": f"{event} for mock {state}",
            "description": "Synthetic NWS MQTT E2E alert.",
            "instruction": "This is a test alert.",
            "response": "None",
            "scope": "Public",
            "code": "IPAWSv1.0",
            "web": "https://api.weather.gov/alerts/mock",
            "parameters": {"NWSheadline": [event], "VTEC": [f"/O.NEW.KXXX.MOCK.{index:04d}/"]},
        })
    return corpus


async def _connect_client(args: argparse.Namespace) -> NWSAlertsMqttMqttClient:
    broker_host, broker_port, tls_from_url, url_user, url_password = _parse_broker_url(args.mqtt_broker_url)
    tls_enabled = args.mqtt_enable_tls or tls_from_url or broker_port == 8883
    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=args.mqtt_client_id or "nws-alerts-mqtt",
        protocol=MQTTv5,
    )
    auth_mode = (args.mqtt_auth_mode or "anonymous").lower()
    username = args.mqtt_username or url_user
    password = args.mqtt_password or url_password

    if auth_mode == "userpass":
        paho_client.username_pw_set(username or "", password or "")
    elif auth_mode == "tls-cert":
        tls_enabled = True
    elif auth_mode == "entra":
        paho_client.username_pw_set(username or args.mqtt_client_id or "nws-alerts-mqtt", "")

    if tls_enabled:
        if auth_mode == "tls-cert" and args.mqtt_client_cert:
            paho_client.tls_set(ca_certs=args.mqtt_ca_file, certfile=args.mqtt_client_cert, keyfile=args.mqtt_client_key)
        else:
            paho_client.tls_set(ca_certs=args.mqtt_ca_file)

    client = NWSAlertsMqttMqttClient(client=paho_client, content_mode="binary", loop=asyncio.get_running_loop())
    logger.info("Connecting to MQTT broker %s:%s (tls=%s, auth=%s)", broker_host, broker_port, tls_enabled, auth_mode)
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        from paho.mqtt.packettypes import PacketTypes
        from paho.mqtt.properties import Properties

        credential = ManagedIdentityCredential(client_id=args.mqtt_entra_client_id) if args.mqtt_entra_client_id else DefaultAzureCredential()
        token = credential.get_token(args.mqtt_entra_audience)
        props = Properties(PacketTypes.CONNECT)
        props.AuthenticationMethod = "OAUTH2-JWT"
        props.AuthenticationData = token.token.encode("utf-8")
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=props)
        paho_client.loop_start()
    else:
        await client.connect(broker_host, broker_port)
    return client


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NWS CAP alerts -> MQTT/UNS bridge")
    sub = parser.add_subparsers(dest="command")
    feed = sub.add_parser("feed", help="Poll NWS alerts and publish MQTT CloudEvents")
    feed.add_argument("--mqtt-broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed.add_argument("--mqtt-enable-tls", action="store_true", default=_env_bool("MQTT_ENABLE_TLS", False))
    feed.add_argument("--mqtt-auth-mode", default=os.getenv("MQTT_AUTH_MODE", "anonymous"))
    feed.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed.add_argument("--mqtt-client-cert", default=os.getenv("MQTT_CLIENT_CERT"))
    feed.add_argument("--mqtt-client-key", default=os.getenv("MQTT_CLIENT_KEY"))
    feed.add_argument("--mqtt-ca-file", default=os.getenv("MQTT_CA_FILE"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed.add_argument("--mqtt-entra-client-id", default=os.getenv("MQTT_ENTRA_CLIENT_ID"))
    feed.add_argument("--mqtt-entra-audience", default=os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/"))
    feed.add_argument("--state-file", default=os.getenv("NWS_STATE_FILE", DEFAULT_STATE_FILE))
    feed.add_argument("--poll-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", str(DEFAULT_POLL_INTERVAL))))
    feed.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    feed.add_argument("--emit-mock-corpus", action="store_true", default=_env_bool("NWS_ALERTS_MQTT_EMIT_MOCK_CORPUS", False))
    feed.add_argument("--log-level", default=os.getenv("LOG_LEVEL", "INFO"))
    return parser


async def _run(args: argparse.Namespace) -> None:
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
    client = await _connect_client(args)
    try:
        bridge = NWSAlertsMqttBridge(client, state_file=args.state_file, poll_interval=args.poll_interval)
        if args.emit_mock_corpus:
            await bridge.emit_mock_corpus()
            await asyncio.sleep(1.0)
            return
        await bridge.poll_and_publish(once=args.once)
    finally:
        await client.disconnect()


def main(argv: Optional[list[str]] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.print_help()
        return
    try:
        asyncio.run(_run(args))
    except KeyboardInterrupt:
        logger.info("Interrupted")


if __name__ == "__main__":
    main()

