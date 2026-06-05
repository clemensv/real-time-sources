from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Iterable, Optional

SUPPORTED_PROVIDERS = ("bods", "trafiklab", "custom")
SUPPORTED_DATA_TYPES = ("vm", "et", "sx")
DEFAULT_BODS_URL = "https://data.bus-data.dft.gov.uk/avl/download/bulk_archive"
DEFAULT_TRAFIKLAB_URL = "https://api.trafiklab.se/siri2.x/{data_type}/{operator}"


def parse_csv_tokens(value: Optional[str]) -> Optional[tuple[str, ...]]:
    if value is None:
        return None
    tokens = tuple(token.strip() for token in value.split(",") if token.strip())
    return tokens or None


def parse_data_types(value: Optional[str]) -> tuple[str, ...]:
    tokens = parse_csv_tokens(value)
    if not tokens:
        return ("vm",)
    normalized: list[str] = []
    for token in tokens:
        lowered = token.lower()
        if lowered not in SUPPORTED_DATA_TYPES:
            raise ValueError(f"Unsupported SIRI data type '{token}'. Expected one of: {', '.join(SUPPORTED_DATA_TYPES)}")
        if lowered not in normalized:
            normalized.append(lowered)
    return tuple(normalized)


@dataclass
class FeedConfig:
    provider: str = "bods"
    siri_url: str = ""
    api_key: str = ""
    operators: Optional[tuple[str, ...]] = None
    data_types: tuple[str, ...] = ("vm",)
    polling_interval: int = 30
    state_file: str = ""
    once: bool = False

    @classmethod
    def from_env(
        cls,
        *,
        provider: Optional[str] = None,
        siri_url: Optional[str] = None,
        api_key: Optional[str] = None,
        operators: Optional[Iterable[str]] = None,
        data_types: Optional[Iterable[str] | str] = None,
        polling_interval: Optional[int] = None,
        state_file: Optional[str] = None,
        once: Optional[bool] = None,
    ) -> "FeedConfig":
        if provider is None:
            provider = os.getenv("SIRI_PROVIDER", "bods")
        provider = (provider or "bods").strip().lower()
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported SIRI provider '{provider}'. Expected one of: {', '.join(SUPPORTED_PROVIDERS)}")

        if siri_url is None:
            siri_url = os.getenv("SIRI_URL", "")
        siri_url = (siri_url or "").strip()
        if not siri_url:
            siri_url = DEFAULT_BODS_URL if provider == "bods" else (DEFAULT_TRAFIKLAB_URL if provider == "trafiklab" else "")

        if api_key is None:
            api_key = os.getenv("SIRI_API_KEY") or os.getenv("BODS_API_KEY", "")

        if operators is None:
            operators = parse_csv_tokens(os.getenv("SIRI_OPERATORS") or os.getenv("OPERATORS"))
        elif not isinstance(operators, tuple):
            operators = tuple(token.strip() for token in operators if token and token.strip()) or None

        if data_types is None:
            resolved_data_types = parse_data_types(os.getenv("SIRI_DATA_TYPES", "vm"))
        elif isinstance(data_types, str):
            resolved_data_types = parse_data_types(data_types)
        else:
            resolved_data_types = parse_data_types(",".join(token for token in data_types if token))

        if polling_interval is None:
            polling_interval = int(os.getenv("POLLING_INTERVAL", "30"))
        if state_file is None:
            state_file = os.getenv("STATE_FILE", os.path.expanduser("~/.siri_state.json"))
        if once is None:
            once = os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes")
        return cls(
            provider=provider,
            siri_url=siri_url,
            api_key=api_key or "",
            operators=operators,
            data_types=resolved_data_types,
            polling_interval=polling_interval,
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
