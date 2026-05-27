"""Parser for DWD CAP (Common Alerting Protocol) weather alerts."""

import logging
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# CAP XML namespace
CAP_NS = {"cap": "urn:oasis:names:tc:emergency:cap:1.2"}


def parse_cap_xml(xml_text: str) -> List[Dict[str, Any]]:
    """Parse a CAP XML document into a list of alert dicts.

    One CAP <alert> may contain multiple <info> elements (language variants).
    We emit one dict per <info> element with the alert-level fields merged in.
    """
    alerts: List[Dict[str, Any]] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        logger.warning("Failed to parse CAP XML: %s", e)
        return []

    # Handle both namespaced and non-namespaced CAP
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"

    identifier = _text(root, f"{ns}identifier")
    sender = _text(root, f"{ns}sender")
    sent = _text(root, f"{ns}sent")
    status = _text(root, f"{ns}status")
    msg_type = _text(root, f"{ns}msgType")

    for info in root.findall(f"{ns}info"):
        alert: Dict[str, Any] = {
            "identifier": identifier,
            "sender": sender,
            "sent": sent,
            "status": status,
            "msg_type": msg_type,
            "severity": _text(info, f"{ns}severity"),
            "urgency": _text(info, f"{ns}urgency"),
            "certainty": _text(info, f"{ns}certainty"),
            "event": _text(info, f"{ns}event"),
            "headline": _text(info, f"{ns}headline"),
            "description": _text(info, f"{ns}description"),
            "effective": _text(info, f"{ns}effective"),
            "onset": _text(info, f"{ns}onset"),
            "expires": _text(info, f"{ns}expires"),
        }

        # Collect area descriptions and geocodes
        areas: List[str] = []
        geocodes: Dict[str, str] = {}
        for area in info.findall(f"{ns}area"):
            area_desc = _text(area, f"{ns}areaDesc")
            if area_desc:
                areas.append(area_desc)
            for gc in area.findall(f"{ns}geocode"):
                name = _text(gc, f"{ns}valueName")
                value = _text(gc, f"{ns}value")
                if name and value:
                    geocodes[name] = value

        alert["area_desc"] = "; ".join(areas) if areas else ""
        # Store geocodes as JSON string for the flat schema
        import json
        alert["geocodes"] = json.dumps(geocodes) if geocodes else "{}"

        alerts.append(alert)

    return alerts


def _text(element: ET.Element, tag: str) -> str:
    """Get text content of a child element, empty string if missing."""
    child = element.find(tag)
    return (child.text or "").strip() if child is not None else ""
