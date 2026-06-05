from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ConfiguredFeed:
    autodiscovery_url: str
    system_id_override: Optional[str] = None


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


def _read_feed_lines(path: Path) -> List[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#")]


def _parse_feed_value(value: Optional[str]) -> List[str]:
    if not value:
        return []
    text = value.strip()
    if not text:
        return []
    if text.startswith("@"):
        return _read_feed_lines(Path(text[1:]).expanduser())
    possible_path = Path(text).expanduser()
    if possible_path.exists() and possible_path.is_file():
        return _read_feed_lines(possible_path)
    return [item.strip() for item in text.split(",") if item.strip()]


def parse_feed_configuration(gbfs_feeds: Optional[str], gbfs_system_ids: Optional[str] = None) -> List[ConfiguredFeed]:
    feeds = _parse_feed_value(gbfs_feeds)
    if not feeds:
        raise ValueError("At least one GBFS auto-discovery URL must be provided via --gbfs-feeds or GBFS_FEEDS.")
    overrides = _parse_feed_value(gbfs_system_ids)
    if overrides and len(overrides) != len(feeds):
        raise ValueError("GBFS_SYSTEM_IDS must provide the same number of entries as GBFS_FEEDS when specified.")
    configured: List[ConfiguredFeed] = []
    for index, feed in enumerate(feeds):
        configured.append(ConfiguredFeed(feed, overrides[index] if index < len(overrides) else None))
    return configured


def parse_kafka_connection_string(connection_string: str) -> Dict[str, str]:
    config_dict: Dict[str, str] = {}
    try:
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
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


def build_kafka_config(bootstrap_servers: str, sasl_username: Optional[str] = None, sasl_password: Optional[str] = None, tls_enabled: bool = True) -> Dict[str, str]:
    config = {
        "bootstrap.servers": bootstrap_servers,
        "client.id": "gbfs-bikeshare",
    }
    if tls_enabled:
        config["security.protocol"] = "SASL_SSL" if sasl_username and sasl_password else "SSL"
        if not sasl_username or not sasl_password:
            config.setdefault("ssl.endpoint.identification.algorithm", "https")
    else:
        config["security.protocol"] = "SASL_PLAINTEXT" if sasl_username and sasl_password else "PLAINTEXT"
    if sasl_username and sasl_password:
        config["sasl.mechanism"] = "PLAIN"
        config["sasl.username"] = sasl_username
        config["sasl.password"] = sasl_password
    return config
