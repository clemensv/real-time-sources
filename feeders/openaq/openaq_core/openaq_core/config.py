from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

TRUE_VALUES = {"1", "true", "yes", "on"}
FALSE_VALUES = {"0", "false", "no", "off"}


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
