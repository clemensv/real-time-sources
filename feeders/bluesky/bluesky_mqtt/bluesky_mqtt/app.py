"""MQTT feeder for the Bluesky AT Protocol firehose.

Connects to the public ``com.atproto.sync.subscribeRepos`` firehose, decodes
each commit into typed records, and republishes them as MQTT 5 binary-mode
CloudEvents on the Unified Namespace topic family

    social/intl/bluesky/bluesky/{collection}/{lang}/{did}/{event}

QoS 0, retain=False — there is no LKV slot for a firehose. Every required
topic placeholder is materialized in the record payload so the generated
producer can resolve the URI template, and so subscribers can rely on
round-trip consistency with the payload.

Run with::

    python -m bluesky_mqtt feed --mqtt-broker-url localhost:1883
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, Iterable, Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import aiohttp
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from bluesky_mqtt_producer_data import Block, Follow, Like, Post, Profile, Repost
from bluesky_mqtt_producer_mqtt_client.client import BlueskyFirehoseMqttMqttClient

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

# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-bluesky/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

logger = logging.getLogger("bluesky_mqtt")

# ---------------------------------------------------------------------------
# Topic placeholder normalization
# ---------------------------------------------------------------------------

_UNDETERMINED_LANG = "und"

def _norm_segment(value: Optional[str]) -> str:
    """Normalize a topic segment to lowercase ASCII without slashes."""
    if not value:
        return ""
    return str(value).strip().lower().replace("/", "_").replace("#", "_").replace("+", "_")

def _pick_lang(record: Dict[str, Any]) -> str:
    langs = record.get("langs") or []
    if isinstance(langs, list) and langs:
        return _norm_segment(langs[0]) or _UNDETERMINED_LANG
    return _UNDETERMINED_LANG

def _safe_get_link(field_value: Any) -> Optional[str]:
    if not field_value or isinstance(field_value, bytes):
        return None
    if isinstance(field_value, dict):
        ref = field_value.get("ref")
        if isinstance(ref, dict):
            return ref.get("$link")
    return None

# ---------------------------------------------------------------------------
# Record -> dataclass builders. Each must populate `collection` and `lang`
# so the MQTT topic placeholders resolve to a real payload field (see
# the xRegistry keying instructions).
# ---------------------------------------------------------------------------

def _build_post(commit, uri, record: Dict[str, Any], cid) -> Post:
    reply = record.get("reply") or {}
    reply_parent = reply.get("parent") or {}
    reply_root = reply.get("root") or {}
    embed = record.get("embed") or {}
    embed_type = embed.get("$type")
    embed_uri = None
    if embed_type == "app.bsky.embed.external":
        embed_uri = (embed.get("external") or {}).get("uri")
    elif embed_type == "app.bsky.embed.record":
        embed_uri = (embed.get("record") or {}).get("uri")
    elif embed_type == "app.bsky.embed.recordWithMedia":
        embed_uri = ((embed.get("record") or {}).get("record") or {}).get("uri")
    return Post(
        uri=str(uri),
        cid=str(cid) if cid else "",
        did=commit.repo,
        handle=None,
        text=record.get("text", ""),
        langs=[str(x) for x in (record.get("langs") or [])],
        reply_parent=reply_parent.get("uri"),
        reply_root=reply_root.get("uri"),
        embed_type=embed_type,
        embed_uri=embed_uri,
        facets=json.dumps(record.get("facets")) if record.get("facets") else None,
        tags=[str(x) for x in (record.get("tags") or [])],
        created_at=record.get("createdAt", ""),
        indexed_at=getattr(commit, "time", "") or "",
        seq=getattr(commit, "seq", 0) or 0,
        collection="app.bsky.feed.post",
        lang=_pick_lang(record),
    )

def _build_like(commit, uri, record: Dict[str, Any], cid) -> Like:
    subject = record.get("subject") or {}
    return Like(
        uri=str(uri),
        cid=str(cid) if cid else "",
        did=commit.repo,
        handle=None,
        subject_uri=subject.get("uri", ""),
        subject_cid=subject.get("cid", ""),
        created_at=record.get("createdAt", ""),
        indexed_at=getattr(commit, "time", "") or "",
        seq=getattr(commit, "seq", 0) or 0,
        collection="app.bsky.feed.like",
        lang=_UNDETERMINED_LANG,
    )

def _build_repost(commit, uri, record, cid) -> Repost:
    subject = record.get("subject") or {}
    return Repost(
        uri=str(uri),
        cid=str(cid) if cid else "",
        did=commit.repo,
        handle=None,
        subject_uri=subject.get("uri", ""),
        subject_cid=subject.get("cid", ""),
        created_at=record.get("createdAt", ""),
        indexed_at=getattr(commit, "time", "") or "",
        seq=getattr(commit, "seq", 0) or 0,
        collection="app.bsky.feed.repost",
        lang=_UNDETERMINED_LANG,
    )

def _build_follow(commit, uri, record, cid) -> Follow:
    return Follow(
        uri=str(uri),
        cid=str(cid) if cid else "",
        did=commit.repo,
        handle=None,
        subject=record.get("subject", ""),
        subject_handle=None,
        created_at=record.get("createdAt", ""),
        indexed_at=getattr(commit, "time", "") or "",
        seq=getattr(commit, "seq", 0) or 0,
        collection="app.bsky.graph.follow",
        lang=_UNDETERMINED_LANG,
    )

def _build_block(commit, uri, record, cid) -> Block:
    return Block(
        uri=str(uri),
        cid=str(cid) if cid else "",
        did=commit.repo,
        handle=None,
        subject=record.get("subject", ""),
        subject_handle=None,
        created_at=record.get("createdAt", ""),
        indexed_at=getattr(commit, "time", "") or "",
        seq=getattr(commit, "seq", 0) or 0,
        collection="app.bsky.graph.block",
        lang=_UNDETERMINED_LANG,
    )

def _build_profile(commit, record: Dict[str, Any]) -> Profile:
    return Profile(
        did=commit.repo,
        handle=None,
        display_name=record.get("displayName"),
        description=record.get("description"),
        avatar=_safe_get_link(record.get("avatar")),
        banner=_safe_get_link(record.get("banner")),
        created_at=record.get("createdAt", "") or "",
        indexed_at=getattr(commit, "time", "") or "",
        seq=getattr(commit, "seq", 0) or 0,
        collection="app.bsky.actor.profile",
        lang=_UNDETERMINED_LANG,
    )

# ---------------------------------------------------------------------------
# Bridge
# ---------------------------------------------------------------------------

class BlueskyMqttBridge:
    DEFAULT_FIREHOSE_URL = "wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos"

    def __init__(
        self,
        client: BlueskyFirehoseMqttMqttClient,
        *,
        firehose_url: str = DEFAULT_FIREHOSE_URL,
        collections: Optional[Iterable[str]] = None,
    ) -> None:
        self.client = client
        self.firehose_url = firehose_url
        self.collections = set(collections) if collections else None
        self._count = 0

    async def run(self, max_events: Optional[int] = None) -> None:
        import atproto_firehose.models
        from atproto import CAR, AtUri, parse_subscribe_repos_message

        retry_delay = 1
        max_retry_delay = 60
        url = self.firehose_url
        while True:
            try:
                async with aiohttp.ClientSession(headers={"User-Agent": USER_AGENT}) as session:
                    async with session.ws_connect(url) as ws:
                        logger.info("Connected to Bluesky firehose at %s", url)
                        retry_delay = 1
                        async for msg in ws:
                            if isinstance(msg, aiohttp.WSMessage) and msg.type == aiohttp.WSMsgType.BINARY:
                                payload = msg.data
                            elif isinstance(msg, bytes):
                                payload = msg
                            else:
                                continue
                            try:
                                frame = atproto_firehose.models.Frame.from_bytes(payload)
                            except Exception:
                                continue
                            if not isinstance(frame, atproto_firehose.models.MessageFrame):
                                continue
                            try:
                                message = parse_subscribe_repos_message(frame)
                            except Exception:
                                continue
                            if not (hasattr(message, "blocks") and getattr(message, "ops", None)):
                                continue
                            try:
                                car = CAR.from_bytes(message.blocks)
                            except Exception:
                                continue
                            for op in message.ops:
                                if op.action not in ("create", "update"):
                                    continue
                                if not op.cid:
                                    continue
                                uri = AtUri.from_str(f"at://{message.repo}/{op.path}")
                                collection = uri.collection
                                if self.collections and collection not in self.collections:
                                    continue
                                record = car.blocks.get(op.cid)
                                if not isinstance(record, dict):
                                    continue
                                try:
                                    await self._dispatch(message, uri, record, op.cid, collection)
                                    self._count += 1
                                    if max_events and self._count >= max_events:
                                        logger.info("max_events=%d reached, exiting", max_events)
                                        return
                                except Exception as exc:  # pragma: no cover - defensive
                                    logger.warning("dispatch failed at %s: %s", uri, exc)
            except (asyncio.CancelledError, KeyboardInterrupt):
                raise
            except Exception as exc:
                logger.error("Firehose connection error: %s. Retrying in %ds", exc, retry_delay)
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, max_retry_delay)

    async def _dispatch(self, commit, uri, record: Dict[str, Any], cid, collection: str) -> None:
        did = commit.repo
        if collection == "app.bsky.feed.post":
            data = _build_post(commit, uri, record, cid)
            await self.client.publish_bluesky_feed_post_mqtt(
                firehoseurl=self.firehose_url,
                did=_norm_segment(did),
                collection=_norm_segment(data.collection),
                lang=_norm_segment(data.lang),
                data=data,
                qos=0,
                retain=False,
            )
        elif collection == "app.bsky.feed.like":
            data = _build_like(commit, uri, record, cid)
            await self.client.publish_bluesky_feed_like_mqtt(
                firehoseurl=self.firehose_url,
                did=_norm_segment(did),
                collection=_norm_segment(data.collection),
                lang=_norm_segment(data.lang),
                data=data,
                qos=0,
                retain=False,
            )
        elif collection == "app.bsky.feed.repost":
            data = _build_repost(commit, uri, record, cid)
            await self.client.publish_bluesky_feed_repost_mqtt(
                firehoseurl=self.firehose_url,
                did=_norm_segment(did),
                collection=_norm_segment(data.collection),
                lang=_norm_segment(data.lang),
                data=data,
                qos=0,
                retain=False,
            )
        elif collection == "app.bsky.graph.follow":
            data = _build_follow(commit, uri, record, cid)
            await self.client.publish_bluesky_graph_follow_mqtt(
                firehoseurl=self.firehose_url,
                did=_norm_segment(did),
                collection=_norm_segment(data.collection),
                lang=_norm_segment(data.lang),
                data=data,
                qos=0,
                retain=False,
            )
        elif collection == "app.bsky.graph.block":
            data = _build_block(commit, uri, record, cid)
            await self.client.publish_bluesky_graph_block_mqtt(
                firehoseurl=self.firehose_url,
                did=_norm_segment(did),
                collection=_norm_segment(data.collection),
                lang=_norm_segment(data.lang),
                data=data,
                qos=0,
                retain=False,
            )
        elif collection == "app.bsky.actor.profile":
            data = _build_profile(commit, record)
            await self.client.publish_bluesky_actor_profile_mqtt(
                firehoseurl=self.firehose_url,
                did=_norm_segment(did),
                collection=_norm_segment(data.collection),
                lang=_norm_segment(data.lang),
                data=data,
                qos=0,
                retain=False,
            )

    async def emit_mock_corpus(self) -> None:
        """Publish one message per event family from canned payloads.

        Used by the Docker E2E test so the topic tree and CloudEvent
        framing can be validated without depending on a live firehose
        connection from the test sandbox.
        """
        seq = 1
        time_iso = "2024-01-01T00:00:00.000Z"

        class _MockCommit:
            def __init__(self, repo: str, seq_: int, time_: str) -> None:
                self.repo = repo
                self.seq = seq_
                self.time = time_

        commit = _MockCommit("did:plc:mockuser0000000000001", seq, time_iso)
        uri = f"at://{commit.repo}/app.bsky.feed.post/aaaaaaaaaa"
        post_record = {
            "text": "hello uns",
            "langs": ["en"],
            "createdAt": time_iso,
        }
        await self._dispatch(commit, uri, post_record, "bafyreigmockpost00000000000000000000000000000000000000000000",
                             "app.bsky.feed.post")

        like_record = {
            "subject": {"uri": uri, "cid": "bafyreigmocklikesubject0000000000000000000000000000000000000000"},
            "createdAt": time_iso,
        }
        await self._dispatch(commit, f"at://{commit.repo}/app.bsky.feed.like/bbbbbbbbbb",
                             like_record, "bafyreigmocklike000000000000000000000000000000000000000000000",
                             "app.bsky.feed.like")

        repost_record = like_record
        await self._dispatch(commit, f"at://{commit.repo}/app.bsky.feed.repost/cccccccccc",
                             repost_record, "bafyreigmockrepost00000000000000000000000000000000000000000000",
                             "app.bsky.feed.repost")

        follow_record = {"subject": "did:plc:targetfollow0000000000001", "createdAt": time_iso}
        await self._dispatch(commit, f"at://{commit.repo}/app.bsky.graph.follow/dddddddddd",
                             follow_record, "bafyreigmockfollow00000000000000000000000000000000000000000000",
                             "app.bsky.graph.follow")

        block_record = {"subject": "did:plc:targetblock0000000000001", "createdAt": time_iso}
        await self._dispatch(commit, f"at://{commit.repo}/app.bsky.graph.block/eeeeeeeeee",
                             block_record, "bafyreigmockblock000000000000000000000000000000000000000000000",
                             "app.bsky.graph.block")

        profile_record = {
            "displayName": "Mock User",
            "description": "Synthetic profile for E2E tests",
            "createdAt": time_iso,
        }
        await self._dispatch(commit, f"at://{commit.repo}/app.bsky.actor.profile/self",
                             profile_record, "bafyreigmockprofile000000000000000000000000000000000000000000",
                             "app.bsky.actor.profile")

# ---------------------------------------------------------------------------
# CLI / entry point
# ---------------------------------------------------------------------------

def _parse_broker(url: str) -> tuple[str, int, bool]:
    """Return (host, port, tls) from ``mqtt[s]://host:port`` or ``host:port``."""
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    host = parsed.hostname or "localhost"
    port = parsed.port or (8883 if scheme == "mqtts" else 1883)
    return host, port, scheme == "mqtts"

async def _run(args: argparse.Namespace) -> None:
    broker_host, broker_port, tls = _parse_broker(args.mqtt_broker_url)
    tls = tls or args.mqtt_enable_tls

    resolved_client_id, resolved_username, resolved_password, _entra_props = _resolve_mqtt_connection_settings(
        username=args.mqtt_username,
        password=args.mqtt_password or "",
        client_id=args.mqtt_client_id or "",
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho_client = mqtt.Client(client_id=resolved_client_id or "", 
        callback_api_version=CallbackAPIVersion.VERSION2,
        protocol=MQTTv5,
    )
    if _entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls or _entra_props is not None:
        paho_client.tls_set()

    loop = asyncio.get_running_loop()
    client = BlueskyFirehoseMqttMqttClient(
        client=paho_client,
        content_mode="binary",
        loop=loop,
    )
    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    if _entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=_entra_props)
        paho_client.loop_start()
    else:
        await client.connect(broker_host, broker_port)

    collections = None
    if args.collections:
        collections = [c.strip() for c in args.collections.split(",") if c.strip()]
    bridge = BlueskyMqttBridge(
        client,
        firehose_url=args.firehose_url,
        collections=collections,
    )
    if args.mock:
        logger.info("Mock mode: emitting synthetic corpus and exiting")
        await bridge.emit_mock_corpus()
        # Give paho a moment to flush before disconnect.
        await asyncio.sleep(1.0)
        await client.disconnect()
        return
    await bridge.run(max_events=args.max_events)

def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    p = argparse.ArgumentParser(description="Bluesky firehose -> MQTT/UNS bridge")
    sub = p.add_subparsers(dest="command")

    feed = sub.add_parser("feed", help="Stream firehose to MQTT")
    feed.add_argument("--mqtt-broker-url",
                      default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed.add_argument("--mqtt-enable-tls", action="store_true",
                      default=os.getenv("MQTT_ENABLE_TLS", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed.add_argument("--firehose-url",
                      default=os.getenv("BLUESKY_FIREHOSE_URL",
                                        BlueskyMqttBridge.DEFAULT_FIREHOSE_URL))
    feed.add_argument("--collections",
                      default=os.getenv("BLUESKY_COLLECTIONS", ""),
                      help="Comma-separated AT collection filter (empty = all)")
    feed.add_argument("--max-events", type=int,
                      default=int(os.getenv("BLUESKY_MAX_EVENTS", "0")) or None,
                      help="Stop after N published events (0=forever, for tests)")
    feed.add_argument("--mock", action="store_true",
                      default=os.getenv("BLUESKY_MOCK", "false").lower() in ("true", "1", "yes"),
                      help="Skip firehose, emit one synthetic event per family, then exit")

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
