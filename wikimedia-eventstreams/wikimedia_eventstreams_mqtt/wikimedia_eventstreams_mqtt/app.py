"""Wikimedia EventStreams firehose -> MQTT/UNS bridge.

Subscribes to the public ``mediawiki/recentchange`` SSE-style stream,
normalizes each event into the :class:`RecentChange` dataclass, and
republishes it as a non-retained QoS-0 MQTT 5 binary-mode CloudEvent
on the topic family

    social/intl/wikimedia/wikimedia-eventstreams/{wiki}/{namespace_bucket}/{event_id}/recent-change

The MediaWiki numeric ``namespace`` is mapped to a stable kebab-case
``namespace_bucket`` so subscribers can wildcard per wiki / namespace
without dragging integers through the UNS topic tree. Unrecognised
namespace numbers fall through to ``ns-<n>``.

Run with::

    python -m wikimedia_eventstreams_mqtt feed --mqtt-broker-url localhost:1883
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import aiohttp
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from wikimedia_eventstreams_mqtt_producer_data import RecentChange
from wikimedia_eventstreams_mqtt_producer_mqtt_client.client import (
    WikimediaEventStreamsMqttMqttClient,
)

logger = logging.getLogger("wikimedia_eventstreams_mqtt")


STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"
DEFAULT_USER_AGENT = (
    "real-time-sources-wikimedia-eventstreams-mqtt/0.1 "
    "(https://github.com/clemensv/real-time-sources)"
)


# MediaWiki canonical namespace numbers -> kebab-case bucket. Anything
# not listed here is bucketed as ``ns-<n>`` so the axis remains stable.
_NAMESPACE_BUCKETS: Dict[int, str] = {
    -2: "media",
    -1: "special",
    0: "main",
    1: "talk",
    2: "user",
    3: "user-talk",
    4: "project",
    5: "project-talk",
    6: "file",
    7: "file-talk",
    8: "mediawiki",
    9: "mediawiki-talk",
    10: "template",
    11: "template-talk",
    12: "help",
    13: "help-talk",
    14: "category",
    15: "category-talk",
    100: "portal",
    101: "portal-talk",
    118: "draft",
    119: "draft-talk",
    828: "module",
    829: "module-talk",
    1198: "translations",
    1199: "translations-talk",
}


def namespace_bucket(ns: Any) -> str:
    """Map a MediaWiki numeric namespace to a kebab-case bucket."""
    try:
        n = int(ns)
    except (TypeError, ValueError):
        return "unknown"
    return _NAMESPACE_BUCKETS.get(n, f"ns-{n}")


def _norm_segment(value: Optional[str]) -> str:
    if not value:
        return ""
    return str(value).strip().lower().replace("/", "_").replace("#", "_").replace("+", "_")


def _serialize_optional_json(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False, sort_keys=True)


def _stringify_optional(value: Any) -> Optional[str]:
    if value is None:
        return None
    return str(value)


def normalize_recent_change(change: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize an upstream recentchange payload for the generated RecentChange."""
    meta = change.get("meta") or {}
    length = change.get("length") or {}
    revision = change.get("revision") or {}
    ns = change.get("namespace")
    return {
        "event_id": _stringify_optional(meta.get("id")),
        "event_time": _stringify_optional(meta.get("dt")),
        "schema_uri": change.get("$schema"),
        "meta": {
            "uri": meta.get("uri"),
            "request_id": meta.get("request_id"),
            "id": _stringify_optional(meta.get("id")),
            "domain": meta.get("domain"),
            "stream": meta.get("stream"),
            "topic": meta.get("topic"),
            "partition": meta.get("partition"),
            "offset": _stringify_optional(meta.get("offset")),
            "dt": meta.get("dt"),
        },
        "id": _stringify_optional(change.get("id")),
        "type": change.get("type"),
        "namespace": ns,
        "namespace_bucket": namespace_bucket(ns),
        "title": change.get("title"),
        "title_url": change.get("title_url"),
        "comment": change.get("comment"),
        "timestamp": change.get("timestamp"),
        "user": change.get("user"),
        "bot": change.get("bot"),
        "minor": change.get("minor"),
        "patrolled": change.get("patrolled"),
        "length": {"old": length.get("old"), "new": length.get("new")},
        "revision": {
            "old": _stringify_optional(revision.get("old")),
            "new": _stringify_optional(revision.get("new")),
        },
        "server_url": change.get("server_url"),
        "server_name": change.get("server_name"),
        "server_script_path": change.get("server_script_path"),
        "wiki": change.get("wiki"),
        "parsedcomment": change.get("parsedcomment"),
        "notify_url": change.get("notify_url"),
        "log_type": change.get("log_type"),
        "log_action": change.get("log_action"),
        "log_action_comment": change.get("log_action_comment"),
        "log_id": _stringify_optional(change.get("log_id")),
        "log_params_json": _serialize_optional_json(change.get("log_params")),
    }


class WikimediaMqttBridge:
    """Pump Wikimedia recentchange SSE events to MQTT."""

    def __init__(
        self,
        client: WikimediaEventStreamsMqttMqttClient,
        *,
        stream_url: str = STREAM_URL,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        self.client = client
        self.stream_url = stream_url
        self.user_agent = user_agent
        self._count = 0

    async def publish_event(self, payload: Dict[str, Any]) -> bool:
        meta = payload.get("meta")
        if not isinstance(meta, dict):
            return False
        if meta.get("domain") == "canary":
            return False
        event_id = meta.get("id")
        event_time = meta.get("dt")
        wiki = payload.get("wiki")
        if not event_id or not event_time or not wiki:
            return False

        normalized = normalize_recent_change(payload)
        data = RecentChange.from_serializer_dict(normalized)

        await self.client.publish_wikimedia_event_streams_recent_change_mqtt(
            wiki=_norm_segment(wiki),
            namespace_bucket=_norm_segment(normalized["namespace_bucket"]),
            event_id=_norm_segment(str(event_id)),
            event_time=str(event_time),
            data=data,
            qos=0,
            retain=False,
        )
        self._count += 1
        return True

    async def run(self, max_events: Optional[int] = None) -> None:
        retry_delay = 1
        max_retry_delay = 60
        timeout = aiohttp.ClientTimeout(total=None, connect=30, sock_read=90)
        headers = {"Accept": "application/json", "User-Agent": self.user_agent}

        while True:
            try:
                async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
                    async with session.get(self.stream_url) as resp:
                        resp.raise_for_status()
                        logger.info("Connected to Wikimedia EventStreams at %s", self.stream_url)
                        retry_delay = 1
                        async for raw_line in resp.content:
                            line = raw_line.decode("utf-8", errors="replace").strip()
                            if not line or not line.startswith("data:"):
                                # EventStreams uses SSE; only `data:` lines carry payload
                                continue
                            try:
                                payload = json.loads(line[5:].strip())
                            except json.JSONDecodeError:
                                continue
                            try:
                                await self.publish_event(payload)
                            except Exception as exc:  # pragma: no cover - defensive
                                logger.warning("publish failed: %s", exc)
                                continue
                            if max_events and self._count >= max_events:
                                logger.info("max_events=%d reached, exiting", max_events)
                                return
            except (asyncio.CancelledError, KeyboardInterrupt):
                raise
            except Exception as exc:
                logger.error("EventStreams error: %s. Retrying in %ds", exc, retry_delay)
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, max_retry_delay)

    async def emit_mock_corpus(self) -> None:
        """Publish one synthetic recentchange per representative namespace bucket."""
        base_time = "2024-01-01T00:00:00Z"
        samples: List[Tuple[str, int, str]] = [
            ("enwiki",        0,  "mock-evt-en-main-0001"),
            ("commonswiki",   6,  "mock-evt-commons-file-0001"),
            ("wikidatawiki",  0,  "mock-evt-wd-main-0001"),
            ("dewiki",        14, "mock-evt-de-category-0001"),
        ]
        for wiki, ns, event_id in samples:
            payload = {
                "$schema": "/mediawiki/recentchange/1.0.0",
                "meta": {
                    "uri": f"https://{wiki}.example/wiki/Mock",
                    "request_id": "00000000-0000-0000-0000-000000000000",
                    "id": event_id,
                    "domain": f"{wiki}.example",
                    "stream": "mediawiki.recentchange",
                    "topic": "eqiad.mediawiki.recentchange",
                    "partition": 0,
                    "offset": "0",
                    "dt": base_time,
                },
                "id": 1,
                "type": "edit",
                "namespace": ns,
                "title": "Mock_Page",
                "title_url": f"https://{wiki}.example/wiki/Mock_Page",
                "comment": "synthetic mock event",
                "timestamp": 1_700_000_000,
                "user": "MockBot",
                "bot": True,
                "minor": False,
                "patrolled": True,
                "length": {"old": 100, "new": 120},
                "revision": {"old": 1000, "new": 1001},
                "server_url": f"https://{wiki}.example",
                "server_name": f"{wiki}.example",
                "server_script_path": "/w",
                "wiki": wiki,
                "parsedcomment": "synthetic mock event",
            }
            await self.publish_event(payload)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_broker(url: str) -> Tuple[str, int, bool]:
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
    client = WikimediaEventStreamsMqttMqttClient(
        client=paho_client,
        content_mode="binary",
        loop=loop,
    )
    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await client.connect(broker_host, broker_port)

    bridge = WikimediaMqttBridge(
        client,
        stream_url=args.stream_url,
        user_agent=args.user_agent,
    )

    if args.mock:
        logger.info("Mock mode: emitting synthetic Wikimedia corpus and exiting")
        await bridge.emit_mock_corpus()
        await asyncio.sleep(1.0)
        await client.disconnect()
        return

    try:
        await bridge.run(max_events=args.max_events)
    finally:
        await client.disconnect()


def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    p = argparse.ArgumentParser(description="Wikimedia EventStreams -> MQTT/UNS bridge")
    sub = p.add_subparsers(dest="command")

    feed = sub.add_parser("feed", help="Stream Wikimedia recentchange to MQTT")
    feed.add_argument("--mqtt-broker-url",
                      default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed.add_argument("--mqtt-enable-tls", action="store_true",
                      default=os.getenv("MQTT_ENABLE_TLS", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed.add_argument("--stream-url",
                      default=os.getenv("WIKIMEDIA_EVENTSTREAMS_URL", STREAM_URL))
    feed.add_argument("--user-agent",
                      default=os.getenv("WIKIMEDIA_EVENTSTREAMS_USER_AGENT", DEFAULT_USER_AGENT))
    feed.add_argument("--max-events", type=int,
                      default=int(os.getenv("WIKIMEDIA_EVENTSTREAMS_MAX_EVENTS", "0")) or None)
    feed.add_argument("--mock", action="store_true",
                      default=os.getenv("WIKIMEDIA_EVENTSTREAMS_MOCK", "false").lower() in ("true", "1", "yes"),
                      help="Skip live SSE, emit one synthetic event per namespace bucket, then exit")

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
