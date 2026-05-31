#!/usr/bin/env python3
"""Build and deploy the ENTSO-E Real-Time (KQLDashboard) item into Fabric.

Creates a 3-page Fabric Real-Time Dashboard bound to the live `entsoe` KQL
database. Every tile maps to a real table / materialized view / helper
function and a validated KQL query. Idempotent: updates the dashboard
definition in place if an item of the same display name already exists.

Auth: uses `az account get-access-token` for the Fabric API. Run `az login`
first. All infra IDs are taken from the deployed Real-Time Open Data
workspace and can be overridden via environment variables / CLI flags.
"""
from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
import time
import urllib.request
import urllib.error
import uuid

FABRIC = "https://api.fabric.microsoft.com/v1"

# --- deployed infra (Real-Time Open Data workspace) -------------------------
WORKSPACE = "c98acd97-4363-4296-8323-b6ab21e53903"
KQL_DB_ID = "a08303ed-4148-4c4d-b0fd-7ad5eb882e68"           # entsoe KQL DB item
CLUSTER_URI = "https://trd-fssgb36e98qh3fk58u.z2.kusto.fabric.microsoft.com"
DISPLAY_NAME = "ENTSO-E European Electricity Market"
DESCRIPTION = "European wholesale electricity market — day-ahead prices, generation mix, cross-border flows (ENTSO-E Transparency Platform)."

DS_ID = "11111111-1111-4111-8111-000000000001"   # dataSource id (referenced by queries)


def tok(resource: str) -> str:
    out = subprocess.run(
        ["az", "account", "get-access-token", "--resource", resource,
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True, check=True, shell=True)
    return out.stdout.strip()


def api(method: str, url: str, token: str, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        resp = urllib.request.urlopen(req)
        raw = resp.read().decode()
        return resp.status, dict(resp.headers), (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        return e.code, dict(e.headers), (json.loads(raw) if raw else {"error": raw})


def poll_lro(headers: dict, token: str):
    loc = headers.get("Location")
    if not loc:
        return None
    while True:
        time.sleep(2)
        st, _, body = api("GET", loc, token)
        if body.get("status") in ("Succeeded", "Completed"):
            s2, _, res = api("GET", loc + "/result", token)
            return res
        if body.get("status") in ("Failed", "Cancelled"):
            raise RuntimeError(f"LRO failed: {json.dumps(body)}")


# --- query/tile/param builders ---------------------------------------------
_qids: dict[str, str] = {}


def qid(name: str) -> str:
    return _qids.setdefault(name, str(uuid.uuid4()))


def Q(name: str, text: str, used=None) -> dict:
    return {
        "dataSource": {"kind": "inline", "dataSourceId": DS_ID},
        "text": text.strip() + "\n",
        "id": qid(name),
        "usedVariables": used or [],
    }


def tile(title, vtype, page, x, y, w, h, qname, opts) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "title": title,
        "visualType": vtype,
        "pageId": page,
        "layout": {"x": x, "y": y, "width": w, "height": h},
        "queryRef": {"kind": "query", "queryId": qid(qname)},
        "visualOptions": opts,
    }


def yaxes(label=""):
    return {"base": {"id": "-1", "label": label, "columns": [],
                     "yAxisMaximumValue": None, "yAxisMinimumValue": None,
                     "yAxisScale": "linear", "horizontalLines": []},
            "additional": [], "showMultiplePanels": False}


def bar_opts(xcol, ycol, label="", series=None, vtype_legend=False):
    return {"multipleYAxes": yaxes(label), "hideLegend": not vtype_legend,
            "legendLocation": "bottom", "xColumnTitle": "", "xColumn": xcol,
            "yColumns": [ycol], "seriesColumns": series, "xAxisScale": "linear",
            "verticalLine": "", "crossFilter": [], "crossFilterDisabled": False,
            "drillthroughDisabled": False, "drillthrough": []}


def pie_opts(label_col, value_col, series=None):
    return {"hideLegend": False, "legendLocation": "right", "xColumn": label_col,
            "yColumns": [value_col], "seriesColumns": series or [label_col],
            "crossFilterDisabled": False, "drillthroughDisabled": False,
            "labelDisabled": False, "pie__label": ["name", "value"],
            "tooltipDisabled": False, "pie__tooltip": ["percentage", "value", "name"],
            "pie__orderBy": "none", "pie__kind": "pie", "pie__topNSlices": None,
            "crossFilter": [], "drillthrough": []}


def multistat_opts(label_col, value_col, slot_w=3):
    return {"multiStat__textSize": "auto", "multiStat__valueColumn": value_col,
            "colorRulesDisabled": True, "colorStyle": "light",
            "multiStat__displayOrientation": "horizontal",
            "multiStat__labelColumn": label_col,
            "multiStat__slot": {"width": slot_w, "height": 1},
            "colorRules": [], "crossFilter": [], "drillthrough": [],
            "crossFilterDisabled": False, "drillthroughDisabled": False}


def table_opts():
    return {"table__enableRenderLinks": True, "colorRulesDisabled": True,
            "colorStyle": "light", "crossFilterDisabled": False,
            "drillthroughDisabled": False, "crossFilter": [], "drillthrough": [],
            "table__renderLinks": [], "colorRules": [],
            "selectedDataOnLoad": {"all": True, "limit": 30}}


def map_opts(lat, lon, label, size=None):
    return {"map__latitudeColumn": lat, "map__longitudeColumn": lon,
            "map__labelColumn": label,
            "map__sizeColumn": size, "map__sizeDisabled": size is None,
            "map__geoType": "numeric", "map__geoPointColumn": None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", default=WORKSPACE)
    ap.add_argument("--db", default=KQL_DB_ID)
    ap.add_argument("--cluster", default=CLUSTER_URI)
    ap.add_argument("--name", default=DISPLAY_NAME)
    args = ap.parse_args()

    p1 = str(uuid.uuid4())  # Prices & Market
    p2 = str(uuid.uuid4())  # Generation Mix & Renewables
    p3 = str(uuid.uuid4())  # System Balance & Cross-Border

    zone1_var = "Zone1"
    p_zone1 = str(uuid.uuid4())
    p_time = str(uuid.uuid4())

    # ---- queries -----------------------------------------------------------
    queries = [
        Q("p1_price_multistat",
          "['eu.entsoe.transparency.DayAheadPricesLatest']\n"
          "| join kind=inner (EICZone()) on $left.inDomain==$right.eic\n"
          "| project zone, price=round(price,2)\n| sort by price desc"),
        Q("p1_price_bar",
          "['eu.entsoe.transparency.DayAheadPricesLatest']\n"
          "| join kind=inner (EICZone()) on $left.inDomain==$right.eic\n"
          "| project zone, ['€/MWh']=round(price,2)\n| sort by ['€/MWh'] asc"),
        Q("p1_spread",
          "let p = ['eu.entsoe.transparency.DayAheadPricesLatest'];\n"
          "p | summarize metric='Price spread €/MWh', value=round(max(price)-min(price),2)\n"
          "| union (p | summarize metric='Highest €/MWh', value=round(max(price),2))\n"
          "| union (p | summarize metric='Lowest €/MWh', value=round(min(price),2))"),
        Q("p1_price_table",
          "['eu.entsoe.transparency.DayAheadPricesLatest']\n"
          "| join kind=inner (EICZone()) on $left.inDomain==$right.eic\n"
          "| project Zone=zone, Country=country, ['€/MWh']=round(price,2), Currency=currency, Resolution=resolution\n"
          "| sort by ['€/MWh'] desc"),
        Q("p1_price_map",
          "['eu.entsoe.transparency.DayAheadPricesLatest']\n"
          "| join kind=inner (EICZone()) on $left.inDomain==$right.eic\n"
          "| project zone, latitude=lat, longitude=lon, price=round(price,1)"),
        # page 2 (Zone1 variable)
        Q("p2_res_multistat",
          "let m = ['eu.entsoe.transparency.ActualGenerationPerTypeLatest']\n"
          f"| where inDomain == {zone1_var}\n"
          "| join kind=inner (PsrType()) on $left.psrType==$right.code\n"
          "| summarize total=sum(quantity), res=sumif(quantity,isRenewable), "
          "wind=sumif(quantity,fuel has 'Wind'), solar=sumif(quantity,fuel=='Solar');\n"
          "m | project metric='RES share %', value=round(100.0*res/total,1)\n"
          "| union (m | project metric='Wind MW', value=round(wind,0))\n"
          "| union (m | project metric='Solar MW', value=round(solar,0))\n"
          "| union (m | project metric='Total generation MW', value=round(total,0))",
          [zone1_var]),
        Q("p2_mix_donut",
          "['eu.entsoe.transparency.ActualGenerationPerTypeLatest']\n"
          f"| where inDomain == {zone1_var}\n"
          "| join kind=inner (PsrType()) on $left.psrType==$right.code\n"
          "| summarize MW=round(sum(quantity),0) by fuel\n| where MW>0\n| sort by MW desc",
          [zone1_var]),
        Q("p2_windsolar",
          "let act = ['eu.entsoe.transparency.WindSolarGenerationLatest']\n"
          f"| where inDomain == {zone1_var}\n"
          "| join kind=inner (PsrType()) on $left.psrType==$right.code\n"
          "| summarize MW=round(sum(quantity),0) by fuel | extend series='Actual';\n"
          "let fc = ['eu.entsoe.transparency.WindSolarForecastLatest']\n"
          f"| where inDomain == {zone1_var}\n"
          "| join kind=inner (PsrType()) on $left.psrType==$right.code\n"
          "| summarize MW=round(sum(quantity),0) by fuel | extend series='Forecast';\n"
          "union act, fc | project fuel, series, MW",
          [zone1_var]),
        Q("p2_gen_by_zone",
          "['eu.entsoe.transparency.ActualGenerationPerTypeLatest']\n"
          "| join kind=inner (EICZone()) on $left.inDomain==$right.eic\n"
          "| join kind=inner (PsrType()) on $left.psrType==$right.code\n"
          "| summarize MW=round(sum(quantity),0) by zone, fuel\n| where MW>0"),
        # page 3
        Q("p3_netpos",
          "let flows = ['eu.entsoe.transparency.CrossBorderPhysicalFlowsLatest'];\n"
          "let imp = flows | summarize imp=sum(quantity) by eic=inDomain;\n"
          "let exp = flows | summarize exp=sum(quantity) by eic=outDomain;\n"
          "imp | join kind=fullouter exp on eic\n"
          "| extend eic=coalesce(eic,eic1), net=coalesce(imp,0.0)-coalesce(exp,0.0)\n"
          "| join kind=inner (EICZone()) on $left.eic==$right.eic\n"
          "| project zone, ['Net position MW']=round(net,0)\n| sort by ['Net position MW'] desc"),
        Q("p3_load_bar",
          "['eu.entsoe.transparency.ActualTotalLoadLatest']\n"
          "| join kind=inner (EICZone()) on $left.inDomain==$right.eic\n"
          "| project zone, ['Load MW']=round(quantity,0)\n| sort by ['Load MW'] asc"),
        Q("p3_top_flows",
          "['eu.entsoe.transparency.CrossBorderPhysicalFlowsLatest']\n"
          "| join kind=inner (EICZone() | project ineic=eic, in_zone=zone) on $left.inDomain==$right.ineic\n"
          "| join kind=inner (EICZone() | project outeic=eic, out_zone=zone) on $left.outDomain==$right.outeic\n"
          "| extend border=strcat(out_zone,' → ',in_zone)\n"
          "| project border, ['Flow MW']=round(quantity,0)\n| top 12 by ['Flow MW']"),
        Q("p3_flow_matrix",
          "['eu.entsoe.transparency.CrossBorderPhysicalFlowsLatest']\n"
          "| join kind=inner (EICZone() | project ineic=eic, To=zone) on $left.inDomain==$right.ineic\n"
          "| join kind=inner (EICZone() | project outeic=eic, From=zone) on $left.outDomain==$right.outeic\n"
          "| project From, To, ['Flow MW']=round(quantity,0)\n| sort by ['Flow MW'] desc"),
        # parameter source
        Q("param_zone1",
          "['eu.entsoe.transparency.ActualGenerationPerTypeLatest']\n"
          "| distinct inDomain\n"
          "| join kind=inner (EICZone()) on $left.inDomain==$right.eic\n"
          "| extend ord=iff(zone=='DE-LU',0,1)\n| sort by ord asc, zone asc\n"
          "| project value=inDomain, label=zone"),
    ]

    # ---- tiles -------------------------------------------------------------
    tiles = [
        # Page 1 — Prices & Market
        tile("Day-ahead price by bidding zone (€/MWh)", "multistat", p1, 0, 0, 24, 4,
             "p1_price_multistat", multistat_opts("zone", "price", slot_w=4)),
        tile("Price ranking — cheapest → most expensive", "bar", p1, 0, 4, 8, 9,
             "p1_price_bar", bar_opts("zone", "€/MWh", "€/MWh")),
        tile("Geographic price map", "map", p1, 8, 4, 8, 9,
             "p1_price_map", map_opts("latitude", "longitude", "zone", size="price")),
        tile("Price detail by zone", "table", p1, 16, 4, 8, 9,
             "p1_price_table", table_opts()),
        tile("Price spread & extremes (congestion signal)", "multistat", p1, 0, 13, 24, 4,
             "p1_spread", multistat_opts("metric", "value", slot_w=4)),
        # Page 2 — Generation Mix & Renewables (zone = Zone1)
        tile("Renewable share & headline generation (selected zone)", "multistat", p2, 0, 0, 24, 4,
             "p2_res_multistat", multistat_opts("metric", "value", slot_w=4)),
        tile("Current fuel mix (selected zone)", "pie", p2, 0, 4, 8, 11,
             "p2_mix_donut", pie_opts("fuel", "MW")),
        tile("Wind & solar — forecast vs actual (MW)", "column", p2, 8, 4, 8, 11,
             "p2_windsolar", bar_opts("fuel", "MW", "MW", series=["series"], vtype_legend=True)),
        tile("Generation by zone & fuel (MW)", "stackedcolumn", p2, 16, 4, 8, 11,
             "p2_gen_by_zone", bar_opts("zone", "MW", "MW", series=["fuel"], vtype_legend=True)),
        # Page 3 — System Balance & Cross-Border
        tile("Net position by zone (import + / export −, MW)", "bar", p3, 0, 0, 8, 11,
             "p3_netpos", bar_opts("zone", "Net position MW", "MW")),
        tile("Actual total load by zone (MW)", "bar", p3, 8, 0, 8, 11,
             "p3_load_bar", bar_opts("zone", "Load MW", "MW")),
        tile("Top cross-border interconnector flows (MW)", "bar", p3, 16, 0, 8, 11,
             "p3_top_flows", bar_opts("border", "Flow MW", "MW")),
        tile("Cross-border flow matrix (from → to, MW)", "table", p3, 0, 11, 24, 8,
             "p3_flow_matrix", table_opts()),
    ]

    parameters = [
        {"kind": "duration", "id": p_time, "displayName": "Time range",
         "description": "", "beginVariableName": "_startTime", "endVariableName": "_endTime",
         "defaultValue": {"kind": "dynamic", "count": 1, "unit": "days"},
         "showOnPages": {"kind": "all"}},
        {"kind": "string", "id": p_zone1, "displayName": "Zone (Page 2)",
         "description": "Bidding zone for the generation-mix deep dive.",
         "variableName": zone1_var, "selectionType": "scalar",
         "includeAllOption": False, "defaultValue": {"kind": "query-result"},
         "dataSource": {"kind": "query",
                        "columns": {"value": "value", "label": "label"},
                        "queryRef": {"kind": "query", "queryId": qid("param_zone1")}},
         "showOnPages": {"kind": "all"}},
    ]

    dashboard = {
        "schema_version": 68,
        "autoRefresh": {"enabled": True, "defaultInterval": "30s", "minInterval": "30s"},
        "tiles": tiles,
        "baseQueries": [],
        "parameters": parameters,
        "dataSources": [{
            "kind": "kusto-trident", "id": DS_ID, "name": "entsoe",
            "clusterUri": args.cluster, "database": args.db,
            "workspace": "00000000-0000-0000-0000-000000000000",
            "scopeId": "kusto-trident"}],
        "pages": [
            {"name": "Prices & Market", "id": p1},
            {"name": "Generation Mix & Renewables", "id": p2},
            {"name": "System Balance & Cross-Border", "id": p3},
        ],
        "queries": queries,
    }

    platform = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "KQLDashboard", "displayName": args.name,
                     "description": DESCRIPTION},
        "config": {"version": "2.0", "logicalId": "00000000-0000-0000-0000-000000000000"},
    }

    def b64(obj):
        return base64.b64encode(json.dumps(obj).encode()).decode()

    parts = [
        {"path": "RealTimeDashboard.json", "payload": b64(dashboard), "payloadType": "InlineBase64"},
        {"path": ".platform", "payload": b64(platform), "payloadType": "InlineBase64"},
    ]

    ft = tok("https://api.fabric.microsoft.com")
    # find existing
    st, _, body = api("GET", f"{FABRIC}/workspaces/{args.workspace}/items?type=KQLDashboard", ft)
    existing = next((i for i in body.get("value", []) if i.get("displayName") == args.name), None)

    if existing:
        item_id = existing["id"]
        print(f"Updating existing KQLDashboard {item_id} …")
        st, hdr, body = api("POST",
                            f"{FABRIC}/workspaces/{args.workspace}/items/{item_id}/updateDefinition",
                            ft, {"definition": {"parts": parts}})
        if st == 202:
            poll_lro(hdr, ft)
        elif st >= 300:
            print("ERROR", st, json.dumps(body)); sys.exit(1)
    else:
        print("Creating KQLDashboard …")
        st, hdr, body = api("POST", f"{FABRIC}/workspaces/{args.workspace}/items", ft,
                            {"displayName": args.name, "type": "KQLDashboard",
                             "description": DESCRIPTION,
                             "definition": {"parts": parts}})
        if st == 202:
            res = poll_lro(hdr, ft)
            item_id = (res or {}).get("id")
        elif st in (200, 201):
            item_id = body.get("id")
        else:
            print("ERROR", st, json.dumps(body)); sys.exit(1)

    if not item_id:
        # resolve by name
        st, _, body = api("GET", f"{FABRIC}/workspaces/{args.workspace}/items?type=KQLDashboard", ft)
        item_id = next((i["id"] for i in body.get("value", []) if i.get("displayName") == args.name), None)

    url = f"https://app.fabric.microsoft.com/groups/{args.workspace}/kustodashboards/{item_id}"
    print(f"\nOK  KQLDashboard ready")
    print(f"    id : {item_id}")
    print(f"    url: {url}")


if __name__ == "__main__":
    main()
