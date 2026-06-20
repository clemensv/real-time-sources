from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, Iterable, Mapping, Optional

SUPPORTED_PROVIDERS = ("bods", "trafiklab", "entur", "custom")
SUPPORTED_DATA_TYPES = ("vm", "et", "sx")
DEFAULT_BODS_URL = "https://data.bus-data.dft.gov.uk/avl/download/bulk_archive"
DEFAULT_TRAFIKLAB_URL = "https://api.trafiklab.se/siri2.x/{data_type}/{operator}"
DEFAULT_ENTUR_URL = "https://api.entur.io/realtime/v1/rest/{data_type}"
DEFAULT_ENTUR_CLIENT_NAME = "clemensv-realtimesources"


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


def parse_request_headers(value: Optional[str]) -> dict[str, str]:
    if not value:
        return {}
    headers: dict[str, str] = {}
    for part in value.replace("\n", ";").split(";"):
        part = part.strip()
        if not part:
            continue
        if "=" not in part:
            raise ValueError(f"Invalid SIRI header '{part}'. Expected NAME=VALUE.")
        name, header_value = part.split("=", 1)
        name = name.strip()
        header_value = header_value.strip()
        if not name:
            raise ValueError("Invalid SIRI header with empty name.")
        headers[name] = header_value
    return headers


def _has_header(headers: Mapping[str, str], name: str) -> bool:
    return any(header_name.lower() == name.lower() for header_name in headers)


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
    request_headers: dict[str, str] = field(default_factory=dict)

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
        request_headers: Optional[Mapping[str, str] | str] = None,
        et_client_name: Optional[str] = None,
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
            if provider == "bods":
                siri_url = DEFAULT_BODS_URL
            elif provider == "trafiklab":
                siri_url = DEFAULT_TRAFIKLAB_URL
            elif provider == "entur":
                siri_url = DEFAULT_ENTUR_URL

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
        if request_headers is None:
            resolved_headers = parse_request_headers(os.getenv("SIRI_HEADERS"))
        elif isinstance(request_headers, str):
            resolved_headers = parse_request_headers(request_headers)
        else:
            resolved_headers = {str(key).strip(): str(value).strip() for key, value in request_headers.items() if str(key).strip()}
        if et_client_name is None:
            et_client_name = os.getenv("SIRI_ET_CLIENT_NAME", "").strip()
        if et_client_name:
            resolved_headers["ET-Client-Name"] = et_client_name
        elif provider == "entur" and not _has_header(resolved_headers, "ET-Client-Name"):
            resolved_headers["ET-Client-Name"] = DEFAULT_ENTUR_CLIENT_NAME
        return cls(
            provider=provider,
            siri_url=siri_url,
            api_key=api_key or "",
            operators=operators,
            data_types=resolved_data_types,
            polling_interval=polling_interval,
            state_file=state_file,
            once=once,
            request_headers=resolved_headers,
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
