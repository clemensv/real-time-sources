"""Transport-agnostic core for the NOAA SWPC L1 propagated solar wind bridge.

The source ships three sibling transport feeders (Kafka, MQTT, AMQP 1.0) from
a single upstream poller. This package contains everything shared between the
three — the SWPC HTTP client, header parsing, row normalization, dedup state,
and Kafka connection-string helpers — and intentionally has no producer
dependency. Each transport-specific feeder consumes :class:`SwpcL1API`,
:class:`FeedConfig` and the normalized row dataclass and pushes the rows into
its own generated CloudEvents producer.
"""

from .acquisition import (
    FEED_URL,
    EXPECTED_COLUMNS,
    SwpcL1API,
    PropagatedSolarWindRow,
    parse_row,
)
from .config import (
    FeedConfig,
    build_kafka_config,
    parse_kafka_connection_string,
)
from .state import load_state, save_state

__all__ = [
    "FEED_URL",
    "EXPECTED_COLUMNS",
    "SwpcL1API",
    "PropagatedSolarWindRow",
    "parse_row",
    "FeedConfig",
    "build_kafka_config",
    "parse_kafka_connection_string",
    "load_state",
    "save_state",
]
