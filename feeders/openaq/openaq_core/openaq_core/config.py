from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

DEFAULT_SOURCES_FILE = os.path.join(os.path.dirname(__file__), "sources", "openaq-sources.json")
_ENV_REF = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

TRUE_VALUES = {"1", "true", "yes", "on"}
FALSE_VALUES = {"0", "false", "no", "off"}


@dataclass(frozen=True)
class OpenAQQuerySlice:
    countries: list[str]
    locations: list[int]
    bbox: Optional[str] = None
    page_limit: int = 25
    max_pages: int = 1


def parse_bool(value: object, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if not text:
        return default
    if text in TRUE_VALUES:
        return True
    if text in FALSE_VALUES:
        return False
    return default


def parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    text = value.strip()
    if not text:
        return []
    if text.startswith("@"):
        return [line.strip() for line in Path(text[1:]).expanduser().read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#")]
    possible = Path(text).expanduser()
    if possible.exists() and possible.is_file():
        return [line.strip() for line in possible.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#")]
    return [part.strip() for part in text.split(",") if part.strip()]


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
        return Path(raw[1:].strip()).expanduser().read_text(encoding="utf-8")
    if raw.startswith("[") or raw.startswith("{"):
        return raw
    possible = Path(raw).expanduser()
    if possible.exists():
        return possible.read_text(encoding="utf-8")
    return raw


def _coerce_entries(data: Any) -> list[dict[str, Any]]:
    """Accept either a {"sources": [...]} catalog or a bare list of entries."""
    if isinstance(data, dict):
        data = data.get("sources", [])
    if not isinstance(data, list):
        return []
    return [dict(item) for item in data if isinstance(item, dict)]


def select_entries(entries: list[dict[str, Any]], selector: str = "") -> list[dict[str, Any]]:
    """Filter catalog entries by the OPENAQ_SOURCES selector.

    Empty selector -> every entry whose ``enabled`` flag is true (default true).
    ``*`` -> every entry, including disabled templates.
    Otherwise a comma-separated allow-list of entry ``name`` values, returned in
    the order requested. An unknown name raises ``ValueError``.
    """
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
        raise ValueError(f"Unknown OPENAQ_SOURCES entries: {', '.join(unknown)}. Known names: {known}")
    return chosen


def _csv_or_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return parse_csv(str(value))


def _int_list(value: Any) -> list[int]:
    return [int(item) for item in _csv_or_list(value)]


def _entries_to_slices(entries: Iterable[dict[str, Any]], default_page_limit: int = 25, default_max_pages: int = 1) -> list[OpenAQQuerySlice]:
    slices: list[OpenAQQuerySlice] = []
    for raw_item in entries:
        item = dict(_interpolate_env(raw_item))
        for metadata_key in ("name", "enabled", "description"):
            item.pop(metadata_key, None)
        slices.append(OpenAQQuerySlice(
            countries=[country.upper() for country in _csv_or_list(item.get("countries") or item.get("country"))],
            locations=_int_list(item.get("locations") or item.get("location_ids")),
            bbox=(str(item.get("bbox")).strip() or None) if item.get("bbox") is not None else None,
            page_limit=int(item.get("page_limit") or default_page_limit),
            max_pages=int(item.get("max_pages") or default_max_pages),
        ))
    return slices


def load_query_slices(
    openaq_countries: Optional[str] = None,
    openaq_locations: Optional[str] = None,
    openaq_bbox: Optional[str] = None,
    page_limit: int = 25,
    max_pages: int = 1,
    raw: str = "",
    mock: bool = False,
    sources_file: str = "",
    selector: str = "",
) -> list[OpenAQQuerySlice]:
    """Resolve OpenAQ query slices to poll.

    Legacy single-query variables (OPENAQ_COUNTRIES, OPENAQ_LOCATIONS, or
    OPENAQ_BBOX) take precedence over the catalog. Otherwise the loader reads
    a configured catalog file or the packaged default and applies
    OPENAQ_SOURCES selection.
    """
    del mock
    if any(value and str(value).strip() for value in (openaq_countries, openaq_locations, openaq_bbox)):
        return [OpenAQQuerySlice(
            countries=[country.upper() for country in parse_csv(openaq_countries or "US")],
            locations=_int_list(openaq_locations),
            bbox=(openaq_bbox.strip() if openaq_bbox and openaq_bbox.strip() else None),
            page_limit=page_limit,
            max_pages=max_pages,
        )]
    if raw and raw.strip():
        entries = _coerce_entries(json.loads(_read_config_text(raw)))
    else:
        path = sources_file.strip() if sources_file and sources_file.strip() else DEFAULT_SOURCES_FILE
        with open(path, "r", encoding="utf-8") as handle:
            entries = _coerce_entries(json.load(handle))
    return _entries_to_slices(select_entries(entries, selector), default_page_limit=page_limit, default_max_pages=max_pages)


def load_state(path: str) -> Dict[str, Any]:
    try:
        return json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except Exception:
        return {}


def save_state(path: str, state: Dict[str, Any]) -> None:
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(state, sort_keys=True, indent=2), encoding="utf-8")


def parse_kafka_connection_string(connection_string: str) -> Dict[str, str]:
    config_dict: Dict[str, str] = {}
    for part in connection_string.split(";"):
        if "Endpoint" in part:
            config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
        elif "EntityPath" in part:
            config_dict["kafka_topic"] = part.split("=", 1)[1].strip('"')
        elif "SharedAccessKeyName" in part:
            config_dict["sasl.username"] = "$ConnectionString"
        elif "SharedAccessKey" in part:
            config_dict["sasl.password"] = connection_string.strip()
        elif "BootstrapServer" in part:
            config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


def build_kafka_config(bootstrap_servers: str, sasl_username: str | None = None, sasl_password: str | None = None, tls_enabled: bool = True) -> Dict[str, str]:
    config = {"bootstrap.servers": bootstrap_servers, "client.id": "openaq"}
    if tls_enabled:
        config["security.protocol"] = "SASL_SSL" if sasl_username and sasl_password else "SSL"
    else:
        config["security.protocol"] = "SASL_PLAINTEXT" if sasl_username and sasl_password else "PLAINTEXT"
    if sasl_username and sasl_password:
        config["sasl.mechanism"] = "PLAIN"
        config["sasl.username"] = sasl_username
        config["sasl.password"] = sasl_password
    return config
