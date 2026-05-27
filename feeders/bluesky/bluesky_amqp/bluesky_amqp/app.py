"""AMQP feeder for the Bluesky AT Protocol firehose.

Connects to the public ``com.atproto.sync.subscribeRepos`` firehose, decodes
each commit into typed records, and republishes them as AMQP 5 binary-mode
CloudEvents on the Unified Namespace topic family

    social/intl/bluesky/bluesky/{collection}/{lang}/{did}/{event}

QoS 0, retain=False — there is no LKV slot for a firehose. Every required
topic placeholder is materialized in the record payload so the generated
producer can resolve the URI template, and so subscribers can rely on
round-trip consistency with the payload.

Run with::

    python -m bluesky_amqp feed --amqp-broker-url localhost:1883
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, Iterable, Optional
from urllib.parse import urlparse

import aiohttp

from bluesky_amqp_producer_data import Block, Follow, Like, Post, Profile, Repost
from bluesky_amqp_producer_amqp_producer.producer import BlueskyFirehoseAmqpProducer

logger = logging.getLogger("bluesky_amqp")


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
# so the AMQP topic placeholders resolve to a real payload field (see
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




DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


def _parse_amqp_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    return parsed.hostname or "localhost", port, tls, parsed.username or None, parsed.password or None, (parsed.path or "").lstrip("/") or None


def add_amqp_arguments(parser: argparse.ArgumentParser, default_address: str) -> None:
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", default_address))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))


def create_amqp_producer(args: argparse.Namespace, producer_cls):
    address = args.address
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_amqp_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        if path:
            address = path
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode in ("entra", "sas")
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential()
        return producer_cls(host=host, address=address, port=port, content_mode=args.content_mode, credential=credential, entra_audience=args.entra_audience, use_tls=tls)
    if args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return producer_cls(host=host, address=address, port=port, content_mode=args.content_mode, sas_key_name=args.sas_key_name, sas_key=args.sas_key, use_tls=tls)
    return producer_cls(host=host, address=address, port=port, username=username, password=password, content_mode=args.content_mode, use_tls=tls)


class AmqpClient:
    def __init__(self, producer):
        self.producer = producer
        self._send_methods = [name for name in dir(producer) if name.startswith("send_") and not name.endswith("_batch")]

    def _resolve(self, publish_name: str) -> str:
        normalized = publish_name.replace("publish_", "", 1).replace("_amqp", "")
        candidates = sorted(self._send_methods, key=len, reverse=True)
        for method in candidates:
            suffix = method.replace("send_", "")
            if normalized.endswith(suffix):
                return method
        if normalized.endswith("_node") or normalized.endswith("_way") or normalized.endswith("_relation"):
            return "send_map_change"
        raise AttributeError(publish_name)

    def __getattr__(self, name: str):
        if not name.startswith("publish_"):
            raise AttributeError(name)
        send_name = self._resolve(name)

        async def _publish(**kwargs):
            import inspect
            data = kwargs.pop("data")
            kwargs.pop("qos", None)
            kwargs.pop("retain", None)
            call_kwargs = {f"_{k}": v for k, v in kwargs.items() if v is not None}
            method = getattr(self.producer, send_name)
            params = set(inspect.signature(method).parameters)
            if "_element_type" in params and "_element_type" not in call_kwargs and hasattr(data, "element_type"):
                call_kwargs["_element_type"] = getattr(data, "element_type")
            call_kwargs = {k: v for k, v in call_kwargs.items() if k in params}
            method(data=data, **call_kwargs)
        return _publish

    async def connect(self, *_args, **_kwargs):
        return None

    async def disconnect(self):
        self.producer.close()


# ---------------------------------------------------------------------------
# Bridge
# ---------------------------------------------------------------------------


class BlueskyMqttBridge:
    DEFAULT_FIREHOSE_URL = "wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos"

    def __init__(
        self,
        client: AmqpClient,
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
                async with aiohttp.ClientSession() as session:
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
            await self.client.publish_bluesky_feed_post_amqp(
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
            await self.client.publish_bluesky_feed_like_amqp(
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
            await self.client.publish_bluesky_feed_repost_amqp(
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
            await self.client.publish_bluesky_graph_follow_amqp(
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
            await self.client.publish_bluesky_graph_block_amqp(
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
            await self.client.publish_bluesky_actor_profile_amqp(
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
    """Return (host, port, tls) from ``amqp[s]://host:port`` or ``host:port``."""
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    host = parsed.hostname or "localhost"
    port = parsed.port or (8883 if scheme == "amqps" else 1883)
    return host, port, scheme == "amqps"


async def _run(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args, BlueskyFirehoseAmqpProducer)
    client = AmqpClient(producer)
    collections = [x.strip() for x in args.collections.split(",") if x.strip()] if args.collections else None
    bridge = BlueskyMqttBridge(client, firehose_url=args.firehose_url, collections=collections)
    try:
        if args.mock:
            logger.info("Mock mode: emitting synthetic corpus and exiting")
            await bridge.emit_mock_corpus()
            return
        await bridge.run(max_events=args.max_events)
    finally:
        producer.close()

def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    p = argparse.ArgumentParser(description="Bluesky firehose -> AMQP 1.0 bridge")
    sub = p.add_subparsers(dest="command")

    feed = sub.add_parser("feed", help="Stream firehose to AMQP")
    add_amqp_arguments(feed, "bluesky")
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
