"""Shared configuration models and connection-string parsers.

The HSL HFP source feeds three downstream transports (Kafka, MQTT, AMQP) from a
single upstream MQTT subscription. Everything in this module is transport- and
producer-agnostic so the three transport apps share one acquisition core.

The upstream side is identical for every transport: the same ``mqtt.hsl.fi``
broker, the same ``journey``-tree subscription filter, and the same GTFS-static
reference-refresh cadence. Those knobs live on :class:`FeedConfig`.

The Kafka feeder additionally accepts a ``CONNECTION_STRING`` that may take one
of two shapes -- a Microsoft Event Hubs / Fabric Event Stream connection
string, or the internal ``BootstrapServer=...;EntityPath=...`` shape used by the
Docker E2E harness. Parsing those is shared here because the other transports
never need them.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# Upstream broker defaults (anonymous, TLS). See
# https://digitransit.fi/en/developers/apis/5-realtime-api/vehicle-positions/high-frequency-positioning/
HFP_DEFAULT_HOST = "mqtt.hsl.fi"
HFP_DEFAULT_PORT = 8883
# Source URI stamped into the CloudEvents ``source`` attribute.
HFP_FEED_URL = "mqtts://mqtt.hsl.fi:8883/hfp/v2/journey"
# Canonical HSL GTFS static feed (CC BY 4.0). Routes and stops are pulled from
# here at start-up and on a periodic refresh and emitted as reference events.
HSL_GTFS_URL = "https://infopalvelut.storage.hsldev.com/gtfs/hsl.zip"


@dataclass
class FeedConfig:
    """Upstream-side configuration shared by every transport variant."""

    # MQTT subscription filters (full HFP topic filters, each terminated with a
    # multi-level ``#`` wildcard by the source). Default is the whole journey
    # tree. Narrow by mode/route/operator via HFP_TOPIC_FILTERS (comma list).
    topic_filters: List[str] = field(default_factory=lambda: ["/hfp/v2/journey/#"])
    upstream_host: str = HFP_DEFAULT_HOST
    upstream_port: int = HFP_DEFAULT_PORT
    upstream_tls: bool = True
    # Seconds between GTFS-static reference refreshes. HSL rebuilds the feed
    # roughly daily; default 12h. ``0`` disables periodic refresh (start-up
    # emission only).
    reference_refresh_interval: int = 12 * 3600
    # Skip the (large, ~75 MB) GTFS download entirely -- telemetry only.
    skip_reference: bool = False
    gtfs_url: str = HSL_GTFS_URL
    once: bool = False

    @classmethod
    def from_env(cls) -> "FeedConfig":
        filters_env = os.getenv("HFP_TOPIC_FILTERS", "").strip()
        topic_filters = (
            [t.strip() for t in filters_env.split(",") if t.strip()]
            if filters_env
            else ["/hfp/v2/journey/#"]
        )
        return cls(
            topic_filters=topic_filters,
            upstream_host=os.getenv("HFP_MQTT_HOST", HFP_DEFAULT_HOST),
            upstream_port=int(os.getenv("HFP_MQTT_PORT", str(HFP_DEFAULT_PORT))),
            upstream_tls=os.getenv("HFP_MQTT_TLS", "true").lower() not in ("false", "0", "no"),
            reference_refresh_interval=int(os.getenv("REFERENCE_REFRESH_INTERVAL", str(12 * 3600))),
            skip_reference=os.getenv("SKIP_REFERENCE", "").lower() in ("1", "true", "yes"),
            gtfs_url=os.getenv("HSL_GTFS_URL", HSL_GTFS_URL),
            once=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
        )


def parse_kafka_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Event Hubs / Fabric / harness connection string into rdkafka knobs.

    Supported keys (case-sensitive, semicolon-separated):
      * ``Endpoint=sb://<ns>.servicebus.windows.net/`` -> bootstrap server with
        ``:9093`` and SASL_SSL+PLAIN mechanism.
      * ``BootstrapServer=host:port`` -> plain bootstrap server.
      * ``EntityPath=<topic>`` -> Kafka topic.
      * ``SharedAccessKeyName`` / ``SharedAccessKey`` -> SASL credentials.
    """
    config: Dict[str, str] = {}
    for part in connection_string.split(";"):
        if "Endpoint" in part:
            host = part.split("=", 1)[1].strip().strip('"').replace("sb://", "").replace("/", "")
            config["bootstrap.servers"] = f"{host}:9093"
        elif "BootstrapServer" in part:
            config["bootstrap.servers"] = part.split("=", 1)[1].strip()
        elif "EntityPath" in part:
            config["kafka_topic"] = part.split("=", 1)[1].strip().strip('"')
        elif "SharedAccessKeyName" in part:
            config["sasl.username"] = "$ConnectionString"
        elif "SharedAccessKey" in part:
            config["sasl.password"] = connection_string.strip()
    if "sasl.username" in config:
        config["security.protocol"] = "SASL_SSL"
        config["sasl.mechanism"] = "PLAIN"
    return config


def build_kafka_config(
    *,
    bootstrap_servers: str,
    sasl_username: Optional[str] = None,
    sasl_password: Optional[str] = None,
    tls_enabled: bool = True,
) -> Dict[str, str]:
    """Compose an rdkafka producer config from individual knobs."""
    cfg: Dict[str, str] = {"bootstrap.servers": bootstrap_servers}
    if sasl_username and sasl_password:
        cfg.update({
            "sasl.mechanisms": "PLAIN",
            "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
            "sasl.username": sasl_username,
            "sasl.password": sasl_password,
        })
    elif tls_enabled:
        cfg["security.protocol"] = "SSL"
    return cfg
