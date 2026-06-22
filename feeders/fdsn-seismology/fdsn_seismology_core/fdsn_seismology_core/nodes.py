from __future__ import annotations

import json
import os
import re
from typing import Any, Iterable


FALLBACK_NODE_CATALOG: dict[str, dict[str, Any]] = {
    "emsc": {
        "name": "European-Mediterranean Seismological Centre (EMSC)",
        "enabled": True,
        "description": "European-Mediterranean Seismological Centre global aggregator FDSN Event service.",
        "node_id": "emsc",
        "base_url": "https://seismicportal.eu/fdsnws/event/1/",
        "coverage": "Global aggregator",
        "country": "FR",
    },
    "gfz": {
        "name": "GFZ German Research Centre for Geosciences (GEOFON)",
        "enabled": True,
        "description": "GFZ GEOFON global M4+ FDSN Event service.",
        "node_id": "gfz",
        "base_url": "https://geofon.gfz-potsdam.de/fdsnws/event/1/",
        "coverage": "Global M4+",
        "country": "DE",
    },
    "ingv": {
        "name": "Istituto Nazionale di Geofisica e Vulcanologia (INGV)",
        "enabled": True,
        "description": "INGV Italy and Mediterranean FDSN Event service.",
        "node_id": "ingv",
        "base_url": "https://webservices.ingv.it/fdsnws/event/1/",
        "coverage": "Italy + Mediterranean",
        "country": "IT",
    },
    "ethz": {
        "name": "Swiss Seismological Service at ETH Zurich (SED)",
        "enabled": True,
        "description": "ETH Zurich Swiss Seismological Service FDSN Event service for Switzerland and the Alpine region.",
        "node_id": "ethz",
        "base_url": "https://eida.ethz.ch/fdsnws/event/1/",
        "coverage": "Switzerland + Alpine",
        "country": "CH",
    },
    "resif": {
        "name": "Réseau Sismologique et géodésique Français (RESIF)",
        "enabled": True,
        "description": "RESIF French and global M5+ FDSN Event service.",
        "node_id": "resif",
        "base_url": "https://ws.resif.fr/fdsnws/event/1/",
        "coverage": "France + global M5+",
        "country": "FR",
    },
    "ipgp": {
        "name": "Institut de Physique du Globe de Paris (IPGP)",
        "enabled": True,
        "description": "IPGP Mayotte volcanic swarm FDSN Event service.",
        "node_id": "ipgp",
        "base_url": "https://ws.ipgp.fr/fdsnws/event/1/",
        "coverage": "Mayotte volcanic swarm",
        "country": "FR",
    },
    "niep": {
        "name": "National Institute for Earth Physics (NIEP)",
        "enabled": True,
        "description": "NIEP Romania and Vrancea FDSN Event service.",
        "node_id": "niep",
        "base_url": "https://eida-sc3.infp.ro/fdsnws/event/1/",
        "coverage": "Romania + Vrancea",
        "country": "RO",
    },
    "usgs": {
        "name": "U.S. Geological Survey Earthquake Hazards Program (USGS)",
        "enabled": True,
        "description": "USGS Earthquake Hazards Program global earthquake catalog FDSN Event service.",
        "node_id": "usgs",
        "base_url": "https://earthquake.usgs.gov/fdsnws/event/1/",
        "coverage": "Global earthquake catalog",
        "country": "US",
    },
}

DEFAULT_SOURCES_FILE = os.path.join(os.path.dirname(__file__), "sources", "fdsn-seismology.sources.json")
_ENV_REF = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


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


def _entries_to_catalog(entries: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    catalog: dict[str, dict[str, Any]] = {}
    for raw_entry in entries:
        entry = _interpolate_env(raw_entry)
        node_id = str(entry.get("node_id") or entry.get("name") or "").strip().lower()
        if not node_id:
            continue
        normalized = dict(entry)
        normalized["node_id"] = node_id
        selector_name = str(entry.get("name") or node_id).strip() or node_id
        normalized["selector_name"] = selector_name
        normalized["name"] = str(entry.get("display_name") or (entry.get("name") if selector_name != node_id else "") or node_id).strip() or node_id
        normalized["base_url"] = str(entry.get("base_url") or entry.get("url") or "").strip()
        normalized["coverage"] = str(entry.get("coverage") or "").strip()
        normalized["country"] = str(entry.get("country") or "").strip() or None
        normalized["enabled"] = entry.get("enabled", True)
        catalog[node_id] = normalized
    return catalog


def load_node_catalog(sources_file: str = "") -> dict[str, dict[str, Any]]:
    """Load the FDSN node catalog from a packaged or operator-provided file."""
    path = sources_file.strip() if sources_file and sources_file.strip() else DEFAULT_SOURCES_FILE
    text = _read_config_text(path)
    catalog = _entries_to_catalog(_coerce_entries(json.loads(text)))
    return catalog or {node_id: dict(node) for node_id, node in FALLBACK_NODE_CATALOG.items()}


try:
    NODE_CATALOG = load_node_catalog()
except Exception:
    NODE_CATALOG = {node_id: dict(node) for node_id, node in FALLBACK_NODE_CATALOG.items()}


def parse_node_filter(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [token.strip().lower() for token in raw.split(",") if token.strip()]


def get_active_nodes(
    include_ids: Iterable[str] | None = None,
    exclude_ids: Iterable[str] | None = None,
    sources_file: str = "",
) -> dict[str, dict[str, Any]]:
    catalog = load_node_catalog(sources_file) if sources_file and sources_file.strip() else NODE_CATALOG
    include = [item.strip().lower() for item in (include_ids or []) if item and item.strip()]
    exclude = {item.strip().lower() for item in (exclude_ids or []) if item and item.strip()}

    unknown = (set(include) | exclude) - set(catalog)
    if unknown:
        known = ", ".join(sorted(catalog)) or "(none)"
        raise ValueError(f"Unknown node id(s): {', '.join(sorted(unknown))}. Known node ids: {known}")

    selected_ids = include or [node_id for node_id, node in catalog.items() if node.get("enabled", True)]
    return {
        node_id: catalog[node_id]
        for node_id in selected_ids
        if node_id not in exclude
    }
