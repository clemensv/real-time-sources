"""Create or refresh a Fabric Map for the gbfs-bikeshare feeder.

The map is tuned for live shared-micromobility situational awareness and adds
three KQL-backed layers:

1. Station availability - bubbles coloured by station fill ratio
2. Free bikes          - dockless-bike points with reservation / disablement state
3. Station labels      - station-name labels for close-in inspection
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


USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-gbfs-bikeshare/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)


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
    session.headers["User-Agent"] = USER_AGENT
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


GBFS_FUNCTIONS = [
    """
.create-or-alter function with (folder = "Map", skipvalidation = "true") gbfs_station_availability() {
    StationInformationLatest
    | where isnotnull(lat) and isnotnull(lon)
    | where lat between (-89.999 .. 89.999)
    | where lon between (-179.999 .. 179.999)
    | project
        system_id,
        station_id,
        station_name = iff(isnotempty(name), name, station_id),
        short_name,
        lat = todouble(lat),
        lon = todouble(lon),
        capacity = toint(capacity),
        address
    | join kind = leftouter (
        StationStatusLatest
        | project
            system_id,
            station_id,
            num_bikes_available = toint(num_bikes_available),
            num_docks_available = toint(num_docks_available),
            num_ebikes_available = toint(num_ebikes_available),
            is_installed,
            is_renting,
            is_returning,
            last_reported,
            status_observed_at = ___time
    ) on system_id, station_id
    | extend
        bikes_available = toint(coalesce(num_bikes_available, 0)),
        docks_available = toint(coalesce(num_docks_available, 0)),
        fill_ratio = iff(isnotnull(capacity) and capacity > 0, todouble(bikes_available) / todouble(capacity), real(null)),
        fill_percent = iff(isnull(fill_ratio), real(null), round(fill_ratio * 100.0, 1)),
        fill_bucket = case(
            isnull(fill_ratio), "unknown",
            fill_ratio < 0.2, "empty",
            fill_ratio < 0.4, "low",
            fill_ratio < 0.7, "balanced",
            fill_ratio < 0.9, "high",
            "full"),
        availability_label = strcat(tostring(bikes_available), " bikes / ", tostring(docks_available), " docks"),
        last_reported_utc = iff(isnull(last_reported), "", format_datetime(unixtime_seconds_todatetime(tolong(last_reported)), "yyyy-MM-dd HH:mm:ss'Z'")),
        geometry = bag_pack("type", "Point", "coordinates", pack_array(lon, lat))
    | project
        geometry,
        system_id,
        station_id,
        station_name,
        short_name,
        lat,
        lon,
        capacity,
        address,
        bikes_available,
        docks_available,
        num_ebikes_available,
        fill_ratio,
        fill_percent,
        fill_bucket,
        availability_label,
        is_installed,
        is_renting,
        is_returning,
        last_reported,
        last_reported_utc,
        status_observed_at
}
""".strip(),
    """
.create-or-alter function with (folder = "Map", skipvalidation = "true") gbfs_free_bikes() {
    FreeBikeStatusLatest
    | where isnotnull(lat) and isnotnull(lon)
    | where lat between (-89.999 .. 89.999)
    | where lon between (-179.999 .. 179.999)
    | extend
        bike_status = case(
            is_disabled == true, "disabled",
            is_reserved == true, "reserved",
            "available"),
        range_km = iff(isnull(current_range_meters), real(null), round(todouble(current_range_meters) / 1000.0, 1)),
        last_reported_utc = iff(isnull(last_reported), "", format_datetime(unixtime_seconds_todatetime(tolong(last_reported)), "yyyy-MM-dd HH:mm:ss'Z'")),
        geometry = bag_pack("type", "Point", "coordinates", pack_array(todouble(lon), todouble(lat)))
    | project
        geometry,
        system_id,
        bike_id,
        lat = todouble(lat),
        lon = todouble(lon),
        bike_status,
        is_reserved,
        is_disabled,
        vehicle_type_id,
        current_range_meters = todouble(current_range_meters),
        range_km,
        last_reported,
        last_reported_utc,
        observed_at = ___time
}
""".strip(),
    """
.create-or-alter function with (folder = "Map", skipvalidation = "true") gbfs_bbox() {
    union isfuzzy = true
        (gbfs_station_availability() | project latitude = lat, longitude = lon),
        (gbfs_free_bikes() | project latitude = lat, longitude = lon)
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
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "https://fabric.microsoft.com/maps/gbfs-bikeshare/" + "/".join(parts)))


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
    return [
        Layer(
            name="gbfs station availability",
            kql="gbfs_station_availability()",
            options=bubble_options(
                visible=True,
                radius=8,
                color=_interpolate(
                    "fill_ratio",
                    [
                        (0.0, "#DC2626"),
                        (0.25, "#F97316"),
                        (0.5, "#EAB308"),
                        (0.75, "#22C55E"),
                        (1.0, "#15803D"),
                    ],
                ),
                stroke_color="#FFFFFF",
                min_zoom=2.0,
                tooltip_keys=[
                    "station_name",
                    "bikes_available",
                    "docks_available",
                    "capacity",
                    "fill_percent",
                    "availability_label",
                    "address",
                    "last_reported_utc",
                ],
            ),
            refresh_interval_ms=60000,
            filters=[
                _text_filter("gbfs station availability", "system_id"),
                _text_filter("gbfs station availability", "fill_bucket"),
                _number_filter("gbfs station availability", "fill_percent", minimum=0, maximum=100),
            ],
        ),
        Layer(
            name="gbfs free bikes",
            kql="gbfs_free_bikes()",
            options=bubble_options(
                visible=True,
                radius=4,
                color="#16A34A",
                stroke_color="#DCFCE7",
                min_zoom=5.0,
                tooltip_keys=[
                    "bike_id",
                    "bike_status",
                    "vehicle_type_id",
                    "range_km",
                    "last_reported_utc",
                ],
            ),
            refresh_interval_ms=60000,
        ),
        Layer(
            name="gbfs station labels",
            kql="gbfs_station_availability()",
            options=bubble_options(
                visible=True,
                radius=2,
                color="#000000",
                stroke_color="#000000",
                opacity=0.0,
                min_zoom=13.0,
                tooltip_keys=["station_name", "availability_label"],
                data_label_keys=["station_name"],
                data_label_size=11,
                allow_overlap=False,
            ),
            refresh_interval_ms=60000,
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


def _set_basemap(mp: dict[str, Any]) -> None:
    mp["basemap"] = {
        "options": {
            "center": [0.0, 30.0],
            "zoom": 2.0,
            "style": "road",
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
        "backgroundColor": "#FFFFFF",
        "theme": "light",
    }
    print("  basemap center=[0.0, 30.0] zoom=2.0")


def _prune_existing_gbfs_layers(mp: dict[str, Any], parts: dict[str, dict[str, Any]]) -> None:
    removable_layers = [
        layer for layer in mp["layerSettings"]
        if str(layer.get("name", "")).startswith("gbfs ")
    ]
    removable_source_ids = {layer.get("sourceId") for layer in removable_layers if layer.get("sourceId")}
    removable_source_ids.update(
        source["id"]
        for source in mp["layerSources"]
        if str(source.get("name", "")).startswith("gbfs ")
    )

    if removable_source_ids:
        for source_id in removable_source_ids:
            parts.pop(f"queries/layerSource-{source_id}.kql", None)

    mp["layerSettings"] = [
        layer for layer in mp["layerSettings"]
        if not str(layer.get("name", "")).startswith("gbfs ")
    ]
    mp["layerSources"] = [
        source for source in mp["layerSources"]
        if source.get("id") not in removable_source_ids
        and not str(source.get("name", "")).startswith("gbfs ")
    ]


def _ensure_map(
    fabric: requests.Session,
    api_base: str,
    workspace_id: str,
    map_id: str | None,
    map_name: str,
) -> str:
    if map_id:
        return map_id

    response = fabric.get(f"{api_base}/workspaces/{workspace_id}/items?type=Map")
    response.raise_for_status()
    items = response.json()
    if items.get("value"):
        match = next((item for item in items["value"] if item.get("displayName") == map_name), None)
        if match and match.get("id"):
            print(f"Reusing existing Fabric Map '{map_name}' ({match['id']})")
            return str(match["id"])

    print(f"Creating Fabric Map '{map_name}'")
    create_response = fabric.post(
        f"{api_base}/workspaces/{workspace_id}/items",
        json={"displayName": map_name, "type": "Map"},
    )
    _poll_lro(fabric, create_response)

    for _ in range(30):
        time.sleep(2)
        list_response = fabric.get(f"{api_base}/workspaces/{workspace_id}/items?type=Map")
        list_response.raise_for_status()
        match = next(
            (item for item in list_response.json().get("value", []) if item.get("displayName") == map_name),
            None,
        )
        if match and match.get("id"):
            print(f"Created Fabric Map '{map_name}' ({match['id']})")
            return str(match["id"])

    raise RuntimeError(f"Fabric Map creation for '{map_name}' did not surface an item id after 60 seconds.")


def wire(
    *,
    workspace_id: str,
    map_id: str | None,
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
    for statement in GBFS_FUNCTIONS:
        header = statement.splitlines()[0].strip()
        print(f"  {header}")
        _kql_mgmt(kusto, kusto_uri, kql_db_name, statement)

    validated_layers: list[tuple[Layer, int]] = []
    layers = _layers()
    for layer in layers:
        print(f"  layer {layer.name}")
        frame = _kql_query(kusto, kusto_uri, kql_db_name, f"{layer.kql}\n| count")
        row_count = frame["Rows"][0][0] if frame and frame.get("Rows") else 0
        print(f"    rows: {row_count}")
        validated_layers.append((layer, row_count))

    if len(validated_layers) != len(layers):
        raise RuntimeError("Layer validation did not cover every gbfs layer.")

    resolved_map_id = _ensure_map(fabric, api_base, workspace_id, map_id, map_name)
    mp, parts = _get_definition(fabric, api_base, workspace_id, resolved_map_id)
    print(f"Fetched Fabric Map '{map_name}' ({resolved_map_id})")

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

    _set_basemap(mp)
    _prune_existing_gbfs_layers(mp, parts)

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
        layer_setting = {
            "id": layer_id,
            "name": layer.name,
            "sourceId": source_id,
            "geometryColumnName": "geometry",
            "filters": layer.filters,
            "options": layer_options,
        }
        mp["layerSettings"].append(layer_setting)
        parts[f"queries/layerSource-{source_id}.kql"] = {
            "path": f"queries/layerSource-{source_id}.kql",
            "payload": _b64(layer.kql),
            "payloadType": "InlineBase64",
        }
        added += 1

    _put_definition(fabric, api_base, workspace_id, resolved_map_id, mp, parts)
    print(f"OK - map {resolved_map_id} updated with {added} gbfs layers")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--workspace-id", default=os.environ.get("FABRIC_WORKSPACE_ID"))
    parser.add_argument("--map-id", default=os.environ.get("FABRIC_MAP_ID"))
    parser.add_argument("--map-name", default=os.environ.get("FABRIC_MAP_NAME", "gbfs-bikeshare-map"))
    parser.add_argument("--kql-db-id", default=os.environ.get("FABRIC_KQL_DB_ID"))
    parser.add_argument("--kql-db-name", default=os.environ.get("FABRIC_KQL_DB_NAME", "gbfs-bikeshare"))
    parser.add_argument("--kusto-uri", default=os.environ.get("KUSTO_CLUSTER_URI"))
    args = parser.parse_args(argv)

    required = {
        "workspace-id": args.workspace_id,
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
