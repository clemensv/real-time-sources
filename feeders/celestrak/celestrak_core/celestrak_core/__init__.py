"""Transport-agnostic core for the CelesTrak bridge.

The CelesTrak source feeds three transports (Apache Kafka, MQTT/UNS and AMQP
1.0) from a single upstream poller. This package contains everything shared
between them -- the HTTP client with its usage-policy guard, the configuration
model, the Kafka connection-string parsing and the dedup-state persistence --
and intentionally has no producer dependency. Each transport-specific feeder
consumes :class:`CelesTrakAPI` and :class:`FeedConfig` and maps the upstream
JSON dictionaries onto its own generated CloudEvents producer.
"""

from .acquisition import (
    BASE_URL,
    GP_URL,
    SATCAT_URL,
    SUPGP_URL,
    CelesTrakAPI,
)
from .config import (
    FeedConfig,
    build_kafka_config,
    parse_kafka_connection_string,
)
from .state import load_state, save_state

__all__ = [
    "BASE_URL",
    "GP_URL",
    "SATCAT_URL",
    "SUPGP_URL",
    "CelesTrakAPI",
    "FeedConfig",
    "build_kafka_config",
    "parse_kafka_connection_string",
    "load_state",
    "save_state",
]
