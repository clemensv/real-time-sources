"""Upstream HSL HFP MQTT subscriber.

This is the novel-approach acquisition core. The upstream HSL HFP broker is
*described* in the xRegistry manifest as an MQTT consumer message group, and
``xrcg`` generates the upstream data classes plus the topic-level definitions in
:mod:`hsl_hfp_upstream_mqtt_client`. This module reuses those generated topic
definitions to parse the firehose rather than hardcoding the HFP topic grammar.

Two HFP realities shape the receive path:

* **Variable geohash tail.** The HFP ``geohash`` is not a single topic level: it
  is the integer pair ``<lat>;<long>`` followed by a variable number of
  interleaved fractional-digit levels (e.g. ``60;24/19/73/44``). A flat
  URI-template placeholder (and therefore the generated fixed-``+`` subscription
  topics) cannot express a variable-length tail, so the source subscribes with
  the multi-level ``#`` wildcard and parses the topic positionally. The stable
  *head* level names (``temporal_type`` ... ``geohash_level``) are still taken
  from the generated template, so the contract remains the single source of
  truth for the topic grammar.
* **Single-key payload wrapper.** Every HFP payload is a single-key object whose
  key is the upper-cased event type, e.g. ``{"VP": {...}}``. The inner object is
  unwrapped and handed to the callback verbatim; the event type is carried
  separately (it is also encoded in the topic).
"""

from __future__ import annotations

import json
import logging
import re
import time
import uuid
from typing import Callable, Dict, List, Optional, Tuple

import paho.mqtt.client as mqtt

# Reuse the generated upstream topic definitions (novel approach): the topic
# grammar is owned by the xRegistry contract, not redeclared here.
from hsl_hfp_upstream_mqtt_client.client import (
    get_default_topic_mappings_fi_hsl_hfp_upstream as _generated_topic_mappings,
)

logger = logging.getLogger(__name__)

# Event types whose HFP topic carries a trailing junction id (``sid``) after the
# geohash tail. Everything else ends with the geohash.
_TL_EVENTS = frozenset({"tlr", "tla"})

_PLACEHOLDER = re.compile(r"^\{([A-Za-z0-9_]+)\}$")

# Callback signature: (event_type, topic_params, payload, raw_topic).
HfpCallback = Callable[[str, Dict[str, str], dict, str], None]


def _derive_head_grammar() -> Tuple[List[Tuple[int, str]], int]:
    """Derive the stable head-level grammar from the generated topic templates.

    Returns ``(head_levels, geohash_start_index)`` where ``head_levels`` is a
    list of ``(topic_split_index, level_name)`` for the fixed head levels
    (``temporal_type`` through ``geohash_level``), the literal event-type level
    being named ``event_type``; ``geohash_start_index`` is the split index at
    which the variable geohash tail begins.
    """
    mappings = _generated_topic_mappings()
    # The veh-family templates share the head with the tl-family; pick the vp
    # template as the canonical head definition.
    template = mappings.get("fi.hsl.hfp.upstream.vp") or next(iter(mappings.values()))
    segments = template.strip("/").split("/")  # e.g. ['hfp','v2','journey','{temporal_type}','vp',...]
    head: List[Tuple[int, str]] = []
    geohash_start = len(segments) + 1
    for i, seg in enumerate(segments):
        topic_index = i + 1  # incoming topics have a leading '' from the prefix slash
        m = _PLACEHOLDER.match(seg)
        if m:
            name = m.group(1)
            if name == "geohash":
                geohash_start = topic_index
                break
            head.append((topic_index, name))
        elif seg in ("hfp", "v2", "journey"):
            continue
        else:
            # The single literal segment inside the journey body is the event type.
            head.append((topic_index, "event_type"))
    return head, geohash_start


_HEAD_LEVELS, _GEOHASH_START = _derive_head_grammar()


def parse_topic(topic: str) -> Optional[Tuple[str, Dict[str, str]]]:
    """Parse an HFP topic into ``(event_type, params)``.

    ``params`` carries every head level plus ``geohash`` (the joined variable
    tail) and, for ``tlr``/``tla``, ``sid``. Returns ``None`` for topics that do
    not match the journey grammar (too few levels).
    """
    parts = topic.split("/")
    # Require the full fixed head (indices 0..geohash_level) to be present; the
    # geohash tail beyond it may be empty.
    if len(parts) < _GEOHASH_START:
        return None
    params: Dict[str, str] = {}
    for idx, name in _HEAD_LEVELS:
        if idx < len(parts):
            params[name] = parts[idx]
    event_type = params.get("event_type")
    if not event_type:
        return None
    tail = parts[_GEOHASH_START:]
    if event_type in _TL_EVENTS and tail:
        params["sid"] = tail[-1]
        tail = tail[:-1]
    params["geohash"] = "/".join(tail) if tail else ""
    return event_type, params


def unwrap_payload(raw: bytes) -> Optional[dict]:
    """Decode the HFP JSON payload and unwrap the single-key event wrapper."""
    try:
        obj = json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        logger.debug("Invalid HFP payload: %s", exc)
        return None
    if isinstance(obj, dict) and len(obj) == 1:
        inner = next(iter(obj.values()))
        if isinstance(inner, dict):
            return inner
    # Already-unwrapped or unexpected shape: return as-is if it is an object.
    return obj if isinstance(obj, dict) else None


class HfpSource:
    """Subscribes to the HSL HFP firehose and delivers parsed events."""

    def __init__(
        self,
        host: str,
        port: int,
        topic_filters: List[str],
        *,
        tls: bool = True,
        max_retry_delay: int = 60,
        client_id_prefix: str = "hsl-hfp-bridge",
    ) -> None:
        self.host = host
        self.port = port
        self.topic_filters = topic_filters
        self.tls = tls
        self.max_retry_delay = max_retry_delay
        self.client_id_prefix = client_id_prefix
        self._callback: Optional[HfpCallback] = None
        self._retry_delay = 1
        self._stop = False
        self._count = 0
        self._max_messages: Optional[int] = None

    def stream(
        self,
        callback: HfpCallback,
        *,
        max_messages: Optional[int] = None,
        max_seconds: Optional[float] = None,
    ) -> int:
        """Connect and stream parsed HFP events to ``callback``.

        Runs until interrupted, or -- when ``max_messages`` / ``max_seconds`` is
        set (used by ``--once`` and the E2E harness) -- until either bound is
        reached. Reconnects with exponential backoff on connection failure in
        the unbounded case. Returns the number of messages delivered to the
        callback.
        """
        self._callback = callback
        self._retry_delay = 1
        self._count = 0
        self._max_messages = max_messages
        bounded = max_messages is not None or max_seconds is not None
        deadline = (time.monotonic() + max_seconds) if max_seconds else None
        while not self._stop:
            try:
                self._connect_and_loop(deadline)
                if bounded:
                    break
            except KeyboardInterrupt:
                logger.info("Interrupted -- stopping HFP subscriber.")
                break
            except Exception as exc:  # pylint: disable=broad-except
                logger.warning("HFP MQTT error: %s. Reconnecting in %ds...", exc, self._retry_delay)
                if bounded and deadline and time.monotonic() >= deadline:
                    break
                time.sleep(self._retry_delay)
                self._retry_delay = min(self._retry_delay * 2, self.max_retry_delay)
        return self._count

    def stop(self) -> None:
        self._stop = True

    def _connect_and_loop(self, deadline: Optional[float] = None) -> None:
        client_id = f"{self.client_id_prefix}-{uuid.uuid4()}"
        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=client_id,
        )

        def on_connect(c, userdata, flags, reason_code, properties):
            if reason_code == 0:
                logger.info("Connected to HFP broker %s:%d", self.host, self.port)
                for topic_filter in self.topic_filters:
                    c.subscribe(topic_filter, qos=0)
                    logger.info("  Subscribed: %s", topic_filter)
                self._retry_delay = 1
            else:
                logger.error("HFP connect failed: %s", reason_code)

        def on_disconnect(c, userdata, flags, reason_code, properties):
            if reason_code != 0:
                logger.warning("HFP disconnected unexpectedly: %s", reason_code)

        def on_message(c, userdata, msg):
            parsed = parse_topic(msg.topic)
            if parsed is None:
                return
            event_type, params = parsed
            payload = unwrap_payload(msg.payload)
            if payload is None:
                return
            self._count += 1
            if self._callback:
                try:
                    self._callback(event_type, params, payload, msg.topic)
                except Exception as exc:  # pylint: disable=broad-except
                    logger.error("Error in HFP callback for %s: %s", msg.topic, exc)
            if self._max_messages is not None and self._count >= self._max_messages:
                self._stop = True

        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message

        if self.tls:
            client.tls_set()
        logger.info("Connecting to HFP broker %s:%d (tls=%s) ...", self.host, self.port, self.tls)
        client.connect(self.host, self.port, keepalive=60)
        client.loop_start()
        try:
            while not self._stop:
                time.sleep(0.2)
                if deadline is not None and time.monotonic() >= deadline:
                    break
                if not client.is_connected() and deadline is None and self._max_messages is None:
                    # Unbounded mode: surface the drop so stream() reconnects.
                    raise ConnectionError("HFP connection lost")
        finally:
            client.loop_stop()
            try:
                client.disconnect()
            except Exception:  # pylint: disable=broad-except
                pass
