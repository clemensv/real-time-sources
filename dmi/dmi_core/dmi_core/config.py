"""Shared configuration helpers for the DMI feeders.

DMI Open Data uses three independent products, each gated by its own API key.
The :class:`DmiApiKeys` dataclass keeps the three keys together and resolves
them from environment variables so the feeders can stay symmetric on the CLI.
The Kafka connection-string parser mirrors the one used by every other source
in this repository so existing deployment templates keep working.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class FeedConfig:
    """Upstream-side configuration shared by every transport variant."""

    polling_interval: int = 300
    state_file: str = ""
    once: bool = False

    @classmethod
    def from_env(
        cls,
        *,
        polling_interval: Optional[int] = None,
        state_file: Optional[str] = None,
        once: Optional[bool] = None,
    ) -> "FeedConfig":
        if polling_interval is None:
            polling_interval = int(os.getenv("POLLING_INTERVAL", "300"))
        if state_file is None:
            state_file = os.getenv("STATE_FILE", os.path.expanduser("~/.dmi_state.json"))
        if once is None:
            once = os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes")
        return cls(polling_interval=polling_interval, state_file=state_file, once=once)


@dataclass
class DmiApiKeys:
    """API keys for the three DMI Open Data v2 products."""

    met_obs: str = ""
    ocean_obs: str = ""
    lightning: str = ""

    @classmethod
    def from_env(
        cls,
        *,
        met_obs: Optional[str] = None,
        ocean_obs: Optional[str] = None,
        lightning: Optional[str] = None,
    ) -> "DmiApiKeys":
        # A single DMI_API_KEY (rare) is accepted as a fallback used by all three;
        # in practice DMI issues a different key per product so the specific
        # variables are preferred.
        fallback = os.getenv("DMI_API_KEY", "")
        return cls(
            met_obs=met_obs if met_obs is not None else os.getenv("DMI_METOBS_API_KEY", fallback),
            ocean_obs=ocean_obs if ocean_obs is not None else os.getenv("DMI_OCEANOBS_API_KEY", fallback),
            lightning=lightning if lightning is not None else os.getenv("DMI_LIGHTNING_API_KEY", fallback),
        )


def parse_kafka_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Event Hubs / Fabric / harness connection string into rdkafka knobs."""
    config: Dict[str, str] = {}
    for part in connection_string.split(";"):
        if "Endpoint" in part:
            host = (
                part.split("=", 1)[1]
                .strip()
                .strip('"')
                .replace("sb://", "")
                .replace("/", "")
            )
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
        cfg.update(
            {
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_username,
                "sasl.password": sasl_password,
            }
        )
    elif tls_enabled:
        cfg["security.protocol"] = "SSL"
    return cfg
