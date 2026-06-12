"""MQTT feeder application for RSS/Atom → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import typing
from datetime import datetime, timezone
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
import json

def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
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
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    token = payload.get("accessToken") or payload.get("access_token")
    if not token:
        raise RuntimeError("IMDS token response did not contain an access token")
    return str(token)

def _resolve_mqtt_connection_settings(*, username=None, password=None, client_id=None, auth_mode=None):
    resolved_client_id = str(client_id or os.getenv("MQTT_CLIENT_ID") or "").strip()
    auth_mode = str(auth_mode or os.getenv("MQTT_AUTH_MODE", "password")).strip().lower() or "password"

    if auth_mode != "entra":
        return resolved_client_id, str(username or ""), str(password or ""), None

    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    resolved_username = resolved_client_id or str(username or "").strip()
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")

    resolved_password = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    from paho.mqtt.properties import Properties as _MqttConnProps
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    _connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
    _connect_props.AuthenticationMethod = "OAUTH2-JWT"
    _connect_props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, _connect_props

try:
    from paho.mqtt.properties import Properties as MqttProperties
    from paho.mqtt.packettypes import PacketTypes
except Exception:  # pragma: no cover
    MqttProperties = None  # type: ignore
    PacketTypes = None  # type: ignore
from cloudevents.conversion import to_binary, to_structured
from cloudevents.http import CloudEvent

from rssbridge.rssbridge import load_feedstore, load_state, poll_feeds, save_feedstore, save_state
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditem import FeedItem

logger = logging.getLogger(__name__)

def _apply_topic_template(template: str, values: dict[str, str]) -> str:
    result = template
    for key, value in values.items():
        result = result.replace("{" + key + "}", str(value))
    return result

class _NoopProducer:
    def flush(self) -> None:
        return None

def _drop_none(value):
    if isinstance(value, dict):
        return {k: _drop_none(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [_drop_none(v) for v in value if v is not None]
    return value

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
            "time": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "datacontenttype": "application/json",
        }
        payload_obj = _drop_none(data.to_serializer_dict())
        import json
        payload = json.dumps(payload_obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
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
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    args = parser.parse_args()
    if args.process != "process":
        parser.error("only the 'process' command is supported")

    import rssbridge.rssbridge as bridge
    bridge.USER_DIR = args.state_dir
    bridge.STATE_FILE = os.path.join(args.state_dir, ".rss-grabber.json")
    bridge.FEEDSTORE_FILE = os.path.join(args.state_dir, ".rss-grabber-feedstore.xml")
    os.makedirs(args.state_dir, exist_ok=True)

    host, port, tls = _parse_broker_url(args.broker_url)
    resolved_client_id, resolved_username, resolved_password, _entra_props = _resolve_mqtt_connection_settings(
        username=args.username,
        password=args.password or "",
        client_id=args.client_id,
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho_client = mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if _entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls or _entra_props is not None:
        paho_client.tls_set()
    # WORKAROUND(xregistry/codegen#432): pass Entra JWT CONNECT properties directly to paho
    if _entra_props is not None:
        paho_client.connect(host, port, keepalive=60, clean_start=True, properties=_entra_props)
    else:
        paho_client.connect(host, port)
    paho_client.loop_start()
    try:
        feed_urls = load_feedstore()
        feed_urls.extend([url for url in args.urls if url])
        if args.urls:
            save_feedstore(list(dict.fromkeys(feed_urls)))
        producer = RssMqttProducer(paho_client, content_mode=args.content_mode)
        if os.getenv("RSS_SAMPLE_MODE", "").lower() in ("1", "true", "yes"):
            producer.send_microsoft_open_data_rss_feeds_feed_item(
                _sourceurl="https://example.invalid/rss.xml",
                _item_id="sample-item",
                data=FeedItem(
                    feed_slug="sample-feed", item="sample-item", id="sample-item",
                    author=None, publisher=None, summary=None, title=None, source=None,
                    content=None, enclosures=None, published=None, updated=None, created=None,
                    expired=None, license=None, comments=None, contributors=None, links=None,
                ),
            )
            return
        state = load_state()
        unique_feed_urls = list(dict.fromkeys(feed_urls))
        if args.once:
            for feed_url in unique_feed_urls:
                bridge.process_feed(feed_url, state, producer)
            save_state(state)
        else:
            await poll_feeds(unique_feed_urls, state, producer)
    finally:
        paho_client.loop_stop()
        paho_client.disconnect()

def main() -> None:
    asyncio.run(run())
