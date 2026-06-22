from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Mapping, Optional

SUPPORTED_PROVIDERS = ("bods", "trafiklab", "entur", "custom")
SUPPORTED_DATA_TYPES = ("vm", "et", "sx")
DEFAULT_BODS_URL = "https://data.bus-data.dft.gov.uk/avl/download/bulk_archive"
DEFAULT_TRAFIKLAB_URL = "https://api.trafiklab.se/siri2.x/{data_type}/{operator}"
DEFAULT_ENTUR_URL = "https://api.entur.io/realtime/v1/rest/{data_type}"
DEFAULT_ENTUR_CLIENT_NAME = "clemensv-realtimesources"
DEFAULT_SOURCES_FILE = os.path.join(os.path.dirname(__file__), "sources", "siri-sources.json")
_ENV_REF = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


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


def _interpolate_env(value: Any) -> Any:
    """Expand ${ENV_VAR} placeholders in strings (recursing into lists/dicts)."""
    if isinstance(value, str):
        return _ENV_REF.sub(lambda match: os.environ.get(match.group(1), ""), value)
    if isinstance(value, list):
        return [_interpolate_env(item) for item in value]
    if isinstance(value, dict):
        return {key: _interpolate_env(item) for key, item in value.items()}
    return value


def _read_config_text(raw: str) -> str:
    """Resolve an inline-config string: JSON literal, @path, or bare path."""
    raw = raw.strip()
    if raw.startswith("@"):
        with open(raw[1:].strip(), "r", encoding="utf-8") as handle:
            return handle.read()
    if raw.startswith("[") or raw.startswith("{"):
        return raw
    if os.path.exists(raw):
        with open(raw, "r", encoding="utf-8") as handle:
            return handle.read()
    return raw


def _coerce_entries(data: Any) -> list[dict[str, Any]]:
    """Accept either a {"sources": [...]} catalog or a bare list of entries."""
    if isinstance(data, dict):
        data = data.get("sources", [])
    if not isinstance(data, list):
        return []
    return [dict(item) for item in data if isinstance(item, dict)]


def select_entries(entries: list[dict[str, Any]], selector: str = "") -> list[dict[str, Any]]:
    """Filter catalog entries by the SIRI_SOURCES selector."""
    selector = (selector or "").strip()
    if selector == "*":
        return list(entries)
    if not selector:
        return [entry for entry in entries if entry.get("enabled", True)]
    by_name = {entry["name"]: entry for entry in entries if entry.get("name")}
    chosen: list[dict[str, Any]] = []
    unknown: list[str] = []
    for token in (part.strip() for part in selector.split(",")):
        if not token:
            continue
        if token in by_name:
            chosen.append(by_name[token])
        else:
            unknown.append(token)
    if unknown:
        known = ", ".join(sorted(by_name)) or "(none)"
        raise ValueError(f"Unknown SIRI_SOURCES entries: {', '.join(unknown)}. Known names: {known}")
    return chosen


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
        operators: Optional[Iterable[str] | str] = None,
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
        elif isinstance(operators, str):
            operators = parse_csv_tokens(operators)
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


def _legacy_single_source_requested(*, provider: Optional[str] = None, siri_url: Optional[str] = None) -> bool:
    resolved_provider = (provider if provider is not None else os.getenv("SIRI_PROVIDER", "bods") or "bods").strip().lower()
    resolved_url = (siri_url if siri_url is not None else os.getenv("SIRI_URL", "") or "").strip()
    return bool(resolved_url) or resolved_provider != "bods"


def _entry_to_config(entry: Mapping[str, Any]) -> FeedConfig:
    item = dict(_interpolate_env(dict(entry)))
    for key in ("name", "enabled", "description"):
        item.pop(key, None)
    if "base_url" in item and "siri_url" not in item:
        item["siri_url"] = item.pop("base_url")
    if "url" in item and "siri_url" not in item:
        item["siri_url"] = item.pop("url")
    if "headers" in item and "request_headers" not in item:
        item["request_headers"] = item.pop("headers")
    return FeedConfig.from_env(
        provider=item.get("provider"),
        siri_url=item.get("siri_url"),
        api_key=item.get("api_key"),
        operators=item.get("operators"),
        data_types=item.get("data_types"),
        request_headers=item.get("request_headers"),
        et_client_name=item.get("et_client_name"),
    )


def load_feed_configs(
    raw: str = "",
    *,
    sources_file: str = "",
    selector: str = "",
    provider: Optional[str] = None,
    siri_url: Optional[str] = None,
    api_key: Optional[str] = None,
    operators: Optional[Iterable[str] | str] = None,
    data_types: Optional[Iterable[str] | str] = None,
    polling_interval: Optional[int] = None,
    state_file: Optional[str] = None,
    once: Optional[bool] = None,
    request_headers: Optional[Mapping[str, str] | str] = None,
    et_client_name: Optional[str] = None,
) -> list[FeedConfig]:
    """Load SIRI source configs from legacy env/CLI or the source catalog.

    Legacy single-source configuration takes precedence when SIRI_URL is set or
    SIRI_PROVIDER resolves to anything other than the default BODS profile.
    """
    if raw and raw.strip():
        entries = _coerce_entries(json.loads(_read_config_text(raw)))
    elif _legacy_single_source_requested(provider=provider, siri_url=siri_url):
        return [
            FeedConfig.from_env(
                provider=provider,
                siri_url=siri_url,
                api_key=api_key,
                operators=operators,
                data_types=data_types,
                polling_interval=polling_interval,
                state_file=state_file,
                once=once,
                request_headers=request_headers,
                et_client_name=et_client_name,
            )
        ]
    else:
        path = sources_file.strip() if sources_file and sources_file.strip() else DEFAULT_SOURCES_FILE
        with open(path, "r", encoding="utf-8") as handle:
            entries = _coerce_entries(json.load(handle))
    configs = [_entry_to_config(entry) for entry in select_entries(entries, selector)]
    if polling_interval is not None or state_file is not None or once is not None:
        configs = [
            FeedConfig(
                provider=config.provider,
                siri_url=config.siri_url,
                api_key=config.api_key,
                operators=config.operators,
                data_types=config.data_types,
                polling_interval=polling_interval if polling_interval is not None else config.polling_interval,
                state_file=state_file if state_file is not None else config.state_file,
                once=once if once is not None else config.once,
                request_headers=config.request_headers,
            )
            for config in configs
        ]
    return configs


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
