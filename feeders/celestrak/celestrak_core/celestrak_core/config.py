"""Shared configuration models and connection-string parsers.

Every transport variant (Kafka, MQTT, AMQP) drives the same upstream CelesTrak
poller and therefore accepts the same upstream-side knobs: which GROUP views to
pull, whether the optional Supplemental GP (SupGP) sources are enabled, the
telemetry polling cadence, how often the SATCAT reference catalog is refreshed,
the dedup state file, and single-shot ``--once`` mode. Those live on
:class:`FeedConfig`.

The Kafka feeder additionally accepts a ``CONNECTION_STRING`` that may take one
of two shapes -- a Microsoft Event Hubs / Fabric Event Stream connection
string, or the internal ``BootstrapServer=...;EntityPath=...`` shape used by the
Docker E2E harness. Parsing those is shared here because the MQTT and AMQP
feeders never need them.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# Conservative defaults. CelesTrak publishes fresh GP element sets a few times a
# day, so polling far more often than hourly wastes their bandwidth and risks a
# usage-policy block; the SATCAT catalog changes even more slowly (new launches,
# decays) so it is refreshed daily by default.
DEFAULT_GROUPS = "stations"
DEFAULT_POLLING_INTERVAL = 3600
DEFAULT_REFERENCE_REFRESH_INTERVAL = 86400


def _split_csv(value: str) -> List[str]:
    """Split a comma/whitespace separated env value into a clean token list."""
    return [tok.strip() for tok in value.replace("\n", ",").split(",") if tok.strip()]


@dataclass
class FeedConfig:
    """Upstream-side configuration shared by every transport variant."""

    groups: List[str] = field(default_factory=lambda: [DEFAULT_GROUPS])
    supgp_sources: List[str] = field(default_factory=list)
    polling_interval: int = DEFAULT_POLLING_INTERVAL
    reference_refresh_interval: int = DEFAULT_REFERENCE_REFRESH_INTERVAL
    state_file: str = ""
    once: bool = False

    @classmethod
    def from_env(
        cls,
        *,
        groups: Optional[List[str]] = None,
        supgp_sources: Optional[List[str]] = None,
        polling_interval: Optional[int] = None,
        reference_refresh_interval: Optional[int] = None,
        state_file: Optional[str] = None,
        once: Optional[bool] = None,
    ) -> "FeedConfig":
        if groups is None:
            groups = _split_csv(os.getenv("CELESTRAK_GROUPS", DEFAULT_GROUPS)) or [DEFAULT_GROUPS]
        if supgp_sources is None:
            supgp_sources = _split_csv(os.getenv("SUPGP_SOURCES", ""))
        if polling_interval is None:
            polling_interval = int(os.getenv("POLLING_INTERVAL", str(DEFAULT_POLLING_INTERVAL)))
        if reference_refresh_interval is None:
            reference_refresh_interval = int(
                os.getenv("REFERENCE_REFRESH_INTERVAL", str(DEFAULT_REFERENCE_REFRESH_INTERVAL))
            )
        if state_file is None:
            state_file = os.getenv("STATE_FILE", os.path.expanduser("~/.celestrak_state.json"))
        if once is None:
            once = os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes")
        return cls(
            groups=groups,
            supgp_sources=supgp_sources,
            polling_interval=polling_interval,
            reference_refresh_interval=reference_refresh_interval,
            state_file=state_file,
            once=once,
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
