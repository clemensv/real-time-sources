"""Create or update the ICON-D2 Fabric Map item that visualises the 8 most
useful single-level forecast parameters as Kusto-backed vector layers.

Layers (all sourced from the ``IconD2Points`` table in the dwd KQL database):

  * t_2m     - 2 m air temperature   (default-on)
  * tot_prec - total precipitation
  * vmax_10m - 10 m wind gust
  * clct     - total cloud cover
  * cape_ml  - mixed-layer CAPE
  * dbz_cmax - simulated max radar reflectivity
  * pmsl     - mean sea-level pressure
  * h_snow   - snow depth

Each layer always renders the **latest** ICON-D2 run available for its
parameter, computed dynamically via
``toscalar(IconD2Points | where parameter == "X" | summarize max(run))`` so the
map auto-refreshes as the bridge ingests new model runs.

A per-layer single-select filter on ``Forecast time (UTC)`` (label-formatted)
lets the user pick which lead-hour to display.

The script is idempotent: re-running drops the 8 layers it manages (matched by
name) and re-creates them with current colour ramps / default filter values.
The Fabric Map item itself must already exist - this script does *not* create
it from scratch (item creation goes through ``setup.ps1`` or the Fabric UI).

Inputs (env vars or CLI args):

  FABRIC_WORKSPACE_ID   - GUID of the Fabric workspace containing the map
  FABRIC_MAP_ID         - GUID of the Fabric Map item to patch
  FABRIC_KQL_DB_ID      - GUID of the KQL database with IconD2Points
  KUSTO_CLUSTER_URI     - https://<cluster>.kusto.fabric.microsoft.com
  KUSTO_DB              - KQL database name (default: dwd)
  FABRIC_TOKEN          - bearer token for the Fabric REST API
                          (https://api.fabric.microsoft.com/.default)
  KUSTO_TOKEN           - bearer token for the Kusto cluster
                          (https://kusto.fabric.microsoft.com/.default)
  FABRIC_API_BASE       - override (default: https://api.fabric.microsoft.com/v1)

If FABRIC_TOKEN / KUSTO_TOKEN are not set, the script falls back to
``azure.identity.DefaultAzureCredential`` to acquire them.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import uuid
from typing import Optional

import requests

# (display name, parameter, unit, label_suffix, label_decimals, color_ramp_stops)
LAYERS = [
    ("ICON-D2 2 m temperature",          "t_2m",    "degC", " degC", 1,
     [-20, "#08306b", -10, "#2171b5", 0, "#6baed6", 5, "#c6dbef",
      10, "#fdae61", 20, "#f46d43", 30, "#a50026"]),
    ("ICON-D2 total precipitation",      "tot_prec", "mm",  " mm",   1,
     [0, "#ffffff", 0.5, "#deebf7", 2, "#9ecae1", 5, "#4292c6",
      10, "#08519c", 25, "#54278f", 50, "#3f007d"]),
    ("ICON-D2 10 m wind gust",           "vmax_10m", "m/s", " m/s",  1,
     [0, "#ffffcc", 5, "#a1dab4", 10, "#41b6c4", 15, "#2c7fb8",
      20, "#253494", 30, "#7a0177"]),
    ("ICON-D2 total cloud cover",        "clct",     "%",   "%",     0,
     [0, "#08306b", 20, "#2171b5", 40, "#6baed6", 60, "#c6dbef",
      80, "#f7fbff", 100, "#ffffff"]),
    ("ICON-D2 CAPE (ML)",                "cape_ml",  "J/kg", " J/kg", 0,
     [0, "#ffffff", 250, "#fee391", 500, "#fec44f", 1000, "#fe9929",
      1500, "#ec7014", 2500, "#cc4c02", 4000, "#8c2d04"]),
    ("ICON-D2 simulated max radar refl.", "dbz_cmax", "dBZ", " dBZ", 0,
     [0, "#ffffff", 10, "#5bd1ff", 20, "#1eaaff", 30, "#00ff00",
      40, "#ffe600", 50, "#ff7a00", 60, "#ff0000", 70, "#9b1de1"]),
    ("ICON-D2 mean sea-level pressure",  "pmsl",     "hPa", " hPa",  1,
     [970, "#4575b4", 990, "#abd9e9", 1005, "#ffffbf",
      1015, "#fdae61", 1030, "#d73027"]),
    ("ICON-D2 snow depth",               "h_snow",   "m",   " m",    2,
     [0, "#ffffff", 0.05, "#deebf7", 0.2, "#9ecae1", 0.5, "#4292c6",
      1.0, "#08519c", 2.0, "#08306b"]),
]

LAYER_NAMES = {name for name, *_ in LAYERS}
DEFAULT_VISIBLE = "t_2m"

KQL_TEMPLATE = r"""let RES = 0.1;
let HALF = RES / 2.0;
let LatestRun = toscalar(IconD2Points | where parameter == "{PARAM}" | summarize max(run));
IconD2Points
| where parameter == "{PARAM}" and run == LatestRun
| extend valid_time = datetime_add('hour', toint(lead_hour), run)
| extend ['Forecast time (UTC)'] = strcat(format_datetime(valid_time, 'yyyy-MM-dd HH:mm'), ' UTC')
| extend label = strcat(tostring(round(value, {DEC})), '{SUF}')
| extend geometry = bag_pack(
    "type", "Polygon",
    "coordinates", pack_array(pack_array(
        pack_array(lon - HALF, lat - HALF),
        pack_array(lon + HALF, lat - HALF),
        pack_array(lon + HALF, lat + HALF),
        pack_array(lon - HALF, lat + HALF),
        pack_array(lon - HALF, lat - HALF))))
| project geometry, value, ['Forecast time (UTC)'], valid_time, label
"""


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


def _poll_lro(session: requests.Session, response: requests.Response):
    """Poll a Fabric long-running-operation to completion; return the result."""
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
            raise RuntimeError(f"LRO failed: {json.dumps(status)[:400]}")
        time.sleep(2)


def _latest_first_hour(kusto_uri: str, kusto_db: str, kusto_session: requests.Session,
                       param: str) -> Optional[str]:
    """Look up the first-hour label string for the latest run of ``param``."""
    q = (
        f'IconD2Points | where parameter == "{param}" '
        f'| summarize r = max(run) '
        f'| extend t = datetime_add("hour", 0, r) '
        f'| project strcat(format_datetime(t, "yyyy-MM-dd HH:mm"), " UTC")'
    )
    r = kusto_session.post(
        f"{kusto_uri.rstrip('/')}/v2/rest/query",
        json={"db": kusto_db, "csl": q},
    )
    if r.status_code != 200:
        return None
    for frame in r.json():
        if (frame.get("FrameType") == "DataTable"
                and frame.get("TableKind") == "PrimaryResult"):
            rows = frame.get("Rows") or []
            if rows and rows[0]:
                return rows[0][0]
    return None


def wire(workspace_id: str, map_id: str, kql_db_id: str,
         kusto_uri: str, kusto_db: str,
         fabric_token: str, kusto_token: str,
         api_base: str = "https://api.fabric.microsoft.com/v1") -> None:

    fab = requests.Session()
    fab.headers["Authorization"] = f"Bearer {fabric_token}"
    fab.headers["Content-Type"]  = "application/json"
    ks = requests.Session()
    ks.headers["Authorization"] = f"Bearer {kusto_token}"
    ks.headers["Content-Type"]  = "application/json"

    # 1. Fetch current map definition.
    res = _poll_lro(fab, fab.post(
        f"{api_base}/workspaces/{workspace_id}/items/{map_id}/getDefinition"))
    parts = {p["path"]: p for p in res["definition"]["parts"]}
    mp = json.loads(base64.b64decode(parts["map.json"]["payload"]))

    # 2. Drop any previously-wired ICON-D2 layers (by name) so this is idempotent.
    removed_src_ids = set()
    kept_settings = []
    for ls in mp.get("layerSettings", []):
        if ls["name"] in LAYER_NAMES:
            removed_src_ids.add(ls.get("sourceId"))
        else:
            kept_settings.append(ls)
    mp["layerSettings"] = kept_settings
    mp["layerSources"] = [s for s in mp.get("layerSources", [])
                          if s["id"] not in removed_src_ids]
    for p in list(parts):
        if p.startswith("queries/layerSource-"):
            sid = p.split("layerSource-")[1].split(".kql")[0]
            if sid in removed_src_ids:
                del parts[p]

    # 3. Ensure the KQL database is registered as a data source.
    if not any(d.get("itemId") == kql_db_id for d in mp.get("dataSources", [])):
        mp.setdefault("dataSources", []).append({
            "itemType": "KqlDatabase",
            "workspaceId": workspace_id,
            "itemId": kql_db_id,
        })

    # 4. Append the 8 ICON-D2 layers.
    for (name, param, unit, suf, dec, stops) in LAYERS:
        color_expr = ["interpolate", ["linear"], ["get", "value"]]
        for v, c in zip(stops[0::2], stops[1::2]):
            color_expr += [v, c]
        default_hour = _latest_first_hour(kusto_uri, kusto_db, ks, param)
        print(f"  {param:9s}: default filter = {default_hour or '(none yet)'}")

        src_id = str(uuid.uuid4())
        mp.setdefault("layerSources", []).append({
            "id": src_id, "name": f"icond2_{param}_kusto", "type": "kusto",
            "options": {"cluster": False}, "itemId": kql_db_id,
            "refreshIntervalMs": 0,
        })
        ls_filters = [{
            "id": str(uuid.uuid4()), "type": "text",
            "field": "Forecast time (UTC)", "locked": False,
            "value": [default_hour] if default_hour else [],
        }]
        mp["layerSettings"].append({
            "id": str(uuid.uuid4()), "name": name, "sourceId": src_id,
            "geometryColumnName": "geometry",
            "filters": ls_filters,
            "options": {
                "type": "vector",
                "visible": (param == DEFAULT_VISIBLE),
                "color": color_expr,
                "polygonOptions": {"fillColor": color_expr, "fillOpacity": 0.7},
                "lineOptions":    {"strokeColor": "#000000", "strokeWidth": 0},
                "dataLabelKeys":  ["label"],
                "dataLabelOptions": {
                    "enabled": True, "size": 14, "color": "#000000",
                    "textStrokeColor": "#FFFFFF", "textStrokeWidth": 2,
                    "allowOverlap": False,
                },
            },
        })
        parts[f"queries/layerSource-{src_id}.kql"] = {
            "path": f"queries/layerSource-{src_id}.kql",
            "payload": base64.b64encode(
                KQL_TEMPLATE.format(PARAM=param, DEC=dec, SUF=suf).encode()
            ).decode(),
            "payloadType": "InlineBase64",
        }

    # 5. Push the updated definition.
    parts["map.json"]["payload"] = base64.b64encode(
        json.dumps(mp, indent=2).encode()).decode()
    print(f"definition: {len(mp['layerSources'])} sources, "
          f"{len(mp['layerSettings'])} settings")
    r = fab.post(
        f"{api_base}/workspaces/{workspace_id}/items/{map_id}/updateDefinition",
        json={"definition": {"parts": list(parts.values())}})
    print(f"updateDefinition HTTP {r.status_code}")
    _poll_lro(fab, r)
    print("OK")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace-id", default=os.environ.get("FABRIC_WORKSPACE_ID"))
    ap.add_argument("--map-id",       default=os.environ.get("FABRIC_MAP_ID"))
    ap.add_argument("--kql-db-id",    default=os.environ.get("FABRIC_KQL_DB_ID"))
    ap.add_argument("--kusto-uri",    default=os.environ.get("KUSTO_CLUSTER_URI"))
    ap.add_argument("--kusto-db",     default=os.environ.get("KUSTO_DB", "dwd"))
    ap.add_argument("--api-base",     default=os.environ.get(
        "FABRIC_API_BASE", "https://api.fabric.microsoft.com/v1"))
    args = ap.parse_args(argv)

    missing = [n for n in ("workspace_id", "map_id", "kql_db_id", "kusto_uri")
               if not getattr(args, n)]
    if missing:
        ap.error(f"missing required: {', '.join('--' + m.replace('_','-') for m in missing)}")

    fabric_token = _get_token("FABRIC_TOKEN",
                              "https://api.fabric.microsoft.com/.default")
    kusto_token  = _get_token("KUSTO_TOKEN",
                              "https://kusto.fabric.microsoft.com/.default")

    wire(args.workspace_id, args.map_id, args.kql_db_id,
         args.kusto_uri, args.kusto_db,
         fabric_token, kusto_token, args.api_base)


if __name__ == "__main__":
    main()
