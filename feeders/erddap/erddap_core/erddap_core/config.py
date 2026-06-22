
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_SOURCES = "ioos-sensors|https://erddap.sensors.ioos.us/erddap|org_cormp_sun2|sea_water_temperature,sea_water_practical_salinity|station|time>=max(time)-1day"
DEFAULT_SOURCES_FILE = os.path.join(os.path.dirname(__file__), "sources", "erddap-sources.json")
TRUE_VALUES = {"1", "true", "yes", "on"}
_ENV_REF = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


@dataclass(frozen=True)
class ErddapSource:
    erddap_id: str
    base_url: str
    dataset_id: str
    variables: List[str]
    station_id_variable: Optional[str] = None
    time_constraint: str = "time>=max(time)-1day"
    auth_header: Optional[str] = None


def parse_bool(value: object, default: bool = False) -> bool:
    if value is None:
        return default
    text = str(value).strip().lower()
    return default if not text else text in TRUE_VALUES


def _interpolate_env(value: Any) -> Any:
    """Expand ${ENV_VAR} placeholders in strings, recursing through lists/dicts."""
    if isinstance(value, str):
        return _ENV_REF.sub(lambda match: os.environ.get(match.group(1), ""), value)
    if isinstance(value, list):
        return [_interpolate_env(item) for item in value]
    if isinstance(value, dict):
        return {key: _interpolate_env(item) for key, item in value.items()}
    return value


def _read_text_or_value(value: str) -> str:
    text = value.strip()
    if text.startswith("@"):
        return Path(text[1:]).expanduser().read_text(encoding="utf-8")
    path = Path(text).expanduser()
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8")
    return text


def _coerce_entries(data: Any) -> List[Dict[str, Any]]:
    """Accept either a {"sources": [...]} catalog or a bare list of entries."""
    if isinstance(data, dict):
        data = data.get("sources", [])
    if not isinstance(data, list):
        return []
    return [dict(item) for item in data if isinstance(item, dict)]


def select_entries(entries: List[Dict[str, Any]], selector: str = "") -> List[Dict[str, Any]]:
    """Filter catalog entries by ERDDAP_SELECT.

    Empty selector -> every entry whose ``enabled`` flag is true (default true).
    ``*`` -> every entry, including disabled templates.
    Otherwise a comma-separated allow-list of entry ``name`` values, returned in
    the requested order. An unknown name raises ``ValueError``.
    """
    selector = (selector or "").strip()
    if selector == "*":
        return list(entries)
    if not selector:
        return [entry for entry in entries if entry.get("enabled", True)]
    by_name = {entry["name"]: entry for entry in entries if entry.get("name")}
    chosen: List[Dict[str, Any]] = []
    unknown: List[str] = []
    for token in (part.strip() for part in selector.split(",")):
        if not token:
            continue
        if token in by_name:
            chosen.append(by_name[token])
        else:
            unknown.append(token)
    if unknown:
        known = ", ".join(sorted(by_name)) or "(none)"
        raise ValueError(f"Unknown ERDDAP_SELECT entries: {', '.join(unknown)}. Known names: {known}")
    return chosen


def _parse_pipe_entries(raw: str) -> List[ErddapSource]:
    sources: List[ErddapSource] = []
    for item in raw.replace("\n", ";").split(";"):
        item = item.strip()
        if not item or item.startswith("#"):
            continue
        parts = [p.strip() for p in item.split("|")]
        if len(parts) < 4:
            raise ValueError("ERDDAP source entries must be erddap_id|base_url|dataset_id|variables[|station_id_variable|time_constraint]")
        sources.append(ErddapSource(
            parts[0],
            parts[1].rstrip("/"),
            parts[2],
            [v.strip() for v in parts[3].split(",") if v.strip()],
            parts[4] or None if len(parts) > 4 else None,
            parts[5] if len(parts) > 5 and parts[5] else "time>=max(time)-1day",
        ))
    return sources


def _entries_to_sources(entries: List[Dict[str, Any]]) -> List[ErddapSource]:
    allowed = {field.name for field in fields(ErddapSource)}
    sources: List[ErddapSource] = []
    for raw_item in entries:
        item = {key: value for key, value in _interpolate_env(raw_item).items() if key in allowed}
        item["base_url"] = str(item["base_url"]).rstrip("/")
        item["dataset_id"] = str(item["dataset_id"])
        item["erddap_id"] = str(item["erddap_id"])
        item["variables"] = [str(v) for v in item.get("variables", [])]
        item["station_id_variable"] = item.get("station_id_variable")
        item["time_constraint"] = str(item.get("time_constraint") or "time>=max(time)-1day")
        item["auth_header"] = item.get("auth_header")
        sources.append(ErddapSource(**item))
    return sources


def parse_sources(value: Optional[str], mock: bool = False, sources_file: str = "", selector: str = "") -> List[ErddapSource]:
    """Resolve ERDDAP tabledap sources.

    Resolution order: ``mock`` -> inline legacy ``ERDDAP_SOURCES`` (semicolon
    list, JSON array/object, ``@file``, or path) -> catalog file override ->
    packaged catalog. ``selector`` is ERDDAP_SELECT: comma names, ``*``, or
    unset for enabled-only.
    """
    effective_selector = selector or os.getenv("ERDDAP_SELECT", "")
    raw_value = value if value and value.strip() else os.getenv("ERDDAP_SOURCES")
    if mock:
        sources = _parse_pipe_entries(DEFAULT_SOURCES)
    elif raw_value and raw_value.strip():
        raw = _read_text_or_value(raw_value)
        if raw.lstrip().startswith("[") or raw.lstrip().startswith("{"):
            sources = _entries_to_sources(select_entries(_coerce_entries(json.loads(raw)), effective_selector))
        else:
            sources = _parse_pipe_entries(raw)
    else:
        path = sources_file.strip() if sources_file and sources_file.strip() else os.getenv("ERDDAP_SOURCES_FILE", "").strip() or DEFAULT_SOURCES_FILE
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as handle:
                entries = _coerce_entries(json.load(handle))
        else:
            entries = _coerce_entries(json.loads(_read_text_or_value(path)))
        sources = _entries_to_sources(select_entries(entries, effective_selector))
    if not sources:
        raise ValueError("No ERDDAP sources configured")
    return sources


def parse_kafka_connection_string(connection_string: str) -> Dict[str, str]:
    config: Dict[str, str] = {}
    for part in connection_string.split(";"):
        if "=" not in part:
            continue
        key, val = part.split("=", 1)
        val = val.strip('"')
        if key == "Endpoint":
            config["bootstrap.servers"] = val.replace("sb://", "").replace("/", "") + ":9093"
        elif key == "EntityPath":
            config["kafka_topic"] = val
        elif key == "SharedAccessKeyName":
            config["sasl.username"] = "$ConnectionString"
        elif key == "SharedAccessKey":
            config["sasl.password"] = connection_string.strip()
        elif key == "BootstrapServer":
            config["bootstrap.servers"] = val
    if "sasl.username" in config:
        config["security.protocol"] = "SASL_SSL"
        config["sasl.mechanism"] = "PLAIN"
    return config


def build_kafka_config(bootstrap_servers: str, sasl_username: Optional[str], sasl_password: Optional[str], tls_enabled: bool) -> Dict[str, str]:
    config = {"bootstrap.servers": bootstrap_servers, "client.id": "erddap"}
    if tls_enabled:
        config["security.protocol"] = "SASL_SSL" if sasl_username and sasl_password else "SSL"
    else:
        config["security.protocol"] = "SASL_PLAINTEXT" if sasl_username and sasl_password else "PLAINTEXT"
    if sasl_username and sasl_password:
        config["sasl.mechanism"] = "PLAIN"
        config["sasl.username"] = sasl_username
        config["sasl.password"] = sasl_password
    return config
