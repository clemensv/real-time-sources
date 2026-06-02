"""Create or refresh a Fabric Map for the aisstream feeder.

The map is tuned for live maritime situational awareness and adds six layers:

1. Vessel density grid   - world-scale heat surface showing vessel concentration
2. Live vessel symbols   - current vessel positions coloured by ship category
3. Vessel footprints     - heading-aware hull polygons for close inspection
4. Feed freshness grid   - where the latest AIS traffic is getting stale
5. Aids to navigation    - physical / virtual / off-position AtoN markers
6. Base stations         - shore-side AIS receivers, including long-range sites

The script is idempotent for its own layers: it removes previously generated
"aisstream " layers from the target map and recreates them against the current
KQL database.
"""

from __future__ import annotations

import argparse
import base64
import copy
import json
import os
import sys
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

import requests


def _get_token(env_name: str, scope: str | list[str]) -> str:
    token = os.environ.get(env_name)
    if token:
        return token.strip()
    try:
        from azure.identity import DefaultAzureCredential
    except ImportError as exc:  # pragma: no cover - exercised in live deploys
        raise SystemExit(
            f"{env_name} not set and azure-identity not installed; "
            f"either export {env_name} or install azure-identity."
        ) from exc
    credential = DefaultAzureCredential()
    scopes = [scope] if isinstance(scope, str) else list(scope)
    last_exc: Exception | None = None
    for candidate in scopes:
        try:
            return credential.get_token(candidate).token
        except Exception as exc:  # pragma: no cover - exercised in live deploys
            last_exc = exc
    if last_exc is not None:
        raise last_exc
    raise SystemExit(f"{env_name} scope list was empty.")


def _session(token: str) -> requests.Session:
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token}"
    session.headers["Content-Type"] = "application/json"
    return session


def _poll_lro(session: requests.Session, response: requests.Response) -> Any:
    if response.status_code != 202:
        response.raise_for_status()
        return response.json() if response.content else None
    op_url = response.headers["Location"]
    while True:
        status = session.get(op_url).json()
        if status.get("status") == "Succeeded":
            result = session.get(op_url + "/result")
            return result.json() if result.content else None
        if status.get("status") == "Failed":
            raise RuntimeError(f"Fabric LRO failed: {json.dumps(status)[:800]}")
        time.sleep(2)


def _kql_mgmt(session: requests.Session, kusto_uri: str, db: str, csl: str) -> dict[str, Any]:
    response = session.post(f"{kusto_uri.rstrip('/')}/v1/rest/mgmt", json={"db": db, "csl": csl})
    if response.status_code >= 400:
        raise RuntimeError(f"KQL mgmt failed ({db}): HTTP {response.status_code} {response.text[:800]}")
    return response.json()


def _kql_query(session: requests.Session, kusto_uri: str, db: str, csl: str) -> Optional[dict[str, Any]]:
    response = session.post(f"{kusto_uri.rstrip('/')}/v2/rest/query", json={"db": db, "csl": csl})
    if response.status_code >= 400:
        raise RuntimeError(f"KQL query failed ({db}): HTTP {response.status_code} {response.text[:800]}")
    for frame in response.json():
        if frame.get("FrameType") == "DataTable" and frame.get("TableKind") == "PrimaryResult":
            return frame
    return None


AIS_FUNCTIONS = [
    """
.create-or-alter function with (folder = "Map", skipvalidation = "true") ais_static_latest() {
    union isfuzzy = true
        (ShipStaticDataLatest
         | project
             mmsi = tolong(UserID),
             vessel_name = trim(" ", tostring(Name)),
             call_sign = trim(" ", tostring(CallSign)),
             destination = trim(" ", tostring(Destination)),
             ship_type = toint(Type),
             draught_m = todouble(MaximumStaticDraught),
             dim_a = toint(Dimension.A),
             dim_b = toint(Dimension.B),
             dim_c = toint(Dimension.C),
             dim_d = toint(Dimension.D),
             static_source = "ShipStaticData",
             static_reported_at = ___time),
        (StaticDataReportLatest
         | project
             mmsi = tolong(UserID),
             vessel_name = trim(" ", tostring(ReportA.Name)),
             call_sign = trim(" ", tostring(ReportB.CallSign)),
             destination = "",
             ship_type = toint(ReportB.ShipType),
             draught_m = real(null),
             dim_a = toint(ReportB.Dimension.A),
             dim_b = toint(ReportB.Dimension.B),
             dim_c = toint(ReportB.Dimension.C),
             dim_d = toint(ReportB.Dimension.D),
             static_source = "StaticDataReport",
             static_reported_at = ___time),
        (ExtendedClassBPositionReportLatest
         | project
             mmsi = tolong(UserID),
             vessel_name = trim(" ", tostring(Name)),
             call_sign = "",
             destination = "",
             ship_type = toint(Type),
             draught_m = real(null),
             dim_a = toint(Dimension.A),
             dim_b = toint(Dimension.B),
             dim_c = toint(Dimension.C),
             dim_d = toint(Dimension.D),
             static_source = "ExtendedClassBPositionReport",
             static_reported_at = ___time)
    | where mmsi > 0
    | summarize arg_max(static_reported_at, *) by mmsi
    | extend
        length_m = iff(coalesce(dim_a, 0) + coalesce(dim_b, 0) > 0, todouble(coalesce(dim_a, 0) + coalesce(dim_b, 0)), real(null)),
        beam_m = iff(coalesce(dim_c, 0) + coalesce(dim_d, 0) > 0, todouble(coalesce(dim_c, 0) + coalesce(dim_d, 0)), real(null)),
        ship_type_bucket = case(
            ship_type between (70 .. 79), "cargo",
            ship_type between (80 .. 89), "tanker",
            ship_type between (60 .. 69), "passenger",
            ship_type == 30, "fishing",
            ship_type in (31, 32, 52), "tug",
            ship_type == 35, "military",
            ship_type == 36, "sailing",
            ship_type == 37, "pleasure",
            ship_type between (40 .. 49), "fast craft",
            ship_type == 51, "search and rescue",
            ship_type in (50, 53, 54, 55, 58), "service",
            ship_type between (90 .. 99), "other",
            "unknown")
}
""".strip(),
    """
.create-or-alter function with (folder = "Map", skipvalidation = "true") ais_live_positions(lookback:timespan) {
    union isfuzzy = true
        (PositionReportLatest
         | project
             mmsi = tolong(UserID),
             latitude = todouble(Latitude),
             longitude = todouble(Longitude),
             sog = todouble(Sog),
             cog = todouble(Cog),
             heading = iff(toint(TrueHeading) between (0 .. 359), todouble(TrueHeading), real(null)),
             nav_status = toint(NavigationalStatus),
             position_source = "Class A",
             reported_at = ___time),
        (StandardClassBPositionReportLatest
         | project
             mmsi = tolong(UserID),
             latitude = todouble(Latitude),
             longitude = todouble(Longitude),
             sog = todouble(Sog),
             cog = todouble(Cog),
             heading = real(null),
             nav_status = int(null),
             position_source = "Class B",
             reported_at = ___time),
        (ExtendedClassBPositionReportLatest
         | project
             mmsi = tolong(UserID),
             latitude = todouble(Latitude),
             longitude = todouble(Longitude),
             sog = todouble(Sog),
             cog = todouble(Cog),
             heading = iff(toint(TrueHeading) between (0 .. 359), todouble(TrueHeading), real(null)),
             nav_status = int(null),
             position_source = "Class B extended",
             reported_at = ___time),
        (LongRangeAisBroadcastMessageLatest
         | project
             mmsi = tolong(UserID),
             latitude = todouble(Latitude),
             longitude = todouble(Longitude),
             sog = todouble(Sog),
             cog = todouble(Cog),
             heading = real(null),
             nav_status = int(null),
             position_source = "Long range",
             reported_at = ___time),
        (StandardSearchAndRescueAircraftReportLatest
         | project
             mmsi = tolong(UserID),
             latitude = todouble(Latitude),
             longitude = todouble(Longitude),
             sog = todouble(Sog),
             cog = todouble(Cog),
             heading = real(null),
             nav_status = int(null),
             position_source = "SAR aircraft",
             reported_at = ___time)
    | where mmsi > 0
    | where isnotnull(latitude) and isnotnull(longitude)
    | where latitude between (-89.999 .. 89.999)
    | where longitude between (-179.999 .. 179.999)
    | where reported_at > ago(lookback)
    | summarize arg_max(reported_at, *) by mmsi
    | extend
        age_min = datetime_diff('minute', now(), reported_at),
        nav_status_label = case(
            nav_status == 0, "under way using engine",
            nav_status == 1, "at anchor",
            nav_status == 2, "not under command",
            nav_status == 5, "moored",
            nav_status == 7, "engaged in fishing",
            nav_status == 8, "under way sailing",
            isnull(nav_status), "",
            strcat("status ", tostring(nav_status)))
}
""".strip(),
    """
.create-or-alter function with (folder = "Map", skipvalidation = "true") ais_vessels_enriched(lookback:timespan) {
    ais_live_positions(lookback)
    | join kind = leftouter (
        ais_static_latest()
        | project
            mmsi,
            vessel_name,
            call_sign,
            destination,
            ship_type,
            ship_type_bucket,
            draught_m,
            dim_a,
            dim_b,
            dim_c,
            dim_d,
            length_m,
            beam_m,
            static_source
    ) on mmsi
    | extend
        vessel_label = iff(isnotempty(vessel_name), vessel_name, tostring(mmsi)),
        ship_type_bucket = case(
            position_source == "SAR aircraft", "search and rescue",
            isnotempty(ship_type_bucket), ship_type_bucket,
            "unknown"),
        ship_type_label = iff(isnull(ship_type), "unknown", strcat("type ", tostring(ship_type))),
        geometry = bag_pack("type", "Point", "coordinates", pack_array(longitude, latitude))
    | project
        mmsi,
        vessel_label,
        vessel_name,
        call_sign,
        destination,
        ship_type,
        ship_type_bucket,
        ship_type_label,
        position_source,
        nav_status,
        nav_status_label,
        sog,
        cog,
        heading,
        draught_m,
        length_m,
        beam_m,
        dim_a,
        dim_b,
        dim_c,
        dim_d,
        reported_at,
        age_min,
        latitude,
        longitude,
        static_source,
        geometry
}
""".strip(),
    """
.create-or-alter function with (folder = "Map", skipvalidation = "true") ais_vessel_density_grid(lookback:timespan, resolution_deg:real) {
    ais_vessels_enriched(lookback)
    | extend
        cell_lon = bin(longitude, resolution_deg),
        cell_lat = bin(latitude, resolution_deg)
    | summarize
        vessel_count = count(),
        cargo_count = countif(ship_type_bucket == "cargo"),
        tanker_count = countif(ship_type_bucket == "tanker"),
        passenger_count = countif(ship_type_bucket == "passenger"),
        avg_speed_kn = round(avg(sog), 1),
        newest_report = max(reported_at)
      by cell_lon, cell_lat
    | extend
        newest_age_min = datetime_diff('minute', now(), newest_report),
        label = strcat(vessel_count, " vessels"),
        geometry = bag_pack(
            "type", "Polygon",
            "coordinates", pack_array(pack_array(
                pack_array(cell_lon, cell_lat),
                pack_array(cell_lon + resolution_deg, cell_lat),
                pack_array(cell_lon + resolution_deg, cell_lat + resolution_deg),
                pack_array(cell_lon, cell_lat + resolution_deg),
                pack_array(cell_lon, cell_lat)
            )))
    | project
        geometry,
        label,
        vessel_count,
        cargo_count,
        tanker_count,
        passenger_count,
        avg_speed_kn,
        newest_age_min,
        newest_report,
        cell_lon,
        cell_lat
}
""".strip(),
    """
.create-or-alter function with (folder = "Map") ais_vessel_rectangles(lookback:timespan) {
    ais_vessels_enriched(lookback)
    | extend render_heading = iff(isnotnull(heading) and heading >= 0 and heading < 360, heading, iff(isnotnull(cog) and cog >= 0 and cog < 360, cog, 0.0))
    | extend angle_rad = render_heading * pi() / 180.0
    | extend length_m = iff(isnull(length_m) or length_m < 35, 35.0, length_m), beam_m = iff(isnull(beam_m) or beam_m < 8, 8.0, beam_m)
    | extend forward_m = iff(coalesce(dim_a, 0) > 0, todouble(dim_a), length_m / 2.0), aft_m = iff(coalesce(dim_b, 0) > 0, todouble(dim_b), length_m / 2.0), port_m = iff(coalesce(dim_c, 0) > 0, todouble(dim_c), beam_m / 2.0), starboard_m = iff(coalesce(dim_d, 0) > 0, todouble(dim_d), beam_m / 2.0)
    | extend lat_scale = 111320.0, lon_scale = 111320.0 * iff(abs(cos(latitude * pi() / 180.0)) > 0.15, abs(cos(latitude * pi() / 180.0)), 0.15)
    | extend bow_lon = longitude + (cos(angle_rad) * forward_m) / lon_scale, bow_lat = latitude + (sin(angle_rad) * forward_m) / lat_scale, s1_lon = longitude + ((cos(angle_rad) * (forward_m * 0.35)) + (sin(angle_rad) * starboard_m)) / lon_scale, s1_lat = latitude + ((sin(angle_rad) * (forward_m * 0.35)) - (cos(angle_rad) * starboard_m)) / lat_scale, s2_lon = longitude + ((-cos(angle_rad) * aft_m) + (sin(angle_rad) * starboard_m * 0.85)) / lon_scale, s2_lat = latitude + ((-sin(angle_rad) * aft_m) - (cos(angle_rad) * starboard_m * 0.85)) / lat_scale, s3_lon = longitude + ((-cos(angle_rad) * aft_m) - (sin(angle_rad) * port_m * 0.85)) / lon_scale, s3_lat = latitude + ((-sin(angle_rad) * aft_m) + (cos(angle_rad) * port_m * 0.85)) / lat_scale, s4_lon = longitude + ((cos(angle_rad) * (forward_m * 0.35)) - (sin(angle_rad) * port_m)) / lon_scale, s4_lat = latitude + ((sin(angle_rad) * (forward_m * 0.35)) + (cos(angle_rad) * port_m)) / lat_scale
    | extend heading_label = strcat(round(render_heading, 0), " deg"), geometry = bag_pack("type", "Polygon", "coordinates", pack_array(pack_array(pack_array(round(bow_lon, 6), round(bow_lat, 6)), pack_array(round(s1_lon, 6), round(s1_lat, 6)), pack_array(round(s2_lon, 6), round(s2_lat, 6)), pack_array(round(s3_lon, 6), round(s3_lat, 6)), pack_array(round(s4_lon, 6), round(s4_lat, 6)), pack_array(round(bow_lon, 6), round(bow_lat, 6)))))
    | project
        geometry,
        mmsi,
        vessel_label,
        position_source,
        ship_type_bucket,
        destination,
        sog,
        cog,
        heading = render_heading,
        heading_label,
        length_m,
        beam_m,
        age_min,
        reported_at
}
""".strip(),
    """
.create-or-alter function with (folder = "Map", skipvalidation = "true") ais_feed_freshness_grid(lookback:timespan, resolution_deg:real) {
    ais_vessels_enriched(lookback)
    | extend
        cell_lon = bin(longitude, resolution_deg),
        cell_lat = bin(latitude, resolution_deg)
    | summarize
        vessel_count = count(),
        avg_age_min = round(avg(age_min), 1),
        min_age_min = min(age_min),
        max_age_min = max(age_min),
        newest_report = max(reported_at)
      by cell_lon, cell_lat
    | extend
        label = strcat(round(max_age_min, 0), " min"),
        geometry = bag_pack(
            "type", "Polygon",
            "coordinates", pack_array(pack_array(
                pack_array(cell_lon, cell_lat),
                pack_array(cell_lon + resolution_deg, cell_lat),
                pack_array(cell_lon + resolution_deg, cell_lat + resolution_deg),
                pack_array(cell_lon, cell_lat + resolution_deg),
                pack_array(cell_lon, cell_lat)
            )))
    | project
        geometry,
        label,
        vessel_count,
        avg_age_min,
        min_age_min,
        max_age_min,
        newest_report,
        cell_lon,
        cell_lat
}
""".strip(),
    """
.create-or-alter function with (folder = "Map", skipvalidation = "true") ais_aton_points() {
    AidsToNavigationReportLatest
    | where isnotnull(Latitude) and isnotnull(Longitude)
    | where Latitude between (-89.999 .. 89.999)
    | where Longitude between (-179.999 .. 179.999)
    | extend
        aid_label = iff(
            isnotempty(trim(" ", strcat(tostring(Name), " ", tostring(NameExtension)))),
            trim(" ", strcat(tostring(Name), " ", tostring(NameExtension))),
            strcat("AtoN ", tostring(UserID))),
        aid_status = case(
            OffPosition == true and VirtualAtoN == true, "virtual off-position",
            OffPosition == true, "off-position",
            VirtualAtoN == true, "virtual",
            "physical"),
        aid_type = strcat("type ", tostring(AtoN)),
        age_min = datetime_diff('minute', now(), ___time),
        geometry = bag_pack("type", "Point", "coordinates", pack_array(todouble(Longitude), todouble(Latitude)))
    | project
        geometry,
        latitude = todouble(Latitude),
        longitude = todouble(Longitude),
        mmsi = tolong(UserID),
        aid_label,
        aid_status,
        aid_type,
        OffPosition,
        VirtualAtoN,
        AssignedMode,
        age_min,
        reported_at = ___time
}
""".strip(),
    """
.create-or-alter function with (folder = "Map", skipvalidation = "true") ais_base_station_points() {
    BaseStationReportLatest
    | where isnotnull(Latitude) and isnotnull(Longitude)
    | where Latitude between (-89.999 .. 89.999)
    | where Longitude between (-179.999 .. 179.999)
    | extend
        station_label = strcat("Base ", tostring(UserID)),
        station_role = iff(LongRangeEnable == true, "long-range enabled", "standard"),
        age_min = datetime_diff('minute', now(), ___time),
        geometry = bag_pack("type", "Point", "coordinates", pack_array(todouble(Longitude), todouble(Latitude)))
    | project
        geometry,
        latitude = todouble(Latitude),
        longitude = todouble(Longitude),
        mmsi = tolong(UserID),
        station_label,
        station_role,
        PositionAccuracy,
        Raim,
        age_min,
        reported_at = ___time
}
""".strip(),
    """
.create-or-alter function with (folder = "Map", skipvalidation = "true") ais_bbox() {
    union isfuzzy = true
        (ais_vessels_enriched(24h) | project latitude, longitude),
        (ais_aton_points() | project latitude, longitude),
        (ais_base_station_points() | project latitude, longitude)
    | summarize
        lat_p01 = percentile(latitude, 1),
        lat_p99 = percentile(latitude, 99),
        lon_p01 = percentile(longitude, 1),
        lon_p99 = percentile(longitude, 99),
        cnt = count()
}
""".strip(),
]


LABEL_BASE = {
    "enabled": False,
    "size": 11,
    "color": "#111111",
    "textStrokeColor": "#FFFFFF",
    "textStrokeWidth": 2,
    "allowOverlap": False,
}

SHIP_TYPE_PALETTE = {
    "cargo": "#2563EB",
    "tanker": "#DC2626",
    "passenger": "#8B5CF6",
    "fishing": "#059669",
    "tug": "#EA580C",
    "military": "#334155",
    "sailing": "#06B6D4",
    "pleasure": "#F59E0B",
    "fast craft": "#DB2777",
    "search and rescue": "#E11D48",
    "service": "#64748B",
    "other": "#6B7280",
    "unknown": "#94A3B8",
}

ATON_STATUS_PALETTE = {
    "physical": "#22C55E",
    "virtual": "#F59E0B",
    "off-position": "#DC2626",
    "virtual off-position": "#7F1D1D",
}

BASE_STATION_PALETTE = {
    "long-range enabled": "#7C3AED",
    "standard": "#475569",
}


def _series(column: str, palette: dict[str, str]) -> dict[str, Any]:
    return {
        "enableSeriesGroup": True,
        "seriesGroup": column,
        "customColors": dict(palette),
    }


def _color_match(column: str, palette: dict[str, str], fallback: str = "#94A3B8") -> list[Any]:
    expr: list[Any] = ["match", ["to-string", ["get", column]]]
    for value, color in palette.items():
        expr.extend([value, color])
    expr.append(fallback)
    return expr


def _icon_image_reference(layer_id: str, icon: str, fill_color: Any) -> Any:
    if not isinstance(fill_color, list) or len(fill_color) < 4 or fill_color[0] != "match":
        return f"{layer_id}:{icon}"

    expr: list[Any] = ["match", copy.deepcopy(fill_color[1])]
    pairs = fill_color[2:-1]
    fallback = fill_color[-1]

    if len(pairs) % 2 != 0 or not isinstance(fallback, str):
        return f"{layer_id}:{icon}"

    for idx in range(0, len(pairs), 2):
        value = copy.deepcopy(pairs[idx])
        color = pairs[idx + 1]
        if not isinstance(color, str):
            return f"{layer_id}:{icon}"
        expr.extend([value, f"{layer_id}:{icon}-{color}"])

    expr.append(f"{layer_id}:{icon}-{fallback}")
    return expr


def _interpolate(column: str, stops: list[tuple[float, str]]) -> list[Any]:
    expr: list[Any] = ["interpolate", ["linear"], ["get", column]]
    for value, color in stops:
        expr.extend([value, color])
    return expr


def _stable_uuid(*parts: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "https://fabric.microsoft.com/maps/aisstream/" + "/".join(parts)))


def _text_filter(layer_name: str, field_name: str, *, locked: bool = False) -> dict[str, Any]:
    return {
        "id": _stable_uuid("filter", layer_name, field_name),
        "type": "text",
        "field": field_name,
        "locked": locked,
        "value": [],
    }


def _number_filter(
    layer_name: str,
    field_name: str,
    *,
    minimum: float,
    maximum: float,
    locked: bool = False,
) -> dict[str, Any]:
    return {
        "id": _stable_uuid("filter", layer_name, field_name),
        "type": "number",
        "field": field_name,
        "locked": locked,
        "min": minimum,
        "max": maximum,
    }


def _vessel_filters(layer_name: str) -> list[dict[str, Any]]:
    return [
        _text_filter(layer_name, "ship_type_bucket"),
        _number_filter(layer_name, "length_m", minimum=0, maximum=500),
        _number_filter(layer_name, "speed_kn", minimum=0, maximum=80),
        _number_filter(layer_name, "age_min", minimum=0, maximum=20),
    ]


def bubble_options(
    *,
    visible: bool,
    radius: int,
    color: Any,
    stroke_color: Any,
    opacity: float = 0.9,
    min_zoom: float | None = None,
    max_zoom: float | None = None,
    tooltip_keys: list[str] | None = None,
    data_label_keys: list[str] | None = None,
    data_label_size: int = 11,
    allow_overlap: bool = False,
    series: dict[str, Any] | None = None,
) -> dict[str, Any]:
    opts: dict[str, Any] = {
        "type": "vector",
        "visible": visible,
        "pointLayerType": "bubble",
        "bubbleOptions": {
            "color": color,
            "radius": radius,
            "opacity": opacity,
            "strokeWidth": 1,
            "strokeColor": stroke_color,
        },
        "tooltipKeys": tooltip_keys or [],
        "enablePopups": True,
    }
    if series:
        opts["bubbleOptions"].update(series)
    if data_label_keys:
        label_opts = dict(LABEL_BASE)
        label_opts.update({"enabled": True, "size": data_label_size, "allowOverlap": allow_overlap})
        opts["dataLabelKeys"] = data_label_keys
        opts["dataLabelOptions"] = label_opts
    if min_zoom is not None:
        opts["minZoom"] = min_zoom
    if max_zoom is not None:
        opts["maxZoom"] = max_zoom
    return opts


def symbol_options(
    *,
    visible: bool,
    size: int,
    icon: str,
    color: Any,
    stroke_color: Any,
    opacity: float = 0.9,
    min_zoom: float | None = None,
    max_zoom: float | None = None,
    tooltip_keys: list[str] | None = None,
    series: dict[str, Any] | None = None,
) -> dict[str, Any]:
    bubble_style = {
        "color": color,
        "radius": 5,
        "opacity": opacity,
        "strokeWidth": 1,
        "strokeColor": stroke_color,
    }
    marker_style: dict[str, Any] = {
        "icon": icon,
        "fillColor": color,
        "strokeColor": stroke_color,
        "strokeWidth": 1,
        "size": size,
    }
    if series:
        bubble_style.update(series)
        for key in ("enableSeriesGroup", "seriesGroup"):
            if key in series:
                marker_style[key] = series[key]
    opts: dict[str, Any] = {
        "type": "vector",
        "visible": visible,
        "pointLayerType": "marker",
        "bubbleOptions": bubble_style,
        "markerOptions": marker_style,
        "tooltipKeys": tooltip_keys or [],
        "enablePopups": True,
    }
    if min_zoom is not None:
        opts["minZoom"] = min_zoom
    if max_zoom is not None:
        opts["maxZoom"] = max_zoom
    return opts


def polygon_options(
    *,
    visible: bool,
    fill_color: Any,
    stroke_color: Any,
    fill_opacity: float = 0.8,
    stroke_width: int = 1,
    min_zoom: float | None = None,
    max_zoom: float | None = None,
    tooltip_keys: list[str] | None = None,
    data_label_keys: list[str] | None = None,
    data_label_size: int = 11,
    allow_overlap: bool = False,
    series: dict[str, Any] | None = None,
) -> dict[str, Any]:
    opts: dict[str, Any] = {
        "type": "vector",
        "visible": visible,
        "polygonOptions": {
            "fillColor": fill_color,
            "fillOpacity": fill_opacity,
        },
        "lineOptions": {
            "strokeColor": stroke_color,
            "strokeWidth": stroke_width,
            "strokeOpacity": 0.9,
        },
        "tooltipKeys": tooltip_keys or [],
        "enablePopups": True,
    }
    if series:
        opts["polygonOptions"].update(series)
    if data_label_keys:
        label_opts = dict(LABEL_BASE)
        label_opts.update({"enabled": True, "size": data_label_size, "allowOverlap": allow_overlap})
        opts["dataLabelKeys"] = data_label_keys
        opts["dataLabelOptions"] = label_opts
    if min_zoom is not None:
        opts["minZoom"] = min_zoom
    if max_zoom is not None:
        opts["maxZoom"] = max_zoom
    return opts


@dataclass(frozen=True)
class Layer:
    name: str
    kql: str
    options: dict[str, Any]
    refresh_interval_ms: int = 60000
    filters: list[dict[str, Any]] = field(default_factory=list)
    marker_icon: str | None = None


def _layers() -> list[Layer]:
    vessel_series = _series("ship_type_bucket", SHIP_TYPE_PALETTE)
    aton_series = _series("aid_status", ATON_STATUS_PALETTE)
    station_series = _series("station_role", BASE_STATION_PALETTE)

    return [
        Layer(
            name="aisstream vessel density",
            kql="ais_vessel_density_grid(90m, 1.0)",
            options=polygon_options(
                visible=True,
                fill_color=_interpolate(
                    "vessel_count",
                    [
                        (1, "#D6ECFF"),
                        (10, "#8BC5FF"),
                        (50, "#3B82F6"),
                        (200, "#1D4ED8"),
                        (800, "#0F172A"),
                    ],
                ),
                stroke_color="#1D4ED8",
                fill_opacity=0.65,
                stroke_width=1,
                max_zoom=8.5,
                tooltip_keys=[
                    "label",
                    "vessel_count",
                    "cargo_count",
                    "tanker_count",
                    "passenger_count",
                    "avg_speed_kn",
                    "newest_age_min",
                ],
            ),
            refresh_interval_ms=120000,
        ),
        Layer(
            name="aisstream live vessels",
            kql=(
                "ais_vessels_enriched(60m) "
                "| where age_min <= 20 "
                "| extend speed_kn = sog "
                "| order by reported_at desc "
                "| take 20000"
            ),
            options=symbol_options(
                visible=True,
                size=18,
                icon="VehicleShip",
                color=_color_match("ship_type_bucket", SHIP_TYPE_PALETTE, "#64748B"),
                stroke_color="#FFFFFF",
                min_zoom=4.5,
                max_zoom=11.5,
                tooltip_keys=[
                    "vessel_label",
                    "mmsi",
                    "position_source",
                    "ship_type_bucket",
                    "destination",
                    "speed_kn",
                    "cog",
                    "heading",
                    "length_m",
                    "beam_m",
                    "age_min",
                ],
                series=vessel_series,
            ),
            refresh_interval_ms=45000,
            filters=_vessel_filters("aisstream live vessels"),
            marker_icon="VehicleShip",
        ),
        Layer(
            name="aisstream vessel footprints",
            kql=(
                "ais_vessel_rectangles(60m) "
                "| where age_min <= 20 "
                "| extend speed_kn = sog "
                "| order by reported_at desc "
                "| take 4000"
            ),
            options=polygon_options(
                visible=True,
                fill_color=_color_match("ship_type_bucket", SHIP_TYPE_PALETTE, "#64748B"),
                stroke_color="#FFFFFF",
                fill_opacity=0.82,
                stroke_width=1,
                min_zoom=11.5,
                tooltip_keys=[
                    "vessel_label",
                    "mmsi",
                    "position_source",
                    "ship_type_bucket",
                    "destination",
                    "speed_kn",
                    "heading_label",
                    "length_m",
                    "beam_m",
                    "age_min",
                ],
                series=vessel_series,
            ),
            refresh_interval_ms=45000,
            filters=_vessel_filters("aisstream vessel footprints"),
        ),
        Layer(
            name="aisstream feed freshness",
            kql="ais_feed_freshness_grid(3h, 1.0)",
            options=polygon_options(
                visible=False,
                fill_color=_interpolate(
                    "max_age_min",
                    [
                        (0, "#10B981"),
                        (15, "#84CC16"),
                        (45, "#F59E0B"),
                        (120, "#DC2626"),
                        (360, "#7F1D1D"),
                    ],
                ),
                stroke_color="#475569",
                fill_opacity=0.55,
                stroke_width=1,
                tooltip_keys=[
                    "label",
                    "vessel_count",
                    "avg_age_min",
                    "min_age_min",
                    "max_age_min",
                    "newest_report",
                ],
            ),
            refresh_interval_ms=90000,
        ),
        Layer(
            name="aisstream aids to navigation",
            kql="ais_aton_points()",
            options=bubble_options(
                visible=True,
                radius=5,
                color=_color_match("aid_status", ATON_STATUS_PALETTE, "#64748B"),
                stroke_color="#FFFFFF",
                min_zoom=6.5,
                tooltip_keys=[
                    "aid_label",
                    "mmsi",
                    "aid_status",
                    "aid_type",
                    "AssignedMode",
                    "age_min",
                ],
                data_label_keys=["aid_label"],
                data_label_size=10,
                allow_overlap=False,
                series=aton_series,
            ),
            refresh_interval_ms=300000,
        ),
        Layer(
            name="aisstream base stations",
            kql="ais_base_station_points()",
            options=bubble_options(
                visible=False,
                radius=5,
                color=_color_match("station_role", BASE_STATION_PALETTE, "#64748B"),
                stroke_color="#FFFFFF",
                min_zoom=3.0,
                tooltip_keys=[
                    "station_label",
                    "mmsi",
                    "station_role",
                    "PositionAccuracy",
                    "Raim",
                    "age_min",
                ],
                data_label_keys=["station_label"],
                data_label_size=10,
                allow_overlap=False,
                series=station_series,
            ),
            refresh_interval_ms=300000,
        ),
    ]


def _b64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def _get_definition(
    fabric: requests.Session,
    api_base: str,
    workspace_id: str,
    map_id: str,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    result = _poll_lro(
        fabric,
        fabric.post(f"{api_base}/workspaces/{workspace_id}/items/{map_id}/getDefinition"),
    )
    parts = {part["path"]: part for part in result["definition"]["parts"]}
    if "map.json" not in parts:
        raise RuntimeError("Map definition has no map.json part")
    mp = json.loads(base64.b64decode(parts["map.json"]["payload"]).decode("utf-8"))
    mp.setdefault("dataSources", [])
    mp.setdefault("iconSources", [])
    mp.setdefault("layerSources", [])
    mp.setdefault("layerSettings", [])
    if "$schema" not in mp:
        mp["$schema"] = (
            "https://developer.microsoft.com/json-schemas/fabric/item/map/"
            "definition/2.0.0/schema.json"
        )
    return mp, parts


def _put_definition(
    fabric: requests.Session,
    api_base: str,
    workspace_id: str,
    map_id: str,
    mp: dict[str, Any],
    parts: dict[str, dict[str, Any]],
) -> None:
    parts["map.json"] = {
        "path": "map.json",
        "payload": _b64(json.dumps(mp, indent=2)),
        "payloadType": "InlineBase64",
    }
    response = fabric.post(
        f"{api_base}/workspaces/{workspace_id}/items/{map_id}/updateDefinition",
        json={"definition": {"parts": list(parts.values())}},
    )
    print(f"updateDefinition HTTP {response.status_code}")
    _poll_lro(fabric, response)


def _bbox(
    kusto: requests.Session,
    kusto_uri: str,
    kusto_db: str,
) -> Optional[tuple[float, float, float, float, int]]:
    try:
        frame = _kql_query(kusto, kusto_uri, kusto_db, "ais_bbox()")
    except Exception as exc:
        print(f"  bbox lookup failed: {exc}")
        return None
    if not frame or not frame.get("Rows"):
        return None
    columns = [col["ColumnName"] for col in frame["Columns"]]
    rec = dict(zip(columns, frame["Rows"][0]))
    if rec.get("cnt", 0) == 0:
        return None
    return (
        float(rec["lat_p01"]),
        float(rec["lat_p99"]),
        float(rec["lon_p01"]),
        float(rec["lon_p99"]),
        int(rec["cnt"]),
    )


def _zoom_for_extent(lat_span: float, lon_span: float) -> float:
    span = max(lat_span, lon_span / 1.7)
    if span >= 120:
        return 1.6
    if span >= 70:
        return 2.0
    if span >= 35:
        return 3.0
    if span >= 18:
        return 4.2
    if span >= 8:
        return 5.4
    if span >= 4:
        return 6.6
    if span >= 2:
        return 7.8
    if span >= 1:
        return 9.0
    if span >= 0.5:
        return 10.2
    return 11.5


def _set_basemap(mp: dict[str, Any], bbox: Optional[tuple[float, float, float, float, int]]) -> None:
    if bbox is None:
        center = [0.0, 20.0]
        zoom = 1.8
    else:
        lat_p01, lat_p99, lon_p01, lon_p99, _ = bbox
        center = [(lon_p01 + lon_p99) / 2.0, (lat_p01 + lat_p99) / 2.0]
        zoom = _zoom_for_extent(lat_p99 - lat_p01, lon_p99 - lon_p01)

    mp["basemap"] = {
        "options": {
            "center": center,
            "zoom": zoom,
            "style": "road_shaded_relief",
            "showLabels": True,
            "language": "en-US",
        },
        "controls": {
            "zoom": True,
            "pitch": True,
            "compass": True,
            "scale": True,
            "traffic": False,
            "style": True,
        },
        "backgroundColor": "#F8FAFC",
        "theme": "light",
    }
    print(f"  basemap center={center} zoom={zoom}")


def _prune_existing_ais_layers(mp: dict[str, Any], parts: dict[str, dict[str, Any]]) -> None:
    removable_layers = [
        layer for layer in mp["layerSettings"]
        if str(layer.get("name", "")).startswith("aisstream ")
    ]
    removable_source_ids = {layer.get("sourceId") for layer in removable_layers if layer.get("sourceId")}
    removable_source_ids.update(
        source["id"]
        for source in mp["layerSources"]
        if str(source.get("name", "")).startswith("aisstream ")
    )

    if removable_source_ids:
        for source_id in removable_source_ids:
            parts.pop(f"queries/layerSource-{source_id}.kql", None)

    mp["layerSettings"] = [
        layer for layer in mp["layerSettings"]
        if not str(layer.get("name", "")).startswith("aisstream ")
    ]
    mp["layerSources"] = [
        source for source in mp["layerSources"]
        if source.get("id") not in removable_source_ids
        and not str(source.get("name", "")).startswith("aisstream ")
    ]


def wire(
    *,
    workspace_id: str,
    map_id: str,
    map_name: str,
    kql_db_id: str,
    kql_db_name: str,
    kusto_uri: str,
) -> None:
    fabric_token = _get_token("FABRIC_TOKEN", "https://api.fabric.microsoft.com/.default")
    kusto_token = _get_token(
        "KUSTO_TOKEN",
        [
            "https://kusto.kusto.windows.net/.default",
            f"{kusto_uri.rstrip('/')}/.default",
        ],
    )
    fabric = _session(fabric_token)
    kusto = _session(kusto_token)
    api_base = "https://api.fabric.microsoft.com/v1"

    print(f"Installing helper KQL functions into {kql_db_name}")
    for statement in AIS_FUNCTIONS:
        header = statement.splitlines()[0].strip()
        print(f"  {header}")
        _kql_mgmt(kusto, kusto_uri, kql_db_name, statement)

    print("Discovering map bounding box from ais_bbox()")
    bbox = _bbox(kusto, kusto_uri, kql_db_name)
    if bbox is None:
        print("  bbox unavailable - using global fallback")
    else:
        lat_p01, lat_p99, lon_p01, lon_p99, n = bbox
        print(
            "  bbox rows={0} lat={1:.3f}..{2:.3f} lon={3:.3f}..{4:.3f}".format(
                n, lat_p01, lat_p99, lon_p01, lon_p99
            )
        )

    validated_layers: list[tuple[Layer, int]] = []
    for layer in _layers():
        print(f"  layer {layer.name}")
        frame = _kql_query(kusto, kusto_uri, kql_db_name, f"{layer.kql}\n| count")
        row_count = frame["Rows"][0][0] if frame and frame.get("Rows") else 0
        print(f"    rows: {row_count}")
        validated_layers.append((layer, row_count))

    if len(validated_layers) != len(_layers()):
        raise RuntimeError("Layer validation did not cover every aisstream layer.")

    mp, parts = _get_definition(fabric, api_base, workspace_id, map_id)
    print(f"Fetched Fabric Map '{map_name}' ({map_id})")

    if not any(
        source.get("itemType") == "KqlDatabase"
        and source.get("workspaceId") == workspace_id
        and source.get("itemId") == kql_db_id
        for source in mp["dataSources"]
    ):
        mp["dataSources"].append(
            {
                "itemType": "KqlDatabase",
                "workspaceId": workspace_id,
                "itemId": kql_db_id,
            }
        )

    _set_basemap(mp, bbox)
    _prune_existing_ais_layers(mp, parts)

    added = 0
    for layer, _row_count in validated_layers:
        print(f"  wiring {layer.name}")

        source_id = str(uuid.uuid4())
        layer_id = str(uuid.uuid4())
        layer_options = copy.deepcopy(layer.options)
        if layer.marker_icon:
            marker_options = layer_options.setdefault("markerOptions", {})
            marker_options.setdefault("icon", layer.marker_icon)
            marker_options.setdefault("iconOptions", {})["image"] = _icon_image_reference(
                layer_id,
                layer.marker_icon,
                marker_options.get("fillColor"),
            )
        mp["layerSources"].append(
            {
                "id": source_id,
                "name": f"{layer.name}_source",
                "type": "kusto",
                "options": {"cluster": False},
                "itemId": kql_db_id,
                "refreshIntervalMs": layer.refresh_interval_ms,
            }
        )
        mp["layerSettings"].append(
            {
                "id": layer_id,
                "name": layer.name,
                "sourceId": source_id,
                "geometryColumnName": "geometry",
                "filters": layer.filters,
                "options": layer_options,
            }
        )
        parts[f"queries/layerSource-{source_id}.kql"] = {
            "path": f"queries/layerSource-{source_id}.kql",
            "payload": _b64(layer.kql),
            "payloadType": "InlineBase64",
        }
        added += 1

    _put_definition(fabric, api_base, workspace_id, map_id, mp, parts)
    print(f"OK - map {map_id} updated with {added} aisstream layers")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--workspace-id", default=os.environ.get("FABRIC_WORKSPACE_ID"))
    parser.add_argument("--map-id", default=os.environ.get("FABRIC_MAP_ID"))
    parser.add_argument("--map-name", default=os.environ.get("FABRIC_MAP_NAME", "aisstream-live-map"))
    parser.add_argument("--kql-db-id", default=os.environ.get("FABRIC_KQL_DB_ID"))
    parser.add_argument("--kql-db-name", default=os.environ.get("FABRIC_KQL_DB_NAME", "aisstream"))
    parser.add_argument("--kusto-uri", default=os.environ.get("KUSTO_CLUSTER_URI"))
    args = parser.parse_args(argv)

    required = {
        "workspace-id": args.workspace_id,
        "map-id": args.map_id,
        "kql-db-id": args.kql_db_id,
        "kql-db-name": args.kql_db_name,
        "kusto-uri": args.kusto_uri,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        parser.error("missing required arguments: " + ", ".join(missing))

    wire(
        workspace_id=args.workspace_id,
        map_id=args.map_id,
        map_name=args.map_name,
        kql_db_id=args.kql_db_id,
        kql_db_name=args.kql_db_name,
        kusto_uri=args.kusto_uri,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
