"""OpenStreetMap minutely diffs -> MQTT/UNS bridge (firehose).

Polls the OSM replication state at
``https://planet.openstreetmap.org/replication/minute/state.txt``, fetches
the ``.osc.gz`` diff per sequence, parses the OsmChange XML, and republishes
each <node|way|relation> create/modify/delete as a non-retained QoS-0 MQTT 5
binary-mode CloudEvent on the topic families::

    osm/intl/wikimedia/wikimedia-osm-diffs/node/{geohash5}/{element_id}/change
    osm/intl/wikimedia/wikimedia-osm-diffs/way/{geohash5}/{element_id}/change
    osm/intl/wikimedia/wikimedia-osm-diffs/relation/{geohash5}/{element_id}/change

A retained side-channel summary of the last processed sequence is published to::

    osm/intl/wikimedia/wikimedia-osm-diffs/replication-state

Ways and relations carry no inline coordinates in OsmChange; the placeholder
``geohash5`` for those elements is the fixed sentinel ``nogeo``.
"""

from __future__ import annotations

import argparse
import asyncio
import datetime
import gzip
import io
import json
import logging
import os
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
import requests
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from wikimedia_osm_diffs_mqtt_producer_data import MapChange, ReplicationState
from wikimedia_osm_diffs_mqtt_producer_mqtt_client.client import (
    OrgOpenStreetMapDiffsMqttMqttClient,
)

from wikimedia_osm_diffs_mqtt.enrichment import geohash5

logger = logging.getLogger("wikimedia_osm_diffs_mqtt")

STATE_URL = "https://planet.openstreetmap.org/replication/minute/state.txt"
DIFF_BASE_URL = "https://planet.openstreetmap.org/replication/minute"
# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-wikimedia-osm-diffs/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)
DEFAULT_USER_AGENT = USER_AGENT
DEFAULT_STATE_FILE = os.path.expanduser("~/.wikimedia_osm_diffs_mqtt_state.json")


# ---------------------------------------------------------------------------
# OSM replication helpers (lifted from the Kafka bridge so the MQTT image
# is self-contained; both share the same xreg-defined dataclasses).
# ---------------------------------------------------------------------------


def parse_state_txt(text: str) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if key == "sequenceNumber":
            result["sequence_number"] = int(value)
        elif key == "timestamp":
            ts_str = value.replace("\\:", ":")
            if ts_str.endswith("Z"):
                ts_str = ts_str[:-1] + "+00:00"
            result["timestamp"] = datetime.datetime.fromisoformat(ts_str)
    return result


def sequence_to_path(seq: int) -> str:
    a = seq // 1_000_000
    b = (seq % 1_000_000) // 1_000
    c = seq % 1_000
    return f"{a:03d}/{b:03d}/{c:03d}"


def sequence_to_url(seq: int, base_url: str = DIFF_BASE_URL) -> str:
    return f"{base_url}/{sequence_to_path(seq)}.osc.gz"


def parse_osmchange_xml(xml_bytes: bytes, sequence_number: int) -> List[Dict[str, Any]]:
    """Parse an OsmChange XML payload into normalized change dicts."""
    changes: List[Dict[str, Any]] = []
    root = ET.fromstring(xml_bytes)
    for action in root:
        change_type = action.tag
        if change_type not in ("create", "modify", "delete"):
            continue
        for elem in action:
            element_type = elem.tag
            if element_type not in ("node", "way", "relation"):
                continue

            tags: Dict[str, str] = {}
            for child in elem:
                if child.tag == "tag":
                    k = child.get("k") or ""
                    v = child.get("v") or ""
                    tags[k] = v

            ts_attr = elem.get("timestamp")
            if ts_attr:
                ts_str = ts_attr
                if ts_str.endswith("Z"):
                    ts_str = ts_str[:-1] + "+00:00"
                ts = datetime.datetime.fromisoformat(ts_str)
            else:
                ts = datetime.datetime.now(datetime.timezone.utc)

            uid_str = elem.get("uid")
            user_id = int(uid_str) if uid_str else None
            user_name = elem.get("user") or None

            lat_str = elem.get("lat")
            lon_str = elem.get("lon")
            latitude = float(lat_str) if lat_str else None
            longitude = float(lon_str) if lon_str else None

            changes.append({
                "change_type": change_type,
                "element_type": element_type,
                "element_id": int(elem.get("id", "0")),
                "geohash5": _geohash5_for(element_type, latitude, longitude),
                "version": int(elem.get("version", "0")),
                "timestamp": ts,
                "changeset_id": int(elem.get("changeset", "0")),
                "user_name": user_name,
                "user_id": user_id,
                "latitude": latitude,
                "longitude": longitude,
                "tags": json.dumps(tags, separators=(",", ":"), ensure_ascii=False),
                "sequence_number": sequence_number,
            })
    return changes


def _geohash5_for(element_type: str, lat: Optional[float], lon: Optional[float]) -> str:
    """Resolve the 5-character geohash placeholder for a UNS topic segment.

    Nodes always have coordinates; ways and relations do not carry them in
    OsmChange. We emit the fixed ``nogeo`` sentinel whenever the coordinate
    pair cannot be resolved, so every topic placeholder has a non-empty
    lowercase ASCII value (never blank, never containing a slash).
    """
    if lat is None or lon is None:
        return "nogeo"
    gh = geohash5(lat, lon)
    return gh or "nogeo"


# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------


class StateStore:
    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def load(self) -> Optional[int]:
        if not self._path.exists():
            return None
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Failed to load state file %s: %s", self._path, exc)
            return None
        return payload.get("last_sequence_number")

    def save(self, last_sequence_number: int) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps({"last_sequence_number": last_sequence_number}, indent=2),
            encoding="utf-8",
        )


# ---------------------------------------------------------------------------
# Bridge
# ---------------------------------------------------------------------------


class OsmDiffsMqttBridge:
    def __init__(
        self,
        client: OrgOpenStreetMapDiffsMqttMqttClient,
        *,
        state_store: Optional[StateStore] = None,
        state_url: str = STATE_URL,
        diff_base_url: str = DIFF_BASE_URL,
        user_agent: str = DEFAULT_USER_AGENT,
        poll_interval: int = 60,
        max_retry_delay: int = 120,
        once: bool = False,
    ) -> None:
        self.client = client
        self._state_store = state_store
        self._state_url = state_url
        self._diff_base_url = diff_base_url
        self._poll_interval = poll_interval
        self._max_retry_delay = max_retry_delay
        self._once = once
        self._last_sequence = state_store.load() if state_store else None
        self._session = requests.Session()
        self._session.headers["User-Agent"] = user_agent
        self._total_events = 0

    async def run(self) -> None:
        retry_delay = 1
        while True:
            try:
                await self._poll_cycle()
                retry_delay = 1
                if self._once:
                    return
                await asyncio.sleep(self._poll_interval)
            except (asyncio.CancelledError, KeyboardInterrupt):
                raise
            except Exception as exc:
                logger.warning("Poll cycle error: %s. Retrying in %ds.", exc, retry_delay)
                if self._once:
                    return
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, self._max_retry_delay)

    async def _poll_cycle(self) -> None:
        state = self._fetch_state()
        if state is None:
            return
        current_seq = state["sequence_number"]
        current_ts = state["timestamp"]

        if self._last_sequence is not None and current_seq <= self._last_sequence:
            return

        start_seq = (self._last_sequence + 1) if self._last_sequence is not None else current_seq
        start_seq = max(start_seq, current_seq - 4)

        for seq in range(start_seq, current_seq + 1):
            await self._process_sequence(seq)

        await self._publish_replication_state(current_seq, current_ts)
        self._last_sequence = current_seq
        if self._state_store:
            self._state_store.save(current_seq)
        logger.info("Processed sequence %d (%d total events)", current_seq, self._total_events)

    def _fetch_state(self) -> Optional[Dict[str, Any]]:
        resp = self._session.get(self._state_url, timeout=30)
        resp.raise_for_status()
        return parse_state_txt(resp.text)

    async def _process_sequence(self, seq: int) -> None:
        url = sequence_to_url(seq, self._diff_base_url)
        logger.debug("Fetching %s", url)
        resp = self._session.get(url, timeout=60)
        resp.raise_for_status()
        xml_bytes = gzip.decompress(resp.content)
        for change in parse_osmchange_xml(xml_bytes, seq):
            await self._publish_change(change)

    async def _publish_change(self, change: Dict[str, Any]) -> None:
        data = MapChange(**change)
        element_type = change["element_type"]
        if element_type == "node":
            await self.client.publish_org_open_street_map_diffs_mqtt_node(
                geohash5=data.geohash5 or "nogeo",
                element_id=str(data.element_id),
                data=data,
                qos=0,
                retain=False,
            )
        elif element_type == "way":
            await self.client.publish_org_open_street_map_diffs_mqtt_way(
                geohash5=data.geohash5 or "nogeo",
                element_id=str(data.element_id),
                data=data,
                qos=0,
                retain=False,
            )
        elif element_type == "relation":
            await self.client.publish_org_open_street_map_diffs_mqtt_relation(
                geohash5=data.geohash5 or "nogeo",
                element_id=str(data.element_id),
                data=data,
                qos=0,
                retain=False,
            )
        else:
            return
        self._total_events += 1

    async def _publish_replication_state(self, seq: int, ts: datetime.datetime) -> None:
        state_data = ReplicationState(
            sequence_number=seq,
            timestamp=ts,
            source_url=sequence_to_url(seq, self._diff_base_url),
        )
        await self.client.publish_org_open_street_map_diffs_mqtt_replication_state(
            data=state_data, qos=0, retain=True,
        )

    async def emit_mock_corpus(self) -> None:
        """Publish one synthetic change per family + a replication-state."""
        seq = 6_500_000
        now = datetime.datetime.now(datetime.timezone.utc)

        node_change = {
            "change_type": "create",
            "element_type": "node",
            "element_id": 1234567890,
            "geohash5": _geohash5_for("node", 53.5511, 9.9937),
            "version": 1,
            "timestamp": now,
            "changeset_id": 987654321,
            "user_name": "mockuser",
            "user_id": 42,
            "latitude": 53.5511,
            "longitude": 9.9937,
            "tags": json.dumps({"amenity": "cafe", "name": "Mock Cafe"}, separators=(",", ":")),
            "sequence_number": seq,
        }
        way_change = {
            "change_type": "modify",
            "element_type": "way",
            "element_id": 222333444,
            "geohash5": _geohash5_for("way", None, None),
            "version": 7,
            "timestamp": now,
            "changeset_id": 987654322,
            "user_name": "mockuser",
            "user_id": 42,
            "latitude": None,
            "longitude": None,
            "tags": json.dumps({"highway": "residential", "name": "Mock Street"}, separators=(",", ":")),
            "sequence_number": seq,
        }
        relation_change = {
            "change_type": "delete",
            "element_type": "relation",
            "element_id": 555666,
            "geohash5": _geohash5_for("relation", None, None),
            "version": 3,
            "timestamp": now,
            "changeset_id": 987654323,
            "user_name": "mockuser",
            "user_id": 42,
            "latitude": None,
            "longitude": None,
            "tags": json.dumps({"type": "route", "route": "bus"}, separators=(",", ":")),
            "sequence_number": seq,
        }

        for change in (node_change, way_change, relation_change):
            await self._publish_change(change)
        await self._publish_replication_state(seq, now)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_broker(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    host = parsed.hostname or "localhost"
    port = parsed.port or (8883 if scheme == "mqtts" else 1883)
    return host, port, scheme == "mqtts"


async def _run(args: argparse.Namespace) -> None:
    broker_host, broker_port, tls = _parse_broker(args.mqtt_broker_url)
    tls = tls or args.mqtt_enable_tls

    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=args.mqtt_client_id or "",
        protocol=MQTTv5,
    )
    if args.mqtt_username:
        paho_client.username_pw_set(args.mqtt_username, args.mqtt_password or "")
    if tls:
        paho_client.tls_set()

    loop = asyncio.get_running_loop()
    client = OrgOpenStreetMapDiffsMqttMqttClient(
        client=paho_client,
        content_mode="binary",
        loop=loop,
    )
    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await client.connect(broker_host, broker_port)

    state_store = StateStore(args.state_file) if args.state_file else None
    bridge = OsmDiffsMqttBridge(
        client,
        state_store=state_store,
        state_url=args.state_url,
        diff_base_url=args.diff_base_url,
        poll_interval=args.poll_interval,
        once=args.once,
    )

    if args.mock:
        logger.info("Mock mode: emitting synthetic OSM corpus and exiting")
        await bridge.emit_mock_corpus()
        await asyncio.sleep(1.0)
        await client.disconnect()
        return

    try:
        await bridge.run()
    finally:
        await client.disconnect()


def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    p = argparse.ArgumentParser(description="OSM minutely diffs -> MQTT/UNS bridge")
    sub = p.add_subparsers(dest="command")

    feed = sub.add_parser("feed", help="Stream OSM diffs to MQTT")
    feed.add_argument("--mqtt-broker-url",
                      default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed.add_argument("--mqtt-enable-tls", action="store_true",
                      default=os.getenv("MQTT_ENABLE_TLS", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed.add_argument("--state-url", default=os.getenv("OSM_DIFFS_STATE_URL", STATE_URL))
    feed.add_argument("--diff-base-url",
                      default=os.getenv("OSM_DIFFS_BASE_URL", DIFF_BASE_URL))
    feed.add_argument("--state-file",
                      default=os.getenv("OSM_DIFFS_STATE_FILE", DEFAULT_STATE_FILE))
    feed.add_argument("--poll-interval", type=int,
                      default=int(os.getenv("OSM_DIFFS_POLL_INTERVAL", "60")))
    feed.add_argument("--once", action="store_true",
                      default=os.getenv("OSM_DIFFS_ONCE", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--mock", action="store_true",
                      default=os.getenv("OSM_DIFFS_MOCK", "false").lower() in ("true", "1", "yes"),
                      help="Skip OSM polling, emit one synthetic change per family + replication state, then exit")

    args = p.parse_args()
    if args.command != "feed":
        p.print_help()
        sys.exit(1)

    try:
        asyncio.run(_run(args))
    except KeyboardInterrupt:
        logger.info("Shutting down")


if __name__ == "__main__":
    main()
