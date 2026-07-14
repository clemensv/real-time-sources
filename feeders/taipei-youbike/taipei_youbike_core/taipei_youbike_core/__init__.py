"""Shared, transport-agnostic building blocks for the Taiwan YouBike 2.0 bridge.

Every transport variant (Kafka, MQTT, AMQP) imports the same upstream
acquisition client, station normalization, dedup state helpers, and
connection-string parsers from this package so the wire-facing apps only differ
in how they publish CloudEvents.
"""

from __future__ import annotations

from .acquisition import FEED_URL, USER_AGENT, YouBikeAPI
from .config import (
    FeedConfig,
    build_kafka_config,
    parse_kafka_connection_string,
)
from .normalize import ParsedStation, parse_station
from .state import load_state, save_state

__all__ = [
    "FEED_URL",
    "USER_AGENT",
    "YouBikeAPI",
    "FeedConfig",
    "build_kafka_config",
    "parse_kafka_connection_string",
    "ParsedStation",
    "parse_station",
    "load_state",
    "save_state",
]
