"""Shared, transport-agnostic building blocks for the Open Charge Map bridge.

Every transport variant (Kafka, MQTT, AMQP) imports the same upstream
acquisition client, POI/reference normalization, dedup/watermark state helpers,
and connection-string parsers from this package so the wire-facing apps only
differ in how they publish CloudEvents.
"""

from __future__ import annotations

from .acquisition import BASE_URL, POI_URL, REFERENCE_URL, USER_AGENT, OpenChargeMapAPI
from .config import (
    FeedConfig,
    build_kafka_config,
    parse_kafka_connection_string,
)
from .normalize import (
    ParsedConnection,
    ParsedLocation,
    ParsedReference,
    REFERENCE_SPECS,
    parse_ocm_datetime,
    parse_poi,
    parse_reference_data,
)
from .state import load_state, save_state

__all__ = [
    "BASE_URL",
    "POI_URL",
    "REFERENCE_URL",
    "USER_AGENT",
    "OpenChargeMapAPI",
    "FeedConfig",
    "build_kafka_config",
    "parse_kafka_connection_string",
    "ParsedConnection",
    "ParsedLocation",
    "ParsedReference",
    "REFERENCE_SPECS",
    "parse_ocm_datetime",
    "parse_poi",
    "parse_reference_data",
    "load_state",
    "save_state",
]
