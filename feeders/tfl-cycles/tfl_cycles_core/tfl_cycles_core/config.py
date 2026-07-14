"""Shared configuration models and connection-string parsers.

Every transport variant accepts the same upstream-side knobs: polling interval,
dedup state file, single-shot ``--once`` mode. Those live on :class:`FeedConfig`.

The Kafka feeder additionally accepts a ``CONNECTION_STRING`` that may take one
of two shapes -- a Microsoft Event Hubs / Fabric Event Stream connection string,
or the internal ``BootstrapServer=...;EntityPath=...`` shape used by the Docker
E2E harness. Parsing those is also shared because the MQTT and AMQP feeders
never need them.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class FeedConfig:
    """Upstream-side configuration shared by every transport variant."""

    polling_interval: int = 60
    state_file: str = ""
    once: bool = False
    reference_refresh_interval: int = 3600

    @classmethod
    def from_env(cls, *, polling_interval: Optional[int] = None,
                 state_file: Optional[str] = None,
                 once: Optional[bool] = None,
                 reference_refresh_interval: Optional[int] = None) -> "FeedConfig":
        if polling_interval is None:
            polling_interval = int(os.getenv("POLLING_INTERVAL", "60"))
        if state_file is None:
            state_file = os.getenv("STATE_FILE", os.path.expanduser("~/.tfl_cycles_state.json"))
        if once is None:
            once = os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes")
        if reference_refresh_interval is None:
            reference_refresh_interval = int(os.getenv("REFERENCE_REFRESH_INTERVAL", "3600"))
        return cls(polling_interval=polling_interval, state_file=state_file, once=once,
                   reference_refresh_interval=reference_refresh_interval)


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
    cfg: Dict[str, str] = {"bootstrap.servers": bootstrap_servers, "client.id": "tfl-cycles"}
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
