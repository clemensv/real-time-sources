from __future__ import annotations

from typing import Iterable

NODE_CATALOG: dict[str, dict[str, str | None]] = {
    "emsc": {
        "node_id": "emsc",
        "name": "European-Mediterranean Seismological Centre (EMSC)",
        "base_url": "https://seismicportal.eu/fdsnws/event/1/",
        "coverage": "Global aggregator",
        "country": "FR",
    },
    "gfz": {
        "node_id": "gfz",
        "name": "GFZ German Research Centre for Geosciences (GEOFON)",
        "base_url": "https://geofon.gfz-potsdam.de/fdsnws/event/1/",
        "coverage": "Global M4+",
        "country": "DE",
    },
    "ingv": {
        "node_id": "ingv",
        "name": "Istituto Nazionale di Geofisica e Vulcanologia (INGV)",
        "base_url": "https://webservices.ingv.it/fdsnws/event/1/",
        "coverage": "Italy + Mediterranean",
        "country": "IT",
    },
    "ethz": {
        "node_id": "ethz",
        "name": "Swiss Seismological Service at ETH Zurich (SED)",
        "base_url": "https://eida.ethz.ch/fdsnws/event/1/",
        "coverage": "Switzerland + Alpine",
        "country": "CH",
    },
    "resif": {
        "node_id": "resif",
        "name": "Réseau Sismologique et géodésique Français (RESIF)",
        "base_url": "https://ws.resif.fr/fdsnws/event/1/",
        "coverage": "France + global M5+",
        "country": "FR",
    },
    "ipgp": {
        "node_id": "ipgp",
        "name": "Institut de Physique du Globe de Paris (IPGP)",
        "base_url": "https://ws.ipgp.fr/fdsnws/event/1/",
        "coverage": "Mayotte volcanic swarm",
        "country": "FR",
    },
    "niep": {
        "node_id": "niep",
        "name": "National Institute for Earth Physics (NIEP)",
        "base_url": "https://eida-sc3.infp.ro/fdsnws/event/1/",
        "coverage": "Romania + Vrancea",
        "country": "RO",
    },
    "usgs": {
        "node_id": "usgs",
        "name": "U.S. Geological Survey Earthquake Hazards Program (USGS)",
        "base_url": "https://earthquake.usgs.gov/fdsnws/event/1/",
        "coverage": "Global earthquake catalog",
        "country": "US",
    },
}


def parse_node_filter(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [token.strip().lower() for token in raw.split(",") if token.strip()]



def get_active_nodes(
    include_ids: Iterable[str] | None = None,
    exclude_ids: Iterable[str] | None = None,
) -> dict[str, dict[str, str | None]]:
    include = [item.strip().lower() for item in (include_ids or []) if item and item.strip()]
    exclude = {item.strip().lower() for item in (exclude_ids or []) if item and item.strip()}

    unknown = (set(include) | exclude) - set(NODE_CATALOG)
    if unknown:
        raise ValueError(f"Unknown node id(s): {', '.join(sorted(unknown))}")

    selected_ids = include or list(NODE_CATALOG)
    return {
        node_id: NODE_CATALOG[node_id]
        for node_id in selected_ids
        if node_id not in exclude
    }
