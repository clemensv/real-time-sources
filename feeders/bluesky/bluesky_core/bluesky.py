"""Transport-neutral Bluesky firehose helpers."""

from __future__ import annotations

import asyncio
import json
import logging
import os
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import urlparse

import aiohttp
from atproto import CAR, AtUri, parse_subscribe_repos_message

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-bluesky/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)
DEFAULT_FIREHOSE_URL = "wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos"
logger = logging.getLogger(__name__)
_UNDETERMINED_LANG = "und"


def load_cursor(cursor_file: Optional[str]) -> Optional[int]:
    if cursor_file and os.path.exists(cursor_file):
        try:
            with open(cursor_file, "r", encoding="utf-8") as handle:
                return json.load(handle).get("cursor")
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to load cursor: %s", exc)
    return None


def save_cursor(cursor_file: Optional[str], cursor: Optional[int]) -> None:
    if cursor_file and cursor is not None:
        try:
            os.makedirs(os.path.dirname(cursor_file), exist_ok=True)
            with open(cursor_file, "w", encoding="utf-8") as handle:
                json.dump({"cursor": cursor}, handle)
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to save cursor: %s", exc)


def normalize_langs(raw_langs: Any) -> list[str]:
    if not isinstance(raw_langs, list):
        return []
    return [lang.strip().lower() for lang in raw_langs if isinstance(lang, str) and lang.strip()]


def normalize_segment(value: Optional[str]) -> str:
    if not value:
        return ""
    return str(value).strip().lower().replace("/", "_").replace("#", "_").replace("+", "_")


def pick_lang(record: dict[str, Any]) -> str:
    langs = normalize_langs(record.get("langs"))
    return langs[0] if langs else _UNDETERMINED_LANG


def safe_get_link(field_value: Any) -> Optional[str]:
    if not field_value or isinstance(field_value, bytes):
        return None
    if isinstance(field_value, dict):
        ref = field_value.get("ref")
        if isinstance(ref, dict):
            return ref.get("$link")
    return None


@dataclass
class BlueskyEvent:
    event_type: str
    did: str
    collection: str
    lang: str
    payload: dict[str, Any]
    seq: int


def _common_fields(repo: str, seq: int, time_iso: str, uri: str, record: Optional[dict] = None, cid: Any = None) -> dict[str, Any]:
    langs = normalize_langs(record.get("langs") if isinstance(record, dict) else None)
    return {
        "uri": uri,
        "cid": str(cid) if cid else "",
        "did": repo,
        "handle": None,
        "indexed_at": time_iso,
        "seq": seq,
        "collection": AtUri.from_str(uri).collection,
        "lang": langs[0] if langs else _UNDETERMINED_LANG,
    }


def build_post_event(repo: str, seq: int, time_iso: str, uri: str, record: dict[str, Any], cid: Any) -> BlueskyEvent:
    reply = record.get("reply", {})
    reply_parent = reply.get("parent", {})
    reply_root = reply.get("root", {})
    embed = record.get("embed", {})
    embed_type = embed.get("$type")
    embed_uri = None
    if embed_type == "app.bsky.embed.external":
        embed_uri = (embed.get("external") or {}).get("uri")
    elif embed_type == "app.bsky.embed.record":
        embed_uri = (embed.get("record") or {}).get("uri")
    elif embed_type == "app.bsky.embed.recordWithMedia":
        embed_uri = ((embed.get("record") or {}).get("record") or {}).get("uri")
    payload = {
        **_common_fields(repo, seq, time_iso, uri, record, cid),
        "text": record.get("text", ""),
        "langs": normalize_langs(record.get("langs")),
        "reply_parent": reply_parent.get("uri"),
        "reply_parent_cid": reply_parent.get("cid"),
        "reply_root": reply_root.get("uri"),
        "reply_root_cid": reply_root.get("cid"),
        "embed_type": embed_type,
        "embed_uri": embed_uri,
        "facets": json.dumps(record.get("facets", [])) if record.get("facets") else None,
        "labels": json.dumps(record.get("labels", {})) if record.get("labels") else None,
        "tags": record.get("tags", []),
        "created_at": record.get("createdAt", ""),
    }
    return BlueskyEvent("Bluesky.Feed.Post", repo, payload["collection"], payload["lang"], payload, seq)


def build_like_event(repo: str, seq: int, time_iso: str, uri: str, record: dict[str, Any], cid: Any) -> BlueskyEvent:
    subject = record.get("subject", {})
    payload = {
        **_common_fields(repo, seq, time_iso, uri, None, cid),
        "subject_uri": subject.get("uri", ""),
        "subject_cid": subject.get("cid", ""),
        "created_at": record.get("createdAt", ""),
    }
    return BlueskyEvent("Bluesky.Feed.Like", repo, payload["collection"], payload["lang"], payload, seq)


def build_repost_event(repo: str, seq: int, time_iso: str, uri: str, record: dict[str, Any], cid: Any) -> BlueskyEvent:
    subject = record.get("subject", {})
    payload = {
        **_common_fields(repo, seq, time_iso, uri, None, cid),
        "subject_uri": subject.get("uri", ""),
        "subject_cid": subject.get("cid", ""),
        "created_at": record.get("createdAt", ""),
    }
    return BlueskyEvent("Bluesky.Feed.Repost", repo, payload["collection"], payload["lang"], payload, seq)


def build_follow_event(repo: str, seq: int, time_iso: str, uri: str, record: dict[str, Any], cid: Any) -> BlueskyEvent:
    payload = {
        **_common_fields(repo, seq, time_iso, uri, None, cid),
        "subject": record.get("subject", ""),
        "subject_handle": None,
        "created_at": record.get("createdAt", ""),
    }
    return BlueskyEvent("Bluesky.Graph.Follow", repo, payload["collection"], payload["lang"], payload, seq)


def build_block_event(repo: str, seq: int, time_iso: str, uri: str, record: dict[str, Any], cid: Any) -> BlueskyEvent:
    payload = {
        **_common_fields(repo, seq, time_iso, uri, None, cid),
        "subject": record.get("subject", ""),
        "subject_handle": None,
        "created_at": record.get("createdAt", ""),
    }
    return BlueskyEvent("Bluesky.Graph.Block", repo, payload["collection"], payload["lang"], payload, seq)


def build_profile_event(repo: str, seq: int, time_iso: str, uri: str, record: dict[str, Any], cid: Any = None) -> BlueskyEvent:
    payload = {
        **_common_fields(repo, seq, time_iso, uri, None, cid),
        "did": repo,
        "display_name": record.get("displayName"),
        "description": record.get("description"),
        "avatar": safe_get_link(record.get("avatar")),
        "banner": safe_get_link(record.get("banner")),
        "created_at": record.get("createdAt", ""),
    }
    return BlueskyEvent("Bluesky.Actor.Profile", repo, payload["collection"], payload["lang"], payload, seq)


def build_event(repo: str, seq: int, time_iso: str, uri: str, record: dict[str, Any], cid: Any) -> Optional[BlueskyEvent]:
    collection = AtUri.from_str(uri).collection
    if collection == "app.bsky.feed.post":
        return build_post_event(repo, seq, time_iso, uri, record, cid)
    if collection == "app.bsky.feed.like":
        return build_like_event(repo, seq, time_iso, uri, record, cid)
    if collection == "app.bsky.feed.repost":
        return build_repost_event(repo, seq, time_iso, uri, record, cid)
    if collection == "app.bsky.graph.follow":
        return build_follow_event(repo, seq, time_iso, uri, record, cid)
    if collection == "app.bsky.graph.block":
        return build_block_event(repo, seq, time_iso, uri, record, cid)
    if collection == "app.bsky.actor.profile":
        return build_profile_event(repo, seq, time_iso, uri, record, cid)
    return None


def iter_commit_events(commit, collections: Optional[set[str]] = None):
    if not getattr(commit, "blocks", None) or not getattr(commit, "ops", None):
        return
    try:
        car = CAR.from_bytes(commit.blocks)
    except Exception as exc:
        logger.warning("Failed to parse CAR file: %s", exc)
        return
    for op in commit.ops:
        if op.action not in ("create", "update") or not op.cid:
            continue
        uri = AtUri.from_str(f"at://{commit.repo}/{op.path}")
        if collections and uri.collection not in collections:
            continue
        record = car.blocks.get(op.cid)
        if not isinstance(record, dict):
            continue
        event = build_event(commit.repo, commit.seq, getattr(commit, "time", "") or "", str(uri), record, op.cid)
        if event is not None:
            yield event


async def iter_firehose_events(*, firehose_url: str = DEFAULT_FIREHOSE_URL, collections: Optional[list[str]] = None, cursor_provider=None, user_agent: str = USER_AGENT) -> AsyncIterator[BlueskyEvent]:
    retry_delay = 1
    max_retry_delay = 60
    allowed = set(collections) if collections else None
    while True:
        url = firehose_url
        cursor = cursor_provider() if cursor_provider else None
        if cursor:
            sep = '&' if '?' in url else '?'
            url = f"{url}{sep}cursor={cursor}"
        try:
            async with aiohttp.ClientSession(headers={"User-Agent": user_agent}) as session:
                async with session.ws_connect(url) as ws:
                    retry_delay = 1
                    async for msg in ws:
                        payload = msg.data if isinstance(msg, aiohttp.WSMessage) and msg.type == aiohttp.WSMsgType.BINARY else msg if isinstance(msg, bytes) else None
                        if payload is None:
                            continue
                        try:
                            from atproto_firehose.models import Frame, MessageFrame
                            frame = Frame.from_bytes(payload)
                            if not isinstance(frame, MessageFrame):
                                continue
                            message = parse_subscribe_repos_message(frame)
                        except Exception:
                            continue
                        for event in iter_commit_events(message, allowed):
                            yield event
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.error("Connection error: %s. Retrying in %d seconds...", exc, retry_delay)
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, max_retry_delay)


async def iter_mock_firehose_events(max_events: int = 12) -> AsyncIterator[BlueskyEvent]:
    """Generate synthetic events for all event types for testing."""
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    seq = 1
    mock_types = [
        ("Bluesky.Feed.Post", "app.bsky.feed.post"),
        ("Bluesky.Feed.Like", "app.bsky.feed.like"),
        ("Bluesky.Feed.Repost", "app.bsky.feed.repost"),
        ("Bluesky.Graph.Follow", "app.bsky.graph.follow"),
        ("Bluesky.Graph.Block", "app.bsky.graph.block"),
        ("Bluesky.Actor.Profile", "app.bsky.actor.profile"),
    ]
    count = 0
    while count < max_events:
        for event_type, collection in mock_types:
            if count >= max_events:
                return
            did = f"did:plc:mock{seq:06d}"
            uri = f"at://{did}/{collection}/mock{seq}"
            payload: dict[str, Any] = {
                "uri": uri,
                "cid": f"bafyreimock{seq:06d}",
                "did": did,
                "handle": None,
                "indexed_at": now,
                "seq": seq,
                "collection": collection,
                "lang": "en",
            }
            if event_type == "Bluesky.Feed.Post":
                payload.update({"text": f"Mock post {seq}", "reply_parent": None, "reply_root": None,
                                "embed_type": None, "embed_uri": None, "embed_title": None,
                                "embed_description": None, "embed_thumb": None, "images": None,
                                "langs": ["en"], "facets": None, "labels": None})
            elif event_type == "Bluesky.Feed.Like":
                payload.update({"subject_uri": f"at://did:plc:target/app.bsky.feed.post/abc{seq}",
                                "subject_cid": f"bafyreitarget{seq:06d}"})
            elif event_type == "Bluesky.Feed.Repost":
                payload.update({"subject_uri": f"at://did:plc:target/app.bsky.feed.post/abc{seq}",
                                "subject_cid": f"bafyreitarget{seq:06d}"})
            elif event_type == "Bluesky.Graph.Follow":
                payload.update({"subject_did": f"did:plc:followed{seq:06d}"})
            elif event_type == "Bluesky.Graph.Block":
                payload.update({"subject_did": f"did:plc:blocked{seq:06d}"})
            elif event_type == "Bluesky.Actor.Profile":
                payload.update({"display_name": f"Mock User {seq}", "description": "Test profile",
                                "avatar": None, "banner": None})
            yield BlueskyEvent(event_type=event_type, did=did, collection=collection, lang="en", payload=payload, seq=seq)
            seq += 1
            count += 1
        await asyncio.sleep(0.01)
