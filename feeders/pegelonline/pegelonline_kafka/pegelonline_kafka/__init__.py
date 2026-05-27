"""Kafka feeder for the PegelOnline source.

This module is the Kafka-specific binding on top of :mod:`pegelonline_core`.
It owns the lifetime of the confluent-kafka producer, drives the polling
loop, and dispatches reference (``Station``) and telemetry
(``CurrentMeasurement``) CloudEvents through the generated
:class:`DeWsvPegelonlineKafkaEventProducer`. The Kafka key for every message
is the upstream station UUID, matching the CloudEvent ``subject`` exactly per
the repository keying contract.
"""

from .app import main, feed

__all__ = ["main", "feed"]
