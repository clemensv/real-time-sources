from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Set, Tuple
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


@dataclass(frozen=True)
class ConfiguredFeed:
    autodiscovery_url: str
    system_id_override: Optional[str] = None


TRUE_VALUES = {"1", "true", "yes", "on"}
FALSE_VALUES = {"0", "false", "no", "off"}
DEFAULT_API_KEY_PARAM = "acl:consumerKey"
_ENV_TEMPLATE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\{([A-Za-z_][A-Za-z0-9_]*)\}")


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


def _expand_url_template(url: str, variables: Mapping[str, str]) -> Tuple[str, Set[str]]:
    used: Set[str] = set()

    def replace(match: re.Match[str]) -> str:
        name = match.group(1) or match.group(2)
        if name not in variables or variables[name] is None:
            raise ValueError(f"GBFS feed URL template references unset environment variable {name}.")
        used.add(name)
        return str(variables[name])

    return _ENV_TEMPLATE.sub(replace, url), used


def _aligned_values(value: Optional[str], count: int, field_name: str) -> List[Optional[str]]:
    values = _parse_feed_value(value)
    if not values:
        return [None] * count
    if len(values) == 1:
        return values * count
    if len(values) != count:
        raise ValueError(f"{field_name} must provide either one value or the same number of entries as GBFS_FEEDS.")
    return values


def _append_api_key(url: str, api_key: Optional[str], api_key_param: Optional[str]) -> str:
    key = (api_key or "").strip()
    param = (api_key_param or DEFAULT_API_KEY_PARAM).strip()
    if not key or not param:
        return url
    parsed = urlsplit(url)
    query_pairs = parse_qsl(parsed.query, keep_blank_values=True)
    if any(name == param for name, _ in query_pairs):
        return url
    query_pairs.append((param, key))
    query = urlencode(query_pairs, doseq=True, safe=":")
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, query, parsed.fragment))


def parse_feed_configuration(
    gbfs_feeds: Optional[str],
    gbfs_system_ids: Optional[str] = None,
    gbfs_api_key: Optional[str] = None,
    gbfs_api_key_param: Optional[str] = DEFAULT_API_KEY_PARAM,
) -> List[ConfiguredFeed]:
    feeds = _parse_feed_value(gbfs_feeds)
    if not feeds:
        raise ValueError("At least one GBFS auto-discovery URL must be provided via --gbfs-feeds or GBFS_FEEDS.")
    overrides = _parse_feed_value(gbfs_system_ids)
    if overrides and len(overrides) != len(feeds):
        raise ValueError("GBFS_SYSTEM_IDS must provide the same number of entries as GBFS_FEEDS when specified.")
    api_keys = _aligned_values(gbfs_api_key, len(feeds), "GBFS_API_KEY")
    api_key_params = _aligned_values(gbfs_api_key_param, len(feeds), "GBFS_API_KEY_PARAM")
    configured: List[ConfiguredFeed] = []
    for index, feed in enumerate(feeds):
        api_key = api_keys[index]
        template_variables = dict(os.environ)
        if api_key:
            template_variables["GBFS_API_KEY"] = api_key
        template_variables["GBFS_FEED_INDEX"] = str(index)
        templated_feed, template_variables_used = _expand_url_template(feed, template_variables)
        append_key = api_key if "GBFS_API_KEY" not in template_variables_used else None
        configured.append(ConfiguredFeed(_append_api_key(templated_feed, append_key, api_key_params[index]), overrides[index] if index < len(overrides) else None))
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
