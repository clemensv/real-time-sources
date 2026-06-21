
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_SOURCES = "ioos-sensors|https://erddap.sensors.ioos.us/erddap|org_cormp_sun2|sea_water_temperature,sea_water_practical_salinity|station|time>=max(time)-1day"
TRUE_VALUES = {"1", "true", "yes", "on"}


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


def _read_text_or_value(value: str) -> str:
    text = value.strip()
    if text.startswith("@"):
        return Path(text[1:]).expanduser().read_text(encoding="utf-8")
    path = Path(text).expanduser()
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8")
    return text


def parse_sources(value: Optional[str]) -> List[ErddapSource]:
    raw = _read_text_or_value(value or os.getenv("ERDDAP_SOURCES") or DEFAULT_SOURCES)
    if raw.lstrip().startswith("["):
        entries = json.loads(raw)
        return [ErddapSource(
            erddap_id=str(e["erddap_id"]),
            base_url=str(e["base_url"]).rstrip("/"),
            dataset_id=str(e["dataset_id"]),
            variables=[str(v) for v in e.get("variables", [])],
            station_id_variable=e.get("station_id_variable"),
            time_constraint=str(e.get("time_constraint") or "time>=max(time)-1day"),
            auth_header=e.get("auth_header"),
        ) for e in entries]
    sources: List[ErddapSource] = []
    for item in raw.replace("\n", ";").split(";"):
        item = item.strip()
        if not item or item.startswith("#"):
            continue
        parts = [p.strip() for p in item.split("|")]
        if len(parts) < 4:
            raise ValueError("ERDDAP source entries must be erddap_id|base_url|dataset_id|variables[|station_id_variable|time_constraint]")
        sources.append(ErddapSource(parts[0], parts[1].rstrip("/"), parts[2], [v.strip() for v in parts[3].split(",") if v.strip()], parts[4] or None if len(parts) > 4 else None, parts[5] if len(parts) > 5 and parts[5] else "time>=max(time)-1day"))
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
