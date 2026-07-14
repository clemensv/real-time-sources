"""Shared, transport-agnostic building blocks for the TfL Santander Cycles bridge.

Every transport variant (Kafka, MQTT, AMQP) imports the same upstream
acquisition client, BikePoint normalization, dedup state helpers, and
connection-string parsers from this package so the wire-facing apps only differ
in how they publish CloudEvents.
"""

from __future__ import annotations

from .acquisition import FEED_URL_ROOT, TfLCyclesAPI, USER_AGENT
from .config import (
    FeedConfig,
    build_kafka_config,
    parse_kafka_connection_string,
)
from .normalize import ParsedStation, parse_bikepoint
from .state import load_state, save_state

__all__ = [
    "FEED_URL_ROOT",
    "TfLCyclesAPI",
    "USER_AGENT",
    "FeedConfig",
    "build_kafka_config",
    "parse_kafka_connection_string",
    "ParsedStation",
    "parse_bikepoint",
    "load_state",
    "save_state",
]
