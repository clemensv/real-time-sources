"""Idempotent patch: add MQTT/UNS axes to aisstream.xreg.json.

Adds, without touching the existing Kafka contract:

* ``IO.AISstream.mqtt.jstruct`` schemagroup with three enriched schemas
  (``PositionReport``, ``ShipStatic``, ``AidToNavigation``) that include
  the five axis fields used by the UNS topic template:
  ``mmsi``, ``flag``, ``ship_type``, ``geohash5``, ``msg_type``.
* ``IO.AISstream.Mqtt`` endpoint.
* ``IO.AISstream.mqtt`` messagegroup with three messages, one per
  ``msg_type`` family. Each message bakes the kebab-case event tail as
  a literal in its ``topic_name`` template and defaults
  ``qos=0``/``retain=false`` (non-retained firehose).

Topic template:

    maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/{msg_type}

Per the xRegistry keying rules, every placeholder is a real top-level
field on the message's schema, and the subject template is identical to
the URI-template tail (``{mmsi}``).
"""
from __future__ import annotations

import json
import pathlib

XREG_PATH = pathlib.Path(__file__).resolve().parents[1] / "aisstream" / "xreg" / "aisstream.xreg.json"

AXIS_FIELDS = [
    (
        "mmsi",
        {
            "type": "string",
            "pattern": "^[0-9]{9}$",
            "description": (
                "Source MMSI (Maritime Mobile Service Identity) as a 9-digit ASCII string. "
                "Mirrors UserID from the upstream AIS payload, padded to 9 digits with leading "
                "zeros. Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject."
            ),
        },
    ),
    (
        "flag",
        {
            "type": "string",
            "pattern": "^[a-z]{2}$|^xx$",
            "description": (
                "ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits "
                "of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is "
                "used for MIDs that do not map to a country (e.g. inland-water identifiers, "
                "auxiliary craft, base stations) or for MMSIs shorter than 9 digits."
            ),
        },
    ),
    (
        "ship_type",
        {
            "type": "string",
            "description": (
                "Kebab-case ship-type bucket. For static reports this is derived directly from "
                "the AIS Type-5/24 ShipType field via the standard ITU-R M.1371 vocabulary "
                "(e.g. 'cargo', 'tanker', 'passenger', 'fishing', 'tug', 'pleasure-craft'). For "
                "position reports it is looked up from an in-process ship-type cache keyed by "
                "MMSI; if no static report has been observed for the MMSI yet, the value is "
                "'unknown'."
            ),
        },
    ),
    (
        "geohash5",
        {
            "type": "string",
            "pattern": "^[0-9b-hjkmnp-z]{5}$",
            "description": (
                "5-character geohash of the reported (Latitude, Longitude) using the standard "
                "base32 geohash alphabet. Approx. 4.9 km x 4.9 km cells at the equator. For "
                "messages without a position (Type 5/24/21 base reports) this is filled from "
                "the most recently observed position for the MMSI, falling back to '00000' if "
                "no position has been seen."
            ),
        },
    ),
    (
        "msg_type",
        {
            "type": "string",
            "enum": ["position-report", "static", "aid-to-navigation"],
            "description": (
                "Kebab-case event family used as the trailing UNS topic segment. Always equals "
                "the segment baked into the message's MQTT topic template."
            ),
        },
    ),
]

ENRICHED_SCHEMAS = {
    "IO.AISstream.mqtt.PositionReport": {
        "summary": "Position report (Type 1/2/3/4/9/18/19/27) projected onto the UNS axes.",
        "fields": {
            "user_id": ("int32", "Source AIS UserID (numeric MMSI, 9-digit)."),
            "latitude": ("double", "Reported latitude in WGS-84 decimal degrees."),
            "longitude": ("double", "Reported longitude in WGS-84 decimal degrees."),
            "sog": ("double", "Speed over ground in knots (0..102.2)."),
            "cog": ("double", "Course over ground in degrees (0..359.9)."),
            "true_heading": ("int32", "True heading in degrees (0..359, 511 = not available)."),
            "navigational_status": ("int32", "ITU navigation status code (0..15)."),
            "rate_of_turn": ("int32", "Rate of turn in AIS-encoded units."),
            "position_accuracy": ("boolean", "True if the reported position is high accuracy (DGPS)."),
            "timestamp": ("int32", "AIS report timestamp seconds-of-minute (0..59, 60..63 = special)."),
            "raim": ("boolean", "RAIM (Receiver Autonomous Integrity Monitoring) flag."),
            "message_id": ("int32", "Original ITU-R M.1371 message ID (1, 2, 3, 4, 9, 18, 19, or 27)."),
        },
        "required": [
            "mmsi", "flag", "ship_type", "geohash5", "msg_type",
            "user_id", "latitude", "longitude", "message_id",
        ],
    },
    "IO.AISstream.mqtt.ShipStatic": {
        "summary": "Static and voyage-related data (Type 5 ShipStaticData / Type 24 StaticDataReport).",
        "fields": {
            "user_id": ("int32", "Source AIS UserID (numeric MMSI, 9-digit)."),
            "name": ("string", "Vessel name as broadcast (max 20 chars, trimmed of AIS '@' padding)."),
            "call_sign": ("string", "Radio call sign as broadcast (max 7 chars)."),
            "imo_number": ("int32", "IMO number (7-digit). 0 if not assigned."),
            "ship_type_code": ("int32", "Raw ITU-R M.1371 ship type code (0..99)."),
            "destination": ("string", "Voyage destination string (max 20 chars). Empty for Type 24."),
            "eta": ("string", "Voyage ETA as ISO-8601 string, derived from AIS month/day/hour/minute. Empty if absent."),
            "draught": ("double", "Maximum present static draught in metres. 0.0 if not provided."),
            "dim_to_bow": ("int32", "Distance from reference point to bow in metres."),
            "dim_to_stern": ("int32", "Distance from reference point to stern in metres."),
            "dim_to_port": ("int32", "Distance from reference point to port side in metres."),
            "dim_to_starboard": ("int32", "Distance from reference point to starboard side in metres."),
            "message_id": ("int32", "Original ITU-R M.1371 message ID (5 or 24)."),
        },
        "required": [
            "mmsi", "flag", "ship_type", "geohash5", "msg_type",
            "user_id", "name", "ship_type_code", "message_id",
        ],
    },
    "IO.AISstream.mqtt.AidToNavigation": {
        "summary": "Aid-to-Navigation report (Type 21).",
        "fields": {
            "user_id": ("int32", "Source AIS UserID for the AtoN station (9-digit MMSI)."),
            "name": ("string", "AtoN name as broadcast."),
            "type": ("int32", "AtoN type code (0..31) per ITU-R M.1371."),
            "latitude": ("double", "Reported latitude in WGS-84 decimal degrees."),
            "longitude": ("double", "Reported longitude in WGS-84 decimal degrees."),
            "off_position": ("boolean", "True if the AtoN is reported off its assigned position."),
            "virtual_atoN": ("boolean", "True if this is a virtual AtoN broadcast by a base station."),
            "message_id": ("int32", "Original ITU-R M.1371 message ID (21)."),
        },
        "required": [
            "mmsi", "flag", "ship_type", "geohash5", "msg_type",
            "user_id", "name", "type", "latitude", "longitude", "message_id",
        ],
    },
}

TOPIC_TEMPLATE_BASE = "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}"

MESSAGES = [
    ("IO.AISstream.mqtt.PositionReport", "position-report", "IO.AISstream.mqtt.PositionReport"),
    ("IO.AISstream.mqtt.ShipStatic", "static", "IO.AISstream.mqtt.ShipStatic"),
    ("IO.AISstream.mqtt.AidToNavigation", "aid-to-navigation", "IO.AISstream.mqtt.AidToNavigation"),
]


def build_enriched_schema(name: str, defn: dict) -> dict:
    short = name.rsplit(".", 1)[-1]
    properties = {}
    for axis_name, axis_schema in AXIS_FIELDS:
        properties[axis_name] = axis_schema
    for fname, (ftype, fdesc) in defn["fields"].items():
        properties[fname] = {"type": ftype, "description": fdesc}
    return {
        "$schema": "https://json-structure.org/meta/extended/v0/#",
        "type": "object",
        "name": short,
        "description": defn["summary"],
        "required": defn["required"],
        "properties": properties,
        "$id": f"https://schemas.real-time-sources.dev/aisstream/mqtt/{short}",
    }


def build_message(name: str, event_tail: str, schema_full: str) -> dict:
    short_name = name.rsplit(".", 1)[-1]
    topic_name = f"{TOPIC_TEMPLATE_BASE}/{event_tail}"
    return {
        "messageid": f"{name}.mqtt",
        "name": short_name,
        "protocol": "MQTT/5.0",
        "envelope": "CloudEvents/1.0",
        "envelopemetadata": {
            "type": {"value": name},
            "source": {"value": "wss://stream.aisstream.io/v0/stream"},
            "subject": {"value": "{mmsi}", "type": "uritemplate"},
        },
        "protocoloptions": {
            "topic_name": topic_name,
            "qos": 0,
            "retain": False,
        },
        "dataschemaformat": "JsonStructure/draft-02",
        "dataschemauri": f"#/schemagroups/IO.AISstream.mqtt.jstruct/schemas/{schema_full}",
    }


def main() -> None:
    manifest = json.loads(XREG_PATH.read_text(encoding="utf-8"))

    # Schemagroup
    sg = manifest["schemagroups"].setdefault(
        "IO.AISstream.mqtt.jstruct",
        {"schemas": {}},
    )
    sg.setdefault("schemas", {})
    for full_name, defn in ENRICHED_SCHEMAS.items():
        schema = build_enriched_schema(full_name, defn)
        short = full_name.rsplit(".", 1)[-1]
        sg["schemas"][full_name] = {
            "name": short,
            "format": "JsonStructure/draft-02",
            "defaultversionid": "1",
            "versions": {
                "1": {
                    "format": "JsonStructure/draft-02",
                    "schema": schema,
                }
            },
        }

    # Endpoint
    manifest.setdefault("endpoints", {})
    manifest["endpoints"]["IO.AISstream.Mqtt"] = {
        "usage": ["producer"],
        "protocol": "MQTT/5.0",
        "envelope": "CloudEvents/1.0",
        "envelopeoptions": {"mode": "binary"},
        "protocoloptions": {
            "deployed": False,
            "options": {
                "topic": TOPIC_TEMPLATE_BASE + "/{msg_type}",
                "qos": 0,
                "retain": False,
            },
        },
        "messagegroups": ["#/messagegroups/IO.AISstream.mqtt"],
    }

    # Messagegroup
    mg = {
        "envelope": "CloudEvents/1.0",
        "messages": {},
    }
    for name, tail, schema in MESSAGES:
        mg["messages"][name] = build_message(name, tail, schema)
    manifest["messagegroups"]["IO.AISstream.mqtt"] = mg

    XREG_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"patched {XREG_PATH}")


if __name__ == "__main__":
    main()
