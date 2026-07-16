"""Kafka feeder for the CelesTrak source.

This module is the Kafka-specific binding on top of :mod:`celestrak_core`. It
owns the lifetime of the confluent-kafka producer, drives the polling loop, and
dispatches reference (``SatelliteCatalogEntry``) and telemetry
(``OrbitMeanElements`` / ``SupplementalOrbitMeanElements``) CloudEvents through
the generated :class:`OrgCelestrakKafkaEventProducer`. The Kafka key for every
message is the object's ``NORAD_CAT_ID``, matching the CloudEvent ``subject``
exactly per the repository keying contract.
"""

from .app import main, feed

__all__ = ["main", "feed"]
