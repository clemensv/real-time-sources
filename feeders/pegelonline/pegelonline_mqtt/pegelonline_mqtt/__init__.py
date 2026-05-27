"""MQTT/UNS feeder for the PegelOnline source.

Publishes the same upstream PegelOnline data the Kafka feeder consumes, but
into a Unified-Namespace MQTT 5.0 topic tree under the ``hydro/`` umbrella:

    hydro/de/wsv/pegelonline/{water_shortname}/{station_id}/info
    hydro/de/wsv/pegelonline/{water_shortname}/{station_id}/water-level

CloudEvent attributes ride as MQTT 5 user properties (binary content mode),
the JSON-encoded payload sits in the MQTT message body, and both leaves are
retained at QoS 1 so subscribers get the latest known state on connect.
"""

from .app import main, feed

__all__ = ["main", "feed"]
