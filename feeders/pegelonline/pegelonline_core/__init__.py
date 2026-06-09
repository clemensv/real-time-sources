"""Compatibility shim for the local pegelonline_core package layout."""

from .pegelonline_core import *  # noqa: F401,F403

__all__ = [
    "PegelOnlineAPI",
    "FEED_URL_ROOT",
    "FeedConfig",
    "build_kafka_config",
    "parse_kafka_connection_string",
    "load_state",
    "save_state",
]
