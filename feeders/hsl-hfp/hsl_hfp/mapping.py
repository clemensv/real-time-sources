"""Normalize raw HFP payloads and GTFS rows into producer-data-class kwargs.

This module is the single place that enumerates every field of every event
schema. It returns plain ``dict`` kwargs keyed by the *Python* field name of the
generated data classes (e.g. ``dr_type``, ``tlp_requestid``,
``signal_groupid``), so each transport app can construct its own producer data
class with ``VehicleEvent(**vehicle_event_kwargs(payload, params))`` without
importing anything from this module's perspective.

Two deliberate design points:

* **Raw values, not enum instances.** Enum-typed fields (``dir``, ``loc``,
  ``tlp-*``, ``location_type`` ...) are passed through verbatim as their raw
  JSON scalar. dataclasses-json serializes a raw scalar held in an enum-typed
  field to exactly the same wire token as the corresponding enum member's
  ``.value`` (verified: the wire output is byte-identical), so keeping the raw
  value preserves the upstream payload verbatim while avoiding a per-transport
  enum-conversion fork (the three producer packages each define their own,
  structurally identical, enum classes).
* **Every field is present.** The generated data classes declare every field
  keyword-only with no default, so ``cls(**kwargs)`` requires every key. Absent
  optional HFP fields are therefore emitted as explicit ``None`` (which
  serializes to JSON ``null``) -- the one structural difference from a
  byte-exact echo, giving downstream consumers a stable typed schema.

``payload`` is the unwrapped inner HFP object (already stripped of the
single-key ``{"VP": ...}`` wrapper); ``params`` is the parsed topic-level dict
from :func:`hsl_hfp_core.hfp_source.parse_topic`.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

# Topic-identity schema fields, populated from the parsed HFP topic levels (see
# :func:`hsl_hfp.hfp_source.parse_topic`). They are real fields on every
# telemetry schema so the CloudEvents subject / Kafka key
# ``{operator_id}/{vehicle_number}`` and the downstream MQTT-topic / AMQP
# application-property routing all resolve from data that is visible on the
# event itself rather than from out-of-band topic state. ``operator_id`` /
# ``vehicle_number`` / ``temporal_type`` / ``transport_mode`` are required and
# always present on a journey topic; the remaining levels are nullable (they are
# empty on the driver/block ``da``/``dout``/``ba``/``bout`` topics). Values are
# passed through verbatim from the topic -- no normalization -- honoring the
# keep-the-topic-structure directive.
_TOPIC_IDENTITY_FIELDS = (
    "operator_id",
    "vehicle_number",
    "temporal_type",
    "transport_mode",
    "route_id",
    "direction_id",
    "headsign",
    "start_time",
    "next_stop",
    "geohash_level",
    "geohash",
)


def _topic_identity(params: Dict[str, str]) -> Dict[str, Any]:
    """Extract the topic-identity schema fields from the parsed topic ``params``."""
    return {name: params.get(name) for name in _TOPIC_IDENTITY_FIELDS}


def vehicle_event_kwargs(payload: Dict[str, Any], params: Dict[str, str]) -> Dict[str, Any]:
    """Map an HFP vehicle/stop/door/sign payload to ``VehicleEvent`` kwargs."""
    g = payload.get
    return {
        **_topic_identity(params),
        "oper": g("oper"),
        "veh": g("veh"),
        "tst": g("tst"),
        "tsi": g("tsi"),
        "desi": g("desi"),
        "dir": g("dir"),
        "dl": g("dl"),
        "oday": g("oday"),
        "jrn": g("jrn"),
        "line": g("line"),
        "start": g("start"),
        "stop": g("stop"),
        "route": g("route"),
        "occu": g("occu"),
        "seq": g("seq"),
        "label": g("label"),
        "spd": g("spd"),
        "hdg": g("hdg"),
        "lat": g("lat"),
        "long": g("long"),
        "acc": g("acc"),
        "odo": g("odo"),
        "drst": g("drst"),
        "loc": g("loc"),
        "ttarr": g("ttarr"),
        "ttdep": g("ttdep"),
        "dr_type": g("dr-type"),
    }


def traffic_light_event_kwargs(payload: Dict[str, Any], params: Dict[str, str]) -> Dict[str, Any]:
    """Map an HFP ``tlr``/``tla`` payload to ``TrafficLightEvent`` kwargs.

    ``sid`` (junction id) is taken from the payload; if the upstream omits it
    from the payload but encodes it as the trailing topic level, the parsed
    topic value is used as a fallback.
    """
    g = payload.get
    sid: Optional[Any] = g("sid")
    if sid is None and params.get("sid"):
        try:
            sid = int(params["sid"])
        except (TypeError, ValueError):
            sid = None
    return {
        **_topic_identity(params),
        "oper": g("oper"),
        "veh": g("veh"),
        "tst": g("tst"),
        "tsi": g("tsi"),
        "desi": g("desi"),
        "dir": g("dir"),
        "dl": g("dl"),
        "oday": g("oday"),
        "jrn": g("jrn"),
        "line": g("line"),
        "start": g("start"),
        "stop": g("stop"),
        "route": g("route"),
        "occu": g("occu"),
        "spd": g("spd"),
        "hdg": g("hdg"),
        "lat": g("lat"),
        "long": g("long"),
        "acc": g("acc"),
        "odo": g("odo"),
        "drst": g("drst"),
        "loc": g("loc"),
        "tlp_requestid": g("tlp-requestid"),
        "tlp_requesttype": g("tlp-requesttype"),
        "tlp_prioritylevel": g("tlp-prioritylevel"),
        "tlp_reason": g("tlp-reason"),
        "tlp_att_seq": g("tlp-att-seq"),
        "tlp_decision": g("tlp-decision"),
        "sid": sid,
        "signal_groupid": g("signal-groupid"),
        "tlp_signalgroupnbr": g("tlp-signalgroupnbr"),
        "tlp_line_configid": g("tlp-line-configid"),
        "tlp_point_configid": g("tlp-point-configid"),
        "tlp_frequency": g("tlp-frequency"),
        "tlp_protocol": g("tlp-protocol"),
    }


def driver_block_event_kwargs(payload: Dict[str, Any], params: Dict[str, str]) -> Dict[str, Any]:
    """Map an HFP ``da``/``dout``/``ba``/``bout`` payload to ``DriverBlockEvent`` kwargs."""
    g = payload.get
    return {
        **_topic_identity(params),
        "oper": g("oper"),
        "veh": g("veh"),
        "tst": g("tst"),
        "tsi": g("tsi"),
        "spd": g("spd"),
        "hdg": g("hdg"),
        "lat": g("lat"),
        "long": g("long"),
        "acc": g("acc"),
        "odo": g("odo"),
        "drst": g("drst"),
        "loc": g("loc"),
        "oday": g("oday"),
        "dr_type": g("dr-type"),
    }


# event_type -> (schema selector). Drives the per-event dispatch in the apps.
VEHICLE_EVENTS = frozenset(
    {"vp", "due", "arr", "dep", "ars", "pde", "pas", "wait", "doo", "doc", "vja", "vjout"}
)
TRAFFIC_LIGHT_EVENTS = frozenset({"tlr", "tla"})
DRIVER_BLOCK_EVENTS = frozenset({"da", "dout", "ba", "bout"})


def operator_kwargs(operator_id: str, operator_number: int, name: str,
                    note: Optional[str]) -> Dict[str, Any]:
    """Map an operator-catalogue entry to ``Operator`` kwargs."""
    return {
        "operator_id": operator_id,
        "operator_number": operator_number,
        "name": name,
        "note": note,
    }


def route_kwargs(row: Dict[str, Any]) -> Dict[str, Any]:
    """Map a GTFS ``routes.txt`` row to ``Route`` kwargs."""
    g = row.get
    return {
        "route_id": g("route_id"),
        "agency_id": g("agency_id"),
        "route_short_name": g("route_short_name"),
        "route_long_name": g("route_long_name"),
        "route_desc": g("route_desc"),
        "route_type": g("route_type"),
        "route_url": g("route_url"),
    }


def stop_kwargs(row: Dict[str, Any]) -> Dict[str, Any]:
    """Map a GTFS ``stops.txt`` row to ``Stop`` kwargs."""
    g = row.get
    return {
        "stop_id": g("stop_id"),
        "stop_code": g("stop_code"),
        "stop_name": g("stop_name"),
        "stop_desc": g("stop_desc"),
        "stop_lat": g("stop_lat"),
        "stop_lon": g("stop_lon"),
        "zone_id": g("zone_id"),
        "stop_url": g("stop_url"),
        "location_type": g("location_type"),
        "parent_station": g("parent_station"),
        "platform_code": g("platform_code"),
        "wheelchair_boarding": g("wheelchair_boarding"),
        "vehicle_type": g("vehicle_type"),
        "digistop_id": g("digistop_id"),
    }
