"""Transport-agnostic core for the DMI bridge.

The DMI source feeds three messagegroups (metObs, oceanObs, lightning) into one
Kafka topic and two into MQTT/UNS. This package contains everything that is
shared between the transports — HTTP clients for the three DMI APIs, config
parsing, and dedup-state persistence — and intentionally has no producer
dependency. Each transport-specific feeder consumes the API classes and pushes
the upstream JSON dictionaries into its own generated CloudEvents producer.
"""

from .acquisition import (
    DmiMetObsAPI,
    DmiOceanObsAPI,
    DmiLightningAPI,
    METOBS_FEED_ROOT,
    OCEANOBS_FEED_ROOT,
    LIGHTNING_FEED_ROOT,
)
from .config import FeedConfig, DmiApiKeys, build_kafka_config, parse_kafka_connection_string
from .state import load_state, save_state

__all__ = [
    "DmiMetObsAPI",
    "DmiOceanObsAPI",
    "DmiLightningAPI",
    "METOBS_FEED_ROOT",
    "OCEANOBS_FEED_ROOT",
    "LIGHTNING_FEED_ROOT",
    "FeedConfig",
    "DmiApiKeys",
    "build_kafka_config",
    "parse_kafka_connection_string",
    "load_state",
    "save_state",
]
