"""Transport-neutral Wikimedia EventStreams helpers."""

from __future__ import annotations

import asyncio
import json
import logging
import os
from collections.abc import Callable, AsyncIterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlencode

import aiohttp

STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"
DEFAULT_STATE_FILE = os.path.expanduser("~/.wikimedia_eventstreams_state.json")
DEFAULT_USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-wikimedia-eventstreams/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com")
    + ")"
)
logger = logging.getLogger(__name__)

_NAMESPACE_BUCKETS: dict[int, str] = {
    -2: "media", -1: "special",
    0: "main", 1: "talk", 2: "user", 3: "user-talk", 4: "project", 5: "project-talk",
    6: "file", 7: "file-talk", 8: "mediawiki", 9: "mediawiki-talk",
    10: "template", 11: "template-talk", 12: "help", 13: "help-talk",
    14: "category", 15: "category-talk",
    100: "portal", 101: "portal-talk", 118: "draft", 119: "draft-talk",
    828: "module", 829: "module-talk", 1198: "translations", 1199: "translations-talk",
}


def build_stream_url(base_url: str, since: Optional[str]) -> str:
    if not since:
        return base_url
    return f"{base_url}?{urlencode({'since': since})}"


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


def namespace_bucket(ns: Any) -> str:
    try:
        n = int(ns)
    except (TypeError, ValueError):
        return "unknown"
    return _NAMESPACE_BUCKETS.get(n, f"ns-{n}")


def normalize_recent_change(change: dict[str, Any]) -> dict[str, Any]:
    meta = change.get("meta", {})
    length = change.get("length") or {}
    revision = change.get("revision") or {}
    ns_value = change.get("namespace")
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
        "namespace_id": ns_value,
        "namespace": namespace_bucket(ns_value),
        "title": change.get("title"),
        "title_url": change.get("title_url"),
        "comment": change.get("comment"),
        "timestamp": change.get("timestamp"),
        "user": change.get("user"),
        "bot": change.get("bot"),
        "minor": change.get("minor"),
        "patrolled": change.get("patrolled"),
        "length": {"old": length.get("old"), "new": length.get("new")},
        "revision": {"old": _stringify_optional(revision.get("old")), "new": _stringify_optional(revision.get("new"))},
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


@dataclass
class BridgeState:
    since: Optional[str]
    recent_event_ids: list[str]


class StateStore:
    def __init__(self, path: str, dedupe_size: int) -> None:
        self._path = Path(path)
        self._dedupe_size = dedupe_size

    def load(self) -> BridgeState:
        if not self._path.exists():
            return BridgeState(since=None, recent_event_ids=[])
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Failed to load state file %s: %s", self._path, exc)
            return BridgeState(since=None, recent_event_ids=[])
        recent_ids = [str(item) for item in payload.get("recent_event_ids", []) if item]
        return BridgeState(since=payload.get("since"), recent_event_ids=recent_ids[-self._dedupe_size :])

    def save(self, state: BridgeState) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"since": state.since, "recent_event_ids": state.recent_event_ids[-self._dedupe_size :]}
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


async def iter_recentchange_payloads(*, stream_url: str = STREAM_URL, user_agent: str = DEFAULT_USER_AGENT, since_provider: Optional[Callable[[], Optional[str]]] = None, max_retry_delay: int = 60) -> AsyncIterator[dict[str, Any]]:
    retry_delay = 1
    timeout = aiohttp.ClientTimeout(total=None, connect=30, sock_read=90)
    headers = {"Accept": "application/json", "User-Agent": user_agent}
    while True:
        url = build_stream_url(stream_url, since_provider() if since_provider else None)
        logger.info("Connecting to %s", url)
        try:
            async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    retry_delay = 1
                    async for raw_line in response.content:
                        line = raw_line.decode("utf-8", errors="replace").strip()
                        if not line:
                            continue
                        if line.startswith("data:"):
                            line = line[5:].strip()
                        yield json.loads(line)
        except asyncio.CancelledError:
            raise
        except (aiohttp.ClientError, asyncio.TimeoutError, ConnectionError) as exc:
            logger.warning("Stream error: %s. Reconnecting in %ds.", exc, retry_delay)
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, max_retry_delay)


