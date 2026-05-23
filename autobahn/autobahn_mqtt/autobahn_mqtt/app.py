"""Autobahn REST polling -> MQTT/UNS bridge."""

from __future__ import annotations

import argparse
import asyncio
import importlib
import json
import logging
import os
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable, Optional
from urllib.parse import urlparse

import aiohttp
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from autobahn.autobahn import (
    DEFAULT_POLL_INTERVAL_SECONDS,
    DEFAULT_REQUEST_CONCURRENCY,
    DEFAULT_RESOURCES,
    DEFAULT_STATE_FILE,
    EVENT_FAMILIES,
    SELECTION_SENTINEL,
    AutobahnPoller,
    build_family_snapshot,
    diff_items,
    merge_snapshots,
    parse_resources_argument,
    parse_roads_argument,
)
from autobahn_mqtt_producer_mqtt_client.client import DEAutobahnMqttMqttClient

logger = logging.getLogger("autobahn_mqtt")

STABLE_RETAINED_FAMILIES = {
    "weight_limit_35_restriction",
    "webcam",
    "parking_lorry",
    "electric_charging_station",
    "strong_electric_charging_station",
}


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _uns_slug(value: Any) -> str:
    raw = unicodedata.normalize("NFKD", str(value or "unknown")).encode("ascii", "ignore").decode("ascii")
    raw = raw.lower().strip()
    out = []
    for ch in raw:
        out.append(ch if ch.isalnum() else "-")
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "unknown"


def _parse_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in {"mqtts", "ssl", "tls"}
    port = parsed.port or (8883 if tls else 1883)
    host = parsed.hostname or "localhost"
    return host, port, tls, parsed.username, parsed.password


def _load_generated_data_classes() -> dict[str, type[Any]]:
    expected = {config["schema"] for config in EVENT_FAMILIES.values()}
    module = importlib.import_module("autobahn_mqtt_producer_data")
    found = {name: getattr(module, name) for name in expected if isinstance(getattr(module, name, None), type)}
    missing = sorted(expected - set(found))
    if missing:
        raise ImportError(f"Generated Autobahn MQTT data classes not found: {', '.join(missing)}")
    return found


class AutobahnMqttBridge:
    """Polls Autobahn REST resources and publishes MQTT lifecycle changes."""

    def __init__(
        self,
        client: DEAutobahnMqttMqttClient,
        *,
        state_file: str = DEFAULT_STATE_FILE,
        poll_interval_seconds: int = DEFAULT_POLL_INTERVAL_SECONDS,
        resources: Iterable[str] = DEFAULT_RESOURCES,
        roads: Optional[Iterable[str]] = None,
        request_concurrency: int = DEFAULT_REQUEST_CONCURRENCY,
    ) -> None:
        self.client = client
        self.poller = AutobahnPoller(
            kafka_config=None,
            state_file=state_file,
            poll_interval_seconds=poll_interval_seconds,
            resources=resources,
            roads=roads,
            request_concurrency=request_concurrency,
        )
        self.data_classes = _load_generated_data_classes()

    @property
    def state(self) -> dict[str, Any]:
        return self.poller.state

    def _data_for(self, family: str, action: str, snapshot: dict[str, Any], event_time: str) -> Any:
        if action == "resolved" and family in STABLE_RETAINED_FAMILIES:
            return None
        config = EVENT_FAMILIES[family]
        data_kwargs = dict(snapshot)
        road_value = snapshot.get("road") or (snapshot.get("road_ids") or ["unknown"])[0]
        data_kwargs["road"] = _uns_slug(road_value)
        data_kwargs["identifier"] = _uns_slug(snapshot["identifier"])
        data_kwargs["event_time"] = event_time
        return self.data_classes[config["schema"]](**data_kwargs)

    async def _publish_change(self, family: str, action: str, snapshot: dict[str, Any], poll_time: datetime) -> None:
        config = EVENT_FAMILIES[family]
        road = _uns_slug(snapshot.get("road") or (snapshot.get("road_ids") or ["unknown"])[0])
        identifier = _uns_slug(snapshot["identifier"])
        event_time = self.poller._get_event_time(action, snapshot, poll_time)  # pylint: disable=protected-access
        data = self._data_for(family, action, snapshot, event_time)
        method_name = f"publish_de_autobahn_{config['method_stem']}_{action}_mqtt"
        method = getattr(self.client, method_name)
        retain = family in STABLE_RETAINED_FAMILIES
        await method(identifier=identifier, event_time=event_time, road=road, data=data, qos=1, retain=retain)

    async def poll_once(self, session: aiohttp.ClientSession, poll_time: datetime) -> dict[str, dict[str, int]]:
        roads = self.poller.roads if self.poller.roads is not None else await self.poller.fetch_roads(session)
        tasks = [self.poller.fetch_resource(session, road_id, resource_type) for resource_type in self.poller.resources for road_id in roads]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result.error:
                logger.warning("Fetch failed for %s/%s: %s", result.road_id, result.resource_type, result.error)
                continue
            if result.status == 304:
                if result.etag:
                    self.state.setdefault("etags", {}).setdefault(result.resource_type, {})[result.road_id] = result.etag
                continue

            resource_state = self.state.setdefault("resource_items", {}).setdefault(result.resource_type, {})
            road_state: dict[str, dict[str, Any]] = {}
            for raw_item in result.items:
                if not isinstance(raw_item, dict):
                    continue
                built = build_family_snapshot(result.road_id, result.resource_type, raw_item)
                if built is None:
                    continue
                family, snapshot = built
                identifier = snapshot["identifier"]
                existing = road_state.get(identifier)
                entry = {"family": family, "snapshot": snapshot}
                if existing is None:
                    road_state[identifier] = entry
                else:
                    road_state[identifier] = {
                        "family": family,
                        "snapshot": merge_snapshots(existing["snapshot"], snapshot),
                    }
            resource_state[result.road_id] = road_state
            self.state.setdefault("etags", {}).setdefault(result.resource_type, {})[result.road_id] = result.etag

        current_by_family = self.poller._aggregate_current_items(roads)  # pylint: disable=protected-access
        changes_by_family = {family: {"appeared": 0, "updated": 0, "resolved": 0} for family in EVENT_FAMILIES}
        previous_by_family = self.state.setdefault("items", {})
        for family in EVENT_FAMILIES:
            previous = previous_by_family.get(family, {})
            current = current_by_family.get(family, {})
            for action, snapshots in diff_items(previous, current).items():
                for snapshot in snapshots:
                    await self._publish_change(family, action, snapshot, poll_time)
                    changes_by_family[family][action] += 1
            previous_by_family[family] = current

        self.poller.save_state()
        return changes_by_family

    async def poll_and_publish(self, once: bool = False) -> None:
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            while True:
                cycle_started = datetime.now(timezone.utc)
                changes = await self.poll_once(session, cycle_started)
                summary = self.poller._summarize_changes(changes)  # pylint: disable=protected-access
                logger.info("Autobahn MQTT cycle complete: %s", summary or "no changes")
                if once:
                    return
                elapsed = datetime.now(timezone.utc) - cycle_started
                remaining = timedelta(seconds=self.poller.poll_interval_seconds) - elapsed
                if remaining.total_seconds() > 0:
                    await asyncio.sleep(remaining.total_seconds())

    async def emit_mock_corpus(self) -> None:
        now = datetime(2024, 1, 1, tzinfo=timezone.utc)
        for index, family in enumerate(EVENT_FAMILIES, start=1):
            snapshot = _mock_snapshot(family, index)
            await self._publish_change(family, "appeared", snapshot, now)
            if family in STABLE_RETAINED_FAMILIES:
                resolved_snapshot = dict(snapshot)
                resolved_snapshot["identifier"] = f"{snapshot['identifier']}-resolved"
                await self._publish_change(family, "resolved", resolved_snapshot, now)


def _base_snapshot(family: str, index: int, display_type: str) -> dict[str, Any]:
    road = "A1" if index % 2 else "A 2"
    return {
        "identifier": f"{family}-MOCK-{index}",
        "road": road,
        "road_ids": [road],
        "display_type": display_type,
        "title": f"Mock {family}",
        "subtitle": "Synthetic Autobahn MQTT E2E record",
        "description_lines": ["Generated mock corpus item"],
        "future": False,
        "is_blocked": family in {"closure", "entry_exit_closure"},
        "icon": None,
        "start_lc_position": 1000 + index,
        "start_timestamp": "2024-01-01T00:00:00+00:00",
        "extent": None,
        "point": None,
        "coordinate_lat": 52.0 + index / 1000,
        "coordinate_lon": 13.0 + index / 1000,
        "geometry_json": None,
        "impact_lower": None,
        "impact_upper": None,
        "impact_symbols": [],
        "route_recommendation_json": None,
        "footer_lines": [],
    }


def _mock_snapshot(family: str, index: int) -> dict[str, Any]:
    display_type = next(iter(EVENT_FAMILIES[family]["display_types"]))
    base = _base_snapshot(family, index, display_type)
    if family == "warning":
        base.update({"delay_minutes": 5, "average_speed_kmh": 60, "abnormal_traffic_type": "SLOW_TRAFFIC", "source_name": "mock"})
    elif family == "parking_lorry":
        base.update({"amenity_descriptions": ["WC"], "car_space_count": 10, "lorry_space_count": 4})
    elif family in {"electric_charging_station", "strong_electric_charging_station"}:
        base.update({"address_line": "Autobahn service area", "charging_point_count": 2, "charging_points_json": "[]"})
    elif family == "webcam":
        base.update({"operator_name": "mock", "image_url": "https://example.invalid/image.jpg", "stream_url": None})
    return base


async def _connect_client(args: argparse.Namespace) -> DEAutobahnMqttMqttClient:
    broker_host, broker_port, tls_from_url, url_user, url_password = _parse_broker_url(args.mqtt_broker_url)
    tls_enabled = args.mqtt_enable_tls or tls_from_url or broker_port == 8883

    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=args.mqtt_client_id or "autobahn-mqtt",
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
        paho_client.username_pw_set(username or args.mqtt_client_id or "autobahn-mqtt", "")

    if tls_enabled:
        if auth_mode == "tls-cert" and args.mqtt_client_cert:
            paho_client.tls_set(ca_certs=args.mqtt_ca_file, certfile=args.mqtt_client_cert, keyfile=args.mqtt_client_key)
        else:
            paho_client.tls_set(ca_certs=args.mqtt_ca_file)

    loop = asyncio.get_running_loop()
    client = DEAutobahnMqttMqttClient(client=paho_client, content_mode="binary", loop=loop)

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
    parser = argparse.ArgumentParser(description="German Autobahn API -> MQTT/UNS bridge")
    sub = parser.add_subparsers(dest="command")
    feed = sub.add_parser("feed", help="Poll Autobahn and publish MQTT CloudEvents")
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
    feed.add_argument("--state-file", default=os.getenv("AUTOBAHN_STATE_FILE", DEFAULT_STATE_FILE))
    feed.add_argument("--poll-interval", type=int, default=int(os.getenv("AUTOBAHN_POLL_INTERVAL", str(DEFAULT_POLL_INTERVAL_SECONDS))))
    feed.add_argument("--resources", default=os.getenv("AUTOBAHN_RESOURCES", SELECTION_SENTINEL))
    feed.add_argument("--roads", default=os.getenv("AUTOBAHN_ROADS", SELECTION_SENTINEL))
    feed.add_argument("--request-concurrency", type=int, default=int(os.getenv("AUTOBAHN_REQUEST_CONCURRENCY", str(DEFAULT_REQUEST_CONCURRENCY))))
    feed.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    feed.add_argument("--emit-mock-corpus", action="store_true", default=_env_bool("AUTOBAHN_MQTT_EMIT_MOCK_CORPUS", False))
    feed.add_argument("--log-level", default=os.getenv("LOG_LEVEL", "INFO"))
    return parser


async def _run(args: argparse.Namespace) -> None:
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
    resources = parse_resources_argument(args.resources or SELECTION_SENTINEL)
    roads = parse_roads_argument(args.roads or SELECTION_SENTINEL)
    client = await _connect_client(args)
    try:
        bridge = AutobahnMqttBridge(
            client,
            state_file=args.state_file,
            poll_interval_seconds=args.poll_interval,
            resources=resources,
            roads=roads,
            request_concurrency=args.request_concurrency,
        )
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
        logger.info("Shutting down")


if __name__ == "__main__":
    main()
