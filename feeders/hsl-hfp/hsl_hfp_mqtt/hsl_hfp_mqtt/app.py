"""HSL HFP -> MQTT / Unified-Namespace bridge.

Re-publishes the HSL HFP firehose as MQTT 5.0 binary-mode CloudEvents. Per the
*keep-structure* directive the downstream topic tree **mirrors the upstream HFP
tree** verbatim (``hfp/v2/journey/{temporal_type}/{event}/{transport_mode}/...``
for telemetry, ``hfp/v2/reference/{operator|route|stop}/{id}`` for the GTFS
reference events); the only change on the wire is the CloudEvents envelope, which
binary mode carries as MQTT 5 user properties.

Two broker auth modes, selected at runtime:

* **Generic MQTT broker** (Mosquitto, HiveMQ, EMQX, ...): anonymous or
  ``--username``/``--password`` over ``mqtt://`` (1883) or ``mqtts://`` (8883).
* **Azure Event Grid namespace** MQTT broker: ``MQTT_AUTH_MODE=entra`` acquires
  an Entra JWT from the instance-metadata endpoint and presents it via MQTT 5
  enhanced authentication (``OAUTH2-JWT``).

The generated ``publish_*`` coroutines never ``await`` -- they wrap the
synchronous ``paho`` ``client.publish`` -- so each is driven to completion on a
per-thread event loop. The per-thread loop keeps the periodic reference-refresh
thread isolated from the telemetry thread.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import threading
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt

from hsl_hfp.config import HFP_FEED_URL, FeedConfig
from hsl_hfp.runner import BridgeRunner
from hsl_hfp_mqtt_producer_data import (
    DriverBlockEvent,
    Operator,
    Route,
    Stop,
    TrafficLightEvent,
    VehicleEvent,
)
from hsl_hfp_mqtt_producer_mqtt_client.client import (
    FiHslGtfsOperatorMqttMqttClient,
    FiHslGtfsRouteMqttMqttClient,
    FiHslGtfsStopMqttMqttClient,
    FiHslHfpMqttMqttClient,
)

logger = logging.getLogger(__name__)

# Upstream HFP topic head levels (everything between the event-type level and
# the variable geohash tail). operator_id / vehicle_number are passed
# explicitly; these are the remaining downstream-topic placeholders.
_HEAD_KEYS = (
    "temporal_type",
    "transport_mode",
    "route_id",
    "direction_id",
    "headsign",
    "start_time",
    "next_stop",
    "geohash_level",
    "geohash",
)


def _fetch_entra_mqtt_token(audience: str, managed_identity_client_id: Optional[str] = None) -> str:
    params = {
        "api-version": "2018-02-01",
        "resource": audience or "https://eventgrid.azure.net/",
    }
    if managed_identity_client_id:
        params["client_id"] = managed_identity_client_id
    request = Request(
        "http://169.254.169.254/metadata/identity/oauth2/token?" + urlencode(params),
        headers={"Metadata": "true"},
    )
    with urlopen(request, timeout=30) as response:  # noqa: S310 - fixed IMDS host
        payload = json.loads(response.read().decode("utf-8"))
    token = payload.get("accessToken") or payload.get("access_token")
    if not token:
        raise RuntimeError("Entra IMDS token response did not contain an access token")
    return token


def _resolve_mqtt_connection_settings(
    *, username: str, password: str, client_id: str, auth_mode: Optional[str]
) -> Tuple[str, str, str, Optional[Any]]:
    """Return (client_id, username, password, connect_properties)."""
    if (auth_mode or "").lower() != "entra":
        return client_id, username, password, None

    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID")
    resolved_username = username or os.getenv("MQTT_CLIENT_ID") or client_id
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")

    token = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended
    # auth, not username/password.
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    from paho.mqtt.properties import Properties as _MqttConnProps

    connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
    connect_props.AuthenticationMethod = "OAUTH2-JWT"
    connect_props.AuthenticationData = token.encode("utf-8")
    return client_id, resolved_username, token, connect_props


class MqttSink:
    """Publishes HFP events as MQTT CloudEvents, mirroring the upstream topic tree."""

    def __init__(self, tele: FiHslHfpMqttMqttClient,
                 operator: FiHslGtfsOperatorMqttMqttClient,
                 route: FiHslGtfsRouteMqttMqttClient,
                 stop: FiHslGtfsStopMqttMqttClient,
                 feed_url: str) -> None:
        self._tele = tele
        self._operator = operator
        self._route = route
        self._stop = stop
        self._feed = feed_url
        self._tls = threading.local()

    def _loop(self) -> asyncio.AbstractEventLoop:
        loop = getattr(self._tls, "loop", None)
        if loop is None:
            loop = asyncio.new_event_loop()
            self._tls.loop = loop
        return loop

    def _drive(self, coro: Any) -> None:
        self._loop().run_until_complete(coro)

    @staticmethod
    def _head(params: Dict[str, Any]) -> Dict[str, str]:
        return {k: str(params.get(k, "")) for k in _HEAD_KEYS}

    # -- reference ----------------------------------------------------------

    def send_operator(self, operator_id: str, kwargs: Dict[str, Any]) -> None:
        self._drive(self._operator.publish_fi_hsl_gtfs_operator_mqtt_operator(
            feedurl=self._feed, operator_id=operator_id, data=Operator(**kwargs)))

    def send_route(self, route_id: str, kwargs: Dict[str, Any]) -> None:
        self._drive(self._route.publish_fi_hsl_gtfs_route_mqtt_route(
            feedurl=self._feed, route_id=route_id, data=Route(**kwargs)))

    def send_stop(self, stop_id: str, kwargs: Dict[str, Any]) -> None:
        self._drive(self._stop.publish_fi_hsl_gtfs_stop_mqtt_stop(
            feedurl=self._feed, stop_id=stop_id, data=Stop(**kwargs)))

    # -- telemetry ----------------------------------------------------------

    def send_vehicle(self, event_type: str, params: Dict[str, Any],
                     kwargs: Dict[str, Any]) -> None:
        method = getattr(self._tele, f"publish_fi_hsl_hfp_mqtt_{event_type}")
        self._drive(method(
            feedurl=self._feed, operator_id=params["operator_id"],
            vehicle_number=params["vehicle_number"], **self._head(params),
            data=VehicleEvent(**kwargs)))

    def send_traffic_light(self, event_type: str, params: Dict[str, Any],
                           kwargs: Dict[str, Any]) -> None:
        method = getattr(self._tele, f"publish_fi_hsl_hfp_mqtt_{event_type}")
        self._drive(method(
            feedurl=self._feed, operator_id=params["operator_id"],
            vehicle_number=params["vehicle_number"], **self._head(params),
            sid=str(params.get("sid", "")), data=TrafficLightEvent(**kwargs)))

    def send_driver_block(self, event_type: str, params: Dict[str, Any],
                          kwargs: Dict[str, Any]) -> None:
        method = getattr(self._tele, f"publish_fi_hsl_hfp_mqtt_{event_type}")
        self._drive(method(
            feedurl=self._feed, operator_id=params["operator_id"],
            vehicle_number=params["vehicle_number"], **self._head(params),
            data=DriverBlockEvent(**kwargs)))

    def flush(self) -> None:
        return

    def poll(self) -> None:
        return


def _parse_broker_url(url: str) -> Tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    host = parsed.hostname or "localhost"
    port = parsed.port or (8883 if tls else 1883)
    return host, port, tls


def _build_client(args: argparse.Namespace) -> mqtt.Client:
    host, port, tls_from_url = _parse_broker_url(args.broker_url)
    tls = tls_from_url if args.enable_tls is None else args.enable_tls

    client_id, username, password, connect_props = _resolve_mqtt_connection_settings(
        username=args.username or "",
        password=args.password or "",
        client_id=args.client_id or "",
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho_client = mqtt.Client(
        client_id=client_id or "",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        protocol=mqtt.MQTTv5,
    )
    if connect_props is None and (username or password):
        paho_client.username_pw_set(username, password)
    if tls or connect_props is not None:
        paho_client.tls_set(ca_certs=args.ca_file or None)

    connected = threading.Event()

    def _on_connack(client, userdata, flags, reason_code, props=None):  # noqa: ANN001
        code = reason_code if isinstance(reason_code, int) else reason_code.value
        if code == 0:
            connected.set()

    paho_client.on_connect = _on_connack
    paho_client.connect(host, port, keepalive=60, properties=connect_props)
    paho_client.loop_start()
    if not connected.wait(30):
        raise RuntimeError("MQTT CONNACK timeout after 30s")
    logger.info("Connected to downstream MQTT broker %s:%s (tls=%s)", host, port, tls)
    return paho_client


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HSL HFP -> MQTT/UNS bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Stream HFP telemetry as MQTT CloudEvents")
    feed_parser.add_argument("--broker-url", type=str,
                             default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"),
                             help="Downstream MQTT broker URL (mqtt://host:1883, mqtts://host:8883)")
    feed_parser.add_argument("--enable-tls", dest="enable_tls", action="store_true", default=None)
    feed_parser.add_argument("--disable-tls", dest="enable_tls", action="store_false")
    feed_parser.add_argument("--username", type=str, default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument("--ca-file", type=str, default=os.getenv("MQTT_CA_FILE"))
    feed_parser.add_argument("--client-id", type=str, default=os.getenv("MQTT_CLIENT_ID"))
    feed_parser.add_argument("--content-mode", type=str,
                             default=os.getenv("MQTT_CONTENT_MODE", "binary"),
                             choices=["binary", "structured"],
                             help="CloudEvents content mode for MQTT (default: binary)")
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                             help="Emit reference data and a bounded telemetry sample, then exit.")
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.command != "feed":
        parser.print_help()
        return

    paho_client = _build_client(args)
    tele = FiHslHfpMqttMqttClient(paho_client, content_mode=args.content_mode)  # type: ignore[arg-type]
    operator = FiHslGtfsOperatorMqttMqttClient(paho_client, content_mode=args.content_mode)  # type: ignore[arg-type]
    route = FiHslGtfsRouteMqttMqttClient(paho_client, content_mode=args.content_mode)  # type: ignore[arg-type]
    stop = FiHslGtfsStopMqttMqttClient(paho_client, content_mode=args.content_mode)  # type: ignore[arg-type]
    sink = MqttSink(tele, operator, route, stop, HFP_FEED_URL)

    config = FeedConfig.from_env()
    if args.once:
        config.once = True

    runner = BridgeRunner(config, feed_url=HFP_FEED_URL)
    logger.info("Starting HSL HFP -> MQTT bridge (content_mode=%s)", args.content_mode)
    try:
        runner.run(sink)
    finally:
        paho_client.loop_stop()
        paho_client.disconnect()


if __name__ == "__main__":
    main()
