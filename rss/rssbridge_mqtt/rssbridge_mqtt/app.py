"""MQTT feeder application for RSS/Atom → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import typing
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
try:
    from paho.mqtt.properties import Properties as MqttProperties
    from paho.mqtt.packettypes import PacketTypes
except Exception:  # pragma: no cover
    MqttProperties = None  # type: ignore
    PacketTypes = None  # type: ignore
from cloudevents.conversion import to_binary, to_structured
from cloudevents.http import CloudEvent

from rssbridge.rssbridge import load_feedstore, load_state, poll_feeds, save_feedstore

logger = logging.getLogger(__name__)


def _apply_topic_template(template: str, values: dict[str, str]) -> str:
    result = template
    for key, value in values.items():
        result = result.replace("{" + key + "}", str(value))
    return result


class _NoopProducer:
    def flush(self) -> None:
        return None


class RssMqttProducer:
    producer = _NoopProducer()

    def __init__(self, client: mqtt.Client, *, content_mode: str = "binary"):
        self.client = client
        self.content_mode = content_mode

    def send_microsoft_open_data_rss_feeds_feed_item(self, *, _sourceurl: str, _item_id: str, data, flush_producer: bool = False) -> None:
        if not data.feed_slug or not data.item:
            raise ValueError("feed_slug and item must be populated before MQTT publish")
        topic = _apply_topic_template(
            "news/intl/rss/rss/{feed_slug}/{item}",
            {"feed_slug": data.feed_slug, "item": data.item},
        )
        attributes = {
            "type": "Microsoft.OpenData.RssFeeds.FeedItem",
            "source": _sourceurl,
            "subject": _item_id or data.item,
            "datacontenttype": "application/json",
        }
        payload = data.to_byte_array("application/json")
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        event = CloudEvent(attributes, payload)
        publish_kwargs: dict[str, typing.Any] = {"qos": 1, "retain": False}
        if self.content_mode == "structured":
            headers, body = to_structured(event)
            wire_payload = body
            if MqttProperties is not None:
                props = MqttProperties(PacketTypes.PUBLISH)
                props.ContentType = headers.get("content-type", "application/cloudevents+json")
                publish_kwargs["properties"] = props
        else:
            headers, body = to_binary(event)
            wire_payload = body
            if MqttProperties is not None:
                props = MqttProperties(PacketTypes.PUBLISH)
                user_properties = []
                for raw_key, value in dict(headers or {}).items():
                    key = str(raw_key).lower()
                    if key == "content-type":
                        props.ContentType = str(value)
                    elif key.startswith("ce-"):
                        user_properties.append((key[3:], str(value)))
                props.UserProperty = user_properties
                publish_kwargs["properties"] = props
        if isinstance(wire_payload, dict):
            import json
            wire_payload = json.dumps(wire_payload).encode("utf-8")
        elif isinstance(wire_payload, str):
            wire_payload = wire_payload.encode("utf-8")
        info = self.client.publish(topic, wire_payload, **publish_kwargs)
        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(f"MQTT publish to {topic!r} failed to queue: rc={info.rc}")
        info.wait_for_publish(timeout=30)
        if not info.is_published():
            raise TimeoutError(f"MQTT publish to {topic!r} timed out waiting for PUBACK")


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls


async def run() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="RSS/Atom MQTT/UNS bridge")
    parser.add_argument("process", nargs="?", default="process")
    parser.add_argument("urls", nargs="*", default=os.getenv("FEED_URLS", "").split(",") if os.getenv("FEED_URLS") else [])
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--state-dir", default=os.getenv("STATE_DIR", os.path.expanduser("~")))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", "rssbridge-mqtt"))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.process != "process":
        parser.error("only the 'process' command is supported")

    import rssbridge.rssbridge as bridge
    bridge.USER_DIR = args.state_dir
    bridge.STATE_FILE = os.path.join(args.state_dir, ".rss-grabber.json")
    bridge.FEEDSTORE_FILE = os.path.join(args.state_dir, ".rss-grabber-feedstore.xml")
    os.makedirs(args.state_dir, exist_ok=True)

    host, port, tls = _parse_broker_url(args.broker_url)
    paho_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=args.client_id, protocol=MQTTv5)
    if args.username:
        paho_client.username_pw_set(args.username, args.password or "")
    if tls:
        paho_client.tls_set()
    paho_client.connect(host, port)
    paho_client.loop_start()
    try:
        feed_urls = load_feedstore()
        feed_urls.extend([url for url in args.urls if url])
        if args.urls:
            save_feedstore(list(dict.fromkeys(feed_urls)))
        producer = RssMqttProducer(paho_client, content_mode=args.content_mode)
        await poll_feeds(list(dict.fromkeys(feed_urls)), load_state(), producer)
    finally:
        paho_client.loop_stop()
        paho_client.disconnect()


def main() -> None:
    asyncio.run(run())
