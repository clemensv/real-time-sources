"""Idempotently (re)wire a Fabric Map item with Kusto-backed vector layers
for a freshly-deployed hsl-hfp (Helsinki HSL High-Frequency Positioning)
source.

A fresh ``hsl-hfp/kql/hsl-hfp.kql`` deployment lays down the following schema
in the target Eventhouse (KQL database ``hsl_hfp``):

  * Bracketed, dotted CloudEvents-shaped base tables:
    ``['fi.hsl.hfp.VehicleEvent']``      - the ~1 Hz vehicle telemetry
                                           (``vp`` GPS heartbeat + stop / door
                                           / sign events all share this table),
    ``['fi.hsl.hfp.TrafficLightEvent']`` - transit-signal-priority ``tlr``/``tla``,
    ``['fi.hsl.hfp.DriverBlockEvent']``  - driver / block sign-in / sign-out,
    ``['fi.hsl.gtfs.Stop']``, ``['fi.hsl.gtfs.Route']``,
    ``['fi.hsl.gtfs.Operator']``         - GTFS reference lookups.
  * Per-table ``<X>Latest`` materialized views that pre-aggregate
    ``arg_max(___time, *) by ___type, ___source, ___subject`` so callers get
    the latest snapshot per logical entity without scanning history.

This script wires the following layers (all parametric, no hand-wiring):

  1.  Live vehicles - bubbles (z8-16, coloured by transport_mode)
  2.  Live vehicles (detail) - heading-oriented rectangles (z16+)
  3.  Transit stops - stratified to fit Fabric's 100k feature cap (z12+)
  4.  Vehicle punctuality - delay-banded bubbles (off by default)
  5.  Vehicle density grid - per-cell live vehicle count (off by default)
  6.  Traffic-signal priority - tlr/tla request/grant points (off by default)

The map's basemap centre + zoom are auto-discovered from the bounding box of
``['fi.hsl.gtfs.StopLatest']`` (falling back to live vehicle positions, and
finally to the Helsinki city centre) so the script needs no manual tuning.

The Fabric Map item must already exist (see ``post-deploy.ps1`` which
auto-creates it). This script is idempotent: re-running drops the layers it
manages (matched by their KQL source's ``itemId`` binding) and recreates them,
so colour ramps, query changes and viewport tweaks land cleanly.

Inputs (env vars or CLI args, mirroring ``gtfs/fabric/wire_gtfs_map.py``):

  FABRIC_WORKSPACE_ID   - GUID of the Fabric workspace containing the Map
  FABRIC_MAP_ID         - GUID of the Fabric Map item to patch
  FABRIC_KQL_DB_ID      - GUID of the KQL database with the hsl-hfp tables
  KUSTO_CLUSTER_URI     - https://<cluster>.kusto.fabric.microsoft.com
  KUSTO_DB              - KQL database name (default ``hsl_hfp``)
  FABRIC_TOKEN          - bearer token for the Fabric REST API
  KUSTO_TOKEN           - bearer token for the Kusto cluster
  FABRIC_API_BASE       - override (default https://api.fabric.microsoft.com/v1)
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import uuid
from dataclasses import dataclass
from typing import Any, Optional

import requests


# ---------------------------------------------------------------------------
# Token + HTTP helpers (factored to match the gtfs/pegelonline hook style).
# ---------------------------------------------------------------------------

def _get_token(env_name: str, scope: str) -> str:
    tok = os.environ.get(env_name)
    if tok:
        return tok.strip()
    try:
        from azure.identity import DefaultAzureCredential
    except ImportError as exc:
        raise SystemExit(
            f"{env_name} not set and azure-identity not installed; "
            f"either set {env_name} or `pip install azure-identity`."
        ) from exc
    return DefaultAzureCredential().get_token(scope).token


def _session(token: str) -> requests.Session:
    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {token}"
    s.headers["Content-Type"] = "application/json"
    return s


def _poll_lro(session: requests.Session, response: requests.Response) -> Any:
    if response.status_code != 202:
        response.raise_for_status()
        return response.json() if response.content else None
    op_url = response.headers["Location"]
    while True:
        status = session.get(op_url).json()
        s = status.get("status")
        if s == "Succeeded":
            r = session.get(op_url + "/result")
            return r.json() if r.content else None
        if s == "Failed":
            raise RuntimeError(f"Fabric LRO failed: {json.dumps(status)[:600]}")
        time.sleep(2)


def _kql_mgmt(ks: requests.Session, kusto_uri: str, db: str, csl: str) -> dict[str, Any]:
    r = ks.post(f"{kusto_uri.rstrip('/')}/v1/rest/mgmt", json={"db": db, "csl": csl})
    if r.status_code >= 400:
        raise RuntimeError(f"KQL mgmt failed ({db}): HTTP {r.status_code} {r.text[:800]}")
    return r.json()


def _kql_query(ks: requests.Session, kusto_uri: str, db: str, csl: str) -> Optional[dict[str, Any]]:
    r = ks.post(f"{kusto_uri.rstrip('/')}/v2/rest/query", json={"db": db, "csl": csl})
    if r.status_code >= 400:
        raise RuntimeError(f"KQL query failed ({db}): HTTP {r.status_code} {r.text[:800]}")
    for frame in r.json():
        if (frame.get("FrameType") == "DataTable"
                and frame.get("TableKind") == "PrimaryResult"):
            return frame
    return None

# ---------------------------------------------------------------------------
# KQL helper functions installed in the target database.
#
# We lean on the materialized views (``['fi.hsl.hfp.VehicleEventLatest']``,
# ``['fi.hsl.gtfs.StopLatest']``, ``['fi.hsl.gtfs.RouteLatest']``,
# ``['fi.hsl.hfp.TrafficLightEventLatest']``) created by ``hsl-hfp.kql``. Each
# MV reduces a CloudEvents-shaped table to one row per (___type, ___source,
# ___subject) - i.e. one row per logical entity per source. Reading the MV
# directly is constant-time regardless of how long the source has ingested.
#
# The live-vehicle layers filter the shared VehicleEvent table down to the
# ``vp`` GPS heartbeat (``___type in ('fi.hsl.hfp.vp','fi.hsl.hfp.upstream.vp')``),
# drop null / 0,0 coordinates and stale rows, and dedupe to the latest row per
# vehicle (``arg_max(___time, *) by ___subject``).
#
# NOTE on ``dl`` (delay) sign convention: per the HSL HFP spec and the
# hsl-hfp.kql column docstring, a POSITIVE ``dl`` means the vehicle is running
# AHEAD of schedule (early) and a NEGATIVE ``dl`` means it is BEHIND (late).
# ---------------------------------------------------------------------------

HSL_HFP_FUNCTIONS: list[str] = [
    # ------------------------------------------------------------------
    # Reference stops: every located HSL stop / station / entrance. Null and
    # 0,0 coordinates are dropped up front.
    r'''
.create-or-alter function with (folder = "Map", skipvalidation = "true") hslhfp_stops() {
    ['fi.hsl.gtfs.StopLatest']
    | where isnotnull(stop_lat) and isnotnull(stop_lon)
    | where stop_lat != 0.0 and stop_lon != 0.0
    | project stop_id, stop_code, stop_name, stop_lat, stop_lon,
              location_type, parent_station, platform_code, vehicle_type
}
''',
    # ------------------------------------------------------------------
    # Map bounding box: queried once at deploy time so the basemap centre and
    # zoom auto-fit the source footprint. 1 % / 99 % quantiles guard against a
    # single mislocated stop dragging the box across the country.
    r'''
.create-or-alter function with (folder = "Map", skipvalidation = "true") hslhfp_bbox() {
    hslhfp_stops()
    | summarize lat_p01 = percentile(stop_lat, 1), lat_p99 = percentile(stop_lat, 99),
                lon_p01 = percentile(stop_lon, 1), lon_p99 = percentile(stop_lon, 99),
                cnt = count()
}
''',
    # ------------------------------------------------------------------
    # Live vehicle points: the most recent ``vp`` GPS heartbeat per vehicle
    # (``___subject`` = operator_id/vehicle_number) within the lookback window,
    # joined to its static route metadata for nicer labels. Colour + legend are
    # driven by ``transport_mode`` (HSL-flavoured palette). ``dl`` keeps the HFP
    # sign convention (positive = early / ahead, negative = late / behind).
    r'''
.create-or-alter function with (folder = "Map", skipvalidation = "true") hslhfp_vehicle_points(lookback:timespan) {
    let routes = ['fi.hsl.gtfs.RouteLatest']
        | project route_id, route_short_name, route_long_name, route_type;
    ['fi.hsl.hfp.VehicleEventLatest']
    | where ___type in ('fi.hsl.hfp.vp', 'fi.hsl.hfp.upstream.vp')
    | where ___time > ago(lookback)
    | where isnotnull(lat) and isnotnull(['long']) and lat != 0.0 and ['long'] != 0.0
    | summarize arg_max(___time, *) by ___subject
    | extend route_id = iff(isempty(route_id), route, route_id)
    | lookup kind=leftouter routes on route_id
    | extend age_min = datetime_diff('minute', now(), ___time)
    | extend freshness = case(age_min <= 1, "live", age_min <= 2, "fresh",
                              age_min <= 5, "recent", "stale")
    | extend fill_color = case(
        transport_mode == "bus",   "#007AC9",
        transport_mode == "tram",  "#00985F",
        transport_mode == "train", "#8C4799",
        transport_mode == "metro", "#FF6319",
        transport_mode == "ferry", "#00B9E4",
        transport_mode == "ubus",  "#9E9E9E",
        transport_mode == "robot", "#616161",
        "#455A64")
    | extend mode_label = case(
        transport_mode == "bus",   "Bus",
        transport_mode == "tram",  "Tram",
        transport_mode == "train", "Commuter train",
        transport_mode == "metro", "Metro",
        transport_mode == "ferry", "Ferry",
        transport_mode == "ubus",  "U-line bus",
        transport_mode == "robot", "Robot bus",
        "Other")
    | extend route_label = coalesce(desi, route_short_name, route_id, "")
    | extend speed_kmh = round(spd * 3.6, 1)
    | extend punctuality = case(isnull(dl), "unknown",
                                dl <= -300, "very late",
                                dl <= -60,  "late",
                                dl < 60,    "on time",
                                "early")
    | extend delay_label = case(isnull(dl), "n/a",
                                dl <= -60, strcat(tostring(abs(dl) / 60), " min late"),
                                dl >= 60,  strcat(tostring(dl / 60), " min early"),
                                "on time")
    | extend punct_color = case(punctuality == "very late", "#B91C1C",
                                punctuality == "late",      "#F97316",
                                punctuality == "on time",   "#10B981",
                                punctuality == "early",     "#3B82F6",
                                "#9CA3AF")
    | extend punct_label = case(punctuality == "very late", "5+ min late",
                                punctuality == "late",      "1-5 min late",
                                punctuality == "on time",   "On time",
                                punctuality == "early",     "Ahead of schedule",
                                "Unknown")
    | extend heading = iff(isnotnull(hdg) and hdg >= 0 and hdg <= 360, todouble(hdg), real(null))
    | extend label = iff(isnotempty(route_label),
                         iff(isnotempty(headsign), strcat(route_label, "  ", headsign), route_label),
                         headsign)
    | extend geometry = bag_pack("type", "Point", "coordinates", pack_array(['long'], lat))
    | project geometry, ___subject, operator_id, vehicle_number, transport_mode, mode_label,
              route_id, route_short_name, route_long_name, desi, route_label, headsign,
              latitude = lat, longitude = ['long'], heading, hdg, spd, speed_kmh, dl, delay_label,
              punctuality, punct_color, punct_label, occu, temporal_type,
              fill_color, freshness, age_min, label, ___time
}
''',
    # ------------------------------------------------------------------
    # Live vehicles rendered as bearing-oriented rectangles at z16+. Width and
    # length scale with latitude so the rectangles look right at street zoom.
    # Reuses ``hslhfp_vehicle_points`` so the colouring stays consistent.
    r'''
.create-or-alter function with (folder = "Map", skipvalidation = "true") hslhfp_vehicle_rectangles(lookback:timespan) {
    hslhfp_vehicle_points(lookback)
    | extend render_heading = coalesce(heading, 0.0)
    | extend rad = render_heading * pi() / 180.0
    | extend lon_scale = 1.0 / cos(latitude * pi() / 180.0)
    | extend half_len = 0.000060, half_wid = 0.000022
    | extend dlon_len = sin(rad) * half_len * lon_scale,
             dlat_len = cos(rad) * half_len,
             dlon_wid = cos(rad) * half_wid * lon_scale,
             dlat_wid = -sin(rad) * half_wid
    | extend p1 = strcat("[", tostring(round(longitude + dlon_len + dlon_wid, 7)), ",",
                              tostring(round(latitude + dlat_len + dlat_wid, 7)), "]"),
             p2 = strcat("[", tostring(round(longitude + dlon_len - dlon_wid, 7)), ",",
                              tostring(round(latitude + dlat_len - dlat_wid, 7)), "]"),
             p3 = strcat("[", tostring(round(longitude - dlon_len - dlon_wid, 7)), ",",
                              tostring(round(latitude - dlat_len - dlat_wid, 7)), "]"),
             p4 = strcat("[", tostring(round(longitude - dlon_len + dlon_wid, 7)), ",",
                              tostring(round(latitude - dlat_len + dlat_wid, 7)), "]")
    | extend geometry = parse_json(strcat('{"type":"Polygon","coordinates":[[',
                                          p1, ",", p2, ",", p3, ",", p4, ",", p1, ']]}'))
    | project geometry, ___subject, operator_id, vehicle_number, transport_mode, mode_label,
              route_id, route_label, desi, headsign, heading = round(render_heading, 0),
              spd, speed_kmh, dl, delay_label, punctuality,
              fill_color, freshness, age_min, label, ___time
}
''',
    # ------------------------------------------------------------------
    # All stops for the map: every logical station (platform-collapsed via
    # ``parent_station``) shown as a small bubble. HSL has ~7k stops (well under
    # Fabric's 100k cap) but we still stratify by ~0.005 degree (~0.5 km) cells
    # keeping the 6 busiest stations per cell, mirroring the gtfs pattern so the
    # layer scales if the feed ever widens.
    r'''
.create-or-alter function with (folder = "Map", skipvalidation = "true") hslhfp_stops_for_map() {
    hslhfp_stops()
    | extend group_key = iff(isempty(parent_station), stop_id, parent_station)
    | summarize stop_name = take_any(stop_name),
                stop_code = take_any(stop_code),
                lat = round(avg(stop_lat), 6),
                lon = round(avg(stop_lon), 6),
                platforms = dcount(stop_id, 1),
                location_type = take_any(location_type)
            by group_key
    | extend cell = strcat(tostring(bin(lat, 0.005)), ":", tostring(bin(lon, 0.005)))
    | partition hint.strategy=native by cell ( top 6 by platforms desc )
    | extend stop_kind = case(location_type == 1, "Station",
                              location_type == 2, "Entrance / exit",
                              location_type == 3, "Node",
                              location_type == 4, "Boarding area",
                              "Stop / platform")
    | extend marker_color = case(location_type == 1, "#0F172A",
                                 location_type == 2, "#1E293B",
                                 location_type == 3, "#475569",
                                 location_type == 4, "#334155",
                                 "#1E40AF")
    | extend label = iff(isnotempty(stop_code), strcat(stop_name, " (", stop_code, ")"), stop_name)
    | extend geometry = bag_pack("type", "Point", "coordinates", pack_array(lon, lat))
    | project geometry, stop_name, stop_code, platforms, stop_kind, marker_color, label
}
''',
    # ------------------------------------------------------------------
    # Vehicle density grid: per-cell count of live vehicles in the lookback
    # window. Operational overview (off by default) of where the fleet is
    # concentrated. Reuses ``hslhfp_vehicle_points`` for the freshness bound.
    r'''
.create-or-alter function with (folder = "Map", skipvalidation = "true") hslhfp_vehicle_grid(lookback:timespan, resolution:real) {
    hslhfp_vehicle_points(lookback)
    | extend lon0 = bin(longitude, resolution), lat0 = bin(latitude, resolution)
    | summarize vehicles = count(), avg_age = round(avg(age_min), 1),
                modes = dcount(transport_mode) by lon0, lat0
    | extend fill_color = case(vehicles >= 50, "#7a0177",
                               vehicles >= 20, "#c51b8a",
                               vehicles >= 5,  "#f768a1",
                               "#fbb4b9")
    | extend density_band = case(vehicles >= 50, "50+ vehicles",
                                 vehicles >= 20, "20-49 vehicles",
                                 vehicles >= 5,  "5-19 vehicles",
                                 "1-4 vehicles")
    | extend label = strcat(tostring(vehicles), " vehicles")
    | extend geometry = bag_pack("type", "Polygon", "coordinates", pack_array(pack_array(
        pack_array(lon0, lat0), pack_array(lon0 + resolution, lat0),
        pack_array(lon0 + resolution, lat0 + resolution), pack_array(lon0, lat0 + resolution),
        pack_array(lon0, lat0))))
    | project geometry, vehicles, avg_age, modes, density_band, fill_color, label
}
''',
    # ------------------------------------------------------------------
    # Transit-signal-priority events: the latest tlr (request) / tla (response)
    # per vehicle per signal group in the lookback window. Off by default - a
    # diagnostic overlay for where buses/trams request green-light priority.
    r'''
.create-or-alter function with (folder = "Map", skipvalidation = "true") hslhfp_tlp_events(lookback:timespan) {
    ['fi.hsl.hfp.TrafficLightEventLatest']
    | where ___time > ago(lookback)
    | where isnotnull(lat) and isnotnull(['long']) and lat != 0.0 and ['long'] != 0.0
    | summarize arg_max(___time, *) by ___subject, signal_groupid
    | extend tlp_kind = case(___type endswith "tla" and tlp_decision == "ACK", "Priority granted",
                         ___type endswith "tla",                            "Priority rejected",
                         ___type endswith "tlr",                            "Priority request",
                         "Other")
    | extend tlp_color = case(tlp_kind == "Priority granted",  "#10B981",
                              tlp_kind == "Priority rejected", "#EF4444",
                              tlp_kind == "Priority request",  "#F59E0B",
                              "#9CA3AF")
    | extend label = trim(" ", strcat(coalesce(desi, route_id, ""), " ", tlp_kind))
    | extend geometry = bag_pack("type", "Point", "coordinates", pack_array(['long'], lat))
    | project geometry, ___subject, transport_mode, desi, route_id, tlp_kind, tlp_decision,
              tlp_prioritylevel, signal_groupid, tlp_color, label, ___time
}
''',
]

# ---------------------------------------------------------------------------
# Layer styling - shared between layers. Fabric Maps doesn't honour
# ``["get", "field"]`` data-driven colours in bubble/line/polygon paint
# properties, so we use a hybrid: ``seriesGroup`` + ``customColors`` (for the
# Data Layers panel legend) AND a MapLibre ``match`` expression on the paint
# property (which is what actually renders). Both are written at deploy time;
# ``customColors`` is populated from a per-layer ``distinct`` query.
# ---------------------------------------------------------------------------

LABEL_BASE = {
    "enabled": False,
    "size": 11,
    "color": "#111111",
    "textStrokeColor": "#FFFFFF",
    "textStrokeWidth": 2,
    "allowOverlap": False,
}

# Seed palettes (keyed on the legend label). When a layer's legend column
# differs from its paint column the seed is re-enumerated from live data; the
# seeds document the expected domain and act as a static fallback.
MODE_PALETTE_SEED = {
    "Bus": "#007AC9", "Tram": "#00985F", "Commuter train": "#8C4799",
    "Metro": "#FF6319", "Ferry": "#00B9E4", "U-line bus": "#9E9E9E",
    "Robot bus": "#616161", "Other": "#455A64",
}
STOP_PALETTE_SEED = {
    "Stop / platform": "#1E40AF", "Station": "#0F172A", "Entrance / exit": "#1E293B",
    "Node": "#475569", "Boarding area": "#334155",
}
PUNCT_PALETTE_SEED = {
    "5+ min late": "#B91C1C", "1-5 min late": "#F97316", "On time": "#10B981",
    "Ahead of schedule": "#3B82F6", "Unknown": "#9CA3AF",
}
DENSITY_PALETTE_SEED = {
    "50+ vehicles": "#7a0177", "20-49 vehicles": "#c51b8a",
    "5-19 vehicles": "#f768a1", "1-4 vehicles": "#fbb4b9",
}
TLP_PALETTE_SEED = {
    "Priority granted": "#10B981", "Priority rejected": "#EF4444",
    "Priority request": "#F59E0B", "Other": "#9CA3AF",
}


def _series(column: str, palette: dict[str, str],
            paint_column: str | None = None) -> dict[str, Any]:
    series: dict[str, Any] = {
        "enableSeriesGroup": True,
        "seriesGroup": column,
        "customColors": dict(palette),
    }
    # When the legend column (seriesGroup) differs from the column that
    # actually carries the paint colour, record the paint column so
    # _populate_palette can map legend-label -> colour. This non-Fabric key is
    # consumed and removed before the definition is serialised.
    if paint_column and paint_column != column:
        series["_paintColorColumn"] = paint_column
    return series


def _color_match(column: str, palette: dict[str, str], fallback: str = "#888888") -> list[Any]:
    expr: list[Any] = ["match", ["get", column]]
    for value, color in palette.items():
        expr.append(value)
        expr.append(color)
    expr.append(fallback)
    return expr


def bubble_options(*, visible: bool, radius: int = 4,
                   labels: bool = False, label_size: int = 11,
                   min_zoom: float | None = None, max_zoom: float | None = None,
                   color_column: str = "fill_color",
                   legend_column: str | None = None,
                   palette: dict[str, str] | None = None,
                   tooltip_keys: list[str] | None = None,
                   stroke_color: str = "#FFFFFF") -> dict[str, Any]:
    pal = palette if palette is not None else {}
    legend = legend_column or color_column
    opts: dict[str, Any] = {
        "type": "vector",
        "visible": visible,
        "pointLayerType": "bubble",
        "bubbleOptions": {
            "color": "#888888",
            "radius": radius,
            "strokeColor": stroke_color,
            "strokeWidth": 1,
            "opacity": 0.92,
            **_series(legend, pal, paint_column=color_column),
        },
        "dataLabelKeys": ["label"],
        "dataLabelOptions": dict(LABEL_BASE, enabled=labels, size=label_size),
        "tooltipKeys": tooltip_keys or ["label"],
        "enablePopups": True,
    }
    if min_zoom is not None:
        opts["minZoom"] = min_zoom
    if max_zoom is not None:
        opts["maxZoom"] = max_zoom
    return opts


def polygon_options(*, visible: bool, color_column: str = "fill_color",
                    legend_column: str | None = None,
                    palette: dict[str, str] | None = None,
                    fill_opacity: float = 0.55,
                    stroke_color: Any = "#202020",
                    stroke_width: int = 0,
                    labels: bool = False, label_size: int = 10,
                    min_zoom: float | None = None) -> dict[str, Any]:
    pal = palette if palette is not None else {}
    legend = legend_column or color_column
    opts: dict[str, Any] = {
        "type": "vector",
        "visible": visible,
        "polygonOptions": {
            "fillColor": "#888888",
            "fillOpacity": fill_opacity,
            **_series(legend, pal, paint_column=color_column),
        },
        "lineOptions": {
            "strokeColor": stroke_color,
            "strokeWidth": stroke_width,
            "strokeOpacity": 0.15,
        },
        "dataLabelKeys": ["label"],
        "dataLabelOptions": dict(LABEL_BASE, enabled=labels, size=label_size),
        "tooltipKeys": ["label", "vehicles", "avg_age", "modes", "density_band"],
        "enablePopups": True,
    }
    if min_zoom is not None:
        opts["minZoom"] = min_zoom
    return opts


def vehicle_rectangle_options() -> dict[str, Any]:
    return {
        "type": "vector",
        "visible": True,
        "minZoom": 16,
        "polygonOptions": {
            "fillColor": "#888888",
            "fillOpacity": 0.95,
            **_series("mode_label", dict(MODE_PALETTE_SEED), paint_column="fill_color"),
        },
        "lineOptions": {
            "strokeColor": "#202020",
            "strokeWidth": 1,
            "strokeOpacity": 0.95,
        },
        "dataLabelKeys": ["route_label"],
        "dataLabelOptions": dict(
            LABEL_BASE,
            enabled=True,
            size=9,
            color="#FFFFFF",
            textStrokeColor="#000000",
            textStrokeWidth=1.5,
            allowOverlap=True,
        ),
        "tooltipKeys": [
            "route_label", "desi", "mode_label", "route_id", "headsign",
            "heading", "speed_kmh", "delay_label", "punctuality",
            "freshness", "age_min", "vehicle_number", "operator_id", "___subject",
        ],
        "enablePopups": True,
    }


def _text_filter(field: str) -> dict[str, Any]:
    return {
        "id": str(uuid.uuid4()),
        "type": "text",
        "field": field,
        "locked": False,
        "value": [],
    }


# ---------------------------------------------------------------------------
# Layer declarations - one entry per Fabric Map vector layer.
# ---------------------------------------------------------------------------

@dataclass
class Layer:
    name: str
    kql: str
    options: dict[str, Any]
    filters: list[dict[str, Any]]


def _layers() -> list[Layer]:
    return [
        Layer(
            "HSL - Live vehicles",
            "hslhfp_vehicle_points(5m)",
            bubble_options(
                visible=True, radius=4, min_zoom=8, max_zoom=16,
                color_column="fill_color", legend_column="mode_label",
                palette=MODE_PALETTE_SEED,
                tooltip_keys=[
                    "route_label", "desi", "route_id", "headsign", "mode_label",
                    "speed_kmh", "delay_label", "punctuality", "occu",
                    "freshness", "age_min", "___subject",
                ],
            ),
            [_text_filter("transport_mode"), _text_filter("desi")],
        ),
        Layer(
            "HSL - Live vehicles (detail)",
            "hslhfp_vehicle_rectangles(5m)",
            vehicle_rectangle_options(),
            [_text_filter("transport_mode"), _text_filter("desi")],
        ),
        Layer(
            "HSL - Transit stops",
            "hslhfp_stops_for_map()",
            bubble_options(
                visible=True, radius=3, labels=True, label_size=10, min_zoom=13,
                color_column="marker_color", legend_column="stop_kind",
                palette=STOP_PALETTE_SEED,
                tooltip_keys=["stop_name", "stop_code", "platforms", "stop_kind"],
            ),
            [],
        ),
        Layer(
            "HSL - Vehicle punctuality",
            "hslhfp_vehicle_points(5m)",
            bubble_options(
                visible=False, radius=5, min_zoom=11,
                color_column="punct_color", legend_column="punct_label",
                palette=PUNCT_PALETTE_SEED,
                tooltip_keys=[
                    "route_label", "desi", "punctuality", "delay_label",
                    "mode_label", "speed_kmh", "age_min",
                ],
            ),
            [_text_filter("punctuality"), _text_filter("transport_mode")],
        ),
        Layer(
            "HSL - Vehicle density",
            "hslhfp_vehicle_grid(5m, 0.01)",
            polygon_options(
                visible=False, color_column="fill_color", legend_column="density_band",
                palette=DENSITY_PALETTE_SEED,
            ),
            [],
        ),
        Layer(
            "HSL - Traffic-signal priority",
            "hslhfp_tlp_events(30m)",
            bubble_options(
                visible=False, radius=6, min_zoom=12,
                color_column="tlp_color", legend_column="tlp_kind",
                palette=TLP_PALETTE_SEED,
                tooltip_keys=[
                    "label", "desi", "route_id", "tlp_kind", "tlp_decision",
                    "tlp_prioritylevel", "signal_groupid", "transport_mode",
                ],
            ),
            [_text_filter("tlp_kind"), _text_filter("transport_mode")],
        ),
    ]

# ---------------------------------------------------------------------------
# Map definition patching.
# ---------------------------------------------------------------------------

HELSINKI_CENTER = [24.9384, 60.1699]  # lon, lat - final basemap fallback


def _b64(s: str) -> str:
    return base64.b64encode(s.encode("utf-8")).decode("ascii")


def _get_definition(fab: requests.Session, api_base: str, workspace_id: str,
                    map_id: str) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    res = _poll_lro(
        fab,
        fab.post(f"{api_base}/workspaces/{workspace_id}/items/{map_id}/getDefinition"),
    )
    parts = {p["path"]: p for p in res["definition"]["parts"]}
    if "map.json" not in parts:
        raise RuntimeError("Map definition has no map.json part")
    mp = json.loads(base64.b64decode(parts["map.json"]["payload"]).decode("utf-8"))
    mp.setdefault("dataSources", [])
    mp.setdefault("iconSources", [])
    mp.setdefault("layerSources", [])
    mp.setdefault("layerSettings", [])
    if "$schema" not in mp:
        mp["$schema"] = ("https://developer.microsoft.com/json-schemas/fabric/item/map/"
                         "definition/2.0.0/schema.json")
    return mp, parts


def _put_definition(fab: requests.Session, api_base: str, workspace_id: str,
                    map_id: str, mp: dict[str, Any],
                    parts: dict[str, dict[str, Any]]) -> None:
    parts["map.json"] = {
        "path": "map.json",
        "payload": _b64(json.dumps(mp, indent=2)),
        "payloadType": "InlineBase64",
    }
    r = fab.post(
        f"{api_base}/workspaces/{workspace_id}/items/{map_id}/updateDefinition",
        json={"definition": {"parts": list(parts.values())}},
    )
    print(f"updateDefinition HTTP {r.status_code}")
    _poll_lro(fab, r)


def _bbox(ks: requests.Session, kusto_uri: str,
          kusto_db: str) -> Optional[tuple[float, float, float, float, int]]:
    """Return (lat_p01, lat_p99, lon_p01, lon_p99, n) or None.

    Tries the stop bounding box first, then falls back to the live vehicle
    footprint (a brand-new database may have telemetry before the GTFS static
    reference has been ingested)."""
    candidates = (
        "hslhfp_bbox()",
        ("hslhfp_vehicle_points(30m) | summarize "
         "lat_p01 = percentile(latitude, 1), lat_p99 = percentile(latitude, 99), "
         "lon_p01 = percentile(longitude, 1), lon_p99 = percentile(longitude, 99), "
         "cnt = count()"),
    )
    for csl in candidates:
        try:
            frame = _kql_query(ks, kusto_uri, kusto_db, csl)
        except Exception as exc:
            print(f"  bbox lookup failed ({csl[:24]}...): {exc}")
            continue
        if not frame or not frame.get("Rows"):
            continue
        cols = [c["ColumnName"] for c in frame["Columns"]]
        rec = dict(zip(cols, frame["Rows"][0]))
        if not rec.get("cnt"):
            continue
        try:
            return (
                float(rec["lat_p01"]), float(rec["lat_p99"]),
                float(rec["lon_p01"]), float(rec["lon_p99"]), int(rec["cnt"]),
            )
        except (TypeError, ValueError):
            continue
    return None


def _zoom_for_extent(lat_span: float, lon_span: float) -> float:
    """Pick a sensible default zoom for the bounding box. Tuned for a
    ~1600x1000 viewport; errs on the side of zooming OUT slightly so the full
    source is visible at first render."""
    span = max(lat_span, lon_span / 2.0)  # account for Mercator distortion
    if span >= 30:  return 3.5
    if span >= 15:  return 4.5
    if span >= 8:   return 5.5
    if span >= 4:   return 6.7
    if span >= 2:   return 8.0
    if span >= 1:   return 9.5
    if span >= 0.5: return 10.6
    if span >= 0.2: return 11.5
    return 12.5


def _set_basemap(mp: dict[str, Any],
                 bbox: Optional[tuple[float, float, float, float, int]]) -> None:
    if bbox is None:
        center = list(HELSINKI_CENTER)
        zoom = 11.0
    else:
        lat_p01, lat_p99, lon_p01, lon_p99, _ = bbox
        center = [(lon_p01 + lon_p99) / 2.0, (lat_p01 + lat_p99) / 2.0]
        zoom = _zoom_for_extent(lat_p99 - lat_p01, lon_p99 - lon_p01)
    mp["basemap"] = {
        "options": {
            "center": center,
            "zoom": zoom,
            "style": "grayscale_light",
            "showLabels": True,
        },
        "controls": {
            "zoom": True, "pitch": True, "compass": True, "scale": True,
            "traffic": False, "style": True,
        },
        "backgroundColor": "#FFFFFF",
        "theme": "light",
    }
    print(f"  basemap center={center} zoom={zoom}")


def _populate_palette(ks: requests.Session, kusto_uri: str, kusto_db: str,
                      layer: Layer) -> None:
    """For each seriesGroup-bound paint property on the layer, fetch the
    distinct values from the live data and populate ``customColors`` as an
    identity map. Also write a MapLibre ``match`` expression to the paint
    property (Fabric's ``seriesGroup`` populates the legend but does not
    actually drive paint colour)."""
    paint_key_for = {
        "bubbleOptions": "color",
        "lineOptions": "strokeColor",
        "polygonOptions": "fillColor",
    }
    for sub, paint_key in paint_key_for.items():
        block = layer.options.get(sub)
        if not block or not block.get("enableSeriesGroup"):
            continue
        column = block.get("seriesGroup")
        if not column:
            continue
        # Non-Fabric marker: when present the legend column (seriesGroup) is a
        # human label distinct from the column carrying the paint colour.
        paint_column = block.pop("_paintColorColumn", None)
        if paint_column and paint_column != column:
            block["customColors"] = {}
        try:
            if paint_column and paint_column != column:
                frame = _kql_query(
                    ks, kusto_uri, kusto_db,
                    f"{layer.kql}\n| where isnotempty({column}) and isnotempty({paint_column})"
                    f"\n| distinct {column}, {paint_column}\n| take 200",
                )
                pairs = [(row[0], row[1]) for row in (frame.get("Rows") or [])
                         if row and row[0] and row[1]]
            else:
                frame = _kql_query(
                    ks, kusto_uri, kusto_db,
                    f"{layer.kql}\n| where isnotempty({column})"
                    f"\n| distinct {column}\n| take 50",
                )
                pairs = [(row[0], row[0]) for row in (frame.get("Rows") or [])
                         if row and row[0]]
        except Exception as exc:
            print(f"    palette enumeration failed for {layer.name}/{column}: {exc}")
            pairs = []
        if not pairs:
            continue
        block.setdefault("customColors", {})
        for label, color in pairs:
            block["customColors"].setdefault(label, color)
        block[paint_key] = _color_match(column, block["customColors"])
        print(f"    palette {column}: {len(block['customColors'])} colors")


# ---------------------------------------------------------------------------
# Top-level wiring entry point.
# ---------------------------------------------------------------------------

def wire(*, workspace_id: str, map_id: str, kql_db_id: str,
         kusto_uri: str, kusto_db: str,
         fabric_token: str, kusto_token: str,
         api_base: str = "https://api.fabric.microsoft.com/v1") -> None:
    fab = _session(fabric_token)
    ks = _session(kusto_token)

    # 1. Create/refresh the helper KQL functions in the target database.
    print(f"Creating {len(HSL_HFP_FUNCTIONS)} helper functions in {kusto_db}")
    for f in HSL_HFP_FUNCTIONS:
        head = next((line.strip() for line in f.splitlines() if line.strip()), "")
        print(f"  {head[:110]}")
        _kql_mgmt(ks, kusto_uri, kusto_db, f)

    # 2. Look up the source's geographic footprint to centre the basemap.
    print("Discovering bounding box from hslhfp_bbox()")
    bbox = _bbox(ks, kusto_uri, kusto_db)
    if bbox is None:
        print("  no stops/vehicles indexed yet; centring on Helsinki")
    else:
        lat_p01, lat_p99, lon_p01, lon_p99, n = bbox
        print(f"  {n} features; lat=[{lat_p01:.3f}, {lat_p99:.3f}]"
              f" lon=[{lon_p01:.3f}, {lon_p99:.3f}]")

    # 3. Patch the map definition idempotently.
    mp, parts = _get_definition(fab, api_base, workspace_id, map_id)
    _set_basemap(mp, bbox)

    # Drop previously-wired layers whose source is bound to this KQL DB so we
    # don't accumulate stale layers across re-runs.
    removed_src_ids = {
        s["id"] for s in mp.get("layerSources", [])
        if s.get("itemId") == kql_db_id
    }
    if removed_src_ids:
        print(f"  removing {len(removed_src_ids)} pre-existing hsl-hfp layer source(s)")
    mp["layerSettings"] = [ls for ls in mp.get("layerSettings", [])
                           if ls.get("sourceId") not in removed_src_ids]
    mp["layerSources"] = [s for s in mp.get("layerSources", [])
                          if s["id"] not in removed_src_ids]
    for path in list(parts):
        if path.startswith("queries/layerSource-"):
            sid = path.split("layerSource-", 1)[1].split(".kql", 1)[0]
            if sid in removed_src_ids:
                del parts[path]

    # Ensure this KQL DB is registered as a data source.
    if not any(d.get("itemId") == kql_db_id for d in mp["dataSources"]):
        mp["dataSources"].append({
            "itemType": "KqlDatabase",
            "workspaceId": workspace_id,
            "itemId": kql_db_id,
        })

    # 4. Add each layer, validating the query and populating the palette.
    for layer in _layers():
        print(f"  layer {layer.name}")
        try:
            cnt_frame = _kql_query(ks, kusto_uri, kusto_db, f"{layer.kql}\n| count")
            cnt = cnt_frame["Rows"][0][0] if cnt_frame and cnt_frame.get("Rows") else "?"
            print(f"    rows: {cnt}")
        except Exception as exc:
            print(f"    validation failed (skipping): {exc}")
            continue

        _populate_palette(ks, kusto_uri, kusto_db, layer)

        src_id = str(uuid.uuid4())
        mp["layerSources"].append({
            "id": src_id,
            "name": f"{layer.name}_source",
            "type": "kusto",
            "options": {"cluster": False},
            "itemId": kql_db_id,
            "refreshIntervalMs": 0,
        })
        mp["layerSettings"].append({
            "id": str(uuid.uuid4()),
            "name": layer.name,
            "sourceId": src_id,
            "geometryColumnName": "geometry",
            "filters": layer.filters,
            "options": layer.options,
        })
        parts[f"queries/layerSource-{src_id}.kql"] = {
            "path": f"queries/layerSource-{src_id}.kql",
            "payload": _b64(layer.kql),
            "payloadType": "InlineBase64",
        }

    _put_definition(fab, api_base, workspace_id, map_id, mp, parts)
    print(f"OK - map {map_id} updated with {len(_layers())} layers")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--workspace-id", default=os.environ.get("FABRIC_WORKSPACE_ID"))
    ap.add_argument("--map-id",       default=os.environ.get("FABRIC_MAP_ID"))
    ap.add_argument("--kql-db-id",    default=os.environ.get("FABRIC_KQL_DB_ID"))
    ap.add_argument("--kusto-uri",    default=os.environ.get("KUSTO_CLUSTER_URI"))
    ap.add_argument("--kusto-db",     default=os.environ.get("KUSTO_DB", "hsl_hfp"))
    ap.add_argument("--api-base",     default=os.environ.get(
        "FABRIC_API_BASE", "https://api.fabric.microsoft.com/v1"))
    args = ap.parse_args(argv)

    missing = [n for n in ("workspace_id", "map_id", "kql_db_id", "kusto_uri")
               if not getattr(args, n)]
    if missing:
        ap.error("missing required: " + ", ".join("--" + m.replace("_", "-") for m in missing))
        return 2

    fabric_token = _get_token("FABRIC_TOKEN", "https://api.fabric.microsoft.com/.default")
    kusto_token = _get_token("KUSTO_TOKEN", "https://kusto.fabric.microsoft.com/.default")

    wire(
        workspace_id=args.workspace_id,
        map_id=args.map_id,
        kql_db_id=args.kql_db_id,
        kusto_uri=args.kusto_uri,
        kusto_db=args.kusto_db,
        fabric_token=fabric_token,
        kusto_token=kusto_token,
        api_base=args.api_base,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())