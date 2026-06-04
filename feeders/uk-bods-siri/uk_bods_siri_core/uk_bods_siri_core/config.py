from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class FeedConfig:
    bods_api_key: str
    polling_interval: int = 30
    operators: Optional[set[str]] = None
    state_file: str = ""
    once: bool = False

    @classmethod
    def from_env(
        cls,
        *,
        bods_api_key: Optional[str] = None,
        polling_interval: Optional[int] = None,
        operators: Optional[set[str]] = None,
        state_file: Optional[str] = None,
        once: Optional[bool] = None,
    ) -> "FeedConfig":
        if bods_api_key is None:
            bods_api_key = os.getenv("BODS_API_KEY", "")
        if polling_interval is None:
            polling_interval = int(os.getenv("POLLING_INTERVAL", "30"))
        if operators is None:
            raw = os.getenv("OPERATORS", "")
            operators = {token.strip() for token in raw.split(",") if token.strip()} or None
        if state_file is None:
            state_file = os.getenv("STATE_FILE", os.path.expanduser("~/.uk_bods_siri_state.json"))
        if once is None:
            once = os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes")
        return cls(
            bods_api_key=bods_api_key or "",
            polling_interval=polling_interval,
            operators=operators,
            state_file=state_file,
            once=once,
        )


def parse_kafka_connection_string(connection_string: str) -> Dict[str, str]:
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
