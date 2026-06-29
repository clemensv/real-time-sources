"""Transport-agnostic acquisition core for the HSL HFP bridge.

This package holds everything the Kafka, MQTT, and AMQP transport apps share:
the upstream HFP MQTT subscriber (:mod:`hsl_hfp.hfp_source`), the GTFS-static
reference fetcher (:mod:`hsl_hfp.hfp_gtfs`), the embedded operator catalogue
(:mod:`hsl_hfp.operators`), and the shared configuration / connection-string
helpers (:mod:`hsl_hfp.config`). The Kafka bridge entry point lives in
:mod:`hsl_hfp.app`; it is intentionally **not** imported here so the MQTT and
AMQP apps can depend on the acquisition core without pulling in the Kafka
producer.
"""

from __future__ import annotations

from .config import (
    HFP_DEFAULT_HOST,
    HFP_DEFAULT_PORT,
    HFP_FEED_URL,
    HSL_GTFS_URL,
    FeedConfig,
    build_kafka_config,
    parse_kafka_connection_string,
)
from .hfp_gtfs import GtfsSnapshot, GtfsStatic
from .hfp_source import HfpSource, parse_topic, unwrap_payload
from .mapping import (
    DRIVER_BLOCK_EVENTS,
    TRAFFIC_LIGHT_EVENTS,
    VEHICLE_EVENTS,
    driver_block_event_kwargs,
    operator_kwargs,
    route_kwargs,
    stop_kwargs,
    traffic_light_event_kwargs,
    vehicle_event_kwargs,
)
from .operators import OPERATORS, iter_operators
from .runner import BridgeRunner, Sink

__all__ = [
    "FeedConfig",
    "HFP_DEFAULT_HOST",
    "HFP_DEFAULT_PORT",
    "HFP_FEED_URL",
    "HSL_GTFS_URL",
    "build_kafka_config",
    "parse_kafka_connection_string",
    "GtfsSnapshot",
    "GtfsStatic",
    "HfpSource",
    "parse_topic",
    "unwrap_payload",
    "OPERATORS",
    "iter_operators",
    "VEHICLE_EVENTS",
    "TRAFFIC_LIGHT_EVENTS",
    "DRIVER_BLOCK_EVENTS",
    "vehicle_event_kwargs",
    "traffic_light_event_kwargs",
    "driver_block_event_kwargs",
    "operator_kwargs",
    "route_kwargs",
    "stop_kwargs",
    "BridgeRunner",
    "Sink",
]
