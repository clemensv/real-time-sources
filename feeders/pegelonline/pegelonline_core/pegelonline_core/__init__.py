"""Transport-agnostic core for the PegelOnline bridge.

The PegelOnline source feeds two transports (Apache Kafka and MQTT/UNS) from a
single upstream poller. This package contains everything that is shared between
the two — the HTTP client, the polling loop, the Kafka connection-string
parsing, dedup-state persistence — and intentionally has no producer
dependency. Each transport-specific feeder consumes :class:`PegelOnlineAPI`,
:class:`FeedConfig` and the ``poll_measurements`` generator and pushes the
upstream JSON dictionaries into its own generated CloudEvents producer.
"""

from .acquisition import PegelOnlineAPI, FEED_URL_ROOT
from .config import FeedConfig, build_kafka_config, parse_kafka_connection_string
from .state import load_state, save_state

__all__ = [
    "PegelOnlineAPI",
    "FEED_URL_ROOT",
    "FeedConfig",
    "build_kafka_config",
    "parse_kafka_connection_string",
    "load_state",
    "save_state",
]
